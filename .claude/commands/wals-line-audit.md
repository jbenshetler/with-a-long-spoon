Sentence-by-sentence consistency and logic audit of drafted chapters, run in
sub-agents, with reports stored on disk and reviewed with the author item by
item. Mechanical continuity instrument, not a craft review — complements
`/wals-scene-review`. **Flag and advise; never rewrite the author's prose
unless the author rules on an item.**

## Modes

- `/wals-line-audit <slug>` — audit one chapter, report in chat (no files).
- `/wals-line-audit run` — the batch/restartable pipeline over Volume One,
  driven by `audits/line-audit/STATUS.md`.

## The pipeline (`run` mode)

**State lives in `audits/line-audit/STATUS.md`** — one row per drafted chapter
in epub order, states `pending → audited → reviewed`. Reports live at
`audits/line-audit/<slug>.md`. The `audits/` tree is deliberately outside the
`na.py` index and outside `meta/` — machine-generated flags must not enter
canon search. On any restart: read STATUS.md, batch-audit the first `pending`
chapters, and review the first `audited` chapter with the author.

1. **Batch ahead.** Keep ~4–6 audits in flight in background sub-agents while
   reviewing in the foreground. Each sub-agent gets the audit brief below and
   WRITES its report to `audits/line-audit/<slug>.md` itself (title line, date,
   verdict, findings). When a report lands, flip the chapter to `audited` in
   STATUS.md and launch the next pending one.
2. **Review in the foreground, one chapter at a time, one item at a time.**
   Before presenting findings, read `meta/meta-triage-<slug>.md` if it exists —
   drop any finding that restates a "left standing" verdict, and say so. Then
   for each finding, in severity order: show the quoted passage in context
   (rg/sed the actual lines — do not trust the report's quotes blindly),
   restate the problem, offer lettered options with a recommendation, and wait
   for the author's ruling before the next item. Push back honestly when a
   finding dissolves on a fair reading (reported-knowledge vs. sight,
   figurative phrasing, defensible ellipsis) — the auditor over-flags by
   design, and camera-angle/positional-logistics items usually deserve
   "leave standing."
3. **Record rulings.**
   - Applied fixes: edit the scene per the ruled option.
   - Substantive left-standing items: record in `meta/meta-triage-<slug>.md`
     (create it if absent, following the existing triage-doc pattern) so later
     passes don't re-flag. Nitpicks the text already answers: no record.
   - Append a `## Rulings (YYYY-MM-DD)` section to the report file — one line
     per item: fixed (how) / left standing (why) / no record.
4. **Close out the chapter.** Mark it `reviewed` in STATUS.md; commit the
   scene edits + triage + report + STATUS together
   (`<Title>: line-audit pass — ...`); remind that the epub is stale (rebuild
   on request or at end of session).

## The audit brief (per sub-agent, general-purpose, background)

> You are doing a sentence-by-sentence consistency and logic audit of one
> chapter of the novel *With a Long Spoon*. Read the file
> `<absolute path to scenes/<slug>.md>` in full.
>
> Method: work through the scene sentence by sentence. For each sentence, ask:
> - Internal logic: does it follow from what came before in the scene? Any
>   non sequitur, impossible physical action, object appearing/disappearing,
>   body position contradicting an earlier sentence, character knowing
>   something they couldn't know yet?
> - Continuity within the scene: time-of-day, lighting, clothing, props, who
>   is holding/wearing/touching what, spatial layout (who is where), drinks/
>   food levels, weather.
> - Pronoun/referent clarity: any "she/he/it" whose antecedent is ambiguous
>   or wrong.
> - Timeline/causality: tense slips, sequence errors, elapsed-time
>   contradictions. Cross-check the scene's date/weekday and character ages
>   against its entry in `meta/meta-plan-chronology.md` and the relevant
>   `meta/meta-arch-*.md`.
> - Dialogue logic: does each reply actually respond to the prior line;
>   attribution errors.
>
> This is NOT a style or prose-quality review — do not flag word choice,
> rhythm, or taste. Do not rewrite prose. Flag only consistency/logic issues,
> plus places where a sentence is genuinely unclear enough that a reader
> would stumble (label those "clarification" rather than "fix").
>
> Write your report to `<absolute path to audits/line-audit/<slug>.md>` as
> markdown: an H1 (`# Line audit — <slug> (YYYY-MM-DD)`), a one-line verdict
> (clean / N issues found, with severity counts), then a numbered findings
> list — each with the quoted sentence plus locating context, the problem,
> severity (fix / clarification / nitpick), and a one-sentence recommended
> fix (do not draft replacement prose). If clean, list what you checked so
> the clean bill is credible. Your final message: just the verdict line.
