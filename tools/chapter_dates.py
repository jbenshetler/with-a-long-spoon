#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Reader-facing chapter date lines, derived from the chronology.

`meta/meta-plan-chronology.md` is the sole owner of scene dates; this module
only reads it. A heading line is weekday + month + day ("Monday, October 19"),
or a range for a multi-day chapter ("Saturday, October 10 – Sunday, October 11").
The year is NEVER shown (author ruling 2026-10-24): it is used here only to
check that each weekday matches its date on the hidden 2026–27 calendar
(fall in 2026, January onward in 2027).

    tools/chapter_dates.py            # every drafted chapter: N, slug, heading
    tools/chapter_dates.py --check    # exit 1 on a weekday that does not match
                                      # its date or a `days:` anchor an edit lost;
                                      # approximate/missing dates do not fail

A multi-day chapter carries a `days:` metadata segment in its chronology entry,
e.g. `days: Sat Sep 19 | Fri Sep 25 @ "Six days later, the professor"`: the
first day runs from the top (it may precede the entry's own date, as for a
diptych whose first panel is earlier); each later day names the opening words of the
section (after a `---` break) where it begins. The chapter heading shows the
first day; each later day gets its own line at that section, unless the part
ends `(quiet)`: recorded for the tools, not shown to readers.

The stable source for chapter-date calculation (author ruling 2026-10-24): the
capture/cold-read dated packets, the epub and the chronology reader all take their
date lines from here (date_lines() for renderers).
Open-questions #48 (prose temporal claims vs. this spine) builds on it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import volume_scenes  # noqa: E402

CHRONOLOGY = Path(__file__).resolve().parent.parent / "meta" / "meta-plan-chronology.md"

WEEKDAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
          "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
FALL_YEAR = 2026  # hidden; never rendered

POINT_RE = re.compile(
    r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*\.?\s+"
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})\b"
)
ENTRY_RE = re.compile(r"^###\s+\[(SCENE|VIGNETTE)\]\s+")
SLUG_RE = re.compile(r"slug:\s*([a-z0-9-]+)")
DAYS_RE = re.compile(r"days:\s*([^·*]+)")
SCENES = CHRONOLOGY.parent.parent / "scenes"
QUIET = "(quiet)"


class DateError(ValueError):
    """The chapter has no exact date to render (missing or approximate)."""


class WeekdayMismatch(DateError):
    """The chronology's weekday contradicts its date: a canon error."""


class AnchorMissing(DateError):
    """A `days:` anchor no longer opens a section of the scene file."""


def _year(month: int) -> int:
    return FALL_YEAR if month >= 8 else FALL_YEAR + 1


def _metadata_lines() -> dict[str, str]:
    lines = CHRONOLOGY.read_text(encoding="utf-8").split("\n")
    out: dict[str, str] = {}
    for i, line in enumerate(lines):
        if ENTRY_RE.match(line) and i + 1 < len(lines):
            m = SLUG_RE.search(lines[i + 1])
            if m:
                out[m.group(1)] = lines[i + 1]
    return out


def _date_segment(meta: str) -> str | None:
    """The first metadata segment carrying an exact weekday date."""
    for seg in meta.strip().strip("*").split("·"):
        if seg.strip().lower().startswith("days:"):
            continue
        if POINT_RE.search(seg):
            return seg.strip().strip("*").strip()
    return None


def _points(seg: str, slug: str) -> list[dt.date]:
    points = []
    for wd, mon, day in POINT_RE.findall(seg):
        month = MONTHS[mon.lower()[:3]]
        date = dt.date(_year(month), month, int(day))
        if date.weekday() != WEEKDAYS[wd.lower()[:3]]:
            raise WeekdayMismatch(
                f"{slug}: chronology says {wd} {mon} {day}, but that date is a "
                f"{WEEKDAY_NAMES[date.weekday()]} on the hidden calendar"
            )
        points.append(date)
    return points


def _render(d: dt.date) -> str:
    return f"{WEEKDAY_NAMES[d.weekday()]}, {MONTH_NAMES[d.month]} {d.day}"


def _chapter_range(slug: str, meta: str) -> tuple[dt.date, dt.date]:
    seg = _date_segment(meta)
    if seg is None:
        raise DateError(f"{slug}: no exact weekday date in its chronology entry")
    if seg.startswith("~"):
        raise DateError(f"{slug}: chronology date is approximate ({seg!r})")
    pts = _points(seg, slug)
    if pts[-1] < pts[0]:
        raise DateError(f"{slug}: date range runs backwards ({seg!r})")
    return pts[0], pts[-1]


