#!/usr/bin/env python3
"""Batch cold-read runner for OMP/eval bridge.

Usage examples:
  python3 tools/cold_read_batch.py --model openrouter/x-ai/grok-4.5 --model-id grok-4.5 --scope fall
  python3 tools/cold_read_batch.py --model openai-codex/gpt-5.6-sol --model-id gpt-5.6-sol --scope fall --resume

This script is driven from an OMP eval cell that provides `agent(...)`.
It is intentionally importable; call `run_batch(...)` from eval.

Not a standalone CLI without the eval bridge.
"""

from __future__ import annotations

import json
import re
import time
import tomllib
from pathlib import Path

MIN_PROSE_CHARS = 500
PROSE_PLACEHOLDERS = ("verbatim stdout", "command output above", "the command output above")
REFUSAL_MARKERS = (
    "no chapter text",
    "cannot review this chapter",
    "can't review this chapter",
    "no page here",
    "chapter text missing",
    "chapter text was missing",
    "chapter text not provided",
    "re-run with the actual chapter",
)

FALL_SCENES = [
    {"title": "The Bench", "slug": "the-bench", "volume_start": 1},
    {"title": "Standards", "slug": "standards"},
    {"title": "The Pointing Game", "slug": "the-pointing-game"},
    {"title": "See You Later", "slug": "see-you-later"},
    {"title": "Substitution", "slug": "substitution"},
    {"title": "The Long Way", "slug": "long-way"},
    {"title": "Water Wings", "slug": "water-wings"},
    {"title": "May I Choose", "slug": "may-i-choose"},
    {"title": "Off Six-Fourteen", "slug": "off-six-fourteen"},
    {"title": "Dear", "slug": "dear"},
    {"title": "Leave No Trace", "slug": "leave-no-trace"},
    {"title": "Rye", "slug": "rye"},
    {"title": "What to Wear", "slug": "what-to-wear"},
    {"title": "Two Towels", "slug": "two-towels"},
    {"title": "A Round", "slug": "a-round"},
    {"title": "Turned Up", "slug": "turned-up"},
    {"title": "How It's Done", "slug": "how-its-done"},
    {"title": "Famished", "slug": "famished"},
    {"title": "Toenails", "slug": "toenails"},
    {"title": "Fed", "slug": "fed"},
    {"title": "Peekaboo", "slug": "peekaboo"},
    {"title": "All Told", "slug": "all-told"},
    {"title": "Sorority", "slug": "sorority"},
    {"title": "Gone", "slug": "gone"},
    {"title": "Rock", "slug": "rock"},
    {"title": "Lesson", "slug": "lesson"},
    {"title": "Broken In", "slug": "broken-in"},
    {"title": "Hills and Valleys", "slug": "hills-and-valleys"},
    {"title": "A Recognized Method", "slug": "recognized-method"},
    {"title": "The Practice Room", "slug": "practice-room"},
    {"title": "The Induction", "slug": "the-induction"},
    {"title": "We Find Out", "slug": "we-find-out"},
    {"title": "Made-Up", "slug": "made-up"},
    {"title": "One Bite", "slug": "one-bite"},
    {"title": "Above Him", "slug": "above-him"},
    {"title": "School Nights", "slug": "school-nights"},
    {"title": "In His Hands", "slug": "in-his-hands"},
    {"title": "All the Time", "slug": "all-the-time"},
    {"title": "The Outlier", "slug": "outlier"},
    {"title": "The New Ordinary", "slug": "new-ordinary"},
    {"title": "Cropped", "slug": "cropped"},
    {"title": "Seconds", "slug": "seconds"},
    {"title": "Under the Rug", "slug": "under-the-rug"},
    {"title": "Bare", "slug": "bare"},
    {"title": "Believe Me", "slug": "believe-me"},
    {"title": "Fairytale", "slug": "fairytale"},
    {"title": "Old Acquaintances", "slug": "old-acquaintances"},
    {"title": "The Usual", "slug": "the-usual"},
    {"title": "My Friend Randi", "slug": "my-friend-randi"},
    {"title": "Nothing Underneath", "slug": "nothing-underneath"},
    # Spring (Volume Two) drafted scenes — appended in story order so scoped runs
    # can reach them; the list name predates the volume split.
    {"title": "Among Friends", "slug": "among-friends", "volume_start": 2},
    {"title": "Another Round", "slug": "another-round"},
]


