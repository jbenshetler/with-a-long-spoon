#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Blind authorship-signal audit — per-chapter perceived-author-gender probe.

Contract: reviews/authorship-audit/SPEC.md (prompts versioned in
reviews/authorship-audit/prompts/ — their SHA is recorded in every output
header). Each read sees ONLY the chapter title + cleaned prose; no memory, no
jacket, no carry-forward — reads are independent and fan out.

Lanes mirror the grounded cold-read harness (tools/cold_read_grounded.py):
Claude models via headless `claude -p` (persona = ENTIRE system prompt,
throwaway non-repo cwd, subscription OAuth, ANTHROPIC_API_KEY scrubbed); GPT
models via codex subscription auth (empty cwd, read-only sandbox).

Usage:
  tools/authorship_audit.py --pilot                 # SPEC pilot slate, 48 reads
  tools/authorship_audit.py --slugs the-bench --models claude-opus-4-8
  tools/authorship_audit.py --pilot --framings adversarial
  tools/authorship_audit.py --pilot --dry-run       # list planned reads
Existing outputs are skipped unless --force.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess as sp
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402  (clean_scene_text, display_title)

AUDIT_ROOT = REPO / "reviews" / "authorship-audit"
PROTOCOL = "authorship-audit-v1-pilot"
# adversarial retained as a prompt file but dropped from runs (SPEC, 2026-09-07)
FRAMINGS = ("neutral", "adversarial", "repair")
CLAUDE_PREFIX = "claude-"

PILOT_SLUGS = ["the-bench", "a-round", "nothing-underneath",
               "water-wings", "one-bite", "two-towels"]
PILOT_MODELS = ["claude-fable-5", "claude-opus-4-8", "gpt-5.6-sol", "gpt-5.5"]
# OpenRouter lane — pay-per-token, author authorization required (token rule).
OPENROUTER_MODELS = {
    "kimi-k3": "moonshotai/kimi-k3",
    "glm-5.3-flash": "z-ai/glm-5.3-flash",
    "qwen3.8-max-0902": "qwen/qwen3.8-max-0902",
    "deepseek-v4-pro-0813": "deepseek/deepseek-v4-pro-0813",
}
PANEL_MODELS = PILOT_MODELS + list(OPENROUTER_MODELS)


def load_persona(framing: str) -> tuple[str, str]:
    """Prompt text + short SHA, from the versioned prompt file."""
    p = AUDIT_ROOT / "prompts" / f"{framing}.md"
    text = p.read_text(encoding="utf-8")
    return text, hashlib.sha256(text.encode()).hexdigest()[:12]


def build_user_prompt(slug: str, framing: str = "neutral") -> str:
    title = checkpoint_bundle.display_title(slug)
    body = checkpoint_bundle.clean_scene_text(slug)
    prompt = f"===== CHAPTER: {title} =====\n\n{body}\n\n===== END OF CHAPTER =====\n\n"
    if framing == "repair":
        fl = AUDIT_ROOT / "fixlists" / f"{slug}.md"
        if not fl.exists():
            raise RuntimeError(f"repair framing needs {fl.relative_to(REPO)}")
        prompt += (f"===== FLAGGED PASSAGES =====\n\n{fl.read_text(encoding='utf-8')}\n\n"
                   "===== END OF FLAGGED PASSAGES =====\n\n"
                   "Produce your repair options now, following your instructions exactly.")
    else:
        prompt += "Produce your audit now, following your instructions exactly."
    return prompt


def out_path(model_id: str, slug: str, framing: str) -> Path:
    return AUDIT_ROOT / model_id / f"{slug}--{framing}.md"


def write_output(model_id: str, slug: str, framing: str, sha: str, text: str) -> Path:
    out = out_path(model_id, slug, framing)
    out.parent.mkdir(parents=True, exist_ok=True)
    title = checkpoint_bundle.display_title(slug)
    out.write_text(
        f"# Authorship audit ({framing}) — {title}\n\n"
        f"*scene: scenes/{slug}.md · model: {model_id} · framing: {framing} · "
        f"protocol: {PROTOCOL} · prompt-sha: {sha} · run: {date.today().isoformat()}*\n\n"
        f"{text.strip()}\n",
        encoding="utf-8")
    return out


def validate(framing: str, text: str, label: str) -> str:
    t = text.strip()
    if len(t) < 400:
        raise RuntimeError(f"suspiciously short audit for {label} ({len(t)} chars)")
    need = {"neutral": "SCORE:", "adversarial": "Verdict",
            "repair": "DIAGNOSIS"}[framing]
    if need not in t:
        raise RuntimeError(f"malformed {framing} audit for {label}: missing {need!r}")
    return t


