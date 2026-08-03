# Triage — One Bite (line audit, 2026-08-02)

Sentence-by-sentence consistency/logic audit (`audits/line-audit/one-bite.md`).
4 findings: 1 fixed (plus a companion disambiguation), 3 left standing.

## Fixed

- **Phantom straw** (:109) — "The straw had gone useless in Vee's dry mouth"
  with no straw in the scene (mimosas in flutes; no water glass established).
  Recast to the payload: "Vee's mouth had gone dry."
- **"the card" briefly parseable as credit card** (companion fix to the
  cheapest-yes finding) — first mention had no antecedent (the hostess carries
  "menus") and "reach for the card" beside "her budget" invited the misread
  for half a sentence. Now "did not reach for the drinks card"; the later bare
  "the card" inherits the antecedent.

## Left standing — do not re-litigate

- **Vee knows the cheapest item without opening the card** (:9) — she's priced
  the genre, not this specific card: "the cheapest yes on the card" is her
  shorthand for *a mimosa is always the cheapest yes at a place like this*,
  and the not-reaching is the characterization (performing ease while
  budgeting). A rendered menu-scan would dilute exactly that.
- **"Forty minutes from home"** (:103) — Radford is ~20–25 minutes from
  Blacksburg; the inflation stays as fabrication texture. The whole story is
  engineered (see cold-read triage below); Randi stretching her stranding for
  effect is in character, and a local reader clocking it gets the designed
  flicker of suspicion.
- **"Randi's bare honest skin"** (:41) vs. the makeup "so finely done it
  passed for skin" (:11) — deliberate close-POV payoff, not narrator error: by
  :41 Vee is experiencing the illusion as fact, the makeup succeeding in real
  time on the very witness who clocked it. "Honest" is the reread charge.

Also: Cassie not present (Vee/Randi only) — `present:` field unchanged. No new
style hits on the edited lines.

---

# Triage — One Bite (cold-read panel, 2026-07-28)

Panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol · `reviews/cold-read/*/one-bite.md`

Note: all four reviews predate the rename — they review the scene under its old
title *"Vee Tells Randi About We Find Out"* (old slug `vee-tells-randi-we-find-out`).

Verdicts on the friction items derived from the panel. **The "Left standing" section
records authorial decisions — do not re-flag these without new evidence** (a new
reader cohort snagging on the same spot, or an edit that re-opens the passage).

## Fixed

- **Old title flat / a log line** (all four; fable-5 hardest: "a log line, not a
  title… gave the game away and gave nothing back") — resolved by the rename to
  **One Bite** before this triage pass; no prose change needed.
- **"me singing the whole song of self-pleasure"** (Opus: "a slightly writerly
  phrase in Randi's mouth") — recast to **"doing a private dance."** Author's
  direction 2026-07-28: Randi is a trained dancer, so the dance idiom is natively
  hers; "private dance" carries the lap-dance connotation that matches the
  porn-generic register the SATC track prescribes for her stories, riding on the
  true (trained-dancer) sense. Linter rerun clean of new hits.
- **Three `unhurried` hits cut** (linter, not reader-flagged) — author ruling
  2026-07-28: *unhurried is Pace's word in this novel*; two of the three hits had
  put it on Randi. All three cut rather than swapped (a neighboring clause
  already carried the calm in each): "warm and sure" (arrival), "going through
  her, the ease of it" (the third wave), "lifting her glass, easy, no curiosity
  anywhere in it" (the protected no-curiosity beat, now more exposed).

## Scene-review pass (2026-07-28, same day)

- **Re-dated Sun Nov 1** (was Mon Nov 2) — author ruling: Monday brunch at 11am
  collides with stats (MWF, lets out 11:50) plus parking/travel logistics, and
  the two women arriving together would kill the arrival beat. Sunday preserves
  it cleanly. {{We Find Out}} litany updated to match ("no Sunday, no Randi to
  be told" — see meta-triage-we-find-out.md). Chronology + HTML regenerated.
- **"without asking her first" cut** (telegraphed the consent theme; the body
  answering was already rendered).
- **"some weather happening near her" cut** (figurative weather tic; "The heat
  was no longer happening near her" stands).
- **Acked as sanctioned:** "so far out ahead of her permission" (two cold
  readers quoted it as a peak) and the goodbye-kiss frame "the way she always
  was" — recorded in style-allow.toml.
- **`the way` cluster resolved (9 hits):** one recast ("as you do for a faint");
  the rest acked — two kept-current on author review (the light on both faces;
  the glass-turn mimicry seed), one kept in the descent line, three adverbial
  "all the way" (degree, not the tic), one inside the protected stall passage.

## Left standing — do not re-litigate

- **Radford story "engineered to the millimeter" / author's hand visible**
  (fable-5: "a planted munition"; Opus: "I could see the mechanism") — working as
  designed. `meta-plan-satc-tracks.md` rules every man-story fabricated and the
  porn-generic register deliberate ("the mismatch is the CONTENT of the
  deception"); both flagging reviewers explicitly read the aim as *Randi's* craft
  and forgave it in the same breath. The suspicion is the designed response.
- **"Sticky fingers?" unresolvable / "no curiosity" too perfect** (all four,
  as praise-shaped unease) — working as designed and protected: the track doc's
  "deniable double-bind" spec requires the innocent reading load-bearing, and the
  unresolved "did she see" is a collectible plant. **Never resolve it.**
- **"Best friend in the whole world" lands with "a tiny clang" / too perfectly
  timed** (gpt-5.5, lone) — working as designed: the counterfeit reward closing
  the extraction cycle (`meta-plan-satc-tracks.md`). A cold reader half-hearing
  the clasp close is the mechanism at spec.

## Protected positives (a fix must not damage)

- The stall stop and its key sentence ("She could not be looked at like that and
  keep her hand where it was, and the two would not hold in one body") — fable-5:
  "the most psychologically precise sentence in the book so far."
- The door/no-door line ("…handed her a door or shown her there had never been
  one. She sat down. She did not find out.") — called "the whole book in a
  sentence" (fable-5).
- The glaze ending — taste-thread **debut** (reveal-weapon training,
  `meta-plan-satc-tracks.md`): the glaze-on-the-kiss, the pastry Vee never
  touched, and the kiss held at its current rung must all survive any edit.
- The "He checked" confession ladder and Randi's "no curiosity" beat.
