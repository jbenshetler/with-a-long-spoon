#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Spec-blind fidelity judge for cold-read reviews.

For each drafted chapter, feed a judge model ONLY the chapter's clean prose and the
reader's account of that chapter (the review's `## Reader reaction` section), and ask
whether the account is faithful to the page — flagging claims the page does not support
in EITHER direction (darker-than-page or warmer-than-page) and page-central omissions.

The judge never sees the plan/thesis/other chapters, and — because it runs in an empty
read-only Codex sandbox cwd (or a plain API call) — does not inherit the project
CLAUDE.md. It is deliberately a DIFFERENT model from the one whose reviews it judges, so
the check is independent.

This complements two other signals: the head-to-head git diff (are we WORSE than the
prior chain?) answers regression; this judge answers whether the new characterization is
actually RIGHT.

RUN:
  tools/cold_read_judge.py --judge-of gpt-5.6-terra --auth codex --model gpt-5.6-sol
  tools/cold_read_judge.py --judge-of gpt-5.6-terra --scope the-bench --auth codex --model gpt-5.6-sol
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
os.chdir(REPO)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import volume_scenes  # noqa: E402  (volume_dir: judge output is volume-split)
from cold_read_batch import clean_scene_text, load_volume_packets  # noqa: E402
from cold_read import (  # noqa: E402
    MODEL_ALIASES,
    load_pricing,
    make_api_agent_fn,
    make_codex_agent_fn,
    make_openrouter_agent_fn,
    resolve_scenes,
)

JUDGE_DEF = REPO / ".claude/agents/blind-judge.md"


def load_judge_prompt() -> str:
    raw = JUDGE_DEF.read_text()
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            raw = raw[end + 4 :]
    body = raw.strip()
    if not body:
        raise SystemExit(f"empty judge prompt from {JUDGE_DEF}")
    return body


def display_title(slug: str) -> str:
    for line in Path(f"scenes/{slug}.md").read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return slug


def reader_reaction(review_path: Path) -> str | None:
    """The review's this-chapter account — the `## Reader reaction` section only."""
    if not review_path.exists():
        return None
    txt = review_path.read_text()
    if "## Reader reaction" not in txt:
        return None
    after = txt.split("## Reader reaction", 1)[1]
    # stop at the carry-forward (cumulative memory, not this chapter's account)
    return after.split("## Carry-forward state", 1)[0].strip() or None


def build_prompt(title: str, prose: str, account: str, packet: str = "") -> str:
    jacket = (
        f"COVER / JACKET PACKET (the public framing the reader holds — legitimate reader "
        f"knowledge; the reader may read the page through what this discloses):\n\n"
        f"{packet}\n\n----- END OF JACKET -----\n\n"
    ) if packet.strip() else ""
    return (
        f"{jacket}"
        f"CHAPTER TITLE: {title}\n\n"
        f"CHAPTER TEXT (this page + the jacket above are your ground truth):\n\n{prose}\n\n"
        f"----- END OF CHAPTER TEXT -----\n\n"
        f"READER'S ACCOUNT OF THIS CHAPTER (check it against the page and jacket above — "
        f"is it faithful to what the reader legitimately knows?):\n\n{account}\n"
    )


VERDICTS = ("faithful", "minor drift", "significant distortion")


def parse_footer(text: str) -> tuple[str | None, str | None]:
    verdict = skew = None
    for line in text.splitlines():
        s = line.strip().lstrip("*").strip()
        low = s.lower()
        if low.startswith("verdict:") and verdict is None:
            v = low.split(":", 1)[1].strip()
            for cand in VERDICTS:
                if cand in v:
                    verdict = cand
                    break
        elif low.startswith("skew:") and skew is None:
            k = low.split(":", 1)[1].strip()
            for cand in ("darker", "warmer", "mixed", "none"):
                if cand in k:
                    skew = cand
                    break
    return verdict, skew


