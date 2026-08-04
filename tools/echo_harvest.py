#!/usr/bin/env python3
"""Stage 0 of the true line edit: harvest cross-chapter echo candidates.

Mechanical, judgment-free, deliberately over-inclusive (same philosophy as
`style_sheet_harvest.py`): it catalogs repetition the prose actually contains —
distinctive n-grams recurring across chapters, rare-word reuse, and repeated
sentence openers — so the echo-rulings pass works from an inventory instead of
each per-chapter editor rediscovering half of it. Flags, never fixes. Whether
an echo is a seeded thread (protect) or an accident (fix) is an authorial
ruling recorded in audits/line-edit/echo-rulings.md, not here.

Usage: tools/echo_harvest.py [-o audits/line-edit/echo-inventory.md]
"""

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES = ROOT / "scenes"

# Function words: an n-gram made only of these is connective tissue, not an
# echo. Content words outside this set make an n-gram "distinctive".
COMMON = set(
    """
    a about above after again against all almost along already also always am
    an and another any anything are around as at away back be because been
    before behind being below between both but by came can cannot come could
    did didn't do does doesn't doing don't down each else even ever every
    everything far felt few first for from get go going gone good got had
    hadn't half hand hands has have haven't having he head her here hers
    herself him himself his how i i'd i'll i'm i've if in into is isn't it
    it's its itself just keep kept knew know last left less let like little
    long look looked looking made make making many may maybe me might mind
    more most mouth much must my myself near need never new next no nor not
    nothing now of off on once one only onto or other our out over own put
    right said same saw say see seen she should side since so some something
    sometimes soon still such take than that that's the their them themselves
    then there these they thing things think this those though thought three
    through time to told too took toward turned two under until up upon us
    very voice want wanted was wasn't way we well went were weren't what when
    where which while who whole why will with without won't would wouldn't
    yes yet you your
    """.split()
)

MIN_N, MAX_N = 3, 8          # n-gram sizes
MIN_CONTENT = 2              # distinctive words required in an n-gram
MAX_GRAM_USES = 8            # above this it's texture/idiom, not an echo
RARE_MAX_TOTAL = 6           # a word this rare, reused, is an echo candidate
OPENER_LEN = 3               # words of each sentence opener compared


