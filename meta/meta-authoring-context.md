# Authoring context — loading what came before, before drafting, revising, or critiquing chapters or beats

*Working procedure for the authoring assistant. Kept out of `AGENTS.md` on purpose:
that file is auto-injected into the tool-less cold-read subagents (`blind-reader`,
`blind-extractor`), which receive its text but cannot follow any reference in it — so
this procedure never reaches the blind instrument. Load it after the `meta/` canon
docs (the Read list in `AGENTS.md`), never before.*

---

## What this is

When drafting, revising, or critiquing chapter **N** or its beats, you need what has come before — not as a fact you look up
one at a time (that stays the `lore-keeper`'s job), but as **standing reader-memory**:
who's who, the relationship states and milestone flags, the dramatic-irony ledger, the
live motifs, the open questions the reader is holding. That memory already exists as the
spec-blind decade **checkpoints** under `reviews/cold-read/<model>/checkpoints/`.

`tools/checkpoint_context.py` assembles the authoring view of it:

```
tools/checkpoint_context.py --scene <slug>    # opus checkpoint by default
```

Address the chapter by its **slug**, not a number: `--scene` resolves the drafted
reading-order N for you (= 1 + the drafted chapters before it in chronology order;
`tools/volume_scenes.py --number <slug>` prints it). It works even when the target
chapter is itself undrafted — the case when you're about to write it. Never hand-count N
off the chronology: the chronology includes planned-but-undrafted entries, so its
position diverges from the drafted order the tool indexes (e.g. `another-round` is
chronology position 60 but drafted N 58). `--to N` remains for when you already know N.

Do not hand-assemble or supplement this context. `checkpoint_context.py` is the
authoring sibling of `tools/cold_read_grounded.py`; both use the same drafted-scene
inventory, boundary rule, and post-boundary prose window:

```
B = ((N-1)//10)*10
```

For chapter `N`, the authoring tool mirrors the grounded cold reader's **boundary and
prose-window topology**:

1. an authoring projection of `ck-ch{B}` — one checkpoint, not a cumulative stack;
2. the **full clean prose** of `ch B+1 .. N-1`.

When `B = 0`, there is no checkpoint and the tool emits the full clean prose of
`ch1 .. N-1`. The selected checkpoint sections are preserved verbatim; the
reader-reaction section is dropped by default so opinion is not mistaken for canon.

Ask the authoring tool for the exact plan before loading:

```
tools/checkpoint_context.py --scene <slug> --check
tools/checkpoint_context.py --scene <slug>
```

To audit that plan against the harness itself, resolve `N` with the `--check` command,
then run `tools/cold_read_grounded.py --emit-prompt N`. That command prints the actual
cold-reader packet. `checkpoint_context.py` retains its boundary checkpoint and recent
window, but removes the reader framing and current chapter and projects the checkpoint
to the authoring keep-set (dropping `Impression` by default).

Trust those tools rather than calculating or composing extra checkpoint commands. For
example, `--scene not-enough --check` resolves chapter N=49, boundary B=40,
`ck-ch040`, and full clean prose ch41–48. No `ck-ch050` belongs in that topology.

If the required boundary checkpoint is missing, follow the missing-checkpoint protocol
below — offer to mint it; do not silently skip it or substitute another checkpoint.

This is **read-time assembly**. It uses the same grounded checkpoint and post-boundary
prose window a cold reader receives; it does not mint a consolidated authoring memory
or create a summary-of-a-summary chain.

## How to use it before developing beats, drafting, revising, or critiquing

1. Load the `meta/` canon docs first (the Read list / `lore-keeper` prep). **Meta before
   the checkpoints** — canon is the foundation; reader-memory colors on top of it.
2. Run `tools/checkpoint_context.py --scene <slug> --check` and trust its reported
   boundary, checkpoint, and recent window. Then run the same command without
   `--check` and bring its complete output into context. The full recent prose lands
   after the checkpoint, so it sits freshest.
3. Only then draft, revise, critique, or develop beats. The per-scene `lore-keeper` prep
   still runs — this background load **composes with** it; it does not replace it.

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
