# Close-third pass — Gone (ch21)

2026-10-27 · claude-opus-5-5 · Pace's POV

**Verdict:** very light. The October workshop already took most of the narrator
out. What is left: one line describing his state from outside him while he
talks, and one summary clause in the second ride. Everything else is his eye
on Randi, his memory or his picture of Vee.

Praise tool: `praise_check.py --text` searched the 12 ch021 gates, both cold
reads and the audits (19 files). I also ran `rg` over the gates and cold reads
for paraphrase. The gates are dated 2026-10-24, so they read the workshop
prose.

## Proposed

### The lamp speech

1. `scenes/gone.md:67`: "He wasn't looking at anything; he was seeing it."
   - Whose: the narrator's. It describes him from outside while he talks, and it
     has the `x-not-y` shape. Pace would not think it of himself.
   - What already shows it: the speech itself ("Like somebody found the lamp…
     and it never once occurs to her"), and :61, where the picture has already
     moved to Vee in his kitchen. :69 then has him register Randi's stillness,
     so the line isn't needed to show he has left her.
   - Result: "\"She comes in and the whole thing goes brighter. Like somebody
     found the lamp. And she has no idea she does it. She spends the entire time
     sure she's too much, and she's the most alive person standing there, and it
     never once occurs to her.\"" (one speech, no break)
   - Praise: none (praise_check and `rg` both clean).

## Open questions — his reading, or the narrator's?

- Q1. `scenes/gone.md:9`: "Whatever she ran on out in the world, she set it down
  at his door."
  - For his: it follows his own observation ("She talked less here than
    anywhere"), and it is the story he tells himself about her. It is wrong
    (she is working the whole scene), which is dramatic irony.
  - For the narrator: it states her interior flatly, with no "he thought".
  - Praise: one authorship audit quotes it neutrally. No reader quotes it.
  - My lean: his; leave.

## Leaving alone

- :7 "Tonight, she had stayed down.": his noticing, under author ruling
  (2026-10-24).
- :9 "the urgency had gone out of him": author ruling (2026-10-24).
- :29 "and let himself look": author ruling (2026-10-24).
- :33 "There was something undefended in her face.": his perception of her
  face.
- :57 "She went quiet at that, and softened past it.": the signed-off
  observation-only exception (`meta-note-gone.md`).
- :59 "showing him with her own body the thing she was describing": protected
  (triage, 2026-08-07).
- :61 the breast-drag beat: his body and his pictures, under author ruling
  (2026-10-24).
- :69 "the kind that takes holding" and "Then something gathered under it":
  protected (triage). New evidence, for the record: the claude-opus-5-5
  romance-graduate gate (:9) says "The book tells me that stillness is 'the
  kind that takes holding,' which I didn't need, but fine." That is one reader,
  against four of five in the earlier wave who quoted the paragraph. Not
  raised.
- :71 "when she'd been quiet a beat too long": his ear for the gap.
- :79 "let her set the pace of it": protected (echo ledger #35).
- :96 "opened the second one down without looking for it": what he sees. Four
  gates quote it (fable-5-1 fsog, opus-5-5 romance, glm romance, and sol's cold
  read on the drawers).
- :98 "so that all of her was inside it but her face and her hands and the blue
  of her toes": what he sees; quoted by sol's cold read.
- :102 "which he would not have expected to survive the first minute": his wry
  view of the flower dispute.
- :128 "Her glass was still nearly half full.": what he sees as she holds it
  out. It is the only signal on the page that the request is a pretext. sol's
  cold read picks it up.
- :136 "He had expected the fork to go down after the chicken.": his
  expectation. It is the reversal against {{Portion}}.

## Borderline — likely his, walk if wanted (strongest first)

a. `:79` "and there was nothing quiet left in either of them now": a summary
   of both their interiors, and a callback to the quiet of :9. The claude-opus-5-5
   romance-graduate gate quotes it with "coming apart by degrees" as "a bit of a
   gloss", in a complaint that the second ride is mostly summary. One authorship
   audit quotes it neutrally. Cut option: "…and he held her and let her set the
   pace of it, and down the hall the playlist kept going, low, under the door."
   This keeps the protected "set the pace".
b. `:100` "He could do this without leaving her to wait long.": his practical
   thought, though it explains the menu. Praise: none. Lean: leave.

## Rulings
1. :67 — **1a** (cut "He wasn't looking at anything; he was seeing it."; speech joined).
Q1. :9 — **left** (his).
Borderline a. :79 — **kept** (his: he feels her urgency through his body, and the clause is the only return of his own urgency after :9).
Borderline b. :100 — **kept** (his).

## Applied 2026-10-27

One edit, at :67.
- Lint: 0 errors. 13 ASK hits, none at :67; all were in the chapter before this
  pass.
- Bare praise check: nothing.
- Orphans: clean for Gone. No chapter recalls the cut line. Rock was passed as
  the next chapter; its one flag («love in», cut by `80696198`) predates this
  pass.
