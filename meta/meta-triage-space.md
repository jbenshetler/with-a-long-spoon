# Triage — Space (second-statement pass, 2026-10-10)

First triage document for this chapter. Evidence base: the **seven grounded cold
readers** on disk (`claude-fable-5`, `claude-opus-4-8`, `claude-opus-5`,
`glm-5.3`, `gpt-5.5`, `gpt-5.6-sol`, `kimi-k3`) and the **14-lane capture panel**
(seven models × `romance-graduate` / `fsog-refugee`), plus an audit of the
Pace/Randi two-handers for the **second-statement defect** — the page stating
once what it has already rendered.

**The instrument readings, for the record.** Cold: **Heat 3 in all seven lanes**;
Romance 1.71 (two lanes at 1, five at 2). Capture: **zero STOPs, CAPTURE 7–10,
mean 8.6.** This is one of the chapter-level high-water marks in the book, and
nothing below was raised against a low score.

**Why these sites survived to 2026-10-10.** The `claude-fable-5-1` line-editor
volume pass covers chapters 1–27 and **stops before this one**. The chapter had
never had a line-level read.

## Fixed this pass

Five sites, 50 words; 2,473 → 2,423. The operative test, carried from
{{The Pointing Game}}'s appetite pass (2026-10-09): the reading earns its place
when it **exposes** Pace, and robs the reader when it only **restates**.

