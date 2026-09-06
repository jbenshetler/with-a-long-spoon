---
description: Grounded cold read — run the full 8-model blind panel on a chapter (or range)
argument-hint: <scene-slug | volN | N | A..B> [--models <id,...>] [--fresh]
---

Run a **grounded cold read**: for each target chapter, each panel model reads
blind — no planning material, no reader-reaction chain — with **grounded memory** instead of a
carry-forward: the volume packet at that volume's opening chapter only, the
resolved checkpoint `ck-ch<B>`, the raw clean prose of the chapters since that
boundary, and the chapter itself. Reads are mutually
independent, so models AND chapters fan out in parallel.

The **chained lane is retired** (author ruling 2026-08-19 — it forgets too
badly). Never run `tools/cold_read.py`'s chained mode or spawn `blind-reader`
for a new review; the chained archive lives frozen under
`reviews/cold-read/<model-id>/chained/`. The shared file contract is
`reviews/cold-read/SPEC.md` (Grounded read v3).

## The panel (default: ALL EIGHT)

The roster and memory policy are authoritative in
`reviews/cold-read/ensemble-config.toml`.

| Model id | Lane | Checkpoint |
|---|---|---|
| `claude-fable-5` | headless Claude subscription | native |
| `claude-opus-4-8` | headless Claude subscription | native |
| `gpt-5.6-sol` | codex subscription | native |
| `gpt-5.5` | codex subscription | native |
| `kimi-k3` | OpenRouter (paid) | native |
| `glm-5.3-flash` | OpenRouter (paid) | native |
| `qwen3.8-max-0902` | OpenRouter (paid) | `ensemble:core` donor |
| `deepseek-v4-pro-0813` | OpenRouter (paid) | `ensemble:core` donor |

A run with no `--models` is the **full panel**. The **fast probe** is
`claude-opus-4-8,gpt-5.6-sol`; both use subscription auth. `claude-sonnet-5`
and `gpt-5.6-terra` are retired from the voting panel; Terra is the non-voting
ensemble matcher. **Token rule (standing):** never launch Kimi, GLM, Qwen, or
DeepSeek through OpenRouter, or use `--auth api-key`, without specific author
authorization. Fable/Opus use Claude subscription OAuth; Sol/GPT-5.5 use
codex subscription auth.

## Step 1 — Resolve targets and preconditions

1. Targets: a slug, a chapter number, `A..B` (numbers or slugs), or a whole
   volume as `vol1`/`vol2`/`vol3` (the harness expands `--scope volN` to that
   volume's drafted chapters; the jacket still injects only at the volume's
   opening chapter). Resolve slug ↔ number via the harness's reading order
   (Vol 1 drafted + Vol 2 drafted in chronology order). The chapter's chronology entry must say
   **`Draft complete`** — the harness fails closed otherwise; fix the status
   only if the chapter truly is drafted end to end.
2. Run `tools/cold_read_grounded.py --check --model-id <id> --scope <slug>`
   for every selected reader. Native readers need their own `ck-ch<B>`.
   Volume 1 checkpoints are grounded raw-prose mints. After Volume 1, every
   checkpoint is minted from the frozen final native checkpoint of the prior
   volume plus all current-volume raw prose through B. Every boundary in that
   volume reuses the same prior-volume seed; never seed `ck-ch070` from
   `ck-ch060`. The current Volume 2 recipe is:

   ```
   tools/checkpoint_extract.py --reader-sequence \
     --seed-checkpoint reviews/cold-read/<model-id>/checkpoints/ck-ch050.md \
     --from 51 --to 60 \
     --model <native-model> \
     --out reviews/cold-read/<model-id>/checkpoints/ck-ch060.md
   ```

   The checkpoint provenance must pin the seed identity/hash and exact raw
   range fingerprint. Qwen and DeepSeek resolve to the same validated
   `ensemble:core` artifact; they never mint native checkpoints. If a native
   checkpoint is missing, STOP and report the separate high-effort mint. If
   the ensemble is missing or stale, STOP and run
   `tools/checkpoint_ensemble.py check --ensemble core --through B`; remint all
   stale source checkpoints against identical seed and raw-source provenance
   before any ensemble rebuild. Do not mint implicitly.
3. Volume packet: the harness injects the volume's public jacket copy from
   `reviews/cold-read/volume-packets.toml` at that volume's opening chapter
   only. Later chapters carry its gist through checkpoint/window memory. If a
   volume has no packet yet, ask the author whether to run its opening without
   one; never substitute another volume's packet.
4. Without `--fresh`, skip targets that already have
   `reviews/cold-read/<model-id>/<slug>.md` for a given model (resume).

## Step 2 — Subscription readers

Run the two codex readers concurrently:

```
tools/cold_read_grounded.py --model gpt-5.6-sol --scope <slug>
tools/cold_read_grounded.py --model gpt-5.5     --scope <slug>
```

Run the two Claude readers concurrently through the harness's headless clean
lane:

```
tools/cold_read_grounded.py --model claude-fable-5  --scope <slug>
tools/cold_read_grounded.py --model claude-opus-4-8 --scope <slug>
```

The Claude harness spawns `claude -p` on subscription OAuth with
`blind-reader-grounded` as the entire system prompt
(`--exclude-dynamic-system-prompt-sections`), from a throwaway non-repo cwd,
with `ANTHROPIC_API_KEY` scrubbed. Never replace this with in-session reader
subagents; they inherit ambient project context.

## Step 3 — OpenRouter readers (author authorization required)

Use `/wals-cold-read-provider` for Kimi, GLM, Qwen, and DeepSeek. Kimi and GLM
use native checkpoints. Qwen and DeepSeek use the `core` ensemble checkpoint
resolved by `--model-id`; never point either at another model's native
checkpoint and never invoke native checkpoint extraction for them.

All readers run at low effort with an 18k output cap. Run independent readers
and chapters concurrently only after the author has authorized the paid
OpenRouter calls.

## Step 4 — Verify and report

- Count active-roster files from `ensemble-config.toml`; a full-panel run is 8.
- Skim each for a refusal/no-read signature before trusting it; a refusal is
  re-run, not recorded.
- Report per model: Heat/Romance (0–3), what landed as designed, what confused
  or bounced, convergent friction (2+ models) vs. singleton taste. Check
  `meta/meta-triage-<slug>.md` first so settled criticisms aren't re-litigated.
- Reviews are **reactions, not canon**; flag, never rewrite prose from them.
- If the chapter was edited after a prior grounded read, that read is stale —
  offer `--fresh`. Chapters *after* the target are unaffected (no chain).

Non-destructive: writes only under `reviews/cold-read/<model-id>/`. The
`.packets/` token dirs are ephemeral transport — never commit them.
