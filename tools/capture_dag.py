#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Capture DAG — cold-reader-model persona reads of Volume 1.

One run per chapter: chapter N is read with the reader's OWN carry-forward
checkpoint ck-ch<B> (B = decade boundary below N) + raw prose of chapters
B+1..N-1 + chapter N (e.g. ch25 = own ck-ch020 + raw ch021-024 + ch025).
Every 10 chapters the reader MINTS its own carry-forward from: prior
checkpoint + the decade's raw prose + its own gate notes. Each reader
(persona x model) mints its own checkpoints — persona memory IS the
instrument. A STOP gate ends the reader permanently (later chapters skipped).

Sequential per reader (correct STOP semantics); readers run in parallel.
Restartable: existing gates/checkpoints are skipped.

Usage:
  tools/capture_dag.py --models claude-opus-4-8 gpt-5.6-sol            # the 3 default personas
  tools/capture_dag.py --models claude-opus-4-8 --personas fsog-refugee --to 12
  tools/capture_dag.py --models ... --to 70 --fresh   # re-read ch70 after revising it
  tools/capture_dag.py --models ... --assemble    # build <persona>--volume-dag.md records
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import authorship_audit  # noqa: E402  (run_claude, CLAUDE_PREFIX)
import cold_read_config  # noqa: E402  (rosters + OpenRouter map — the single source)
import chapter_dates  # noqa: E402  (the stable chapter-date source)

PANEL_ROOT = REPO / "reviews" / "capture-panel"
PROTOCOL = "capture-dag-v2-rich"
# Experiment lanes (set from --experiment / --dated in main). An experiment writes
# under split-experiments/<name>/, outside the */dag/* glob capture_stats reads,
# so it can never mix into the real capture record. DATED adds the reader-facing
# date lines from chapter_dates (weekday, month, day; never the year). The real
# lanes read dated by default (author ruling 2026-10-25: the book ships with
# date lines; the dated experiment arm was promoted to the real lanes). Quiet
# section days are omitted, exactly as in the epub.
EXPERIMENT: str | None = None
DATED = False
PERSONAS = ["romance-graduate", "fsog-refugee"]
# Standing TWO (author ruling 2026-10-10): the default capture panel is the two
# primary-vector readers, `romance-graduate` and `fsog-refugee`. `relationship-first`
# gives up the third seat it held under the 2026-09-27 ruling and becomes selectable;
# its gates stay on disk as history. Supersedes "roster x 3".
# Still selectable, never default: consent-sensitive is ON REQUEST (free-sample runs
# and any run touching the reveal chapters); romantasy-refugee for the volume-close
# calibration only; relationship-first and line-editor on request. v1 persona texts:
# personas/archive/.
# RETIRED from running (author ruling 2026-09-12): `dark-romance-control` is the
# WRONG reader — a book that captures her is failing the repel goal, so her STOPs
# were the success condition. She has delivered it (opus STOPPED at ch021, sol at
# ch006), and the lanes that didn't stop sat permanently behind, making every
# "catch up to chapter N" scope cost more than the signal was worth. Do not run
# her again. She stays in ALL_PERSONAS so a run that names her fails loudly.
# 2026-09-26: her gates, checkpoints and STOPPED markers were erased from the
# tree (author ruling; git history keeps them), so --assemble no longer applies.
RETIRED_PERSONAS = ["dark-romance-control"]
# `queer-woman` is selectable but NOT in the default panel — opt in with
# --personas, so a bare run never silently opens a fresh 70-chapter read on a
# subscription lane.
ALL_PERSONAS = PERSONAS + ["relationship-first", "consent-sensitive", "line-editor",
                           "romantasy-refugee", "queer-woman"] + RETIRED_PERSONAS
DECADE = 10


def volume_one_count() -> int:
    return len(checkpoint_bundle.volume_scenes.volume_one_slugs(drafted_only=True))


def slugs() -> list[str]:
    """The full drafted cross-volume sequence (Vol 1, then Vol 2, then Vol 3),
    so a reader can be run on past the Volume 1 boundary. `--to` bounds the run
    and defaults to `N_CH` = the drafted Volume 1 length, so a bare invocation
    still reads Volume 1 only."""
    return checkpoint_bundle.reader_slugs()


N_CH = volume_one_count()