VOLUME_PACKETS = Path("reviews/_harness/volume-packets.toml")


def load_volume_packets() -> dict[int, dict]:
    data = tomllib.loads(VOLUME_PACKETS.read_text()).get("volumes", {})
    return {int(volume): packet for volume, packet in data.items()}

READER_PROTOCOL = "v2-volume-entry-jacket"
LEGACY_PROTOCOL = "v1-repeated-jacket-legacy"

def clean_scene_text(slug: str) -> str:
    raw = Path(f"scenes/{slug}.md").read_text()
    lines = raw.splitlines()
    start = 0
    if lines and lines[0].startswith("# "):
        start = 1
    divider = None
    for i in range(start, min(len(lines), start + 12)):
        if lines[i].strip() == "---":
            divider = i
            break
    body = lines[divider + 1 :] if divider is not None else lines[start:]
    if divider is None:
        while body and not body[0].strip():
            body.pop(0)
        if body and body[0].lstrip().startswith("*"):
            body.pop(0)
    body = [ln for ln in body if not ln.lstrip().startswith("[AI")]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    text = "\n".join(body)
    if "[AI" in text:
        raise RuntimeError(f"AI marker survived in {slug}")
    return text


def parse_response(raw_output):
    parsed = raw_output
    if isinstance(raw_output, str):
        try:
            parsed = json.loads(raw_output)
        except Exception:
            parsed = raw_output
    if isinstance(parsed, dict):
        return (
            parsed.get("response")
            or parsed.get("text")
            or parsed.get("output")
            or json.dumps(parsed, ensure_ascii=False, indent=2)
        ).strip()
    return str(parsed).strip()


def split_reader(text: str):
    carry_pattern = re.compile(
        r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?Carry[- ]forward state:?(?:\*\*)?\s*$"
    )
    matches = list(carry_pattern.finditer(text))
    if not matches:
        return text.strip(), ""
    m = matches[0]
    before = text[: m.start()].strip()
    after = text[m.end() :].strip()
    reader_pattern = re.compile(
        r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?Reader reaction:?(?:\*\*)?\s*$"
    )
    before = reader_pattern.sub("", before, count=1).strip()
    return before, after


def extract_usage(agent_id: str):
    sessions = Path.home() / ".omp/agent/sessions"
    matches = list(sessions.rglob(f"{agent_id}.jsonl"))
    if not matches:
        return None
    p = max(matches, key=lambda x: x.stat().st_mtime)
    totals = {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0,
        "totalTokens": 0,
        "reasoningTokens": 0,
        "cost": 0.0,
        "promptTokens": 0,
        "nonMessageTokens": 0,
        "duration_ms": 0.0,
        "turns": 0,
        "jsonl": str(p),
    }
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("type") != "message":
            continue
        m = r.get("message") or {}
        if m.get("role") != "assistant" or "usage" not in m:
            continue
        u = m["usage"]
        c = u.get("cost") or {}
        totals["input"] += u.get("input") or 0
        totals["output"] += u.get("output") or 0
        totals["cacheRead"] += u.get("cacheRead") or 0
        totals["cacheWrite"] += u.get("cacheWrite") or 0
        totals["totalTokens"] += u.get("totalTokens") or 0
        totals["reasoningTokens"] += u.get("reasoningTokens") or 0
        totals["cost"] += float((c.get("total") if isinstance(c, dict) else 0) or 0)
        totals["duration_ms"] += float(m.get("duration") or 0)
        totals["turns"] += 1
        cs = m.get("contextSnapshot") or {}
        pt = cs.get("promptTokens") or 0
        if pt >= totals["promptTokens"]:
            totals["promptTokens"] = pt
            totals["nonMessageTokens"] = cs.get("nonMessageTokens") or 0
    return totals


