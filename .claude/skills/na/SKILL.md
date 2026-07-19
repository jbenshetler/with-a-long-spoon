---
name: na
description: >-
  Run the novel-assistant CLI (na.py) — search, reindex, style — using the
  canonical, permission-allowlisted command form. Use whenever you need to
  invoke na.py: recall search over scenes/ + meta/, the session-start reindex,
  or the prose style linter. Standardizes the invocation so it never triggers a
  fresh permission prompt — always the relative path tools/novel-assistant/na.py
  and the built-in formatted output, never a hand-written `python3 -c` JSON
  parser and never an absolute or ./-prefixed path.
---

# na — novel-assistant CLI

The allowlisted command prefix is `Bash(tools/novel-assistant/na.py:*)`. So
**always invoke it exactly as `tools/novel-assistant/na.py …` from the repo
root** — never `./tools/...`, never an absolute path, never piped into an
ad-hoc `python3 -c "..."`. Each of those is a different, un-allowlisted command
string and will prompt.

## Golden rule for output

`na.py search` **already prints clean, human-readable results** — rank · file ·
`seq` · score · heading path · snippet. Use that output directly. **Do not pipe
`--json` into a hand-written python one-liner** — that is exactly the "random
python lines" to stop doing. If you need the full untruncated passage for a hit,
take the file path from the search output and `Read` that file.

## Search — recall over scenes/ + meta/

```
tools/novel-assistant/na.py search "QUERY"
tools/novel-assistant/na.py search "QUERY" --top 8
tools/novel-assistant/na.py search "QUERY" --active-edit <slug> --max-sequence <slug>
tools/novel-assistant/na.py search "PATTERN" --regex               # keyword/PCRE lane, no Ollama
tools/novel-assistant/na.py search "PATTERN" --regex -i --file 'scenes/%'
```

- `--top N` results returned · `--k N` per-lane candidate pool.
- When drafting/editing a scene, pass **both** `--active-edit <slug>` (tags the
  WIP scene + its lagging companion) and `--max-sequence <slug>` (scope results
  "as of" that scene, so nothing downstream leaks in).
- `--regex` is a pure pattern lane that works with Ollama down; add `-i` for
  case-insensitive and `--file 'scenes/%'` (SQL LIKE glob) to restrict scope.
- Per CLAUDE.md, in the main session **factual lookups still go through the
  `lore-keeper` subagent** — this skill is how the command should be *shaped*
  (by lore-keeper, or by you for planning-corpus orientation), not a license to
  bypass that delegation.

## Reindex — run once at session start

```
tools/novel-assistant/na.py reindex            # incremental, hash-gated (the session-start command)
tools/novel-assistant/na.py reindex --scan     # dry run: report what's stale, write nothing
tools/novel-assistant/na.py reindex --force    # clear DB and re-embed everything
```

## Style — DB-free prose linter (needs no index, no Ollama)

```
tools/novel-assistant/na.py style scenes/<slug>.md              # one file (works even if unindexed)
tools/novel-assistant/na.py style                               # all of scenes/
tools/novel-assistant/na.py style --all                         # + meta/
tools/novel-assistant/na.py style --all --severity error        # hard canon rules only
tools/novel-assistant/na.py style scenes/<slug>.md --show-suppressed
tools/novel-assistant/na.py style scenes/<slug>.md --ack --fp <hash> --note "why"
```

- Flags candidates; it never fixes. `error` severity = a canon breach
  (`never-name`), not a style tic — treat it as a real violation.
- Only run `--ack` **after the author has signed off** — it records an
  authorial decision into `style/style-allow.toml`. `--fp <hash>` acks one hit
  (hash is the `[#…]` tag in output); bare `--ack` acks all hits in scope.

## If you genuinely need machine-readable output

Only when a caller must parse results programmatically. `--json` emits records
(`file`, `heading_path`, `flags`, `text`, …). Even then, prefer taking the file
path from the default output and `Read`-ing the source over parsing JSON. Do not
invent a new parser string per call.
