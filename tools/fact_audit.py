#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Lane A — cross-chapter factual audit of drafted prose.

Catches the class the per-chapter instruments cannot: a fact established in
one chapter contradicted in another. The worked example is `not-enough.md`,
where Pace waits for Vee and "his body gathered itself toward ... a truck
turning in" four lines before "her car finding the narrow drive" — Vee drives
a Corolla; the truck is Pace's.

TWO PASSES, and the split is the point:

  1. LEDGER — one call over the WHOLE volume, producing a ledger of
     falsifiable attributes (vehicles, garments, marks, spatial layout, named
     objects, dates, who-knows-what). Volume One is ~202k tokens, well inside
     a frontier context, so the auditor sees every chapter at once.
  2. CHECK  — per chapter, ledger + that chapter, reporting contradictions.

Deliberately NOT a DAG. The cold-read and capture lanes limit memory on
purpose, to simulate what a first reader knows at chapter N. An auditor wants
the opposite — total recall — so the sequential-memory machinery is the wrong
shape here even though the scaffolding (audits/ tree, restartability, author
review loop) is reused.

The ledger is derived per model. Running a second model and DIFFING the two
ledgers is the real thoroughness win: where independently-derived ledgers
disagree, either the prose is ambiguous or one model confabulated, and both
are worth knowing.

FLAGS, never findings — same discipline as the style linter and line audit.
It over-flags by design and the author rules on every item.

Usage:
    tools/fact_audit.py --model gpt-5.6-sol --ledger-only     # build the ledger
    tools/fact_audit.py --model gpt-5.6-sol --slugs not-enough the-pointing-game
    tools/fact_audit.py --model gpt-5.6-sol --volume 1        # whole volume
    tools/fact_audit.py --diff-ledgers gpt-5.6-sol gemini-3.8-flash
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import volume_scenes  # noqa: E402

AUDIT_ROOT = REPO / "audits" / "fact-audit"
PROMPTS = AUDIT_ROOT / "prompts"


def out_dir(model_id: str) -> Path:
    return AUDIT_ROOT / model_id


def ledger_path(model_id: str, volume: int) -> Path:
    return out_dir(model_id) / f"ledger-vol{volume}.md"


def report_path(model_id: str, slug: str) -> Path:
    return out_dir(model_id) / f"{slug}.md"


def volume_prose(volume: int) -> str:
    """Every drafted chapter of the volume, titled, in reading order."""
    parts = []
    for i, slug in enumerate(volume_scenes.volume_slugs(volume, drafted_only=True), 1):
        parts.append(f"===== CHAPTER {i}: {checkpoint_bundle.display_title(slug)} "
                     f"({slug}) =====\n\n{checkpoint_bundle.clean_scene_text(slug)}\n")
    return "\n".join(parts)


def chapter_block(slug: str, n: int) -> str:
    return (f"===== CHAPTER {n}: {checkpoint_bundle.display_title(slug)} ({slug}) "
            f"=====\n\n{checkpoint_bundle.clean_scene_text(slug)}\n")


def load_prompt(name: str) -> str:
    p = PROMPTS / f"{name}.md"
    if not p.exists():
        raise SystemExit(f"missing prompt: {p}")
    return p.read_text(encoding="utf-8")


def work_dir(model_id: str, label: str) -> Path:
    """A PERSISTENT scratch directory inside the project.

    Deliberately not a tempfile.TemporaryDirectory. The Claude lane can write
    files, and on 2026-09-19 claude-opus-5 saved its ledger to FACT_LEDGER.md
    in a temp cwd and replied with a summary of having done so — the directory
    was discarded on exit and a good 47k artifact was lost. Anything a model
    produces now survives the run and can be recovered or inspected.

    Gitignored: this is machine scratch. The artifact that matters is promoted
    to ledger-vol<N>.md."""
    d = AUDIT_ROOT / ".work" / model_id / label
    d.mkdir(parents=True, exist_ok=True)
    return d


