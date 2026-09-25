#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Blind reader-difficulty pass: ask a model which sentences were work to read,
knowing nothing about how `reading_effort.py` measures anything.

The point is an INDEPENDENT second opinion, so the comparison means something.
`reading_effort.py` is a parser plus arithmetic and has already been caught
inventing findings (15 of 20 `front` flags on the-bench were mis-parses). A
model reading the prose cold is wrong in completely different ways, so
agreement between them is evidence and disagreement is a question worth asking.

Blindness is enforced on three fronts:

1. **No vocabulary leak.** The prompt never says clause, subordinate, nest,
   suspension, preposition, dependency, branching, or length. It asks only
   where reading cost effort. A model told what shapes to look for would find
   those shapes and the comparison would be circular.
2. **No tool output.** The model never sees a score, a flag, or which
   sentences the tool picked.
3. **No repo contamination.** Every lane runs from a throwaway non-repo cwd
   with project instructions excluded, exactly as the cold-read lanes do, so
   CLAUDE.md, git state and the memory index cannot reach the reader.

Sentences are enumerated by importing `reading_effort` rather than
re-splitting, so both instruments score the SAME units and results join
exactly, by content fingerprint rather than by line.

TOKEN RULE (CLAUDE.md). Subscription lanes are the default and need no
permission: `claude -p` for Claude models, the Codex CLI for GPT. OpenRouter
models (glm, kimi, qwen, deepseek) bill per token and are **author-authorized
only** — this tool refuses to run one without --authorized.

Usage:
    tools/effort_blind.py the-bench --model claude-sonnet-5
    tools/effort_blind.py the-bench --model gpt-5.6-sol
    tools/effort_blind.py the-bench --model glm-5.3 --authorized
    tools/effort_blind.py the-bench --compare
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import reading_effort as RE  # noqa: E402  (stdlib-only at import time)

OUT = REPO / "audits" / "reading-effort" / "blind"

# Lane per model. Subscription lanes are free and default; `openrouter` bills.
LANES = {
    "claude-sonnet-5": ("claude", "sonnet"),
    "claude-opus-4-8": ("claude", "opus"),
    "claude-fable-5": ("claude", "fable"),
    "claude-fable-5-1": ("claude", "claude-fable-5-1"),
    "gpt-5.6-sol": ("codex", "gpt-5.6-sol"),
    "gpt-5.5": ("codex", "gpt-5.5"),
    "gpt-6-astra": ("codex", "gpt-6-astra"),
    "glm-5.3": ("openrouter", "z-ai/glm-4.6"),
    "kimi-k3": ("openrouter", "moonshotai/kimi-k3"),
}

# ---------------------------------------------------------------------------
# The blind prompt. Every word here was chosen to avoid naming a structure.
# ---------------------------------------------------------------------------
SYSTEM = """\
You are an experienced, attentive reader of literary fiction. You read the way \
a good editor reads: at natural pace, paying attention to your own experience \
as you go.

You will be given one chapter of a novel, with every sentence numbered. Read it \
straight through, in order, as a reader would.

Your only task is to notice where the READING ITSELF cost you effort — places \
where you had to slow down, back up, re-read, or hold something in your head \
longer than felt comfortable before it paid off. Where you lost the thread and \
had to find it again. Where you reached the end of a sentence and were not sure \
what it had said.

Judge the EXPERIENCE OF READING, not the quality of the writing. A sentence can \
be beautiful and still be work. A sentence can be plain and easy. You are not \
assessing prose style, taste, subject matter, or craft — only cost to the reader.

Most sentences will be fine. Do not pad the list. Flag a sentence only if it \
genuinely cost you something; if nothing did, return few or none. Do not aim for \
any particular number.

One thing to ignore. The sentence numbering is applied mechanically, and it \
sometimes cuts a single line of speech in half — so a quotation mark may look \
unclosed at the end of one numbered sentence and unopened at the start of the \
next. That is an artifact of the numbering, not of the writing. Read across it, \
and never flag it.

Rate each one you flag:
  3 = I had to re-read it to understand it
  2 = I got through it once, but it took real work
  1 = a noticeable bump, but I kept moving

For each, say in your own words what made it work to read. Describe your \
experience, not a diagnosis.

Return ONLY a JSON array, no prose before or after, no markdown fence:

[{"n": 42, "cost": 3, "why": "..."}, {"n": 87, "cost": 1, "why": "..."}]

`n` is the sentence number shown in brackets. Return [] if nothing cost you.
"""


def enumerate_sentences(path: Path):
    """Sentence units identical to reading_effort's, with its fingerprints, so
    the two instruments join exactly. Paragraph breaks are preserved so the
    model reads prose rather than a list."""
    rows, blocks = [], []
    for line, raw in RE.load_prose(path):
        para = []
        for text in RE.split_sentences(RE.clean(raw)):
            rows.append({
                "n": len(rows) + 1,
                "line": line,
                "text": text,
                "fp": RE.fingerprint("effort", text),
            })
            para.append(f"[{len(rows)}] {text}")
        if para:
            blocks.append(" ".join(para))
    return rows, "\n\n".join(blocks)


