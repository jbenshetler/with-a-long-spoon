# Line audit — gone (2026-08-01)

**Verdict:** 1 issue found (1 clarification; 0 fix, 0 nitpick).

## Findings

1. **Line 47** — "Then the tell of it dropped, half a register, went somewhere low and hoarse."
   - Problem: referent clarity. "It" has no antecedent in the sentence or the paragraph before it — the reader must infer mid-sentence that "it" is her *voice* (only "hoarse," four clauses in, confirms this), and "the tell of it" stacks a second unanchored "it" (the tell of *what* — the desire? the voice?). A first-pass reader is likely to stumble and re-read.
   - Severity: **clarification** (not a fix — the leak-as-tell is intentional per `meta-note-gone.md` beat 4; only the pronoun anchoring is at issue).
   - Recommended fix: anchor the sentence so "voice" (or an equivalent concrete referent) is present before or at the drop, without spelling out what the tell reveals.

## Verified clean

- **Date/weekday:** Chronology (`meta-plan-chronology.md:128`) places the scene Mon Oct 19; Oct 19, 2026 is a Monday. Randi's "God, Saturday" for the shoe trip matches {{Sorority}} at Sat Oct 17 (chronology line 124), two days prior — "Best time I've had in a store in years" is a natural two-day-old reference. Scene sits before {{Rock}} (Tue Oct 20) per header and chronology; no calendar date appears in the scene header (convention held).
- **Shoe-store retelling vs. `scenes/sorority.md` (lines 37–61):** the divergences are real — in canon *Vee* set the canoe shoe in front of Randi as a taunt, *Randi* did the platform walk, and the older-couple flush was Vee's, minor and let go; in Randi's telling Vee wears the shoe, does the bigfoot walk, and is mortified. This is the **designed embellishment** (scene header; `meta-note-gone.md`: dual-account unreliability, soft-register divergence, never adjudicated) — not flagged. The retained kernels (yeti ragging, canoe/snow-tire shoe found by Vee, older couple watching) all match the canon scene.
- **Randi's physical canon:** black fine hair (matches `the-pointing-game.md:65`, `ignition-scalding.md:15`), blue eyes (`meta-arch-randi.md:287`, `in-her-place.md:17`), small and pale, blue toenail polish "still perfect" (established at `the-bench.md:177,271`; recurs `in-her-place.md:17,97`). All consistent.
- **Cross-scene facts:** Pace knowing Randi wants Vee openly since {{The Pointing Game}} (Tue Sep 8, well before this scene) — the frank "curves under that cardigan / you already know" talk is licensed by that canon (`meta-note-gone.md`). "The whole hour" matches the canonical weekly Randi/Vee hour ("the one warm hour of her week," `meta-arch-randi.md:251`). Vee's cardigan-hiding and body-shame match her arch and the {{Cropped}} mother material. "You already know" is clean — Pace and Vee are lovers by this slot.
- **Within-scene body/spatial continuity:** Randi astride/folded on his chest (l.7) → lifts head (l.27) → comes up to kiss, draws back (l.29) → cheek back on chest (l.39) → leans up for the lower-lip kiss, settles back (l.45) → presses up on hands for the breast-drag (l.47) → his hands to her thighs (l.49) → thighs to hips/seat (l.63–67) → riding (l.69). No position teleports; the two kisses (lingering, then brief) match the planned beat order.
- **Props/setting continuity:** lamp low at l.7 and "low lamplight" at l.69; playlist established "down in the front rooms" (l.7) and closing "down the hall … under the door" (l.69) — consistent geometry; Sade is *her* playlist, no conflict with Pace's own playlists (`all-the-time.md:83`). Warm house is Pace's established habit.
- **Dialogue logic:** every reply tracks its prompt ("You went shopping" → the Saturday story; "And she talks about you" → "The whole hour"; "Tell me" → the room speech; "Yeah … She is" answers "the most alive person standing there"; "So soon?" answers finding him hard). Attributions unambiguous throughout; consecutive Randi paragraphs (l.39/41) both tagged.
- **Author-approved exception honored:** the interior brush at l.45 ("Something in Randi went quiet at that, and softened past it") is signed off in `meta-note-gone.md` (observation-only exception) — not flagged.
- **Triage:** no `meta/meta-triage-gone.md` exists; nothing pre-settled to avoid beyond the meta-note exception above.
- **Tense/timeline:** continuous single evening, past tense throughout; no elapsed-time contradictions.

## Author rulings (2026-08-01)

1. **Fixed** — ":47 Then her voice dropped half a register" (was "the tell of
   it dropped, half a register"); :49 already does the tell-registering
   explicitly.

See `meta/meta-triage-gone.md`.
