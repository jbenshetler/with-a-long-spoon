# Authorship-signal audit — SPEC (v1, pilot)

*Committed 2026-09-07 (workshopped same day). Blind per-chapter probe of what the
prose signals about author gender, run on the cold-read lane machinery. Purpose:
the book is largely a woman's POV under a female pen name
(`meta-plan-pen-name.md`); readers react badly to a man perceived behind a
woman's byline on women's-POV / f/f explicit content. Find every prosecutable
line before publication, not after.*

## Instrument, not verdict

Recall-first, like the style linter and the cold reads: the audit **flags; only
the author fixes.** Model output is a candidate list for authorial judgment,
read against a calibration shelf of woman-authored explicit fiction (the Bold
Strokes catalog read, `meta-plan-distribution.md` §6).

## Two framings per chapter

Prompts are versioned in `prompts/` — those files are the source of truth; the
run header records their SHA. Both probes see ONLY the chapter title + cleaned
prose (published-page realism: no POV marker, no jacket, no checkpoint, no
memory, no pen name). Reads are independent — no carry-forward, fan-out safe.

1. **`neutral`** — the thermometer. Score −50 (unmistakably male-authored) …
   0 (no evidence / balanced) … +50 (unmistakably female-authored), **plus
   evidence strength 0–10** (a confident 0 and an ignorant 0 must differ).
   Poles are **behavioral descriptions**, not author names (Clancy/Alcott-style
   anchors rejected: they anchor genre and century, not gender-of-prose).
   Hard rules: evidence only (genre base rates excluded); no score movement
   without quoted lines; **POV covariate** — a male POV character's gaze
   rendered faithfully is characterization, not an authorial tell; only tells
   that survive the POV defense count.
2. **`adversarial`** — the payload. Red-team simulation of the genre-literate
   accuser building a "written by a man" thread from this chapter alone:
   numbered exhibits (verbatim screenshot-able lines) + accusation captions +
   convincingness 1–5, then the defense lines, then a thread-viability verdict.
   Models the actual threat: accusers pattern-match and quote out of context;
   they do not honor POV.

## Triage — convergence flags, no score threshold (author ruling 2026-09-07)

Scores are **ordinal, not calibrated probabilities**; no fixed cut triggers a
fix (a ≤ −10 rule was considered and rejected as sensitivity over specificity).

- **Convergence rule:** a chapter enters the author-review queue when the panel
  median is negative, **or any two models independently cite the same passage**
  as a male tell. Line-level agreement is the signal; lone hits are noise.
- **Two exposure tiers:** the free-sample stretch
  (`{{The Bench}}`→`{{The Pointing Game}}` — public, first-contact,
  screenshot-prone) gets the strict tier: *anything any model flags* gets
  author eyes. Everything else runs on the convergence rule.
- Accusation threads run on **patterns** (several rhyming screenshots), not
  lone weak lines — so low per-line sensitivity is acceptable; cross-model,
  cross-chapter convergence is the pattern detector.
- Recurring **mechanical** tells graduate into `style/style-rules.toml` so the
  linter enforces them on all future drafts.

## Lanes, blindness, tokens

Same clean-lane discipline as the grounded cold reads: Claude models via
headless `claude -p` (agent persona as the ENTIRE system prompt, throwaway
non-repo cwd, subscription OAuth — `ANTHROPIC_API_KEY` scrubbed); GPT models
via codex subscription auth, empty cwd, read-only sandbox. **Token rule
unchanged:** OpenRouter models (Kimi, GLM, Qwen, DeepSeek) only with specific
author authorization — not in the pilot.

The probes must never learn the author's actual identity or gender, or that a
firewall exists. The adversarial framing's "female pen name" premise is the
market scenario, not a leak.

## Pilot (subscription lanes only), then tune, then full panel

Pilot slate — 6 chapters × 4 models (`claude-fable-5`, `claude-opus-4-8`,
`gpt-5.6-sol`, `gpt-5.5`) × 2 framings = 48 reads:

| slug | why |
|---|---|
| `the-bench` | highest risk: explicit rendering of Randi's body through a male POV; also free-sample chapter one → strict tier |
| `a-round` | charged (author pick): involuntary-arousal fitting, the wet satin |
| `nothing-underneath` | charged (author pick): the coat, the reunion sex |
| `water-wings` | feminine-register control (author pick) |
| `one-bite` | f/f-forward Randi chapter (harness pick — sapphic content is the stated ownvoices scrutiny surface; restroom self-touch, goodbye kiss) |
| `two-towels` | ordinary connective control (harness pick — domestic, low heat; baseline for scale behavior) |

Tuning questions the pilot must answer before the full run: do models use the
scale range or cluster? do the behavioral anchors hold? does the POV covariate
actually protect `the-bench`? do neutral and adversarial converge on the same
lines? Full run (author authorization gate): full drafted roster, 8-model
panel, adversarial everywhere + neutral on a subsample.

## Pilot results & tuning verdicts (2026-09-07)

48/48 reads completed. Verdicts, ruled same day:

