#!/usr/bin/env python3
"""Emit a spec-blind CLEAN prose bundle for the checkpoint extractor.

A checkpoint is minted by feeding a blind-extractor the *clean* text of a
contiguous span of chapters (grounded, single pass — no chaining). This tool
produces exactly that bundle: the public jacket (optional) followed by each
chapter's display title + its clean body, in story order.

The cleaner below MIRRORS cold_read_batch.clean_scene_text (kept in sync by
hand — it is imported there for the reader harness). It strips the H1 and the
leading italic POV/purpose header (a spoiler) so the bundle is byte-identical
to what a blind reader sees. Duplicated only because cold_read_batch imports
tomllib (py3.11+) at module load and this tool must run on py3.10.

Usage:
  tools/checkpoint_bundle.py                 # all drafted Volume One chapters
  tools/checkpoint_bundle.py --to 10         # chapters 1..10 (1-based, inclusive)
  tools/checkpoint_bundle.py --from 11 --to 20
  tools/checkpoint_bundle.py --no-jacket     # omit the jacket copy
Order and inventory come from tools/volume_scenes.py (chronology-authoritative).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import volume_scenes  # noqa: E402


def clean_scene_text(slug: str) -> str:
    """Mirror of cold_read_batch.clean_scene_text — see module docstring."""
    raw = (REPO / f"scenes/{slug}.md").read_text()
    lines = raw.splitlines()
    start = 1 if lines and lines[0].startswith("# ") else 0
    divider = None
    for i in range(start, min(len(lines), start + 12)):
        if lines[i].strip() == "---":
            divider = i
            break
    body = lines[divider + 1 :] if divider is not None else lines[start:]
    if divider is None:
        while body and not body[0].strip():
            body.pop(0)
        if body and body[0].lstrip().startswith("*"):
            body.pop(0)
    body = [ln for ln in body if not ln.lstrip().startswith("[AI")]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    text = "\n".join(body)
    if "[AI" in text:
        raise RuntimeError(f"AI marker survived in {slug}")
    return text


def jacket_packet() -> str:
    """Volume One packet string, regex-extracted from volume-packets.toml."""
    toml = (REPO / "reviews/cold-read/volume-packets.toml").read_text()
    m = re.search(r"packet\s*=\s*'''(.*?)'''", toml, re.DOTALL)
    return m.group(1).strip() if m else ""


def volume_packet(volume: int) -> tuple[str, str]:
    """(opening_slug, packet) for a volume from volume-packets.toml, or ('', '') if
    that volume has no packet yet (fail closed — no jacket for it). Regex-parsed, so it
    stays tomllib-free for the bare-python --check / --emit-prompt path. A volume packet
    is injected EXACTLY ONCE, at its opening_slug chapter (the toml's own contract)."""
    toml = (REPO / "reviews/cold-read/volume-packets.toml").read_text()
    sec = re.search(rf'\[volumes\."{volume}"\](.*?)(?=\n\[|\Z)', toml, re.DOTALL)
    if not sec:
        return "", ""
    body = sec.group(1)
    om = re.search(r"""opening_slug\s*=\s*["']([^"']+)["']""", body)
    pm = re.search(r"packet\s*=\s*'''(.*?)'''", body, re.DOTALL)
    return (om.group(1) if om else "", pm.group(1).strip() if pm else "")


def display_title(slug: str) -> str:
    first = (REPO / f"scenes/{slug}.md").read_text().splitlines()[0]
    return first[2:].strip() if first.startswith("# ") else slug


def build_bundle(start: int = 1, end: int | None = None, jacket: bool = True) -> str:
    """Return the clean prose bundle for chapters [start..end] (1-based inclusive)."""
    slugs = volume_scenes.volume_one_slugs(drafted_only=True)
    end = end if end is not None else len(slugs)
    if not (1 <= start <= end <= len(slugs)):
        raise ValueError(f"range {start}..{end} out of bounds (1..{len(slugs)} drafted)")
    span = slugs[start - 1 : end]

    out: list[str] = []
    if jacket:
        packet = jacket_packet()
        if packet:
            out.append("===== JACKET / GOING-IN FRAMING (marketing, not story) =====\n")
            out.append(packet)
            out.append("")

    for i, slug in enumerate(span, start=start):
        out.append(f"\n\n===== CHAPTER {i}: {display_title(slug)} =====\n")
        out.append(clean_scene_text(slug))

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=None)
    ap.add_argument("--no-jacket", action="store_true")
    args = ap.parse_args()
    sys.stdout.write(build_bundle(args.start, args.end, jacket=not args.no_jacket))


if __name__ == "__main__":
    main()
