#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Structural measurements per chapter and per volume — the countable half of a
structural edit. Deterministic and free.

Why it exists: a structural editor's verdicts on absence and pacing ("Randi
disappears for ten chapters", "the middle sags") cannot be backed by a quote.
They are checked here instead, against counts, and against the reader corpus
the panel already produced. The blind structural letters
(`tools/structural_edit.py`) never see this output; it is used afterwards, to
test their claims and to sit beside them when the author rules.

Per chapter:
  - words, dialogue share (words inside double quotes)
  - days since the previous chapter (chapter_dates.py, the sole date source)
  - present: (the chronology's field, principals only)
  - mentions of each recurring proper name (auto-detected from the prose, never
    a hand list, so a minor character the plan forgot still shows)
  - capture z (capture_stats.py: each reader against her own mean) and how many
    ALMOST-STOPPED entries were resolved vs standing (almost_stopped_audit.py).
    A resolved ALMOST-STOPPED in a high-capture chapter is usually the chapter's
    most charged moment, not a sag; only `standing` counts toward drag.
  - cold-read pace: how many current-panel readers' "Pace — chapter to chapter"
    lead with a drag word (stall, sag, plateau, repetitive...). A sag is a sag
    when two or more readers say so.

Per volume, per recurring name: chapters with a mention, first and last
chapter, and the longest run of chapters with no mention.

Usage:
  tools/structure_metrics.py --volumes 1 2 3          # writes audits/structural/metrics.md + .json
  tools/structure_metrics.py --volumes 1 --stdout
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import capture_stats  # noqa: E402
import almost_stopped_audit  # noqa: E402
import chapter_dates  # noqa: E402
import checkpoint_bundle  # noqa: E402
import chronology_html  # noqa: E402
import cold_read_config  # noqa: E402
import volume_scenes  # noqa: E402

OUT_DIR = REPO / "audits" / "structural"
SCENES = REPO / "scenes"

CAP_WORD = re.compile(r"\b[A-Z][a-z]{2,}\b")
NOT_NAMES = set("""January February March April May June July August September October
November December Monday Tuesday Wednesday Thursday Friday Saturday Sunday God
Christmas Thanksgiving English French European American Italian Spanish Chinese
Mexican Japanese Latin Greek Irish Mondays Tuesdays Wednesdays Thursdays Fridays
Saturdays Sundays""".split())
DRAG = re.compile(r"\b(stall|stalls|stalled|stalling|sag|sags|sagging|drag|drags|dragging|"
                  r"plateau|plateaus|repetitive|repeats|repeating|treading water|static|"
                  r"slack|loses momentum|losing momentum|marking time|circling|flat)\b", re.I)
PACE_C2C = re.compile(r"\*\*Pace — chapter to chapter:\*\*\s*(.+)")
DIALOGUE = re.compile(r"[\"“]([^\"”]{1,2000})[\"”]")


def prose(slug: str) -> str:
    p = SCENES / f"{slug}.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def body(text: str) -> str:
    # drop the H1 title and italic header lines the reader never sees as prose
    return "\n".join(l for l in text.splitlines()
                     if not l.startswith("#") and not re.fullmatch(r"\s*\*[^*].*\*\s*", l))


def detect_names(texts: list[str], min_mid: int = 4) -> list[str]:
    mid, lower = Counter(), Counter()
    for t in texts:
        for m in CAP_WORD.finditer(t):
            before = t[max(0, m.start() - 3):m.start()]
            if not re.search(r"[.!?\"“”\n—]\s*[*_]?$|^\s*[*_]?$", before):
                mid[m.group(0)] += 1
        for w in re.findall(r"\b[a-z]{3,}\b", t):
            lower[w] += 1
    out = [w for w, c in mid.items()
           if c >= min_mid and w not in NOT_NAMES and lower[w.lower()] < 0.15 * c]
    return sorted(out, key=lambda w: -mid[w])


def principals_present() -> dict[str, set[str] | None]:
    md = (REPO / "meta" / "meta-plan-chronology.md").read_text(encoding="utf-8")
    entries, _ = chronology_html.parse(md)
    out = {}
    for e in entries:
        slug, pres = None, None
        for kind, val in e.segments:
            if kind == "slug":
                slug = val["label"]
            elif kind == "present" and val["known"]:
                pres = val["names"]
        if slug:
            out[slug] = pres
    return out


def cold_drag(slug: str) -> tuple[int, int, list[str]]:
    hits, n, who = 0, 0, []
    for m in cold_read_config.panel_models():
        f = REPO / "reviews" / "cold-read" / m / f"{slug}.md"
        if not f.exists():
            continue
        mm = PACE_C2C.search(f.read_text(encoding="utf-8"))
        if not mm:
            continue
        n += 1
        lead = re.split(r"(?<=[.;:])\s", mm.group(1), maxsplit=1)[0]
        if DRAG.search(lead):
            hits += 1
            who.append(m)
    return hits, n, who


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--volumes", nargs="+", type=int, default=[1, 2])
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    all_slugs = checkpoint_bundle.reader_slugs()
    vol_of, chapters = {}, []
    for v in args.volumes:
        for s in volume_scenes.volume_slugs(v, drafted_only=True):
            if s in all_slugs:
                vol_of[s] = v
                chapters.append(s)
    chapters.sort(key=all_slugs.index)
    texts = {s: body(prose(s)) for s in chapters}
    names = detect_names(list(texts.values()))
    present = principals_present()

    gates = capture_stats.load()
    series = capture_stats.chapter_series(gates, capture_stats.zscores(gates))
    stops = defaultdict(Counter)
    active = set(cold_read_config.capture_models())
    for r in almost_stopped_audit.collect(None, None):
        if r["model"] in active:
            stops[r["ch"]][r["bucket"]] += 1

    rows, prev_end = [], None
    for s in chapters:
        n = all_slugs.index(s) + 1
        t = texts[s]
        words = len(re.findall(r"\b[\w'’-]+\b", t))
        dwords = sum(len(re.findall(r"\b[\w'’-]+\b", d)) for d in DIALOGUE.findall(t))
        try:
            start, end = chapter_dates._span(s)
            gap = (start - prev_end).days if prev_end else None
            prev_end = end
            date = start.isoformat()
        except Exception:
            gap, date = None, None
        ment = {nm: len(re.findall(rf"\b{nm}\b", t)) for nm in names}
        cs = series.get(n, {})
        dh, dn, dwho = cold_drag(s)
        rows.append({
            "n": n, "slug": s, "vol": vol_of[s], "title": checkpoint_bundle.display_title(s),
            "date": date, "gap_days": gap, "words": words,
            "dialogue": round(dwords / words, 2) if words else 0,
            "present": sorted(present.get(s) or []),
            "mentions": {k: v for k, v in ment.items() if v},
            "capture_z": round(cs["z"], 2) if cs.get("z") is not None else None,
            "capture_readers": cs.get("n_readers", 0),
            "almost_resolved": stops[n]["resolved"], "almost_standing": stops[n]["standing"],
            "cold_drag": dh, "cold_readers": dn, "cold_drag_models": dwho,
        })

    per_vol = {}
    for v in args.volumes:
        vr = [r for r in rows if r["vol"] == v]
        stats = {}
        for nm in names:
            hit = [i for i, r in enumerate(vr) if r["mentions"].get(nm)]
            if not hit:
                continue
            gaps, run, best_at = 0, 0, None
            for i, r in enumerate(vr):
                run = 0 if r["mentions"].get(nm) else run + 1
                if run > gaps:
                    gaps, best_at = run, i
            stats[nm] = {
                "chapters": len(hit), "of": len(vr),
                "total": sum(r["mentions"].get(nm, 0) for r in vr),
                "first": vr[hit[0]]["n"], "last": vr[hit[-1]]["n"],
                "longest_gap": gaps,
                "gap_ends": vr[best_at]["n"] if best_at is not None else None,
            }
        per_vol[v] = stats

    md = render(rows, per_vol, names, args.volumes)
    if args.stdout:
        print(md)
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = "-".join(map(str, args.volumes))
    (OUT_DIR / f"metrics-vol{tag}.json").write_text(
        json.dumps({"names": names, "chapters": rows, "volumes": per_vol}, indent=1), encoding="utf-8")
    (OUT_DIR / f"metrics-vol{tag}.md").write_text(md, encoding="utf-8")
    print(f"wrote {OUT_DIR.relative_to(REPO)}/metrics-vol{tag}.md (.json)")


def render(rows, per_vol, names, vols) -> str:
    L = ["# Structural measurements — Volumes " + ", ".join(map(str, vols)), "",
         "*Generated by `tools/structure_metrics.py`. Counts, not verdicts. Capture z is "
         "each capture reader against her own mean (current roster); `ALMOST res/stand` "
         "splits resolved hovers from standing ones (a resolved hover in a strong chapter "
         "is usually its charge, not a sag); `drag` is how many current cold-panel readers "
         "lead their chapter-to-chapter pace note with a drag word. Gates and reads may "
         "predate later edits.*", ""]
    for v in vols:
        vr = [r for r in rows if r["vol"] == v]
        L += [f"## Volume {v} — {len(vr)} chapters, {sum(r['words'] for r in vr):,} words", "",
              "| ch | chapter | date | +days | words | dlg | present | cap z (n) | ALMOST res/stand | drag |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in vr:
            cz = f"{r['capture_z']:+.2f} ({r['capture_readers']})" if r["capture_z"] is not None else "—"
            drag = f"{r['cold_drag']}/{r['cold_readers']}" if r["cold_readers"] else "—"
            if r["cold_drag"] >= 2:
                drag = f"**{drag}**"
            L.append(f"| {r['n']} | {r['title']} | {r['date'] or '—'} | "
                     f"{'' if r['gap_days'] is None else r['gap_days']} | {r['words']:,} | "
                     f"{r['dialogue']:.2f} | {', '.join(r['present']) or '?'} | {cz} | "
                     f"{r['almost_resolved']}/{r['almost_standing']} | {drag} |")
        L += ["", f"### Recurring names, Volume {v}", "",
              "| name | chapters | mentions | first | last | longest gap (ends before ch) |",
              "|---|---|---|---|---|---|"]
        for nm, s in sorted(per_vol[v].items(), key=lambda kv: -kv[1]["total"]):
            L.append(f"| {nm} | {s['chapters']}/{s['of']} | {s['total']} | {s['first']} | "
                     f"{s['last']} | {s['longest_gap']}"
                     f"{'' if not s['longest_gap'] else ' (to ch ' + str(s['gap_ends']) + ')'} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
