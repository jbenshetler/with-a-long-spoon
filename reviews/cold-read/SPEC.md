# Cold read — file & harness contract

The shared spec every harness follows so the same book, read by different models,
produces **drop-in-compatible, directly comparable** files. The Claude tiers
(`claude-opus-*`, `claude-fable-*`, …) are produced by the `/cold-read` command in
this repo (`.claude/commands/cold-read.md`); non-Claude models (`gemini-*`, `gpt-*`,
`grok-*`, …) are produced by an external harness that MUST conform to this spec.

## What a cold read is

A **blind, sequential first reader.** For each drafted chapter, in story order, a
model reads *only*: the chapter's display title, its clean prose, and a carry-forward
summary of the reader's experience through the previous chapters. It has seen no
planning material, no future chapters, no author intent. It returns a **reader
reaction** (how the chapter lands, to this point) and an updated **carry-forward
state** (what this continuous reader now knows/feels) that feeds the next chapter.
The instrument measures whether the book "earns the dark by being light."

## Directory layout

```
reviews/cold-read/
  README.md                     ← human overview (shared)
  SPEC.md                       ← this file (shared)
  <model-id>/                   ← one dir per model, named by its versioned id
    <slug>.md                   ← one per scene reviewed
    SYNTHESIS.md                ← that model's arc-level synthesis (multi-scene runs)
```

- **`<model-id>` = versioned model id**, verbatim as the folder name. Examples:
  `claude-opus-4-8`, `claude-fable-5`, `gemini-2.5-pro`, `gpt-5`, `grok-4`.
  Use the version so a later model upgrade lands in a new sibling dir instead of
  overwriting. Every harness must agree on the exact string.
- `<slug>` = the scene's on-disk slug (the `scenes/<slug>.md` filename without `.md`).
- No model's run ever writes outside its own `<model-id>/` dir.

## Per-scene file format

```
# Cold read — <Display Title>

*scene: scenes/<slug>.md · model: <model-id> · read after: <predecessor-slug or "— (opening, cold)">*

## Reader reaction

<verbatim reader reaction>

## Carry-forward state

<verbatim carry-forward state>
```

Both `##` sections are required, in this order, with these exact headings.

## Story order & scope

- **Story order** comes from `meta/meta-plan-chronology.md` (every `[SCENE]`/`[VIGNETTE]`
  entry in document order; `[EVENT]`s skipped). The orchestrator uses it only for
  ordering/drafted-status — **the reader model never sees it.**
- A run covers a contiguous drafted stretch, in order, stopping at the first
  undrafted gap. The reader for scene *N* is fed the carry-forward from scene *N−1*.

## The carry-forward chain (per model)

- Chains are **per model.** Scene *N*'s input is scene *N−1*'s `## Carry-forward state`,
  read from the **same model's** subdir. **Never mix carry-forward across models** —
  each model is its own continuous reader.
- The book's opening scene has no predecessor → the reader is told it is opening the
  book cold (empty prior state).

## Input preparation (what the reader is fed)

The reader gets, inline in its prompt, **only**:
1. the display title;
2. the **clean prose**, verbatim — with these stripped first, because a real reader
   would never see them:
   - the leading *italic scene-header note* under the `# Title` (POV/participant/
     purpose gloss);
   - any `[AI]` / `[AI?]` notes or embedded author annotations;
   - any trailing **craft-notes / revision-notes block**;
   - (keep `---` section breaks and everything else verbatim);
3. the prior carry-forward state (or the "opening, cold" note).

Never pass the reader: a file path, the slug, the chapter's position/number, the
thesis/bible/chronology or anything from `meta/`, the model name, or any framing of
what the scene "does."

## Blindness contract (non-negotiable)

The reader must be unable to reach anything beyond its prompt — no file reads, no
search, no retrieval, no web. In the Claude harness this is enforced by a **hard
tripwire**: after each scene the orchestrator checks the subagent's `tool_uses`, and
any value other than `0` halts the whole run (that scene's review is discarded).
External harnesses MUST provide an equivalent guarantee: the model has no tools/no
retrieval for the reading turn, or the run is invalid. A clean run is tool-free on
every scene.

## Reader reaction — rubric (to this point in the book)

Cover, in natural order (don't pad sections with nothing to say):
- **How I feel about each character right now** — attraction, trust, sympathy,
  discomfort; what moved since last chapter and why.
- **Trust vs. suspicion** — does anyone/anything feel "off" yet? Be precise about
  whether the *text on the page* earned it or there's simply no reason to doubt.
  ("No suspicion of anyone" is a valid, important answer.)
- **Erotic charge** — is it working, where does it peak, where does it go slack/clinical.
- **Friction as a reader** — confusion, boredom, telegraphing, the author's thumb;
  quote the line.
- **What I want / expect / dread next** — pull to keep reading; guesses marked as guesses.

Write as a person talking; quote the page; body-response before tidy interpretation.

## Carry-forward state — contents

A compact, cumulative **reader-memory** (not a review — no craft critique here):
- **What happened** — plain plot memory, a few lines.
- **Who's who** — each named character + the one-line impression currently held.
- **How I feel** — current trust/attraction/unease per character; overall mood.
- **Open questions** — what the reader is still wondering/waiting to see.

Fold the prior state in; update what changed; drop nothing load-bearing. The next
reader will have ONLY this plus the next chapter.

## Synthesis

One `SYNTHESIS.md` per model (in its subdir), for multi-scene runs: the arc-level
trajectory — trust/attraction/sympathy/suspicion per character; where suspicion of
Randi first leaks and whether the text earned it; where sympathy for Pace peaks and
wobbles; erotic momentum; telegraphing / thumb-on-the-scale clusters. Cross-model
comparison is done by hand across the per-model syntheses.
