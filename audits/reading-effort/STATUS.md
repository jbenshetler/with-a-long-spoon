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
only: it returns ~54 findings on one chapter and each needs a ruling. Running it
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

Five per-sentence costs off the parse — peak open dependencies (unresolved arcs
spanning any one point: the working-memory high-water mark), clause embedding
depth, mean dependency distance, subject–verb gap, words before the main verb —
and four flag classes:

| class | what it catches |
|---|---|
| `suspend` | a dash/paren interruption the main clause **resumes** after |
| `chain` | an idea passed down N clause levels |
| `strand` | a modifier reaching back past an intervening clause to its head |
| `split` | a long verbless sentence, or a connective opener, after a long one |

Plus a **fatigue profile**: ~220-word windows scored by effort per word, since
fatigue is cumulative rather than per-sentence, and a long chapter has more of
it to survive. Breathers (short or dialogue sentences) count in — they are the
relief that makes a passage survivable.

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
| the-bench | 2026-09-20 | 54 open | **swept, none ruled** |

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

1. Rule `the-bench`'s 54 findings with the author, hardest first
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
