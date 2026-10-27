# Editorial procedure — road to publication

*The pre-publication passes, in the order they run. This doc defines each pass:
what it catches, its instrument, where its state lives, what must be settled
before it runs, and what edits make it stale. **Progress is not recorded here**:
it lives in one status doc per volume (`meta-plan-editorial-status-vol<N>.md`)
and in each pass's own `STATUS.md`. First recorded 2026-08-01 from an editorial-pipeline review;
restructured into phases 2026-10-27.*

## How the order works

- **A pass runs after every pass that can invalidate it.** Cutting passes change
  facts, break callbacks and shift dates, so the passes that verify those run on
  the text the cuts leave. A verification pass run before the cuts has to run
  again after them.
- **Stale is a status.** A pass is complete only for the prose it read. When a
  later edit lands in a chapter the pass covered, the pass is **stale** for that
  chapter. Each entry below says what makes it stale.
- **Re-run the delta, not the book.** A stale pass is re-run on the chapters
  changed since it last covered them (`git log --since=<pass date> -- scenes/`),
  and `tools/ruling_anchors.py` names the settled rulings those edits broke.
- **A chapter merge, split or insertion stales everything after Phase 0**
  for the chapters it touches, and any record keyed by chapter number.
- **Per-edit steps are not passes.** CLAUDE.md (*Before writing any prose*)
  requires lint, the orphan check, the praise check and the fact check on every
  edit. Those keep a revision clean; they do not replace the systematic sweep.
- **Every instrument flags; the author rules.** Token rule throughout:
  subscription lanes by default; OpenRouter is paid and needs the author's
  authorization for each run.

---

## Volumes

**The procedure runs per volume.** Each volume moves through the phases on its
own, with its own status doc. Volume membership and order come from
`tools/volume_scenes.py` (titles from `meta-blurb.md`); never restate the
chapter lists here.

- **A volume enters pre-publication when its drafting is complete.** Before
  that, only the per-edit steps apply. Phase 0's exit (structure declared
  final) is per volume.
- **Status docs:** `meta-plan-editorial-status-vol1.md`,
  `meta-plan-editorial-status-vol2.md`. A volume gets one when it enters
  pre-publication.
- **Volumes may move together.** Running a chapter pass over two volumes at
  once is fine; each volume's status doc records its own chapters.

**Every pass has a scope**, which says how it splits:

| Scope | Passes | How it runs for volume N |
|---|---|---|
| **chapter** | retell, explain audit, close-third, true line edit, reading effort, continuity line audit, ruling anchors, copyedit, style tics, flat interrogatives, age-coded | On volume N's chapters only. Progress is counted per volume. |
| **volume** | line-editor whole-volume pass, capture panel (fresh DAG), legal read, front and back matter, typesetting, proofread, beta round | Once per volume, on that volume as a whole. |
| **cross-volume** | fact audit (Lane A), figure sweep, date check, orphaned references, cross-chapter echo triage | On volume N **against itself and every earlier volume**. These catch a contradiction or a repeat between chapters, and a later volume can collide with an earlier one. |

**Cross-volume collisions are fixed in the later volume once the earlier one
is published.** A published volume is frozen: when volume N contradicts or
repeats something in a published volume, the fix goes in volume N. Before
publication, either side may change, and the author rules which. *(Author ruling
2026-10-27.)* **Volumes publish separately** (author ruling 2026-10-27), so the
rule first applies between Volume 1 and Volume 2. A cross-volume pass is re-run
for each new volume, never skipped because an earlier volume passed it.

---

## Phase 0 — Structure

### Developmental edit
- **Catches:** arc, architecture and thesis problems; chapters that should not
  exist, should merge, or are missing.
- **Instrument:** the `meta/` architecture and thesis; `/wals-scene-review`,
  `/wals-place-in-novel`; cold-read panels (`/wals-cold-read`) and
  `wals-cold-reader-feedback`; triage docs (`meta-triage-<slug>.md`); oracle
  probes.