def make_claude_agent(system_prompt: str, effort: str, cwd: Path):
    """Claude headless lane on subscription OAuth, run in a PERSISTENT cwd.

    Mirrors checkpoint_extract.make_claude_extractor_fn but keeps the working
    directory, so a file the model writes is recoverable instead of discarded."""
    import os
    import subprocess

    def run(*, prompt: str, model: str, label: str):
        env = dict(os.environ)
        env.pop("ANTHROPIC_API_KEY", None)   # subscription auth only, per the token rule
        sp = cwd / "system-prompt.md"
        sp.write_text(system_prompt, encoding="utf-8")
        result = subprocess.run(
            ["claude", "-p", "--model", model,
             "--system-prompt-file", str(sp),
             "--exclude-dynamic-system-prompt-sections",
             "--effort", effort],
            input=prompt, capture_output=True, text=True,
            cwd=str(cwd), env=env, timeout=2400,
        )
        if result.returncode != 0:
            detail = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()[-600:]
            raise RuntimeError(f"claude -p failed: {detail}")
        return {"output": result.stdout, "usage": {}, "id": label}

    return run


def recover_from_work(cwd: Path, required: tuple[str, ...]) -> str | None:
    """If the reply was a summary, look for the artifact the model wrote.

    Returns the largest file in the scratch dir that carries the structure a
    ledger must have, or None."""
    best, best_len = None, 0
    for f in sorted(cwd.rglob("*.md")):
        if f.name == "system-prompt.md":
            continue
        try:
            body = f.read_text(encoding="utf-8")
        except OSError:
            continue
        if len(body) > best_len and all(h.lower() in body.lower() for h in required):
            best, best_len = body, len(body)
    return best


def make_agent(model: str, effort: str, cwd: Path | None = None):
    """Dispatch to the right lane by model id.

    Three vendors are wired so the ledgers are genuinely independent —
    ledgers derived by one model share that model's blind spots, so
    disagreement between vendors is the signal worth having.

      claude-*   headless clean lane, Claude subscription OAuth
      <p>/<m>    OpenRouter, paid, under the [openrouter.policy.fact] tag
      else       codex subscription (gpt-5.6-sol, gpt-5.5)
    """
    import cold_read
    system = load_prompt("system")
    if model.startswith("claude-"):
        if cwd is None:
            raise SystemExit("claude lane needs a working directory")
        return make_claude_agent(system, effort, cwd), (lambda: None)
    if "/" in model:
        import os
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("OpenRouter model needs OPENROUTER_API_KEY set")
        print(f"[auth] openrouter — billing PER TOKEN (author-authorized) · {model}",
              file=sys.stderr)
        return (cold_read.make_openrouter_agent_fn(
            system_prompt=system, policy="fact", effort=effort, api_key=key),
            (lambda: None))
    return cold_read.make_codex_agent_fn(system_prompt=system, effort=effort)


def max_input_tokens(model: str) -> int | None:
    """Author-verified input ceiling from cold_read_pricing.toml, or None."""
    import tomllib
    cfg = tomllib.loads((REPO / "tools" / "cold_read_pricing.toml")
                        .read_text(encoding="utf-8"))
    return cfg.get("models", {}).get(model, {}).get("max_input")


def preflight(model: str, prompt_chars: int, label: str) -> None:
    """Fail BEFORE the call when a bundle cannot fit.

    This lane is the only one that builds whole-volume prompts, so it is the
    only one that can outgrow a model. Discovering that mid-request wastes the
    call and — on a slow provider — a long wait first."""
    limit = max_input_tokens(model)
    if limit is None:
        print(f"[preflight] no recorded max_input for {model}; proceeding "
              f"(~{prompt_chars//4:,} tokens)", file=sys.stderr)
        return
    est = prompt_chars // 4
    if est > limit:
        raise SystemExit(
            f"{label}: ~{est:,} input tokens exceeds {model}'s recorded ceiling "
            f"of {limit:,}. Narrow the scope (--volume/--slugs) or record a "
            f"larger max_input in tools/cold_read_pricing.toml."
        )
    print(f"[preflight] ~{est:,} / {limit:,} input tokens ({est*100//limit}%)",
          file=sys.stderr)


