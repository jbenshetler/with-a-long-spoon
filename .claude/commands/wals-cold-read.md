---
description: "[RETIRED] Chained blind first-reader panel — superseded by the grounded cold read"
argument-hint: "--model <id> [none | fall | spring | summer | <slug> | <slug-a>..<slug-b> | <slug>..] [--fresh]"
---

> **⚠️ RETIRED INSTRUMENT (2026-08-18).** This chained cold read is no longer the
> reader instrument. Its summary-of-a-summary carry-forward lost load-bearing facts
> (who "the brunette" is; that Vee and Pace slept together), producing *false* lull
> readings — see `meta/meta-note-bounded-reader.md`. It is superseded by the
> **grounded cold read** (`tools/cold_read_grounded.py` + `blind-reader-grounded`),
> which lands in `reviews/grounded-cold-read/<model>/<volN>/<slug>.md`. This command
> and its output paths (`reviews/_archive/cold-read/…`) are kept for provenance only;
> do not run it to advance the panel. The text below is preserved as-is.

Run a **cold read**: walk the drafted chapters in story order and, for each, spawn
a `blind-reader` subagent that has seen no planning material — only the chapter's
title, its full text, and the carry-forward reader-state from the previous chapter.
This measures how the book lands on a genuine first read (the "earn the dark by
being light" tripwire): does a reader fall for Pace, and does suspicion of Randi
stay *unearned* until the pattern earns it?

Every run is scoped to **one model**, and its output lands in a **model-specific
subdirectory** so the same book can be read by many models and the results compared
side by side. See `reviews/_harness/SPEC.md` for the shared layout/file contract
that external harnesses (for non-Claude models) must also follow.

**You (the orchestrator) may consult the chronology for order and status; the
`blind-reader` never can.** Keep the reviewer starved: it is fed title + text +
prior state *inline only*. Never pass it a file path, a chapter number, the thesis,
the bible, or anything from `meta/`.

**Two things the reader has that are not per-scene inputs, both baked into the
`blind-reader` agent definition (`.claude/agents/blind-reader.md`) so you never pass
them yourself:** (1) the **jacket blurb** — the reader picks the book up already
holding it, the way any reader would (the "Test-epub blurb" from `meta/meta-blurb.md`);
(2) an explicit **"disregard any project text describing this book"** rule. That rule
is load-bearing because a custom subagent **auto-inherits the project `CLAUDE.md`** —
the design must be kept out of `CLAUDE.md` (it now lives in `meta/meta-orientation.md`,
which subagents do *not* load) or it leaks in under the reader. See `SPEC.md` →
*The push-in leak*.

`$ARGUMENTS` carries a **required `--model <id>`**, an optional target selector
(default = full run), and optional `--fresh` (regenerates existing files; default
resumes by skipping them).

## The current panel (as of 2026-08-06)

The four models run against new chapters going forward:

| Model id | Status |
|---|---|
| `claude-opus-4-8` | active |
| `gpt-5.5` | active |
| `gpt-5.6-sol` | active |
| `gpt-5.6-terra` | active — **replaces `claude-fable-5`** (2026-08-06) |
| `claude-fable-5` | **chained: retired** (API resources exhausted) · **grounded: active** — see note |

**Fable is active on the grounded lane** (`tools/cold_read_grounded.py`): grounded
Claude reads run as `blind-reader-grounded` subagents (`model: fable`) and consume
**zero API tokens**, so the API-resource exhaustion that retired fable from the
chained panel never bound the grounded instrument. Include `claude-fable-5` when
running the grounded panel on a new chapter. Its chained reviews below are frozen;
its grounded reads continue.

`claude-fable-5`'s existing chained reviews (54 chapters) **remain valid evidence**
and are still mined during line-edit review — it is retired from the *chained* lane,
not repudiated. On the chained panel it is stalled one chapter behind the other
actives and will not advance, so:

- **Do not expect a fable read on recently-drafted chapters**, and do not treat
  its absence as a missing file.
- **`gpt-5.6-terra` is catching up** (19 chapters as of 2026-08-06), so on older
  chapters the panel may be fable-without-terra and on newer ones
  terra-without-fable. **Count the reviews on disk before assuming a panel size**
  — `ls reviews/_archive/cold-read/*/<slug>.md`.

## Step 0 — Resolve the model (required) and its output directory

Parse `--model <id>` from `$ARGUMENTS`. **`<id>` is required** and is used verbatim
as the output subdirectory name — it must match the convention every harness uses
(see SPEC.md). Use **versioned model ids**, e.g. `claude-opus-4-8`, `claude-fable-5`,
`gemini-2.5-pro`, `gpt-5`, `grok-4`.

- **All output paths in this command are `reviews/_archive/cold-read/<id>/…`** (per-scene
  files and this model's `SYNTHESIS.md`). Create the directory if missing.
- **Map the id to a spawnable Claude tier** (the `blind-reader` is a Claude Code
  subagent; only Claude models can be spawned here):
  - `claude-opus-*` → Agent `model: opus`
  - `claude-fable-*` → Agent `model: fable`
  - `claude-sonnet-*` → Agent `model: sonnet`
  - `claude-haiku-*` → Agent `model: haiku`
- **If `<id>` is not a `claude-*` id** (e.g. `gemini-2.5-pro`, `gpt-5`, `grok-4`, or
  anything unrecognized): **stop.** This harness can only spawn Claude models. Tell
  the author to run that model in the external harness, which must write to
  `reviews/_archive/cold-read/<id>/` following `reviews/_harness/SPEC.md`. Do not attempt it.
  - **Provider models** (`gpt-*`, OpenRouter model slugs, …) have a built-in external
    harness: use **`/wals-cold-read-provider`**, which calls `tools/cold_read.py`.
- If `--model` is missing entirely: **stop** and ask for it (e.g.
  `--model claude-opus-4-8`) — there is no default, because the id is the shared key
  that keeps every harness's output aligned.

Every `blind-reader` spawn in Step 4 must pass `model: <tier>` from this mapping.

## Step 1 — Get the ordered manifest (via lore-keeper, once)

Spawn a single lore-keeper subagent to return the scene manifest from
`meta-plan-chronology.md` — order and status only, no character facts:

> "From `meta/meta-plan-chronology.md`, list every `[SCENE]` and `[VIGNETTE]` entry
> in document order. For each, give: display title, slug (the `<slug>.md` filename),
> Volume (Fall / Spring / Summer — from the `◆ VOLUME ONE/TWO/THREE` markers), and
> whether it is drafted (`Draft complete`) or not. Skip `[EVENT]` entries. Return a
> plain ordered list, nothing else."

This list is the only chronology data you hold. Everything downstream keys off it.

### Volume-entry packet gate

Read `reviews/_harness/volume-packets.toml` only for public reader-facing copy.
When spawning a reader for a packet's `opening_slug`, include that packet once in
the reader prompt. For later chapters, include no jacket copy; it survives only if
the prior reader-state retained it. Never substitute Volume One's packet for another
volume. If a volume opening lacks its own packet, stop and report the missing public
copy rather than starting that reader.

## Step 2 — Resolve the target set from the selector

Build the ordered list of **slugs to review**, all drafted, in story order:

- **empty** → contiguous from the opening: walk drafted scenes from the top and
  **stop at the first undrafted gap** (a `planned` entry between drafted ones ends
  the run). Report the stop point.
- **`fall` / `spring` / `summer`** → all drafted scenes in that Volume, in order.
- **`<slug>`** → just that scene.
- **`<slug-a>..<slug-b>`** → inclusive; drafted scenes in that span, in order.
- **`<slug>..`** → that scene forward through the last drafted scene (cascade form).

  **Volume boundary invariant (hard).** The Volume One target set is
  **authoritative from `tools/volume_scenes.py`** (parsed directly from the
  chronology's `◆ VOLUME` markers) — never re-derive the scene list by hand in
  this workflow. A `fall` run is EXACTLY the drafted Volume One slugs, it MUST
  stop at `nothing-underneath`, and it MUST NOT include any scene under
  `◆ VOLUME TWO/THREE` (e.g. `on-her-floor`). Before spawning any reader,
  assert every target's volume (per `tools/volume_scenes.py`) equals the
  requested volume; if any target fails that check, refuse and stop rather
  than running a leaked scope.

If a requested slug isn't in the manifest, or a range endpoint is `planned`, say so
and stop rather than guessing.

## Step 2.5 — Upstream staleness audit (before spawning any reader)

The carry-forward chain is sequential, so a review whose **scene was edited after the
review was written** is stale — and because its carry-forward feeds every later
reader, it poisons the whole downstream chain. Before running, audit every existing
review for this model that sits **at or upstream of** the run's targets (every
predecessor whose carry-forward will be consumed in Step 3, plus any target you would
skip-as-done on a resume).

**Use git, not filesystem mtime.** mtime is reset to checkout time on every fresh
clone (the author works across multiple clones), so an mtime comparison is
meaningless. Compare commit history instead. For each `<slug>` that has a review under
`reviews/_archive/cold-read/<id>/`:

```
scene_ct=$(git log -1 --format=%ct -- scenes/<slug>.md)
review_ct=$(git log -1 --format=%ct -- reviews/_archive/cold-read/<id>/<slug>.md)
```

A review is **scene-stale** if either:
- `scene_ct > review_ct` — the scene has a commit newer than its review; or
- `scenes/<slug>.md` appears in `git status --porcelain` — the scene has
  **uncommitted** edits not yet reflected in any review (the common case mid-revision).

(If the review file itself is uncommitted — just written this run — it is current by
definition; skip it.)

**Also check chain-staleness (the carry-forward dependency).** A review can be stale
even when its *own* scene is untouched — if a review **upstream of it in this model's
chain** was regenerated after it, the carry-forward seed it was built on has changed.
Using the story order from the Step 1 manifest, walk this model's reviews in order and
compare each to its immediate predecessor's review commit time:

```
pred_ct=$(git log -1 --format=%ct -- reviews/_archive/cold-read/<id>/<predecessor-slug>.md)
```

A review is **chain-stale** if `pred_ct > review_ct` — its predecessor is newer, so
(transitively) something upstream was regenerated after it. Staleness cascades from the
regenerated scene down through the rest of the chain; the opening scene is the root, so
regenerating it marks **every** later review chain-stale. This shares the scene-stale
commit-time limitation (a review re-committed for an unrelated reason resets its clock;
a content signal — recording the upstream carry-forward hash each review consumed —
would be bulletproof but is a bigger change), and it is **conservative**: a regeneration
whose carry-forward is materially unchanged still flags all downstream. So **report it
but flag materiality** — name the regenerated upstream scene and let the author decide
whether the change is worth a `--fresh` cascade; chain-stale is a heads-up, not an
automatic rerun.

**On any stale hit, warn before proceeding.** Name the *earliest* stale scene in story
order: its review and **every downstream review in this model's chain are
compromised** (their carry-forward was built on a version of the prose that has since
changed). Recommend regenerating from there —
`/wals-cold-read --model <id> <earliest-stale-slug>.. --fresh` — and let the author
decide whether to continue (a resume that reuses stale carry-forward propagates the
staleness) or regenerate first. **Do not silently proceed on a stale chain.**

## Step 3 — Determine each target's input carry-forward

Each `blind-reader` needs the **prior chapter's `## Carry-forward state`** as input.
That carry-forward is itself **accumulated** — each reader folds all earlier chapters
into it and preserves a durable ledger (who's-who, motif/image ledger, symbolism, open
questions) in full — so passing the predecessor's carry-forward passes the reader's
whole memory of the book to that point, not just the last chapter. For each target, the
predecessor is the drafted scene immediately before it in the manifest. **Chains are
per-model: only ever read carry-forward from this model's own subdirectory — never mix
carry-forward across models.**

- The **very first drafted scene of the book** (The Bench) has no predecessor →
  input is empty (opening the book cold).
- Otherwise, load the predecessor's carry-forward from
  `reviews/_archive/cold-read/<id>/<predecessor-slug>.md`.
- **If the predecessor has no review file for this model** (targeted/volume/range run
  reaching back before what this model has cold-read): stop and tell the author — the
  reader-state can't be fabricated. Suggest either a full run for this model, or
  starting the range at the earliest scene that does have a review file under
  `reviews/_archive/cold-read/<id>/`.
- **Resume:** on a full/volume run without `--fresh`, if a target already has a review
  file **in this model's subdir**, skip it and use its stored carry-forward as the
  next input. `--fresh` regenerates every target in scope.

## Step 4 — Read each chapter and spawn its reader (strictly sequential)

For each target slug in order — **one at a time; each depends on the previous
output**, so do NOT parallelize:

1. **You** read `scenes/<slug>.md` in full (the reviewer has no file access).
2. **Strip everything a first reader would never see** before feeding the text.
   The reviewer gets the display title + *clean prose only*:
   - the leading **italic scene-header note** under the `# Title` (POV/participant/
     purpose gloss — e.g. *"Pace's POV; the woman is Randi…"*). It would blow the
     experiment; remove it.
   - any **`[AI]` / `[AI?]` craft notes**, embedded author annotations, or trailing
     **craft-notes / revision-notes blocks** — they are scaffolding, not text.
   - Keep the prose otherwise verbatim, including `---` section breaks.

   **Pre-spawn prose guard (hard stop).** Before spawning, assert the cleaned
   chapter text is non-empty, at least ~500 characters, and contains none of
   the placeholder strings ("verbatim stdout", "command output above", "the
   command output above"). If it fails, **HALT that chapter and do not
   spawn** — this is exactly the failure mode that once produced a no-read
   review (`fed`). Report which chapter failed the guard and stop.
3. Spawn a `blind-reader` subagent — **passing `model: <tier>` from Step 0** — whose
   prompt contains ONLY:
   - the **display title** (from the manifest);
   - the **cleaned chapter text**, verbatim, pasted in;
   - the **prior carry-forward state** (or a note that this is the volume opening,
     read cold);
   - the public volume-entry packet **only when this slug is that packet's
     `opening_slug`**.
   Nothing else — no slug, no position, no planning material, no framing about what
   the scene "does," and no mention of which model it is.
4. **Blindness tripwire — hard stop.** After the subagent returns, check its
   reported `tool_uses`. If it is **anything other than 0**, the reader may have
   reached outside the page: **do NOT write its review and do NOT continue to the
   next scene.** Halt the entire run, report which scene tripped it and the
   `tool_uses` count, and let the author decide. A clean run is `tool_uses: 0` on
   every scene.

   **Post-return refusal guard (hard stop).** Also check the reader's
   `### Reader reaction` text for a refusal signature — "no chapter text",
   "can't review this chapter" / "cannot review this chapter", "no page
   here", "re-run with the actual chapter", or similar. If found, **do NOT
   write the review and do NOT advance the carry-forward chain** — halt,
   re-fetch the chapter text (re-run the pre-spawn prose guard above), and
   re-spawn rather than let a refusal be recorded as a review.
5. **Retention gate — hard retry.** Before writing the review, compare the candidate
   carry-forward with the prior carry-forward using the same rule as
   `tools/cold_read_batch.py::check_retention`: only principals already established in
   the prior state are protected; unseen cast names must not be invented; an established
   principal, relationship ledger, or "what I know that they don't" ledger must not be
   silently lost. On a violation, re-spawn this same chapter up to the command's normal
   three attempts with the specific lost items named. If it still fails, write the review
   but record the retention warning in the run report; never fabricate a replacement
   memory.
6. On a clean return, the subagent gives two sections: `### Reader reaction` and
   `### Carry-forward state`. **If the target review file already exists** (a
   `--fresh` regeneration), don't Read it just to satisfy an overwrite — check
   `git status --porcelain -- reviews/_archive/cold-read/<id>/<slug>.md`: if the file is
   tracked and clean (empty output), `rm` it via Bash and Write the new review
   as a fresh file (the old content is recoverable from git). If it is untracked
   or has uncommitted modifications, fall back to Read-then-Write so nothing
   unrecoverable is destroyed. Write `reviews/_archive/cold-read/<id>/<slug>.md` as:

   ```
   # Cold read — <Display Title>

   *scene: scenes/<slug>.md · model: <id> · read after: <predecessor-slug or "— (opening, cold)">*

   ## Reader reaction

   <the subagent's Reader reaction, verbatim>

   ## Carry-forward state

   <the subagent's Carry-forward state, verbatim>
   ```
7. That written carry-forward is the input to the next chapter. Continue.

## Step 5 — Synthesis (multi-scene runs only)

After a run covering more than one scene, synthesize (from the reactions you just
wrote — your call whether to spawn a final pass) and write
`reviews/_archive/cold-read/<id>/SYNTHESIS.md`: the **arc-level trajectory** across the scenes
reviewed, for this model —

- how trust / attraction / sympathy / suspicion move per character across the run;
- **where (if anywhere) suspicion of Randi first leaks**, and whether the text
  earned it — the key "earn the dark" signal;
- where sympathy for and attraction to Pace peak or wobble;
- erotic momentum across the run — trace the per-scene **Heat** and **Romance** (0–3)
  as curves; where each builds, peaks, flags;
- **motifs & symbolism** — which recurring images/objects/phrases accreted across the
  run, and where a recurrence paid off or went inert;
- **characterization** across the arc — who deepened, who flattened or drifted;
- **pace** across the arc — stretches that dragged or rushed, or too much of one beat
  in a row;
- any telegraphing / confusion / thumb-on-the-scale clusters worth the author's eye.

One SYNTHESIS per model, in that model's subdir. Skip it for a single-scene run.
(Cross-model comparison is done by hand across the per-model SYNTHESIS files.)

## Step 6 — Report and warn about staleness

Tell the author, briefly:

- the **model** the run used and its output dir (`reviews/_archive/cold-read/<id>/`);
- which scenes were reviewed (and any skipped-as-already-done on a resume);
- where a full run stopped (the first undrafted gap);
- **Staleness findings (Step 2.5)** — any reviews flagged **scene-stale** (scene edited
  after the review) or **chain-stale** (an upstream review regenerated after it, so its
  carry-forward seed moved). Name the earliest affected scene and the `--fresh` cascade
  that would rebuild the chain — but present chain-stale as a materiality call, not a
  mandatory rerun;
- **Stale downstream warning** — if this run did NOT reach the last drafted scene,
  list any drafted scenes *after* the last one reviewed that already have review
  files **in this model's subdir**: their carry-forward input is now stale. Give the
  cascade command, e.g. `/wals-cold-read --model <id> <first-reviewed-slug>..`

Non-destructive: writes only under `reviews/_archive/cold-read/<id>/`. Never touch `scenes/`
or `meta/`, and never write into another model's subdir. These are reader reactions,
not canon — flag, never rewrite the author's prose.