- **`:25` — "pleased" stated three more times after the page showed it.** Cut
  *"She was pleased with him about it, and pleased to be here, and it was all
  over her;"* and *"It was there, and"*. The surviving clause — *"she had never
  once come through that door pleased and let it show like this"* — is the one
  **three readers quoted verbatim** (`claude-fable-5`: "the page says outright
  she's never done that"; `claude-opus-5`; `kimi-k3`). The cut removed the
  statements nobody quoted and kept the deviation, which is the beat.
- **`:31` — the same non-thought twice.** *"He did not think to change it and it
  did not occur to him that he might."* → *"and it did not occur to him to change
  it."* **See the breach note below** — an intermediate version named the frame
  and was reverted.
- **`:49` — the third graded-motive statement.** Cut *"He was glad she had gone
  to Randi."*, which flatly restated *"He was relieved there had been somewhere
  for her to go"* two clauses earlier. **The stronger reason, found in the
  reviews:** *"I'm glad it was you"* arrives as **dialogue** eight lines later at
  `:57`, and two readers name that line as a top beat (`kimi-k3`: "landed on me
  like a blow"; `gpt-5.6-sol` cites it as the Romance rationale). The narration
  was pre-stating in Pace's interior what the dialogue delivers as speech. The
  gladness now arrives only once, and as speech.
- **`:67` — the bench memory's tail.** *"That she had got so far, and that he had
  been the one to take her, was a thing he kept. It came up in him now, and he
  was harder for it."* → one sentence, the two that-clauses becoming the subject:
  *"That she had got so far, and that he had been the one to take her there, came
  up in him now, and he was harder for it."* Author's objection to the plain cut
  was correct and is recorded: dropping the clause lost both the agency ("he had
  been the one") and the antecedent of "It". **`claude-fable-5-1`'s
  romance-graduate had flagged this paragraph** as "the one paragraph that
  stepped back to tell me about the bench" — and forgave it, because it delivered
  a fact she had been "begging for." The step-back stands; its tail is shorter.
- **`:83` — the four-part tail.** Cut *"and he could feel both of them in her,
  and it fired him, and he let it"*, replaced with a discrimination:
  *"and the taking was the part that fired him."* The give-and-take clause is
  retained because **three readers used it** (`gpt-5.6-sol`: "is precisely the
  charge"; `claude-opus-5`; `claude-opus-4-8`). The replacement is on-model per
  `meta-arch-pace.md` ("aroused by watching a woman break her own rules of her
  own free will… The line is hers; the stepping is hers") — she framed the
  telling as a gift for him, and the taking is her stepping over her own framing.

**Breach and repair, recorded.** An intermediate `:31` was *"It did not occur to
him to change it for her."* The assistant proposed **"for her"** on the strength
of the chronology's *"her music on"* at {{Swim Lanes}} without re-checking
`meta-note-music-thread.md`, which carries two guards it violates: *"Never
spotlight Pace choosing per woman; that makes him a puppeteer"* and *"Intent
stays ambiguous, lean intuitive… it reads as temperament, not strategy. Never
resolve whether he knows."* The thread doc additionally quotes the **original**
sentence and calls it *"the model rendering of the non-curation guard."*
Reverted the same session. **The guard is the authority on this line; do not
reintroduce a per-woman frame here, in either polarity.**

## Left standing — do not re-litigate

- **"The tit goddess was generous with that girl."** Two readers, the only
  convergent line-level friction in the chapter. `claude-opus-5`: "tipped a
  half-step past Randi's register for me, the only line I heard as written rather
  than said." `claude-fable-5` jolted and **bought it**: "it's Randi's low
  register, the coarseness she only uncrates in that house." The coarseness is
  house-only and that is the point. Stands.
- **"That's what a blonde is for."** `gpt-5.6-sol`, the one line that snagged
  him: "it turns the unnamed woman into a stock function and lets Randi dismiss
  the provocation too neatly." One reader — and the dismissiveness is Randi's,
  not the book's. Stands.
- **The catch-and-set-down beat reading systematic.** `claude-opus-4-8`: *"as if
  the day were his to give, and he set that down beside the rest"* is "a touch
  systematic, the same beat as the untouched bowl in {{Portion}}" — and files it
  himself as "small." Against it, two readers read the same beat as
  load-bearing: `gpt-5.5` ("even he feels the shape of Randi's control") and
  `gpt-5.6-sol` ("he notices something odd in Randi's authority, yet he merely
  sets it aside"). The pattern is the Console architecture — catches every
  signal, assembles none. Stands.
- **The debrief-chapter structure.** `glm-5.3` named "the second 'cold' chapter in
  a row where the plan-side couple takes the bed while Vee, offstage, spends her
  day getting ready." `claude-fable-5-1`'s romance-graduate had pre-committed to
  "one more debrief, not two" and took this one anyway, because "it isn't
  summarizing a scene I was inside, it's *falsifying* it in front of me, and
  that's plot, not recap." Answered by the reader who raised it. Stands.

## Open, not ruled

- **The telling-versus-picture distinction.** `kimi-k3`: *"The narration tells me
  it was Randi's telling that fired him, not the picture; **I don't fully believe
  the distinction, and I don't think the chapter does either.**"* This names
  `:83`'s *"it was not the picture she had given him that did it, or not only; it
  was Randi"* — which **survives this pass**. Note the risk honestly: the `:83`
  edit replaced one assertion about what fired him with a finer one, so the
  paragraph still makes the move kimi disbelieved. The re-read is the test. One
  reader; not acted on.
- **The same construction runs in two chapters.** `:83`'s *"not the picture…; it
  was Randi"* and `gone.md:85`'s *"not the picture of Vee she'd handed him, but
  Randi"* are the same figure doing the same job, four chapters apart. If only
  one should survive, `gone`'s is the tighter instance — but {{Gone}}'s
  over-explaining zone is marked do-not-reopen (`meta-triage-gone.md:31`), so
  this needs an author ruling before either is touched.
- **The third round of the harvest-to-heat move.** `claude-opus-4-8`'s
  romance-graduate: "'There's more, she said' landing me in a third round of the
  same harvest-to-heat move, and I braced for a pattern instead of a turn. **It
  turned.**" Braced-and-released, not a complaint — but it is the same reader and
  the same instrument that produced the open scaffold item at
  `meta-triage-gone.md:166-173`. Read the two together.

## Confirmed positives — protect in any future edit

- **"She made a sound and hoped I didn't hear it. … I heard it."** Quoted by
  **all seven** cold readers as the peak or next to it, and the ALMOST-STOPPED
  line in `glm-5.3`'s fsog-refugee lane. `claude-fable-5`: "I felt that land in
  my own body before my conscience got a vote." `kimi-k3`: "the single most
  intimate thing Vee owns." The most convergent line in the chapter.
- **"and it was not the look you give a table."** Five readers. `claude-fable-5`:
  "That one sentence did more to me than the whole sex scene." Observable plus a
  seven-word figure, with nothing explained after it — **the chapter's model of
  the construal done right**, and the standard the rest of the chapter was
  audited against.
- **"That was not a thing he had decided. It was only what he was."** Four
  readers. `glm-5.3`: "that's the version of Pace I like trusting." `kimi-k3`
  reads it against Randi's prediction to Vee and calls that rightness "the
  scariest thing in the chapter."
- **"Not like that. Not yet. Lie down."** Five readers. `claude-opus-5`: "she
  will come while talking, on top, in charge, delivering — she will not come
  while being given to… the whole shape of her in one gesture."
- **"a voice he had not heard from her before or since"** and **"Three weeks
  in"** — both inside `:67`, the paragraph edited this pass, and both untouched.
  `kimi-k3` on the first: "ached more than anything in the chapter."
  `claude-fable-5` on the second: "re-places chapter one for me." Any future
  trim of that paragraph must leave these.
- **"I had her standing in my room this morning. … In her bra."** The convergent
  ALMOST-STOPPED: four capture lanes across four models, every one attached to a
  CONTINUE at 7–9.

## Instrument notes

- The chapter has **no line-audit or line-edit lane document**; this triage is the
  first ruling record for it. `ruling_anchors.py` therefore has nothing to check
  here yet — it will from now on.
- The close was recast on **2026-10-03** after it was found to reproduce six
  elements of {{Tannin}}'s closing sequence; `meta-note-tannin.md` owns that
  ruling and that close. Not revisited this pass.
