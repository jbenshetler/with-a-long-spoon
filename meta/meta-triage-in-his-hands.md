# Triage — In His Hands (line audit, 2026-08-02)

Sentence-by-sentence consistency/logic audit (`audits/line-audit/in-his-hands.md`).
3 findings: 2 fixed, 1 left standing.

## Fixed

- **Blinds moving glare at night with no light source** (:55) — a day-switch
  was considered and rejected (weeknight slot + class schedule + the lamplit
  fall register). Recast to the lamp: "He crossed to the lamp and tilted the
  shade until the glare slid off her skin" — source explicit, lamp placement
  left to the reader (nightstand lamps would sit at the wrong angle for the
  shot), the cross-adjust-return rhythm kept.
- **"They drank the wine" with only her glass poured** (:69/:81) — now "he
  poured a glass for each of them"; funds :81's shared quiet, matches his
  sparing-glass-while-cooking pattern ({{The New Ordinary}}).

## Left standing — do not re-litigate

- **Unmarked table↔counter drift** (:75–83) — kitchen choreography reads
  loose by nature: being fed tastes off the spoon *is* the move, "her hand on
  the counter" confirms arrival, plating reseats her. Stage directions would
  clutter the scene's most languid stretch.

Also: Cassie not present (Vee/Pace only) — `present:` already correct. Linter
clean after edits.

---

# Triage — In His Hands

*Cold-read feedback pass, 2026-07-29. Panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol (`reviews/_archive/cold-read/*/in-his-hands.md`). Each item: what was flagged, who raised it, verdict.*

## Fixed

- **Cold-sane-thought inventory over-explained** (claude-fable-5, claude-opus-4-8: "over-explains a risk the scene had already dramatized"). Fixed *before* this pass in the approach-A over-insurance trims, commit `e69522f` (2026-07-28): the inventory ("that it was a naked picture of her… ruined the women in them. She knew all of that.") cut; the category ("the cold sane thought any girl had about a picture like this") plus "believing him was the brave part" carry it. The panel read the pre-trim draft — a fresh cold read should re-test the trimmed version.
- **Kitchen sequence read as a full recipe rather than the impression of one** (gpt-5.6-sol: "exhaustive pan chronology" a slight slackening; claude-opus-4-8: "a touch long as pure procedure"; the other two praised it at full length). Fixed this pass, author-directed: the two cooking paragraphs compressed — clock/sequencing logistics cut (pot seeding, "some four minutes," onion-dice scheduling, spatula-ring choreography, the "Chicken stock. The lemon juice." checklist); the pan's sound now does the timekeeping (he turns the breasts by ear, without looking); the smells moved into Vee's body at the table (lemon zest reaching her mid-grate; onion-garlic arriving a minute late, gone sweet and savory; the lemon juice sharp and immediate); stock kept lightly ("Stock after the wine, and then the lemon") as the sauce's backbone; butter finish added ("from bright to silk"). Capers stay at plating only — not doubled in the pan.

## Left standing — do not re-litigate

- **The promise wording, "I'd never share your photograph."** Fable and opus both caught the noun substitution (her *me* → his *photograph*) as possibly load-bearing; both GPT models believed the promise at face value. This is the designed genie-bargain (`meta-note-in-his-hands.md`, Load-bearing mechanics) and the 2/4 detection split is the intended calibration — suspicious readers chill, trusting readers trust, like Vee. Do not clarify, soften, or underline the wording.
- **His re-arousal at the send.** Fable caught the timing without assembling it ("she gets there on her own… or did it?" adjacent read). Per the craft note, the kink shows on the send, never named. Working as designed; leave the timing bare.
- **Photo on her phone / she sends the copy.** Reviewers who noticed read it as tenderness; it is load-bearing mechanics (every copy under her control; the later sharing is her hand). Invisible as intended.
- **Sheri at Thanksgiving.** Panel stayed warm toward Sheri while keeping "two at once" wariness alive — the pity-not-romance defusal plus the planted absorber both landing per `meta-note-in-his-hands.md`. Sheri stays offstage/reported until {{Another Round}}.
- **"I don't go back" (third parents-slam).** All four registered it as sealed and charged, none read con-shadow — matches the "warm-sad, not con-shadow" spec. Cause stays vaulted.

## Not actionable

- The GPT models' long open-question inventories are carry-forward bookkeeping, not criticism.

## Style acks recorded this pass (2026-07-29)

- `unhurried` at the posing beat (`#c2d66ee4e712`) — sanctioned Pace use, load-bearing.
- Four `warm` hits (`#ef161b40658e`, `#b5a2fb73f16d`, `#0111b04e6de1`, `#55e354c87f1c`) — all judged load-bearing warmth.

