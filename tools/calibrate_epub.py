#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
"""Extract a prose sample from a published epub so `reading_effort.py` can be
calibrated against real books instead of only against this one.

The problem it solves: every figure the reading-effort pass reports is relative
to this novel's own corpus. That answers "is this chapter heavy FOR ME" and
cannot answer "is this heavy for a published book in this genre" — which is the
question that decides whether a finding is worth acting on at all.

Extracts chapter XHTML in spine order, strips markup, and takes a CONTIGUOUS
sample of roughly a target word count, starting far enough in to clear front
matter. Contiguous rather than sampled at random because the fatigue profile
needs real sequence — a shuffled bag of paragraphs has no runs in it.

The sample is written where the epub lives, under a gitignored path: it is a
substantial extract of a copyrighted book and must not enter version control.
Only the derived STATISTICS are safe to commit.

Usage:
    tools/calibrate_epub.py ref/sirens-and-muses.epub --words 11200
    tools/reading_effort.py audits/reading-effort/.calib/sirens-and-muses.md --json
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CALIB = REPO / "audits" / "reading-effort" / ".calib"

BLOCK_END = re.compile(r"</(p|div|h[1-6]|li|blockquote)\s*>", re.I)
TAG = re.compile(r"<[^>]+>")
DROP = re.compile(r"<(script|style)[^>]*>.*?</\1\s*>", re.I | re.S)


def spine_docs(z: zipfile.ZipFile) -> list[str]:
    """Content documents in reading order, per the OPF spine."""
    opf_name = next((n for n in z.namelist() if n.endswith(".opf")), None)
    if not opf_name:
        return sorted(n for n in z.namelist()
                      if n.lower().endswith((".xhtml", ".html", ".htm")))
    opf = z.read(opf_name).decode("utf-8", "replace")
    base = opf_name.rsplit("/", 1)[0] if "/" in opf_name else ""
    href = dict(re.findall(r'<item\s[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf))
    href.update({i: h for h, i in re.findall(
        r'<item\s[^>]*href="([^"]+)"[^>]*id="([^"]+)"', opf)})
    order = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf)
    names = set(z.namelist())
    out = []
    for ident in order:
        h = href.get(ident)
        if not h:
            continue
        h = h.split("#")[0]
        for cand in (f"{base}/{h}" if base else h, h):
            if cand in names:
                out.append(cand)
                break
    return out


def paragraphs(xhtml: str) -> list[str]:
    body = DROP.sub(" ", xhtml)
    body = BLOCK_END.sub("\n", body)
    body = TAG.sub("", body)
    out = []
    for line in body.split("\n"):
        t = html.unescape(line).replace("\xa0", " ")
        t = re.sub(r"\s+", " ", t).strip()
        # A paragraph of prose, not a heading, page number or running head.
        if len(t.split()) >= 12:
            out.append(t)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("epub")
    ap.add_argument("--words", type=int, default=11200,
                    help="target sample size (default matches the-bench)")
    ap.add_argument("--skip", type=float, default=0.15,
                    help="fraction of the book to skip first, clearing front "
                         "matter and opening-chapter throat-clearing")
    args = ap.parse_args()

    path = Path(args.epub)
    if not path.is_file():
        sys.exit(f"no such epub: {path}")
    with zipfile.ZipFile(path) as z:
        paras: list[str] = []
        for doc in spine_docs(z):
            try:
                paras.extend(paragraphs(z.read(doc).decode("utf-8", "replace")))
            except KeyError:
                continue
    if not paras:
        sys.exit("extracted no prose paragraphs — epub layout not recognised")

    total = sum(len(p.split()) for p in paras)
    start = 0
    seen = 0
    for i, p in enumerate(paras):
        if seen >= total * args.skip:
            start = i
            break
        seen += len(p.split())

    sample, n = [], 0
    for p in paras[start:]:
        sample.append(p)
        n += len(p.split())
        if n >= args.words:
            break

    CALIB.mkdir(parents=True, exist_ok=True)
    out = CALIB / f"{path.stem}.md"
    out.write_text(
        f"# {path.stem}\n\n---\n\n" + "\n\n".join(sample) + "\n",
        encoding="utf-8")
    print(f"{path.name}: {total:,} words total; sampled {n:,} words "
          f"({len(sample)} paragraphs, from {args.skip:.0%} in)")
    print(f"→ {out.relative_to(REPO)}  (gitignored: copyrighted extract)")


if __name__ == "__main__":
    main()
