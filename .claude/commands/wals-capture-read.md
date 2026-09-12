---
description: Capture DAG — run persona-conditioned capture/retention readers to a chapter (STOP/CONTINUE gates)
argument-hint: <scene-slug | N> [--models <id,...>] [--personas <name,...>] [--reread]
---

Run the **capture DAG**: persona-conditioned blind readers take the book one
chapter at a time with a hard **STOP/CONTINUE gate** after each. It measures
*capture and retention* — where a target reader would put the book down — not
craft quality. Its sibling `/wals-cold-read` measures how a chapter reads; this
measures whether the reader turns the page.

Each reader = one **persona × one model**, and **persona memory IS the
instrument**: chapter N is read with that reader's OWN carry-forward `ck-ch<B>`
(B = decade boundary below N) + raw prose of B+1..N-1 + chapter N. Every 10
chapters the reader mints its own carry-forward from prior checkpoint + the
decade's raw prose + its own gate notes. Readers never share memory.

Harness: `tools/capture_dag.py`. Contract and results history:
`reviews/capture-panel/SPEC.md`. Output: `reviews/capture-panel/<model>/dag/<persona>/`.

## Personas (`reviews/capture-panel/personas/`)

| Persona | Role | Default |
|---|---|---|
| `romance-graduate` | outgrown spicy romance, won't give up the heat (primary vector) | yes |
| `fsog-refugee` | FSoG intensity with real consent and warmth (crossover) | yes |
| `consent-sensitive` | vigilant about predation-romanticizing; the con-misread instrument | yes |
| `dark-romance-control` | the WRONG reader; **should bounce** — her STOPs are successes | yes |
| `queer-woman` | opt-in only | **no** |

A bare `--personas`-less run is the four defaults. `queer-woman` is selectable
but deliberately **not** in the default set, so a bare invocation never silently
opens a fresh 70-chapter read on a subscription lane.

## Models

Claude ids run headless on Claude subscription OAuth; `gpt-*` on codex
subscription auth; everything in `capture_dag.OPENROUTER_MODELS` (`glm-5.3`,
`glm-5.3-flash`, `gemini-3.8-flash`, `kimi-k3`, `qwen3.8-max-0902`,
`deepseek-v4-pro-0813`) is **paid OpenRouter**.

**Token rule (standing):** never launch an OpenRouter model without specific
author authorization. Unlike the cold-read panel there is no fixed roster — the
author names the models per run.

## Step 1 — Resolve the target chapter number

`--to N` takes the **reader sequence** number: the chapter's position in
`checkpoint_bundle.reader_slugs()` (Vol 1 drafted, then Vol 2, then Vol 3, in
chronology order). This is the same source of truth the authoring and grounded
cold-read lanes use.

**It is not `reading_order.py`'s ordinal.** That tool numbers the whole
chronology *including planned* chapters, so the two bases diverge — `grace` is
chronology ordinal 83 but reader chapter **70**. Using the wrong one silently
reads the wrong chapter. Resolve it against the harness's own sequence:

```
python3 -c "import sys; sys.path.insert(0,'tools'); import capture_dag as d; \
  s=d.slugs(); print(s.index('<slug>')+1, 'boundary', d.boundary(s.index('<slug>')+1))"
```

The chapter must be `Draft complete` in the chronology.

## Step 2 — Survey reader state before promising a scope

Readers are usually at *different* chapters, and a STOP is permanent. Always
count the actual deficit first — "re-read one chapter" is rarely one call:

```
for m in <models>; do for p in <personas>; do d=reviews/capture-panel/$m/dag/$p;
  printf '%-16s %-18s last=%-14s cks=%s stopped=%s\n' "$m" "$p" \
    "$(ls $d 2>/dev/null | grep '^gate-ch' | tail -1)" \
    "$(ls $d 2>/dev/null | grep -c '^ck-ch')" \
    "$([ -f $d/STOPPED ] && echo YES || echo no)"; done; done
```

