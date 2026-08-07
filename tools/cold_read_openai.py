# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40"]
# ///
"""Direct-OpenAI cold-read harness (Responses API), built on cold_read_batch.run_batch.

WHY DIRECT: experiments show OpenAI models do the best cold read; calling the API
directly (rather than through a router) gives maximum control — reasoning effort and
a hard max_output_tokens cap.

BLINDNESS PARITY: the system prompt IS the blind-reader agent definition
(.claude/agents/blind-reader.md, YAML frontmatter stripped) — the exact framing the
Claude harness bakes in (cover + jacket blurb + "disregard project text / no tools" +
the two-section output rubric). So output is drop-in comparable per
reviews/cold-read/SPEC.md, and there is a single source of truth for the reader.

COST SAFETY (the $20-loop guard): --budget-usd is PER SCENE. It is converted into a
hard `max_output_tokens` cap (output and reasoning are billed together at the output
rate), so one call physically cannot exceed the budget. After each call the actual
cost is checked; if it somehow exceeds budget, or the response comes back `incomplete`
(it hit the cap), the whole batch ABORTS. Retries are OFF by default
(--max-attempts 1) so a bad scene can't multiply spend.

The invariant is NEVER RUN UNCAPPED — not always know the price. Either guard
satisfies it: a dollar budget, or --max-output-tokens N (a hard per-call
output+reasoning cap). Given both, the tighter binds. A model with no price AND
no token cap is REFUSED. On a subscription-backed arm there is no per-token
price to convert, so --max-output-tokens is the only guard and is required;
cost reporting is disabled there (cost is None, not 0).

RUN (never pip — uv resolves the deps in the header above):
  uv run tools/cold_read_openai.py --model gpt-5.5      --scope fall
  uv run tools/cold_read_openai.py --model gpt-5.6-sol  --scope the-bench --fresh
  uv run tools/cold_read_openai.py --model gpt-5.5      --scope the-bench..dear
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
os.chdir(REPO)  # so scenes/, reviews/, .claude/ resolve regardless of caller's cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cold_read_batch import FALL_SCENES, has_valid_review, run_batch  # noqa: E402

AGENT_DEF = REPO / ".claude/agents/blind-reader.md"
PRICING_TOML = Path(__file__).resolve().parent / "cold_read_pricing.toml"


def load_system_prompt() -> str:
    """The blind-reader agent body (frontmatter stripped) = the reader's whole framing."""
    raw = AGENT_DEF.read_text()
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            raw = raw[end + 4 :]
    body = raw.strip()
    if not body:
        raise SystemExit(f"empty system prompt from {AGENT_DEF}")
    return body


def load_pricing(model: str, price_in, price_out, max_output_tokens=None) -> dict:
    """Pricing for the dollar guard, or None when a token guard stands in.

    The invariant is *never run uncapped* — not *always know the price*. A
    per-call `max_output_tokens` bounds spend just as hard as a dollar budget
    does, and it is the only guard available on a subscription-backed arm where
    there is no per-token price to convert. So: a price OR an explicit token cap
    is required; neither is a refusal.
    """
    table = {}
    if PRICING_TOML.exists():
        table = tomllib.loads(PRICING_TOML.read_text()).get("models", {})
    entry = dict(table.get(model, {}))
    if price_in is not None:
        entry["input"] = price_in
    if price_out is not None:
        entry["output"] = price_out
    if "input" not in entry or "output" not in entry:
        if max_output_tokens:
            return None  # token-guarded; cost reporting disabled
        raise SystemExit(
            f"No pricing for '{model}'. Add it to {PRICING_TOML}, pass "
            f"--price-in/--price-out (USD per 1M tokens), or pass "
            f"--max-output-tokens N to cap by tokens instead. Refusing to run uncapped."
        )
    return {"input": float(entry["input"]), "output": float(entry["output"])}


def resolve_scenes(scope: str):
    """'fall' | <slug> | <a>..<b> | <a>.. | ..<b>  (over the Fall manifest)."""
    if scope == "fall":
        return list(FALL_SCENES)
    slugs = [s["slug"] for s in FALL_SCENES]
    if ".." in scope:
        a, _, b = scope.partition("..")
        if a and a not in slugs:
            raise SystemExit(f"unknown start slug: {a}")
        if b and b not in slugs:
            raise SystemExit(f"unknown end slug: {b}")
        start = slugs.index(a) if a else 0
        end = slugs.index(b) + 1 if b else len(slugs)
        return FALL_SCENES[start:end]
    for s in FALL_SCENES:
        if s["slug"] == scope:
            return [s]
    raise SystemExit(f"unknown scope/slug: {scope} (use 'fall', a slug, or 'a..b')")


