#!/usr/bin/env python3
"""Standalone authority for per-volume scene inventory.

Parses `meta/meta-plan-chronology.md` directly (no dependency on
`cold_read_batch.py` or its hand-maintained `FALL_SCENES` list) so the
volume boundary can never silently drift out of sync with the chronology,
which is the source of truth for volume membership via `◆ VOLUME ONE/TWO/THREE`
markers.

No third-party imports; safe to run under bare `python3` (does not import
`tomllib` or `cold_read_batch` at module load).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHRONOLOGY = Path(__file__).resolve().parent.parent / "meta" / "meta-plan-chronology.md"

_VOLUME_WORDS = {"ONE": 1, "TWO": 2, "THREE": 3}

_VOLUME_RE = re.compile(r"^\*?\*?◆ VOLUME (ONE|TWO|THREE)")
_HEADING_RE = re.compile(r"^### \[(SCENE|VIGNETTE)\]\s+(.+?)\s*$")
_SLUG_RE = re.compile(r"slug:\s*([a-z0-9-]+)")


def all_scenes() -> list[dict]:
    """Parse the chronology and return the ordered scene inventory.

    Each entry: {"slug", "title", "volume", "drafted"}.
    """
    lines = CHRONOLOGY.read_text().splitlines()
    scenes: list[dict] = []
    volume = None
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        vm = _VOLUME_RE.match(line)
        if vm:
            volume = _VOLUME_WORDS[vm.group(1)]
            i += 1
            continue
        hm = _HEADING_RE.match(line)
        if hm:
            title = hm.group(2)
            # find the next non-empty line
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            meta_line = lines[j] if j < n else ""
            sm = _SLUG_RE.search(meta_line)
            if sm:
                slug = sm.group(1)
                drafted = "Draft complete" in meta_line
                scenes.append(
                    {
                        "slug": slug,
                        "title": title,
                        "volume": volume,
                        "drafted": drafted,
                    }
                )
            i = j + 1
            continue
        i += 1
    return scenes


def scenes_for_volume(vol: int, drafted_only: bool = False) -> list[dict]:
    result = [s for s in all_scenes() if s["volume"] == vol]
    if drafted_only:
        result = [s for s in result if s["drafted"]]
    return result


def volume_one_slugs(drafted_only: bool = True) -> list[str]:
    return [s["slug"] for s in scenes_for_volume(1, drafted_only=drafted_only)]


_SLUG_VOLUME: dict[str, int] | None = None


def volume_dir(slug: str) -> str:
    """Volume subdir name ('vol1', 'vol2', ...) for a scene slug, from the
    chronology (source of truth). Used to place per-scene review files in the
    volume-split lanes (grounded-cold-read, judge). Raises KeyError if the slug
    is not in the chronology — callers writing a brand-new scene's review must
    add its chronology entry first."""
    global _SLUG_VOLUME
    if _SLUG_VOLUME is None:
        _SLUG_VOLUME = {s["slug"]: s["volume"] for s in all_scenes()}
    vol = _SLUG_VOLUME.get(slug)
    if vol is None:
        raise KeyError(f"slug {slug!r} not found in chronology; add its entry before writing a review")
    return f"vol{vol}"


def _parse_fall_scenes_slugs(path: Path):
    """Textually extract the ordered Volume One slug prefix from
    `cold_read_batch.py`'s `FALL_SCENES` list literal, without importing it
    (that module requires tomllib, unavailable under bare python3 here).

    Returns the slug list up to (not including) the first entry that also
    contains `"volume_start": 2` (i.e. the first Volume Two entry, `among-friends`).
    """
    text = path.read_text()
    m = re.search(r"FALL_SCENES\s*=\s*\[(.*?)\n\]", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"could not locate FALL_SCENES list literal in {path}")
    body = m.group(1)
    # Split into individual dict-literal entries by top-level `{...}` blocks.
    entries = re.findall(r"\{[^{}]*\}", body)
    slugs = []
    for entry in entries:
        sm = re.search(r'"slug":\s*"([a-z0-9-]+)"', entry)
        if not sm:
            continue
        if re.search(r'"volume_start":\s*2\b', entry):
            break
        slugs.append(sm.group(1))
    return slugs


def _cli():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", nargs="?", const="all", metavar="N", help="list volume N (default all)")
    parser.add_argument("--check", action="store_true", help="validate chronology Volume One drafted slugs against FALL_SCENES")
    args = parser.parse_args()

    if args.check:
        batch_path = Path(__file__).resolve().parent / "cold_read_batch.py"
        provider_slugs = _parse_fall_scenes_slugs(batch_path)
        chron_slugs = volume_one_slugs(drafted_only=True)
        if provider_slugs == chron_slugs:
            print(f"OK: {len(chron_slugs)} Volume One slugs match")
            sys.exit(0)
        else:
            only_provider = [s for s in provider_slugs if s not in chron_slugs]
            only_chron = [s for s in chron_slugs if s not in provider_slugs]
            print("MISMATCH")
            if only_provider:
                print(f"  in FALL_SCENES only: {only_provider}")
            if only_chron:
                print(f"  in chronology only: {only_chron}")
            first_diverge = None
            for idx, (a, b) in enumerate(zip(provider_slugs, chron_slugs)):
                if a != b:
                    first_diverge = idx
                    break
            else:
                if len(provider_slugs) != len(chron_slugs):
                    first_diverge = min(len(provider_slugs), len(chron_slugs))
            if first_diverge is not None:
                print(f"  first diverging index: {first_diverge}")
            sys.exit(1)

    if args.list is not None:
        if args.list == "all":
            vols = [1, 2, 3]
        else:
            vols = [int(args.list)]
        for vol in vols:
            for s in scenes_for_volume(vol):
                print(f"{s['volume']}\t{'drafted' if s['drafted'] else 'planned'}\t{s['slug']}\t{s['title']}")
        return

    # default: print everything
    for s in all_scenes():
        print(f"{s['volume']}\t{'drafted' if s['drafted'] else 'planned'}\t{s['slug']}\t{s['title']}")


if __name__ == "__main__":
    _cli()