def load_prose(path):
    """Scene text minus the H1, the italic metadata block before the first
    ---, and horizontal rules."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    out, seen_rule = [], False
    for ln in lines:
        if ln.startswith("# "):
            continue
        if ln.strip() == "---":
            seen_rule = True
            continue
        if not seen_rule:
            continue
        out.append(ln)
    if not out:
        out = [ln for ln in lines if not ln.startswith("# ") and ln.strip() != "---"]
    return "\n".join(out)


def sentences(text):
    flat = re.sub(r"\s+", " ", text.replace("*", ""))
    return [s for s in re.split(r"(?<=[.!?])[\"'”’)\]]*\s+", flat) if s.strip()]


def words(sent):
    return [w.lower() for w in re.findall(r"[A-Za-z][\w'’]*", sent)]


def ngram_echoes(corpus):
    """Distinctive n-grams appearing in 2+ chapters. Longest-match wins:
    an n-gram wholly inside a reported longer one (same file set) is dropped."""
    locs = defaultdict(lambda: defaultdict(int))  # gram -> slug -> count
    for slug, prose in corpus.items():
        for sent in sentences(prose):
            ws = words(sent)
            for n in range(MIN_N, MAX_N + 1):
                for i in range(len(ws) - n + 1):
                    gram = ws[i : i + n]
                    if sum(1 for w in gram if w not in COMMON) >= MIN_CONTENT:
                        locs[" ".join(gram)][slug] += 1
    multi = {
        g: fs for g, fs in locs.items()
        # crosses a chapter boundary, and rare enough to be an echo rather
        # than the book's ambient texture
        if len(fs) >= 2 and sum(fs.values()) <= MAX_GRAM_USES
    }
    # subsumption: drop g if a longer reported gram contains it and appears in
    # every file g appears in at least as often
    by_len = sorted(multi, key=lambda g: -len(g.split()))
    kept = []
    for g in by_len:
        gs, gf = f" {g} ", multi[g]
        subsumed = any(
            f" {g} " in f" {k} " or k.startswith(g + " ") or k.endswith(" " + g)
            for k in kept
            if set(gf) <= set(multi[k])
        )
        if not subsumed:
            kept.append(g)
    rows = []
    for g in kept:
        fs = multi[g]
        total = sum(fs.values())
        rows.append((g, total, len(fs), fs))
    rows.sort(key=lambda r: (-r[2], -r[1], r[0]))
    return rows


def rare_words(corpus):
    """Words rare book-wide (2..RARE_MAX_TOTAL uses) that appear in 2+
    chapters — the striking-word-reused-innocently case."""
    counts, files = Counter(), defaultdict(lambda: defaultdict(int))
    for slug, prose in corpus.items():
        for w in words(prose):
            if w in COMMON or len(w) < 5 or "'" in w or "’" in w:
                continue
            counts[w] += 1
            files[w][slug] += 1
    rows = [
        (w, counts[w], files[w])
        for w in counts
        if 2 <= counts[w] <= RARE_MAX_TOTAL and len(files[w]) >= 2
    ]
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows


def openers(corpus):
    """Repeated sentence-opening word patterns (first OPENER_LEN words),
    book-wide frequency >= 8 — pet-construction candidates."""
    counts, files = Counter(), defaultdict(set)
    for slug, prose in corpus.items():
        for sent in sentences(prose):
            ws = words(sent)
            if len(ws) >= OPENER_LEN:
                op = " ".join(ws[:OPENER_LEN])
                counts[op] += 1
                files[op].add(slug)
    rows = [
        (op, c, sorted(files[op]))
        for op, c in counts.most_common()
        if c >= 8 and len(files[op]) >= 3
    ]
    return rows


def fmt_files(fs):
    if isinstance(fs, dict):
        items = sorted(fs.items(), key=lambda kv: (-kv[1], kv[0]))
        parts = [f"{s} ×{n}" if n > 1 else s for s, n in items]
    else:
        parts = list(fs)
    if len(parts) > 8:
        parts = parts[:8] + [f"… ({len(fs)} files)"]
    return ", ".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-o", "--out",
        default=str(ROOT / "audits" / "line-edit" / "echo-inventory.md"),
    )
    ap.add_argument("--min-files", type=int, default=2,
                    help="minimum chapters an n-gram must span (default 2)")
    args = ap.parse_args()

    corpus = {p.stem: load_prose(p) for p in sorted(SCENES.glob("*.md"))}
    n_words = sum(len(t.split()) for t in corpus.values())

    grams = [r for r in ngram_echoes(corpus) if r[2] >= args.min_files]
    rare = rare_words(corpus)
    opens = openers(corpus)

    L = []
    L.append("# Echo inventory (line-edit Stage 0 harvest)")
    L.append("")
    L.append(
        f"*Generated by `tools/echo_harvest.py` over {len(corpus)} scene files "
        f"(~{n_words:,} words). Mechanical and over-inclusive by design — every "
        f"item is a candidate, not a finding. Whether an echo is a seeded "
        f"thread (PROTECTED), an accident (FIX-AT), or noise (IGNORE) is an "
        f"authorial ruling recorded in `audits/line-edit/echo-rulings.md`; "
        f"this file regenerates and holds no decisions.*"
    )
    L.append("")

    L.append(f"## 1. Cross-chapter n-gram echoes ({len(grams)} candidates)")
    L.append("")
    L.append(f"Distinctive phrases (3–8 words, ≥{MIN_CONTENT} content words, "
             f"≤{MAX_GRAM_USES} total uses) appearing in 2+ chapters, longest "
             "match reported, most-widespread first.")
    L.append("")
    L.append("| Phrase | Uses | Chapters | Where |")
    L.append("|---|---|---|---|")
    for g, total, nf, fs in grams:
        L.append(f"| {g} | {total} | {nf} | {fmt_files(fs)} |")
    L.append("")

    L.append(f"## 2. Rare-word reuse ({len(rare)} candidates)")
    L.append("")
    L.append(f"Words used {2}–{RARE_MAX_TOTAL}× book-wide, spanning 2+ "
             "chapters — a striking word spent twice is an echo whether or "
             "not the phrasing around it repeats. Rarest first.")
    L.append("")
    L.append("| Word | Uses | Where |")
    L.append("|---|---|---|")
    for w, c, fs in rare:
        L.append(f"| {w} | {c} | {fmt_files(fs)} |")
    L.append("")

    L.append(f"## 3. Repeated sentence openers ({len(opens)} candidates)")
    L.append("")
    L.append(f"First {OPENER_LEN} words of a sentence, ≥8 uses across ≥3 "
             "chapters — pet-construction candidates for the linter.")
    L.append("")
    L.append("| Opener | Uses | Chapters |")
    L.append("|---|---|---|")
    for op, c, fs in opens:
        L.append(f"| {op} | {c} | {len(fs)} |")
    L.append("")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out}: {len(grams)} n-gram, {len(rare)} rare-word, "
          f"{len(opens)} opener candidates")


if __name__ == "__main__":
    main()