def section_days(slug: str, *, include_quiet: bool = False) -> list[tuple[str | None, str]]:
    """[(anchor, date line), ...]: anchor None for the opening day.

    Single-day and range chapters with no `days:` field return one entry.
    A part ending `(quiet)` is recorded but not shown (author ruling
    2026-10-25: a section line only where the prose does not land the day
    itself); it is omitted unless `include_quiet`."""
    meta = _metadata_lines().get(slug)
    if meta is None:
        raise DateError(f"{slug}: no chronology entry with this slug")
    first, last = _chapter_range(slug, meta)
    m = DAYS_RE.search(meta)
    if not m:
        line = _render(first) if first == last else f"{_render(first)} – {_render(last)}"
        return [(None, line)]
    out: list[tuple[str | None, str]] = []
    prev = None
    for k, part in enumerate(p.strip() for p in m.group(1).split("|")):
        anchor = None
        quiet = part.endswith(QUIET)
        if quiet:
            part = part[: -len(QUIET)].strip()
        if "@" in part:
            part, anchor = (x.strip() for x in part.split("@", 1))
            anchor = anchor.strip('"').strip()
        pts = _points(part, slug)
        if len(pts) != 1:
            raise DateError(f"{slug}: each `days:` part needs one date ({part!r})")
        if (k == 0) != (anchor is None):
            raise DateError(f"{slug}: only the first `days:` part may omit an anchor")
        if prev and pts[0] < prev:
            raise DateError(f"{slug}: `days:` dates run backwards")
        prev = pts[0]
        if quiet and k == 0:
            raise DateError(f"{slug}: the opening day cannot be quiet")
        out.append((anchor, _render(pts[0]), quiet))
    _check_anchors(slug, [a for a, _, _ in out if a])
    return [(a, line) for a, line, q in out if include_quiet or not q]


def _section_openings(text: str) -> list[str]:
    lines = text.split("\n")
    opens = []
    for i, line in enumerate(lines):
        if line.strip() == "---":
            for nxt in lines[i + 1:]:
                if nxt.strip():
                    opens.append(nxt.strip())
                    break
    return opens


def _check_anchors(slug: str, anchors: list[str]) -> None:
    opens = _section_openings((SCENES / f"{slug}.md").read_text(encoding="utf-8"))
    for a in anchors:
        if sum(o.startswith(a) for o in opens) != 1:
            raise AnchorMissing(
                f"{slug}: `days:` anchor {a!r} does not open exactly one section "
                f"of scenes/{slug}.md — an edit moved it; update the chronology"
            )


def heading(slug: str) -> str:
    """The date line under the chapter title; raises DateError if not exact."""
    return section_days(slug)[0][1]


def dated_text(slug: str, text: str) -> str:
    """Insert each later day's line at the top of the section it anchors.

    `text` is the chapter body (as given to readers); the heading line is the
    caller's to place under the title."""
    days = section_days(slug)
    lines = text.split("\n")
    for anchor, line in days[1:]:
        for i, ln in enumerate(lines):
            if ln.strip().startswith(anchor):
                lines[i:i] = [f"*{line}*", ""]
                break
        else:
            raise AnchorMissing(f"{slug}: anchor {anchor!r} not found in the text given")
    return "\n".join(lines)

def date_lines(slug: str, text: str) -> tuple[str | None, dict[int, str]]:
    """(heading, {0-based line index: date line}) for a renderer.

    The index is the source line that opens each later day's section, so a
    renderer can place the date there without altering the text (the chronology
    reader keys `:N` jumps to source lines). A chapter without an exact date
    returns (None, {}): nothing is shown rather than a guess."""
    try:
        days = section_days(slug)
    except DateError:
        return None, {}
    lines = text.split("\n")
    at: dict[int, str] = {}
    for anchor, line in days[1:]:
        for i, ln in enumerate(lines):
            if anchor and ln.strip().startswith(anchor):
                at[i] = line
                break
    return days[0][1], at


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    drafted = [s for s in volume_scenes.all_scenes() if s["drafted"]]
    errors = inexact = 0
    for n, s in enumerate(drafted, 1):
        try:
            line = heading(s["slug"])
        except (WeekdayMismatch, AnchorMissing) as exc:
            errors += 1
            line = f"!! {exc}"
        except DateError as exc:
            inexact += 1
            line = f"~  {exc}"
        if not args.check or line[:2] in ("!!", "~ "):
            print(f"{n:3d}  {s['tag']:<8} {s['slug']:<22} {line}")
            if not args.check and not line.startswith(("!!", "~")):
                shown = section_days(s["slug"])
                for day in section_days(s["slug"], include_quiet=True)[1:]:
                    tag = "" if day in shown else "   (quiet: not shown)"
                    print(f"{'':37}{day[1]}   @ {day[0]!r}{tag}")
    if args.check:
        print(f"{len(drafted) - errors - inexact}/{len(drafted)} exact · "
              f"{inexact} without an exact date · {errors} error(s) (weekday mismatch or lost anchor)")
        sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
