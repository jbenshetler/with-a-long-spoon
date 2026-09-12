#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Capture DAG — cold-reader-model persona reads of Volume 1.

One run per chapter: chapter N is read with the reader's OWN carry-forward
checkpoint ck-ch<B> (B = decade boundary below N) + raw prose of chapters
B+1..N-1 + chapter N (e.g. ch25 = own ck-ch020 + raw ch021-024 + ch025).
Every 10 chapters the reader MINTS its own carry-forward from: prior
checkpoint + the decade's raw prose + its own gate notes. Each reader
(persona x model) mints its own checkpoints — persona memory IS the
instrument. A STOP gate ends the reader permanently (later chapters skipped).

Sequential per reader (correct STOP semantics); readers run in parallel.
Restartable: existing gates/checkpoints are skipped.

Usage:
  tools/capture_dag.py --models claude-opus-4-8 gpt-5.6-sol            # the 3 default personas
  tools/capture_dag.py --models claude-opus-4-8 --personas fsog-refugee --to 12
  tools/capture_dag.py --models ... --to 70 --fresh   # re-read ch70 after revising it
  tools/capture_dag.py --models ... --assemble    # build <persona>--volume-dag.md records
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import authorship_audit  # noqa: E402  (run_claude, CLAUDE_PREFIX)

PANEL_ROOT = REPO / "reviews" / "capture-panel"
PROTOCOL = "capture-dag-v2-rich"
PERSONAS = ["romance-graduate", "fsog-refugee", "consent-sensitive"]
# RETIRED from running (author ruling 2026-09-12): `dark-romance-control` is the
# WRONG reader — a book that captures her is failing the repel goal, so her STOPs
# were the success condition. She has delivered it (opus STOPPED at ch021, sol at
# ch006), and the lanes that didn't stop sat permanently behind, making every
# "catch up to chapter N" scope cost more than the signal was worth. Do not run
# her again. She stays in ALL_PERSONAS only so `--assemble` can still build the
# historical record from the gates already on disk; her existing data is kept.
RETIRED_PERSONAS = ["dark-romance-control"]
# `queer-woman` is selectable but NOT in the default panel — opt in with
# --personas, so a bare run never silently opens a fresh 70-chapter read on a
# subscription lane.
ALL_PERSONAS = PERSONAS + ["queer-woman"] + RETIRED_PERSONAS
DECADE = 10


def volume_one_count() -> int:
    return len(checkpoint_bundle.volume_scenes.volume_one_slugs(drafted_only=True))


def slugs() -> list[str]:
    """The full drafted cross-volume sequence (Vol 1, then Vol 2, then Vol 3),
    so a reader can be run on past the Volume 1 boundary. `--to` bounds the run
    and defaults to `N_CH` = the drafted Volume 1 length, so a bare invocation
    still reads Volume 1 only."""
    return checkpoint_bundle.reader_slugs()


N_CH = volume_one_count()


