#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Capture re-read significance: did an edit move the panel, or is it noise?

A re-read gives one paired change per lane (new score - old score). A +-1
move on one lane is noise; the question is whether the PANEL moved more than
chance allows. Chance is measured, not assumed (author ruling 2026-11-01,
SPEC rule 3b):

  * THE NULL comes from git. Every committed version of every DAG gate is
    paired with the next version of the same gate when the chapter prose AND
    the prompt are unchanged (same prose-sha, same prompt-sha). Those pairs
    are test-retest: nothing changed but sampling and the reader's memory of
    other chapters. The null is conditioned on the OLD score, because the
    drift depends on it (regression to the mean plus the ceiling: a lane at
    10 drops on ~1 re-read in 4 by chance; a lane at 8 rises on ~1 in 3).
  * PER-MODEL NOISE differs (argon steady, glm noisy). Each model's null is
    its own history shrunk toward the pooled null in proportion to how much
    history it has (pseudo-count --pool-k).

Report, per metric (CAPTURE, NEXT):

  1. EXACT TEST (headline). The per-lane nulls are convolved into the exact
     distribution of the panel's summed change; the observed sum's one-sided
     P in its direction. Verdict in plain words: improved / held against
     expected slippage / dropped / noise.
  2. GRID POSTERIOR. One unknown, the edit's effect, as an exponential tilt
     of each lane's null (support unchanged, so the ceiling stays exact).
     P(improved) = P(tilt > 0 | data) under a N(0,1) prior on the tilt, and a
     90% credible interval for the effect in points per lane.
  3. BOOTSTRAP BAND. The null pairs are resampled (--boot draws) and the
     test re-run, giving a 5-95% band on P: how much the answer leans on a
     thin null (the 10-baseline cell is the thinnest).
  4. MODEL-CLUSTERED CHECK. Two personas on one model are not independent.
     Each model's personas are summed into one unit; the count of models
     net-up minus net-down is tested exactly against the null.

Lanes reading the chapter for the first time are listed and excluded.
Reactions (ALMOST-STOPPED) are listed, not scored. The author's lane
weighting (rule 3a) is a separate question and is NOT mixed in.

Usage:
  tools/capture_delta.py --chapter 56                 # uncommitted gates vs HEAD;
                                                      # if none, the last commit that
                                                      # touched this chapter's gates
                                                      # vs its parent
  tools/capture_delta.py --chapter 56 --old-rev c57420ad^ --new-rev c57420ad
  tools/capture_delta.py --chapter 36 --personas romance-graduate
