---
name: graded-writes
description: >-
  Turn a batch of workshopped decisions into faithful, auditable, canon-consistent
  writes to the planning docs, using a produce→grade→revise loop that iterates until
  it passes or hits a cap. Use after a design/workshop session when many intertwined
  decisions must land in meta/ without flattening the nuance — a Danaë-scale batch,
  not a one-line edit. Wraps the general `graded-loop` workflow with this repo's
  defaults: a producer subagent drafts the exact per-doc writes; a GRADER checks
  canon-consistency + lean/clean conventions; a NUANCE-CHECKER checks fidelity
  against a source log (net of decisions). All versions and findings are logged to
  files so the run is restartable. NEVER writes to meta/ until the author signs off.
---

# graded-writes — faithful, auditable doc-writes via a graded loop

The recurring problem: a workshop produces many subtle, intertwined decisions
(oppositions that must stay unresolved, rules that need their *reason*, guards,
preserve-verbatim phrasings) that must land across many `meta/` docs **without
flattening**. A fresh subagent can't see the conversation, so fidelity is won or
lost in **files you author first**. This skill encodes that discipline; the loop
mechanics live in `.claude/workflows/graded-loop.js`.

## The four invariants (do not skip #2)

1. **The loop** — produce → evaluate (parallel) → revise → repeat to a cap.
2. **The fidelity bridge (main-agent-only).** You serialize the decisions to files
   *before* the loop: a faithful **source log** and a **must-survive checklist**.
   A subagent cannot do this — only you hold the conversation.
3. **A boolean pass-bar** each evaluator returns, that the loop branches on.
4. **File-logged + restartable** — versioned drafts + per-round findings on disk.

## Procedure

### 1. Working dir
`mkdir -p /tmp/<task>-graded`. Everything scratch lives here (never in `meta/`).

### 2. Author the two source files yourself (the fidelity bridge)

- **`source-log.md`** — a *faithful* record of every decision and its reasoning from
  the relevant span of the conversation. Preserve **both sides** of each "X AND Y,
  never resolved" opposition, each rule's **reason**, each **guard/failure-mode**,
  and load-bearing phrasings in `"quotes"`. **Mark superseded ideas `[SUPERSEDED]`**
  so the nuance-checker judges *net of decisions* and doesn't flag deliberately
  dropped material as loss.
- **`checklist.md`** — the must-survive items, each: **claim (both sides) · reason/guard ·
  → target doc**, preserve-verbatim phrases in `"quotes"`, tagged `[NEW]` / `[REVISE]`
  (overrides locked canon) / `[CONFIRM]`. Include the **repo doc conventions** block
  (below). `[REVISE]` items must be applied across **every** doc that held the old
  version — list them.

**Repo doc conventions (put this in the checklist):** lean, only what's decided;
**single source of truth** (one home per fact; pointers, never restatements);
**written clean** (current design only, no "was X now Y" banners — git is history);
chapter-title cross-refs in `{{Braces}}` (own chapter bare); `scenes/` files are
prose-only; dates live only in the chronology.

### 3. Run the loop

Invoke the workflow by name with the producer + the two default evaluators. The
producer drafts a **single consolidated file** with a headed section per target doc:
full content for `[NEW]` files, precise **anchor → replace/insert** blocks for edits
(quote enough surrounding text to anchor). Tell it to warn that `meta/` uses curly
quotes/em-dashes so appliers must match on the real characters.

```
Workflow({ name: "graded-loop", args: {
  workdir: "/tmp/<task>-graded",
  producer: {
    draftPrompt:  "You are drafting the exact planned writes for the novel's meta/ docs. Read <workdir>/checklist.md and <workdir>/source-log.md (ignore [SUPERSEDED]). Read every real target doc named in the checklist to match register. Produce ONE consolidated file: a headed section per doc — full content for [NEW] notes, precise anchor→replace/insert blocks for edits. Honor every checklist item (both sides of each opposition, the reason, the guard, the verbatim quotes). Apply [REVISE] overrides across every forked doc. Follow the repo conventions block in the checklist.",
    revisePrompt: "You are revising the consolidated doc-writes. Read the current draft, the evaluator findings, and <workdir>/checklist.md + source-log.md. Fix every issue: restore each lost/flattened nuance and correct each canon/lean issue. Introduce no new losses or restatements."
  },
  evaluators: [
    { key: "grade",  passField: "pass",     schema: GRADER_SCHEMA,  prompt: GRADER_PROMPT },
    { key: "nuance", passField: "zeroLoss", schema: NUANCE_SCHEMA,  prompt: NUANCE_PROMPT }
  ],
  maxIters: 5
}})
```

**GRADER_PROMPT** (canon + lean): "You are the GRADER. Read the draft, `<workdir>/checklist.md`,
and the ACTUAL target docs in `meta/` + `CLAUDE.md`. Judge (1) canon-consistency —
does it contradict locked canon EXCEPT where the checklist marks an item `[REVISE]`
(sanctioned overrides), and is each `[REVISE]` applied consistently across every
forked doc with no dangling `{{Title}}`? and (2) lean/clean conventions (single-source,
no change-banners, correct braces, register matched). Write findings to the given
path; return the verdict. Set `pass` true only with no high/medium issues."
**GRADER_SCHEMA:** `{ pass:boolean, canonConsistent:boolean, leanConventions:boolean,
issues:[{doc, severity:high|medium|low, issue}], summary }` (make `pass` = the AND).

**NUANCE_PROMPT** (fidelity): "You are the NUANCE-CHECKER. Read the draft,
`<workdir>/source-log.md` (ground truth), and `checklist.md`. Compare NET OF DECISIONS:
ignore `[SUPERSEDED]`. For every LIVE nuance verify the draft keeps BOTH sides of each
opposition, each rule's reason, each guard, and every preserve-verbatim quote. Name the
author's known-risk points explicitly. Write findings; return the verdict.
`zeroLoss` true ONLY with no high/medium losses."
**NUANCE_SCHEMA:** `{ zeroLoss:boolean, losses:[{item, whatLost, whereInLog, severity}], summary }`.

Configurable: add/drop evaluators (each needs `key`, `prompt`, `schema`, `passField`);
raise/lower `maxIters`. Restart after an interruption or a script edit with
`Workflow({ scriptPath, resumeFromRunId })` — unchanged agents replay from cache.

### 4. Review gate (never auto-apply)

On completion: if it **hit the cap without passing**, report the residual failures
honestly — do not pretend it converged. If it **passed**, present the final draft
**next to its source-log anchors** and get the author's explicit sign-off before any
write to `meta/`.

### 5. Apply — disjoint-file writers

Spawn writer subagents (Haiku is fine) to apply the approved draft. **Group by file
so no two writers touch the same doc** (parallel edits to one file race). Each writer:
read the real file, **build the Edit `old_string` by copying the file's actual
characters** (curly quotes/em-dashes — not the draft's ASCII), and **STOP-and-report
any anchor it can't locate rather than guessing**. `[NEW]` files are plain writes.

### 6. Finalize

`tools/lint_titles.py --all` (all `{{…}}` resolve) · `tools/novel-assistant/na.py reindex`
· if the chronology changed, `tools/chronology_html.py` (and include the regenerated
`chronology.html`). Report any skipped anchor from step 5.

### 7. Commit

Only when the author asks. Stage the specific work (exclude unrelated dirty state like
the `tools/novel-assistant` submodule pointer); if the remote has moved, `git pull
--rebase` then push.
