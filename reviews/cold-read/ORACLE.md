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

- **`pov-reliability`** — does the reader *discount* a POV character's feeling-colored
  read of others? Measured as **narrator-trust, not craft comprehension** (asking "do you
  understand POV is colored" is leading, hits a ceiling, and breaks the naive stance). The
  probe closest to that line — trust the **neutral** tier and the delta.
  - *neutral:* "When you're inside a character's head and they're describing someone they love or want — Vee on Pace, or on Randi — do you take that as how the person really is, or as colored by what the narrator feels? Walk me through how much you trust each viewpoint's read of the others."
  - *pointed:* "0–5: how much do you read each POV as feeling-colored rather than objective — a character who loves or wants someone seeing them more flatteringly, or more forgivingly, than they might deserve? (0 = straight truth; 5 = I constantly adjust for who's looking and what they feel.) Point to a place you caught yourself doing it."
- **`believability`** — do the mains read as real people vs. plot-constructs?
  - *neutral:* "Do these people feel like real people to you, or like constructions in a scheme? Anyone ring false, anyone especially alive?"
  - *pointed:* "Rate how believable each is as a real person — Vivienne, Randi, Pace — 0–5 (0 = a device/plot-construct; 5 = utterly real). One line each on what makes them ring true or false."
- **`identification`** — could the reader see themselves making the same choices in the
  character's circumstance? The **thesis-carry / reader-complicity** probe. Cross-read
  against `sympathy`: high-sympathy + low-identification = reads as someone it happens
  *to*, not a mirror (thesis failing, esp. for Pace); sympathy ≈ identification = reader
  implicated. Deepens across later volumes as the full deception lands.
  - *neutral:* "Put yourself in each of their shoes. Do you get why they did what they did — could you see yourself doing the same in their situation?"
  - *pointed:* "For each — Vivienne, Randi, Pace — 0–5: how much could you see yourself making the same choices in their circumstances? (0 = alien to me, I'd never; 5 = honestly, I'd probably do the same.) Name the one choice that most tests your answer."
- **`arms-length`** — the reader's **stance**: held at a distance, or drawn in / taken in alongside Vee? The complicity axis from the reader-position side (pairs with `identification`).
  - *neutral:* "As you read, did you feel like someone watching these people from the outside, or like someone being drawn in with them? Was there anyone you kept at a distance the whole way?"
  - *pointed:* "Pace and Randi specifically — could you hold them at arm's length, or did they get past your guard and pull you in the way they pull Vee in? 0–5 each (0 = stayed an observer; 5 = completely got past me), with what did or didn't let them reach you."
- **`professor`** — the statistics professor / his lectures as an author–reader **wink**: did the joke land, and hold or wear thin across his ~4 appearances?
  - *neutral:* "Anything that read as a running joke or a wink — aimed over the characters' heads, at you? Anything you caught yourself smiling at on a second or third appearance?"
  - *pointed:* "The stats professor and his lectures (the paradox, the codes, the outliers) — how did he land the first time, and had that changed by the third or fourth? Straight device or joke/wink; if a joke, enjoyed or worn thin? 0–5 on how much you enjoyed him by the end, with what changed your read."

### Grounded panel — oracle at end-of-book

For the **grounded** panel (`SPEC.md`, "Grounded read (v3)") there is no carry-forward
chain. To interview a finished reader, feed it its **own 50 chapter reactions** (its whole
reading record) as memory — richer for felt probes than the neutral checkpoint — via a
sandboxed packet: `cold_read_grounded.py --model-id <id> --emit-oracle-packet <probe>
<tier>` mints it (jacket + reactions + the tier question), and a `blind-oracle-grounded`
subagent reads it and self-persists the answer to `<id>/oracle/<probe>--<tier>.md`. Same
tiered funnel (neutral, then a **fresh** pointed spawn), same blindness (packet-only, no
`meta/`), free on the subscription. Blindness stakes are lower here than mid-book (the
reader has finished; there is no future prose to protect — only `meta/` to avoid).

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

## Cross-harness / multi-model (GPT, Grok, …)

The oracle generalizes to **any** model that has a cold-read chain, the same way the
cold read does (SPEC.md). Three files are **shared and model-agnostic** — one copy each,
never per-model:

- `oracle-battery.json` — the probe questions (machine-readable; this doc is its mirror).
- `oracle-persona.md` — the verbatim system prompt + jacket every harness sends.
- `oracle-runs/<runid>.json` — a reproducible run manifest.

Only two things are keyed by model, via `{model}` templating: the **input**
(`reviews/cold-read/{model}/{stage}.md` → its `## Carry-forward state`) and the **output**
(`reviews/cold-read/{model}/oracle/…`). Model ids are the **versioned `<model-id>`** from
SPEC.md (`claude-opus-4-8`, `gpt-5.5`, `grok-4.5`, …) — the same string names the chain
dir, the oracle dir, and the entry in a run's `models` list.

A run manifest lists **all** target models; **each harness runs only the ids it can
spawn** (the Claude command runs `claude-*` over their carry-forwards; an external harness
runs its own model) and skips the rest — exactly as SPEC.md splits the cold read. Every
harness: loads the shared battery + persona, reads the stage's carry-forward from its
model's chain, runs the tiered funnel **tool-free** (neutral, then a **fresh** pointed
call), and writes `{stage}--{probe}.md` under `{model}/oracle/`. Because filenames and
format are identical, results across models are **drop-in comparable** — set the opus,
gpt-5.5, and grok-4.5 files for a probe side by side and read the spread. A model whose
chain isn't finished yet (e.g. grok mid-run) is simply `pending` in the manifest until
`reviews/cold-read/{model}/{stage}.md` exists.

## Contract

- Read-only: the oracle never writes to `scenes/`, `meta/`, or the cold-read **chain**
  files — only under `oracle/`. It advances no carry-forward.
- Same **blindness tripwire** as the cold read: the `blind-oracle` spawn must return
  `tool_uses: 0`; any tool use voids that answer (the reader may have reached outside
  its memory).
- These are *reactions*, not canon. A probe result is evidence about how the book
  lands, never a fact about the book.
