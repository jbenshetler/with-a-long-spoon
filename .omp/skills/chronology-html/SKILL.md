---
name: chronology-html
description: >-
  Rebuild chronology.html after edits to meta/meta-plan-chronology.md using
  tools/chronology_html.py, preserving the chronology edit workflow and review
  tracking conventions.
---

# chronology-html — rebuild chronology.html

Use this skill whenever `meta/meta-plan-chronology.md` is edited or when the
author asks to rebuild `chronology.html`.

## Canonical command

Run from the novel repo root:

```sh
tools/chronology_html.py
```

Use the OMP `bash` tool with `cwd` set to the repo root. Do not wrap the command
in `cd ... &&`.

Expected success output is shaped like:

```text
wrote chronology.html: <entry-count> entries, <dated-count> dated, status {...}
```

## Required workflow

1. Make the intended edit to `meta/meta-plan-chronology.md`.
2. Run `tools/chronology_html.py`.
3. Keep the regenerated `chronology.html` with the chronology edit. Never leave a
   chronology source edit without the matching HTML rebuild.
4. Verify the generated HTML contains the changed entry, especially any changed
   title, slug, date, status, or review chip.

## Review tracking

To mark a scene reviewed, append an ISO-date segment to that scene's metadata
line in `meta/meta-plan-chronology.md`:

```text
· reviewed: YYYY-MM-DD
```

For later review passes, append the date to the existing field:

```text
· reviewed: 2026-07-12, 2026-09-30
```

Only the author supplies review dates. Do not invent them. After editing the
reviewed field, rebuild `chronology.html` and verify the scene card displays the
newest date in its review chip.

## Verification patterns

Use targeted checks, not broad rereads:

- Source check: read or grep the edited entry in `meta/meta-plan-chronology.md`.
- HTML check: grep `chronology.html` for the title/slug and the changed date or
  status.
- Rebuild check: confirm `tools/chronology_html.py` exited successfully and
  reported `wrote chronology.html`.

If the rebuild fails, fix the chronology source or generator issue at the source,
then rerun the generator before yielding.
