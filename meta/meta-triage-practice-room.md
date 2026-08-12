# Triage — The Practice Room (line-audit pass, 2026-08-02)

Source: `audits/line-audit/practice-room.md`, reviewed with the author.
**The "Left standing" section records authorial decisions — do not re-flag
these without new evidence** (a new reader cohort snagging on the same spot,
or an edit that re-opens the passage).

## Fixed

- **":99 "Mine," she said. → "Mine," Randi said.** — new paragraph opening
  with a quote signals a speaker change, and with two women in the room the
  bare "she" could hand the line to Vee for a beat before the ex-husband
  content corrects it.
- **":115 "all afternoon" → "since the morning"** (author's wording) — the
  build starts with the knee at the eleven o'clock lecture, and her morning
  began at Pace's; the phrase now sweeps in the whole day's saturated state,
  not a span the noon–12:45 clock can't hold. "Arrived" also cut in the same
  edit — the sentence runs straight from the fact of it to standing up too
  fast.
- **Chronology :530 "November" → "late-October"** — the Telling housekeeping
  note's reference to this scene's bathroom beat was stale against the
  scene's own entry (Mon Oct 26); the note's predates-the-cabin point is
  unaffected.

## Left standing — do not re-litigate

- **":113 closed-quote/new-paragraph continuation ("And always, toward the
  end, his hand would slip.")** — unmistakably Randi mid-story; Vee's
  contributions have shrunk to a name and stillness, and "Randi's mouth
  curved" confirms within the line. The unencumbered paragraph break is the
  timing of the confession's last card.

---

# Triage — The Practice Room (`practice-room.md`)

Cold-read feedback pass, 2026-07-28. Panel: claude-opus-4-8, gpt-5.5, gpt-5.6-sol
(`reviews/cold-read/*/practice-room.md`). Author-decided verdicts; later review
passes should not re-litigate the "left standing" items unless the flagged
passage has since been edited or a genuinely new failure mode surfaces.

## What the panel confirmed (protect in any future edit)

