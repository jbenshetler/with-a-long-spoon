# Line audit — sorority (2026-08-01)

**Verdict:** 6 issues found — 1 fix, 3 clarification, 2 nitpick.

## Findings

1. **"the two narrow beds and the milk-crate shelves and the Stevie Nicks poster"** (line 5) — Canon establishes Vee and Cassie's double as a **bunked** room, not two side-by-side beds: `scenes/toenails.md:3` ("Cassie was on the bottom bunk"), `scenes/may-i-choose.md:7` ("Cassie folded up on the bottom bunk"), `scenes/turned-up.md:171` ("the top of the bunk") and `:209` ("grinning at the underside of the top bunk"). "Two narrow beds" (and, secondarily, "Cassie's side — the bed made tight and square" at line 7, which reads as a side-by-side layout) contradicts the established furniture. **Severity: fix.** Recommended: rephrase the room inventory so the sleeping arrangement matches the bunk established in the three earlier scenes.

2. **"the Stevie Nicks poster, *Bella Donna*, she'd hung freshman year … lit by what she'd brought in with her"** (line 5) — Two "she"s in the same long sentence with different referents: the poster-hanger is Vee, but the sentence's governing subject at that point is Randi ("taking the whole double in"), and the closing "she'd brought in with her" is Randi again. A first-pass reader can momentarily attach the poster to Randi. **Severity: clarification.** Recommended: anchor the poster clause to Vee by name or restructure so the two referents don't alternate unmarked.

3. **"You've made me wait a whole week"** (line 7), **"the picture she'd been rehearsing in private for a week"** (line 99), **"a man who had thought of nothing else for a week"** (line 101) — The elapsed times run long against canon: the fitting was Sat Oct 3 (`{{A Round}}`), today is Sat Oct 17 — exactly two weeks; Randi has been "hearing about it" since the brunch telling Sun Oct 4 (`{{How It's Done}}`, chronology); and `scenes/peekaboo.md:19` itself calibrates the making as "A week and a half ago it had been a flat bolt of cloth." Randi's spoken line can pass as hyperbole, but the two narration instances (lines 99, 101) sit in Vee's free indirect and undercount what Peekaboo's own prose counted. **Severity: nitpick.** Recommended: loosen the narration's two "a week"s toward "two weeks" / an unnumbered duration, or accept as idiom.

4. **"The woman who worked there came over with the box"** (line 87) — The attendant arrives carrying the right-size box, but no one in the boutique has been told Vee's size (the "Seven" exchange happened at the first store; the attendant wasn't there). A small off-page step is missing. **Severity: clarification.** Recommended: give the size-request a half-beat (Randi asking, or the attendant asking) or make the fetch visibly follow one.

5. **"The heel went on. Randi did the little buckle at the ankle … and Vee rose up into them"** (line 95), then **"both flats gone, all leg now"** (line 99) — Only one flat is removed (line 89, "slipped the flat off") and only one heel is narrated on, yet Vee rises into "them" and both flats are gone one paragraph later; the second shoe happens nowhere. A careful reader stumbles on the singular-to-plural jump. **Severity: clarification.** Recommended: a two-word acknowledgment of the second shoe (or make the plural arrive after a beat that plausibly covers it).

6. **"gone a full head taller and taking it like it cost her nothing: six-inch platforms"** (line 43) — Randi was already wearing heels (now "hooked off two fingers"), so the net gain over her prior height is well under six inches, and "a full head" is ~9–10 inches even from flat. Reads as Vee's comic hyperbole and probably intended, but the sentence frames it as observation. **Severity: nitpick.** Recommended: leave if the hyperbole is deliberate; otherwise soften "a full head."

## Verified clean

- **Date/weekday:** Sat Oct 17 (chronology); consistent with Sun Oct 4 = `{{How It's Done}}`. No calendar date or weekday appears in the scene header or prose (per convention).
- **Setup continuity:** the Saturday shoe-trip was bound at `{{All Told}}` (Fri Oct 16, "How's Saturday"); Randi has heard about but not seen the dress — consistent (gown "home at the dorm, zipped, shown to no one").
- **Mercedes callbacks:** "dark green going to black" and the frameless window dropping "its half inch to the handle on its own" match the first ride, `scenes/how-its-done.md:5,11`; "more easily than the first time" correctly implies exactly one prior ride.
- **Mirror / sun-porch callbacks:** "seen in his mirror," rising "onto her bare toes … instead of waiting on a height she wasn't giving it," and "stood in his sun porch and cried" all check against `scenes/peekaboo.md:15,19,21,37,41` (new full-length mirror, on-toes rise with the same "height she wasn't giving it" figure, happy tears at the unveiling).
- **Toenail polish:** frosted plum already on Vee's toes is canon since `scenes/toenails.md:33` (painted for the Famished date, Oct 9); "chosen to catch the light as the silk did" is plausible (she saw the silk Oct 3) and matches the chronology's induction note ("Nails: frosted plum … matched at {{Sorority}}").
- **Shoe-size seed:** the same-size-7 discovery matches the chronology's shoe-loan motif design (registry: "same size," shoes circulate); four-inch black heels match the induction entry ("black four-inch heels Randi steered her onto at {{Sorority}}").
- **Planned beats present:** the impulse-buy plant (Randi's loafers, worn out of the store), the dorm→bypass→boutique triptych, the "buckled" seed (line 95), the credit-card transgression vs. Randi's careless multiple, no scrunchie layer.
- **Props/inventory through the scene:** garment bag (door → bathroom → zipped → car → boutique brass hook, top foot unzipped → Randi's arm on the sidewalk); the tan heel (found, held, vetoed, never bought); Randi's own heels (worn → carried during the platform gag → boxed at the boutique); box/bag/rope handles at the exit all reconcile ("the boxes and the bag").
- **Body positions:** Randi's kneel → buckle → sit back on heels; Vee seated → hand to Randi's shoulder → standing; the try-on benches stay bolted and consistent.
- **Dialogue logic and attribution:** every reply tracks its prompt (yeti gag → "About all those yetis" payoff; "It's the sensible one" echoed and turned); no attribution errors found.
- **Character facts:** Vee is a junior (`meta-arch-vivienne.md`: "entering her third year"), so the poster "hung freshman year" is sound; Cassie as roommate, absent, is consistent.
- **Payment logic:** debit-vs-credit beat is internally consistent and consistent with line 53's "a price that didn't make the debit flinch."
- No `meta/meta-triage-sorority.md` exists; nothing re-litigated.

## Author rulings (2026-08-01)

1. **Fixed** — ":5 the bunked beds"; ":7 Cassie's bunk — made tight and
   square" (bunk canon restored).
2. **Fixed** — ":5 Vee'd hung freshman year" (was "she'd").
3. **Left standing** — all three "a week"s: hyperbole + free-indirect
   felt-duration ({{Fed}}/{{How It's Done}} precedent).
4. **Left standing** — luxury-register elision; the off-page size ask is the
   store working.
5. **Left standing** — deliberate second-shoe elision ({{Toenails}}
   undress-elision precedent).
6. **Left standing** — comic felt-magnitude in the gag paragraph.

See `meta/meta-triage-sorority.md`.
