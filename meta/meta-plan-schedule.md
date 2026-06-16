# Schedule Management — Plan

*How in-world time is recorded across the project. Governs the calendar-anchor block, per-scene texture lines, and what may be pinned to a hard date.*
*Companion to `meta-process-chronology.md` (which governs when/how the chronology is updated). This file governs the **time model itself**.*
*Status: **Pass A (identity/names) applied; Pass B (texture + summer calendar) pending the summer-expansion decisions — see §6.***

---

## The Problem This Solves

Three different jobs were being carried by one field (the scene number, and later the date), which is why reordering kept triggering project-wide renumbering and cross-reference drift (the 14/15, 26/28, 40/41 splits between docs are the symptom).

The jobs are distinct and have **opposite stability profiles**:

| Job | Question it answers | Stability |
|-----|--------------------|-----------|
| **Identity** | *Which scene is this?* | Permanent — never changes |
| **Sequence** | *Where in the order does it fall?* | Changes on every reorder |
| **In-world stamp** | *What does it feel like — season, weather, campus moment?* | Stable against reorder; rides season + academic phase, not the calendar date |

**The governing rule:** *no handle may encode position.* Identity must carry no sequence information and no date information. References point at identity (the name), never at a position. Then reordering and re-calendaring change only *attributes* of a scene — never a reference — so the blast radius of a move shrinks from "every downstream reference in the project" to "the one scene that moved."

---

## The Three Layers

### Layer 1 — Identity: the name

The **distinctive scene name is the permanent handle.** "The Fitting," "The Froyo Walk," "Randi's Walk of Shame." All cross-references in all `meta-*` docs point at the name. A name never breaks on insertion, reorder, renumber, or calendar revision.

- **Cross-references use names, not numbers:** "see The Fitting," not "see scene 15."
- **Optional stable ID (birth-order):** if a numeric handle is ever wanted (tooling, "X of ~41" tracking), assign a *never-reassigned birth-order* ID — the scene's permanent serial, unrelated to position. The Froyo Walk is born `#008` and dies `#008` regardless of where it sits or what month it lands in. New scenes take the next free integer. **This is optional; names already serve as handles.** Adopt only if numeric sorting in a tool becomes useful.
- **"X of ~41 complete"** is a *count*, not a max-number. It lives as prose in `meta-brief.md`, computed from how many are drafted — never inferred from the highest scene number.

### Layer 2 — Sequence: phase-grouped, list-ordered

Narrative order is carried by **phase grouping + position in the list**, not by a number.

- Scenes are grouped under broad phases (the existing Phase 0–5 structure, plus a summer phase — see §6).
- **Within a phase, order = the order entries are listed in the chronology doc.** The document's top-to-bottom line order *is* the sequence. Reordering = cut and paste an entry up or down within its phase. Nothing to recompute.
- Sub-clusters (the former 15a–15e lettered grammar) **retire into plain adjacency** — scenes that belong together simply sit next to each other in the list. No special numbering grammar needed.
- For same-moment ordering (diptych panels, brunch movements), a short within-entry note carries it: *"same afternoon," "second movement."*

This makes inserts free: a new scene gets a name and drops into its phase at the right line. No cascade.

### Layer 3 — In-world stamp: the texture line

Each entry carries one **texture line** that records season + academic moment + weather, written against the *stable* layer so it survives reordering and the summer expansion untouched. **This is what the prose's atmosphere is written against** — it states the texture directly so you don't re-infer "what does mid-September feel like" each draft.

**Format:**
> *Season · Term-phase · Weather · Day (hard/soft) · Fixed-point proximity (if any) · (≈ derived date)*

**Field rules:**
- **Season** — weather-and-mood anchor: *early fall, deep fall, first cold snap, the grey before break, mud-season, high summer.* Moves only if you deliberately change the scene's season.
- **Term-phase** — campus-pressure layer: *week 1, settling-in, pre-midterm, midterms, reading period, finals, break, dead-campus.* What the ambient student body is doing around the characters.
- **Weather** — derived from season; stated plainly. *Warm, leaves green; raw, leaves down; bright and crisp.*
- **Day** — day-of-week **only where the prose uses it**, tagged **(hard)** if load-bearing, **(soft)** if flavor. Most scenes omit it or mark it soft. Day-of-week is the *most fragile* stamp (shifts with every calendar revision) and the *least often* load-bearing — so spend it only where earned.
- **Fixed-point proximity** — only if the scene leans on a calendar edge: *Thanksgiving in 4 days; mid-winter-break; commencement week.*
- **Derived date** — available but demoted. Write as a clearly-computed parenthetical estimate: *(≈ wk of Sep 18).* Never a hard pin unless the Day or a fixed point is tagged **(hard)**.

