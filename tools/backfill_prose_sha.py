#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Backfill `prose-sha` into review/gate headers written before sha tracking existed.

Both reader instruments now record the hash of the chapter text a reader actually
read (`capture_dag.py`, `cold_read_grounded.py`), so a later edit to the prose is
detectable instead of silent. Everything written before that lands as
"unverifiable" — true, but useless.

This reconstructs the missing hash from git. A gate/review carries a date in its
header; the chapter text *as of that date* is what the reader saw. So:

    git rev-list -1 --before=<date 23:59:59> HEAD -- scenes/<slug>.md
    git show <commit>:scenes/<slug>.md      → clean → sha256[:12]

The reconstruction is honest about its own limits and records them:

  * It resolves to the last commit touching that scene on or before the header
    date. A read taken between two same-day commits can land on the earlier text.
    Same-day ambiguity is reported, not hidden.
  * A scene with no commit at or before the date (drafted and read before its
    first commit) cannot be reconstructed; those stay unverifiable.
  * Backfilled hashes are written as `prose-sha~<hex>` — the tilde marks them
    *reconstructed*, never to be confused with a hash recorded at read time.
    The staleness checkers accept both forms; only this script writes the tilde.

Usage:
  tools/backfill_prose_sha.py --dry-run          # report only, touch nothing
  tools/backfill_prose_sha.py                    # write
  tools/backfill_prose_sha.py --what cold-read   # limit to one instrument
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
HAS_SHA_RE = re.compile(r"prose-sha ~?[0-9a-f]{12}")


def clean(raw: str) -> str:
    """Mirror of checkpoint_bundle.clean_scene_text, but on a git blob rather than a
    path — it reads from disk, and we need historical text.

    MUST stay byte-identical in behaviour to that function: the whole point is that a
    backfilled hash equals the hash the live checker computes. Hashing the *raw* file
    instead would mark every backfilled entry permanently stale.
    """
    lines = raw.splitlines()
    start = 1 if lines and lines[0].startswith("# ") else 0
    divider = None
    for i in range(start, min(len(lines), start + 12)):
        if lines[i].strip() == "---":
            divider = i
            break
    body = lines[divider + 1:] if divider is not None else lines[start:]
    if divider is None:
        while body and not body[0].strip():
            body.pop(0)
        if body and body[0].lstrip().startswith("*"):
            body.pop(0)
        while body and not body[0].strip():
            body.pop(0)
        if body and body[0].startswith("# "):
            body.pop(0)
    body = [ln for ln in body if not ln.lstrip().startswith("[AI")]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return "\n".join(body)


def file_commit_date(f: Path) -> str | None:
    """Last commit date of a review file — the fallback when its header carries no
    date (the cold-read header form). The review was written at or before the commit
    that introduced it, so the chapter text as of that date is what the reader saw."""
    rel = f.relative_to(REPO).as_posix()
    out = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short",
                          "--", rel], cwd=REPO, capture_output=True, text=True)
    return out.stdout.strip() or None


def scene_text_at(slug: str, date: str) -> tuple[str | None, str | None, bool]:
    """(text, commit, same_day_ambiguous) for scenes/<slug>.md as of `date`."""
    path = f"scenes/{slug}.md"
    rev = subprocess.run(
        ["git", "rev-list", "-1", f"--before={date} 23:59:59", "HEAD", "--", path],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not rev:
        return None, None, False
    text = subprocess.run(["git", "show", f"{rev}:{path}"],
                          cwd=REPO, capture_output=True, text=True).stdout
    if not text:
        return None, None, False
    same_day = len(subprocess.run(
        ["git", "rev-list", f"--since={date} 00:00:00", f"--until={date} 23:59:59",
         "HEAD", "--", path], cwd=REPO, capture_output=True, text=True
    ).stdout.split()) > 1
    return text, rev[:12], same_day


def targets(what: str) -> list[tuple[Path, str]]:
    """(file, slug) pairs needing a backfill."""
    out = []
    if what in ("all", "cold-read"):
        for f in sorted((REPO / "reviews" / "cold-read").glob("*/*.md")):
            if f.parent.name == "checkpoints" or f.stem.startswith("ck-"):
                continue
            out.append((f, f.stem))
    if what in ("all", "capture"):
        slugs = checkpoint_bundle.reader_slugs()
        for f in sorted((REPO / "reviews" / "capture-panel").glob("*/dag/*/gate-ch*.md")):
            m = re.search(r"gate-ch(\d{3})", f.name)
            if not m:
                continue
            i = int(m.group(1))
            if 1 <= i <= len(slugs):
                out.append((f, slugs[i - 1]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--what", choices=["all", "cold-read", "capture"], default="all")
    args = ap.parse_args()

    done = skipped = nodate = nocommit = ambiguous = 0
    for f, slug in targets(args.what):
        head = f.read_text(encoding="utf-8").split("\n\n", 2)
        header = "\n\n".join(head[:2])
        if HAS_SHA_RE.search(header):
            skipped += 1
            continue
        d = DATE_RE.search(header)
        date = d.group(1) if d else file_commit_date(f)
        if not date:
            nodate += 1
            continue
        text, commit, amb = scene_text_at(slug, date)
        if text is None:
            nocommit += 1
            continue
        sha = hashlib.sha256(clean(text).encode()).hexdigest()[:12]
        if amb:
            ambiguous += 1
        if not args.dry_run:
            body = f.read_text(encoding="utf-8")
            # insert before the closing '*' of the italic provenance line
            new = re.sub(r"(\n\*[^\n]*?)(\*\n)",
                         lambda m: f"{m.group(1)} · prose-sha ~{sha}{m.group(2)}",
                         body, count=1)
            if new == body:  # single-line header form (capture gates)
                new = re.sub(r"( · \d{4}-\d{2}-\d{2}\*)",
                             lambda m: f" · prose-sha ~{sha}{m.group(1)}", body, count=1)
            f.write_text(new, encoding="utf-8")
        done += 1

    verb = "would backfill" if args.dry_run else "backfilled"
    print(f"{verb}: {done}")
    print(f"  already had a sha : {skipped}")
    print(f"  no date in header : {nodate}")
    print(f"  no commit at/before date (unreconstructable): {nocommit}")
    print(f"  same-day ambiguity (hash may be the earlier text): {ambiguous}")


if __name__ == "__main__":
    main()
