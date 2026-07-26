---
description: Interrogate a frozen cold-read reader — probe what a blind first reader knows/feels at a chosen stage, via a neutral→pointed funnel
argument-hint: "--model <id> (--probe <key[,key...]> | --ask \"<neutral> || <pointed>\") (<slug> | --checkpoints [s1,s2,..] | --sweep [<a>..<b>])"
---

Run the **cold-read oracle**: pause a model's blind first-reader at one or more stages
and ask it questions, to measure what a genuine reader *knows and feels* there without
leaking design. Read `reviews/cold-read/ORACLE.md` first — it defines the reader-at-stage-N
rule, the **tiered funnel**, the delta interpretation, the scale, and the fixed battery.

This is **read-only and off the chain**: it never advances a carry-forward, never writes
to `scenes/`, `meta/`, or the cold-read chain files — only under
`reviews/cold-read/<id>/oracle/`. The `blind-oracle` reader sees only the jacket (baked
into its agent) + a frozen carry-forward; never the prose, never `meta/`.

`$ARGUMENTS` carries a **required `--model <id>`**, a **probe source** (`--probe` battery
keys or `--ask` ad-hoc), and a **stage selector**.

## Step 0 — Resolve the model and its oracle dir

Parse `--model <id>` (**required**, verbatim, versioned — e.g. `claude-opus-4-8`,
`gpt-5.5`). Map `claude-*` ids to a spawnable tier exactly as `/wals-cold-read` does
(`claude-opus-*`→`opus`, `claude-fable-*`→`fable`, `claude-sonnet-*`→`sonnet`,
`claude-haiku-*`→`haiku`). Every `blind-oracle` spawn passes that `model: <tier>`.

- **Non-`claude-*` id** (e.g. `gpt-5.5`): this harness can't spawn it. You may still run
  the oracle **if that model's cold-read chain files exist** — but the reader must be the
  *same* model to be valid, so **stop** and tell the author to run the oracle for that id
  in the external harness (conforming to `ORACLE.md`). Do not substitute a Claude reader
  over another model's carry-forward — that mixes readers and is invalid.
- Missing `--model`: **stop** and ask for it.
- Output dir: `reviews/cold-read/<id>/oracle/` (create if missing).

## Step 1 — Resolve the probe set (and its two tiers)

- **`--probe <key[,key...]>`** → load each key's **neutral** and **pointed** questions
  and scale from the battery in `reviews/cold-read/ORACLE.md`. Unknown key → stop and
  list the valid keys.
- **`--ask "<neutral> || <pointed>"`** → an ad-hoc probe; the `||` separates the two
  tiers. If only one clause is given, ask it as the neutral tier and derive a tight
  pointed form (name the thing directly, request a 0–5 with evidence); show the author
  the pointed form you derived in the report.

Never merge probes into one prompt — each probe is its own funnel so answers stay
attributable and un-cross-contaminated.

## Step 2 — Resolve the stages from the selector

Stages are named by scene slug and map to that scene's **own** carry-forward (the
reader's memory *after* reading it). Get the ordered, drafted manifest the same way
`/wals-cold-read` does (one lore-keeper call for order/slug/volume/drafted-status only —
never character facts) if you need it to expand ranges/checkpoints.

- **`<slug>`** → single stage: the reader after that scene.
- **`end`** → the last drafted scene (whole-book-to-here). **`<volume> end`**
  (`fall end` / `spring end` / `summer end`) → the last drafted scene of that volume.
- **`--checkpoints [s1,s2,..]`** → the listed stages; with no list, pick a few
  spread across the drafted run (name them in the report) for a rough shape.
- **`--sweep [<a>..<b>]`** → every drafted stage (optionally within the inclusive slug
  range) — the full curve. Expensive; use when the trajectory matters (e.g. deciding
  where to place a scene).

For each resolved stage, the carry-forward source is
`reviews/cold-read/<id>/<stage-slug>.md` → its `## Carry-forward state`. **If that file
is missing for this model, stop** and say so — the reader-state can't be fabricated;
suggest running `/wals-cold-read --model <id>` to that stage first.

## Step 3 — Run the funnel per (stage × probe)

For each stage, for each probe — the two tiers are **separate spawns**:

1. **You** read the stage's `## Carry-forward state` from its cold-read file (that text
   is the only reader-memory you pass; do not pass the prose or anything from `meta/`).
2. **Neutral spawn** — spawn a `blind-oracle` (`model: <tier>`) whose prompt contains
   ONLY: the frozen carry-forward state, and the probe's **neutral** question(s).
   Nothing else — no slug, no chapter number, no prose, no framing of what you're testing.
3. **Blindness tripwire — hard stop.** If the spawn's `tool_uses` is anything other than
   `0`, discard that answer and **halt**; report the stage/probe and the count.
4. **Pointed spawn** — spawn a **fresh** `blind-oracle` (`model: <tier>`) with the
   **same** carry-forward + the probe's **pointed** question(s). The pointed spawn must
   **not** receive the neutral answers (fresh instance = no priming carried over). Same
   tripwire.
5. Capture both answers verbatim, and each tier's 0–5 score where the probe is scored.

A stage's spawns are independent, so a single stage's probes may run in parallel; across
a **sweep** the stages are independent too (no chain), so you may batch them — but keep
each probe's neutral and pointed strictly on separate spawns.

## Step 4 — Record

Write under `reviews/cold-read/<id>/oracle/` per the `ORACLE.md` layout
(`<stage>--<probe>.md` single · `<probe>--checkpoints.md` · `<probe>--sweep.md` ·
`<stage>--adhoc-<slug>.md`). Every file records, verbatim: the **exact neutral and
pointed questions asked**, the stage(s), the model, both answers, and — for
checkpoints/sweeps — a table:

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
