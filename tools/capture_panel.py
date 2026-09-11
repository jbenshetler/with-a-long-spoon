#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Capture/retention panel — persona readers gate the free-sample chapters.

Contract: reviews/capture-panel/SPEC.md. Each read: core reader frame + one
persona (system prompt) → [jacket +] chapters 1-4 sequential with STOP/CONTINUE
gates. Lanes mirror tools/authorship_audit.py (claude headless subscription /
codex subscription / OpenRouter paid, author-authorized).

Usage:
  tools/capture_panel.py --full             # 4 personas x 8 models x 2 arms
  tools/capture_panel.py --personas fsog-refugee --models claude-opus-4-8 --arms jacket
  tools/capture_panel.py --full --dry-run
Existing outputs are skipped unless --force.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import authorship_audit  # noqa: E402  (run_claude, OPENROUTER_MODELS, CLAUDE_PREFIX)

PANEL_ROOT = REPO / "reviews" / "capture-panel"
PROTOCOL = "capture-panel-v1"
SAMPLE_SLUGS = ["the-bench", "standards", "the-pointing-game", "see-you-later"]
PERSONAS = ["romance-graduate", "fsog-refugee", "consent-sensitive", "dark-romance-control"]
ARMS = ("jacket", "cold")
MODELS = ["claude-fable-5", "claude-opus-4-8", "gpt-5.6-sol", "gpt-5.5",
          "kimi-k3", "glm-5.3-flash", "qwen3.8-max-0902", "deepseek-v4-pro-0813"]

OPENROUTER_MODELS = dict(authorship_audit.OPENROUTER_MODELS)
OPENROUTER_MODELS.setdefault("glm-5.3", "z-ai/glm-5.3")


def system_prompt(persona: str, core_file: str = "core.md") -> tuple[str, str]:
    core = (PANEL_ROOT / "prompts" / core_file).read_text(encoding="utf-8")
    pers = (PANEL_ROOT / "personas" / f"{persona}.md").read_text(encoding="utf-8")
    text = core.rstrip() + "\n\n" + pers.strip() + "\n"
    return text, hashlib.sha256(text.encode()).hexdigest()[:12]


def volume_user_prompt() -> str:
    """Jacket + all drafted Volume One chapters (volume mode is jacket-arm by design)."""
    jacket = checkpoint_bundle.jacket_packet()
    if not jacket:
        raise SystemExit("volume mode: empty jacket packet")
    parts = [f"===== JACKET COPY =====\n\n{jacket}\n"]
    v1_slugs = checkpoint_bundle.volume_scenes.volume_one_slugs(drafted_only=True)
    for i, slug in enumerate(v1_slugs, 1):
        title = checkpoint_bundle.display_title(slug)
        body = checkpoint_bundle.clean_scene_text(slug)
        parts.append(f"===== CHAPTER {i}: {title} =====\n\n{body}\n")
    parts.append("===== END OF VOLUME ONE =====\n\nBegin. Gate after each "
                 "chapter, decade journals and verdict exactly per your instructions.")
    return "\n".join(parts)


DAG_GATE_TITLE_CHECKS = {
    49: "Not Enough",
    50: "My Friend Randi",
    51: "Nothing Underneath",
}


def interview_record_path(model_id: str, persona: str, *, dag: bool = False) -> Path:
    suffix = "--volume-dag.md" if dag else "--volume.md"
    return PANEL_ROOT / model_id / f"{persona}{suffix}"


def validate_dag_record(model_id: str, persona: str, text: str) -> None:
    missing = [
        f"GATE {n} — {title}"
        for n, title in DAG_GATE_TITLE_CHECKS.items()
        if f"GATE {n} — {title}" not in text
    ]
    if missing:
        label = f"{model_id}·{persona}·volume-dag"
        raise RuntimeError(f"{label} missing required gates: {', '.join(missing)}")


def interview_record_sha(model_id: str, persona: str, arm: str) -> str | None:
    if arm == "volume-dag-interview":
        rec = interview_record_path(model_id, persona, dag=True)
    elif arm == "volume-interview":
        rec = interview_record_path(model_id, persona)
    else:
        return None
    return hashlib.sha256(rec.read_bytes()).hexdigest()[:12]


