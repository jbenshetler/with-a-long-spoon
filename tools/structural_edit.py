#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Structural edit — blind diagnosis of a whole volume (or the series so far).

Stage 1, `diagnose`: a developmental-editor letter from raw prose plus the
public jacket, nothing else. No meta, no triage, no CLAUDE.md: Claude runs
through the clean headless lane (authorship_audit.run_claude), GPT through the
codex subscription lane in an empty cwd (cold_read.make_codex_agent_fn),
OpenRouter models only with the author's authorization (--paid).

Each letter has four parts (prompt: audits/structural/prompts/diagnose.md):
LETTER, CHAPTER MAP (per-chapter function + DRAG vote), FINDINGS (category,
chapters, severity, claim, evidence, question) and STRENGTHS. Quotes in the
evidence are checked against the bundle and marked; absence and pacing claims
carry no quote by nature and are checked later against
`tools/structure_metrics.py`, never trusted on one model's word.

A finding counts when two or more models report it (`consensus`, next stage);
the meta-aware reconciliation that proposes changes comes after that.

Targets:
  --volume N             volume N alone, with its own jacket
  --volume N --through   volumes 1..N, judging volume N in the light of the
                         earlier ones (its chapter map covers volume N only)

Usage:
  tools/structural_edit.py diagnose --volume 1 --models gpt-5.6-sol claude-opus-5-5
  tools/structural_edit.py diagnose --volume 3 --through --models gpt-5.6-sol
  tools/structural_edit.py diagnose --volume 1 --dry-run     # sizes only, no calls
Outputs: audits/structural/<target>/<model>.md (existing outputs are skipped
unless --fresh).

The bundle is the book as it ships: each chapter via
`checkpoint_bundle.reader_chapter_text` (clean prose plus the reader-facing date
lines), the same text the cold and capture readers see. `consensus` reads only
editor letters diagnosed from the current bundle; stale ones are skipped.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import checkpoint_bundle  # noqa: E402
import checkpoint_audit  # noqa: E402
import volume_scenes  # noqa: E402

ROOT = REPO / "audits" / "structural"
PROMPT = ROOT / "prompts" / "diagnose.md"
CLAUDE_PREFIX = "claude-"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bundle(volume: int, through: bool) -> tuple[str, int, int]:
    """(text, first chapter no., last chapter no.) of the volume under review."""
    slugs = checkpoint_bundle.reader_slugs()
    vols = range(1, volume + 1) if through else [volume]
    out = []
    for v in vols:
        _, packet = checkpoint_bundle.volume_packet(v)
        title = volume_scenes.volume_title(v)
        out.append(f"\n\n######## VOLUME {v}: {title} ########\n")
        if packet:
            out.append("===== JACKET / COVER COPY (marketing, not story) =====\n")
            out.append(packet)
        for s in volume_scenes.volume_slugs(v, drafted_only=True):
            n = slugs.index(s) + 1
            out.append(f"\n\n===== CHAPTER {n}: {checkpoint_bundle.display_title(s)} =====\n")
            # The chapter as the book ships it, date lines included — the same text
            # the cold and capture readers see (checkpoint_bundle.reader_chapter_text).
            out.append(checkpoint_bundle.reader_chapter_text(s))
    own = volume_scenes.volume_slugs(volume, drafted_only=True)
    first, last = slugs.index(own[0]) + 1, slugs.index(own[-1]) + 1
    planned = len(volume_scenes.volume_slugs(volume, drafted_only=False))
    note = ""
    if planned > len(own):
        note = (f"\nNote: volume {volume} is not finished; {planned - len(own)} of its "
                f"{planned} planned chapters are not written yet and are absent here. "
                "Judge what is present; do not count the gap itself as a finding.\n")
    return "\n".join(out).strip() + "\n" + note, first, last


