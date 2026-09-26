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

- **`:517` "what was not her could be given away all day and cost nothing" —
  stands (line edit, cost-vague, 2026-08-11).** Raised in the book-wide
  `cost-vague` back-sweep (vague "cost something/nothing/anything"; rule + author
  ruling in `style/style-rules.toml`). Not the backward "high-effort thing dressed
  as effortless" snag that got peekaboo recast — the opposite structure: it's the
  the-face dissociation mechanism. The face takes the being-looked-at/wanted/
  touched and none of it reaches her, so it costs *her* nothing *because the face
  is not her*. Within that psychology the "nothing" is literally true — nothing is
  spent because she isn't behind it. Load-bearing for the-face architecture; do
  not re-raise.
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
- **"the coral lips"** (5.5, lone and hedged: "stylized/clinical") — ~~stands~~
  **SUPERSEDED 2026-09-07 (authorship audit — different charge, new evidence
  class):** the full-panel authorship audit flagged the color clause at 7/8
  models as a perceived-male-authorship tell (`meta-plan-authorship-fixes.md`);
  author trimmed the sentence to scent ("The cleft between her legs opened, and
  the scent of her began to reach him, unmistakable, the sea in it."). The
  reveal-as-peak praise attaches to the moment and survives; the original
  stands-verdict was correct against the craft flag it answered.

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
  reader evidence.** — **SUPERSEDED 2026-08-11: the line is now CUT (Pace-warming
  pass); the canon caveat below is retired with it. See the addendum.**

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

## Addendum — Pace-warming pass (2026-08-11, branch `pace-warming-the-bench`)

- **Seven-months/three-weeks line (`:99`, "He had begun building it seven months
  ago. He had met her three weeks ago.") — CUT, reversing the 2026-07-31 KEEP
  above.** Author ruling during the interior-warming pass: *a great line, but bad
  for the character.* It buys dread by making the bench predate Randi — Pace reads
  as cold/premeditated, the opposite of the first-read-clean mandate the pass is
  built on. Cut and committed (`cf83bf4`); excises clean (the throat-baring beat
  joins to "She did not turn back to him.").
  - **The prior KEEP's canon caveat is retired with the line.** The 2026-07-31
    ruling kept it partly as "the only on-page carrier of *the plan predates the
    woman*," its absence making "built for Randi" the read — then called that
    *false to canon.* The author now **accepts built-for-Randi as the reading**: a
    bench built for Randi and later used with Vee, rather than a standing
    pre-existing fixture (workshop ruling: possibly *stronger*; Pace can survive
    the end-of-Vol-2 darkness after ~700 pp of lovable-but-misguided). So the
    on-page premise is no longer "the plan predates the woman."
  - Full-panel cold reads post-warming (opus, sonnet-5, terra, sol, gpt-5.5)
    confirm Pace warmed with **no darkness cost**; Heat 3 / Romance 2 held.
  - **Do not re-flag the cut as a regression, and do not restore the line** unless
    the warming is later judged insufficient (author's stated escape hatch).
  - Open doc-trail: if "the plan/bench predates the woman" is asserted as canon in
    the arch/plan docs, reconcile it there to match this cut.

## Addendum — blazon pass + the ¶41 dossier ruling (2026-09-14)

`claude-opus-5` was trialled as a capture reader and all four personas
independently flagged the same thing on their first read: the undressing
sequence reads as a catalog and outruns the reader's patience
(*"cataloguing her like joinery… restless for her to be a person and not a
finish"* — fsog-refugee; *"I started thumbing ahead"* — romance-graduate).
`claude-opus-4-8` had never flagged it.

**The fix was diagnostic, not cosmetic: readers were not objecting to her
body — they were objecting to the commentary on it.** Cut the exposition,
add contact. Out went the gloss/warmth gloss (the razor-missed hairs already
enact it), the belly clause pricing her against her own regimen, the
buffed-and-polished thesis, "She felt all of it", "He could see the thinking
on her", three "flat plane"s, two filter verbs. In went her hands finding his
hair and Pace lifting them off with two fingers — *he wanted her hands empty,
not a distraction from what she had chosen* — and her body answering his
mouth against the wrist she is holding herself.

- **"She had buffed and polished herself" is deliberately ACTIVE** (author
  ruling). Canon says Pace does not price her labour (`meta-craft-pace.md:58`,
  *"the cleaner the win, the less reason to ask what it cost her"*), which
  argues for the agentless passive; the objectification finding outranks it,
  and his blindness survives intact at the coda and the mirror. Do not revert
  to "She had been buffed and polished."
- Verified on a full **7 models × 4 personas** grid on this chapter: 28/28
  CONTINUE, no stops. The body-catalog complaint now appears in one lane
  (opus-5/romance-graduate, self-timed at "maybe forty seconds"). glm-5.3
  cleared the passage by name: *"none — I was braced during the long undressing
  sequence that it might be pretty-but-empty, and it wasn't."* The cold panel
  raised no gaze friction at all.

### ¶41 — "and he was sorry about it" — LEFT STANDING, with the dissent recorded

Two opus-5 personas hit the apple-table sentence (*"He watched the thing behind
her face that policed her relationship to food…"*). It was the chapter's only
instance of Pace perceiving a **mechanism** rather than a body or a behaviour —
every comparable construction elsewhere is physical, and ¶227 is the correct
form (*"He knew this **because** the first time…"*, inference after evidence).
Diagnosis: the sentence was *method*, which `meta-craft-pace.md:21` forbids —
Pace is rendered in **reception**, never method. Author's framing: *we marry
what he sees with what he knows; what is missing is any feeling he has about
it.* Fix was six words, not a cut — the facts are load-bearing for the apple
motif and for the coda's misread. (Bonus: `the-induction.md:13` later names the
trait — *"sorry about it in the quiet way he was sorry about things"* — so this
is its first instance.)

**Two-call opus-5 probe split.** romance-graduate cleared and quoted the new
clause back approvingly (*"He's **sorry about it.** That's four sentences of
food-restriction backstory"*), and her "him narrating her interiority to me"
side-eye vanished. fsog-refugee stayed on the same sentence and **reframed**
the objection: *"his gaze felt less like love and more like a **dossier he'd
been keeping**, and I wondered if I was being asked to **admire** a man
appraising a woman's eating disorder."* Scores unchanged, 9/9 both.

- **Author ruling: this is by design and is not a defect.** The reader is
  correctly catching that **Pace watches and remembers**. She values the trait
  more negatively than intended — that is what she is seeing, not an error in
  the page.
- **Do not thin the facts to soften it.** The mother's egg whites, the
  sorority's one scale, "he had seen them", the drawn line — those *are* the
  dossier, and the dossier is the character. Adding warmth changes his
  temperature, not the fact that he has the file; that was the point.
- Do not revert the "sorry" clause on the strength of this one lane. n=1 per
  persona is noise by the panel's own discipline, and it demonstrably cleared
  the other reader's stated objection at no cost to score.

### The queer-woman column — expected, not actionable

`queer-woman` is the lowest score in every row that has it (7–8 against 9–10),
and three lanes across three vendors converge on the same complaint: the
chapter is all Pace's eyes and the prose admires his tempo (opus-4-8, *"the
book admiring his tempo for the third or fourth time"*; glm-5.3, *"too pleased
with its own slowness… the hand of an author savoring their own
craftsmanship"*). **Author ruling: a bonus pickup, always going to be tough in
a novel that is primarily hetero with a queer awakening.** It is a structural
property of a one-aperture Pace chapter, not something trimming reaches. Do not
re-flag as a regression and do not chase the scores.

## Addendum — developmental pass, four panel rounds (2026-09-26)

Four grounded cold rounds and four capture rounds on the same day against
successive versions (prose 620f4c13 → db78667b → 8d71b321 → today's final).
Reads in `reviews/` are the last round only; the earlier rounds' numbers are
summarized here. Scores held throughout: cold Heat 3 / Romance 2 (one Opus 4.8
Heat 2 on the compressed-loop version, back to 3 the next round); capture
21/21 CONTINUE every round, mean NEXT 9.2 → 9.5. Edits are recorded in
`meta-note-the-bench.md` (same date); this section records what was **left
standing** and why.

**Weighting rule (author, 2026-09-26): Opus lanes are down-weighted.** Opus
(4.8 and 5) is the most critical model on both panels; consider its flags,
weight them below the others. Removed models' reads are not consulted
(glm-5.3-flash, qwen, sonnet, terra, astra were erased the same day).

### Fixed this pass (see the note for the edits)
- Stated unhurriedness (229 / 237 / 247) — the "told me four times" complaint
  vanished from every lane after the cut.
- Undressing inventory — four models named it; none did after compression.
- Mirror anaphora — five models, then one, then none after the eyes paragraph
  was compressed. What remained ("explains itself at slightly too high a
  volume", GPT-5.5 / Sol / GLM) was the mechanism paragraph's restatement;
  "It had worked on everyone. It had worked for years." cut.
- "She was about to know." — GLM (full) and GLM-flash both called it the
  author's thumb; it telegraphed; cut.
- The right-please almost-stops (four to six consent lanes for three rounds)
  fell to zero once the lead-up was compressed. Nothing in the passage changed.
- Pace reading as rich (GPT-5.5 romance: "rich-man kink showroom") — gone after
  the small-house paragraph; no fresh read mentions money, wealth or the
  counters.
- Bench reveal read as spec sheet (Fable, Opus 5, GPT-5.5) after the hip
  support was added — rewritten as how it would hold her.
- The walk — DeepSeek's "one line too many" cut; Fable's dance/cheer bump
  folded.

### Left standing — do not re-litigate
- **The strike/soothe/check-in cycle at "Right, then left."** Opus 5's
  romance-graduate stalls there in every round and forgives it in the same
  breath ("a pattern I've read a lot of"). Same reader, same place, three
  rounds; Opus down-weighted; the cycle is Pace. Stands.
- **Daphne paragraph "inserted / a tidy lesson"** — Opus 4.8 only, three
  rounds; Sol, GLM, Kimi, GPT-5.5 credit it as earned. Stands.
- **"The orgasm was *hers*"** — Sol would rather feel it than be told; the
  2026-07-27 ruling stands (Pace free indirect).
- **Pace's coda ("All he had done was find it, and answer it"; "quietly happy
  about her")** — consent lanes name it and read it as the designed irony
  every round. Stands.
- **Italic *hers* "hammered by the fifth"** (Opus 4.8) — there are two in the
  chapter. Dismissed.
- **The final paragraph** — cited by four to six of seven cold readers each
  round as the source of forward pull; every "what I want next" is Vee and
  what Randi does with the lock. Author ruling: not replaced with a concrete
  hook; a hook would be a plan-tell, and chapter 2 ({{Standards}}) stays with
  Randi.
- **"the sea in it"** — Kimi blinked once. Stands.

### Instrument notes
- kimi-k3 failed validation three times on the 8d71b321 version (structured
  block missing); not recorded. The cold harness now persists rejected output
  under `<model-id>/.failed/` for diagnosis.
- gpt-6-astra trialled on capture for one round and replaced by gpt-6-sol
  (needs `CODEX_BIN`); astra's gates removed, never committed.
