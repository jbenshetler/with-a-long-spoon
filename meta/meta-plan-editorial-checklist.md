# Editorial checklist — road to publication (Volume One)

*Recorded 2026-08-01 from an editorial-pipeline review: what a trade editor
would do, mapped against what this project has already done. Working checklist —
mark items done with dates as they complete.*

## Done / in progress

- [x] **Developmental edit** — the `meta/` architecture + thesis, multi-model
  cold-read panels, triage verdicts, oracle probes. Ongoing as scenes land.
- [x] **Continuity/logic line audit** — sentence-level, per chapter, via
  `/wals-line-audit` (state: `audits/line-audit/STATUS.md`). Complete
  2026-08-03: all 49 chapters audited and reviewed with the author.
- [x] **Style-tic policing** — `na.py style` + `style/style-allow.toml`
  ledger. Ongoing per draft.

## To do

- [x] **True line edit** — rhythm, cross-chapter repetition and unintentional
  echoes, pet constructions the linter doesn't yet know, paragraph pacing.
  Systematic front-to-back, distinct from the continuity audit. Complete
  2026-08-14: all 50 chapters reviewed (`audits/line-edit/STATUS.md`).
- [x] **Copyedit against a style sheet** — build the style sheet as the pass
  runs: names/spellings, places, hyphenation rulings, numerals, italics
  conventions (interiority italics applied consistently?), dash/ellipsis
  house rules, capitalization of recurring objects. Sheet lives in `style/`.
  **Decision 2026-08-01: this is its own skill/command, separate from
  `/wals-line-audit`** (that pass is mid-flight; don't graft a second rubric
  onto it). Complete 2026-08-03: Pass 0/1/2 all done 2026-08-02, escalated
  candidates ruled (`ef57bdc`); sheet at `style/style-sheet.md` with no open
  items. Curly-quote conversion deferred to epub typesetting.
- [x] **Whole-book timeline sweep** — one closing audit reconciling every
  elapsed-time claim against the master chronology in a single pass; run
  after all chapters clear the line audit. Complete 2026-08-03: 734 claims
  across 49 chapters (`audits/timeline/`), 9 findings ruled, no cumulative
  drift.
- [ ] **Cross-chapter fact audit (Lane A)** — the class every per-chapter
  instrument is blind to: a fact established in one chapter **contradicted in
  another**. The linter has a closed vocabulary, the lore-keeper only answers
  what it's asked, and a cold reader holds no other chapter in memory — none of
  them can see it. Worked case: `not-enough.md`, where Pace waits for a truck
  turning in four lines before *her car* finds the drive, and Vee drives a car.
  Tool `tools/fact_audit.py` / `/wals-fact-audit`; per-model ledgers in
  `audits/fact-audit/<model>/`; state: `audits/fact-audit/STATUS.md`. Runs
  **independent ledgers across vendors** — five models, four vendors as of
  2026-09-19 (`b082c4f6`: a *second vendor* is what finds real problems, so
  spend on cross-vendor breadth, not depth in one family) — and keeps what more
  than one lands on. **Over-flags by design — the author rules on every item.**
  Token rule: subscription lanes are the default; OpenRouter is paid and
  author-authorized only. **In progress — first ten chapters audited by five
  models (+`a-round`, `not-enough` by sol alone), 2026-09-19; nothing ruled with
  the author yet. Dates are out of scope for this pass** (the whole-book
  timeline sweep above owns them).
