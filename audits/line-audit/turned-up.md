# Line audit — turned-up (2026-08-01)

**Verdict: 9 issues found — 1 fix, 4 clarifications, 4 nitpicks.** No date/weekday errors; the scene's cross-references to the hike, {{Rye}}, {{Two Towels}}, and {{A Round}} are otherwise accurate.

## Findings

1. **"And I could feel his — " Vee reached back and patted her own ass ... "His *package.* Right here. When he was pinning the back seam." / "*I* was grinding on *him.*"** (lines 189–205, the closing comic run)
   - Problem: cross-scene contradiction with `scenes/a-round.md`. In the source scene all back-seam and hem work is done **on his knees** (a-round line 154: "He'd been on his knees since the side seam, and he stayed on them"); his crotch is never at her ass, and the scene never renders Vee feeling his erection anywhere. The only standing-behind contacts are his palm between her shoulder blades (a-round 232) and hands on her ass (a-round 156). The chronology entry for {{A Round}} also specifies the fitting's whole point is *deferred* tension with "Keep still" holding the line. The scene frames this not as embellishment but as "the thing she'd been keeping all the way at the bottom" — i.e. true.
   - Severity: **fix**
   - Recommended fix: either seed a brief standing-behind, felt-hardness beat into `a-round.md` (kneeling geometry currently forbids it), or re-anchor Vee's claim to contact the source scene supports (his hands/breath while she leaned into him), or explicitly frame it as her exaggerating.

2. **"Vee was up again, narrating with her hands."** (line 87)
   - Problem: internal blocking error — Vee has been standing since line 59 ("Vee was up again, to the window and back") and is never re-seated before line 87, so the second "up again" contradicts her tracked position.
   - Severity: **clarification**
   - Recommended fix: render a sit between lines 75 and 87, or drop "up again" at one of the two spots.

3. **"Then Cassie shifted against her pillow"** (line 177)
   - Problem: Cassie was established at her desk (line 7) with knees pulled to her chest in the chair (lines 31, 47), and at line 169 reaches over to touch Vee's knee from that station; her move onto her own bed is never rendered, yet by 177 she is against her bed pillow — with Vee simultaneously seated on (and at 209 lying across) that same bottom bunk.
   - Severity: **clarification**
   - Recommended fix: add a small positional beat moving Cassie from the desk chair to the bed sometime before line 177 (and confirm the two of them sharing the bottom bunk at 209 is intended).

4. **"Vee sat down on the edge of the bed."** (line 49) vs **"Vee sat down on the edge of Cassie's bed. Just the edge."** (line 137)
   - Problem: line 49's "the bed" is ambiguous — since Vee's own bed is the top bunk (lines 171, 209), it can only be Cassie's; but then line 137's careful "Cassie's bed. Just the edge." reads as a first, weighted act although she already sat there at 49.
   - Severity: **clarification**
   - Recommended fix: name the bed at line 49 (or seat her elsewhere there) so line 137's deliberate edge-sit keeps its charge.

5. **"...the shirt Pace had made was folded on Vee's pillow at the top of the bunk because she'd put it there without thinking when she changed."** (line 171)
   - Problem: "when she changed" has no in-scene antecedent — Vee walks in and talks; no change of clothes is rendered, so the reader must guess (that morning? just now, off-page?). Genuinely stumble-inducing on the scene's key closing image.
   - Severity: **clarification**
   - Recommended fix: anchor the moment ("that morning" or equivalent) so the timing of the placing is unambiguous.

6. **"The induction," Cassie said softly. ... / "And he just —" / "He just." Vee spread her hands.** (lines 21–25)
   - Problem: paragraph-alternation convention momentarily assigns "And he just —" to Vee (it follows a Cassie paragraph), and the misread only corrects at line 25.
   - Severity: nitpick
   - Recommended fix: attach a brief attribution or Cassie-side gesture to "And he just —".

7. **"He has had you standing in his living room in your underwear..."** (line 179)
   - Problem: Vee told Cassie it was the sun porch (line 59: "on the long table in his sun porch"); Cassie's "living room" is a plausible loose paraphrase but is a within-scene mismatch a close reader may catch.
   - Severity: nitpick
   - Recommended fix: keep only if the compression is meant as Cassie's shorthand; otherwise say "his house."

8. **Cassie stopped laughing ... "You did?"** (line 135, reacting to "And then I let him look")
   - Problem: Cassie already heard this in {{Rye}} ("I took my wet shirt off in front of him. On purpose. ... and he just looked" — `scenes/rye.md` line 41), so surprise at the fact re-litigates known information; defensible if the beat is meant as reaction to Vee's changed register rather than the fact.
   - Severity: nitpick
   - Recommended fix: if intended as register-shock, no change; otherwise tilt the line toward reacting to *how* Vee says it, not the news.

9. **"Vee threw a pillow at her."** (line 121)
   - Problem: Vee is standing mid-room (up since line 87); the pillow's source is unanchored — workable in a dorm room, but the prop appears from nowhere and later does double duty (caught, hugged, thrown back, hugged again) alongside Cassie's own bed pillow at 177.
   - Severity: nitpick
   - Recommended fix: a two-word anchor for where the pillow comes from.

## Verified clean

- **Calendar:** Sat Oct 3 (hidden-year 2026) is a real Saturday; hike Sun Sep 27 → "sleeping in that shirt all week" and "breakfast on Tuesday" (Sep 29) both work.
- **Cross-scene facts confirmed:** silk-naming over the cherries on the summit rocks (`leave-no-trace.md` 121–137); the mirror beat with the silk at her face (`two-towels.md` 105); "I couldn't find a shirt I liked, so I made one" verbatim (`two-towels.md` 123); the no-tag shirt; the riser/box; bra-off order and "It changes the line" (`a-round.md` 21–28); heat-turned-up-hours-before (`a-round.md` 19); knees-for-the-hem and top-down measuring; shirt-off count of two; "never seen naked" (true — only kissed, first kiss at {{May I Choose}}); Cassie's "built" knowledge from {{Rye}} supporting the bodybuilder/powerlifter exchange; Vee's powerlifter knowledge (seeded at {{What to Wear}}); dress unfinished at scene end matching header and chronology.
- Dialogue logic elsewhere tracks (the Yes/No at line 99 answers Cassie's double question; the pivots at 75 and 179 are motivated).
