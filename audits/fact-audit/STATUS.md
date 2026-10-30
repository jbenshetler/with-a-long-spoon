# Fact audit (Lane A) — status, Volume One

Cross-chapter factual audit: a fact established in one chapter **contradicted in
another** — the class the style linter (closed vocabulary), the lore-keeper
(answers only what it's asked), and a cold reader (holds no other chapter) are
each structurally blind to.

Harness `tools/fact_audit.py` / `/wals-fact-audit`. Per-model reports at
`audits/fact-audit/<model>/<slug>.md`; each model's accumulated fact ledger at
`audits/fact-audit/<model>/ledger-vol1.md`; prompts at
`audits/fact-audit/prompts/`. Pass tracked in
`meta/meta-plan-editorial-checklist.md` (Lane A).

**States:** `pending` → `audited` (reports on disk, not yet ruled) → `reviewed`
(author ruled; fixes committed, standing items recorded).

**Discipline: over-flags by design, and the author rules on every item.** Flags,
never findings. A model's `## NOTED (not errors)` section is deliberately not a
defect list. **Dates are out of scope for this pass** — the whole-book timeline
sweep (`audits/timeline/`) owns elapsed-time claims, and re-litigating them here
produces noise, not findings.

**Multi-vendor by design.** Five models across four vendors, so a finding that
only one model sees can be weighed against four that didn't. Author ruling
2026-09-19 (`b082c4f6`): a *second vendor* is what surfaces real problems — keep
cross-vendor breadth rather than adding depth within one family. Token rule:
subscription lanes are the default and need no permission; **OpenRouter is paid
and needs the author's explicit authorization each run.**

## Coverage — partial restart 2026-10-23

Per-edit check of merged `fed` completed on gpt-5.6-sol against a new Volume One ledger: **no contradictions of fact found** (`gpt-5.6-sol/fed.md`). The initial merge retained both passages verbatim; a fresh check after the approved 225-word retelling reduction also found no contradictions. Rechecked after the subsequent 85-word explanation pass, again with no contradictions. Report and ledger are on disk; no author rulings have been made on the report's non-error observations. This limited per-volume check does not complete the preferred whole-book audit below.

### Reset history — 2026-10-09

**The lane was dumped and will be regenerated when the author is ready to run
it** (author ruling 2026-10-09). What was discarded: 72 chapter reports across
7 models covering 12 of 79 drafted chapters (~15%), plus 7 whole-fall
`ledger-vol1.md` files. Recoverable from git at `62b06759`.

Why dumping cost nothing:

- **Zero adjudications.** Every report was `audited`, none ever `reviewed` with
  the author, so no settled verdict was lost — only raw model output.
- **The ledgers were stale** by 76+ prose commits since 2026-09-19.
- **The volume labels had moved.** `ledger-vol1.md` meant *the whole fall*; the
  2026-10-09 split made Volume One 27 chapters, so the scope label no longer
  described the contents.
- Coverage was 15%, so a fresh run is closer to starting the pass than resuming
  it.

Kept: `prompts/` (the ledger/check/system templates — inputs, not output) and
this tracker.

**When it is re-run**, two findings from the 2026-10-09 investigation apply:

1. **Every lane on the roster is 1M-class** (ceilings now recorded in
   `tools/cold_read_pricing.toml`). The whole book is ~350k tokens, so a
   **whole-book ledger** fits everywhere.
2. **Per-volume ledgers are structurally blind** to the defect this lane exists
   to catch — a fact established in one volume contradicted in another. Four
   books means four blind seams. Prefer one whole-book ledger, with per-volume
   ledgers only as a fallback.


## Restart

1. Rule the audited-not-reviewed chapters with the author, chapter by chapter,
   in epub order — read the five models' reports for one chapter together, since
   agreement across vendors is the signal.
2. Record rulings as they land (see below), then continue the sweep from
   chapter 11.
3. Re-run any chapter whose prose changes afterward: each report header carries
   a **prose-sha**, so a stale report is detectable rather than silently trusted.

## Rulings

**None recorded yet.** When the author rules, the verdict goes in the chapter's
`meta/meta-triage-<slug>.md` — authorial decisions live in `meta/`
(default-indexed), not under `audits/`, and the triage docs are what stop a
settled criticism from being re-litigated by a later pass. Note here only that
the chapter reached `reviewed` and where the verdicts landed.

## Per-edit checks (moved from the editorial checklist, 2026-10-27)

Limited per-edit checks against an existing ledger. None of them completes the
whole-book pass.

- **Per-edit check 2026-10-23:** merged *Fed* (former *Toenails* plus *Fed*,
  both passages verbatim) checked by gpt-5.6-sol against a freshly derived Volume
  One ledger; no factual contradictions flagged. Rechecked after the subsequent
  225-word retelling reduction, again with no contradictions flagged. Rechecked
  after the further 85-word explanation pass: no contradictions flagged. This
  limited check does not complete the whole-book, cross-volume Lane A pass.
- **Per-edit check 2026-10-23, Dear diptych:** gpt-5.6-sol checked both merged
  movements against the existing Volume One ledger; no factual contradictions
  flagged. Limited per-edit check only.
- **Per-edit check 2026-10-23, How It’s Done diptych draft:** gpt-5.6-sol
  checked the merged chapter against the existing Volume One ledger. Final run
  found no factual contradictions. First-run room flag was already settled in the
  Turned Up triage. Limited per-edit check only.
- **Per-edit check 2026-10-23, How It’s Done explanation draft:** gpt-5.6-sol
  rechecked the 22-word reduction against the existing Volume One ledger; no
  factual contradictions flagged. Limited per-edit check only.
- **Per-edit check 2026-10-23, How It’s Done author restoration:**
  subscription check retained; its two flags compare the old ledger’s chapter
  18/19 citations with merged chapter 17. They concern approved structural
  renumbering, not changed events. No prose fix made from them.
- **Per-edit check 2026-10-23, How It’s Done approved after-explanation
  cuts:** subscription fact check repeated the already-settled Cassie
  living-room/sun-porch shorthand; no new issue from the cuts. Limited per-edit
  check only.
- **Per-edit check 2026-10-23, Gone workshop restoration:** gpt-5.6-sol checked
  the restored bedroom sequence/new kitchen aftermath against the existing Volume
  One ledger. Three flags compare older scene numbers with the current merged
  chronology (Sorority before Gone); no new factual conflict identified by
  continuity review. Raw report retained; no automatic prose fixes. Workshop
  draft pending author review, limited per-edit check only.
- **Per-edit check 2026-10-23, Gone conference revision:** gpt-5.6-sol checked
  the replacement of the proof discussion with the prior Chicago presentation.
  Only flag compares old ledger chapter 25 with current chapter 23; no new
  factual conflict flagged. Limited per-edit check only.
- **Per-edit check 2026-10-30, palate-thread pass:** gpt-5.6-sol built a new
  Volume Two ledger (`ledger-vol2.md`) and checked *Above Him*, *In His Hands*,
  *The New Ordinary*, *Under the Rug*, *Believe Me* and *Nothing Underneath*.
  One flag (MEDIUM): *Under the Rug* `:95` "couldn't hear herself say
  [*boyfriend*] to her mother" against *Cropped* `:35` ("I told them he was my
  boyfriend… a question mark on it"); the line predates the pass. Awaiting
  author ruling. *Nothing Underneath* was edited again after its check (cut
  and smile beat, no fact change), so its report is stale by prose-sha.