def interview_user_prompt(model_id: str, persona: str, *, dag: bool = False) -> str:
    rec = interview_record_path(model_id, persona, dag=dag)
    if not rec.exists():
        raise RuntimeError(f"interview needs {rec.relative_to(REPO)} first")
    text = rec.read_text(encoding="utf-8")
    if dag:
        validate_dag_record(model_id, persona, text)
    body = text.split("\n", 4)[-1]
    source = "DAG reading record" if dag else "READING RECORD"
    return (f"===== YOUR {source.upper()} =====\n\n{body}\n\n"
            "===== END OF RECORD =====\n\nAnswer T1, then T2, then T3.")


def user_prompt(arm: str) -> str:
    parts = []
    if arm == "jacket":
        jacket = checkpoint_bundle.jacket_packet()
        if not jacket:
            raise SystemExit("jacket arm: empty jacket packet")
        parts.append(f"===== JACKET COPY =====\n\n{jacket}\n")
    for i, slug in enumerate(SAMPLE_SLUGS, 1):
        title = checkpoint_bundle.display_title(slug)
        body = checkpoint_bundle.clean_scene_text(slug)
        parts.append(f"===== CHAPTER {i}: {title} =====\n\n{body}\n")
    parts.append("===== END OF SAMPLE =====\n\nBegin. Gate after each chapter, "
                 "exactly per your instructions.")
    return "\n".join(parts)


def out_path(model_id: str, persona: str, arm: str) -> Path:
    return PANEL_ROOT / model_id / f"{persona}--{arm}.md"


def validate(text: str, label: str, arm: str = "") -> str:
    t = text.strip()
    if len(t) < 300:
        raise RuntimeError(f"suspiciously short read for {label} ({len(t)} chars)")
    if arm in {"volume-interview", "volume-dag-interview"}:
        if "T3" not in t:
            raise RuntimeError(f"malformed interview for {label}: no T3")
        return t
    if "GATE 1" not in t.upper().replace("GATE  ", "GATE "):
        raise RuntimeError(f"malformed read for {label}: no GATE 1")
    if "VERDICT" not in t.upper() and "STOP" not in t.upper():
        raise RuntimeError(f"malformed read for {label}: neither VERDICT nor STOP")
    return t


