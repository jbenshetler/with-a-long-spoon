#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Emit spec-blind CLEAN source for checkpoint extraction.

Volume One checkpoints read raw prose from the opening. Later-volume checkpoints
make the one permitted consolidation hop: the frozen final checkpoint of the
previous volume plus raw prose from the current volume's opening through the
target boundary. This module builds both the canonical full-manuscript bundle
used for provenance and the exact current-volume window used for that hop.

The cleaner below MIRRORS cold_read_batch.clean_scene_text (kept in sync by
hand — it is imported there for the reader harness). It strips the H1 and the
leading italic POV/purpose header (a spoiler) so the bundle is byte-identical
to what a blind reader sees. (Historically duplicated so this tool could run
on py3.10; it now requires 3.11 via its uv shebang, and the copy is kept in
sync by hand until someone folds it back.)

Usage:
  tools/checkpoint_bundle.py                 # all drafted Volume One chapters
  tools/checkpoint_bundle.py --to 10         # chapters 1..10 (1-based, inclusive)
  tools/checkpoint_bundle.py --from 11 --to 20
  tools/checkpoint_bundle.py --no-jacket     # omit the jacket copy
Order and inventory come from tools/volume_scenes.py (chronology-authoritative).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import volume_scenes  # noqa: E402

CLEANER_VERSION = 1


