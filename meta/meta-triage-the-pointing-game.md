# Triage — The Pointing Game (line-audit pass, 2026-08-01)

Source: sentence-level consistency audit (`audits/line-audit/the-pointing-game.md`),
reviewed item-by-item with the author. **The "Left standing" section records
authorial decisions — do not re-flag these without new evidence** (a new reader
cohort snagging on the same spot, or an edit that re-opens the passage).

## Line edit (2026-08-05)

Source: `audits/line-edit/the-pointing-game.md`, reviewed item-by-item with the
author; 12 findings plus one reader-flagged bonus item; 10 edits applied. This
pass also piloted the **cold-read enrichment step**: the chapter's four
`reviews/cold-read/*/the-pointing-game.md` reader reactions were mined for
line-level praise/criticism before ruling, and reader evidence decided several
items (now standard prep — see the command doc).

### Fixed (line edit)

- ":31 adverb pair reversed to "deliberately, slowly" — kills the stock cadence,
  puts intent in governing position (tempo as expression of decision).
- :37 "She would be happy." cut; "earned" → "deserved" (earned is transactional/
  bookkeeper register; deserved is the gift-logic judgment of worth).
- :41 "…and the flinch was the sound of the catching" cut — ruled left-standing
  at first, then re-opened on reader evidence: claude-fable-5 (only reviewer to
  quote it) called it "one clause past necessary," the sole line any cold reader
  flagged as overwritten. The comprehension clause ("The want had shown itself
  before she could dress it as anything") KEPT — it carries reader
  understanding and seeds the costume-reach in the next paragraph.
- :49 "the way the last piece of a thing settles" simile cut — doubled "settle,"
  and the verb + chest was already complete (also clears a `the-way` linter hit).
- :65 second "The wind came down off the ridge" → "The wind found her hair" —
  protects the :127 callback (the wind given Vee's hair what Randi refused it).
- :65 "and got almost nothing for the trouble" cut — the joke told once, in its
  stronger form (the tail flirting/giving nothing sets up "not a strand more").
- Unhurried motif thinned to zero literal uses (linter ruling: Pace's word,
  thin drastically; none of these touched his care with Randi/Vee): :35 "in no
  hurry to be anywhere" → "contented" (author: contentment is a state a body
  publishes — readable like a cat's, not mind-reading); :63 "long unhurried
  passes" → "long slow passes"; :91 ", in no hurry at all" cut; :123
  "eventually and without hurry" → "eventually" ("delivered" carries the
  leisure); :145 "an unhurried angle" → "a comfortable angle" (author: physical,
  carries the enjoyment without naming it; "waiting on someone" already covers
  the camouflage). :93's full no-rush argument kept as the motif's one
  load-bearing statement — it never uses the word.
- :93 appositive tail trimmed — ends "…because it was fun, her edge and his
  attention." ("the kind of afternoon she had learned to expect from him"
  restated :57's she'd-learned-to-be-game).
- :119 "He'd guessed wrong." cut — reversed from the finding: the *setup*
  ("He thought he had it") is what gives "God, no" its height; the
  after-the-fact restatement is the redundant bracket.
- :137 "But she had already told him — with the dropped stride, before the
  editing." cut — paragraph opens at "The maple was burning". Reader-backed:
  the surrounding beats are the chapter's most-praised sequence (landed without
  help), and gpt-5.6-sol's one craft complaint named exactly this
  stating-after-showing around Randi's camouflage.
- :51 "and meant several things by it" cut (reader-flagged, claude-opus-4-8
  "a small nudge") — the prior paragraph enumerates the several things; "easy"
  does the sinister work; the tag re-inflates the word the sentence
  deliberately deflated. Author ruled cut on the craft case despite the
  comprehension rule.

### Left standing — do not re-litigate (line edit)

