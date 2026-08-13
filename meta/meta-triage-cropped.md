# Triage — Cropped (line audit, 2026-08-03)

Sentence-by-sentence consistency/logic audit (`audits/line-audit/cropped.md`).
**Clean — 0 findings.** Photo-crop mechanics, dateline (Sun Nov 29), dress
backstory, ages, in-scene props, and the dorm-friends name-drop guard all
verified; prior triage verdicts respected. Housekeeping only: chronology
`present:` corrected to `Vee, Cassie` (Cassie is the second party throughout).

---

# Triage — Cropped (`cropped.md`)

Cold-read feedback pass, 2026-07-29. Panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol (all read after {{The Outlier}}). Reception was near-frictionless across all four; only two friction points surfaced, both from Opus alone.

## Fixed

- **"She had a gift for knowing when a door was closed" cut** (final paragraph). Opus flagged it as telling; lore-keeper check confirmed the trait is already *shown* in `school-nights.md:29-33` (Cassie letting the "maybe" stand, going back to her book) and the phrase is not a preserved line anywhere in meta/. The beat now reads: "Cassie nodded and went back to her plate. She didn't push at it." The behavior carries the trait without the label. (Commit: this pass.)

## Fixed (2026-07-30 scene-review pass)

- **The collarbone-exchange echo reworded.** Author found "You know the one." / "I know the one." awkward — "the one" refers back to the mother's gesture but dangles. Now: *"You know how she does." / "I know how she does."* The call-and-response echo shape is preserved deliberately: all four cold readers quoted this exchange as a high point, and it was the *echo*, not the specific words, that landed. **If the next review panel snags on the new wording, the prior version is a known-good fallback — revert candidate, not a re-litigation.**

## Left standing — do not re-litigate

- **The "essay moment" — "Wrong is something he understands and rejects. Weird is something that doesn't fit anywhere in how he sees the world."** Opus alone said the arithmetic monologue "edges toward essay for a moment," then self-retracted ("it's in character; she's the girl who prices everything. I bought it"). The other three readers praised the same passage — fable-5 called "weird is worse than wrong" "the sharpest sociology this book has done in a while." Author ruled: keep as is.
- **The `x-not-y` cluster in the closing stretch** (linter, lines 39–41: "exact, not prying"; the triple "not the… not the… not the"). The line-41 triple is deliberate anaphora — Vee failing three ways at once to fit the truth into Cassie's frame — not a tic. Author ruled: stands.

## Left standing — line edit, 2026-08-12

Report: `audits/line-edit/cropped.md` (13 findings). Panel confirmed fresh — six of
seven cold reads postdate the scene's last commit; the only line-level criticism
anywhere in the panel was sol's note on the closing tricolon, already ruled above.

- **Cassie's high-school beat** (:7, "They still treat me like I'm in high school.
  Not overtly. But I can tell they don't quite see me as an adult yet."). Editor
  called the third sentence an abstract restatement of the first. Author ruled:
  stands — it is Cassie's only self-disclosure and the setup that lets Vee go
  second; trimming it turns an exchange into a prompt.
- **"A little bit of a dork."** (:7). Editor flagged the four-word run-up as
  grammatical where Cassie elsewhere clips. Author ruled: stands — the looseness
  is characterization, and it is what makes her later compression read as a shift.
- **"In some ways weird is worse than wrong."** (:35). Editor proposed cutting the
  hedge in front of the reader-quoted formulation. Author ruled: stands — the
  qualifier is the sound of a nineteen-year-old working something out rather than
  pronouncing a maxim, and four readers responded to the line in its hedged form.
  (Reinforces the "essay moment" verdict above.)
- **"fit" three times** (:25, :35, :39). Logged, no action, so a later pass does not
  raise it as new. :25/:39 are a designed bookend in the same sense; :35 is a
  different sense inside protected material. If :25/:39 are ever reworked, keep the
  pair and let :35 be the one that gives.

Applied in the same pass (recorded so the passages are not re-flagged as unchanged):
opening sentence split (:3); "syncopated" → "punctuated" (:3); ", which was the
right call" cut (:21); the free tray beat cut (former :27), leaving two; two of five
"And" paragraph-openers unhooked (:21, :27), leaving three; "doing the math" →
"pricing it" (:27); both filler "really"s cut (:27, :29); the verbatim cooks/owns
re-list cut (:29); "And the strange thing is," cut (:35).

## Confirmed positives — protect in any future edit

All four readers, independently: the title's crop-extends-to-biography mechanism; "Sex he understands. The sewing he never would."; "weird is worse than wrong"; the collarbone exchange (reviewed as "You know the one." / "I know the one."; reworded 2026-07-30 to "You know how she does." — the echo shape is the protected element); the ending couplet ("Both. Probably both." → "Vee was grateful. She was also, a little, not."). Vee's inability to name Pace and Cassie's unpushed door landed exactly as designed on all four readers — working as designed, no fix wanted.
