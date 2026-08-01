Run a sentence-by-sentence consistency and logic audit of `scenes/$1.md` in a
sub-agent, and report the findings in chat. This is a mechanical continuity
instrument, not a craft review — it complements `/wals-scene-review`, which
owns craft/architecture/thesis judgment. **Flag and advise; never rewrite the
author's prose unless asked.**

## Step 1 — Spawn the auditor

Spawn ONE `general-purpose` sub-agent (synchronous) with this brief, filling in
the absolute path to `scenes/$1.md`:

> You are doing a sentence-by-sentence consistency and logic audit of one
> chapter of the novel *With a Long Spoon*. Read the file `<absolute path>` in
> full.
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
> Output a report: (1) a one-line verdict (clean / N issues found); (2) a
> numbered list of findings, each with the quoted sentence plus locating
> context, the problem, severity (fix / clarification / nitpick), and a
> recommended fix described in one sentence (do not draft replacement prose);
> (3) if nothing found, say what you checked so the clean bill is credible.
> Return the report as your final message — raw report text, no preamble.

## Step 2 — Check prior triage

While the auditor runs, check for `meta/meta-triage-$1.md`. If it exists, its
"left standing" verdicts are authorial decisions — drop any finding that
restates one, and say so.

## Step 3 — Report

Relay the findings ordered by severity (fix → clarification → nitpick), each
with the quoted line and the risk. Include the auditor's what-was-checked
summary when the verdict is clean or near-clean, so the bill is credible.
Do not apply any fix; the author decides.
