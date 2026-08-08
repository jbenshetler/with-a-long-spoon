# Triage — Hills and Valleys (line-audit pass, 2026-08-02)

Source: `audits/line-audit/hills-and-valleys.md`, reviewed with the author.
**The "Left standing" section records authorial decisions — do not re-flag
these without new evidence** (a new reader cohort snagging on the same spot,
or an edit that re-opens the passage).

## Fixed

Nothing — the audit's only finding was left standing; everything else checked
clean (dates vs. chronology, cross-scene continuity with {{Lesson}} and
{{A Recognized Method}}, Sheri facts, spatial logic, dialogue logic, tense).

## Left standing — do not re-litigate

- **":45 "He caught her up" with no stated re-separation** — she has been
  *soft-pedaling* (still rolling) since :29, and "already looking down the
  road" is her moving off while he declines to answer; the drift apart is
  reconstructible and her not waiting is the characterization. A stated
  re-separation would be exactly the logistics beat this 45-line vignette
  is built to omit.

---

# Triage — Hills and Valleys

*Cold-read feedback pass, 2026-07-27. Panel: claude-opus-4-8, gpt-5.5, gpt-5.6-sol (all read after {{Broken In}}). No prior triage.*

## Panel consensus — what's landing (protect)

- **Sheri lands fully formed, unanimously** — "a real person, not a device"; instant reader trust; "loyal heat." The lines doing the work are the defining ones: *"remarked on women the way other people remarked on the weather"*, *"could turn it on a person inside a breath and keep it burning for years."*
- **"Listen to you" is the chapter for all three readers** — Pace's overflow (walnut joint, math book) read as involuntary tenderness; no machinery detected.
- **Placement works** — read as an earned breather that widens the field and builds dread before the reconciliation.

## Fixed (this pass)

- **Triple Pace-won't-say beat** (opus): cut the middle *"He said nothing."* — the road tilting up now carries the silence; the canonical final *"He didn't answer"* keeps full weight.
- **Climb-paragraph tic cluster** (linter, no reader stumble): light pass only — *"the way she always did"* → *"as she always did"*; *"the way he always did"* → *", as ever,"*. Filter verbs, "a small frame", "there was never", and the *"whole of it"* closer left standing (see below).

## Left standing — do not re-litigate

- **The "weather" sentence** (*"She remarked on women the way other people remarked on the weather"*). gpt-5.6-sol alone felt it pre-explains Sheri; the linter double-flags it. Author keeps it: two of three readers quote it as a favorite and it is Sheri's defining note. Hits suppressed in `style/style-allow.toml`.
- **"That's not finished" + the non-answer to "two of them at once"** — working exactly as designed (`meta-note-hills-and-valleys.md`: the warning in the one register Pace can parse, refused). gpt-5.6-sol's trust drop at this line is the intended effect, not friction.
- **Title** — retitled **Hills and Valleys** (was "Sheri — First Ride"; author, 2026-07-28). The old title's puzzle (not their first ride; self-resolved by opus and gpt-5.6-sol to *the reader's* first ride) is moot. New rationale: surface = the literal terrain of the ride / the ups-and-downs idiom; charge = women's bodies in Sheri's register — this scene **begins Sheri's pattern of crassly commenting on women's bodies** ("hell of a backside on her, though"; "remarked on women the way other people remarked on the weather"), and the title accrues charge each time the pattern recurs. Sheri-flavored by design: the chapter is the reader's introduction to her.
- **"She filed it somewhere"** — `file-verb` linter tic, but gpt-5.6-sol quoted it approvingly and independently rhymed it with the sorority "folder"/institution motif. Earning its keep.
- **"That was the whole of it" closer** — `whole-of` tic, but praised by gpt-5.6-sol as "deliberately casual, though what Sheri learns is not casual at all." Stands.
- **"Would have ridden farther with her"** (opus, gpt-5.5) — appetite, not friction; the scene is designed brief, and Sheri recurs ({{The Usual}}, {{Another Round}}). No lengthening.
- **Cold-open disorientation** (gpt-5.5, momentary) — the bracing shift out of the Vee/Randi rooms is the point; settles within a paragraph. Stands.

## Housekeeping

- Corrected stale date in `meta-condensed-hills-and-valleys.md`: now ~Sat Oct 24 (the Saturday after the Thu Oct 22 CW-Dance blowup, matching the chronology). An earlier version of this note said Oct 31 in error — corrected by the timeline sweep 2026-08-03.

---

# Triage — Hills and Valleys (line-edit pass, 2026-08-08)

Source: `audits/line-edit/hills-and-valleys.md` (9 findings), reviewed with the
author item by item. Cold-read enrichment: all five models
(claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol, gpt-5.6-terra).
**8 items ruled, 6 edits applied, 1 finding dropped as already-settled, 1
pre-ruled echo resolved as a keeper.**

## Context worth keeping

