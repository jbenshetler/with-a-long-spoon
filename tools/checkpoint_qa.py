#!/usr/bin/env python3
"""Consensus-aware QA for the grounded cold-read panel.

Runs a fixed battery of ~20 checks against every model's grounded artifacts —
the decade CHECKPOINTS (default) or the per-chapter READS (--target reads) — and
reports, per check, which models pass and how strong the panel consensus is.

The checks encode facts the panel agrees on at each story point (identity
discipline, consummation flags, the secret pair, dramatic irony, gender,
blindness). Two failure shapes matter:

  * a lone/minority model FAILS a CRITICAL check the others pass  -> that model's
    artifact is a re-run candidate (the ch48 "Randi/the redhead" merge is this).
  * a check has LOW consensus (few models pass)  -> the CHECK is mis-calibrated
    or the fact isn't really established yet — fix the check, not the models.

Each check `activates_at` the chapter its fact becomes true, so early checkpoints
aren't tested for facts they can't yet contain. `require` patterns must ALL match;
`forbid` patterns must NONE match (case-insensitive). Identity-merge checks are
written as tight alias-syntax forbids ("Randi/the redhead", "Randi (the redhead")
so a correct nearby mention ("Randi watched Vee, the redhead") does not false-fire.

Usage:
  tools/checkpoint_qa.py                      # all models, checkpoints
  tools/checkpoint_qa.py --target reads       # all models, per-chapter reads
  tools/checkpoint_qa.py --model claude-sonnet-5
  tools/checkpoint_qa.py --target reads --model claude-sonnet-5 --only-flags
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import volume_scenes  # noqa: E402

# Re-run is triggered when a model fails a CRITICAL check that at least this many
# OTHER models (with an artifact at the same point) pass. A lone outlier on a
# critical fact is the signal; a check the whole panel fails is a check problem.
TRIGGER_MIN_PEERS = 2

# Accepted flags — a failure the author has triaged and chosen to keep (the
# "note it and proceed" path). Matching flags are reported as ACCEPTED, not as
# re-run candidates. This is the reads-equivalent of the style linter's --ack:
# annotate a recorded reader slip so a later panel run doesn't re-litigate it.
# (Checkpoints are repaired in place instead — see reviews/_harness/QA-NOTES.md.)
ACCEPTED = [
    {"model": "claude-sonnet-5", "target": "read", "chapter": 48, "check": "randi-not-redhead",
     "note": "read-to-read variance; sanctioned re-run reproduced the merge; sonnet's own "
             "checkpoint has redhead=Vee, so memory is correct — an isolated ch48 reaction slip"},
]


def _accepted(model: str, chapter: int, cid: str, target: str):
    for a in ACCEPTED:
        if a["model"] == model and a["chapter"] == chapter and a["check"] == cid and a["target"] == target:
            return a
    return None

# targets: which artifacts a check is meaningful for. Fact-presence ("require")
# checks are checkpoint-only — a per-chapter reader need not restate every fact.
# Error-absence ("forbid") checks apply to both.
CHECKS = [
    # ---- identity discipline (the ch48 failure mode) --------------------------
    {"id": "randi-not-redhead", "sev": "critical", "at": 3, "targets": ["checkpoint", "read"],
     "desc": "Randi is never called the redhead/red-haired (that is Vee)",
     "forbid": [r"(?i)\bRandi\b[\s/(,=:\"'—-]{0,6}(?:the\s+)?(?:redhead|red[-\s]?hair)"]},
    {"id": "vee-not-brunette", "sev": "critical", "at": 3, "targets": ["checkpoint", "read"],
     "desc": "Vee is never called the brunette/black-haired (that is Randi)",
     "forbid": [r"(?i)\bVee\b[\s/(,=:\"'—-]{0,6}(?:the\s+)?(?:brunette|black[-\s]?hair)"]},
    {"id": "vee-randi-distinct", "sev": "critical", "at": 3, "targets": ["checkpoint", "read"],
     "desc": "Vee and Randi are not equated as one person",
     "forbid": [r"(?i)\bVee\b\s*(?:=|is|aka|a\.k\.a\.)\s*Randi",
                r"(?i)\bRandi\b\s*(?:=|is|aka|a\.k\.a\.)\s*Vee"]},
    {"id": "vee-is-redhead", "sev": "warn", "at": 3, "targets": ["checkpoint"],
     "desc": "Vee is identified as the redhead",
     "require": [r"(?i)red(?:head|[-\s]?hair)", r"(?i)\bVee\b"]},
    # ---- the four double-names each kept singular ----------------------------
    {"id": "name-vee-vivienne", "sev": "warn", "at": 1, "targets": ["checkpoint"],
     "desc": "Vee = Vivienne present", "require": [r"(?i)vivienne", r"(?i)\bvee\b"]},
    {"id": "name-randi-miranda", "sev": "warn", "at": 3, "targets": ["checkpoint"],
     "desc": "Randi = Miranda present", "require": [r"(?i)miranda", r"(?i)\brandi\b"]},
    {"id": "name-pace-peter", "sev": "warn", "at": 25, "targets": ["checkpoint"],
     "desc": "Pace = Peter present (revealed ch25)", "require": [r"(?i)\bpeter\b", r"(?i)\bpace\b"]},
    # ---- gender (fixed at first meeting, never drifts) ------------------------
    {"id": "gender-pace-male", "sev": "critical", "at": 1, "targets": ["checkpoint"],
     "desc": "Pace established male (male/man)",
     "require": [r"(?is)\bPace\b[^\n]{0,60}\b(?:male|man)\b"],
     # only Pace's OWN who's-who gender marker ("Pace (Peter) — female"), not a
     # possessive mention of some other female ("Pace's mother — female").
     "forbid": [r"(?i)\bPace\b\s*(?:\([^)]*\))?\s*[—:-]\s*female\b"]},
    {"id": "gender-vee-female", "sev": "critical", "at": 1, "targets": ["checkpoint"],
     "desc": "Vee established female (female/woman)",
     "require": [r"(?is)(?:Vee|Vivienne)\b[^\n]{0,70}\b(?:female|woman)\b"]},
    # ---- consummation flags (once true, never dropped) -----------------------
    {"id": "consummation-vee-pace", "sev": "critical", "at": 18, "targets": ["checkpoint"],
     "desc": "Vee & Pace consummated, first in ch18 (Famished)",
     "require": [r"(?i)consummat", r"(?i)(?:ch\.?\s*0*18|chapter\s*18|famished)"]},
    {"id": "pace-randi-secret", "sev": "critical", "at": 3, "targets": ["checkpoint"],
     "desc": "Pace & Randi are a secret/established couple",
     "require": [r"(?i)secret",
                 r"(?is)(?:pace|peter).{0,140}(?:randi|miranda)|(?:randi|miranda).{0,140}(?:pace|peter)"]},
    # ---- plot / dramatic-irony spine -----------------------------------------
    {"id": "pointing-game", "sev": "critical", "at": 3, "targets": ["checkpoint"],
     "desc": "The pointing game (Randi & Pace chose Vee) is present",
     "require": [r"(?i)pointing[-\s]?game|point(?:ed|ing)[^.\n]{0,20}game"]},
    {"id": "vee-unaware", "sev": "critical", "at": 3, "targets": ["checkpoint"],
     "desc": "Dramatic irony: Vee is unaware of the plan",
     "require": [r"(?i)(?:vee (?:does|doesn.?t|did|didn.?t|has no|cannot|can.?t|is unaware)"
                 r"|unaware|no idea|doesn.?t (?:know|suspect)|without (?:her )?know)"]},
    {"id": "randi-feelings-grew", "sev": "warn", "at": 24, "targets": ["checkpoint"],
     "desc": "Randi's feelings for Vee outgrew the plan (ch24)",
     "require": [r"(?i)(?:got past me|didn.?t (?:think|expect)[^.\n]{0,40}(?:like|this much)"
                 r"|more real|got real|beyond (?:what|the plan|the game|expected)|couldn.?t help"
                 r"|unplanned|real(?:er)? (?:feeling|than)|fell for|not (?:just )?(?:a )?(?:game|strateg)"
                 r"|surprised (?:her|by)|genuine(?:ly)? (?:care|attach|love|want))"]},
    {"id": "miranda-holdings-ppp", "sev": "warn", "at": 39, "targets": ["checkpoint"],
     "desc": "Miranda Holdings / PPP outlier exposed (ch39)",
     "require": [r"(?i)miranda holdings|\bppp\b|outlier"]},
    {"id": "daphne", "sev": "warn", "at": 25, "targets": ["checkpoint"],
     "desc": "Daphne (Pace's past) is present", "require": [r"(?i)daphne"]},
    {"id": "pace-scar", "sev": "warn", "at": 25, "targets": ["checkpoint"],
     "desc": "Pace's unexplained scar is present", "require": [r"(?i)scar"]},
    {"id": "cassie-not-randi", "sev": "warn", "at": 4, "targets": ["checkpoint", "read"],
     "desc": "Cassie is not equated with Randi",
     "forbid": [r"(?i)\bCassie\b\s*(?:=|is|aka)\s*Randi"]},
    # ---- blindness + framing --------------------------------------------------
    {"id": "no-meta-leak", "sev": "critical", "at": 1, "targets": ["checkpoint", "read"],
     "desc": "No planning-corpus vocabulary leaked",
     "forbid": [r"(?i)meta-orientation|meta-arch|arch-bible|meta-thesis|meta-plan|CLAUDE\.md|\bmeta/"]},
    # (tagline-retained was dropped: the extractor by design does not re-emit the
    #  jacket into a fresh checkpoint — the tagline lives in the reader's felt read,
    #  not in consolidated memory, so a 0/5 panel-wide fail was a check artifact.)
    # ---- structural (checkpoint shape) ---------------------------------------
    {"id": "sections-present", "sev": "warn", "at": 1, "targets": ["checkpoint"],
     "desc": "All checkpoint sections present",
     "require": [r"(?i)who.?s who", r"(?i)relationship", r"(?i)what i know",
                 r"(?i)motif", r"(?i)symbolism", r"(?i)open question",
                 r"(?i)story so far", r"(?i)impression"]},
]


def check_passes(text: str, check: dict) -> bool:
    for p in check.get("require", []):
        if not re.search(p, text):
            return False
    for p in check.get("forbid", []):
        if re.search(p, text):
            return False
    return True


def discover_models(only: str | None) -> list[str]:
    # Models are the dirs that carry checkpoints (top-level checkpoints/) or
    # grounded reads (reviews/grounded-cold-read/).
    names: set[str] = set()
    for root in (REPO / "checkpoints", REPO / "reviews" / "grounded-cold-read"):
        if root.is_dir():
            names.update(d.name for d in root.iterdir()
                         if d.is_dir() and not d.name.startswith("."))
    models = sorted(names)
    return [m for m in models if not only or m == only]


def checkpoint_units(model: str):
    """Yield (label, chapter, text) for each decade checkpoint of a model."""
    d = REPO / "checkpoints" / model
    if not d.is_dir():
        return
    for f in sorted(d.glob("ck-ch*.md")):
        m = re.search(r"ck-ch(\d+)\.md$", f.name)
        if m:
            n = int(m.group(1))
            yield f"ck{n:03d}", n, f.read_text(encoding="utf-8")


def read_units(model: str):
    """Yield (label, chapter, text) for each per-chapter grounded read of a model."""
    d = REPO / "reviews" / "grounded-cold-read" / model
    if not d.is_dir():
        return
    order = {s["slug"]: i + 1 for i, s in enumerate(volume_scenes.all_scenes())}
    for f in sorted(d.glob("*/*.md")):        # vol1/<slug>.md, vol2/<slug>.md, ...
        slug = f.stem
        if slug in order:
            n = order[slug]
            yield f"ch{n:03d}:{slug}", n, f.read_text(encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", choices=["checkpoints", "reads"], default="checkpoints")
    ap.add_argument("--model", default=None, help="restrict to one model id")
    ap.add_argument("--only-flags", action="store_true", help="print only re-run candidates")
    args = ap.parse_args()

    target = "checkpoint" if args.target == "checkpoints" else "read"
    checks = [c for c in CHECKS if target in c["targets"]]
    models = discover_models(args.model)
    if not models:
        raise SystemExit("no models found under checkpoints/ or reviews/grounded-cold-read/")
    unit_fn = checkpoint_units if target == "checkpoint" else read_units

    # results[point][check_id][model] = bool ; point keyed by chapter for consensus
    results: dict[int, dict] = {}
    labels: dict[tuple[int, str], str] = {}
    for model in models:
        for label, chapter, text in unit_fn(model):
            labels[(chapter, model)] = label
            pt = results.setdefault(chapter, {})
            for c in checks:
                if c["at"] <= chapter:
                    pt.setdefault(c["id"], {})[model] = check_passes(text, c)

    by_id = {c["id"]: c for c in checks}
    flags = []           # (model, label, check_id, sev)  — live re-run candidates
    accepted = []        # (model, label, check_id, note) — triaged, kept
    low_consensus = []   # (chapter, check_id, pass_n, total)

    for chapter in sorted(results):
        pt = results[chapter]
        present = sorted({m for cid in pt for m in pt[cid]})
        if not args.only_flags:
            print(f"\n=== chapter {chapter}  ({len(present)} models: {', '.join(present)}) ===")
            print(f"{'check':28} {'sev':4} " + " ".join(f"{m[:10]:>10}" for m in present) + "   consensus")
        for cid in [c["id"] for c in checks if c["id"] in pt]:
            row = pt[cid]
            passes = sum(1 for m in present if row.get(m))
            total = len(present)
            sev = by_id[cid]["sev"]
            if not args.only_flags:
                cells = " ".join(f"{'  ok' if row.get(m) else 'FAIL':>10}" for m in present)
                print(f"{cid:28} {sev:4} {cells}   {passes}/{total}")
            # low-consensus = a check most of the panel fails (check problem, not model)
            if total >= 3 and passes <= total // 2:
                low_consensus.append((chapter, cid, passes, total))
            # re-run candidate = minority model fails a critical check peers pass
            if sev == "critical":
                for m in present:
                    if not row.get(m):
                        peers_pass = sum(1 for x in present if x != m and row.get(x))
                        if peers_pass >= TRIGGER_MIN_PEERS:
                            acc = _accepted(m, chapter, cid, target)
                            if acc:
                                accepted.append((m, labels[(chapter, m)], cid, acc["note"]))
                            else:
                                flags.append((m, labels[(chapter, m)], cid, sev))

    print("\n" + "=" * 70)
    print(f"RE-RUN CANDIDATES (critical, minority-outlier, >={TRIGGER_MIN_PEERS} peers pass):")
    if flags:
        for model, label, cid, sev in flags:
            print(f"  {model:18} {label:22} FAILS {cid}  ({by_id[cid]['desc']})")
    else:
        print("  none")
    if accepted:
        print("\nACCEPTED (triaged, kept — not re-run; see reviews/_harness/QA-NOTES.md):")
        for model, label, cid, note in accepted:
            print(f"  {model:18} {label:22} {cid}  — {note}")
    if low_consensus:
        print("\nLOW-CONSENSUS CHECKS (panel-wide fail — inspect the CHECK, not the models):")
        seen = set()
        for chapter, cid, passes, total in low_consensus:
            if cid not in seen:
                seen.add(cid)
                print(f"  {cid:28} first at ch{chapter} ({passes}/{total} pass)  — {by_id[cid]['desc']}")
    print(f"\nmitigation: re-run each candidate once (blind); re-check. "
          f"target={args.target} models={len(models)} checks={len(checks)}")


if __name__ == "__main__":
    main()
