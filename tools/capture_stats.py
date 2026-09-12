#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Capture-panel read-out: within-reader normalization, runs, dip triage.

The read-out discipline this enforces (author ruling 2026-09-11, SPEC
"Reading a capture dip"):

  1. Raw CAPTURE is NOT comparable across lanes. Measured lane offset on
     identical prose is ~2.1 points (sol/queer-woman 9.01 vs
     opus/queer-woman 6.88), larger than any chapter effect. Compare a
     reader only against her own mean (z).
  2. A breather with ALMOST-STOPPED *none* is healthy by standing rule.
     CAPTURE measures pull, not quality.
  3. The actionable unit is the RUN, not the chapter. Readers name run
     length as their limit ("two quiet chapters is my limit"), never the
     individual quiet chapter. Flag stretches, not dips.
  4. Where gates carry NEXT, the split is the signal: low CAPTURE + high
     NEXT is a working breather; low + low is a stall.

Usage:
  tools/capture_stats.py                      # readers, chapters, runs
  tools/capture_stats.py --runs-min 3         # only stretches of 3+
  tools/capture_stats.py --chapters 52-55     # zoom one stretch, with WHY
  tools/capture_stats.py --persona queer-woman --model claude-opus-4-8
"""
from __future__ import annotations

import argparse
import re
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import checkpoint_bundle  # noqa: E402

PANEL_ROOT = REPO / "reviews" / "capture-panel"
FREE_SAMPLE = 4  # ch1-4: no goodwill banked, a dip here is always a finding

NONE_RE = re.compile(r'^\**\s*"?none"?\b', re.I)
DISQUALIFY_RE = re.compile(r"not that I'?d (quit|leave|stop)", re.I)


class Gate:
    __slots__ = ("model", "persona", "n", "capture", "next_", "almost", "why", "stop")

    def __init__(self, model, persona, n, text):
        self.model, self.persona, self.n = model, persona, n
        self.capture = _int(text, r"CAPTURE:\s*\**\s*(\d+)")
        self.next_ = _int(text, r"NEXT:\s*\**\s*(\d+)")
        m = re.search(r"ALMOST[- ]STOPPED:\s*(.*)", text)
        self.almost = m.group(1).strip() if m else ""
        m = re.search(r"WHY:\s*(.*?)(?:\n[A-Z][A-Z -]{2,}:|\Z)", text, re.S)
        self.why = " ".join(m.group(1).split()) if m else ""
        self.stop = bool(re.search(r"DECISION:\s*\**\s*STOP", text, re.I))

    @property
    def reader(self) -> str:
        return f"{self.model}·{self.persona}"

    @property
    def real_exit(self) -> bool:
        """A quoted exit moment that doesn't disqualify itself."""
        if not self.almost or NONE_RE.match(self.almost):
            return False
        return not DISQUALIFY_RE.search(self.almost)


def _int(text: str, pat: str) -> int | None:
    m = re.search(pat, text)
    return int(m.group(1)) if m else None


def load(model=None, persona=None) -> list[Gate]:
    out = []
    for gp in sorted(PANEL_ROOT.glob("*/dag/*/gate-ch*.md")):
        mo, pe = gp.parts[-4], gp.parts[-2]
        if (model and mo != model) or (persona and pe != persona):
            continue
        n = int(re.search(r"gate-ch(\d+)", gp.name).group(1))
        g = Gate(mo, pe, n, gp.read_text(encoding="utf-8"))
        if g.capture is not None:
            out.append(g)
    return out


def titles() -> dict[int, str]:
    slugs = checkpoint_bundle.reader_slugs()
    return {i + 1: checkpoint_bundle.display_title(s) for i, s in enumerate(slugs)}


def zscores(gates: list[Gate]) -> dict[tuple[str, int], float]:
    """z of each gate against its OWN reader's distribution."""
    by = defaultdict(list)
    for g in gates:
        by[g.reader].append(g.capture)
    stats = {r: (st.mean(v), st.pstdev(v) or 1.0) for r, v in by.items()}
    return {(g.reader, g.n): (g.capture - stats[g.reader][0]) / stats[g.reader][1]
            for g in gates}


