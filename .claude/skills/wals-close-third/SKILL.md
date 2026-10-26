---
name: wals-close-third
description: >-
  Read one chapter by eye for narration that does the reader's work for them —
  a gloss after a shown beat, an announcement before a line, a recap, a
  narrator's motive or verdict the POV character would not herself think — and
  propose cuts so everything left is something the close-third POV character
  senses, thinks, or feels in the moment. Checks reviewer praise and settled
  triage before proposing, presents a numbered batch, applies only what the
  author approves, then lints, hunts orphans and records the rulings. Use when
  the author asks to examine a chapter for explain-after-showing, telling,
  narrator interpretation, or close-third POV slippage.
---

# wals-close-third — leave the reader the pleasure of getting it

Readers enjoy understanding things themselves rather than having them explained.
In close third, **if something needs saying, the POV character senses it, thinks
it, or feels it.** Anything else on the page is the narrator stepping in front of
her: naming what a beat just did, announcing what she is about to say, recapping
the scene, or supplying a motive or a verdict from outside her head.

This skill reads **one chapter, by eye**. Its sibling `wals-explain-audit`
harvests the same defect from the reader corpus across a range; that finds only
what a reviewer said out loud. This pass finds the rest. Worked example: the
Dear pass, 2026-10-25/26 (`meta/meta-triage-dear.md`, "Explain-after-show pass"
and "Capture follow-ups").

Flag and propose; the author rules on every item.

## State

**Progress lives in `audits/close-third/STATUS.md`**, one row per chapter
(`pending` → `proposed` → `reviewed`). With no slug given, finish the first
`proposed` chapter, else take the first `pending` one. Each chapter's proposal
batch is saved to `audits/close-third/<slug>.md`, so a session break loses
nothing.

## Step 1 — load context

1. The meta read list from `CLAUDE.md`, then the authoring projection:
   `tools/checkpoint_context.py --scene <slug> --check`, then without `--check`.
   Feed it as is.
2. The whole chapter, `scenes/<slug>.md`. Read it all; candidates depend on what
   came before them in the scene.
3. `meta/meta-triage-<slug>.md` — *Left standing*, *Protected positives*, and
   anything already cut or declined. Do not re-raise a settled line without new
   evidence.
4. The POV character's **Console rules** in `meta/meta-craft-<name>.md` (via the
   lore-keeper). They say what she notices and how she reads a room, which is what
   a "render it instead" fix has to draw on.

## Step 2 — the test, sentence by sentence

For each sentence of narration ask: **is this something she senses, thinks or
feels, right now?** If not, does it tell the reader something the scene has
already shown or is about to show? That is a candidate.

**Whose is it, clause by clause — before anything else.** Repetition alone does
not make a candidate. If the clause is hers (her memory, her reading of someone,
her working something out), it stays even when it repeats, and if only the
*phrasing* is outside her ("the reflex of a woman who…"), the fix is to reword it
into her voice, not to cut it (`two-towels.md:105`, 6A). Of eleven Two Towels
proposals the author withdrew or kept seven, all on this test; the four that
survived were each a narrator's wink, verdict, or label. Propose only what you
can name as the narrator's, and say whose it is in the item. **A "repeat" of something hers is not a candidate either** unless it adds nothing: check what the later sentence knows that the earlier one didn't (`a-round.md:56` looked like a third statement of the withdrawal and was really her surprise at his frank looking; withdrawn).

The shapes it takes (all from the Dear pass unless noted):

