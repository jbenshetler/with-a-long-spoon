#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Split capture-panel ALMOST-STOPPED entries into hover-and-resolve vs. standing.

WHY THIS EXISTS. `capture_stats.py` reports an `exits` count per reader — how
many gates carry a non-`none` ALMOST-STOPPED. That number was being read as
"times this reader nearly put the book down," and it is not that. The field
records WHERE a reader's attention snagged; the resolution lives in the WHY
that follows it. The worked case is peekaboo (ch021):

    ALMOST-STOPPED: "...It just felt like what she was for." — I hovered
                    there, checking whether the book knew what it had said.
    WHY:            It knew — ... "getting away with something" closes the
                    chapter with the irony fully loaded.

Counting that as an exit inverts its meaning: the reader is reporting that the
chapter passed a test, which is the instrument working, not a defect. An
`exits` column that cannot tell this apart from a genuine near-miss overstates
risk everywhere it is cited.

WHAT IT DOES NOT DO. This is a lexical classifier over free prose, so it is a
triage aid, not a verdict — the same discipline as every other instrument here:
it FLAGS, it does not rule. It keys on resolution markers that predicate
something affirmative of the BOOK ("the book answered it", "it knew", "it
didn't", "earned", "held") rather than on conjunctions: "but" appears in nearly
every WHY in both directions, so any test built on it is noise. Entries with no
marker fall to STANDING, which means the STANDING bucket is where the
misclassifications concentrate. Run `--list standing` and read them.

Always report the sampled accuracy alongside the counts; `--sample N` prints a
deterministic random subset for hand-labelling.

Usage:
    tools/almost_stopped_audit.py                        # counts per reader
    tools/almost_stopped_audit.py --model claude-fable-5
    tools/almost_stopped_audit.py --list resolved        # dump one bucket
    tools/almost_stopped_audit.py --sample 24            # for hand-verification
"""
from __future__ import annotations

import argparse
import random
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PANEL = REPO / "reviews" / "capture-panel"

FIELD_RE = re.compile(r"^(DECISION|CAPTURE|NEXT|ALMOST-STOPPED|WHY)\s*:\s*(.*)$")

# ---------------------------------------------------------------------------
# CLASSIFIER DIRECTION (measured 2026-09-25, do not re-invert without remeasuring)
#
# The first version of this tool defaulted to STANDING and promoted an entry to
# RESOLVED on a marker. Hand-labelling 20 random entries killed it: the true
# resolved rate is ~85%, the tool reported 18%, and its STANDING calls were
# right only 3 of 16. Readers affirm the book in unboundedly many phrasings
# ("It doesn't want me to cheer", "it scared me because the book knows it
# should", "the chill, not a quit, but a lean-back", "not because the book
# failed"), so no marker list will catch them all.
#
# Genuine near-misses are a NARROW and repetitive class, because they describe
# the reader's own attention failing rather than a fear about the book's
# ethics: attention sliding, a thumb slowing, a device becoming a treadmill, a
# retread, patience running out, a conditional threat to quit. So the default
# is now RESOLVED and STANDING is the promoted bucket — which also puts the
# errors in the small bucket a human can actually read.
# ---------------------------------------------------------------------------

# Persistence markers: the snag is disengagement, and it survives the WHY.
STANDING_MARKERS = [
    r"\battention (slid|slide|slipped|drift)", r"\bmy thumb (slowed|hovered)\b",
    r"\btreadmill\b", r"\bretread\b", r"\bran (a beat|a hair|on) too long\b",
    r"\btoo long\b", r"\bdragg?(ed|ing)\b", r"\bslog\b", r"\bskimm?(ed|ing)\b",
    r"\bhad my fill\b", r"\bmy patience\b", r"\bpatience (for|is|ran)\b",
    r"\bif the next\b", r"\bi'?m out\b", r"\bi'?d have been out\b",
    r"\bstart(ed)? looking for the exit\b", r"\bchecking the exits\b",
    r"\bwallpaper\b", r"\bbeige\b", r"\bneed bodies back\b",
    r"\bfelt (the|every degree of the) stall\b", r"\bthe stall\b",
    r"\bfourth (quiet|warm) chapter\b", r"\bthird (quiet|warm) chapter\b",
    r"\bgetting a recap\b", r"\bmight be laps\b", r"\bzero heat\b",
]
STANDING_RE = re.compile("|".join(STANDING_MARKERS), re.IGNORECASE)

# Kept for --explain: what the reader said that reads as resolution. No longer
# load-bearing for the bucket.
RESOLVED_MARKERS = [
    r"\bit knew\b", r"\bthe book knew\b", r"\bit did ?n[o']t\b",
    r"\bthe book (answered|held|earned|is smarter|was ahead)",
    r"\bthe narration (kept|held)", r"\bthe eyebrow held\b",
    r"\bearned (the|it|that|every)", r"\bheld\b.{0,20}\bbecause\b",
    r"\bgone by the (paragraph|end)", r"\bthen (i|she|he|randi|vee|the book)\b",
    r"\band then\b", r"\bresolved\b", r"\bcleared\b", r"\breassured\b",
    r"\bthe line held\b", r"\bthe breath passed\b", r"\bdeposition, not\b",
    r"\bnot a defense\b", r"\bit was ?n[o']t\b", r"\bdidn't tip\b",
    r"\bnearly tipped\b", r"\bkept (its|every) receipt", r"\bshowed me every gear\b",
    r"\bsmarter than that\b", r"\bfeels intentional\b", r"\bis intentional\b",
]
RESOLVED_RE = re.compile("|".join(RESOLVED_MARKERS), re.IGNORECASE)


def parse_gate(path: Path) -> dict[str, str]:
    """Field name -> value, folding continuation lines into the field."""
    out: dict[str, str] = {}
    current = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        m = FIELD_RE.match(line)
        if m:
            current = m.group(1).upper()
            out[current] = m.group(2).strip()
        elif current and line.strip():
            out[current] += " " + line.strip()
        elif not line.strip():
            current = ""
    return out


def is_none(value: str) -> bool:
    """`none`, and also `none — though I hovered at ...`, which is already a
    reader telling us she did not stop. Those never counted as exits."""
    return value.strip().lower().startswith("none") or not value.strip()


def collect(model: str | None, persona: str | None) -> list[dict]:
    rows = []
    for gate in sorted(PANEL.glob("*/dag/*/gate-ch*.md")):
        m, p = gate.parts[-4], gate.parts[-2]
        if (model and m != model) or (persona and p != persona):
            continue
        f = parse_gate(gate)
        almost = f.get("ALMOST-STOPPED", "")
        if is_none(almost):
            continue
        blob = f"{almost} {f.get('WHY', '')}"
        hit = STANDING_RE.search(blob)
        num = re.search(r"ch(\d+)", gate.name)
        rows.append({
            "model": m, "persona": p,
            "ch": int(num.group(1)) if num else 0,
            "capture": f.get("CAPTURE", "?"),
            "bucket": "standing" if hit else "resolved",
            "marker": hit.group(0) if hit else "",
            "almost": almost, "why": f.get("WHY", ""),
        })
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model")
    ap.add_argument("--persona")
    ap.add_argument("--list", choices=["resolved", "standing"])
    ap.add_argument("--sample", type=int, metavar="N",
                    help="print N random entries unlabelled, for hand-verification")
    args = ap.parse_args()

    rows = collect(args.model, args.persona)
    if not rows:
        print("no ALMOST-STOPPED entries in scope")
        return

    if args.sample:
        random.seed(20260925)
        for r in random.sample(rows, min(args.sample, len(rows))):
            print(f"--- {r['model']}·{r['persona']}·ch{r['ch']:03d} "
                  f"(cap {r['capture']}) [tool says: {r['bucket']}"
                  f"{' via ' + repr(r['marker']) if r['marker'] else ''}]")
            print(f"  AS:  {r['almost'][:300]}")
            print(f"  WHY: {r['why'][:300]}\n")
        return

    if args.list:
        for r in [x for x in rows if x["bucket"] == args.list]:
            print(f"--- {r['model']}·{r['persona']}·ch{r['ch']:03d} (cap {r['capture']})")
            print(f"  AS:  {r['almost'][:260]}")
            print(f"  WHY: {r['why'][:260]}\n")
        return

    res = sum(1 for r in rows if r["bucket"] == "resolved")
    print(f"{len(rows)} ALMOST-STOPPED entries · "
          f"{res} resolved ({res / len(rows):.0%}) · {len(rows) - res} standing")
    print("  resolved = default; the snag is a fear the BOOK errs, answered in the WHY")
    print("  standing = a persistence marker fired (attention failing, and it survives")
    print("             the WHY) — READ THESE, the misclassifications live here\n")
    print(f"  {'reader':<44} {'entries':>7} {'resolved':>9} {'standing':>9}")
    seen: dict[tuple[str, str], list[dict]] = {}
    for r in rows:
        seen.setdefault((r["model"], r["persona"]), []).append(r)
    for (m, p), rs in sorted(seen.items()):
        r_n = sum(1 for x in rs if x["bucket"] == "resolved")
        print(f"  {m + '·' + p:<44} {len(rs):>7} {r_n:>9} {len(rs) - r_n:>9}")


if __name__ == "__main__":
    main()
