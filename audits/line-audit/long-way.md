# Line audit — long-way (2026-07-31)

**Verdict:** Effectively clean — 3 minor issues found (0 fix, 1 clarification, 2 nitpick).

## Findings

1. **"He'd been gone twenty minutes … when the phone lit up face-down where she'd left it."** (opening sentence)
   Problem: A face-down phone's screen faces the table, so "lit up" is only visible as edge-glow; the next clause has her already reading the sender's number and message with no flip-over action shown.
   Severity: nitpick.
   Recommended fix: Optionally insert the implicit action of turning the phone over between the light and the reading, or leave as-is (readers infer it).

2. **"She bit her lower lip, knowing it would drip, and then found she didn't care."** (froyo-shop paragraph)
   Problem: The antecedent of "it" is the overbuilt froyo, but the nearest noun is "her lower lip" — a reader can momentarily parse "it" as the lip dripping.
   Severity: clarification.
   Recommended fix: Consider anchoring "it" explicitly to the cup/froyo if the momentary misparse bothers the author.

3. **Chronology metadata mismatch (not a prose issue): the scene includes Cassie speaking twice ("As long as he doesn't make you roll a healer again"), but the `meta-plan-chronology.md` entry lists `present: Vee, Pace, Randi` only.**
   Problem: The chronology's `present:` field omits Cassie, who is on the page in the opening table scene.
   Severity: nitpick (metadata, not the scene).
   Recommended fix: Add Cassie to the `present:` list for The Long Way in `meta/meta-plan-chronology.md` (and regenerate `chronology.html`).

## What was checked (basis for the near-clean bill)

- **Internal logic:** Text arrives 20 min after Pace leaves — consistent with Substitution's ending (she gave him her number, never got his; can't text first). Phone hand-offs (Vee → Randi → back) are clean. Cup/spoons/napkins/wallet/door choreography at the shop is coherent (he pays for both, hands full, holds door with his back).
- **In-scene continuity:** Time of day tracks morning-coffee table → "by evening" at the shop → "outside it had gone blue and cool" on the walk. The froyo survives the walk plausibly given the tart-on-the-bottom setup, and the closing "your tart's holding up" pays off that same cup ("cone" in "the cone of it leaning" reads as the heap's shape, not a literal cone — not flagged).
- **Cross-document continuity:** Chronology entry (Thu Sep 17, hours after Substitution) matches the scene's same-day compression; Tue Sep 8 (The Pointing Game) → Thu Sep 17 is weekday-consistent. "The same attention he'd given her calculus" matches Substitution (the tutoring was calculus; stats is only her class with Randi). The "wait a day / can't answer the first one" rule is consistent with Substitution's "she can't text first." Cassie's "roll a healer / business major" gibe matches the condensed brief's canonical gamer ex. Scene matches `meta-condensed-long-way.md` beat for beat.
- **Pronouns/dialogue:** All speaker attributions check out; every reply answers the prior line ("It's frozen yogurt" to "he wants to see you naked"; "That was one semester" to the healer gibe; the rule exchange). Only pronoun wobble is finding 2.
- **Tense/POV:** Past tense throughout, no slips; Vee POV holds (header matches).
