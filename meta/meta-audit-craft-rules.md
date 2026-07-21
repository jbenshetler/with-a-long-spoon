# Craft-Rules Consistency Audit

**Purpose:** Review the canonical craft rules against the key meta docs (bible, per-character arch + craft docs, thesis, brief). Flag where a doc **contradicts**, **drifts from**, carries a **stale/retired** version of, or **plans a beat that would break** a craft rule. This is a *flag-only* audit — findings are for the author to decide; nothing is rewritten off a finding.

**Started:** 2026-07-20

## Yardstick (the canonical craft rules)

Two docs, authoritative together; where a rule appears in both they must agree:

- `meta/meta-rules.md` — the Character Rules verification checklist (Vee / Pace / Randi / cross-cutting / writing-style / scene-details).
- `meta/meta-arch-bible.md` §**GLOBAL CRAFT RULES** + §**Craft Rules** + §**Running threads to seed** (lines ~325–381).

## How to restart

The **task table** below is the source of truth. Re-spawn a subagent (see prompt template in the audit note) for any doc whose **Status ≠ `done`**. Each agent reads the yardstick, reads its one target doc, and returns findings; paste those under the doc's heading in **Findings**, then flip its Status to `done`. Order doesn't matter; docs are independent. Safe to run same-session or after a cold restart.

## Task table

| # | Target doc | Status | Findings (H/M/L) |
|---|------------|--------|------------------|
| 1 | meta-arch-bible.md | done | 1H / 1M |
| 2 | meta-arch-pace.md | done | 1H / 1M |
| 3 | meta-arch-randi.md | done | 2M |
| 4 | meta-arch-vivienne.md | done | clean |
| 5 | meta-craft-pace.md | done | 1M / 1L |
| 6 | meta-craft-randi.md | done | 2L |
| 7 | meta-craft-vivienne.md | done | clean |
| 8 | meta-thesis.md | done | clean |
| 9 | meta-brief.md | done | 2L |

**Severity key:** high = direct contradiction or retired/stale rule still live · med = drift (rule stated in weaker/diverging form) or planning that could break a rule · low = gap / minor divergence.

## Findings

### 1. meta-arch-bible.md
_Audited 2026-07-20 — 2 findings (1H / 1M). Note: this doc is the source of the ruleset; findings are internal self-contradiction + cross-doc drift vs `meta-rules.md`._

**[HIGH] "He doesn't push; files it." — the banned filing verb prescribed for Pace, in the doc that bans it (and likely an omniscient peek).**
- Rule: "No filing, no cataloging, for Pace… No *filed-it. registered-it. clocked-it.*" (`meta-arch-bible.md:361`, restated :176; `meta-rules.md:43`). Also no omniscient peeks in a Vee-POV scene (`:330`, `meta-rules.md:115`).
- Doc: "He doesn't push; **files it**." (line 315, in the {{First Taste}} best-phrasing note).
- Conflict: exact banned construction applied to Pace, inside the doc that bans it — a self-contradiction that would license a "files it" beat. Compounding: {{First Taste}} is Vee-POV, so "he files it" reaches into Pace's cognition Vee can't perceive.
- Suggest: embodied recast ("he lets it land" / "it reaches him"); if Vee-POV, render as something she *sees him do*.

**[MED] Cup "fires at every SATC lunch / in engineered scenes" (bible) vs. `meta-rules.md`'s binary "cup does NOT fire when Randi is operating/dominant."**
- Rule: "Cup does NOT fire when Randi is operating/dominant — the operation itself is the discharge" (`meta-rules.md:79`).
- Doc: cup "recurs at **every SATC lunch**… recurs in **engineered scenes she has architected**" (line 222).
- Conflict: at the lunches/engineered scenes Randi *is* operating — the condition the checklist says suppresses the cup. The bible reconciles it ("no operational lever to discharge the *Pace-jealousy* charge through") but `meta-rules.md`'s binary omits that carve-out, so a verifier applying the checklist would wrongly flag these appearances.
- Suggest: align the two — tighten `meta-rules.md:79` to "does not fire when the *running charge* has an operational lever (she is topping its source)," or add the no-lever-for-the-Pace-charge carve-out.

_Confirmed clean:_ "self-sadism" appears only as "Drop the label" instructions (77, 343); Pace explicitly "NOT neurodivergent… never labeled" (137); no retired filenames; reserved-vocabulary split, chiasmus-never-surfaces, porch three-source discomfort, honorable exits, prolepsis fact/pattern, Randi-POV containment all agree across the two docs. Other "files/clocks" hits belong to Vee/Brooke/reader (permitted — rule is Pace-specific).

