---
description: Inspect and clear the lore-keeper subagent's persistent memory
argument-hint: check | list | grep TERM | forget SLUG [--to NEW] | wipe --all
---

Manage the lore-keeper subagent's **persistent memory** — its hand-authored
notes under `.claude/agent-memory/lore-keeper/*.md`. This is a different store
from the `na.py` search index: `reindex` rebuilds the index from disk and
self-heals on renames/deletes, but these notes do **not**, so a renamed or
deleted scene leaves a stale pointer here that only this command clears.

Run the tool with whatever the author passed (default to `check` if no args):

```
tools/lore_mem.py $ARGUMENTS
```

Then interpret the output for the author. Hold to these rules:

- **Never delete without an explicit, in-this-turn go-ahead.** The `wipe` and
  `forget --delete` paths require `--yes`; do **not** add `--yes` yourself off a
  standing instruction. First run the command *without* `--yes` to show the
  plan, report exactly what would be removed, and let the author confirm. Only
  then re-run with `--yes`.
- **`check` over-reports on purpose.** It flags every `.md` reference that
  doesn't resolve on disk. Some are genuinely stale (renamed/deleted scenes —
  the tool tags high-confidence `(renamed? -> …)` article-drop cases); others
  are **planned-not-yet-drafted** scenes the memory legitimately references.
  Present the split; never mass-`forget` a whole `check` run.
- **Prefer surgical fixes.** For a rename, `forget <old-slug>.md --to <new>.md`
  rewrites the pointer in place (non-destructive) rather than deleting the note.
- **Full wipe is a last resort** — those notes are expensive curated canon
  (e.g. `cassie-canon.md`, `spring-satc-inventory-current.md`). Only wipe on an
  unambiguous request, and say what's being lost first.
- **Git note:** the memory dir is git-ignored, so edits are local-only — except
  a couple of tracked-despite-ignore notes, whose changes will show in
  `git status`. Deletions are already git-aware (`git rm` for tracked files).

Report back plainly: what the command found or changed, and — for a `check` —
which dangling refs look like real staleness worth a `forget --to` versus
planned scenes to leave alone.
