#!/usr/bin/env python3
"""Find settled rulings whose quoted line no longer exists in the prose.

The problem this solves. Three lanes hold the author's settled decisions —
`audits/line-audit/<slug>.md`, `audits/line-edit/<slug>.md`, and
`meta/meta-triage-<slug>.md` ("left standing — do not re-litigate"). Unlike the
style linter and the reading-effort ledger, which key each suppression to a
sentence FINGERPRINT and therefore re-arm the moment that sentence is edited,
these three are prose documents carrying only a date. After a round of small
edits there is no way to tell which rulings still describe the text.

Chapter-level staleness is the wrong instrument here. A `prose-sha` over the
whole chapter marks a ruling about paragraph 40 stale because paragraph 3
changed — the failure the capture lane needed three-tier staleness to survive.
These rulings are about individual lines, so the anchor is the line.

The anchor already exists informally: these documents QUOTE the prose they rule
on. This tool reads the quotes back out and checks them against the chapter.

Three outcomes per quote, and the middle one is the whole point:

  PRESENT     the quoted text is still in the chapter — the ruling still applies
  MOVED       absent now, but present in the chapter AS OF the ruling's date —
              the prose changed under a settled decision. THIS is the finding.
  UNVERIFIED  absent from both — not a verbatim quote of this chapter at all
              (a paraphrase, the audit's own wording, or a line from a
              neighbouring chapter). Noise, hidden unless asked for.

The as-of comparison is what keeps the signal clean. Without it every paraphrase
in a 50-file corpus reads as a broken anchor. The git technique is the one
`backfill_prose_sha.py` already uses: resolve the last commit touching the scene
on or before the document's header date, and read the text as it stood.

Deterministic, no model calls, no network, stdlib only. Flags, never fixes —
same discipline as the linter and the line audit: a moved anchor is a question
for the author, not a defect.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import volume_scenes  # noqa: E402  (to tell a dead chapter from a lane artifact)

REPO = Path(__file__).resolve().parent.parent
SCENES = REPO / "scenes"

# Lanes that hold rulings in prose. (doc-glob, how to get the slug from the stem)
LANES = [
    ("audits/line-audit", "*.md", lambda s: s),
    ("audits/line-edit", "*.md", lambda s: s),
    ("meta", "meta-triage-*.md", lambda s: s[len("meta-triage-"):]),
]

# A ruling's date, from the document header: "# Line audit — famished (2026-08-01)"
# or "# Triage — Famished (line-audit pass, 2026-08-01)".
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# Quoted prose. The corpus quotes with straight or curly double quotes, often
# wrapped in bold/italic markers which are stripped by _norm.
QUOTE_RE = re.compile(r'["“]([^"”\n]{12,400})["”]')

# Shorter than this and a "quote" is usually a single word or a stock phrase that
# appears everywhere; it produces noise in both directions.
MIN_WORDS = 6

# A ruling that RECORDS A CUT quotes text it expects to be gone. Those quotes are
# absent by design, so counting them as moved anchors inflates the finding --
# discovered 2026-10-09, when 25 of this chapter's 49 anchors turned out to be
# cut-records from the triage's own "Fixed" sections. The corpus writes them in
# one shape, the verb close behind the closing quote:
#     - :119 "He'd guessed wrong." cut -- reversed from the finding: ...
# so only a short tail is searched. A wider window would swallow "a trim was
# proposed and declined", which is a LIVE ruling and must still be checked.
CUT_RE = re.compile(r"\b(cut|deleted|removed|dropped|replaced|recast|reversed)\b", re.I)
CUT_TAIL = 80

# Chapters the chronology knows about, so a ruling doc with no prose file can be
# told apart from a lane artifact that was never a chapter (echo-inventory).
KNOWN_SLUGS = {s["slug"] for s in volume_scenes.all_scenes()}

_TRANS = str.maketrans({
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "—": "-", "–": "-", "…": "...", " ": " ",
})


def _norm(s: str) -> str:
    """Comparison form: unify punctuation, drop emphasis markers, collapse space.

    Markdown emphasis is dropped on BOTH sides rather than only in the quote,
    because the prose italicises interiority and a quote of it may or may not
    carry the asterisks.
    """
    s = s.translate(_TRANS)
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def ever_existed(slug: str) -> bool:
    """Did scenes/<slug>.md ever exist in history?

    Separates a MERGED chapter — whose rulings are orphaned and are a real
    finding — from a lane artifact that was never a chapter at all
    (echo-inventory.md). `all-told` is the worked case: merged 2026-10-07 and
    dropped from the chronology, so a chronology-membership test alone calls it
    an artifact and hides three documents of live rulings."""
    try:
        out = subprocess.run(["git", "log", "--all", "-1", "--format=%h",
                              "--", f"scenes/{slug}.md"],
                             cwd=REPO, capture_output=True, text=True, check=True)
        return bool(out.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def scene_text(slug: str) -> str | None:
    p = SCENES / f"{slug}.md"
    return _norm(p.read_text(encoding="utf-8")) if p.exists() else None


def scene_text_asof(slug: str, date: str) -> str | None:
    """The chapter as it stood on `date`, or None if git can't resolve it."""
    rel = f"scenes/{slug}.md"
    try:
        rev = subprocess.run(
            ["git", "rev-list", "-1", f"--before={date} 23:59:59", "HEAD", "--", rel],
            cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()
        if not rev:
            return None
        blob = subprocess.run(["git", "show", f"{rev}:{rel}"],
                              cwd=REPO, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    return _norm(blob)


def quotes(doc: str) -> list[tuple[str, bool]]:
    """Each quote, paired with whether its ruling records cutting it."""
    out, seen = [], set()
    for m in QUOTE_RE.finditer(doc):
        q = _norm(m.group(1))
        if len(q.split()) < MIN_WORDS or q in seen:
            continue
        seen.add(q)
        out.append((q, bool(CUT_RE.search(doc[m.end():m.end() + CUT_TAIL]))))
    return out


def check_doc(path: Path, slug: str) -> dict:
    doc = path.read_text(encoding="utf-8")
    cur = scene_text(slug)
    res = {"path": path, "slug": slug, "present": 0, "moved": [], "unverified": 0,
           "cut_records": 0, "date": None, "note": None, "orphan": False}
    if cur is None:
        res["note"] = f"no prose file scenes/{slug}.md"
        res["orphan"] = slug in KNOWN_SLUGS or ever_existed(slug)
        return res
    m = DATE_RE.search(doc.split("\n\n")[0] if "\n\n" in doc else doc[:400])
    res["date"] = m.group(1) if m else None
    asof = scene_text_asof(slug, res["date"]) if res["date"] else None
    if res["date"] and asof is None:
        res["note"] = "no commit of this scene on or before the ruling date"
    for q, is_cut_record in quotes(doc):
        if q in cur:
            res["present"] += 1
        elif is_cut_record:
            res["cut_records"] += 1       # absent because the ruling cut it
        elif asof and q in asof:
            res["moved"].append(q)
        else:
            res["unverified"] += 1
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slugs", nargs="*", help="limit to these chapter slugs")
    ap.add_argument("--show-unverified", action="store_true",
                    help="also count quotes absent from both versions (noise)")
    ap.add_argument("--quiet", action="store_true", help="only report moved anchors")
    args = ap.parse_args()

    docs = []
    for lane, glob, to_slug in LANES:
        for p in sorted((REPO / lane).glob(glob)):
            if p.name == "STATUS.md":
                continue
            slug = to_slug(p.stem)
            if args.slugs and slug not in args.slugs:
                continue
            docs.append((p, slug))
    if not docs:
        print("no ruling documents in scope", file=sys.stderr)
        return 0

    results = [check_doc(p, s) for p, s in docs]
    moved_docs = [r for r in results if r["moved"]]
    tot_present = sum(r["present"] for r in results)
    tot_unver = sum(r["unverified"] for r in results)
    tot_cut = sum(r["cut_records"] for r in results)
    tot_moved = sum(len(r["moved"]) for r in results)

    moved_docs.sort(key=lambda r: -len(r["moved"]))
    for r in moved_docs:
        rel = r["path"].relative_to(REPO)
        print(f"\n{rel}  (ruled {r['date']}) — {len(r['moved'])} anchor(s) moved")
        for q in r["moved"]:
            shown = q if len(q) <= 150 else q[:147] + "..."
            print(f'    "{shown}"')

    if not args.quiet:
        orphans = [r for r in results if r["note"] and r["orphan"]]
        skipped = [r for r in results if r["note"] and not r["orphan"]]
        if orphans:
            print(f"\n{len(orphans)} ruling document(s) for a chapter with NO PROSE FILE "
                  "— merged or renamed, and the rulings were left behind:")
            for r in orphans:
                print(f"    {r['path'].relative_to(REPO)}  (slug {r['slug']})")
        if skipped:
            print(f"\n{len(skipped)} lane artifact(s) skipped (never a chapter): "
                  + ", ".join(r["path"].name for r in skipped))
        print(f"\n{len(results)} ruling document(s) · {tot_present} anchor(s) still present"
              f" · {tot_moved} moved · {tot_cut} cut-record(s) skipped"
              + (f" · {tot_unver} unverified (not verbatim quotes)" if args.show_unverified
                 else ""))
    if tot_moved:
        print(f"\n{tot_moved} settled ruling(s) quote prose that has since changed — "
              "re-read them before trusting the verdict. Flags, not defects.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
