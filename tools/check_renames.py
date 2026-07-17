#!/usr/bin/env python3
"""Spot-check recent scene renames for lingering references to old names.

For each rename we search two kinds of pattern:
  STALE  — old slug / old file-path form. The file no longer exists under that
           name, so any hit is almost certainly a broken reference to fix.
  REVIEW — old *title* wording. Some of these are legitimate and must be kept
           (the in-world event, a plain object, or a different sibling scene),
           so hits are printed for human classification, not auto-condemned.

The two forms most likely to escape a rename sweep are bare slugs (no `.md`, e.g.
in a slug list) and `[[wiki-links]]` — neither matches a `<slug>.md` or
title-text search. The REVIEW bucket catches those for eyeballing.

Add a row to RENAMES per future rename. Run from anywhere: `tools/check_renames.py`.
"""
import os
import re

# repo root = parent of the tools/ dir this script lives in
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH_DIRS = ["scenes", "meta", "style"]
EXTS = (".md", ".toml")
EXCLUDE = {"chronology.html"}  # generated artifact

# (new label, [(kind, regex, severity, note)])
RENAMES = [
    ("Believe Me  (was The Christmas Fight)", [
        ("slug",  r"christmas-fight",                       "STALE",  ""),
        ("title", r"The Christmas Fight",                   "REVIEW", "lowercase 'the Christmas fight' = event, keep"),
    ]),
    ("Bare  (was His Shirt)", [
        ("slug",  r"his-shirt",                             "STALE",  ""),
        ("title", r"His Shirt",                             "REVIEW", "'his shirt' the object = keep"),
    ]),
    ("Cropped  (was Back from Thanksgiving)", [
        ("slug",  r"back-from-thanksgiving",                "STALE",  ""),
        ("title", r"Back from Thanksgiving",                "REVIEW", "'back from Thanksgiving break' = event, keep"),
    ]),
    ("How It's Done  (was the Fitting Brunch)", [
        ("slug",  r"brunch-fitting-randi",                  "STALE",  ""),
        ("title", r"Fitting Brunch",                        "REVIEW", ""),
        ("title", r"Tells Randi About the Fitting",         "REVIEW", ""),
    ]),
    ("Toenails  (was Cassie — After)", [
        ("slug",  r"cassie-after",                          "STALE",  ""),
        ("title", r"Cassie[\s—–-]+After",         "REVIEW", "siblings Cassie-Hike/Dinner/School-Nights excluded by pattern"),
    ]),
    ("Lesson  (was The CW Dance)", [
        ("slug",  r"cw-dance\.md",                          "STALE",  ""),
        ("slug",  r"the-cw-dance",                          "STALE",  ""),
        ("slug",  r"\[\[cw-dance\]\]",                      "STALE",  "wiki-link"),
        ("slug",  r"[(, ]cw-dance[),;]",                    "STALE",  "bare slug in a list"),
        ("title", r"(?i)CW[\s-]dance",                      "REVIEW", "CW-Dance Debrief / dance hall / blowup = event/venue/other-scene, keep"),
    ]),
    ("Standards  (was Randi's Walk of Shame)", [
        ("slug",  r"randis-walk-of-shame",                  "STALE",  ""),
        ("title", r"(?i)walk[\s-]of[\s-]shame",             "REVIEW", ""),
        ("title", r"The Morning After",                     "REVIEW", "old H1"),
    ]),
    ("Two Towels  (was The Fitting)", [
        ("slug",  r"fitting\.md",                           "STALE",  "old scene/companion path (ignore historical the-fitting.md in todo docs)"),
        ("slug",  r"meta-condensed-fitting",                "STALE",  ""),
        ("slug",  r"\[\[fitting\]\]",                       "STALE",  "wiki-link"),
        ("title", r"The Fitting",                           "REVIEW", "lowercase 'the fitting'=dress-fitting event; 'fitting shoes'/'the fitting hem'/'fitting tellings'=common noun, keep"),
    ]),
]


def files():
    for d in SEARCH_DIRS:
        for dirpath, _, names in os.walk(os.path.join(ROOT, d)):
            for n in names:
                if n in EXCLUDE or not n.endswith(EXTS):
                    continue
                yield os.path.join(dirpath, n)


def snippet(line, m, width=90):
    a = max(0, m.start() - width // 2)
    b = min(len(line), m.end() + width // 2)
    s = line[a:b].strip()
    return ("..." if a else "") + s + ("..." if b < len(line) else "")


def main():
    scanned = list(files())
    total_stale = 0
    for label, patterns in RENAMES:
        stale, review = [], []
        compiled = [(kind, re.compile(rx), sev, note) for kind, rx, sev, note in patterns]
        for path in scanned:
            rel = os.path.relpath(path, ROOT)
            try:
                with open(path, encoding="utf-8") as fh:
                    for ln, line in enumerate(fh, 1):
                        for kind, rx, sev, note in compiled:
                            m = rx.search(line)
                            if m:
                                (stale if sev == "STALE" else review).append(
                                    (rel, ln, snippet(line, m)))
                                break  # one hit per line per rename is enough
            except (UnicodeDecodeError, IsADirectoryError):
                continue
        print("=" * 78)
        print(label)
        print("-" * 78)
        if not stale and not review:
            print("  clean — no references in any form")
        if stale:
            total_stale += len(stale)
            print(f"  !! STALE ({len(stale)}) — broken refs, fix these:")
            for rel, ln, snip in stale:
                print(f"     {rel}:{ln}: {snip}")
        if review:
            print(f"  ?  REVIEW ({len(review)}) — old title wording, confirm each is legit:")
            for rel, ln, snip in review:
                print(f"     {rel}:{ln}: {snip}")
        print()
    print("=" * 78)
    print(f"scanned {len(scanned)} files.  TOTAL STALE (must-fix): {total_stale}")


if __name__ == "__main__":
    main()
