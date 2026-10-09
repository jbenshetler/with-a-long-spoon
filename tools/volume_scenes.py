#!/usr/bin/env python3
"""Standalone authority for per-volume scene inventory.

Volume IDENTITY (how many volumes there are, their tags, ordinals, titles and
boundary chapters) comes from `meta/meta-volumes.toml` — the single data file.
Scene ORDER and draft status still come from `meta/meta-plan-chronology.md`,
which owns scene inventory; this module joins the two.

Before 2026-10-09 volume membership was parsed from the chronology's
`◆ VOLUME ONE/TWO/THREE` headers. That had two defects, both of which bit:
the parser mapped only the English words ONE/TWO/THREE, so a fourth volume was
unrepresentable; and a duplicate `◆ VOLUME TWO` header (a merged split-experiment
marker left inside the Fall section) was silently accepted by reassigning, so
Volume Two resolved to Fall B + Spring — 77 chapters — and mis-scoped every
caller. Boundaries now live in one validated place and `--check` fails loudly on
a duplicate, a gap, or a chronology header that disagrees.

THE TAG IS THE DURABLE IDENTITY; THE ORDINAL IS DERIVED. Persist `tag`, resolve
`ordinal` at the point of use: splitting the spring moves Summer from 4 to 5
while its tag stays `summer`.

No third-party imports, and deliberately NO `tomllib` — `checkpoint_bundle`'s
bare-python `--check` / `--emit-prompt` path imports this module on a python3
without it. The data file is read with a small hand parser covering only the
subset of TOML it uses.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHRONOLOGY = REPO / "meta" / "meta-plan-chronology.md"
VOLUMES_TOML = REPO / "meta" / "meta-volumes.toml"

_HEADING_RE = re.compile(r"^### \[(SCENE|VIGNETTE)\]\s+(.+?)\s*$")
_SLUG_RE = re.compile(r"slug:\s*([a-z0-9-]+)")

# Retained only so --check can compare the human headers against the data file.
_VOLUME_WORDS = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}
_VOLUME_MARKER_RE = re.compile(r"^\*?\*?◆ VOLUME ([A-Z]+)")


# --------------------------------------------------------------------------
# The data file
# --------------------------------------------------------------------------

def _scalar(raw: str):
    raw = raw.strip()
    if raw.startswith('"""'):
        return raw.strip('"').strip()
    if raw[:1] in {'"', "'"}:
        return raw[1:].rsplit(raw[0], 1)[0]
    if raw in {"true", "false"}:
        return raw == "true"
    try:
        return int(raw)
    except ValueError:
        return raw


def _parse_data(text: str) -> dict:
    """Parse the subset of TOML `meta-volumes.toml` uses.

    Handles `[table]`, `[[array.of.tables]]`, `key = <scalar>` and triple-quoted
    multi-line strings. Comments and blank lines are skipped. Anything fancier is
    not supported on purpose — if the data file needs it, use a real parser in a
    caller that can afford tomllib.
    """
    data: dict = {}
    cursor: dict | None = None
    pending_key: str | None = None
    pending_val: list[str] = []

    def container(path: list[str], array: bool) -> dict:
        node = data
        for part in path[:-1]:
            nxt = node.get(part)
            if isinstance(nxt, list):
                nxt = nxt[-1]
            if not isinstance(nxt, dict):
                nxt = {}
                node[part] = nxt
            node = nxt
        leaf = path[-1]
        if array:
            node.setdefault(leaf, [])
            fresh: dict = {}
            node[leaf].append(fresh)
            return fresh
        node.setdefault(leaf, {})
        return node[leaf]

    for line in text.splitlines():
        if pending_key is not None:
            if '"""' in line:
                pending_val.append(line.split('"""')[0])
                target = cursor if cursor is not None else data
                target[pending_key] = " ".join(
                    " ".join(pending_val).split()
                )
                pending_key, pending_val = None, []
            else:
                pending_val.append(line)
            continue

        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("[["):
            cursor = container(stripped[2:].split("]]")[0].strip().split("."), True)
            continue
        if stripped.startswith("["):
            cursor = container(stripped[1:].split("]")[0].strip().split("."), False)
            continue
        if "=" not in stripped:
            continue
        key, raw = stripped.split("=", 1)
        key, raw = key.strip(), raw.split(" #")[0].strip()
        target = cursor if cursor is not None else data
        if raw.startswith('"""') and not raw.endswith('"""'):
            pending_key = key
            pending_val = [raw[3:]]
            continue
        target[key] = _scalar(raw)
    return data


_DATA: dict | None = None


def _data() -> dict:
    global _DATA
    if _DATA is None:
        _DATA = _parse_data(VOLUMES_TOML.read_text())
    return _DATA


