---
description: Interactive [AI]-marker review pipeline for a chapter (Pass 0 + N/N+1 prefetch)
argument-hint: <chapter-slug> (e.g. the-bench)
---

Drive an interactive review of `scenes/$1.md` from its inline `[AI]` markers. You
(the main loop) are the orchestrator and the **only** agent that talks to the
author; background subagents do the non-interactive work. **Never rewrite prose
on a solo judgment call unless a marker authorizes it; workshop the interactive
ones live.** The judgment stays with the author.

## Marker grammar

An instruction is any line beginning with `[AI`. Two independent modifiers:

- `?` → **interactive** (workshop with the author). No `?` → **solo** (handled
  in Pass 0 without the author).
- `:doc` → applies to the **whole document**. No `:doc` → applies to the
  **passage the line precedes** (until the next marker or blank-line boundary).

| Marker | Handling |
|---|---|
| `[AI] …` | solo, local — Pass 0 |
| `[AI:doc] …` | solo, whole-document — Pass 0 |
| `[AI?] …` | interactive, local — worklist item |
| `[AI?:doc] …` | interactive, whole-document — worklist item |

## Step 0 — Scan and kick off

1. `rg -n '^\s*\[AI' scenes/$1.md` to enumerate every marker with its line.
2. If there are none: say so and stop.
3. Classify each by the grammar. Build the **interactive worklist**: whole-doc
   `[AI?:doc]` items first (they frame how to read everything), then local
   `[AI?]` items in document order.
4. Launch **Pass 0** (Step 1) and the **prep for worklist item 1** (Step 2)
   together as background agents — Pass 0 edits solo passages, prep is read-only,
   so they don't collide.

## Step 1 — Pass 0 (background, non-interactive)

Spawn one background general-purpose Agent to work `scenes/$1.md`:

- Execute every **solo** marker (`[AI]`, `[AI:doc]`) — apply the edits directly.
- After editing, run a `lore-keeper` continuity check on the changed passages
  (project rule: solo prose edits must stay canon-safe); fix or flag conflicts.
- **Remove** each solo marker line once handled.
- Return a concise changelog (marker → what changed) plus any continuity flag it
  could not resolve. It must **not** touch interactive (`?`) markers.

When it returns, present the changelog and tell the author to review
`git diff scenes/$1.md`. If they dislike an auto-edit, **Esc-Esc (rewind)**
restores the pre-Pass-0 checkpoint.

## Step 2 — Interactive loop (sliding window of 1)

For each worklist item N, in order:

1. Ensure item N's **prep brief** is ready (it was launched while you were on
   N−1). If it hasn't landed yet, wait for it.
2. **Immediately launch background prep for item N+1** so it's ready when you
   arrive there. This overlap is what shrinks the author's wait.
3. Work item N with the author: open with the brief (operative canon +
   continuity + 2–3 concrete options, or the specific question the marker
   poses), then workshop / propose per the `[AI?]` instruction. Apply only
   agreed edits.
4. On resolution, **remove** item N's `[AI?]` marker line.
5. Advance to N+1.

### The prep agent (background, read-only, per item)

Spawn a background general-purpose Agent: given the `[AI?]` instruction and its
passage (**quoted directly** — the subagent can't see the file state or this
conversation), gather the operative canon (delegating to `lore-keeper` /
`na.py` / `rg` as needed), run a continuity check on the passage, and draft 2–3
options or frame the decision. Return a **brief**. No file edits.

## Stopping (say this to the author at kickoff)

The loop pauses at every item, so nothing runs away:

- **End the review:** type `stop` at any prompt — the loop halts and will not
  advance to the next item.
- **Interrupt the current action:** Ctrl+C.
- **Undo Pass 0's auto-edits:** Esc-Esc → rewind to the pre-pass checkpoint.
- At most one background task (the N+1 prefetch) is ever alive; it is read-only
  and short. To kill it immediately, `/tasks` → stop. Single/double ESC does
  **not** stop background tasks.

Do not commit or push unless the author asks.