- **:41 first clause** ("The want had shown itself before she could dress it as
  anything") — comprehension-carrying; author principle: when we think we're
  oversignaling, cold readers may not get it. Kept while the metaphor tail was
  cut on reader evidence.
- **:141 "hers to take" run** — NOT an echo of the italicized "*is this one
  mine to take*": call-and-response. The clause is the antecedent of "And it
  took" (the answer taking); cut it and the pronoun grabs air. Finding
  dissolved on fair reading; the full run stands (only candidate trim, if ever
  re-opened: "before she went").
- **:147 three "looked like"s** — a designed ladder of misreadings, one per
  phase: *chance* (approach), *nothing* (contact), *the redhead walked into
  her* (causality reversed). The first term's unmarkedness is correct — the
  approach is the phase not meant to be noticed; the construction surfaces
  into explicit anaphora exactly when the execution becomes visible. 90 words
  is well within a reader's refrain-reach; do not re-flag as repetition.
- **"before the lead" / follow-lead metaphor** — crosses to `lesson.md:101`
  by design (the dance floor is the metaphor's literal source); a thread, not
  an echo.

## Narration-certainty pass (2026-08-05)

Author-initiated: reduce spans where the narration *endorses or grades* Pace's
certainty rather than inhabiting it. Distinct from the declined de-operator
pass (that targeted his operator register, which stands); this targeted
narrator-verifying-Pace spans, with cold-read evidence weighed per the
enrichment step. Readers uniformly experience Pace's certainty as
characterization ("he's certain he's giving her a gift" — opus, as praise of
the effect), so this was a trim, not a recolor.

### Fixed (certainty pass)

- :29 "That was the honest part, the part he'd have told her if telling were
  his grammar." cut — gpt-5.5 flagged the phrase as the book's intelligence
  being "very visible."
- :29 "by some old architecture he did not examine" → "by some old
  architecture" — split evidence: claude-fable-5 called the full sentence "the
  scariest thing in the book so far" (kept), gpt-5.5 called it "a warning label
  applied directly to him" (the self-aware hedge cut). Ruled c): keep the
  sentence, drop the examines-his-own-not-examining paradox.
- :33 "Pleasure was not a trick. It was a true thing he was giving her — and
  if it was also a bridge" → "If pleasure was also a bridge" — gpt-5.6-sol:
  "the line where I most feel pressure from the narration"; the bridge
  concession (fable-praised: "he's rationalizing, and half-believing it") kept.
- :41 "the kind of thing a less attentive man would have missed entirely and
  called her calm. He did not miss it." → "the kind of thing he might have
  missed entirely if he had not been paying attention." — removes the
  lesser-man ranking and the self-verifying tag.
- :131 "— the girl was never who he was watching, Randi was —" cut —
  claude-fable-5: "I'd already understood that; the line underlines it. Small
  thumb on the scale."
- :47 "and because he was built to see it" cut (post-edit re-run, same day) —
  initially left standing, re-opened on convergent fresh evidence: the re-run
  cohort snagged on this exact clause twice (claude-opus-4-8: "a hair too
  pleased with Pace's perceptiveness, telling me he's a genius reader rather
  than only showing it"; gpt-5.6-sol: "presses his special perceptiveness
  hard, especially when the prior chapter showed how badly he missed Randi's
  concealed distress"). Sentence now ends "because it was beautiful." The
  "Same act. A different owner." payload it introduces remains protected.

### Left standing (certainty pass)

- **:7 "He knew the difference between a woman performing release and a woman
  delivered to it."** — gpt-5.5 quoted it as "sexy as competence, but also
  immediately controlling as certainty": the double read landing as designed.
- **:43 "on another man it would have worked completely"** — HELD, not ruled:
  revisit after the post-edit cold-read re-run if the lesser-man comparison
  still reads as ranking.
- **:37 "that mattered to him more than the answer did"** — opus argues with
  it ("Does it, though? … The 'choice' is theater") — a reader distrusting
  Pace, not the author; the certainty is generating the intended distrust.
- **:47 "The same act. A different owner."** — the frame-analysis payload
  stays protected (fable and sol quote it as the chapter's key insight); only
  the introducing "built to see it" clause was cut (see Fixed, re-opened on
  the post-edit re-run).

## Fixed

- **Date/season conflict with the chronology** (audit item 1) — the scene said
  "Wednesday-afternoon current" and "late-September afternoon" against the
  chronology's Tue Sep 8 pin (which the scene's own "four weeks in" supports).
  Fixed: Wednesday → Tuesday; "late-September" dropped; an early-September
  **cold snap** (~Sep 1–6) established to carry the early color ("the nights
  had come in cold the week before") — now canon, chronology continuity
  flag 28. `meta-condensed-the-pointing-game.md` corrected to match.

## Left standing — do not re-litigate

- **"She had decided that morning how much of herself the day would get" vs.
  the post-bed shower** (audit item 2) — the audit read the ponytail as a
  morning artifact contradicted by the afternoon shower/redress. Author
  ruling: the line names a *decision* (the day's ration, set that morning),
  not a styling event; the post-shower re-binding is the same decision
  re-executed, which is characterization, not error. "That morning" is
  load-bearing (the ration predates Pace's bed).
- **Panel one's compressed exit vs. panel two's shower** (audit item 3) — panel
  one reads as a continuous dress-and-leave ("reached for hers too" → "held
  the door for her") while panel two adds a shower/makeup interval. Author
  ruling: leave standing — "held the door" is exit-summary whose cargo is
  "did not tell her what the walk was for"; the panel break is a time cut and
  readers assign the shower to it. The line-77 shower detail stays (fresh,
  re-assembled, game).
- **The unwiped-mouth kiss carrying her taste an hour after the bed** (audit
  item 5) — flagged as a physiological stretch. Author ruling: leave standing —
  the beat is *designed* (the chronology entry plans "a hard kiss without his
  mouth wiped, to teach her what the maybe costs"; taste-thread canon), and
  the claim runs through her recognition, not chemistry. Do not re-flag as
  biology.
- **De-operator pass — proposed and DECLINED whole (author ruling 2026-08-02).**
  A nine-item recolor of Pace's operator-register narration (per the
  `meta-craft-pace.md` "warm, tender, misguided — never technician" rule; items
  included "He had decided this beforehand," "worked the third one out…
  deliberately," "the exact frame he needed to proceed," "fast and without
  seeming to, for the angle it gave on the doors," "watched his afternoon's
  work talk to its result"). Author reviewed the proposals and ruled: the
  impactful ones softened the scene's best lines and images to
  meaninglessness — the operator register in this scene is carrying the
  diptych's argument (reconnaissance wearing a game's costume), not drifting
  from it. The scene stands as drafted. Do not re-propose a technician-drift
  recolor of this scene without new reader evidence.
- **"The maple was burning" at the dining hall** (audit item 6) — flagged as a
  dubious sightline (the maple is near the chapel, several landmarks back).
  Author ruling: leave standing — it is a refrain, not geography: the
  early-turned tree fused to the copper-haired girl in the same sentence.
  Do not re-flag as a sightline.
- **"A hundred feet…still to close" vs. "across thirty feet"** (audit
  item 7) — the gap closes in rendered action (Randi dispatched, Pace
  relocating to the light pole); not a contradiction.

- **"she had stopped being a good sport a quarter mile back. She was shopping."** —
  line-editor (fable-5-1, whole-volume read 2026-09-30) tagged it
  *told-after-shown*; no other reader quoted it (0 of 162 files). Author ruling
  2026-09-30: stands — a designed line.

## Addendum — developmental pass (2026-09-26)

Source: author + human-reader flag (bed→walk transition abrupt; implied Pace
already had a woman in mind), read against the eight-lane cold panel and the
ch003 capture gates. Canon check: Vee is a first sight and the walk is
improvised (chronology, condensed brief, pace-misread note).

### Fixed

- **Opening paragraph added** — Randi's ask, recalled: on her way into the
  bedroom she slows at the long table with its top back on and, this time,
  looks at it (Saturday morning she walked past it without looking), and
  says *Let's do something different. Today.* Handed over rather than asked
  (the {{The Bench}} "what are we doing tonight" mechanism). Second pass
  same day: the author replaced a door-recall version with the looking
  version so the bench brackets the chapter. Gives :9 "He had decided this
  beforehand" its antecedent — her request.
- **The game is invented in the moment** — bridge paragraph after *"Okay"*:
  he lies there thinking and the idea arrives out of her *with you* — *All
  right, then: with him. He could show her. They could find it together.*
  Kept bare on author ruling (the campus/women/"a game, say" lines and the
  gold light were cut): "she would not go toward it named" flagged a consent problem rather
  than a fun game, and spelling the mechanism out here took away the surprise
  the reader currently has alongside Randi. The two pre-namings of "the game" in bed (:29, :37) were trimmed so the
  invention reads as invention; :59 "He had no name for the game yet" stands
  and now follows from the bridge. Author ruling: do **not** render him
  planless — the game is planned, generously, in the moment.
- **:125 denial cut** — "He had not chosen the spot in advance" removed (a
  denial plants what it denies); the object widened from "the doors" to "the
  doors and everyone coming through them" — a stream, not a stakeout. The
  operator-register wording of the sentence (declined recolor, 2026-08-02)
  is otherwise untouched.
- **Orphan repaired** — :129 "the closed camel-coat project" survived the
  2026-09-14 candidate cut (claude-opus-5 cold read: "nobody on this quad wore
  a camel coat"). Term dropped; condensed brief and chronology typology
  trimmed to match.

### Left standing

- **"He took the body's answer for the true one. He usually did."** — the
  convergent capture almost-stop (10 of 18 gates); every lane continues and
  reads it as designed. Stands per the certainty-pass ruling.
- **Candidate parade length** (five lanes, "one past necessary") — already
  cut once; the *maybe* / *God, no* pair is the taste triangulation.
- **"Go meet her" arriving fast** (three lanes) — the permission beat at
  :143 answers it.
- **Closing beat added (second pass, same day)** — after the second *yes*,
  quiet against him, eyes still on Vee: *"Do you think she'll like the
  bench?"* He kisses the top of her head (the {{The Bench}} gesture) and
  does not answer: *"Let's go feed you."* Author ruling, taken knowingly:
  the Bench panel's dominant forward guess (Randi steering Vee toward the
  bench) is confirmed here as a promise; on reread {{Vee on the Bench}} is
  a wish Randi voiced in September and hears fulfilled without her at
  {{Vee Tells Randi About the Bench}}. "The fact of her pleasure stayed
  bright in him" cut to make room; no Pace interior sits between the
  question and the answer.
- **Second ask grounded in bed (third pass, same day)** — before *"Do you
  actually want to taste another woman?"*: her head on his chest, her
  fingers idle on him, chest to stomach and back; *Her breath had come
  all the way down* (the :39 condition met — he waits for the heat to
  leave the room; the prior waiting and framing stand); *He asked it into
  her hair* (rhymes the first ask's *into the warm disorder of her*). :43
  "said in bed" kept (a "said in the heat" recast was tried and reverted on
  author ruling — the grounding sentence now does that work). The flinch re-opened on author ruling: a flinch is
  instantaneous, a shiver takes time — the "shiver under the skin" gloss
  cut; the flinch is *felt*, not seen (her body against his going tight
  for an instant and letting go), a shock to her, not a literal lifting of
  her fingers. The kept comprehension clause (:41 ruling above) untouched.
- **Word-level (same pass)** — :91 "the frame snapped into place" →
  "the picture", reserving *frame* for the dance hold at :137; "register"
  thinned 4 → 1 (:45 "the low warm voice", :71 noun dropped, :123 "the
  trailing voice"; :163 "the register she only used in his bed" kept as
  the load-bearing one). Rec-center pair paragraph: trim proposed on the
  detail-versus-verdict argument, **declined** by the author; stands.
- **Heat slip diagnosed and repaired (fourth pass, same day)** — the round
  on fb27fff0 dropped Heat to 2 in four cold lanes (fable, opus-4-8, kimi,
  deepseek) with only the bed-panel spans changed. Cause: the grounding
  sentence pre-spent the recovery's finger-down-the-chest move (her fingers
  were already tracing chest to stomach) and stated the cooldown outright
  ("Her breath had come all the way down"). Recast: head on his chest, one
  leg over him, her hand lying still on his stomach; the breath sentence
  cut (:39 already carries the waiting). Added, after the flinch and before
  the comprehension clause: *The tip of her tongue touched her lip and was
  gone.* — appetite after recoil, her own taste on her mouth at the
  question; no gloss (author's "as if searching for another taste" dropped
  as decoding). Retest ordered.

## Addendum — appetite pass (2026-10-09)

Author-initiated: Pace read too saintly in his interior for the man who built
the bench and is arranging a threesome around an unknowing girl. Seven drafts,
each read by a nine-lane cold panel; capture run on five of them. Chapter
5,101 → 4,977 words.

### Rulings reversed (all author, 2026-10-09)

1. **:25 "He took the body's answer for the true one. He usually did." — CUT,
   reversed in meaning** to "He knew her body's answer. He did not take it for
   her answer." Reverses the certainty-pass left-standing entry below (the
   convergent capture almost-stop, 10 of 18 gates) and `:25 APPLIED
   2026-09-07`. Carried on the first wording tried ("He still meant to ask
   her") being read as flattery — `claude-opus-5`: "his self-narration is
   starting to flatter him faster than the page earns"; `claude-opus-4-8`:
   "thinnest when it lets him be right about everything." The second wording
   is a claim the chapter then watches him violate, which pays him nothing.
   `claude-opus-5` on the result: "he asks the question twice and refuses her
   body's answer as her answer." **About 25 corpus files quote the old line,
   including a carry-forward checkpoint
   (`claude-fable-5-1/dag/romance-graduate/ck-ch010.md`).**
2. **"The same act. A different owner." — CUT.** Reverses `:47 APPLIED
   2026-09-07` ("untouched — 3/4 repair contest + cold-reader protection
   carried it") and the certainty-pass protection of the frame-analysis
   payload. Author: "I KNOW. I was there."
3. **"She deserved that gentleness. He wanted it for her." — CUT.** Reverses
   the 2026-08-05 line-edit outcome, where the pair survived a pass aimed at
   this paragraph and "earned" was deliberately reworded to "deserved."
   Three on-roster lanes named it on the current draft.
4. **The frame-break's dance sentence — CUT.** "The follow had felt the music
   and broken frame before the lead called the step." Inside the zone the
   pace-misread note fences. It was the fourth statement of the same event in
   its own paragraph, and its claim contradicted the page: ":143" is "'Her,'
   Pace said, and pointed" — the lead had called the step two lines earlier.
   The note's own principle ("only the observable belongs on the page") is
   what the cut serves. Result: the "used twice" charge left all nine lanes
   and `claude-opus-5` praised the surviving first use — "the
   follow-gathering-before-the-lead image is gorgeous."

### Tested and restored — do not cut again

- **":37" "that mattered more to him than the answer did"** — cut, then
  restored the same day. Romance fell 2 → 1 in `claude-opus-4-8` and
  `gpt-5.5` on the round it was cut, and both recovered to 2 when it came
  back. `glm-5.3` then quoted the restored clause **as** the tenderness:
  "that second asking, 'that mattered more to him than the answer did', is
  the tenderness." The 2026-08-05 left-standing ruling was correct.

### Breached and repaired

- **":129" "He was not guessing any more."** was added to make his certainty
  about the room-runner louder, which **breached the 2026-08-05 ruling** on
  this slot (":119 'He'd guessed wrong.' cut — the setup, 'He thought he had
  it', is what gives 'God, no' its height; the after-the-fact restatement is
  the redundant bracket"). Removed. `glm-5.3` on the restored state: his one
  misfire "is welcome because it keeps him human."

### Also cut (not previously adjudicated)

- "It was the wrapper the wanting needed to come out in." (three models, two
  vendors, no reader praised it as prose)
- "Her body wanted this; her mind had not yet caught up to it."
- "If pleasure was also a bridge…" (`claude-opus-5`, three drafts running)
- "command and abundance riding in the same frame" (the caption on the clause
  before it; the athlete clause stays — it is Vee's swimmer body,
  `four.md:109`, and the athlete *under* the lushness is what makes Randi's
  grading grammar fail)
- "and mostly he had" at the taste summary; the hundred-word paragraph
  explaining the permission; ":31"'s closing duplicate of ":39"

### Attributed rather than cut (author 2026-10-09)

- "which was unsurvivable" → **"which he could see was unsurvivable."**
  Implements the shape of alternative (a) held on file at
  `meta-plan-authorship-fixes.md` since 2026-09-07 and never ruled.
  `claude-opus-5-5` read it as intended — "He even registers that wanting
  another woman is 'unsurvivable' for her, and goes ahead and builds a game
  to take her there." `claude-fable-5-1` objects that it claims
  "near-omniscience about her interior, when I just read a whole chapter
  proving her interior is the one room he can't enter"; the audit's hedged
  alternative ("which he was certain she'd find unsurvivable") remains on
  file, unruled.
- "It was the best idea he'd had in a month." → **"He thought it was the best
  idea he'd had in a month."** `gpt-6-astra`: "I have just watched him
  misunderstand what followed the bench, and now *he thinks* this is 'the
  best idea he'd had in a month.'"

### Left standing on this pass (author 2026-10-09)

- **":9" "He knew the difference between a woman performing release and a
  woman delivered to it."** The `:9 RULED 2026-09-07` revision trigger
  ("subject to revision on a future panel read") **fired** — `gpt-5.6-sol`
  and `deepseek-v4-pro-0813` both named it — and the author declined.
  `deepseek` closed on "Small. It didn't damp the chapter." The Opus hedge
  stays on file.
- **":101" "the whole art of it was that it stay a game"** — two vendors
  (`claude-opus-5`, `deepseek`). Stands.
- **The quad/colonnade paragraph.** Interrogated on the author's belief that
  it had only ever drawn complaints; it had not. One skate
  (`claude-fable-5-1`, self-qualified "not close to stopping") against one
  cash (`claude-opus-5`: "composed two centuries ago by men who wanted the
  eye to travel exactly this way, laid directly beside a man directing her
  eye — invited, not forced"). The two audit files that mention it do so only
  in a route-continuity check and in a hit on the *following* paragraph.
  Stands.
- **The candidate parade** and **"She was shopping"** — re-flagged by
  `claude-opus-5` and `claude-opus-5-5`; both previously ruled. Stand.

### Open

- The **appositive** at the former hinge ("not a woman who hungered for
  another woman … but a girlfriend offering her man a gift") — two vendors
  across three drafts. Unruled.
- The **dance motif** as a whole, not the cut sentence: `claude-opus-4-8`
  "the dance metaphors stacking up (follow, lead, turn called); it's a touch
  over-sold." The motif spans ":119", ":173" and the collision's "a decade of
  dance." Unruled.

### Measurement note — the scores are the noisy output, the prose is not

A same-prose retest was run to calibrate: 14 subscription lanes, byte-identical
chapter, no edit between. **9 of 14 lanes moved, every move exactly ±1, no axis
ever moved 2.** Mean |delta|: CAPTURE 0.36, NEXT 0.21, HEAT 0.14, ROMANCE 0.29.
Baseline preserved at `reviews/capture-panel/noise-baseline-ch003-2026-10-09.md`.

**Consequence for reading this instrument: a single lane moving a single point
is noise.** Treat a score as signal only when two or more lanes move the same
direction on the same axis, or any lane moves 2+. The ":37" finding above
clears that bar (two lanes down together, both back up on restoration); a
Heat drop attributed to the dance cut did not, and was withdrawn. The written
complaints converged reliably all day while the numbers did not.
