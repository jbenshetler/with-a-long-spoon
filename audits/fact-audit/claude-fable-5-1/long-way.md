# Fact audit — The Long Way

*model: claude-fable-5-1 · ch006 · 2026-09-20 · prose-sha ~1b9cac32f89b*

---

## Findings

**1. Froyo time of day — evening vs. daylight (cross-chapter; not in ledger, found on lookup)**

- **WHERE** (this chapter): "By evening she and Pace were standing under the neon in a too-bright shop" … "Outside it had gone blue and cool. They walked the long way, not toward anything."
- **AGAINST** (`scenes/may-i-choose.md:31`): "The froyo — that had been daylight, easy, the kind of thing that could turn out to be nothing. This was an evening, and he'd asked her for it like something he meant to do properly."
- **WHY** — The later chapter contrasts the froyo as *daylight* against the dinner as *an evening*, but this chapter places the froyo itself "by evening" with the sky "gone blue."
- **CONFIDENCE** — MEDIUM. Early-fall "evening" can still be light out, and "gone blue" is dusk, so a reading exists where Vee's later memory flattens it to "daylight"; but the contrast in the later passage depends on the froyo *not* being an evening.

Nothing else in the chapter contradicts the ledger or itself.

## NOTED (not errors)

- "She'd given him hers; it hadn't occurred to her to ask for his" — matches ledger "his number only after he texts [6]".
- Randi and Cassie present at the coffee table — both were present in the Wilson coffee shop in [5]; Randi "urges Vee to go out with him [5, 6]" matches "You should go."
- Randi's "He looked like a man who wants you… He wants to see you naked" — Randi knows Pace intimately, but the line reads as a stranger's plausible guess; no knowledge leak past the performed-stranger state of [5].
- "the same attention he'd given her calculus" — verified in `scenes/substitution.md:73,193` ("Did I just warn a math PhD that my calculus was hard?"); consistent.
- "keeping a business major alive in a video game" — refers to a past boy, not Pace (math PhD); no one in the ledger is identified as a business major; no conflict.
- "the way her grandfather used to ask things" — grandfather appears nowhere in the ledger; new detail, not a contradiction.
- Vee hearing her mother's "that's plenty, that's enough now" — consistent with the body-shame thread [24] and mother-as-nurse; no conflict.
- "Your tart's holding up" after "She built her cup without thinking" — she needn't have consciously followed his system to have put tart on the bottom; not a contradiction.
- Phone "facedown where she'd left it" then "Randi took the phone out of her hand" — Vee picked it up in between ("Her stomach went before she did"); consistent.
- Pace paying for both — Vee's debit/credit habits [17, 20, 23, 39] not contradicted.
- Cassie knowing of the froyo — ledger has "Pace's name, meeting, froyo [5, 6]"; she's at the table for the text.
- "By evening" / "twenty minutes" — same-day sequencing only; no date or interval arithmetic attempted per scope.
