# Triage — The Bench (cold-read panel, 2026-07-27; claude-fable-5 addendum 2026-07-30)

Panel: claude-opus-4-8, gpt-5.4-mini, gpt-5.5, gpt-5.6-sol · `reviews/cold-read/*/the-bench.md`

Verdicts on the friction items derived from the panel. **The "Left standing" section
records authorial decisions — do not re-flag these without new evidence** (a new
reader cohort snagging on the same spot, or an edit that re-opens the passage).

## Line-edit pass (2026-08-04)

14 items reviewed with the author (report: `audits/line-edit/the-bench.md`).
Ten prose edits applied (repetition thinning: weight-shift beat, salt kiss
moved to its earned arrival at the second forehead kiss, "athletic" moved to
the escalation, heartbeat kept only at the coda's "finally," "registered the
slick" pair cut/kept, lap-sequence beat recast as her subtle rocking, strike
warmth recast as "the heat coming up under his palm," bench-tilt explaining
tail cut at "designed for," hum coda trimmed to "she did not yet have a name
for," "lovely/pleasantly" thinned, doubled walk-order cut). Durable rulings:

- **"warm weight of them" (`:171`) — the Vol-1 keeper** (echo-rulings #5).
- **"chasing what her body had just lost, before she'd decided to chase it"
  (`:303`) — the Vol-1 keeper** (echo-rulings #8).
- **"let her have" / "he let her" — PROTECTED book-wide** (echo-rulings #12):
  Pace's governing grant-verb; do not flag.
- **"registering" kept twice by ruling** (`:33`-area cost-register and the
  social-vocabulary line) — acked in `style/style-allow.toml` with notes; the
  retired-frame rule stands elsewhere.
- **"She made a sound" density — no action:** the graded uses are a designed
  system; only the two ungraded neutral uses would bear varying and the
  author let them stand.
- Auditor findings 6 (gloss/sweat density) and 9 ("the way" cluster) were
  dropped as re-litigation of settled verdicts (gloss trim 2026-07-27;
  acked the-way suppressions).

## Fixed

- **Gloss motif over-hammered** (5.5; echoed 5.6-sol, 5.4-mini) — 8 tokens thinned
  to 6: the triple at the polish-register sentence reduced to one ("finish" picks up
  the woodworker register); the incidental body-register instance at the first
  parting went to plain "slick of her." The designed migration — gloss-as-polish
  → gloss-as-sweat/slick — is preserved via the remaining six. Commit `5c4427f`.
- **"Unwrapped gift" simile in the closing image** (Opus: on-the-nose; 5.6-sol
  uneasy from the other direction) — cut. The tricolon close ("full of what it was,
  doing what it would continue to do, waiting for the next time") carries the menace.
  Commit `5f5ebf8`.
- **Omniscient drift at the script-failing beat** (found during the editorializing
  check, not reader-flagged) — "she could feel something wasn't working" claimed
  Randi's interior in a Pace-locked passage; re-anchored as his observation (hands
  worrying the grips). Also removed a breathing-beat echo of the rhythm-break
  paragraph fourteen lines up. Commit `5f5ebf8`.
- **"her reading a purpose" fragment at the bench reveal** (Opus) — the one
  grammatical wobble in the reveal (narrator stumbling, not expressive
  fragmentation); made a full sentence, which also sets up "He knew what she was
  reading." Commit `738a7bf`.

## Left standing — do not re-litigate

- **Mid-section strike/soothe/kiss/withdraw cycle "a touch long"** (Opus + 5.5,
  both self-forgave in the same breath) — intentional. The patience *is* Pace's
  characterization; 5.4-mini and 5.6-sol cited exactly this stretch as where the
  heat peaks. Over-correcting is the larger risk.
- **"The bench was not the wanted position. The bench was the needing position."**
  and **"The orgasm was *hers*"** (5.6-sol: narrator thumb on the scale) — verified
  in context as Pace free indirect: the first sits inside his "He could see" script
  analysis; the second reprises his own italicized *Hers.* six lines earlier. The
  reader's discomfort is the intended effect of Pace's interpretive arrogance,
  misattributed to the author. The aphorism *shape* (freestanding paragraph) is what
  triggers the misread — acceptable cost. **SUPERSEDED 2026-07-31: the aphorism is
  cut** (see the 2026-07-31 addendum below). *"The orgasm was hers"* still stands.
- **Spatial parseability of the bench-reveal staccato** ("Open, everything open,"
  the piece-by-piece parse) (Opus, self-labeled "Minor"; other three readers clean,
  5.5 praised the specificity) — the staccato is Randi's real-time comprehension
  arriving in stages; blueprint clarity before she has it would be a POV loss.
  "Open, everything open" is her word landing in his paragraph — the reveal in
  miniature. "Her hands closed on nothing" stands.
- **"the coral lips"** (5.5, lone and hedged: "stylized/clinical") — stands.
  Precision-of-color is Pace's connoisseur register throughout (blue toes, deep
  pink); the sentence was already touched once in the gloss trim, and three readers
  cited the reveal as the erotic peak.

## Addendum — claude-fable-5 read (triaged 2026-07-30)

A fifth cold read (claude-fable-5), postdating the panel triage. Net-new findings:

- **"The needing position" aphorism — re-opened and fixed.** Fable-5 snagged on the
  same freestanding line 5.6-sol had flagged ("a sentence I didn't need after the
  paragraph that dramatized it"), meeting this doc's stated re-open condition (a new
  reader on the same spot; 2 of 5 readers now misattributed it to the author). The
  wanted/needing opposition stands as Pace's free indirect; the explaining appositive
  ("— something required that you could not supply yourself") is cut. Author chose
  cut-the-tail over merging the line into the preceding paragraph.
- **Consent-paradox line ("…had not consented to even though she had consented to
  the position") — left standing.** Fable-5 alone read it as "the tagline restated
  on the page"; three readers (Opus, 5.5, 5.6-sol) independently cited the same line
  as the chapter's kill shot. Lone dissent vs. confirmed positive — do not
  re-litigate on a single future snag.
- **Aftercare pacing "runs slack"** — self-forgiven by the reviewer ("it's meant to;
  the mirror pays it off"); same territory as the settled mid-section verdict above.
- Confirmations: the jacket-misdirect landed (fable-5 half-assumed the unnamed "she"
  was Vivienne until "There you are, Randi"); the locks bookend was noticed
  unprompted; mirror scene again named best writing in the chapter.

Note: all five reviews predate the 2026-07-30 undressing restage (standing, kneel,
single rise — commits `56adfd2` ff.); their references to bed-staging describe the
superseded draft.

- **The mother link in the mirror ("a voice she had not used since she was a small
  child in tears asking her mother…") — deliberate exception, left standing
  (author ruling 2026-07-30).** The scene-review pass flagged it as the one place
  the sanctioned aperture narrates genealogy rather than felt truth; the docs are
  silent on sanctioning the link. Author ruling: it stays — it is a memory of when
  the voice was last used (experience-level), not a mechanism analysis, and the
  cold readers uniformly read it as deepening. Do not re-litigate in either
  direction: do not cut it, and do not extend the mother connection further in
  this scene.

- **Pace's vantage in the Brooke sequence (line-audit 2026-07-31) — left standing.**
  A sentence-level audit flagged the unnarrated move from behind her to her head
  and the sightline claim ("Wet enough that I can see it from where I'm
  standing") as marginal geometry. Author ruling: the sightline is not
  precluded (bent-standing at the head end, knees spread), the dialogue
  self-certifies the vantage, and five cold readers never snagged. Do not
  re-litigate positional logistics in this sequence.
- **"Hang from the grips" / upside-down face (line-audit 2026-07-31) — left
  standing.** The audit read the phrase literally (a head can't hang from
  handgrips; a face in the cradle isn't inverted to a crouching viewer).
  Author ruling: the hanging is figurative — she is gripping hard, pushing
  into the grips, arms loaded, the head released into that frame; "from the
  grips" names the load path. "Upside-down"/"inverted" is Pace's impression
  of the hanging, hair-fallen face. Do not re-flag.
- **Blue lacquer named while the heels are on (line-audit 2026-07-31) — left
  standing.** The sentence claims knowledge, not sight ("still up in the
  heels he had not taken off" concedes they're hidden); prior acquaintance is
  confirmed by "He liked her feet."
- **Face turned sideways off-page (line-audit 2026-07-31) — left standing.**
  "Turned sideways now" back-announces a turn during elapsed bodywork —
  ordinary ellipsis; used consistently afterward.

## What the panel confirmed (no action; for the record)

All four readers, independently: the split-ledger Pace effect (seduced, then
recolored) reads as earned, not telegraphed; the consent-paradox line is the
chapter's kill shot and connects to the tagline; the mirror scene is the emotional
center, with the flinch and the bottle-cap tell prized *because* unexplained; the
seven-months/three-weeks line retroactively recolors the warmth as designed. Heat 3
/ Romance 2 across the board. Two readers unprompted predicted Randi turning outward
toward the game to recover control.

## Addendum — post warmth-pass rereads + author cuts (2026-07-31)

All four readers were re-run on the recolored scene (Pace-interior warmth pass;
see `meta-note-the-bench.md`), and a `pace-suspicion` oracle probe run on the two
Claude readers. Findings and the author's rulings:

- **The warmth pass landed.** No reader read Pace as a cold technician; both
  oracle readers scored calculating-vs-loving 3/5 and stated they never caught
  him faking warmth — suspicion attached to the *facts* (seven-months/three-weeks,
  end-of-night obliviousness), not the tone. Target state per the Console rule.
- **"The needing position" aphorism — CUT (2026-07-31), reversing the earlier
  KEEP.** Three of four fresh readers snagged again (professorial / too tidy /
  "the moment I distrust him most"), and the author ruled the one clean naming
  no longer worth the recurring thumb. The failing-script passage now carries
  the beat fully shown ("She could not pout her way back…"). Do not restore.
- **Coda de-operatored (2026-07-31).** Author ruling: the novel's argument is
  withheld information, not Pace's planning; the jacket + information asymmetry
  already carry forward pressure, and stated managerial intent taxed reader
  sympathy for Pace book-long. Cut from the coda: "He had been right about her.
  He had been right about the bench." (vindication register); the entire roadmap
  sentence ("…scene by scene… what he might want to do with her next… the
  surface he had just begun to lift"). "made small contented plans about her" →
  "quietly happy about her". The coda retains the benefactor-misread (apple/
  hunger), "gotten further into her," and "as often as she wanted to bring it
  to him" — the seed stays marked, in facts not tone. Do not re-add
  planning language to Pace's interior in this scene. (Follow-on ruling, same
  day: the possessive/acquisition register is **retired book-wide**, not fenced —
  see `meta-craft-pace.md` §Pride-in-effect, not possession. "gotten further
  into her" subsequently recast to "with his help, she had met more of herself…"
  — see `meta-note-the-bench.md`, de-operator pass.)
- **Audience-handhold paragraph ("The script had one handhold left: the audience…")
  — KEEP, flag for next panel (2026-07-31).** Added in the warmth pass as a
  counterweight where suspicion is known to concentrate (the Brooke maneuver, per
  the seven-months experiment). No reader has been asked about it specifically;
  the post-pass rereads that included it landed clean. Next cold-read round (or a
  targeted oracle probe on the Brooke sequence) should check whether it reads as
  care or as one script-analysis paragraph too many.
- **Cross-clone reconciliation (2026-07-31, second session).** The author walked
  all 24 of the day's changes (both clones) one by one. Rulings that adjust the
  warmth/de-operator pass above — these supersede where they conflict:
  - *Waiter-please passage restored verbatim* ("the voice she said *please* in
    when she asked a waiter for a glass of water…") — the recast stated the idea
    the image dramatized, and the waiter was a panel-confirmed positive. Do not
    re-abstract.
  - *"…and she had not yet figured out what to do with that" restored* (no-hurry
    paragraph) — ruled low-operator (observation of her agency, no plan/
    instrument/vindication marker); the warmth recast moved the beat's weight off
    her.
  - *"He was showing her what the next hour would be."* — author's own recast:
    "the map of" cut (surveyor register) but the showing kept concrete; replaces
    the warmth-pass "no clock on her tonight" version.
  - *Intention line*: "He **wanted**, before the night was out, to take the gloss
    well past itself" — warmth verb kept, original object restored ("take the
    gloss past itself" acts on the surface, not the woman; ruled no operator
    problem).
  - *Wanted-position trio restored + new five-word bridge* ("…She had spent her
    whole adult life there. **The bench was not there.**"). The needing-position
    aphorism stays CUT per the unanimous rereads; the bridge renders the
    displacement as pure subtraction, destination unnamed. Do not restore the
    aphorism; do not name the needing pole.
  - *Kitchen offering de-nouned to "her breasts asking for his hands"* — the
    chapter's first ask now lives in her body; "offering" appears once, at the
    appraisal. (Also this session: priming-press response "a sound came out of
    her"; scent-logic fixes; razor-not-wax legs; question marks per the
    flat-interrogative ruling.)
  - Everything else in the warmth/de-operator/mirror pass confirmed as-is,
    including the mirror expansion ("twenty-one years" kept) and the full coda.
- **Seven-months/three-weeks line — cut tested and ruled KEEP (2026-07-31).**
  A targeted experiment: the line was cut and the full four-model panel re-run
  fresh on the cut text (hypothesis: readers would warm substantially on Pace
  without the premeditation fact). Result: the weirdo/creep read did vanish —
  no fresh reader questioned the bench's construction, and all four took "For
  you. Tonight" as romantic craftsmanship ("built for her") — but overall
  suspicion did **not** drop; it relocated wholesale onto the Brooke maneuver
  and the end-of-night misread. Trust levels, Heat 3 / Romance 2, unchanged.
  The scene's suspicion load is over-determined; the line is not what costs
  Pace sympathy. Author ruling: the line stays — the beat's impact and the
  reread detonator are worth more than the null sympathy gain, and the line is
  the only on-page carrier of "the plan predates the woman" (in its absence
  readers uniformly believe the bench was built for Randi, false to canon).
  The experiment's reads were discarded (working tree reverted to the
  committed baseline panel, which matches the restored text; the OpenAI batch
  cost history retains the runs). **Do not re-propose this cut without new
  reader evidence.**

## Linter acks (2026-08-06)

- **`clock-verb` `:29` (`#ba366b91c77e`) — left standing, acked.** "he had
  watched her clock them the first night, and the second night, and the third,
  and had watched her never say anything." Surfaced late (during the
  {{How It's Done}} line edit, when `clock-verb`'s pattern was rewritten to
  detect the verb positively rather than exclude noun phrases — the old regex
  missed this line). Ruled *not* the frame the rule targets: the rule guards
  against Pace/Randi rendered as cold collectors, and here the
  noticing-and-storing is **Vee's**, characterizing her; Pace's action is
  watching, and the sentence's payload is the second clause — that she never
  says anything.
