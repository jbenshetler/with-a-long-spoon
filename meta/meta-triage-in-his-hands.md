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

*Cold-read feedback pass, 2026-07-29. Panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol (`reviews/cold-read/*/in-his-hands.md`). Each item: what was flagged, who raised it, verdict.*

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