- [ ] **Orphaned-reference sweep (Lane B)** — text still pointing at something
  a revision removed. Worked case: a cut passer-by "in a camel coat too warm
  for the afternoon" whose later callback, "the closed camel-coat project,"
  survived the cut and now names a character the reader never meets. Tool
  `tools/orphan_refs.py`; sweeps in `audits/orphan-refs/`; state:
  `audits/orphan-refs/STATUS.md`. Deterministic and
  free, so it is also a **per-edit step** (`AGENTS.md` → *Before writing any
  prose*, 3b) and runs advisory-only in `.githooks/pre-commit --staged`; this
  checklist item is the **systematic front-to-back sweep**, which the hook
  cannot substitute for (it fires after staging, is silenced, and sees only
  staged paths). **First Vol 1 sweep run 2026-09-19
  (`audits/orphan-refs/vol1-2026-09-19.txt`) — 26 candidates, none ruled with
  the author.** Heaviest in the most-revised chapters: `the-bench` 10,
  `the-pointing-game` 6 (including the camel-coat cluster, the pass's own worked
  case).
- [ ] **Reading-effort sweep** — sentences that charge the reader more than
  they pay back: one idea split across stacked subordinate clauses, or across a
  sentence boundary, where a rearrangement carries the same content at lower
  cost. From human reader feedback on `the-bench`, 2026-09-20. Worked case:
  `the-bench.md:49`, where "She slid her hands up over the front of his shirt"
  was held open across a 41-word dash interruption before the clause resumed —
  rearranged into three sentences at 92 → 91 words, nothing cut, peak open
  dependencies 8 → 6. Tool `tools/reading_effort.py` (deterministic: a fixed
  spaCy dependency parse plus arithmetic, no model calls, no tokens);
  per-chapter worklists at `audits/reading-effort/<slug>.md`, author rulings in
  `audits/reading-effort/rulings.toml`, state:
  `audits/reading-effort/STATUS.md`. **Over-flags by design — the author rules
  on every item**, and high effort is frequently earned: suspension is a real
  device and the accretive tail is deliberate voice. **Not a per-edit step
  (author ruling 2026-09-20)** — unlike Lane B this is a deliberate sweep only,
  because it returns ~87 findings on a single chapter and every one needs a
  ruling; running it per keystroke would swamp the drafting loop. Scored
  relative to this book's own corpus, never an external readability index.
  **Protocol (author ruling 2026-09-20): the tool AND a blind model panel,
  both required — this is a pre-publication pass, not a diagnostic.** The
  tool's `chain`/`strand`/`suspend` classes are the structural half (its
  `hold`/`nest`/`front`/`pp`/`split` are demoted: weak predictors). A blind
  model panel — `tools/effort_blind.py`, **at least four models**; a
  three-model consensus is unstable (Jaccard 0.56 to five) — is the semantic
  half, and 58% of what 2+ readers converge on the parser cannot see
  (compressed metaphor, ambiguous reference, abstraction). Work **convergent**
  findings (2+ of 5) first, highest vote count first; a sentence only one
  reader flags is noise. Subscription lanes by default; `glm-5.3` is
  OpenRouter, paid, author-authorized per run, and fails first-try half the
  time. Validation, F1, class tiering, and the published-comp calibration:
  `audits/reading-effort/STATUS.md`. **Progress 2026-09-20: `the-bench` and
  `the-pointing-game` swept by tool + five models; the three top convergent
  sentences (5/5, 4/5, 4/5) rewritten and ruled; 31 convergent findings still
  open (5 at 4+ votes, 8 at 3); 1 tool finding left standing.**
- [ ] **Flat-interrogative sweep** — a question closed with a period or comma
  where a person saying it would voice it as a question. The Bible rule
  (Global Craft Rules, *Questions get question marks — every time*) and the
  linter both stopped at dialogue, so italic interiority and recalled speech
  were invisible: `the-pointing-game.md:143` shipped *is this one mine to
  take.* with 19 more flat italic interrogatives book-wide. Author ruling
  2026-09-20: **the voicing test, every register** — flat only where the page
  marks the line as not really asked (rhetorical, a glossed laugh or gesture),
  and recalled **Cassie** stays flat, hers by design. Tool: `na.py style` rule
  `flat-interrogative`, widened the same day to see `*italic*` spans (20 hits,
  no noise); the linter's live hit list is the state, there is no separate
  file. **Blind spot: an elliptical question with no interrogative word (*Your
  folks coming up.*) is undetectable by pattern, so the front-to-back sweep
  needs a human eye — and the assistant's bias is one-directional (drops
  marks, never over-marks), so when in doubt, mark it.** **Progress
  2026-09-20: 14 marks applied across 11 chapters. Left flat pending author
  ack: `strokes` ×4 (Cassie, marked on the page), `standards:131` (glossed
  laugh), `covering:77` (gesture), `boyfriend:49` (noun, false positive).
  Five pre-existing dialogue hits still unruled: `one-bite:39,51`,
  `two-towels:73`, `clean-plate:163`, `covering:155`.**