### 2. meta-arch-pace.md
_Audited 2026-07-20 — 2 findings (1H / 1M)._

**[HIGH] Pace's reticence framed as "neurological comfort" — residual neurodivergence framing the canon retired.**
- Rule: Pace is neurotypical, temperament introvert-charismatic, *not* on the spectrum (`meta-arch-bible.md:137`). Currency audit flags this exact phrase as an unapplied neuro-swap (`meta-audit-currency.md:278`), and workstream N's ripple list never reached this file.
- Doc: "the reticence is **neurological comfort**, not hiding" (line 171); "the privacy stops being **neurological comfort** and becomes small ordinary fear of commitment" (line 173).
- Conflict: "neurological" attributes his privacy to innate wiring — the framing the neurotypical reconception retired. Canon grounds the trait in temperament + formation (mother's love-as-currency).
- Suggest: "neurological comfort" → "temperamental"/"constitutional comfort" (both lines); architecture intact, just de-neurologized.

**[MED] Pace's reception rendered in the retired filing/cataloging frame.**
- Rule: "No filing, no cataloging, for Pace… No *filed-it. registered-it. clocked-it.*" (`meta-arch-bible.md:361`; `meta-rules.md:43`).
- Doc: "an alteration his apparatus **registers as a good moment and files as consent honored**" (line 205).
- Conflict: uses the forbidden verbs (registers/files) to model his attention — imports the analyst-reviewing-data coolness the rule guards against.
- Suggest: embodied/consent-logic reframe without cataloging verbs — e.g. "receives as a good moment, consent honored."

_Confirmed clean:_ vow as habit not decision (155–163); honorable exits real & unprotected (19, 187–195); no verbal declaration (141); no softening / coercion / interim-cruelty; no "self-sadism" label; "hyperfocus" (231) and choice-become-habit blindness (97, 105–117) are current neurotypical-consistent canon, not drift.

### 3. meta-arch-randi.md
_Audited 2026-07-20 — 2 findings (2M), both cross-doc reconciliation tensions. No "self-sadism"; never a warm-shell-over-cold-core (love insisted real throughout); all filenames resolve._

**[MED] {{Fairytale}} prescribed in Randi's POV — collides with the flat "never inside Randi's POV" rule.**
- Rule: "We are never inside Randi's POV — assembled from behavior and tells" (`meta-rules.md:112`, :95). The bible POV block (`:330`) names only strict-Vee / strict-Pace — no Randi-POV carve-out.
- Doc: "POV (containers rule): Rendered in Randi's POV — the second opening of the mirror aperture… Full rule in the Bible; chronology flag 15." (228–229), with direct interiority: "there is no one behind it. *She has known that for a while.*" (219).
- Conflict: `meta-rules.md` states outside-Randi as absolute; the doc prescribes a full Randi-POV scene opening her interiority. Either the beat breaks the rule, or `meta-rules.md` (and the bible POV block) are stale for not carrying the two-mirror-aperture exception the doc says lives "in the Bible."
- Suggest: reconcile — if the mirror-aperture Randi-POV is sanctioned, add the exception to `meta-rules.md` + confirm in the bible POV block; else revisit the Fairytale POV note. **(Verify whether the Bible actually contains this exception — the doc asserts it does; the bible audit did not surface it.)**

**[MED] Appetite-(b) ignition schedule frames the sadism as learned/growing — drifts toward the forbidden "discovered" reading.**
- Rule: "Sadism is present from the start, not discovered — already operating at adult resolution" (`meta-rules.md:87`).
- Doc: "(b)… Ignites through being experienced, not anticipated. Not fully present at the first lunch; the first extraction *teaches Randi's body what this gives her.* Across the early lunches (b) catches and grows." (136).
- Conflict: "not fully present at the first lunch / teaches… / catches and grows" reads as sadism discovered across early scenes. The doc self-guards on *competence* (140) but the appetite-growth wording still supplies a discovery framing a scene-prep could act on.
- Suggest: separate *appetite/reward* (may ignite experientially) from *capacity* (adult resolution from lunch one) — first extraction *confirms/feeds* a sadism already operating, not teaches one into being.

### 8. meta-thesis.md
_Audited 2026-07-20 — **clean, no drift.** (Master doc much of the ruleset was derived from.)_

Holds every watch item: "sadism" only ever applied to Randi, never Vee (no self-sadism); Pace's non-reading framed as choice-hardened habituated refusal, not diagnosis (105); harm fast-installed (83); goods real-in-real-time, contamination retrospective (83, 202–203); configuration as agent, no single villain (23, working rules 21–22); each carrier half-sees (113–125); Vee keeps shame — explicit "do not render as liberation-from-shame" (188); chiasmus never surfaces (75). Cross-refs resolve; lint passes. _(Out-of-scope hygiene note: "Secret Plans" bare at line 123 amid braced titles — title-brace convention, author's call, not a drift violation.)_

