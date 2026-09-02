---
description: Place-in-novel review — judge a chapter's role in the arc, architecture, and thesis, grounded in the whole volume
argument-hint: <scene-slug> (e.g. forbidden-kiss)
---

Judge not how `scenes/$1.md` reads line by line (that is `/wals-scene-review`'s
job) but **what place this chapter has in the novel**: its work in the arc, the
characterization trajectories it advances or bends, the architecture it serves,
the thesis strands it carries, and whether it earns its position among its
neighbors. Flag and advise; never rewrite prose.

**This review is FED its evidence — it never goes looking.** The difference
between being handed the thesis, the arch docs, and the story-so-far versus
having to search for them is the difference between a reviewer who holds the
design and one who samples it. Load everything below into context before
judging; use the lore-keeper only for follow-up verification of a specific
claim, never as the primary source.

## Step 1 — Load the design (read in full, in this order)

1. `meta/meta-orientation.md` — structural engine, non-negotiable craft rules,
   thread registry pointer.
2. `meta/meta-thesis.md` — the argument the book is making.
3. `meta/meta-arch-bible.md` — character truths + Global Craft Rules.
4. The arch doc of every principal in the scene (`meta-arch-vivienne.md`,
   `meta-arch-pace.md`, `meta-arch-randi.md` as applicable).
5. The chapter's own plan: its `meta-plan-chronology.md` entry (and the entries
   of its immediate neighbors, drafted or planned), plus `meta-note-$1.md` /
   `meta-condensed-$1.md` and any track doc the chronology names for it
   (e.g. `meta-plan-satc-tracks.md`, `meta-note-taste-thread.md`).
6. `meta/meta-triage-$1.md` if it exists — settled criticisms are authorial
   decisions; do not re-litigate them without new evidence.

## Step 2 — Load the story (grounded, volume-scale)

Address the chapter by its slug — `tools/checkpoint_context.py --scene <slug>`
resolves the drafted reading-order N for you (`tools/volume_scenes.py --number
<slug>`); don't hand-count it off the chronology, which includes
planned-but-undrafted entries and so diverges from the drafted order the tools
index. The factual record of the book is the grounded checkpoint machinery —
the same memory the cold-read panel trusts:

- **Prefer whole-volume grounding.** For a Volume 2+ chapter: read the volume
  boundary checkpoint (e.g. `ck-ch050` = all of Volume 1) **plus the raw clean
  prose of every drafted chapter of the current volume** (via
  `tools/checkpoint_bundle.py` or reading `scenes/` files directly), so the
  chapter is judged inside its own volume read end to end.
- For a Volume 1 chapter, or when the volume is too large for context:
  `tools/checkpoint_context.py --scene <slug>` (checkpoint + recent raw window), and
  additionally read the checkpoint *after* N if one exists — place-in-novel
  needs what follows, not just what precedes.
- Use a Claude-family checkpoint (`claude-fable-5` or `claude-opus-4-8` under
  `reviews/cold-read/<model>/checkpoints/`) as the memory of record.

Then read `scenes/$1.md` itself, last, inside all of that.

## Step 3 — Judge (novel-level rubric)

Synthesize; cite chapters and docs by name. Judge:

- **Arc position** — what work does the book need done *here*, per the
  chronology and thesis, and does the chapter do it? What would break or go
  slack if it were cut, moved, or merged?
- **Characterization trajectory** — for each principal: where their arc stands
  entering the chapter (from the grounded record), where it stands leaving,
  and whether that step matches the arch doc's designed slope. Flag regression,
  stasis where movement is owed, or a jump the record hasn't earned.
- **Architecture service** — the engine beats, gates, ladders, and named
  threads this chapter owns per its note/track docs: present, in register, at
  designed intensity? Seeds it owes later chapters planted; payoffs it owes
  earlier chapters honored?
- **Thesis-carry** — which strands does it advance, by resonance not
  exposition; is any strand over-lit or dropped in this stretch?
- **Echo economy (volume-scale)** — images, gestures, phrasings, and scene
  shapes this chapter reuses: earned recurrence (motif accreting) or
  repetition (the record shows it already spent)? Name the prior chapter for
  each.
- **Pacing among neighbors** — heat/quiet, POV, venue, and beat-type sequence
  across the surrounding chapters; does this one crowd or starve the rhythm?
- **Reader-knowledge ledger** — what a first reader knows and suspects at N
  (dramatic-irony state per the checkpoint): does the chapter respect it, or
  does it assume knowledge not yet on the page / re-explain what the reader
  already holds?

## Step 4 — Report

- **The chapter's job, and whether it does it** — one honest paragraph first.
- **Trajectory table** — per principal: entering → leaving → on-slope?
- **Architecture ledger** — owed beats/seeds/payoffs: delivered / missing /
  off-register, each with its source doc.
- **Echo economy** — earned vs. spent, with the prior-use citations.
- **Neighbor friction** — anything the chapters around it (drafted or planned)
  now need to absorb or avoid.
- **Bottom line** — does the chapter earn its place as designed, and the few
  novel-level risks actually worth the author's attention.

The judgment stays with the author. Flag conflicts between docs rather than
silently resolving them — those are authorial decisions.
