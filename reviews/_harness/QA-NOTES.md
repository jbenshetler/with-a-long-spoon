# Grounded panel — QA notes & triage

Consensus QA for the grounded cold-read panel is run with `tools/checkpoint_qa.py`
(see `SPEC.md`, "Grounded read (v3)" → "Panel QA & recovery"). This file records
**triaged failures the author has chosen to keep** — the "note it and proceed"
path — plus the repair history for any checkpoint edits.

A flag listed here is also encoded in `checkpoint_qa.py`'s `ACCEPTED` list, so the
harness reports it as **ACCEPTED** rather than a fresh re-run candidate.

## Accepted reader slips (reads — annotated, not edited)

A reader's reaction is the instrument's measurement, so it is **never hand-edited**;
a persistent slip is re-run once (blind) and, if it reproduces, kept and annotated.

- **claude-sonnet-5 · ch48 (`the-usual`) · `randi-not-redhead`** — 2026-08-15.
  In its structured cast line sonnet stapled Vee's descriptors ("the redhead," "the
  curvy one") onto Randi. Ground truth (prose): "the redhead"/"the curvy one" = Vee,
  "the brunette"/"the sorority one" = Randi — two people. Sonnet's own ck40 checkpoint
  correctly resolves redhead = Vee, so its *memory* is right; this is an isolated
  chapter-48 reaction slip. The one sanctioned blind re-run reproduced the merge, so
  it stands as recorded read-to-read variance. Confined to ch48 — the grounded design
  means it contaminates no later read.

## Checkpoint repairs (memory — edited in place, with provenance)

A checkpoint is a factual substrate, not opinion, so a wrong fact **may** be corrected
by hand toward what is on the page in that span — **never** adding future or planning
knowledge — with a provenance line recorded here, after which the reads in that decade
that consumed the bad memory are re-run. (Prefer re-minting if the checkpoint is broadly
wrong.) None to date.
