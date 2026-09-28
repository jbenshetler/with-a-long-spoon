#!/usr/bin/env python3
"""Persona calibration read: a window of chapters, single-go, with neutral memory.

Deviation from the capture DAG, recorded in every header: the reader's memory of
chapters 1..B is the neutral quote-backed core ensemble checkpoint, not a
persona-owned mint, so the only variable across readers is the persona. For
calibrating persona drafts against each other; never a retention measurement.

Usage:
  tools/capture_calibrate.py --run drafts-v2 --from 12 --to 18 \
      --personas drafts/romance-graduate-v2 consent-sensitive ... \
      --models claude-opus-5 gpt-5.6-sol [--dry-run] [--force]
Persona names may be paths relative to reviews/capture-panel/personas/ (without .md).
Output: reviews/capture-panel/calibration/<run>/<model>/<persona>--window-chAAA-BBB.md
"""
from __future__ import annotations
import argparse, hashlib, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import checkpoint_bundle  # noqa: E402
import authorship_audit  # noqa: E402
import cold_read_config  # noqa: E402

PANEL = REPO / "reviews" / "capture-panel"
ENSEMBLE_CK = REPO / "reviews" / "cold-read" / "checkpoint-ensembles" / "core" / "checkpoints"
OPENROUTER_MODELS = cold_read_config.openrouter_models()


def sha12(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:12]


def persona_text(name: str) -> tuple[str, str, Path]:
    p = PANEL / "personas" / f"{name}.md"
    t = p.read_text(encoding="utf-8")
    return t, sha12(t.encode()), p


def system_prompt(persona: str) -> tuple[str, str, str]:
    core = (PANEL / "prompts" / "core-window.md").read_text(encoding="utf-8")
    pers, psha, _ = persona_text(persona)
    text = core.rstrip() + "\n\n" + pers.strip() + "\n"
    return text, sha12(text.encode()), psha


