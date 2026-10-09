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

## Coverage — RESET 2026-10-09, nothing on disk

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