def source_fingerprints(bundle: str, extractor_prompt: str) -> dict[str, str | int]:
    """Fingerprint the exact checkpoint source and the rules that compress it."""
    bundle_sha256 = hashlib.sha256(bundle.encode("utf-8")).hexdigest()
    extractor_sha256 = hashlib.sha256(extractor_prompt.encode("utf-8")).hexdigest()
    payload = json.dumps(
        {
            "bundle_sha256": bundle_sha256,
            "cleaner_version": CLEANER_VERSION,
            "extractor_sha256": extractor_sha256,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "source_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "bundle_sha256": bundle_sha256,
        "cleaner_version": CLEANER_VERSION,
        "extractor_sha256": extractor_sha256,
    }


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
        # marker-first layout: the H1 sits after the POV marker — strip it too
        while body and not body[0].strip():
            body.pop(0)
        if body and body[0].startswith("# "):
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
    # The H1 is usually line 1, but new chapters may open with the italic POV
    # marker instead — take the first H1 wherever it sits in the header block.
    for line in (REPO / f"scenes/{slug}.md").read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return slug


def reader_slugs() -> list[str]:
    """The full cross-volume chapter sequence: Vol 1 drafted first, then Vol 2
    drafted, then Vol 3 drafted, in chronology order. The Volume 1 boundary is
    parsed from the chronology, so inserting a drafted Volume 1 scene updates the
    reader inventory instead of leaving stale hand-maintained chapter numbers. This
    is the single source of truth shared by the authoring lane (checkpoint_context)
    and the grounded cold-read lane (cold_read_grounded), so the two can never drift
    on inventory."""
    v1 = volume_scenes.volume_one_slugs(drafted_only=True)
    v2 = [s["slug"] for s in volume_scenes.scenes_for_volume(2, drafted_only=True)]
    v3 = [s["slug"] for s in volume_scenes.scenes_for_volume(3, drafted_only=True)]
    return v1 + v2 + v3


def build_bundle(start: int = 1, end: int | None = None, jacket: bool = True,
                 slugs: list[str] | None = None) -> str:
    """Return the clean prose bundle for chapters [start..end] (1-based inclusive).

    `slugs` is the chapter universe to index into; it defaults to Vol 1 drafted
    (the minting path's contract). Cross-volume callers pass reader_slugs()."""
    if slugs is None:
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


CONFIG_PATH = REPO / "reviews" / "cold-read" / "ensemble-config.toml"


def _load_checkpoint_seeds(path: Path = CONFIG_PATH) -> dict[int, str]:
    """Read `[checkpoint_seeds]` from the shared ensemble config.

    The seam lives in ONE file shared by every tool (author ruling 2026-09-26);
    it was a literal dict here until then. Keys are decade boundaries, values
    are slugs (a story landmark must be named, never numbered — see
    volume_scenes.volume_last_slug).
    """
    with path.open("rb") as handle:
        raw = tomllib.load(handle).get("checkpoint_seeds") or {}
    return {int(k): str(v) for k, v in raw.items()}


# boundary -> the SLUG whose checkpoint seeds it; sourced from ensemble-config.toml.
CHECKPOINT_SEEDS: dict[int, str] = _load_checkpoint_seeds()


def checkpoint_plan(end: int) -> tuple[int | None, int]:
    """Return the explicit `(seed_boundary, raw_start)` policy for `end`.

    Volume One boundaries are raw passes from chapter 1. Later-volume boundaries
    must be named in ``[checkpoint_seeds]`` (ensemble-config.toml); future seams are not inferred from
    mutable drafted-scene counts or decade arithmetic.
    """
    slugs = reader_slugs()
    if not (1 <= end <= len(slugs)):
        raise ValueError(f"end {end} out of bounds (1..{len(slugs)} drafted)")
    volume_one_last = volume_scenes.volume_last_slug(1, drafted_only=True)
    volume_one_end = volume_scenes.chapter_number(volume_one_last)
    if end <= volume_one_end:
        return None, 1
    seed_slug = CHECKPOINT_SEEDS.get(end)
    if seed_slug is None:
        raise ValueError(
            f"no explicit checkpoint seed policy for boundary {end}; "
            "add an author-approved [checkpoint_seeds] entry in ensemble-config.toml"
        )
    first_seeded_boundary = min(CHECKPOINT_SEEDS)
    if end == first_seeded_boundary and seed_slug != volume_one_last:
        raise ValueError(
            f"checkpoint seed policy for boundary {end} seeds from {seed_slug!r} "
            f"(ch{volume_scenes.chapter_number(seed_slug):03d}), but drafted Volume One "
            f"ends at {volume_one_last!r} (ch{volume_one_end:03d}); "
            "update [checkpoint_seeds] in ensemble-config.toml and remint affected checkpoints atomically"
        )
    seed_boundary = volume_scenes.chapter_number(seed_slug)
    return seed_boundary, seed_boundary + 1


def checkpoint_body(raw: str) -> str:
    """Strip a persisted checkpoint's provenance header."""
    marker = "\n---\n\n"
    return raw.split(marker, 1)[1].strip() if marker in raw else raw.strip()

def checkpoint_metadata(raw: str, key: str) -> str | None:
    """Read one ` · `-delimited provenance field from a checkpoint header."""
    header = raw.split("\n---\n", 1)[0]
    match = re.search(rf"(?m)(?:^| · )\*?{re.escape(key)}: ([^·*\n]+)", header)
    return match.group(1).strip() if match else None


def validate_seed_lineage(
    seed_raw: str,
    *,
    expected_boundary: int,
    expected_model: str,
    extractor_prompt: str,
) -> str:
    """Validate a frozen seed; return ``current`` or explicit legacy ``unknown``."""
    boundary_match = re.search(
        r"^# Checkpoint — through Chapter (\d+)\b", seed_raw, re.MULTILINE
    )
    if not boundary_match or int(boundary_match.group(1)) != expected_boundary:
        raise ValueError(f"seed header must declare Chapter {expected_boundary}")
    actual_model = checkpoint_metadata(seed_raw, "model")
    if actual_model != expected_model:
        raise ValueError(
            f"seed model {actual_model or 'missing'} does not match {expected_model}"
        )
    declared_source = checkpoint_metadata(seed_raw, "source-sha256")
    if declared_source is None:
        return "unknown"
    expected_source = source_fingerprints(
        build_reader_bundle(expected_boundary), extractor_prompt
    )["source_sha256"]
    if declared_source != expected_source:
        raise ValueError(
            f"seed ck-ch{expected_boundary:03d} is stale: "
            f"{declared_source[:12]} != current {str(expected_source)[:12]}"
        )
    return "current"


def build_seeded_source(
    seed_raw: str, seed_boundary: int, start: int, end: int, window: str
) -> str:
    """Build the exact source text shown to a volume-boundary extractor."""
    return (
        f"===== PRIOR CHECKPOINT THROUGH CHAPTER {seed_boundary} =====\n\n"
        f"{checkpoint_body(seed_raw)}\n\n"
        f"===== RAW CURRENT-VOLUME SPAN: CHAPTERS {start} THROUGH {end} =====\n\n"
        f"{window}"
    )


def build_reader_bundle(end: int, start: int = 1) -> str:
    """Exact cross-volume raw source for reader chapters `start..end`.

    Volume entry packets appear once when their opening chapter is in the span.
    For Volume One boundaries this delegates to the legacy bundle byte-for-byte.
    """
    v1 = volume_scenes.volume_one_slugs(drafted_only=True)
    if start == 1 and end <= len(v1):
        return build_bundle(1, end, jacket=True, slugs=v1)
    slugs = reader_slugs()
    if not (1 <= start <= end <= len(slugs)):
        raise ValueError(f"range {start}..{end} out of bounds (1..{len(slugs)} drafted)")
    out: list[str] = []
    for index, slug in enumerate(slugs[start - 1 : end], start=start):
        volume = volume_scenes.volume_of(slug)
        opening_slug, packet = volume_packet(volume)
        if slug == opening_slug and packet:
            out.append(
                f"===== VOLUME {volume} ENTRY PACKET (marketing, not story) =====\n\n{packet}\n"
            )
        out.append(f"\n\n===== CHAPTER {index}: {display_title(slug)} =====\n")
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
