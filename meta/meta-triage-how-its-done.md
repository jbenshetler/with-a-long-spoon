# Triage — How It's Done (line-audit pass, 2026-08-01)

Source: `audits/line-audit/how-its-done.md`, reviewed with the author.
**Left-standing entries are authorial decisions — do not re-flag without new
evidence** (audit verdicts re-open on a text edit to the passage).

## Fixed

- De-clocked the lunch: dropped "at eleven in the morning" (:13) and the
  noon/by-two anchors in the wine quip (now "If I have wine, I'll be facedown
  in the stacks this afternoon…"). The golden-hour return now needs no
  accounting; Vee's study plan still quietly dies (Randi-gravity, deniable).
- Car garment reconciled: the wind opens "the collar of the cashmere" (was
  "silk") — open cashmere over the camisole in the car, removed at the booth;
  the wrist-band clause ends at "there now" (no silk against a bare arm).
- The Rombauer gets its on-page beat: ":104 turning her wine glass" — the
  glass-fidget is Randi's tell (cf. the water glass at :80), so "glass" stays
  in the phrase.
- Geography: the restaurant is "off Prices Fork" (was the impossible "Route
  9" — Loudoun County). Pace's house stays on 614 (per {{Off Six-Fourteen}});
  the Chili's stays "out by 460"; each road keeps its own register.

## Left standing — do not re-litigate

- **The waiter's unrendered arrival (:35)** — deliberate frictionlessness:
  staff materialize around Randi ("The host knew Randi"); restaurant
  convention covers the elision, and "wrote it down without comment" lands
  better from nowhere.
- **"Best thing that's happened to me all month" on Oct 4 (:57)** — stock
  intensifier in Randi's performance register; calendar arithmetic is the
  wrong instrument for a told story.
- **"You said he's a looker, this man" (:104) with no drafted antecedent** —
  no gap: Randi saw Pace herself in {{Substitution}}; the "you said" is Randi
  laundering her own observation through Vee, keeping her own eye hidden —
  a tell, not an attribution slip. Do not seed a prior "looker" line
  (verified 2026-08-01: the word appears nowhere else in scenes/).

---

# Triage — How It's Done (line-edit pass, 2026-08-06)

Source: `audits/line-edit/how-its-done.md` (12 findings) plus cold-read
enrichment and the style linter, reviewed with the author item by item.
**Left-standing entries are authorial decisions — do not re-flag without new
evidence** (line-edit verdicts re-open on a text edit to the passage).

## Fixed

- `:17` — (line edit, cost-vague, 2026-08-11) "Randi appeared not to **register**
  the girls at all, **or if she did they cost her nothing**, and she drove them off
  campus one-handed" → "Randi appeared not to **notice** the girls at all, and she
  drove them off campus one-handed". Book-wide `cost-vague` back-sweep (rule +
  author ruling in `style/style-rules.toml`). Cut the hedge clause outright — it
  did triple duty as a tic: register-verb ("register"), vague cost ("cost her
  nothing"), and overwork (the hedge weakened the sovereign imperviousness).
  "appeared not to notice the girls at all" is the stronger, undivided version of
  Randi's impassivity; the "or if she did" concession undercut it.
- `:5` — cut the second "at the curb" (the sentence already knows where the
  car is).
- `:13` — cut the hair/wind trailing clause ("a torrid affair with the
  wind…"): two courtship personifications in one paragraph split the joke;
  Randi's controlled flirtation is the one doing character work. Also
  resolved the doubled "boisterous" for free.
- `:15` — "kept looking a beat too long" → "kept looking too long"
  (echo-ledger FIX-AT #2); "studied Randi the way you study what you'd like
  to learn" → "studied Randi" (study/learn near-tautology); cut "instead of
  the glamorous girl" (a label after four clauses of showing — `:164`'s "the
  most glamorous woman she knew" is Vee's own vocabulary and stands).
- `:7` and `:17` — echo FIX-AT #2 ("a beat past"). *Both* varied; the chapter
  claims no keeper slot. `:7` "it stayed a beat past when it might have
  stopped" → "it stayed past when it might have stopped"; `:17` "held the look
  a beat past nothing" → "held the look a beat". The first attempt kept `:7`
  and varied `:17` to "held the look past nothing" — reversed the same day: the
  figure was opaque ("past nothing means nothing to me") and cutting "a beat"
  orphaned the antecedent of "for that beat" later in the sentence. `:7` also
  measured as the weaker use, a near-twin of `fed:73`. Detail in
  `audits/line-edit/echo-rulings.md` #20.
- `:21` — Sinatra gloss trimmed to the identifying stroke ("the one where he
  calls it witchcraft"): the cut clauses stated the book's own argument in
  the narrator's voice. gpt-5.6-sol called it "a little pointed";
  claude-fable-5 praised the same span, but its reading requires attributing
  the line to Randi, and it is narration in a paragraph Vee is not thinking
  in.
- `:25` — cut "The room was built so that you could." claude-fable-5:
  "tips the author's hand a half-inch." The preceding sentence is
  atmosphere; this one asserts the enclosure was *designed* to produce
  confession, in the chapter where exactly that happens in that booth.
- `:59` — cut "So she did what she did." Bare instance of the
  did-the-thing-she-did construction (5× in chapter), and redundant with
  "fast, bright, heading it off" three words later.
- `:67`, `:82` — attention-as-lamp thinned from four in-chapter uses to two
  (see echo-rulings #18). Casualty noted: `:67`'s "aimed" was the sharpest
  word in the set; the trim-instead form ("the beam came back on, aimed")
  was offered and declined.
- `:71` — cut "She could hear how good it sounded, how clean, a lovely thing
  happening to a girl over lunch." One of four Vee-hears-her-own-voice
  instances (`:71a`, `:71b`, `:90`, `:126`) whose progression — perform →
  admire the performance → lose it → gone — was reading as repetition
  because three shared near-identical grammar. `:71b` was the only one not
  at a turn. The cut left two speeches butted together; the two were merged
  and a beat added inside the line: **"It's —" Vee looked down, and back up.
  "It's kind of the most romantic thing anyone's ever done for me."**
  (Author's gesture. An eyes-down delivery was considered and rejected —
  Vee is not ashamed of the romance; the shame in this chapter is the
  measuring. The return is what makes it shy-pleased rather than
  confessional, and hanging it inside the utterance makes the rise
  concurrent with the line.)
- `:73` — cut "It was, Vee thought, the nicest part of Randi, this. The way
  she made you feel like the sort of girl who got asked things and had
  answers worth hearing." The eye-tracking already showed it, and the
  sentences pre-approve Randi one line before the chapter starts showing
  what the attention is for. "Nobody else listened like that." is the true
  close.

## Left standing — do not re-litigate

- **The wine arithmetic at `:37` and `:158` — a designed bookend, not a
  repetition (finding 11 withdrawn).** `:37` is Vee pricing Randi's Rombauer
  *before ordering*: the comparison is projected ("everything she **was
  going to allow herself** to order"). `:158` is the same figure closing with
  both terms changed — what she actually ate, against a glass Randi bought —
  delivered as the card goes down. Nor is "She did not do the arithmetic out
  loud" undercut by the narration: the narration *is* the silent arithmetic,
  and doing it in her head and not at the table is the beat.
- **`:146` "and her secret was still half out of her with nowhere to go."**
  claude-opus-4-8 read the passage as over-insuring the door-close image.
  The triptych ("It was gentle. It was kind. It was a door closing very
  softly.") is untouched, and "the laugh did not come… a clean silence" is a
  broken pattern the reader can feel against the whole run of coffee-shop
  laughs. The surviving clause is the only thing keeping the paragraph in
  Vee's body; the alternatives (cut it, or cut "there was instead a clean
  silence") were offered and declined.
- **"the way" ×13 — measured and cleared.** 2.5 per 1k words against a
  **1.6 per 1k** mean across the 60 drafted chapters; high-normal, not an
  outlier (`toenails` 6.2, `peekaboo` 4.5, `fed` 4.0). The real cluster is
  the second-person instructive simile ("the way you X") at `:31`, `:33`,
  `:78`, `:80`, `:90`, `:96`, `:100` — which is the chapter's *subject*: the
  narrator instructs the reader in how things are done while Randi instructs
  Vee, and the two converge at `:96`, "it's just how it's done." `:31`/`:33`
  are a designed pair (Vee reads the right side, Randi the left). Measure
  before re-raising.
- **`:172` "a small drawing-back, the barest pause… a little more"** — three
  miniaturizers in one chain, kept. Not one measurement three times:
  spatial, temporal, pressure. The smallness is the content — the second
  press works by being almost undetectable, which is what keeps it
  deniable. Chapter has only one "a small" (book-wide: 60 across 26
  chapters).
- **The did-the-thing-she-did construction at `:11`, `:31`, `:71`, `:73`** —
  kept (only `:59` cut). The three that get unpacked are a colon, not a
  shrug; `:11` ("set the thought where she set those thoughts") is a
  location figure, not a habit-label.

## Linter acks (author sign-off 2026-08-06)

`style/style-allow.toml`, 19 hits suppressed → chapter now 0 error, 0 warn.

- `register-verb` `:17` (`#f2746fb701c5`) — negated and doubly hedged
  ("appeared not to", "or if she did"); renders Vee's inability to read
  Randi, not Randi as collector.
- `register-verb` `:27` (`#5628364f57a8`) — Vee, not Pace/Randi; the
  look → catch → launder sequence is body-before-mind and is the beat.
- `filter-verbs` `:88` (`#7358ef520622`) — the perceiving *is* the thing:
  Vee discovering her own want mid-sentence, hinging into "The wanting got
  there before the plan did."
- `filter-verbs` `:71`, `:90` (`#6f2e4e5236ad`, `#8c8e551738bb`) — the two
  surviving self-hearings, each at a turn.
- `the-way` ×13 — the instructive-simile ruling above.

## Tooling change made during this pass

`style/style-rules.toml`: **`register-verb` and `clock-verb` rewritten** from
a one-word negative lookbehind to positive verb detection. The old patterns
caught "the register" but not "the warm low register": 14 of 28 `register`
hits and 4 of 10 `clock` hits were nouns. The fix also closes a gap, catching
two real verb uses both rules previously missed —
`ignition-scalding:87` ("He watched her **register** that his yes had come
from…") and `the-bench:29` ("he had watched her **clock** them the first
night"). **Both are live findings in chapters already marked `reviewed`** and
want a look or an explicit ack. Existing acks survived the pattern change
(`practice-room` "barely clocked it", `dear:43`).

## Diptych draft — 2026-10-23

Author requested the structural-review proposal be drafted. Turned Up is preserved verbatim as the Saturday movement; Sunday follows after a scene break and “The next day” cue. Title How It’s Done retained. Sunday’s magazine wish, unaffordability and Pace finding the silk are retained in one narrated sentence, preserving Randi’s receipt. The opening speech is shortened to “He’s making me a dress. For the induction. Burgundy silk, the real thing.” Vee’s self-conscious performance, shy-pleased gesture, and romantic declaration remain. Warm-house account, jealousy tell, bra normalization, cold/hot exchange, interrupted secret, money bookends, return drive, first kiss, and aftermath remain unchanged. No change in either confidante’s relative receipt. Prior praise check on the provenance setup found no direct praise; structural review identified an existing capture-reader complaint at this re-entry. No cuts made to protected positives.

Authoring context loaded at the entry slot turned-up: chapter 17, Opus 5.5 checkpoint 10 plus complete raw chapters 11–16. Required checkpoint 10 minted through the subscription lane with the author’s existing permission. Later reader gates and existing reviews remain unchanged pending assessment.

### Draft verification

Saturday clean prose compared exactly with the source backup. Sunday clean-prose diff contains only the next-day cue and one account-paragraph replacement. Combined body: 6,984 → 6,949 whitespace words. Lore continuity check confirms source receipt preserved through the narrated provenance summary, no broken callbacks, and all protected Cassie content intact. Style: zero errors, 43 ASK hits (1 warning, 42 informational) surfaced without fixes or acknowledgements; 32 existing suppressions survive. Echo harvest: no candidates. Orphan check: no flags. Three ruling-anchor flags refer to pre-existing room/glass/arithmetic wording; neither merge edit removes those lines. The first subscription fact-audit run flagged Cassie’s “living room” for the sun porch, already expressly left standing as comic compression in meta-triage-turned-up.md; not changed. Final subscription audit on the current draft found no factual contradictions; it treated the “living room” line as compatible shorthand. No cold reads or capture runs launched in this drafting pass.

## Grounded cold-read panel — 2026-10-23

Author requested minting whatever was needed and cold reads of this diptych, then confirmed OpenRouter funds. Six runnable active readers completed: claude-opus-4-8, claude-opus-5, gpt-5.6-sol, glm-5.3, claude-opus-5-5, gemini-4-argon. Reads use native checkpoint 10 plus raw chapters 11–16 and the merged chapter at position 17. Refreshed chapter-10 checkpoints for Opus 4.8, Opus 5, Sol and GLM, and minted Gemini’s missing checkpoint; the already-current Opus 5.5 checkpoint from authoring prep was retained. All six have current source fingerprint 09caee3a8d72e72e7e0924d4aa8af3ff98395ee37948cad6d58290bd586ca7db and all eight required sections. The extractor validated complete stopping output. Legacy checkpoint_qa recognized four of these model ids and returned no rerun candidates; it did not recognize Opus 5.5 or Gemini, so no six-model QA-battery claim is made.

DeepSeek did not run: ensemble:core requires GPT-5.5’s stale source checkpoint, while GPT-5.5 is retired and unavailable on subscription. No retired model was launched and no donor policy changed. This is six completed reads of seven active configured readers, not a full seven-model completion.

### Reception

All six value the Cassie movement, including its comedy, emotional safety and knee-touch. Opus 5 calls the dorm scene earned line for line; GLM calls it potentially its favorite scene so far; Gemini explicitly says the two halves balance and illuminate each other. All six describe chapter-to-chapter momentum as building. Opus 5.5 alone explicitly complains that Cassie’s account repeats the fitting; even that reader says the comedy mostly justifies it. Sol, Opus 4.8 and Opus 5 register the change into Randi’s scene as forward movement. These are current-run reactions, not a controlled before/after comparison.

Heat/Romance: Opus 4.8 2/2; Opus 5 2/2; Sol 3/2; GLM 2/2; Opus 5.5 2/2; Gemini 2/2.

Convergent mild friction: Sunday’s setup length (Opus 5.5 car/restaurant, GLM drive); the left-hip line’s calibration or explanation (Sol and GLM both qualify their reservations, Opus 5 questions the explanatory gloss). Singletons: Opus 4.8 finds some class-conscious interior explanation slightly told; Opus 5 questions the explicit kinder-reading explanation; Opus 5.5 calls Sinatra pointed. Gemini reports no pacing waste. Existing protected money bookends remain protected. No prose revised from these reviews.

Reader interpretations are not canon. In particular, Gemini claims Swim Lanes withheld the fitting from Randi, although that scene precedes the fitting; its useful reaction to the paired chapter does not validate that temporal claim. Other readers treat Randi’s invented-man story or motives as more certain than the page establishes; those remain readings.

### Paid usage and execution

GLM checkpoint: 44,410 input / 11,155 output, including 4,039 reasoning; read: 41,033 input / 1,680 output, finish stop. Gemini checkpoint: 45,558 input / 20,832 output, including 11,292 reasoning; read: 44,431 input / 2,436 output, finish stop. Read reasoning breakdowns and exact provider costs were not returned in the harness console. Estimated combined mint/read cost at configured rates: approximately $0.52; reasoning is not added twice. One Gemini checkpoint request met a transient OpenRouter credit-verification 429 and succeeded after retry. Initial unqualified paid-model CLI aliases were rejected by Codex before any artifact was written; provider-qualified invocations ran through OpenRouter. No balance shortage was reported.

All reader-written reactions remain verbatim. Later cold reads, capture gates and checkpoints beyond the needed chapter-10 native memories remain untouched; no renumbering performed. Chronology view refreshed after recording review status.

## Draft explanation reductions — 2026-10-23

After committing and pushing the reviewed diptych as ba1e2b18, the author requested drafted changes to reduce over-calibration or explanation. Two small, uncommitted reductions: (1) “which meant nothing at all and landed like a benediction” becomes “which landed like a benediction”; (2) the older-friend gloss after “happy for her” and the second certainty tag “That was the look” are removed. “That had to be it” and Vee’s settling remain. No new action or motive is supplied.

Praise/complaint balance: the left-hip passage has positive uptake from Opus 4.8, GLM and Sol versus Opus 5’s explicit over-explanation complaint. Therefore the benediction and Vee’s bodily/emotional reception stay; only the assertion that the line means nothing is cut. Opus 5 also praises Vee reaching for the kinder interpretation while questioning its explicit elaboration. That act of self-persuasion, the jealous tell, and the initial fear remain; the analogy spelling out the kind expression is the cut. Existing six cold reads describe the committed pre-reduction draft. No renumbering or fresh reader runs are part of this edit.

Verification of the explanation draft: 22 words removed, two prose hunks only. Lore continuity check found no changed receipt, chronology, callbacks or protected Cassie content. Style has zero errors; all 43 ASK hits left standing, including the re-armed warm hit in the edited left-hip sentence. Orphan and echo checks found no candidates. Ruling anchors add the expected now-cut “meant nothing” quotation to three pre-existing historical flags. Subscription fact audit on prose hash 210dc9a4d252 found no factual contradictions. Six current cold reads remain the pre-reduction assessment; no new reader calls made.

## Explanation-revision reread — 2026-10-23

Author requested readers on the 22-word reduction after questioning whether the criticisms had cross-family support. Reran the same six available active readers blind on the revised prose, using byte-identical checkpoint memories to the preceding wave (all six SHA-256 hashes verified). No minting or DeepSeek run; its retired-source dependency remains blocked. Prior responses are preserved in git at ba1e2b18; all current reaction files contain the new responses verbatim. No prose changed during this reread.

### Comparative reception

No reader in this wave objects to the left-hip passage. Sol and GLM, which previously had qualified reservations about its calibration, both remain strongly engaged and praise the guided questioning without repeating that reservation. The benediction and Vee’s yielding still land. This is compatible with keeping the small cut, not proof that the five deleted words caused the difference.

Opus 5 still finds the broader double-reading of Randi’s tightness (“she thinks I’m awful” / “maybe she’s moved”) a shade over-narrated. The older-friend gloss cut does not eliminate that reader’s larger concern. None of Sol, GLM or Gemini raises it; no cross-family grounds for extending the cut. Vee’s intentional kinder interpretation remains legible.

All six continue to value Cassie’s warmth and the two-movement progression; all describe chapter-to-chapter momentum as building. Gemini reports no friction and calls the two-act structure excellent. Opus 4.8 now praises the unchanged class detail as unshowy, where the previous run found it slightly told; this demonstrates ordinary response variation. Opus 5.5 softens its unchanged setup/repetition reservation to “lingers but works” and new pressure rather than echo. These unedited-passage changes must not be credited to the 22-word reduction.

New singleton reservations: Sol revisits the already-settled not-gay joke (stands under Turned Up triage); GLM thinks the unchanged check moment sits a half-beat long; Opus 4.8 qualifies the overdue-reserve quip as polished but in character; Opus 5.5 briefly blurs the seventeen-day/Sunday timing. No changes made from these remarks.

Heat/Romance: Opus 4.8 3/2 (previous 2/2); Opus 5 2/2; Sol 2/2 (previous 3/2); GLM 3/2 (previous 2/2); Opus 5.5 2/2; Gemini 2/2. The rating movement is mixed and not evidence of an erotic-charge gain from the tiny edit.

Assessment: revised text holds across families with no apparent loss of the praised material. Retain the modest draft reduction for author review; do not pursue the remaining Opus-only explanation complaint without author direction. The wave does not establish a measurable improvement over the original.

### Paid run record

GLM: 41,009 input / 1,830 output, finish stop. Gemini: 44,407 input / 2,405 output, finish stop. Read reasoning breakdown and exact provider cost not returned in the harness console. Combined estimate at configured rates: approximately $0.15. No paid checkpoint calls needed. Four subscription reads also completed. No further edits, commits, gate renumbering or later-reader reruns performed.

### Protected positives — arbitrary praise restored (author ruling, 2026-10-23)

Restore “meant nothing at all and” in the left-hip sentence. The author identifies this as Vee blooming under Randi’s warmth about her experience despite the praise itself being arbitrary: not the factual content but how Randi says it. It renders Vee’s reception rather than explaining Randi’s technique. Preserve the distinction between the meaningless claim and its real emotional effect. This supersedes the provisional recommendation to retain that five-word cut. The separate line-274 reduction remains under consideration.

Restoration verification: no style errors; 43 ASK hits remain unchanged and unacknowledged. Orphan check clean; ruling anchors return to the three historical flags. Subscription fact audit on a730be916951 flags former ledger chapter numbers 18/19 against the merged chapter 17; these are merge/renumbering artifacts, not changes to the story events. The raw audit is retained. No new prose cuts applied during the candidate search. The remaining prose diff from ba1e2b18 is solely the 17-word line-274 reduction; the six most recent reactions describe the preceding 22-word variant.

### Author-approved after-explanation cuts — 2026-10-23

Applied the two candidates on the author’s “apply”: removed “which was its own kind of statement” after Randi pulls out without checking readiness, and removed the narration describing Vee’s evasive words after the stammer ending “so—”. The action and spoken evasion now stand without their explanatory tails. Earlier voice/posture changes remain; arbitrary-praise phrase remains restored. Praise check found no direct praise or complaint for either candidate; these were editorial suggestions, not a panel demand. No other prose changed in this step.

Verification after the two approved cuts: no style errors; 44 ASK hits (2 warnings, 42 informational), with the retained “the way you lean to give up a secret” re-armed by the sentence edit. No ASK hit changed or acknowledged. Orphan and echo checks clean; three historical ruling-anchor flags remain. Subscription fact audit at 0738735086d3 repeats only the already-settled Cassie “living room” shorthand for the sun porch; left standing under the original Turned Up ruling. Local chronology view refreshed. No further reader calls or renumbering.

## Reread after restoration and two approved cuts — 2026-10-23

Author requested the same six readers on current prose 0738735086d3: restored arbitrary-praise wording, retained line-274 reduction, removed statement label at :207 and post-stammer explanation at :284. All six completed with the same byte-identical chapter-10 native memories as the previous wave. Full structured fields and current memory range verified. No minting, new prose edits, renumbering or later-reader runs.

All six describe chapter-to-chapter movement as building and praise the Cassie/Randi contrast. No confusion or lost beat is reported from the two new cuts. Gemini reports no friction and calls the two-act structure masterful; GLM says the chapter earns its length completely and nothing dragged; Sol also says nothing dragged. This supports retaining the current draft, with no causal claim that the small deletions produced shifts in response.

The author-restored arbitrary-praise distinction lands explicitly for GLM: its motifs entry calls the left-hip sentence “it means nothing and lands like a benediction — the purest example of Randi’s method.” Opus 4.8 likewise describes meaningless praise landing as benediction. Sol has a qualified hesitation about how readily Vee accepts the praise, then says the near-trance is convincing enough to buy it. That does not reopen the author’s restoration ruling.

Opus 5 again questions the broader charitable reinterpretation paragraph at :274. The complaint remains unconfirmed by the other families. Other Opus reservations concern unchanged material: Opus 4.8 questions “a thing spent rather than handed around” and briefly qualifies the long verbal descent; Opus 5.5 questions setup length, the warm/cold exchange, gay joke and Sinatra cue. Existing settled rulings remain in force. No new cut proposed from these singleton/within-family reservations.

Heat/Romance: Opus 4.8 2/2; Opus 5 2/2; Opus 5.5 2/2; Sol 3/2; GLM 2/3; Gemini 2/2. Ratings fluctuate in both directions against the preceding wave; do not use them as evidence of an edit effect.

GLM’s first response lacked required structured fields; the harness rejected it and did not write a new reaction. One fresh blind retry completed validly. Successful paid usage: GLM 40,978 input / 2,257 output, finish stop; Gemini 44,374 input / 2,222 output, finish stop. Read reasoning breakdowns and exact provider costs were not returned in the console. Estimate for those two successful calls at configured rates: about $0.15, excluding any charge for GLM’s rejected attempt (usage unavailable). All reader reactions retained verbatim. Changes and new reviews remain uncommitted.
