# Triage — Believe Me (line edit, 2026-08-13)

Craft-level line-edit pass (`audits/line-edit/believe-me.md`, 12 findings) plus
one uncounted note. Cold-read prep mined all **7** panels (fable-5, opus-4-8,
sonnet-5, gpt-5.5, sol, terra, kimi-k3) — the panel reported essentially zero
craft friction, so every finding was weighed against praise rather than
complaint. **9 applied, 3 left standing.** Style linter was clean going in.

## Applied

- **`:7`** — cut "and it had gone through her a little every time since"; the
  paragraph's payoff ("It went through her now, and she hated that it did") now
  lands off her deduction rather than off a third ritual tag.
- **`:11`** — cut "thin and metal" from the coin figure; the coin carries its own
  thinness and metal, and the appositive explained an image after it landed.
- **`:13`** — cut "on the nights she stayed" from the music line (kept "the kind
  he played," so the music stays *his* and not ambient); the ritual tag now
  belongs to the bag alone.
- **`:13`** — reordered so the paragraph ends on the bag: "She stayed where she
  was and went no further into the room. The bag was in the car; she had carried
  nothing in." The bag is the paragraph's knockout (three models named it) and
  now exits on it.
- **`:15`** — cut "waiting" from the wine; "one for her" is the knife and now ends
  the sentence.
- **`:15`** — cut "the way it opened every time" (see **ritual-marker thinning**
  below).
- **`:29`** — cut the attribution "He said it simply, with certainty" entirely;
  three speech paragraphs now quicken into "But what am I?", and "certainty" is
  left to Pace's load-bearing use at `:15`.
- **`:39`** — "came out of her mouth" → "**left** her mouth"; kills the doubled
  "came out" inside twenty-five words while keeping the mouth as the concrete
  anchor. The thematic clause is untouched (kimi-k3 quoted it approvingly).
- **`:47`** — "Pace stood looking at her, saying nothing" → "Pace stood looking at
  her." His silence is now first *named* at `:55`, where the designed escalation
  lives.
- **`:55`** — the four-clause *and*-chain recast to asyndeton (author's wording):
  "He stepped back, his arms came up and folded, he held there, still, the still
  of a man holding a line at cost, and he said nothing." The discrete closures
  now land separately, and the terminal "and he said nothing" reads as the
  arrival rather than the fourth item in a list. **The comma splices are
  deliberate** — register, not error; a copyedit pass must not restore the
  conjunctions.
- **`:59`** — cut "That was the one thing she could not take from him now"; the
  protected line "Not the hand in place of the word" now lands two beats sooner,
  off the reaching hand rather than off a gloss of it.
- **`:33`** — cut "and it was rising" from "because she had it now and it was
  rising and she wasn't going to lose it." Added **after** the post-edit panel, on
  opus-4-8's only friction item ("I'd already felt the rise; being told was a
  half-beat of over-help"). "He drew breath to answer and she went on over him"
  already dramatizes the rise; talking over a man mid-breath *is* the momentum.
  The outer two clauses stand — "she had it now" marks the direct question finally
  arriving after a relationship of indirect ones, and "she wasn't going to lose it"
  is nerve being held, neither visible in the blocking. **Not in the original 12** —
  it surfaced only because the overwork around it was removed.

### Ritual-marker thinning (author ruling 2026-08-13) — cold-read test PASSED

Four "every time / the way it always did" markers fired in the chapter's first
nine lines. Author ruling: **repetition at that density makes the ritual ambient
when the chapter needs it to be evidence** — Vee is reading his care as a case
file, and evidence should be counted, not hummed. Thinned four markers to two by
subtraction: kept `:7`'s lamplight instance (acked 2026-07-28) and `:7`'s
load-bearing heat instance ("every time, so she would never once be cold"),
cut `:7`'s "every time since" and `:15`'s "the way it opened every time."

A **summary sentence** consolidating the ritual ("this was how he welcomed her
every time") was considered and rejected: it asserts a pattern instead of
enacting it, and `:7`'s "she had worked that out a long while back without his
ever saying it" already does that job as *her* deduction rather than the
narrator's.

**This is an experiment with an explicit revert condition.** `:15`'s cut clause
was **reader-praised** — opus-4-8 quoted it as the thing "that keeps this from
being a simple unmasking… his gladness at the sight of her reads real, and it
makes what follows worse, not cleaner," which is the earn-the-dark tripwire
working. Cutting by subtraction rather than adding a new sentence keeps the test
clean: **if the next cold-read panel loses the gladness reading, revert `:15`**,
because nothing else was introduced that could account for it.

### Cold-read result (2026-08-13) — no revert

Full panel re-run post-edit (opus-4-8, sonnet-5, gpt-5.6-terra, gpt-5.6-sol,
gpt-5.5), compared line-by-line against the pre-edit reads at commit `965b214`.

**The tripwire held on 5/5.** Every reader still refuses the simple-unmasking
reading; none acquired suspicion that Pace's care is fake. `:15` **stands**.

But the *evidence* rotated, unanimously and worth recording:

- **The face motif went from two-sided to one-sided — the real cost of the pass.**
  Pre-edit, four of five cited the opening as belief-evidence: opus ("I believe
  that opening"), terra ("I believe his face opening at the door"), sol ("his face
  opening at her arrival. I melted at all of that"), gpt-5.5 ("The heat, the
  preparation, his face opening… all feel real"). **Post-edit, every surviving
  mention of his face is the *shutting*** — opus "the shut face," terra "something
  'shut' across his face," sol "when something in his face shuts" — and sonnet and
  gpt-5.5 do not use the word "face" at all (sonnet 3→0, gpt-5.5 2→0; panel-wide,
  *open* fell everywhere and *shut* rose).
- The event was **never cut** — "His face opened when he saw her" stayed on the
  page. What was cut was its status as **evidence**: "the way it opened every time"
  converted a momentary beat into a *pattern claim*, and a pattern claim is what a
  cold reader reaches for when arguing his care is real. One door-opening proves
  nothing; a habit does.
- **But the deeper damage is structural.** The face is the chapter's own
  before/after instrument — it opens at the door, it shuts at the question. Losing
  the opening's weight **broke the pair**: the shut at `:55` no longer has a
  counterpart to reverse, so readers register it as a standalone event rather than
  a turn. This is the likeliest driver of the Pace-hardens-toward-decision shift
  below — *the only thing his face does now is close.*
### The face fix — two attempts, and the ruling (2026-08-13)

**Attempt 1 — a period for a comma, no new words.** "His face opened when he saw
her**.** He crossed to her…" Theory: give the beat its own stop and restore
prominence without restoring marker density. **FAILED.** Re-ran terra + sol: terra
still cited only the shut; sol did not use the word "face" at all. Scores dipped
(terra Romance 3→2, sol Heat 1→0, Romance 3→2). **Lesson: the cut clause was not
supplying emphasis, it was supplying the *claim*. Punctuation cannot manufacture a
pattern claim.** Reverted.

**Attempt 2 — restore "the way it opened every time" verbatim. ADOPTED.** `:15`
now reads as it did pre-edit *except* that "waiting" stays cut, so the face clause
is the sole delta. Re-ran terra + sol:

- **terra:** "Pace's face opening for the usual kiss got me too. I still believe
  the welcome is real."
- **sol:** "the waiting wine, Pace's face opening at the sight of her—all the
  things that usually make me melt now press directly on the bruise. I still
  believe his welcome is real."
- **The two-sided motif is back in one reaction** (sol, `face 2 / open 4 / shut 2`,
  up from `0/3/1`): "His face shutting and his folded arms are the first moments
  here that make me recoil from him. I do not know whether he cannot find the word,
  rejects the available words, or refuses something they imply. The page leaves that
  open. What is no longer open is that, when she asks directly, he withholds."
  **The best Pace formulation any reader produced across four runs** — the *whether*
  stays open, the *that* is settled — and the recoil is stronger than in any earlier
  read *because the opening preceded it*. A shut needs an open.
- sol's scores recovered to pre-edit (Heat 1, Romance 3).

**Standing ruling: `:15`'s "the way it opened every time" is now PROTECTED.** It
was cut once on a density argument and the cut cost the chapter its before/after
instrument; three ritual markers in nine lines is the working number, four was
ambient. Do not re-flag it as repetition. The other three thinning cuts stand.

**Method note for future experiments:** across four runs of near-identical prose,
single-reader *shadings* (terra's Pace reading occupied three different positions;
Romance drifted 3/3/2/2 on identical glosses) proved unreliable, while
**presence/absence facts** — is this line in the reader's evidence list at all —
held consistently across readers and runs. Weight the latter; discount the former.
- **Replacements, per reader:** opus → the heat brought up hours early; sonnet →
  the reaching hand; terra → unlocked door, warm house, consistency with the man
  she's known; sol → the declaration plus his softening at her tears; gpt-5.5 →
  the prepared evening plus, newly, "silence costs him too."
- Both mechanisms ran at once: **demoted here, promoted there.** `:7`'s heat
  marker now lands as its paragraph's payoff instead of the second of three, which
  is exactly the split the thinning was designed around.

**Pace hardened toward *decision* — 4 of 5** *(recorded as observed, but see the
method note below: later runs showed this class of shading is unstable run-to-run,
and both codex readers reverted toward the hedge on re-read. Treat as suggestive,
not established.)*, without any reader crossing into
"he was faking." terra: "plainly his sincere conviction" → "exactly the refuge he
uses… unable—or unwilling," and **attributes the shift directly to the `:29`
attribution cut** (with the author's warrant gone, the reader weighs the line as
possible strategy). sol: hedged three ways → "a line he has consciously chosen not
to cross." gpt-5.5: "his language fails" → "his verbal refusal is now
unmistakable," offset by a new credit that the silence costs him. opus: "a man
under a rule — whether the rule is Randi's or his own I don't know." **sonnet is
the lone dissenter**, softening to "he genuinely doesn't have the word." Two
readers now ask *whose rule*, unprompted — the earn-the-dark seeding strengthened
while staying inside the band.

**The `:13` bag reorder is the unambiguous win — 4 of 5.** terra promoted it from
unmentioned prop to a named opening motif ("the uncarried bag marks that she has
not come to stay"); sol gave it its own praise beat and motif line, neither of
which it had; opus: "a whole argument made with luggage." gpt-5.5 alone still does
not mention it.

**Two losses, recorded so a later pass doesn't rediscover them as new:**

1. **gpt-5.5 lost "Not the hand in place of the word."** It was that reader's
   designated peak pre-edit; post-edit it survives only as generic paraphrase.
   Ironic, since the `:59` cut was meant to bring it *closer* to the gesture.
   opus and sonnet still call it the chapter's best short line and sol keeps the
   beat — one reader of five, but it is a protected line and it moved the wrong
   way. **First smoke that subtraction is nearing erosion in this chapter.**
2. **terra lost the stillness** — "the still of a man holding a line at cost"
   dropped out of its reaction entirely; the `:55` asyndeton did not register.
   gpt-5.5 ran the opposite way and quoted "line at cost" for the first time ever
   off that same recast. Net a wash.

Scores held flat across the board (opus 1/3, terra 1/3, sol 1/3, gpt-5.5 1/2,
sonnet 0/2). No reader reported the chapter as thinner, colder, or more abrupt.

**Standing caution for future passes on this chapter: ten overwork cuts have
landed. The chapter is at or past its economy ceiling — treat further subtraction
as suspect absent multi-reader evidence.**

## Left standing — do not re-litigate

- **`:21` in full** — the offer ("I've got the chicken going… we sit out on the
  porch… It's clear tonight, you can see everything"), the narration ("He offered
  it plainly, the whole good evening laid out for her to take"), and the closing
  restatement ("That's what I thought we'd do"). sonnet-5 called the narration "a
  little writerly but it's doing real work"; the editor wanted it cut. **Author
  ruling: no cuts.** The offer is Pace's thesis stated as an itinerary, and the
  porch is the tell — his one gesture at outdoors is still attached to his house.
  He can give her the entire sky without leaving the property, which is exactly
  what Vee indicts at `:35` ("All of that is in here. Inside this house, with the
  door shut."). The restatement is not repetition but *closing the offer* — the
  way someone does when the plan **is** the feeling. Cutting it also collapses the
  speech into one unbroken block in which his closing echo reads as a stutter
  rather than a return.
- **`:39`'s three closing questions** ("Out there. What is this relationship? What
  am I to you out there?"). Editor wanted the middle one cut as the flattest.
  **Author ruling: all three stand.** This is *speech*, not narration — she has
  asked this question indirectly for the length of the relationship, and asking it
  three ways in one breath is what it looks like when the indirect versions have
  all failed. A single clean question reads composed; she is not composed. **The
  redundancy is the frustration.** Prose economy is the wrong instrument on a line
  whose job is to sound unedited.
- **Pace's counter-question** ("Do any of your friends have a relationship you'd
  rather have than this one?"). **New post-edit friction from gpt-5.6-sol only**:
  "it feels so oblique that I nearly share her disbelief." **Left standing.** The
  line was **not touched** in this pass — and the same reader read the same beat as
  a *strength* pre-edit ("I admire that she refuses to let his true counterquestion
  displace hers"). A lone reader inverting on an unedited line is taste, not signal;
  four of five readers raise nothing here, and the obliqueness is the character
  (his grammar is plans and acts, not names). By the final run sol had integrated it
  approvingly — "it is true, intimate, and still an evasion… pulled against me
  exactly as it pulls against Vee." Re-open only on multi-reader corroboration.
- **Pace's "I thought we'd have the evening"** — the 2026-07-30 left-standing item,
  which **recurred as sol's sole friction in two consecutive later runs**. Still
  **left standing**: sol self-resolves it both times ("his literal answer fits what
  I know of him, and the text lets Vee see him turn the words over rather than
  making him coy"). Logged because it is now a *recurring* sol item rather than a
  one-off — a persistent soft spot for one reader, self-rescued by the page each
  time, and never raised by any other reader.
- **`:35`'s "such care" / "this precious thing"** — the two abstract phrases in an
  otherwise concrete speech; "precious thing" flagged as greeting-card diction.
  **Author ruling: both stand**, on the same principle as the questions above —
  it's her voice under pressure, and the soft cliché is what a careful person
  grabs when her own words run out. (Consistent with the 2026-07-30 verdict that
  the speech's slight over-fullness reads as *her*, not the author.)

---

# Triage — Believe Me (line audit, 2026-08-03)

Sentence-by-sentence consistency/logic audit (`audits/line-audit/believe-me.md`).
**Prose clean — 0 edits.** Arrival ritual, mat-anchored blocking, props, dialogue
logic, and the two-nights-running timeline (per prior ruling) all verified; Cassie
dialogue-only, `present: Vee, Pace` correct. One finding resolved in the set doc:

## Fixed (in `meta-plan-pace-house.md`, not the prose)

- **Wine-glasses sightline from the front mat** (:15) — geometry pinned in the
  house doc: counter visible from the entry mat through the kitchen doorway
  (committed to the page here), **plus new canon**: the kitchen has a
  front-facing window beside the covered stoop (kitchen fronts the house on the
  stoop side). Worded "stoop," never "porch" — the porch is the sun porch.

---

# Triage — {{Believe Me}} (cold-read pass, 2026-07-30)

Panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol. The cleanest sheet
any scene has received — every friction point raised was self-resolved by the
reviewer who raised it. No prose changes made.

## Fixed

Nothing from the cold-read pass itself. From the same-day scene review
(2026-07-30):

- **Music thread planted** (author decision): one ambient beat added to the
  arrival sensorium — piano, quiet, slow, "the kind he played on the nights
  she stayed." Rationale: Pace has no idea she came for a fight; the flowing
  music is the evening running on without her, one more thing pulling her in,
  counterpoint to her state. Satisfies the Bible registry's music-thread
  trigger (any scene at Pace's house) — decided, not reflexive.

## Scene-review verdicts (2026-07-30) — decided, do not re-open

- **"two nights running" (the sleeplessness) is allowed** (author ruling
  2026-07-30): {{Bare}} renders the second night; the first is granted as
  plausible off-page. Not a continuity error.

## Left standing — do not re-litigate

- **Vee's speech as a full inventory of the relationship's goods** (fable-5:
  "a touch too complete an inventory of the book's own motifs"). Standing:
  the speech is the planned realization of the "demand to be named"
  (chronology entry, condensed brief), and the Bible's stress-tell rule
  requires the goods to carry full weight so the refusal lands as refusal of
  something real. The reviewer bought it as rehearsed-then-breaking — which is
  the fiction: two sleepless nights of rehearsal.
- **"it was true, and it wasn't the point, and she hated that he'd made the
  true thing pull against the point"** (opus-4-8: closest to over-explaining).
  Standing: reviewer conceded it earned itself; the doubling is the felt shape
  of his deflection working on her.
- **"reach for the thing she was asking for and not find it anywhere in
  himself"** (gpt-5.6-sol: POV overreach — she can't know that). Standing:
  lone reviewer, self-resolved; the sentence opens "She watched him," so it
  reads as her inference within close third, which is the license the whole
  book runs on.
- **Pace's literal "I thought we'd have the evening"** (gpt-5.6-sol: briefly
  risks implausible obtuseness). Standing: rescued on the page by the "small
  pause"; the literalism is the character (plans and acts are his grammar).
- **Style acks (2026-07-30, in `style/style-allow.toml`):** `the-way` on the
  lamplight line (ritual-repetition work); `unhurried certainty` at the
  door-kiss (Pace's word, load-bearing beat); the six `warm` hits (the
  scene's subject is weaponized warmth — all load-bearing).

## Confirmed positives — protect in any future edit

All four models: "Words are cheap, and you still won't spend them on me" (the
peak); the bag left in the car; "Not the hand in place of the word"; the
fairness of the indictment ("I'm not complaining about one minute of it");
"the still of a man holding a line at cost" (read as damage, seeding the
Randi-shaped suspicion exactly as designed); the ending — "Vee" as not the
word she'd come for, and "it was worse, and she did not go back in" (load-
bearing for the January payoff in {{Nothing Underneath}}, First Weekend Back).