---

# Triage — In His Hands

*Line edit, 2026-08-10. Report: `audits/line-edit/in-his-hands.md` (19 findings;
9 applied). Panel evidence: 6 cold reads. Items below are settled — do not
re-litigate. Verdicts re-open on a text edit to the passage.*

## Left standing — do not re-litigate

- **`:47` "the wrecked, sated woman" (line edit, 2026-08-10).** Flagged as the
  middle of a triple restatement. It is the antecedent, not a restatement:
  Pace has just said "I like you exactly like this" (`:45`) of *that* woman,
  and this sentence names precisely what she deletes — which is what makes
  `:51`'s "No, not like that" land as him reaching back past her correction.
  Three sentences, three functions: intent, erasure, product.
- **`:47` "composed, arranged" (line edit, 2026-08-10).** Flagged as one
  arrange-word too many against `:49`/`:53`. Kept: she arranges herself, he
  rejects it and arranges her — the verbal rhyme is what makes `:53` an
  overwrite rather than a preference. Two uses, deliberately chimed. (`:53`
  is a paragraph of the action, not a third instance of the word.)
- **`:59` "She looked, she thought, beautiful." (line edit, 2026-08-10).**
  Flagged as the third of three appraisals. It is the only unhedged
  first-person claim on her own beauty in the chapter — a woman built out of
  body-shame saying it plainly — and the next sentence exists to take it away
  from her. Cut the claim and the discount qualifies nothing; both registers
  (he made her able to think it / she can't think it except through him) die
  with it.
- **`:53` "where he wanted her" / "where he wanted them" (line edit,
  2026-08-10).** Flagged as an identical formula twice in one sentence. Cutting
  the second is grammatically unsafe — "moved her legs together" reads as
  closing them, prim against a pinup's line, because "together" stops being
  appositive. A "where he liked them" variant was considered and declined;
  the paragraph is reader-praised by four models as drafted.
- **`:77` "hissed at him" / "hissed at him too" (line edit, 2026-08-10).**
  Flagged as part of a four-instance pan-as-speaker figure. The figure's
  recurrence is an author-directed fix (2026-07-29 pass: the pan's sound was
  *assigned* the timekeeping when clock logistics were cut), and opus-4-8
  praised two of the four instances. The "too" is the joke — the kitchen
  answering him item by item.
- **`:79` "She had used to just eat." (line edit, 2026-08-10).** Flagged as a
  nonstandard construction stumbling in a sentence that wants to be flat. Kept:
  the pluperfect seals that self off as *completed*, which is exactly what the
  next clause claims ("no going back to the other") — the grammar enacts the
  irreversibility. Praised by all six cold readers.
- **`:9`–`:107` seven findings dropped pre-ruling (line edit, 2026-08-10)** —
  #2 (`:17` "Which rather spoiled her theory": action / her pleasure / her
  revised belief are three functions; fable-5 praised the construction), #4a
  (`:19` "No man had ever wanted her body like this one did": kimi-k3 and
  gpt-5.5 both praised it; the comparative grounds the inversion), #5
  (`:19`/`:47` "a girl who had ___": the recurring frame makes `:47` a
  *revision* of `:19`), #11 (`:53` the summarizing clause: it establishes that
  the kissed places are the placed places), #13 (`:53`/`:59` calendar: the
  repetition IS the match between what she wanted and what he made), #19a
  (`:97` "She didn't ask.": reflex → choice → kindness, and the only short flat
  sentence carrying the stop), #19c (`:101` "a man talking about a friend": the
  pity-not-romance defusal, confirmed landing across the panel).

## Load-bearing wording — do not trim

- **`:25` "**Sometimes** I take care of it myself." (author, 2026-08-11).**
  The adverb is **canon, not a hedge.** Without it the sentence reads as a
  complete account of his outlet, which is false — he is sleeping with Randi.
  "Sometimes" makes the answer *true and incomplete*, which is exactly the
  register of "I'd never share your photograph" at `:41`: two technically
  honest evasions in one exchange, the chapter's designed genie-bargain run
  twice. It also sharpens rather than softens the beat kimi-k3 named as "the
  first time his *words*, not his silences, have done the managing" — the
  omission now works alone, with no falsehood to hide behind.

  **Standing instruction to any line edit or copyedit:** this is the exact
  shape those instruments flag as a weak qualifier softening a flat
  declarative. Never propose cutting it, and never accept a proposal to. The
  rationale is invisible from the page, so a reviewer who does not know about
  Randi will read it as a tic.
