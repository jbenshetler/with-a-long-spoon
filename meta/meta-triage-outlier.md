# Triage — The Outlier (line audit, 2026-08-02)

Sentence-by-sentence consistency/logic audit (`audits/line-audit/outlier.md`).
4 findings: 2 fixed, 2 left standing.

## Fixed

- **Cassie's blind verdict named specifics the graph can't show** (:79) —
  "One holding company, a stack of loans" wasn't derivable from a point's
  position, and sourcing it to her data-pull implied she'd seen the name.
  Now "One company, that size, everybody cut anyway" (author's wording) —
  her read comes entirely off the point's visible size, which also credits
  Randi's graph (size encodes scale; only companies could apply).
- **Drill-down silently changed what a point is** (:45) — counties-as-points
  switched to companies-as-points on "pulled up her own," inviting a brief
  misread that Randi's *county* was the outlier. Now "pulled up the companies
  in her own county" (author's wording, tail retained — "driving now" and the
  aiming clause stand).

## Left standing — do not re-litigate

- **"The laptop" at :89** (definite article, no named owner) — stands; the
  beat is the gesture (Vee taking over Randi's machine), context carries it,
  and naming the owner adds bookkeeping to a sentence about the hands.
- **Closing image's literal mechanics** (:95 — closed laptop displays
  nothing; the point "goes back" twice) — stands as deliberate figuration:
  :83's return is Randi's keystroke, :95's is the camera's; the image lives
  in Vee's head, not on a screen. Register already triage-protected.

Also: chronology `present:` corrected to include Cassie (on the page through
both panels).

---

# Triage — The Outlier

*Cold-read panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol (all read after {{All the Time}}). Feedback pass 2026-07-29; the panel's reviews predate the 2026-07-28 surprise-legibility edit (25516df).*

## Confirmed positives — protection, not praise

Any later edit must not damage these:

- **Randi's stillness** — "Not a motion — the withdrawal of motion." All four models singled out the bodily precision of the shock (color, breath, hand frozen on trackpad); fable-5 called it the best thing on the page.
- **"Cheating bastards" landing wrong** — all four heard the register as intended (intimate, first-time, not stranger-aimed). The two-words-no-clause discipline holds (see `meta-note-outlier.md`, hinge line).
- **Cassie's flat delivery** — "My dad got laid off in 2020" ("no handle left out") and "didn't carry things into rooms she meant to walk out of," quoted admiringly by all four. "Right and doesn't know how right" (opus); "the book's plumb line" (fable-5).
- **Vee's protective silence** — "somewhere to put her hands" quoted by three models; the invented exculpating story read as "her whole tragedy in one paragraph" (fable-5), "love as suppression of evidence, mirror-inversion of Randi's love-as-extraction" (opus).
- **The heat-0 pivot** after two intimacy chapters — all four called it earned.

## Fixed