def build_ledger(model: str, model_id: str, volume: int, effort: str) -> str:
    path = ledger_path(model_id, volume)
    path.parent.mkdir(parents=True, exist_ok=True)
    prose = volume_prose(volume)
    print(f"[ledger] volume {volume} · {len(prose):,} chars "
          f"(~{len(prose)//4:,} tokens) · {model}", file=sys.stderr)
    preflight(model, len(prose), f"ledger-vol{volume}")
    cwd = work_dir(model_id, f"ledger-vol{volume}")
    agent_fn, close = make_agent(model, effort, cwd)
    try:
        r = agent_fn(prompt=load_prompt("ledger").replace("{{PROSE}}", prose),
                     model=model, label=f"ledger-vol{volume}")
    finally:
        close()
    body = (r.get("output") or "").strip()
    # A lane with file-write capability may SAVE the ledger and reply with a
    # summary of having done so; the working directory is then discarded and
    # the artifact is lost. Length alone does not catch it — the summary is
    # prose of respectable length — so check for the structure a ledger must
    # have (claude-opus-5, 2026-09-19).
    required = ("People", "Vehicles")
    # Always keep the raw reply — nothing a paid or slow call produced should
    # be discarded because validation rejected it.
    (cwd / "raw-response.md").write_text(body, encoding="utf-8")
    missing = [h for h in required if h.lower() not in body.lower()]
    if len(body) < 4000 or missing:
        salvaged = recover_from_work(cwd, required)
        if salvaged:
            print(f"[recover] reply was a summary; promoting the file the model "
                  f"wrote in {cwd} ({len(salvaged):,} chars)", file=sys.stderr)
            body = salvaged
        else:
            # Surface WHY. `max_output_tokens` is shared between reasoning and
            # visible output, so a model thinking hard at effort=high can spend
            # the whole budget and return little or nothing — that looks like a
            # refusal until you see the token split (glm-5.3 returned 0 chars,
            # gemini-3.8-flash a ledger truncated mid-section, both on 2026-09-19).
            u = r.get("usage") or {}
            diag = " · ".join(
                f"{k}={u[k]}" for k in
                ("finishReason", "output", "reasoningTokens", "max_output_tokens")
                if u.get(k) is not None
            )
            raise SystemExit(
                f"ledger looks like a summary, not a ledger ({len(body)} chars"
                + (f"; missing section(s): {', '.join(missing)}" if missing else "")
                + f"). Nothing recoverable in {cwd}."
                + (f"\n  provider: {diag}" if diag else "")
                + "\n  If reasoning consumed the budget, retry with a lower --effort."
            )
    path.write_text(
        f"# Fact ledger — Volume {volume}\n\n*model: {model} · "
        f"{date.today().isoformat()} · derived from prose only*\n\n---\n\n{body}\n",
        encoding="utf-8")
    print(f"[ledger] wrote {path}", file=sys.stderr)
    return body


