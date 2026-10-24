# Triage — Gone (line-audit pass, 2026-08-01)

Source: `audits/line-audit/gone.md`, reviewed with the author.

## Fixed

- **":47 Then her voice dropped half a register, went somewhere low and
  hoarse." (was "Then the tell of it dropped, half a register, went somewhere
  low and hoarse.")** — the original stacked two unanchored "it"s (voice;
  the leaking want) at the exact beat where Randi steps over her own line.
  The "tell" work is done better by :49's interior beat ("wanting something
  out loud in his bed and not able to stop it"), so the word could go.

## Left standing — do not re-litigate

(none — the audit's single finding was fixed. For the record: the shoe-store
retelling's divergences from `scenes/sorority.md` are the *designed*
dual-account embellishment per `meta-note-gone.md` and were correctly not
flagged; ditto the :45 interior brush, the signed-off observation-only
exception.)

---

# Triage — Gone (line-edit pass, 2026-08-07)

Source: `audits/line-edit/gone.md` (13 findings) plus a cold-read enrichment
pass over all five `reviews/cold-read/*/gone.md` reactions, reviewed with the
author item by item. Nine edits applied; four items left standing.

**Context worth keeping.** Three of the five cold readers independently flagged
the same over-explaining zone — the analytical gloss following Randi's register
drop — but every line they quoted ("He knew what he'd heard", "That was the
thing the bright way was built to carry", "before the quiet could go where it
had started to go") had **already been cut before the fifth draft**. That
criticism is answered; do not re-open it against the surviving text.

## Fixed

- **`:59`** — (line edit, cost-vague, 2026-08-11) "A different one, the kind that
  **costs something to hold**. Then something gathered under it" → "A different one,
  the kind that **takes holding**. Then something gathered under it". Book-wide
  `cost-vague` back-sweep (rule + author ruling in `style/style-rules.toml`). The
  recast drops the vague "costs something" AND clears the doubled "something…
  something" in consecutive sentences, while keeping the craft-randi containment
  tell — she holds still (the different stillness, not the loose after-stillness)
  while jealousy + attraction over Vee churn into heat. "takes holding" renders the
  effortful stillness without the idiom.
- **`:7`** — "folded down onto his chest" → "down onto his chest" (the fold
  figure belongs to concealment, not body position; see echo ledger #34).
- **`:7`** — "loose in the way she only went afterward" → "loose as she only
  went afterward" (two "the way"s in the establishing sentence; the
  warm-house one kept — echo ledger #33).
- **`:15`** — "A small breath." → "A breath." (linter `a-small`; the pause is
  needed in front of her most undefended line, the modifier is reflex).
- **`:21`** — "He felt her smiling against his chest" → "He felt her smiling"
  (part of the chest de-densification below).
- **`:43`** — cut a bare "A beat." before "Somebody taught her to be ashamed of
  her body," so the line lands straight off "without heat."
- **`:45`** — "Something in Randi went quiet at that" → "She went quiet at
  that" (fourth "Something…" subject in the chapter *and* fourth instance of
  the book-wide `Something [verb]ed in [X]'s [body part]` frame; echo ledger #32).
- **`:45`** — "settled back onto his chest" → "settled back down."
- **`:49`** — cut "Her, stepping over her own line, of her own accord." (a
  summary of the sentence before it, and "of her own accord" argues *against*
  the sharper "not able to stop it"; the cut also makes "before the thought was
  done" true).
- **`:51`** — cut "What came up in him was the other thing." (a pointer that
  delayed the lamp speech by a beat; it now arrives off the silence).
- **`:59`** — "Then something gathered under it — a readiness, in the faintest
  tightening of her against him." → "Then something gathered under it, the
  faintest tightening of her against him." (the abstraction pre-empted the
  physical evidence; body-before-mind).
- **`:61`** — cut "lighter than the stillness" (the lightness measured twice;
  "a beat too long" is the sharper tell).

The chest count went 8 → 6 via `:21` and `:45`. `:19` (she hides her face) and
`:39` (she turns away from a question she didn't like) both earn theirs, and
thinning the other two restores `:47` — the one place the chest is *pressed*
rather than rested on — as the chapter's hardest physical beat.

## Left standing — do not re-litigate

- **`:47` "showing him with her own body the thing she was describing"** —
  flagged as a caption on the chapter's best physical beat. **Reader evidence
  inverts it:** three of five readers reached for that exact formulation
  unprompted to explain why the beat works (claude-fable-5 quoted the clause
  verbatim; claude-opus-4-8: "the seducer wearing the target"; gpt-5.5: "using
  her own body to show him Vee's hidden body… displaced, triangulated"). The
  action alone shows a woman rubbing against a man; the clause is what makes it
  a woman *wearing another woman*. It is the substitution, not a caption.
- **`:69` "let her set the pace of it"** — flagged as an unintended pun on
  Pace's name in the last sentence. Left standing: two readers hit it and
  neither stumbled, and gpt-5.6-sol converted it to theme ("who really sets
  anyone's pace"). Recorded in echo ledger #35 so a later pass does not
  "fix" it.
- **`:19` "It was so cute. She was *so* embarrassed." / "That was kind of
  hot."** — flagged as three flat assessments where a Randi-specific word
  belongs. **The flatness is the alibi:** "so cute" is the socially safe
  cover, "so embarrassed" restates the safe reading, and the third beat breaks
  through both. Sharpen the first and the third has nothing to break. Two
  readers quoted all three rungs as the chapter's payload —
  claude-opus-4-8 called it "the genuinely creepy beat, the one the *text*
  earned," the one place the book "put real ice in me"; claude-fable-5: "I have
  never once watched her *leak*."
- **The six remaining "chest"s** — after the two cuts, the noun is the
  chapter's resting position by design: she never gets up. Not to be thinned
  further.
- **`:39` "Something crossed her face and was gone" and `:59`'s stillness
  paragraph** — both kept as the *signal* uses of the vague-subject grammar
  once `:45` was recast. `:39` quoted by gpt-5.6-terra; `:59` quoted by four
  of five readers.
- **`:35`'s bare "A beat."** — kept: Randi lands "She's got it *bad*,"
  pauses, then gives away "It's romantic," the thing she does not have, said
  to the man providing it. The pause *is* the tell. (The pre-`6e00792a`
  "It's a little pathetic." / "I love it." is not to be restored: author
  ruling 2026-10-12, after a praise check found only glm quoting it.)

## Linter acks (author sign-off 2026-08-07)

One fix (`:15` "A small breath." → "A breath.") and six acks. Three of the six
were **re-arms of prior author acks** whose fingerprints changed under this
pass's edits (`:7` `the-way`, `:7` `warm`, `:21` `filter-verbs`) — re-acked with
their original rationale carried forward. Newly acked: `:29` `look-at-her`
(physical repositioning to meet his eyes, not the appreciation beat), and both
`there-was-were` info hits (`:27`, Pace reading her from outside is the
chapter's POV method; `:69`, the protected closing cadence).

Chapter clean: 0 active hits, 10 suppressed.

## Addendum — `:67` recast (2026-08-07, same day)

`:67` "His hands slid up to cup the round of her." → **"His hands slid up the
backs of her thighs and cupped the curve of her ass."**

Raised as a book-wide echo ("the round of her"), and **ruled not one** — see
echo ledger #36: three real instances across chapters 18/24/49 is not a density
a reader carries, and the harvester's count of nine was wrong. The recast is on
the sentence's own merits: the phrase was the entire payload of a two-beat
transitional line, it took no weight and made no lift (unlike `famished:73` and
`nothing-underneath:77`, both of which stand), and it failed to locate the
gesture. The new line also lands `:49`'s "stroking slow up the backs of them" —
a stroke begun twenty lines earlier that never arrived — and "cupped → held"
(`:69`) reads as a firm hand relaxing into a steady one, which is him answering
"So soon?" and then getting out of her way.

Constraints observed: no steering (the protected `:69` is "let her set the pace
of it"); "settled back down" was already spent at `:45` this pass; "filled"
avoided as it collides with `famished:73`'s keeper.

## Panel reads on the sixth draft (2026-09-27) — the truce retune

Cold: six models. Capture: 21 lanes through ch27. Records under
`reviews/cold-read/<model>/gone.md` and
`reviews/capture-panel/<model>/dag/<persona>/gate-ch027.md`.

### Left standing

- **The shoe-store retelling read as a lie (opus-5, sol, cold).** Both now have
  {{Sorority}} in their raw window and catch that Randi moved her own clowning
  onto Vee. This is the dual-account design (soft-register divergence, never
  adjudicated); sol's "it made me replay the prior chapter" is the intended
  reread. Do not reconcile the two accounts on the page.
- **"That was kind of hot" (gpt-5.5 · relationship-first flinched; opus-4-8
  cold read it as the desire leak).** The leak-and-rewrap line the scene exists
  for. Stands.
- **The lamp speech "a shade saintly" (glm, singleton).** Its payoff is her
  stillness on the chair; the reader said so in the same breath. Stands.

### Open, not ruled

- **The scaffold (opus-4-8 · relationship-first, CAPTURE 6 at Gone).** Named the
  third run of cooks / eats or doesn't / down the hall / the chill / sleeps
  across {{Swim Lanes}}, {{Portion}}, Gone, and "felt the pattern instead of the
  people for a beat." Single reader; the three nights are built as a triangle
  (left / stayed cold / stayed warm). If varied, vary Gone's last movement, not
  {{Portion}}.

## Line-editor pass (fable-5-1 whole-volume read, 2026-09-30)

- **Fixed — the migrated-sentence gloss shortened.** "It was his sentence. She had kept
  it exactly and handed it back to him in his own words, and he took that…" → "She had
  handed him back exactly his own words, and he took that for what it was, that she had
  come round to it." Line-editor flag (*explains*, 0 of 159 other readers quoted it);
  author's wording.


## Workshop draft — bedroom sequence restored (2026-10-23; author review pending)

Author requested the pre-kitchen bedroom sequence as the base: sustained kiss, breast drag in bed, Pace's praise of Vee, Randi's stillness and renewed sex. Later accepted wording retained, including the short altered shoe-store account, “I get bored of everybody,” “It's romantic,” the dress praise, and the unowned Sade playlist. The quote-back of Pace's position is withdrawn by the author; the draft instead gives Randi a seductive reframing.

New aftermath follows the second encounter: he holds her under the blanket through the chills, roughly fifteen minutes; she asks him to make food, takes his undershirt, tucks herself into the kitchen chair and watches him cook. She discusses sorority business, asks about his dissertation, and asks sweetly for a premature wine top-up. Pace is visibly pleased; she finishes her plate and later sleeps against him under the blanket. The dissertation subject remains unspecified. Food is boneless chicken breasts cut into thin cutlets and sautéed in a little olive oil, with couscous and asparagus (author correction to the workshop draft), replacing the ambiguous raw-breast preparation.

These are workshop prose on disk, not a settled replacement beat sheet. The existing companion note and chronology still describe the sixth-draft kitchen sequence; reconcile them when the author accepts the draft. Existing cold/capture reads assess earlier prose and have not been rerun.

Checks: style zero errors, 16 ASK hits (six warn, ten info), all left unchanged; full output `/tmp/gone-workshop-style.txt`. Continuity prep/pass found no factual or physical conflicts. Orphan-reference check on Gone clean; within-chapter echo harvest zero candidates. Ruling anchors reports two historical changes (“the kind that costs something to hold,” “wanting the floor to take her”), already absent before this revision. Praise check identifies positive responses to the kitchen's silent-chair beat and shed shirt; their precise staging is lost in the authorized bedroom restoration, while her stillness and undershirt intimacy remain. No claim that those responses are complaints.

Subscription fact audit (`gpt-5.6-sol`, prose SHA `91e6d6f7b39d`) raised three chapter-number comparisons against the older ledger: gown showing/shoe shopping at old ch24, and Gone's own disclosures at old ch25. Current chronology and the tool's grounded packet place Sorority before Gone (ch22 then ch23). The cited disclosures are unchanged existing Gone material. These flags concern stale structural numbering, not new draft events; no prose repair made. Raw audit retained verbatim.


## Cold reads — workshop bedroom restoration (2026-10-23)

Six requested readers completed fresh grounded reads: Opus 4.8, Opus 5, Sol, GLM, Opus 5.5, Gemini Argon. Same six as the preceding How It's Done wave; donor DeepSeek not included. All six native ck20 memories reminted first because earlier chapter merges/revisions had staled their sources. All six new checkpoints have eight required headings and identical source fingerprint `f34b6f6b8e855a25f02c791f4edcd243821f7581c77a69d5890c7c95fa7e26e5`; each read used its own native memory plus raw ch21–22. Checkpoint hashes verified unchanged across reads. Reviewed scene file SHA256 `4c115b1ec718df7ff1c54713a9f58a4c5f7239c2b6ef73a9a00fae997b6a4c54` (raw Markdown, not cleaner hash). Reactions preserved verbatim; all structured fields complete; no refusal/incomplete response. Backups of prior reviews/memories in `/tmp/gone-before-workshop-reread/`.

All six Heat 2. Romance 3 from Opus 4.8, Opus 5, Sol and GLM; Romance 2 from Opus 5.5 and Gemini. All six find the domestic aftermath earns its length; none complains about repeated sex or concealment of the second encounter. Cross-family positives: she asks for food, finishes her plate, wears his undershirt, receives warmth and stays; the dissertation exchange pleases Pace and adds intimacy; the premature wine request registers. Sol explicitly connects her listening to what both admire in Vee. Gemini explicitly considers her performing Vee; that is a reader interpretation, not narrated motive. Opus 5 and Opus 5.5 leave the wine request's warmth/practice unresolved.

Friction remains dispersed rather than convergent: Opus 5.5 alone finds attribution tangled at “And she talks about you” / “The whole hour. Pace this, Pace that,” and the transition from “God, you two” to “You do nice work” abrupt; its yesterday/Saturday timing question concerns existing material. GLM alone calls the proof/knowing-but-unable-to-show metaphor a possible authorial wink, then lets it pass. Sol's rescuing-role unease concerns the existing shame dialogue and the concealed arrangement, not a new draft defect. No prose changed from this panel.

Interpretive/recall cautions: Gemini calls the night Sunday although chronology places it Monday, and says Pace never notices the stillness despite his observing it. GLM's motif block says Randi asks for more food; the draft has her decline seconds. Sol calls blue toenails a first sighting despite earlier appearances. These are not canon findings. Several reactions retell emotional beats out of order; assess them against the actual scene. The older reviews also cover superseded wordings and stale memories, so this is not a controlled before/after trial.

Paid successful calls, author-authorized: GLM ck20 84,211 input / 16,890 output (10,809 reasoning included), read 21,387 / 1,234; Gemini ck20 86,518 / 27,814 (11,241 reasoning included), read 32,947 / 2,379. Both paid reads finished stop; both mints complete. Subscription lanes for the three Opus models and Sol.


### Author correction — conference interest replaces proof discussion (2026-10-23)

The author rejected the research conversation despite reader praise: dissertation-level mathematics is too specialized for Randi to follow in this short kitchen exchange, and neither her questions nor Pace's volunteering the proof fit the characters. Preserve the attention and his pleasure, not the technical compatibility. Replaced with her asking how his presentation in Chicago went, following up on a researcher staying afterward, and asking whether he was nervous. His professional recognition and her interest carry the warmth. The premature wine request and meal remain.

Location checked against `famished.md:3` and chronology's Famished entry: three-day University of Chicago trip before Friday Oct 9, the most recent conference before Gone (Monday Oct 19). Berkeley Oct 28 and the later Chicago trip are still future. The presentation and its reception are new workshop details authorized by this revision, not facts previously established in Famished. No exact mathematical topic added.

Praise balance: all six workshop readers valued her attention and/or the intellectual exchange; Sol and Opus 5 especially praised the resulting intimacy. GLM alone felt the proof's knowing/showing distinction might be an authorial wink. The replacement is an authorial characterization/plausibility correction, not a panel-consensus cut. Those six reviews now assess the prior proof version; retain their reactions verbatim and mark their scope here. No fresh cold reads launched.

Checks: continuity pass clean; style zero errors, 14 ASK hits (six warn, eight info), left unchanged. Orphan check clean; echo harvest zero candidates. Ruling-anchor flags remain historical quotations/duplicate records, not new losses from this exchange.

Subscription fact audit repeated on conference revision (prose SHA `051657cc41bf`): only flag is the older ledger's Gone ch25 versus current ch23. Current ordering remains Sorority then Gone; existing disclosures are unchanged. No new conference, room, age, garment, or presence conflict flagged. No prose change made from that bookkeeping flag.


### Author refinement — Pace volunteers his nerves (2026-10-23)

Applied the author's exchange: Randi asks how the Chicago presentation went; Pace says it started rough because his grandsupervisor was there and he was nervous. She asks about the term; he explains that the man supervised his supervisor and more or less invented his research area. She asks whether it turned out okay; he says he forgot to be nervous as he got into presenting. Removed her later explicit question about nerves and the earlier invented attendee-follow-up anecdote. Wine request follows his account; wrist touch retained. No name, exact research topic, or institution added for the grandsupervisor. Informal term checked against published academic usage; workshop addition authorized by author.


### Author ruling — opening temporal contrast (2026-10-24)

Changed the opening to “Tonight, she had stayed down.” Removed the lamp-comparison sentence and resolved the associated inline AI comment. The contrast is with Portion's immediate withdrawal and turned back; the following paragraph's hand in her hair answers his withheld touch there. No replacement gesture or explanatory gloss added. Prior reader praise for his receiving her closeness was considered; the physical closeness remains.


### Author ruling — urgency after sex (2026-10-24)

Replaced the quiet wanting shared by both with “the urgency had gone out of him.” Desire remains; immediate pressure subsides. Kept the statement within Pace's experience and cut the repeated letting-it-stay-quiet clause. Resolved only the associated inline AI comment.


### Author ruling — blanket contact (2026-10-24)

Cut the feet-tucking movement from the first shiver/blanket passage and resolved its inline physiology comment. The blanket covers her back and she stays against him; no physiological explanation added.


### Author ruling — Randi brings up Vee (2026-10-24)

Replaced Pace's yesterday/Saturday prompt with Randi's “That redhead is something,” spoken against his chest. She introduces Vee while receiving his closeness. “Our redhead” was considered and declined because it would emphasize a joint claim. Resolved only the corresponding AI comment; the following laugh/transition comments remain for workshop.


### Author ruling — smile, laugh, wanting, admission (2026-10-24)

Applied the workshopped shoe-story transitions: Pace feels her initial smile; her laugh begins at the bigfoot action rather than before the story. After “That was kind of hot,” she squirms against him, then lies still before admitting Vee got past her. Removed the extra quieter-transition gloss. The squirm carries arousal; the stillness permits the more exposed admission without explaining either. Resolved the two associated AI comments; later unworkshopped comments remain. The author approved keeping the felt-smile line after its style warning was surfaced. No style suppression recorded.


### Workshop replacement — Vee's presence, not listener role (2026-10-24)

Author clarified that Randi listens to Vee and Pace listens to both; Vee's appeal here is her warm, electric, lush, unselfconscious presence. With Vee, Randi gets unperformed happiness outside sorority cruelty, and secretly envies her bodily freedom. Read Sorority, Standards and The Pointing Game in full for the contrast.

Replaced the listener-praise paragraph with a draft in which Randi keeps thinking of things to tell Vee just to hear her laugh, even immediately after dropping her off; her attention slips toward Vee's whole-body laugh, thrown-back head and hair, ending in “God, she's lovely.” Existing “She got past me” admission retained. No narrated explanation of envy, imitation, social contrast or motive. This passage remains a workshop draft for author assessment. Praise check reviewed: earlier reader praise for Vee listening does not override the author's role correction; no claim of a consensus complaint. Continuity pass found no conflicts; style zero errors, eleven ASK flags unchanged; orphan check clean and echo harvest zero candidates. Earlier cold reads now assess superseded prose. No new model-backed readers/audit launched for this incremental workshop passage.


### Author refinement — “She's so free” (2026-10-24)

The praise now opens “I can't help but laugh with her. She's so free.” The author emphasized Randi's social intelligence and sustained preoccupation: she can recognize Vee's freedom and the absence of performance. “Free” carries what she envies and desires, while remaining her perception rather than a narrator's claim that Vee has no shame. Head-back/hair detail and the tender closing remain.


### Author ruling — Pace's imagined laughter (2026-10-24)

Inserted the approved interior beat after “God, she's lovely”: he imagines the women laughing together, then the identical picture with both naked, still laughing. No move to bed, no insertion of himself into the picture. The author wanted his appetite present alongside his tenderness; the imagined happiness remains unchanged.


### Author ruling — Randi owns the report (2026-10-24)

Joined “And she talks about you” to Randi's following report, removing its attribution to Pace. Retained “And.” The examples concern Vee talking about Pace; this resolves the speaker/referent mismatch flagged earlier by Opus 5.5.


### Author approval — first-date exchange and bracelet touch (2026-10-24)

Applied the workshopped first-date recollection: Randi says she did not let Pace take his time, knew he was different, and would not wait; he kisses her palm. The nice-work/dress joke pivots back to Vee. Resolved the associated AI comment. After the dress joke, her fingers find the white-gold bracelet she always wears; “Quieter” follows immediately before her praise. Reader uncertainty about whether Pace gave her the bracelet is intentional; no giver, origin, brand, name or removal mechanism is revealed or implied as fact.


### Author ruling — Pace's lust at the *criminal* beat (2026-10-24)

Replaced “It went through him — not the picture of Vee she'd handed him, but Randi… not able to stop it” and cut “He didn't take up the rest of what she'd set down; that was hers to hold.” The author judged both too pure: the first excluded Vee from his desire, the second interrupted the heat with a judgment of his discretion. New beat: Randi's breasts on him (small, firm) call up the remembered feel of Vee's (full, soft) — remembered, deliberately unplaced — then he imagines Randi doing the same to Vee in his bed, Vee's head going back. The contrast is felt only; no preference is expressed. Cuts weighed against reader praise (31 files on “wanting something out loud,” 7 verbatim on “hers to hold”); the author ruled for appetite over displayed restraint. Follow-up (same day): cut “His hands went to her thighs before the picture was done…”; the beat now pivots to Vee alone in his kitchen in his top sheet, watching him cook (from {{Famished}}), chaining into “You know what she does to a room.” `meta-note-gone.md:55` still carries the superseded wording.


### Author ruling — he takes her in (2026-10-24)

After “So soon?” the line now ends with Pace using his grip on her ass to bring her down onto him, until he is in her, and hearing the air go out of her. Kept “the air go out of her” despite its near-echo of {{Peekaboo}} (“drawing a groan out of him and the air out of her”); the author ruled it stands. Randi still sets the pace in the next paragraph.


### Author ruling — aftermath trims and Randi's hair (2026-10-24)

Cut “Fifteen minutes, perhaps.” (a clock measure in a scene of feeling; the two songs already carry the time). “Are you hungry?” → “You're hungry?” Undershirt beat: she frees her hair from the neck and it falls to the tops of her shoulder blades; the shirt gets its own subject (“The shirt came to the middle of her thighs”). Randi's hair is longer than Vee's (Vee's curl shortens hers); book-wide reconciliation is open as `meta-todo-open-questions.md` #51.