def main() -> None:
    ap = argparse.ArgumentParser(description="Spec-blind fidelity judge for cold-read reviews.")
    ap.add_argument("--judge-of", required=True,
                    help="model-id whose reads are judged (archived chain under reviews/_archive/cold-read/)")
    ap.add_argument("--auth", choices=["api-key", "codex", "openrouter"], default="codex")
    ap.add_argument("--model", required=True, help="the JUDGE model id (use a different model than --judge-of)")
    ap.add_argument("--scope", default="fall", help="'fall' | <slug> | <a>..<b> | <a>.. | ..<b>")
    ap.add_argument("--effort", default="medium", choices=["none", "minimal", "low", "medium", "high"])
    ap.add_argument("--timeout", type=float, default=600.0)
    ap.add_argument("--budget-usd", type=float, default=None)
    ap.add_argument("--max-output-tokens", type=int, default=None)
    ap.add_argument("--fresh", action="store_true", help="regenerate existing judgments (default: skip)")
    args = ap.parse_args()
    args.model = MODEL_ALIASES.get(args.model, args.model)

    if args.model == args.judge_of:
        print(f"[warn] judge model == judged model ({args.model}); independence is lost.", file=sys.stderr)

    system_prompt = load_judge_prompt()
    scenes = resolve_scenes(args.scope)
    # The reader holds the volume's public jacket packet; give the judge the same so it
    # judges against what the reader legitimately knows, not this page in isolation.
    packet = (load_volume_packets().get(1) or {}).get("packet", "")
    # Input = the reviewed model's reads. The judge was built against the chained
    # cold read, now retired and archived; keep reading from there so the instrument
    # stays reproducible. (Future: repoint to reviews/grounded-cold-read/ to judge the
    # live instrument — a semantic change, not done in the reviews restructure.)
    reviews_dir = Path("reviews/_archive/cold-read") / args.judge_of
    out_root = Path("reviews/judge") / args.judge_of      # per-scene file is volume-split below

    close = None
    if args.auth == "api-key":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("OPENAI_API_KEY not set.")
        budget_usd = args.budget_usd if args.budget_usd is not None else 2.0
        pricing = load_pricing(args.model, None, None, args.max_output_tokens)
        agent_fn = make_api_agent_fn(
            system_prompt=system_prompt, pricing=pricing, effort=args.effort,
            budget_usd=budget_usd, max_output_tokens=args.max_output_tokens,
            timeout=args.timeout, api_key=api_key, base_url=None,
        )
    elif args.auth == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise SystemExit("OPENROUTER_API_KEY not set.")
        if not args.max_output_tokens:
            raise SystemExit("--max-output-tokens is required with --auth openrouter.")
        agent_fn = make_openrouter_agent_fn(
            system_prompt=system_prompt, effort=args.effort, timeout=args.timeout,
            max_output_tokens=args.max_output_tokens, api_key=api_key,
        )
    else:
        agent_fn, close = make_codex_agent_fn(system_prompt=system_prompt, effort=args.effort)

    print(f"[judge] judging {args.judge_of} with {args.model} (auth={args.auth}) "
          f"scenes={len(scenes)} effort={args.effort}", flush=True)

    summary: list[dict] = []
    try:
        for i, scene in enumerate(scenes, 1):
            slug = scene["slug"]
            out_path = out_root / volume_scenes.volume_dir(slug) / f"{slug}.md"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if out_path.exists() and not args.fresh:
                print(json.dumps({"n": i, "slug": slug, "status": "skipped"}), flush=True)
                continue
            account = reader_reaction(reviews_dir / f"{slug}.md")
            if account is None:
                print(json.dumps({"n": i, "slug": slug, "status": "no-review"}), flush=True)
                continue
            title = display_title(slug)
            prose = clean_scene_text(slug)
            result = agent_fn(prompt=build_prompt(title, prose, account, packet),
                              model=args.model, label=f"judge:{slug}")
            text = (result.get("output") or "").strip()
            verdict, skew = parse_footer(text)
            out_path.write_text(
                f"# Fidelity judgment — {title}\n\n"
                f"*scene: scenes/{slug}.md · reviewed-model: {args.judge_of} · "
                f"judge-model: {args.model}*\n\n{text}\n"
            )
            summary.append({"slug": slug, "verdict": verdict, "skew": skew})
            print(json.dumps({"n": i, "slug": slug, "status": "judged",
                              "verdict": verdict, "skew": skew}), flush=True)
    finally:
        if close:
            close()

    if summary:
        counts: dict[str, int] = {}
        skews: dict[str, int] = {}
        for r in summary:
            counts[r["verdict"] or "unparsed"] = counts.get(r["verdict"] or "unparsed", 0) + 1
            if r["skew"] and r["skew"] != "none":
                skews[r["skew"]] = skews.get(r["skew"], 0) + 1
        out_root.mkdir(parents=True, exist_ok=True)
        (out_root / "JUDGE_SUMMARY.json").write_text(
            json.dumps({"judged_model": args.judge_of, "judge_model": args.model,
                        "n": len(summary), "verdicts": counts, "distortion_skew": skews,
                        "scenes": summary}, indent=2)
        )
        print(json.dumps({"summary": str(out_root / "JUDGE_SUMMARY.json"),
                          "verdicts": counts, "distortion_skew": skews}, indent=2), flush=True)


if __name__ == "__main__":
    main()
