#!/usr/bin/env python3
"""Stage oracle on the grounded reader: pause a blind first reader after chapter N and
ask it questions.

The reader at stage N holds exactly the memory the grounded cold reader would carry
out of chapter N:

    the jacket of the volume N belongs to   (reviews/cold-read/volume-packets.toml)
  + its own checkpoint ck-ch<B>, B = the last decade boundary <= N
  + the raw prose of chapters B+1..N, as the book ships them

Every chapter in the raw window is headed with its title AND its reader-facing date
line (chapter_dates: weekday, month, day; never the year), and carries its section
date lines in the body. The persona is .claude/agents/blind-oracle.md, used as the
ENTIRE system prompt: Claude ids run headless `claude -p` on subscription OAuth from a
throwaway cwd with no tools at all (`--tools ""`), gpt-* ids on codex subscription. Paid
(OpenRouter) readers are refused.

Funnel: neutral and pointed are separate, independent calls; the pointed call never
sees the neutral answer. Output: reviews/cold-read/<model-id>/oracle/<stage-slug>--<probe>--<tier>.md.
Read-only on the book; writes nothing but those answer files.

  tools/cold_read_oracle_stage.py --model claude-opus-5-5 --stage tannin --probes randi-love
  tools/cold_read_oracle_stage.py --model gpt-5.6-sol --stage 25 --ask "neutral? || pointed?" --label x
  tools/cold_read_oracle_stage.py --model claude-opus-5-5 --stage tannin --show-prompt
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess as sp
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import chapter_dates  # noqa: E402
import cold_read_config  # noqa: E402
import cold_read_grounded as g  # noqa: E402

PERSONA = REPO / ".claude/agents/blind-oracle.md"


def resolve_stage(stage: str) -> tuple[int, str]:
    slugs = g.reader_slugs()
    if stage.isdigit():
        n = int(stage)
        if not 1 <= n <= len(slugs):
            raise SystemExit(f"stage {n} out of range 1..{len(slugs)}")
        return n, slugs[n - 1]
    if stage not in slugs:
        raise SystemExit(f"unknown or undrafted stage slug {stage!r}")
    return slugs.index(stage) + 1, stage


def stage_boundary(n: int, decade: int) -> int:
    """Last decade checkpoint at or before chapter n: the reader has finished n."""
    return (n // decade) * decade


def chapter_block(slug: str) -> str:
    """Title + date in the header line; the body with its section date lines."""
    title = checkpoint_bundle.display_title(slug)
    when = chapter_dates.heading(slug)
    head = f"===== {title} · {when} =====" if when else f"===== {title} ====="
    body = chapter_dates.dated_text(slug, checkpoint_bundle.clean_scene_text(slug))
    return f"{head}\n\n{body.strip()}"


def memory_line(model_id: str, n: int, decade: int) -> str:
    b = stage_boundary(n, decade)
    src = cold_read_config.checkpoint_provenance(model_id, b) if b > 0 else ""
    if b > 0 and b < n:
        return f"{src} + raw ch{b + 1:03d}..ch{n:03d}"
    if b > 0:
        return f"{src} (no window)"
    return f"raw ch001..ch{n:03d} (pre-first-checkpoint)"


def build_prompt(model_id: str, n: int, decade: int, question: str) -> str:
    slugs = g.reader_slugs()
    slug = slugs[n - 1]
    volume = checkpoint_bundle.volume_scenes.volume_of(slug)
    _, packet = checkpoint_bundle.volume_packet(volume)
    if not packet:
        raise SystemExit(f"volume {volume} has no packet in volume-packets.toml")
    b = stage_boundary(n, decade)
    checkpoint = g.load_checkpoint(model_id, b)
    parts = ["===== THE COVER AND JACKET YOU SAW PICKING THE BOOK UP (marketing, not story) =====\n\n"
             + packet]
    if checkpoint:
        parts.append("===== YOUR MEMORY OF THE EARLIER CHAPTERS (you cannot re-read them; "
                     "treat it as your own recollection) =====\n\n" + checkpoint)
    window = [chapter_block(s) for s in slugs[b:n]]
    if window:
        parts.append("===== THE CHAPTERS YOU HAVE JUST READ (fresh in your mind, in order; "
                     "the last one is where you paused) =====\n\n" + "\n\n\n".join(window))
    parts.append("===== THE QUESTION (answer from what you have read above; return ONLY "
                 "your answer) =====\n\n" + question.strip())
    return "\n\n\n".join(parts) + "\n"


def questions(args) -> list[tuple[str, str, str]]:
    """[(probe-key, tier, question)]"""
    out = []
    if args.ask:
        neutral, _, pointed = args.ask.partition("||")
        label = args.label or "adhoc"
        out.append((f"adhoc-{label}", "neutral", neutral.strip()))
        if pointed.strip():
            out.append((f"adhoc-{label}", "pointed", pointed.strip()))
        return out
    probes = [p.strip() for p in args.probes.split(",")] if args.probes else g.all_probes()
    for p in probes:
        for t in ("neutral", "pointed"):
            out.append((p, t, g._probe_question(p, t)))
    return out


def ask_claude(model: str, system_prompt: str, prompt: str) -> str:
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)  # subscription OAuth only (token rule)
    detail = ""
    for attempt in range(5):
        with tempfile.TemporaryDirectory(prefix="oracle-") as td:
            spf = Path(td) / "system-prompt.md"
            spf.write_text(system_prompt, encoding="utf-8")
            r = sp.run(["claude", "-p", "--model", model, "--system-prompt-file", str(spf),
                        "--exclude-dynamic-system-prompt-sections", "--tools", ""],
                       input=prompt, capture_output=True, text=True, env=env, cwd=td,
                       timeout=2400)
        if r.returncode == 0:
            return r.stdout
        detail = ((r.stdout or "") + "\n" + (r.stderr or "")).strip()[-600:]
        if not any(s in detail for s in ("529", "verloaded", "rate limit", "rate_limit",
                                         " 500", " 502", " 503", "imeout")):
            break
        time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"claude -p failed: {detail}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="reader id (claude-* or gpt-*)")
    ap.add_argument("--model-id", default=None, help="reader dir / checkpoint owner (default: --model)")
    ap.add_argument("--stage", required=True, help="chapter slug or reader-sequence number")
    ap.add_argument("--probes", default=None, help="comma-separated battery keys (default: all)")
    ap.add_argument("--ask", default=None, help='ad-hoc "neutral || pointed"')
    ap.add_argument("--label", default=None, help="name for an --ask probe")
    ap.add_argument("--decade", type=int, default=10)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--fresh", action="store_true", help="overwrite existing answers")
    ap.add_argument("--allow-stale-checkpoint", action="store_true",
                    help="run on a checkpoint older than the chapters it summarizes; only when the "
                    "author has said so for this run (recorded in each answer header)")
    ap.add_argument("--show-prompt", action="store_true", help="print the first prompt and exit (free)")
    args = ap.parse_args()

    model_id = args.model_id or args.model
    if cold_read_config.is_openrouter(args.model) or cold_read_config.is_openrouter(model_id):
        raise SystemExit("paid (OpenRouter) readers are not supported by the stage oracle")
    if not (args.model.startswith("claude-") or args.model.startswith("gpt-")):
        raise SystemExit("stage oracle runs claude-* (headless) or gpt-* (codex) readers only")
    n, slug = resolve_stage(args.stage)
    qs = questions(args)
    b = stage_boundary(n, args.decade)
    g.ALLOW_STALE_CHECKPOINT = args.allow_stale_checkpoint
    if b > 0 and not cold_read_config.checkpoint_path(model_id, b).exists():
        g.load_checkpoint(model_id, b)  # raises with the mint command
    stale = g.checkpoint_staleness(model_id, b)
    if stale and not args.allow_stale_checkpoint:
        raise SystemExit(f"refusing: stale checkpoint. {stale}.\nRemint it, or pass "
                         "--allow-stale-checkpoint only if the author has approved this run.")
    if stale:
        print(f"[oracle-stage] WARNING: stale checkpoint allowed: {stale}", file=sys.stderr)
    system_prompt = g.load_agent_prompt(PERSONA)

    if args.show_prompt:
        p = build_prompt(model_id, n, args.decade, qs[0][2])
        print(p)
        print(f"\n[{len(p):,} chars · memory: {memory_line(model_id, n, args.decade)}]", file=sys.stderr)
        return

    outdir = REPO / f"reviews/cold-read/{model_id}/oracle"
    todo = [(p, t, q) for (p, t, q) in qs
            if args.fresh or not (outdir / f"{slug}--{p}--{t}.md").exists()]
    if not todo:
        print("[oracle-stage] nothing to do", file=sys.stderr)
        return

    codex_pool, closes = None, []
    if args.model.startswith("gpt-"):
        import cold_read
        from queue import Queue
        codex_pool = Queue()
        for _ in range(max(1, min(args.jobs, len(todo)))):
            fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=args.effort)
            closes.append(close)
            codex_pool.put(fn)

    mem = memory_line(model_id, n, args.decade)

    def one(probe: str, tier: str, question: str) -> Path:
        prompt = build_prompt(model_id, n, args.decade, question)
        if codex_pool is None:
            ans = ask_claude(args.model, system_prompt, prompt)
        else:
            fn = codex_pool.get()
            try:
                ans = fn(prompt=prompt, model=args.model, label=f"oracle-{slug}-{probe}-{tier}").get("output") or ""
            finally:
                codex_pool.put(fn)
        ans = g.strip_leading_heading(ans)
        if len(ans) < 120:
            raise RuntimeError(f"short answer ({len(ans)} chars)")
        out = outdir / f"{slug}--{probe}--{tier}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            f"# Oracle (stage) — {slug} · {probe} · {tier}\n\n"
            f"*model: {model_id} · stage: {slug} (ch {n}) · memory: jacket (vol "
            f"{checkpoint_bundle.volume_scenes.volume_of(slug)}) + {mem}{' (STALE, allowed)' if stale else ''} · dated chapter headers · "
            f"persona: blind-oracle*\n\n**Question asked (verbatim):** {question}\n\n---\n\n{ans.strip()}\n",
            encoding="utf-8")
        return out

    print(f"[oracle-stage] {model_id} @ {slug} (ch {n}) · {len(todo)} answers · memory: {mem}", file=sys.stderr)
    errors = 0
    try:
        with ThreadPoolExecutor(max_workers=max(1, min(args.jobs, len(todo)))) as ex:
            futs = {ex.submit(one, *t): t for t in todo}
            for f in as_completed(futs):
                p, t, _ = futs[f]
                try:
                    print(f"[done] {f.result().relative_to(REPO)}", file=sys.stderr)
                except Exception as e:  # noqa: BLE001
                    errors += 1
                    print(f"[FAIL] {p}--{t}: {type(e).__name__}: {e}", file=sys.stderr)
    finally:
        if codex_pool is not None:
            for c in closes:
                c()
    if errors:
        raise SystemExit(f"{errors} answer(s) failed")


if __name__ == "__main__":
    main()