def check_chapter(agent_fn, model: str, model_id: str, slug: str, n: int,
                  ledger: str) -> Path:
    """Reports are short, so no recovery path is needed here — but the raw
    reply is still kept beside the report for the same reason."""
    prompt = (load_prompt("check")
              .replace("{{LEDGER}}", ledger)
              .replace("{{CHAPTER}}", chapter_block(slug, n)))
    r = agent_fn(prompt=prompt, model=model, label=f"fact-{slug}")
    body = (r.get("output") or "").strip()
    p = report_path(model_id, slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    # Record what was actually audited, so a later prose edit makes the report
    # verifiably stale rather than silently so (the lesson from the cold-read
    # memory-window failure, 2026-09-17).
    sha = hashlib.sha256(
        checkpoint_bundle.clean_scene_text(slug).encode()).hexdigest()[:12]
    p.write_text(
        f"# Fact audit — {checkpoint_bundle.display_title(slug)}\n\n"
        f"*model: {model} · ch{n:03d} · {date.today().isoformat()} · "
        f"prose-sha ~{sha}*\n\n---\n\n{body}\n",
        encoding="utf-8")
    return p


# Models format the finding header differently — "**WHERE**", "**WHERE:**",
# "* **WHERE:**". A strict pattern silently reports zero findings for a model
# that is actually finding things, which happened twice on 2026-09-20 and
# produced two wrong conclusions before it was caught. Tally through this.
FINDING_RE = re.compile(r"^\s*[*-]?\s*\*\*WHERE:?\*\*:?", re.IGNORECASE | re.MULTILINE)


def count_findings(path: Path) -> int:
    try:
        return len(FINDING_RE.findall(path.read_text(encoding="utf-8")))
    except OSError:
        return 0


def tally(models: list[str], volume: int) -> None:
    slugs = volume_scenes.volume_slugs(volume, drafted_only=True)
    width = max(len(s) for s in slugs) + 2
    print("".ljust(width) + "".join(m[:10].ljust(11) for m in models))
    totals = {m: 0 for m in models}
    for s in slugs:
        row = []
        for m in models:
            n = count_findings(report_path(m, s))
            totals[m] += n
            row.append(str(n).ljust(11))
        if any(int(x) for x in row):
            print(s.ljust(width) + "".join(row))
    print("TOTAL".ljust(width) + "".join(str(totals[m]).ljust(11) for m in models))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="gpt-5.6-sol")
    ap.add_argument("--model-id", default=None, help="output dir (default: --model)")
    ap.add_argument("--volume", type=int, default=1)
    ap.add_argument("--slugs", nargs="*", help="limit the check pass to these chapters")
    ap.add_argument("--ledger-only", action="store_true")
    ap.add_argument("--rebuild-ledger", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="redo existing reports")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--tally", nargs="+", metavar="MODEL",
                    help="count findings per chapter across models")
    ap.add_argument("--diff-ledgers", nargs=2, metavar=("A", "B"),
                    help="report where two models' ledgers disagree")
    args = ap.parse_args()

    model_id = args.model_id or args.model

    if args.tally:
        tally(args.tally, args.volume)
        return

    if args.diff_ledgers:
        a, b = (ledger_path(m, args.volume) for m in args.diff_ledgers)
        for p in (a, b):
            if not p.exists():
                raise SystemExit(f"missing ledger: {p}")
        print(f"Ledger A: {a}\nLedger B: {b}\n")
        print("Diffing ledgers is a judgement task, not a text diff — feed both "
              "to a reviewer and ask where they disagree on a falsifiable fact.")
        return

    lp = ledger_path(model_id, args.volume)
    if args.rebuild_ledger or not lp.exists():
        ledger = build_ledger(args.model, model_id, args.volume, args.effort)
    else:
        ledger = checkpoint_bundle.checkpoint_body(lp.read_text(encoding="utf-8"))
        print(f"[ledger] reusing {lp}", file=sys.stderr)
    if args.ledger_only:
        return

    vol = volume_scenes.volume_slugs(args.volume, drafted_only=True)
    numbered = {s: i for i, s in enumerate(vol, 1)}
    targets = [s for s in vol if (not args.slugs or s in args.slugs)]
    if not args.fresh:
        targets = [s for s in targets if not report_path(model_id, s).exists()]
    if not targets:
        print("[check] nothing to do", file=sys.stderr)
        return

    print(f"[check] {len(targets)} chapter(s) · {args.model}", file=sys.stderr)
    agent_fn, close = make_agent(args.model, args.effort,
                                 work_dir(model_id, "check"))
    try:
        for slug in targets:
            p = check_chapter(agent_fn, args.model, model_id, slug,
                              numbered[slug], ledger)
            print(f"  {slug} -> {p}", file=sys.stderr)
    finally:
        close()


if __name__ == "__main__":
    main()
