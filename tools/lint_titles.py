#!/usr/bin/env python3
"""Validate {{Chapter Title}} references across the planning docs.

Chapter-title references in the planning corpus are wrapped in {{double braces}}
so a title is machine-distinguishable from the same words used as an event or a
common word (see CLAUDE.md, "Chapter-title references"). This checks that every
{{...}} names a real chapter — the entry headings in meta-plan-chronology.md — so
a rename or a typo can't leave a dangling reference.

Usage:
    tools/lint_titles.py            # validate meta/meta-plan-chronology.md
    tools/lint_titles.py --all      # validate every meta/*.md
    tools/lint_titles.py --bare     # also flag likely-unmarked multi-word titles
    tools/lint_titles.py --list     # print the canonical title set and exit

Exit status is nonzero when any {{...}} names an unknown chapter.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHRONOLOGY = REPO / "meta" / "meta-plan-chronology.md"

HEADING_RE = re.compile(r"^###\s+\[(SCENE|VIGNETTE|EVENT)\]\s+(.*)$")
MARK_RE = re.compile(r"\{\{([^}]+)\}\}")


def canonical(raw: str) -> str:
    """The title as it is referenced: drop a trailing (parenthetical) and any
    trailing `slot` marker, then collapse surrounding whitespace."""
    t = raw.strip()
    t = re.sub(r"\s*`[^`]*`\s*$", "", t)      # trailing `[slot TBD]`
    t = re.sub(r"\s*\([^()]*\)\s*$", "", t)   # trailing (parenthetical)
    return t.strip()


def load_titles(chron: Path):
    """Return (all_titles, chapter_titles) as sets of canonical strings.

    all_titles includes EVENTs (a reference may name one); chapter_titles is
    SCENE/VIGNETTE only, used for the --bare heuristic.
    """
    all_titles, chapters = set(), set()
    for line in chron.read_text(encoding="utf-8").splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        kind, title = m.group(1), canonical(m.group(2))
        all_titles.add(title)
        if kind in ("SCENE", "VIGNETTE"):
            chapters.add(title)
    return all_titles, chapters


def check_file(path: Path, valid: set):
    """Yield (lineno, title, ok) for each {{...}} occurrence in the file."""
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for m in MARK_RE.finditer(line):
            title = m.group(1).strip()
            yield i, title, (title in valid)


def find_bare(path: Path, chapters: set):
    """Advisory: multi-word chapter titles appearing un-braced (possible missed
    references). Noisy by nature; single-word titles are skipped."""
    multi = sorted((t for t in chapters if len(t.split()) >= 2), key=len, reverse=True)
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        # blank out braced spans so only bare occurrences remain
        bare = MARK_RE.sub(lambda m: " " * len(m.group(0)), line)
        for t in multi:
            start = 0
            while (j := bare.find(t, start)) >= 0:
                yield i, t
                start = j + len(t)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="validate every meta/*.md")
    ap.add_argument("--bare", action="store_true",
                    help="also flag likely-unmarked multi-word titles (advisory)")
    ap.add_argument("--list", action="store_true",
                    help="print the canonical title set and exit")
    args = ap.parse_args()

    if not CHRONOLOGY.exists():
        sys.exit(f"chronology not found: {CHRONOLOGY}")
    all_titles, chapters = load_titles(CHRONOLOGY)

    if args.list:
        for t in sorted(all_titles):
            print(t)
        return

    files = sorted((REPO / "meta").glob("*.md")) if args.all else [CHRONOLOGY]
    bad = 0
    for f in files:
        for lineno, title, ok in check_file(f, all_titles):
            if not ok:
                bad += 1
                print(f"{f.relative_to(REPO)}:{lineno}: unknown chapter "
                      + "{{" + title + "}}", file=sys.stderr)
    if args.bare:
        for f in files:
            for lineno, title in find_bare(f, chapters):
                print(f"{f.relative_to(REPO)}:{lineno}: [advisory] un-braced "
                      f"title '{title}'")

    if bad:
        print(f"\n{bad} unknown reference(s) against {len(all_titles)} known "
              "titles", file=sys.stderr)
        sys.exit(1)
    print(f"ok — all title references resolve ({len(all_titles)} known titles)")


if __name__ == "__main__":
    main()
