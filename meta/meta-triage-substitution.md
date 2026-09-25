# Triage — Substitution (fact-audit pass, 2026-09-23/24)

Source: `audits/fact-audit/*/substitution.md` (Lane A cross-chapter fact
audit). Seven models run; two corroborated findings, both seating geometry,
both fixed. Model tally on this chapter: `claude-opus-5` 2, `gpt-6-astra` 2,
`claude-fable-5-1` 1, `gemini-3.8-flash` 1 (a false positive, below);
`glm-5.3`, `gpt-5.6-sol`, and `gpt-5.5` returned none.

## Fixed

- **:37 Cassie's locative cut** — "when she looked up again Cassie, two tables
  over, was watching Randi thumb at her phone" → "when she looked up again
  Cassie was watching Randi thumb at her phone". Three other locatives put her
  at the *next* table (:15, :81, :95), and so does this scene's own brief:
  "Cassie, at the next table, clocks the text for what it is and goes still"
  (`meta-condensed-substitution.md:5`) — which is this very beat. Four to one.
  - Contamination source identified: "two tables over" is Cassie's canonical
    prop phrasing — "headphones (volume low enough that she laughs at things
    said two tables over)" (`meta-arch-cassie.md:94`), first drafted in
    `see-you-later.md` and carried into :15 here as "two tables away". The
    character's own prop description resurfaced twenty lines later as a
    locative.
  - Cutting rather than correcting in place: the chapter already says "next
    table" three times, and :37 does not need the reminder.

