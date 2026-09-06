#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Mint a spec-blind MEMORY CHECKPOINT in one grounded pass.

Feeds the clean prose of chapters 1..N to a big-context model (default Sol via
codex subscription auth) with the blind-extractor rules as the system prompt,
and writes the returned checkpoint. Single grounded pass — no chaining, no
carry-forward hops — so nothing decays across a summarize-of-a-summary chain.
The prose is injected as the message body (NOT via the Read tool, which caps at
25k tokens); subscription-backed models run in an isolated empty cwd, so they
never load meta/ or project instructions.

Usage:
  tools/checkpoint_extract.py                       # ck through ch50 (all of Vol 1), sol
  tools/checkpoint_extract.py --to 20               # ck through ch20
  tools/checkpoint_extract.py --model gpt-5.6-sol --to 50
Output: reviews/cold-read/<model-id>/checkpoints/ck-ch<NNN>.md
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import re
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import cold_read  # noqa: E402  (reuses make_codex_agent_fn, load_agent_prompt)
import cold_read_config  # noqa: E402

AGENT_DEF = REPO / ".claude/agents/blind-extractor.md"


def make_claude_extractor_fn(system_prompt: str, effort: str):
    """Headless clean-lane Claude checkpoint extraction on subscription OAuth."""

    def run(*, prompt: str, model: str, label: str):
        env = dict(os.environ)
        env.pop("ANTHROPIC_API_KEY", None)
        detail = ""
        for attempt in range(5):
            with tempfile.TemporaryDirectory(prefix="checkpoint-extract-") as td:
                prompt_path = Path(td) / "system-prompt.md"
                prompt_path.write_text(system_prompt, encoding="utf-8")
                result = subprocess.run(
                    [
                        "claude",
                        "-p",
                        "--model",
                        model,
                        "--system-prompt-file",
                        str(prompt_path),
                        "--exclude-dynamic-system-prompt-sections",
                        "--effort",
                        effort,
                    ],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    cwd=td,
                    env=env,
                    timeout=2400,
                )
            if result.returncode == 0:
                return {"output": result.stdout, "usage": {}, "id": label}
            detail = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()[-600:]
            transient = any(
                marker in detail
                for marker in ("529", "verloaded", "rate limit", "rate_limit", " 500", " 502", " 503", "imeout")
            )
            if not transient:
                break
            if attempt < 4:
                time.sleep(10 * (attempt + 1))
        raise RuntimeError(f"claude -p checkpoint extraction failed: {detail}")

    return run

def normalize_section_headings(text: str, headings: tuple[str, ...]) -> str:
    """Normalize an extractor's bold section labels to the required H3 form."""
    for heading in headings:
        text = re.sub(
            rf"(?m)^\*\*{re.escape(heading)}\*\*\s*$",
            f"### {heading}",
            text,
        )
    return text



