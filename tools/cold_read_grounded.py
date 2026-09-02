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
reviews/cold-read/<model-id>/<slug>.md (the model root). The retired chained
reviews are archived under <model-id>/chained/ (cold_read.py / blind-reader.md
untouched, frozen).

Usage:
  tools/cold_read_grounded.py --to 50                     # all Vol 1, terra
  tools/cold_read_grounded.py --from 41 --to 50           # chapters 41..50
  tools/cold_read_grounded.py --scope nothing-underneath  # one chapter by slug
  tools/cold_read_grounded.py --scope vol2                # a whole volume by volN
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
import os
import re
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


def reader_slugs() -> list[str]:
    """The grounded reader's chapter sequence: Vol 1 drafted (1..50) followed by
    Vol 2 drafted, in chronology order. Vol 1 is exactly 50 drafted scenes, so
    appending Vol 2 never shifts a Vol 1 index — a Vol 1 read (n<=50) is byte-for-byte
    what it was before Vol 2 existed. Vol 2 drafts become 51, 52, ... and read from
    ck-ch050 (end of Vol 1) plus the raw prose of any earlier drafted Vol 2 chapters.
    NOTE: only chapters flagged 'Draft complete' in the chronology are included, so
    planning-only chapters between Vol 2 drafts are (unavoidably) skipped — the reader
    will see narrative gaps where unwritten chapters belong. The oracle battery
    deliberately stays on vol1_slugs().

    Drafted Vol 3 chapters are appended after Vol 2 (author ruling 2026-08-23) so they
    are cold-readable before the Vol 3 checkpoint machinery exists. Appending never
    shifts a Vol 1 or Vol 2 index. There is no ck past ck-ch050 yet, so a Vol 3 read
    must run with --decade 50 (boundary stays at ck-ch050 + the full raw Vol 2 window);
    the default decade 10 would demand a nonexistent ck-ch060.

    Delegates to checkpoint_bundle.reader_slugs() — the single cross-volume source shared
    with the authoring lane (checkpoint_context), so the two can never drift on inventory."""
    return checkpoint_bundle.reader_slugs()


