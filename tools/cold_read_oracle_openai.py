# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40"]
# ///
"""Direct-OpenAI cold-read ORACLE harness (Responses API).

Interrogates a FROZEN cold-read reader (the oracle, per reviews/cold-read/ORACLE.md):
it pauses the reader at a stage and asks the fixed battery, tiered funnel
(neutral, then a FRESH pointed call), to measure what a genuine first reader knows
and feels there — without leaking design.

PARITY: system prompt is reviews/cold-read/oracle-persona.md (the model-agnostic
persona + jacket every harness must send verbatim), followed by the stage's frozen
`## Carry-forward state` and one probe/tier per call. Questions come verbatim from the
shared battery reviews/cold-read/oracle-battery.json. So output is drop-in comparable
with the Claude oracle and any other external harness.

BLINDNESS: the Responses call passes NO tools, so the reader can reach nothing beyond
the prompt — the tool-free guarantee ORACLE.md requires (equivalent to the Claude
harness's tool_uses:0 tripwire). Read-only: writes ONLY under
reviews/cold-read/<model>/oracle/, never scenes/, meta/, or the cold-read chain files.

COST SAFETY: --budget-usd is PER CALL, converted to a hard max_output_tokens cap
(output+reasoning billed together), so a call cannot exceed budget. A model with no
price (cold_read_pricing.toml or --price-*) is REFUSED rather than run uncapped.

RUN (never pip — uv resolves the header deps):
  uv run tools/cold_read_oracle_openai.py --model gpt-5.6-sol --stage nothing-underneath \
      --probe pace-backstory,sympathy,randi-love,randi-suspicion
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
os.chdir(REPO)

PERSONA = REPO / "reviews/cold-read/oracle-persona.md"
BATTERY = REPO / "reviews/cold-read/oracle-battery.json"
PRICING_TOML = Path(__file__).resolve().parent / "cold_read_pricing.toml"


def load_persona() -> str:
    """Persona proper = the text AFTER the first `---` divider (the part before it is
    harness-author instructions, not the reader's system prompt)."""
    raw = PERSONA.read_text()
    idx = raw.find("\n---")
    body = raw[idx + 4 :] if idx != -1 else raw
    body = body.strip()
    if not body:
        raise SystemExit(f"empty persona from {PERSONA}")
    return body


def load_pricing(model, price_in, price_out) -> dict:
    table = {}
    if PRICING_TOML.exists():
        table = tomllib.loads(PRICING_TOML.read_text()).get("models", {})
    entry = dict(table.get(model, {}))
    if price_in is not None:
        entry["input"] = price_in
    if price_out is not None:
        entry["output"] = price_out
    if "input" not in entry or "output" not in entry:
        raise SystemExit(
            f"No pricing for '{model}'. Add it to {PRICING_TOML} or pass "
            f"--price-in/--price-out (USD per 1M tokens). Refusing to run uncapped."
        )
    return {"input": float(entry["input"]), "output": float(entry["output"])}


def load_carryforward(model_id: str, stage: str) -> str:
    f = REPO / "reviews/cold-read" / model_id / f"{stage}.md"
    if not f.exists():
        raise SystemExit(
            f"no cold-read file for stage '{stage}' in {f.parent} — the reader-state "
            f"can't be fabricated. Run the cold read to that stage first."
        )
    txt = f.read_text()
    if "## Carry-forward state" not in txt:
        raise SystemExit(f"{f} has no `## Carry-forward state` section.")
    carry = txt.split("## Carry-forward state", 1)[1].strip()
    if not carry:
        raise SystemExit(f"{f} has an empty carry-forward.")
    return carry


def make_call_fn(*, persona, pricing, effort, budget_usd, timeout, model):
    from openai import OpenAI

    client = OpenAI(timeout=timeout, max_retries=0)  # we own retry policy
    in_per_tok = pricing["input"] / 1_000_000
    out_per_tok = pricing["output"] / 1_000_000

    def call(prompt: str) -> dict:
        est_input_tokens = (len(persona) + len(prompt)) / 4
        out_budget = max(budget_usd - est_input_tokens * in_per_tok, budget_usd * 0.5)
        max_out = max(int(out_budget / out_per_tok), 512)
        kwargs = dict(
            model=model,
            instructions=persona,  # persona + jacket = system prompt
            input=prompt,          # carry-forward + one probe/tier
            max_output_tokens=max_out,
            store=False,
            # NO tools passed -> tool-free / no retrieval (blindness guarantee)
        )
        if effort and effort != "none":
            kwargs["reasoning"] = {"effort": effort}
        t0 = time.time()
        resp = client.responses.create(**kwargs)
        duration_ms = (time.time() - t0) * 1000.0
        u = resp.usage
        in_tok = getattr(u, "input_tokens", 0) or 0
        out_tok = getattr(u, "output_tokens", 0) or 0
        cost = in_tok * in_per_tok + out_tok * out_per_tok
        incomplete = getattr(resp, "status", None) == "incomplete"
        if incomplete:
            raise RuntimeError("response incomplete (hit the output cap) — raise --budget-usd")
        if budget_usd is not None and cost > budget_usd:
            raise RuntimeError(f"over budget: ${cost:.4f} > ${budget_usd:.2f}")
        return {"text": (resp.output_text or "").strip(), "cost": cost,
                "input": in_tok, "output": out_tok, "duration_ms": duration_ms}

    return call


def write_probe(model_id, stage, probe, defn, neutral, pointed):
    out_dir = REPO / "reviews/cold-read" / model_id / "oracle"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{stage}--{probe}.md"
    body = (
        f"# Oracle — {probe}\n\n"
        f"*stage: after `{stage}` · model: {model_id} · probe: {probe} · "
        f"tiered funnel (neutral → pointed, separate calls, tool-free)*\n\n"
        f"## Neutral\n\n"
        f"**Q:** \"{defn['neutral']}\"\n\n"
        f"**A:** {neutral}\n\n"
        f"## Pointed\n\n"
        f"**Q:** \"{defn['pointed']}\"\n\n"
        f"**A:** {pointed}\n"
    )
    path.write_text(body)
    return path


def main():
    ap = argparse.ArgumentParser(description="Direct-OpenAI cold-read oracle (Responses API).")
    ap.add_argument("--model", required=True, help="OpenAI API model id, e.g. gpt-5.6-sol")
    ap.add_argument("--model-id", default=None, help="dir under reviews/cold-read/ (default: --model)")
    ap.add_argument("--stage", required=True, help="stage slug (the reader after that scene)")
    ap.add_argument("--probe", required=True, help="comma-separated battery probe keys")
    ap.add_argument("--budget-usd", type=float, default=0.75, help="hard per-call budget (default $0.75)")
    ap.add_argument("--effort", default="low", choices=["none", "minimal", "low", "medium", "high"])
    ap.add_argument("--timeout", type=float, default=600.0)
    ap.add_argument("--price-in", type=float, default=None)
    ap.add_argument("--price-out", type=float, default=None)
    args = ap.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set in the environment.")

    model_id = args.model_id or args.model
    persona = load_persona()
    pricing = load_pricing(args.model, args.price_in, args.price_out)
    battery = json.loads(BATTERY.read_text())["probes"]
    probes = [p.strip() for p in args.probe.split(",") if p.strip()]
    unknown = [p for p in probes if p not in battery]
    if unknown:
        raise SystemExit(f"unknown probe(s): {unknown}. Valid: {sorted(battery)}")

    carry = load_carryforward(model_id, args.stage)
    call = make_call_fn(persona=persona, pricing=pricing, effort=args.effort,
                        budget_usd=args.budget_usd, timeout=args.timeout, model=args.model)

    print(f"[oracle] model={args.model} stage={args.stage} probes={probes} "
          f"effort={args.effort} budget=${args.budget_usd:.2f}/call", flush=True)

    total = 0.0
    for probe in probes:
        defn = battery[probe]
        # Neutral, then a FRESH pointed call (fresh context = no priming carried over):
        # each call is independent; carry-forward is identical, only the question differs.
        n = call(f"{carry}\n\n{defn['neutral']}")
        p = call(f"{carry}\n\n{defn['pointed']}")
        path = write_probe(model_id, args.stage, probe, defn, n["text"], p["text"])
        total += n["cost"] + p["cost"]
        print(json.dumps({"probe": probe, "path": str(path),
                          "cost": round(n["cost"] + p["cost"], 6),
                          "neutral_out": n["output"], "pointed_out": p["output"]}), flush=True)
    print(json.dumps({"stage": args.stage, "probes": len(probes),
                      "total_cost": round(total, 6)}), flush=True)


if __name__ == "__main__":
    main()
