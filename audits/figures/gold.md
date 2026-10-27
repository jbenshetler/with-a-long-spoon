# Figure sweep — acceptance set (gold)

The recall test for `tools/figure_harvest.py`. Every **FIND** line must come back
from extraction. Every **LITERAL** line must not come back as a figure. This file
is a test fixture, not a ruling: nothing here has been judged designed or
accidental. Those rulings go in `audits/figures/rulings.md` once the sweep runs.

The set was assembled 2026-10-27 by `rg` and by reading. It is deliberately
built from cases a word search handles badly:
- the remembered phrasing is wrong ("missed a stair" is written "like a missed
  stair", and "taken stairs too quick" was "too fast");
- the figure has no simile marker ("climbing the same stair", "that was the
  rail on the stair");
- the same picture is applied to different people (the lamp);
- different pictures render the same feeling (the drop).

Format: `- FIND|LITERAL slug:line · group · quote`. The tool parses these
lines. A line number may drift by a few lines after an edit; the scorer matches
on slug plus quote and uses the line only as a hint.

## Picture: stairs

- FIND recognized-method:23 · stairs · like a missed stair
- FIND boyfriend:13 · stairs · the way you reach for the rail on a stair
- FIND boyfriend:203 · stairs · that was the rail on the stair
- FIND postcard:53 · stairs · the way you come down a stair in the dark
- FIND how-its-done:312 · stairs · carried up too many stairs
- FIND grace:245 · stairs · climbing the same stair

History only, not in current prose: `substitution.md` "had taken stairs too
fast", cut 2026-10-25 by `a79bb2d7`. A history sweep (`--rev`) should find it
there.

## Picture: lamp, light coming on (attention, presence)

- FIND practice-room:39 · lamp · her attention coming on like a lamp
- FIND sorority:21 · lamp · like a lamp finding you
- FIND how-its-done:239 · lamp · like a room light coming on
- FIND how-its-done:270 · lamp · turned to her like a lamp
- FIND under-the-rug:53 · lamp · like a light turned up
- FIND among-friends:17 · lamp · Like he was a lamp
- FIND gone:67 · lamp · Like somebody found the lamp

## Picture: sun (attention as warmth)

Author ruling 2026-10-27: a different picture from the lamp; its own group.

- FIND how-its-done:15 · sun · felt the attention like sun on her face

## Picture: lit from inside

- FIND the-induction:43 · lit-within · like it was lit from inside
- FIND peekaboo:15 · lit-within · the burgundy lit from inside itself
- FIND old-acquaintances:19 · lit-within · lit like it held its own light
- FIND grace:127 · lit-within · lit from within

## Picture: held up to the light

- FIND see-you-later:123 · held-to-light · a thing you held to the light
- FIND clean-plate:97 · held-to-light · hold a thing up to the light to see it

## Feeling: the sudden drop (different pictures, same sensation)

- FIND recognized-method:23 · drop · like a missed stair
- FIND substitution:243 · drop · the high-board drop, nothing under her
- FIND vee-on-the-bench:57 · drop · her stomach dropped the way it always dropped
- FIND a-round:88 · drop · Her stomach dropped as if
- FIND how-its-done:274 · drop · Vee's stomach dropped toward it
- FIND boyfriend:101 · drop · The floor went out from under
- FIND one-bite:153 · drop · the floor went out from under Vee again
- FIND my-friend-randi:127 · drop · her stomach went over

## Literal — must NOT be reported as figures

- LITERAL covering:27 · stairs · a loft up a steep little stair
- LITERAL covering:255 · stairs · went down the little stair
- LITERAL standards:107 · stairs · Eight steps to the landing
- LITERAL clean-plate:141 · stairs · The food came up the stair
- LITERAL fairytale:83 · stairs · The stair curved
- LITERAL my-friend-randi:33 · stairs · coming down them fast
- LITERAL made-up:35 · lamp · the lamp throwing its circle
  Known false positive (author ruling 2026-10-27): claude-sonnet-5-5 reads
  "throwing" as a figurative verb. The lamp is literal; the hit stays
  listed here and is not a reason to tune the prompt.
- LITERAL gone:7 · lamp · the lamp low