def clean_markdown(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n"



def write_output(model_id: str, persona: str, arm: str, sha: str, text: str) -> Path:
    out = out_path(model_id, persona, arm)
    out.parent.mkdir(parents=True, exist_ok=True)
    if arm == "volume":
        chapters = "Volume One full text"
    elif arm == "volume-interview":
        chapters = "single-go volume record"
    elif arm == "volume-dag-interview":
        chapters = "capture-DAG volume record"
    else:
        chapters = ", ".join(SAMPLE_SLUGS)
    input_sha = interview_record_sha(model_id, persona, arm)
    input_part = f" · input-sha: {input_sha}" if input_sha else ""
    out.write_text(
        f"# Capture panel — {persona} · {arm}\n\n"
        f"*model: {model_id} · persona: {persona} · arm: {arm} · "
        f"input: {chapters}{input_part} · protocol: {PROTOCOL} · "
        f"prompt-sha: {sha} · run: {date.today().isoformat()}*\n\n"
        f"{clean_markdown(text)}",
        encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--full", action="store_true",
                    help="all personas x 8-model panel x both arms (paid lane "
                         "author-authorized per SPEC)")
    ap.add_argument("--volume", action="store_true",
                    help="full-Vol-1 single-go read (jacket arm), per-chapter "
                         "gates + decade journals; arm forced to 'volume'")
    ap.add_argument("--interview", action="store_true",
                    help="post-volume T1/T2/T3 funnel from the reader's own "
                         "record (requires --volume output on disk)")
    ap.add_argument("--dag-interview", action="store_true",
                    help="post-volume T1/T2/T3 funnel from the assembled capture-DAG "
                         "record (requires --volume-dag output on disk)")
    ap.add_argument("--personas", nargs="*", default=None, choices=PERSONAS)
    ap.add_argument("--models", nargs="*", default=None)
    ap.add_argument("--arms", nargs="*", default=None, choices=list(ARMS))
    ap.add_argument("--effort", default="low")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    vol_mode = args.volume or args.interview or args.dag_interview
    personas = args.personas or (PERSONAS if (args.full or vol_mode) else None)
    models = args.models or (MODELS if args.full else None)
    if args.dag_interview:
        arms = ["volume-dag-interview"]
    elif vol_mode:
        arms = ["volume-interview" if args.interview else "volume"]
    else:
        arms = args.arms or (list(ARMS) if args.full else None)
    if not personas or not models or not arms:
        ap.error("give --full / --volume / --interview (+--models), or --personas/--models/--arms")

    if args.interview or args.dag_interview:
        prompts = {p: system_prompt(p, "funnel.md") for p in personas}
        user = None  # per-(model,persona), built lazily from the volume record
    elif args.volume:
        prompts = {p: system_prompt(p, "core-volume.md") for p in personas}
        user = {arms[0]: volume_user_prompt()}
    else:
        prompts = {p: system_prompt(p) for p in personas}
        user = {a: user_prompt(a) for a in arms}
    tasks = [(m, p, a) for m in models for p in personas for a in arms
             if args.force or not out_path(m, p, a).exists()]
    skipped = len(models) * len(personas) * len(arms) - len(tasks)
    print(f"planned: {len(tasks)} reads ({skipped} already on disk)", flush=True)
    if args.dry_run:
        for t in tasks:
            print("  %s · %s · %s" % t)
        return

    failures: list[str] = []
    task_set = set(tasks)

    def get_user(m, p, a):
        if a == "volume-interview":
            return interview_user_prompt(m, p)
        if a == "volume-dag-interview":
            return interview_user_prompt(m, p, dag=True)
        return user[a]

    def finish(m, p, a, sha, raw, label):
        write_output(m, p, a, sha, validate(raw, label, a))
        print(f"  done {label}", flush=True)

    def one_claude(m, p, a):
        label = f"{m}·{p}·{a}"
        try:
            text, sha = prompts[p]
            raw = authorship_audit.run_claude(m, text, get_user(m, p, a), label)
            finish(m, p, a, sha, raw, label)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{label}: {e}")
            print(f"  FAIL {label}: {e}", flush=True)

    def one_agent(fn, model_arg, m, p, a, sha):
        label = f"{m}·{p}·{a}"
        last = None
        for _ in range(2):
            try:
                result = fn(prompt=get_user(m, p, a), model=model_arg,
                            label=f"capture-{p}-{a}")
                finish(m, p, a, sha, result.get("output") or "", label)
                return
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(15)
        failures.append(f"{label}: {last}")
        print(f"  FAIL {label}: {last}", flush=True)

    def codex_lane(cm):
        import cold_read
        for p in personas:
            text, sha = prompts[p]
            fn, close = cold_read.make_codex_agent_fn(system_prompt=text, effort=args.effort)
            try:
                sub = [(m, a) for m in cm for a in arms if (m, p, a) in task_set]
                with ThreadPoolExecutor(max_workers=2) as pool:
                    list(pool.map(lambda t: one_agent(fn, t[0], t[0], p, t[1], sha), sub))
            finally:
                close()

    def openrouter_lane(om):
        import cold_read
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OpenRouter lane needs OPENROUTER_API_KEY (author-authorized)")
        print("[auth] openrouter lane — billing PER TOKEN (author-authorized)", flush=True)
        for p in personas:
            text, sha = prompts[p]
            fn = cold_read.make_openrouter_agent_fn(
                system_prompt=text, effort=args.effort, timeout=2400,
                max_output_tokens=8000, api_key=key)
            sub = [(m, a) for m in om for a in arms if (m, p, a) in task_set]
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(
                    lambda t: one_agent(fn, OPENROUTER_MODELS[t[0]],
                                        t[0], p, t[1], sha), sub))

    claude_tasks = [t for t in tasks if t[0].startswith(authorship_audit.CLAUDE_PREFIX)]
    or_models = [m for m in models if m in OPENROUTER_MODELS]
    codex_models = [m for m in models if not m.startswith(authorship_audit.CLAUDE_PREFIX)
                    and m not in OPENROUTER_MODELS]
    with ThreadPoolExecutor(max_workers=args.jobs + 2) as pool:
        futs = []
        if codex_models:
            futs.append(pool.submit(codex_lane, codex_models))
        if or_models:
            futs.append(pool.submit(openrouter_lane, or_models))
        futs += [pool.submit(one_claude, *t) for t in claude_tasks]
        for f in futs:
            f.result()

    print(f"\nfinished: {len(tasks) - len(failures)}/{len(tasks)} ok", flush=True)
    if failures:
        print("failures:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
