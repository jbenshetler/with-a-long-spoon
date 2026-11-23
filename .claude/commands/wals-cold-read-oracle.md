---
description: Interrogate a frozen cold-read reader — probe what a blind first reader knows/feels at a chosen stage, via a neutral→pointed funnel
argument-hint: "--model <id> (--probe <key[,key...]> | --ask \"<neutral> || <pointed>\") (<slug> | --checkpoints [s1,s2,..] | --sweep [<a>..<b>])"
---

Run the **cold-read oracle**: pause a model's grounded blind reader after a chosen chapter
and ask it questions, to measure what a genuine reader *knows and feels* there without
leaking design. Read `reviews/cold-read/ORACLE.md` first: the reader-at-stage-N memory, the
**tiered funnel**, the delta interpretation, the scale, and the fixed battery
(`oracle-battery.json`).

The reader at stage N gets the jacket of N's volume (from `volume-packets.toml`), its own
checkpoint `ck-ch<B>` (B = last decade boundary ≤ N), and the raw prose of B+1..N, each
chapter headed with its title and date. Harness: **`tools/cold_read_oracle_stage.py`**;
persona `.claude/agents/blind-oracle.md`. Read-only: writes only under
`reviews/cold-read/<id>/oracle/`.

## Step 0 — Resolve the model

`--model <id>` is **required**, the versioned id from `reviews/cold-read/ensemble-config.toml`.
`claude-*` runs headless on subscription OAuth with no tools; `gpt-*` on codex subscription.
OpenRouter readers are refused. Missing `--model`: stop and ask.

The tool refuses to run when the stage's checkpoint is **missing** (it prints the mint
command) or **stale** (minted before an edit to a chapter it summarizes). Remint, or pass
`--allow-stale-checkpoint` only when the author has approved that run; each answer then
records the stale memory in its header. `--show-prompt` runs the same checks and prints the
assembled prompt and its size, free.

## Step 1 — Resolve the probes

- **`--probe <keys>`** → `--probes <keys>`: each key's neutral and pointed question from the
  battery. Unknown key → the tool stops and lists the valid ones.
- **`--ask "<neutral> || <pointed>"`** with `--label <slug>`. If only one clause is given,
  derive a tight pointed form (name the thing directly, ask 0–5 with evidence), pass both,
  and show the author the pointed form you derived.

## Step 2 — Resolve the stages

`--stage` takes a slug or a reader-sequence number. `end` = the last drafted chapter;
`<volume> end` = that volume's last chapter (`tools/volume_scenes.py --list N`). For
`--checkpoints [s1,..]` run each listed stage (with no list, pick a few spread across the
drafted run and name them); for `--sweep [a..b]` run every stage in the range. Stages are
independent, so run them in parallel, one invocation each.

## Step 3 — Run

```
tools/cold_read_oracle_stage.py --model <id> --stage <slug> --probes <keys>
tools/cold_read_oracle_stage.py --model <id> --stage <slug> --ask "<neutral> || <pointed>" --label <slug>
```

Each (probe, tier) is its own fresh call; the pointed call never sees the neutral answer.
Existing answers are skipped; `--fresh` overwrites.

## Step 4 — Record

Answers land at `reviews/cold-read/<id>/oracle/<stage>--<probe>--<tier>.md`, each with the
verbatim question and the memory it was given. For checkpoints or sweeps, also write
`<probe>--checkpoints.md` / `<probe>--sweep.md` with the table

```
| stage (slug) | neutral 0–5 | pointed 0–5 | delta | note |
```

The questions are part of the measurement — never omit or paraphrase them.

## Step 5 — Report the finding

Give the author the shape, not just the files. For each probe, read the delta per
`ORACLE.md`:

- **neutral high / pointed high** → landed on its own.
- **neutral low / pointed high** → *buried* — present but not salient (the blind spot);
  name the stage where it stays buried.
- **both low** → not on the page.
- **high neutral where it should stay hidden** (e.g. `randi-suspicion` in the light
  stretch) → **telegraphing** — quote what the reader flagged.

For a sweep, describe the **curve**: where the score crosses from low to clear, or never
does. That crossing point is the answer to "when does the reader get it?" — the thing
the author can't feel from inside. Flag any stage where an earn-the-dark probe spikes
early.

Non-destructive: writes only under `reviews/cold-read/<id>/oracle/`. Reactions, not
canon — never rewrite the author's prose.
