# Figure sweep — status

Repeated metaphors and similes across the whole book. Skill
`.claude/skills/wals-figure-sweep/`; tool `tools/figure_harvest.py`; acceptance
set `gold.md`; rulings `rulings.md`; designed families `designed.md`.

## Runs

- 2026-10-27 · gpt-5.6-sol (effort high) · trial, stopped by the author after 5
  chapters: too slow for the job. Archived in `.old/` (gitignored).
- 2026-10-27 · claude-sonnet-5-5 + gpt-6.1-terra (medium), first prompt ·
  extraction recall 28/28 and 27/28, but grouping split every gold group:
  free-text picture and feeling labels did not merge. Archived in `.old/`.
- 2026-10-27 · claude-sonnet-5-5 + gpt-6.1-terra (medium), vehicles and
  sensation prompt, gold chapters (24) · union: recall 28/28, 1 literal
  reported (`made-up:35` "the lamp throwing its circle"), groups 4 of 5 `ok`.
  The lamp group splits on `how-its-done:15` ("like sun on her face", picture
  *sun*, not *light*). Whole book: not run.
- 2026-10-27 · gold rulings (author): `how-its-done:15` "like sun on her face"
  is its own picture group (sun), not the lamp; `made-up:35` stays a known
  literal false positive. Rescored: recall 28/28, 1 known literal, all 6 gold
  groups `ok`. **Gate passed.** Whole book: not run (needs the author's go).

