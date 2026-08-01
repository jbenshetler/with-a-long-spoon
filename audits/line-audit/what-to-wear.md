# Line audit — what-to-wear (2026-07-31)

**Verdict:** 3 issues found — 1 fix, 1 clarification, 1 nitpick. Otherwise clean.

## Findings

1. **"Six weeks running, nobody had."** (opening paragraph, on eating at the athletic dorm since the routine started)
   - **Problem:** Calendar contradiction. The scene is pinned to Thu Oct 1; the chronology anchors fall classes at ~Mon Aug 31. Oct 1 is only ~4.5 weeks into the semester — even generously counting an early move-in week, six weeks of dinners there isn't possible.
   - **Severity:** fix
   - **Recommendation:** Reduce the figure to something the calendar supports ("four weeks running" or an unpinned "weeks running").

2. **"She'd had the shirt, folded on her pillow at this exact hour of the night."** (interior beat after "It's the least information a human being has ever sent me")
   - **Problem:** Genuinely unclear referent for the time phrase: the scene is a ~6–7 p.m. dinner in golden light, so "this exact hour of the night" doesn't parse — it's not night, and it's ambiguous whether the sentence means the shirt is on her pillow right now, or that it has habitually been there at some (which?) hour.
   - **Severity:** clarification
   - **Recommendation:** Rephrase the time reference so the reader knows whether this is "the shirt is lying on her pillow at this very moment" or a nightly ritual, without the "night" mismatch against the dinner-hour setting.

3. **"Then I backed him into a tree and we made out. For a while."** (Vee's account of the second-date kiss)
   - **Problem:** Contradicts the on-page staging in `scenes/may-i-choose.md` (lines 95–115): a tree's *shadow* fell across the path, he slowed and stopped and started them gently back, and she closed the distance he'd already given up — nobody was backed into anything. The scene elsewhere licenses her embellishment ("She could hear the story getting better in the telling and did not care"), so this is very plausibly intentional performance, but it's the one retold beat with no in-text embellishment cue attached.
   - **Severity:** nitpick
   - **Recommendation:** Confirm the exaggeration is intended (and covered by the earlier embellishment cue); no change needed if so.

## Adjacent note (out of scene, no action here)

- Cross-corpus flag worth a look elsewhere: `scenes/nothing-underneath.md` has "Kayla from two doors down," while chronology flag 22 places **Meg** "two doors down from Vee" ({{Lesson}}). Not touched by this scene (no door geography stated here), but the dorm-floor map should pick one.

## What was checked and found clean

- **Date/weekday:** Thu Oct 1 matches the chronology entry (real-calendar 2026: Oct 1 is a Thursday). "Two in the afternoon is not dinner" and the Saturday 2 o'clock invite match {{Two Towels}} (Sat Oct 3, afternoon).
- **Elapsed-time math:** "Twelve days" since the second date is exact (Sat Sep 19 → Thu Oct 1); "I don't kiss a man I've known two days" is exact (met Thu Sep 17, kissed Sat Sep 19); "a couple weeks ago" and Theo's "In September" ask both consistent.
- **Retold hike vs. `leave-no-trace.md`:** shirt reached from behind the seat, packed-for-himself flannel, his stepping back out into the rain with his back to the truck, the shivering that stops the kiss, the fire-lane/overhang drop-off, the blue-and-white with lights, the single siren bark, the cop following him out to the road — all match the drafted scene. Her omission of the strip-facing-him beat is in-character concealment, not an error.
- **Character facts vs. `meta/meta-arch-bible.md` / `meta-arch-pace.md`:** Pace 22, math PhD candidate nearly finished, competitive powerlifter — all canon (start-of-novel age correct for Oct).
- **Friend continuity:** Meg "dark-haired and level" matches her {{See You Later}} intro ("dark-haired, unhurried"); Meg coupled (boyfriend story) per flag 22; Kayla's chatterbox register matches {{Nothing Underneath}}; Theo's one job (asked her out, took "let's be friends" well) matches flag 22.
- **In-scene object/space continuity:** Meg's fork (telling with it → pointing it → setting it down), Vee's glass (two turns), the fries (stolen and stolen back), the phone (buzzes face-up → held out of reach → turned over), seating (corner table, Vee between them), lighting arc (gold at six → orange → thin) — all consistent.
- **Dialogue logic:** every reply tracks its prior line; no attribution errors (consecutive Kayla paragraphs at "He's nice" / "So what's Pace do" are both tagged).
- **Pronoun referents:** no ambiguous she/he/it that would misassign an antecedent.