def boundary(n: int, decade: int) -> int:
    """Last decade checkpoint strictly before chapter n (0 = none / opening cold)."""
    return ((n - 1) // decade) * decade


def memory_line(n: int, decade: int) -> str:
    """Human-readable description of chapter n's grounded memory, for the review header."""
    b = boundary(n, decade)
    if b > 0 and b < n - 1:
        return f"ck-ch{b:03d} + raw ch{b + 1:03d}..ch{n - 1:03d}"
    if b > 0:
        return f"ck-ch{b:03d} (no window)"
    if n > 1:
        return f"raw ch001..ch{n - 1:03d} (pre-first-checkpoint)"
    return "— (opening, cold)"


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
    slugs = reader_slugs()
    parts: list[str] = []
    for i in range(b1, b2 + 1):
        slug = slugs[i - 1]
        parts.append(f"\n\n===== {checkpoint_bundle.display_title(slug)} =====\n")
        parts.append(checkpoint_bundle.clean_scene_text(slug))
    return "\n".join(parts).strip()


def build_prompt(model_id: str, n: int, decade: int) -> str:
    """Assemble the grounded reader prompt for chapter n (1-based)."""
    slugs = reader_slugs()
    slug = slugs[n - 1]
    title = checkpoint_bundle.display_title(slug)
    b = boundary(n, decade)
    checkpoint = load_checkpoint(model_id, b)
    window = build_window(b + 1, n - 1)

    parts = []
    card = volume_title_card(checkpoint_bundle.volume_scenes.volume_of(slug))
    if card:
        # Title card (author ruling 2026-08-22): the reader always knows which book is
        # in their hands — series + volume title, cover-board fact, NOT jacket copy.
        # The blurb itself still injects exactly once, at the volume's opening chapter.
        parts.append(f"THE BOOK IN YOUR HANDS (cover board): {card}\n")
    parts.append(f"TITLE:\n{title}\n")
    # Jacket policy (author ruling 2026-08-18): the volume packet is injected ONLY at
    # its opening chapter — never re-injected, whole or thinned, on later chapters.
    # Re-injecting it every chapter kept the dark "game" framing at full weight and
    # over-anchored the reader's suspicion against the accumulating warm evidence (see
    # meta/meta-note-bounded-reader.md). On non-opening chapters the reader carries the
    # framing via the grounded checkpoint, exactly as a real reader carries a gist.
    volume = checkpoint_bundle.volume_scenes.volume_of(slug)
    opening_slug, packet = checkpoint_bundle.volume_packet(volume)
    is_volume_entry = bool(opening_slug) and slug == opening_slug
    if is_volume_entry and packet:
        parts.append(
            "PUBLIC VOLUME-ENTRY PACKET (the cover + jacket for the volume you are opening "
            "now — marketing, not story; hold it loosely):\n" + packet + "\n"
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
    prompt = "\n".join(parts)
    assert_jacket_policy(slug, is_volume_entry, prompt)
    return prompt


def volume_title_card(volume: int) -> str:
    """Series + volume title for the packet header, parsed from the volume packet's own
    cover line so it can never drift from the toml. Empty when the volume has no packet
    or the cover line doesn't match the house format. Guarded: the card must never
    contain jacket copy (any probe line of any volume) — the blurb injects exactly
    once, at the opening chapter, and the card is cover-board fact only."""
    _, packet = checkpoint_bundle.volume_packet(volume)
    if not packet:
        return ""
    m = re.search(r"the series line \*\*(.+?)\*\*, the volume title \*\*(.+?)\*\*", packet)
    if not m:
        return ""
    card = f"{m.group(1)} — {m.group(2)}"
    for vol in (1, 2, 3):
        _, pk = checkpoint_bundle.volume_packet(vol)
        if pk and any(pr in card for pr in _jacket_probes(pk)):
            raise SystemExit("[jacket guardrail] title card contains jacket copy — refusing")
    return card


def _jacket_probes(packet: str) -> list[str]:
    """Distinctive long lines of a jacket packet, used as re-injection tripwires. Blurb
    copy is marketing prose that never appears in scene text or a spec-blind checkpoint,
    so a match anywhere on a non-entry chapter means the jacket leaked back in. Long
    lines survive thinning/truncation as long as any one full sentence is kept."""
    out = []
    for ln in packet.splitlines():
        s = ln.strip().lstrip(">").strip().lstrip("*").strip()
        if len(s) >= 60:
            out.append(s)
    return out


def assert_jacket_policy(slug: str, is_volume_entry: bool, prompt: str) -> None:
    """Guardrail (author ruling 2026-08-18): the volume packet appears in a reader's
    prompt/packet ONLY at the volume's opening chapter, and never re-injected — whole or
    thinned — anywhere else. Checks the assembled packet text (the same string chunked
    into the .packets files) against every volume packet's signature lines. Raises rather
    than let a violating read reach a model."""
    for vol in (1, 2, 3):
        _, packet = checkpoint_bundle.volume_packet(vol)
        if not packet:
            continue
        probes = _jacket_probes(packet)
        present = any(pr in prompt for pr in probes)
        slug_vol = checkpoint_bundle.volume_scenes.volume_of(slug)
        if is_volume_entry:
            # the entry chapter must carry its own volume's packet; other volumes' must not appear
            own = slug_vol == vol
            if own and probes and not present:
                raise SystemExit(f"[jacket guardrail] {slug}: volume-entry chapter is missing its jacket packet")
            if not own and present:
                raise SystemExit(f"[jacket guardrail] {slug}: vol{vol} jacket text leaked into a vol{slug_vol} entry chapter")
        elif present:
            raise SystemExit(
                f"[jacket guardrail] {slug}: jacket text found on a NON-opening chapter. The "
                f"volume packet is injected exactly once, at its opening chapter; it must never "
                f"be re-injected (whole or thinned). Check build_prompt and the checkpoint."
            )


PACKET_BASE = REPO / "reviews" / "cold-read" / ".packets"
# The packet MCP tool truncates a single result above ~30KB (49KB confirmed
# truncated, 22KB confirmed whole). Chunk every packet file well under that so a
# sandboxed subagent always receives the FULL text — a partial read silently
# corrupts the checkpoint/reaction (observed: a 50KB bundle part came through as a
# 2KB preview). Split on line boundaries; the reader concatenates parts in order.
PACKET_MAX_CHARS = 22000


def gc_packets(max_age_hours: float = 24.0) -> int:
    """Remove packet dirs older than `max_age_hours` so .packets can't accumulate. A
    packet is a short-lived scratch dir consumed once by a reader subagent; anything
    this old is a leftover from a finished or abandoned run. Returns the count removed.
    mtime-based and best-effort — a packet still being written is far younger than 24h."""
    import shutil
    if not PACKET_BASE.is_dir():
        return 0
    cutoff = time.time() - max_age_hours * 3600
    removed = 0
    for p in PACKET_BASE.iterdir():
        try:
            if p.is_dir() and p.stat().st_mtime < cutoff:
                shutil.rmtree(p, ignore_errors=True)
                removed += 1
        except OSError:
            pass
    return removed


def _write_chunked_packet(text: str, readme_head: str, readme_tail: str) -> tuple[str, Path, list[str]]:
    """Split `text` into <=PACKET_MAX_CHARS line-boundary parts and write them (plus a
    README) under a fresh unguessable token dir. Returns (token, dir, ordered names)."""
    import secrets
    gc_packets()                      # sweep stale packets before minting a new one
    token = secrets.token_hex(16)
    d = PACKET_BASE / token
    d.mkdir(parents=True, exist_ok=True)

    parts: list[list[str]] = [[]]
    size = 0
    for ln in text.split("\n"):
        if size + len(ln) + 1 > PACKET_MAX_CHARS and parts[-1]:
            parts.append([])
            size = 0
        parts[-1].append(ln)
        size += len(ln) + 1

    names: list[str] = []
    n = len(parts)
    for i, chunk in enumerate(parts, start=1):
        name = f"{i:02d}-part.md"
        (d / name).write_text(
            f"[part {i} of {n} — read in order; this is one continuous document]\n\n"
            + "\n".join(chunk).strip() + "\n", encoding="utf-8")
        names.append(name)

    readme = (
        readme_head
        + "\n".join(f"  {i + 1}. {nm}" for i, nm in enumerate(names))
        + "\n\n" + readme_tail
    )
    (d / "00-README.md").write_text(readme, encoding="utf-8")
    return token, d, ["00-README.md"] + names


def _set_destination(d: Path, dest_rel: str, header: str) -> None:
    """Record where write_output should persist this packet's result (routing markers the
    MCP server reads; never listed or readable by the subagent)."""
    (d / ".dest").write_text(dest_rel + "\n", encoding="utf-8")
    (d / ".header").write_text(header, encoding="utf-8")


def emit_packet(model_id: str, n: int, decade: int) -> tuple[str, Path, list[str]]:
    """Write chapter n's reading packet (the assembled grounded read prompt — jacket +
    checkpoint + window + this chapter) as sub-cap chunk files under a token dir, for a
    sandboxed blind-reader-grounded subagent. Returns (token, dir, ordered names)."""
    slug = reader_slugs()[n - 1]
    title = checkpoint_bundle.display_title(slug)
    text = build_prompt(model_id, n, decade)
    head = ("This is your reading packet — ONE continuous document (your jacket, your "
            "grounded memory checkpoint, the recent chapters oldest→newest, and finally "
            "THIS CHAPTER) split across the numbered parts below. Read EVERY part, IN "
            "ORDER, with your packet tool (list_packet, then read_packet for each), "
            "before you write anything:\n\n")
    tail = ("Concatenate the parts in order — the section headers inside them tell you "
            "which is the checkpoint, the recent chapters, and THIS CHAPTER. Then write "
            "your Reader reaction and save it by calling write_output ONCE at the very end "
            "(packet id + your full reaction as `text`). That save is the ONLY way your "
            "read is recorded: do NOT reply with the reaction itself — returning it as a "
            "message instead of calling write_output is a failed read.\n")
    token, d, ordered = _write_chunked_packet(text, head, tail)
    header = (f"# Cold read (grounded) — {title}\n\n"
              f"*scene: scenes/{slug}.md · model: {model_id} · memory: {memory_line(n, decade)} · "
              f"reader-protocol: {READER_PROTOCOL}*\n\n## Reader reaction\n\n")
    _set_destination(d, f"reviews/cold-read/{model_id}/{slug}.md", header)
    return token, d, ordered


def persist_output(packet_id: str, text: str) -> Path:
    """Salvage path: persist a reaction/checkpoint that a subagent produced but returned
    as a chat message instead of calling the packet MCP's write_output (an intermittent
    failure of Claude reader subagents). Given the packet id and the returned text, this
    writes the same file write_output would have, deterministically — no hand-transcription.

    Mirrors tools/packet_reader_mcp.py:write_output; KEEP THE TWO IN SYNC (dest/header
    routing, the reviews-only + .md jail, the heading strip, the min-length guard)."""
    base = (REPO / "reviews" / "cold-read" / ".packets").resolve()
    if not re.match(r"^[0-9a-f]{32}$", packet_id or ""):
        raise SystemExit("invalid packet id")
    d = (base / packet_id).resolve()
    if d.parent != base or not d.is_dir():
        raise SystemExit(f"unknown packet {packet_id} (its .packets dir may have been cleaned up)")
    dest_file = d / ".dest"
    if not dest_file.is_file():
        raise SystemExit("this packet has no output destination")
    rel = dest_file.read_text(encoding="utf-8").strip()
    header = (d / ".header").read_text(encoding="utf-8") if (d / ".header").is_file() else ""
    dest = (REPO / rel).resolve()
    reviews_root = (REPO / "reviews" / "cold-read").resolve()
    if reviews_root not in dest.parents or dest.suffix != ".md":
        raise SystemExit("destination not permitted")
    body = (text or "").strip()
    # Drop a reader-emitted section heading; the destination header already carries one.
    body = re.sub(r"(?is)^\s*#{1,3}\s*(?:reader reaction|checkpoint)\b[^\n]*\n+", "", body, count=1).strip()
    if len(body) < 200:
        raise SystemExit(f"output too short to save ({len(body)} chars) — pass the full reaction on stdin")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(header + body + "\n", encoding="utf-8")
    return dest


def emit_bundle_packet(to_b: int, model_id: str) -> tuple[str, Path, list[str]]:
    """Write the clean prose bundle for chapters 1..to_b as sub-cap chunk files under a
    token dir, for a sandboxed blind-extractor subagent to mint ck-ch{to_b}. Returns
    (token, dir, ordered names)."""
    text = checkpoint_bundle.build_bundle(1, to_b, jacket=True)
    head = ("This is a reading packet holding ONE continuous document — the book's jacket "
            "followed by the clean text of the chapters to consolidate — split across the "
            "numbered parts below. Read EVERY part, IN ORDER, with your packet tool "
            "(list_packet, then read_packet for each), before you write anything:\n\n")
    tail = ("They are consecutive slices of the same document; concatenate them in order. "
            "Then produce your checkpoint and save it with write_output.\n")
    token, d, ordered = _write_chunked_packet(text, head, tail)
    header = (f"# Checkpoint — through Chapter {to_b} (grounded, single pass)\n\n"
              f"*model: {model_id} · span: ch001–ch{to_b:03d} · grounded "
              f"(full clean prose, sandboxed packet read, no chaining)*\n\n---\n\n")
    _set_destination(d, f"reviews/cold-read/{model_id}/checkpoints/ck-ch{to_b:03d}.md", header)
    return token, d, ordered


ORACLE_BATTERY = REPO / "reviews" / "cold-read" / "oracle-battery.json"
ORACLE_AGENT_DEF = REPO / ".claude/agents/blind-oracle-grounded.md"


def _reaction_body(model_id: str, slug: str) -> str:
    """A grounded read file's reaction (its metadata header stripped)."""
    t = (REPO / f"reviews/cold-read/{model_id}/{slug}.md").read_text(encoding="utf-8")
    i = t.find("## Reader reaction")
    return t[i:] if i >= 0 else t


def _probe_question(probe: str, tier: str) -> str:
    import json
    battery = json.loads(ORACLE_BATTERY.read_text(encoding="utf-8"))
    if probe not in battery["probes"]:
        raise SystemExit(f"unknown probe '{probe}'. Known: {', '.join(sorted(battery['probes']))}")
    if tier not in ("neutral", "pointed"):
        raise SystemExit("tier must be 'neutral' or 'pointed'")
    return battery["probes"][probe][tier]


def all_probes() -> list[str]:
    import json
    return list(json.loads(ORACLE_BATTERY.read_text(encoding="utf-8"))["probes"])


def _oracle_text(model_id: str, probe: str, tier: str) -> tuple[str, str]:
    """The oracle memory (jacket + this model's 50 reactions) + the probe's tier question,
    as one continuous document. Returns (text, question)."""
    question = _probe_question(probe, tier)
    parts = []
    packet = checkpoint_bundle.jacket_packet()
    if packet:
        parts.append("===== THE JACKET YOU HAD GOING IN (marketing, not story) =====\n\n" + packet)
    for slug in vol1_slugs():
        parts.append(f"\n\n===== YOUR READING — {checkpoint_bundle.display_title(slug)} =====\n")
        parts.append(_reaction_body(model_id, slug))
    parts.append("\n\n===== THE INTERVIEW QUESTION (answer from your reading above) =====\n\n" + question)
    return "\n".join(parts), question


def _oracle_header(model_id: str, probe: str, tier: str, question: str) -> str:
    return (f"# Oracle (grounded) — {probe} · {tier}\n\n"
            f"*model: {model_id} · probe: {probe} · tier: {tier} · stage: end (whole book) · "
            f"battery: oracle-battery.json*\n\n"
            f"**Question asked (verbatim):** {question}\n\n---\n\n")


def emit_oracle_packet(model_id: str, probe: str, tier: str) -> tuple[str, Path, list[str]]:
    """Mint an oracle interview packet for (model, probe, tier): the jacket + this model's
    own 50 chapter reactions (its whole reading record) + the probe's tier question, chunked
    for the sandboxed blind-oracle-grounded subagent. .dest routes its answer to
    reviews/cold-read/<model>/oracle/<probe>--<tier>.md. Returns (token, dir, names)."""
    text, question = _oracle_text(model_id, probe, tier)

    head = ("This is your reading record and one interview question, ONE continuous document "
            "split across the numbered parts below (the jacket, your own chapter-by-chapter "
            "reactions across the whole book, and finally the question). Read EVERY part, IN "
            "ORDER, with your packet tool (list_packet, then read_packet for each), before you "
            "answer:\n\n")
    tail = ("The last part holds the interview question. Answer it from your reading record above, "
            "then save your answer with write_output.\n")
    token, d, ordered = _write_chunked_packet(text, head, tail)
    _set_destination(d, f"reviews/cold-read/{model_id}/oracle/{probe}--{tier}.md",
                     _oracle_header(model_id, probe, tier, question))
    return token, d, ordered


def run_oracle_codex_battery(model: str, model_id: str, probes, effort: str = "low",
                             jobs: int = 1, fresh: bool = False) -> None:
    """Run the oracle over a codex model (the GPT trio) inline: for each (probe, tier) build
    the memory+question and answer it with the blind-oracle-grounded persona as system prompt,
    writing reviews/cold-read/<model_id>/oracle/<probe>--<tier>.md. Funnel-b holds by
    construction — neutral and pointed are separate, independent calls."""
    import cold_read  # noqa: E402
    from queue import Queue
    from concurrent.futures import ThreadPoolExecutor, as_completed

    system_prompt = load_agent_prompt(ORACLE_AGENT_DEF)
    tasks = [(p, t) for p in probes for t in ("neutral", "pointed")]
    todo = [(p, t) for (p, t) in tasks
            if fresh or not (REPO / f"reviews/cold-read/{model_id}/oracle/{p}--{t}.md").exists()]
    if not todo:
        print(f"[oracle] {model_id}: nothing to do", file=sys.stderr)
        return
    jobs = max(1, min(jobs, len(todo)))
    pool: "Queue" = Queue()
    closes = []
    for _ in range(jobs):
        fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=effort)
        closes.append(close)
        pool.put(fn)

    def one(probe, tier):
        text, question = _oracle_text(model_id, probe, tier)
        prompt = text + ("\n\n(The material above is pasted inline. Answer the interview "
                         "question from your reading record; return ONLY your answer.)")
        fn = pool.get()
        try:
            result = fn(prompt=prompt, model=model, label=f"oracle-{probe}-{tier}")
        finally:
            pool.put(fn)
        ans = strip_leading_heading(result.get("output") or "")
        if len(ans) < 120:
            raise RuntimeError(f"short oracle answer for {probe}--{tier} ({len(ans)} chars)")
        out = REPO / f"reviews/cold-read/{model_id}/oracle/{probe}--{tier}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_oracle_header(model_id, probe, tier, question) + ans + "\n")
        return probe, tier, out

    print(f"[oracle] {model_id}: {len(todo)} answers · jobs={jobs} · effort={effort}", file=sys.stderr)
    errors = []
    try:
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            futs = {ex.submit(one, p, t): (p, t) for (p, t) in todo}
            for i, fut in enumerate(as_completed(futs), 1):
                p, t = futs[fut]
                try:
                    _, _, out = fut.result()
                    print(f"[done {i}/{len(todo)}] {out.relative_to(REPO)}", file=sys.stderr)
                except Exception as e:
                    errors.append((p, t, e))
                    print(f"[FAIL {i}/{len(todo)}] {p}--{t}: {type(e).__name__}: {e}", file=sys.stderr)
    finally:
        for c in closes:
            c()
    if errors:
        raise SystemExit(f"{len(errors)} oracle answer(s) failed")


def run_interview_codex(model: str, model_id: str, n: int, decade: int,
                        questions: str, label: str, effort: str = "low") -> Path:
    """Interview a codex reader about ONE chapter it has just read (the codex twin of
    resuming a Claude blind-reader subagent with follow-up questions). Codex runs are
    stateless, so the reader's state is reconstructed exactly: the same grounded read
    prompt (jacket + checkpoint + window + chapter), then its own saved written
    reaction, then the questions — answered under the blind-reader-grounded persona,
    page-only rules. Writes reviews/cold-read/<model_id>/interviews/<slug>--<label>.md."""
    import cold_read  # noqa: E402
    slugs = reader_slugs()
    slug = slugs[n - 1]
    reaction = _reaction_body(model_id, slug)
    prompt = (
        build_prompt(model_id, n, decade)
        + "\n\n===== YOUR WRITTEN REACTION (you have already read the chapter above "
        "and saved this reaction) =====\n\n"
        + reaction
        + "\n\n===== FOLLOW-UP INTERVIEW =====\n\n"
        "This is a follow-up interview about the chapter you just read; the OUTPUT "
        "instruction above no longer applies. Answer from your experience of the page "
        "only — the same rules as your read apply (nothing you weren't given). Answer "
        "each question in order, separately, as specifically as you can; quote the "
        "page where it helps. Return ONLY your numbered answers.\n\n"
        + questions.strip() + "\n"
    )
    system_prompt = load_agent_prompt(AGENT_DEF)
    fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=effort)
    try:
        result = fn(prompt=prompt, model=model, label=f"interview-{slug}")
    finally:
        close()
    ans = strip_leading_heading(result.get("output") or "")
    if len(ans) < 200:
        raise RuntimeError(f"suspiciously short interview answer for {slug} ({len(ans)} chars)")
    out = REPO / f"reviews/cold-read/{model_id}/interviews/{slug}--{label}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# Interview (grounded) — {slug} · {label}\n\n"
        f"*model: {model_id} · chapter: {slug} (ch {n}) · memory: "
        f"ck-ch{boundary(n, decade):03d}+window · reader-protocol: v3-grounded-checkpoint "
        f"(follow-up interview; context rebuilt, own reaction re-supplied)*\n\n"
        f"## Questions (verbatim)\n\n{questions.strip()}\n\n---\n\n## Answers\n\n{ans}\n",
        encoding="utf-8")
    return out


