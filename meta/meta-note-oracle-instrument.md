# Oracle instrument — note for consideration (2026-08-15)

Methodology note on the grounded oracle battery (`tools/cold_read_grounded.py`,
battery `reviews/cold-read/ln.json`). **Not a committed change — a flag for Volume 2.**
Recorded so the Vol 1 findings can't be misread and so the idea isn't lost.

## The issue: rating scales are inconsistent in *polarity*, and there are two scales

Every oracle probe is scored **0–5** (uniform magnitude). What is *not* uniform is
**which direction is "good."** Three kinds of probe are mixed under the same 0–5:

- **Lower is better** — `thumb` (0 = no author's thumb felt; 5 = heavy telegraphing).
  A low score is a *good* result. (Vol 1 whole-book `thumb` came in around 2 = mostly clean.)
- **Higher is better / "working"** — `believability` (5 = utterly real), `erotic-charge` (5 = peak).
- **Neither — purely descriptive, not good/bad** — `identification`, `pov-reliability`,
  `arms-length`. A high or low number here is a *reading*, not a grade. (`arms-length`
  leans "pulled in = design intent," but it's still descriptive, not a pass/fail.)

Separately, the **grounded per-chapter reads** emit `Heat:` / `Romance:` on their own
smaller scale — a *different instrument* from the oracle battery. Numbers from the two
should never be compared directly.

Consequence in practice: a bare "2" is ambiguous without knowing the probe. On `thumb`
a 2 is good news; on `believability` a 2 would be alarming. During Vol 1 triage this
already caused a misread (a low, forgiven `thumb` clause treated as if it were a
demerit). See [[meta-triage-two-towels]] for the one flag that *did* survive.

## Constraint: preserve Vol 1 comparability

Do **not** rescore or restructure the Vol 1 battery. The 6-model × 14-probe × 2-tier
run (commit `93ff506`) is the baseline; changing scale semantics retroactively would
break comparison against it. Vol 1 stays as-is.

## Proposal for Volume 2 (author will likely adopt some form)

- **Label each probe's polarity in the battery JSON** (`direction: lower-better |
  higher-better | descriptive`) and print it in the emitted header, so no answer's
  number is read without its direction.
- **Segregate the descriptive probes** (`identification`, `pov-reliability`,
  `arms-length`) from the graded ones in reporting — don't average or rank them against
  polarized probes.
- Keep the Vol 1 battery frozen alongside the new one so cross-volume drift is measurable
  against a fixed reference, not a moving one.

## Post-mortem: the false-positive triage (why ~60% of "open items" were noise)

During the 2026-08-15 thumb pass, a list of "remaining open items" (C = *In His Hands*
lamp/composing, D = *Water Wings* close over-explains, E = *What to Wear* installments)
was carried into triage. On verification against the source probe files, **all three
were false positives** — none appeared in any `thumb` probe; each was a single-reader,
low-scored, self-forgiven aside, and in two of the three another reader *praised* the
exact line flagged. The only real thumb findings the battery ever produced were the
**stats-lecture cluster** (fixed) and the **Two Towels competency stack** (accepted,
`d54339c`). The list was almost entirely noise. Root causes, ranked:

1. **Summaries stood in for sources.** The list was built from working notes / a
   compaction summary, not from re-reading the probe files. Each restatement shed a
   qualifier. Worst case: gpt-5.5's grief "stayed gentle rather than *over*explained"
   (praise) became "*Water Wings close over-explains*" (a defect) — a **polarity
   inversion manufactured by lossy summarizing.** Violates the Prime Rule and the
   cite-file-line discipline.
2. **Grading metadata was discarded.** The oracle emits quote + whole-book score +
   explicit hedge. Flattening those into binary "items" erased the difference between a
   forgiven N=1 low-score aside and a real, convergent, high-score flag.
3. **The list frame created its own demand.** Once named "open items," the frame
   pressured population and action — a three-option fix menu was drafted for C *before*
   the finding was verified real. Inventing work, dressed as diligence.
4. **Motivated linking.** C's beat (taking a few photos to get a good one) was stapled to
   the Two Towels "over-competence" frame because it matched a thread already in hand —
   pattern-matching to a prior instead of reading what the reader said.
5. **Polarity ambiguity (above) compounded it** — low-and-forgiven `thumb` notes read as
   demerits when they were actually clean results.

### Operating rules for the next battery (binding)

- **Build findings lists only from the probe files**, never from a summary — carry
  **quote + score + hedge verbatim** into any triage list.
- **Threshold to consider an item**: either **2 weak/unforgiven readers** *or* **1 strong
  finding** (a single reader is enough if it's emphatic, high-scored, and unforgiven).
  What does *not* clear the bar is a single, hedged, low-scored, self-forgiven aside —
  that's a footnote, not a task. (The three false positives this pass were all the
  disqualified kind; the two real findings each cleared it — Two Towels as convergence,
  the stats cluster as a strong repeated device.)
- **Quote before analysis; no fix menu before the finding is verified real** against source.
- This is durable working process, so it lives in the versioned repo (this doc), **not**
  in machine-local memory — see `CLAUDE.md` "Where decisions live" (memory does not
  travel across clones). Cross-refs: [[meta-triage-two-towels]], [[meta-triage-lesson]].
