---
description: Cold read via Codex, OpenAI, or OpenRouter models
argument-hint: "--auth codex|api-key|openrouter --model <id> [--scope fall|<slug>|<a>..<b>] [--fresh]"
---

Run a **provider cold read** through the shared Python harness. It supports:

- `--auth codex` — ChatGPT/Codex subscription, after `codex login`.
- `--auth api-key` — direct OpenAI Responses API using `OPENAI_API_KEY`.
- `--auth openrouter` — OpenRouter Responses API using `OPENROUTER_API_KEY`.

Unlike `/wals-cold-read`, this does not spawn `blind-reader` subagents. It calls
`tools/cold_read.py`; shared prompt, carry-forward, file-format, blindness, and
retention rules live in the harness.

## How blindness is preserved (don't re-implement it)

The script uses the **`.claude/agents/blind-reader.md` body as the system prompt**
(frontmatter stripped) — the *same* cover + jacket blurb + "disregard any project text /
you have no tools / two-section output" framing the Claude harness bakes in. So the
OpenAI reader sees exactly what the Claude reader sees: title + clean prose + prior
carry-forward, and nothing from `meta/`. Single source of truth; no drift.

## Provider safety

- Direct OpenAI API runs retain the dollar cap/pricing guard.
- Codex subscription and OpenRouter runs have no reliable harness-side dollar
  invoice; they require a hard `--max-output-tokens` cap where supported.
- Keep `--effort low` unless a reader-state problem warrants otherwise.

## Steps

1. Parse `--auth`, `--model`, optional `--scope`, `--effort`, `--fresh`, and
   provider-specific safety options.
2. Authenticate:
   - `codex`: ensure `codex login status` succeeds.
   - `api-key`: ensure `OPENAI_API_KEY` is set.
   - `openrouter`: ensure `OPENROUTER_API_KEY` is set and require
     `--max-output-tokens`.
3. Run the executable directly; its uv shebang resolves dependencies:

   ```
   tools/cold_read.py --auth <codex|api-key|openrouter> --model <id> --scope <scope> \
       [--budget-usd <n> | --max-output-tokens <n>] [--effort low] [--fresh]
   ```

   The run is strictly sequential and chains carry-forward per scene and per
   model. `--fresh` regenerates selected reviews; pass
   `--allow-volume-one-rewrite` when overwriting existing Volume One reviews.
4. Report generated/skipped scenes, token usage, and cost only when the provider
   reports a reliable numeric cost. Subscription/OpenRouter cost is `null`.

## Guard rails

- Writes only under `reviews/_archive/cold-read/<model-id>/`.
- Uses the shared blind-reader prompt and the same retention validator as the
  Claude workflow.
- Reader reactions are not canon; flag them, never rewrite prose from them.