def volumes() -> list[dict]:
    """Every volume record from the data file, in ordinal order."""
    vols = _data().get("volume", [])
    if not vols:
        raise RuntimeError(f"no [[volume]] records in {VOLUMES_TOML}")
    return sorted(vols, key=lambda v: v["ordinal"])


def volume_count() -> int:
    """How many volumes there are. Never hardcode 3."""
    return len(volumes())


def volume_ordinals() -> list[int]:
    """Every volume ordinal, for iteration. Never write `(1, 2, 3)`."""
    return [v["ordinal"] for v in volumes()]


def volume_record(vol: int | str) -> dict:
    """A volume record by ordinal or by tag."""
    for v in volumes():
        if v["ordinal"] == vol or v["tag"] == vol:
            return v
    raise KeyError(
        f"no volume {vol!r} in {VOLUMES_TOML.name} "
        f"(have {[v['tag'] for v in volumes()]})"
    )


def volume_title(vol: int | str) -> str:
    return volume_record(vol)["title"]


def volume_tag(vol: int | str) -> str:
    return volume_record(vol)["tag"]


def spring_split() -> dict:
    """The recorded-but-unapplied spring split, including the reserved title."""
    return _data().get("spring_split", {})


# --------------------------------------------------------------------------
# The join: chronology order x data-file boundaries
# --------------------------------------------------------------------------

def _chronology_scenes() -> list[dict]:
    """Ordered scene inventory from the chronology: slug, title, drafted."""
    lines = CHRONOLOGY.read_text().splitlines()
    scenes: list[dict] = []
    i, n = 0, len(lines)
    while i < n:
        hm = _HEADING_RE.match(lines[i])
        if hm:
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            meta_line = lines[j] if j < n else ""
            sm = _SLUG_RE.search(meta_line)
            if sm:
                scenes.append({
                    "slug": sm.group(1),
                    "title": hm.group(2),
                    "drafted": "Draft complete" in meta_line,
                })
            i = j + 1
            continue
        i += 1
    return scenes


def all_scenes() -> list[dict]:
    """The ordered scene inventory with volume membership resolved.

    Each entry: {"slug", "title", "volume", "tag", "drafted"}.
    """
    scenes = _chronology_scenes()
    vols = volumes()
    by_last = {v["last"]: v for v in vols}
    idx = 0
    current = vols[0]
    for s in scenes:
        if idx >= len(vols):
            raise RuntimeError(
                f"scene {s['slug']!r} falls past the last volume boundary "
                f"({vols[-1]['last']!r}) — add it to a volume in {VOLUMES_TOML.name}"
            )
        current = vols[idx]
        s["volume"] = current["ordinal"]
        s["tag"] = current["tag"]
        if s["slug"] in by_last and by_last[s["slug"]] is current:
            idx += 1
    return scenes


def scenes_for_volume(vol: int | str, drafted_only: bool = False) -> list[dict]:
    ordinal = volume_record(vol)["ordinal"]
    result = [s for s in all_scenes() if s["volume"] == ordinal]
    if drafted_only:
        result = [s for s in result if s["drafted"]]
    return result


def volume_slugs(vol: int | str, drafted_only: bool = True) -> list[str]:
    return [s["slug"] for s in scenes_for_volume(vol, drafted_only=drafted_only)]


def volume_one_slugs(drafted_only: bool = True) -> list[str]:
    return volume_slugs(1, drafted_only=drafted_only)


def volume_last_slug(vol: int | str, drafted_only: bool = True) -> str:
    """The slug of a volume's final chapter — the durable name for its boundary.

    A volume seam is a story landmark and must be keyed by NAME, never by
    position. A chapter inserted anywhere earlier renumbers everything after it
    while leaving this slug untouched. On 2026-09-17 `strokes` (#37) and
    `not-enough` (#50) moved Volume One's end from ch050 to ch052 and silently
    invalidated four numeric call sites, two of which had been wrong for a
    while without anyone noticing. Positions are derived at the point of use
    (see `volume_bounds`); only the slug is stored.

    With `drafted_only` this is the last *drafted* chapter, which is not the
    volume's declared `last` while a volume is still being written.
    """
    slugs = volume_slugs(vol, drafted_only=drafted_only)
    if not slugs:
        raise KeyError(
            f"no {'drafted ' if drafted_only else ''}scenes for volume {vol} "
            f"— check the boundaries in {VOLUMES_TOML.name}"
        )
    return slugs[-1]


def volume_bounds(vol: int | str, drafted_only: bool = True) -> tuple[int, int]:
    """(first, last) drafted reading-order numbers for a volume, resolved now.

    Always call this instead of writing a literal: the numbers are correct only
    for the current chronology and must never be persisted."""
    slugs = volume_slugs(vol, drafted_only=drafted_only)
    if not slugs:
        raise KeyError(f"no scenes for volume {vol}")
    return chapter_number(slugs[0]), chapter_number(slugs[-1])