- **Randi's shock read as old knowledge, not surprise** (3 of 4 models refused to grant her ignorance). Ruled and fixed **2026-07-28** (commit 25516df): discovery beat added (the fast-then-slow double read), curse gloss recast from "floor under it" to first-time rawness. Full ruling in `meta-note-outlier.md` § "She didn't know" — do not re-litigate, do not restore the floor-under-it phrasing.
- **Lecture a touch schematic; "the exception often proved the rule" the thumb closest to the scale** (opus; gpt-5.5 softly). Fixed 2026-07-29: the proverb clause cut — the one time the professor spoke in idiom rather than method. The set-aside clause (load-bearing for Vee's later move) stays. Companion ruling: the stats-mirror discipline is (1) the professor delivers method, never meaning; (2) Vee's misfiled transcription is the punchline; (3) the lecture stays subordinate to a social beat. One-in-four reviewers getting the running joke is the intended hit rate; consensus legibility would mean it's too loud. The same discipline governs Dr. Marsh in spring.
- **Cassie's "Told you" cut; Randi's reply recast** (scene-review pass 2026-07-29, author ruling). "Told you," however mild, breached the never-a-crow rule (`meta-note-outlier.md` § Cassie) — and it's more Cassie to spend no words on Randi; her satisfied face is her entire statement. Randi's second-person reply ("You told me the country…") also read as engagement with Cassie, off the asymmetric-enmity canon (Cassie is not a player in Randi's exchange). Replaced with one line aimed at the data: *"The country isn't my county," Randi said.* — concession and stake in the same breath, no address.
- **"She knew whose it was." replaced** (2026-07-29, author's line). The sentence had no clean antecedent and told what the surrounding prose already showed. Now: *"There could be no other Miranda."* — the recognition as felt certainty (no deduction), with Vee's aspiration register in it (Randi as one of one); reader-only second register: the girl and the company are one name. Completes the Miranda toll 61→65→67 (entity → remembered name → verdict).
- **Name-origin contradiction with the {{See You Later}} name-bit fixed** (2026-07-29, author ruling). "the name Randi had been given and filed down" read as Randi coining her own nickname, against the bit's "my parents had a sense of humor." Ruled: the parents named her Miranda and deliberately called her Randi — the joke theirs, the routine her pre-emption (recorded in `meta-arch-randi.md` § Aliases). Line now: "…the long formal version on the chapter paperwork of the name her parents had given her and then, with a sense of humor, shortened to something a person could stand to answer to."
- **Style pass** (linter, 2026-07-29): second figurative "weather" cut (line ~53); "small" dropped from "a small shift" and "a small nod." Remaining hits acked with notes in `style/style-allow.toml`; scene scans clean.
- **Author line-read pass, 2026-07-29** (post-panel):
  - **PPP gloss extended for non-US/younger readers** — now "the government money that was supposed to keep people on payroll — forgiven on the employer's say-so that it had." The self-certification clause is the one mechanism a cold-to-PPP reader can't infer, and it's what makes "Cheating bastards" a moral verdict with no court behind it. One clause, once, at the teaching moment — inside the "gestural, never forensic" ruling (`meta-note-outlier.md`). Deliberately **excluded**: "and mostly didn't" — the verdict belongs to Cassie's thesis and the graph, not the narration; front-loading it would pre-refute Randi and editorialize.
  - **"and already checked" cut** from Cassie's thesis line — premise leak: the project's engine is belief proven later by the data; she hadn't done the work yet. "She said it like a fact she'd looked up, which she pretty much had" stands (headlines-vs-data: absorbed the national coverage, hadn't run the numbers).
  - **"no weight on it" cut** from the laid-off line — the fact has enormous weight; what Cassie withholds is the plea. "No handle left out" carries the whole image.
  - **Aggregate sentence: metaphor collision + understated finding fixed** — "the loans came down and the payrolls barely moved" had *down* meaning more money one clause after *up* did, and "barely moved" understated the scene's own verdict ("everybody cut anyway") and the real data (negative time-correlation; loan-heavy counties cut regardless). Now: "The money went up; the jobs went the other way. County after county, the loans landed and the payrolls fell anyway." Cassie's aphorism "It went up, it didn't go down" stands as the only vertical — money to the top, never down to workers.
  - **Fault-line beat restructured** — the old "Randi didn't answer it / Vee didn't answer it either / glad when it moved" presumed an argument before Randi had spoken. Now: Cassie's fact → Randi's counter and "We'll see" (verbatim, repositioned) → Vee's sensing paragraph, so the tension is reader-visible before Vee reacts to it. Vee's beat gains the seating geometry ("the laid-off father on her right, the loans on her left") and loses "glad when it moved" (no stall left to be relieved about).

## Left standing — do not re-litigate

- **"Randi had no idea she'd been looked at" stated flatly** (gpt-5.6-sol only: narration asserts what Vee can't know). **Author ruling 2026-07-29: kept as-is.** The guard-down state is canon and *the measure* of how real the wound is (`meta-note-outlier.md` § the gaze); the flat assertion is part of the tables-turned charge the other three readers loved. Acked in the linter (`look-at-her` — literal gaze mechanics, not the appreciation tic).
- **MIRH → Miranda Holdings "a little neat"** (gpt-5.5, lone, and they bought it). Working as designed: MIRH is Randi's own labeling convention — her name rendered as the villain-tag by her own visualization (`meta-note-outlier.md` § MIRH).
- **Closing image leans "a half-inch" toward telling the moral** (fable-5, lone, "but it earned it"). Working as designed: the closing outlier-image deliberately carries the reader-ahead instead of the narrator (`meta-note-outlier.md` § register).
- **"Worst point in the county" pushes slightly hard** (gpt-5.5, lone, self-dismissed). Taste; not actionable.