def parse_reply(raw) -> list[dict]:
    """Models wrap JSON in fences or prose however much you ask them not to.

    Lanes also disagree on shape: `claude -p` yields a plain string, while the
    cold-read codex/openrouter factories return {"output", "id", "usage"}.
    """
    if isinstance(raw, dict):
        raw = raw.get("output") or raw.get("text") or ""
    txt = str(raw).strip()
    txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.MULTILINE).strip()
    start, end = txt.find("["), txt.rfind("]")
    if start != -1 and end != -1:
        try:
            items = json.loads(txt[start:end + 1])
            return [{"n": int(it["n"]), "cost": int(it.get("cost", 1)),
                     "why": str(it.get("why", "")).strip()}
                    for it in items if isinstance(it, dict) and "n" in it]
        except json.JSONDecodeError as exc:
            print(f"[salvage] array did not parse ({exc}); recovering objects "
                  f"individually", file=sys.stderr)

    # Salvage. A whole-array parse is all-or-nothing, and one bad escape
    # anywhere throws away every finding — unacceptable on a PAID lane, where
    # re-running costs real money. glm-5.3 returned a malformed array at char
    # 2744 on its first run. Pull the well-formed objects out one at a time.
    objs = re.findall(
        r'\{\s*"n"\s*:\s*(\d+)\s*,\s*"cost"\s*:\s*(\d+)\s*,'
        r'\s*"why"\s*:\s*"((?:[^"\\]|\\.)*)"\s*\}', txt)
    if not objs:
        raise ValueError(f"no recoverable findings in reply "
                         f"(first 300 chars): {txt[:300]}")
    return [{"n": int(n), "cost": int(c),
             "why": c_why.encode().decode("unicode_escape", "replace").strip()}
            for n, c, c_why in objs]


# ---------------------------------------------------------------------------
# Lanes
# ---------------------------------------------------------------------------
def run_claude(model: str, prompt: str) -> str:
    """Clean-lane `claude -p`, mirroring cold_read_grounded.run_claude_headless:
    throwaway non-repo cwd and dynamic system-prompt sections excluded, so no
    CLAUDE.md, git snapshot or memory index reaches the reader.
    ANTHROPIC_API_KEY is scrubbed — subscription OAuth only, per the token rule."""
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)
    with tempfile.TemporaryDirectory(prefix="effortblind-") as td:
        spf = Path(td) / "system-prompt.md"
        spf.write_text(SYSTEM, encoding="utf-8")
        cmd = ["claude", "-p", "--model", model,
               "--system-prompt-file", str(spf),
               "--exclude-dynamic-system-prompt-sections"]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           env=env, cwd=td, timeout=2400)
    if r.returncode != 0:
        detail = ((r.stdout or "") + "\n" + (r.stderr or "")).strip()[-600:]
        raise RuntimeError(f"claude -p failed: {detail}")
    return r.stdout


def run_codex(model: str, prompt: str) -> str:
    """Subscription Codex lane, reusing the cold-read factory (empty cwd +
    read-only sandbox hold the blind boundary)."""
    import cold_read
    fn, cleanup = cold_read.make_codex_agent_fn(system_prompt=SYSTEM, effort="medium")
    try:
        return fn(prompt=prompt, model=model, label="effort-blind")
    finally:
        cleanup()


def run_openrouter(model_id: str, prompt: str) -> str:
    """PAID lane. Guarded by --authorized at the call site."""
    import cold_read
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OpenRouter lane needs OPENROUTER_API_KEY in the environment")
    fn = cold_read.make_openrouter_agent_fn(
        system_prompt=SYSTEM, api_key=key, policy="read")
    return fn(prompt=prompt, model=model_id, label="effort-blind")