_SLUG_VOLUME: dict[str, int] | None = None


def volume_of(slug: str) -> int:
    """Volume ordinal (1, 2, ...) for a scene slug."""
    global _SLUG_VOLUME
    if _SLUG_VOLUME is None:
        _SLUG_VOLUME = {s["slug"]: s["volume"] for s in all_scenes()}
    vol = _SLUG_VOLUME.get(slug)
    if vol is None:
        raise KeyError(f"slug {slug!r} not found in chronology; add its entry before writing a review")
    return vol


def tag_of(slug: str) -> str:
    """Volume tag for a scene slug — the value to persist."""
    return volume_tag(volume_of(slug))


def chapter_number(slug: str) -> int:
    """Drafted reading-order number N for a scene = 1 + the count of *drafted* scenes that
    precede it in chronology order. This is the number checkpoint_context.py --to expects.

    Deliberately NOT the chronology position (which counts planned-but-undrafted entries
    too) and NOT reader_slugs().index()+1 (which raises for an undrafted target). It works
    whether or not `slug` is itself drafted: for a drafted scene it equals its drafted
    index; for an undrafted target (a chapter about to be written) it is the position it
    will occupy, so the authoring window — the drafted chapters before it — is exact."""
    scenes = all_scenes()
    target = next((i for i, s in enumerate(scenes) if s["slug"] == slug), None)
    if target is None:
        raise KeyError(f"slug {slug!r} not found in chronology")
    return 1 + sum(1 for s in scenes[:target] if s["drafted"])


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


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate() -> list[str]:
    """Return a list of problems; empty means the data file and chronology agree."""
    problems: list[str] = []
    vols = volumes()

    ordinals = [v["ordinal"] for v in vols]
    if ordinals != list(range(1, len(vols) + 1)):
        problems.append(f"ordinals must be 1..N with no gaps or repeats; got {ordinals}")
    tags = [v["tag"] for v in vols]
    if len(set(tags)) != len(tags):
        problems.append(f"duplicate volume tags: {tags}")
    for v in vols:
        for field in ("tag", "ordinal", "title", "first", "last", "status"):
            if field not in v:
                problems.append(f"volume {v.get('tag', '?')} is missing `{field}`")

    chron = _chronology_scenes()
    order = {s["slug"]: i for i, s in enumerate(chron)}
    for v in vols:
        for field in ("first", "last"):
            if v.get(field) not in order:
                problems.append(
                    f"volume {v['tag']}: {field} = {v.get(field)!r} is not a scene "
                    "in the chronology"
                )

    # Contiguity and full coverage.
    if not problems:
        if order[vols[0]["first"]] != 0:
            problems.append(
                f"volume {vols[0]['tag']} starts at {vols[0]['first']!r} but the "
                f"chronology's first scene is {chron[0]['slug']!r}"
            )
        for prev, nxt in zip(vols, vols[1:]):
            gap = order[nxt["first"]] - order[prev["last"]]
            if gap != 1:
                between = [s["slug"] for s in chron[order[prev["last"]] + 1:order[nxt["first"]]]]
                problems.append(
                    f"volumes {prev['tag']} -> {nxt['tag']} are not contiguous: "
                    f"{prev['last']!r} then {nxt['first']!r}"
                    + (f", leaving {between} in no volume" if between else " (overlap)")
                )
        if order[vols[-1]["last"]] != len(chron) - 1:
            trailing = [s["slug"] for s in chron[order[vols[-1]["last"]] + 1:]]
            problems.append(
                f"volume {vols[-1]['tag']} ends at {vols[-1]['last']!r}, leaving "
                f"{len(trailing)} scene(s) in no volume: {trailing[:5]}"
            )

    # The chronology's human ◆ markers are not authoritative, but a disagreement
    # means someone edited one of the two and not the other.
    markers: list[tuple[int, str]] = []
    for line in CHRONOLOGY.read_text().splitlines():
        m = _VOLUME_MARKER_RE.match(line)
        if m:
            word = m.group(1)
            if word not in _VOLUME_WORDS:
                problems.append(f"chronology marker '◆ VOLUME {word}' is not a known volume word")
                continue
            markers.append((_VOLUME_WORDS[word], line.strip()))
    seen: dict[int, str] = {}
    for num, line in markers:
        if num in seen:
            problems.append(
                f"chronology has two '◆ VOLUME' markers for volume {num} — "
                f"the defect that made Volume Two 77 chapters:\n      {seen[num]}\n      {line}"
            )
        seen[num] = line
    if len(markers) != len(vols):
        problems.append(
            f"chronology has {len(markers)} '◆ VOLUME' marker(s) but "
            f"{VOLUMES_TOML.name} declares {len(vols)} volume(s)"
        )

    # The blind-reader cover board is prose inside volume-packets.toml. A packet
    # keyed to the wrong volume, or carrying a stale title, feeds a false book
    # number straight to a cold reader, so it is checked here rather than trusted.
    problems.extend(_packet_problems(vols))
    return problems