def report_readers(gates: list[Gate]) -> None:
    by = defaultdict(list)
    for g in gates:
        by[g.reader].append(g)
    print("READERS — raw scores are lane-relative; use z below, never these means\n")
    print(f"  {'reader':44s} {'n':>3s} {'mean':>5s} {'sd':>5s} {'min':>4s} "
          f"{'exits':>6s} {'NEXT':>5s}")
    for r in sorted(by):
        gs = by[r]
        cap = [g.capture for g in gs]
        nxt = [g.next_ for g in gs if g.next_ is not None]
        exits = sum(1 for g in gs if g.real_exit)
        nx = f"{st.mean(nxt):.2f}" if nxt else "—"
        stopped = "  STOPPED" if any(g.stop for g in gs) else ""
        print(f"  {r:44s} {len(cap):3d} {st.mean(cap):5.2f} {st.pstdev(cap):5.2f} "
              f"{min(cap):4d} {exits:6d} {nx:>5s}{stopped}")


def chapter_series(gates: list[Gate], z: dict) -> dict[int, dict]:
    by = defaultdict(list)
    for g in gates:
        by[g.n].append(g)
    out = {}
    for n, gs in by.items():
        nxt = [g.next_ for g in gs if g.next_ is not None]
        out[n] = {
            "n_readers": len(gs),
            "cap": st.mean(g.capture for g in gs),
            "z": st.mean(z[(g.reader, g.n)] for g in gs),
            "next": st.mean(nxt) if nxt else None,
            "exits": [g for g in gs if g.real_exit],
        }
    return out


def report_chapters(series: dict, ti: dict) -> None:
    print("\nCHAPTERS — z is mean deviation from each reader's own average\n")
    print(f"  {'ch':>3s} {'title':30s} {'rdrs':>4s} {'cap':>5s} {'z':>6s} "
          f"{'NEXT':>5s} {'exits':>5s}")
    for n in sorted(series):
        s = series[n]
        nx = f"{s['next']:.1f}" if s["next"] is not None else "—"
        mark = "  <" if s["z"] <= -1.0 else ""
        print(f"  {n:3d} {ti.get(n, '?')[:30]:30s} {s['n_readers']:4d} "
              f"{s['cap']:5.2f} {s['z']:+6.2f} {nx:>5s} {len(s['exits']):5d}{mark}")


def find_runs(series: dict, min_len: int, deadband: float) -> list[list[int]]:
    """Consecutive chapters meaningfully below their readers' own baseline.

    The deadband matters: a bare `z < 0` test recruits chapters sitting AT
    baseline into a run and inflates its length. `missed-a-spot` (z -0.11,
    raw 7/8/9, every gate enthusiastic) was padding a 2-chapter softness
    into a reported 4-chapter stretch. A chapter within +/- deadband of its
    readers' own mean is baseline, and baseline breaks a run.
    """
    runs, cur = [], []
    for n in sorted(series):
        if series[n]["z"] < -deadband:
            cur.append(n)
        else:
            if len(cur) >= min_len:
                runs.append(cur)
            cur = []
    if len(cur) >= min_len:
        runs.append(cur)
    return runs


def report_solo_dips(series: dict, ti: dict, deadband: float, runs: list) -> None:
    """A single deep chapter is still worth seeing — it just isn't a run."""
    inrun = {n for r in runs for n in r}
    solo = [n for n in sorted(series)
            if n not in inrun and series[n]["z"] <= -1.0]
    if not solo:
        return
    print("SOLO DIPS — deep, but isolated; judge by rebound, not by length\n")
    for n in solo:
        after = n + 1
        reb = (f"rebound {series[after]['z'] - series[n]['z']:+.2f} at ch{after}"
               if after in series else "no rebound measurable")
        print(f"  ch{n:3d} {ti.get(n, '?')[:34]:34s} z {series[n]['z']:+.2f}"
              f"  cap {series[n]['cap']:.2f}  {reb}")
    print()


