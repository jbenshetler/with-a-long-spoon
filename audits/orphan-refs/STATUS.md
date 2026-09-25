# Orphaned references (Lane B) — status, Volume One

Text still pointing at something a revision removed. Worked case: a passer-by
"in a camel coat too warm for the afternoon" and Randi's verdict "She'd be a
project" were cut from `the-pointing-game` (`ade99b4b`), but a later sentence
still reads "the closed camel-coat project would never laugh at anything in
public" — a callback to a character and a coinage the reader now never meets.

Harness `tools/orphan_refs.py`. Sweeps at `audits/orphan-refs/vol1-<date>.txt`.
Pass tracked in `meta/meta-plan-editorial-checklist.md` (Lane B).

Deterministic and free, so it runs in three places, which are **not**
interchangeable:

- **Per edit** — `AGENTS.md` → *Before writing any prose*, step 3b. Required
  whenever an edit cut or replaced anything, and it must be given **every
  chapter that recalls the edited one**, because the orphan surfaces in the
  *other* file (`between.md` ↔ `barely-stings.md` is the worked pair).
- **Pre-commit** — `.githooks/pre-commit` runs `--staged`, **advisory only**:
  it fires after you stage, is silenced (`2>/dev/null || true`), and sees only
  staged paths. It cannot substitute for either of the others.
- **This pass** — the systematic front-to-back sweep, ruled with the author.

**Discipline: FLAGS, never findings.** The tool says so in its own header —
"an ordinary surviving use is common." A term whose introducing text was cut is
usually still fine; the question is always whether *this* surviving use leans on
what the reader no longer has.

**Rulings live in `orphan-allow.toml`** (this directory, versioned). The sweep
re-derives from git on every run, so without it every dismissed candidate comes
back forever. When the author rules a hit ordinary:
`tools/orphan_refs.py --slugs <slug> --ack --fp <hash> --note "why"` (the hash
is the `[#…]` tag). Same shape and rules as `na.py style --ack`: anchored to the
line's *content*, so it survives reflow but re-arms if the line's wording
changes; **only after the author signs off**. `--show-suppressed` re-shows,
`--unack --fp <hash>` reverses. Entries for hits no longer flagged are kept on
purpose — Lane B's thresholds let findings vanish and return — and are dropped
only by an explicit `--prune-allow --yes`, which touches only the chapters
scanned. A hit the author rules a *real* orphan is fixed in the prose, not acked.

## Sweeps

| Date | Scope | Result | State |
|---|---|---|---|
| 2026-09-19 | Volume One, 52 chapters | 26 candidates | **audited, none ruled** |

`vol1-2026-09-19.txt`. Each entry gives the slug, the orphaned term, how many
chapters it appears in, **the commit that cut the referent**, and the surviving
lines with line numbers — so a candidate can be judged against the diff that
created it.

## The 26 candidates, unruled

Concentrated in the chapters that took the heaviest revision:

| Chapter | Candidates | Terms |
|---|---|---|
| the-bench | 10 | position she, massage table, wooden top, table again, body warm, belly and, time without, breasts the, massage, audible |
| the-pointing-game | 6 | camel coat, seam in, small recoil, recoil, camel, ponytail |
| two-towels | 3 | brick red, magazine that, reflex |
| see-you-later | 2 | thing randi, notebook |
| nothing-underneath | 2 | fingers moving, or anything |
| leave-no-trace | 1 | rock at |
| outlier | 1 | stack of |
| rock | 1 | love in |

Worth ruling first, on two grounds — the **camel-coat cluster** in
`the-pointing-game` (camel coat / camel / ponytail, three candidates pointing at
one cut passer-by) is the pass's own worked example and the likeliest true
orphan; and `the-bench`'s **bench-furniture cluster** (massage table / wooden
top / table again / massage), since two separate commits cut bench-intro
material there and four candidates survive it.

Candidates spanning 3 chapters (`thing randi`, `stack of`, `camel`, `reflex`,
`ponytail`) are the most likely to be ordinary surviving uses rather than
orphans — breadth across chapters usually means the term lives independently of
the cut text.

## Restart

1. Rule the two clusters above with the author against the cutting commits.
2. Record verdicts in the chapter's `meta/meta-triage-<slug>.md` — authorial
   decisions live in `meta/`, not under `audits/` — and mark the sweep row
   `reviewed` here.
3. Re-sweep after the ruling pass, and after any run of chapter revisions; a
   new dated file per sweep, never overwriting the prior one.

## Rulings

**None recorded yet.**
