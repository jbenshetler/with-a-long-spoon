---
description: Cross-chapter factual audit — find facts one chapter contradicts in another
argument-hint: "[<slug>... | volN] [--model <id>] [--rebuild-ledger] [--fresh]"
---

Run the **fact audit** (Lane A): find places where the prose contradicts itself
on a matter of fact across chapters. Its sibling is **`tools/orphan_refs.py`**
(Lane B), which catches a different class — references orphaned by an edit —
and needs no model at all.

This is a **mechanical continuity instrument, not a craft review**. It
complements `/wals-scene-review` (craft), `/wals-line-audit` (within-chapter
sentence logic), and `/wals-place-in-novel` (arc). **Flags and advises; never
rewrites prose.**

## What it catches, and why the other instruments can't

The worked case is `not-enough.md`: Pace waits for Vee and *"his body gathered
itself toward … a truck turning in"* four lines before *"her car finding the
narrow drive."* Vee drives a Corolla; the truck is Pace's. A per-chapter
auditor has no way to know what Vee drives — that fact lives in other
chapters. This lane exists to hold the whole volume at once.

## Design (do not turn this into a DAG)

Volume One is ~182k tokens, so the whole volume fits in one frontier-model
prompt. The cold-read and capture lanes deliberately **limit** memory to
simulate a first reader at chapter N; an auditor wants the opposite — **total
recall**. The `audits/` scaffolding is reused; the sequential-memory machinery
is not.

Two passes:

1. **Ledger** — one call over the whole volume producing falsifiable
   attributes (vehicles, garments, marks, layout, named objects, dates, and
   who-knows-what-when). Written to
   `audits/fact-audit/<model>/ledger-vol<N>.md`.
2. **Check** — per chapter: ledger + that chapter → contradictions, to
   `audits/fact-audit/<model>/<slug>.md`.

`audits/` is outside the `na.py` index by design — machine flags must never
enter canon search.

## Run

```
tools/fact_audit.py --model gpt-5.6-sol --volume 1 --ledger-only
tools/fact_audit.py --model gpt-5.6-sol --slugs not-enough
tools/fact_audit.py --model gpt-5.6-sol --volume 1
```

Restartable: existing reports are skipped unless `--fresh`. The ledger is
reused unless `--rebuild-ledger`. Each report records a `prose-sha`, so a
later edit makes it **verifiably** stale rather than silently so.

**Auth.** `gpt-5.6-sol` and `gpt-5.5` run on codex subscription — free, and the
default. `claude-*` uses the headless clean lane. An OpenRouter id (containing
`/`) is rejected until given an `[openrouter.policy.*]` tag in
`ensemble-config.toml`; never spend paid tokens here without author
authorization.

## Multiple models

Thoroughness comes from **independently derived ledgers**, not from re-running
one model. Build a ledger per model, then compare: where two ledgers disagree
on a falsifiable fact, either the prose is ambiguous or one model confabulated
— both worth knowing. `--diff-ledgers A B` locates the pair for review.

Treat a ledger as a *derived artifact, never an oracle*. Blind-reader
checkpoints in `reviews/cold-read/` record reader errors (one says "Miranda
Holdings, LLC" where canon is **Miranda Interests, LLC**), and a ledger can do
the same. A contradiction against the ledger is a question, not a verdict.

## Reviewing with the author

Same discipline as `/wals-line-audit`:

1. Read `meta/meta-triage-<slug>.md` first — drop anything restating a
   "left standing" verdict, and say so.
2. One item at a time, severity order. Quote the passage from the file
   (`rg`/`Read`) — **do not trust the report's quotes blindly**.
3. Offer lettered options with a recommendation; wait for the ruling.
4. **Push back honestly when a finding dissolves.** The auditor over-flags by
   design. Variation in how a thing is rendered is this book's normal register
   — "a soft drapey thing in no particular color" is not a contradiction of a
   named garment. Worked example: `the-bench` «massage table» looks like an
   orphan, but the preceding sentence re-establishes the association in place,
   so it stands.
5. Record left-standing items in `meta/meta-triage-<slug>.md` so they are not
   re-litigated.

**Precedence (author ruling 2026-09-19):** prose-vs-prose contradictions are
defects. Divergence from `meta/` is **lower precedence — useful, not an
error**; report it separately and never as a defect. When prose and a planning
doc disagree, that is an authorial decision, not a bug.

Reviews and audits are **reactions to** the novel, never canon.
