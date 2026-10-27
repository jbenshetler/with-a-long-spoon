# Close-third pass — Peekaboo (ch19)

2026-10-26 · claude-opus-5-5 · Vee's POV

**Verdict:** very light. The chapter almost never steps out from behind her. I
found two small narrator glosses, both in sex beats, and one reading of Pace's
interior to put to the author. The two most-quoted runs ("hide the trouble" at
:19; the :119/:121 pair) are hers, and the :119/:121 pair is protected.

Praise tool note: `praise_check.py --text` searched the 12 ch019 capture gates,
both cold reads and the authorship audits (16 files). I also ran `rg` on the
gates and cold reads for paraphrase. The tallies below combine both.

## Proposed

### The mirror

1. `scenes/peekaboo.md:49`: "the shame of having stripped herself bare on purpose
   to be looked at,"
   - Whose: the narrator's. It is a gloss after the beat. She has just taken the
     underwear off so the line would run clean, and the clause names what the
     act was. It is the wording of the design note (`meta-note-peekaboo.md:15`,
     "she slides the underwear off *on purpose to be looked at*"), set on the
     page.
   - What already shows it: the whole underwear beat (:47–:49), and "she was the
     one who'd taken the edge away".
   - 1a (recommended): "The shame of it went through her hot, and it crossed into
     wanting almost before it was shame at all, and she let it come."
   - 1b: keep.
   - Praise: the claude-opus-5-5 romance-graduate gate (:13) paraphrases it
     approvingly: "She chose to strip herself bare to be looked at, the shame
     turned into want almost before it was shame". The glm-5.3 romance-graduate
     gate (:7) engages with the act, not the clause. Two authorship audits quote
     it neutrally. So one reader paraphrases the clause.

### The bed

2. `scenes/peekaboo.md:99`: "which was the whole point, and she knew it was the
   point"
   - Whose: split. "Which was the whole point" is the narrator stating his
     intent; "she knew it was the point" is hers. The sentence says the same
     thing twice.
   - 2a (recommended): "He came back into her slower than she wanted, and she knew
     it was the point: a little, and stopped…"
   - 2b: "…slower than she wanted, which was the whole point: a little…". This
     keeps the narrator's half and loses hers.
   - Praise: none (praise_check and `rg` both clean).

## Open questions — her reading, or the narrator's?

- Q1. `scenes/peekaboo.md:99`: "and he twitched against the inside of her, once,
  and she knew exactly what it was costing him and that he meant to spend it
  anyway."
  - For hers: it says "she knew". She feels the twitch inside her, and she reads
    his restraint from his body.
  - For the narrator: it explains the twitch that the next line ("You're
    enjoying this." / "Very much.") answers. The author ruling of 2026-10-08
    (`meta-condensed-peekaboo.md:58-59`) has the twitch there "so the cost is
    **felt, not stated**", and this clause states it.
  - Cut option: "…and he simply held, heavy and still above her, and he twitched
    against the inside of her, once."
  - Praise: two readers paraphrase it approvingly. The claude-fable-5-1
    fsog-refugee gate (:17) has "twitching once so she'd know what it cost him
    and that he meant to spend it anyway". The claude-opus-5-5 fsog-refugee gate
    has "she knows it's costing him, and he spends it anyway. Tenderness and
    dominance in the same man".
  - My lean: narrator-shaped, but praised. Author's call.
- Q2. `scenes/peekaboo.md:9`: "his eyes already going past her to the thing he'd
  made and couldn't wait another minute for her to see."
  - For hers: she watches his eyes go past her, and the kid-with-a-surprise
    simile is her reading.
  - For the narrator: it states his impatience as fact.
  - My lean: hers. Three cold readers praise the beat
    (`meta-triage-peekaboo.md:115-118`).

## Leaving alone

- :3 the opening recap and "without saying why even to herself": left standing
  (triage, line-edit pass). Her own not-saying is character.
- :15 "He'd set the whole thing up for her.": left standing (triage).
- :19 "That was the thing that got to her — that he'd taken all that trouble…":
  her working out why she is moved, at a peak. It is quoted or paraphrased by
  fable-5-1, gemini-4-argon and glm-5.3 gates; the wording was settled in the
  line-edit pass.
- :23 "and didn't make it smaller": her perception of his manner.
- :27 "not far, never far": hers; praised (triage).
- :31 "That was what her skin knew before her head did… cut to the actual shape of
  her": the head arriving after the skin, which is the body-before-mind order.
  Structural (triage).
- :33 the lining sentence: hers; quoted (triage).
- :39 *Floozy* / "the looking stopped being shame": protected.
- :53 "harder to look at and impossible to look away from": her perception.
- :55 "nothing left for either of them to decide": left standing (triage).
- :91 "the sound she made should have shamed her but didn't": her shame engine,
  registering its own absence.
- :113 "They'd gotten it hung, in the end…": her fond memory; the condensed
  brief keeps it as the one-line callback.
- :115 "she knew without being told that he'd been up the night before…": her
  reconstructing, in the afterglow.
- :119 / :121 "what she was for" / "getting away with something": the protected
  load-bearing pair (triage, 2026-09-25).

## Borderline — likely hers, walk if wanted (strongest first)

a. `:7` "and under the circumstances it was never going to stay gentle. It
   didn't.": "It didn't." confirms what the next sentence shows (the hand in her
   hair, the fistful of shirt, "deep and certain"). The wry voice is hers. Cut
   option: drop "It didn't." Praise: none.
b. `:41` "because the shoes this called for weren't anything she owned,": the
   third statement of the shoe gap in one paragraph, after "more of one than she
   owned" and "nowhere near tall enough". It is a plant, and readers clocked it:
   the gemini-4-argon romance-graduate gate quotes it verbatim, and the
   fable-5-1, opus-5-5 and sol gates all pick up the shoes. Cut option: "…and
   came back down, and that woman could wait." Lean: leave.

## Rulings

1. :49 — **1a** (cut "the shame of having stripped herself bare on purpose to be looked at,").
2. :99 — **2a** ("…slower than she wanted, and she knew it was the point:").
Q1. :99 — **R2** rephrase, author-approved with filter-verbs ack: "…and he twitched against the inside of her, once, and she felt what the holding was costing him, and that he meant to spend it anyway."
Q2. :9 — **Q2a**, left (hers).
Borderline a. :7 — **cut** "It didn't."
Borderline b. :41 — **leave** (the shoe plant).

## Applied 2026-10-26

Four edits applied: :7, :49, and two at :99.
- Lint: 0 errors. 12 ASK hits, 11 of them carried in by the earlier
  extension. The :99 `filter-verbs` hit (#ec90f2b4c24a) was acked with the
  author's sign-off.
- Bare praise check: only the :49 clause; nothing new.
- Orphans: clean.
