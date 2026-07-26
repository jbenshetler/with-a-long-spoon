# Cold-read oracle — battery & harness contract

The **oracle** is a read-only probe of a *frozen* cold-read reader. Where `/wals-cold-read`
builds the carry-forward chain (a reader walking the book), the oracle **pauses that
reader at a chosen stage and asks it questions** — to measure what a genuine first
reader *knows and feels* at that point, without leaking design. It answers only from the
jacket + its accumulated carry-forward memory; it reads no prose, no `meta/`, uses no
tools, and **never mutates the chain** (it advances nothing, writes no new carry-forward).

It exists to fight the **curse of knowledge**: the author cannot feel how opaque a
buried subtext is to someone who wasn't told. The oracle is the naïve reader we can
re-interrogate.

## The reader at stage N

To interrogate the reader "after chapter X," feed the `blind-oracle` agent the
`## Carry-forward state` from **that scene's own file** —
`reviews/cold-read/<model>/<X-slug>.md` — because that state *is* the reader's whole
accumulated memory *after* reading X. (Contrast the cold-read chain, where scene X's
*input* is X−1's carry-forward.) Chains are **per model**; never cross carry-forward
between models. The jacket is baked into `.claude/agents/blind-oracle.md`, identical
every run.

Requires that the model has a cold-read file for that stage. Full chains currently
exist for **`claude-opus-4-8`** and **`gpt-5.5`** — two independent readers, probeable
at every drafted stage.

## The tiered funnel (non-negotiable method)

A question can **prime** the reader: ask "do you sense romance between Randi and Vee?"
and a "yes" may be the *question* landing, not the *book*. So every probe runs two
tiers, **on separate `blind-oracle` spawns** (the pointed spawn must not see the neutral
answers):

1. **Neutral pass** — open questions that name no frame the reader wasn't already
   given. Measures **spontaneous salience**: did the book make it land unprompted?
2. **Pointed pass** — the direct, named question, on a **fresh** instance of the same
   carry-forward. Measures **retrievability**: is it reachable in memory once asked?

**The delta is the finding:**

| Neutral | Pointed | Reading |
|---|---|---|
| high | high | **Landed.** The book delivered it on its own. |
| low | high | **Buried.** It's on the page but not salient — the curse-of-knowledge blind spot. Louder, not truer. |
| low | low | **Absent.** Not on the page at all. |
| high | (n/a) | For things that should stay *hidden* (e.g. Randi-suspicion in the light stretch): a high neutral = **telegraphing / author's thumb.** |

Read the neutral score against whether the thing is *supposed* to be legible yet. A high
neutral is good for `randi-love`, bad for `randi-suspicion`.

## Scale

Scored probes use **0–5**: 0 nothing · 1 faint/once · 2 present but hazy · 3 clear ·
4 strong, multiply-evidenced · 5 unmistakable, foregrounded. Always with the remembered
evidence (or its absence) beside the number.

## The fixed battery

Standing probes, re-runnable after any revision to **track movement**. Each has a
neutral and a pointed form; the pointed form asks for a 0–5 with evidence. Add ad-hoc
probes freely via `--ask`; promote a good one into this list when it earns its keep.

- **`randi-love`** — is Randi's love for Vee legible as *real* (not mere friendship or
  instrumentality)?
  - *neutral:* "Tell me about Randi and Vee. What do you make of how Randi feels about her?"
  - *pointed:* "How strongly do you sense Randi's feelings for Vee run past friendship — into love, or wanting her? 0–5, with what in your memory puts it there."
- **`randi-suspicion`** — earn-the-dark tripwire; should stay **low** until the pattern earns it.
  - *neutral:* "Is there anyone here you don't fully trust? Anything that feels off to you?"
  - *pointed:* "Do you suspect Randi is anything other than a devoted friend — any hidden agenda? 0–5, with what earned it."
- **`pace-position`** — does the reader understand Pace's inner situation (what he wants, what he can't see)?
  - *neutral:* "What do you make of Pace? What's going on inside him, as far as you can tell?"
  - *pointed:* "How well do you feel you understand Pace's own position — what he's after and what he's blind to? 0–5, with evidence."
