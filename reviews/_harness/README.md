# Cold Read — first-reader panel

Blind, sequential reader reactions to each drafted chapter, **one run per model**, so
the same book can be read by many models and compared. Each `<model-id>/<slug>.md` is
written by a reader that saw **only** the chapter's title, its clean prose, and a
carry-forward summary of the reader's experience through the previous chapters — never
the planning corpus, thesis, or character bible. It is the instrument for the book's
central craft rule ("earn the dark by being light"): a first-time reader should fall
for Pace and should *not* suspect Randi until the pattern earns it.

## Layout

```
reviews/cold-read/
  README.md            ← this file
  SPEC.md              ← the shared file/harness contract (read this to add a model)
  <model-id>/          ← one dir per model, e.g. claude-opus-4-8, gemini-2.5-pro
    <slug>.md          ← per-scene review (Reader reaction + Carry-forward state)
    SYNTHESIS.md       ← that model's arc-level synthesis
    README.md          ← ONLY if the run has a seam (see "Spliced runs")
```

Model dirs are named by **versioned id** (`claude-opus-4-8`, `claude-fable-5`,
`gemini-2.5-pro`, `gpt-5`, `grok-4`, …). Cross-model comparison is done by reading the
per-model `SYNTHESIS.md` files side by side.

**Spliced runs.** A run whose model changed mid-book carries a `README.md` in its dir
naming the donor model and the seam chapter. Its donated chapters are byte-identical
copies of the donor's files (and keep the donor's `model:` line), so they must **not**
be counted as an independent read in a cross-model comparison — compare only from the
seam forward. `gpt-5.6-terra` is the first of these: chapters 1–8 are
`claude-fable-5`'s, chapter 9 on are terra's. Rules in `SPEC.md`, "Model substitution
mid-run."

## Chain currency — where each model actually is

**A model dir being full of files does not mean its chain is current.** A file is stale
if it was read before a later edit to its own chapter's prose, or before a change to the
cover/blurb the whole run is framed by. Because the chain is sequential, a stale file
also makes every file after it stale. Check with git — compare a review's last-commit
date against its `scenes/<slug>.md`, and against the cover commit `4fe7d55`.

As of **2026-08-06**, the live (current-cover, current-prose) chains end at:

| model | live through | note |
|---|---|---|
| `gpt-5.6-terra` | **ch. 15** (`a-round`) | spliced from fable at ch. 9 |
| `gpt-5.5` | **ch. 15** | |
| `gpt-5.6-sol` | **ch. 15** | |
| `claude-fable-5` | **ch. 8** (`may-i-choose`) | retired — Anthropic budget exhausted; continued as `gpt-5.6-terra` |
| `claude-opus-4-8` | **ch. 8** | see below |

The `c6b56c9` re-run under the corrected cover regenerated only chapters 1–8 for fable
and opus, so **their ch. 9+ files are all pre-cover and must not be read as current.**

**Author ruling 2026-08-06 — opus is not being advanced.** Bringing `claude-opus-4-8`
to ch. 15 would cost seven `blind-reader` runs (ch. 9–13 regenerated, then 14–15)
against the same scarce Anthropic budget that retired fable. Three current models
(terra, gpt-5.5, sol) are sufficient for comparison at this stage. Opus's ch. 9+ files
are **left in place but stale** — do not cite them, and do not resume its chain without
regenerating from ch. 9. If opus is wanted later, the options are to spend the seven
runs or to splice it onto a cheaper model from the ch. 8 seam, as fable was.

## Producing a run

- **Claude tiers** (opus/fable/sonnet/haiku): `/wals-cold-read --model <id> [target]` in
  this repo. The command spawns a tool-starved `blind-reader` subagent, runs the
  scenes sequentially with a per-scene blindness tripwire (`tool_uses` must be 0), and
  writes into `reviews/cold-read/<id>/`. Non-Claude ids are refused with a pointer to
  the external harness.
- **Use `--legacy-resume` (author ruling 2026-08-09).** Every review on disk predates
  the `v2-volume-entry-jacket` protocol, so `has_valid_review()` does not recognize any
  of them as a seedable predecessor and the harness refuses to start. Pass
  `--legacy-resume` to seed from the existing chain; new files are stamped
  `reader-protocol: v1-repeated-jacket-legacy`, which keeps them comparable with the
  baselines already here. **This is the standing default until the panel is rebuilt
  under v2** — a full-chain job across all four active models, not yet scheduled. Do
  not silently start a v2 chain on top of legacy carry-forward.
- **Non-Claude models** (gemini/gpt/grok/…): produced by a separate harness that
  **must follow `SPEC.md`** — same layout, same filenames, same two-section format,
  same carry-forward chaining and blindness rules — so its files line up exactly with
  the Claude runs.

## Grounded read (v3) — the chain-free reader

The chained instrument above forgets: chapter *N* reads the carry-forward of chapter
*N−1*, a paraphrase-of-a-paraphrase up to ~50 hops deep, and hard facts (the
consummation, who "the brunette" is) decay across the chain no matter how much retention
machinery is added. The **grounded** variant fixes this at the root by removing the
chain. Each chapter is read with memory reconstructed from ground truth: the **grounded
checkpoint** at the last decade boundary (minted from the raw prose 1..B in one pass) plus
the **raw prose of the chapters since** that boundary — zero paraphrase hops. The reader
emits only a `## Reader reaction` (memory is external now), and files land in
`<model-id>/grounded/<slug>.md`, leaving the chained files untouched.

- **Produce it:** `tools/checkpoint_extract.py --model <id> --to <B>` to mint each decade
  checkpoint (they're independent — parallelizable), then `tools/cold_read_grounded.py
  --model <id> [--from N --to M | --scope <slug>]` for the reads. `--check` lists the
  checkpoints a range needs; `--emit-prompt N` prints a chapter's assembled prompt so a
  Claude `blind-reader-grounded` subagent (no API tokens) can be driven by hand.
- **Contract, format, and the parallel two-wave design:** see `SPEC.md`, "Grounded read
  (v3)."
- **QA it:** `tools/checkpoint_qa.py` (`--target checkpoints|reads`) runs a consensus
  battery and flags minority outliers (re-run candidates) vs. whole-panel fails
  (mis-calibrated checks). Triaged-and-kept failures live in `QA-NOTES.md` + the tool's
  `ACCEPTED` list. Recovery policy (edit checkpoints, annotate reads, no chain to lose):
  `SPEC.md`, "Panel QA & recovery."

Each chained file holds two parts: **`## Reader reaction`** (the deliverable — a felt read
followed by a structured block: cast present in person, Heat/Romance 0–3, motifs &
symbolism, characterization, and pace within- and between-chapters) and
**`## Carry-forward state`** (plumbing — the *accumulated* reader-memory fed to the
next chapter's reader, carrying a durable ledger of who's-who / motifs / symbolism /
open questions; editing a source scene re-arms it and makes every downstream file
stale). These are reader reactions, not canon and not craft verdicts — the judgment
stays with the author. Ratings use shared 0–3 anchors (see `SPEC.md`) so they compare
across models.