def boundary(n: int) -> int:
    return ((n - 1) // DECADE) * DECADE


# Personas that read through their own frame (author ruling 2026-09-29): the
# line-editor keeps the reader voice but adds a verbatim NOTES block and a
# WHAT I'VE MARKED section in her mint, so a flagged line can live in summary memory.
PERSONA_FRAMES = {"line-editor": ("core-line.md", "core-line-mint.md")}


def sysprompt(persona: str, frame: str) -> tuple[str, str]:
    core = (PANEL_ROOT / "prompts" / frame).read_text(encoding="utf-8")
    pers = (PANEL_ROOT / "personas" / f"{persona}.md").read_text(encoding="utf-8")
    text = core.rstrip() + "\n\n" + pers.strip() + "\n"
    return text, hashlib.sha256(text.encode()).hexdigest()[:12]


def dag_dir(model_id: str, persona: str) -> Path:
    if MEMORY != "chain":
        return v3_root(model_id) / persona
    if EXPERIMENT:
        return PANEL_ROOT / "split-experiments" / EXPERIMENT / model_id / "dag" / persona
    return PANEL_ROOT / model_id / "dag" / persona


def variant_tag() -> str:
    if not EXPERIMENT:
        return " · dated" if DATED else " · undated"
    return f" · experiment {EXPERIMENT}" + (" · dated" if DATED else " · undated")


def gate_path(d: Path, n: int) -> Path:
    return d / f"gate-ch{n:03d}.md"


def ck_path(d: Path, b: int) -> Path:
    return d / f"ck-ch{b:03d}.md"


def chapter_block(i: int) -> str:
    s = slugs()[i - 1]
    body = checkpoint_bundle.clean_scene_text(s)
    head = f"===== CHAPTER {i}: {checkpoint_bundle.display_title(s)} =====\n\n"
    if DATED:
        line = chapter_dates.heading(s)
        if line:  # None: the chapter opens undated (a flashback panel)
            head += f"*{line}*\n\n"
        body = chapter_dates.dated_text(s, body)
    return f"{head}{body}\n"


def chapter_sha(i: int) -> str:
    """Short hash of chapter i's clean text — what a reader actually read."""
    return hashlib.sha256(
        checkpoint_bundle.clean_scene_text(slugs()[i - 1]).encode()).hexdigest()[:12]


GATE_HEADER_RE = re.compile(
    r"gate ch(\d{3}).*?(?:prose-sha ([0-9a-f]{12}))?(?:\s|·|\*|$)")


def recorded_prose_sha(gate_file: Path) -> str | None:
    """The prose-sha a gate recorded, or None for gates written before tracking."""
    try:
        head = gate_file.read_text(encoding="utf-8").split("\n", 1)[0]
    except OSError:
        return None
    m = re.search(r"prose-sha ~?([0-9a-f]{12})", head)
    return m.group(1) if m else None


def stale_report(model_ids: list[str], personas: list[str], to_n: int) -> dict:
    """Classify existing gates against current prose. Never blocks — this is a warning.

    Three tiers, because they matter very differently for a style edit:
      direct      — this gate's OWN chapter changed; the reaction is to text that is gone
      window      — a chapter in this gate's raw window (B+1..N-1) changed
      checkpoint  — a changed chapter fed this gate's ck-ch<B> mint (weakest signal:
                    the reader's memory of it is a consolidated summary, which a
                    style edit usually leaves true)
    """
    current = {}
    for n in range(1, min(to_n, len(slugs())) + 1):
        try:
            current[n] = chapter_sha(n)
        except Exception:
            pass
    changed, unverifiable = set(), 0
    gates = []
    for m in model_ids:
        for p in personas:
            d = dag_dir(m, p)
            if not d.is_dir():
                continue
            for n in range(1, to_n + 1):
                gp = gate_path(d, n)
                if not gp.exists():
                    continue
                rec = recorded_prose_sha(gp)
                gates.append((m, p, n, rec))
                if rec is None:
                    unverifiable += 1
                elif n in current and rec != current[n]:
                    changed.add(n)
    tiers = {"direct": 0, "window": 0, "checkpoint": 0}
    for _m, _p, n, rec in gates:
        b = boundary(n)
        if n in changed:
            tiers["direct"] += 1
        elif any(b < c < n for c in changed):
            tiers["window"] += 1
        elif any(c <= b for c in changed):
            tiers["checkpoint"] += 1
    return {"changed_chapters": sorted(changed), "tiers": tiers,
            "unverifiable": unverifiable, "gates": len(gates)}


def print_stale_report(rep: dict) -> None:
    if rep["unverifiable"]:
        print(f"  note: {rep['unverifiable']} gate(s) predate prose-sha tracking "
              f"— staleness unverifiable for those", flush=True)
    if not rep["changed_chapters"]:
        if rep["gates"] and not rep["unverifiable"]:
            print("  prose check: all existing gates match current chapter text",
                  flush=True)
        return
    ch = ", ".join(f"ch{c:03d}" for c in rep["changed_chapters"])
    t = rep["tiers"]
    print(f"  STALE PROSE — changed since minting: {ch}", flush=True)
    print(f"    direct     {t['direct']:5}  gate's own chapter changed "
          f"(re-read these if the edit was substantive)", flush=True)
    print(f"    window     {t['window']:5}  changed chapter sat in the raw window",
          flush=True)
    print(f"    checkpoint {t['checkpoint']:5}  changed chapter fed the carry-forward "
          f"(usually ignorable for a style edit)", flush=True)
    print("    proceeding — re-read a chapter with `--to <N> --fresh`", flush=True)


def jacket_block(n: int) -> str:
    """The jacket of the volume the reader is currently holding.

    Volume-aware since 2026-09-19, when this DAG first ran past Volume One.
    `jacket_packet()` returns Volume One's copy unconditionally, so a persona
    crossing into Book Two would have been told it was still reading *A
    Polite Invitation* for all 23 chapters. These gates reason against the
    jacket explicitly — a ch020 reaction quotes the tagline by name — so the
    wrong cover corrupts exactly the judgement the instrument measures.

    Unlike the cold-read lane, which shows a volume packet once at that
    volume's opening chapter, the capture reader is holding the book, so the
    current volume's jacket rides every prompt. Volume One output is
    unchanged: volume_packet(1) is byte-identical to jacket_packet()."""
    vol = checkpoint_bundle.volume_scenes.volume_of(slugs()[n - 1])
    _opening, packet = checkpoint_bundle.volume_packet(vol)
    if not packet:
        raise SystemExit(
            f"no jacket packet for volume {vol} in volume-packets.toml — "
            "add one; never substitute another volume's packet"
        )
    return f"===== THE JACKET =====\n\n{packet}\n"


def read_prompt(d: Path, n: int) -> str:
    b = boundary(n)
    parts = [jacket_block(n)]
    if b:
        ck = ck_path(d, b).read_text(encoding="utf-8")
        parts.append(f"===== YOUR CARRY-FORWARD NOTES (written after chapter {b}) "
                     f"=====\n\n{ck}\n")
    if n - 1 > b:
        parts.append("===== RECENT CHAPTERS (raw, still fresh) =====\n")
        for i in range(b + 1, n):
            parts.append(chapter_block(i))
    parts.append("===== THE NEW CHAPTER =====\n")
    parts.append(chapter_block(n))
    parts.append(f"Read chapter {n} and produce your REACTION, then your single "
                 "gate block.")
    return "\n".join(parts)


def mint_prompt(d: Path, n: int) -> str:
    b = boundary(n)  # previous boundary (n is a multiple of 10 -> b = n-10)
    parts = [jacket_block(n)]
    if b:
        parts.append(f"===== YOUR PREVIOUS CARRY-FORWARD NOTES (after chapter {b}) "
                     f"=====\n\n{ck_path(d, b).read_text(encoding='utf-8')}\n")
    parts.append("===== CHAPTERS YOU JUST READ =====\n")
    for i in range(b + 1, n + 1):
        parts.append(chapter_block(i))
    parts.append("===== YOUR OWN GATE NOTES FOR THEM =====\n")
    for i in range(b + 1, n + 1):
        parts.append(gate_path(d, i).read_text(encoding="utf-8"))
    parts.append(f"\nWrite your carry-forward notes through chapter {n} now.")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Memory v3 (author ruling 2026-11-01): no summary of a summary.
#
# The chain mint above re-summarises its own previous summary every decade, in the
# persona's voice, and by ck-ch050 the bench night was one line. v3 splits memory:
#   facts   — the cold-read lane's grounded checkpoint (one hop from raw prose,
#             spec-blind extractor), or in `full` mode the raw book itself;
#   persona — her own words, never re-summarised: every reaction verbatim for the
#             current volume, the gate blocks verbatim for earlier volumes, and a
#             LEDGER (fears, loves, grudges, suspicions, waiting-fors) that code
#             folds from the per-gate LEDGER deltas.
# v3 gates live in dag-v3/ (dag-v3-full/), outside the */dag/* glob that
# capture_stats and capture_delta read, so the eras never mix. SPEC "Memory v3".
MEMORY = "chain"
BORROW = False
PROTOCOL_V3 = "capture-dag-v3"
LEDGER_KINDS = {"FEAR": "F", "LOVE": "L", "GRUDGE": "G", "SUSPICION": "S", "WAITING": "W"}
OPEN_STATUSES = {"DEEPENED", "SHIFTED"}
SETTLED_STATUSES = {"CONFIRMED", "DISPROVED", "RESOLVED", "FORGIVEN", "ANSWERED", "FADED"}
_KIND = "|".join(LEDGER_KINDS)
_STATUS = "|".join(sorted(OPEN_STATUSES | SETTLED_STATUSES))
LEDGER_HEAD_RE = re.compile(r"(?im)^\W*LEDGER\W*$")
ADD_RE = re.compile(rf"(?i)^\W*\+\s*\**({_KIND})\**\s*[:\-—–]\s*(.+)$")
UPDATE_RE = re.compile(rf"(?i)^\W*~\s*\[?([A-Za-z]\d+\.\d+)\]?\s+\**({_STATUS})\**\s*[:\-—–]\s*(.+)$")
SEED_RE = re.compile(rf"(?i)^\W*\+\s*\**({_KIND})\**\s*\(ch\s*(\d+)\)\s*"
                     rf"(?:\**({_STATUS})\**\s*ch\s*(\d+))?\s*[:\-—–]\s*(.+)$")
GATE_LINE_RE = re.compile(r"(?m)^\W*GATE\s+\d+")


def v3_root(model_id: str) -> Path:
    sub = "dag-v3-full" if MEMORY == "full" else "dag-v3"
    if EXPERIMENT:
        return PANEL_ROOT / "split-experiments" / EXPERIMENT / model_id / sub
    return PANEL_ROOT / model_id / sub


def chain_dir(model_id: str, persona: str) -> Path:
    """The chain-era lane, the only source a --borrow-history trial borrows from."""
    return PANEL_ROOT / model_id / "dag" / persona


def fact_model() -> str:
    return str(cold_read_config.load_config()["capture"]["fact_checkpoint"])


def fact_checkpoint(b: int) -> tuple[str, str]:
    """(body, provenance) of the shared grounded checkpoint at boundary b."""
    m = fact_model()
    # "consensus" = the slot-consensus fact memory (tools/fact_consensus.py).
    p = (REPO / "reviews" / "cold-read" / "fact-consensus" / f"ck-ch{b:03d}.md"
         if m == "consensus" else cold_read_config.checkpoint_path(m, b))
    if not p.exists():
        raise RuntimeError(
            f"missing grounded checkpoint {p.relative_to(REPO)} — mint it with "
            f"tools/cold_read_grounded.py (see reviews/cold-read/SPEC.md); "
            "the capture harness never mints facts itself")
    raw = p.read_text(encoding="utf-8")
    stale = fact_stale(b, raw)
    if stale:
        print(f"  STALE FACTS — {p.relative_to(REPO)} was minted from prose that has since "
              f"changed (chapters 1..{b}). A style edit leaves it true; a plot addition does "
              "not (SPEC 'Checkpoint staleness after a plot addition') — re-mint with "
              "tools/checkpoint_extract.py. Proceeding.", flush=True)
    # Facts only (author ruling 2026-11-01): the fact sections, with every sentence the
    # evidence audit did not establish as FACT removed. Her feelings come from her own
    # reactions and ledger, never from the extractor's Impression. The audit runs itself
    # on first use; if it fails, the read proceeds on the unaudited fact sections.
    import checkpoint_audit
    try:
        audit = checkpoint_audit.run_audit(p)
    except Exception as e:  # noqa: BLE001
        print(f"  audit of {p.name} failed ({e}); using unaudited fact sections", flush=True)
        audit = None
    body, note = checkpoint_audit.projection(p, audit)
    return (body, f"ck-ch{b:03d}@{m} ({note})" + (" (stale)" if stale else ""))


_FACT_STALE: dict[int, bool] = {}


def fact_stale(b: int, raw: str) -> bool:
    """Does the checkpoint's recorded bundle-sha256 still match the prose of 1..b?
    The bundle covers every chapter the checkpoint (and its seed) consolidated."""
    if b not in _FACT_STALE:
        recorded = checkpoint_bundle.checkpoint_metadata(raw, "bundle-sha256")
        current = hashlib.sha256(
            checkpoint_bundle.build_reader_bundle(b, start=1).encode()).hexdigest()
        _FACT_STALE[b] = recorded != current
    return _FACT_STALE[b]


def strip_header(text: str) -> str:
    """Drop the harness's provenance line; keep exactly what the reader wrote."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("*") and " · gate ch" in lines[0]:
        lines = lines[1:]
    return "\n".join(lines).strip()


def split_ledger(text: str) -> tuple[str, str]:
    """(everything before the LEDGER heading, the LEDGER lines)."""
    heads = list(LEDGER_HEAD_RE.finditer(text))
    if not heads:
        return text.strip(), ""
    h = heads[-1]
    return text[:h.start()].strip(), text[h.end():].strip()


def gate_block(text: str) -> str:
    body, _ = split_ledger(strip_header(text))
    hits = list(GATE_LINE_RE.finditer(body))
    return body[hits[-1].start():].strip() if hits else body


def history_source(d: Path, model_id: str, persona: str, i: int) -> tuple[Path, bool] | None:
    """(gate file for chapter i, borrowed?) — the v3 gate, else the chain gate if
    the run borrows history. None if neither exists."""
    own = gate_path(d, i)
    if own.exists():
        return own, False
    if BORROW:
        b = gate_path(chain_dir(model_id, persona), i)
        if b.exists():
            return b, True
    return None


def history(d: Path, model_id: str, persona: str, n: int) -> tuple[str, list[int]]:
    """WHAT I SAID for chapters 1..n-1, plus the chapters that were borrowed."""
    vol = checkpoint_bundle.volume_scenes.volume_of(slugs()[n - 1])
    parts, borrowed, missing = [], [], []
    for i in range(1, n):
        src = history_source(d, model_id, persona, i)
        if src is None:
            missing.append(i)
            continue
        path, was_borrowed = src
        if was_borrowed:
            borrowed.append(i)
        text = path.read_text(encoding="utf-8")
        title = checkpoint_bundle.display_title(slugs()[i - 1])
        if checkpoint_bundle.volume_scenes.volume_of(slugs()[i - 1]) == vol:
            body, _ = split_ledger(strip_header(text))
        else:
            body = gate_block(text)
        parts.append(f"--- chapter {i}: {title} ---\n{body}\n")
    if missing:
        raise RuntimeError(
            f"no reaction on file for chapter(s) {missing[:8]}{'…' if len(missing) > 8 else ''} "
            f"in {d.relative_to(REPO)} — read from chapter 1, or pass --borrow-history "
            "for a diagnostic that borrows the chain-era reactions")
    return "\n".join(parts), borrowed


class Ledger:
    """Folded deterministically from the seed and the per-gate deltas. Never summarised."""

    def __init__(self):
        self.items: dict[str, dict] = {}
        self.unmatched: list[str] = []

    def _new_id(self, kind: str, born: int) -> str:
        k = 1 + sum(1 for i in self.items if i.split(".")[0][1:] == str(born))
        return f"{LEDGER_KINDS[kind]}{born}.{k}"

    def add(self, kind: str, born: int, text: str, status: str | None = None,
            at: int | None = None) -> None:
        kind = kind.upper()
        iid = self._new_id(kind, born)
        self.items[iid] = {"kind": kind, "born": born, "text": text.strip(), "history": []}
        if status:
            self.items[iid]["history"].append((at or born, status.upper(), ""))

    def update(self, iid: str, status: str, text: str, at: int) -> None:
        iid = iid.upper()
        if iid not in self.items:
            self.unmatched.append(f"ch{at} ~ {iid} {status}: {text}")
            return
        self.items[iid]["history"].append((at, status.upper(), text.strip()))

    def apply(self, lines: str, at: int) -> None:
        for line in lines.splitlines():
            if m := UPDATE_RE.match(line):
                self.update(m.group(1), m.group(2), m.group(3), at)
            elif m := ADD_RE.match(line):
                self.add(m.group(1), at, m.group(2))

    def apply_seed(self, lines: str) -> None:
        for line in lines.splitlines():
            if m := SEED_RE.match(line):
                kind, born, status, at, text = m.groups()
                self.add(kind, int(born), text, status, int(at) if at else None)

    @staticmethod
    def settled(item: dict) -> bool:
        return any(s in SETTLED_STATUSES for _, s, _ in item["history"])

    def render(self) -> str:
        def line(iid, it):
            out = [f"[{iid}] {it['kind']}, since ch{it['born']}: {it['text']}"]
            out += [f"    ch{at} {s}" + (f": {t}" if t else "") for at, s, t in it["history"]]
            return "\n".join(out)
        open_ = [line(i, it) for i, it in self.items.items() if not self.settled(it)]
        done = [line(i, it) for i, it in self.items.items() if self.settled(it)]
        parts = ["Open:", *(open_ or ["(nothing yet)"])]
        if done:
            parts += ["", "Settled:", *done]
        return "\n".join(parts)


def seed_path(d: Path, k: int) -> Path:
    return d / f"ledger-seed-ch{k:03d}.md"


def ledger_for(d: Path, model_id: str, persona: str, n: int) -> tuple[Ledger, str]:
    """The ledger as of chapter n-1: the newest seed at or before n-1 whose later
    chapters are all v3 gates, then every v3 gate's deltas after it."""
    led, note = Ledger(), "no seed"
    seeds = sorted((int(p.stem[-3:]), p) for p in d.glob("ledger-seed-ch*.md"))
    k0 = 0
    for k, p in reversed(seeds):
        if k <= n - 1 and all(gate_path(d, i).exists() for i in range(k + 1, n)):
            _, lines = split_ledger(p.read_text(encoding="utf-8"))
            led.apply_seed(lines)
            k0, note = k, f"seed ch{k:03d}"
            break
    for i in range(k0 + 1, n):
        gp = gate_path(d, i)
        if gp.exists():
            _, lines = split_ledger(strip_header(gp.read_text(encoding="utf-8")))
            led.apply(lines, i)
    return led, note


def seed_prompt(model_id: str, persona: str, k: int) -> str:
    d = v3_root(model_id) / persona
    parts = ["===== WHAT I SAID — your reactions, verbatim =====\n"]
    for i in range(1, k + 1):
        src = history_source(d, model_id, persona, i)
        if src is None:
            raise RuntimeError(f"no reaction on file for chapter {i} to seed the ledger from")
        body, _ = split_ledger(strip_header(src[0].read_text(encoding="utf-8")))
        title = checkpoint_bundle.display_title(slugs()[i - 1])
        parts.append(f"--- chapter {i}: {title} ---\n{body}\n")
    parts.append(f"Write your LEDGER as it stands after chapter {k}.")
    return "\n".join(parts)


def read_prompt_v3(d: Path, model_id: str, persona: str, n: int) -> tuple[str, str]:
    """(prompt, memory provenance for the gate header)."""
    b = boundary(n)
    parts = [jacket_block(n)]
    if MEMORY == "full":
        if n > 1:
            parts.append(f"===== THE BOOK SO FAR (chapters 1–{n - 1}) =====\n")
            parts += [chapter_block(i) for i in range(1, n)]
        facts = f"raw ch001..ch{n - 1:03d}" if n > 1 else "none"
    else:
        facts = "none"
        if b:
            body, facts = fact_checkpoint(b)
            parts.append(f"===== WHAT HAPPENED (a record of the story through chapter {b}) "
                         f"=====\n\n{body}\n")
        if n - 1 > b:
            facts += f" + raw ch{b + 1:03d}..ch{n - 1:03d}"
    said, borrowed = history(d, model_id, persona, n) if n > 1 else ("", [])
    if said:
        parts.append("===== WHAT I SAID (your own reactions, verbatim: everything for "
                     "this volume, the gate notes for earlier ones) =====\n\n" + said)
    led, note = ledger_for(d, model_id, persona, n)
    if n > 1:
        parts.append(f"===== MY LEDGER (as of chapter {n - 1}) =====\n\n{led.render()}\n")
    if MEMORY != "full" and n - 1 > b:
        parts.append("===== RECENT CHAPTERS (raw, still fresh) =====\n")
        parts += [chapter_block(i) for i in range(b + 1, n)]
    parts.append("===== THE NEW CHAPTER =====\n")
    parts.append(chapter_block(n))
    parts.append(f"Read chapter {n} and produce your REACTION, then your single gate "
                 "block, then your LEDGER.")
    prompt = "\n".join(parts)
    hist = f"history ch001..ch{n - 1:03d}" if n > 1 else "history none"
    if borrowed:
        hist += f" (borrowed from chain ch{borrowed[0]:03d}..ch{borrowed[-1]:03d})"
    lsha = hashlib.sha256(led.render().encode()).hexdigest()[:12]
    prov = f"memory {MEMORY}: facts {facts} · {hist} · ledger {note} {lsha}"
    if led.unmatched:
        print(f"  ledger: {len(led.unmatched)} update(s) name an unknown id "
              f"(first: {led.unmatched[0]})", flush=True)
    return prompt, prov


def ensure_seed(model_id: str, persona: str, agent_fn, n: int) -> None:
    """A borrowed-history trial needs a ledger the chain gates never wrote: one call
    over her verbatim reactions (one hop from raw, never re-summarised after)."""
    d = v3_root(model_id) / persona
    k = n - 1
    while k > 0 and gate_path(d, k).exists():
        k -= 1
    if k == 0 or seed_path(d, k).exists():
        return
    sys_text, sha = sysprompt(persona, "core-ledger-seed.md")
    label = f"{model_id}·{persona}·ledger-seed-ch{k:02d}"
    raw = agent_fn(sys_text, seed_prompt(model_id, persona, k), label).strip()
    if not SEED_RE.search(raw.replace("\r", "")) and "LEDGER" not in raw.upper():
        raise RuntimeError(f"malformed ledger seed for {label} — {save_raw(d, k, label, raw)}")
    write_doc(seed_path(d, k), f"*{PROTOCOL_V3} · ledger seed ch{k:03d} · {model_id} · "
                               f"{persona} · prompt-sha {sha} · from borrowed chain reactions "
                               f"ch001..ch{k:03d} · {date.today().isoformat()}*", raw)
    print(f"  seed {label}", flush=True)


def clean_markdown(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n"


def save_raw(d: Path, n: int, label: str, raw: str) -> str:
    """Preserve a rejected response so a failure is diagnosable.

    A gate is rejected on a missing DECISION line, and the raw text used to be
    dropped on the floor — which costs a paid call and returns nothing to look
    at. The common causes leave distinct fingerprints: an empty body means the
    reasoning budget consumed `max_output_tokens` before any visible output, a
    body that stops mid-sentence means the same cap hit late, and a body that
    reads fine but lacks the heading means the model answered in its own
    format. They need different fixes, so keep the evidence.

    Written under `.failed/` (gitignored by the capture-panel rules) rather
    than beside the gates, so a rejected artifact can never be mistaken for a
    reader's actual reaction.
    """
    out = d / ".failed" / f"gate-ch{n:03d}-{date.today().isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"*REJECTED gate · {label} · {len(raw)} chars*\n\n{raw}\n",
                   encoding="utf-8")
    return f"{len(raw)} chars saved to {out.relative_to(REPO)}" if raw \
        else f"EMPTY response; marker at {out.relative_to(REPO)}"


def write_doc(path: Path, header: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{header}\n\n{clean_markdown(body)}", encoding="utf-8")


def run_reader(model_id: str, persona: str, agent_fn, to_n: int,
               fresh: int | None = None, start: int = 1) -> str:
    """Sequential chapters 1..to_n with decade mints. agent_fn(system, prompt, label).

    `fresh` names a single chapter whose existing gate (and decade mint, if it
    sits on a boundary) is overwritten instead of resumed past — the re-read of
    a revised chapter. Scoped to one chapter on purpose: the run's scope is the
    whole range 1..to_n, so a blanket refresh would re-read the entire book."""
    if MEMORY != "chain":
        return run_reader_v3(model_id, persona, agent_fn, to_n, fresh, start)
    d = dag_dir(model_id, persona)
    stopped = d / "STOPPED"
    read_frame, mint_frame = PERSONA_FRAMES.get(persona, ("core-chapter.md", "core-mint.md"))
    read_sys, read_sha = sysprompt(persona, read_frame)
    mint_sys, mint_sha = sysprompt(persona, mint_frame)
    if start > 1:
        b0 = boundary(start)
        if b0 and not ck_path(d, b0).exists():
            return (f"{model_id}·{persona}: --from {start} needs ck-ch{b0:03d} in {d} "
                    "(a diagnostic start borrows or pre-mints it; nothing was read)")
    for n in range(start, to_n + 1):
        if stopped.exists():
            return f"{model_id}·{persona}: stopped earlier"
        gp = gate_path(d, n)
        if not gp.exists() or n == fresh:
            label = f"{model_id}·{persona}·ch{n:02d}"
            raw = agent_fn(read_sys, read_prompt(d, n), label).strip()
            if "DECISION" not in raw.upper():
                raise RuntimeError(f"malformed gate for {label}"
                                   f" — {save_raw(d, n, label, raw)}")
            write_doc(gp, f"*{PROTOCOL} · gate ch{n:03d} · {model_id} · {persona} · "
                          f"prompt-sha {read_sha} · prose-sha {chapter_sha(n)}{variant_tag()} · "
                          f"{date.today().isoformat()}*", raw)
            print(f"  gate {label}", flush=True)
        if re.search(r"DECISION:\s*STOP", gp.read_text(), re.I):
            stopped.write_text(f"stopped at ch{n:03d}\n")
            print(f"  STOP {model_id}·{persona} at ch{n}", flush=True)
            return f"{model_id}·{persona}: STOPPED at ch{n}"
        if n % DECADE == 0:
            cp = ck_path(d, n)
            if not cp.exists() or n == fresh:
                label = f"{model_id}·{persona}·mint-ch{n:02d}"
                raw = agent_fn(mint_sys, mint_prompt(d, n), label).strip()
                if len(raw) < 800:
                    raise RuntimeError(f"suspiciously short mint for {label}")
                write_doc(cp, f"*{PROTOCOL} · carry-forward ck-ch{n:03d} · {model_id} · "
                              f"{persona} · prompt-sha {mint_sha}{variant_tag()} · "
                              f"{date.today().isoformat()}*", raw)
                print(f"  mint {label}", flush=True)
    return f"{model_id}·{persona}: through ch{to_n}"


def run_reader_v3(model_id: str, persona: str, agent_fn, to_n: int,
                  fresh: int | None = None, start: int = 1) -> str:
    """The v3 loop: no mints. A STOP still ends the reader."""
    if persona in PERSONA_FRAMES:
        raise RuntimeError(f"{persona} reads through its own frame; v3 memory is for capture readers")
    d = dag_dir(model_id, persona)
    stopped = d / "STOPPED"
    read_sys, read_sha = sysprompt(persona, "core-chapter-v3.md")
    for n in range(start, to_n + 1):
        if stopped.exists():
            return f"{model_id}·{persona}: stopped earlier"
        gp = gate_path(d, n)
        if not gp.exists() or n == fresh:
            if BORROW and n > 1:
                ensure_seed(model_id, persona, agent_fn, n)
            label = f"{model_id}·{persona}·ch{n:02d}·{MEMORY}"
            prompt, prov = read_prompt_v3(d, model_id, persona, n)
            raw = agent_fn(read_sys, prompt, label).strip()
            if "DECISION" not in raw.upper():
                raise RuntimeError(f"malformed gate for {label}"
                                   f" — {save_raw(d, n, label, raw)}")
            if not LEDGER_HEAD_RE.search(raw):
                print(f"  note: {label} wrote no LEDGER", flush=True)
            write_doc(gp, f"*{PROTOCOL_V3}-{MEMORY} · gate ch{n:03d} · {model_id} · {persona} · "
                          f"prompt-sha {read_sha} · prose-sha {chapter_sha(n)}{variant_tag()} · "
                          f"{prov} · {date.today().isoformat()}*", raw)
            print(f"  gate {label} (~{len(prompt) // 4} tokens in)", flush=True)
        if re.search(r"DECISION:\s*STOP", gp.read_text(), re.I):
            stopped.write_text(f"stopped at ch{n:03d}\n")
            print(f"  STOP {model_id}·{persona} at ch{n}", flush=True)
            return f"{model_id}·{persona}: STOPPED at ch{n}"
    return f"{model_id}·{persona}: through ch{to_n}"


# model id -> OpenRouter provider model, read from ensemble-config.toml reader blocks.
OPENROUTER_MODELS = cold_read_config.openrouter_models()
OR_MAX_OUTPUT = 16000   # checkpoint mints run ~3.6k visible; the rest is reasoning headroom
OR_TIMEOUT = 900.0


def make_agent(model_id: str, effort: str):
    """Return (agent_fn(system,prompt,label), close())."""
    if model_id.startswith(authorship_audit.CLAUDE_PREFIX):
        def fn(system, prompt, label):
            return authorship_audit.run_claude(model_id, system, prompt, label)
        return fn, (lambda: None)
    import cold_read
    if model_id in OPENROUTER_MODELS:
        import os
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("OPENROUTER_API_KEY not set in the environment.")
        selector = OPENROUTER_MODELS[model_id]
        holders = {}

        def fn(system, prompt, label):
            k = hashlib.sha256(system.encode()).hexdigest()[:8]
            if k not in holders:
                holders[k] = cold_read.make_openrouter_agent_fn(
                    system_prompt=system, policy="capture", effort=effort, api_key=key)
            r = holders[k](prompt=prompt, model=selector, label=label) or {}
            return r.get("output") or ""
        return fn, (lambda: None)
    # codex: developer_instructions fixed per thread factory -> make per-call factories
    holders = {}

    def fn(system, prompt, label):
        key = hashlib.sha256(system.encode()).hexdigest()[:8]
        if key not in holders:
            holders[key] = cold_read.make_codex_agent_fn(system_prompt=system, effort=effort)
        f, _ = holders[key]
        return (f(prompt=prompt, model=model_id, label=label) or {}).get("output") or ""

    def close():
        for _, c in holders.values():
            c()
    return fn, close


def assemble(model_id: str, persona: str) -> Path:
    d = dag_dir(model_id, persona)
    parts = []
    for n in range(1, len(slugs()) + 1):
        gp = gate_path(d, n)
        if gp.exists():
            parts.append(clean_markdown(gp.read_text(encoding="utf-8")).rstrip())
        if n % DECADE == 0 and ck_path(d, n).exists():
            parts.append(
                "\n----- CARRY-FORWARD MINTED AFTER CHAPTER "
                f"{n} -----\n"
                + clean_markdown(ck_path(d, n).read_text(encoding="utf-8")).rstrip()
            )
    out = PANEL_ROOT / model_id / f"{persona}--volume-dag.md"
    out.write_text(
        f"# Capture DAG record — {persona}\n\n*model: {model_id} · protocol: "
        f"{PROTOCOL} · assembled {date.today().isoformat()}*\n\n"
        + "\n".join(parts)
        + "\n",
        encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+", required=True,
                    help="capture roster ids from ensemble-config.toml [capture].models")
    ap.add_argument("--allow-retired", action="store_true",
                    help="permit a model listed in [capture].retired (an explicit author request)")
    ap.add_argument("--personas", nargs="*", default=PERSONAS, choices=ALL_PERSONAS)
    ap.add_argument("--from", dest="start", type=int, default=1,
                    help="diagnostic: start the sequential read at this chapter instead of 1; "
                         "the lane must already hold the boundary checkpoint below it")
    ap.add_argument("--to", type=int, default=N_CH)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--fresh", action="store_true",
                    help="re-read the target chapter (--to N), overwriting its existing "
                         "gate and, on a decade boundary, re-minting its carry-forward")
    ap.add_argument("--check-stale", action="store_true",
                    help="report which existing gates were minted from prose that has "
                         "since changed, then exit. Costs no tokens.")
    ap.add_argument("--experiment", metavar="NAME",
                    help="write to reviews/capture-panel/split-experiments/NAME/ "
                         "instead of the real lanes (never read by capture_stats)")
    ap.add_argument("--dated", action="store_true",
                    help="experiments only: add chapter_dates lines (the real lanes are always dated)")
    ap.add_argument("--undated", action="store_true",
                    help="experiments only: read without date lines (the default for experiments)")
    ap.add_argument("--show-packet", type=int, metavar="N",
                    help="print chapter N as the reader would see it, then exit (no calls)")
    ap.add_argument("--memory", choices=["chain", "grounded", "full"], default="chain",
                    help="chain = the decade-mint lanes in dag/; grounded = memory v3 "
                         "(grounded fact checkpoint + her verbatim reactions + ledger) in "
                         "dag-v3/; full = v3 with the raw book in place of the checkpoint "
                         "(pre-pub reads), in dag-v3-full/")
    ap.add_argument("--borrow-history", action="store_true",
                    help="v3 diagnostic: where the v3 lane has no gate, use the chain-era "
                         "reaction, and seed the ledger from those reactions (one call)")
    ap.add_argument("--show-prompt", type=int, metavar="N",
                    help="v3: print the assembled prompt for chapter N of the first "
                         "model/persona and its token estimate, then exit (no calls)")
    args = ap.parse_args()

    global EXPERIMENT, DATED, MEMORY, BORROW
    EXPERIMENT = args.experiment
    MEMORY = args.memory
    BORROW = args.borrow_history
    if BORROW and MEMORY == "chain":
        raise SystemExit("--borrow-history is for --memory grounded|full")
    if not EXPERIMENT and args.undated:
        raise SystemExit("--undated requires --experiment: the real lanes read the book as it ships, dated")
    DATED = args.dated if EXPERIMENT else True
    if args.show_packet:
        print(chapter_block(args.show_packet))
        return
    if args.show_prompt:
        if MEMORY == "chain":
            raise SystemExit("--show-prompt is for --memory grounded|full")
        m, p = args.models[0], args.personas[0]
        prompt, prov = read_prompt_v3(dag_dir(m, p), m, p, args.show_prompt)
        print(prompt)
        print(f"\n[{prov} · ~{len(prompt) // 4} tokens]", file=sys.stderr)
        return

    if args.assemble:
        for m in args.models:
            for p in args.personas:
                print(assemble(m, p))
        return

    # The roster lives in ensemble-config.toml [capture]; anything else is drift.
    roster = set(cold_read_config.capture_models(include_available=True))
    retired_models = set(cold_read_config.capture_retired())
    unknown = [m for m in args.models if m not in roster and m not in retired_models]
    if unknown:
        raise SystemExit(
            f"unknown capture model(s): {', '.join(unknown)}. Add them to "
            "reviews/cold-read/ensemble-config.toml [capture].models first — that file "
            "is the single roster for both instruments.")
    off_roster = [m for m in args.models if m in retired_models]
    if off_roster and not args.allow_retired:
        raise SystemExit(
            f"refusing to run retired capture model(s): {', '.join(off_roster)} "
            "(ensemble-config.toml [capture].retired). Pass --allow-retired if the "
            "author has named the model for this run.")

    # Retired personas must not be run again.
    retired = [p for p in args.personas if p in RETIRED_PERSONAS]
    if retired:
        raise SystemExit(
            f"refusing to run retired persona(s): {', '.join(retired)}. "
            "Retired by author ruling (see RETIRED_PERSONAS); her gates were erased "
            "2026-09-26. Reviving one needs author approval.")

    # Staleness is a warning, never a gate. A style edit to an early chapter must not
    # force a re-read of every downstream chapter; report the tiers and proceed.
    print_stale_report(stale_report(args.models, list(args.personas), args.to))
    if MEMORY == "grounded":
        for b in sorted({boundary(n) for n in range(max(args.start, 1), args.to + 1)} - {0}):
            p = (REPO / "reviews" / "cold-read" / "fact-consensus" / f"ck-ch{b:03d}.md"
                 if fact_model() == "consensus"
                 else cold_read_config.checkpoint_path(fact_model(), b))
            if p.exists() and fact_stale(b, p.read_text(encoding="utf-8")):
                print(f"  STALE FACTS: {p.relative_to(REPO)} predates a prose change in "
                      f"ch1..{b} (re-mint after a plot addition)", flush=True)
    if args.check_stale:
        return

    results, failures = [], []

    def one(m, p):
        fn, close = make_agent(m, args.effort)
        try:
            results.append(run_reader(m, p, fn, args.to,
                                      args.to if args.fresh else None,
                                      start=args.start))
        except Exception as e:  # noqa: BLE001
            failures.append(f"{m}·{p}: {e}")
            print(f"  FAIL {m}·{p}: {e}", flush=True)
        finally:
            close()

    readers = [(m, p) for m in args.models for p in args.personas]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda t: one(*t), readers))

    print("\n".join(results))
    if args.fresh and MEMORY == "chain" and not EXPERIMENT:
        print(f"\nRe-read done. Before committing these gates, run "
              f"`tools/capture_delta.py --chapter {args.to}` (SPEC rule 3b) and report it.",
              flush=True)
    if failures:
        print("failures:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
