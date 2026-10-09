---
name: wals-explain-audit
description: >-
  Hunt the explain-after-showing defect — a line that stops and states what the
  prose just enacted — across a volume or a chapter range, harvested from the
  reader corpus rather than by re-reading. Classifies each candidate against the
  settled triage rulings and the complaining lane's CAPTURE score before
  surfacing it, then walks survivors past the author one at a time with a
  suggested fix (usually a cut). Flags and proposes; applies only what the
  author rules. Use when the author asks for an explain/over-explain/caption
  audit, or asks where the book explains itself.
---

# wals-explain-audit — where the book explains what it already showed

The defect: a sentence that **names the mechanism the preceding beat performed**.
The prose shows, lands, and then glosses. Readers describe it in their own words
when they hit it — *"the book cleared its throat and said it again"*, *"you don't
need to caption him for me"*, *"explaining Randi when her flinch had already done
it"*, *"the italics explaining to me a thing the two breaths had already done"*.

Flag, never fix. The author rules on every item.

## Why harvest instead of read

Readers name this defect unprompted and in quotable language, so the corpus turns
an unbounded re-read into a finite candidate list. **Known blind spot: it only
finds what somebody said out loud.** Vol A's `gone` had three instances found by
eye and the corpus flagged none of them. Treat the harvest's output as a floor,
not a census, and say so when reporting.

## Step 1 — harvest, scoped correctly

Bind the gate number to the chapter. A bare glob over `gate-*.md` matches every
chapter's gates for every slug and produces pure noise.

```
PY=<uv capture-dag interpreter>
$PY - <<'PY'
import sys, subprocess, glob, re
sys.path.insert(0,'tools'); import capture_dag as d
slugs = d.slugs()[FROM-1:TO]          # the chapter range
pat = (r"explain|spell(ed|ing)?\s+(it|them)?\s*out|didn'?t need|"
       r"already (shown|showed|told|knew|felt|said)|on the nose|underlin|"
       r"belabou?r|glosse?[sd]?\b|over-?stat|says the quiet part|"
       r"tells? me what|trusted? me to|caption")
for i, s in enumerate(slugs, FROM):
    files = (glob.glob('reviews/cold-read/*/%s.md' % s)
             + glob.glob('reviews/capture-panel/*/dag/*/gate-ch%03d.md' % i))
    ...
PY
```

**Only `*/dag/*/gate-chNNN.md` and `reviews/cold-read/<model>/<slug>.md` count.**
`--jacket.md`, `--volume*.md` and `--cold.md` files are other instruments; a quote
mined from one and presented as a gate finding is a fabricated convergence.

Most hits will be **praise** for the book not explaining. That is the expected
shape and it makes the real complaints easy to isolate.

## Step 2 — kill the false positives BEFORE presenting

Two checks, both cheap, both mandatory. Skipping them produced a 40% false-positive
rate on the first run of this audit.

**A. Read `meta/meta-triage-<slug>.md` first.** CLAUDE.md already requires this so
settled criticisms are not re-litigated. Look for the line under *Left standing* /
*do not re-litigate*, and for the same complaint under *Fixed* — a review file can
predate the edit that answered it. On Vol A this alone killed two of five
candidates, one protected by name and one already cut in response to that exact
reader.

**A protective ruling covers a passage; the test is narrower than that
(author ruling 2026-10-08).** A triage entry protecting a beat, a stretch or a
neighbouring line does **not** retire a candidate. What retires it is **the
flagged language itself being repeatedly praised.** So:

```
rg -n -o -i '.{0,70}<the exact flagged words>.{0,130}' reviews/
```

and read what comes back. Praise of *the words* disqualifies. A reader
**adopting** the phrasing as their own — carrying it into a later gate or into a
`ck-ch*.md` checkpoint — is the strongest disqualifier there is, stronger than a
compliment, because it proves the line travels.

This cuts both ways and both halves matter:

