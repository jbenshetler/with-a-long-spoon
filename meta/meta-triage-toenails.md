# Triage — Toenails (line-audit pass, 2026-08-01)

Source: `audits/line-audit/toenails.md`, reviewed with the author.
**Left-standing entries are authorial decisions — do not re-flag without new
evidence** (audit verdicts re-open on a text edit to the passage).

## Fixed

Nothing — the audit came back clean (1 nitpick only).

## Left standing — do not re-litigate

- **The closing undressing elides the unzip and drops the shower towel**
  (:45 "She let the towel fall, and stepped out of the skirt at last" vs.
  the re-zipped hip-zip skirt at :35 and the towel taken down for the
  shower at :31) — "at last" is the payoff of the aborted :31–35
  undressing; the sentence is a release cadence, not a blocking sequence,
  and an unzip beat would put procedure inside the exhale. The towel
  falling is everything falling — she's alone, the editing is over.

---

# Triage — Toenails (line-edit pass, 2026-08-07)

Source: `audits/line-edit/toenails.md` (5 findings) plus cold-read enrichment
(five readers) and the style linter, reviewed with the author item by item.
**Left-standing entries are authorial decisions — do not re-flag without new
evidence** (line-edit verdicts re-open on a text edit to the passage).

Context for later passes: the **zipper beat** (:31–:33), the **closing line**
(:45), and **"Cassie said it kindly, certainly, wrong"** (:41) drew zero
negative reaction from all five cold readers. Cassie's "Was he worth painting
your toenails? / In October. / I have eyes." is likewise unanimously praised.
None were touched.

## Fixed

- `:5` — "read her friend **the way** she read everything" → "read her friend
  **as** she read everything." Four `the way` constructions in a two-page
  chapter; this was the only one doing no work. The other three are protected
  (see below).
- `:19` — "the patient **complete** attention he brought to it" → "the patient
  attention he brought to it." Doubled unpunctuated modifiers inside a list
  whose other four items are hard concrete nouns; *complete* is a scope word
  the itemized dinner already proves. **Reader-praised** — gpt-5.6-sol quoted
  the phrase by name ("Pace's care survives into her retelling… so my
  attraction to him remains strong") — but the praise attached to *patient*,
  which is Pace's tempo and survives intact.
- `:21` — cut "This was never Cassie's country; you did not march her through
  it." **The one criticism with cross-reader agreement.** claude-opus-4-8:
  the ladle "is extended right to the edge of over-explaining… three
  consecutive turns on the same insight, and a leaner hand might have trusted
  one"; gpt-5.6-sol independently found two of the three. Of the three turns
  this was the only *assertion* rather than image, and it was separately the
  line gpt-5.6-terra and gpt-5.5 both paused on ("a striking assumption about
  Cassie, who has repeatedly proven able to meet Vee's sexual truth gently").
  The cut answers both criticisms at once and butts the doubled *kindness*
  flush, which sharpens the self-persuasion loop. Side effect: it also
  resolves the "country" echo below at no cost.
- `:31` — "She wanted the shower more than she'd **wanted** anything sensible
  in days" → "more than anything sensible in days." Third strike of *want* in
  two sentences flattened the deliberate anaphora into accident; the pure
  deletion also makes the second sentence shorter than the first, which sets
  up the run of verbs that follows.

## Left standing — do not re-litigate

- **"country" ×2 (`:9` hair / `:21` Cassie's)** — ruled *leave both* before the
  bonus item cut the second occurrence, so the echo is now moot; the ruling is
  recorded because the hair image is the surviving half and must not be
  varied later on echo grounds. Both were quoted by readers and no reader
  heard the repetition: claude-fable-5 and claude-opus-4-8 both quoted "her
  hair its own wild country" approvingly ("it's the happiest I've seen her").
- **kindness / kindness / kindly (`:21` ×2, `:41`) — designed, not a tic.**
  The `:21` doubling is self-persuasion rendered as syntax (and now sits
  flush after the bonus cut); `:41` is the mirror — Vee tells herself a
  withholding is a kindness, and twenty lines later Cassie performs an actual
  kindness and is wrong about everything. All five readers named "kindly,
  certainly, wrong" as the chapter's most efficient beat (claude-opus-4-8:
  "That little 'wrong' is doing a lot"); none heard it as an echo.
- **The three surviving `the way` constructions** — `:3` "The lock stuck the
  way it always stuck" is half the door bookend (`:43` "The door stuck and
  gave"); `:21` the ladle is the chapter's engine (claude-fable-5: "That
  sentence is the chapter"); `:21` "She believed it the way you believe the
  thing that lets you keep what you want to keep" is its most-praised line
  (claude-opus-4-8: "the sharpest line in the chapter"). Do not vary any of
  the three. (`:9` "on the way home" is the literal noun, not the
  construction.)

## Linter acks (author sign-off 2026-08-07)

All six remaining hits acked; chapter closes at 0 active hits.

- `filter-verbs` `:23` (`#c7e24c0b8582`) — "Whether she felt it there, Vee
  couldn't have said." **POV, not distance:** the sensation is Cassie's and
  Vee has no access to it; the sentence's content *is* the epistemic gap, and
  rendering it directly would require narrating Cassie's interior. It keeps
  open the question gpt-5.6-sol raised off Cassie's half-second at `:5`
  ("makes me wonder whether she saw more than she said").
- `not-x-but-y` `:19` (`#fbfda1a8adda`) — "not a story but only her body
  naming what it wanted." Single occurrence, so the rule's own cluster
  condition is unmet; the antithesis is the hinge between the public version
  and the private fact. claude-fable-5 noted it "edges toward over-articulate
  for Vee's own head" and pardoned it in the same breath as within register.
- `the-way` `:3` (`#3fa14975f14e`), `:9` (`#fcd6bccc2ecd`), `:21`
  (`#e032a1da394a`), `:21` (`#bbc7d7c99a04`) — the bookend, the literal
  false positive, the ladle, and the believed-line. Rationale above.