def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="gpt-5.6-sol", help="reader/extractor model id")
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=None)
    ap.add_argument(
        "--reader-sequence",
        action="store_true",
        help="use the full drafted cross-volume reader sequence; required for boundaries past Volume 1",
    )
    ap.add_argument("--effort", default="high", choices=["none", "low", "medium", "high"])
    ap.add_argument("--max-output-tokens", type=int, default=80000,
                    help="output-token cap for OpenRouter checkpoint extraction (default 80000)")
    ap.add_argument("--out", default=None, help="override output path")
    ap.add_argument(
        "--salvage-output",
        type=Path,
        default=None,
        help="validate and persist a previously archived raw model output without another call",
    )
    args = ap.parse_args()

    if not cold_read_config.can_mint_checkpoint(args.model):
        source = cold_read_config.checkpoint_source(args.model)
        raise SystemExit(
            f"{args.model} is a donor-memory reader ({source}); native checkpoint minting is disabled"
        )

    if args.reader_sequence:
        if args.start != 1 or args.end is None:
            raise SystemExit("--reader-sequence requires --from 1 and an explicit --to boundary")
        end = args.end
        bundle = checkpoint_bundle.build_reader_bundle(end)
    else:
        bundle = checkpoint_bundle.build_bundle(args.start, args.end, jacket=True)
        end = args.end if args.end is not None else len(
            checkpoint_bundle.volume_scenes.volume_one_slugs(drafted_only=True))
    approx_tok = int(len(bundle.split()) * 1.35)
    print(f"[bundle] chapters {args.start}..{end}  ~{approx_tok:,} tokens", file=sys.stderr)

    system_prompt = cold_read.load_agent_prompt(AGENT_DEF)
    fingerprints = checkpoint_bundle.source_fingerprints(bundle, system_prompt)
    user_prompt = (
        "The message below is the book's public jacket followed by the full clean "
        "text of Chapters " + f"{args.start} through {end}, in story order, each under a "
        "`===== CHAPTER n: Title =====` delimiter. This is the entire book so far; there "
        "is no prior checkpoint (build the memory from the opening, cold). The text is "
        "pasted inline — do not attempt to read any file. Consolidate it into ONE "
        "cumulative checkpoint per your instructions, losing nothing that matters, and "
        "return exactly the specified sections.\n\n" + bundle
    )
    t0 = time.time()
    if args.salvage_output is not None:
        result = {
            "output": args.salvage_output.read_text(encoding="utf-8"),
            "usage": {},
            "id": f"salvage-{args.salvage_output.name}",
        }
        print(f"[salvage] validating {args.salvage_output}", file=sys.stderr)
    else:
        if args.model.startswith("claude-"):
            print(f"[auth] claude subscription OAuth · {args.model}", file=sys.stderr)
            agent_fn = make_claude_extractor_fn(system_prompt, args.effort)
            close = lambda: None
        elif "/" in args.model:   # OpenRouter model (provider/model), e.g. moonshotai/kimi-k3
            key = os.environ.get("OPENROUTER_API_KEY")
            if not key:
                raise SystemExit("OpenRouter model needs OPENROUTER_API_KEY set in the environment")
            print(f"[auth] openrouter — billing PER TOKEN (author-authorized) · {args.model}",
                  file=sys.stderr)
            agent_fn = cold_read.make_openrouter_agent_fn(
                system_prompt=system_prompt, effort=args.effort, timeout=2400,
                max_output_tokens=args.max_output_tokens, api_key=key)
            close = (lambda: None)
        else:
            agent_fn, close = cold_read.make_codex_agent_fn(
                system_prompt=system_prompt, effort=args.effort
            )
        try:
            print(f"[run] {args.model} effort={args.effort} …", file=sys.stderr)
            result = agent_fn(prompt=user_prompt, model=args.model, label=f"ck-ch{end:03d}")
        finally:
            close()

    text = (result.get("output") or "").strip()
    # Strip the extractor's `tool_uses:` acknowledgment line if it led the reply.
    if text.lower().startswith("tool_uses:"):
        text = text.split("\n", 1)[1].lstrip() if "\n" in text else ""
    usage = result.get("usage") or {}
    required_headings = (
        "Who's who",
        "Relationships",
        "What I know that they don't",
        "Motifs & images",
        "Symbolism",
        "Open questions",
        "Story so far",
        "Impression",
    )
    text = normalize_section_headings(text, required_headings)
    heading_positions = [text.find(f"### {heading}") for heading in required_headings]
    missing_headings = [
        heading for heading, position in zip(required_headings, heading_positions)
        if position < 0
    ]
    problems = []
    if not text:
        problems.append("empty checkpoint")
    if usage.get("incomplete"):
        problems.append("provider reported incomplete output")
    finish_reason = usage.get("finishReason")
    if finish_reason not in (None, "stop"):
        problems.append(f"provider finish reason: {finish_reason}")
    if missing_headings:
        problems.append("missing headings: " + ", ".join(missing_headings))
    if not missing_headings and heading_positions != sorted(heading_positions):
        problems.append("required headings are out of order")
    if problems:
        failure_dir = Path("/tmp/ramdisk")
        failure_dir.mkdir(parents=True, exist_ok=True)
        safe_model = args.model.replace("/", "_")
        stem = f"checkpoint-failure-{safe_model}-ch{end:03d}-{int(time.time())}"
        failure_path = failure_dir / f"{stem}.json"
        output_path = failure_dir / f"{stem}.md"
        failure_path.write_text(json.dumps({
            "model": args.model,
            "chapter": end,
            "response_id": result.get("id"),
            "usage": usage,
            "problems": problems,
            "output_path": str(output_path) if text else None,
        }, indent=2, default=str) + "\n")
        if text:
            output_path.write_text(text + "\n")
        raise SystemExit(
            f"invalid checkpoint returned; diagnostics={failure_path}; "
            + "; ".join(problems)
        )

    out_path = Path(args.out) if args.out else (
        REPO / f"reviews/cold-read/{args.model}/checkpoints/ck-ch{end:03d}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Checkpoint — through Chapter {end} (grounded, single pass)\n\n"
        f"*model: {args.model} · span: ch{args.start:03d}–ch{end:03d} · "
        f"source-sha256: {fingerprints['source_sha256']} · "
        f"bundle-sha256: {fingerprints['bundle_sha256']} · "
        f"cleaner-version: {fingerprints['cleaner_version']} · "
        f"extractor-sha256: {fingerprints['extractor_sha256']} · "
        f"grounded (full clean prose, no chaining)*\n\n---\n\n"
    )
    out_path.write_text(header + text + "\n")
    try:
        disp = out_path.relative_to(REPO)
    except ValueError:                          # --out given as a path outside REPO
        disp = out_path
    print(
        f"[done] {disp}  "
        f"in={usage.get('input')} out={usage.get('output')} "
        f"reasoning={usage.get('reasoningTokens')} {time.time()-t0:.0f}s "
        f"incomplete={usage.get('incomplete')}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