def _packet_problems(vols: list[dict]) -> list[str]:
    packets = REPO / "reviews" / "cold-read" / "volume-packets.toml"
    if not packets.exists():
        return [f"missing {packets}"]
    text = packets.read_text()
    out: list[str] = []
    for v in vols:
        sec = re.search(rf'\[volumes\."{v["ordinal"]}"\](.*?)(?=\n\[|\Z)', text, re.DOTALL)
        if not sec:
            out.append(
                f"volume {v['ordinal']} ({v['tag']}) has no [volumes.\"{v['ordinal']}\"] "
                "packet — the reader gets no cover board"
            )
            continue
        body = sec.group(1)
        om = re.search(r"""opening_slug\s*=\s*["']([^"']+)["']""", body)
        if not om:
            out.append(f"volume {v['ordinal']} packet has no opening_slug")
        elif om.group(1) != v["first"]:
            out.append(
                f"volume {v['ordinal']} ({v['tag']}) packet opens at "
                f"{om.group(1)!r} but the volume starts at {v['first']!r}"
            )
        tm = re.search(r"the volume title \*\*(.+?)\*\*", body)
        if not tm:
            out.append(f"volume {v['ordinal']} packet has no cover-board title line")
        elif tm.group(1).strip().upper() != v["title"].upper():
            out.append(
                f"volume {v['ordinal']} ({v['tag']}) packet cover board says "
                f"{tm.group(1)!r} but the title is {v['title']!r}"
            )
    extra = {int(m) for m in re.findall(r'\[volumes\."(\d+)"\]', text)} - {
        v["ordinal"] for v in vols
    }
    if extra:
        out.append(f"volume-packets.toml has packets for nonexistent volume(s) {sorted(extra)}")
    return out


def _cli():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", nargs="?", const="all", metavar="N", help="list volume N (default all)")
    parser.add_argument("--number", metavar="SLUG", help="print the drafted reading-order N for a scene slug (what checkpoint_context --to expects)")
    parser.add_argument("--volumes", action="store_true", help="print the volume table from the data file")
    parser.add_argument("--check", action="store_true", help="validate the data file against the chronology")
    parser.add_argument("--check-fall-scenes", action="store_true", help="validate chronology Volume One drafted slugs against FALL_SCENES")
    args = parser.parse_args()

    if args.number:
        print(chapter_number(args.number))
        return

    if args.volumes:
        for v in volumes():
            first, last = volume_bounds(v["ordinal"], drafted_only=True)
            n_all = len(scenes_for_volume(v["ordinal"]))
            n_draft = len(scenes_for_volume(v["ordinal"], drafted_only=True))
            print(f"{v['ordinal']}  {v['tag']:<9} {v['title']:<24} "
                  f"{n_all:3d} ch ({n_draft:2d} drafted)  "
                  f"{v['first']} .. {v['last']}  [drafted ch{first}-{last}]")
        split = spring_split()
        if split and not split.get("applied", False):
            print(f"\nreserved (split not applied): {split.get('reserved_tag')} "
                  f"= {split.get('reserved_title')!r}")
        return

    if args.check:
        problems = validate()
        if problems:
            print("MISMATCH")
            for p in problems:
                print(f"  - {p}")
            sys.exit(1)
        print(f"OK: {volume_count()} volumes, "
              f"{len(all_scenes())} scenes, contiguous and fully covered")
        sys.exit(0)

    if args.check_fall_scenes:
        batch_path = Path(__file__).resolve().parent / "cold_read_batch.py"
        provider_slugs = _parse_fall_scenes_slugs(batch_path)
        chron_slugs = volume_one_slugs(drafted_only=True)
        if provider_slugs == chron_slugs:
            print(f"OK: {len(chron_slugs)} Volume One slugs match")
            sys.exit(0)
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
        vols = volume_ordinals() if args.list == "all" else [int(args.list)]
        for vol in vols:
            for s in scenes_for_volume(vol):
                print(f"{s['volume']}\t{'drafted' if s['drafted'] else 'planned'}\t{s['slug']}\t{s['title']}")
        return

    for s in all_scenes():
        print(f"{s['volume']}\t{'drafted' if s['drafted'] else 'planned'}\t{s['slug']}\t{s['title']}")


if __name__ == "__main__":
    _cli()