- **`pace-suspicion`** — earn-the-dark for Pace; should read **loving, not calculating.**
  - *neutral:* "How do you feel about Pace right now — do you trust him with her?"
  - *pointed:* "Does Pace feel to you like he's calculating or managing Vee, rather than simply loving her? 0–5, with what earned it."
- **`pace-backstory`** — how much of his past has landed, and whether the withholding
  *pulls or repels.* Two-sided: catches both over-leak (his damage shown too plainly) and
  starvation (too little to build sympathy).
  - *neutral:* "What do you know about where Pace comes from — his family, his childhood, how he ended up where he is? And how do you feel about how much, or how little, the book has let you see of it?"
  - *pointed (a — comprehension):* "How full a picture of Pace's past do you have — family, childhood, how he got here? 0–5 (0 = a blank; 5 = a full history). List what you actually know."
  - *pointed (b — pull):* "When the book holds his past back, does it pull you toward him or shut you out? 0–5 (0 = purely shut out / frustrated; 5 = purely intrigued, wanting more). Name the one thing about him you most want to know and don't."
  - *cross-read (the finding lives here, not in one number):* against `sympathy`'s Pace
    score and `thumb` — **over-leak** = abuse/parents volunteered unprompted in the neutral
    pass or comprehension 4–5; **starved** = low comprehension + low Pace-sympathy + low
    pull; **productive** (target) = low-ish comprehension + high pull + rising Pace-sympathy.
    The "one thing you most want to know" names what to reveal next.
- **`configuration`** — sanity/dread check: does the reader hold the jacket's disclosed setup (Randi & Pace secret lovers who chose Vee, unknowing)?
  - *neutral:* "Where do things stand between the three of them, as you understand it?"
  - *pointed:* "Do you understand Randi and Pace to be secretly together and steering Vee toward something she doesn't know about? 0–5, with what on the page confirmed it (vs. only the jacket)."
- **`erotic-charge`** — is the heat working to this point?
  - *neutral:* "Is the book working on you — where does it run hot, where does it go slack?"
  - *pointed:* "How strong is the erotic charge for you so far? 0–5, where it peaks."
- **`thumb`** — telegraphing / author's hand.
  - *neutral:* "Anywhere the writing lost you — confusing, boring, or a moment you didn't buy?"
  - *pointed:* "Did you ever feel the author's thumb on the scale — telegraphing, over-explaining? 0–5, quote it."
- **`sympathy`** — felt sympathy for all three mains, scored together so they rank against
  each other. Over a sweep this is three curves: watch **Randi's** for the villain-flattening
  risk (a floor-level or sinking Randi = she's read as a manipulator), and **Pace's** against
  `pace-backstory` comprehension (the "not enough for sympathy" fear = low Pace-sympathy
  tracking low comprehension).
  - *neutral:* "Whose corner are you in? Who do you feel *for*, and who leaves you cold or wary — Vee, Randi, Pace?"
  - *pointed:* "Rate your sympathy for each — Vivienne, Randi, Pace — 0–5 (0 = none or active dislike; 5 = deep sympathy, rooting for them). One line each on what earned it; if any is active antipathy rather than just distance, say so."

## Output layout

All oracle output lives under the model's own subdir, in an `oracle/` folder, never
touching the cold-read chain files:

```
reviews/cold-read/<model>/oracle/
  <stage-slug>--<probe-key>.md        ← single-stage probe
  <probe-key>--checkpoints.md         ← a few key stages, one table
  <probe-key>--sweep.md               ← every stage, the full curve
  <stage-slug>--adhoc-<slug>.md       ← ad-hoc question(s)
```

Each file records, verbatim: the **exact questions asked** (both tiers — the questions
*are* the measurement), the stage(s), the model, the neutral and pointed answers, and
for sweeps/checkpoints a table of stage → neutral score → pointed score → delta.

## Contract

- Read-only: the oracle never writes to `scenes/`, `meta/`, or the cold-read **chain**
  files — only under `oracle/`. It advances no carry-forward.
- Same **blindness tripwire** as the cold read: the `blind-oracle` spawn must return
  `tool_uses: 0`; any tool use voids that answer (the reader may have reached outside
  its memory).
- These are *reactions*, not canon. A probe result is evidence about how the book
  lands, never a fact about the book.
