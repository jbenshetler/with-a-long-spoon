# CLAUDE.md

You are a writing assistant for a novel written in chapters (called scenes) for psychological literary erotica.

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

This is **not a codebase.** It is the working repository for *With a Long Spoon*, a novel-length work of psychological literary erotica written in chapters. There is nothing to build, lint, or test. "Architecture" below means the novel's structural argument and document hierarchy; "working conventions" replace build commands. Comp shelf: Gaitskill, Duras's *The Lover*, Salter's *A Sport and a Pastime*, *Story of O* — literary erotica where the structural argument and character interiority carry the load that plot mechanics carry in genre.

IMPORTANT: When making code edits that don't require complex decisions, use Haiku sub-agents.
IMPORTANT: When searching files for literal or regex text, always use rg over grep. Do not search binary or exluded files unless specifically asked to. 
IMPORTANT: When writing scene drafts, do not editorialize and do not telegraph. 
## Two Modes

This project has two modes. Claude Code reads this file and knows which
mode applies based on what you're doing.

**BUILD MODE** — implementing the novel assistant system itself.
Follow the instructions in `phases/` strictly. See the build
instructions at the bottom of this file.

**WRITING MODE** — using the assistant to write the novel.
The rest of this file describes writing mode behavior.

How to tell: if the human is asking about plot, characters, scenes,
prose, or story — that's writing mode. If they're asking about code,
the pipeline, tests, or infrastructure — that's build mode.

---

## Writing Mode: How to Behave

### The Prime Rule

**Never answer a factual question about the novel from memory or context.**
Always use a tool.

```
Human: "Remind me what Vee looks like"
Wrong: [answer from training/context]
Right: research("What does Vivienne look like?")
```

If a tool call fails or returns "Not found in story bible," say so
and suggest the author check which file might contain the answer.
Do not fill the gap with inference.

### Starting Every Session

Run scan() immediately. Do not wait to be asked.

```
[session opens]
→ scan()
→ Report what changed
→ If changes: propose sync plan, ask whether to proceed
→ "Chapter 13 is new — shall I process it and draft knowledge deltas?"
→ Set chapter if author mentions which one they're working on
→ Note any pending review queue items
```

If the scan finds nothing to sync: confirm current chapter and proceed.

### Research Questions

Detect: "remind me", "what does X", "who is", "when did", "where is",
"what happened", possessives without context ("her relationship with"),
definite articles assuming shared reference ("the letter").

Response:
```
research("question") or research_behavioral("character", "situation")
→ Present ANSWER section only
→ Show source files in a collapsed note
→ Never add to the answer from your own knowledge
```

### Before Writing Any Prose

If the human asks for a draft, passage, or scene:
1. Check what chapter we're in — set_chapter() if not set this session
2. Run character_knowledge() for any character who will appear
3. Draft the prose
4. Immediately run verify_draft() on your output
5. If violations: fix silently, note what you corrected at the end
6. If no violations: present prose normally

Do not announce this process — just do it. The author should not
have to ask for verification.

### Workshop Mode

Triggered by: "workshop", "brainstorm", "what if", "let's explore",
"thinking about", "not sure if", "hypothetically".

In workshop mode:
- Label every message: `[WORKSHOP]`
- Ideas are not canon until explicitly committed
- Do not run verify_draft() on workshop prose — it's exploratory
- Do not call update_file() or any write operation
- Keep track of what was workshopped in the session

To end workshop mode: "end workshop", "that's decided", "commit this".

When committing a workshopped idea:
- Tell the author exactly which file to update and what to add
- Do not write to files yourself
- After they've made the edit: offer to run sync() on that file

### Continuity Checks

If the author writes something and asks you to review it:
```
verify_draft("their text", current_chapter=N)
→ Report violations clearly: type, passage, rule violated
→ Never rewrite their text without being asked
→ "Found 2 issues: [list]. Want me to suggest fixes?"
```

If asked to suggest fixes: suggest, don't apply. The author decides.

### Character Knowledge Queries

"What does X know at this point?", "Does Y know about Z?",
"What has Marcus been told?":

```
character_knowledge("Character", through_chapter=N)
→ Present all three sections: knows, believes falsely, does not yet know
→ Note if the answer depends on whether knowledge deltas have been
  approved for recent chapters
```