def run_model(model: str, prompt: str, authorized: bool) -> str:
    if model not in LANES:
        raise SystemExit(f"unknown model {model!r}; known: {', '.join(LANES)}")
    lane, ident = LANES[model]
    if lane == "openrouter" and not authorized:
        raise SystemExit(
            f"{model} runs through OpenRouter, which BILLS PER TOKEN.\n"
            "CLAUDE.md requires the author's explicit authorization for every "
            "paid run. Re-run with --authorized once they have given it.")
    print(f"[lane] {lane} · {model} → {ident}"
          + ("  (PAID, author-authorized)" if lane == "openrouter"
             else "  (subscription, free)"), file=sys.stderr)
    if lane == "claude":
        return run_claude(ident, prompt)
    if lane == "codex":
        return run_codex(ident, prompt)
    return run_openrouter(ident, prompt)


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------
def compare(slug: str, rows: list[dict]) -> None:
    """Cross-tabulate every blind run against the tool, joined by fingerprint.

    Reports each side's picks, the overlap, and — the interesting column — what
    each side found ALONE. A sentence only the tool flags is a candidate false
    positive; one only the readers flag is a defect class the tool cannot see.
    """
    tool_path = REPO / "audits" / "reading-effort" / f"{slug}.md"
    if not tool_path.is_file():
        sys.exit(f"no tool worklist at {tool_path} — run reading_effort.py --save first")
    tool_fps = set(re.findall(r"`\[#([0-9a-f]{12})\]`", tool_path.read_text()))
    by_fp = {r["fp"]: r for r in rows}
    by_n = {r["n"]: r for r in rows}

    runs = {}
    for f in sorted((OUT).glob(f"*/{slug}.json")):
        data = json.loads(f.read_text())
        picks = {}
        for it in data["findings"]:
            # fp when the file has it (all runs from 2026-09-20 on, plus the
            # backfilled ones); fall back to the number for anything older.
            fp = it.get("fp") or (by_n.get(it["n"]) or {}).get("fp")
            if fp:
                picks[fp] = it
        runs[data["model"]] = picks

    if not runs:
        sys.exit(f"no blind runs found under {OUT}/*/{slug}.json")

    print(f"\nBLIND vs TOOL — {slug}")
    print(f"  tool flagged {len(tool_fps)} of {len(rows)} sentences\n")
    print(f"  {'model':<18}{'picks':>7}{'∩ tool':>9}{'blind only':>13}{'agreement':>12}")
    for model, picks in runs.items():
        inter = len(set(picks) & tool_fps)
        rate = f"{100 * inter / len(picks):.0f}%" if picks else "—"
        print(f"  {model:<18}{len(picks):>7}{inter:>9}{len(picks) - inter:>13}{rate:>12}")

    if len(runs) > 1:
        common = set.intersection(*(set(p) for p in runs.values()))
        print(f"\n  all {len(runs)} readers agree on {len(common)} sentences; "
              f"{len(common & tool_fps)} of those the tool also flagged")
        missed = sorted(common - tool_fps,
                        key=lambda fp: -max(runs[m][fp]["cost"] for m in runs if fp in runs[m]))
        if missed:
            print(f"\n  BLIND SPOT — every reader flagged these, the tool did not:")
            for fp in missed[:10]:
                r = by_fp[fp]
                why = next(runs[m][fp]["why"] for m in runs if fp in runs[m])
                print(f"    {slug}.md:{r['line']}  {r['text'][:110]}")
                print(f"      reader: {why[:150]}")
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("scene")
    ap.add_argument("--model", help="one of: " + ", ".join(LANES))
    ap.add_argument("--authorized", action="store_true",
                    help="author has authorized this PAID OpenRouter run")
    ap.add_argument("--compare", action="store_true",
                    help="cross-tabulate saved blind runs against the tool")
    ap.add_argument("--dump-prompt", action="store_true",
                    help="print the exact prompt and exit (inspect the blindness)")
    args = ap.parse_args()

    path = RE.resolve_scene(args.scene)
    rows, body = enumerate_sentences(path)
    prompt = (f"Here is the chapter. Every sentence is numbered in brackets.\n\n"
              f"{body}\n\nReturn the JSON array now.")

    if args.dump_prompt:
        print(SYSTEM)
        print("=" * 70)
        print(prompt[:3000] + f"\n… [{len(rows)} sentences total]")
        return
    if args.compare:
        compare(path.stem, rows)
        return
    if not args.model:
        sys.exit("need --model (or --compare)")

    raw = run_model(args.model, prompt, args.authorized)
    dest = OUT / args.model
    dest.mkdir(parents=True, exist_ok=True)
    # Write the raw response BEFORE parsing. A parse failure must never
    # destroy a response that cost money (or subscription quota) to obtain —
    # the salvage path and any later re-parse both work off this file.
    rawtxt = raw.get("output", "") if isinstance(raw, dict) else str(raw)
    (dest / f"{path.stem}.raw.txt").write_text(rawtxt, encoding="utf-8")
    findings = parse_reply(raw)
    # Key every finding by content fingerprint as well as by number. The
    # number is only stable until the chapter is edited — the first revision
    # pass after the panel ran split two sentences and shifted every index
    # after them, which would have silently mis-joined the results. The
    # fingerprint rides with the sentence.
    n2fp = {r["n"]: r["fp"] for r in rows}
    for it in findings:
        it["fp"] = n2fp.get(it["n"], "")
    out = dest / f"{path.stem}.json"
    out.write_text(json.dumps({
        "model": args.model,
        "scene": path.stem,
        "sentences": len(rows),
        "findings": findings,
    }, indent=2), encoding="utf-8")
    costs = {c: sum(1 for f in findings if f["cost"] == c) for c in (3, 2, 1)}
    print(f"{args.model}: {len(findings)} of {len(rows)} sentences flagged "
          f"(cost 3:{costs[3]} 2:{costs[2]} 1:{costs[1]}) → "
          f"{out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
