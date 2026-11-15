---
name: wals-ch-title
description: >-
  Propose new display titles for an existing chapter (scene) under the book's
  scene-title engine — innocuous surface going in, charged meaning on reread,
  never the central object or act — plus the criteria the past renames settled
  on and the retail-screen rule against age-coded words. Grounds the search in
  the chapter's prose, chronology entry, companion notes and neighbouring
  titles, then presents a ranked shortlist with surface / charge / goals /
  risks per candidate. Proposes only: a rename happens only on the author's
  explicit "rename X to Y", and then follows the rename checklist here. Use
  when the author asks for a new title, a retitle, title candidates, or says a
  title isn't working (telegraphs, collides, or trips a retailer or model
  safety screen).
---

# wals-ch-title — a title that means nothing until you've read it

**Authority:** the scene-title engine in `meta/meta-orientation.md` ("Scene
titles", `:67–86`). Load it fresh every run; it wins over anything restated
here. This skill adds (a) criteria the author settled during past renames that
live only in commit messages, (b) the retail-screen rule, and (c) the procedure.

Flag and propose. The author picks; nothing is renamed without an explicit
instruction (see **Title/slug scope lock** in `CLAUDE.md`).

## Step 1 — load context

1. The meta read list from `CLAUDE.md`, then the authoring projection:
   `tools/checkpoint_context.py --scene <slug> --check`, then without `--check`.
   Feed it as is.
2. `meta/meta-orientation.md:67–86` (the engine, endorsed examples,
   anti-patterns, the proposing format, calibration).
3. **The whole chapter**, `scenes/<slug>.md`. Read it all. Candidates come from
   its own language, and the strongest ones are often a phrase already on the
   page (Missed a Spot was Vee's dishwashing-pretext line).
4. Fan out lore-keepers **in parallel, one per query**, active slug `<slug>`:
   - the chapter's chronology entry (`meta/meta-plan-chronology.md`) — beats,
     `present:` field, any title history or `(was "…")` note;
   - its companion docs: `meta-note-<slug>.md`, `meta-condensed-<slug>.md`,
     `meta-triage-<slug>.md` — anything said about the title or the chapter's
     hinge, frame, final image;
   - the **neighbouring chapters** (two before, two after): their titles and
     what each turns on, so a candidate can chain or staircase, and doesn't
     collide;
   - any track doc or arch passage naming this chapter's job in the arc.
5. `tools/lint_titles.py --list` — the full current title set, for collisions
   and word clusters (no third "Held", no fifth chapter starting "The").
6. `git log --format='%h %ad %s' --date=short -i --grep="<current title>"` and
   the chronology entry — has this chapter been retitled before, and why? Don't
   re-propose a title already rejected.

## Step 2 — understand the chapter before naming it

Write down, for yourself, before any candidate:
- **The hinge** — the central act/object/turn. This is what a title must
  *not* name.
- **The frame** — the ordinary occasion, setting, routine or courtesy the hinge
  happens inside. Titles live here.
- **The final image and the closing line.**
- **Phrases on the page** with an innocent surface and a second meaning in
  context: dialogue, idioms, a character's pet words.
- **What a reread knows** that a first read doesn't (from the checkpoint and the
  later chapters the lore-keeper returned) — the charge often detonates later.

## Step 3 — the tests

**Hard floor (disqualifies):**
1. **Telegraphs** — names the central object, act, or the act plus its quality
   ("Forbidden Kiss", `37329bdf`; "Still My Shirt", "Wearing Him" — the
   orientation anti-patterns).
2. **Retail / safety screen** — no age-coded or minor-adjacent words
   (`meta/meta-blurb.md:214`, author 2026-10-20: retailer erotica filters read
   them as signals of minors; chapter titles land in the epub TOC, which is
   screened). Out: girl/girls, girlhood, child/childhood/kid, teen/teenage,
   young/youth, little, baby/babysit, school/schoolgirl/schoolyard, homework,
   class/classroom as a youth-school word, recess, cheer(leader), daddy, and
   anything evoking pre-college age. **College framing doesn't rescue the word
   — the filter can't see context** (why School Nights was retitled Not in Your
   Bed, 2026-11-15). Also check the *combination*: two innocent words can make an
   age-coded phrase. Flag borderlines ("first", "lesson", "student") rather
   than ruling on them.
