---
name: wals-epub
description: >-
  Build the Volume 1 test epub with tools/build_epub.py — chapters assembled
  from scenes/ in chronology order, front/back matter per the packaging spec
  in meta/meta-blurb.md. Use whenever the author asks to build, rebuild, or
  preview the epub (or its chapter roster). Standardizes the invocation to the
  permission-allowlisted form `tools/build_epub.py` from the repo root.
---

# wals-epub — build the Volume 1 test epub

The allowlisted command prefix is `Bash(tools/build_epub.py:*)`. **Always
invoke it exactly as `tools/build_epub.py …` from the repo root** — never
`./tools/...`, never an absolute path, never via `python3 tools/...`. Each of
those is a different, un-allowlisted command string and will prompt.

## What it builds

`build/with-a-long-spoon-book-one.epub` (the `build/` dir is gitignored —
outputs are artifacts, never committed). Assembly order, per the "Test-epub
assembly" spec in `meta/meta-blurb.md`:

cover → **blurb page before the title page** (simulates the retail listing:
decided blurb, centered tagline, *Beauty* comp line) → title page → copyright
→ Volume One chapters (story order = chronology list order; SCENE/VIGNETTE
entries only) → note to test readers.

All sources are parsed at build time — chronology, blurb, and scene prose stay
authoritative in their own files, so an edit there flows into the next build
with no script change. Builds are **deterministic**: identical inputs produce
byte-identical epubs (diffable rebuilds).

## Canonical invocations

```
tools/build_epub.py --list                 # ALWAYS run first: roster preview + missing-prose check, no build
tools/build_epub.py --author "Pen Name"    # the real build
tools/build_epub.py --author "Pen Name" -o build/custom-name.epub
```

- **Run `--list` before every build** — it prints the numbered chapter roster
  and flags any Volume One chapter whose prose file is missing.
- A missing prose file **aborts the build by design** (a test reader must
  never receive a silently incomplete book). `--allow-missing` overrides;
  never use it without the author's explicit say-so.
- **Never invent a pen name.** `--author` defaults to `Anonymous` (with a
  warning); if the author hasn't specified one, ask — don't guess.

## Inputs (defaults; override flags exist for each)

- `meta/meta-plan-chronology.md` — chapter inventory + order (`--chronology`)
- `meta/meta-blurb.md` — blurb page + epub metadata description (`--blurb`)
- `scenes/` — prose; H1 and the leading italic editorial note above the first
  `---` are stripped, interior `---` become scene breaks (`--scenes`)
- `images/cover.png` — cover (`--cover`; **any** run, even `--list`, aborts
  if absent). It's a **symlink** naming the currently chosen cover asset —
  to switch covers, retarget the link (`ln -sfn <asset>.png images/cover.png`),
  don't edit the builder.

There is deliberately **no decorative page background** (the parchment
treatment was removed 2026-07-27): CSS background images fight reader
theming (dark-mode contrast) and pagination (Calibre partial renders,
Apple Books bleed). Don't reintroduce one.

## When to rebuild

After any edit to the chronology (chapter order/inventory), the Test-epub
blurb section of `meta-blurb.md`, or Volume One scene prose. The
note-to-test-readers text and copyright lines live **only in the script's
constants** (`NOTE_TO_READERS`, `COPYRIGHT_NOTICE`, `DRAFT_NOTICE`) — changing
them is a code edit to `tools/build_epub.py`, committed like any tool change.

## What this skill does NOT cover

Watermarking and delivery are downstream, out of scope: the author builds
per-reader watermarked copies from this epub with their own process and sends
them directly to test readers.
