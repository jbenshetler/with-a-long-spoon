---
name: na
description: >-
  Use the With a Long Spoon novel-assistant CLI (tools/novel-assistant/na.py)
  from OMP: session-start reindexing, recall-first search over scenes/ and
  meta/, regex lookup, and the DB-free prose style linter.
alwaysApply: true
---

# na — novel-assistant CLI for With a Long Spoon

Use `tools/novel-assistant/na.py` for novel-corpus recall and style checks.
Run it from the novel repo root. In OMP, set the `bash` tool's `cwd` to the
repo root when the session is in a subdirectory; do not wrap it in `cd ... &&`.

Canonical command prefix:

```sh
tools/novel-assistant/na.py <command> ...
```

Avoid absolute paths and `./tools/...` unless there is a concrete reason. The
relative repo-root path keeps usage portable across clones and sessions.

## Prime rule

Never answer a factual question about the novel from memory when `na.py` can
check the corpus. Use recall search first, read the source passages that answer,
and cite the file/section you used. If the index cannot answer, say so; do not
fill canon gaps by inference.

`na.py search` already prints ranked, readable results: rank, file, sequence,
score, heading path, flags, and snippet. Use that output directly. Only use
`--json` when a caller must parse records programmatically. For full context,
take the file path and heading from the search output and use `read` on the
source file.

## Reindex — session-start maintenance

Run once near the start of a novel-work session, before relying on recall:

```sh
tools/novel-assistant/na.py reindex
```

Useful variants:

```sh
tools/novel-assistant/na.py reindex --scan     # dry run: report stale files only
tools/novel-assistant/na.py reindex --force    # rebuild the DB from scratch
```

Reindexing is incremental and hash-gated. Semantic indexing needs Ollama at
`OLLAMA_URL` (default `http://localhost:11434`) with `NA_EMBED_MODEL` (default
`nomic-embed-text`). Regex search and style checks do not need Ollama.

## Search — recall over scenes/ and meta/

```sh
tools/novel-assistant/na.py search "QUERY"
tools/novel-assistant/na.py search "QUERY" --top 8
tools/novel-assistant/na.py search "QUERY" --k 80 --top 20
tools/novel-assistant/na.py search "QUERY" --active-edit <slug> --max-sequence <slug>
```

Guidance:

- `--top N` controls returned results; `--k N` controls the per-lane candidate
  pool.
- When drafting or editing a scene, pass `--active-edit <slug>` to tag the WIP
  scene and its lagging companion note.
- Also pass `--max-sequence <slug>` when answers must be scoped to what exists
  as of that scene, so downstream chronology does not leak in.
- Search covers both `scenes/` prose and `meta/` planning files.

## Regex lane — keyword/PCRE lookup without Ollama

```sh
tools/novel-assistant/na.py search "P(ace|eter)\\b" --regex
tools/novel-assistant/na.py search "green\\s+sheets" --regex -i
tools/novel-assistant/na.py search "PATTERN" --regex -i --file 'scenes/%'
```

`--regex` is a pure pattern lane over indexed section text: no embedding, no
similarity lane, same staleness/scope flags as semantic search. Use `-i` for
case-insensitive matching. `--file` is a SQL `LIKE` filter, e.g. `scenes/%` or
`meta/%`.

## Style — DB-free prose linter

```sh
tools/novel-assistant/na.py style scenes/<slug>.md
tools/novel-assistant/na.py style
tools/novel-assistant/na.py style --all
tools/novel-assistant/na.py style --all --severity error
tools/novel-assistant/na.py style scenes/<slug>.md --show-suppressed
```

Style checks read live files, not the index. They work on explicit paths even
before a new scene is indexed. They flag candidates; they never fix prose.
Treat `error` severity as a real canon breach, not a style nicety.

Acknowledge only after the author explicitly signs off:

```sh
tools/novel-assistant/na.py style scenes/<slug>.md --ack --fp <hash> --note "why this stands"
tools/novel-assistant/na.py style scenes/<slug>.md --unack --fp <hash>
```

The fingerprint is the `[#...]` value printed in style output. A bare `--ack`
acknowledges every active hit in scope; use it only when that is the explicit
intent. Acknowledgements are written to `style/style-allow.toml` and should be
committed with the novel when they represent authorial decisions.

## OMP usage notes

- Use `bash` for one `na.py` invocation at a time; it is a real CLI command.
- Use OMP `read` for source files named by search output.
- Use OMP `grep`/`glob` for codebase mechanics, but use `na.py search` for
  novel-corpus recall because it combines FTS, embeddings, chronology, staleness,
  and active-edit flags.
- Do not pipe default search output through ad-hoc parsers. Prefer the printed
  ranking plus targeted `read` calls.
- If a lookup is broad, split independent questions and run them in parallel;
  keep each query focused so returned passages are filterable.