def run_claude(model: str, system_prompt: str, prompt: str, label: str) -> str:
    """Clean-lane headless `claude -p` — mirrors cold_read_grounded.run_claude_headless
    (subscription OAuth only; ANTHROPIC_API_KEY scrubbed per the token rule)."""
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)
    detail = ""
    for attempt in range(5):
        with tempfile.TemporaryDirectory(prefix="authaudit-") as td:
            spf = Path(td) / "system-prompt.md"
            spf.write_text(system_prompt, encoding="utf-8")
            cmd = ["claude", "-p", "--model", model,
                   "--system-prompt-file", str(spf),
                   "--exclude-dynamic-system-prompt-sections"]
            r = sp.run(cmd, input=prompt, capture_output=True, text=True,
                       env=env, cwd=td, timeout=2400)
        if r.returncode == 0:
            return r.stdout
        detail = ((r.stdout or "").strip() + "\n" + (r.stderr or "").strip()).strip()[-600:]
        transient = any(s in detail for s in ("529", "verloaded", "rate limit",
                                              "rate_limit", " 500", " 502", " 503", "imeout"))
        if not transient:
            raise RuntimeError(f"claude -p failed for {label}: {detail}")
        time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"claude -p failed for {label} (transient, 5 attempts): {detail}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pilot", action="store_true", help="run the SPEC pilot slate")
    ap.add_argument("--vol1", action="store_true", help="all Volume 1 drafted chapters")
    ap.add_argument("--panel", action="store_true",
                    help="full 8-model panel (includes paid OpenRouter models — "
                         "author authorization required per the token rule)")
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--models", nargs="*", default=None)
    ap.add_argument("--framings", nargs="*", default=["neutral"],
                    choices=list(FRAMINGS))
    ap.add_argument("--effort", default="low", help="codex reasoning effort")
    ap.add_argument("--jobs", type=int, default=2, help="parallel claude-lane reads")
    ap.add_argument("--force", action="store_true", help="redo existing outputs")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    slugs = args.slugs or (checkpoint_bundle.reader_slugs()[:50] if args.vol1
                           else PILOT_SLUGS if args.pilot else None)
    models = args.models or (PANEL_MODELS if args.panel
                             else PILOT_MODELS if args.pilot else None)
    if not slugs or not models:
        ap.error("give --pilot / --vol1 / --panel, or --slugs and --models")
    for s in slugs:
        if not (REPO / f"scenes/{s}.md").exists():
            ap.error(f"no such scene: {s}")

    personas = {f: load_persona(f) for f in args.framings}
    tasks = [(m, s, f) for m in models for s in slugs for f in args.framings
             if args.force or not out_path(m, s, f).exists()]
    skipped = len(models) * len(slugs) * len(args.framings) - len(tasks)
    print(f"planned: {len(tasks)} reads ({skipped} already on disk)", flush=True)
    if args.dry_run:
        for m, s, f in tasks:
            print(f"  {m} · {s} · {f}")
        return

    failures: list[str] = []

    def one_claude(m: str, s: str, f: str) -> None:
        label = f"{m}·{s}·{f}"
        try:
            text, sha = personas[f]
            raw = run_claude(m, text, build_user_prompt(s, f), label)
            write_output(m, s, f, sha, validate(f, raw, label))
            print(f"  done {label}", flush=True)
        except Exception as e:  # noqa: BLE001 — collect, report at end
            failures.append(f"{label}: {e}")
            print(f"  FAIL {label}: {e}", flush=True)

    def run_task(fn, model_arg: str, m: str, s: str, f: str, sha: str) -> None:
        label = f"{m}·{s}·{f}"
        last: Exception | None = None
        for attempt in range(2):
            try:
                result = fn(prompt=build_user_prompt(s, f), model=model_arg,
                            label=f"audit-{s}-{f}")
                raw = result.get("output") or ""
                write_output(m, s, f, sha, validate(f, raw, label))
                print(f"  done {label}", flush=True)
                return
            except Exception as e:  # noqa: BLE001 — retry once, then record
                last = e
                time.sleep(15)
        failures.append(f"{label}: {last}")
        print(f"  FAIL {label}: {last}", flush=True)

    def codex_lane(codex_models: list[str]) -> None:
        import cold_read  # noqa: E402
        for f in args.framings:
            text, sha = personas[f]
            fn, close = cold_read.make_codex_agent_fn(system_prompt=text,
                                                      effort=args.effort)
            try:
                sub = [(m, s) for m in codex_models for s in slugs
                       if (m, s, f) in task_set]
                with ThreadPoolExecutor(max_workers=2) as p:
                    list(p.map(lambda t: run_task(fn, t[0], t[0], t[1], f, sha), sub))
            finally:
                close()

    def openrouter_lane(or_models: list[str]) -> None:
        import cold_read  # noqa: E402
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OpenRouter models need OPENROUTER_API_KEY "
                               "(paid lane — author authorization required)")
        print("[auth] openrouter lane — billing PER TOKEN (author-authorized)", flush=True)
        for f in args.framings:
            text, sha = personas[f]
            fn = cold_read.make_openrouter_agent_fn(
                system_prompt=text, effort=args.effort, timeout=2400,
                max_output_tokens=8000, api_key=key)
            sub = [(m, s) for m in or_models for s in slugs if (m, s, f) in task_set]
            with ThreadPoolExecutor(max_workers=4) as p:
                list(p.map(lambda t: run_task(fn, OPENROUTER_MODELS[t[0]],
                                              t[0], t[1], f, sha), sub))

    task_set = set(tasks)
    claude_tasks = [t for t in tasks if t[0].startswith(CLAUDE_PREFIX)]
    or_models = [m for m in models if m in OPENROUTER_MODELS]
    codex_models = [m for m in models
                    if not m.startswith(CLAUDE_PREFIX) and m not in OPENROUTER_MODELS]
    with ThreadPoolExecutor(max_workers=args.jobs + 2) as pool:
        futs = []
        if codex_models:
            futs.append(pool.submit(codex_lane, codex_models))
        if or_models:
            futs.append(pool.submit(openrouter_lane, or_models))
        futs += [pool.submit(one_claude, *t) for t in claude_tasks]
        for fut in futs:
            fut.result()

    print(f"\nfinished: {len(tasks) - len(failures)}/{len(tasks)} ok", flush=True)
    if failures:
        print("failures:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
