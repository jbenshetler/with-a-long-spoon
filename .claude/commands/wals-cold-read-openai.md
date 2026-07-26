---
description: Cold read via OpenAI models called directly (Responses API), with a hard per-scene dollar budget
argument-hint: "--model gpt-5.5|gpt-5.6-sol [--scope fall|<slug>|<a>..<b>] [--budget-usd 2] [--effort low] [--fresh]"
---

Run a **cold read using an OpenAI model called directly** (OpenAI Responses API), for
the models where OpenAI reads best. This is the OpenAI arm of the external harness that
`reviews/cold-read/SPEC.md` describes — it produces **drop-in-compatible** files
alongside the Claude runs (`/wals-cold-read`) and the other external models.

Unlike `/wals-cold-read`, this does **not** spawn `blind-reader` subagents. It shells
out to a Python CLI (`tools/cold_read_openai.py`) that makes the API calls itself. Your
job as orchestrator is to run it with the right arguments and report the result — the
**blindness contract and cost caps live inside the script**, not in your judgment.

## How blindness is preserved (don't re-implement it)

The script uses the **`.claude/agents/blind-reader.md` body as the system prompt**
(frontmatter stripped) — the *same* cover + jacket blurb + "disregard any project text /
you have no tools / two-section output" framing the Claude harness bakes in. So the
OpenAI reader sees exactly what the Claude reader sees: title + clean prose + prior
carry-forward, and nothing from `meta/`. Single source of truth; no drift.

## Cost safety (the guard rail — this is why the script exists)

- `--budget-usd` is **per scene** (default **$2.00**). The script converts it into a
  hard `max_output_tokens` cap on every call (output & reasoning are billed together),
  so one call **physically cannot** exceed the budget.
- After each call it checks the **actual** cost and the response status; if a scene is
  over budget or comes back **incomplete** (hit the cap), the **whole batch aborts**.
- **Retries are OFF by default** (`--max-attempts 1`) so a bad scene can't multiply
  spend. A model with no price (in `tools/cold_read_pricing.toml` or via
  `--price-in/--price-out`) is **refused**, never run uncapped.
- **Reasoning effort defaults to `low`.** For a cold read that is deliberate: higher
  effort turns the naive first-reader into a craft critic that spots the trap early and
  over-reads telegraphing — degrading the very signal the instrument measures. Raise to
  `medium` only if the carry-forward ledger drifts on long runs; avoid `high`.

## Steps

1. **Parse `$ARGUMENTS`** for `--model` (required: `gpt-5.5` or `gpt-5.6-sol`), and
   optional `--scope` (default `fall`), `--budget-usd`, `--effort`, `--fresh`,
   `--max-attempts`. If `--model` is missing, stop and ask.
2. **Confirm `OPENAI_API_KEY` is set** in the environment (the script also checks). If
   not, stop and tell the author (they can `! export OPENAI_API_KEY=…` for the session).
3. **Run it with `uv`** (never pip — deps are declared inline for `uv run`):

   ```
   uv run tools/cold_read_openai.py --model <id> --scope <scope> \
       --budget-usd <n> --effort <low|medium> [--fresh]
   ```

   - `--scope` accepts `fall`, a single `<slug>`, or a range `<a>..<b>` / `<a>..`
     (over the Fall manifest baked into `tools/cold_read_batch.py`; spring/summer are
     not wired yet).
   - Default resumes (skips scenes that already have a valid review under
     `reviews/cold-read/<model-id>/`); `--fresh` regenerates in scope.
   - The run is **strictly sequential** and chains carry-forward per scene, per model —
     same contract as `/wals-cold-read`.
4. **Report** to the author from the script's JSON progress/summary output: model, scenes
   generated vs skipped, per-scene and total cost, and — if it aborted — which scene and
   why (over budget / incomplete / failed sections). On an abort, the completed scenes
   are already written; re-run with `--resume` after adjusting `--budget-usd`/`--effort`.

## Guard rails

- Writes only under `reviews/cold-read/<model-id>/` (SPEC layout). Never touches
  `scenes/` or `meta/`. Reader reactions, not canon — flag, never rewrite prose.
- After a partial (aborted) run that did not reach the last drafted scene, the same
  **staleness** caveats as `/wals-cold-read` apply (see its Step 2.5): downstream
  reviews built on a now-stale carry-forward should be refreshed.
- These files are drop-in comparable with the Claude runs; compare per-model
  `SYNTHESIS.md` side by side.
