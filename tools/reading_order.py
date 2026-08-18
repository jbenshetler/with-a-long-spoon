#!/usr/bin/env python3
"""Reading-order navigator — "what do I read around here?" for the review lanes.

Story order is owned by the chronology (meta-plan-chronology.md); this tool is a
*view* over it, so nothing about order is duplicated into the filesystem. Given a
scene slug it prints a window of neighbouring scenes in story order — by default
the 3 before and 3 after — so you don't have to pop between the chronology and a
directory listing to find the next thing to read.

Usage:
  tools/reading_order.py a-round                 # 3 before + a-round + 3 after
  tools/reading_order.py a-round --before 5      # widen the leading side
  tools/reading_order.py a-round --after 0       # only what precedes it
  tools/reading_order.py among-friends --volume vol2   # window within one volume
  tools/reading_order.py a-round --model claude-opus-4-8  # mark grounded review ✓/✗

Ordinals are the scene's position in the whole chronology (SCENE/VIGNETTE only;
EVENTs are not reading units). The focus slug is marked with ►.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import volume_scenes  # noqa: E402

GROUNDED = REPO / "reviews" / "grounded-cold-read"


def grounded_exists(model: str, slug: str, vol: int) -> bool:
    return (GROUNDED / model / f"vol{vol}" / f"{slug}.md").is_file()


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Show the reading-order window around a scene slug.")
    ap.add_argument("slug", help="scene slug to centre the window on")
    ap.add_argument("--before", type=int, default=3, help="scenes to show before (default 3)")
    ap.add_argument("--after", type=int, default=3, help="scenes to show after (default 3)")
    ap.add_argument("--volume", help="restrict the window to one volume, e.g. vol2")
    ap.add_argument("--model", help="annotate each row with grounded-review presence for this model")
    args = ap.parse_args()

    scenes = volume_scenes.all_scenes()               # story order, SCENE/VIGNETTE only
    ordinals = {s["slug"]: i + 1 for i, s in enumerate(scenes)}   # position in whole chronology

    if args.slug not in ordinals:
        near = [s["slug"] for s in scenes if args.slug in s["slug"]]
        hint = f"  did you mean: {', '.join(near[:5])}" if near else ""
        raise SystemExit(f"slug {args.slug!r} not in the chronology.{hint}")

    view = scenes
    if args.volume:
        want = args.volume.lower().removeprefix("vol")
        try:
            vnum = int(want)
        except ValueError:
            raise SystemExit(f"bad --volume {args.volume!r}; use vol1/vol2/...")
        view = [s for s in scenes if s["volume"] == vnum]
        if args.slug not in {s["slug"] for s in view}:
            raise SystemExit(f"{args.slug!r} is not in vol{vnum}")

    idx = next(i for i, s in enumerate(view) if s["slug"] == args.slug)
    lo = max(0, idx - max(0, args.before))
    hi = min(len(view), idx + max(0, args.after) + 1)
    window = view[lo:hi]

    for s in window:
        focus = "►" if s["slug"] == args.slug else " "
        ordn = ordinals[s["slug"]]
        if args.model:
            tag = "✓" if grounded_exists(args.model, s["slug"], s["volume"]) else "✗"
        else:
            tag = "drafted" if s["drafted"] else "planned"
        print(f"{focus} {ordn:>3}  vol{s['volume']}  {tag:<7}  {s['slug']:<28}  {s['title']}")


if __name__ == "__main__":
    main()