- [ ] **Proofread after typesetting** — on-device (Books/Kindle) against the
  built epub: section-rule breaks, italics at chapter boundaries, curly
  quotes/apostrophes, scene-break rendering.
- [x] **Legal/content read** — real-institution exposure (VT identifiability:
  professors, campus police behavior), no quoted lyrics, brand-name usage.
  Counsel sourcing/briefing: `meta-plan-lawyer.md`; per-volume findings sheet:
  `meta-plan-legal-read.md` (Vol 1). **Complete for the ARC/beta round (author
  ruling 2026-09-18.)** All nine risk≥2 items closed without counsel
  (2026-09-13), Dr. Marsh archive leg run and clear, Miranda Holdings resolved
  by canon rename plus the prose naming no entity at all. Deferred to *wide
  release*, not to beta: the ALLi-grade platform consult (category pairing) and
  one flat-fee pre-publication read before Volume 2 or first revenue.
- [ ] **Front/back matter completeness** — dedication and acknowledgments
  decisions; Helen Rivers bio (**copy locked 2026-08-15**, three surfaces in
  `meta-plan-distribution.md` §5 → *Author bio*; use surface 1, the
  About-the-Author, which already ends on the newsletter CTA — remaining work
  is wiring it into `build_epub.py`, not writing it); series page pointing at
  Volume Two; the call-to-action / mailing-list page (the funnel's conversion
  point — required for the indie lane, see `meta-plan-free-sample.md`). All
  three are **wide-release** back matter, deliberately absent from the test
  epub.
- [x] **Capture/retention panel (simulated target readers)** — standing
  instrument, run 2026-09-07/08; contract and results in
  `reviews/capture-panel/SPEC.md`; harnesses `tools/capture_panel.py`
  (4-chapter sample, jacket/cold arms) and `tools/capture_dag.py`
  (full-volume cold-reader model: per-chapter runs, reader-owned decade
  mints, STOP gates). Persona panel = romance-graduate, FSoG-refugee,
  consent-sensitive, dark-romance-control (the wrong-reader control, whose
  stops are successes). What it measures at this stage: per-chapter
  capture/survival, almost-stopped moments, trust-ledger drift, Book Two
  conversion, and the tiered comeuppance funnel. Already produced prose
  revisions (`we-find-out` ch32 consent beat, flag→fix→re-measure loop) and
  the cold-posting framing rule in `meta-plan-free-sample.md`.
  **Re-run triggers:** any substantive revision to a Vol 1 chapter (re-read
  the affected gates, as done for ch32); the Vol 2 draft-complete milestone
  (fresh DAG); before the human beta round (its hypotheses — the ch-2 dip,
  gate-3 cold exposure, comeuppance tripwire — shape that round's question
  set). Simulated readers are hypothesis generators; the human pipeline below
  is the confirmatory instrument.
- [ ] **Beta/test-reader pipeline** — full plan in `meta-plan-test-readers.md`
  (recruit → collect → deliver channel layers, intake screener, Helen Rivers
  recruit copy, behavioral-first question set). Value at *this* stage is
  affective / arousal / reader-implication / drop-off + target-market fit +
  social proof — **not** line/continuity fixes (those passes are done, 2026-08).
  Recruit via BookSprout/BookSirens; collect via StoryOrigin Beta Copies;
  deliver via BookFunnel. Confirm each platform's adult-content ToS first.
