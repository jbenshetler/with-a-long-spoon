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

**`build/a-polite-invitation.epub`** — reader-facing filename = the volume
title, *A Polite Invitation* (Volume One of the *With a Long Spoon* trilogy;
titles per `meta-blurb.md`). (The `build/` dir is gitignored — outputs are
artifacts, never committed.)

**The default filename is plain** (author ruling 2026-08-09). The build stamp
— `<source-date> · <sha>`, gaining **`+dirty` when any build input is
uncommitted** — still identifies every copy, but it lives *inside* the file
(copyright page + OPF metadata), not in the filename. If you see `+dirty` and
didn't intend a scratch build, commit first and rebuild so the artifact
carries a real commit stamp.

**`--stamped-name`** appends `-<source-date>-<sha>` to the filename, for
keeping builds of different drafts side by side. **`--reader`** names the file
for its recipient (see below).

Assembly order, per the "Test-epub assembly" spec in `meta/meta-blurb.md`:

cover → **blurb page before the title page** (simulates the retail listing:
decided blurb, centered tagline, *Beauty* comp line) → title page → copyright
→ Volume One chapters (story order = chronology list order; SCENE/VIGNETTE
entries only) → note to test readers.

All sources are parsed at build time — chronology, blurb, and scene prose stay
authoritative in their own files, so an edit there flows into the next build
with no script change. Builds are **deterministic**: identical inputs produce
byte-identical epubs (diffable rebuilds). Note the build stamp (source date +
sha) is part of the output, including the metadata UUID — so rebuilds at
*different commits* differ by design, and only same-commit rebuilds compare
byte-for-byte.

## Canonical invocations

```
tools/build_epub.py --list                                    # ALWAYS run first: roster preview + missing-prose check, no build
tools/build_epub.py                                           # build/a-polite-invitation.epub
tools/build_epub.py --reader "Jane Doe <jane@example.com>"    # build/a-polite-invitation-jane-doe.epub
tools/build_epub.py --stamped-name                            # build/a-polite-invitation-<date>-<sha>.epub
tools/build_epub.py -o build/custom-name.epub
```

- **Run `--list` before every build** — it prints the numbered chapter roster
  and flags any Volume One chapter whose prose file is missing.
- A missing prose file **aborts the build by design** (a test reader must
  never receive a silently incomplete book). `--allow-missing` overrides;
  never use it without the author's explicit say-so.
- **Never invent a pen name.** `--author` now defaults to the recorded
  decision, **Helen Rivers** (`meta/meta-plan-pen-name.md`, 2026-07-30) — use
  it unless the author says otherwise, and never substitute a different name.

## Per-reader copies (`--reader`)

`--reader "Jane Doe <jane@example.com>"` — a bare email or a bare name also
parses — stamps the recipient into the copy in four places:

- the **copyright page**: "Prepared for Jane Doe (jane@example.com)."
- the **note to test readers**: greets them by first name and closes with the
  same identification, so the watermark sits where a reader actually reads
- the **OPF metadata**: `wals:recipient`
- the **filename**: `build/a-polite-invitation-jane-doe.epub`

and appends a row to **`build/RECIPIENTS.tsv`** (built-at, name, email, build
id, filename, package uuid), so a leaked copy maps back to a person. Each
recipient's copy also gets a distinct package UUID, since the UUID is derived
from content.

**That ledger holds real names and email addresses.** It lives in `build/`
because `build/` is gitignored — never commit it, never paste its contents
into a session, and never read it into context to answer a question about who
has a copy.

Per-reader copies are the deliberate exception to determinism: two readers'
copies of identical prose differ, which is the whole point. A rebuild for the
*same* reader from the same inputs is still byte-identical.

This is a deterrent, not forensics — the metadata and copyright lines are
strippable by anyone who thinks to look. Per-copy invisible variation in the
prose was considered and declined (2026-08-09): real attribution, but only
worth it if a leak would actually be pursued.

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
note-to-test-readers text and copyright lines live **only in the script**
(`note_to_readers()`, `COPYRIGHT_NOTICE`, `DRAFT_NOTICE`) — changing them is a
code edit to `tools/build_epub.py`, committed like any tool change.

## What this skill does NOT cover

**Delivery.** The author sends the built copies to test readers directly; this
skill stops at the file on disk.