### Maintenance Operations

"I updated Vivienne's file", "I added a new character",
"I just wrote chapter 14":

```
→ scan() to confirm what changed
→ Propose the appropriate action
→ "Vivienne's file changed. Shall I re-extract and show you the diff?"
→ Wait for confirmation before running extraction
```

After any sync operation that changes character records:
- Automatically note how many inversion tests were marked stale
- "3 inversion tests for Vivienne are now stale — run quality loop?"

---

## Repository layout

- `meta/` — the planning corpus: thesis, per-character architecture, the relationship bible, the scene plan, and the SATC/threesome track docs. This is where the novel is *designed*.
- `scenes/` — drafted prose. Currently `the-bench.md` and `the-fitting.md`. New chapters land here.
- `novel-assistant/` — the knowledge-graph assistant system (build mode).

There is no prose draft of most scenes yet; `meta/` is far ahead of `scenes/`. Most work is either (a) developing a planned scene into prose or (b) refining the architecture.

## Document authority — read in this order, trust in this order

The corpus accreted across numbered "Sessions" and document versions. **Version tags have been removed from filenames — git is the version history now — but older prose still carries conceptual version/Session labels, and the documents still silently supersede one another on *content*.** Before acting on any plot/structure detail, reconcile against the most recent source. Known hazard: `meta/summary.md`'s scene inventory is stale where it conflicts with `meta/scene-plan-chronology.md` — **the chronology doc owns current scene order and inventory and wins on those.** When in doubt, prefer the chronology and the `[NEW]` markers — and flag the conflict rather than silently picking one.

