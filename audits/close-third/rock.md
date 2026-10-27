# Close-third pass — Rock (ch22)

2026-10-27 · claude-opus-5-5 · Vee's POV

**Verdict:** light to moderate. The August line-edit pass took out most of the
glosses. What is left: an opening line telling us the point of the image, a
stack of restatements around the Daphne beat (two capture readers flag one of
them as grading), and two summary tails in the scar and name beats. Almost
everything else is her reading of him, which this chapter is made of.

Praise tool: `praise_check.py --text` searched the 11 ch022 gates, both cold
reads and the authorship audits (15 files). I also ran `rg` over the gates and
cold reads for paraphrase and for complaints about explaining.

## Proposed

### Opening

1. `scenes/rock.md:3`: "and the smallness of it was the point."
   - Whose: the narrator's. It comes before we are in Vee's head and tells us
     what the image means.
   - What already shows it: the paragraph itself. The cold leans in on the
     glass, and the quilt and fire "made all the warmth there was". The frame
     acks (2026-08-07) rule that the warm density is the frame.
   - Result: "…and the quilt over the two of them and the fire at their backs
     made all the warmth there was."
   - Praise: none.

### Daphne

2. `:215`: "She didn't choose it. She simply stopped moving."
   - Whose: the narrator's, describing her body from outside. It is the
     `dear.md:13` shape: "slowed" is shown, then "She hadn't meant to slow."
   - What already shows it: "Vee went still." Going still at "She was
     nineteen" is the involuntary reaction.
   - Result: "Vee went still."
   - Praise: none.

