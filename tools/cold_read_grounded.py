#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Grounded cold read — the chain-free reader instrument (Job 2).

The chained instrument (tools/cold_read.py) feeds chapter N the *carry-forward
of chapter N-1* — a paraphrase-of-a-paraphrase up to ~50 hops deep, across which
hard facts decay (whether Vee and Pace have slept together; who "the brunette"
is). This harness removes the chain entirely. Each chapter is read with GROUNDED
memory:

    boundary  B = ((N-1)//decade)*decade          # last decade checkpoint < N
    memory      = grounded checkpoint ck-ch{B}     # from raw prose 1..B, one pass
                + raw prose of chapters B+1..N-1    # the window since the boundary
    this        = chapter N

Zero paraphrase hops: the checkpoint is minted grounded (checkpoint_extract.py,
full clean prose in one pass — no chaining) and the window is real prose, not a
summary. Because chapter N's memory is reconstructed from ground truth rather
than from reader N-1, the reads are mutually independent and can fan out.

The reader (.claude/agents/blind-reader-grounded.md) emits ONLY a Reader
reaction — no carry-forward — since memory is external now. Output lands under
reviews/cold-read/<model-id>/grounded/<slug>.md, leaving the chained reviews
(and cold_read.py / blind-reader.md) untouched.

Usage:
  tools/cold_read_grounded.py --to 50                     # all Vol 1, terra
  tools/cold_read_grounded.py --from 41 --to 50           # chapters 41..50
  tools/cold_read_grounded.py --scope nothing-underneath  # one chapter by slug
  tools/cold_read_grounded.py --model gpt-5.6-sol --to 50
  tools/cold_read_grounded.py --emit-prompt 50            # print chapter 50's
      # fully-assembled prompt to stdout (to drive a Claude blind-reader-grounded
      # subagent by hand — Claude readers consume no API tokens)
  tools/cold_read_grounded.py --check --to 50             # list needed checkpoints

Checkpoints must already exist (mint them with checkpoint_extract.py, which runs
at high effort). This harness runs the READER at low effort and refuses rather
than mint implicitly — the two are different jobs on different budgets.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402  (clean_scene_text, display_title, jacket_packet, volume_scenes)
# NB: cold_read (for make_codex_agent_fn) imports tomllib (py3.11+) and is imported
# lazily inside main(), so --check / --emit-prompt run under bare python3.10 too.

AGENT_DEF = REPO / ".claude/agents/blind-reader-grounded.md"
READER_PROTOCOL = "v3-grounded-checkpoint"


def load_agent_prompt(path: Path) -> str:
    """The agent body with its YAML frontmatter stripped = the reader's whole framing."""
    raw = Path(path).read_text()
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            raw = raw[end + 4:]
    body = raw.strip()
    if not body:
        raise SystemExit(f"empty prompt from {path}")
    return body


def vol1_slugs() -> list[str]:
    return checkpoint_bundle.volume_scenes.volume_one_slugs(drafted_only=True)


def boundary(n: int, decade: int) -> int:
    """Last decade checkpoint strictly before chapter n (0 = none / opening cold)."""
    return ((n - 1) // decade) * decade


def checkpoint_path(model_id: str, b: int) -> Path:
    return REPO / f"reviews/cold-read/{model_id}/checkpoints/ck-ch{b:03d}.md"


def load_checkpoint(model_id: str, b: int) -> str:
    """The checkpoint body (its `---`-delimited header stripped), or '' if b == 0."""
    if b <= 0:
        return ""
    p = checkpoint_path(model_id, b)
    if not p.exists():
        raise SystemExit(
            f"missing grounded checkpoint {p.relative_to(REPO)}. Mint it first:\n"
            f"  tools/checkpoint_extract.py --model {model_id} --to {b}"
        )
    raw = p.read_text()
    # Files written by checkpoint_extract.py lead with a `# ...\n\n*...*\n\n---\n\n` header.
    marker = "\n---\n\n"
    return raw.split(marker, 1)[1].strip() if marker in raw else raw.strip()


def build_window(b1: int, b2: int) -> str:
    """Clean prose of chapters [b1..b2], title-only delimiters (no chapter numbers —
    the reader is never told this chapter's index). Empty when b1 > b2."""
    if b1 > b2:
        return ""
    slugs = vol1_slugs()
    parts: list[str] = []
    for i in range(b1, b2 + 1):
        slug = slugs[i - 1]
        parts.append(f"\n\n===== {checkpoint_bundle.display_title(slug)} =====\n")
        parts.append(checkpoint_bundle.clean_scene_text(slug))
    return "\n".join(parts).strip()


def build_prompt(model_id: str, n: int, decade: int) -> str:
    """Assemble the grounded reader prompt for chapter n (1-based)."""
    slugs = vol1_slugs()
    slug = slugs[n - 1]
    title = checkpoint_bundle.display_title(slug)
    b = boundary(n, decade)
    checkpoint = load_checkpoint(model_id, b)
    window = build_window(b + 1, n - 1)

    parts = [f"TITLE:\n{title}\n"]
    # The packet is injected on EVERY chapter, not just the opening: a real reader
    # carries the cover + blurb the whole run as their going-in framing (SPEC). The
    # grounded reader has no chain to carry it, so relying on the checkpoint to
    # re-surface it silently dropped the tagline on late chapters (observed ch50).
    packet = checkpoint_bundle.jacket_packet()
    if packet:
        parts.append(
            "PUBLIC VOLUME-ENTRY PACKET (the cover + jacket you have held since you opened "
            "this volume — marketing, not story; hold it loosely):\n" + packet + "\n"
        )
    if checkpoint:
        parts.append(
            "GROUNDED MEMORY CHECKPOINT (your faithful memory of every earlier chapter "
            "you have read but cannot re-read — treat it as your own recollection):\n"
            + checkpoint + "\n"
        )
    if window:
        parts.append(
            "RECENT CHAPTERS (the full prose of the chapters immediately before this "
            "one, in order — still fresh in your mind; read them as the continuous "
            "lead-in to this chapter):\n" + window + "\n"
        )
    if not checkpoint and not window:
        parts.append(
            "You are opening the book cold: there is no prior memory. Read this first "
            "chapter knowing only the packet above (if any) and the page.\n"
        )
    parts.append(
        "OUTPUT: Return ONLY your Reader reaction (the felt read, then the structured "
        "block). Do not write any carry-forward, memory, or chapter record — your "
        "memory is supplied above and maintained elsewhere.\n"
    )
    parts.append(f"THIS CHAPTER:\n\n===== {title} =====\n{checkpoint_bundle.clean_scene_text(slug)}\n")
    return "\n".join(parts)


def strip_leading_heading(text: str) -> str:
    """Drop a leading `tool_uses:` echo or a `### Reader reaction` heading if present."""
    t = text.strip()
    if t.lower().startswith("tool_uses:"):
        t = t.split("\n", 1)[1].lstrip() if "\n" in t else ""
    import re
    t = re.sub(r"(?is)^\s*(?:#{1,3}\s*)?(?:\*\*)?reader reaction:?(?:\*\*)?\s*\n+", "", t, count=1)
    return t.strip()


def write_review(model_id: str, n: int, decade: int, reaction: str) -> Path:
    slugs = vol1_slugs()
    slug = slugs[n - 1]
    title = checkpoint_bundle.display_title(slug)
    b = boundary(n, decade)
    if b > 0 and b < n - 1:
        memory = f"ck-ch{b:03d} + raw ch{b + 1:03d}..ch{n - 1:03d}"
    elif b > 0:
        memory = f"ck-ch{b:03d} (no window)"
    elif n > 1:
        memory = f"raw ch001..ch{n - 1:03d} (pre-first-checkpoint)"
    else:
        memory = "— (opening, cold)"
    out = REPO / f"reviews/cold-read/{model_id}/grounded/{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f"# Cold read (grounded) — {title}\n\n"
        f"*scene: scenes/{slug}.md · model: {model_id} · memory: {memory} · "
        f"reader-protocol: {READER_PROTOCOL}*\n\n"
        f"## Reader reaction\n\n{reaction}\n"
    )
    out.write_text(content)
    return out


def resolve_range(args) -> list[int]:
    slugs = vol1_slugs()
    if args.scope:
        if args.scope not in slugs:
            raise SystemExit(f"unknown slug: {args.scope}")
        return [slugs.index(args.scope) + 1]
    start = args.start or 1
    end = args.end or len(slugs)
    if not (1 <= start <= end <= len(slugs)):
        raise SystemExit(f"range {start}..{end} out of bounds (1..{len(slugs)})")
    return list(range(start, end + 1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="gpt-5.6-terra", help="codex model id")
    ap.add_argument("--model-id", default=None, help="output dir (default: --model)")
    ap.add_argument("--scope", default=None, help="a single chapter by slug")
    ap.add_argument("--from", dest="start", type=int, default=None, help="first chapter (1-based)")
    ap.add_argument("--to", dest="end", type=int, default=None, help="last chapter (1-based)")
    ap.add_argument("--decade", type=int, default=10, help="checkpoint boundary size (default 10)")
    ap.add_argument("--effort", default="low", choices=["none", "low", "medium", "high"],
                    help="reader reasoning effort (default low; high turns the reader into a critic)")
    ap.add_argument("--fresh", action="store_true", help="regenerate existing grounded reviews")
    ap.add_argument("--emit-prompt", type=int, default=None, metavar="N",
                    help="print chapter N's assembled prompt to stdout and exit (no model call)")
    ap.add_argument("--check", action="store_true",
                    help="list the checkpoints the requested range needs (present/missing) and exit")
    args = ap.parse_args()
    model_id = args.model_id or args.model

    if args.emit_prompt is not None:
        try:
            sys.stdout.write(build_prompt(model_id, args.emit_prompt, args.decade))
        except BrokenPipeError:
            pass  # downstream closed the pipe (e.g. `| head`)
        return

    chapters = resolve_range(args)

    if args.check:
        needed = sorted({boundary(n, args.decade) for n in chapters} - {0})
        for b in needed:
            p = checkpoint_path(model_id, b)
            print(f"{'present' if p.exists() else 'MISSING'}  ck-ch{b:03d}  {p.relative_to(REPO)}")
        if not needed:
            print("no checkpoints needed for this range (all chapters ≤ first boundary)")
        return

    # Fail fast if any needed checkpoint is missing, before spending a single call.
    for b in sorted({boundary(n, args.decade) for n in chapters} - {0}):
        load_checkpoint(model_id, b)

    import cold_read  # noqa: E402  (make_codex_agent_fn — imports tomllib, py3.11+)
    system_prompt = load_agent_prompt(AGENT_DEF)
    agent_fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=args.effort)
    slugs = vol1_slugs()
    try:
        for n in chapters:
            slug = slugs[n - 1]
            out = REPO / f"reviews/cold-read/{model_id}/grounded/{slug}.md"
            if out.exists() and not args.fresh:
                print(f"[skip] ch{n:03d} {slug} (exists)", file=sys.stderr)
                continue
            prompt = build_prompt(model_id, n, args.decade)
            approx = int(len(prompt.split()) * 1.35)
            b = boundary(n, args.decade)
            print(f"[run] ch{n:03d} {slug}  memory=ck{b:03d}+win  ~{approx:,} tok  "
                  f"effort={args.effort} …", file=sys.stderr)
            t0 = time.time()
            result = agent_fn(prompt=prompt, model=args.model, label=f"grounded-{slug}")
            reaction = strip_leading_heading(result.get("output") or "")
            if len(reaction) < 200:
                raise SystemExit(f"suspiciously short reaction for {slug} ({len(reaction)} chars)")
            path = write_review(model_id, n, args.decade, reaction)
            u = result.get("usage") or {}
            print(f"[done] {path.relative_to(REPO)}  in={u.get('input')} out={u.get('output')} "
                  f"{time.time() - t0:.0f}s", file=sys.stderr)
    finally:
        close()


if __name__ == "__main__":
    main()
