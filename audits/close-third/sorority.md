# Close-third pass — Sorority (ch20)

2026-10-26 · claude-opus-5-5 · Vee's POV

**Verdict:** light. The 2026-08-07 line-edit pass already took out most of the
narrator (`meta-triage-sorority.md:52-106`). What remains: one label, one
announcement before a speech, and one explained callback. A handful of borderline
lines are in her wry voice.

Praise tool: `praise_check.py --text` searched the 11 ch020 gates, both cold
reads and the audits (15 files). I also ran `rg` over the gates and cold reads
for paraphrase.

## Proposed

### The dorm room

1. `scenes/sorority.md:85`: "Coming back was its own small ceremony."
   - Whose: the narrator's. It labels the beat before showing it.
   - What already shows it: the rest of the paragraph ("She came out of the
     bathroom in it, bare-shouldered… and stood in the middle of the room and
     let Randi look.") and :87 ("And Randi looked.").
   - Result: "She came out of the bathroom in it, bare-shouldered, the hem just
     off the floor without the shoes, and stood in the middle of the room and let
     Randi look."
   - Praise: none. The fable-5-1 fsog gate (:13) praises the coming-out itself,
     not the label.

### The bypass store

2. `scenes/sorority.md:133`: "and talked herself into it out loud, which was the
   same as talking Randi into it."
   - Whose: mostly the narrator's. It announces the speech that follows and
     tells you what the speech is doing. Her own awareness of it comes after,
     in :135 ("She could hear exactly how it sounded. She kept going anyway.").
   - 2a (recommended): "…a price that didn't make the debit flinch. She turned it
     over in her hands." Then the speech.
   - 2b: cut only the tail: "She turned it over in her hands and talked herself
     into it out loud."
   - Praise: none.

3. `scenes/sorority.md:151`: "Randi had just said out loud, easy and offhand, the
   thing Vee had been running behind her own eyes all week,"
   - Whose: explaining the callback. Randi's "walk in late and stop the room
     cold" (:149) gives the {{Peekaboo}} daydream back almost word for word ("in
     late, on purpose… The way the room would turn"). Then :179 states the same
     thing again in Vee's head ("the picture she'd been rehearsing in private for
     a week: in late, the door, the whole room turning"), and that statement is
     left standing.
   - 3a (recommended): "Vee didn't answer. Hearing it in someone else's mouth
     made it real, and made her face go warm, and she followed her out." This
     keeps her feeling and its cause in her own terms.
   - 3b: keep.
   - Praise: the fable-5-1 romance-graduate gate (:7) paraphrases the clause
     ("she says the thing Vee's been running behind her eyes all week, *walk in
     late and stop the room cold*"). The gemini-4-argon romance-graduate gate
     (:13) reads the same echo darkly, as "Randi knows Vee's daydream". So two
     readers engage with the echo, one through this clause. Both get it from
     Randi's line as well.

## Open questions — her reading, or the narrator's?

- Q1. `scenes/sorority.md:43`: "because the friend was the only part of any of it
  Cassie had ever been able to see."
  - For hers: it is her realisation at the moment it lands ("it landed on Vee
    then"), and it is her knowledge of Cassie (the fleece, two winters).
  - For the narrator: it is a `because` clause after a shown reaction, and it
    states the design (`meta-condensed-sorority.md:7`, "Cassie watches the
    *person*").
  - Praise: glm-5.3 quotes it, in both its cold read (:13, "got me in the
    heart") and its romance-graduate gate. Opus-5-5's two gates and sol's gate
    praise the beat in their own words.
  - My lean: hers; leave.
- Q2. `scenes/sorority.md:29`: "Cassie had cracked it hours ago off the made bed,
  and let Randi have it anyway."
  - For hers: Vee knows Cassie saw the bed, since Cassie said so at :13–:17.
    Reading Cassie's restraint is her habit with Cassie.
  - For the narrator: "let Randi have it anyway" reads Cassie's motive.
  - Praise: none.
  - My lean: hers; leave.

## Leaving alone

- :51 "Vee took it the only way there was to take it. Both of them.": her
  misreading, the designed one (`meta-note-sorority.md:29`). It is also
  listed under Borderline (c).
- :55 "'Slut' landed lower than Randi meant it to.": her reading of Randi's
  register.
- :63 "Cassie had never once in her life cared what was on anyone's feet.": her
  reading of the eyebrow, which is wrong in character.
- :83 "the wanting got there before the plan…", :163 *lover*, :173 the floor tip,
  :129 "the real laugh, the one that costs her something to give", :185 "There
  was nothing under it.": left standing (triage).
- :87 "the way you take in a thing you're going to have to account for": her
  generalizing reading of Randi's look. Quoted by the opus-5-5 romance-graduate
  gate (:11).
- :97 "felt the word land — *to* — felt it name the thing the tears had been
  about": her processing at a peak, linking back to the sun porch. glm cold
  read (:15) quotes the line it answers.
- :107 Randi's second quiet: a designed beat under author ruling
  (`meta-note-sorority.md:25-32`).
- :161 "which was its own kind of going under": her own water figure.
- :181 "A different arithmetic had taken the wheel…": her rationalization, a
  wrong reason she hands herself.
- :197 "she had never once in her life had a friend like this": her thought; the
  ironic close.

## Borderline — likely hers, walk if wanted (strongest first)

a. `:119` "and the hunt tipped over into the other thing.": an announcement of
   the comedy. The line-edit pass already cut its gloss ("as hunts do when they
   stop paying out"). The paragraph after it opens on "It started when…", so a
   cut would also need "Then Randi wedged herself…". Praise: none.
b. `:65` "And that was Vee for the length of the lecture, turned between the two
   of them, happy in the middle.": a recap at the paragraph's end, short, with
   "happy in the middle" as its image. Praise: none.
c. `:51` "Vee took it the only way there was to take it.": "the only way there
   was" can read as a wink, since the reader sees another way. It is also her
   certainty, which is the irony. Praise: none.
d. `:57` "And there was the one snag in the gold of the day, and Randi had
   reached in and found it.": an announcement before "I don't have shoes". But
   "snag in the gold of the day" is her figure. Praise: none.
e. `:91` "A verdict, in a word Vee would never have reached for.": "A verdict" is
   a label; the rest is hers. Praise: none.
f. `:73` "still shown to not one living soul.": it points ahead to the
   unveiling. glm cold read quotes it (:35). Lean: leave.

## Rulings

1. :85 — **cut** "Coming back was its own small ceremony."
2. :133 — **2a** (cut to "She turned it over in her hands.").
3. :151 — **3a** ("Vee didn't answer. Hearing it in someone else's mouth made it real, and made her face go warm, and she followed her out.").
Q1. :43 — **left** (hers).
Q2. :29 — **left** (hers).
Borderline a. :119 — **cut** "and the hunt tipped over into the other thing"; :121 "It started when Randi" → "Then Randi".
Borderline e. :91 — **cut** "A verdict, in a word Vee would never have reached for."
Borderline b, c, d, f — **kept**.

## Applied 2026-10-27

Six edits.
- Lint: 0 errors.
- 6 ASK hits:
  - One was re-armed by this pass: `warm` at :151, whose sentence changed. It
    had been acked in August as group F.
  - Five were already re-armed before this pass: `there-was-were` ×2 at :51;
    `the-way` at :77; `filter-verbs` at :105, "I watched", in dialogue;
    `cost-vague` at :129, the protected "real laugh".
- Bare praise check: only the :151 clause.
- Orphans: clean.
