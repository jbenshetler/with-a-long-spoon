"""Rebuild the local chronology.html after a reader run (author ruling 2026-11-21).

`cold_read_grounded.py` and `capture_dag.py` call `rebuild()` at the end of any run
that wrote a review or gate, unless the run passed `--no-html`. Runs are often
launched in parallel (one invocation per model), so the rebuild takes an exclusive
lock: each rebuild runs whole, one at a time, and the last run to finish rebuilds
with every file in place. chronology_html.py writes atomically (temp + rename).
A failed rebuild is a warning, never a failed run — the reads are already saved."""
from __future__ import annotations

import fcntl
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCK = REPO / ".git" / "chronology-html.lock"


def rebuild(reason: str = "") -> bool:
    lock_path = LOCK if LOCK.parent.is_dir() else Path("/tmp") / "wals-chronology-html.lock"
    print(f"[html] rebuilding chronology.html{' — ' + reason if reason else ''} "
          "(--no-html to skip)", file=sys.stderr, flush=True)
    try:
        with open(lock_path, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            r = subprocess.run([str(REPO / "tools" / "chronology_html.py")], cwd=REPO,
                               capture_output=True, text=True)
    except OSError as e:
        print(f"[html] WARNING: rebuild failed to start: {e}", file=sys.stderr)
        return False
    if r.returncode != 0:
        print(f"[html] WARNING: chronology_html.py exited {r.returncode}:\n"
              f"{(r.stderr or r.stdout).strip()[-800:]}", file=sys.stderr)
        return False
    print(f"[html] {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'done'}",
          file=sys.stderr)
    return True
