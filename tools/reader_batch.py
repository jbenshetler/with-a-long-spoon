#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Run a batch of blind readers, one invocation per model in parallel, and rebuild
chronology.html ONCE at the end (author ruling 2026-11-21).

Each child runs with --no-html; when every child has finished, successful or
not, the page is rebuilt a single time. A failed child never skips the rebuild,
and the batch exits 1 if any child failed.

    tools/reader_batch.py capture [capture_dag lane args] [capture_dag run args]
    tools/reader_batch.py cold    [--models ...] [cold_read_grounded run args]

Capture: lanes resolve exactly as in capture_dag.py (--models/--personas narrow
the default lanes; --lane MODEL:PERSONA names any other; --with-defaults), then
are grouped by model, one child per model. Everything else (--to, --from,
--fresh, --effort, --paid-ok, --allow-retired, ...) passes through.
    tools/reader_batch.py capture --paid-ok                 # Volume 1, default lanes
    tools/reader_batch.py capture --to 16 --fresh --paid-ok

Cold: --models defaults to [panel].models; an OpenRouter reader is launched as
--model <provider/model> --model-id <id>. Everything else (--scope, --from/--to,
--fresh, --jobs, --on-demand, --allow-retired, --paid-ok, ...) passes through.
    tools/reader_batch.py cold --scope vol1 --paid-ok

Child logs go to /tmp/reader-batch/<stamp>/<model>.log; the tail of a failed
child's log is printed at the end.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import cold_read_config  # noqa: E402
import chronology_rebuild  # noqa: E402


def capture_jobs(argv: list[str]) -> list[tuple[str, list[str]]]:
    import capture_dag
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--models", nargs="+", default=None)
    ap.add_argument("--personas", nargs="+", default=None)
    ap.add_argument("--lane", nargs="+", default=None)
    ap.add_argument("--with-defaults", action="store_true")
    ap.add_argument("--allow-retired", action="store_true")
    ap.add_argument("--paid-ok", action="store_true")
    a, rest = ap.parse_known_args(argv)
    lanes = capture_dag.resolve_lanes(a.models, a.personas, a.lane, a.with_defaults,
                                      a.allow_retired)
    paid = [f"{m}:{p}" for m, p in lanes if cold_read_config.is_openrouter(m)]
    if paid and not a.paid_ok and not ({"--check", "--check-stale"} & set(rest)):
        raise SystemExit(f"refusing to start: {', '.join(paid)} bill OpenRouter per token. "
                         "Pass --paid-ok only when the author has authorized paid reads "
                         "for this run.")
    by_model: dict[str, list[str]] = {}
    for m, p in lanes:
        by_model.setdefault(m, []).append(f"{m}:{p}")
    extra = (["--allow-retired"] if a.allow_retired else []) + (["--paid-ok"] if a.paid_ok else [])
    tool = str(REPO / "tools" / "capture_dag.py")
    return [(m, [tool, "--lane", *ls, *extra, *rest, "--no-html"])
            for m, ls in by_model.items()]


def cold_jobs(argv: list[str]) -> list[tuple[str, list[str]]]:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--models", nargs="+", default=None)
    ap.add_argument("--paid-ok", action="store_true")
    a, rest = ap.parse_known_args(argv)
    if any(x in ("--model", "--model-id") for x in rest):
        raise SystemExit("use --models <id> ... (model ids from ensemble-config.toml); the "
                         "batch derives --model/--model-id itself")
    models = a.models or list(cold_read_config.panel_models())
    paid = [m for m in models if cold_read_config.is_openrouter(m)]
    if paid and not a.paid_ok and not ({"--check", "--check-stale"} & set(rest)):
        raise SystemExit(f"refusing to start: {', '.join(paid)} bill OpenRouter per token. "
                         "Pass --paid-ok only when the author has authorized paid reads "
                         "for this run.")
    orm = cold_read_config.openrouter_models()
    tool = str(REPO / "tools" / "cold_read_grounded.py")
    jobs = []
    for m in models:
        sel = ["--model", orm[m], "--model-id", m] if m in orm else ["--model", m]
        jobs.append((m, [tool, *sel, *(["--paid-ok"] if a.paid_ok else []), *rest,
                         "--no-html"]))
    return jobs


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("capture", "cold"):
        print(__doc__)
        raise SystemExit(2)
    kind, argv = sys.argv[1], sys.argv[2:]
    no_html = "--no-html" in argv
    argv = [x for x in argv if x != "--no-html"]
    jobs = capture_jobs(argv) if kind == "capture" else cold_jobs(argv)
    if not jobs:
        raise SystemExit("no readers to run")

    logdir = Path("/tmp/reader-batch") / time.strftime("%Y%m%d-%H%M%S")
    logdir.mkdir(parents=True, exist_ok=True)
    print(f"[batch] {kind}: {len(jobs)} model(s) in parallel · logs {logdir}", flush=True)
    for m, cmd in jobs:
        print(f"  {m}: {' '.join(cmd[1:])}", flush=True)

    def run(job):
        m, cmd = job
        log = logdir / f"{m}.log"
        t0 = time.time()
        with log.open("w") as fh:
            rc = subprocess.run(cmd, cwd=REPO, stdout=fh, stderr=subprocess.STDOUT).returncode
        print(f"[batch] {m}: {'ok' if rc == 0 else f'FAILED (exit {rc})'} "
              f"in {time.time() - t0:.0f}s", flush=True)
        return m, rc, log

    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        results = list(pool.map(run, jobs))

    failed = [(m, rc, log) for m, rc, log in results if rc != 0]
    if not no_html:
        chronology_rebuild.rebuild(f"{kind} batch, {len(results) - len(failed)}/{len(results)} ok")
    for m, rc, log in failed:
        tail = log.read_text(encoding="utf-8", errors="replace").splitlines()[-15:]
        print(f"\n--- {m} (exit {rc}) — last lines of {log} ---\n" + "\n".join(tail))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
