# Line audit — may-i-choose (2026-07-31)

**Verdict:** 5 issues found — 1 fix, 2 clarifications, 2 nitpicks. Prose body is internally consistent; the one hard error is in the header line.

## Findings

1. **Header date contradicts the chronology.**
   > *[SCENE / half-scene] · early fall · ~Sat Sep 26 · the second date · Vee's POV*

   `meta/meta-plan-chronology.md` places {{May I Choose}} at **Sat Sep 19** (after Water Wings, Fri Sep 18; before Dear, Fri Sep 25, and the third date Leave No Trace, Sun Sep 27). The scene's own internal clock confirms Sep 19: the froyo date was Thu Sep 17 ("hours after the meet-cute," per the chronology's Long Way entry), the text arrives Friday evening ("The froyo had been yesterday, and here he was asking for tomorrow"), and Vee's "I don't kiss a man I've known a couple of days" only works if the meet-cute was two days ago, not nine. The `~Sep 26` looks like a stale pre-redate value. **Severity: fix.** Recommended: change the header date to Sat Sep 19.

2. **"an hour ago over a glass of tea" mislocates the earlier surrender.**
   > "She'd done it an hour ago over a glass of tea and the world hadn't ended."

   The letting-the-thread-go happened at the table during the meal (the drip beat, "The thread went and she let it go"), well *before* the tea — the tea is what surfaced her from it. A careful reader who tracks the sequence will stumble on the surrender being attributed to the tea moment. **Severity: clarification.** Recommended: re-anchor the callback to the table/dinner rather than the tea (or accept as loose shorthand if intentional).

3. **The smoke-dark dip's color shifts.**
   > "The bright green one. The smoke-dark one under its dust of spice." … later: "scooped a little of the tan dip under its dusting of red-brown spice"

   The same dish (baba ghanoush) is visually "smoke-dark" at arrival and "tan" when eaten; the second passage then calls its taste "smoke-dark," so the identification is recoverable, but the color flip can momentarily read as a third dish. **Severity: clarification.** Recommended: keep one visual color for the dip and let "smoke-dark" stay a flavor word.

4. **"the right hand again, a pattern now" — no prior on-page hand observation.**
   > "It was the right hand again, a pattern now, enough times over to be one: always the right, never the other…"

   Neither earlier eating beat (the bread-tear/fold, the second dip) specifies which hand, so "again" points at noticings that never landed on the page. Readable as summarizing accumulated off-sentence observation (and it's a planned hand-motif plant), but the "again" has no textual antecedent. **Severity: nitpick.** Recommended: either specify the hand in one earlier beat or soften "again."

5. **She grips the hot cage the handle exists to avoid.**
   > "made… so you could hold them while they were still too hot to hold. She wrapped her hands around the little brass cage and the heat came through it, just bearable"

   The sentence first explains the handle's purpose, then has her bypass it and wrap the cage itself; a literal-minded reader may hitch on why the just-explained affordance goes unused. Works as a character beat (wanting the heat), but the juxtaposition is slightly self-undermining. **Severity: nitpick.** Recommended: no change needed unless the author wants the handle explanation trimmed or her choice of grip made faintly deliberate.

## Checked and clean

- **Friday/Saturday clock:** text Friday evening → froyo "yesterday" (Thu) → dinner "tomorrow" (Sat) — internally consistent.
- **Water Wings tie-in:** the Friday pool afternoon ("chlorine in her hair") matches Water Wings on Fri Sep 18.
- **"two years of living a ten-minute walk away":** matches Vee as a junior entering her third year (`meta-arch-vivienne.md`).
- **Hunger continuity:** no food since breakfast, noon missed to the dress/shoes prep, "hollow from noon" callbacks — all consistent.
- **Elevator/lobby blocking:** she sees him from inside the elevator, doors time out, she exits — coherent.
- **Meal sequence:** menu → "May I choose?" → order → talk before food → dishes arrive → tabbouleh first, baba ghanoush second, drip, tea last — no prop or order contradictions (she never orders the hummus herself; he takes over — consistent).
- **The taut-hand beat:** "her hand drawn along with his" then pulling taut "a few inches on" reads as one continuous motion, not a contradiction.
- **Christine, coat, night walk, moonlight, campus route:** no contradictions; the coat is unestablished earlier but nothing contradicts it.
- **Pronouns and dialogue attribution:** clear throughout; every reply answers the prior line (Cassie's "He's not making you wait" answers the delay-comparison Vee then articulates).
- **Tense:** consistent past throughout; the section-two opener's pluperfect frames are correct.

## Rulings (2026-08-01)

1. Mooted — header dates stripped repo-wide (2026-08-01 convention: chronology owns dates); Sat Sep 19 stands in the chronology.
2. Fixed (author wording) — "over a glass of tea" → "over warm bread": true to the staging (tea is the waking agent), and both kiss-moment callbacks (the letting-go, the hand) now point at the same table image.
3. Fixed — "the tan dip" → "the dark dip": three dishes are ordered (her hummus, his baba ghanoush + tabbouleh); the line had fused hummus's color with baba's taste; the bright/dark pairing is his two dishes by design.
4. Left standing (no record) — "the right hand again" is POV summary of accumulated watching; "enough times over to be one" supplies its own antecedent; planted motif lands when Vee consciously registers it.
5. Left standing (no record) — gripping the hot cage past the explained handle is the beat: sensation chosen over protection, legible only because the handle's purpose is stated.