def report_runs(series: dict, ti: dict, min_len: int, deadband: float) -> None:
    runs = find_runs(series, min_len, deadband)
    print(f"\nRUNS — consecutive chapters more than {deadband:.2f}z below their "
          f"readers' own average (min {min_len})")
    print("  The actionable unit. Readers name run LENGTH as their limit, not "
          "the single quiet chapter.\n")
    report_solo_dips(series, ti, deadband, runs)
    if not runs:
        print("  no runs")
        return
    for run in runs:
        depth = min(series[n]["z"] for n in run)
        target = [g for n in run for g in series[n]["exits"]
                  if g.persona != "dark-romance-control"]
        exits = len(target)
        nxt = [series[n]["next"] for n in run if series[n]["next"] is not None]
        after = run[-1] + 1
        reb = (f"+{series[after]['z'] - series[run[-1]]['z']:.2f} at ch{after}"
               if after in series else "end of drafted corpus")
        flags = []
        if len(run) >= 3:
            flags.append(f"LENGTH {len(run)}")
        if depth <= -1.5:
            flags.append(f"DEPTH {depth:.2f}")
        if exits:
            flags.append(f"{exits} TARGET-READER EXIT(S)")
        if after not in series:
            flags.append("NO REBOUND MEASURABLE")
        if run[0] <= FREE_SAMPLE:
            flags.append("IN FREE SAMPLE")
        if nxt and st.mean(nxt) < 6:
            flags.append(f"NEXT SAGS {st.mean(nxt):.1f}")
        head = f"  ch{run[0]}–{run[-1]} ({len(run)} ch)"
        print(f"{head:24s} {'  ·  '.join(flags) if flags else 'shallow, cleared'}")
        for n in run:
            s = series[n]
            nx = f" next {s['next']:.1f}" if s["next"] is not None else ""
            print(f"      ch{n:3d} {ti.get(n, '?')[:34]:34s} z {s['z']:+.2f}"
                  f"  cap {s['cap']:.2f}{nx}")
        print(f"      rebound: {reb}")
        for n in run:
            for g in series[n]["exits"]:
                # dark-romance-control is the WRONG reader; her exits are
                # the filter working, not a finding (SPEC, Personas §4).
                tag = " (control — repel is the goal)" \
                    if g.persona == "dark-romance-control" else ""
                print(f"      EXIT ch{n} {g.reader}{tag}: {g.almost[:110]}")
        print()


def report_zoom(gates: list[Gate], lo: int, hi: int, ti: dict) -> None:
    print(f"\nZOOM ch{lo}–{hi}\n")
    for n in range(lo, hi + 1):
        gs = sorted((g for g in gates if g.n == n), key=lambda g: g.capture)
        if not gs:
            continue
        print(f"  ── ch{n} {ti.get(n, '?')}")
        for g in gs:
            nx = f"/next {g.next_}" if g.next_ is not None else ""
            tag = "EXIT" if g.real_exit else "none" if not g.almost else "—"
            print(f"     cap {g.capture}{nx}  [{tag}]  {g.reader}")
            if g.why:
                print(f"        {g.why[:300]}")
        print()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model")
    ap.add_argument("--persona")
    ap.add_argument("--runs-min", type=int, default=2)
    ap.add_argument("--deadband", type=float, default=0.35,
                    help="a chapter within this z of baseline is AT baseline "
                         "and breaks a run (default 0.35)")
    ap.add_argument("--chapters", help="zoom a range, e.g. 52-55")
    args = ap.parse_args()

    gates = load(args.model, args.persona)
    if not gates:
        raise SystemExit("no gates matched")
    ti = titles()
    z = zscores(gates)
    series = chapter_series(gates, z)

    print(f"{len(gates)} gates · {len({g.reader for g in gates})} readers · "
          f"ch{min(series)}–{max(series)}\n")
    report_readers(gates)
    if args.chapters:
        lo, _, hi = args.chapters.partition("-")
        report_zoom(gates, int(lo), int(hi or lo), ti)
    else:
        report_chapters(series, ti)
    report_runs(series, ti, args.runs_min, args.deadband)


if __name__ == "__main__":
    main()
