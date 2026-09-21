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

| Chapter | Swept | Findings | State |
|---|---|---|---|
| the-bench | 2026-09-20 | 87 open | **swept, none ruled** |

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

1. Rule `the-bench`'s 87 findings with the author, hardest first
   (`audits/reading-effort/the-bench.md`). Use
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

## Rulings

**None recorded yet.**