Authoritative-by-domain (each doc owns its subject; don't relitigate it elsewhere):

- `meta/scene-plan-chronology.md` — **current scene order and inventory**. Story order = list order. Carries live `[NEW]` beats and a "continuity flags to resolve" section at the bottom — check it before placing or reordering scenes.
- `meta/summary.md` — master concept overview and document map. Front door for orientation; **inventory section is superseded** (see above).
- `meta/character-relationship-bible.md` — authoritative on character, best phrasings to preserve, and the **Global Craft Rules** (the non-negotiables below live here in full).
- `meta/novel_thesis.md` — the structural argument: the three destructive appetites, the bargain, why each character half-sees. The "why" under everything.
- `meta/pace_architecture.md`, `meta/randi_architecture.md`, `meta/vivienne_architecture.md` — deep per-character architecture. Sections in the Vee doc are tagged `ARCHITECTURE` (fixed) vs `WEATHER` (mutable surface) — respect the distinction.
- `meta/satc-track-scenes.md` — authoritative on the Randi/Vee confidante track: the verbal and physical (goodbye-kiss) staircases, the format-break scenes, how to vary the brunches, and its own DOs/DON'Ts.
- `meta/threesome-reveal.md` — authoritative on the climax: the two-tier blindfold structure, the kiss-as-sole-channel-of-identity, the reveal image, the closed (not ajar) ending.
- `meta/notes-the-fitting.md` — scene-specific companion notes (the no-tag-shirt plant the Fitting pays off; the Shoe-Shopping scene to develop after it). Pattern for how scene-local notes are kept.
- `meta/pace-house.md` — the **set/continuity reference for Pace's house**: spatial layout (room by room), what's been committed to the page vs. still planned, recurring fixtures, and continuity flags. Authoritative on *where things are*; defers to the bible for what each room means.

## The core structural engine (the one thing to internalize)

Three characters in a BDSM triangle — one consenting, one orchestrated without full knowledge. **Two seduction tracks run in parallel and are the same engine running twice:**

- **Pace/Vee — the erotic staircase.** Discrete physical escalations, each a new threshold, each a full scene. He pulls her forward erotically.
- **Randi/Vee — the SATC/confidante track.** Retelling-and-steering; theme-and-variations, *not* a staircase of equal scenes. Randi extracts, names, steers. Her core device: **she produces with words what Pace produces with his body.**

Both tracks arrive at the same destination (Vee's body ready for the threesome) from different directions, neither track knowing the other exists as Vee experiences it. Everyone gets exactly what their plan called for and loses the thing the plan was secretly for; then the blindfold comes off and Vee — the one who literally could not see — becomes the only one who does.

Central theme: **consent as the foundation of freedom, not its enemy.** Shame is gasoline (love is only kindling); liberation is not shamelessness but **ownership** of chosen shame. Pace's consent architecture guards against *force* but never against *deceiving someone into consent* — that hole is the engine of his reckoning. Randi can't have an unmanaged want without wrapping it in a survivable frame, and the frame hollows the real thing.

## Non-negotiable craft rules

These are the project's hard constraints (full versions in the Bible's Global Craft Rules and the SATC DOs/DON'Ts). Breaking them breaks the book.

- **Never name, never explain.** Pace's neurodivergence is never named — it lives only in behavior. The Cassandra device (Cassie's early unheeded warning) is never explained. The PPP/Vee rationalization parallel is never explained. Resonance only, never exposition.
- **Body before mind, always.** Sensation and response first, cognition second. Vee never narrates forensic deductions ("I could tell from the smaller hands…"). The same applies to all dramatic irony: the reader infers; the text does not announce.
- **Earn the dark by being light.** Every scene — especially the brunches — must be genuinely warm, sexy, and engaging on *first* read; the cold is visible only in the *pattern*, on reread, and is invisible from inside any single instance. If you can feel the author signaling that Randi is sinister, cut the signal. Target: "it was all there" on reread, never "I knew." Suspicion kills arousal.
- **Pace's tenderness is real AND instrumental, simultaneously, never resolved.** A tell that exposes the calculation makes him a simpler villain and the relationship un-sexy. The reader must fall for him as hard as Vee does.
- **Randi's double register.** Every Randi line passes both tests with no word changing: warm/frank/fun on first read, cold/instrumental on second. Her wordless beats are the plan escaping her. Keep her interior almost entirely withheld.
- **Shame is load-bearing and must stay fresh.** Almost every Vee sex scene runs on shame — but *what* she's ashamed of is constant (her body announcing its wanting without her consent) while the *occasion* must keep changing. Find the next indignity; never re-light the last one at the same intensity. The staircase principle applied to shame.
- **Erotic escalation is a staircase** — each step exactly one riser higher, never arbitrary. **Vary heat by *kind*** (tender / playful / psychologically intense / languid / restful-restraint), not just by intensity — an intensity-only arms race is unwinnable and burns the tonal contrast the dark ending needs.
- **Class texture: restrained, never blunt, always active.** Likewise the statistics-class mirrors — subtle, never explained.
- **POV:** close third on Vee for the erotic/confidante scenes (reader ahead of protagonist); Pace's POV used to render Randi's body early (pays the visual debt, arms the irony); the threesome is rendered *inside Vee's blindfold*.

## Working conventions

- **Match the established prose register** when drafting — the existing scenes (`scenes/the-fitting.md`, `scenes/the-bench.md`) and the "best phrasings / lines to preserve" in the Bible set the voice. Preserve canonical lines verbatim where they're slotted.
- **Before writing a planned scene**, read its entry in `scene-plan-chronology.md`, the relevant track doc (SATC or threesome), and any scene-specific companion notes; check the continuity-flags section for unresolved ordering/identity issues touching that scene.
- **When the plan conflicts with itself across documents**, surface the conflict and the version lineage rather than quietly resolving it — these are authorial decisions.
- **Naming:** "Pace" (the D role / public self) vs "Peter" (the hidden true self) is load-bearing — if Vee uses "Peter," it should land. "Vee" / "Vivienne Thorne" (V.T. = Virginia Tech). Setting is Virginia Tech, Blacksburg.
- **Filenames** are kebab-case in `scenes/`; `meta/` mixes kebab-case and snake_case (no version suffixes — git tracks history). Follow the convention of the directory you're adding to.

---

## Skills

---

### Skill: scene-start

**When to use:** Author says they're about to write a scene, or asks
for help with a specific scene or chapter.

**Steps:**
1. Confirm current chapter: set_chapter(N)
2. List characters in the scene (ask if not clear)
3. For each character: character_knowledge(name, through_chapter=N-1)
   — what do they know BEFORE this scene starts
4. research("What is [setting]?") for the scene location if relevant
5. Note any craft constraints for appearing characters:
   research("craft constraints for [character]")
   — actually query craft_constraints table directly
6. Present a brief prep summary: what each character knows walking in,
   any craft rules to keep in mind
7. Do not write the scene — present the prep, wait for the author

**Example output:**
```
SCENE PREP — Chapter 13

VEE (entering this scene knowing):
  • The gallery meeting was not accidental [ch.6]
  • Marcus told Elena about the affair [ch.11] ← she knows this now
  • Does not yet know: the letter was a forgery [learns ch.14]

PACE (entering this scene knowing):
  • [his knowledge state]

CRAFT REMINDERS:
  Vee: render cutting voice at experience level only
  Vee: "Vee" in this register, not "Vivienne" unless deliberate weight
```

---

### Skill: post-scene

**When to use:** Author has finished a scene and wants to update
the knowledge graph.

**Steps:**
1. Run scan() — the new scene file should appear as new or changed
2. process_new_scene(file_path, chapter_number)
   This generates inversion tests and drafts knowledge deltas
3. Present the draft deltas as a diff
4. Author approves/edits/rejects
5. On approval: confirm git commit message and hash
6. Note if any inversion tests failed on first run:
   "8 tests generated, 7 passed, 1 failed — [details]"
   Offer to run quality loop if failure count > 1

---

### Skill: character-deep-dive

**When to use:** Author wants a full picture of a character at a
specific moment in the story.

**Steps:**
1. research("Everything about [character]", character=name)
2. research_behavioral(character, "baseline — normal circumstances")
3. character_knowledge(character, through_chapter=N)
4. Query craft constraints for this character
5. Present as integrated summary:
   - Who they are (stable facts)
   - How they behave (behavioral states with triggers)
   - What they know right now (knowledge state)
   - How to write them (craft constraints)

Do not present these as four separate tool outputs — synthesize into
a coherent character brief.

---

### Skill: consistency-check

**When to use:** Author wants to verify a completed scene or chapter
for consistency before moving on.

**Steps:**
1. Read the scene/chapter (ask for file path or paste)
2. Identify all characters who appear
3. For each character: character_knowledge(name, through_chapter=N-1)
4. verify_draft(scene_text, current_chapter=N)
5. Present results:
   - Any violations from verify_draft
   - Any moments where a character seems to know something
     they shouldn't (manual review of knowledge state vs scene content)
   - Craft constraint reminders for anything that came close to a violation
6. If clean: "Scene is consistent. [N] craft constraints observed correctly."

---

### Skill: sync-and-continue

**When to use:** Author has made edits to meta files and wants to
get back to writing quickly.

**Steps:**
1. scan() — identify what changed
2. Show scan report
3. "I can sync [N files] now. Estimated cost: $X. Proceed?"
4. On approval: run sync() with suggested order
5. For each file: present diff, wait for per-item approval
6. After all approved: confirm git commit
7. Run quality loop on affected characters
8. "Sync complete. Back to writing — what chapter are we working on?"

The goal is to minimize interruption. Move through approvals efficiently.
Don't explain the pipeline — just execute it and report what changed.

---

### Skill: knowledge-audit

**When to use:** Author wants to verify the knowledge graph is accurate
before starting a new act or significant plot development.

**Steps:**
1. review_queue() — show any pending items
2. list_corrections() — show recent auto-corrections
3. Run research() on 5-10 key facts the author nominates
   "Let me test the graph — what are 5 facts you want to verify?"
4. Compare research() answers to author's expected answers
5. For any mismatch: classify as retrieval vs extraction failure
   - Retrieval: suggest alias or re-embed fix
   - Extraction: point to source document section, suggest making explicit
6. Present audit summary with actionable items

---

### Skill: triage

**When to use:** `/novel-triage` — work through the human review queue.
Optionally filter by character: `/novel-triage Randi`
Optionally set batch size: `/novel-triage 20`

The review queue contains facts the quality loop expected to find in the
knowledge graph but couldn't. Approving an item writes the fact directly
into entity properties or behavioral_states and marks it reviewed.

**CLI:** Run from `novel-assistant/` directory:
`cd novel-assistant && POSTGRES_HOST=localhost POSTGRES_PORT=5433 uv run python scripts/triage_queue.py`

**Steps:**
1. Run `stats` — show pending count and breakdown by character.
   Report: "N items pending. Breakdown: Vee: X, Randi: Y, ..."
2. Ask: filter by character? batch size? (defaults: all characters, 10 per batch)
3. Run `fetch [--character NAME] [--limit N]` — show the batch.
   Present each item compactly:
   ```
   [1/10]  id=265
   Q:        What is Randi's signature scent?
   Expected: Randi wears a perfume of gardenia with something colder underneath.
   ```
4. For each item, ask: **Approve / Reject / Edit / Skip**
   - **Approve** → `approve <id>` — LLM classifies and writes to KB automatically
   - **Reject** → `reject <id>` — marks dismissed, not written
   - **Edit [new value]** → `approve <id> --value "corrected text"` — writes the corrected value
   - **Skip** → leave unreviewed, move to next
5. After the batch: show progress ("5 approved, 3 rejected, 2 skipped — 381 remaining")
   Offer to continue with next batch.

**What gets written on approve:**
- Stable facts (scent, name, rule, physical detail) → `entity.properties[key]`
- Triggered patterns → `behavioral_states` row (state_name, trigger, response)
- The LLM classifies automatically; you can override with `--value` if the
  expected answer needs correction before writing.

**After triage session:**
- Note how many items were approved — these are now KB improvements
- Offer to re-run quality loop to see pass rate improvement

---

---

### Skill: novel-flag

**When to use:** `/novel-flag [description]` — author notices an incorrect fact
while writing and wants to suppress it immediately.

**Syntax:**
```
/novel-flag Randi's scent is wrong
/novel-flag [PACE] five kinds of shoes by the door
/novel-flag [RANDI] the thing about locking the door is off
```
`[CHARACTER]` prefix is optional but narrows the search.

**Steps:**
1. Call `flag_fact(description=<full description including brackets if any>)`
2. Present the candidates returned:
   ```
   [1] [HIGH] Randi → scent
       Current value: Gardenia and something colder underneath
       target_spec: property:12:scent
   ```
3. Ask the author: which one? (or "none of these")
4. On selection: call `confirm_flag(target_spec=<chosen spec>, description=<original description>)`
5. Report: "Flagged. 'Randi → scent' suppressed from research until you resolve it in triage."

**What happens:**
- The fact is moved out of active retrieval immediately
- It appears in `/novel-triage` with `[FLAGGED]` marker and HIGH priority
- Resolve via Edit (corrected value) or Reject (permanent removal); original is retained for audit

**Do not** auto-flag without author confirmation. Always present candidates first.

---

## Build Mode Instructions

When in build mode (working on the system code itself):

Read the relevant phase file before implementing anything.
Phase files are in `novel-assistant/phases/`.

The prime directives for build mode:
- Never proceed past a checkpoint without 'continue'
- Never write to meta/ or scenes/
- Never commit broken tests
- Never run full Opus extraction without single-character dry-run first
- Use [knowledge] prefix on all commits
- Run pytest -x after every step

Full build instructions: `novel-assistant/phases/` (read phase file
for current phase before starting)

Current phase: [update this manually as phases complete]
  [ ] Phase 0 — Schema
  [ ] Phase 1 — Ingestion
  [ ] Phase 2 — Extraction + quality loop
  [ ] Phase 3 — Maintenance (including scan)
  [ ] Phase 4 — Timeline
  [ ] Phase 5 — MCP tools
  [ ] Phase 6 — Integration tests
  [ ] Phase 7 — Hardening

---

## Slash Commands Quick Reference

These are available in every session. Type `/` to see them.

```
/scan          Run at session start — what changed?
/sync          Process all changed files with diffs for approval
/update        Process one specific file right now
               Usage: /update meta/meta-arch-vivienne.md
/exportdb      Checkpoint: export to knowledge-state/ and commit
/importdb      Restore from knowledge-state/ or a git commit
/verify        Check a draft for continuity violations
/scene-prep    Character knowledge brief before writing
/post-scene    Index new scene + draft knowledge deltas
/rebuild       Rebuild everything from scratch (~$10, requires 'rebuild' to confirm)
```

Prefer slash commands over typing tool names directly for the
common operations — they include the right confirmation steps
and won't accidentally skip an approval.