def user_prompt(lo: int, hi: int) -> tuple[str, dict]:
    slugs = checkpoint_bundle.reader_slugs()
    b = ((lo - 1) // 10) * 10  # decade boundary below the window
    ck = ENSEMBLE_CK / f"ck-ch{b:03d}.md"
    if not ck.exists():
        raise SystemExit(f"missing neutral checkpoint {ck}")
    ck_text = ck.read_text(encoding="utf-8")
    jacket = checkpoint_bundle.jacket_packet()
    parts = [f"===== THE JACKET =====\n\n{jacket}\n",
             f"===== YOUR MEMORY OF CHAPTERS 1–{b} =====\n\n{ck_text}\n"]
    if lo - 1 > b:
        parts.append(f"===== THE CHAPTERS YOU READ MOST RECENTLY (raw, still fresh) =====\n")
        for i in range(b + 1, lo):
            s = slugs[i - 1]
            parts.append(f"===== CHAPTER {i}: {checkpoint_bundle.display_title(s)} =====\n\n"
                         f"{checkpoint_bundle.clean_scene_text(s)}\n")
    parts.append("===== THE NEW CHAPTERS =====\n")
    shas = {}
    for i in range(lo, hi + 1):
        s = slugs[i - 1]
        body = checkpoint_bundle.clean_scene_text(s)
        shas[i] = (s, sha12(body.encode()))
        parts.append(f"===== CHAPTER {i}: {checkpoint_bundle.display_title(s)} =====\n\n{body}\n")
    parts.append("===== END =====\n\nBegin. Gate after each new chapter, then the note to a friend, "
                 "exactly per your instructions.")
    meta = {"boundary": b, "ck_sha": sha12(ck_text.encode()), "chapters": shas}
    return "\n".join(parts), meta


def validate(text: str, lo: int, hi: int, label: str) -> str:
    t = text.strip()
    if len(t) < 300:
        raise RuntimeError(f"short read {label} ({len(t)} chars)")
    up = t.upper()
    if f"GATE {lo}" not in up:
        raise RuntimeError(f"malformed read {label}: no GATE {lo}")
    if "STOP" not in up and f"GATE {hi}" not in up:
        raise RuntimeError(f"malformed read {label}: no GATE {hi} and no STOP")
    return t


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--from", dest="lo", type=int, required=True)
    ap.add_argument("--to", dest="hi", type=int, required=True)
    ap.add_argument("--personas", nargs="+", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    user, meta = user_prompt(args.lo, args.hi)
    prompts = {p: system_prompt(p) for p in args.personas}
    arm = f"window-ch{args.lo:03d}-{args.hi:03d}"
    out_root = PANEL / "calibration" / args.run

    def out_path(m, p):
        return out_root / m / f"{Path(p).name}--{arm}.md"

    tasks = [(m, p) for m in args.models for p in args.personas
             if args.force or not out_path(m, p).exists()]
    print(f"planned: {len(tasks)} reads · window ch{args.lo}-{args.hi} · memory ensemble:core "
          f"ck-ch{meta['boundary']:03d}@{meta['ck_sha']} · ~{len(user.split())} words of packet", flush=True)
    if args.dry_run:
        for t in tasks:
            print("  %s · %s" % t)
        return
    if any(m in OPENROUTER_MODELS for m in args.models):
        raise SystemExit("calibration runs on subscription lanes only; paid lanes need a separate authorization")

    failures = []

    def finish(m, p, raw):
        text, ssha, psha = prompts[p]
        body = validate(raw, args.lo, args.hi, f"{m}·{p}")
        out = out_path(m, p)
        out.parent.mkdir(parents=True, exist_ok=True)
        chs = " ".join(f"{i}:{s}@{h}" for i, (s, h) in meta["chapters"].items())
        header = (f"# Persona calibration — {Path(p).name} · {arm}\n\n"
                  f"*model: {m} · persona-file: {p}.md@{psha} · frame: core-window.md · prompt-sha: {ssha} · "
                  f"memory: ensemble:core ck-ch{meta['boundary']:03d}@{meta['ck_sha']} (NEUTRAL, not persona-owned — "
                  f"calibration deviation) · chapters: {chs} · run: {date.today().isoformat()}*\n\n---\n\n")
        out.write_text(header + body + "\n", encoding="utf-8")
        print(f"  done {m}·{p}", flush=True)

    def one_claude(m, p):
        label = f"{m}·{p}"
        try:
            raw = authorship_audit.run_claude(m, prompts[p][0], user, label)
            finish(m, p, raw)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{label}: {e}"); print(f"  FAIL {label}: {e}", flush=True)

    def codex_lane(models):
        import cold_read
        for p in args.personas:
            fn, close = cold_read.make_codex_agent_fn(system_prompt=prompts[p][0], effort=args.effort)
            try:
                sub = [m for m in models if (m, p) in set(tasks)]
                def go(m):
                    label = f"{m}·{p}"; last = None
                    for _ in range(2):
                        try:
                            r = fn(prompt=user, model=m, label=f"calib-{Path(p).name}")
                            finish(m, p, r.get("output") or ""); return
                        except Exception as e:  # noqa: BLE001
                            last = e; time.sleep(15)
                    failures.append(f"{label}: {last}"); print(f"  FAIL {label}: {last}", flush=True)
                with ThreadPoolExecutor(max_workers=2) as pool:
                    list(pool.map(go, sub))
            finally:
                close()

    claude_tasks = [t for t in tasks if t[0].startswith(authorship_audit.CLAUDE_PREFIX)]
    codex_models = [m for m in args.models if not m.startswith(authorship_audit.CLAUDE_PREFIX)]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = []
        if codex_models:
            futs.append(pool.submit(codex_lane, codex_models))
        for m, p in claude_tasks:
            futs.append(pool.submit(one_claude, m, p))
        for f in futs:
            f.result()
    print(f"finished: {len(tasks) - len(failures)}/{len(tasks)} ok", flush=True)
    for f in failures:
        print("  " + f)


if __name__ == "__main__":
    main()
