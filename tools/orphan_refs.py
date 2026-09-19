#!/usr/bin/env python3
"""Find references orphaned by an edit — text that still points at something
the revision removed.

The defect class, from `the-pointing-game.md`: commit ade99b4b cut the whole
paragraph introducing a passer-by "in a camel coat too warm for the afternoon",
including Randi's verdict "She'd be a project." A later sentence still reads
"the closed camel-coat project would never laugh at anything in public" — a
callback to a character and a coinage the reader now never sees.

No reader-side instrument can catch this. Read as it now stands the sentence
parses fine as an archetype; the evidence is not in the text, it is in the
diff. So this is git archaeology, not a model: for every commit touching a
scene, take the distinctive terms that the commit REMOVED and did not re-add,
and report the ones that still appear in the chapter today.

Deliberately mechanical and deterministic — it costs nothing, so it can run as
a pre-commit warning. Like the style linter it FLAGS, never fixes, and it
over-flags on purpose: a surviving term is often a legitimate ordinary use.
The author judges.

Usage:
    tools/orphan_refs.py                  # Volume One, whole history
    tools/orphan_refs.py --volume 2
    tools/orphan_refs.py --staged         # pre-commit mode: only staged scenes
    tools/orphan_refs.py --max-df 3       # tighten/loosen the rarity filter
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import volume_scenes  # noqa: E402  (stdlib-only; safe under bare python3)

# Unigrams this common carry no referential weight even when rare in the corpus.
STOP = set("""a an the and or but so then than that this these those of in on at to for with
from by as is was were be been being it its it's he she they them his her their you your i me my
we us our not no nor if when while after before again once here there all any both each few more
most other some such only own same too very can will just should now what which who whom whose how
why where said says say into out up down over under through about against between during without
within along across behind beyond off near upon around back still even also like unless until
because since though although whether one two three first last next another every""".split())

WORD_RE = re.compile(r"[a-z0-9']+")


def norm(text: str) -> list[str]:
    """Lowercase word tokens. Hyphens become breaks so `camel-coat` and
    `camel coat` are the same two tokens — the camel case turns on exactly
    that, since the edit removed the spaced form and the hyphenated one
    survived."""
    return WORD_RE.findall(text.lower().replace("-", " ").replace("—", " "))


def terms(text: str) -> set[str]:
    """Distinctive unigrams plus every bigram. Bigrams carry most of the
    signal: `camel coat` is specific where `camel` and `coat` are not."""
    toks = norm(text)
    out = {t for t in toks if t not in STOP and len(t) > 2}
    out |= {f"{a} {b}" for a, b in zip(toks, toks[1:])}
    return out


DEFINITE = {"the", "that", "those", "this", "these", "her", "his", "their",
            "its", "another", "same", "other"}


def is_definite(line: str, term: str) -> bool:
    """Does this occurrence point BACK at something?

    A dangling reference is definite — "the closed camel-coat project" assumes
    a project the reader has met. An indefinite or bare use ("a camel coat",
    "live inside") introduces or merely describes, and is not evidence of a
    missing antecedent. This is the filter that separates the real orphan from
    every ordinary phrase a revision happened to touch.
    """
    toks = norm(line)
    want = term.split()
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            # allow intervening adjectives: "the closed camel-coat project"
            if any(w in DEFINITE for w in toks[max(0, i - 2):i]):
                return True
    return False


INDEF = {"a", "an"}


def introduced_in(text: str, term: str) -> bool:
    """Did this text INTRODUCE the term — "a camel coat", "an old bench"?

    This is the other half of the defect and the one that makes it precise.
    An orphan is not merely a phrase a revision touched; it is an antecedent
    that was cut. The signature is an indefinite introduction in the removed
    text ("in a camel coat too warm for the afternoon") paired with a definite
    callback that survived ("the closed camel-coat project"). Requiring both
    ends drops the ordinary verb-phrase churn that any rewrite produces.
    """
    toks = norm(text)
    want = term.split()
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            if any(w in INDEF for w in toks[max(0, i - 3):i]):
                return True
    return False


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True).stdout


def document_frequency(slugs: list[str]) -> Counter:
    """How many chapters each term appears in. A term spread across the book is
    ambient texture; the interesting orphan is concentrated."""
    df: Counter = Counter()
    for s in slugs:
        p = REPO / "scenes" / f"{s}.md"
        if p.exists():
            df.update(terms(p.read_text(encoding="utf-8")))
    return df


def commits_for(path: str) -> list[str]:
    out = git("log", "--format=%H", "--", path)
    return [ln for ln in out.splitlines() if ln.strip()]


def diff_terms(sha: str, path: str) -> tuple[set[str], set[str], str]:
    """(removed terms, added terms, raw removed text) for one commit."""
    diff = git("show", "--format=", "--unified=0", sha, "--", path)
    removed, added = [], []
    for line in diff.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    cut = "\n".join(removed)
    return terms(cut), terms("\n".join(added)), cut


def scan(slug: str, df: Counter, max_df: int, max_hits: int,
         definite_only: bool = True) -> list[dict]:
    path = f"scenes/{slug}.md"
    current = (REPO / path)
    if not current.exists():
        return []
    text = current.read_text(encoding="utf-8")
    live = terms(text)
    lines = text.splitlines()
    findings = []
    seen: set[str] = set()
    for sha in commits_for(path):
        removed, added, cut_text = diff_terms(sha, path)
        # Removed and NOT re-added by the same commit (else it merely moved),
        # yet still present in the chapter today.
        for t in sorted((removed - added) & live):
            if t in seen or df[t] > max_df:
                continue
            if definite_only and not introduced_in(cut_text, t):
                continue   # the cut did not introduce it; not an antecedent
            seen.add(t)
            hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
                    if not ln.startswith("#")
                    and t in " ".join(norm(ln))
                    and (not definite_only or is_definite(ln, t))]
            # An orphan is a LONE dangling reference. A term still used several
            # times is doing ordinary work; only the survivor-of-a-cut reads as
            # a callback to something gone.
            if not hits or len(hits) > max_hits:
                continue
            subject = git("show", "--format=%s", "-s", sha).strip()
            findings.append({"slug": slug, "term": t, "sha": sha[:8],
                             "subject": subject, "df": df[t], "hits": hits})
    return findings


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--volume", type=int, default=1)
    ap.add_argument("--slugs", nargs="*", help="limit to these chapters")
    ap.add_argument("--staged", action="store_true",
                    help="pre-commit mode: only staged scenes/*.md; never fails the commit")
    ap.add_argument("--any-reference", action="store_true",
                    help="also report indefinite/bare uses (much noisier)")
    ap.add_argument("--max-hits", type=int, default=2,
                    help="skip terms still used more than N times (default 2)")
    ap.add_argument("--max-df", type=int, default=3,
                    help="skip terms appearing in more than N chapters (default 3)")
    args = ap.parse_args()

    vol = volume_scenes.volume_slugs(args.volume, drafted_only=True)
    if args.staged:
        staged = [Path(p).stem for p in git("diff", "--cached", "--name-only").split()
                  if p.startswith("scenes/") and p.endswith(".md")]
        slugs = [s for s in vol if s in staged]
    elif args.slugs:
        slugs = [s for s in vol if s in args.slugs]
    else:
        slugs = vol
    if not slugs:
        return

    df = document_frequency(vol)
    allf = []
    for s in slugs:
        allf.extend(scan(s, df, args.max_df, args.max_hits, not args.any_reference))

    allf.sort(key=lambda f: (" " not in f["term"], f["df"], len(f["hits"])))

    if not allf:
        print(f"orphan-refs: nothing flagged across {len(slugs)} chapter(s)")
        return

    print(f"orphan-refs: {len(allf)} candidate(s) across {len(slugs)} chapter(s)")
    print("  a term whose introducing text was cut, still referenced in the chapter")
    print("  FLAGS, never findings — an ordinary surviving use is common.\n")
    for f in allf:
        print(f"  {f['slug']}  «{f['term']}»  (in {f['df']} chapter(s))")
        print(f"    cut by {f['sha']}  {f['subject'][:70]}")
        for ln, txt in f["hits"][:2]:
            print(f"    :{ln}  {txt[:150]}")
        print()
    if args.staged:
        print("  (warning only — this never blocks a commit)")


if __name__ == "__main__":
    main()
