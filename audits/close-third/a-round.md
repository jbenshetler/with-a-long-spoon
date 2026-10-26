# Close-third pass — A Round (ch14)

*2026-10-26 · claude-opus-5-5 · `/wals-close-third` (with the Two Towels lessons) · Vee's POV · nothing applied*

Verdict: light. The 2026-08-06 line edit already removed the captions (the ending sentence, the second "Keep still" gloss). Nearly every interpretive sentence is Vee's own: her wit, her reading of him, her processing. Four candidates; only one is clearly the narrator's.

Praise counted by `praise_check` plus a paraphrase search of the cold reads and ch014 gates.

## Proposed

1. `:56` — "She had not anticipated this part. She had thought the measuring would be the exposure. The measuring was only half of it." **Hers**, but it is the third statement of one discovery: `:52` "The stepping-away was the thing", `:54` "It was the withdrawing she hadn't expected to feel." It repeats in the abstract, the Dear `:57` shape. Readers praise the discovery heavily (fable: "when she said the withdrawing was the part she hadn't braced for"; glm, opus-5-5, sol, argon on the rhythm), but always as located at `:52`/`:54`, which stay. → cut the three sentences; `:56` ends "…He wasn't sneaking glances. He was looking."
2. `:130` — "and what he was doing was not building a dress on a form. He was building a dress *for her*, with her standing inside it, and the standing inside it was part of the design." **Hers**, an `x-not-y` gloss on the shown beat ("He kept looking at her — at her face, at the line of her neck, stepping back to consider the whole of her…"), and `:134` says it again in fuller form ("The dress had a particular woman in it and the particular woman was her, and there was nowhere in that to hide"). → end `:130` at "…to adjust something he'd decided to change." No praise.
3. `:174` — "That was the bravest thing she did all day, the not being able to stand it." **The narrator's**: a verdict from the end of the day ("all day"), grading her from outside the moment, at the chapter's peak of suspense. "She couldn't stand not knowing. She opened her eyes." already does it. No praise (opus-5-5's "bravest thing this book has done" is about the wet satin).
4. `:202` — "It was also the first time he had touched her since the reveal, and they both felt the difference in it." "They both felt" reports Pace's interior. **Borderline**: she could read it off him, as at `:232` ("He knew she knew"). Options: 4a "…since the reveal, and she felt the difference in it." · 4b cut the clause: "It was also the first time he had touched her since the reveal." · leave. No praise.

## Leaving alone

- `:13` "The traitorous question a woman asks…": hers ("Randi, Randi!").
- `:17` the swimsuit and her body history: her memory, set off by "tried to call it a swimsuit".
- `:36` "*admired*": author ruling 2026-09-30.
- `:42` "Wryly.", `:50` horse, `:58`, `:120` weather, `:184`, `:200`, `:220`, `:226`: protected by the triage.
- `:82` "Watched the part of her she'd been apologizing for become, in his hands, something worth getting right.": hers.
- `:96` "The pad was full of her…": the section's close; her summary of the tide.
- `:116` "He hadn't seen it. He couldn't have seen it…": her bargaining; the repetition is the anxiety.
- `:152` "The hope was visible.": her bitter wit.
- `:188` "physically, in her body… the rearranging of how she was carrying herself": readers carry it (glm "her posture physically rearranges"; flash "you could physically feel her spine straighten").
- `:198` "Something shifted in her… a kind of power she'd never been issued": adopted by fable and glm ("best character…").
- `:232` "He knew she knew.": her read of the shared game.
- `:242` "the dazed new knowledge of two things at once": her processing ("*her*, she'd nearly done that").
- `:246`–`:248` the close: praised by name across five files; the line edit already cut the caption after it.

## Rulings

- 1 `:56` "She had not anticipated this part… only half of it." — **withdrawn** (author: her perspective, her surprise at how different he is). Not a repeat: `:52`/`:54` are about the withdrawal; `:56` is about his frank, unhidden looking ("He wasn't sneaking glances. He was looking."), her surprise answering the ogling she braced for at `:34`–`:36`.
- 2 `:130` "not building a dress on a form… *for her*" — **withdrawn** before review, on the same test: her realization at the turn ("The thought did not last. The way he worked would not let it."), and `:134` deepens it (the picture in his head) rather than repeating it.
- 3 `:174` "That was the bravest thing she did all day, the not being able to stand it." — **cut** (author). Narrator's retrospective verdict ("all day") grading her at the suspense peak.
- 4 `:202` — **4a** (author): "and they both felt the difference in it" → "and she felt the difference in it" (the touch reported from her side only).

**Applied 2026-10-26:** 3, 4a. Lint: 0 errors. One new warn, created by 4a: `filter-verbs` at `:202` («she felt»), surfaced to the author and not acted on. Otherwise the plain run is unchanged (103 → 104 hits). praise_check over the diff: only opus-5-5's "bravest thing this book has done", which is about the wet satin. orphan_refs (a-round, two-towels): only the two historical `7f94afe2` candidates.