### 4. meta-arch-vivienne.md
_Audited 2026-07-20 — **clean, no drift.** (This doc is itself one of the sources the ruleset was distilled from.)_

Verified compliant on every watch item: no "self-sadism" label (cutting voice at experience level, 92–95); shame constitutional & kept, never liberation-from (15, 95, 211); body-before-mind scoped to involuntary tells only, not romantic agency (85, 157); no surpassing relationship / no free lunch (107, 213, 215); the "no" as equipment working (15–17, 137, 185); goods contamination retrospective only (109, 155, 177); reserved seeing-vocabulary not misapplied; filenames/titles current (linter: 101 refs resolve).

### 5. meta-craft-pace.md
_Audited 2026-07-20 — 2 findings (1M / 1L). Filing-ban, vow-as-habit, three-phrase guard, no-interim-cruelty, 95% rule, present/after asymmetry all carried correctly._

**[MED] Selective-inattention framed as "a particular kind of mind" — residual mind-type framing.**
- Rule: never label Pace's temperament — behavior only, never a diagnosis (`meta-arch-bible.md:327`); recent pass made him neurotypical. "Selective inattention" is endorsed as a 95% *behavioral* lapse (`:363`), not a category of mind.
- Doc: "Render it as *a particular kind of mind*, not a flaw." (line 147).
- Conflict: "a particular kind of mind" reifies the attention-profile into a trait-of-mind — closest kin to the retired "wired differently" frame. Guidance, not prose, but it steers toward mind-typing.
- Suggest: drop "a particular kind of mind"; keep behavior only — e.g. "texture Vee adjusts to, not a flaw."

**[LOW] Chapter-title "Pool" bare in a braced list** (line 44) — mechanical title-mark hygiene, not a craft rule. _Correction on review: `lint_titles.py` reports no chapter titled "Pool" (101 known titles), so the agent's premise that "Pool" is a bracable chapter is likely wrong — it may be an informal cluster name or part of a longer title. Leave bare; do not brace. Worth an author glance at `meta-craft-pace.md:44` to confirm what "Pool" refers to._

### 6. meta-craft-randi.md
_Audited 2026-07-20 — 2 findings (2L). Strikingly current: no "self-sadism"/"warm shell"/"cold core" anywhere; `sweet-dress-barb.md` present only as a labeled retired pointer._

