# Authoring context — loading what came before, before drafting

*Working procedure for the authoring assistant. Kept out of `AGENTS.md` on purpose:
that file is auto-injected into the tool-less cold-read subagents (`blind-reader`,
`blind-extractor`), which receive its text but cannot follow any reference in it — so
this procedure never reaches the blind instrument. Load it after the `meta/` canon
docs (the Read list in `AGENTS.md`), never before.*

---

## What this is

When drafting chapter **N**, you need what has come before — not as a fact you look up
one at a time (that stays the `lore-keeper`'s job), but as **standing reader-memory**:
who's who, the relationship states and milestone flags, the dramatic-irony ledger, the
live motifs, the open questions the reader is holding. That memory already exists as the
spec-blind decade **checkpoints** under `reviews/cold-read/<model>/checkpoints/`.

`tools/checkpoint_context.py` assembles the authoring view of it:

```
tools/checkpoint_context.py --to N            # opus checkpoint by default
```

It emits, in order:

1. the most-recent **decade memory checkpoint** (`ck-ch{B}`, where `B = ((N-1)//10)*10`),
   **projected** — the reader-reaction `Impression` section is sliced off so it can't be
   mistaken for canon; the seven factual/ledger sections are kept;
2. the **full clean prose** of every chapter since that checkpoint (`ch B+1 .. N-1`).

This is **read-time assembly** — it never mints a new consolidated checkpoint, so nothing
decays across a summary-of-a-summary chain. The decade checkpoint is read verbatim (it was
already panel-QA'd); the recent window is real prose at full fidelity.

## How to use it when drafting

1. Load the `meta/` canon docs first (the Read list / `lore-keeper` prep). **Meta before
   the checkpoint** — canon is the foundation; the checkpoint colors on top of it.
2. Run `tools/checkpoint_context.py --to N` and bring its output into context. The recent
   prose lands last, so it sits freshest.
3. Draft. The per-scene `lore-keeper` prep still runs — this background load **composes
   with** it, it does not replace it.

**It is reader-memory, not ground truth.** It tells you what the reader knows and expects
at chapter N — exactly what you need to calibrate the next chapter's reveals. Canonical
facts ("what is actually true") still go through the `lore-keeper`.

## Options

- `--model <id>` — which checkpoint (default `claude-opus-4-8`; e.g. `claude-fable-5`,
  `gpt-5.6-terra`). You author off opus, so opus is the default.
- `--check` — print the load plan (boundary, checkpoint present/missing, window range,
  keep-set) and emit nothing.
- `--keep a,b,c` / `--drop x,y` — re-cut the projection. The default keep-set lives in
  `DEFAULT_KEEP` in the tool (all sections except `Impression`).
- `--mint` — accept the offer to create a missing checkpoint without asking (codex mints
  directly; Claude hands off to a subagent). `--no-mint` — decline; proceed without it.

## When the decade checkpoint is missing — offer to create it

A missing decade checkpoint is expected the first time you draft into a new decade. The
tool **offers to create it** rather than failing; it exits with code **2** (`MINT_NEEDED`)
so you can react. **Offer the author, in the text flow, to mint it before loading context**
(it takes a few minutes) — don't silently mint or silently skip.

On the author's yes:

- **opus / fable (Claude models)** — the tool can't spawn the subagent itself, so mint it:
  it writes the clean bundle to `/tmp/ck-bundle-<model>-ch<B>.md` (or run
  `tools/checkpoint_bundle.py --to B`), spawn a **`blind-extractor` subagent** (no API
  tokens; `.claude/agents/blind-extractor.md` as system prompt, the bundle as the message,
  consolidate cold), save its output to
  `reviews/cold-read/<model>/checkpoints/ck-ch<B>.md` with the standard header, then re-run.
- **codex / OpenAI-family (terra/sol/gpt-5.5)** — re-run with `--mint`; it mints directly
  via `checkpoint_extract.py` (reads prose `1..B` at high effort) and then emits the context.

On the author's no, pass `--no-mint` and proceed without the checkpoint (recent prose only).

## Undrafted chapters are fine

The recent window (`ch B+1 .. N-1`) reaching past what's drafted is a **normal mid-draft
state**, not an error — you're often drafting forward before every earlier scene is final.
The tool includes whatever prose exists, prints a calm `[note]`, and proceeds. Likewise, if
a whole decade isn't drafted yet it can't mint that checkpoint — it says so and proceeds on
recent prose. A later editing pass catches the gaps.

**Decade discipline:** still mint + QA each decade checkpoint on schedule (every ten
chapters). It's the load-bearing assumption — let it lapse and the recent window quietly
grows past ten chapters.