- **:15 Randi is beside Vee, not across from her** (corroborated by
  `claude-opus-5` and `gpt-6-astra` — 2 models, 2 vendors). "looked across the
  table at Randi" → "looked over at Randi". Two later passages put her beside
  Vee (":67 Beside her, Randi's hand moved to her coffee cup", ":149 Beside
  her, Randi's hand went to her coffee cup"), and :67 lands while Pace is
  still crossing the floor — he does not sit until :81 — so no seat change can
  reconcile them. The settled geometry is Vee and Randi side by side with Pace
  opposite, which :201 confirms ("the man across from her") and :81's singular
  "the empty chair at their table" fits.
  - Why "beside" wins rather than "across": both Beside-her lines run a
    mechanism — Vee's attention is on Pace while Randi's tell registers at the
    edge of vision, which is how the brief specifies Randi's tells be
    delivered ("rendered as Vee perceives-and-misprocesses them",
    `meta-condensed-substitution.md:5`). Seating Randi opposite would force a
    direct look and spend the tell.
  - Not evidence against: `long-way:11` "She slid it back across the table",
    same table twenty minutes later — read as sliding over the tabletop, not
    as a seat position.

## Not a defect — model error

- **`gemini-3.8-flash`'s only flag here is a ledger confabulation.** It flagged
  :217 ("He typed it into his phone, repeated it back to her once to confirm,
  and pocketed the phone") against its own Fact Ledger §5, which claims Pace
  "leaves his number with Vee". The prose is correct — he takes *her* number,
  and {{The Long Way}} turns on exactly that ("She'd given him hers; it hadn't
  occurred to her to ask for his"). The same bad ledger entry produced a
  HIGH-confidence false positive against `long-way:7`. Tell for the class: the
  AGAINST side cites a ledger line rather than a passage.

## Left standing — do not re-litigate

- **Cassie stays at her own table; she is not moved to Vee and Randi's.**
  Considered 2026-09-23 on the reasonable grounds that three girls studying
  together would share a table. Declined: Cassie is *not* in the study session
  (":15 with her own work spread out … headphones in", ":45 Cassie returned to
  her work"), so two tables is the natural staging, not the odd one. The move
  would also cost five touches including a line of dialogue whose shape
  depends on the gap — ":39 'How's it going over there?'" — and the wave at
  :95; and it raises the Cassie–Randi interaction pressure that
  `meta-arch-cassie-randi.md:71` exists to keep low ("They barely interact …
  The power is in how little needs to happen").

---

# Triage — Substitution (line-edit pass, 2026-08-05)

Source: `audits/line-edit/substitution.md`, reviewed item-by-item with the
author; 15 findings + a bonus linter slate, with the cold-read enrichment step
(all four `reviews/cold-read/*/substitution.md` reactions mined before ruling —
unanimous friction point: the :137 "The way he had…" litany runs a hair long,
saved by "The thought did not finish").

## Fixed (line edit)

- :35 "the small private focus" → "the private, absorbed focus of a girl
  writing to someone who had her attention" — clears the FIX-AT "small
  private" echo while keeping the tell (Randi caught up in a hurried note to
  Pace, not meant to be noticeable).
- :15 "her own laptop … her own work" thinned to one "her own" (kept on
  Cassie's work).
- :61 closing sentence cut ("…she had been being looked at for what felt
  like, but could not have been, a long time.") — author flagged that the
  pair made him seem to cross the floor looking at her twice; :71 is now the
  sole owner of the crossing's duration. Paragraph ends "Something in her
  chest went quiet."
- :63 "He was looking at her." cut; "He stopped at the corner." kept — it now
  carries arrival after the :61 cut.
- :65 "She felt singled out." cut; "She felt, absurdly, chosen." stands alone
  — **restore-watch** (see Left standing).
- :87 "the room tilting half a degree toward her" cut — the room-instrument
  image lives only at :65 on Pace; the sentence lands on "the borrowed poise
  sitting on her better than she'd expected."
- :81 "Both women returned the brief acknowledgment." cut.
- :85 "filed it" → "tucked it away to try on later" (filing-frame retirement).
- :137 credential aside halved: single "was," econ-eye aside tightened to
  "she could see it with her econ eye, the eye for *how a smart person
  handles a problem they could handle in any of several ways*" — the direct
  fix for the unanimous reader flag; italics (praised) kept.
- :137 "clock" → "the kind of beat she would not catch until later".
- :149 narrated summary sentence cut ("Randi's question had gotten the
  answer it had asked for…"); "filed it without filing it" untouched
  (designed, previously suppressed).
- :161 "in her experience" cut (:213's instance kept); "She did not know the
  polite-short answer to that question; it would have to be invented. She
  decided to skip inventing it."
- :171 tidied: "about a research project she wanted to do — not started, but
  thought about, and never articulated to anyone in this much detail,
  because no one had asked."
- :175 "The smile was warm and unbothered." cut — the italic *go on, this is
  nice* smile carries it.
- "small" sweep: cut at :15 (social registers), :27 (*of course you do*
  smile), :95 (wave), :175 (mental note); kept :7 curl, :55 *huh*, :103
  unfinished way, :153 sip.
- :203 recast per author direction (softer but humiliating, meet-cute
  register): "What went through her at the glance made her want to fall
  through her seat — she was embarrassed to be looking at him and could not
  look anywhere else." Wording is the assistant's, accepted; "embarrassed"
  flagged as possibly stating too much.
- :213 "and to respond to it" cut ("her body had already responded" carries
  it); "she registered" → "she understood".
- Linter acks (author sign-off): :97 "registering names properly"
  (`#2990c62b378b` — the got-it nod carries it) and :175 "registered the
  small busy-ness" (`#5a07d4d59085` — edges-of-attention registering is the
  misread mechanism).

## Left standing (line edit) — do not re-litigate

- **:65 "She felt, absurdly, chosen." — RESOLVED (2026-08-05 re-run).** The
  span stands without its "She felt singled out." lead-in: the post-edit
  re-run quotes it verbatim (fable, opus) and the chosen-motif stays central
  for both GPT readers. Author ruling: watch removed; the cut is final. Do
  not restore the pair.
- **:137 "The way he had…" litany** — designed anaphora; all four readers
  flag it as running "a hair long" but all four also say "The thought did not
  finish" saves it. The credential-aside trim above is the fix; do not thin
  the litany itself.
- **:61 / :223 "in her chest"** — the two keepers after the pass; do not
  further thin.
- **:137 "She felt —" filter-verb hit** — the body-ahead-of-mind beat itself;
  linter hit stands unruled, not a defect.
- **Warm at :87/:171** — reader-engaged spans; left.

---

# Triage — Substitution (line-audit pass, 2026-08-01)

Source: sentence-level consistency audit (`audits/line-audit/substitution.md`),
reviewed item-by-item with the author. **The "Left standing" section records
authorial decisions — do not re-flag these without new evidence.**

## Fixed

- **"On Monday" → "the day they'd met"** (audit item 1) — the watched name-line
  performance is the Cassie bit in {{See You Later}} (Wed Sep 9, per the
  condensed brief); the rewording also ties Vee's borrowed routine to the day
  Randi chose her.
- **Chronology `present:` now includes Cassie** (audit item 2).
- **"Forty minutes" → "an hour" in the break exchange** (audit item 3) —
  matches the narration's 40 + 20 total.
- **"The pencil sat in the gutter between the pages" → "The pencil lay across
  the page"** (audit item 4) — the work is a single loose sheet throughout
  (handed over, "would not bend," turned to show scratch work); no bound
  object exists in the scene.

## Left standing — do not re-litigate

- **Pace overhearing Vee's "to the table, to nobody" line** (audit item 5) —
  author framing: the counter line is deliberately close enough to the table
  for a plausible overhear — on the page, "He had a few steps to cover."
  "To the table, to nobody" names the addressee, not the volume. The overhear
  is plausible on first read; do not raise her volume or loosen his opener.
