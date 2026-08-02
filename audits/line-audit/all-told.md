# Line audit — all-told (2026-08-01)

**Verdict: 5 issues found — 1 fix, 1 clarification, 3 nitpicks.** No hard continuity breaks against the chronology (Fri Oct 16, morning after {{Peekaboo}}, stats MWF day — all consistent; Sorority follows Sat Oct 17, matching "You and me, Saturday"; Cassie as two-year roommate matches "two winters of Vee's life"; Randi's "four years" sorority habit matches her senior standing).

## Findings

1. **"Cassie had cracked it an hour ago off the made bed"** (¶ after "She left at eight," Randi told Cassie…). The scene establishes Cassie was *already gone* from the dorm when Vee blew through around 8:15, so Cassie saw the made bed before ~8 a.m. Stats is "the last class before lunch," after Vee's nine and ten — roughly 11 a.m. Cassie therefore cracked it **three-plus hours** ago, not one. Severity: **fix**. Recommend changing the elapsed-time phrase to match the morning's established clock (or removing the specific interval).

2. **"'Slut' landed lower than Randi meant it to. Her body had been keeping the night's account since eight…"** The nearest antecedent for "Her" is Randi (subject of the preceding sentence), but the body being described is Vee's; a reader parses it correctly only a beat later off "since eight." Severity: **clarification**. Recommend making the referent explicit at the sentence's head.

3. **"She had not looked at the professor once."** (Cassie-watching paragraph.) Vee's eyes were on the screen for the whole forty seconds ("Vee made herself pull her eyes to the front… followed the two columns up the screen"), yet the narration states as flat fact what Cassie did during exactly that interval. "As she had been since Vee sat down" partially covers it (posture inferred on surfacing), but "not once" is knowledge Vee couldn't have. Severity: **nitpick**. Recommend softening the claim to what Vee can infer on coming back up.

4. **"Vivienne Thorne. It is a Friday." … "On a school night."** The overnight was Thursday; "school night" is correct for Thursday-before-Friday-classes, and "It is a Friday" presumably means *today is a class day*. But on first read the two lines can register as contradictory (Friday night is famously *not* a school night), making Randi sound confused rather than scandalized. Severity: **nitpick** (likely intentional banter). Recommend author confirm the joke reads as intended; no change if so.

5. **Chronology metadata mismatch (not a prose issue).** `meta/meta-plan-chronology.md` line 120 lists `present: Vee, Randi` for {{All Told}}, but Cassie is a principal on-page participant throughout (and the scene brief centers her). Severity: **nitpick**. Recommend adding Cassie to the `present:` field and regenerating `chronology.html`.

## Checked and clean

- Timeline: left Pace's at 8, dorm stop, late nine, barely-made ten, stats before lunch, exit at "bright cold noon" — internally consistent.
- Date/weekday: Fri Oct 16 (internal 2026 calendar) is a real Friday; MWF stats lands correctly; Saturday shoe date = {{Sorority}}, Sat Oct 17.
- Seating/spatial: Cassie | Vee | Randi holds throughout (Cassie first speaker one side, Randi "on her other side," later "from the aisle," Cassie's eyebrow "on Vee's other side"); wrist-grab and descent down tiered steps consistent.
- Props: garment bag zipped in dorm closet at open and close ("three blocks back… still shown to not one living soul"); highlighter "back up" consistent with Cassie not taking notes while watching; book bag/both-shoulders carry fine.
- Dialogue logic: every reply tracks its prior line; attributions unambiguous except finding 2.
- "Two winters of Vee's life" (Cassie's fleece) vs. two-year roommate canon — consistent. "Had the dress for weeks" vs. Oct 3–4 fitting tellings (~13 days) — acceptable.
- Simpson's-paradox lecture: setup and reversal use the same two-players/two-seasons data; the '95/'96 historical example is fine in-world and names no story year.

## Author rulings (2026-08-01)

1. **Fixed** — ":29 hours ago" (was "an hour ago").
2. **Fixed** — ":53 Vee's body" (was "Her body").
3. **Left standing** — earned free-indirect inference; evidence one clause
   earlier ("as she had been since Vee sat down").
4. **Left standing** — intentional escalating charge sheet; calendar scans.
5. **Fixed (docs, expanded)** — Cassie added to `present:` for {{All Told}}
   and six other already-reviewed scenes where she's physically on-page
   (author is adding a Cassie pill to `chronology.html`); {{Dear}} left
   unchanged (walk-off in opening lines); unreviewed Cassie scenes to follow
   at their reviews.

See `meta/meta-triage-all-told.md`.
