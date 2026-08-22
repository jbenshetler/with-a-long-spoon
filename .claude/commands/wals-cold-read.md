---
description: Grounded cold read — run the full 6-model blind panel on a chapter (or range)
argument-hint: <scene-slug | volN | N | A..B> [--models <id,...>] [--fresh]
---

Run a **grounded cold read**: for each target chapter, each panel model reads
blind — no planning material, no chain — with **grounded memory** instead of a
carry-forward: the volume packet (jacket), the decade checkpoint `ck-ch<B>`
(minted in one pass from the raw prose of ch 1..B), the raw clean prose of the
chapters since that boundary, and the chapter itself. Reads are mutually
independent, so models AND chapters fan out in parallel.

The **chained lane is retired** (author ruling 2026-08-19 — it forgets too
badly). Never run `tools/cold_read.py`'s chained mode or spawn `blind-reader`
for a new review; the chained archive lives frozen under
`reviews/cold-read/<model-id>/chained/`. The shared file contract is
`reviews/cold-read/SPEC.md` (Grounded read v3).

## The panel (default: ALL SIX, author ruling 2026-08-19)

| Model id | Lane | How |
|---|---|---|
| `claude-fable-5` | headless | `cold_read_grounded.py --model claude-fable-5` |
| `claude-opus-4-8` | headless | `cold_read_grounded.py --model claude-opus-4-8` |
| `claude-sonnet-5` | headless | `cold_read_grounded.py --model claude-sonnet-5` |
| `gpt-5.6-terra` | codex | `cold_read_grounded.py --model gpt-5.6-terra` |
| `gpt-5.6-sol` | codex | `cold_read_grounded.py --model gpt-5.6-sol` |
| `gpt-5.5` | codex | `cold_read_grounded.py --model gpt-5.5` |

A run with no `--models` is the **full panel**. `--models terra,sonnet` (any
comma list of ids or shorthands) scopes it; the **fast probe** is
`terra,sonnet`. **Token rule (standing):** never `--auth api-key` without
specific author authorization — the codex trio runs on **codex subscription
auth** (the harness default), and the Claude trio runs headless on **Claude
subscription OAuth** (the harness scrubs `ANTHROPIC_API_KEY`, so pay-per-token
billing is impossible by construction).

## Step 1 — Resolve targets and preconditions

1. Targets: a slug, a chapter number, `A..B` (numbers or slugs), or a whole
   volume as `vol1`/`vol2`/`vol3` (the harness expands `--scope volN` to that
   volume's drafted chapters; the jacket still injects only at the volume's
   opening chapter). Resolve slug ↔ number via the harness's reading order
   (Vol 1 drafted + Vol 2 drafted in chronology order). The chapter's chronology entry must say
   **`Draft complete`** — the harness fails closed otherwise; fix the status
   only if the chapter truly is drafted end to end.
2. `tools/cold_read_grounded.py --check --scope <slug>` (or `--from/--to`) —
   verify the needed `ck-ch<B>` checkpoints exist **for every panel model**.
   If one is missing, STOP and tell the author: minting is a separate,
   high-effort job (`checkpoint_extract.py` for codex models;
   `--emit-bundle-packet B` + a `blind-extractor` subagent for Claude models).
   Do not mint implicitly.
3. Volume packet: the harness injects the volume's public jacket copy from
   `reviews/cold-read/volume-packets.toml` into every prompt. If the target's
   volume has no packet yet, ask the author whether to run without jacket copy
   (they have ruled this per-volume before) — do not substitute another
   volume's packet.
4. Without `--fresh`, skip targets that already have
   `reviews/cold-read/<model-id>/<slug>.md` for a given model (resume).

## Step 2 — Codex trio (terra, sol, gpt-5.5): inline background runs

For each codex model, launch in the background and let them run concurrently:

```
tools/cold_read_grounded.py --model <id> --scope <slug>        # one chapter
tools/cold_read_grounded.py --model <id> --from A --to B -j 4  # a range
```

The harness assembles the prompt, runs the reader at **low effort** (high
turns a reader into a critic), and writes
`reviews/cold-read/<model-id>/<slug>.md` itself.

## Step 3 — Claude trio (fable, opus, sonnet): headless clean lane

**(Author ruling 2026-08-22, superseding the packet-MCP subagent lane.)** The
Claude readers run exactly like the codex trio — background harness
invocations, one per model:

```
tools/cold_read_grounded.py --model claude-fable-5   --scope <slug> [--fresh]
tools/cold_read_grounded.py --model claude-opus-4-8  --scope <slug> [--fresh]
tools/cold_read_grounded.py --model claude-sonnet-5  --scope <slug> [--fresh]
```

The harness spawns `claude -p` on subscription OAuth with the
`blind-reader-grounded` agent def as the **entire** system prompt
(`--exclude-dynamic-system-prompt-sections`), from a throwaway non-repo cwd,
env scrubbed of `ANTHROPIC_API_KEY` — so no `CLAUDE.md`/`AGENTS.md`, git
commit snapshot, or memory index can reach the reader (all three were
probe-confirmed leaks in the in-session subagent lane, 2026-08-22). The
harness writes `reviews/cold-read/<model-id>/<slug>.md` itself.

**Never spawn in-session `blind-reader-grounded` subagents for panel reads** —
they inherit ambient session context. The packet-MCP path (`--emit-packet` +
subagent, salvage via `--persist-output`) remains only as a documented
fallback if the headless lane is unavailable, and its reads should be treated
as potentially contaminated.

## Step 4 — Verify and report

- Count the files: `ls reviews/cold-read/*/<slug>.md` — a full-panel run is 6.
- Skim each for a refusal/no-read signature before trusting it; a refusal is
  re-run, not recorded.
- Report per model: Heat/Romance (0–3), what landed as designed, what confused
  or bounced, convergent friction (2+ models) vs. singleton taste. Check
  `meta/meta-triage-<slug>.md` first so settled criticisms aren't re-litigated.
- Reviews are **reactions, not canon**; flag, never rewrite prose from them.
- If the chapter was edited after a prior grounded read, that read is stale —
  offer `--fresh`. Chapters *after* the target are unaffected (no chain).

Non-destructive: writes only under `reviews/cold-read/<model-id>/`. The
`.packets/` token dirs are ephemeral transport — never commit them.
