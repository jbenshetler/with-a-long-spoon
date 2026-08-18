#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Mint a spec-blind MEMORY CHECKPOINT in one grounded pass.

Feeds the clean prose of chapters 1..N to a big-context model (default terra
via codex subscription auth) with the blind-extractor rules as the system
prompt, and writes the returned checkpoint. Single grounded pass — no chaining,
no carry-forward hops — so nothing decays across a summarize-of-a-summary chain.
The prose is injected as the message body (NOT via the Read tool, which caps at
25k tokens); terra runs in codex's read-only, empty-cwd sandbox, so it never
loads meta/ or CLAUDE.md — it is blind by construction.

Usage:
  tools/checkpoint_extract.py                       # ck through ch50 (all of Vol 1), terra
  tools/checkpoint_extract.py --to 20               # ck through ch20
  tools/checkpoint_extract.py --model gpt-5.6-sol --to 50
Output: checkpoints/<model-id>/ck-ch<NNN>.md
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import cold_read  # noqa: E402  (reuses make_codex_agent_fn, load_agent_prompt)

AGENT_DEF = REPO / ".claude/agents/blind-extractor.md"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="gpt-5.6-terra", help="codex model id")
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=None)
    ap.add_argument("--effort", default="high", choices=["none", "low", "medium", "high"])
    ap.add_argument("--out", default=None, help="override output path")
    args = ap.parse_args()

    bundle = checkpoint_bundle.build_bundle(args.start, args.end, jacket=True)
    end = args.end if args.end is not None else len(
        checkpoint_bundle.volume_scenes.volume_one_slugs(drafted_only=True))
    approx_tok = int(len(bundle.split()) * 1.35)
    print(f"[bundle] chapters {args.start}..{end}  ~{approx_tok:,} tokens", file=sys.stderr)

    system_prompt = cold_read.load_agent_prompt(AGENT_DEF)
    user_prompt = (
        "The message below is the book's public jacket followed by the full clean "
        "text of Chapters " + f"{args.start} through {end}, in story order, each under a "
        "`===== CHAPTER n: Title =====` delimiter. This is the entire book so far; there "
        "is no prior checkpoint (build the memory from the opening, cold). The text is "
        "pasted inline — do not attempt to read any file. Consolidate it into ONE "
        "cumulative checkpoint per your instructions, losing nothing that matters, and "
        "return exactly the specified sections.\n\n" + bundle
    )

    agent_fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=args.effort)
    try:
        print(f"[run] {args.model} effort={args.effort} …", file=sys.stderr)
        t0 = time.time()
        result = agent_fn(prompt=user_prompt, model=args.model, label=f"ck-ch{end:03d}")
    finally:
        close()

    text = (result.get("output") or "").strip()
    # Strip the extractor's `tool_uses:` acknowledgment line if it led the reply.
    if text.lower().startswith("tool_uses:"):
        text = text.split("\n", 1)[1].lstrip() if "\n" in text else ""
    usage = result.get("usage") or {}
    if not text:
        raise SystemExit("empty checkpoint returned")

    out_path = Path(args.out) if args.out else (
        REPO / f"checkpoints/{args.model}/ck-ch{end:03d}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Checkpoint — through Chapter {end} (grounded, single pass)\n\n"
        f"*model: {args.model} · span: ch{args.start:03d}–ch{end:03d} · "
        f"grounded (full clean prose, no chaining)*\n\n---\n\n"
    )
    out_path.write_text(header + text + "\n")
    print(
        f"[done] {out_path.relative_to(REPO)}  "
        f"in={usage.get('input')} out={usage.get('output')} "
        f"reasoning={usage.get('reasoningTokens')} {time.time()-t0:.0f}s "
        f"incomplete={usage.get('incomplete')}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
