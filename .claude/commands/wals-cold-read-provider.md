---
description: Grounded cold read through OpenRouter — native or ensemble checkpoint policy
argument-hint: "<provider/model> --model-id <id> [--scope <slug>|volN | --from A --to B] [--fresh]"
---

Run an OpenRouter-backed grounded cold read. This lane serves four standing
panel readers plus explicit guest models. It has the same blind-reader and file
contract as `/wals-cold-read`; only billing and checkpoint ownership differ.

**Every OpenRouter call bills per token and requires specific author
authorization.** Never infer authorization from panel membership or a prior
run. Malformed, truncated, provider-error, or reasoning-only output is invalid:
archive diagnostics outside the review corpus and never write it as a reaction
or checkpoint.

The authoritative reader policies live in
`reviews/cold-read/ensemble-config.toml`:

| Output model id | OpenRouter model | Checkpoint |
|---|---|---|
| `kimi-k3` | `moonshotai/kimi-k3` | native |
| `glm-5.3-flash` | `z-ai/glm-5.3-flash` | native |
| `qwen3.8-max-0902` | `qwen/qwen3.8-max-0902` | `ensemble:core` donor |
| `deepseek-v4-pro-0813` | `deepseek/deepseek-v4-pro-0813` | `ensemble:core` donor |

## Preconditions

1. Confirm the author authorized this paid run and `OPENROUTER_API_KEY` is set.
2. Resolve the reader policy by **output model id**, not provider id.
3. Run:

   ```
   tools/cold_read_grounded.py --check --model-id <model-id> --scope <slug>
   ```

   Kimi/GLM resolve to native checkpoints. Qwen/DeepSeek resolve to
   `reviews/cold-read/checkpoint-ensembles/core/checkpoints/ck-ch<B>.md`.
4. For native Kimi/GLM gaps, mint separately at high effort. This is another
   paid OpenRouter call and requires its own specific authorization. Volume 1
   checkpoints are raw-prose mints. After Volume 1, seed every boundary from
   the frozen final native checkpoint of the prior volume and include all raw
   prose in the current volume through that boundary. For the current Volume 2
   seam:

   ```
   tools/checkpoint_extract.py --reader-sequence \
     --seed-checkpoint reviews/cold-read/<model-id>/checkpoints/ck-ch050.md \
     --from 51 --to 60 \
     --model <provider/model> \
     --out reviews/cold-read/<model-id>/checkpoints/ck-ch060.md
   ```

   Extraction defaults to an 80k output cap and rejects incomplete,
   non-stopping, missing-section, or out-of-order output. Its provenance must
   pin the seed identity/hash and exact raw ch 51..60 fingerprint.
5. Never mint Qwen/DeepSeek checkpoints. The extractor and grounded harness
   reject it. Validate their donor memory instead:

   ```
   tools/checkpoint_ensemble.py check --ensemble core --through 50
   ```

   If stale, remint every stale native source checkpoint against identical seed
   and raw-source provenance, then rebuild the ensemble. Building
   uses the non-voting Terra matcher through subscription auth; it does not
   spend OpenRouter tokens.

## Run

```
tools/cold_read_grounded.py \
  --model <provider/model> \
  --model-id <model-id> \
  --scope <slug> \
  --effort low \
  --max-output-tokens 18000
```

For every Volume 2 decade boundary, use native `ck-ch050` as the seed and raw
ch 51 through that boundary; never seed one Volume 2 checkpoint from another.
Reader reactions still use the resolved decade checkpoint plus the raw
since-decade window, and remain independent. Independent chapters may use
`--jobs N`. `--fresh` is explicit because it spends again.

The harness writes `reviews/cold-read/<model-id>/<slug>.md`. Donor-reader
headers record the ensemble name and checkpoint hash. Keep the emitted
`## Reader reaction` body verbatim; any internal headings must be `###` or
bold, never sibling `##` headings.

## Report and guard rails

- Report input, output, reasoning tokens, provider, finish reason, and exact
  provider cost when returned. Otherwise compute and label a price estimate.
- A resume skips an existing review. If its donor hash differs from the current
  ensemble, report it stale; do not spend a replacement call without explicit
  `--fresh` authorization.
- Reviews are reactions, not canon.
- Kimi/GLM native continuity signals are independent. Qwen/DeepSeek continuity
  assertions inherited only from the shared ensemble are correlated and count
  once; their reactions to the current raw window/chapter count independently.
- Never write outside the canonical `<model-id>/` root. Experimental donor
  labels belong in metadata, not parallel model directories.
