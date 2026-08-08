# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""OpenAI cold-read harness, built on cold_read_batch.run_batch.

The direct API path keeps the existing dollar-capped Responses API behavior.
`--auth codex` reuses a ChatGPT subscription session created by the official
Codex CLI (`codex login`).

Subscription calls have no API dollar price or SDK-supported per-turn output
cap. They record cost as `null`; subscription rate/quota enforcement remains
with Codex. They run in an empty temporary working directory with a read-only
sandbox: the blind reader receives only its supplied prompt and cannot inspect
this repo.
RUN (never pip — uv resolves the deps in the header above):
  OPENAI_API_KEY=... uv run tools/cold_read_openai.py --model gpt-5.5 --scope fall
  codex login
  uv run tools/cold_read_openai.py --auth codex --model gpt-5.6-terra --scope the-bench
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
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


def load_pricing(model: str, price_in, price_out, max_output_tokens=None) -> dict | None:
    """Pricing for the direct API dollar guard, if known.

    A direct API run without published pricing is permitted only with an
    explicit output-token cap. Codex subscription runs never call this helper.
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
            return None
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
def make_codex_agent_fn(*, system_prompt, effort):
    """Return a subscription-backed agent function and its resource cleanup.

    The official Codex CLI owns credential persistence, refresh, and
    subscription quota enforcement. An empty cwd plus a read-only sandbox
    protects the blind-reader boundary even though the harness runs from the
    novel repository.
    """
    from openai_codex import Codex, Sandbox

    codex = Codex()
    workdir = tempfile.TemporaryDirectory(prefix="cold-reader-codex-")
    account = codex.account(refresh_token=True)
    if not getattr(account, "account", None):
        codex.close()
        workdir.cleanup()
        raise SystemExit("No reusable Codex OAuth session. Run `codex login` first.")

    def agent_fn(*, prompt, model, label):
        thread = codex.thread_start(
            cwd=workdir.name,
            developer_instructions=system_prompt,
            model=model,
            sandbox=Sandbox.read_only,
        )
        t0 = time.time()
        result = thread.run(
            prompt,
            cwd=workdir.name,
            effort=None if effort == "none" else effort,
            model=model,
            sandbox=Sandbox.read_only,
        )
        duration_ms = (time.time() - t0) * 1000.0
        if result.error:
            raise RuntimeError(f"Codex turn failed: {result.error}")
        text = result.final_response or ""
        token_usage = getattr(result, "usage", None)
        total = getattr(token_usage, "total", token_usage)
        in_tok = getattr(total, "input_tokens", 0) or 0
        out_tok = getattr(total, "output_tokens", 0) or 0
        reasoning_tok = getattr(total, "reasoning_output_tokens", 0) or 0
        total_tok = getattr(total, "total_tokens", 0) or (in_tok + out_tok)
        usage = {
            "input": in_tok,
            "output": out_tok,
            "reasoningTokens": reasoning_tok,
            "totalTokens": total_tok,
            "cacheRead": getattr(total, "cached_input_tokens", 0) or 0,
            "max_output_tokens": None,
            "promptTokens": in_tok,
            "nonMessageTokens": 0,
            "cost": None,
            "duration_ms": getattr(result, "duration_ms", None) or duration_ms,
            "turns": 1,
            "incomplete": getattr(result, "status", None) == "incomplete",
        }
        return {"output": text, "id": getattr(result, "id", None) or label, "usage": usage}

    def close():
        try:
            codex.close()
        finally:
            workdir.cleanup()

    return agent_fn, close


def main():
    ap = argparse.ArgumentParser(description="OpenAI cold-read harness.")
    ap.add_argument(
        "--auth",
        choices=["api-key", "codex"],
        default="api-key",
        help="authentication backend (default: api-key)",
    )
    ap.add_argument("--model", required=True, help="model id accepted by the selected backend")
    ap.add_argument("--model-id", default=None, help="output dir under reviews/cold-read/ (default: --model)")
    ap.add_argument("--scope", default="fall", help="'fall' | <slug> | <a>..<b> | <a>.. | ..<b>")
    ap.add_argument(
        "--budget-usd",
        type=float,
        default=None,
        help="hard per-scene API budget (default: $2.00 in --auth api-key mode)",
    )
    ap.add_argument("--effort", default="low", choices=["none", "minimal", "low", "medium", "high"],
                    help="reasoning effort (default low; high turns the reader into a critic)")
    ap.add_argument("--timeout", type=float, default=600.0, help="per-call direct API request timeout, seconds")
    ap.add_argument("--max-attempts", type=int, default=3,
                    help="attempts per scene (default 3). A retry appends a FORMAT REMINDER, "
                    "which self-heals the occasional missing-section response.")
    ap.add_argument("--fresh", action="store_true", help="regenerate existing reviews (default: resume/skip)")
    ap.add_argument("--price-in", type=float, default=None, help="override API input price (USD/1M tokens)")
    ap.add_argument("--price-out", type=float, default=None, help="override API output price (USD/1M tokens)")
    ap.add_argument("--max-output-tokens", type=int, default=None,
                    help="hard direct-API per-call output+reasoning cap; not supported by Codex subscription mode.")
    ap.add_argument(
        "--allow-volume-one-rewrite",
        action="store_true",
        help="the new carry-forward spec is now the default for all runs; this flag "
             "opts in to a --fresh run REGENERATING existing (Volume One) reviews under "
             "it. Without it, --fresh refuses if the scope would overwrite any review "
             "already on disk.",
    )
    args = ap.parse_args()

    if args.auth == "api-key":
        if not os.environ.get("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY not set in the environment.")
        budget_usd = args.budget_usd if args.budget_usd is not None else 2.0
        pricing = load_pricing(args.model, args.price_in, args.price_out, args.max_output_tokens)
    else:
        if args.price_in is not None or args.price_out is not None:
            raise SystemExit("--price-in/--price-out apply only to --auth api-key.")
        if args.budget_usd is not None:
            raise SystemExit("--budget-usd applies only to --auth api-key; subscription cost is unavailable.")
        if args.max_output_tokens is not None:
            raise SystemExit(
                "--max-output-tokens is not supported by the Codex SDK; "
                "subscription rate and quota limits are enforced by Codex."
            )
        budget_usd = None
        pricing = None

    model_id = args.model_id or args.model
    system_prompt = load_system_prompt()
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
    close = None
    if args.auth == "api-key":
        agent_fn = make_agent_fn(
            system_prompt=system_prompt,
            pricing=pricing,
            effort=args.effort,
            budget_usd=budget_usd,
            max_output_tokens=args.max_output_tokens,
            timeout=args.timeout,
        )
    else:
        agent_fn, close = make_codex_agent_fn(
            system_prompt=system_prompt,
            effort=args.effort,
        )

    print(
        f"[cold_read_openai] auth={args.auth} model={args.model} id={model_id} "
        f"scenes={len(scenes)} effort={args.effort} "
        + (
            f"budget=${budget_usd:.2f}/scene "
            + (f"price in=${pricing['input']}/1M out=${pricing['output']}/1M "
               if pricing else f"UNPRICED (token-guarded, cap={args.max_output_tokens}) ")
            if args.auth == "api-key"
            else "subscription (rate/quota limited by Codex, cost=unavailable) "
        )
        + f"resume={not args.fresh} max_attempts={args.max_attempts}",
        flush=True,
    )
    try:
        run_batch(
            agent_fn=agent_fn,
            model_selector=args.model,
            model_id=model_id,
            scenes=scenes,
            resume=not args.fresh,
            max_attempts=args.max_attempts,
            budget_usd=budget_usd,
            provider_label="OpenAI API" if args.auth == "api-key" else "Codex subscription",
        )
    finally:
        if close:
            close()


if __name__ == "__main__":
    main()