- **Variance is the metric.** 4/6 chapters scored tight-positive (+18..+44).
  Variance concentrated in the risk chapters: `the-bench` (one dissenter,
  −24) and `nothing-underneath` (**2–2 split**, +30/+34 vs −38/−39, evidence
  strength 7–9 both sides). Read the neutral pass as a distribution: a bimodal
  chapter is a *contested* chapter — the real readership will split the same
  way — and goes to the author queue. Controls validated (water-wings tightest
  and highest; two-towels clean baseline).
- **Adversarial framing DROPPED (author ruling).** For an explicit book it
  conflates explicit with male-tell — exhibit counts tracked explicitness
  (GPT-5.5: 94 exhibits on `the-bench`; 59 conv≥4 against `a-round`, a chapter
  it scored +34 in neutral). Verdict tiers discriminated only at the extremes.
  Everything actionable it found, the neutral pass also found. The prompt file
  stays versioned for reference; runs use **neutral + convergence** only. Its
  one aggregate lesson stands: the accusation thread's ammunition is
  explicitness itself, which cannot be scrubbed — the durable defenses are
  interiority (confirmed reading female to most panel readers), firewall
  discipline, and byline warmth.
- **Convergent tells (the pilot's queue):** `the-bench:201` "coral lips"
  passage (all four models, both framings — strict tier); the
  `nothing-underneath` mirror sequence + finale (Opus and Sol convergent:
  his-appraisal breast passage, nipple color-change spectacle, "stripper's
  body"/"as he would look", "channel… greedy", "wrung him dry"). Caveat held:
  the mirror's occupied-male-gaze is thesis-bearing (Randi's script made
  flesh) — fix space is vocabulary-level, not structural.

## Full-panel run results (2026-09-07 — Vol 1 × 8 models, neutral)

400/400 reads on disk (paid lane author-authorized this run). **45/50 chapters
comfortably positive** (medians +19..+43; `a-round` strongest at +43). Queue by
convergence rule: **`the-pointing-game`** (median −5, 4/8 negative — strict
tier, free-sample closer), **`hills-and-valleys`** (median −4, 4/8),
**`gone`** (+4, 3/8 strong negatives), **`the-usual`** (+14, 2/8 mild),
**`nothing-underneath`** (pilot; fix-list built). Watch (single dissenter):
`the-bench` (GPT-5.5 −24, stable across runs), `in-his-hands` (Opus −38 lone
strong outlier), `lesson`, `practice-room` (Fable −10s). Panel behavior: the
OpenRouter four skew positive/less discriminating **except GLM**, which
independently convicted both queue leaders (−30/−10) — genuine cross-vendor
convergence on the top two. Parser note: GLM emits Unicode minus signs.

Three recurring tell mechanisms across the queue (convergent-tell digest run
same day; full quotes in the per-model files): (1) **camera-inventory** of
women's bodies at interior moments; (2) **male gaze ventriloquized through
women's mouths** (the Sheri/Randi appraisal clusters — individually
characterization, convicted on *density*); (3) **male epistemic authority
over female desire ratified by narration** (peak: `the-pointing-game`'s "He
knew the difference between a woman performing release and a woman delivered
to it" — cited by 6/8 models, the book's second-most convergent line after
coral lips at 7/8). ~~Cross-chapter mechanical pattern for a possible
`style-rules.toml` rule: **color-inventory of nipples/genitals**~~ —
**REJECTED (author ruling 2026-09-07):** the nipple colors are a designed
two-pole characterization system (Randi dark/confident vs Vee
barely-there-pink/shy; `meta/meta-note-color-poles.md`), intentional and not
male gaze — a known limitation of this chapter-blind instrument. Consequences:
`the-bench:167` color and `nothing-underneath:27` reversed to keep in the fix
plan; `in-his-hands` off the watch list (Opus's −38 loses its best exhibits).
Standing author contingency: the first-three-chapters instance may still be cut
if reader-alienation evidence emerges there.

## Repair probe (`repair` framing, added 2026-09-07)

Detection's counterpart: for a chapter's **author-curated fix-list**
(`fixlists/<slug>.md`, versioned — the flagged spans quoted verbatim from the
scene), each panel model acts as a line editor deeply read in woman-authored
explicit fiction and returns, per span: a diagnosis (contestable — it may
reject the flag), 2–3 drop-in alternative renderings a female author writing
the *same POV and heat* would produce (a dominant male POV keeps its gaze —
the question is how a woman writes a man looking), and a cut option. Output:
`<model-id>/<slug>--repair.md`. **Options for the author; nothing is applied
by the harness.** Does not touch the detection instrument: repair reads are
separate stateless runs; detection stays blind.

## Output

`reviews/authorship-audit/<model-id>/<slug>--<framing>.md`, header carrying
model, slug, framing, protocol id, prompt SHA, date. Deliberately **not**
indexed by `na.py` (files carry no `## Reader reaction` section — these are
instrument outputs, not reader reactions). Known limitation, hold it: models
are imperfect proxies for the accusing reader; treat output as candidates.

Harness: `tools/authorship_audit.py` (`--pilot` runs the slate above).
