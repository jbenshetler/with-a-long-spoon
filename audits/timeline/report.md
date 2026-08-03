# Whole-book timeline sweep — consolidated report (2026-08-03)

Stage 1: 49 parallel per-chapter extraction agents (`audits/timeline/ledgers/<slug>.md`),
734 temporal claims verified against `meta/meta-plan-chronology.md`; triage rulings
honored (felt-time and retelling-drift verdicts returned as "settled", not re-flagged).
Stage 2: sequential front-to-back synthesis of the 49 ledgers for cross-chapter
contradictions and cumulative drift.

**Verdict: 9 findings — 4 fix, 3 clarification, 2 note-only.** No cumulative drift:
the dated spine (Sep 4 → Jan 24) closes; every arithmetic claim that both ends of an
interval date ("Twelve days," "seventeen days," "Two days I'd known him," the
Gstaad/Ohio NYE diptych) verifies exactly.

## Fix

1. **Vee in two places on Tue Oct 20.** `scenes/lesson.md:7` "Tuesday night Meg's
   door was open, two down" (two nights before the Thursday dance) — but the
   chronology has {{Rock}} that same Tue Oct 20: a weeknight stay at Pace's,
   overnight. The Meg retelling and the Pace overnight cannot share the night as
   written.
2. **"She had only had him the once."** `scenes/recognized-method.md:65` — by Sat
   Oct 24 the chronology has First Night ({{Famished}} Oct 9), {{Peekaboo}} (Oct 15,
   sex + overnight), and {{Rock}} (Oct 20, post-sex stay). The line predates the
   [NEW] Rock/Gone insertions and now undercounts by at least two.
3. **"Had had it ready for days."** `scenes/all-the-time.md:103` — the cropped nude
   is taken Thu Nov 12 evening ({{In His Hands}}); the brunch is Sat Nov 14 morning,
   ~1.5 days later. "For days" implies several.
4. **Meta-doc date contradiction, Hills and Valleys.** `meta-triage-hills-and-valleys.md:52`
   records a condensed-doc correction to "~Sat Oct 31 (Oct 31 is the Saturday
   matching the chronology entry)" — but the chronology entry reads Sat Oct 24
   (both are Saturdays in-world; the triage note picked the wrong one). The prose
   checks clean against Oct 24; the meta docs disagree with each other.

## Clarification

5. **"A longer parting than a Monday."** `scenes/see-you-later.md:83` — read
   literally it names the wrong day: the scene is Wed Sep 9 and the prose itself
   says "a Wednesday-morning stats lecture" (`:33`). Defensible as idiom for "an
   ordinary weekday"; as written it can snag.
6. **"A nothing Tuesday."** `scenes/fairytale.md:135` — no dated Randi/Vee weekday
   table exists; the dated tables are weekend brunches. Fine if idiom for "an
   ordinary day" or if the brunch spine is non-exhaustive; literal reading has no
   anchor.
7. **Header convention breach.** `scenes/we-find-out.md:3` "A Friday afternoon into
   evening" — a weekday in a scene header, which the 2026-08-01 header sweep
   reserves to the chronology. (Matches the chronology's Fri Oct 30; convention
   issue, not a date error. Also `scenes/recognized-method.md:3`'s header span
   "Saturday evening into Sunday morning" understates the scene, which runs to
   Monday morning per the chronology.)

## Note-only (no action recommended)

8. **The Bench "three weeks ago"** vs. chronology's ~Sat Aug 8 Pace-meets-Randi
   (~3wk6d): a ~6-day drift inside a "~" anchor, inside a line already ruled KEEP
   (`meta-triage-the-bench.md`). Becomes actionable only if the meet is ever hard-dated.
9. **The unanchored backstory cluster (84 claims).** Nearly all pre-book durations
   the chronology deliberately doesn't date: Pace's Blacksburg arrival/furniture
   years, Randi's residence/age, Vee's class year (verified consistent with
   `meta-arch-vivienne.md` where it surfaces), synchro/rec-season/childhood
   references, the magazine-dress first sighting, the induction letter's arrival
   day, Sheri's Thanksgiving cooking, Randi's Gstaad return date, and the
   last-cooked-meal referent behind `nothing-underneath.md:125`. None conflict;
   they'd anchor only if new canon dates them. Full list per chapter in the ledgers.

## Author rulings (2026-08-03)

1. **Lesson Tuesday collision** — fixed (a): "Tuesday night" → "Wednesday night"
   at `lesson.md:7`.
2. **"Only had him the once"** — fixed (a): clause cut at `recognized-method.md:65`.
3. **"Ready for days"** — fixed (a): → "ready since the morning after" at
   `all-the-time.md:103`.
4. **Hills and Valleys meta discrepancy** — fixed (a): the erroneous Oct 31
   housekeeping note in `meta-triage-hills-and-valleys.md` amended to Oct 24.
5. **"Longer parting than a Monday"** — fixed (a): → "than a Wednesday" at
   `see-you-later.md:83`.
6. **"A nothing Tuesday"** — left standing (a): idiom over ambient undated
   contact; recorded in `meta-triage-fairytale.md`.
7. **Header weekdays** — fixed (a): `we-find-out.md:3` → "An afternoon into
   evening"; `recognized-method.md:3` → "Two nights and the day between".
8. **The Bench "three weeks ago"** — accepted as note-only: ~6-day drift inside
   the "~Aug 8" soft anchor and an existing KEEP ruling; revisit only if the
   meet is ever hard-dated (then nudge the event date, not the prose).
9. **Unanchored cluster (84 claims)** — accepted as note-only: deliberately
   undated backstory, zero conflicts; the ledgers serve as the checklist if new
   canon ever dates any of it.