- **The chapter is the best-liked short piece in the pass so far.** No reader
  found it long; claude-opus-4-8 wanted it *longer* ("I'd have ridden farther
  with her"). All five read it as a deliberate exhale that widens the field and
  builds dread. **Do not lengthen and do not trim for pace** — every edit this
  pass was local overwork, none structural.
- **Reader-protected lines (five-model consensus):** the `:19` gush (walnut
  joint, thumb down the grain, the math book "not put it back like it had
  burned her"), `:23` "Listen to you," `:25` "He didn't know what there was to
  listen to" (opus: *"That's the tell — he can engineer a woman's whole night
  but he can't hear himself falling"*), `:31` "She could turn it on a person
  inside a breath and keep it burning for years," `:33` "She couldn't take your
  heat" (fable-5: Pace protecting Vee from his own friend), `:39` "Randi.
  That's not finished" (opus: *"the first time a sane bystander has looked at
  the shape of this and said, flatly, this ends badly"*), and `:29` "not as
  winded as would have suited either of them."
- **gpt-5.6-terra is the only reader to have seen the final title** and found
  it effective: literal terrain plus emotional terrain, *"does not spoil
  anything; it makes the chapter's physical rhythm feel like a mood."* The
  earlier four reviewed "Sheri — First Ride." The title question is closed.

## Fixed (6 edits)

- **`:1`** — "They rode Saturdays when the weather **let them**, out past his
  place" → "They rode **most** Saturdays, out past his place." The first of two
  "let them" eleven words apart; the second ("they talked where it let them")
  is the chapter's governing idea and was being spent early. Side effect: the
  chapter's only *figurative-adjacent* weather hit is gone, leaving the
  protected simile as the sole use.
- **`:3`** — cut "She was small on the bike and fast on it, all of her folded
  down into the work," keeping "She had been faster than him on the climbs…"
  `:27` renders the same observation with images (child's frame, standing legs,
  ponytail); the assertion was pre-empting its own dramatisation, and "small"
  ran three times across the two paragraphs. Echo ledger #51.
- **`:13`** — cut "and it had never once cost him anything," keeping "and she'd
  been doing it across this handlebar for two years." The protected weather
  simile is untouched; what went is the narrator's reassurance tail, which is
  where gpt-5.6-sol's over-explain reaction actually lived. Also resolves the
  "never once" repeat with `:3` at no cost. Echo ledger #52.
- **`:21`** — cut "the look she got when she'd caught him out," leaving "When
  he ran down Sheri was looking at him sideways." The narration was diagnosing
  the catch, then Sheri delivered it, then his blankness confirmed it — three
  deliveries. All five readers quoted the exchange; none quoted the label.
  Echo ledger #50.
- **`:27`** — cut "He marvelled at it, as ever," leaving "He saved his breath
  for the hill, and came up at the top a length behind." "Marvelled" named the
  response the colon-clause had just produced — body-before-mind running
  backwards. (The clause had been touched once before, in the 2026-07-27 tic
  pass; that fix did not address the overwork.)
- **`:31`** — cut "She'd do it, too." from "'You want me to not like her?' she
  said. **She'd do it, too.** She could turn it on a person…" The verb repeated
  inside four clauses ("She'd do it" / "he'd seen her do it"). The closing
  gloss "which was everything" was **kept**: gpt-5.5 quoted the sentence
  *including the tail* as the line that made them "both like and fear her."

## Left standing — do not re-litigate

- **`:19` "And then he was past the name before he'd decided to be"** —
  stands (author, 2026-08-08), on claude-fable-5's citation of the line by name
  as the moment Pace gushes — the same evidentiary standard that protected
  `a-round:220`. **The same ruling retired echo #8's ration**: the "six in
  Volume One" was a census of what the harvest found, never a quota the author
  approved, and six across ~137,700 words of a non-striking construction is not
  overuse. Newly surfaced instances are presented neutrally on the merits, with
  no vary-by-default presumption. See echo ledger #49.
- **`:45` "and that was the whole of it"** — the editor's finding 9 (ends one
  beat late) was **dropped before presentation**: already ruled left standing
  at the 2026-07-27 triage on gpt-5.6-sol's praise. Rediscovery, not new
  evidence.
- **`:31` "which was everything"** — see Fixed above; kept against the editor's
  recommendation on gpt-5.5's direct quotation.
- **The `x-not-y` cluster (`:27`, `:29`, `:43`)** — three info-level hits.
  `:29` ("soft-pedaling, not as winded as would have suited either of them") is
  a keeper line; the other two are structural. Density ruled acceptable.
- **`:19` filter-verb "He heard himself going and didn't stop" and `:25`
  "there was"** — both sit inside the five-reader-praised beat, and *hearing
  himself* is literally the content of the moment. Not tics here.

## Linter acks (author sign-off 2026-08-08)

All 12 active hits acked; 0 errors. Nothing unruled among them:

- `:13` **the-way** + **weather** were **re-arms**, not regressions — the
  fingerprints re-fired when the item-4 edit reworded the protected simile's
  sentence. Same protected line.
- `:27` **a-small** / **filter-verbs** / **there-was-were**, `:41`
  **file-verb**, `:45` **whole-of** were all left standing at the 2026-07-27
  triage but never acked, which is why they kept nagging. Now suppressed.
- `:19` **filter-verbs**, `:25` **there-was-were**, and the three **x-not-y**
  hits per the left-standing entries above.

## Housekeeping

- The chronology entry (line 144) lists `present: Pace` — Sheri is the other
  participant and is not listed. Flagged, not changed (chronology metadata is
  the author's).