def strip_leading_heading(text: str) -> str:
    """Drop a leading `tool_uses:` echo or a `### Reader reaction` heading if present."""
    t = text.strip()
    if t.lower().startswith("tool_uses:"):
        t = t.split("\n", 1)[1].lstrip() if "\n" in t else ""
    import re
    t = re.sub(r"(?is)^\s*(?:#{1,3}\s*)?(?:\*\*)?reader reaction:?(?:\*\*)?\s*\n+", "", t, count=1)
    return t.strip()


def write_review(model_id: str, n: int, decade: int, reaction: str) -> Path:
    slugs = reader_slugs()
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
    out = REPO / f"reviews/cold-read/{model_id}/{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f"# Cold read (grounded) — {title}\n\n"
        f"*scene: scenes/{slug}.md · model: {model_id} · memory: {memory} · "
        f"reader-protocol: {READER_PROTOCOL}*\n\n"
        f"## Reader reaction\n\n{reaction}\n"
    )
    out.write_text(content)
    return out


def run_claude_headless(model: str, model_id: str, n: int, decade: int,
                        system_prompt: str) -> Path:
    """Clean-lane Claude read via headless `claude -p` (author ruling 2026-08-22):
    subscription OAuth (never an API key — ANTHROPIC_API_KEY is scrubbed so billing
    can't silently switch to pay-per-token), agent def as the ENTIRE system prompt
    (--exclude-dynamic-system-prompt-sections), run from a throwaway non-repo cwd so
    no project CLAUDE.md/AGENTS.md, git snapshot, or memory index can leak into the
    reader. Mirrors the codex lane: packet on stdin, reaction on stdout, harness
    writes the review file."""
    import subprocess as sp
    import tempfile
    prompt = build_prompt(model_id, n, decade)
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)  # subscription auth only, per the token rule
    with tempfile.TemporaryDirectory(prefix="coldread-") as td:
        spf = Path(td) / "system-prompt.md"
        spf.write_text(system_prompt, encoding="utf-8")
        cmd = ["claude", "-p", "--model", model,
               "--system-prompt-file", str(spf),
               "--exclude-dynamic-system-prompt-sections"]
        r = sp.run(cmd, input=prompt, capture_output=True, text=True,
                   env=env, cwd=td, timeout=2400)
    if r.returncode != 0:
        raise RuntimeError(f"claude -p failed for ch{n}: {r.stderr.strip()[-600:]}")
    reaction = strip_leading_heading(r.stdout)
    if len(reaction) < 200:
        raise RuntimeError(f"suspiciously short reaction for ch{n} ({len(reaction)} chars)")
    return write_review(model_id, n, decade, reaction)


