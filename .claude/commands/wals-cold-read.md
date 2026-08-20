---
description: Grounded cold read — run the full 6-model blind panel on a chapter (or range)
argument-hint: <scene-slug | N | A..B> [--models <id,...>] [--fresh]
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
| `claude-fable-5` | subagent | `blind-reader-grounded`, `model: fable` |
| `claude-opus-4-8` | subagent | `blind-reader-grounded`, `model: opus` |
| `claude-sonnet-5` | subagent | `blind-reader-grounded`, `model: sonnet` |
| `gpt-5.6-terra` | codex | `cold_read_grounded.py --model gpt-5.6-terra` |
| `gpt-5.6-sol` | codex | `cold_read_grounded.py --model gpt-5.6-sol` |
| `gpt-5.5` | codex | `cold_read_grounded.py --model gpt-5.5` |

A run with no `--models` is the **full panel**. `--models terra,sonnet` (any
comma list of ids or shorthands) scopes it; the **fast probe** is
`terra,sonnet`. **Token rule (standing):** never `--auth api-key` without
specific author authorization — the codex trio runs on **codex subscription
auth** (the harness default), and the Claude trio runs as **subagents**, which
consume no API tokens.

## Step 1 — Resolve targets and preconditions

1. Targets: a slug, a chapter number, or `A..B` (numbers or slugs). Resolve
   slug ↔ number via the harness's reading order (Vol 1 drafted + Vol 2 drafted
   in chronology order). The chapter's chronology entry must say
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

## Step 3 — Claude trio (fable, opus, sonnet): packet-MCP subagents

The Claude readers are **`blind-reader-grounded` subagents** blinded through
the packet MCP server — never paste prose into their prompts and never hand
them repo paths.

For each (model × chapter):

1. `tools/cold_read_grounded.py --model-id <model-id> --emit-packet <N>` —
   mints a token dir under `reviews/cold-read/.packets/` holding the packet
   files + a `.dest` routing the output to
   `reviews/cold-read/<model-id>/<slug>.md`. **One packet per model per
   chapter** (the `.dest` differs).
2. Spawn a `blind-reader-grounded` subagent with `model:` fable/opus/sonnet,
   passing ONLY the packet id. It reads via `list_packet`/`read_packet` and
   persists its reaction via `write_output`. All (model × chapter) subagents
   can go in one message — the reads are independent.
3. Verify the output file landed. If a subagent returned its reaction as text
   instead of calling `write_output`, salvage it:
   `tools/cold_read_grounded.py --persist-output <PACKET_ID>` with the text on
   stdin. Never retype/paraphrase a reaction by hand.

**Blindness invariants:** the subagent prompt contains no slug, no chapter
number beyond what the packet shows, no planning material, no framing about
what the scene "does." `CLAUDE.md` is inherited by subagents — spoiler-grade
material must stay out of it (it lives in `meta/meta-orientation.md`).

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