- Missing gates in 1..N **plus** a mint at every decade boundary ≤ N = the call
  count. Reaching a decade chapter mints a carry-forward, so N=70 always adds one.
- A lane with no directory is a read **from chapter 1**. Report that cost before
  running it, never absorb it silently.
- **A `STOPPED` marker ends that reader permanently.** Never delete one to
  revive a reader without explicit author approval — the stop is data.
- Report the total to the author and get scope confirmed before spending,
  especially on paid lanes.

## Step 3 — Run, one invocation per model

```
tools/capture_dag.py --models <one-model> --personas <p1> <p2> ... --to <N>
```

**Always invoke once per model, backgrounded, concurrently.** `main()` builds
`[(m, p) for m in models for p in personas]` — model-major — and feeds it to a
pool of **4 workers**. A single multi-model call therefore serializes the last
model behind every lane of the earlier ones: in a 12-lane run the third model
did not start at all until the long catch-up lanes drained. Per-model
invocations give each model its own pool of 4.

Effort defaults to `low`. The run is **restartable** — existing gates and mints
are skipped, so a killed run loses only its in-flight calls.

## Step 4 — Re-reading a revised chapter

The resume behaviour that makes restarts safe also means **an existing gate
blocks a re-read**. Pass `--fresh` to overwrite it in place:

```
tools/capture_dag.py --models <one-model> --personas <p1> ... --to <N> --fresh
```

`--fresh` is scoped to the **target chapter only** (`--to N`) — it overwrites
that gate and, when N is a decade boundary, re-mints that carry-forward (correct:
the mint consumes the gate being replaced). It is deliberately not a blanket
refresh; the run's scope is the whole range 1..N, so a bare boolean would
re-read the entire book. Every other chapter still resumes normally.

**Never archive gates or commit as a precondition to a run.** Gates are
committed as a batch after a run and git is the history; the author manages all
commits. Retrieve a prior read with `git show <rev>:<path>` and compare with
`git diff <rev> -- <path>`. Do not create `archive/` copies — they duplicate
history and clutter every persona directory.

Note the re-read is only a true before/after for readers that
had *already* reached N; for readers caught up from behind it is a first read,
and the difference must be stated in the report. Gates *after* N are now stale
in memory terms — the reader's later checkpoints were minted from the old text.

## Step 5 — Read out and report

Run `tools/capture_stats.py` (`--chapters A-B` to zoom, `--persona`/`--model` to
scope) and follow its discipline:

1. **Raw CAPTURE is not comparable across lanes** — measured lane offset on
   identical prose (~2.1 points) exceeds any chapter effect. Compare a reader
   only against her own mean.
2. A breather with ALMOST-STOPPED *none* is healthy. CAPTURE measures pull, not quality.
3. **The actionable unit is the RUN, not the chapter.** Readers name run length
   as their limit; flag stretches, not single dips.
4. Where gates carry NEXT, the split is the signal: low CAPTURE + high NEXT is a
   working breather; low + low is a stall.

Report: DECISION/CAPTURE/NEXT per reader, STOPs (a control's STOP is a success —
the repel filter working), and **ALMOST-STOPPED quoted exactly** — the
actionable output even when everyone continues. Single-reader stops are noise;
**convergent ones are findings**. Weight convergence across *models* as well as
personas, and apply the author's standing model-weighting when reading heat.

Personas are simulations of readers, not readers. Output is candidate signal for
authorial judgment; the ground truth is the human cohort
(`meta-plan-test-readers.md`). Check `meta/meta-triage-<slug>.md` first so
settled criticisms aren't re-litigated. Gates are **reactions, not canon** —
flag, never rewrite prose from them.

`--assemble` builds the `<persona>--volume-dag.md` whole-run record from gates +
mints; it makes no model calls.

Non-destructive: writes only under `reviews/capture-panel/<model>/dag/<persona>/`.