---

## The Calendar-Anchor Block

**The single source of truth — the only place absolute dates live.** All scene placement is relative to these anchors. Revise here once; do not re-stamp individual scenes. When the calendar changes (e.g. the summer goes in), every scene's *derived* date recomputes for free, and every scene's *texture* — written against season + term-phase — needs no change.

This block lives at the top of `meta-plan-chronology.md`, replacing the current single-line anchor.

> **Calendar anchors** — *the only place hard dates live. All scene placement is relative to these. Revise here once; do not re-stamp individual scenes.*
>
> **Fall semester** — classes begin ~Mon Aug 28. Week 1 = Aug 28. Midterms ~mid-Oct (weeks 7–8). Thanksgiving break ~Wed Nov 22–Sun Nov 26. Reading period / finals early Dec. Last final ~Fri Dec 15.
> **Winter break** — ~Fri Dec 15 – Sun Jan 14. (Town empties; campus dead. Load-bearing for the flat date — the emptiness is the content, not the date.)
> **Spring semester** — classes begin ~Mon Jan 15. Spring break ~early-mid March. Midterms ~late Feb. Reading period / finals late Apr–early May. Commencement ~Sat May 11.
> **Summer** — *(TO BE SPECIFIED — see §6).* Candidate shape: Summer Session I ~mid-May–late June; Session II ~early July–mid-Aug; the long unstructured stretch is the texture, not the course schedule. Town half-empty, hot, slow; the academic-pressure layer goes silent.
>
> **Seasonal weather (Blacksburg / Virginia Tech, SW Virginia, ~2,000 ft elevation — cooler and later-turning than lowland Virginia):**
> - *Late Aug–Sep:* warm days, cool nights, leaves green. Move-in heat.
> - *Oct:* the turn — leaves color mid-to-late Oct, first frost ~late Oct, crisp and bright.
> - *Nov:* leaves down, grey, first hard cold; raw by Thanksgiving.
> - *Dec:* cold, often overcast; snow possible, not reliable.
> - *Jan–Feb:* coldest; snow/ice events; the long grey.
> - *Mar:* mud season, unpredictable — warm tease then cold snap.
> - *Apr–early May:* green returns, dogwoods, warm by commencement.
> - *Summer:* hot, humid, afternoon thunderstorms; green and heavy.

**Year specificity:** if the prose ever names a year or a dated real campus event, pin the anchors to an actual VT academic calendar for that year (look it up). If the year stays unspecified, the `~` estimates stand. Blacksburg's elevation is the detail most likely to be gotten wrong by defaulting to generic "Virginia" — keep the turn late and the cold real.

---

## What May Be Pinned to a Hard Date

A date earns a hard pin **only when the prose depends on the specific day**, not merely on the season or term-phase. Default is relative; hard pins are the rare exception and must state their reason.

**Worked examples (the three cases):**

**Hard-date case — Randi's Walk of Shame:**
> *Season: early fall, warm. Term: week 1, settling-in. Day: **Saturday morning (hard)** — the day-after, empty house; the gauntlet only happens because it's a weekend. (≈ Sep 2.)*

Day-of-week is load-bearing (the hungover day-after, the empty house). Pinned hard. Everything else relative.

**All-soft case — The Froyo Walk:**
> *Season: early fall, warm, leaves green, cool evening ("gone blue and cool"). Term: week 3, pre-midterm, settling-in. Day: a weekday (soft) — "a Tuesday" in draft, flavor only. (≈ wk of Sep 18.)*

Nothing pinned. Reorder it, add a summer, shift the calendar — the *warm-day / cool-evening / early-fall / nothing-due-yet* texture is untouched, because that is what the prose was written against.

**Fixed-window case — the flat date:**
> *Season: deep winter, cold/grey, possible snow. Term: **winter break (hard window)** — dead campus, town emptied; the emptiness is the content. Day: soft. Relative constraint: after SATC track at full intensity, before the threesome is scheduled.*

