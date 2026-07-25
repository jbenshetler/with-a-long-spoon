---
description: Blind first-reader panel — sequential, meta-free reader reactions per chapter, per model
argument-hint: "--model <id> [none | fall | spring | summer | <slug> | <slug-a>..<slug-b> | <slug>..] [--fresh]"
---

Run a **cold read**: walk the drafted chapters in story order and, for each, spawn
a `blind-reader` subagent that has seen no planning material — only the chapter's
title, its full text, and the carry-forward reader-state from the previous chapter.
This measures how the book lands on a genuine first read (the "earn the dark by
being light" tripwire): does a reader fall for Pace, and does suspicion of Randi
stay *unearned* until the pattern earns it?

Every run is scoped to **one model**, and its output lands in a **model-specific
subdirectory** so the same book can be read by many models and the results compared
side by side. See `reviews/cold-read/SPEC.md` for the shared layout/file contract
that external harnesses (for non-Claude models) must also follow.

**You (the orchestrator) may consult the chronology for order and status; the
`blind-reader` never can.** Keep the reviewer starved: it is fed title + text +
prior state *inline only*. Never pass it a file path, a chapter number, the thesis,
the bible, or anything from `meta/`.

`$ARGUMENTS` carries a **required `--model <id>`**, an optional target selector
(default = full run), and optional `--fresh` (regenerates existing files; default
resumes by skipping them).

## Step 0 — Resolve the model (required) and its output directory

Parse `--model <id>` from `$ARGUMENTS`. **`<id>` is required** and is used verbatim
as the output subdirectory name — it must match the convention every harness uses
(see SPEC.md). Use **versioned model ids**, e.g. `claude-opus-4-8`, `claude-fable-5`,
`gemini-2.5-pro`, `gpt-5`, `grok-4`.

- **All output paths in this command are `reviews/cold-read/<id>/…`** (per-scene
  files and this model's `SYNTHESIS.md`). Create the directory if missing.
- **Map the id to a spawnable Claude tier** (the `blind-reader` is a Claude Code
  subagent; only Claude models can be spawned here):
  - `claude-opus-*` → Agent `model: opus`
  - `claude-fable-*` → Agent `model: fable`
  - `claude-sonnet-*` → Agent `model: sonnet`
  - `claude-haiku-*` → Agent `model: haiku`
- **If `<id>` is not a `claude-*` id** (e.g. `gemini-2.5-pro`, `gpt-5`, `grok-4`, or
  anything unrecognized): **stop.** This harness can only spawn Claude models. Tell
  the author to run that model in the external harness, which must write to
  `reviews/cold-read/<id>/` following `reviews/cold-read/SPEC.md`. Do not attempt it.
- If `--model` is missing entirely: **stop** and ask for it (e.g.
  `--model claude-opus-4-8`) — there is no default, because the id is the shared key
  that keeps every harness's output aligned.

Every `blind-reader` spawn in Step 4 must pass `model: <tier>` from this mapping.

## Step 1 — Get the ordered manifest (via lore-keeper, once)

Spawn a single lore-keeper subagent to return the scene manifest from
`meta-plan-chronology.md` — order and status only, no character facts:

> "From `meta/meta-plan-chronology.md`, list every `[SCENE]` and `[VIGNETTE]` entry
> in document order. For each, give: display title, slug (the `<slug>.md` filename),
> Volume (Fall / Spring / Summer — from the `◆ VOLUME ONE/TWO/THREE` markers), and
> whether it is drafted (`Draft complete`) or not. Skip `[EVENT]` entries. Return a
> plain ordered list, nothing else."

This list is the only chronology data you hold. Everything downstream keys off it.

## Step 2 — Resolve the target set from the selector

Build the ordered list of **slugs to review**, all drafted, in story order:

- **empty** → contiguous from the opening: walk drafted scenes from the top and
  **stop at the first undrafted gap** (a `planned` entry between drafted ones ends
  the run). Report the stop point.
- **`fall` / `spring` / `summer`** → all drafted scenes in that Volume, in order.
- **`<slug>`** → just that scene.
- **`<slug-a>..<slug-b>`** → inclusive; drafted scenes in that span, in order.
- **`<slug>..`** → that scene forward through the last drafted scene (cascade form).

If a requested slug isn't in the manifest, or a range endpoint is `planned`, say so
and stop rather than guessing.

## Step 3 — Determine each target's input carry-forward

Each `blind-reader` needs the **prior chapter's `## Carry-forward state`** as input.
That carry-forward is itself **accumulated** — each reader folds all earlier chapters
into it and preserves a durable ledger (who's-who, motif/image ledger, symbolism, open
questions) in full — so passing the predecessor's carry-forward passes the reader's
whole memory of the book to that point, not just the last chapter. For each target, the
predecessor is the drafted scene immediately before it in the manifest. **Chains are
per-model: only ever read carry-forward from this model's own subdirectory — never mix
carry-forward across models.**

- The **very first drafted scene of the book** (The Bench) has no predecessor →
  input is empty (opening the book cold).
- Otherwise, load the predecessor's carry-forward from
  `reviews/cold-read/<id>/<predecessor-slug>.md`.
- **If the predecessor has no review file for this model** (targeted/volume/range run
  reaching back before what this model has cold-read): stop and tell the author — the
  reader-state can't be fabricated. Suggest either a full run for this model, or
  starting the range at the earliest scene that does have a review file under
  `reviews/cold-read/<id>/`.
- **Resume:** on a full/volume run without `--fresh`, if a target already has a review
  file **in this model's subdir**, skip it and use its stored carry-forward as the
  next input. `--fresh` regenerates every target in scope.

## Step 4 — Read each chapter and spawn its reader (strictly sequential)

For each target slug in order — **one at a time; each depends on the previous
output**, so do NOT parallelize:

1. **You** read `scenes/<slug>.md` in full (the reviewer has no file access).
2. **Strip everything a first reader would never see** before feeding the text.
   The reviewer gets the display title + *clean prose only*:
   - the leading **italic scene-header note** under the `# Title` (POV/participant/
     purpose gloss — e.g. *"Pace's POV; the woman is Randi…"*). It would blow the
     experiment; remove it.
   - any **`[AI]` / `[AI?]` craft notes**, embedded author annotations, or trailing
     **craft-notes / revision-notes blocks** — they are scaffolding, not text.
   - Keep the prose otherwise verbatim, including `---` section breaks.
3. Spawn a `blind-reader` subagent — **passing `model: <tier>` from Step 0** — whose
   prompt contains ONLY:
   - the **display title** (from the manifest);
   - the **cleaned chapter text**, verbatim, pasted in;
   - the **prior carry-forward state** (or a note that this is the book's opening,
     read cold).
   Nothing else — no slug, no position, no planning material, no framing about what
   the scene "does," and no mention of which model it is.
4. **Blindness tripwire — hard stop.** After the subagent returns, check its
   reported `tool_uses`. If it is **anything other than 0**, the reader may have
   reached outside the page: **do NOT write its review and do NOT continue to the
   next scene.** Halt the entire run, report which scene tripped it and the
   `tool_uses` count, and let the author decide. A clean run is `tool_uses: 0` on
   every scene.
5. On a clean return, the subagent gives two sections: `### Reader reaction` and
   `### Carry-forward state`. Write `reviews/cold-read/<id>/<slug>.md` as:

   ```
   # Cold read — <Display Title>

   *scene: scenes/<slug>.md · model: <id> · read after: <predecessor-slug or "— (opening, cold)">*

   ## Reader reaction

   <the subagent's Reader reaction, verbatim>

   ## Carry-forward state

   <the subagent's Carry-forward state, verbatim>
   ```

6. That written carry-forward is the input to the next target. Continue.

## Step 5 — Synthesis (multi-scene runs only)

After a run covering more than one scene, synthesize (from the reactions you just
wrote — your call whether to spawn a final pass) and write
`reviews/cold-read/<id>/SYNTHESIS.md`: the **arc-level trajectory** across the scenes
reviewed, for this model —

- how trust / attraction / sympathy / suspicion move per character across the run;
- **where (if anywhere) suspicion of Randi first leaks**, and whether the text
  earned it — the key "earn the dark" signal;
- where sympathy for and attraction to Pace peak or wobble;
- erotic momentum across the run — trace the per-scene **Heat** and **Romance** (0–3)
  as curves; where each builds, peaks, flags;
- **motifs & symbolism** — which recurring images/objects/phrases accreted across the
  run, and where a recurrence paid off or went inert;
- **characterization** across the arc — who deepened, who flattened or drifted;
- **pace** across the arc — stretches that dragged or rushed, or too much of one beat
  in a row;
- any telegraphing / confusion / thumb-on-the-scale clusters worth the author's eye.

One SYNTHESIS per model, in that model's subdir. Skip it for a single-scene run.
(Cross-model comparison is done by hand across the per-model SYNTHESIS files.)

## Step 6 — Report and warn about staleness

Tell the author, briefly:

- the **model** the run used and its output dir (`reviews/cold-read/<id>/`);
- which scenes were reviewed (and any skipped-as-already-done on a resume);
- where a full run stopped (the first undrafted gap);
- **Stale downstream warning** — if this run did NOT reach the last drafted scene,
  list any drafted scenes *after* the last one reviewed that already have review
  files **in this model's subdir**: their carry-forward input is now stale. Give the
  cascade command, e.g. `/cold-read --model <id> <first-reviewed-slug>..`

Non-destructive: writes only under `reviews/cold-read/<id>/`. Never touch `scenes/`
or `meta/`, and never write into another model's subdir. These are reader reactions,
not canon — flag, never rewrite the author's prose.
