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


PACKET_BASE = REPO / "reviews" / "cold-read" / ".packets"


def emit_packet(model_id: str, n: int, decade: int) -> tuple[str, Path, list[str]]:
    """Write chapter n's reading packet as small clean files under an unguessable
    token dir, for the sandboxed packet MCP server. Returns (token, dir, ordered
    file names). Each file is well under the Read/tool output cap; one window
    scene per file, so nothing needs paginating.

    Files are numbered so a plain filename sort is the intended read order:
      00-README   · 10-jacket · 20-checkpoint · 30..-recent-NN · 90-this-chapter
    """
    import secrets
    slugs = vol1_slugs()
    slug = slugs[n - 1]
    title = checkpoint_bundle.display_title(slug)
    b = boundary(n, decade)
    token = secrets.token_hex(16)
    d = (PACKET_BASE / token)
    d.mkdir(parents=True, exist_ok=True)

    names: list[str] = []

    def put(name: str, body: str) -> None:
        (d / name).write_text(body.rstrip() + "\n", encoding="utf-8")
        names.append(name)

    packet = checkpoint_bundle.jacket_packet()
    if packet:
        put("10-jacket.md",
            "PUBLIC VOLUME-ENTRY PACKET (the cover + jacket you have held since you "
            "opened this volume — marketing, not story; hold it loosely):\n\n" + packet)
    checkpoint = load_checkpoint(model_id, b)
    if checkpoint:
        put("20-checkpoint.md",
            "GROUNDED MEMORY CHECKPOINT (your faithful memory of every earlier chapter "
            "you have read but cannot re-read — treat it as your own recollection):\n\n"
            + checkpoint)
    if b + 1 <= n - 1:
        for j, i in enumerate(range(b + 1, n), start=1):
            wslug = slugs[i - 1]
            put(f"30-recent-{j:02d}.md",
                f"RECENT CHAPTER (read in order; real prose, still fresh in your mind — "
                f"the lead-in to this chapter):\n\n===== {checkpoint_bundle.display_title(wslug)} "
                f"=====\n\n" + checkpoint_bundle.clean_scene_text(wslug))
    if not checkpoint and not names:
        put("05-opening.md",
            "You are opening the book cold: there is no prior memory. Read this first "
            "chapter knowing only the jacket (if present) and the page.")
    put("90-this-chapter.md",
        f"THIS CHAPTER (the one you are reading now):\n\n===== {title} =====\n\n"
        + checkpoint_bundle.clean_scene_text(slug))

    ordered = sorted(names)
    readme = (
        "This is your reading packet. Read EVERY file below, in THIS ORDER, using your "
        "packet tool — call list_packet then read_packet for each. They are all small.\n\n"
        + "\n".join(f"  {i+1}. {nm}" for i, nm in enumerate(ordered))
        + "\n\nThe files are, in order: your jacket, your grounded memory checkpoint, the "
        "recent chapters (oldest to newest), and finally THIS CHAPTER (the last file). "
        "After reading them all, write ONLY your Reader reaction per your instructions.\n"
    )
    (d / "00-README.md").write_text(readme, encoding="utf-8")
    return token, d, ["00-README.md"] + ordered


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


