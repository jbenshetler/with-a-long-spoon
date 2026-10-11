#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Before a cut lands, find out whether readers praised what it removes.

The defect class, from `my-friend-randi.md:115`: commit e52a7d8d trimmed "the
wanting coming up hand in hand with the mortification and sharper for it" on
one capture reader's complaint ("I didn't need it labeled"). Six of six cold
reads, seven capture gates, and eight authorship audits had praised it, and the
chapter's triage doc listed it under Protected positives. The complaint
arrived as a verbatim quote; the praise was spread over twenty files, much of
it paraphrase ("the heat came up through the mortification", "sharper for
it"). Nothing weighed one against the other before the cut.

So, for removed prose, this searches the review corpus by three keys, because
reviewers praise by paraphrase as often as by quote:

  * the removed run verbatim,
  * its distinctive 3-word fragments,
  * the stems of its rare words that no longer appear in the chapter
    ("mortif" catches "mortified", "mortification").

It also reads the chapter's `meta/meta-triage-<slug>.md` for the same keys,
flagging any hit inside a Protected-positives section.

Mechanical, free, deterministic. Like the style linter and orphan_refs it
FLAGS, never fixes, and over-flags on purpose: a hit may be neutral mention or
a complaint, so read the snippet. The author rules.

Usage:
    tools/praise_check.py                         # uncommitted scene edits vs HEAD
    tools/praise_check.py --rev e52a7d8d          # what a past commit removed,
                                                  # against the reviews before it
    tools/praise_check.py --slug my-friend-randi --text "the wanting coming up…"
                                                  # a cut you are about to make
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "reviews"

STOP = set("""a an the and or but if then so of to in on at by for with from up down out
off over under into onto as is was were be been being am are it its it's this that these
those he she him her his hers they them their we us our you your i me my mine not no nor
had has have do did does done would could should will can may might must just only very
too all any some each every one two what which who whom whose when where why how there
here than like still even more most much many such own same back again ever never once
s t d ll re ve m""".split())

WORD = re.compile(r"[A-Za-z][A-Za-z'’]*")


def words(text: str) -> list[str]:
    return [w.lower().replace("’", "'") for w in WORD.findall(text)]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def removed_runs(diff: str) -> dict[str, list[str]]:
    """slug -> removed word-runs (word-level diff within each hunk)."""
    out: dict[str, list[str]] = {}
    slug = None
    minus: list[str] = []
    plus: list[str] = []

    def flush():
        if slug and minus:
            a = " ".join(minus).split()
            b = " ".join(plus).split()
            sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
            for tag, i1, i2, _, _ in sm.get_opcodes():
                if tag in ("delete", "replace"):
                    run = " ".join(a[i1:i2])
                    if len(words(run)) >= 2 or any(
                            len(w) >= 7 and w not in STOP for w in words(run)):
                        out.setdefault(slug, []).append(run)
        minus.clear()
        plus.clear()

    for line in diff.splitlines():
        if line.startswith("diff --git"):
            flush()
            m = re.search(r" b/scenes/([^/]+)\.md$", line)
            slug = m.group(1) if m else None
        elif line.startswith("@@"):
            flush()
        elif line.startswith("-") and not line.startswith("---"):
            minus.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            plus.append(line[1:])
        elif line.startswith(" "):
            flush()
    flush()
    return out


def chapter_number(slug: str) -> int | None:
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import capture_dag  # noqa: PLC0415
        return capture_dag.slugs().index(slug) + 1
    except Exception:
        return None


def review_files(slug: str, rev: str | None = None) -> list[Path]:
    n = chapter_number(slug)
    pats = [rf"^reviews/cold-read/[^/]+/{re.escape(slug)}\.md$",
            rf"^reviews/authorship-audit/[^/]+/{re.escape(slug)}--[^/]*\.md$"]
    if n:
        pats.append(rf"^reviews/capture-panel/[^/]+/dag/[^/]+/gate-ch{n:03d}\.md$")
    if rev:  # the reviews as they stood when the cut was made
        listing = git("ls-tree", "-r", "--name-only", rev, "reviews/").splitlines()
    else:
        listing = [str(p.relative_to(ROOT)) for p in REVIEWS.rglob("*.md")]
    return sorted(ROOT / f for f in listing if any(re.match(p, f) for p in pats))


def read(path: Path, rev: str | None) -> str:
    if rev:
        return git("show", f"{rev}:{path.relative_to(ROOT)}")
    return path.read_text(errors="replace")


def keys(run: str, chapter_now: str) -> tuple[list[str], list[str]]:
    ws = words(run)
    now = " ".join(words(chapter_now))
    frags = []
    for i in range(len(ws) - 2):
        tri = ws[i:i + 3]
        if sum(w not in STOP for w in tri) >= 2:
            f = " ".join(tri)
            if f not in now and f not in frags:
                frags.append(f)
    stems = []
    for w in ws:
        if len(w) >= 7 and w not in STOP:
            st = w[:6]
            if st not in now and st not in stems:
                stems.append(st)
    return frags, stems


def search(path: Path, run: str, frags: list[str], stems: list[str],
           rev: str | None = None):
    text = read(path, rev)
    flat = " ".join(words(text))
    kind = None
    if " ".join(words(run)) in flat and len(words(run)) >= 3:
        kind = "verbatim"
    elif any(f in flat for f in frags):
        kind = "fragment"
    elif any(re.search(r"\b" + re.escape(s), flat) for s in stems):
        kind = "stem"
    if not kind:
        return None
    pats = [re.escape(f).replace(r"\ ", r"\W+") for f in frags] + \
           [r"\b" + re.escape(s) for s in stems]
    snip = ""
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            s = text[max(0, m.start() - 90): m.end() + 90].replace("\n", " ")
            snip = "…" + s + "…"
            break
    return kind, snip


def triage_hits(slug: str, frags: list[str], stems: list[str]) -> list[str]:
    p = ROOT / "meta" / f"meta-triage-{slug}.md"
    if not p.exists():
        return []
    hits, section = [], ""
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if line.startswith("#"):
            section = line.strip("# ").strip()
        flat = " ".join(words(line))
        if any(f in flat for f in frags) or any(
                re.search(r"\b" + re.escape(s), flat) for s in stems):
            tag = "PROTECTED" if "protected" in section.lower() else section[:40]
            hits.append(f"{p.relative_to(ROOT)}:{i} [{tag}] {line.strip()[:160]}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    ap.add_argument("--rev", help="check what this commit removed")
    ap.add_argument("--slug", help="scene slug (required with --text)")
    ap.add_argument("--text", help="prose you are about to cut")
    ap.add_argument("--snippets", type=int, default=3)
    args = ap.parse_args()

    if args.text:
        if not args.slug:
            ap.error("--text needs --slug")
        runs = {args.slug: [args.text]}
    elif args.rev:
        runs = removed_runs(git("show", "--format=", args.rev, "--", "scenes/"))
    else:
        runs = removed_runs(git("diff", "HEAD", "--", "scenes/"))

    flagged = 0
    for slug, rs in runs.items():
        scene = ROOT / "scenes" / f"{slug}.md"
        chapter_now = scene.read_text() if scene.exists() else ""
        if args.text:  # the cut hasn't happened yet: judge against the chapter minus it
            chapter_now = chapter_now.replace(args.text, " ")
        before = f"{args.rev}^" if args.rev else None
        files = review_files(slug, before)
        for run in rs:
            frags, stems = keys(run, chapter_now)
            if not frags and not stems:
                continue
            found = [(f, r) for f in files if (r := search(f, run, frags, stems, before))]
            tri = triage_hits(slug, frags, stems)
            if not found and not tri:
                continue
            flagged += 1
            by = {k: sum(1 for _, (kk, _) in found if kk == k)
                  for k in ("verbatim", "fragment", "stem")}
            print(f"\n{slug}: removed «{run[:200]}»")
            print(f"  reviews: {len(found)} files "
                  f"(verbatim {by['verbatim']}, fragment {by['fragment']}, "
                  f"stem-only {by['stem']}) of {len(files)} searched")
            for t in tri:
                print(f"  triage: {t}")
            for f, (k, s) in found[: args.snippets]:
                print(f"  [{k}] {f.relative_to(ROOT)}: {s[:260]}")
    if not flagged:
        print("(no reviewer mentions of removed prose)")
    print("\nFLAGS, not findings: read each snippet — a hit may be praise, "
          "neutral mention, or the complaint that motivated the cut.")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