3. `:219`: "and the good order was the tell"
   - Whose: arguably hers (she is reading him), but it is phrased as a verdict
     on what the reader has just watched. :217 shows the order ("each word set
     down separately and precisely in its place…"). :219 then names it, and
     the full-glass simile shows it a third time.
   - Readers:
     - Against, 2 gates. claude-fable-5-1 romance: "the book explained itself
       to me twice… 'The good order was the tell' — yes, I had the tell… you
       didn't need to grade it for me." claude-opus-5-5 romance: "The book
       explained its subtext to me again: 'the good order was the tell'… I had
       it, I promise. The scene had already shown me the full glass."
     - For or neutral, 2. glm-5.3 fsog gate: "Vee names it exactly — the good
       order IS the tell." glm-5.3 cold read: "the page itself flags it"
       (neutral).
   - Options:
     - 3a (recommended): cut the clause. Result: "He laid it out in good order,
       every reason accounted for and set in its slot. All evening she had
       heard him undersell things — the hall, the fifteen — and this was that
       same voice gone one degree flatter, held the careful way a person
       carries a full glass so it won't go over the rim." Her comparison with
       the evening's underselling, and the glass, still carry the reading.
     - 3b: keep.

4. `:223`: "So she did not say the word, and she did not say she was sorry."
   - Whose: the narrator's summary connective ("So…"). It restates :221
     ("she held it down under her tongue. It was not hers to say.") and calls
     back :159 ("She wanted to say she was sorry. She did not.").
   - What already shows it: :221 for the word, :159 for the sorry. :225 "She
     kept the rest behind her teeth" holds it a third time.
   - Result: "She set the mug on the table, turned under the quilt, and fitted
     herself along his side, her head to his shoulder, her palm flat on his
     chest over the place the careful voice had come out of."
   - Praise: two fragment hits. Both praise the not-saying that :221 carries
     (fable-5-1 "smart enough not to say the word"; glm "hold it down under
     her tongue"). :225's "behind her teeth" is praised by fable-5-1 and glm
     fsog, so it is not offered as a cut.

### The scar and the name

5. `:259`: "and that was the whole of the asking and the whole of the answer"
   - Whose: the narrator's. It sums up the gesture after the gesture.
   - What already shows it: palms turned together over the scar, after "Not
     tonight" and the door with a time on it.
   - Result: "She turned her hand over under his so their palms were together
     over the scar, and left it."
   - Praise: none for the tail. The protected "only a door with a time on it
     that wasn't now" is untouched.

6. `:263`: "She was not asking him for anything, and she was not trying it on."
   - Whose: the narrator, explaining the callback to :87 ("to feel how it sat
     in her own mouth"). It also has the `x-not-y` shape.
   - What already shows it: "No question in it this time." and "the way you
     say a word to keep it".
   - Options:
     - 6a (recommended): cut the sentence. Result: "\"Peter,\" she said.
       Softly. No question in it this time. She was only saying it, once, into
       the warm dark, the way you say a word to keep it."
     - 6b: also cut "No question in it this time." Result: "…Softly. She was
       only saying it, once…" This loses the explicit contrast with :87, which
       the reader may want.
   - Praise: none.

## Open questions — her reading, or the narrator's?

- Q1. `:117`: "Not quite a smile, because he was too precise not to first check
  whether she meant it, and too used to her by now to think she did."
  - For hers: she is the one who knows he's precise and used to her teasing.
    This is her fond theory of his face.
  - For the narrator: it reads his interior mechanism with certainty, as a
    `because` clause after a shown reaction.
  - Praise: none.
  - My lean: hers; leave.

## Leaving alone

- :9 "without any sense of having been steered": her generalization, and the
  dramatic irony (she was steered).
- :23 "because it was true and because she could hear her mother's defense":
  her reason.
- :31 "Pace went first to the hand underneath the thing.": her reading of him.
  The claude-opus-5-5 fsog gate praises it ("I melted a little"); the glm cold
  read notes it as "now named by the narration", neutrally.
- :51 "That was the trouble with him": protected (triage, 2026-08-07).
- :63, :155, :173, :185, :217: her perception of his manner or tone.
- :69 "which she was grateful for, because it was not sad…": her own view.
- :73 the two kinds of quiet: protected (triage).
- :77 "It was not withheld. It was only the size of it": her reading at that
  moment; :85 then corrects it ("He had taken his mother out of the answer").
- :141 "almost comic in its restraint": her wry judgment.
- :159 "Sorry would have asked him to accept comfort…": her reasoning for her
  restraint.
- :161 the hallway as the door to the part he wanted to tell: left standing
  (triage) as the hinge.
- :175 "something in him leaned forward": left standing (triage).
- :199 "the second kind of quiet": her callback to :73, the setup and payoff
  the triage protects.
- :201 "to make it a trade": her motive.
- :221 the arithmetic paragraph and "the clean ugly grown-up word": body
  before mind, protected.
- :227 "he did not hear himself doing it" and "named it luck": protected
  (three models). New evidence, for the record: the claude-opus-5-5 romance
  gate lists "named it luck" with "the good order was the tell" as
  explanation. That is one reader against the three who protect it. Not
  raised.
- :261 "though he had just told her they were moving": her mind, setting up
  "one piece" at :275.
- :271–:275: her own wrong account of the semester (the "stumble" into
  Randi), which is dramatic irony. The closing refrain is designed (the glm
  gate reads the repetition as deliberate).

## Borderline — likely hers, walk if wanted (strongest first)

a. `:211` "The flatness in it reminded her of how he'd sounded when she asked
   about his parents.": explaining the callback (`famished.md:83` shape). The
   reader has :77 and :209 "Just the name". Cut result: "\"How did you know
   her?\"" stands alone after :209. Praise: none. It is her memory linking,
   though, not at a peak.
b. `:245` "She was putting something together, and it came together in her
   body before it came together as a thought, low and warm and a little
   unsteady.": an announcement before :247. But two gates praise this exact
   beat: fable-5-1 ("she got there herself, slowly, in her body first, and I
   loved that") and glm romance ("Vee putting that together in her body
   before her head, that's interiority doing what I'm starving for"). fable's
   flinch is at the dialogue that follows, not this line. Lean: keep.
c. `:265` "and did not need to": a narrator's verdict on his silence. Cut
   result: "He let it sit. He did not answer it. His hand closed…", or cut
   the whole sentence, since "He let it sit" already says it. Praise: none.
d. `:189` "not because she understood the mathematics, but because he did, and
   he had turned the understanding toward her like light": her sense of why
   the world shifted, in `not-x-but-y` shape. Only stem hits on the praise
   check. Lean: hers; keep.
e. `:91` "because the name had made him seem suddenly unmeasured…, and because
   this was the kind of question new people were allowed to ask…": her motive
   for the age question. Nothing else shows it. Lean: keep.
f. `:5` "because they had stopped drinking it in order to keep talking": a
   logistic explanation that :9 ("They had been talking for a while") then
   repeats. Cut result: "…and the tea gone cool in the mugs on the low
   table." Praise: none.

## Trims (redundancy, not explanation)

- `:251`: "moved without her deciding it" and "before she thought about whether
  to" state the same involuntariness twice. The triage (2026-08-01) kept the
  paragraph's inventory but did not rule on this pair.
- `:89` "She let it be." comes two sentences after :85 "Vee let him."

## Rulings
1. :3 — **1a** (cut "and the smallness of it was the point").
2. :215 — **2a** (cut "She didn't choose it. She simply stopped moving.").
3. :219 — **3a** (cut "and the good order was the tell").
4. :223 — **4a** (cut "So she did not say the word, and she did not say she was sorry."). Author asked about cutting ":221 It was not hers to say." + "So" instead; declined on evidence: 3 gates praise "not hers to say" (opus-5-5 romance, glm romance, glm fsog; praise_check missed it), and it is the only statement of her reason.
5. :259 — **5a** (cut "and that was the whole of the asking and the whole of the answer").
6. :263 — **6a** (cut "She was not asking him for anything, and she was not trying it on.").
Q1. :117 — **left** (hers).
Borderline a. :211 — **cut** ("The flatness in it reminded her of how he'd sounded when she asked about his parents.").
Borderline b. :245 — **kept** (2 gates praise the body-first beat).
Borderline c. :265 — **c1** (cut "He did not answer it and did not need to.").
Borderline d. :189 — **kept** (hers; the cause is him, not the math).
Borderline e. :91 — **e3** (cut second clause ", and because this was the kind of question new people were allowed to ask each other after born-where and brother and mother"; keep the name clause).
Borderline f. :5 — **kept**.

## Applied 2026-10-27

Nine cuts: :3, :91, :211, :215, :219, :223, :259, :263, :265.
- Lint: 0 errors. 7 ASK hits.
  - New, because the :3 sentence changed and its earlier acks re-armed:
    :3 `warm` and :3 `there-was-were`.
  - Already active before this pass: :11, :51 and :185 `a-small`; :127
    `fluorescent-site` (ruled KEPT 2026-08-12 but never acked); :269
    `x-not-y`.
- Bare praise check: only the :219 and :223 hits already weighed.
- Orphans (rock and 15 recallers): only the standing «love in» flag (cut by
  `80696198`), unrelated to this pass.
Trim T1. :251 — **T1a** (cut "without her deciding it"; "drifted" already carries it, "before she thought about whether to" kept).
Trim T2. :89 — **T2a** (cut "She let it be.").

Trims applied (:251, :89). Lint unchanged (same 7 ASK). Praise check: no hits
on the trims. Orphans: unchanged.
