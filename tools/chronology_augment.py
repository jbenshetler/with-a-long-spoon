#!/usr/bin/env python3
"""Augment meta-plan-chronology.md entry metadata with `slug:` and `present:`.

Two segments are appended to each entry's metadata line (idempotent — a segment
already present is never rewritten, so the author's hand-edits to `present:`
survive re-runs):

  slug:     every entry (SCENE/VIGNETTE/EVENT). Article-dropped, and *verified
            against scenes/ on disk*: prefer the basename of the cited `*.md`
            when that file exists; else the article-dropped kebab of the title;
            drafted entries whose slug has no file on disk are flagged.
  present:  SCENE/VIGNETTE only. Which of the three principals (Vee/Pace/Randi)
            are physically present. Bootstrapped from the cold-read
            "Cast present (in person)" footers (majority across models); the
            author owns it afterward. Split votes and review-less scenes are
            flagged, not silently guessed.

Default is a DRY RUN (prints the proposed line diffs + a flag report). Pass
--apply to write the file in place. Re-run tools/chronology_html.py afterward.

Usage:
    tools/chronology_augment.py [--apply] [INPUT.md]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PRINCIPALS = ["Vee", "Pace", "Randi"]
# Pace goes by "Peter" in some reviews; count either as Pace present.
NAME_RE = {
    "Vee": re.compile(r"\bVee\b"),
    "Pace": re.compile(r"\b(?:Pace|Peter)\b"),
    "Randi": re.compile(r"\bRandi\b"),
}

ENTRY_RE = re.compile(r"^###\s+\[(SCENE|VIGNETTE|EVENT)\]\s+(.*)$")
MIDDOT = "·"
# first *.md that isn't a meta-* planning doc (mirrors chronology_html.py)
SCENE_MD_RE = re.compile(r"(?:scenes/)?([a-z0-9][a-z0-9-]*\.md)")


def cited_file(meta_raw: str):
    for m in SCENE_MD_RE.finditer(meta_raw):
        name = m.group(1)
        if name.startswith("meta"):
            continue
        return name
    return None


def slug_from_title(title: str) -> str:
    t = re.sub(r"\{\{|\}\}", "", title)
    t = re.sub(r"\(.*?\)", "", t)          # drop trailing parenthetical
    t = t.strip().lower()
    t = re.sub(r"^(?:the|a|an)\s+", "", t)  # drop leading article (disk convention)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "beat"


def norm_slug(s: str) -> str:
    """Article-insensitive key for matching (review files are inconsistent)."""
    return re.sub(r"^(?:the|a|an)-", "", s)


def resolve_slug(etype, title, meta_raw, scenes_dir):
    """Return (slug, has_file, note). note is a warning string or None."""
    cf = cited_file(meta_raw)
    if cf:
        stem = cf[:-3]
        exists = (scenes_dir / cf).exists()
        note = None if exists else f"cited `{cf}` not on disk"
        return stem, exists, note
    stem = slug_from_title(title)
    exists = (scenes_dir / f"{stem}.md").exists()
    drafted = "draft complete" in meta_raw.lower()
    note = "drafted but no scene file found" if (drafted and not exists) else None
    return stem, exists, note


# --- present: bootstrap from the cold reviews -------------------------------
def cast_window(text: str):
    """Extract just the 'Cast present (in person)' names text from a review."""
    i = text.find("Cast present (in person):")
    if i == -1:
        return None
    w = text[i + len("Cast present (in person):"):]
    # stop at the mentioned-only list or the next bold field or a blank line
    for stop in ("Mentioned-only", "mentioned-only", "**Heat", "**Romance",
                 "**Motifs", "**Cast", "\n\n"):
        j = w.find(stop)
        if j != -1:
            w = w[:j]
    return w


def present_from_reviews(slug, reviews_root):
    """Majority-vote presence of each principal across model reviews.

    Returns (present_set, note). note flags split votes / no coverage.
    """
    if not reviews_root.is_dir():
        return set(), "no reviews dir"
    key = norm_slug(slug)
    files = []
    for model_dir in sorted(reviews_root.iterdir()):
        if not model_dir.is_dir():
            continue
        for f in model_dir.glob("*.md"):
            if norm_slug(f.stem) == key:
                files.append(f)
    if not files:
        return set(), "no reviews"
    votes = {n: 0 for n in PRINCIPALS}
    counted = 0
    for f in files:
        w = cast_window(f.read_text(encoding="utf-8"))
        if w is None:
            continue
        counted += 1
        for n in PRINCIPALS:
            if NAME_RE[n].search(w):
                votes[n] += 1
    if counted == 0:
        return set(), "no parseable cast lines"
    present, split = set(), []
    for n in PRINCIPALS:
        if votes[n] * 2 > counted:
            present.add(n)
        if 0 < votes[n] < counted:      # not unanimous either way
            split.append(f"{n} {votes[n]}/{counted}")
    note = ("split: " + ", ".join(split)) if split else None
    return present, note


def find_meta_idx(lines, start):
    """Index of the metadata line for an entry heading at `start`."""
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if s == "":
            continue
        if s.startswith("*") and MIDDOT in s:
            return i
        return None   # first non-blank line isn't a metadata line
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", default="meta/meta-plan-chronology.md")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"input not found: {src}")
    root = src.resolve().parent.parent
    scenes_dir = root / "scenes"
    reviews_root = root / "reviews" / "cold-read"

    lines = src.read_text(encoding="utf-8").splitlines()
    changes, flags = [], []
    i = 0
    while i < len(lines):
        m = ENTRY_RE.match(lines[i])
        if not m:
            i += 1
            continue
        etype, title = m.group(1), m.group(2).strip()
        mi = find_meta_idx(lines, i)
        if mi is None:
            flags.append(f"[{title}] no metadata line — skipped")
            i += 1
            continue
        meta = lines[mi]
        slug, has_file, note = resolve_slug(etype, title, meta, scenes_dir)
        if note:
            flags.append(f"[{title}] slug={slug}: {note}")

        add = []
        if "slug:" not in meta:
            add.append(f"slug: {slug}")
        if etype in ("SCENE", "VIGNETTE") and "present:" not in meta:
            present, pnote = present_from_reviews(slug, reviews_root)
            if pnote:
                flags.append(f"[{title}] present: {pnote}")
            val = ", ".join(n for n in PRINCIPALS if n in present) if present else "?"
            add.append(f"present: {val}")

        if add:
            newmeta = meta.rstrip() + " " + MIDDOT + " " + (" " + MIDDOT + " ").join(add)
            changes.append((title, meta, newmeta))
            lines[mi] = newmeta
        i = mi + 1

    for title, old, new in changes:
        tail = new[len(old.rstrip()):].strip()
        print(f"  + [{title}]  {tail}")
    print(f"\n{len(changes)} entries augmented.", file=sys.stderr)
    if flags:
        print(f"\n--- flags ({len(flags)}) — review before trusting ---", file=sys.stderr)
        for fl in flags:
            print("  ! " + fl, file=sys.stderr)

    if args.apply and changes:
        src.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nwrote {src}", file=sys.stderr)
    elif not args.apply:
        print("\n(dry run — pass --apply to write)", file=sys.stderr)


if __name__ == "__main__":
    main()
