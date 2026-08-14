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
- [ ] **Proofread after typesetting** — on-device (Books/Kindle) against the
  built epub: section-rule breaks, italics at chapter boundaries, curly
  quotes/apostrophes, scene-break rendering.
- [ ] **Legal/content read** — real-institution exposure (VT identifiability:
  professors, campus police behavior), no quoted lyrics, brand-name usage.
  Counsel sourcing/briefing: `meta-plan-lawyer.md`; per-volume findings sheet:
  `meta-plan-legal-read.md` (Vol 1).
- [ ] **Front/back matter completeness** — dedication and acknowledgments
  decisions; Helen Rivers bio (a positioning artifact — write deliberately,
  see `meta-plan-pen-name.md`); series page pointing at Volume Two; the
  call-to-action / mailing-list page (the funnel's conversion point —
  required for the indie lane, see `meta-plan-free-sample.md`).
- [ ] **Beta/test-reader synthesis structure** — fixed question set per
  reader so responses aggregate (test-reader plan: `meta-blurb.md` /
  distribution docs).