- The verbal-only erotic escalation ladder ("His hand was wet" → "doing it
  again. Here. Now." → "welcome, very welcome" → the bolt) — all three models
  named it the scene's engine. Do not add contact; the slightness is the point.
- The bathroom refusal, verbatim ("Not here. Not over a story… she would not
  say yes to it") — all three quoted it; sol reads it as the book's sharpest
  arousal-≠-consent statement against the cover tagline.
- The reversal staging (Vee towing Randi; the held hug blamed on tiredness) and
  the held-note ending.
- The title's innocent-in / exact-out turn.

## Fixed this pass

- **Narrator-opacity breach (the pass's payload).** Original line: "She didn't
  hear what she'd agreed to. Randi did. Randi let it sit a second, the way the
  professor let things sit, the small private pleasure of a woman who had laid
  the same soft trap a hundred times." Flagged by gpt-5.6-sol as pressing
  harder than needed; lore-keeper check confirmed it violated the design
  ("keep Randi opaque throughout," `meta-note-practice-room.md`; "never inside
  her… not even in close third," `meta-craft-randi.md`). Note: opus's review
  *praised* these lines ("that line is the whole chapter") while reporting the
  cold arriving on first read ("coldest I've felt toward her") — inadvertent
  proof the reread-only guard had failed. Replaced with the realization moved
  into Vee, mind-then-body, Randi visible only as surface: "A moment late, she
  realized what she'd just agreed to. Randi's smile brightened. It went down
  through her like a swallow of something warm."
- **"pleasant as weather"** (Randi at the practice-room door) — cut the simile
  (now "…Randi said, and that was all…"). Style-rule breach, and semantically
  wrong: weather is proverbially fickle; the beat wants Randi frictionless and
  unshockable. The flat non-reaction is the tell.
- **Style acks** (`style/style-allow.toml`): "barely clocked it" (worn-in kiss
  line stands); "she realized" on the new line 67 (deliberately cognitive
  before the embodiment); "swallow of something warm" (load-bearing warm).

## Left standing — do not re-litigate

- **Stats lecture runs thesis-loud** (opus only: "the one place the machine
  hums audibly"). Left standing. Lone flag — gpt-5.5 explicitly bought it
  ("lands less like authorial neon than Simpson's paradox did, maybe because
  Vee doesn't interpret it") and sol said it "earns its space." The design
  guard ("the stats mirror stays silent… never connected to Vee on the page")
  is honored: Vee copies *never all the way gone* without reading it.
- **Cassie's displacement hurts the reader** (all three felt it). Working as
  designed — the scene's planned structural beat (`meta-note-practice-room.md`:
  the first time Vee initiates the isolation; surface = eagerness, meaning =
  reread-only). The readers' hurt is the intended effect; do not soften.
- **Mouse-story ambiguity** (readers suspect the ex is invented or displaced-
  Pace). Working as designed — the intended inoculation; no reader *concluded*
  mouse=Pace. Do not clarify in either direction.

---

# Triage — The Practice Room (line edit, 2026-08-09)

`/wals-line-edit run`, chapter 30. Source: `audits/line-edit/practice-room.md`.
Fourteen edits applied; the items below were ruled and **left standing** — do
not re-litigate without new evidence.

## Left standing — do not re-litigate

- **`:53` "something in her had gone very still and very interested" — the
  doubled intensifier stands.** The parallelism is load-bearing, not emphasis:
  identical frames *equate* the two adjectives, and that equation is the move —
  *still* is innocuous, *interested* is the predator, and the parallel smuggles
  the second in on the first's passport. Break it and *interested* stands alone
  as a narrator verdict on Randi, the close-third breach this chapter was
  already repaired for on 2026-07-28. **Reader-protected:** gpt-5.6-sol and
  gpt-5.6-terra both quoted the sentence, both reported *"made my body tighten."*
  The doubled *still* (`gone very still` / `a cat goes still`) is the simile
  completing its own word — designed, not repetition. **Acked** (`the-way`
  `#d16282e6f5a8`).
- **`:27` "There was no time to go anywhere" — free indirect, stands.** The
  paragraph is already in reported speech, so this is *Randi's* assessment in
  the narrator's grammar, not narratorial fact. Forty-five minutes is ample; the
  sentence is false as fact and true as Randi. What it renders is **Randi
  manufacturing the constraint** — close the options, declare the emergency,
  then produce the destination two minutes away she had evidently already
  chosen. Flagged as a logic wobble by the line editor; the flag was wrong. Rule
  now recorded book-wide at `meta-plan-satc-tracks.md`, *"Randi's register
  colonizes the narration."* **Acked** (`there-was-were` `#8e2448353630`).
- **`:121` "the proof was there before she wanted to know it" — the abstract
  placeholder stands, and must never be "fixed" into a concrete noun.** Flagged
  as mind-before-body; withdrawn. The placeholder **is the refusal** — naming
  the thing would be acknowledging it, and her shame architecture won't. The
  concrete (*soaked through*) arrives a half-beat later, from outside her, as an
  accusation she did not authorize. Established house idiom: `grace:205`,
  `famished:51`, `we-find-out:107`, `believe-me:57`. Rule now recorded at
  `meta-craft-vivienne.md`, *"The evidentiary register."* Tightened from *"the
  proof of that"* to bare *"the proof"* to sharpen the designed rhyme with
  `grace:205` — same noun, same permission-clause shape, opposite reception
  (Pace looking at it *"like treasure"* vs. Vee convicted by it alone under
  fluorescent light).
- **`:95` "the way you let someone find their feet" — CUT (2026-08-09).** Line
  now reads *"Randi let her hang there a moment, kindly."* Two reasons: it
  rehearsed `:141`'s second-person simile forty-six lines before the payoff,
  and the figure was untrue to the beat — Vee never does find her feet; she
  can't finish the question and Randi supplies the answer herself two lines
  later. The adverb carries the beat alone. (Correction of record: an earlier
  note in this pass wrongly stated the `:95` cut had already removed this
  simile; it had removed a different sentence.)
- **`:141` "She noticed it the way you notice a held note after the song has
  already moved on" — stands, `filter-verbs` and `the-way` hits
  notwithstanding.** The most-cited passage in the chapter across all five cold
  reads (fable-5 and sol quote it verbatim; sol lists the held note as a
  first-sighting motif *and* under Symbolism; kimi-k3 *"The goodbye undid me"*;
  opus-4-8 *"the smallest, saddest thing"*). The `filter-verbs` hit is a false
  positive by design — *noticing* is the subject; the beat is the lag between
  her arms acting and her mind catching up, and body-before-mind is satisfied
  one sentence earlier. Doubled *notice* left in: it makes the simile read as
  her own thought reaching for the comparison. Now the chapter's only
  second-person simile. **Acked** (`the-way` `#b741f0c8170a`, `filter-verbs`
  `#5fa30e9ba3c0`).
- **`:107` "It was humiliating" — stands.** Flagged as abstraction after image;
  kept. This is Randi speaking, and naming it is her *move* — putting a word in
  the room Vee doesn't own yet, same operation as *"Did you deserve it?"* at
  `:63`. `:111` (*"it made me buck"*) only detonates because the word is on the
  table. The redundancy was in the *preceding* clause, cut instead.
- **`:75` "the warm wet weight of his hand"** — not a hit under echo **#5**,
  which polices the identical three-word string *"warm weight of"*; already
  varied, quota retired 2026-08-08. Chapter's core image; kimi-k3 quoted it.
- **`:21` "turned a few degrees"** vs `all-told:43` — flagged, left standing.
  Same stats room, eight chapters apart, both about Cassie; different enough in
  function. Logged so a later harvest does not re-present it.
- **Bonus items cleared.** sol's "stats lecture runs thesis-loud" on current
  text was aimed at `:19`'s *"She did not think about herself at all,"* now cut
  — the earlier lone-flag ruling above stands unchanged. terra's *"almost too
  claustrophobic"* on the bathroom was weighed at `:121` and ruled against
  trimming.

## Applied

| line | change | why |
|---|---|---|
| `:13` | *"reading the back of a cereal box"* → *"reading a course catalog aloud"* | verbatim dupe of `all-told:35`; breaks rotate-the-vehicle (`meta-note-stats-professor.md:25`). Noun-use `catalog-verb` ack `#890c98778a6b` |
| `:19` | cut *"She did not think about herself at all."* | nudge ban; sol read it as announcement |
| `:19` | *"the warmth of it went up through her"* → *"it rose in her"* | reflex `warm` + abstract noun; re-varied to clear the `went…through her` frame shared with `:67`/`:81` |
| `:21` | cut *"sixty people deciding at once that it was over"* | near-verbatim repeat of `dear:7` — nine words, same dismissal, same professor |
| `:25` | cut *"It was a small thing and she didn't notice she'd done it."* | `a-small` tic + nudge pattern; the paragraph enacts the reversal three further ways |
| `:29` | *"felt the color come up her neck"* → *"felt her neck go hot"* | `the color` shared with `:109`; *hot* is the truer POV — she can't see her own neck |
| `:39` | dropped *"the whole bright weight of"* | closes echo **#27** and **#18**'s sub-note; protected lamp intact |
| `:87` | cut *"She didn't say what she herself could see."* | close-third; *"That was all"* does it |
| `:95` | cut *"Then she gave her the end of the sentence…"* | the unfinished question stated three times in three sentences |
| `:95` | cut *"the way you let someone find their feet"* | rehearsed `:141`'s second-person simile 46 lines early; also untrue to the beat — Vee never finds her feet |
| `:107` | cut *"You know what that does to a person, counting your own."* | vaguer of two stacked summaries; Randi compresses as she closes in |
| `:113` | cut *"the whole worldly weight of it in the gesture"* | `the whole ___ weight` frame |
| `:115` | supplied the missing verb — *"…since the morning **arrived**, the actual physical fact of it…"* | verbless middle clause read as a dropped word, not a chosen fragment |
| `:121` | *"the proof of that was there"* → *"the proof was there"* | sharpens the `grace:205` rhyme |
| `:127` | *"she looked up with the whole warm face turning on at once"* → *"she looked up, so pleased to see her that Vee felt it land, warm all through"* | the hunger/warmth misread — below |
| `:131` | *"It came out a beat too fast"* → *"It came out too fast"* | `held-past` family; *beat* also at `:53` |

## The `:127` ruling — Randi's hunger through Vee's POV

Author spec (2026-08-09): *Randi looks up as if at a lover overcome with desire
for her. The smile is real, intense, and has hunger in it. Vee reads it as
warmth because she refuses to see the hunger. The page renders warmth; on reread
the reader perceives Vee's faulty POV.*

This recurs across the SATC track, so the constraints derived here are recorded
book-wide at `meta-plan-satc-tracks.md`, *"Rendering Randi's hunger through
Vee's POV."* Short form: render the percept never the diagnosis; Vee supplies
the label flat and **unhedged**; prefer the label as a bodily effect on Vee over
an adjective on Randi; the datum must be genuinely bivalent; one flag per page
(`:133` already opens the question, so `:127` stays clean data with no wink).

---

# Triage — The Practice Room (anachronism sweep, 2026-08-12)

Raised during the {{All the Time}} line edit; chapter re-opened for one word.

## Fixed

- **`:121` "Under the thin fluorescent light" → "Under the hard white light"** —
  author ruling: fluorescent tubes are an anachronism in the new/renovated
  buildings of a modern, well-funded university; a current-day campus interior
  reads LED. House style is to render the light's *quality*, never the fixture.
  **The designed rhyme with `grace:205` survives** (`meta-craft-vivienne.md:102`
  — same noun *proof*, same clause-shape, opposite reception): the contrast is
  full-light-as-treasure vs. cold-light-as-conviction, and "hard white light"
  keeps the light harsh and institutional.

## Left standing

- **`:135` "the bad fluorescent hum"** — kept. The hum is the sentence's sound
  detail in a clause that is *about* ambient building noise, and LEDs do not
  hum. Ruled a legitimate older/cheaper fixture in that corridor.

See the `fluorescent-site` rule in `style/style-rules.toml` — an info-level
**site check, not a ban** (`rock:127`'s high-school gymnasium and
`under-the-rug:43`'s cheap bright restaurant were both kept for the same
reason).