- `lesson:147`–`:151` — triage-protected *and* the words praised by name across
  four readers (*"the hair on my arms went up"*, *"the blurb's whole thesis in
  three lines"*). **Out.**
- `the-pointing-game:51`'s diagram — triage-protected, kimi quotes it as *"the
  book earned it"*, and opus-5 carried it into `ck-ch020`. **Out.**
- `lesson:145` — inside a protected stretch, but the sentence splits: the *tail*
  is what the triage quotes approvingly (*"nothing to do but take it"*) and the
  *head* is the flagged pointer, which draws one complaint and zero praise.
  **Live, and fixed by cutting only the head.**

So when a protected sentence is flagged, **test its clauses separately**. The
praised half and the problem half are frequently different halves.

**Weigh praise against criticism; do not just count complaints.** A convergent
complaint is not automatically a finding. Build both columns before deciding:

| weight | signal |
|---|---|
| strongest **keep** | the words carried into a `ck-ch*.md` checkpoint or a `core` ensemble claim set — the reader made it their own memory |
| strong keep | praised **by name** in several cold reads, across vendors |
| strong **cut** | complaints from several *different* personas and vendors |
| weak either way | several complaints from **one persona** or one model family |

**Read the instrument split.** The cold-read lane judges craft; the capture lane
judges pull. A line can be *symbol* to one and *thumb* to the other, and that is
not a contradiction to resolve — it is information. The worked case is
`outlier:95`, where **`claude-opus-5` calls the same clause "a gorgeous piece of
work" in its cold read and "tapped the glass for me… Don't do that again" in its
capture gate.** When a split like that appears, the line is usually doing its job
and annoying the reader who is being pulled rather than admiring.

**Also weigh what the line is structurally.** A chapter's last line, a title's
payoff, or a recurring symbol's home instance costs far more to cut than a
mid-paragraph gloss, because removing it takes the thread with it.

**When a candidate is withdrawn but the evidence has moved, record it.** A triage
entry that says "(lone)" and is now three readers should be corrected even though
the ruling stands — otherwise the next pass rediscovers it as new. Write the
convergence, the persona/instrument pattern, and the reason it survived.

**B. Score the complaining lane.** Per `reviews/capture-panel/SPEC.md`:

| signal | reading |
|---|---|
| ALMOST-STOPPED at CAPTURE 9–10 | usually **the most powerful line in the chapter**, not a complaint. Receipt. |
| complaint at a lane-low CAPTURE | genuine defect signal |
| `fsog-refugee` almost-stop on intimacy | **appetite** — receipt, never fix |
| `queer-woman` | deprecated as a tuning target; never a defect on its own |

Then classify per SPEC: **appetite** = receipt · **craft** = actionable at any
score · **trust** = top priority · **self-disqualifying** = noise.

Print the whole lane's scores for the chapter, not just the complainant's — a 5
among 8s reads very differently from a 5 among 5s.

## Step 3 — locate and verify the actual defect

Quote the passage and the beat it glosses. The finding only holds if you can show
**what already did the work**: the flinch, the ladle, the thermostat in the prior
chapter. If the preceding beat does not in fact perform it, there is no finding.

Watch for the two co-signatures:
- the gloss is often an **`x-not-y`** construction (the labelled diagram), and
- the paragraph **keeps talking past the reaction** that already landed.

## Step 4 — one at a time, with a suggested fix

Present a single finding, then **stop and wait for the ruling.** Each one gets:

1. the reader quote in full, with model·persona and the CAPTURE score
2. the passage, and the earlier beat that already did the work
3. **a suggested fix, usually a cut** — the gloss adds no information
4. **what the cut costs**, named honestly: often the most quotable line in the scene
5. numbered options, typically: cut whole · trim to the load-bearing clause · leave

Default to the **cut**. These sentences read as the best prose in the paragraph
precisely because they are the thesis stated cleanly; that is what makes them
captions.

## Step 5 — after each applied edit

Lint the chapter (`tools/novel-assistant/na.py style scenes/<slug>.md`) and confirm
no new hit lands on changed text. Cutting a gloss frequently clears a lint hit too —
the linter is often finding the same seam from the other direction.

Record rulings in `meta/meta-triage-<slug>.md` (or the scene's note) so the next
pass does not reopen them — including the **declines**, with the reason.

## Reporting

Give the author the hit rate and the blind spot, not just the findings. On Vol A:
five candidates, three real defects, two false positives from skipped checks, and a
chapter known to contain three more that the corpus never mentioned.
