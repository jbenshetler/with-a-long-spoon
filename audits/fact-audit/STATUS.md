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

## Coverage — 10 chapters × 5 models, +2 sol-only

Epub order. All reports below are **audited, none reviewed with the author yet.**

| # | Chapter | opus-5 | gemini-3.8-flash | glm-5.3 | gpt-5.5 | sol |
|---|---|---|---|---|---|---|
| 1 | the-bench | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | standards | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3 | the-pointing-game | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4 | see-you-later | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 | substitution | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6 | long-way | ✓ | ✓ | ✓ | ✓ | ✓ |
| 7 | water-wings | ✓ | ✓ | ✓ | ✓ | ✓ |
| 8 | may-i-choose | ✓ | ✓ | ✓ | ✓ | ✓ |
| 9 | off-six-fourteen | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10 | dear | ✓ | ✓ | ✓ | ✓ | ✓ |
| 15 | a-round | — | — | — | — | ✓ |
| 50 | not-enough | — | — | — | — | ✓ |

**Chapters 11–52 are `pending`** (except the two sol-only rows above).
`not-enough` is the pass's worked case — Pace waits and "his body gathered
itself toward … a truck turning in" four lines before "her car finding the
narrow drive," and Vee drives a car.

Only two reports come back clean: `claude-opus-5/dear.md` and
`claude-opus-5/may-i-choose.md`. **Every other report carries at least one
flagged item, all unruled.**

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