| shape | example |
|---|---|
| **Gloss after the beat** — names what the action just showed | "and slowed" shown, then "She hadn't meant to slow. But here was the part, and the part wanted a different voice…" (`dear.md:13`, cut) |
| **Announcement before the line** — tells you the speech is sincere before she says it | "and here the thing she most wanted Cassie to have, the whole of it, came up plain and certain" (`dear.md:29`, cut; speech joined) |
| **Explaining the joke** — the reason for a reaction that the next line delivers | "because it was Cassie, because the gladness in Cassie always had a flat dry floor under it" (`dear.md:25`, cut) |
| **Repeat in the abstract** — the same realisation restated a sentence later | "It hadn't occurred to her until just now that she didn't know…" after "found she didn't have it" (`dear.md:57`, cut) |
| **Recap at the paragraph's end** — the narrator retelling the scene, then stating its meaning (not her mind replaying it; see Step 3) | "Randi had stood up into all of it… that she had a place now…" (`dear.md:195`, cut to "But it had been answered.") |
| **The narrator's ledger** — the meaning or price of a beat stated from outside her | "She did not know what it had cost Randi… that it had cost something" (`dear.md:181`, *rendered* — see Step 5) |
| **The nudge** — narration remarking on what she fails to notice | "and gave it no further thought" (`all-told.md`, `meta-triage-all-told.md:216`) |
| **Narrator grading a character** — endorsing or verifying instead of inhabiting | `meta-triage-the-pointing-game.md:83`, narration-certainty pass; "and that was the end of his interest in being admired" (`two-towels.md:123`, cut — the narrator reading his interior) |
| **The wink** — the narrator signalling over her shoulder that something is coming | "As if that were the problem." (`two-towels.md:113`, cut; the real problem lands at `:133`) |

Co-signatures worth watching for: an `x-not-y` construction, a `because` clause
after a shown reaction, and a paragraph that keeps talking after its reaction has
landed.

## Step 3 — what is NOT a candidate

Leave these alone and say why in the report:

- **Her own explanation, free indirect, especially a wrong one.** If she hands
  herself a reason, that is character, and the reader sees past it
  (`meta-triage-my-friend-randi.md:210`; `dear.md:123`, "one more kindness",
  dramatic irony).
- **A motive the scene does not show any other way.** Cutting it loses
  information rather than redundancy (`dear.md:175`).
- **Designed refrains and protected passages** listed in the triage doc — unless
  the author reopens one, as they did with `dear.md:181`.
