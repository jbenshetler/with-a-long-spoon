#!/usr/bin/env python3
"""Pass 0 of the copyedit: harvest style-sheet candidates from scenes/.

Mechanical, judgment-free, deliberately over-inclusive (same philosophy as
`na.py style`): it catalogs what the prose actually does — proper nouns and
their casing variants, hyphenation variants, numerals in context, the italics
census, and a punctuation census — so the rulings pass (Pass 1) works from an
inventory instead of a blank page. Flags, never fixes.

Usage: tools/style_sheet_harvest.py [-o style/style-sheet-candidates.md]
"""

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES = ROOT / "scenes"

# Words that capitalize mid-sentence without being names (sentence-ish starters
# inside dialogue, the pronoun I, etc.) — trimmed from proper-noun candidates.
STOP = {
    "I", "I'm", "I'll", "I'd", "I've", "A", "An", "The", "And", "But", "Or",
    "So", "Then", "He", "She", "It", "They", "You", "We", "His", "Her", "Him",
    "Hers", "Their", "Its", "Your", "My", "Mine", "That", "This", "There",
    "What", "When", "Where", "Which", "Who", "Why", "How", "If", "In", "On",
    "At", "Of", "For", "To", "By", "With", "From", "As", "Not", "No", "Yes",
    "Now", "Just", "Oh", "Okay", "OK", "Well", "Because", "Maybe", "Don't",
    "Doesn't", "Didn't", "Wasn't", "Isn't", "Can't", "Couldn't", "Wouldn't",
    "Won't", "Let", "Come", "Go", "Get", "Good", "All", "One", "Two", "Some",
    "Nothing", "Everything", "Something", "Anything", "Nobody", "Everyone",
    "Someone", "Anyone", "Please", "Thank", "Thanks", "Hi", "Hey", "Hello",
    "Fine", "Right", "Sure", "Sorry", "Wait", "Stop", "Look", "Listen", "See",
    "Tell", "Say", "Said", "Do", "Did", "Does", "Is", "Are", "Was", "Were",
    "Be", "Been", "Have", "Has", "Had", "Will", "Would", "Should", "Could",
    "Can", "May", "Might", "Must", "Every", "Each", "Both", "Any", "Once",
    "Never", "Always", "Still", "Even", "Also", "Only", "Very", "Too", "Up",
    "Down", "Out", "Over", "Under", "Again", "Here", "Away", "Back", "Yeah",
    "Nope", "Mm", "Hm", "Huh", "Um", "Uh", "Ah", "God", "Jesus", "Christ",
}
# Kept even though common: honorifics that matter for the sheet.
KEEP = {"Dr", "Mr", "Mrs", "Ms", "Miss", "Professor", "Coach", "Aunt", "Uncle"}

SPELLED_NUMS = (
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
    "thirty forty fifty sixty seventy eighty ninety hundred thousand"
).split()


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
            continue  # metadata block (or preamble) before first rule
        out.append(ln)
    if not out:  # no metadata block — take everything but the H1
        out = [ln for ln in lines if not ln.startswith("# ") and ln.strip() != "---"]
    return "\n".join(out)


def sentences(text):
    flat = re.sub(r"\s+", " ", text)
    return re.split(r"(?<=[.!?])[\"'”’)\]]*\s+", flat)