def resolve_range(args) -> list[int]:
    slugs = reader_slugs()
    if args.scope:
        m = re.fullmatch(r"vol([123])", args.scope.strip().lower())
        if m:
            vol = int(m.group(1))
            idxs = [i + 1 for i, s in enumerate(slugs)
                    if checkpoint_bundle.volume_scenes.volume_of(s) == vol]
            if not idxs:
                raise SystemExit(f"no drafted chapters for vol{vol} in the reader set")
            return idxs
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
    ap.add_argument("--scope", default=None, help="a single chapter by slug, or a whole volume by 'vol1'/'vol2'/'vol3'")
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
    ap.add_argument("--emit-bundle-packet", type=int, default=None, metavar="B",
                    help="write the clean prose bundle for chapters 1..B as sub-cap chunk "
                    "files under a token dir, for a sandboxed blind-extractor subagent to "
                    "mint ck-ch{B}; print the token + files and exit (no model call)")
    ap.add_argument("--emit-oracle-packet", nargs=2, default=None, metavar=("PROBE", "TIER"),
                    help="write an oracle interview packet (this model's 50 reactions + the "
                    "battery probe's tier question) for a sandboxed blind-oracle-grounded "
                    "subagent; print the token and exit (no model call)")
    ap.add_argument("--run-oracle-battery", action="store_true",
                    help="run the oracle over a CODEX model (the GPT trio) inline: every probe "
                    "(or --probes) × both tiers, writing <model-id>/oracle/<probe>--<tier>.md")
    ap.add_argument("--probes", default=None,
                    help="comma-separated probe keys for --run-oracle-battery (default: all)")
    ap.add_argument("--interview", type=int, default=None, metavar="N",
                    help="interview this codex model about chapter N it has already read: "
                         "rebuilds the read context + its saved reaction, asks the questions "
                         "from --questions (or stdin), writes "
                         "reviews/cold-read/<model-id>/interviews/<slug>--<label>.md")
    ap.add_argument("--questions", default=None, metavar="FILE",
                    help="questions file for --interview (default: read stdin)")
    ap.add_argument("--label", default="interview",
                    help="output filename suffix for --interview (default: interview)")
    ap.add_argument("--check", action="store_true",
                    help="list the checkpoints the requested range needs (present/missing) and exit")
    ap.add_argument("--persist-output", metavar="PACKET_ID", default=None,
                    help="salvage: read reaction/checkpoint text from stdin and persist it to "
                    "PACKET_ID's destination (same file write_output would write). Use when a "
                    "Claude reader subagent returned its text instead of calling write_output.")
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

    if args.persist_output is not None:
        dest = persist_output(args.persist_output, sys.stdin.read())
        print(f"saved to {dest.relative_to(REPO)}")
        return

    if args.emit_bundle_packet is not None:
        token, d, ordered = emit_bundle_packet(args.emit_bundle_packet, model_id)
        print(f"packet_id: {token}")
        print(f"dir: {d.relative_to(REPO)}")
        print(f"parts: {len(ordered) - 1}")
        return

    if args.emit_oracle_packet is not None:
        probe, tier = args.emit_oracle_packet
        token, d, ordered = emit_oracle_packet(model_id, probe, tier)
        print(f"packet_id: {token}")
        print(f"dir: {d.relative_to(REPO)}")
        print(f"parts: {len(ordered) - 1}")
        return

    if args.interview is not None:
        q = (Path(args.questions).read_text(encoding="utf-8") if args.questions
             else sys.stdin.read())
        if not q.strip():
            raise SystemExit("no questions supplied (use --questions FILE or pipe stdin)")
        out = run_interview_codex(args.model, model_id, args.interview, args.decade,
                                  q, args.label, effort=args.effort)
        print(f"saved {out.relative_to(REPO)}")
        return

    if args.run_oracle_battery:
        probes = [p.strip() for p in args.probes.split(",")] if args.probes else all_probes()
        run_oracle_codex_battery(args.model, model_id, probes, effort=args.effort,
                                 jobs=args.jobs, fresh=args.fresh)
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

    slugs = reader_slugs()
    todo = [n for n in chapters
            if args.fresh or not (REPO / f"reviews/cold-read/{model_id}/{slugs[n-1]}.md").exists()]
    skipped = [n for n in chapters if n not in todo]
    for n in skipped:
        print(f"[skip] ch{n:03d} {slugs[n-1]} (exists)", file=sys.stderr)
    if not todo:
        print("nothing to do (all requested chapters already read; use --fresh to regenerate)",
              file=sys.stderr)
        return

    if args.model.startswith("claude-"):
        # Headless clean lane for the Claude trio (author ruling 2026-08-22).
        from concurrent.futures import ThreadPoolExecutor, as_completed
        system_prompt = load_agent_prompt(AGENT_DEF)
        jobs = max(1, min(args.jobs, len(todo)))
        print(f"[wave2/claude-headless] {len(todo)} reads · jobs={jobs}", file=sys.stderr)
        failures = []
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            futs = {ex.submit(run_claude_headless, args.model, model_id, n,
                              args.decade, system_prompt): n for n in todo}
            for fut in as_completed(futs):
                n = futs[fut]
                try:
                    path = fut.result()
                    print(f"[done] ch{n:03d} → {path.relative_to(REPO)}", file=sys.stderr)
                except Exception as e:
                    failures.append(n)
                    print(f"[FAIL] ch{n:03d}: {e}", file=sys.stderr)
        if failures:
            raise SystemExit(f"{len(failures)} headless read(s) failed: {failures}")
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