def mint_checkpoints(model_id: str, boundaries: list[int], args, jobs: int = 1) -> None:
    """Wave 1 of the DAG: mint the missing decade checkpoints in parallel.

    Each checkpoint is grounded independently (from raw prose 1..B, one pass) with
    no dependency on any other checkpoint, so they fan out freely. Minting is a
    separate, higher-effort job than reading, so it always runs the extractor at
    high effort regardless of the reader's --effort. Runs checkpoint_extract.py as
    subprocesses (independent codex sessions) capped at `jobs`.
    """
    import subprocess
    from concurrent.futures import ThreadPoolExecutor, as_completed
    extract = str(REPO / "tools" / "checkpoint_extract.py")
    n = max(1, min(jobs, len(boundaries)))
    print(f"[wave1] minting {len(boundaries)} checkpoint(s) {boundaries} · jobs={n} · effort=high",
          file=sys.stderr)

    def mint(b: int):
        out = checkpoint_path(model_id, b)
        cmd = [extract, "--model", args.model, "--from", "1", "--to", str(b),
               "--effort", "high", "--out", str(out)]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            raise RuntimeError(f"checkpoint mint failed for ck-ch{b:03d}:\n{r.stderr.strip()[-800:]}")
        return b, time.time() - t0

    with ThreadPoolExecutor(max_workers=n) as ex:
        futs = {ex.submit(mint, b): b for b in boundaries}
        for fut in as_completed(futs):
            b, dt = fut.result()
            print(f"[wave1] ck-ch{b:03d} minted  {dt:.0f}s", file=sys.stderr)


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
    ap.add_argument("--jobs", "-j", type=int, default=1, metavar="N",
                    help="parallel reads (default 1). Reads are independent (grounded, no "
                    "chain), so wave 2 fans out to N concurrent codex sessions. On a slow "
                    "model this is the difference between ~8h serial and ~8h/N.")
    ap.add_argument("--auto-mint", action="store_true",
                    help="wave 1: mint any missing decade checkpoints first (in parallel, "
                    "capped by --jobs, at high effort) instead of refusing. Off by default — "
                    "minting is a distinct, more expensive job.")
    ap.add_argument("--emit-prompt", type=int, default=None, metavar="N",
                    help="print chapter N's assembled prompt to stdout and exit (no model call)")
    ap.add_argument("--emit-packet", type=int, default=None, metavar="N",
                    help="write chapter N's reading packet as small clean files under an "
                    "unguessable token dir (for the sandboxed packet MCP server / free "
                    "Claude-subagent reads); print the token + files and exit (no model call)")
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

    if args.emit_packet is not None:
        token, d, ordered = emit_packet(model_id, args.emit_packet, args.decade)
        print(f"packet_id: {token}")
        print(f"dir: {d.relative_to(REPO)}")
        print("files (read in this order):")
        for nm in ordered:
            print(f"  {nm}")
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

    needed = sorted({boundary(n, args.decade) for n in chapters} - {0})
    missing = [b for b in needed if not checkpoint_path(model_id, b).exists()]
    if missing:
        if not args.auto_mint:
            # Fail fast, naming every gap, before spending a single read call.
            for b in missing:
                load_checkpoint(model_id, b)  # raises with the mint command for the first
        mint_checkpoints(model_id, missing, args, jobs=args.jobs)

    slugs = vol1_slugs()
    todo = [n for n in chapters
            if args.fresh or not (REPO / f"reviews/cold-read/{model_id}/grounded/{slugs[n-1]}.md").exists()]
    skipped = [n for n in chapters if n not in todo]
    for n in skipped:
        print(f"[skip] ch{n:03d} {slugs[n-1]} (exists)", file=sys.stderr)
    if not todo:
        print("nothing to do (all requested chapters already read; use --fresh to regenerate)",
              file=sys.stderr)
        return

    import cold_read  # noqa: E402  (make_codex_agent_fn — imports tomllib, py3.11+)
    system_prompt = load_agent_prompt(AGENT_DEF)
    jobs = max(1, min(args.jobs, len(todo)))

    # A bounded pool of pre-built codex sessions: created serially (so token refresh
    # never races), reused across tasks, and handed out one-per-in-flight-read via a
    # queue. This caps concurrency at `jobs` and reuses sessions rather than spinning
    # up one per chapter.
    from queue import Queue
    from concurrent.futures import ThreadPoolExecutor, as_completed
    pool: "Queue" = Queue()
    closes = []
    for _ in range(jobs):
        fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=args.effort)
        closes.append(close)
        pool.put(fn)

    def read_one(n: int):
        slug = slugs[n - 1]
        b = boundary(n, args.decade)
        prompt = build_prompt(model_id, n, args.decade)
        fn = pool.get()
        try:
            t0 = time.time()
            result = fn(prompt=prompt, model=args.model, label=f"grounded-{slug}")
        finally:
            pool.put(fn)
        reaction = strip_leading_heading(result.get("output") or "")
        if len(reaction) < 200:
            raise RuntimeError(f"suspiciously short reaction for {slug} ({len(reaction)} chars)")
        path = write_review(model_id, n, args.decade, reaction)
        u = result.get("usage") or {}
        return n, slug, b, path, u, time.time() - t0

    print(f"[wave2] {len(todo)} reads · jobs={jobs} · effort={args.effort}", file=sys.stderr)
    errors = []
    try:
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            futs = {ex.submit(read_one, n): n for n in todo}
            for i, fut in enumerate(as_completed(futs), 1):
                n = futs[fut]
                try:
                    n, slug, b, path, u, dt = fut.result()
                    print(f"[done {i}/{len(todo)}] ch{n:03d} {slug}  memory=ck{b:03d}+win  "
                          f"in={u.get('input')} out={u.get('output')} {dt:.0f}s", file=sys.stderr)
                except Exception as e:
                    errors.append((n, e))
                    print(f"[FAIL {i}/{len(todo)}] ch{n:03d} {slugs[n-1]}: {type(e).__name__}: {e}",
                          file=sys.stderr)
    finally:
        for c in closes:
            c()
    if errors:
        raise SystemExit(f"{len(errors)} read(s) failed: "
                         + ", ".join(f"ch{n:03d}" for n, _ in sorted(errors)))


if __name__ == "__main__":
    main()