- **Exit:** the chapter inventory in `meta-plan-chronology.md` is final for
  the volume. **Every later phase assumes it.** The October diptych merges ({{Fed}},
  {{Dear}}, {{How It's Done}}) are part of why the August passes are stale.

---

## Phase 1 — Cutting passes

Passes that remove interpretive or retold text. Run the corpus-driven ones
first (they find what readers said out loud), then the by-eye pass (it finds
the rest), so the author rules on each line once.

### Retell pass
- **Catches:** the prose re-narrating an event the reader has already seen.
  Processing and reception stay; retelling goes. The gap between what Cassie
  and Randi are told is the arc and is never cut across the pair.
- **Instrument:** `meta-plan-retell-pass.md` (test, stacks, gauge).
- **Stale when:** a confidante chapter is added or re-scoped.

### Line-editor whole-volume pass
- **Catches:** interpretive lines no other reader quoted (`explains`,
  `told-after-shown`, `editorial`), verified repeats, and gestures that bleed
  between characters across the volume. Rule: an interpretive sentence earns
  its place when it is the sentence readers quote. Scene shapes (the brunches,
  the meals, the arrival-drink-bed evening) are the structure and excluded.
- **Instrument:** `tools/capture_panel.py --volume --personas line-editor`, then
  `tools/notes_verify.py --volume <record> --uptake`. Contract:
  `reviews/capture-panel/SPEC.md`, "`line-editor` reframed". Cross-chapter
  findings feed `meta-plan-echo-triage.md`.
- **Stale when:** any chapter in the volume is removed, split, inserted or
  substantially revised. Re-run; never patch.

### Explain audit
- **Catches:** a line that states what the prose just enacted, harvested from
  the reader corpus (cold reads and capture gates) and filtered against
  settled triage rulings and the complaining lane's capture score.
- **Instrument:** skill `wals-explain-audit`.
- **Stale when:** the chapter's reads are re-run.

### Close-third pass
- **Catches:** narration that explains a beat already shown, announces a line
  before it is said, recaps, or supplies a motive or verdict from outside the
  POV character. Everything left should be something the POV character senses,
  thinks or feels. Finds what no reader said out loud.
- **Instrument:** skill `wals-close-third`, one chapter at a time by eye.
  State: `audits/close-third/STATUS.md`; batches in
  `audits/close-third/<slug>.md`; rulings in each `meta-triage-<slug>.md`.
- **Needs first:** that chapter's explain-audit and line-editor flags, folded
  into its batch.

---

## Phase 2 — Sentence craft

### True line edit
- **Catches:** rhythm, word-level precision, paragraph pacing, pet
  constructions the linter does not know yet, within-chapter and cross-chapter
  echoes.
- **Instrument:** `/wals-line-edit` (state `audits/line-edit/STATUS.md`);
  `tools/echo_harvest.py` for within-chapter repeats;
  `meta-plan-echo-triage.md` for returning phrases and gestures across
  chapters.
- **Stale when:** the chapter is revised.

### Figure sweep
- **Catches:** repeated metaphors and similes across the whole book: the same
  picture returning in different words ("like a missed stair", "the rail on a
  stair", "climbing the same stair"), one picture applied to different people
  (the lamp that is Randi's attention and Vee's presence), and different
  pictures rendering one sensation (the missed stair, the floor going out, the
  high-board drop). Readers remember a figure; reuse spends it. Word search
  cannot find these (a figure returns in other words), so extraction is a
  model reading in context.
- **Instrument:** skill `wals-figure-sweep`; `tools/figure_harvest.py`
  (extraction on `claude-sonnet-5-5` and `gpt-6.1-terra`, unioned; local
  grouping); acceptance set `audits/figures/gold.md`; state
  `audits/figures/STATUS.md`.
- **Needs first:** Phase 1 complete for the volume (cuts remove figures).
  **Gate:** the gold set must pass before any volume run. Re-run the gold
  chapters first if either model has changed.
- **Run at pre-publication** (author ruling 2026-10-27), per volume:
  `extract --volume N` for each model, then `group --through N` so the
  volume's figures are grouped with every earlier volume's. About 25–35
  minutes per model per 24 chapters, in parallel on subscription lanes.
- **Stale when:** a chapter is revised (each record carries its prose sha).

### Reading-effort sweep
- **Catches:** sentences that charge the reader more than they pay back (one
  idea split across stacked clauses or a sentence boundary) where a
  rearrangement carries the same content at lower cost. Scored against this
  book's own corpus, never an external readability index.
- **Instrument:** `tools/reading_effort.py` (deterministic; `chain`, `strand`
  and `suspend` are the classes that matter) **and** a blind model panel,
  `tools/effort_blind.py`, at least four models. Both are required (author
  ruling 2026-09-20). Work convergent findings (2+ readers) first; a sentence
  one reader flags is noise. State and calibration:
  `audits/reading-effort/STATUS.md`; rulings in `rulings.toml`.
- **Not a per-edit step** (author ruling 2026-09-20): ~87 findings per
  chapter, each needing a ruling.
- **Stale when:** the chapter is revised.

---

## Phase 3 — Verification

Run on the text Phases 1–2 leave.

### Continuity and logic line audit
- **Catches:** sentence-level continuity and logic errors inside a chapter.
- **Instrument:** `/wals-line-audit` (state `audits/line-audit/STATUS.md`).
- **Stale when:** the chapter is revised.

### Cross-chapter fact audit (Lane A)
- **Catches:** a fact established in one chapter contradicted in another,
  which the linter, the lore-keeper and a cold reader are each blind to. Worked
  case: in `the-usual.md` Pace waits for a truck four lines before *her car*
  finds the drive, and Vee drives a car.
- **Instrument:** `tools/fact_audit.py` / `/wals-fact-audit`; ledgers per model
  in `audits/fact-audit/<model>/`; state `audits/fact-audit/STATUS.md`.
  **Independent ledgers across vendors** (a second vendor is what finds real
  problems, `b082c4f6`); keep what more than one lands on. **One ledger over
  the volume and every earlier volume** (cross-volume scope, above), never a
  ledger of one volume alone: that cannot see the cross-volume contradiction
  this pass exists to catch. **Dates are out of scope** (the date
  check below owns them).
- **Stale when:** any chapter in its scope is revised.

### Date check
- **Catches:** a date, weekday or interval in the prose that disagrees with the
  chapter's date. Chapters now print their date at the top, so a "Friday" in
  the prose under a Sunday heading is visible to every reader.
- **Instrument, two halves:**
  - **Headings: built.** `tools/chapter_dates.py` is the sole source of
    chapter dates; the epub takes its date lines from it, and `--check` runs
    in pre-commit (weekday against the hidden calendar; multi-day section
    anchors still present).
  - **Prose claims: not built** (open question #48). Weekday names,
    "yesterday", "N days/weeks", "in October", "before Thanksgiving", checked
    against each chapter's date. Deterministic, built on `chapter_dates.py`,
    never a second parser. It replaces the 2026-08-03 timeline sweep
    (`audits/timeline/`), which is keyed to old chapter numbers.
- **Stale when:** a chapter is revised or its chronology date moves.

### Orphaned-reference sweep (Lane B)
- **Catches:** text still pointing at something a revision removed. Worked
  case: a cut passer-by "in a camel coat" whose later callback, "the closed
  camel-coat project", survived the cut.
- **Instrument:** `tools/orphan_refs.py`; sweeps and state in
  `audits/orphan-refs/`. Deterministic and free, so it is also a per-edit step
  and an advisory pre-commit hook; neither replaces the front-to-back sweep
  (the hook sees only staged paths).
- **Needs first:** every cut in Phases 1–2.

### Ruling-anchor check
- **Catches:** settled rulings (line audit, line edit, triage) whose quoted
  prose an edit has since changed, so the ruling no longer applies to what is
  on the page. These go stale silently, unlike linter acks, which re-arm.
- **Instrument:** `tools/ruling_anchors.py`. Deterministic and free.
- **Runs:** after each revision round, and as the input to every delta re-run.

---

## Phase 4 — Mechanics

### Copyedit against the style sheet
- **Catches:** names and spellings, places, hyphenation, numerals, italics
  conventions, dash and ellipsis rules, capitalization of recurring objects.
- **Instrument:** `style/style-sheet.md`. Curly quotes are converted at
  typesetting.
- **Stale when:** the chapter is revised.

### Style-tic policing
- **Catches:** the book's known tics and canon breaches, by closed vocabulary.
- **Instrument:** `na.py style` with `style/style-rules.toml` and
  `style/style-allow.toml`. A per-edit step; the pre-publication pass is one
  whole-volume run with every remaining `ASK` hit ruled.

### Flat-interrogative sweep
- **Catches:** a question closed with a period or comma where a person saying
  it would voice it as a question, in every register: dialogue, italic
  interiority, recalled speech (author ruling 2026-09-20). Flat only where the
  page marks it as not really asked; recalled Cassie stays flat by design.
- **Instrument:** `na.py style` rule `flat-interrogative` (its live hit list is
  the state). **Blind spot:** an elliptical question with no interrogative
  word (*Your folks coming up.*) needs a human eye. The assistant's bias is
  one-directional (it drops marks), so when in doubt, mark it.

### Age-coded language sweep
- **Catches:** narration in sex scenes that could suggest a minor to a
  retailer's screen: "girl" in narration, especially beside words stressing
  smallness or youth. Prefer her name or "woman" there. **Dialogue is out of
  scope.** Retailers' sensitivities come from author-community experience, not
  a published list; Draft2Digital and Apple are stricter than Amazon.
- **Instrument:** none yet; by eye, per volume. Flag, never fix; an
  erotica-experienced editor's assessment has the final word. Jacket, title
  and metadata are covered by the blurb rule in `meta-blurb.md`.

---

## Phase 5 — Reader confirmation

### Capture/retention panel
- **Measures:** per-chapter capture and survival, almost-stopped moments,
  trust-ledger drift, Book Two conversion, the comeuppance funnel. Simulated
  readers generate hypotheses; the human beta round confirms them.
- **Instrument:** `/wals-capture-read`; `tools/capture_panel.py`,
  `tools/capture_dag.py`; contract `reviews/capture-panel/SPEC.md`. Personas:
  romance-graduate, FSoG-refugee, relationship-first; consent-sensitive and
  line-editor on request.
- **Re-run:** the gates of any substantively revised chapter
  (`capture_dag.py --check-stale` lists them; staleness is a warning, never a
  blocker); a fresh DAG at a volume's draft-complete milestone; before the
  human beta round.

---

## Phase 6 — Package

### Legal and content read
- **Catches:** real-institution exposure (Virginia Tech identifiability,
  professors, campus police), quoted lyrics, brand names.
- **Instrument:** `meta-plan-legal-read.md` (findings, per volume);
  `meta-plan-lawyer.md` (counsel). A publication-time tail is scheduled there.

### Front and back matter
- **Covers:** dedication and acknowledgments; the author bio (copy in
  `meta-plan-distribution.md` §5, surface 1); the series page pointing at the
  next volume; the call-to-action / mailing-list page
  (`meta-plan-free-sample.md`). All are wide-release matter, deliberately
  absent from the test epub.

### Typesetting
- **Instrument:** skill `wals-epub` (`tools/build_epub.py`).

### Proofread after typesetting
- **Catches:** on-device (Books, Kindle) against the built epub: section-rule
  breaks, italics at chapter boundaries, curly quotes and apostrophes,
  scene-break rendering, and **the date lines**: each later day's line at the
  right section break, and chapters without an exact date rendering as
  intended.
- **Needs first:** every earlier phase.

---

## Phase 7 — Readers

### Beta / test-reader round
- **Value at this stage:** affective response, arousal, reader implication,
  drop-off, target-market fit, social proof. Not line or continuity fixes.
- **Instrument:** `meta-plan-test-readers.md` (recruit via
  BookSprout/BookSirens; collect via StoryOrigin Beta Copies; deliver via
  BookFunnel; confirm each platform's adult-content terms first).

---

## Gaps in the instruments

Not yet built; tracked here so the procedure does not pretend otherwise.

- **Date check, prose half** (open question #48).
- **Delta re-run tooling:** a skill or `--since <ref>` mode that lists, per
  verification pass, the chapters changed since it last covered them.
- **Reading-effort skill:** the tool + panel protocol lives only in prose.
- **Orphan-sweep walk:** the first sweep's candidates have no walking skill.
- **Age-coded rule:** a narration-only `na.py style` rule would make this
  sweep a hit list, as `flat-interrogative` is.
- **Proofread aid:** epubcheck plus a per-chapter device checklist.
