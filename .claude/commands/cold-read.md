---
description: Blind first-reader panel — sequential, meta-free reader reactions per chapter
argument-hint: "[none | fall | spring | summer | <slug> | <slug-a>..<slug-b> | <slug>..] [--fresh]"
---

Run a **cold read**: walk the drafted chapters in story order and, for each, spawn
a `blind-reader` subagent that has seen no planning material — only the chapter's
title, its full text, and the carry-forward reader-state from the previous chapter.
This measures how the book lands on a genuine first read (the "earn the dark by
being light" tripwire): does a reader fall for Pace, and does suspicion of Randi
stay *unearned* until the pattern earns it?

**You (the orchestrator) may consult the chronology for order and status; the
`blind-reader` never can.** Keep the reviewer starved: it is fed title + text +
prior state *inline only*. Never pass it a file path, a chapter number, the thesis,
the bible, or anything from `meta/`.

`$ARGUMENTS` selects the target (default = full run). `--fresh` regenerates files
that already exist (default resumes by skipping them).

## Step 1 — Get the ordered manifest (via lore-keeper, once)

Spawn a single lore-keeper subagent to return the scene manifest from
`meta-plan-chronology.md` — order and status only, no character facts:

> "From `meta/meta-plan-chronology.md`, list every `[SCENE]` and `[VIGNETTE]` entry
> in document order. For each, give: display title, slug (the `<slug>.md` filename),
> Volume (Fall / Spring / Summer — from the `◆ VOLUME ONE/TWO/THREE` markers), and
> whether it is drafted (`Draft complete`) or not. Skip `[EVENT]` entries. Return a
> plain ordered list, nothing else."

This list is the only chronology data you hold. Everything downstream keys off it.

## Step 2 — Resolve the target set from `$ARGUMENTS`

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
For each target, the predecessor is the drafted scene immediately before it in the
manifest.

- The **very first drafted scene of the book** (The Bench) has no predecessor →
  input is empty (opening the book cold).
- Otherwise, load the predecessor's carry-forward from
  `reviews/cold-read/<predecessor-slug>.md`.
- **If the predecessor has no review file** (targeted/volume/range run reaching back
  before what's been cold-read): stop and tell the author — the reader-state can't be
  fabricated. Suggest either a full run, or starting the range at the earliest scene
  that does have a review file.
- **Resume:** on a full/volume run without `--fresh`, if a target already has a
  review file, skip it and use its stored carry-forward as the next input. `--fresh`
  regenerates every target in scope.

## Step 4 — Read each chapter and spawn its reader (strictly sequential)

For each target slug in order — **one at a time; each depends on the previous
output**, so do NOT parallelize:

1. **You** read `scenes/<slug>.md` in full (the reviewer has no file access).
2. **Strip everything a first reader would never see** before feeding the text.
   The reviewer gets the display title + *clean prose only*:
   - the leading **italic scene-header note** under the `# Title` (POV/participant/
     purpose gloss — e.g. *"Pace's POV; the woman is Randi…"*). It would blow the
     experiment; remove it.
   - any **`[AI]` / `[AI?]` craft notes** or other bracketed author annotations
     embedded in the prose — they are scaffolding, not text.
   - Keep the prose otherwise verbatim, including `---` section breaks.
3. Spawn a `blind-reader` subagent whose prompt contains ONLY:
   - the **display title** (from the manifest);
   - the **cleaned chapter text**, verbatim, pasted in;
   - the **prior carry-forward state** (or a note that this is the book's opening,
     read cold).
   Nothing else — no slug, no position, no planning material, no framing about what
   the scene "does."
4. **Blindness tripwire — hard stop.** After the subagent returns, check its
   reported `tool_uses`. If it is **anything other than 0**, the reader may have
   reached outside the page: **do NOT write its review and do NOT continue to the
   next scene.** Halt the entire run, report which scene tripped it and the
   `tool_uses` count, and let the author decide. A clean run is `tool_uses: 0` on
   every scene.
5. On a clean return, the subagent gives two sections: `### Reader reaction` and
   `### Carry-forward state`. Write `reviews/cold-read/<slug>.md` as:

   ```
   # Cold read — <Display Title>

   *scene: scenes/<slug>.md · read after: <predecessor-slug or "— (opening, cold)">*

   ## Reader reaction

   <the subagent's Reader reaction, verbatim>

   ## Carry-forward state

   <the subagent's Carry-forward state, verbatim>
   ```

6. That written carry-forward is the input to the next target. Continue.

## Step 5 — Synthesis (multi-scene runs only)

After a run covering more than one scene, spawn one final `blind-reader`-style pass
(or synthesize yourself from the reactions you just wrote — your call) to write
`reviews/cold-read/SYNTHESIS.md`: the **arc-level trajectory** across the scenes
reviewed —

- how trust / attraction / sympathy / suspicion move per character across the run;
- **where (if anywhere) suspicion of Randi first leaks**, and whether the text
  earned it — the key "earn the dark" signal;
- where sympathy for and attraction to Pace peak or wobble;
- erotic momentum across the run (where it builds, where it flags);
- any telegraphing / confusion / thumb-on-the-scale clusters worth the author's eye.

Skip the synthesis for a single-scene run.

## Step 6 — Report and warn about staleness

Tell the author, briefly:

- which scenes were reviewed (and any skipped-as-already-done on a resume);
- where a full run stopped (the first undrafted gap);
- **Stale downstream warning** — if this run did NOT reach the last drafted scene,
  list any drafted scenes *after* the last one reviewed that already have review
  files: their carry-forward input is now stale (built on a version that changed).
  Give the cascade command to refresh them, e.g. `/cold-read <first-reviewed-slug>..`

Non-destructive: writes only under `reviews/cold-read/`. Never touch `scenes/` or
`meta/`. These are reader reactions, not canon — flag, never rewrite the author's prose.
