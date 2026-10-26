# Close-third pass — Famished (ch16)

*2026-10-26 · claude-opus-5-5 · `/wals-close-third` · Vee's POV · nothing applied*

Verdict: very light. The chapter already had its glosses taken out in the
2026-08-07 line edit (`:23`, `:47`, `:53`, `:65`, `:79`). Two candidates are
left, both before the bedroom. From the bedroom on, everything is her body or
her mind at the peak.

Praise tallies are from `tools/praise_check.py --slug famished --text …`, plus
an `rg` of the 15 Famished cold reads and ch16 capture gates for the idea in
other words.

## Proposed

**The kitchen**

1. `:21` — "He'd done all the preparation and stopped." The board is already
   laid out ("garlic minced, onion diced, pepper flakes measured into a bowl
   beside the tin of crushed tomatoes"), and "The pan was dry and clean on the
   burner." The sentence states the conclusion she reaches. It is the same
   kind of sentence as `:23` "He'd opened it before she arrived.", which the
   line edit cut as "restated the inference as flat fact in a paragraph whose
   whole method is showing." Console rule: body before mind, never the
   deduction.
   → "…beside the tin of crushed tomatoes. The pan was dry and clean on the
   burner."
   Tally: no verbatim or fragment hits. Paraphrase: two readers took the
   stopped meal, both in their own words — argon fsog-refugee gate ("left the
   pan cold and dry on the burner. He prepped dinner and *stopped*") and the
   gpt-5.6-sol cold read ("prepared dinner but stopped before cooking"). Argon
   quotes the pan, not the gloss. Note: `:105` "from where he'd stopped" picks
   up "stopped"; it still reads without the antecedent.
2. `:37` — "and this was different from him asking if he could order her
   dinner, and asking if he could make her a dress, and every narrow register
   she'd held herself to since, because it had nowhere to go except forward
   and she did not try to slow it". The kiss shows the turn, and the next
   beats are all her doing it: the apron strap, "Will you show me your
   bedroom?", "She was already moving." The comparison is the narrator setting
   the kiss against the book's asking motif, and "narrow register" is not
   her word at this heat (Console: under pressure her voice goes plainer).
   - **2a (recommended):** "She kissed him before he could answer, and did not
     try to slow it. His hands found…" This keeps her refusing to slow it,
     which is hers.
   - **2b:** cut only "and every narrow register she'd held herself to since,"
     and keep the dinner/dress comparison and the because clause.
   Tally: no verbatim or fragment hits (five stem-only, none on this line).
   Paraphrase: readers credit her initiative from the actions — opus fsog
   gate ("from there every move belongs to her… the apron strap… 'Will you
   show me your bedroom?'"), fable fsog gate ("she kisses him first"), sol
   cold read ("She initiates the kiss, asks for the bedroom"). None of them
   quotes the comparison.

## Leaving alone

- `:7` "chose without thinking too hard about why": her refusal to look at
  why. The line-edit triage relies on it to carry what the cut "reason
  enough" sentence argued.
- `:11` "Like a short story… kidding herself": left standing (line-edit
  triage).
- `:13` "told herself none of this meant anything in particular": her own
  explanation; the reader sees past it.
- `:39` "the question already in his hands — the beginning of care…": her
  perception of his manner (glm romance gate praises it).
- `:49` "because there was no seam, they ran on the same wire": her
  experience of the shame, not a gloss; the chapter's engine.
- `:51` "She knew what was coming. That was the worst of it": her anxiety
  spiral, in her voice.
- `:59` "That was the worst it had.": her answering the voice.
- `:65`, `:69`, `:71`, `:73`, `:79`, `:97`–`:99`: reader-praised or left
  standing in the line-edit triage.
- `:83` "the answer to his question arriving ahead of everything else": her
  mind linking back at the peak.
- `:93` "the thing he'd been holding since the door, since the sun porch…
  He stopped governing it.": her reading of him at the peak (Step 3). "He
  stopped governing it" half-repeats "let go", but it adds that his care was
  held on purpose, which is what "She had wanted that" answers.
- `:107` "The evening had used her well.": left standing (line-edit triage).
- `:123` "Something in his shoulders was private": her perception of him.

## Rulings
- 1 `:21` "He'd done all the preparation and stopped." — **cut** (author). On challenge, conceded the sentence reads as her inference, not the narrator's; the cut is a trim on the `:23` precedent (an inference stated flat that adds nothing to the dry pan and leaves her no reaction to it).
- 2 `:37` — **2a** (author): "She kissed him before he could answer, and did not try to slow it." The dinner/dress comparison, "every narrow register", and the because clause go; the turn is carried by her actions (apron strap, "Will you show me your bedroom?").

**Applied 2026-10-26:** 1, 2a. Lint: 0 errors; 14 info hits, none on the changed lines. praise_check over the diff: nothing new (stem-only hits, none on the cut words). orphan_refs (famished, missed-a-spot, covering, clean-plate): nothing flagged.

### Second batch (author: "that was all you found?") — walked 2026-10-26

- 3 `:83` "That was the first of it, the answer to his question arriving ahead of everything else, unmistakable." — **3a, cut** (author), over one praise quote (gpt-5.6-sol cold read). Explaining the joke: "He was so hard" pays off `:63` without the pointer.
- 4 `:93` recap clause + "He stopped governing it." — **kept** (author). Heavily praised ("stopped governing", fable/opus fsog, sol romance), and with `:83`'s pointer cut, the recap is the chapter's one link from "told no" back to `:67` (fable romance used it).
- 5 `:57` "so he met it before he had bared her at all." — **kept** (author). Her inference from her own sensation ("met" is contact, not his mind; `:61` "She saw him see them" is the step up). No "she knew" needed — a filter would blur the `:57`→`:61` escalation. Paraphrase praise: fable romance, flash romance.
- 6 `:51` "The anticipation sat on top of the fact of it, which made it worse, which made more anticipation." — **cut** (author). Repeat in the abstract of "She was already ashamed of what he hadn't seen yet."; no praise.
- 7 `:13` "and told herself none of this meant anything in particular" — **kept** (author). Her own denial, the last in the chapter's run of refusals (`:7`, `:11`); sol cold read verbatim "funny, aching, and completely her", glm paraphrase. Not a wink.

**Applied 2026-10-26 (second batch):** 3a, 6. Lint: 0 errors; 14 info hits, none on the changed lines. praise_check over the diff: only the known sol quote of `:83`. orphan_refs (famished, missed-a-spot, covering, clean-plate): nothing flagged.