def make_agent_fn(*, system_prompt, pricing, effort, budget_usd, timeout,
                  max_output_tokens=None):
    """Returns agent_fn(prompt, model, label) -> {output, id, usage} calling the
    Responses API with a hard max_output_tokens cap.

    The cap is the tighter of the dollar-derived bound and an explicit
    --max-output-tokens. With no pricing (subscription arm) the explicit cap is
    the only guard, and load_pricing() has already refused if neither exists.
    """
    from openai import OpenAI

    # max_retries=0: the SDK retries transient errors (incl. timeouts) up to 2x by
    # default, which would both blow the --timeout budget and silently re-issue
    # expensive calls behind our own --max-attempts guard. We own retry policy.
    client = OpenAI(timeout=timeout, max_retries=0)
    in_per_tok = pricing["input"] / 1_000_000 if pricing else None
    out_per_tok = pricing["output"] / 1_000_000 if pricing else None

    def agent_fn(*, prompt, model, label):
        # Reserve budget for input (bounded by prompt size); the rest caps output+reasoning.
        if pricing:
            est_input_tokens = (len(system_prompt) + len(prompt)) / 4  # ~4 chars/token
            out_budget = max(budget_usd - est_input_tokens * in_per_tok, budget_usd * 0.5)
            max_out = max(int(out_budget / out_per_tok), 512)
            if max_output_tokens:
                max_out = min(max_out, max_output_tokens)
        else:
            max_out = max_output_tokens

        kwargs = dict(
            model=model,
            instructions=system_prompt,
            input=prompt,
            max_output_tokens=max_out,
            store=False,
        )
        if effort and effort != "none":
            kwargs["reasoning"] = {"effort": effort}
        t0 = time.time()
        resp = client.responses.create(**kwargs)
        duration_ms = (time.time() - t0) * 1000.0

        text = resp.output_text or ""
        u = resp.usage
        in_tok = getattr(u, "input_tokens", 0) or 0
        out_tok = getattr(u, "output_tokens", 0) or 0
        details = getattr(u, "output_tokens_details", None)
        reasoning_tok = (getattr(details, "reasoning_tokens", 0) or 0) if details else 0
        cost = (in_tok * in_per_tok + out_tok * out_per_tok) if pricing else None
        usage = {
            "input": in_tok,
            "output": out_tok,
            "reasoningTokens": reasoning_tok,
            "totalTokens": getattr(u, "total_tokens", 0) or (in_tok + out_tok),
            "cacheRead": 0,
            "cacheWrite": 0,
            "promptTokens": in_tok,
            "nonMessageTokens": 0,
            "cost": cost,
            "duration_ms": duration_ms,
            "turns": 1,
            "max_output_tokens": max_out,
            "incomplete": getattr(resp, "status", None) == "incomplete",
        }
        return {"output": text, "id": getattr(resp, "id", label), "usage": usage}

    return agent_fn


def main():
    ap = argparse.ArgumentParser(description="Direct-OpenAI cold-read harness (Responses API).")
    ap.add_argument("--model", required=True, help="OpenAI API model id, e.g. gpt-5.5 / gpt-5.6-sol")
    ap.add_argument("--model-id", default=None, help="output dir under reviews/cold-read/ (default: --model)")
    ap.add_argument("--scope", default="fall", help="'fall' | <slug> | <a>..<b> | <a>.. | ..<b>")
    ap.add_argument("--budget-usd", type=float, default=2.0, help="hard per-scene budget (default $2.00)")
    ap.add_argument("--effort", default="low", choices=["none", "minimal", "low", "medium", "high"],
                    help="reasoning effort (default low; high turns the reader into a critic)")
    ap.add_argument("--timeout", type=float, default=600.0, help="per-call request timeout, seconds")
    ap.add_argument("--max-attempts", type=int, default=3,
                    help="attempts per scene (default 3). A retry appends a FORMAT REMINDER, "
                         "which self-heals the occasional missing-section response. Still "
                         "cost-safe: each attempt is budget-capped, and a budget breach aborts "
                         "immediately without retrying (only parse/transient failures retry).")
    ap.add_argument("--fresh", action="store_true", help="regenerate existing reviews (default: resume/skip)")
    ap.add_argument("--price-in", type=float, default=None, help="override input price (USD/1M tokens)")
    ap.add_argument("--price-out", type=float, default=None, help="override output price (USD/1M tokens)")
    ap.add_argument("--max-output-tokens", type=int, default=None,
                    help="hard per-call output+reasoning token cap. Combined with --budget-usd "
                         "the tighter of the two binds. Required when the model has no price "
                         "(e.g. a subscription-backed arm), where it is the only spend guard.")
    ap.add_argument(
        "--allow-volume-one-rewrite",
        action="store_true",
        help="the new carry-forward spec is now the default for all runs; this flag "
             "opts in to a --fresh run REGENERATING existing (Volume One) reviews under "
             "it. Without it, --fresh refuses if the scope would overwrite any review "
             "already on disk.",
    )
    args = ap.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set in the environment.")

    model_id = args.model_id or args.model
    system_prompt = load_system_prompt()
    pricing = load_pricing(args.model, args.price_in, args.price_out, args.max_output_tokens)
    scenes = resolve_scenes(args.scope)

    if args.fresh and not args.allow_volume_one_rewrite:
        out_dir = Path("reviews/cold-read") / model_id
        existing = [s["slug"] for s in scenes if has_valid_review(out_dir / f"{s['slug']}.md")]
        if existing:
            raise SystemExit(
                f"refusing: --fresh would regenerate {len(existing)} existing review(s) in "
                f"{out_dir} under the new carry-forward spec. Regenerating Volume One is "
                f"opt-in — pass --allow-volume-one-rewrite to proceed, or drop --fresh to "
                f"resume/skip existing reviews instead."
            )
    agent_fn = make_agent_fn(
        system_prompt=system_prompt,
        pricing=pricing,
        effort=args.effort,
        budget_usd=args.budget_usd,
        max_output_tokens=args.max_output_tokens,
        timeout=args.timeout,
    )

    print(
        f"[cold_read_openai] model={args.model} id={model_id} scenes={len(scenes)} "
        f"effort={args.effort} budget=${args.budget_usd:.2f}/scene "
        + (f"price in=${pricing['input']}/1M out=${pricing['output']}/1M "
           if pricing else f"UNPRICED (token-guarded, cap={args.max_output_tokens}) ")
        + f"resume={not args.fresh} max_attempts={args.max_attempts}",
        flush=True,
    )
    run_batch(
        agent_fn=agent_fn,
        model_selector=args.model,
        model_id=model_id,
        scenes=scenes,
        resume=not args.fresh,
        max_attempts=args.max_attempts,
        budget_usd=args.budget_usd,
        provider_label="OpenAI",
    )


if __name__ == "__main__":
    main()