The *break window* is pinned (the empty town is the engine); the specific date inside it is free. The relative placement constraint travels *with* the texture line, so the logic lives next to the scene rather than buried in a flags list.

---

## §6 — The Two Migration Passes

The original plan bundled everything into one after-summer pass. That was a mistake: **identity (the name) has no dependency on the summer decisions** — a name encodes neither position nor date, so summer shape cannot affect it. And the name migration is exactly what makes expansion cheap (a name never breaks on insertion). So it is **decoupled** and run first; only the texture/calendar work waits for summer.

### Pass A — Identity (no blocker; applied)

Summer-independent. Within Pass A, do the conversion completely in one sitting so two grammars are never live at once — but it does not wait on summer.

- **Birth-order IDs: declined.** The name is the sole handle; no numeric IDs adopted. Revisit only if tooling ever needs numeric sorting (they would be assigned never-reassigned, so adopting them later is itself expansion-safe).
- [x] **Retired numbers from cross-references** across all `meta-*` docs — each converted to the scene **name**. Ends the renumbering tax and closes the 14/15, 26/28, 40/41 drift permanently (names can't drift).
- [x] **Retired the lettered sub-clusters** (15a–15e, 8a/8b, 12a, etc.) into plain adjacency within their phase.
- [x] **Reconciled the divergent scene numbers** as part of the name-conversion; verified no stray numeric scene-ref survives.
- [x] **Updated `meta-process-chronology.md`:** removed the "sequential number" required field — identity is the name, order is list position.
- [x] Update `DOCUMENTS.md`: note the chronology now references scenes by name.

### Pass B — Texture + calendar (after-summer)

**Decisions required first (blockers — these genuinely depend on summer):**

1. **Summer shape.** Does the configuration run hot through summer, attenuate, or break? This determines whether summer is a phase full of scenes or a thin connective stretch — and therefore the summer anchor's content.
2. **Who is on campus in summer.** Vee, Pace, Randi — who stays, who leaves, who takes a session? The academic-pressure layer goes silent in summer; what replaces it as ambient texture (jobs, near-empty town, heat) depends on this.
3. **Year specificity** (see anchor block). Pin to a real VT calendar or keep `~` estimates.

**Migration steps (one pass, once the above are decided):**

- [ ] Replace the single-line calendar anchor in `meta-plan-chronology.md` with the full anchor block above, **with the summer section filled in.**
- [ ] Add a summer **phase** to the chronology (insert/renumber phases as the summer's position requires).
- [ ] Convert every entry to carry a **texture line** (Layer 3 format).
- [ ] Demote any remaining hard dates that aren't load-bearing to relative `(≈ …)` estimates; keep only the **(hard)**-tagged pins, each with a stated reason. *(Partly done: the condensed/note briefs already carry only relative anchors and the chronology owns all dates.)*
- [ ] Move relative placement constraints (currently in the continuity-flags section, e.g. the flat-date placement flag) onto the relevant scenes' texture lines, so placement logic sits with the scene.
- [ ] Update `meta-process-chronology.md`: add **texture line** as a required field in "What Every Entry Must Contain," and the rule that **absolute dates live only in the anchor block** (entries carry derived estimates, never hard pins except where tagged **(hard)** with a reason).
- [x] Update `DOCUMENTS.md`: add this file to the Tier 5b (Process) table. *(already present)*

**Standing rule after migration:**
- New scenes: assign a **name**, drop into the correct **phase** at the correct line, write a **texture line**. No renumbering. No date pin unless **(hard)** with a reason.

---

## What This Costs (eyes open)

- **Reordering is never free** — *something* must record that a scene moved. This system shrinks the cost to updating one scene's position; it does not eliminate the move itself.
- **"How far along at a glance"** is lost from the numbering and must come from a count in the brief instead.
- **Verbal shorthand** is slightly longer ("the Froyo Walk" vs "scene 8") — but names were already the working register in conversation.
- **One central maintenance point** — the anchor block — must be kept as the single source of truth. The payoff: revise the calendar once, never re-stamp scenes.

The recurring renumbering tax is **not** the irreducible price of refactoring. It was avoidable, and this ends it. The irreducible price is small: when a scene moves, update where it sits — once.