3. **Collides** with an existing title or alias (`lint_titles.py --list`).
4. **Never-name.** Write the shortlist to a scratch file and run
   `tools/novel-assistant/na.py style <scratch> --severity error`; any hit is
   out.

**Goals (tradeoffs, not disqualifiers — orientation calibration):** hits more
than one of oblique · ambiguous · erotic · ironic · layered; meaningful only
after reading; deepens on reread.

**Precedent criteria** — settled in past renames, apply as tradeoffs:
- **Frame, not the hinge** (`37329bdf`, Missed a Spot): the title names the
  occasion around the turn, never the turn.
- **Several layers on reread** — Missed a Spot works three ways (the gate she
  swerved from / the spot he missed wiping / the untasted feminine pole).
- **Reaches the chapter's final image or closing line** (`37329bdf`; For You
  "lands on the closing line", `dc0972bc`).
- **Staircases or chains with neighbours** — Missed a Spot → A Clean Plate;
  My Pleasure / For You ("two courtesies masking one want", `dc0972bc`); the
  matched "Held" diptych, Safely Held / Held Loosely (`6e7573b1`). Note when a
  candidate would pair with a neighbour and when it would accidentally echo one.
- **No unwanted outside association** — Me Too dropped for #MeToo
  (`dc0972bc`). Search your own sense of idiom, song, brand, slogan, and
  headline for each candidate.
- **Laundered through courtesy/domestic language** — the volume's
  politeness-as-apparatus (My Pleasure resonating with the series' politeness
  frame, `dc0972bc`; Boyfriend as "the sayable word amid the unsayable ones",
  `5d386310`).
- **Bare form** — no "Character —" prefix or subtitle (`9f34f4dd`,
  `6e7573b1`).
- **On-disk slug drops a leading article** (CLAUDE.md naming convention) —
  note the slug each candidate would get.

## Step 4 — present

Per `meta-orientation.md:84`: **lead with oblique/ironic frames.** Give 8–12
candidates, ranked, then a recommendation of one or two. For each:

- **Title** → slug
- **Surface** (what a stranger reads) / **Charge** (what it means after the
  chapter, and on reread)
- **Goals hit**; **precedent criteria** it meets or spends
- **Source** — `scenes/<slug>.md:<line>` if it comes from the page
- **Risks** — telegraph-adjacency, screen borderline, neighbour echo, outside
  association

Then two short lists: **Ruled out at the floor** (title + which test, one line
each — so the author sees what was considered) and, if relevant, **neighbour
pairings** the shortlist opens up.

Misses beyond the floor are tradeoffs, not grounds to drop a candidate — say
what it spends and let the author weigh. Don't re-litigate retained titles.
No popups; options in prose.

## Step 5 — only on "rename X to Y"

A choice in conversation is not a rename instruction. When the author says
"rename/change the display title from X to Y", ask once whether the **slug**
changes too (it need not; `e9fae6f3` changed both, Grace in `9f34f4dd` kept
its slug).
Then, as one commit:

1. `meta/meta-plan-chronology.md` entry heading (add `(was "X")` only if the
   author wants the history in the entry), and the `# ` heading in
   `scenes/<slug>.md`.
2. Every `{{X}}` → `{{Y}}` across `meta/`; check `tools/lint_titles.py`
   `ALIASES` for entries pointing at X. Leave bare same-word prose uses alone.
3. If the slug changes: `git mv` the scene, its companion docs
   (`meta-note/condensed/triage-<slug>.md`), and `reviews/**/<slug>.md`; update
   slug pointers in `meta/` (incl. `meta/meta-volumes.toml` and any
   `reviews/cold-read/volume-packets.toml` `opening_slug`), `audits/`, and tool configs —
   `rg -n '<old-slug>'` over the repo, excluding nothing tracked.
4. `meta/meta-blurb.md` if the title appears there.
5. Checks: `tools/lint_titles.py --all`, `tools/lint_titles.py --bare`,
   `tools/orphan_refs.py --slugs <slug> …`, `tools/chapter_dates.py --check`,
   `tools/chronology_html.py`, `tools/build_epub.py` TOC sanity if the volume
   builds. `rg -n -F 'X'` once more for stragglers and show them to the author.
6. Commit message per precedent: old → new, the surface and the reread charge,
   and the reason for the change (e.g. the retail screen).