def has_valid_review(path: Path) -> bool:
    if not path.exists():
        return False
    txt = path.read_text()
    if f"reader-protocol: {READER_PROTOCOL}" not in txt:
        return False
    if "## Carry-forward state" not in txt:
        return False
    return bool(txt.split("## Carry-forward state", 1)[1].strip())


# The reaction's structured block (Cast present / Heat / Romance / Motifs /
# Symbolism / Characterization / Pace) belongs under `## Reader reaction`. Models
# intermittently emit it AFTER the carry-forward heading instead — observed 3x in
# 9 gpt-5.6-terra runs. split_reader() then faithfully files it under the wrong
# section, and na.py (which indexes ONLY `## Reader reaction`) silently loses the
# Heat/Romance ratings for that chapter. Repair it here so it cannot reach disk.
_BLOCK_START = re.compile(r"(?im)^\s*(?:#{1,4}\s*)?\*\*(?:Cast present|Heat|Romance)\b")
_LEDGER_START = re.compile(
    r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?"
    r"(?:Who.s who|Motif & image ledger|Symbolism noticed|Open questions|"
    r"Running memory|Story so far|How I feel|Principals|Relationship ledger|"
    r"What I know that they don[''’]t|Motifs)\b"
)

_CHAPTER_RECORD_RE = re.compile(
    r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?Chapter record:?(?:\*\*)?\s*$"
)


def forward_carry(carry: str) -> str:
    """The part of the carry-forward the next reader receives.

    The Chapter record is written to the review file but never chained
    forward — it is per-chapter continuity detail, deliberately not part of
    reader memory.
    """
    if not carry:
        return carry
    m = _CHAPTER_RECORD_RE.search(carry)
    return carry[: m.start()].rstrip() if m else carry


def relocate_structured_block(reader: str, carry: str):
    """Move a misplaced structured block from the carry-forward back into the
    reaction. Returns (reader, carry, moved: bool). No-op when placement is fine."""
    if not carry.strip() or _BLOCK_START.search(reader or ""):
        return reader, carry, False
    if not _BLOCK_START.match(carry.lstrip("\n")):
        return reader, carry, False
    ledger = _LEDGER_START.search(carry)
    if not ledger:
        # Whole carry-forward looks like a structured block — that is a genuinely
        # malformed response, not a misplacement. Leave it for the caller to reject.
        return reader, carry, False
    block = carry[: ledger.start()].strip()
    remainder = carry[ledger.start() :].strip()
    if not block or not remainder:
        return reader, carry, False
    return f"{reader.rstrip()}\n\n### Structured block\n\n{block}", remainder, True


# Retention enforcement. SPEC and blind-reader.md already forbid both of these in
# prose, and readers violate them anyway: claude-fable-5 dropped named characters
# (including Vee's own surname and Brooke) at 7 points in chs.1-8, and collapsed 35
# motifs into "— all as previously logged", stripping every appearance trail and
# pointing at files the next reader never sees. A dropped fact is silently
# unrecoverable: the next reader has ONLY this ledger. So check it in code.
_POINTER_RE = re.compile(
    r"(?i)(as previously logged|previously logged|all prior (?:entries|questions) stand"
    r"|all (?:prior|earlier) \w+ (?:stand|remain)|unchanged from (?:the )?prior)"
)


