# Reading effort — status, Volume One

Sentences that charge the reader more than they pay back: one idea split across
stacked subordinate clauses, or across a sentence boundary, where a
rearrangement would carry the same content at lower cost. Opened from human
reader feedback on `the-bench`, 2026-09-20.

Harness `tools/reading_effort.py` — deterministic, a fixed spaCy dependency
parse (`en_core_web_sm` 3.8.0) plus arithmetic over it. No model calls, no
tokens, no authorization needed. Per-chapter worklists at
`audits/reading-effort/<slug>.md`; author rulings at
`audits/reading-effort/rulings.toml`; parse cache at `cache.json` (gitignored
machine scratch, regenerable). Pass tracked in
`meta/meta-plan-editorial-checklist.md`.

**States:** `pending` → `swept` (worklist on disk, not yet ruled) → `reviewed`
(author ruled; fixes committed, standing items recorded in `rulings.toml`).

**Not a per-edit step (author ruling 2026-09-20).** Unlike the orphaned-reference
sweep, which is cheap enough to run on every edit, this is a deliberate sweep
only: it returns ~87 findings on one chapter and each needs a ruling. Running it
inside the drafting loop would swamp it.

## Discipline: flags, never findings

**The test for a single suspension (author ruling 2026-10-02).** A single
dash interruption is *earned* when what sits inside the dashes belongs to the
noun the sentence is holding — the foot → its arch and toes (`:269`), the
blanket → its provenance (`:465`), *her* → *not the face, with her* (`:521`).
The reader is still looking at the thing, not carrying it across something
else. It *costs* when the interruption is about something other than the held
clause, or when the resumption restates what was already said — the hair
(`:223`: held clause about his fingers, interruption about the hair, resumption
re-saying *her scalp*) and the shudder (`:447`: the material after the dash was
a separate verdict, not the clause's completion). The dash is the mechanism of
the hold, not a feature a fix "costs"; when the suspension is not justified,
removing the dash *is* the fix. Where a sentence is rebuilt, vary the structure
against its neighbours — `:223` sits in a run of nine *He + verb* openers, so
the hair led. The panel cannot see any of this (zero votes on every single
suspension); it is the author's test, applied by eye.

**High effort is frequently earned.** Suspension is a real device — the reader
holds the sentence the way the character holds still — the short verbless
sentence is this book's registering-beat, and the accretive tail is deliberate
voice. The tool over-flags on purpose; separating a load the prose earns from
one it does not is the author's ruling, never the tool's.

**Length is not difficulty.** Several of the highest-effort sentences in
`the-bench` carry no structural flag at all — they are long *coordinate*
sentences ("and … and … and"), high total cost purely from length and low
difficulty per word. They read fast and they are the voice. Hunting long
sentences would cut the easy ones and keep the hard ones.

**Scored against this book, not an external index.** Every figure is reported
against the corpus baseline of the other chapters, so "hard" means hard for this
author. Readability grade formulas (Flesch-Kincaid and kin) were considered and
rejected 2026-09-20: they are functions of sentence and word length only and are
blind to syntax, which is the whole defect class here.

## What it measures

Per-sentence costs off the parse — peak open dependencies (unresolved arcs
spanning any one point: the working-memory high-water mark), clause embedding
depth, depth reached *before* the main verb, mean dependency distance,
subject–verb gap, words before the main verb, prepositions in linear
succession — and eight flag classes:

| class | what it catches |
|---|---|
| `chain` | an idea passed down N clause levels, anywhere |
| `nest` | that stack sitting **before** the main verb |
| `front` | main verb arrives late: nothing dischargeable until it does |
| `hold` | peak open dependencies high: too much carried at once |
| `suspend` | a dash/paren interruption the main clause **resumes** after |
| `strand` | a modifier reaching back past an intervening clause to its head |
| `pp` | a string of prepositional phrases |
| `split` | a long verbless sentence, or a connective opener, after a long one |

**`hold` and `front` were one class (`load`) until 2026-09-20.** They proved
near-disjoint — on `the-bench`, 39 sentences fired on peak-open alone, 17 on
verb-delay alone, 3 on both — so the merged flag named *that* a sentence was
heavy while hiding *which kind*. Same objection that applies to a composite
score, one level down.

**The composite ranking is a judgement call and `--sort` exists to bypass it.**
The weights were set by feel; `--sort <metric>` ranks by any single axis
instead, which needs no such call. It matters: `--sort pp` surfaces sentences
scoring 1.5 on the composite that would never reach a top-20, e.g.
`the-bench.md:59`, five prepositions in succession at clause depth 1.

**`pp` measures linear succession, not structure.** Structural measures
(`pp_chain`, `pp_stack`) are computed but drive nothing — they miss "Slow along
her sides, from the hips up over the ribs under the cardigan and down again"
(chain 2, stack 2, run 4) while firing on "the small rise and fall of her
breathing in the hollow of her throat" (chain 3), which reads fine.

**The parser mis-roots long coordinate sentences, and `predelay` compensates.**
en_core_web_sm routinely picks a late verb as ROOT in this book's long
sentences and attaches the genuine opening main clause to it as `ccomp` —
`the-bench.md:131` roots on `went` at word 38 while the reader got "He led her"
at word 2. Taken raw, that reported right-branching sentences as steeply
left-branching: **15 of 20 `front` flags were artifacts.** `predelay` now takes
the earliest top-level predicate (ROOT plus `conj`/`parataxis`, plus any
`ccomp` that *precedes* its head, which is a parse error rather than a
complement). `advcl` is deliberately excluded — a leading adverbial genuinely
is subordinate, and that is the case `front` exists to catch. Where the parse
resolves no verbal ROOT at all, `nest` and `front` are suppressed entirely
rather than scored, since root position is their only input.

**Known gap: no cross-sentence referent tracking.** A pronoun held across
several sentences is invisible to this instrument, which is strictly
per-sentence. That gap matters most where this book is most exposed — any
chapter with Vee and Randi both present has two women sharing "she."

Plus a **fatigue profile**: ~220-word windows scored by effort per word, since
fatigue is cumulative rather than per-sentence, and a long chapter has more of
it to survive. Breathers (short or dialogue sentences) count in — they are the
relief that makes a passage survivable.

## Validation against a blind model panel (2026-09-20)

`tools/effort_blind.py` asks models which sentences were work to READ, knowing
nothing about how this tool measures anything. Five models — `claude-fable-5-1`,
`claude-sonnet-5`, `glm-5.3`, `gpt-5.6-sol`, `gpt-6-astra` — over `the-bench`
and `the-pointing-game`, 1,046 narration sentences. Ground truth: flagged by
**2+ of 5**. Leave-one-out, so no model is scored against itself.

**Per-class predictive power** (2+ readers, vs a 4% base rate):

| class | sentences | hit | vs base | |
|---|---|---|---|---|
| `chain` | 18 | 39% | **10.5×** | primary |
| `strand` | 16 | 31% | **8.4×** | primary |
| `front` | 12 | 17% | 4.5× | |
| `suspend` | 14 | 14% | 3.8× | kept anyway — see below |
| `split` | 19 | 11% | 2.8× | |
| `pp` | 30 | 10% | 2.7× | |
| `hold` | 56 | 9% | 2.4× | **demoted** |
| `nest` | 14 | 7% | 1.9× | |

**F1, leave-one-out:**

| | F1 |
|---|---|
| a single model | **0.41** |
| this tool, all flags | 0.17 |
| this tool, `chain`+`strand` only | **0.32** |

Three rulings follow, and are implemented:

1. **`hold` is demoted.** Largest class in the tool, near-weakest predictor —
   56 sentences of which 5 survive a two-reader test. Hidden by default with
   `nest`/`front`/`pp`/`split`; `--all-classes` shows them.
2. **The composite score is not a ranking.** F1 was flat at 0.19 across
   top-20, top-40 and all flags. Class membership carries the signal; the
   number does not. The report now says so in its own header.
3. **`suspend` stays in the default view despite scoring weakly.** The ground
   truth is model-derived, and a transformer attends over the whole sequence
   at once rather than holding a clause open as a human reader does, so it
   under-weights precisely this structure. Suspension is also what the human
   reader complained about — the reason this pass exists. Demoting it on LLM
   evidence would let the proxy overrule the thing it proxies for.

**Suspension re-scored by COUNT, not length** (same panel). `the-bench:9` —
two stacked interruptions, 19 words — was flagged by every reader, who each
described losing and re-finding the main clause. `:465` (one interruption, 26
words) and `:517` (one, 22 words) were flagged by none, despite being longer.
So `suspend_n` carries the weight and length is a small secondary term. Caveat:
this rests on three sentences; neither chapter uses stacked interruptions
often, and it needs a chapter that does.

**Panel-size finding.** A 3-model consensus agrees with the 5-model consensus
only 56% (Jaccard) and finds 19 of 34 sentences; 4 models reach 0.79. **Do not
run a 3-model panel.** Also `glm-5.3` failed on first attempt in 2 of 4 paid
runs (once truncated, once empty) and succeeded on retry both times — budget
for double.

**The standing gap: no human labels.** Everything above is proxy against
proxy. Five LLMs sharing architecture and training distribution agreeing with
each other is weaker evidence than the F1 figures suggest. The highest-value
next step is a blind human labelling of ~50 sentences, after which both
instruments can be evaluated against the thing actually cared about.

## Calibration against published work (2026-09-20)

Every other figure here is relative to this novel's own corpus, which can say
"heavy for me" and never "heavy for a published book." So: `the-bench`
(11,201 words) against a contiguous 11,212-word sample of **Antonia Angress,
*Sirens & Muses*** (2022), taken from 15% in to clear front matter.
`tools/calibrate_epub.py` does the extraction; the extract itself is
gitignored under `.calib/` because it is a copyrighted text — only these
derived numbers are committable.

**On average the two are the same book.** This is the headline, and it argues
against any general "simplify the prose" response:

| per sentence | the-bench | Sirens & Muses |
|---|---|---|
| peak open dependencies | 3.61 | 3.65 |
| mean dependency distance | 2.01 | 2.00 |
| subject–verb gap | 1.92 | 1.88 |
| clause depth | 0.82 | **0.92** |
| words | 16.3 | 15.0 |

**The difference is entirely in the tails, and in two specific structures:**

| flag | the-bench | Sirens & Muses | |
|---|---|---|---|
| `suspend` | **2.0%** | 0.6% | 3.3× |
| `hold` | **6.4%** | 2.3% | 2.8× |
| `front` | 0.8% | **2.5%** | 0.3× |
| `nest` | 1.4% | **2.2%** | 0.6× |
| `split` | 1.1% | **2.1%** | 0.5× |
| p90 sentence length | **38** | 30 | |
| prose inside a flagged sentence | **32.7%** | 17.9% | 1.8× |

Two conclusions worth holding on to:

1. **`suspend` is the finding.** It is the one structure where this chapter
   runs multiples above a published comp, it is what the human reader
   described, and it is what the blind readers converge on. Everything else is
   within, or below, published norms.
2. **Left-branching is not this book's problem.** Angress front-loads three
   times as often. A leading adverbial before the main verb is ordinary
   literary technique, and `the-bench` uses it *less* than the comp — so a
   `front` or `nest` finding here should clear a high bar before it is acted
   on. (This also independently supports excluding `advcl` from the
   main-predicate repair: had that exclusion been wrong, the-bench's `front`
   rate would have looked anomalous rather than low.)

Caveat: one comp, one sample, one genre-adjacent title. Treat it as a sanity
check on the thresholds, not a population statistic.

## Rulings are fingerprinted, and there is no "done" state

Findings key on `sha256("effort\x00<sentence>")[:12]`, the same scheme as the
style linter's `--ack` allowlist (`na.py::_fingerprint`), with the file path
deliberately excluded so a ruling rides with the prose and survives line shifts
and renames — and **re-arms when the sentence's wording changes**.

So there is one action and no bookkeeping: `--ack --fp <hash> --note "why"`
records a finding reviewed and **left standing**; `--unack --fp <hash>` reverses
it. A *revised* sentence fingerprints differently and drops off the worklist by
itself. Only the decision **not** to change something needs recording, so that a
later pass does not re-litigate it.

## Coverage

| Chapter | Swept | Tool, default classes | Panel convergent (2+ of 5) | State |
|---|---|---|---|---|
| the-bench | 2026-09-20 | 24 open · 1 standing | 18 open (2 at 4/5, 4 at 3/5) | **swept, 3 ruled** |
| the-pointing-game | 2026-09-20 | 16 open | 13 open (3 at 4/5, 4 at 3/5) | **swept, 1 ruled** |

Panel: `claude-fable-5-1`, `claude-sonnet-5`, `glm-5.3`, `gpt-5.6-sol`,
`gpt-6-astra`. Of the 31 open convergent findings, 8 are on the tool's default
worklist, 5 only in a demoted class, and **18 the tool cannot see at all**.

Chapter-level load, ranked by share of prose inside a flagged sentence
(`tools/reading_effort.py --corpus`), heaviest first:

| Chapter | Words | Flagged prose |
|---|---|---|
| vee-on-the-bench | 17,213 | 66.8% |
| barely-stings | 2,549 | 62.6% |
| the-induction | 1,402 | 62.2% |
| among-friends | 4,930 | 62.1% |
| missed-a-spot | 8,110 | 57.4% |
| … | | |
| the-bench | 11,201 | 29.2% |

75 chapters ranked (those with 20+ narration sentences).

`the-bench` is one of the *lightest* chapters in the book — 56th of 75 — and its
relief rhythm is normal (53% breathers against a 52% corpus average). Its median
window sits below the corpus median; what it has is length (second longest) and
a handful of genuine peaks. The reader feedback that opened this pass landed
there because it is the opening chapter, not because it is the worst.

**`vee-on-the-bench` is where length and density coincide** — longest chapter in
the book *and* densest — and is the obvious next sweep.

## Restart

1. Work the **convergent panel findings** first, highest vote count first
   (`tools/effort_blind.py <slug> --compare`, then the per-sentence list) —
   next up are the five at 4/5. Then the tool's default worklist
   (`audits/reading-effort/<slug>.md`). Use
   `tools/reading_effort.py the-bench --explain <line>` on any sentence whose
   numbers look high — the peak-open count mixes cheap local arcs with
   expensive long-range ones, and only the per-arc breakdown separates them.
2. Record standing decisions with `--ack --fp <hash> --note "why"`; fixes need
   no bookkeeping (the fingerprint re-arms).
3. Regenerate with `--save` after a ruling pass, and mark the row `reviewed`.
4. Sweep `vee-on-the-bench` next.

## Fixes applied

| Date | Location | Change |
|---|---|---|
| 2026-09-20 | `the-bench.md:49` | 41-word suspension unpacked into three sentences; 92 → 91 words, nothing cut; effort/word 3.43 → 2.27, peak open 8 → 6 |
| 2026-09-20 | `the-bench.md:47` | 5/5 readers. *the thing … the thing* clause recast (*what … that*), tail broken into finite sentences; effort 223 → 118 |
| 2026-09-20 | `the-bench.md:201` | 4/5 readers. One 71-word, three-dash sentence → four; supported/unsupported contrast kept in one sentence; effort 233 → 144 |
| 2026-09-20 | `the-pointing-game.md:143` | 4/5 readers. Unclosed aside closed, antithesis split across a sentence break, *is this one mine to take?* — mark added under the voicing rule; effort 184 → 49 |
| 2026-09-20 | `the-bench.md:9` (bag) | 4/5 readers. Two stacked interruptions → one, closed at a full stop; "and came into him" made its own sentence; nothing cut; effort 219 → 145, suspend 2× → 0 |
| 2026-09-20 | `the-bench.md:9` (face) | 4/5 readers. *which … which* chain broken at the eyes; stranded "being looked at for" given its object ("for them"); chain cleared; total effort flat by design — the fix resolves a tail, not load |
| 2026-09-20 | `the-bench.md:41` | 3/5 readers, tool-invisible. "a thing she said with a knife in it" → "a thing she had told him with a knife in it": the ambiguous *she* (mother or daughter) now resolves through *him*; the knife kept compressed by author ruling; *the one scale* left standing |
| 2026-09-24 | `the-bench.md:95` | 3/5 readers, tool-invisible. Bench geometry. **Superseded on merge (2026-10-04):** a parallel session rewrote the reveal (`102115c3`) so the geometry is read by *her* — *where her hips would lie, the highest point of her, held up. Her knees would go out and down from there. Her head would be down* — same shape the author ruled (fold at the waist, hips highest), better placed; my sentence dropped. Open flag on `vee-on-the-bench:87` (*level with the rest*) still stands |
| 2026-09-24 | `the-bench.md:95` | 3/5 readers, tool-invisible. Bench geometry. **Superseded on merge (2026-10-04):** a parallel session rewrote the reveal (`102115c3`) so the geometry is read by *her* — *where her hips would lie, the highest point of her, held up. Her knees would go out and down from there. Her head would be down* — same shape the author ruled (fold at the waist, hips highest), better placed; my sentence dropped. Open flag on `vee-on-the-bench:87` (*level with the rest*) still stands |
| 2026-10-01 | `the-bench.md:517` (looked past the face) | suspend 22w, 0 readers. Split at "— and": the *past/past/past* figure keeps its reach, then "And found her." stands alone and the italic *her* closes its own sentence. Suspension cleared; `pp` remains and is the figure |
| 2026-10-01 | `the-bench.md:517` (under the smile) | suspend 17w + 2/5 readers (glm: could not resolve *Under it*). Referent: "Under it" → "Under the smile" — continues the previous sentence's stacking image; *disjunction* kept once (twice read stiff; *gap* read body-spatial; *seam* is spent on her sex). Suspension released at the dash: "…in the same instant. And it had not come from her…"; the *ever —* breath kept |
| 2026-10-01 | `the-bench.md:223` | suspend 11w, open 9 — **standing** (author ack; see rulings.toml) |
| 2026-10-01 | `the-bench.md:521` | suspend 11w — **standing** (author ack: the interruption is the sentence's meaning) |
| 2026-10-01 | `the-bench.md:447` | suspend 18w, 0 readers. Split at the second dash: the shudder's path completes the withheld noun, then "It was not anything she could have produced…" takes the verdict as its own sentence; *shudder* no longer doubled |
| 2026-10-02 | `the-bench.md:223` (hair) | suspend 16w, 0 readers; the resumption restated *her scalp*. Dash removed (author: the dash IS the suspension, not a feature to preserve). Chosen for local variety — the surrounding run is nine *He + verb* openers and the prior sentence already has *he found* — so the hair leads: "Her hair was lighter and smoother than he had expected, …, as he let his fingers move through it to her scalp. He worked them there…" |
| 2026-10-02 | `the-bench.md:269` | suspend 16w — **standing** (author ack: arch and toes belong to the held foot) |
| 2026-10-03 | `the-bench.md:349` | suspend 13w — **standing** (author ack: the interruption is the hit itself; the chapter's strike shape) |
| 2026-10-03 | `the-bench.md:147` | suspend 12w, earned (the skin of the sides being swept) — left intact. The 73-word sentence seamed after the clasp: the sweep and the unhooking become two sentences; nothing cut |
| 2026-10-03 | `the-bench.md:149` | suspend 21w → 16w. Interruption earned (what he finds at the kiss); trimmed the excursion to the throat — "where she had dabbed it at the base of her throat" → "from the base of her throat" |
| 2026-10-03 | `the-bench.md:197` | suspend 10w — **standing** (author ack: the dashes are his reading of the held unsteadiness; the mounting is one motion) |
| 2026-10-03 | `the-bench.md:547` | chain 6 + strand, 0 readers. Seamed at the *and* (lying / thinking each get one subject) and the recursive tail unwound a turn: "what she was going to do about this" → "what to do about this" |
| 2026-10-04 | `the-bench.md:133` | strand ×2 + an unjustified 24w suspension, 0 readers. Dash removed; three sentences. **Fact fix found on the way:** "soft and heavy … the dense particular weight of real cashmere" had cashmere backwards (famously light and warm) and contradicted `missed-a-spot:207` (*almost no weight at all*) — now "soft and almost weightless in his hands, the particular lightness of real cashmere". "as he removed it" cut as redundant with *took off* |
| 2026-10-04 | `the-bench.md:295` | chain 5 + a 24w suspension the parser missed, 0 readers. Away / except / purpose were three things on one dash pair; now three sentences, the middle opening *Between strikes* for variety; *wetter* triple kept |
| 2026-10-04 | `the-bench.md:7` | chain 5 — **standing** (author ack: the opening sentence; right-branching, the tail is Pace by provision) |
| 2026-10-04 | `the-bench.md:69` | strand — **standing** (author ack: parser mis-attachment; the dash is a colon) |
| 2026-10-04 | `the-bench.md:137` | strand — **standing** (author ack: parser mis-attachment across a colon) |
| 2026-10-04 | `the-bench.md:157` | chain 5, 0 readers. Double relative on a stranded preposition (*a way … that she had not been looked at in before*) → "as she had not been looked at before"; paragraph's third *way* gone |
| 2026-10-04 | `the-bench.md:255` | strand (appositive pair across a colon-dash), 0 readers. Author's own cut: "…caught and then released. It was the laugh of a woman…" — the dash keeps the sound, the judgment gets its sentence, the period enacts the release |
| 2026-10-04 | `the-bench.md:471` | chain 4 on the smile — **standing** (self-correction, thought → known). Reader catch in the same paragraph, tool-invisible (sonnet, cost 1): *the sharp inner edge of it* — *it* read as the bottle, meant the cap → "of the cap" |
| 2026-10-04 | `the-bench.md:527` | chain 4, 93w, 2/5 readers (her smile held through his). One seam at the look: her sentence, then his; the performed/genuine contrast now one smile per sentence |

## Rulings

**None recorded yet.**
