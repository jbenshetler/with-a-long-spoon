# Chronology Update Protocol

*This file governs when and how `meta-plan-chronology.md` must be updated.*
*Pointer to this file lives at the top of `meta-plan-chronology.md` and in `DOCUMENTS.md`.*

---

## When to Update

Update `meta-plan-chronology.md` whenever any of the following occurs:

- **A scene is drafted or substantially revised.** Update the entry's summary paragraph and status line to reflect what is actually on the page. The chronology summary is the authoritative description of the draft, not the planning notes that preceded it.
- **A scene is added to the plan** (even beats-only). Add a new entry with type label, approximate date, and whatever is known.
- **A scene's position in the sequence changes.** Cut and paste the entry to its new line within the phase; update the phase header if the scene moves between phases. No renumbering — order is list position.
- **A non-rendered event is established** as canonical backstory. Add an `[EVENT]` entry at the correct chronological position.
- **A continuity issue is resolved.** Update both the relevant entry and the continuity flags section (or remove the flag if resolved).
- **A character fact is established in a scene that doesn't exist elsewhere.** Add it to the entry summary so it doesn't disappear into a draft file.

## What Every Entry Must Contain

Every entry in the chronology — scene, vignette, or event — must have:

1. **Type label:** `[SCENE]`, `[VIGNETTE]`, or `[EVENT]`
2. **Title** — the scene's name, its permanent identity handle. **No sequential number:** narrative order is carried by list position within the phase (see `meta-plan-schedule.md`), and sub-clusters sit in plain adjacency. Cross-references everywhere use the name, never a number.
3. **Approximate date and day of week** — format: `~Fri Sep 1` or `~early October`. Use `~` for all approximations. Pin to specific dates where the narrative requires it (e.g. Standards must land on a Saturday morning).
4. **Status line:** `draft complete`, `partial`, `beats only`, `unwritten`, or `not a scene` — plus file reference if a draft exists
5. **Summary:** one paragraph maximum for scenes and vignettes; one to two sentences for events. For completed drafts, the summary must reflect what is actually written, not the original plan.

## Entry Types

**`[SCENE]`** — full prose scene; has its own file or will have one. Planning entry is a full summary paragraph.

**`[VIGNETTE]`** — shorter prose; single image or beat; no full dramatic arc. One or two sentences in the planning entry. Gets a file if drafted; doesn't require one in advance.

**`[EVENT]`** — not rendered in prose; canonical in-universe fact needed for timeline reasoning. One or two sentences. No file. Include a pointer to the document where the backstory lives if relevant.

## What to Check for Consistency

When adding or revising an entry, check:

- **Date arithmetic.** Does the new date fit between its neighbors? Does the day of week follow correctly from the previous scene's day?
- **Continuity flags.** Does the new entry resolve or create a continuity issue? Update the flags section accordingly.
- **Status of related entries.** If a scene's draft changes what a later scene assumes, note it. If a SATC scene's content changes, check that the corresponding source scene's entry is consistent.
- **File references.** If a file is renamed, update all chronology pointers to it.
- **Phase placement.** If a scene's date now falls in a different phase, move it and update both phase headers.

## Format Reference

```
### [SCENE] Substitution
**~Thu Sep 24 · Week 4 of fall semester**
*Draft complete · `substitution.md`*

Summary paragraph here — one paragraph maximum, accurate to the draft.
```

```
[EVENT] **~Sat Aug 5 · Pre-novel**
*Not a scene · backstory in `meta-arch-bible.md`*
Pace meets Randi on the sorority common. First date follows within the week.
```

```
### [VIGNETTE] The Good Shirt / No-Tag Plant
**~late September · Early phase**
*Unwritten · will fold into an existing early domestic beat*
Pace gives Vee a well-made shirt with no brand tag. She notices the absence, guesses wrong, drops it.
```