def _cast_names(carry: str) -> set:
    """Names in the who's-who section, lowercased."""
    if not carry:
        return set()
    head = re.search(r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?(?:Who.s who|Principals)\b.*$", carry)
    if not head:
        return set()
    rest = carry[head.end():]
    nxt = _LEDGER_START.search(rest)
    section = rest[: nxt.start()] if nxt else rest
    return {n.strip().lower() for n in re.findall(r"^[-*]\s+\*\*([^*]+?)\*\*", section, re.M)}


def _norm_apos(s: str) -> str:
    """Fold curly apostrophes to straight.

    Models write "Vee's mother" with U+2019 far more often than U+0027, while
    principals.toml is hand-written with the straight form. Without this the
    retention check reports a false dropped-principal and burns a paid retry.
    """
    return s.replace("’", "'").replace("ʼ", "'")


# Old-format (v1) ledgers predate the Principals / Relationship ledger spec.
# Any one of these headings marks a carry-forward as v1, so the new
# structural checks are skipped rather than failing a legitimate legacy chain.
_LEGACY_HEADINGS = re.compile(
    r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?"
    r"(?:Who.s who|Motif & image ledger|Running memory|Story so far)\b"
)


def _is_legacy_carry(carry: str) -> bool:
    if not carry:
        return False
    if _LEGACY_HEADINGS.search(carry):
        return True
    # Some models emit the v1 ledger without bolded headings at all; treat a
    # carry that has neither new-format anchor as legacy too.
    has_new = re.search(
        r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?(?:Principals|Relationship ledger)\b", carry
    )
    return not has_new


def _load_principals(path=None):
    """Never-drop names from reviews/_harness/principals.toml (canonical + aliases).

    The blind-reader never sees this file; its prompt states the rule
    functionally. Only the harness, which is not blind, knows the names.
    """
    import tomllib
    p = Path(path) if path else Path(__file__).resolve().parents[1] / "reviews" / "_harness" / "principals.toml"
    if not p.exists():
        return {}
    data = tomllib.loads(p.read_text(encoding="utf-8"))
    canon = [str(x).lower() for x in data.get("book", {}).get("principals", [])]
    aliases = {str(k).lower(): [str(v).lower() for v in vals]
               for k, vals in (data.get("aliases") or {}).items()}
    return {c: [c] + aliases.get(c, []) for c in canon}


def check_retention(prior_carry: str, new_carry: str, principals=None):
    """Retention violations (empty = clean).

    A principal becomes protected only after the previous reader-state contains
    them. Requiring every configured book principal from chapter one invents
    people before the reader has met them; this check detects only a genuine
    drop from the carried state.
    """
    problems = []
    if principals is None:
        principals = _load_principals()
    names = {_norm_apos(n) for n in _cast_names(new_carry)}
    blob = _norm_apos(new_carry.lower())
    prior_blob = _norm_apos(prior_carry.lower())
    missing = []
    for canon, forms in principals.items():
        forms = [_norm_apos(f) for f in forms]
        if not any(f in prior_blob for f in forms):
            continue
        if any(f in names for f in forms):
            continue
        # Fall back to a substring hit anywhere in the ledger before failing.
        if any(f in blob for f in forms):
            continue
        missing.append(canon)
    if missing:
        problems.append("dropped PRINCIPAL: " + ", ".join(sorted(missing)))

    if not _is_legacy_carry(new_carry):
        if not re.search(r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?What I know that they don['’]t", new_carry):
            problems.append("missing 'what I know that they don't' ledger")
        if not re.search(r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?Relationship ledger", new_carry):
            problems.append("missing relationship ledger")

    hits = sorted({m.group(0).lower() for m in _POINTER_RE.finditer(new_carry)})
    if hits:
        problems.append("pointer-style compression (strips trails): " + "; ".join(hits))
    return problems


def write_review(out_dir: Path, model_id: str, model_selector: str, scene, response_text, predecessor, provider_label: str = "OMP", protocol: str = READER_PROTOCOL):
    reader, carry = split_reader(response_text)
    reader, carry, moved = relocate_structured_block(reader, carry)
    if moved:
        print(
            json.dumps({"slug": scene["slug"], "repaired": "structured-block-relocated"}),
            flush=True,
        )
    if not reader or not carry:
        raise ValueError(
            f"missing sections for {scene['slug']}: reader={len(reader)} carry={len(carry)}"
        )
    path = out_dir / f"{scene['slug']}.md"
    predecessor_label = predecessor if predecessor else "— (opening, cold)"
    content = (
        f"# Cold read — {scene['title']}\n\n"
        f"*scene: scenes/{scene['slug']}.md · model: {model_id} ({provider_label}: {model_selector}) · "
        f"read after: {predecessor_label} · reader-protocol: {protocol}*\n\n"
        f"## Reader reaction\n\n{reader}\n\n"
        f"## Carry-forward state\n\n{carry}\n"
    )
    path.write_text(content)
    return path, forward_carry(carry)


# Four relationship axes as (positive-pole, negative-pole). Rotated per chapter so no
# axis sits permanently in the high-attention first slot and no valence always leads —
# debiasing the carry-forward hand-off. The reader defers to this AXIS ORDER line.
_AXES = [
    ("warmth", "cold"),
    ("belonging", "isolation"),
    ("cherished", "used"),
    ("desire hers", "desire worked-on-her"),
]


def axis_order_line(i: int) -> str:
    order = _AXES[i % 4:] + _AXES[: i % 4]      # rotate which axis leads
    flip = (i % 2) == 1                         # alternate which valence leads
    parts = [f"{b} ↔ {a}" if flip else f"{a} ↔ {b}" for a, b in order]
    return (
        "AXIS ORDER FOR THIS CHAPTER (record the four relationship axes in exactly this "
        "order, leading each with the pole named first): " + " · ".join(parts)
    )


def run_batch(
    *,
    agent_fn,
    model_selector: str,
    model_id: str,
    scenes=None,
    resume: bool = True,
    max_attempts: int = 5,
    allow_legacy_resume: bool = False,
    label_prefix: str = "BlindBatch",
    budget_usd: float | None = None,
    compactor=None,
    compaction_threshold: int = 18000,
    provider_label: str = "OMP",
):
    """agent_fn(prompt, model, label) -> result dict with output/text/id, and
    optionally a `usage` dict (input/output/cost/…). If `usage` is present it is
    used directly (the direct-API path); otherwise usage is read post-hoc from the
    OMP session jsonl via extract_usage().

    Cost safety: if `budget_usd` is set, the batch ABORTS (raises) the moment a
    scene's actual cost exceeds it, or a call comes back marked `incomplete`
    (hit its output cap). Combined with the caller's per-call max_output_tokens
    cap and a low `max_attempts`, this bounds per-scene spend."""
    def usable_review(path: Path) -> bool:
        return has_valid_review(path) or (allow_legacy_resume and path.exists())
    scenes = list(scenes or FALL_SCENES)
    out_dir = Path("reviews/_archive/cold-read") / model_id
    out_dir.mkdir(parents=True, exist_ok=True)
    volume_packets = load_volume_packets()

    carry = ""
    predecessor = None
    log = []

    # Seed carry-forward when the run starts mid-book (e.g. a scoped `gone..` run).
    # The first scene's predecessor lives outside `scenes`, so the reader would
    # otherwise read it cold as the opening. Load the predecessor's carry-forward
    # from its review on disk; refuse rather than fabricate an opening read.
    full_slugs = [s["slug"] for s in FALL_SCENES]
    if scenes and scenes[0]["slug"] in full_slugs and "volume_start" not in scenes[0]:
        pos = full_slugs.index(scenes[0]["slug"])
        if pos > 0:
            pred_slug = full_slugs[pos - 1]
            pred_file = out_dir / f"{pred_slug}.md"
            if not usable_review(pred_file):
                raise RuntimeError(
                    f"cannot seed carry-forward for {scenes[0]['slug']}: predecessor "
                    f"'{pred_slug}' has no review in {out_dir}. Start the run from the "
                    f"opening, or ensure {pred_slug}.md exists first."
                )
            carry = pred_file.read_text().split("## Carry-forward state", 1)[1].strip()
            predecessor = pred_slug

    for idx, scene in enumerate(scenes, 1):
        if "volume_start" in scene:
            carry = ""
            predecessor = None
        existing = out_dir / f"{scene['slug']}.md"
        if existing.exists() and not usable_review(existing) and resume:
            raise RuntimeError(
                f"review protocol mismatch for {scene['slug']} at {existing}; "
                "choose a new --model-id, explicitly regenerate with "
                "--fresh --allow-volume-one-rewrite, or pass --legacy-resume."
            )
        if resume and usable_review(existing):
            carry = existing.read_text().split("## Carry-forward state", 1)[1].strip()
            predecessor = scene["slug"]
            rec = {
                "slug": scene["slug"],
                "title": scene["title"],
                "path": str(existing),
                "status": "skipped-existing",
                "usage": None,
                "attempt": 0,
                "wall_s": 0,
            }
            log.append(rec)
            print(
                json.dumps(
                    {
                        "n": idx,
                        "of": len(scenes),
                        "slug": scene["slug"],
                        "status": "skipped-existing",
                        "carry_chars": len(carry),
                    }
                ),
                flush=True,
            )
            continue

        clean = clean_scene_text(scene["slug"])
        clean_lower = clean.strip().lower()
        if len(clean.strip()) < MIN_PROSE_CHARS or any(
            ph in clean_lower for ph in PROSE_PLACEHOLDERS
        ):
            raise RuntimeError(
                f"prose guard: {scene['slug']} yielded empty/placeholder chapter text "
                f"({len(clean.strip())} chars) — refusing to feed it to the reader."
            )
        prior_block = carry if carry.strip() else "empty — opening chapter"
        if predecessor and not carry.strip():
            raise RuntimeError(f"empty prior carry before {scene['slug']}")
        packet_block = ""
        if "volume_start" in scene:
            volume = scene["volume_start"]
            packet = volume_packets.get(volume)
            if not packet or packet.get("opening_slug") != scene["slug"]:
                raise RuntimeError(
                    f"missing public packet for Volume {volume} opening {scene['slug']}; "
                    "refusing to substitute another volume's jacket."
                )
            packet_block = f"PUBLIC VOLUME-ENTRY PACKET (shown once at this volume's opening):\n{packet['packet']}\n\n"
        base_prompt = (
            f"TITLE:\n{scene['title']}\n\n"
            f"{packet_block}"
            f"PRIOR READER-STATE (authoritative memory from every earlier chapter):\n{prior_block}\n\n"
            f"OUTPUT PRIORITY:\nKeep `### Reader reaction` concise. Always complete "
            f"`### Carry-forward state` in full; if space is tight, shorten the reaction, "
            f"never the carry-forward.\n\n"
            f"{axis_order_line(idx)}\n\n"
            f"CHAPTER TEXT:\n{clean}\n"
        )

        ok = False
        usage = None
        prior_carry_text = carry if carry.strip() else ""
        last_problems = []
        for attempt in range(1, max_attempts + 1):
            prompt = base_prompt
            if attempt > 1:
                prompt += (
                    "\n\nFORMAT REMINDER: Return exactly three top-level sections headed "
                    "`### Reader reaction`, `### Carry-forward state`, and `### Chapter "
                    "record`. The carry-forward section must be a full updated memory, "
                    "not empty."
                )
            if last_problems:
                prompt += (
                    "\n\nRETENTION REMINDER: your previous attempt lost memory the next "
                    "reader cannot recover — " + "; ".join(last_problems) + ". Carry EVERY "
                    "principal character and every entry in the 'what I know that they "
                    "don't' ledger forward. Consolidate motifs rather than logging every "
                    "appearance — letting walk-ons and scenery go is correct and expected. "
                    "Never write 'as previously logged' or point at earlier chapters: the "
                    "next reader sees ONLY this ledger."
                )
            # unique label every attempt/time to avoid artifact collisions
            label = (
                f"{label_prefix}_{model_id}_{scene['slug'].replace('-', '_')}"
                f"_try{attempt}_{int(time.time())}"
            )
            try:
                t0 = time.time()
                result = agent_fn(prompt=prompt, model=model_selector, label=label)
                wall = time.time() - t0
                response_text = parse_response(result.get("output") or result.get("text"))
                reader, parsed = split_reader(response_text)
                refusal = bool(reader) and any(
                    marker in reader.lower() for marker in REFUSAL_MARKERS
                )
                if refusal:
                    print(
                        json.dumps(
                            {
                                "slug": scene["slug"],
                                "status": "refusal_detected",
                                "attempt": attempt,
                            }
                        ),
                        flush=True,
                    )
                elif reader and parsed:
                    last_problems = check_retention(prior_carry_text, parsed)
                    if last_problems and attempt < max_attempts:
                        print(
                            json.dumps({
                                "slug": scene["slug"],
                                "status": "retention-retry",
                                "attempt": attempt,
                                "problems": last_problems,
                            }),
                            flush=True,
                        )
                        continue
                    if last_problems:
                        # Out of attempts: keep the review (a partial ledger beats no
                        # chain) but make the loss loud and durable in the stats.
                        print(
                            json.dumps({
                                "slug": scene["slug"],
                                "status": "retention-warning",
                                "problems": last_problems,
                            }),
                            flush=True,
                        )
                    if compactor and len(parsed) > compaction_threshold:
                        try:
                            comp = compactor(parsed, scene["slug"])
                            # Accept only if smaller AND the deterministic retention check
                            # still passes (backstop behind the LLM compaction judge).
                            if comp and len(comp) < len(parsed) and not check_retention(prior_carry_text, comp):
                                print(json.dumps({"slug": scene["slug"], "status": "compacted",
                                                  "from_chars": len(parsed), "to_chars": len(comp)}), flush=True)
                                response_text = (
                                    f"### Reader reaction\n\n{reader}\n\n"
                                    f"### Carry-forward state\n\n{comp}"
                                )
                            else:
                                print(json.dumps({"slug": scene["slug"], "status": "compaction-skipped",
                                                  "reason": "not-smaller-or-failed-retention",
                                                  "from_chars": len(parsed),
                                                  "to_chars": (len(comp) if comp else 0)}), flush=True)
                        except Exception as e:
                            print(json.dumps({"slug": scene["slug"], "status": "compaction-error",
                                              "error": f"{type(e).__name__}: {e}"}), flush=True)
                    path, carry = write_review(
                        out_dir, model_id, model_selector, scene, response_text, predecessor,
                        provider_label, LEGACY_PROTOCOL if allow_legacy_resume else READER_PROTOCOL,
                    )
                    predecessor = scene["slug"]
                    usage = result.get("usage") or extract_usage(result.get("id") or label)
                    rec = {
                        "slug": scene["slug"],
                        "title": scene["title"],
                        "path": str(path),
                        "agent": result.get("id"),
                        "attempt": attempt,
                        "status": "generated",
                        "wall_s": round(wall, 1),
                        "response_chars": len(response_text),
                        "carry_chars": len(carry),
                        "usage": usage,
                    }
                    if last_problems:
                        rec["retention_problems"] = last_problems
                    log.append(rec)
                    print(
                        json.dumps(
                            {
                                "n": idx,
                                "of": len(scenes),
                                "slug": scene["slug"],
                                "status": "generated",
                                "attempt": attempt,
                                "cost": (
                                    None
                                    if not usage or usage.get("cost") is None
                                    else round(usage["cost"], 6)
                                ),
                                "input": None if not usage else usage["input"],
                                "output": None if not usage else usage["output"],
                                "totalTokens": None if not usage else usage["totalTokens"],
                                "promptTokens": None if not usage else usage["promptTokens"],
                                "carry_chars": len(carry),
                            }
                        ),
                        flush=True,
                    )
                    ok = True
                    break
                else:
                    print(
                        f"invalid sections {scene['slug']} attempt={attempt} "
                        f"reader={len(reader)} carry={len(parsed)}",
                        flush=True,
                    )
            except Exception as e:
                print(
                    f"exception {scene['slug']} attempt={attempt}: {type(e).__name__}: {e}",
                    flush=True,
                )
                time.sleep(min(30, 5 * attempt))
                continue
            # brief pause between invalid-section retries
            time.sleep(2 * attempt)
        if not ok:
            raise RuntimeError(
                f"failed {scene['slug']}; completed={[r['slug'] for r in log if r.get('status')=='generated']}"
            )
        # Cost safety: abort the whole batch on an over-budget or capped (incomplete) scene.
        if usage:
            if usage.get("incomplete"):
                raise RuntimeError(
                    f"response incomplete on {scene['slug']} (hit the output cap). "
                    f"Raise the applicable output cap or lower --effort, then re-run with --resume."
                )
            if budget_usd is not None and float(usage.get("cost") or 0) > budget_usd:
                raise RuntimeError(
                    f"budget exceeded on {scene['slug']}: "
                    f"${float(usage['cost']):.4f} > ${budget_usd:.2f} — aborting batch."
                )

    gen = [r for r in log if r.get("status") == "generated"]
    summary = {
        "model_selector": model_selector,
        "model_id": model_id,
        "completed": len(log),
        "generated": len(gen),
        "skipped": sum(1 for r in log if r.get("status") == "skipped-existing"),
        "total_cost": (
            None
            if any((r.get("usage") or {}).get("cost") is None for r in gen)
            else sum((r.get("usage") or {}).get("cost", 0) for r in gen)
        ),
        "total_input": sum((r.get("usage") or {}).get("input", 0) for r in gen),
        "total_output": sum((r.get("usage") or {}).get("output", 0) for r in gen),
        "total_tokens": sum((r.get("usage") or {}).get("totalTokens", 0) for r in gen),
        "per_chapter": [
            {
                "slug": r["slug"],
                "title": r["title"],
                "status": r.get("status"),
                "cost": None if not r.get("usage") else r["usage"]["cost"],
                "input": None if not r.get("usage") else r["usage"]["input"],
                "output": None if not r.get("usage") else r["usage"]["output"],
                "totalTokens": None if not r.get("usage") else r["usage"]["totalTokens"],
                "promptTokens": None if not r.get("usage") else r["usage"]["promptTokens"],
                "reasoningTokens": None if not r.get("usage") else r["usage"]["reasoningTokens"],
                "cacheRead": None if not r.get("usage") else r["usage"]["cacheRead"],
                "duration_s": None
                if not r.get("usage")
                else round(r["usage"]["duration_ms"] / 1000, 1),
                "wall_s": r.get("wall_s"),
                "path": r["path"],
            }
            for r in log
        ],
    }
    stats_path = out_dir / "BATCH_STATS.json"
    stats_path.write_text(json.dumps(summary, indent=2) + "\n")
    # Durable cost record: append this run to BATCH_RUNS.jsonl (one line per batch).
    # BATCH_STATS.json remains the latest-run convenience view; the jsonl is the history.
    from datetime import datetime, timezone
    run_record = {
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": f"{log[0]['slug']}..{log[-1]['slug']}" if log else None,
        "budget_usd": budget_usd,
        **summary,
    }
    runs_path = out_dir / "BATCH_RUNS.jsonl"
    with runs_path.open("a") as f:
        f.write(json.dumps(run_record) + "\n")
    print(json.dumps({"summary_path": str(stats_path), **{k: summary[k] for k in (
        "completed","generated","skipped","total_cost","total_input","total_output","total_tokens"
    )}}, indent=2), flush=True)
    return summary