"""
from __future__ import annotations

import argparse
import collections
import math
import random
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PANEL = "reviews/capture-panel"
CONFIG = ROOT / "reviews/cold-read/ensemble-config.toml"
METRICS = ("CAPTURE", "NEXT")
GATE_RE = re.compile(r"/dag/[^/]+/gate-ch\d+\.md$")
MAX_ABS_D = 3          # test-retest changes beyond this are parse/format accidents
ALPHA = 0.05


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, input=data,
                          capture_output=True, check=True).stdout


def parse_gate(text: str | None) -> dict | None:
    if not text:
        return None
    out = {}
    for k, pat in (("prose", r"prose-sha (\w+)"), ("prompt", r"prompt-sha (\w+)")):
        m = re.search(pat, text)
        out[k] = m.group(1) if m else None
    for k in METRICS:
        m = re.search(rf"^{k}: (\d+)", text, re.M)
        out[k] = int(m.group(1)) if m else None
    m = re.search(r"^ALMOST-STOPPED: (.*)$", text, re.M)
    out["almost"] = m.group(1).strip() if m else ""
    return out


def batch_show(reqs: list[str]) -> list[str | None]:
    if not reqs:
        return []
    data = git("cat-file", "--batch", data=("\n".join(reqs) + "\n").encode())
    out, pos = [], 0
    for _ in reqs:
        e = data.index(b"\n", pos)
        hdr = data[pos:e].decode()
        if hdr.endswith("missing"):
            out.append(None)
            pos = e + 1
            continue
        size = int(hdr.split()[2])
        out.append(data[e + 1:e + 1 + size].decode("utf-8", "replace"))
        pos = e + 1 + size + 1
    return out


def gate_history() -> dict[str, list[str]]:
    """path -> commit hashes touching it, newest first."""
    log = git("log", "--format=>%H", "--name-only", "--", PANEL).decode()
    revs, cur = collections.defaultdict(list), None
    for line in log.splitlines():
        if line.startswith(">"):
            cur = line[1:]
        elif GATE_RE.search(line):
            revs[line].append(cur)
    return revs


# ---------------------------------------------------------------- the null

def mine_null(revs: dict[str, list[str]]) -> list[tuple[str, str, int, int]]:
    """(metric, model, old score, change) for every same-prose, same-prompt pair."""
    multi = {f: r for f, r in revs.items() if len(r) > 1}
    reqs = [f"{h}:{f}" for f, r in multi.items() for h in r]
    texts = dict(zip(reqs, batch_show(reqs)))
    pairs = []
    for f, r in multi.items():
        model = f.split("/")[2]
        vs = [parse_gate(texts.get(f"{h}:{f}")) for h in r]   # newest first
        for older, newer in zip(vs[1:], vs[:-1]):
            if not (older and newer and older["prose"] and older["prose"] == newer["prose"]
                    and older["prompt"] == newer["prompt"]):
                continue
            for k in METRICS:
                a, b = older[k], newer[k]
                if a is not None and b is not None and abs(b - a) <= MAX_ABS_D:
                    pairs.append((k, model, a, b - a))
    return pairs


def bucket(score: int) -> int:
    return min(max(score, 7), 10)          # 7 = "7 or below"


class Null:
    """Baseline-conditioned null, per model, shrunk toward the pool."""

    def __init__(self, pairs, metric: str, pool_k: float):
        self.k = pool_k
        self.pool = collections.defaultdict(collections.Counter)
        self.model = collections.defaultdict(collections.Counter)
        self.glob = collections.Counter()
        for k, m, a, d in pairs:
            if k != metric:
                continue
            self.pool[bucket(a)][d] += 1
            self.model[(m, bucket(a))][d] += 1
            self.glob[d] += 1
        self.n = sum(self.glob.values())

    def dist(self, model: str, old: int) -> dict[int, float]:
        b = bucket(old)
        pool = self.pool[b] if sum(self.pool[b].values()) >= 10 else self.glob
        pn = sum(pool.values())
        own = self.model[(model, b)]
        on = sum(own.values())
        support = set(pool) | set(own)
        p = {d: (own[d] + self.k * pool[d] / pn) / (on + self.k) for d in support}
        # the scale is 1..10: no mass past either end
        p = {d: q for d, q in p.items() if 1 <= old + d <= 10 and q > 0}
        z = sum(p.values())
        return {d: q / z for d, q in p.items()}


def convolve(dists: list[dict[int, float]]) -> dict[int, float]:
    tot = {0: 1.0}
    for dd in dists:
        nxt = collections.defaultdict(float)
        for s, p in tot.items():
            for d, q in dd.items():
                nxt[s + d] += p * q
        tot = nxt
    return tot


def tails(dist: dict[int, float], obs: int) -> tuple[float, float, float]:
    mean = sum(s * p for s, p in dist.items())
    hi = sum(p for s, p in dist.items() if s >= obs)
    lo = sum(p for s, p in dist.items() if s <= obs)
    return mean, hi, lo


def verdict(obs: int, mean: float, hi: float, lo: float) -> str:
    if obs > mean and hi < ALPHA:
        return "improved" if obs > 0 else "held against expected slippage"
    if obs < mean and lo < ALPHA:
        return "dropped"
    return "noise"


# ---------------------------------------------------------- grid posterior

def tilt(dd: dict[int, float], t: float) -> dict[int, float]:
    w = {d: q * math.exp(t * d) for d, q in dd.items()}
    z = sum(w.values())
    return {d: q / z for d, q in w.items()}


def posterior(lanes: list[tuple[dict[int, float], int]]) -> tuple[float, float, float, float]:
    """P(improved), posterior-mean effect, 90% interval (points per lane)."""
    grid = [i / 100 for i in range(-400, 401)]
    logpost, effect = [], []
    base_mean = sum(sum(d * q for d, q in dd.items()) for dd, _ in lanes) / len(lanes)
    for t in grid:
        lp = -t * t / 2
        eff = 0.0
        for dd, d in lanes:
            td = tilt(dd, t)
            lp += math.log(max(td.get(d, 0.0), 1e-300))
            eff += sum(x * q for x, q in td.items())
        logpost.append(lp)
        effect.append(eff / len(lanes) - base_mean)
    mx = max(logpost)
    w = [math.exp(v - mx) for v in logpost]
    z = sum(w)
    w = [v / z for v in w]
    p_up = sum(q for t, q in zip(grid, w) if t > 0)
    post_mean = sum(e * q for e, q in zip(effect, w))
    order = sorted(zip(effect, w))
    acc, lo_e, hi_e = 0.0, order[0][0], order[-1][0]
    for e, q in order:
        acc += q
        if acc >= 0.05 and lo_e == order[0][0]:
            lo_e = e
        if acc >= 0.95:
            hi_e = e
            break
    return p_up, post_mean, lo_e, hi_e


# ------------------------------------------------------------- clustering

def clustered(rows, metric, null) -> tuple[int, float, float]:
    """Models as units: (#net-up - #net-down) vs its exact null."""
    by_model = collections.defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    unit_dists, obs = [], 0
    for m, rs in by_model.items():
        s = convolve([null.dist(m, r["old"][metric]) for r in rs])
        up = sum(p for v, p in s.items() if v > 0)
        dn = sum(p for v, p in s.items() if v < 0)
        unit_dists.append({1: up, -1: dn, 0: 1 - up - dn})
        net = sum(r["new"][metric] - r["old"][metric] for r in rs)
        obs += (net > 0) - (net < 0)
    mean, hi, lo = tails(convolve(unit_dists), obs)
    return obs, hi, lo


# -------------------------------------------------------------- the lanes

def load_models() -> list[str]:
    with open(CONFIG, "rb") as fh:
        return list(tomllib.load(fh)["capture"]["models"])


def gather(chapter: int, models, personas, old_rev, new_rev, revs):
    rows, first, same = [], [], []
    for m in models:
        for p in personas:
            path = f"{PANEL}/{m}/dag/{p}/gate-ch{chapter:03d}.md"
            if new_rev:
                new_t = batch_show([f"{new_rev}:{path}"])[0]
            else:
                fp = ROOT / path
                new_t = fp.read_text() if fp.exists() else None
            new = parse_gate(new_t)
            if not new:
                continue
            old_t = batch_show([f"{old_rev or 'HEAD'}:{path}"])[0]
            if old_t == new_t:
                same.append(f"{m}/{p}")
                continue
            old = parse_gate(old_t)
            if not old:
                first.append(f"{m}/{p}")
                continue
            rows.append({"model": m, "persona": p, "old": old, "new": new})
    return rows, first, same


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chapter", type=int, required=True, help="reader-sequence number")
    ap.add_argument("--models", nargs="*", help="default: [capture].models")
    ap.add_argument("--personas", nargs="*", default=["romance-graduate", "fsog-refugee"])
    ap.add_argument("--old-rev", help="git rev for the OLD gates")
    ap.add_argument("--new-rev", help="git rev for the NEW gates (default: worktree)")
    ap.add_argument("--pool-k", type=float, default=10.0,
                    help="pseudo-count shrinking each model's null toward the pool")
    ap.add_argument("--boot", type=int, default=500, help="bootstrap draws over the null")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    revs = gate_history()
    pairs = mine_null(revs)
    models = a.models or load_models()
    old_rev, new_rev = a.old_rev, a.new_rev
    if not old_rev and not new_rev:
        dirty = git("status", "--porcelain", "--", f"{PANEL}/*/dag/*/gate-ch{a.chapter:03d}.md").strip()
        if not dirty:   # nothing pending: the most recent committed re-read of this chapter
            last = git("log", "-1", "--format=%H", "--", f"{PANEL}/*/dag/*/gate-ch{a.chapter:03d}.md").decode().strip()
            old_rev, new_rev = f"{last}^", last
            print(f"(no uncommitted gates; comparing the last re-read commit {last[:8]} with its parent)")
    rows, first, same = gather(a.chapter, models, a.personas, old_rev, new_rev, revs)

    print(f"ch{a.chapter:03d} re-read · {len(rows)} paired lanes · "
          f"null: {sum(1 for p in pairs if p[0] == 'CAPTURE')} test-retest pairs from git")
    if first:
        print(f"first reads (excluded): {', '.join(first)}")
    if same:
        print(f"not re-read between the revs (excluded): {', '.join(same)}")
    if not rows:
        print("no paired lanes")
        return 1

    print("\n  lane                                  CAPTURE   NEXT")
    for r in rows:
        c = f"{r['old']['CAPTURE']}->{r['new']['CAPTURE']}"
        n = (f"{r['old']['NEXT']}->{r['new']['NEXT']}"
             if r["old"]["NEXT"] is not None and r["new"]["NEXT"] is not None else "-")
        print(f"  {r['model'] + '/' + r['persona']:<38}{c:<10}{n}")

    rng = random.Random(a.seed)
    for metric in METRICS:
        mrows = [r for r in rows if r["old"][metric] is not None and r["new"][metric] is not None]
        if not mrows:
            continue
        null = Null(pairs, metric, a.pool_k)
        lanes = [(null.dist(r["model"], r["old"][metric]), r["new"][metric] - r["old"][metric])
                 for r in mrows]
        obs = sum(d for _, d in lanes)
        mean, hi, lo = tails(convolve([dd for dd, _ in lanes]), obs)
        p_dir = hi if obs >= mean else lo
        up = sum(d > 0 for _, d in lanes)
        dn = sum(d < 0 for _, d in lanes)
        p_up, eff, e_lo, e_hi = posterior(lanes)
        # bootstrap the null pairs
        mpairs = [p for p in pairs if p[0] == metric]
        boot = []
        for _ in range(a.boot):
            bnull = Null([mpairs[rng.randrange(len(mpairs))] for _ in mpairs], metric, a.pool_k)
            bl = [bnull.dist(r["model"], r["old"][metric]) for r in mrows]
            _, bh, bl_ = tails(convolve(bl), obs)
            boot.append(bh if obs >= mean else bl_)
        boot.sort()
        b5, b95 = boot[int(0.05 * len(boot))], boot[int(0.95 * len(boot)) - 1]
        c_obs, c_hi, c_lo = clustered(mrows, metric, null)
        print(f"\n{metric}  ({len(mrows)} lanes: {up} up, {dn} down)")
        print(f"  exact test     observed sum {obs:+d}, null expects {mean:+.2f}; "
              f"P(this {'high' if obs >= mean else 'low'} or more) = {p_dir:.3f}  "
              f"→ {verdict(obs, mean, hi, lo)}")
        print(f"  posterior      P(improved) = {p_up:.2f}; effect {eff:+.2f} pts/lane "
              f"(90% {e_lo:+.2f} to {e_hi:+.2f})")
        print(f"  bootstrap      P across resampled nulls: {b5:.3f}–{b95:.3f} (5–95%)")
        print(f"  by model       net models up−down {c_obs:+d}; "
              f"P(≥) = {c_hi:.3f}, P(≤) = {c_lo:.3f}")

    print("\nALMOST-STOPPED (new gates; reactions are listed, not scored):")
    for r in rows:
        if r["new"]["almost"] and not r["new"]["almost"].lower().startswith("none"):
            print(f"  {r['model']}/{r['persona']}: {r['new']['almost'][:160]}")
    print("\nLane weighting (rule 3a) is a separate read; it is not in these numbers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