def boundary(n: int) -> int:
    return ((n - 1) // DECADE) * DECADE


def sysprompt(persona: str, frame: str) -> tuple[str, str]:
    core = (PANEL_ROOT / "prompts" / frame).read_text(encoding="utf-8")
    pers = (PANEL_ROOT / "personas" / f"{persona}.md").read_text(encoding="utf-8")
    text = core.rstrip() + "\n\n" + pers.strip() + "\n"
    return text, hashlib.sha256(text.encode()).hexdigest()[:12]


def dag_dir(model_id: str, persona: str) -> Path:
    return PANEL_ROOT / model_id / "dag" / persona


def gate_path(d: Path, n: int) -> Path:
    return d / f"gate-ch{n:03d}.md"


def ck_path(d: Path, b: int) -> Path:
    return d / f"ck-ch{b:03d}.md"


def chapter_block(i: int) -> str:
    s = slugs()[i - 1]
    return (f"===== CHAPTER {i}: {checkpoint_bundle.display_title(s)} =====\n\n"
            f"{checkpoint_bundle.clean_scene_text(s)}\n")


def jacket_block() -> str:
    j = checkpoint_bundle.jacket_packet()
    if not j:
        raise SystemExit("empty jacket packet")
    return f"===== THE JACKET =====\n\n{j}\n"


def read_prompt(d: Path, n: int) -> str:
    b = boundary(n)
    parts = [jacket_block()]
    if b:
        ck = ck_path(d, b).read_text(encoding="utf-8")
        parts.append(f"===== YOUR CARRY-FORWARD NOTES (written after chapter {b}) "
                     f"=====\n\n{ck}\n")
    if n - 1 > b:
        parts.append("===== RECENT CHAPTERS (raw, still fresh) =====\n")
        for i in range(b + 1, n):
            parts.append(chapter_block(i))
    parts.append("===== THE NEW CHAPTER =====\n")
    parts.append(chapter_block(n))
    parts.append(f"Read chapter {n} and produce your REACTION, then your single "
                 "gate block.")
    return "\n".join(parts)


def mint_prompt(d: Path, n: int) -> str:
    b = boundary(n)  # previous boundary (n is a multiple of 10 -> b = n-10)
    parts = [jacket_block()]
    if b:
        parts.append(f"===== YOUR PREVIOUS CARRY-FORWARD NOTES (after chapter {b}) "
                     f"=====\n\n{ck_path(d, b).read_text(encoding='utf-8')}\n")
    parts.append("===== CHAPTERS YOU JUST READ =====\n")
    for i in range(b + 1, n + 1):
        parts.append(chapter_block(i))
    parts.append("===== YOUR OWN GATE NOTES FOR THEM =====\n")
    for i in range(b + 1, n + 1):
        parts.append(gate_path(d, i).read_text(encoding="utf-8"))
    parts.append(f"\nWrite your carry-forward notes through chapter {n} now.")
    return "\n".join(parts)


def clean_markdown(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n"


def write_doc(path: Path, header: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{header}\n\n{clean_markdown(body)}", encoding="utf-8")


def run_reader(model_id: str, persona: str, agent_fn, to_n: int,
               fresh: int | None = None) -> str:
    """Sequential chapters 1..to_n with decade mints. agent_fn(system, prompt, label).

    `fresh` names a single chapter whose existing gate (and decade mint, if it
    sits on a boundary) is overwritten instead of resumed past — the re-read of
    a revised chapter. Scoped to one chapter on purpose: the run's scope is the
    whole range 1..to_n, so a blanket refresh would re-read the entire book."""
    d = dag_dir(model_id, persona)
    stopped = d / "STOPPED"
    read_sys, read_sha = sysprompt(persona, "core-chapter.md")
    mint_sys, mint_sha = sysprompt(persona, "core-mint.md")
    for n in range(1, to_n + 1):
        if stopped.exists():
            return f"{model_id}·{persona}: stopped earlier"
        gp = gate_path(d, n)
        if not gp.exists() or n == fresh:
            label = f"{model_id}·{persona}·ch{n:02d}"
            raw = agent_fn(read_sys, read_prompt(d, n), label).strip()
            if "DECISION" not in raw.upper():
                raise RuntimeError(f"malformed gate for {label}")
            write_doc(gp, f"*{PROTOCOL} · gate ch{n:03d} · {model_id} · {persona} · "
                          f"prompt-sha {read_sha} · {date.today().isoformat()}*", raw)
            print(f"  gate {label}", flush=True)
        if re.search(r"DECISION:\s*STOP", gp.read_text(), re.I):
            stopped.write_text(f"stopped at ch{n:03d}\n")
            print(f"  STOP {model_id}·{persona} at ch{n}", flush=True)
            return f"{model_id}·{persona}: STOPPED at ch{n}"
        if n % DECADE == 0:
            cp = ck_path(d, n)
            if not cp.exists() or n == fresh:
                label = f"{model_id}·{persona}·mint-ch{n:02d}"
                raw = agent_fn(mint_sys, mint_prompt(d, n), label).strip()
                if len(raw) < 800:
                    raise RuntimeError(f"suspiciously short mint for {label}")
                write_doc(cp, f"*{PROTOCOL} · carry-forward ck-ch{n:03d} · {model_id} · "
                              f"{persona} · prompt-sha {mint_sha} · "
                              f"{date.today().isoformat()}*", raw)
                print(f"  mint {label}", flush=True)
    return f"{model_id}·{persona}: through ch{to_n}"


OPENROUTER_MODELS = {
    "kimi-k3": "moonshotai/kimi-k3",
    "glm-5.3": "z-ai/glm-5.3",
    "glm-5.3-flash": "z-ai/glm-5.3-flash",
    "gemini-3.8-flash": "google/gemini-3.8-flash",
    "qwen3.8-max-0902": "qwen/qwen3.8-max-0902",
    "deepseek-v4-pro-0813": "deepseek/deepseek-v4-pro-0813",
}
OR_MAX_OUTPUT = 16000   # checkpoint mints run ~3.6k visible; the rest is reasoning headroom
OR_TIMEOUT = 900.0


def make_agent(model_id: str, effort: str):
    """Return (agent_fn(system,prompt,label), close())."""
    if model_id.startswith(authorship_audit.CLAUDE_PREFIX):
        def fn(system, prompt, label):
            return authorship_audit.run_claude(model_id, system, prompt, label)
        return fn, (lambda: None)
    import cold_read
    if model_id in OPENROUTER_MODELS:
        import os
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("OPENROUTER_API_KEY not set in the environment.")
        selector = OPENROUTER_MODELS[model_id]
        holders = {}

        def fn(system, prompt, label):
            k = hashlib.sha256(system.encode()).hexdigest()[:8]
            if k not in holders:
                holders[k] = cold_read.make_openrouter_agent_fn(
                    system_prompt=system, effort=effort, timeout=OR_TIMEOUT,
                    max_output_tokens=OR_MAX_OUTPUT, api_key=key)
            r = holders[k](prompt=prompt, model=selector, label=label) or {}
            return r.get("output") or ""
        return fn, (lambda: None)
    # codex: developer_instructions fixed per thread factory -> make per-call factories
    holders = {}

    def fn(system, prompt, label):
        key = hashlib.sha256(system.encode()).hexdigest()[:8]
        if key not in holders:
            holders[key] = cold_read.make_codex_agent_fn(system_prompt=system, effort=effort)
        f, _ = holders[key]
        return (f(prompt=prompt, model=model_id, label=label) or {}).get("output") or ""

    def close():
        for _, c in holders.values():
            c()
    return fn, close


def assemble(model_id: str, persona: str) -> Path:
    d = dag_dir(model_id, persona)
    parts = []
    for n in range(1, len(slugs()) + 1):
        gp = gate_path(d, n)
        if gp.exists():
            parts.append(clean_markdown(gp.read_text(encoding="utf-8")).rstrip())
        if n % DECADE == 0 and ck_path(d, n).exists():
            parts.append(
                "\n----- CARRY-FORWARD MINTED AFTER CHAPTER "
                f"{n} -----\n"
                + clean_markdown(ck_path(d, n).read_text(encoding="utf-8")).rstrip()
            )
    out = PANEL_ROOT / model_id / f"{persona}--volume-dag.md"
    out.write_text(
        f"# Capture DAG record — {persona}\n\n*model: {model_id} · protocol: "
        f"{PROTOCOL} · assembled {date.today().isoformat()}*\n\n"
        + "\n".join(parts)
        + "\n",
        encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--personas", nargs="*", default=PERSONAS, choices=ALL_PERSONAS)
    ap.add_argument("--to", type=int, default=N_CH)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--fresh", action="store_true",
                    help="re-read the target chapter (--to N), overwriting its existing "
                         "gate and, on a decade boundary, re-minting its carry-forward")
    args = ap.parse_args()

    if args.assemble:
        for m in args.models:
            for p in args.personas:
                print(assemble(m, p))
        return

    # Retired personas stay assemble-able (above) but must not be run again.
    retired = [p for p in args.personas if p in RETIRED_PERSONAS]
    if retired:
        raise SystemExit(
            f"refusing to run retired persona(s): {', '.join(retired)}. "
            "Retired by author ruling (see RETIRED_PERSONAS); existing gates are "
            "kept and --assemble still works. Reviving one needs author approval.")

    results, failures = [], []

    def one(m, p):
        fn, close = make_agent(m, args.effort)
        try:
            results.append(run_reader(m, p, fn, args.to,
                                      args.to if args.fresh else None))
        except Exception as e:  # noqa: BLE001
            failures.append(f"{m}·{p}: {e}")
            print(f"  FAIL {m}·{p}: {e}", flush=True)
        finally:
            close()

    readers = [(m, p) for m in args.models for p in args.personas]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda t: one(*t), readers))

    print("\n".join(results))
    if failures:
        print("failures:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