def proper_nouns(corpus):
    """corpus: {slug: prose}. Returns (phrase_counter, phrase_files,
    case_variants) counting only mid-sentence capitalized runs."""
    counts, files = Counter(), defaultdict(set)
    for slug, prose in corpus.items():
        plain = prose.replace("*", "").replace("_", "")
        for sent in sentences(plain):
            toks = re.findall(r"[A-Za-z][\w'’\-]*", sent)
            i, first_alpha = 0, 0
            while i < len(toks):
                t = toks[i]
                if t[0].isupper() and (i > first_alpha) and (
                    t not in STOP or t in KEEP
                ):
                    j = i
                    run = []
                    while j < len(toks) and (
                        toks[j][0].isupper()
                        and (toks[j] not in STOP or toks[j] in KEEP or j > i)
                    ):
                        if toks[j] in STOP and toks[j] not in KEEP and j > i:
                            break
                        run.append(toks[j])
                        j += 1
                    phrase = " ".join(run)
                    counts[phrase] += 1
                    files[phrase].add(slug)
                    i = j
                else:
                    i += 1
    variants = defaultdict(set)
    for p in counts:
        variants[p.lower()].add(p)
    variants = {k: v for k, v in variants.items() if len(v) > 1}
    return counts, files, variants


def hyphenation(corpus):
    """Compounds seen in 2+ of the forms hyphenated / open / closed."""
    all_text = "\n".join(corpus.values()).replace("*", "")
    lower = all_text.lower()
    hyph = Counter(
        m.group(0).lower()
        for m in re.finditer(r"\b([a-z]+)-([a-z]+)\b", lower)
    )
    rows = []
    for comp, n_h in hyph.most_common():
        a, b = comp.split("-", 1)
        n_open = len(re.findall(rf"\b{a} {b}\b", lower))
        n_closed = len(re.findall(rf"\b{a}{b}\b", lower))
        forms = sum(1 for n in (n_h, n_open, n_closed) if n)
        if forms >= 2:
            rows.append((comp, n_h, n_open, n_closed))
    return rows


def numerals(corpus):
    hits = []
    for slug, prose in corpus.items():
        for m in re.finditer(r"\d[\d:.,]*", prose):
            s, e = max(0, m.start() - 45), min(len(prose), m.end() + 45)
            ctx = re.sub(r"\s+", " ", prose[s:e]).strip()
            hits.append((slug, m.group(0), ctx))
    return hits


def italics(corpus):
    spans, per_file = Counter(), Counter()
    for slug, prose in corpus.items():
        for m in re.finditer(r"(?<!\*)\*([^*\n]+)\*(?!\*)", prose):
            span = m.group(1).strip()
            spans[span] += 1
            per_file[slug] += 1
    return spans, per_file