def user_prompt(volume: int, through: bool, text: str, first: int, last: int) -> str:
    scope = (f"volumes 1 to {volume}; review volume {volume} (chapters {first}-{last}) "
             "in the light of the earlier volumes, and raise series-level problems too"
             if through and volume > 1 else
             f"volume {volume} (chapters {first}-{last}), read on its own")
    return (f"Here is the text. Your review covers {scope}. The CHAPTER MAP covers "
            f"chapters {first}-{last} only.\n\n{text}")


def target_dir(volume: int, through: bool) -> Path:
    return ROOT / (f"vol1-{volume}" if through and volume > 1 else f"vol{volume}")


QUOTE = re.compile(r"[\"“]([^\"”\n|]{12,400})[\"”]")


def check_quotes(raw: str, page_norm: str) -> tuple[int, int, list[str]]:
    good, bad = 0, []
    for q in QUOTE.findall(raw):
        parts = [checkpoint_audit.words(x) for x in re.split(r"\.\.\.|…", q)]
        parts = [x for x in parts if x]
        if parts and all(x in page_norm for x in parts):
            good += 1
        else:
            bad.append(q)
    return good, good + len(bad), bad


def validate(raw: str, first: int, last: int) -> str:
    for part in ("LETTER", "CHAPTER MAP", "FINDINGS", "STRENGTHS"):
        if not re.search(rf"^\s*\**{part}\**\s*$", raw, re.M):
            raise RuntimeError(f"missing section {part}")
    mapped = {int(m) for m in re.findall(r"^\s*(\d+)\s*\|", raw, re.M)}
    missing = [n for n in range(first, last + 1) if n not in mapped]
    if len(missing) > max(2, (last - first + 1) // 10):
        raise RuntimeError(f"chapter map missing {len(missing)} chapters: {missing[:8]}")
    if len(re.findall(r"^\s*FINDING\s+\d+", raw, re.M)) < 5:
        raise RuntimeError("fewer than 5 findings")
    return raw.strip()


def run_model(model: str, system: str, user: str, label: str, effort: str) -> str:
    if model.startswith(CLAUDE_PREFIX):
        import authorship_audit
        return authorship_audit.run_claude(model, system, user, label)
    import cold_read
    if not model.startswith("gpt-"):
        # OpenRouter (paid): the reader block's provider_model, routed through the
        # shared adapter so the quantization floor and per-call cost line apply.
        import os
        import cold_read_config
        provider = cold_read_config.openrouter_models().get(model)
        if not provider:
            raise SystemExit(f"{model} has no provider_model in ensemble-config.toml")
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OpenRouter lane needs OPENROUTER_API_KEY (author-authorized)")
        print(f"[auth] openrouter lane {model} — billing PER TOKEN (author-authorized)",
              flush=True)
        fn = cold_read.make_openrouter_agent_fn(
            system_prompt=system, policy="structural", effort=effort, api_key=key)
        return fn(prompt=user, model=provider, label=label).get("output") or ""
    fn, close = cold_read.make_codex_agent_fn(system_prompt=system, effort=effort)
    try:
        return fn(prompt=user, model=model, label=label).get("output") or ""
    finally:
        close()


def diagnose(args) -> None:
    system = PROMPT.read_text(encoding="utf-8")
    text, first, last = bundle(args.volume, args.through)
    user = user_prompt(args.volume, args.through, text, first, last)
    page_norm = checkpoint_audit.words(text)
    d = target_dir(args.volume, args.through)
    print(f"[structural] {d.relative_to(REPO)} · chapters {first}-{last} · "
          f"~{len(user) // 4:,} tokens in · bundle {sha(text)[:12]} · prompt {sha(system)[:12]}",
          flush=True)
    if args.dry_run:
        return
    for m in args.models:
        if not (m.startswith(CLAUDE_PREFIX) or m.startswith("gpt-")) and not args.paid:
            raise SystemExit(f"{m} is an OpenRouter (paid) lane; pass --paid only with "
                             "the author's authorization for this run")
    d.mkdir(parents=True, exist_ok=True)

    def one(m: str) -> str:
        out = d / f"{m}.md"
        if out.exists() and not args.fresh:
            return f"skip {m} (exists)"
        last_err = None
        # A paid lane gets one attempt: a retry re-bills the whole volume.
        for attempt in range(2 if (m.startswith(CLAUDE_PREFIX) or m.startswith("gpt-")) else 1):
            t0 = time.time()
            try:
                raw = validate(run_model(m, system, user, f"structural-{d.name}-{m}",
                                         args.effort), first, last)
            except Exception as e:  # noqa: BLE001
                last_err = e
                print(f"  retry {m}: {e}", flush=True)
                continue
            good, total, bad = check_quotes(raw, page_norm)
            head = (f"*structural-diagnose-v1 · {d.name} · model {m} · chapters {first}-{last} · "
                    f"bundle {sha(text)[:12]} · prompt {sha(system)[:12]} · quotes verified "
                    f"{good}/{total} · {date.today().isoformat()}*\n\n")
            tail = ("" if not bad else "\n\n## Unverified quotes\n\n" +
                    "\n".join(f"- “{q}”" for q in bad) + "\n")
            out.write_text(head + raw + "\n" + tail, encoding="utf-8")
            return f"done {m}: quotes {good}/{total} · {time.time() - t0:.0f}s"
        return f"FAIL {m}: {last_err}"

    with ThreadPoolExecutor(max_workers=len(args.models)) as pool:
        for msg in pool.map(one, args.models):
            print(f"  {msg}", flush=True)


# --------------------------------------------------------------------- consensus
BLOCK = re.compile(r"^\s*(FINDING|STRENGTH)\s+(\d+)\s*$(.*?)(?=^\s*(?:FINDING|STRENGTH)\s+\d+\s*$|^\s*STRENGTHS\s*$|\Z)",
                   re.M | re.S)
FIELD = re.compile(r"^\s*([A-Z]+):\s*(.*?)(?=^\s*[A-Z]+:|\Z)", re.M | re.S)
MAPLINE = re.compile(r"^\s*(\d+)\s*\|\s*(.*?)\s*\|\s*DRAG:\s*(none|some|heavy)", re.M | re.I)


def parse_letter(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8").split("\n\n## Unverified quotes")[0]
    items = {"F": [], "S": []}
    for kind, n, blob in BLOCK.findall(raw):
        f = {k: " ".join(v.split()) for k, v in FIELD.findall(blob)}
        f["n"] = int(n)
        items["F" if kind == "FINDING" else "S"].append(f)
    drag = {int(n): d.lower() for n, _, d in MAPLINE.findall(raw)}
    fn = {int(n): fx.strip() for n, fx, _ in MAPLINE.findall(raw)}
    return {"items": items, "drag": drag, "function": fn}


def chapters_of(spec: str) -> set[int]:
    out = set()
    for a, b in re.findall(r"(\d+)\s*(?:[-–—]\s*(\d+))?", spec or ""):
        a = int(a)
        out |= set(range(a, int(b) + 1)) if b else {a}
    return out


def consensus(args) -> None:
    d = target_dir(args.volume, args.through)
    # Editor letters only (never the consensus or reconcile outputs), and only those
    # diagnosed from the current bundle: a letter on an older text is stale and is
    # left out rather than mixed in.
    current = sha(bundle(args.volume, args.through)[0])[:12]
    letters = []
    for p in sorted(d.glob("*.md")):
        if p.name.startswith(("consensus", "reconcile")):
            continue
        m = re.search(r"bundle ([0-9a-f]{12})", p.read_text(encoding="utf-8").split("\n", 1)[0])
        if m and m.group(1) != current:
            print(f"skip {p.name}: diagnosed from bundle {m.group(1)}, current {current} "
                  "(re-run diagnose --fresh to include it)", file=sys.stderr)
            continue
        letters.append(p)
    if len(letters) < 2:
        raise SystemExit(f"need two or more letters in {d.relative_to(REPO)}")
    models = [p.stem for p in letters]
    parsed = {m: parse_letter(p) for m, p in zip(models, letters)}
    letter = {m: chr(ord("A") + i) for i, m in enumerate(models)}
    lines = []
    for m in models:
        L = letter[m]
        for f in parsed[m]["items"]["F"]:
            lines.append(f"{L}{f['n']} [{f.get('CATEGORY','')}; ch {f.get('CHAPTERS','')}] {f.get('CLAIM','')}")
        for f in parsed[m]["items"]["S"]:
            lines.append(f"{L}S{f['n']} [strength; ch {f.get('CHAPTERS','')}] {f.get('CLAIM','')}")
    system = (ROOT / "prompts" / "match.md").read_text(encoding="utf-8")
    user = "Editors: " + ", ".join(f"{letter[m]}" for m in models) + "\n\n" + "\n".join(lines)
    cache = d / f"consensus.match.{args.matcher}.txt"
    key = sha(system + user)[:16]
    if cache.exists() and not args.rematch and cache.read_text().startswith(f"#key {key}\n"):
        raw = cache.read_text().split("\n", 1)[1]
    else:
        raw = run_model(args.matcher, system, user, f"structural-match-{d.name}", "medium")
        cache.write_text(f"#key {key}\n{raw}", encoding="utf-8")

    by_label = {}
    for m in models:
        for f in parsed[m]["items"]["F"]:
            by_label[f"{letter[m]}{f['n']}"] = (m, f)
        for f in parsed[m]["items"]["S"]:
            by_label[f"{letter[m]}S{f['n']}"] = (m, f)
    groups = {"F": [], "S": []}
    for kind, ids in re.findall(r"^\s*([FS]):\s*(.+)$", raw, re.M):
        labs = [x for x in re.findall(r"[A-Z]S?\d+", ids) if x in by_label]
        if len({by_label[x][0] for x in labs}) >= 2:
            groups[kind].append(labs)

    # A broad finding the matcher placed in several groups merges them: the author
    # rules on one problem once, not on each pairing of it.
    for kind in ("F", "S"):
        merged = []
        for g in groups[kind]:
            hit = [m for m in merged if set(m) & set(g)]
            for m in hit:
                merged.remove(m)
            merged.append(sorted(set(g).union(*map(set, hit)), key=lambda x: (x[0], int(re.sub(r"\D", "", x)))))
        groups[kind] = merged

    sev_rank = {"major": 0, "moderate": 1, "minor": 2}
    def g_rank(g):
        sv = min(sev_rank.get(by_label[x][1].get("SEVERITY", "minor").lower(), 2) for x in g)
        return (-len({by_label[x][0] for x in g}), sv)
    groups["F"].sort(key=g_rank)

    first_last = None
    out = [f"# Structural consensus — {d.name}", "",
           f"*Letters: {', '.join(f'{letter[m]} = {m}' for m in models)}. Matcher: {args.matcher}. "
           f"A finding is listed when two or more editors raise it. Single-editor findings are "
           f"in the letters, not here. {date.today().isoformat()}.*", ""]
    out += ["## Findings raised by two or more editors", ""]
    for i, g in enumerate(groups["F"], 1):
        eds = sorted({by_label[x][0] for x in g})
        chs = sorted(set().union(*(chapters_of(by_label[x][1].get("CHAPTERS", "")) for x in g)))
        sev = "/".join(sorted({by_label[x][1].get("SEVERITY", "?").lower() for x in g}))
        out.append(f"### C{i}. {by_label[g[0]][1].get('CLAIM','')}")
        out.append(f"*{len(eds)} editors ({', '.join(letter[e] for e in eds)}) · severity {sev} · "
                   f"chapters {', '.join(map(str, chs)) if len(chs) < 25 else f'{chs[0]}–{chs[-1]}'}*")
        out.append("")
        for x in g:
            m, f = by_label[x]
            out.append(f"- **{x}** ({m}, {f.get('CATEGORY','')}): {f.get('CLAIM','')}  ")
            out.append(f"  Evidence: {f.get('EVIDENCE','')}  ")
            out.append(f"  Question: {f.get('QUESTION','')}")
        out.append("")
    out += ["## Strengths named by two or more editors", ""]
    for g in groups["S"]:
        out.append("- " + " · ".join(f"**{x}** ({by_label[x][0]}): {by_label[x][1].get('CLAIM','')}" for x in g))
    out += ["", "## Drag votes (chapter map)", "",
            "| ch | " + " | ".join(letter[m] for m in models) + " | votes |",
            "|---|" + "---|" * (len(models) + 1)]
    chs = sorted(set().union(*(parsed[m]["drag"].keys() for m in models)))
    for n in chs:
        v = [parsed[m]["drag"].get(n, "—") for m in models]
        k = sum(1 for x in v if x in ("some", "heavy"))
        cell = f"**{k}**" if k >= 2 else str(k)
        out.append(f"| {n} | " + " | ".join(v) + f" | {cell} |")
    (d / "consensus.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {(d / 'consensus.md').relative_to(REPO)}: {len(groups['F'])} shared findings, "
          f"{len(groups['S'])} shared strengths")


# --------------------------------------------------------------------- reconcile
def reconcile(args) -> None:
    """Stage 2: set the shared findings against the plan and prior rulings. Runs IN
    the repo (read-only) so the model can search meta/, triage and the metrics."""
    import subprocess as sp
    d = target_dir(args.volume, args.through)
    cons = d / "consensus.md"
    if not cons.exists():
        raise SystemExit(f"run consensus first ({cons.relative_to(REPO)})")
    system = (ROOT / "prompts" / "reconcile.md").read_text(encoding="utf-8")
    body = cons.read_text(encoding="utf-8")
    body = body.split("## Drag votes")[0]
    prompt = (system + "\n\n---\n\nVolume under review: " + d.name +
              ". The findings (with each editor's evidence and question):\n\n" + body)
    out = d / f"reconcile.{args.model}.md"
    if not args.model.startswith("gpt-"):
        raise SystemExit("reconcile runs on the codex lane (gpt-*) in the repo")
    print(f"[reconcile] {d.relative_to(REPO)} · {args.model} · read-only in repo", flush=True)
    r = sp.run(["codex", "exec", "-m", args.model, "-s", "read-only", "-C", str(REPO),
                "-c", f"model_reasoning_effort={args.effort}", "-o", str(out), "-"],
               input=prompt, capture_output=True, text=True, timeout=7200)
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"codex failed: {(r.stderr or r.stdout)[-800:]}")
    head = (f"*structural-reconcile-v1 · {d.name} · model {args.model} · consensus "
            f"{sha(body)[:12]} · prompt {sha(system)[:12]} · {date.today().isoformat()}*\n\n")
    out.write_text(head + out.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diagnose")
    d.add_argument("--volume", type=int, required=True)
    d.add_argument("--through", action="store_true")
    d.add_argument("--models", nargs="+", default=["gpt-5.6-sol", "claude-opus-5-5"])
    d.add_argument("--effort", default="high")
    d.add_argument("--fresh", action="store_true")
    d.add_argument("--paid", action="store_true",
                   help="allow OpenRouter lanes (author-authorized runs only)")
    d.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("consensus")
    c.add_argument("--volume", type=int, required=True)
    c.add_argument("--through", action="store_true")
    c.add_argument("--matcher", default="claude-opus-5-5")
    c.add_argument("--rematch", action="store_true", help="ignore the cached match")
    r = sub.add_parser("reconcile")
    r.add_argument("--volume", type=int, required=True)
    r.add_argument("--through", action="store_true")
    r.add_argument("--model", default="gpt-5.6-sol")
    r.add_argument("--effort", default="high")
    args = ap.parse_args()
    if args.cmd == "reconcile":
        reconcile(args)
    if args.cmd == "diagnose":
        diagnose(args)
    elif args.cmd == "consensus":
        consensus(args)


if __name__ == "__main__":
    main()
