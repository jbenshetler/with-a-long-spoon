# Capture/retention panel — SPEC (v1)

*Committed 2026-09-07. Measures **capture and retention** across the free-sample
stretch: persona-conditioned blind readers take the first four chapters
(`the-bench`, `standards`, `the-pointing-game`, `see-you-later`) sequentially
in one sitting, with a hard STOP/CONTINUE gate after each chapter. Purpose: find
where target readers would put the book down, before the sample goes public
(`meta-plan-free-sample.md`).*

## Instrument

Each read = one persona × one model × one arm, on the clean lanes (same
isolation as the authorship audit; `tools/capture_panel.py`). The reader gets
the core reader frame (`prompts/core.md`) + a persona block (`personas/*.md`)
as the ENTIRE system prompt, then [arm-dependent jacket +] the four chapters.
After each chapter: DECISION (STOP/CONTINUE), CAPTURE 0–10, ALMOST-STOPPED
(the exact moment, quoted — the actionable output even when they continue),
WHY in persona voice. A STOP ends the read (no later gates). Finishers answer
the conversion questions (would-pay at $9.99, mailing list, tell-a-friend
paragraph).

**Honesty mechanism:** models are completion-biased, so the frame weaponizes
the real economics — infinite free alternatives one click away; stopping is
the default; the book must earn each next chapter. Gradient (CAPTURE) and
ALMOST-STOPPED give signal even when outright stops are rare. Read the results
as a survival curve + ranked almost-stopped moments; single-read stops are
noise, convergent ones are findings (same convergence discipline as the
authorship audit).

## Personas (versioned in `personas/`; run header records SHA)

1. `romance-graduate` — outgrown spicy romance, won't give up the heat
   (primary vector, `meta-plan-distribution.md` §4).
2. `fsog-refugee` — wants the FSoG intensity with real consent and warmth
   (the crossover strategy, `meta-plan-pen-name.md`).
