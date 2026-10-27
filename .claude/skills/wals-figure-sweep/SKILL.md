---
name: wals-figure-sweep
description: >-
  Find repeated metaphors and similes across the whole book: the same picture
  returning in different words ("like a missed stair", "the rail on a stair",
  "climbing the same stair"), the same picture applied to different people
  (the lamp that is Randi's attention and Vee's presence), and the same feeling
  rendered by different pictures (the missed stair, the floor going out, the
  high-board drop). Runs tools/figure_harvest.py, gates on the gold set, then
  walks each family past the author one at a time. Flags and proposes; applies
  only what the author rules. Use when the author asks for a metaphor, figure,
  simile or image-repetition sweep, or names a figure that keeps coming back.
---

# wals-figure-sweep — one figure, one owner

Readers remember a figure. The second "like a missed stair" spends the first,
and a lamp that lights up Randi in one chapter and Vee in another blurs who is
being seen. Word-based tools can't find this. `rg "stair"` returns ~35 hits, of
which 6 are figures, and still misses "climbing the same stair". "Missed a
stair" and "taken stairs too quick" were both remembered wrong (the text has
"like a missed stair" and "too fast"). So step 1 is a model reading in context,
and everything after it is deterministic.

Flag and propose; the author rules on every family. The book runs on designed
returns (doors, the deadbolt, warmth, the Bible's running threads). A repeat is
as likely to be designed as accidental.

## Where it sits

It comes after the cutting passes (close-third, explain-audit, retell), which
remove some instances anyway, and before the verification passes (line audit,
fact audit, orphan sweep), which have to check the prose it leaves.

## State

- `audits/figures/gold.md`: the acceptance set. The tool must find every FIND
  line and must not report a LITERAL line. Add to it whenever the author names
  a figure the sweep missed.
- `audits/figures/<model>/chapters/<slug>.json`: one model's figures per
  chapter, with a prose sha so a later edit shows the record is stale.
- `audits/figures/<model-a>+<model-b>/groups.json` and `report.md`: the union
  of the models' figures, grouped, and the families in 2+ chapters.
- `audits/figures/designed.md`: families the author has ruled designed, as
  `- picture: <family> · <ruling, date>` or `- sensation: <family> · …`. The
  report lists these apart and does not raise them.
- `audits/figures/rulings.md`: every ruling on a family, with the figures
  kept, varied and cut.
- `audits/figures/STATUS.md`: run dates, models, score, families walked.

## Step 1 — run, and gate on the gold set

**Two models, unioned (author ruling 2026-10-27): `claude-sonnet-5-5` and
`gpt-6.1-terra`**, both on subscription lanes, at effort `medium`. They are
the tool's defaults. A figure either model finds counts; the two agree on
about 60% of figures, so each catches what the other misses. A
provider/model id is OpenRouter: paid, and it needs the author's
authorization for each run. Not Haiku (author, 2026-10-27).

```
tools/figure_harvest.py extract --model claude-sonnet-5-5 --gold   # run both in parallel
tools/figure_harvest.py extract --model gpt-6.1-terra --gold
tools/figure_harvest.py group                                      # local, no model calls
tools/figure_harvest.py score
```

**Do not run the whole book until the gold score passes.** Recall on FIND
lines should be at least 90%, no LITERAL line should come back as a figure,
and each gold group should share one family (`ok`, not `SPLIT`). If it falls
short, fix the prompts or the grouping and re-run the gold chapters with
`--fresh`. Never edit the gold set to pass.

**Then run it per volume** (the sweep has cross-volume scope,
`meta-plan-editorial-checklist.md`, Volumes): extract the volume's chapters on
both models, then group and report **through** that volume, so its figures are
grouped with every earlier volume's. A repeat of a figure from a published
volume is fixed in the later volume.

```
tools/figure_harvest.py extract --model claude-sonnet-5-5 --volume 2
tools/figure_harvest.py extract --model gpt-6.1-terra --volume 2
tools/figure_harvest.py group --through 2
tools/figure_harvest.py report --through 2
```

How it groups (step 2, deterministic):
- **Pictures** come from each figure's vehicle nouns, lemmatized and merged
  by embedding (lamp, light, lamplight merge; sun and ladder stay apart). A
  picture is **grounded** when its noun is on the page in the quote; a
  category the model inferred ("object", "container") goes to a lower
  section, because it ranks as rare only because the prose never says it.
- **Feelings** come from a fixed sensation list in the extraction prompt
  ("drop or lurch", "light coming on", …). Free-text feeling labels do not
  cluster; the fixed tag puts the missed stair, the floor going out and the
  high-board drop together.
- **Ranking:** most chapters first. A picture whose noun the book mostly uses
  literally (rarity below the floor) sinks to the end of its section.

Extraction takes about 25–35 minutes per model for the 24 gold chapters, and
is restartable: a chapter is saved only when every window came back usable,
and raw replies are kept under `.work/`. After a prose edit, re-extract only
the changed chapters with `--slugs … --fresh`, for both models, then
`group`.

## Step 2 — triage the report before showing it

The report is deliberately over-full. Most families of worn phrases ("lose my
nerve", "set it right") are not what a reader carries. Before walking, sort
the families into three groups:

1. **Raise.** A vivid or specific picture that returns: the stairs, the lamp,
   lit-from-inside, held-to-the-light. Rank first the pictures applied to more
   than one person, then the most instances.
2. **Feeling clusters.** Different pictures rendering one sensation (the drop
   family). Raise one when the pictures are vivid enough that a reader would
   hear the second as an echo of the first.
3. **Not raised.** Worn idioms, families already in `designed.md`, and designed
   motifs from the Bible's running threads and the echo ledger
   (`meta/meta-plan-echo-triage.md`). List these in the batch file with the
   reason, so the author can pull one back.

Check each candidate against the running-threads registry and
`meta-plan-echo-triage.md` before raising it. A returning image that is a
seeded thread is designed until the author says otherwise.

Write the batch to `audits/figures/batch-<date>.md`: the families in rank
order, each with every instance (`scenes/<slug>.md:<line>`, who it describes,
whose POV, the quote).

## Step 3 — walk one family at a time

For each family, show every instance **in context** (the sentence around it,
with the figure in **bold**), in reading order, with who it describes and whose
POV it is in. Then give the options:

- **Designed.** It returns on purpose; add it to `designed.md` with the
  author's reason.
- **One owner.** Give the picture to one character or one moment, usually the
  strongest or the first. Vary or cut the others.
- **Cut to N.** Keep the best one or two instances and cut the rest.

Recommend one, and say which instance you would keep and why (the first
landing, the most vivid, the one readers quote). For an instance to be cut,
run `tools/praise_check.py --slug <slug> --text "<the figure>"` and give the
tally beside it. For a "vary", follow the close-third rule: **cut first,
render second**. Never invent a weaker figure to replace one. A plain
statement, or the character's own sensory vocabulary (the POV craft doc's
Console rules), beats a fresh metaphor. A replacement figure is new prose:
propose it in `[WORKSHOP]`, and check that it does not start a new family.

Wait for the ruling before the next family. Record each ruling in
`rulings.md` as it comes. **Only an explicit approval applies an edit.**

## Step 4 — apply and check

Apply the approved edits together, each with a script that asserts the old
text occurs exactly once. Then, for every changed chapter:

1. `na.py style scenes/<slug>.md --severity error`, then the plain run. Paste
   the `ASK` hits without acting on them.
2. `tools/praise_check.py --slug <slug>` bare, over the diff.
3. `tools/orphan_refs.py --slugs <slugs> <chapters that recall them>`. A figure
   that is cut may be called back elsewhere (`boyfriend.md:203`'s "the rail
   on the stair" calls back `:13`).
4. Re-extract the changed chapters (`extract --slugs … --fresh`) and confirm
   the family shrank as ruled.

Record the cuts in each chapter's `meta/meta-triage-<slug>.md` under
`## Figure sweep — <date>`, update `STATUS.md`, and commit and push only when
the author asks.
