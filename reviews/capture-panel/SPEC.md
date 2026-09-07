# Capture/retention panel — SPEC (v1)

*Committed 2026-09-07. Measures **capture and retention** across the free-sample
stretch: persona-conditioned blind readers take the first four chapters
(`the-bench`, `standards`, `the-pointing-game`, `see-you-later`) sequentially
in one sitting, with a hard STOP/CONTINUE gate after each chapter. Purpose: find
where target readers would put the book down, before the sample goes public
(`meta-plan-free-sample.md`).*

## Instrument

Each read = one persona × one model × one arm, on the clean lanes (same
isolation as the authorship audit; `tools/capture_panel.py`). The reader gets
the core reader frame (`prompts/core.md`) + a persona block (`personas/*.md`)
as the ENTIRE system prompt, then [arm-dependent jacket +] the four chapters.
After each chapter: DECISION (STOP/CONTINUE), CAPTURE 0–10, ALMOST-STOPPED
(the exact moment, quoted — the actionable output even when they continue),
WHY in persona voice. A STOP ends the read (no later gates). Finishers answer
the conversion questions (would-pay at $9.99, mailing list, tell-a-friend
paragraph).

**Honesty mechanism:** models are completion-biased, so the frame weaponizes
the real economics — infinite free alternatives one click away; stopping is
the default; the book must earn each next chapter. Gradient (CAPTURE) and
ALMOST-STOPPED give signal even when outright stops are rare. Read the results
as a survival curve + ranked almost-stopped moments; single-read stops are
noise, convergent ones are findings (same convergence discipline as the
authorship audit).

## Personas (versioned in `personas/`; run header records SHA)

1. `romance-graduate` — outgrown spicy romance, won't give up the heat
   (primary vector, `meta-plan-distribution.md` §4).
2. `fsog-refugee` — wants the FSoG intensity with real consent and warmth
   (the crossover strategy, `meta-plan-pen-name.md`).
3. `consent-sensitive` — vigilant about predation-romanticizing; measures the
   **con-misread exposure** the docs flag for exactly these chapters (stays
   with dark content only if the book visibly knows what it's doing).
4. `dark-romance-control` — the WRONG reader ("wreck me with a bad man");
   should bounce. A book that captures her is failing the repel goal; her
   stops are successes.

## Arms

- `jacket` — Volume One jacket packet (`checkpoint_bundle.jacket_packet()`)
  precedes chapter one: the retail-sample funnel, with the designed
  complicated-love-not-a-con pre-framing in play.
- `cold` — chapters only: the Literotica-style funnel, no pre-framing.
  The delta between arms measures how much work the jacket actually does.

## Roster & scale

Full 8-model panel, paid lane author-authorized 2026-09-07 ("full panel
including paid"). 4 personas × 8 models × 2 arms = 64 reads. Personas are
simulations of readers, not readers — treat output as candidate signal for
authorial judgment, strongest where personas × models converge; the eventual
ground truth is the human test-reader cohort (`meta-plan-test-readers.md`).

## Run 1 results (2026-09-07 — 64 reads, full panel, both arms)

Survival (finished/8 · pay-yes · list-yes): romance-graduate jacket 8/8·8·8,
cold 8/8·8·7 · fsog-refugee jacket 8/8·8·8 (after one truncation re-run), cold
6/8·6·6 · consent-sensitive jacket 8/8·8·8, cold 8/8·7·5 · dark-romance-control
jacket 7/8·6·6, cold 5/8·3·3. **Six stops total**: 4 = control bouncing off
"safe Pace" in chs 1–2 (the filter working: "not the man I came here for");
2 = fsog-refugee **cold-arm only**, exiting chs 3–4 over Vee's uninformed /
Randi's managed consent — the premise, not the craft ("the third person's
consent is this far behind the couple's desire").

Key findings: (1) **the jacket is load-bearing for the FSoG refugee** — 8/8
with pre-framing vs 6/8 cold; the Literotica funnel should carry framing that
does the jacket's permission-work (→ `meta-plan-free-sample.md`). (2) **The
2026-09-07 pointing-game irony cue is the panel's most-cited trust line** —
"He took the body's answer for the true one. He usually did." cited by ~23
reads as the reason fsog/consent readers stayed ("a loaded gun on the wall";
"the author's thumb on the scale, marking his epistemology as a habit, not
wisdom"). (3) **Ch 2 `standards` is the universal capture dip** (9→7→9→8
book-shape; the "did not cry" stillness cluster cited ~25×) — no target
reader stopped there; monitor, don't fix. (4) **Control leak is genuine
attraction, not misread**: the 9 finishing controls stayed for Randi-as-
predator / daylight grooming ("my exact kink wearing a Sunday dress") —
a secondary audience the no-villain ending may later betray; keep them out of
targeting (already policy). Consent-sensitive persona granted trust
explicitly conditionally: the book reads as *knowing* — trust to be honored
downstream.

## Output

`reviews/capture-panel/<model-id>/<persona>--<arm>.md`. Not indexed by `na.py`
(no `## Reader reaction` section — instrument output, not a cold read).