3. `consent-sensitive` — vigilant about predation-romanticizing; measures the
   **con-misread exposure** the docs flag for exactly these chapters (stays
   with dark content only if the book visibly knows what it's doing).
4. `dark-romance-control` — the WRONG reader ("wreck me with a bad man");
   should bounce. A book that captures her is failing the repel goal; her
   stops are successes.

## Arms

- `jacket` — Volume One jacket packet (`checkpoint_bundle.jacket_packet()`)
  precedes chapter one: the retail-sample funnel, with the designed
  complicated-love-not-a-con pre-framing in play.
- `cold` — chapters only: the Literotica-style funnel, no pre-framing.
  The delta between arms measures how much work the jacket actually does.

## Roster & scale

Full 8-model panel, paid lane author-authorized 2026-09-07 ("full panel
including paid"). 4 personas × 8 models × 2 arms = 64 reads. Personas are
simulations of readers, not readers — treat output as candidate signal for
authorial judgment, strongest where personas × models converge; the eventual
ground truth is the human test-reader cohort (`meta-plan-test-readers.md`).

## Run 1 results (2026-09-07 — 64 reads, full panel, both arms)

Survival (finished/8 · pay-yes · list-yes): romance-graduate jacket 8/8·8·8,
cold 8/8·8·7 · fsog-refugee jacket 8/8·8·8 (after one truncation re-run), cold
6/8·6·6 · consent-sensitive jacket 8/8·8·8, cold 8/8·7·5 · dark-romance-control
jacket 7/8·6·6, cold 5/8·3·3. **Six stops total**: 4 = control bouncing off
"safe Pace" in chs 1–2 (the filter working: "not the man I came here for");
2 = fsog-refugee **cold-arm only**, exiting chs 3–4 over Vee's uninformed /
Randi's managed consent — the premise, not the craft ("the third person's
consent is this far behind the couple's desire").

Key findings: (1) **the jacket is load-bearing for the FSoG refugee** — 8/8
with pre-framing vs 6/8 cold; the Literotica funnel should carry framing that
does the jacket's permission-work (→ `meta-plan-free-sample.md`). (2) **The
2026-09-07 pointing-game irony cue is the panel's most-cited trust line** —
"He took the body's answer for the true one. He usually did." cited by ~23
reads as the reason fsog/consent readers stayed ("a loaded gun on the wall";
"the author's thumb on the scale, marking his epistemology as a habit, not
wisdom"). (3) **Ch 2 `standards` is the universal capture dip** (9→7→9→8
book-shape; the "did not cry" stillness cluster cited ~25×) — no target
reader stopped there; monitor, don't fix. (4) **Control leak is genuine
attraction, not misread**: the 9 finishing controls stayed for Randi-as-
predator / daylight grooming ("my exact kink wearing a Sunday dress") —
a secondary audience the no-villain ending may later betray; keep them out of
targeting (already policy). Consent-sensitive persona granted trust
explicitly conditionally: the book reads as *knowing* — trust to be honored
downstream.

## Run 2 results (2026-09-07 — full-volume, two memory arms)

**Arms:** single-go perfect recall (4 models × 4 personas, `<persona>--volume.md`
+ `--volume-interview.md`) and the **capture DAG** (author-specified
cold-reader architecture: one run per chapter, reader-owned decade mints;
opus+sol × 4 personas; `dag/` trees + `--volume-dag.md` records).

- **Retention: the volume holds its target readers under realistic memory.**
  6/6 DAG target readers finished all 50 chapters; capture averages 7.3–8.9,
  DAG ≥ single-go almost everywhere. No convergent mid-book trough; the four
  scattered capture-5 gates are all **debrief/breather chapters** (What to
  Wear, Turned Up — "a debrief, not a scene"; hills-and-valleys; Made-Up) —
  convergent with the interviews' debrief-economy complaint. What re-arms a
  dipped reader is the con's continuity, never the romance.
- **The wrong-reader filter works better in the realistic instrument:** both
  DAG dark-romance controls stopped at ch 2 (vs mostly coasting to the Randi
  payoff under single-go perfect recall). Genre mismatch, not craft failure.
- **Comeuppance (interviews, tiered funnel):** 2/16 raised it unprompted at
  T1, 13/16 named it as debt at T2; Claude readers reframe at T3 ("convicted,
  not sentenced"), GPT readers stay bothered; **15/15 finishers still buy Book
  Two — as creditors**, with a universal tripwire: a second volume with Pace
  unbilled triggers loud exit and retroactive condemnation. The debt is a
  **Book Two design question, not a Vol 1 revision question**. Secondary T2
  inventory: Cassie owed an acting scene (2 readers); debrief density; more
  mass in the un-enchanted world (Kayla/Meg).
- **The mints confirm the thesis mechanism on readers:** trust-ledgers drift
  exactly as designed (tenderness trusted more *and* read as instrument;
  ck-050: "his hand reaching in place of the word now reads as the
  withholding it is"), and the FSoG reader's recurring fade — "I keep having
  to remind myself Pace and Randi are already a couple… which is, I suspect,
  exactly the trick being played on me too" — is the configuration receding
  in reader memory, i.e., the book's con working at the reader level.
- **Echo-economy flags from "what's fading"** (real production signals): the
  nude photo — "a gun on the mantel I haven't heard fire; I've half-lost
  track of it and I want to know if the book has too" — and Pace's real name
  "barely held — it hasn't mattered in chapters." Long-gap plants may want
  refresher beats; author's call.

## Prose revision traced to this instrument (2026-09-08)

`we-find-out` (ch 32) consent mechanics revised on the Sol consent-sensitive
DAG reader's flag ("silently expands the bargain… converts a constrained nod
into permission"): Vee now initiates the game (kiss + swat + "You want to play
that?"), a steady-nod check gates the penetration threshold ("Her breath was
not steady, but the nod was"), a quiet verbal check gates bare-bottom ("Do you
want to keep going?"), and the false bet-expansion is replaced by an open
request received as power ("Slow." / "For me." → "It was hers now, give or
keep, and she loved it."). The three "Uh-huh"s now descend in register
(laughing → wordless-steady → smaller). Future full-volume runs should watch
whether the ch-32 flag clears.

## Prose revision traced to this instrument (2026-09-08, second)

`famished` (ch 18) intercourse extended from one compressed paragraph to a
fully rendered act, on two DAG flags: Sol romance-graduate ("penetration
rendered rather than dissolved into impressionistic language. The book nearly
lost goodwill by skipping the physical center") and Sol consent-sensitive
("the chapter's coy blur skips… an actual check-in at precisely the point
where this book's whole moral architecture says specificity matters" — the
pull is now rendered, so the choosing is legible at the threshold). Male-finish
rendering rule amended alongside (`meta-note-tender-relief.md` §6, author
ruling: his undoing is her payoff).

**Re-read (6 gates, opus+sol × 3 target personas, controls excluded):** all
CONTINUE; captures 9/9/8 → 9/9/8 (opus) and 9/10/9 → 10/10/9 (sol). Both
prior complaints cleared — Sol rg: "delivered the explicit payoff without
sacrificing a molecule of the psychological specificity that made me want it"
(10, first ch18 none-almost-stopped from that reader). **New convergent flag
(both Sol readers, born of the rendered finish):** no visible contraception /
safer-sex beat — "unprotected penetration and ejaculation without any visible
conversation is a glaring consent-and-safety hole, and the next chapter needs
to prove the book knows that." Canon is silent on contraception volume-wide;
**author ruling 2026-09-08: stays silent ("no condoms, ignore it")** —
rationale and do-not-re-flag guard in `meta-triage-famished.md`.

## Prose revision traced to this instrument (2026-09-08, third)

`peekaboo` (ch 21) sex extended from the threshold cut ("nothing left for
either of them to decide" → "After") to a fully rendered sequence — standing
entry in the gown, the wait-the-dress pause played live as farce (the
disentangle, "Ow. Don't point down.", "a lot of you covered in a lot of me,"
the twitch rule-of-three), the finger-clean (ruled below the taste ladder —
`meta-condensed-peekaboo.md`), the sun-porch re-hang, the joined carry to the
bed, rendered finish. Author-designed choreography; flags it answers: Sol rg
"second time the book… closed the curtain / penetration lives behind frosted
glass" and two readers quoting the ellipsis line itself as ALMOST-STOPPED.

**Re-read (6 gates, opus+sol × 3 target personas):** all CONTINUE; captures
7/9/8 → **9**/9/8 (opus) and 9/9/9 → **10**/9/9 (sol). The ellipsis
almost-stoppeds are gone (five of six now "none"). Sol consent-sensitive
re-flags contraception — settled, left standing per the 2026-09-08 ruling
(`meta-triage-famished.md`); expected persona behavior, not a new finding.
Minor: opus rg felt the standing fumble "running long" until "Ow. Don't
point down" landed — noted, no action.

**Instrument amendment (2026-09-08):** all four reader prompts (`core.md`,
`core-chapter.md`, `core-volume.md`, `funnel.md`) now carry a
genre-convention note directing readers not to raise contraception / safer
sex / STI-pregnancy risk ("nobody in a novel can get pregnant or sick") —
implements the author's stays-silent ruling at the instrument level so the
settled flag stops recurring in future gates. Prompt SHAs change from here;
gates minted before this date were run without the note.

## Prose revision traced to this instrument (2026-09-08, fourth)

`recognized-method` (ch 29) Sunday sex extended from the kitchen-exit cut to a
rendered scene; design = *her cover story over his witness* (she runs it all to
paper over the look he caught; his palm covers the swat's print and holds; her
objectless *"Please"*). Answers Sol rg's "I actually swore… I am becoming
suspicious that this book likes approaching explicitness more than delivering
it." **Saturday's reunion fade (":65 the night took her under") left standing
by author ruling** — the apology movement's landing; the chapter's engine is
the kitchen.

**Re-read (6 gates):** all CONTINUE; captures 9/8/8 → **9/9/9** (opus) and
8/9/9 → **10**/9/9 (sol). Sol rg: "This gave me the explicitness the first sex
scene withheld and made the heat inseparable from Vee's interior life."
**New convergent flag (both Sol readers): "He didn't ask. He didn't say one
word."** read as a consent gap — *and both credit the book for knowing it*
("the chapter clearly marks the moment as unresolved"; "the prose refuses to
pretend those are the same thing"). No action: the silence is the architecture
(nobody names it here — {{The Practice Room}} extraction and {{We Find Out}}'s
naming both require it), and fsog's stated condition ("an explicit
conversation before he acts on this discovery again") is exactly what ch32
delivers three chapters later. Hover, not bounce — track it, don't fix it.

**Contraception-note amendment verified:** zero contraception/STI mentions
across all six gates (first run with the amended prompts).

## famished ch18 — second pass + flag→fix→re-measure (2026-09-09)

The first extension fixed the blur but stayed brief. Second pass added the
duration the chapter's center needs (held stillness, long middle, the
**witness** as the PIV-specific shame occasion, restraint ending on the page).
Panel scope widened: the DAG now has **four** models — `claude-fable-5` and
`gpt-5.5` full-volume readers arrived from the remote — so ch18 has 15
reader combinations, not 7.

**Run A (15 attempted, 11 completed).** All four `claude-fable-5` readers
failed on subscription quota ("You've reached your Fable limit"); their gates
were restored from git unchanged. Of the 11: all CONTINUE, three up
(gpt-5.5 consent-sensitive 9→10, sol romance-graduate 9→10, opus control
5→6), none down. **New convergent flag, on the new prose:** both Sol readers
independently quoted *"past where she was accustomed to being asked, her body
making room because he was already there and had never once been in doubt"* —
"he took before asking and then read her body as permission."

**Fix + Run B (11 re-run).** Asking moved to her body; his certainty cut; the
single-stroke entry replaced with a rocked one and the size coding stripped.
**Flag cleared: no gate quotes the clause.** Sol consent-sensitive 9→10 with
ALMOST-STOPPED *none*; Sol fsog-refugee now reads him the opposite way
("Pace's dominance attentive to her answer"). Two benign downticks: gpt-5.5
consent-sensitive 10→9, its almost-stopped moving off the bed onto his
control of pacing/information; opus dark-romance-control 6→5, the wrong
reader drifting back toward the exit ("the promise of teeth, not teeth") —
the repel arm recovering from the previous run's pull-in.

Incidental: opus fsog-refugee's near-flinch was the **repeated *floozie*** in
the kitchen kiss — a second model on the density gpt-5.6-sol noted in cold
read. Not actioned; the four-strike count is the designed loop
(`meta-triage-famished.md`).

## Reading a capture dip — standing rule (author ruling 2026-09-10)

**CAPTURE measures arousal and pull, not quality.** This book varies heat by
*kind*, so its breather chapters are designed to run lower — sustained tension
is exhausting and the rest beats are what make the risers land. **Lower
engagement in a breather is design, not failure**, and must not be triaged as a
weak chapter. A uniform 9 across fifty chapters would be the actual warning
sign: it would mean the breathers aren't breathing.

**A dip is a finding only if it shows one of:**
1. **No rebound** — the next chapter doesn't recover (or the decline compounds).
2. **Trust drop, not arousal drop** — the reader's confidence in the book falls,
   not merely their heat. Read the WHY, not the number.
3. **A real ALMOST-STOPPED** — an exit moment, not impatience ("not that I'd
   quit" is appetite, and appetite is the engine working).
4. **It lands in the free sample (ch1–4)**, where no goodwill is banked yet.

**Measured baseline (glm-5.3 full volume, 2026-09-10).** Target-reader baseline
**8.37**; deepest dips ~2 points (`what-to-wear`, `school-nights` 6.33;
`water-wings`, `hills-and-valleys` 6.67), every one rebounding +1.67 to +2.67
the following chapter. No target reader fell below 6 anywhere in the volume.
Readers frame these as earned: *"the heat chapters have banked enough trust that
I'll happily take a breath"*; *"'Listen to you' did more for the love story than
a sex scene would have"*; *"a quiet chapter that's actually load-bearing."*

**The adjacent-dip stretches ch6–7 and ch12–13 were checked and cleared.** Six
of seven target gates report ALMOST-STOPPED *none*; the exception disqualifies
itself ("not that I'd quit"). Floor 6, immediate rebound both times (ch8 8/9/9,
ch14 9/9/8). Meanwhile the **control** craters to 4–5 across exactly those
chapters — the wrong reader repelled by the courtship where target readers stay
engaged, which is the filter working. Both stretches sit inside ch5–17, the
volume's longest heat-free run before `famished`; ch11 `leave-no-trace` scores a
**10** between them, so the stretch is building appetite, not sagging.

## Reading a complaint against a high score — the dip rule's inverse (recorded 2026-09-12, at author request)

The dip rule above handles low scores. This handles the opposite and more common
case: a reader who scores a chapter 9 or 10 **and files a complaint anyway.**

**The score sets urgency, never validity.** CAPTURE and NEXT measure pull; a
complaint is content. A 10 does not mean defect-free — it means the defect did not
cost the page. The instrument only measures the first claim, so a high score never
clears a flagged line.

**1. Classify before weighing.** Four kinds, opposite handling:

- **Appetite** — *"I'm keen for the Randi fallout, not another Pace worship
  crawl."* The engine working. Reads like a complaint, is a receipt. Never fix.
- **Craft** — *"ran the same gear nine times in a row"*; *"the kiss-and-feed
  rhythm started to feel procedural."* Actionable at any score.
- **Trust** — *"for one line the book asked me to just melt at the romance of it,
  clean, and I nearly…"* Highest priority regardless of score: the thesis is at
  risk, not a sentence.
- **Self-disqualifying** — *"not that I'd quit,"* or a complaint whose own WHY
  converts it to dread. `gpt-5.5 · consent-sensitive` quoted {{Still Life}}'s new
  last line as her closest-to-leaving moment, then explained it as *"the whole
  beautiful scene feels like a held breath, because secrecy is no longer just
  around Vee"* — the engine, not a defect.

**2. Weight by convergence, not by the attached score.** Three readers on one line
at 10/10 beats one reader at 5. Cross-**model** convergence outranks
cross-persona: personas share a prompt, models don't.

**3. Correct for lane before reading severity.** `gpt-5.6-sol` runs ~2.1 points
above `claude-opus-4-8` on identical prose and reports `ALMOST-STOPPED: none` most
of the time, so **sol complaining at all outranks opus complaining**, even though
opus's number looks worse. A grumble from a generous lane is the louder signal.

**4. An ALMOST-STOPPED attached to a high score is the single most valuable datum
the instrument produces** — no survivorship bias: the book held the reader
completely and still nearly lost her, at a line she will quote. Five readers
quoting *"Would you tell me, when you touch yourself thinking of me?"* while
scoring {{Grace}} a 9 matters more than any of the 9s.

**5. Only then use the score, for sequencing.** Same complaint at 10 = real, no
revenue at risk, fix it next time you're in the file. At 6 = fix before
publication. Anywhere in ch1–4 = fix now; no goodwill is banked.

**The inversion worth internalizing: a 10 with no complaint is the least
informative gate available.** Sol's four 10/10s on {{Still Life}} said only "didn't
lose her"; every usable finding that day came from the lane with the worst
numbers. That is the standing argument for keeping opus on the panel despite it
dragging every average down — and for reading a lane that stops complaining as a
lane that has stopped being useful.

**Structural corollary — capture silence is not craft clearance.** Complaints
harvested here should be triaged by the **cold-read** lane's standards, not this
lane's; the scores are capture data, the complaints are craft findings that
arrived in a capture wrapper. {{Grace}} is the proof: `consent-sensitive` — the
instrument built for exactly that problem — never flagged the un-asked
penetration in either version, while `gpt-5.6-sol`'s *cold* read caught it
cleanly and drove the revision. A chapter that the capture panel loves may still
be owed a cold read.

## Instrument revision + read-out discipline (author ruling 2026-09-11)

Prompted by the question of whether the breather drops were a misconfigured
instrument. Diagnosis from the full corpus (1,161 gates, 24 readers, ch1–68):
the readers are reporting **accurately** — nearly every dip gate volunteers the
design read in its own WHY with `ALMOST-STOPPED: none` (*"the quiet chapters are
load-bearing"*; *"I'd sit through ten of these chapters to get to that dinner"*;
*"a breather chapter with none of what I read for, but it's laying the table"*).
The problem was **single-channel measurement**, not persona error: CAPTURE asks
only *how hard did this chapter pull you*, so a table-setter's honest answer is
5–6 and the forward commitment the reader keeps volunteering has nowhere to be
recorded. `claude-opus-4-8·consent-sensitive` scored ch28 a **5** while writing
*"which is exactly why I turn the page."*

**Three findings that outrank the dips.**

1. **Lane offset dwarfs chapter effect.** Same persona, same prose, same prompt:
   `gpt-5.6-sol·queer-woman` mean **9.01** (floor 7 over 68 chapters) vs
   `claude-opus-4-8·queer-woman` mean **6.88** (floor 4). A **2.1-point** lane
   difference, larger than any chapter's deviation. **Raw CAPTURE is not
   comparable across lanes** — compare a reader only against her own mean.
2. **Not length, though length is confounded with it.** CAPTURE correlates
   **+0.44** with chapter word count across every reader, and the dips are the
   short chapters. But `{{Gone}}` (1,002 w) scores **9.2** and `{{Believe Me}}`
   (1,341 w) scores **9.3** — the two highest in the volume. Short-and-quiet
   dips; short-and-charged does not. The instrument does not penalize brevity.
3. **The actionable unit is the RUN, not the chapter.** Every reader complaint
   names run *length* as the limit, never the individual quiet chapter: *"two
   quiet chapters is my limit"*; *"I've now had four warm chapters running"*;
   *"three quiet chapters circling the same withheld word is right at my
   limit."* Nobody objects to a breather. They object to the third one.

**Change 1 — `NEXT` added to the gate block (additive).** `prompts/core-chapter.md`,
`core.md`, `core-volume.md` now ask, after CAPTURE: `NEXT: <0–10, how much you
want the next chapter right now>`, with an explicit instruction that the two
diverge **in both directions** (a quiet chapter can leave you keen; a hot one
can leave you tired of a pattern) and must not be averaged toward each other —
the both-directions framing is what keeps this from coaching leniency. The
discriminating signature: **low CAPTURE + high NEXT = a working breather; low +
low = a stall.**

CAPTURE keeps its name deliberately, so the existing 1,161-gate series stays
comparable. **No re-read or re-mint is forced:** `capture_dag.run_reader` skips
existing gates and checkpoints by *file existence* (`capture_dag.py:153,167`);
the `prompt-sha` in each header is provenance only and is never compared. Gates
minted before this change simply carry no NEXT, and `capture_stats.py` prints
`—` for them. Mixed-format gates are safe in mints too — `core-mint.md` reads
gate notes as prose and parses no fields.

**Change 2 — personas given the pacing habits of their own shelf.** The persona
docs were pure *appetite* (what she wants, what makes her leave) with nothing
about **structure**, so all five reacted to a breather identically — as "none of
what I read for" — when a literary reader and a KU binge reader in fact have
opposite habits. Added, in each voice: `romance-graduate` reads shape from
hundreds of books, knows a bridge chapter and doesn't resent one, notices the
*second* in a row, and has never read a two-page chapter so has no habits for
it; `fsog-refugee` reads in long sittings and measures patience in chapters
rather than pages, tracking how long since the two of them were alone in a room;
`consent-sensitive` does her *best* reading in the lulls (framing shows plainest
with no heat to hide inside) and is lost instead by unexamined warmth;
`dark-romance-control` reads fast and forward, and a quiet chapter is an
off-ramp; `queer-woman` has no quarrel with stillness but keeps **stillness and
deferral apart**, and does not charge impatience about the second to the first.
This is a *fidelity* fix, not leniency — it should make run complaints sharper
and single-breather noise quieter.

**Change 3 — read-out discipline, enforced by `tools/capture_stats.py`.**
Replaces ad-hoc analysis. It reports per-reader mean/sd/floor (labeled
*lane-relative, do not compare*), per-chapter mean CAPTURE **and mean z against
each reader's own distribution**, mean NEXT where present, and detects runs of
consecutive below-own-average chapters — flagging LENGTH ≥3, DEPTH ≤ −1.5,
target-reader exits, sagging NEXT, no measurable rebound, and free-sample
position. `dark-romance-control` exits are tagged and excluded from the exit
count: she is the WRONG reader and her exits are the filter working.
`--chapters 52-55` zooms a stretch with the WHY text attached.

Standing rules: **(a)** use z, never raw scores, for any cross-lane or
cross-chapter comparison; **(b)** a breather with `ALMOST-STOPPED: none` is
healthy per the 2026-09-10 ruling above; **(c)** triage stretches of 3+, not
single dips.

**A run needs a deadband** (author correction 2026-09-11, `--deadband`, default
0.35z). A bare `z < 0` test recruits chapters sitting *at* baseline into a run
and inflates its length. `{{Missed a Spot}}` (z **−0.11**, raw 7/8/9, every gate
enthusiastic — *"the one thing I've been waiting the whole book to see done
right"*; *"I am exhilarated by her appetite"*) was padding a 2-chapter softness
into a reported 4-chapter stretch, and its two flagged exits are dread rather
than off-ramps (*"Randi would know what to make of it"*). **A chapter within
±0.35z of its readers' own mean is at baseline, and baseline breaks a run.**
Deep-but-isolated chapters are reported separately as SOLO DIPS, judged by
rebound rather than length.

**Runs in the drafted corpus, corrected** (z = mean deviation from own reader
average): ch6–7, ch9–10, ch12–13, ch19–20 (all 2-chapter, cleared above);
**ch40–41** (−0.65 → −1.05, rebound +1.76); **ch53–55** (3 chapters, −1.86/−1.77
at `unpacking`/`across`, rebound +2.75). ch35–37, ch47–48, ch52–55 and ch62–63
dissolve under the deadband — they were baseline chapters recruited by adjacency.
Solo dips, all healthy: ch16 `turned-up` (−1.13, rebound +2.01), ch28
`hills-and-valleys` (−1.65, +2.44), ch36 `school-nights` (−1.67, +1.35).

Note ch52–68 is measured by **`queer-woman` on three lanes only** — one persona,
so it is weaker evidence than Volume One's 20+ readers per chapter, and wants the
full panel before any structural change.

### Validation of the revision (2026-09-11, `romance-graduate` on Volume Two)

Ran the revised prompt + persona on `claude-opus-4-8`, `gpt-5.6-sol`, `gpt-5.5`,
`glm-5.3` from ch52 forward (a single-chapter smoke test at ch52 first; all four
lanes emitted a parsable NEXT).

**`NEXT` discriminates, and the tie at ch52 was not anchoring.** The
CAPTURE→NEXT gap scales with how much of a breather the chapter is:

| ch | title | CAPTURE | NEXT | gap |
|----|-------|---------|------|-----|
| 52 | `{{Missed a Spot}}` | 8.50 | 8.5 | 0.00 |
| 53 | `{{Back}}`          | 7.75 | 8.5 | +0.75 |
| 54 | `{{Unpacking}}`     | 6.25 | 7.5 | +1.25 |
| 55 | `{{Across}}`        | 6.00 | 8.5 | +2.50 |

On the charged chapter all four readers tied CAPTURE and NEXT exactly (7/7, 8/8,
9/9, 10/10) — a legitimate tie, since both answers are high. On the breathers
they separate, monotonically. **CAPTURE ranges 6.0–9.5 across ch52–68 while NEXT
never drops below 7.5** — the deepest-pull chapter in the volume (`across`,
opus CAPTURE **4**) carries NEXT **7**. That is the working-breather signature,
now measured rather than inferred from free text.

**Consequence for ch53–55.** The dip is *deeper* than `queer-woman` showed
(z −2.28 / −2.47 at `unpacking` / `across` vs −1.86 / −1.77) **and the retention
risk is nil.** Two independent channels now say the same thing the 2026-09-10
ruling asserted. No action on those chapters.

**Two inversions — a signal the single-channel instrument could not see.** On the
completed four-reader run, ch62 `{{Hangover}}` (CAPTURE 8.50 / NEXT 7.50) and ch64
`{{Still Life}}` (9.00 / 8.00) are the only chapters where NEXT falls a full point
*below* CAPTURE: they read hot and do not pull forward. Everywhere else in ch52–68
NEXT meets or exceeds CAPTURE. Worth watching as a pair, since they sit in the same
stretch — but note neither is a dip by CAPTURE, so no amount of re-reading the old
series would have surfaced them.

**End-of-draft dip:** ch67–68 (`{{Coming Due}}` −0.92, `{{Some of Mine}}` −1.38)
falls below baseline with **no rebound measurable** — the drafted corpus simply
ends. NEXT is 8.5 on both, so this is the draft edge rather than a finding; re-check
once ch69 exists.

**The persona pacing habits changed reader behavior.** Structural vocabulary
("bridge chapter", "quiet chapter", "breather", "third quiet chapter running",
"calm-before", "I can read the shape", skimming) per gate, `romance-graduate`
before vs after: opus 0.18 → **1.00**, glm 0.12 → **0.47**, and **sol and gpt-5.5
went from zero hits in 51 chapters to 0.33 and 0.29** — despite Volume One
containing plenty of breathers (`hills-and-valleys`, `school-nights`, `cropped`)
where they never reached for it. opus now counts the run out loud (*"Genuinely
the third quiet chapter running"*) and reports **skimming** at ch55, which is the
behavior the added text predicts; it reads a bridge as earned rather than as a
defect (*"A true bridge chapter that earned itself… I'm not tired; I'm leaning
in"*). Partly confounded by ch53–55 being more breather-dense than the Volume One
average, but the two zero-baseline lanes make content alone an insufficient
explanation.

**Run state:** all four readers complete through **ch68** with `ck-ch060` minted,
no STOPs. The ch53–55 run finishes at depth **−2.51** with the **largest rebound in
the corpus, +3.09 at `{{Covering}}`** — the gradient's payoff chapter. Two channels
and the rebound magnitude now agree that the stretch is setup cost, not sag.

## `dark-romance-control` retired from running (author ruling 2026-09-12)

**Do not run her again.** She is the WRONG reader — a book that captures her is
failing the repel goal, so her STOPs were the success condition, and she has
delivered it: `claude-opus-4-8` **STOPPED at ch021**, `gpt-5.6-sol` **STOPPED at
ch006**. The lanes that never stopped (`gpt-5.5`, `glm-5.3`, both parked at ch049)
sat permanently behind the rest of the panel, so every "catch the panel up to
chapter N" scope carried ~24 calls of control catch-up for signal already banked.

Enforced in `capture_dag.py`: removed from the default `PERSONAS`, listed in
`RETIRED_PERSONAS`, and a run that names her **exits with an error**. She stays in
`ALL_PERSONAS` so `--assemble` can still build her historical record, and **all
existing gates, checkpoints and STOPPED markers are kept** — the stops are data.
Reviving her needs explicit author approval.

The default panel is now the three target readers: `romance-graduate`,
`fsog-refugee`, `consent-sensitive`. `queer-woman` remains opt-in.

## Vendor comparison for the DAG lane (2026-09-10)

`capture_dag.make_agent` previously handled only the claude and codex lanes —
every OpenRouter model fell through to codex, so the paid models could never run
the capture DAG. An **OpenRouter branch** is now wired in (`OPENROUTER_MODELS`,
`OR_MAX_OUTPUT=16000`, `OR_TIMEOUT=900`), effort `low`.

Measured per-reader volume: **1.47M input tokens** for a full volume (1.22M in
the 50 chapter packets + 251k in the 5 decade mints); visible output only ~70k
(gates ~1,034 tok, checkpoints ~3,607). Input is ~95% of spend, so input rate
dominates. Four-persona volume at moderate reasoning: **gemini-3.8-flash ~$7.5,
glm-5.3 ~$8.8, kimi-k3 ~$24**. For contrast the **Fable subscription lane could
not complete four reads of one chapter** ("You've reached your Fable limit").

**Verdict: glm-5.3 is the DAG workhorse.**
- **Reliability.** GLM: 200 gates + 20 mints, zero malformed responses.
  Gemini-3.8-flash: **2 malformed gates in 20 chapters (~10%)**, at ch07 and
  ch19 — not refusal or context overflow (a diagnostic re-call handled the same
  35k packet cleanly), just intermittent formatting. A malformed gate aborts the
  whole reader, so this needs manual resumes at ~10% of chapters.
- **Discrimination.** Same persona, same 20 chapters: GLM mean 8.16, sd 1.09,
  range 6–10; Gemini mean 8.94, sd 0.78, **floor 8**. A reader that never drops
  below 8 cannot tell you where the book loses people.
- **Long context is fine for both** — the recurring 40k-class packets (max
  45,195 tok) caused no degradation; Gemini's ck-ch010 was the richest of the
  three. The flash-tier worry did not materialize on memory quality.

**Caveat — STOP behavior is model-specific.** GLM's dark-romance-control read all
50 chapters, where opus's stopped at ch20 and sol's at ch6. It still *registered*
the repulsion (mean 7.56 vs ~8.37 for targets, the only persona hitting 4s and
5s, lows exactly on the courtship/campus chapters). Compare controls on their
**capture curves**, not on whether they quit.

## Fifth persona — `queer-woman` (added 2026-09-10)

`personas/queer-woman.md`. **Selectable, not in the default panel** — a bare
`capture_dag.py` run still executes only the original four, so nobody silently
opens a fresh 50-chapter read on a subscription lane; opt in with
`--personas queer-woman`.

**Why she exists.** Vol 1's queer content is entirely oblique — Randi's want for
Vee is on the page from ch3 (the *"taste another woman"* orgasm, the bare
*"Yes"*), plus the goodbye-kiss staircase, the glaze on the lip, and the ch49
scent beat — while **Vee never once cognizes attraction to a woman**; the gates
are Vol 2/3. So she tests the *setup*, and above all the risk canon already
guards against in `meta-note-taste-thread.md`: that Vee's queer arc, being
engineered by two people with a plan, reads as **desire installed in her rather
than hers** (the conversion-narrative shape). Secondary: whether Randi, the one
character with queer desire, reads as the predatory-queer type.

**Design rule — keep her experiential.** Never ask a persona to assess
representation; the moment a reader is invited to *evaluate*, models drop out of
reader register into critic register and return a diversity audit instead of a
felt read. Ask *did you see it before she did / did you want it / did it feel
like hers*. Her wariness is written as **had, not performed**, and she is
explicitly able to be turned on by something she has reservations about.

**Run 1 (2026-09-10, opus + sol + glm, full volume).** All three finished 50/50,
no failures. **The persona is the most model-split we have measured** — sol
8.90 (7–10), glm 8.34 (7–9), **opus 6.82 (4–9)**, the last running 1.5 points
under its own romance-graduate and posting the lowest target-reader scores in
the corpus. One model alone would have reported either delight or bare
survival; identity personas *require* the cross-vendor panel.

**Finding — the tripwire clears: her desire is hers, convergent across all
three.** Sol's ck-050 on the ch50 coat: *"Randi supplied the proposition, but
Vee possessed it: chose her face, chose her shoes, touched herself, denied
herself, drove out, opened the coat… Her desire was not installed."* GLM
independently: *"the mirror scene was all Vee: her own hands… stopping
unfinished because 'it was not hers to finish.'"* Opus held the question as its
standing test — *"the line I've stood on the whole book: hers underneath or
installed"* — and ends holding both readings, which is the designed
irresolution, not a failure.

**Finding — what thins her is Pace, not the queer content.** Opus's lows are the
breather chapters and the complaint is consistent: ch40 *"runs entirely on the
couple I'm least invested in and on Pace's technique-as-love, which I've had my
fill of"*; ch35 *"a lull built entirely to make me love the man I refuse to
trust."* She stays for Randi. The volume's Pace-heavy stretches are where this
reader thins — not the almost-and-never fatigue that was expected.

**Next.** The real gates are Vol 2/3 ({{Missed a Spot}}, {{Boyfriend}}'s *"I'm
not gay"*, {{First Taste}}, the threesome). Re-run her against Vol 2 when that
draft exists; this run is the baseline.

## Cleanup EXECUTED 2026-09-08 (author-confirmed)

Deleted per the plan below: `dag-v1-terse/` trees and all single-go
`<persona>--volume.md` files. Kept: funnel interviews, 4-chapter run-1
outputs. `--volume-dag.md` records re-assembled from the v2 gates including
the final ch-32. (Deleted material remains in git history.)

## ~~Pending~~ cleanup plan (author, 2026-09-07 — executed above)

The first full-volume round is superseded: the single-go arm compressed 50
chapters of reaction into one output per reader, and the DAG v1 gates were
spec'd too terse. **After the `capture-dag-v2-rich` runs complete and are
verified:** delete `<model>/dag-v1-terse/` trees, the stale v1-assembled
`<persona>--volume-dag.md` records (re-assemble from v2), and the single-go
`<persona>--volume.md` files. **Keep:** the `--volume-interview.md` funnel
interviews (the comeuppance evidence — their findings and the run-2 numbers
above stay recorded in this SPEC even after their source records go), and the
4-chapter run-1 outputs. Do not execute before author confirmation on the day.

## Lane-blindness verification (canary probes, 2026-09-07)

Both lanes probed empirically with test-probe system prompts asking for an
exhaustive inventory of visible context. **No global `~/.codex/AGENTS.md` or
`~/.claude/CLAUDE.md` exists on this machine.** Codex lane (Sol/GPT-5.5):
clean — sandbox/tooling scaffolding only; no user identity, no project files,
no book information. Claude lane (Fable/Opus): **no project CLAUDE.md, no
memory, no repo skills, no book content** — but the CLI injects harness
scaffolding (tool/agent/global-skill lists, current date) **and the account
userEmail (`jeff.benshetler@gmail.com`)**. That email is the one boundary
leak: identity metadata, not book content, and it is a longstanding property
of the entire clean lane (same invocation as the cold-read corpus, author
ruling 2026-08-22) — documented here rather than silently accepted. Readers
receive nothing else beyond the packet the harness builds.

`reviews/capture-panel/<model-id>/<persona>--<arm>.md`. Not indexed by `na.py`
(no `## Reader reaction` section — instrument output, not a cold read).