**[LOW] Mechanism note uses the reserved *seeing* word for what Randi's warmth produces.**
- Rule: seeing-register (*seen/known/perceived/met/beheld*) belongs to Pace, never for what Randi produces in Vee (`meta-rules.md:74`; this doc's own line 75).
- Doc: "the affirmation feels specific and **seeing**, when it is in fact her standard move…" (line 34).
- Conflict: uses the reserved word to describe Randi's effect — the exact conflation this doc's own line 75 forbids. Framed as the counterfeit, so intent is right, but the wording models the slip a drafter is told to catch.
- Suggest: "feels specific and *perceptive*/*attentive*" (or "feels like being *noticed*").

**[LOW] Doc carries only the seeing-register half of the paired "distinct rendering vocabularies" rule; the analytic/math half is unstated.**
- Rule: Pace owns the math register; Randi's grammar is room-reading/status, *never Pace's math* — a paired rule that cross-refs this doc (`meta-arch-bible.md:335`).
- Doc: Reserved Vocabulary (68–85) carries the *seen*/signature-phrase split but is silent on the "not Pace's math" guard.
- Conflict: not a contradiction (doc never gives Randi math), but a Randi-drafter reading only this file won't see the math-half guard.
- Suggest: add one line ("Randi's grammar… never Pace's analytic/mathematical register") or defer explicitly to bible :335. Marginal.

### 6. meta-craft-randi.md
_pending_

### 7. meta-craft-vivienne.md
_Audited 2026-07-20 — **clean, no drift.**_

Faithful, current rendering companion. No "self-sadism" (cutting voice at experience level, 79–81, with architectural truth parked below); shame as permanent engine, never liberated-from (14, 138–140); voice regresses DOWN (15, 32), academic baseline cordoned from under-pressure defense (30); body-before-mind scoped to involuntary tells, romantic agency explicitly conscious (13, 47, 58–69, 92–93); no free lunch (140); mother's voice displaced not self-directed (41); "no" = equipment working (138); goods not pre-contaminated (136); chiasmus invisible (144–146); cracker-and-meal single porch exception (152); all cited filenames/scene paths current.

### 8. meta-thesis.md
_pending_

### 9. meta-brief.md
_Audited 2026-07-20 — 2 findings (2L). Notably current: carries the up-to-date "not neurodivergent" tag; affirms anti-villain, goods-real, seen/chosen, cup, voice-regression._

**[LOW] "the rules were perfectly executed" brushes the 95%-not-perfect rule and mislocates the reckoning's engine.**
- Rule: Pace excellent at 95%, not perfect (`meta-arch-bible.md:363`); the engine is the consent architecture's *hole* (guards force, not deception-into-consent — CLAUDE.md).
- Doc: "the destruction proceeds *because* the rules were perfectly executed." (line 22).
- Conflict: canonical cause is a structural hole in the rules, not flawless execution of the man; "perfectly executed" reads as endorsing perfect-Pace.
- Suggest: e.g. "because his rules had no term for deceiving someone into consent — the consent architecture was followed, and guarded nothing here."

**[LOW] "Five Craft Rules That Cannot Be Violated" omits the shame rule — the bible's most-repeated load-bearing constraint.**
- Rule: shame load-bearing throughout, new indignity each scene, chosen/kept not liberated-from (`meta-arch-bible.md:336–337`; `meta-rules.md:21`).
- Doc: the "Five" (42–52) cover goods-real, power-wears-warmth, chiasmus, cup, voice-regression — no shame rule.
- Conflict: a top-level "cannot be violated" five without the single most load-bearing Vee-scene constraint under-weights it. Mitigated: shame surfaces in Vee's paragraph (20) and the map points to `meta-rules.md`; the five may be a deliberate curated subset.
- Suggest: add a shame rule to the five, or leave as-is if deliberately the most-often-violated set. Author decides.

---

## Resolutions applied (2026-07-20)

Author-ruled and written into canon this pass:

- **HIGH `meta-arch-pace.md:171,173`** — "neurological comfort" → "constitutional comfort" (both). ✅ fixed.
- **HIGH `meta-arch-bible.md:315`** — "He doesn't push; files it." → "…lets it land." ✅ fixed.
- **Cup rule** (was the bible-vs-checklist tension) — RULING (refined): the cup stays the **bottom's gesture** (being-done-to, no lever to discharge); the charge is the **envy-charge** — Randi near Vee's real intimacy with Pace, Vee *seen* and thriving on what Randi can't have in channel. "Fires when bottoming" is **correct** — bottoming to the *charge/content*: in the SATC extraction she tops Vee (steers the retelling) yet bottoms to what she hears, and the extraction is the primary delivery mechanism for the envy-material, so the cup fires mid-operation. The **only** wrong half of the old binary was "the operation itself is the discharge" (operating never discharges the envy). Fires often at SATC but not only; can fire outside it. Bench debut (Vee absent) fires on her *own* need, not envy — same gesture, evolving charge. `meta-rules.md` cup section rewritten to match. ✅ reconciled. (bible :222 already consistent via venues + "no operational lever to discharge" — left as-is.)
- **Randi-POV** (was the {{Fairytale}} tension) — RULING: Randi-POV is permitted **only when neither Pace nor Vee is present**; {{Fairytale}} qualifies (a brief Vee text exchange ≠ Vee present), plus a small aperture at the end of {{The Bench}}. Added the "containers rule" to `meta-arch-bible.md:330` (the "full rule in the Bible" that `meta-arch-randi.md:228` points to) and to `meta-rules.md` (POV items). ✅ reconciled — {{Fairytale}} note is correct.
- **LOW craft-pace "Pool"** — the "brace it" premise was wrong (no chapter titled "Pool"); resolved by author to `{{We Find Out}}, {{Jitterbug}}, {{The Deep End}}` (`meta-craft-pace.md:44`). ✅
- **MED `meta-arch-randi.md:136` (appetite-b "discovered" drift)** — RULING: not real architectural drift — a legibility gap between two senses of "sadism." Her *competence/resolution* is present from the first lunch (no on-page discovery); what deepens experientially is the *reward* (appetite (b) catches and grows), an already-operating hunger intensifying. Fixed both: `:136` "teaches Randi's body what this gives her" → "**feeds a hunger already operating**"; `meta-rules.md:87` rewritten to split competence (present from start) from reward (deepens). ✅

- **MED `meta-craft-pace.md:147`** — "a particular kind of mind" (residual mind-typing) → "**how his attention works**" — behavior-level, no mind-category, intent (not-a-flaw) preserved. ✅

- **LOW `meta-craft-randi.md:34`, `:68–85`** — "seeing" → "attentive"; analytic-register companion guard added to Reserved Vocabulary. ✅
- **Shame taxonomy (new canon, from discussion)** — three *distinct, co-equal* charge-sources ((1) involuntary display / (2) premeditation / (3) transgressive content), the *fuels-not-fights* guard over all three, and the anti-prude / healthy-baseline note scoped to (3). Written full to `meta-craft-vivienne.md` §The Three Charge-Sources; compressed into `meta-rules.md` (VEE / Interior-and-shame, replacing the old "not chosen acts" line); added as brief rule #6. ✅
- **Consent-by-reading (new canon, from discussion)** — Pace asks-without-asking (question in the act, answer in her body); the four-part white/black test; act-level scrupulous, harm is *frame-level* not act-level. Written to `meta-craft-pace.md` §Consent by Reading, Not by Clearance; reinforces brief:22. ✅
- **`meta-brief.md`** — line 22 "perfectly executed" + deception-hole tail; cup rule #4 reconciled to the envy-charge ruling; line 24 cup mention softened; "Five"→"Six" Craft Rules with the shame rule (#6) added. ✅

Remaining open (author decision, not applied): `meta-arch-pace.md:205` (registers/files — MED, *intentionally left* per author — the filing-verb guard belongs at the prose layer, not planning). All other findings resolved.

## Executive summary (all 9 done · 2026-07-20)

**13 findings total: 2 high · 5 med · 6 low.** Four docs clean.

**Highest priority — act first:**
1. **`meta-arch-pace.md:171,173` — two live "neurological comfort" phrases** (HIGH). Residual neurodivergence framing the neurotypical sweep missed; the currency audit even flagged `:141` but the fix never reached this file. → "temperamental/constitutional comfort."
2. **`meta-arch-bible.md:315` — "He doesn't push; files it."** (HIGH). The banned filing-verb prescribed for Pace *inside the doc that bans it*; also an omniscient peek in a Vee-POV scene ({{First Taste}}). → embodied recast.

**Two genuine cross-doc reconciliation calls (author decisions, not just fixes):**
- **Cup rule** — bible ("fires at every SATC lunch / engineered scenes") vs. `meta-rules.md:79` binary ("does NOT fire when Randi is operating"). The bible's no-lever nuance is missing from the checklist; a verifier would mis-flag. → align the two forms.
- **{{Fairytale}} Randi-POV** — `meta-arch-randi.md:228` prescribes a full Randi-POV scene citing a "mirror-aperture exception… in the Bible," but `meta-rules.md:112/95` and the bible POV block state outside-Randi as absolute with no such carve-out. **The bible audit did not find that exception** — so either it needs adding, or the Fairytale POV note is wrong. Needs an author ruling + a bible check.

**Softer drift / gaps (med/low):**
- `meta-arch-pace.md:205` "registers/files as consent honored" — cataloging register (MED).
- `meta-arch-randi.md:136` appetite-(b) "teaches… catches and grows" — drifts toward sadism-discovered (MED); separate appetite from capacity.
- `meta-craft-pace.md:147` "a particular kind of mind" — residual mind-typing (MED).
- `meta-craft-randi.md:34` "feels… seeing" — reserved word for Randi's effect (LOW); `:68–85` missing the math-half guard (LOW).
- `meta-brief.md:22` "perfectly executed" (LOW); the "Five" omit shame (LOW).

**Clean, no drift:** `meta-arch-vivienne.md`, `meta-craft-vivienne.md`, `meta-thesis.md` (each a source the ruleset was distilled from); `meta-brief` clean on all majors.

**Cross-cutting pattern:** the only HIGH/MED *content* drift clusters on **Pace** — every instance is a residue of the neurotypical conversion (neuro-labeling) or the filing/cataloging ban not fully swept. The Vee and thesis material, and Randi's core rendering, are current. The two reconciliation items are checklist-vs-bible *form* mismatches, not prose risks.

_Flag-only audit: nothing above has been changed. Author decides which to apply._
