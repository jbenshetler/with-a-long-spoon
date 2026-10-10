# Capture noise baseline — ch003, 2026-10-09

**What this is.** Two capture runs over the *same* chapter text, byte-identical,
with no edit between them. The delta is therefore pure model variance. It exists
because score moves were being attributed to edits all day with no way to tell a
real move from jitter: `claude-opus-4-8`'s HEAT ran 3, 2, 2, 3, 3, 3, 2, 2 across
seven drafts, and no edit explained the swings.

**Method.** `capture_dag.py --personas romance-graduate fsog-refugee --to 3
--fresh`, run twice in succession on `the-pointing-game` at 4,977 words. Seven
subscription models, fourteen lanes. The two OpenRouter lanes (`glm-5.3`,
`gemini-3.8-flash`) were deliberately **not** re-run — fourteen free lanes
characterise the band as well as eighteen, and paying to measure jitter rather
than prose is waste. Run B overwrote run A's gates on disk; run A survives only
in the table below.

| model | persona | run A | run B |
|---|---|---|---|
| claude-opus-4-8 | romance-graduate | 8/9/2/1 | 9/9/2/1 |
| claude-opus-4-8 | fsog-refugee | 7/7/2/1 | 8/8/2/2 |
| claude-opus-5 | romance-graduate | 9/10/3/2 | 9/9/3/3 |
| claude-opus-5 | fsog-refugee | 9/10/3/2 | 9/10/3/2 |
| gpt-5.6-sol | romance-graduate | 10/10/3/2 | 10/10/3/3 |
| gpt-5.6-sol | fsog-refugee | 9/10/3/3 | 10/10/3/3 |
| gpt-5.5 | romance-graduate | 9/10/3/2 | 9/10/3/2 |
| gpt-5.5 | fsog-refugee | 9/10/3/3 | 9/9/3/2 |
| claude-fable-5-1 | romance-graduate | 8/9/2/2 | 9/9/2/2 |
| claude-fable-5-1 | fsog-refugee | 9/9/3/2 | 8/9/2/2 |
| claude-opus-5-5 | romance-graduate | 8/9/2/2 | 8/9/2/2 |
| claude-opus-5-5 | fsog-refugee | 8/9/2/2 | 8/9/3/2 |
| gpt-6-astra | romance-graduate | 8/9/2/2 | 8/9/2/2 |
| gpt-6-astra | fsog-refugee | 9/9/2/2 | 9/9/2/2 |

*(CAPTURE/NEXT/HEAT/ROMANCE)*

## Result

**9 of 14 lanes moved. Every move was exactly ±1. No axis ever moved 2.**

| axis | mean delta | mean abs delta | max abs delta | unchanged |
|---|---|---|---|---|
| CAPTURE | +0.21 | 0.36 | 1 | 9/14 |
| NEXT | −0.07 | 0.21 | 1 | 11/14 |
| HEAT | +0.00 | 0.14 | 1 | 12/14 |
| ROMANCE | +0.14 | 0.29 | 1 | 10/14 |

## How to read a capture score after this

**A single lane moving a single point is noise.** Treat a score as signal only
when **two or more lanes move the same direction on the same axis**, or **any
lane moves 2 or more**.

Worked both ways on 2026-10-09: cutting *"that mattered more to him than the
answer did"* dropped ROMANCE 2 → 1 in `claude-opus-4-8` *and* `gpt-5.5`, and both
returned to 2 when it was restored — two lanes, same direction, replicated in
both directions, so it cleared the bar and the clause went back. A HEAT drop
attributed to cutting the dance sentence did not clear it and was withdrawn;
`claude-fable-5-1` dropped HEAT 3 → 2 on identical prose in this very baseline.

**The written complaints are the reliable output of this instrument; the numbers
are not.** HEAT's mean abs delta of 0.14 is the tightest axis and still moves
without cause, while three vendors naming the same target in prose held up every
time it happened today. One caveat: a single retest gives a band, not a
confidence interval — it says ±1 is routine, and says little about ±2.

A single-lane note worth keeping: `gpt-6-astra` returned **identical numbers on
both personas across both runs**, the only model that did.