def punct(corpus):
    checks = {
        "em dash spaced ( — )": r" — ",
        "em dash unspaced (a—b)": r"(?<=\S)—(?=\S)",
        "double hyphen (--)": r"(?<!-)--(?!-)",
        "en dash (–)": r"–",
        "ellipsis char (…)": r"…",
        "three dots (...)": r"\.\.\.",
        "curly double quotes (“”)": r"[“”]",
        "straight double quote (\")": r'"',
        "curly apostrophe (’)": r"’",
        "straight apostrophe (')": r"'",
    }
    totals = Counter()
    per_file = defaultdict(Counter)
    for slug, prose in corpus.items():
        for name, pat in checks.items():
            n = len(re.findall(pat, prose))
            totals[name] += n
            if n:
                per_file[name][slug] += n
    return checks, totals, per_file


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--out", default=str(ROOT / "style" / "style-sheet-candidates.md"))
    args = ap.parse_args()

    corpus = {
        p.stem: load_prose(p) for p in sorted(SCENES.glob("*.md"))
    }
    words = sum(len(t.split()) for t in corpus.values())

    pn_counts, pn_files, pn_variants = proper_nouns(corpus)
    hyph_rows = hyphenation(corpus)
    num_hits = numerals(corpus)
    it_spans, it_files = italics(corpus)
    p_checks, p_totals, p_files = punct(corpus)

    L = []
    L.append("# Style-sheet candidates (Pass 0 harvest)")
    L.append("")
    L.append(f"*Generated by `tools/style_sheet_harvest.py` over {len(corpus)} scene files "
             f"(~{words:,} words), metadata headers stripped. Mechanical and over-inclusive "
             f"by design — every item is a candidate for a Pass 1 ruling, not a finding. "
             f"Regenerate any time; rulings live in `style/style-sheet.md`, not here.*")
    L.append("")

    L.append("## 1. Proper nouns (mid-sentence capitalized runs)")
    L.append("")
    L.append("### Casing/spelling variants (rule on one canonical form)")
    L.append("")
    if pn_variants:
        for key in sorted(pn_variants):
            forms = " / ".join(
                f"`{f}` ×{pn_counts[f]}" for f in sorted(pn_variants[key])
            )
            L.append(f"- {forms}")
    else:
        L.append("- none found")
    L.append("")
    L.append("### Full inventory (frequency ≥ 2, then singletons)")
    L.append("")
    L.append("| Term | Count | Files |")
    L.append("|---|---|---|")
    multi = [(p, c) for p, c in pn_counts.most_common() if c >= 2]
    for p, c in multi:
        fs = sorted(pn_files[p])
        shown = ", ".join(fs[:6]) + (f", … ({len(fs)} files)" if len(fs) > 6 else "")
        L.append(f"| {p} | {c} | {shown} |")
    singles = sorted(p for p, c in pn_counts.items() if c == 1)
    L.append("")
    L.append(f"**Singletons ({len(singles)}):** " + ", ".join(
        f"{p} ({next(iter(pn_files[p]))})" for p in singles))
    L.append("")

    L.append("## 2. Hyphenation variants (compound seen in 2+ forms)")
    L.append("")
    L.append("| Compound | hyphenated | open | closed |")
    L.append("|---|---|---|---|")
    for comp, h, o, c in hyph_rows:
        L.append(f"| {comp} | {h} | {o} | {c} |")
    L.append("")

    L.append("## 3. Numerals in prose (rule: when digits vs. spelled out)")
    L.append("")
    if num_hits:
        L.append("| File | Numeral | Context |")
        L.append("|---|---|---|")
        for slug, num, ctx in num_hits:
            ctx = ctx.replace("|", "\\|")
            L.append(f"| {slug} | {num} | …{ctx}… |")
    else:
        L.append("No digit tokens in prose — all numbers spelled out.")
    L.append("")
    spelled = Counter()
    all_lower = "\n".join(corpus.values()).lower()
    for w in SPELLED_NUMS:
        n = len(re.findall(rf"\b{w}\b", all_lower))
        if n:
            spelled[w] = n
    L.append("Spelled-out number frequency (for the ruling's context): " + ", ".join(
        f"{w} ×{n}" for w, n in spelled.most_common()))
    L.append("")

    L.append("## 4. Italics census")
    L.append("")
    rep = [(s, c) for s, c in it_spans.most_common() if c >= 2]
    L.append(f"{sum(it_spans.values())} italic spans total; "
             f"{len(it_spans)} distinct. Heaviest files: " + ", ".join(
                 f"{s} ({n})" for s, n in it_files.most_common(8)) + ".")
    L.append("")
    L.append("### Repeated italicized spans (frequency ≥ 2)")
    L.append("")
    for s, c in rep:
        L.append(f"- *{s}* ×{c}")
    L.append("")
    L.append("### Long italic spans (> 12 words — check: interiority convention or emphasis creep?)")
    L.append("")
    long_spans = [s for s in it_spans if len(s.split()) > 12]
    for s in long_spans:
        L.append(f"- *{s[:120]}{'…' if len(s) > 120 else ''}*")
    if not long_spans:
        L.append("- none")
    L.append("")

    L.append("## 5. Punctuation census")
    L.append("")
    L.append("| Mark | Total | Files (if scarce — the outliers) |")
    L.append("|---|---|---|")
    for name in p_checks:
        n = p_totals[name]
        note = ""
        if 0 < n <= 30:
            note = ", ".join(f"{s} ×{c}" for s, c in p_files[name].most_common())
        L.append(f"| {name} | {n} | {note} |")
    L.append("")

    out = Path(args.out)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(L)} lines)")


if __name__ == "__main__":
    main()
