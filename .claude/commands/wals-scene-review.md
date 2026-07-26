---
description: Full craft/architecture/continuity review of a drafted scene
argument-hint: <scene-slug> (e.g. see-you-later)
---

Perform a constructive, critical review of the scene `scenes/$1.md` — how it's
landing against the novel's craft rules, character architecture, and structural
plan. This is a review aid: **flag and advise, never rewrite the author's prose
unless asked.** The judgment stays with the author.

## Step 1 — Freshen the index and run the linter

Run both, in parallel:
- `tools/novel-assistant/na.py reindex` (incremental; keeps recall fresh)
- `tools/novel-assistant/na.py style scenes/$1.md` (an explicit path works even
  before the scene is indexed)

Read the style hits as *candidates*, not verdicts — surface clusters and any
`never-name` (severity `error`) canon breaches; ignore accepted suppressions.

## Step 2 — Read the scene, then fan out the prep lookups

Read `scenes/$1.md` in full. Then spawn these lore-keeper subagents **in a
single message so they run concurrently**. Each prompt must name the scene, its
POV, and what it's doing; ask for *rules and relevant passages with sources*,
not whole-file dumps. Adapt the four queries to whichever characters and beats
this scene actually contains:

1. **POV character's architecture + console rules** — core psychology, the
   operative do/don'ts most easily missed for rendering this character
   (`meta-arch-<name>.md`, `meta-craft-<name>.md`), physical-rendering rules.
2. **Other principal(s) in the scene** — architecture + console/double-register
   guards; how they should read to the POV character; the DON'Ts about
   telegraphing (esp. Randi's "earn the dark by being light").
3. **This scene's plan + threads** — its entry in `meta-plan-chronology.md`
   (planned beats, purpose, placement, `[NEW]`/`[detail]`), any
   `meta-condensed-$1.md` / `meta-note-$1.md`, the running-threads registry
   (which seeds belong in *this* scene and in what register), and any
   continuity flags touching it.
4. **Thesis + foreshadowing constraints** — which thesis strands should be
   *seeded by resonance only* here; the Cassandra device and "never explained"
   rule if a warning figure appears; the full earn-the-dark rule; what a
   "signal to cut" looks like.

## Step 3 — Review against the rubric

Synthesize (don't just relay the subagents). Judge the draft on:

- **Craft rules** — never-name/never-explain, body-before-mind, minimize
  em-dashes, don't editorialize/telegraph, POV discipline, vary recurring-ritual
  phrasing.
- **Character architecture** — is each character on-model (psychology, register,
  physical rendering)? Flag any off-axis note.
- **Sensory grounding** — concrete, embodied, response-before-cognition.
- **Characterization** — voice, behavior, relationship dynamics.
- **Plot** — does the scene do its structural work; internal logic.
- **Thesis-carry** — which strands land, by resonance not exposition.
- **Foreshadowing / seed-calibration** — are the seeds this scene owes present,
  and pitched so the cold is invisible on first read, "all there" on reread?
  This is usually where the real risks live: name any line where the machinery
  hums too close to the surface.
- **Earn-the-dark** — genuinely warm/engaging on first read; no author's thumb.
- **Continuity / dates** — reconcile against the chronology (which owns dates);
  verify weekdays, elapsed time, venue, and canon details. Flag conflicts.

## Step 4 — Report

Output in this shape, prioritized, scannable:

- **What's landing (don't touch)** — name what's working so it's protected.
- **Where I'd point the flashlight** — the few things actually worth the
  author's knife, ordered by importance; for each, quote the line, say the
  specific risk, and — only if it helps the author decide — offer options.
- **Verify** — anything to reconcile against canon/chronology before trusting.
- **Bottom line** — an honest overall verdict on how the scene is landing.

Do not rewrite the author's prose off any hit. Offer alternatives only when they
sharpen a decision, and let the author choose.
