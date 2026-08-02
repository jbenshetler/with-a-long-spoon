# Line audit — practice-room (2026-08-01)

**Verdict:** 4 issues found — 0 fix, 1 clarification, 3 nitpick. No hard continuity or logic breaks.

## Findings

1. **"and the thing her body had been building toward all afternoon arrived"** (line 115) — Time-of-day slip. The stats lecture "met at eleven" (line 3), the hour "came apart" (~11:50), Randi has 45 minutes (line 27), so the practice-room conversation runs roughly noon–12:45; "all afternoon" implies a duration the clock doesn't support (the arousal has been building since a late-morning class, over well under an hour of "afternoon"). Severity: **nitpick**. Recommended fix: replace the time-span phrase with one matching the elapsed hour (or since the lecture).

2. **"Mine," she said.** (line 99, opening a new paragraph after Randi's closed quote at line 97) — Pronoun/attribution ambiguity at a paragraph break. The prior paragraph closes Randi's quotation; a new paragraph opening with a quote conventionally signals a speaker change, and with two women in the room "she" has two available antecedents — a first-pass reader can momentarily hand "Mine" to Vee before the ex-husband content corrects them. Severity: **clarification**. Recommended fix: attribute the line to Randi by name (or merge into the preceding paragraph).

3. **"And always, toward the end, his hand would slip." Randi's mouth curved.** (line 113, after the closed quote at line 111) — Same closed-quote-then-new-paragraph continuation pattern as finding 2, but the "Randi's mouth curved" beat lands one sentence in, so the stumble is briefer. Severity: **nitpick**. Recommended fix: none strictly needed; if finding 2 is addressed, consider whether this paragraph break should match the chosen convention.

4. **Meta-doc date mismatch (not a prose issue).** `meta/meta-plan-chronology.md` line 530 calls this scene's bathroom beat "The November bathroom suppression ({{The Practice Room}})," but the scene's own chronology entry (line 152) dates it **Mon Oct 26**. Severity: **nitpick** (fix belongs in the chronology doc, not the scene). Recommended fix: change "November" to "late-October" (or equivalent) at chronology line 530.

## Cross-checked against triage (`meta/meta-triage-practice-room.md`)

No finding above restates a "left standing" verdict. I did **not** flag: the thesis-loud stats lecture, Cassie's displacement, or the mouse-story ambiguity — all settled authorial decisions. The rewritten realization beat (line 67) and the flat "I do know" (line 35) match the triage's "fixed this pass" text exactly.

## Checked and clean

- **Date/weekday:** Mon Oct 26 (chronology line 152) is a real Monday in the pinned 2026 calendar; stats is a MWF class ("stats class day" pattern at {{Dear}}, {{All Told}}) — an 11 a.m. Monday lecture fits.
- **Sunday-night sleeplessness (line 3):** consistent with {{A Recognized Method}} — she stayed a second unplanned night at Pace's Sun→Mon and left Monday morning; the scene never claims she was in her dorm.
- **The retelling vs. {{A Recognized Method}} prose:** cognac heels ✓ (loaned in `broken-in.md` line 173, worn in `recognized-method.md` line 9); heels put on in the car ✓; taller by an inch or two on the porch, first time ✓; reaching to unbuckle on the porch, mortified ✓; "Leave them on" / gods-and-loan line ✓ (faithful paraphrase of `recognized-method.md` line 33); slept in "forever" the next day ✓ (she wakes past noon Sunday); dishes → tickle → swat → sex sequence ✓; "his hand was wet" is a legitimate inference Randi draws from Vee's own "he was up doing the dishes" (line 51 → 73).
- **Seating/spatial:** Cassie left, Randi aisle-right, Vee between (line 5) — the knee contact (line 19) and the two-fingers-on-wrist turn away from Cassie (lines 21–25) are geometrically consistent; practice-room blocking (two chairs turned to face, Vee standing up at line 115, Randi bagged and phone-out on return) has no contradictions.
- **Props:** shoes stay in Vee's bag → hands → set down → never contradicted; Randi's 45-minute budget (line 27) is honored by her leaving on return (lines 127–139) with matching "people across campus" phrasing (27 → 133).
- **"Empty at this hour" (line 27) vs. scales two doors down (line 135):** ~45 minutes elapse; not a contradiction.
- **Dialogue logic:** every exchange responds to its prior line, including the delayed trap (63 → 65 → 67) and the interrupted "Have you ever—" answered obliquely at 95–97.
- **Tense:** consistent past throughout; the kitchen flashback (line 75) is clearly framed as memory.
- **No calendar dates or weekdays in the scene header or prose** (per the no-header-dates convention).
- **`never-name`:** Pace's temperament is nowhere labeled in the scene.