- **Her mind going back over it at an emotional peak.** When she reconstructs
  what just happened — links a memory to what is in front of her, works out why
  someone did something — that is her processing, not a recap, even if the
  reader already has the facts. Her reading of his motive is often where the
  dramatic irony lives (`two-towels.md:131`, the volume's hinge: "He'd gone and
  found the cloth… waited for her to come out here", withdrawn). The long
  reconstructing sentence is also what her voice breaks down out of ("No one had
  ever—"); shortening it removes the fall.
- **Her memory, in her own generalizing voice** ("Said it the way you say things
  you've already let go of", `two-towels.md:109`, kept).
- **Her perception of someone's manner or tone.** A clause saying *how* a line was said is often the only thing setting its tone; without it the line can read as pressure (`two-towels.md:129`, withdrawn).
- **Plain redundancy that is not explanation** (a reaction stated twice in
  physical terms). Mention it separately as a trim, not as a finding.

## Step 4 — weigh praise, then present the batch

Before proposing any cut, run `tools/praise_check.py --slug <slug> --text "<the
words to cut>"` and give the tally beside the item. Test a sentence's clauses
separately: the praised half and the explaining half are often different halves
(`dear.md:99` kept "because Randi was standing right there", cut only the tail).
**`praise_check` misses paraphrase**, so for a line about manner, tone or motive, also `rg` the chapter's cold reads and capture gates for the *idea* in other words (`two-towels.md:129` "left the rest to her, open" came back clean, while two readers had it as "left it open" and "leaves the rest open"). The weighting table in `wals-explain-audit` applies. **One reviewer's quote, for
or against, is never decisive** — do not build a recommendation on it.

Write the whole batch to `audits/close-third/<slug>.md` (below), then give the
author the one-line verdict and walk the items **one at a time, in context**
(author ruling 2026-10-26): show the surrounding paragraph as it stands, then
the same paragraph with the cut made, the praise tally, and the options. Wait
for the ruling before showing the next item. The batch file holds:

1. A one-line verdict on how heavy the chapter is.
2. A numbered list, grouped by section or movement. Each item: the
   `scenes/<slug>.md:<line>` anchor; the explaining words quoted verbatim; what
   already shows it; the proposed result quoted in full; the praise tally.
   Give lettered options (8a / 8b) where there is more than one honest cut, with
   a recommendation and what each costs.
3. **Leaving alone, with reasons** — the Step 3 lines.
4. **Borderline — likely hers, walk if the author wants.** Do not drop a line
   silently because it *might* be hers. The whose-is-it test is for ranking,
   not for hiding: after the Two Towels withdrawals the first Famished batch
   held back everything arguable, and the author, asking "that was all you
   found?", cut two of the five held back (`famished.md:51`, a repeat in the
   abstract; `:83`, explaining the callback). Rank this tier strongest first.
   **"Told herself" plus her own denial is character, not a narrator's wink**
   (`famished.md:13`, kept: "completely her", sol).

Header: chapter, date, model. Set the chapter's row in `STATUS.md` to
`proposed`. Record each ruling in the batch file as it comes, and apply the
approved edits together once every item has been ruled on. **Only an explicit approval applies an edit.** A question, a
challenge, or a remark about the evidence ("one quote is weak") is not approval.
If the author questions a paragraph, justify each of its beats — what it does,
what reads it, what would go if it went — and let them decide.

## Step 5 — fixes: cut first, render second

- **Default to the cut.** Most glosses carry no information the scene lacks; the
  fix is to delete them and join what is left. Never invent a weaker phrase to
  replace a cut one.
- **Render instead of cut** when the explained thing is load-bearing and nothing
  else on the page carries it. Replace the narrator's statement with **how she
  knows it**: what she senses in the room, drawn from who she is. `dear.md:181`
  is the worked case: the narration *told* the cost of Randi's gesture; the
  revision has Vee feel "a charge come into the air over the white table, every
  smile staying exactly where it was and the room underneath them rearranged",
  which she knows from the top of her own high-school tables
  (`meta-craft-vivienne.md:209`). A render is new prose: workshop it
  (`[WORKSHOP]`), check canon for every physical detail you put in, and check
  that it does not undercut a later chapter's payoff (the Dear render seeds
  `on-her-floor.md:145` and leaves `my-friend-randi.md:227` its bill).
- Do not add anything the author did not ask for.

## Step 6 — after applying

1. `na.py style scenes/<slug>.md --severity error`, fix those; then the plain run,
   and paste the `ASK` hits to the author without acting on them.
2. `tools/praise_check.py --slug <slug>` bare, over the whole uncommitted diff. The
   pre-cut check can miss praise for part of a sentence (the `dear.md:99` tail was
   caught only here). Surface anything new.
3. `tools/orphan_refs.py --slugs <slug> <every chapter that recalls this one>`.
   Find the recallers first: a later chapter quoting a detail from this one (the
   cardigan at `on-her-floor.md:125`) breaks silently if only this slug is passed.
4. Show the author the changed lines and the check results.

## Step 7 — record

Append to `meta/meta-triage-<slug>.md` a section `## Explain-after-show pass —
<date>`: what was cut (anchors, short quotes), any cut made over praise with the
author's ruling in their words, any render with its rationale, and **Left
standing** with reasons, so the next pass does not reopen them. If a render
replaces wording an earlier ruling protected, say that it supersedes it, and
when.

Append the author's rulings to `audits/close-third/<slug>.md` and set the row in
`STATUS.md` to `reviewed <date> (N proposed: A applied, D declined, L left
alone; <commit>)`, filling the commit once there is one.

## Capture reads and commits

Only on the author's request. Capture reads for this pass are **chapter-local**:
`--from N --to N` on the changed chapter only, in an `--experiment`, models from
`tools/cold_read_config.py` (never a list restated here). OpenRouter lanes are
paid and need the author's authorization for each run. Promote experiment gates
to the real lanes and remove the experiment only when the author says so. Commit
and push only when asked.
