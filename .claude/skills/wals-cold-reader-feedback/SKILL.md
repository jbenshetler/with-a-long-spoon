---
name: wals-cold-reader-feedback
description: >-
  Turn the cold readers' reviews of a drafted scene into an actionable revision
  plan: pull every model's cold-read review of the scene, synthesize the
  cross-model feedback (net of triage verdicts already settled), plan concrete
  changes, and walk them past the author for approval before touching any
  prose. Use when the author asks to act on / triage / apply the cold-read
  feedback for a scene. Flags and proposes; applies only what the author
  approves.
---

# wals-cold-reader-feedback — from cold-read reviews to approved revisions

Input: a scene slug (e.g. `lesson`). If the author didn't give one, ask which
scene before doing anything.

Reviews are **reactions, not canon** (CLAUDE.md). This skill is the one
sanctioned place they drive work — as *feedback about how the prose lands*,
never as facts about the book. When a reviewer asserts a fact, verify it
against canon via the lore-keeper before treating it as real.

## Step 1 — Gather

In parallel:

- Read every `reviews/cold-read/*/<slug>.md` that exists — the
  `## Reader reaction` section is the payload (skip `## Carry-forward state`).
  Note which models reviewed the scene; if none exist, stop and say so
  (suggest running `/wals-cold-read` first).
- Read `meta/meta-triage-<slug>.md` if it exists. Its **"left standing —
  do not re-litigate"** verdicts are authorial decisions: drop any review
  criticism they cover unless the flagged passage has since been edited or a
  reviewer surfaces a genuinely new failure mode (not the same criticism
  restated). If you re-raise one anyway, say explicitly that you're
  contradicting a recorded verdict and why.
- Read `scenes/<slug>.md` in full — you need the actual prose to judge the
  criticism and to quote candidate lines.
- Run `tools/novel-assistant/na.py style scenes/<slug>.md` (via the `na`
  skill's canonical form) — style hits that coincide with reviewer friction
  are stronger candidates.

## Step 2 — Synthesize across models

Cluster the feedback; do not relay reviews model-by-model. For each distinct
point, record: what was said, **which models raised it** (consensus across
models is the strongest signal; a lone reviewer's pet reading is the weakest),
the quoted line(s) at issue, and whether triage already settled it.

Sort every point into:

- **Confirmed positives** — what's landing. These are *protection*, not
  praise: a fix must not damage them.
- **Actionable friction** — prose-level problems worth the author's knife
  (typography, a line pulling readers out, machinery humming too close to the
  surface, a seed pitched too loud/quiet).
- **Working-as-designed** — the reviewer felt exactly what the design intends
  (a cold reader trusting someone they shouldn't, unease the book planted).
  Verify against the scene's plan via a **lore-keeper** lookup (its chronology
  entry, condensed/note docs, operative craft rules) before classifying —
  don't assume; and never explain the design back in terms that leak spoilers
  into a fix.
- **Not actionable** — taste, contradicts canon/triage, or would require the
  reviewer to know things a cold reader can't.

## Step 3 — Plan the changes

For each **actionable** item, propose a concrete change: the exact line(s)
quoted, the specific risk the reviewers identified, and the proposed edit or
2–3 options where the choice is genuinely the author's. Keep proposals in the
scene's established register; check any fix that touches canon, chronology, or
another scene with the lore-keeper first. Honor the craft rules — no
editorializing, no telegraphing, never-name is absolute.

## Step 4 — Author approval, item by item

Present the synthesis (positives first, then the plan, then what you set
aside and why). Then walk the actionable items past the author — use
AskUserQuestion per item or batch, with apply / modify / reject / defer as the
choices. **Nothing is applied until approved.** The author may also redirect a
fix; re-plan rather than push the original.

## Step 5 — Apply and record

For approved items only:

1. Apply the edits to `scenes/<slug>.md`, then rerun the style linter on the
   scene; surface any new hits (an edit re-arms suppressions — that's correct).
2. Offer to write/update `meta/meta-triage-<slug>.md`: what was flagged, what
   was fixed (with the commit once made), and — the payload — what was **left
   standing with rationale**, so later passes don't re-litigate. Rejected and
   working-as-designed items go here.
3. Do **not** add a `reviewed:` date to the chronology — only the author
   records a review. Remind them it's available if they consider this pass one.
4. Commit only if the author asks.

Never edit the review files themselves — they are the readers' record.
