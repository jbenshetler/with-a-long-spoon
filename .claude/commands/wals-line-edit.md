True line edit of drafted chapters — rhythm, cross-chapter repetition and
unintentional echoes, pet constructions the linter doesn't yet know, word-level
precision, paragraph pacing. Run in sub-agents, reports stored on disk,
reviewed with the author item by item. This is the craft-level pass, distinct
from `/wals-line-audit` (continuity/logic) and the copyedit (mechanics).
**Flag and advise; never rewrite the author's prose unless the author rules on
an item.** Most findings here are taste calls — the author's ruling IS the
edit; the instrument only surfaces candidates.

## Modes

- `/wals-line-edit <slug>` — line-edit one chapter, report in chat (no files).
- `/wals-line-edit harvest` — (re)run `tools/echo_harvest.py` and review the
  echo inventory with the author (Stage 0; see below).
- `/wals-line-edit run` — the batch/restartable pipeline over Volume One,
  driven by `audits/line-edit/STATUS.md`.

## Stage 0 — the echo inventory (once, before `run`)

`tools/echo_harvest.py` mechanically extracts book-wide repetition candidates
into `audits/line-edit/echo-inventory.md`: repeated distinctive n-grams that
cross chapter boundaries, rare-word reuse, and repeated sentence-opening
patterns. Over-inclusive by design — every item is a candidate, not a finding.

Review the inventory with the author **before** per-chapter editing starts;
record each ruled echo in `audits/line-edit/echo-rulings.md` as one of:

- **PROTECTED** — intentional: a seeded thread, canonical line, or designed
  echo. Per-chapter editors must never flag these.
- **FIX-AT** — accidental: keep the stronger occurrence, cut/vary the ones
  listed. Applied during the owning chapter's review, not in bulk.
- **IGNORE** — too common to matter (idiom, connective tissue).

Unruled inventory items may be raised by per-chapter editors; ruled ones are
settled. The rulings file is the durable ledger — the inventory regenerates.

## The pipeline (`run` mode)

**State lives in `audits/line-edit/STATUS.md`** — one row per drafted chapter
in epub order, states `pending → edited → reviewed`. Reports live at
`audits/line-edit/<slug>.md`. The `audits/` tree stays outside the `na.py`
index and outside `meta/` — machine-generated flags must not enter canon
search. On any restart: read STATUS.md, batch the first `pending` chapters,
review the first `edited` chapter with the author.

1. **Batch ahead.** Keep ~4–6 line edits in flight in background sub-agents
   while reviewing in the foreground. Each sub-agent gets the brief below plus
   the current `echo-rulings.md` and WRITES its report to
   `audits/line-edit/<slug>.md` itself. When a report lands, flip the chapter
   to `edited` in STATUS.md and launch the next pending one.
2. **Review in the foreground, one chapter at a time, one item at a time.**
   Before presenting findings:
   - Read `meta/meta-triage-<slug>.md` if it exists — drop any finding that
     restates a "left standing" verdict, and say so.
   - Run `tools/novel-assistant/na.py style scenes/<slug>.md` and drop any
     finding that duplicates an accepted (suppressed) style hit.
   Then for each finding, in severity order: show the quoted passage in
   context (rg/sed the actual lines — never trust the report's quotes
   blindly), restate the problem, offer lettered options with a
   recommendation, and wait for the author's ruling before the next item.
   Any proposed replacement prose is shown verbatim and applied only on an
   explicit "apply." Push back honestly when a finding is the voice, not a
   flaw — the book's register (spaced em dashes, fragments, recursive
   interiority) is the style sheet, and an editor flagging it is out of scope
   by definition. The editor over-flags by design.
3. **Record rulings.**
   - Applied fixes: edit the scene per the ruled option.
   - **Every left-standing item gets a line in `meta/meta-triage-<slug>.md`**
     (create it if absent, following the triage-doc pattern; label entries
     "line edit" with the date). The triage doc is the ONLY durable ledger —
     a re-run overwrites the report file. Line-edit verdicts re-open on a
     text edit to the passage, like audit verdicts.
   - **Tics feed back:** when a ruling reveals a recurring construction worth
     policing book-wide, add it to `style/style-rules.toml` (with the author's
     sign-off) so the linter knows it for Volume Two; when a flagged line is
     ruled good, `--ack` it per the style-checking rules.
   - Echo findings: record the ruling in `audits/line-edit/echo-rulings.md`
     so sibling chapters inherit it.
   - Append a `## Author rulings (YYYY-MM-DD)` section to the report file —
     one line per item.
4. **Close out the chapter.** Mark it `reviewed` in STATUS.md; commit the
   scene edits + triage + report + rulings + STATUS together
   (`<Title>: line-edit pass — ...`); the epub is stale after any applied
   fix — rebuild on request or at end of session.

## The line-edit brief (per sub-agent, general-purpose, background)

> You are doing a true line edit of one chapter of a psychological literary
> erotica novel. Read the file `<absolute path to scenes/<slug>.md>` in full,
> twice — once for flow, once slowly.
>
> THE VOICE IS NOT ON TRIAL. This book's register is established and
> deliberate: spaced em dashes, sentence fragments for rhythm, recursive
> interiority in italics, plain Anglo-Saxon diction in scenes of intensity.
> Calibrate to the chapter's own best passages, not to an external standard.
> Do not flag the register itself; flag places where the chapter falls short
> of its own voice.
>
> Also read `<absolute path to audits/line-edit/echo-rulings.md>` if it
> exists: PROTECTED echoes must never be flagged; FIX-AT entries naming this
> chapter should appear in your report as pre-ruled items to apply.
>
> Work paragraph by paragraph. Flag only:
> - **Rhythm** — sentences whose length/shape fights the moment (a long
>   subordinated sentence at a point of impact; three same-shaped sentences
>   in a row); paragraphs that continue past their true last sentence;
>   scene sections that end one beat late or one beat early.
> - **Within-chapter repetition** — a distinctive word, image, or
>   construction used twice close together without design; the SAME gesture
>   or beat rendered twice (she looked away / she looked away).
> - **Cross-chapter echo candidates** — distinctive phrases that feel like
>   they may recur elsewhere in the book (list them; the reviewer checks them
>   against the inventory).
> - **Overwork** — three sentences doing one sentence's work; interiority
>   that restates what the action just showed; a metaphor explained after
>   it lands.
> - **Word precision** — the almost-right word, doubled modifiers, abstract
>   nouns where the scene has a concrete one available, verbs buried in
>   nominalizations.
> - **Dialogue shape** — speech that runs grammatical where the character
>   would compress; attributions/beats that interrupt a rhythm they should
>   ride.
>
> Do NOT flag: continuity or facts (a separate audit owns those), mechanics
> (hyphenation/italics/punctuation — the copyedit owns those), explicitness
> or content, or anything that is simply the book's register. Do not rewrite
> prose — describe each recommended change in one sentence; you may quote a
> minimal cut (words to delete) but never draft replacement wording.
>
> Write your report to `<absolute path to audits/line-edit/<slug>.md>` as
> markdown: an H1 (`# Line edit — <slug> (YYYY-MM-DD)`), a one-line verdict
> (clean / N findings, with counts by class), a short paragraph naming the
> chapter's strongest passages (what the rest is calibrated against), then a
> numbered findings list — each with the quoted line(s) plus locating
> context, the class (rhythm / repetition / echo / overwork / precision /
> dialogue), why it falls short of the chapter's own standard, and a
> one-sentence recommendation. End with an `## Echo candidates` list of
> distinctive phrases worth checking book-wide (empty if none). Your final
> message: just the verdict line.
