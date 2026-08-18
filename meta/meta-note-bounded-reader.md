# Bounded-memory reader — design note for consideration (2026-08-17)

Methodology note on a **third reader instrument** we do not yet have. **Not a
committed change — a design idea for Volume 2**, recorded so it isn't lost and so
the reasoning behind retiring the chained cold read survives. Companion to
[[meta-note-oracle-instrument]].

## Why neither current instrument measures the lull

The book's central craft rule is a claim about a *fallible* reader: a first-time
reader should fall for Pace and should **not** suspect the game until the pattern
earns it. Certifying that needs an instrument that reads the way a human reads.
Neither of the two we have does.

- **Chained cold read (retired).** Feeds chapter N the carry-forward of chapter
  N−1 — a summary of a summary, ~50 hops deep. It didn't decay like a human; it
  suffered lossy-codec collapse, dropping *load-bearing* facts a real reader never
  loses: that the brunette is Randi, that the redhead is Vee, that Vee and Randi
  had ever met, that Vee and Pace had slept together by the last decade of Vol 1.
  A chain that "doesn't suspect" **because it forgot who the brunette is** is not a
  fooled reader — it's a broken one. So its lull readings are false signal, not a
  soft version of the truth. Disqualifying; retired. (Migration: the live lane is
  now `reviews/grounded-cold-read/`; the chain is archived under
  `reviews/_archive/cold-read/`.)

- **Grounded cold read (current, valid, but harsh).** Reconstructs memory from
  ground truth every chapter — a grounded decade checkpoint plus the raw prose
  window since. Zero paraphrase hops, so it never loses a load-bearing fact. That
  makes it a sound **continuity / seed-audit** instrument and a *conservative* lull
  instrument: if even the perfect-recall reader is held to the reveal, a human
  certainly is. But it reads harsher than a human, and — the key finding below —
  the harshness is **not** mainly a recall artifact.

## The real bug in grounded: belief updating, not recall

Two observations, one diagnosis.

1. **The chain's harshness had a mechanical cause we can now name.** The cold
   readers were fed the **jacket copy in every chapter**, re-injecting the dark
   framing (it once included the word *trap*) on every hop. That kept the dark
   *prior* artificially fresh while the *facts* rotted — precisely inverted from a
   human, who retains the facts and lets an early blurb recede.

2. **Grounded doesn't counterbalance either.** Author's lived experience of the
   grounded reads: a softened reveal that Pace and Randi are running a game on Vee is
   **not** outweighed even by ~35 chapters of Pace being extremely good to Vee — not
   to the degree a human reader would weigh it.

**Correction (found while restructuring the harness, 2026-08-18):** grounded does
**not** feed the jacket once. `cold_read_grounded.py:160` (`build_prompt`) injects
the full jacket packet into *every* chapter read — deliberately, on the rationale
that "a real reader carries the cover + blurb the whole run" (it's marked *hold it
loosely*). So grounded's over-weighting of the dark prior is, at least in part, the
**same re-injection amplification** as the chain — not a subtle belief-integration
failure but a concrete, fixable prompt behavior. Each independent grounded chapter
re-reads the "game" framing at full strength with no decay, then weighs ~one chapter
of lived counter-evidence against it. No wonder the dark prior dominates.

Diagnosis, revised: two compounding causes. (a) **Re-injection** — the jacket is
re-fed at full weight every chapter; (b) **no belief dynamics** — even setting the
jacket aside, a perfect-recall reader has no recency/volume weighting, so an early
framing never fades in salience the way it does for a human living through 35
chapters. A human's *affect* (suspicion, affection) is recency- and volume-weighted;
grounded holds every input at flat, undecayed weight.

## The "heavy hand" problem — and the resolution

The author's worry: **by choosing what to forget, we lay a heavy hand on the
reader's judgement.** Correct — selective-by-valence forgetting (drop this dark
beat, keep that light one, or the reverse) is rigging the instrument. Any per-chapter
model curating *which memories survive* biases the suspicion reading by construction.

Three principles resolve it:

1. **Two stores, two laws — separate facts from feelings.**
   - **Fact ledger** (identity, first-meetings, relationship/sexual state changes,
     physical canon, promises): lossless, append-only, **never** forgotten. This is
     exactly what the chain catastrophically lost. Content-neutral *by type* — a
     fixed taxonomy applied uniformly, so nothing is chosen for retention per
     instance.
   - **Affect state** (suspicion-of-the-game, affection-for-Pace, unease): a small
     running estimate updated each chapter.

2. **Forget by attenuation, not erasure.** Don't delete anything — keep grounded's
   full lossless fact base. Weight each memory's influence on the *affect* state by
   a **content-neutral recency × salience** curve. Old framing is present but
   low-weight; recent lived chapters dominate. The only "choice" is one uniform
   decay curve applied to dark and light alike — the thumb comes off the scale
   because nothing is selected for deletion.

3. **The jacket is a prior, not evidence.** It should be a *discountable* prior
   whose influence decays as lived evidence accrues — the way a blurb read three
   weeks ago recedes against the book you're living in. **Both** current instruments
   get this wrong the same way: the chain re-injects it every hop, and grounded
   re-injects it every chapter (`build_prompt`, confirmed above) — neither decays it.
   The fix is a decay schedule on the prior's salience, symmetric with how lived
   evidence accumulates. **This is the single cheapest lever to test first** (see
   below): grounded already re-feeds the jacket at full weight, so simply tapering or
   dropping the packet on later chapters is a one-function change.

The structural insight: the chain collapsed because it forced *everything* — facts
and feelings — through one lossy summary channel. **Split the channels.** Grounded,
lossless facts + a *bounded, small* affect carry-forward (a few sentences: current
suspicion level, current affection, open questions). The affect carry-forward is tiny
and doesn't try to carry the facts, so it can't suffer summary-of-summary collapse.
Each channel uses the right mechanism.

## Why we'd want it

It is the only instrument that would measure the **actual experiential lull**: a
reader who remembers the facts (unlike the chain) but *feels* in recency-weighted
time (unlike grounded). Grounded gives a harsh upper bound on suspicion; the bounded
reader would give the realistic reading the book lives on — does Pace's accumulated
goodness outweigh a softened, one-time dark framing the way it should for a human?

## Cheapest path to try it

Likely **not** a new harness. Grounded already supplies the lossless fact base; the
delta is an **affect-integration protocol** layered onto the grounded reader
(`.claude/agents/blind-reader-grounded.md` + `tools/cold_read_grounded.py`):

- **The jacket lever has been pulled (author ruling 2026-08-18) — measure it next.**
  `build_prompt` no longer re-injects the jacket. The volume packet is now supplied
  **exactly once, at its opening chapter** (`opening_slug` in `volume-packets.toml`),
  never re-injected whole or thinned, enforced by an `assert_jacket_policy` guardrail
  that fails any read whose packet carries jacket text off the opening chapter. The
  **existing on-disk grounded reads predate this** — they were generated under
  every-chapter injection, so a fresh late-book grounded read is needed to tell whether
  removing re-injection eases the dark-prior over-weighting. If it does, re-injection
  was the dominant cause and the belief-dynamics work below may be unnecessary.
- Carry a small bounded affect state chapter-to-chapter (suspicion / affection /
  open questions), grounded facts still reconstructed fresh each chapter.
- Instruct recency-weighting explicitly: recent lived chapters outweigh early
  framing on matters of *feeling*, never on matters of *fact*.

If that retrofit closes the counterbalance gap the author observes, we have the
bounded reader without a third codebase. If it doesn't, the two-store design above is
the fallback build. Either way: **do not resurrect the chain.**
