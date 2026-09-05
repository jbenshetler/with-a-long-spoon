---
description: Grounded cold read via a provider model (OpenRouter / OpenAI api-key) — mint its checkpoint, then read
argument-hint: "<provider/model or model-id> [--scope <slug>|volN | --from A --to B] [--fresh] [prices $in/$out per M]"
---

Run a **grounded cold read with a non-panel provider model** — a third-party
reader (OpenRouter id like `z-ai/glm-5.3-flash` or `moonshotai/kimi-k3`, or an
OpenAI model on `--auth api-key`) joining the six-model panel's file contract.
Same instrument as `/wals-cold-read`, different billing lane.

**The chained lane is retired** (author ruling 2026-08-19). Never run
`tools/cold_read.py` for a new review — it survives only as a library
(`make_openrouter_agent_fn` etc.) and its reviews sit frozen under
`<model-id>/chained/`. Everything below goes through
`tools/cold_read_grounded.py` + `tools/checkpoint_extract.py`.

## Lane selection (how the harness picks the provider)

- A **`/` in the model id** (`provider/model`) auto-selects the **OpenRouter
  lane** in both tools — needs `OPENROUTER_API_KEY`; billing is **per token**
  (author-authorized only, per the token rule in `CLAUDE.md`).
- `--auth api-key` without a `/` = OpenAI Responses API via `OPENAI_API_KEY`
  (also author-authorized only).
- Pick a short **`--model-id`** for the output dir — drop the provider prefix
  (`moonshotai/kimi-k3` → `kimi-k3`; `z-ai/glm-5.3-flash` → `glm-5.3-flash`).
  `checkpoint_extract.py` has no `--model-id`; use `--out` (below) instead.

## How blindness is preserved (don't re-implement it)

The harness uses the **`.claude/agents/blind-reader-grounded.md` body as the
system prompt** (checkpoint minting uses `blind-extractor.md`) — identical to
what the panel readers see: jacket packet, decade checkpoint, raw prose
window, the chapter. Nothing from `meta/`; the reader emits **only a Reader
reaction** (memory is external now, so there is no carry-forward section).

## Steps

1. **Guard rails first**: confirm the key for the lane is set
   (`OPENROUTER_API_KEY` / `OPENAI_API_KEY`); per-token billing means the
   author must have asked for this run. Note the model's quoted **$/M input
   and output prices** if given — the only way to report cost (step 5).
2. **Mint the model's own checkpoint(s)** — the reader refuses to mint
   implicitly. For Vol 2 reads the boundary is the whole of Vol 1:

   ```
   tools/checkpoint_extract.py --model <provider/model> \
       --out reviews/cold-read/<model-id>/checkpoints/ck-ch050.md
   ```

   One grounded pass over ~184k tokens of clean prose; default effort high;
   the OpenRouter lane caps output at 20k tokens. Sanity-check the result
   (who's-who with genders, consummation flags, the descriptor ledger) before
   spending reads on it. `cold_read_grounded.py --check` lists any missing
   checkpoints for a scope.
3. **Run the reads** — grounded reads are independent, so fan out:

   ```
   tools/cold_read_grounded.py --model <provider/model> --model-id <model-id> \
       --scope <slug>                    # one chapter
       --from 51 --to <N> --jobs 4       # a range (Vol 2 panel convention:
       --decade 50                       #  boundary = the Vol 1 checkpoint)
   ```

   Defaults are right: `--effort low` (high turns the reader into a critic),
   `--max-output-tokens 8000`. Resume mode skips existing reviews; `--fresh`
   regenerates.
4. **Verify format**: each file under `reviews/cold-read/<model-id>/` needs
   its `## Reader reaction` section, and any sub-headings inside it must be
   `###` or bold, never `##` (an `##` sibling truncates both the na.py
   reviews-lane index and the chronology.html model split — normalized once
   already, 2026-09-05).
5. **Report** chapters read/skipped and token totals. OpenRouter returns no
   invoice (`cost: null`) — compute the estimate yourself from usage × the
   quoted prices, and label it an estimate.

## Guard rails

- Writes only under `reviews/cold-read/<model-id>/` (+ its `checkpoints/`).
- Checkpoints are minted per model — never hand one model another's
  checkpoint (the checkpoint *is* that reader's memory).
- Reader reactions are not canon; flag them, never rewrite prose from them.
- Committing the new reader's reviews is the author's call, as is adding the
  model to the standing panel in `/wals-cold-read` (that file is the panel
  roster; this one is the guest lane).
