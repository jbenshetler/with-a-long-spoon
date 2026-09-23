# Triage — The Long Way (fact-audit pass, 2026-09-21)

Source: `audits/fact-audit/claude-opus-5/long-way.md` (Lane A cross-chapter
fact audit, first ten Vol 1 chapters, seven-model comparison). Singleton
finding — no other model flagged it.

## Left standing — do not re-litigate

- **:35 / :51 the froyo "system" is not self-contradictory.** The audit read
  *"Tart on the bottom holds up under the heavy ones. You put chocolate on
  tart and it's an argument the whole way down"* as a rule that negates
  itself, with the payoff at :51 (*"Your tart's holding up"*) validating only
  the first half. It does not. The first clause is **structural** — a tart
  base bears weight — and the second is about **flavor**: chocolate is the
  named exception to an otherwise general rule, not a counterexample to it.
  The :51 payoff is purely structural (*"the whole stack of it, still
  standing"*), so it confirms the first clause and never engages the second.
  Ordinary spoken advice, not a defect.
  - The audit's stated reason — that this is "the signature of one sentence
    being edited and the other left" — is **false**. Both lines entered in
    the same commit (`9b615e77`, 2026-07-13) and neither has been touched
    since; `git log -S` on either phrase returns only that commit. The model
    asserted a diff history it cannot see.
  - Considered and **not** taken: recasting *"the whole way down"* to drop
    the vertical, which is what lets the flavor clause lean on the structural
    one. The lines stand as written.

---

# Triage — The Long Way (line-edit pass, 2026-08-05)

Source: `audits/line-edit/long-way.md` (3 findings + linter slate), reviewed
item-by-item with the author, with cold-read enrichment (all four
`reviews/cold-read/*/long-way.md` reactions mined before ruling).

## Fixed (line edit)

- :39 narration simile recast off the "like a man" frame: "as if he'd set
  something down exactly where he meant it to go" — Randi's designed pair at
  :11 now sole owner of "like a man"; also clears the `a-small` linter hit.
  Wording is the assistant's, accepted.
- :41 "on the scale" cut ("He weighed his own cup and paid for both…") —
  weighed doubles the scale; no reader had quoted the sentence.
- Linter acks (author sign-off): :41 "she heard her mother"
  (`#7833971a1c9e` — hearing vs. not-hearing is the beat's mechanism), :49
  "She heard how it landed" (`#5561498dece8` — hearing her own line from
  outside is the beat), :41 "on the way past" (`#7d3d04250e55` — literal
  path sense, false positive), :43 "the way her grandfather used to ask"
  (`#5c6a0d396fe5` — grandfather paragraph, reader-protected).

## Left standing (line edit) — do not re-litigate

- **:9 "It was easier to go looking for the flaw than to sit in the
  wanting." — reader-protected.** The audit called it overwork (narrator
  naming the deflection the dialogue shows), but all four cold readers
  praised the exact line (fable "exactly the girl I've come to know"; opus
  "I love her for this and I ache for her"; gpt-5.5 "so recognizably
  human"; sol approving echo). The gloss is doing warmth-work. Do not cut
  or thin.
- **:11 Randi's "like a man" pair** — designed parallel, quoted approvingly
  by opus and gpt-5.5; stands untouched.

---

# Triage — The Long Way (line-audit pass, 2026-08-01)

Source: `audits/line-audit/long-way.md`, reviewed with the author.
**Left-standing entries are authorial decisions — do not re-flag without new
evidence.**

## Fixed

- "knowing it would drip" → "knowing the cup would drip" (bitten-lip misparse).
- Chronology `present:` gained Cassie.

## Left standing — do not re-litigate

- **Face-down phone read without a narrated flip** — ordinary ellipsis;
  "here it was" carries the pickup; the face-down detail stays.
