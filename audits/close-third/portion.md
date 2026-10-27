# Close-third pass — Portion (ch18)

2026-10-26 · claude-opus-5-5 · Pace's POV

**Verdict:** light. The chapter leaves Randi's motive to the reader and mostly
stays behind Pace's eyes. The one habit is stating his not-knowing: :79, :85,
:91 and :95 each say it. Only :85 is a clause the narrator says over his
shoulder; the others are him.

Praise tool note: `praise_check.py` returned clean for every candidate below,
but `rg` over the ch018 capture gates found verbatim quotes of three of them
(the gates are at prose-sha 96625992/6a8d1d1b). The tallies below are from
`rg`.

## Proposed

### The bed

1. `scenes/portion.md:85`: "He knew that much and not the rest,"
   - Whose: the narrator's. It tells the reader there is a "rest" Pace is
     missing, a ledger kept from outside him.
   - What already shows it: the sentence before ("After a while he understood
     it was not going to, and that whatever this was, it was not for him"),
     :91 ("would not go together into anything he could name; it was the
     want, he thought"), and :95 ("He did not know what he had done").
   - Craft note: `meta-note-portion.md:47-49`, "do not let the narration know
     better than he does". The condensed brief (`meta-condensed-portion.md:54`)
     already reads "He gives it to her anyway."
   - 1a (recommended): "…and that whatever this was, it was not for him. He
     gave it to her anyway. She was quick about it."
   - 1b: "…and that whatever this was, it was not for him, and he gave it to
     her anyway. She was quick about it."
   - Praise: gpt-5.6-sol fsog-refugee gate-ch018:23 gives the whole sentence
     as its ALMOST-STOPPED line, about the pain of the scene ("severance
     disguised as intensity") rather than this clause. One reader; neutral on
     the cut.

### The table

2. `scenes/portion.md:81`: "because it was in front of him and he was who he
   was,"
   - Whose: arguable. "Because it was in front of him" could be his own dry
     reason. "He was who he was" is a summary of his character, and that
     summary is the narrator's.
   - What already shows it: "and it did not taste like anything" carries
     eating without appetite. The bowl in the fridge "for her" (:97) carries
     the man who doesn't waste and still looks after her.
   - 2a (recommended): "He finished his own, and it did not taste like
     anything."
   - 2b: "He finished his own, because it was in front of him, and it did not
     taste like anything." This keeps his reason and cuts only the label.
   - Praise: none (praise_check clean; `rg` clean).

## Open questions — his reading, or the narrator's?

- `scenes/portion.md:65`: "because she was not holding anything. It was out."
  - For his: he knows the tell ("the thing at the corner of her mouth that
    came a beat late when she was holding something"), so its absence is
    his to read.
  - For the narrator: the clause states her interior flatly, without a "he
    thought".
  - My lean: his.
  - Praise: claude-opus-5-5 romance-graduate gate-ch018:7 quotes it.
- `scenes/portion.md:69`: "Not where she had aimed it; somewhere to the side
  of that"
  - For his: he can judge where "selfish" was aimed from the argument, which
    was about Vee's schedule.
  - For the narrator: it is a confident reading of her aim at a moment when
    he can't read her anything else.
  - My lean: his.
  - Praise: glm-5.3 cold read :17 quotes "lands somewhere sideways of where
    she aimed".

## Leaving alone

- :23 "She did not say things like that to him…": his reasoning, and the
  alarm the reader catches before he does.
- :29 "That was Vee's.": his. The opus fsog-refugee gate (:7) calls it "the
  line I needed".
- :33 "He was glad all the way down.": his. "Randi watched him be glad" (:35)
  depends on it.
- :77 "He heard how it had come out. He did not take it back, because it was
  true, and because he did not know how.": his hearing and his reason. Quoted
  approvingly by the opus fsog-refugee gate (:9).
- :91 "He went over it… He had all of it… it was the want, he thought": his
  mind going back over it at a peak, ending in a wrong explanation. That is
  dramatic irony, not a recap.
- :95 "He did not know what he had done… and it was not there.": his. The
  glm cold read (:17) quotes it as the chapter's turn for him.

## Borderline — likely his, walk if wanted (strongest first)

a. `:79` "and he could not have said where": the nudge shape (narration
   remarking on what he can't put into words), and the second of the four
   not-knowings. But it is his inarticulacy, and claude-fable-5-1
   romance-graduate gate-ch018:9 quotes it and answers it ("I could have said
   where"). The clause hands the reader the inference.
b. `:37` "and he noticed it, and left it.": a remark on his attention, but the
   choice is his, and it sets up the line still there at :95.

## Rulings

1. :85 — **1b** (join: "…it was not for him, and he gave it to her anyway.")
2. :81 — **2b** (cut "and he was who he was" only).
Q1. :65 — his reading, but the author reworked the paragraph: "He looked at her. Her face was doing very little. The blue of her eyes was on him, level and sharp, in a way he had not seen before." (mouth tell and "It was out." cut; author wording, assistant tightening)
Q2. :69 — author disliked the paragraph (hurt and puzzled; he cares for Randi; they planned it together; he'd have to be thick to miss the Friday connection). Workshopped replacement accepted; jealousy guard (`meta-note-portion.md:42`) overridden by the author — he may read it as jealousy of Friday, never the real layers:
   "He felt it land, and it hurt. Friday, then. She had come from Vee's table this morning to his, and told him, and watched him be glad. She wanted Vee as much as he did. He had felt it in her, on his couch and in his bed, a want too big for her face, and *I want us*, torn out of her. They had picked Vee together, and Friday had happened without her. He could see why that would sting. He could not see what he was supposed to do about it. He heard his own voice go exact."
Borderline a. :79 — **cut** "and he could not have said where" (author: fable's "I could have said where" is criticism, not praise — the kind of line fable dislikes; I had misread it).
Borderline b. :37 — **middle**: "…the top of the sauce, and he left it."

## Applied 2026-10-26

All six applied. Lint: 0 errors; 14 ASK hits, all pre-existing in the chapter or carried over from the old line. Orphans: clean (portion gone one-bite covering all-the-time). Post-edit praise check: the fitting clause dropped from :69 was engaged by 4 readers (irony against Pace); the author ruled that the cut stands. Meta updated: `meta-note-portion.md` (jealousy guard and assembles-only-the-first), `meta-condensed-portion.md`, `meta-plan-chronology.md`.

Tool gap: `praise_check.py --text` came back clean before the cuts on lines the ch018 capture gates quote verbatim; the bare post-edit run found them. Pre-cut, `rg` the gates as well.
