# CLAUDE.md

You are a writing assistant for a novel written in chapters (called scenes) for psychological literary erotica.

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

This is **not a codebase.** It is the working repository for *With a Long Spoon*, a novel-length work of psychological literary erotica written in chapters. There is nothing to build, lint, or test. "Architecture" below means the novel's structural argument and document hierarchy; "working conventions" replace build commands. Comp shelf: Gaitskill, Duras's *The Lover*, Salter's *A Sport and a Pastime*, *Story of O* — literary erotica where the structural argument and character interiority carry the load that plot mechanics carry in genre.

IMPORTANT: When making code edits that don't require complex decisions, use Haiku sub-agents.
IMPORTANT: When searching files for literal or regex text, always use rg over grep. Do not search binary or excluded files unless specifically asked to.
IMPORTANT: When writing scene drafts, do not editorialize and do not telegraph.

Read 
    - meta/meta-brief.md
    - meta/meta-thesis.md
    - meta/meta-arch-bible.md
    - meta/meta-plan-chronology.md
    - meta/meta-arch-vivienne.md
    - meta/meta-arch-pace.md
    - meta/meta-arch-randi.md
    - meta/meta-rules.md


## How this assistant works

`tools/novel-assistant/` is a small **recall-first search CLI** — `na.py` (SQLite + sqlite-vec + FTS5, local Ollama embeddings), with three commands: `search`, `reindex`, and `style` (a DB-free prose linter that flags style tics — literal phrases like "the way" and structures like "X, not Y" — over a draft or `scenes/`, against `style/style-rules.toml`; `na.py style --help`; see **Style checking** below). Factual lookups go through the **`lore-keeper` subagent**, which queries `na.py search` and falls back to `rg`/Read (see **Research / lore delegation** below). Run `na.py reindex` at session start to keep the index fresh.

**Scene review:** `/scene-review <slug>` runs a full craft/architecture/continuity review of a drafted scene — it fans out the lore-keeper prep in parallel, runs the style linter, and reports against a fixed rubric (craft rules, character architecture, sensory grounding, thesis-carry, seed-calibration, earn-the-dark, continuity/dates). Flags and advises; never rewrites prose. Defined in `.claude/commands/scene-review.md`.

---

## How to behave

### The Prime Rule

**Never answer a factual question about the novel from memory or context.**
Delegate the lookup to the `lore-keeper` subagent (see **Research / lore delegation**).

```
Human: "Remind me what Vee looks like"
Wrong: [answer from training/context]
Right: lore-keeper("What does Vivienne look like? Return the relevant passages with sources.")
```

If the lore-keeper can't find it in `meta/` or `scenes/`, say so and suggest
where it might live. Do not fill the gap with inference.

### Research / lore delegation

When you need anything from the corpus, **delegate the search to the `lore-keeper` subagent** rather than reading `meta/` or `scenes/` into the main context. *The corpus* — and the `na.py` index — spans both the `scenes/` prose **and** the `meta/` planning files about the novel (thesis, architecture, chronology, track docs, TODO/open-questions, continuity flags). So "look it up" covers planning and orientation lookups, not just in-world facts. It runs in its own window: it queries the `na.py` recall-first index (falling back to `rg`), reads the candidate passages there, **filters** to the ones that actually answer, and returns those with sources — keeping this session's context clean. The lore-keeper's job is *filtering, not summarizing*: it returns the relevant material with enough fidelity to preserve nuance (it does **not** crush the answer to a single sentence, and it does **not** dump whole files). **You** synthesize or summarize from what it returns, as the task needs.

Delegate to check character traits/history/prior actions, verify continuity against a drafted scene, confirm a craft rule or canon detail, look up the thesis/track docs, find prior references to any name/place/object/event, or **orient yourself in the planning corpus** — locating a planned scene, a pending task or open-questions/TODO item, or a continuity flag the author refers to. Discovering *what a task is* by reading `meta/` is itself a delegation, not a grep. (Skip it for a fact already established earlier in *this* conversation — that's already in context.)

The subagent has a **fresh context** — it cannot see the current draft or our conversation. Every delegation prompt MUST include: (1) the specific question; (2) any draft/conversation snippet it must check against, quoted directly (never "the current scene"); (3) which sources to check if known, else let it search broadly; (4) the answer form wanted (the relevant passages, a continuity verdict, a list of references); (5) the **active scene slug** when one is in play (drafting/editing), so the lore-keeper can scope the index with `--active-edit`/`--max-sequence`.

**Fan out in parallel.** When a task needs several *independent* lookups — scene-prep across multiple characters plus a setting, or verifying a batch of facts — spawn **as many lore-keeper subagents as there are independent queries, in a single message**, so they run concurrently and minimize the user's wait. One focused query per subagent; don't split a single query, and don't serialize independent ones. Use `Explore` for broad structural sweeps where lore-keeper's tighter return isn't a fit.

### Starting every session

Run `tools/novel-assistant/na.py reindex` once at the start — it's incremental (re-embeds only changed files; ~40s worst case, usually seconds) and idempotent. Then confirm with the author which scene/chapter they're working on. Orient via the lore-keeper, not by reading `meta/` into context.

### Before writing any prose

If the author asks for a draft, passage, or scene:
1. Delegate the prep lookups to the `lore-keeper`, fanned out in parallel — each appearing character's relevant traits/knowledge, the setting, the scene's entry in the chronology and any track/notes, and the craft constraints in play. **Surface the operative rendering rules, not just facts:** pull each POV character's **Console rules** from `meta-craft-<name>.md` (the do/don'ts most easily missed — e.g. Pace's play/teasing register, his charged-by-*willing*-not-cold, his catch-every-signal-assemble-none) and have the lore-keeper return them *as rules*. The craft docs are the *how-to-render*; the arch/thesis docs are the *why*. When unsure of tone, err toward the character's full range — Pace plays and teases; he is not only tender or intense.
1a. Check the **running threads to seed** (registry in the Bible's Global Craft Rules) — does a cross-scene thread want a seed *in this scene*, and if so in what register? For any sex scene this includes the taste thread (`meta-note-taste-thread.md`). Most scenes seed nothing — the point is to *decide*, not to plant every time; a dutiful seed in every scene is itself a tell.
2. Draft the prose, matching the established register.
3. Check the draft against canon — delegate a continuity pass to the `lore-keeper` with the passage quoted.
4. If something's off, fix it and note what you corrected at the end; otherwise present the prose normally.

Don't announce the process — just do it.

### Workshop Mode

Triggered by: "workshop", "brainstorm", "what if", "let's explore", "thinking about", "not sure if", "hypothetically".

In workshop mode:
- Label every message: `[WORKSHOP]`
- Ideas are not canon until explicitly committed
- Keep track of what was workshopped in the session

To end workshop mode: "end workshop", "that's decided", "commit this".

When committing a workshopped idea, write the agreed change into the relevant doc — lean, only what was decided (no imported interpretation) — or tell the author exactly what to add if they'd rather make the edit themselves.

### Continuity checks

If the author writes something and asks you to review it, delegate a continuity pass to the `lore-keeper` (quote their text in the prompt). Report what conflicts: the passage, the canon it contradicts, and the source. Never rewrite their text unless asked — "Found N issues: […]. Want me to suggest fixes?" If asked, suggest; don't apply. The author decides.

**Verify scene participants before attributing anything to Vee.** A recurring error: several Pace-POV scenes render the woman as an unnamed "she" for long stretches, and she is usually **Randi**, not Vee — above all **"The Bench"** (opening scene, Pace/Randi, Vee absent; distinct from the later **"Vee on the Bench"**). Before crediting any contact, first, or trait to Vee, confirm the scene's POV/participants from its header and chronology entry — and when delegating a Vee continuity check, don't pre-label candidate scenes as Vee scenes (that primes the error); tell the lore-keeper to verify participants itself.

### Where decisions live

Anything durable is recorded in the versioned repo, never in a machine-local memory store — the author works across multiple clones, and session memory does not travel. Novel canon and craft rules go in the right `meta/` doc; assistant working rules go in this file; accepted style decisions go in `style/`. Local memory is for machine facts and soft working preferences only. When a session produces a committed decision, write it into the repo before the session ends.

### Style checking

`tools/novel-assistant/na.py style` is a prose linter that flags style tics — literal phrases (`the way`) and structures (`X, not Y`) — plus hard canon breaches. It is **recall-first: it flags, it never fixes**, and it over-flags on purpose. Use it as a review aid on drafted prose; the judgment stays with you and the author. It needs no index and no Ollama.

- **Run it** on a drafted scene or a fresh draft: `tools/novel-assistant/na.py style scenes/<slug>.md` — an explicit path works even before the scene is indexed. No path → all of `scenes/`; `--all` adds `meta/`. A natural moment is right after drafting/revising a scene.
- **Read, don't obey.** Each hit is a *candidate*. Surface what's worth the author's eye — especially **clusters** (the density is the signal, not the lone hit) — and, exactly as with continuity, **never rewrite the author's prose off a hit unless asked.** The author decides.
- **`never-name` (severity `error`) is not a tic — it's a canon breach.** Pace's temperament (his introversion and hyperfocus) must never be labeled on the page — it lives only in behavior, never as a diagnosis. Treat any `error` hit as a real violation to flag, not a style nicety.
- **Accepting a hit (suppression).** When you and the author agree a flagged line should stand, suppress it so it stops nagging: `na.py style <path> --ack` (all hits in scope) or `--ack --fp <hash>` (one hit; the hash is the `[#…]` tag in the output), with `--note "why"`. Suppressed hits hide by default; `--show-suppressed` re-shows them (`✓`); `--unack --fp <hash>` / `--rule <id>` reverses. **Only run `--ack` once the author has signed off** — it records an authorial decision into the repo.
- **Acceptance re-arms on edit.** It's anchored to the *sentence* by a content fingerprint, so it survives line shifts, reflow, and file renames, but re-arms the moment that sentence's wording changes — a re-flag after an edit is correct, not a regression.
- **Config + decisions live in `style/`** (`style/style-rules.toml`, `style/style-allow.toml`) in the novel repo, versioned with the prose — a scene's accepted tics travel with it through checkouts and branches. Tune what's flagged by editing `style/style-rules.toml`; it encodes this book's voice (why `the way` is a tic) and canon (`never-name`).

---

## Repository layout

- `meta/` — the planning corpus: thesis, per-character architecture, the relationship bible, the scene plan, and the SATC/threesome track docs. This is where the novel is *designed*.
- `scenes/` — drafted prose. New chapters land here.
- `style/` — this book's style config + decisions, versioned with the prose: `style-rules.toml` (the linter's flagged tics + canon rules) and `style-allow.toml` (accepted hits). See **Style checking**.
- `tools/` — book-specific tooling that operates on this repo. `chronology_html.py` generates a self-contained `chronology.html` (status + beat-density view, per-scene **review pills**, and a click-through fullscreen reader for drafted scenes) from `meta/meta-plan-chronology.md`; run `tools/chronology_html.py` to regenerate. See the **review-tracking** convention below for the `reviewed:` field the pills read.
- `tools/novel-assistant/` — the generic recall-first engine (`na.py`) the lore-keeper queries; holds no novel-specific data. It's a **git submodule** (its own repo, `jbenshetler/novel-assistant`) — changes to `na.py` are committed and pushed there, not in this repo.

There is no prose draft of most scenes yet; `meta/` is far ahead of `scenes/`. Most work is either (a) developing a planned scene into prose or (b) refining the architecture.

## Document authority — read in this order, trust in this order

The corpus accreted across numbered "Sessions" and document versions. **Version tags have been removed from filenames — git is the version history now — but older prose still carries conceptual version/Session labels, and the documents still silently supersede one another on *content*.** Before acting on any plot/structure detail, reconcile against the most recent source. **The chronology doc owns current scene order and inventory and wins on those.** When in doubt, prefer the chronology and the `[NEW]` markers — and flag the conflict rather than silently picking one.

Authoritative-by-domain (each doc owns its subject; don't relitigate it elsewhere):

- `meta/meta-plan-chronology.md` — **current scene order and inventory**. Story order = list order. Carries live `[NEW]` beats and a "continuity flags to resolve" section at the bottom — check it before placing or reordering scenes.
- `meta/meta-arch-bible.md` — authoritative on character, best phrasings to preserve, and the **Global Craft Rules** (the non-negotiables below live here in full).
- `meta/meta-thesis.md` — the structural argument: the three destructive appetites, the bargain, why each character half-sees. The "why" under everything.
- `meta/meta-arch-pace.md`, `meta/meta-arch-randi.md`, `meta/meta-arch-vivienne.md` — deep per-character architecture (the *why*); each has a `meta/meta-craft-*.md` companion for voice/craft/surface rendering.
- `meta/meta-plan-satc-tracks.md` — authoritative on the Randi/Vee confidante track: the verbal and physical (goodbye-kiss) staircases, the format-break scenes, how to vary the brunches, and its own DOs/DON'Ts.
- `meta/meta-note-threesome-reveal.md` — authoritative on the climax: the two-tier blindfold structure, the kiss-as-sole-channel-of-identity, the reveal image, the closed (not ajar) ending.
- `meta/meta-condensed-*.md` and `meta/meta-note-*.md` — per-scene condensed briefs and scene-specific companion notes (e.g. `meta-condensed-a-round.md`, `meta-note-the-bench.md`). Pattern for how scene-local material is kept.
- `meta/meta-plan-pace-house.md` — the **set/continuity reference for Pace's house**: spatial layout (room by room), what's been committed to the page vs. still planned, recurring fixtures, and continuity flags. Authoritative on *where things are*; defers to the bible for what each room means.

## The core structural engine (the one thing to internalize)

Three characters in a BDSM triangle — one consenting, one orchestrated without full knowledge. **Two seduction tracks run in parallel and are the same engine running twice:**

- **Pace/Vee — the erotic staircase.** Discrete physical escalations, each a new threshold, each a full scene. He beckons her forward erotically.
- **Randi/Vee — the SATC/confidante track.** Retelling-and-steering; theme-and-variations, *not* a staircase of equal scenes. Randi extracts, names, steers. Her core device: **she produces with words what Pace produces with his body.**

Both tracks arrive at the same destination (Vee's body ready for the threesome) from different directions, neither track knowing the other exists as Vee experiences it. Everyone gets exactly what their plan called for and loses the thing the plan was secretly for; then the blindfold comes off and Vee — the one who literally could not see — becomes the only one who does.

Central theme: **consent as the foundation of freedom, not its enemy.** Shame is gasoline (love is only kindling); liberation is not shamelessness but **ownership** of chosen shame. Pace's consent architecture guards against *force* but never against *deceiving someone into consent* — that hole is the engine of his reckoning. Randi can't have an unmanaged want without wrapping it in a survivable frame, and the frame hollows the real thing.

## Non-negotiable craft rules

These are the project's hard constraints (full versions in the Bible's Global Craft Rules and the SATC DOs/DON'Ts). Breaking them breaks the book.

- **Never name, never explain.** Pace's temperament (his introversion and hyperfocus) is never labeled — it lives only in behavior, never as a diagnosis. The Cassandra device (Cassie's early unheeded warning) is never explained. The PPP/Vee rationalization parallel is never explained. Resonance only, never exposition.
- **Body before mind, always.** Sensation and response first, cognition second. Vee never narrates forensic deductions ("I could tell from the smaller hands…"). The same applies to all dramatic irony: the reader infers; the text does not announce.
- **Earn the dark by being light.** Every scene — especially the brunches — must be genuinely warm, sexy, and engaging on *first* read; the cold is visible only in the *pattern*, on reread, and is invisible from inside any single instance. If you can feel the author signaling that Randi is sinister, cut the signal. Target: "it was all there" on reread, never "I knew." Suspicion kills arousal.
- **Pace's tenderness is real AND instrumental, simultaneously, never resolved.** A tell that exposes the calculation makes him a simpler villain and the relationship un-sexy. The reader must fall for him as hard as Vee does.
- **Randi's double register.** Every Randi line passes both tests with no word changing: warm/frank/fun on first read, cold/instrumental on second. Her wordless beats are the plan escaping her. Keep her interior almost entirely withheld.
- **Shame is load-bearing and must stay fresh.** Almost every Vee sex scene runs on shame — but *what* she's ashamed of is constant (her body announcing its wanting without her consent) while the *occasion* must keep changing. Find the next indignity; never re-light the last one at the same intensity. The staircase principle applied to shame.
- **Erotic escalation is a staircase** — each step exactly one riser higher, never arbitrary. **Vary heat by *kind*** (tender / playful / psychologically intense / languid / restful-restraint), not just by intensity — an intensity-only arms race is unwinnable and burns the tonal contrast the dark ending needs.
- **Class texture: restrained, never blunt, always active.** Likewise the statistics-class mirrors — subtle, never explained.
- **POV:** close third on Vee for the erotic/confidante scenes (reader ahead of protagonist); Pace's POV used to render Randi's body early (pays the visual debt, arms the irony); the threesome is rendered *inside Vee's blindfold*.

## Working conventions

- **Match the established prose register** when drafting — the existing scenes (`scenes/a-round.md`, `scenes/the-bench.md`) and the "best phrasings / lines to preserve" in the Bible set the voice. Preserve canonical lines verbatim where they're slotted.
- **Before writing a planned scene**, read its entry in `meta-plan-chronology.md`, the relevant track doc (SATC or threesome), and any scene-specific companion notes; check the continuity-flags section for unresolved ordering/identity issues touching that scene.
- **When the plan conflicts with itself across documents**, surface the conflict and the version lineage rather than quietly resolving it — these are authorial decisions.
- **Regenerate the chronology HTML after editing the chronology.** Whenever you change `meta/meta-plan-chronology.md`, run `tools/chronology_html.py` to rebuild `chronology.html` and include the regenerated `chronology.html` in the same commit — never commit or push a chronology edit without refreshing its HTML.
- **Review-tracking (the `reviewed:` field).** To mark a scene reviewed, append a `· reviewed: YYYY-MM-DD` segment to its entry's metadata line in `meta-plan-chronology.md` (ISO dates only, so they never collide with the in-world story date). Each later review pass adds another comma-separated date — `reviewed: 2026-07-12, 2026-09-30`. In `chronology.html` the pill shows the **most recent** date, colored by **review round = number of dates listed** (categorical ColorBrewer palette; slate = unreviewed); no field = 0 reviews. Pills show on SCENE/VIGNETTE entries only (EVENTs get none). Regenerate the HTML as above after editing. Don't invent review dates — only the author records a review.
- **Naming:** "Pace" (the D role / public self) vs "Peter" (the hidden true self) is load-bearing — if Vee uses "Peter," it should land. "Vee" / "Vivienne Thorne" (V.T. = Virginia Tech). Setting is Virginia Tech, Blacksburg.
- **Filenames** are kebab-case in `scenes/`; `meta/` mixes kebab-case and snake_case (no version suffixes — git tracks history). Follow the convention of the directory you're adding to. **On-disk slugs drop the leading article** (`the`/`a`) to avoid "the"-clustering in `scenes/`, while the **display title keeps the article** — e.g. title "The New Ordinary" / slug `new-ordinary`, title "The Practice Room" / slug `practice-room`. Companion docs follow the slug (`meta-condensed-<slug>.md`, `meta-note-<slug>.md`). When renaming, distinguish scene-**title** references (update) from same-word prose/object/event uses (preserve). After a rename, run `tools/lore_mem.py check` to catch stale scene pointers in the lore-keeper's **persistent memory** (`.claude/agent-memory/`): `na.py reindex` self-heals the search index, but those hand-authored notes do not. Fix one with `tools/lore_mem.py forget <old>.md --to <new>.md`; the `/lore-keeper-mem` command wraps this (also `list` / `grep` / `wipe`).
- **Chapter-title references (`{{Title}}`).** In **planning docs only** (`meta/`, never `scenes/`), wrap a reference to a chapter *by its title* in double braces — `{{Famished}}`, `{{The Usual}}`, `{{A Round}}` — so it is machine-distinguishable from the same words used as an event, object, or common word (the *first night* event vs. the chapter `{{Famished}}`; a *fitting* vs. the chapter `{{A Round}}`). The **bare** display title is reserved for that event/prose sense; the **backticked slug** (`famished.md`) still names the file. Canonical titles are the entry headings in `meta-plan-chronology.md` (drop any trailing parenthetical). This makes a rename a safe find-and-replace on `{{OldTitle}}`, lets **`tools/lint_titles.py`** verify every reference resolves to a real chapter, and `tools/chronology_html.py` strips the braces for display. A doc's reference to its **own** chapter stays **bare** — the marks disambiguate *cross*-references, and title-as-word exegesis (a note explaining what its own title means) is never a chapter reference. A tracked **pre-commit hook** (`.githooks/pre-commit` — activate per clone with `git config core.hooksPath .githooks`) runs `lint_titles.py --all` whenever a `meta/*.md` is staged, so a dangling `{{…}}` can't be committed. **Adopt incrementally — mark title-refs as you touch a doc.**

## Scene titles

**Titles carry meaning, never plot.** Every scene title should hit *more than one* of: oblique · ambiguous · erotic · ironic · layered. Two hard rules: (1) the title must **not telegraph** what happens in the chapter; (2) it must be **meaningful only after reading** it (ideally deepening on reread).

**The engine:** present an innocuous, literal, or idiomatic **surface** going in, and detonate a **charged** second meaning once the chapter is read. The strongest titles **launder the erotic or the dark through ordinary/domestic language**, so nothing is given away and the irony is invisible from outside the chapter. A good title names a *frame* that turns out to mean something else — **never the central object or action.**

Worked examples (all endorsed):
- **A Recognized Method** — surface: a dish-soaking domestic idiom → charge: swatting as an erotic "method," and her body's involuntary method of arousal. (oblique/erotic/ironic/layered)
- **The Practice Room** — surface: a campus music room → charge: where Randi & Vee *rehearse* the seduction mechanism. (oblique/ironic/layered)
- **The New Ordinary** — surface: the new domestic routine → charge: the erotic baseline later scenes depart from; ordinariness as cover for deepening possession. (oblique/ironic/layered)
- **In Her Place** (was "Green Sheets") — surface: Randi in the spot Vee planned → charge: "put in her place" (humiliation/dominance); usurped position. (erotic/ironic/ambiguous/layered)
- **The Usual** (was "Cheeseburgers") — surface: their customary diner meal → charge: Pace's default of love-as-ledger; the warmth is the tell. (oblique/ironic/layered)
- **Old Acquaintances** (was "Vee — Christmas") — surface: Auld Lang Syne nostalgia → charge: the unresolved Pace/Randi "acquaintances"; jealousy poisoning memory. (ironic/ambiguous/layered)
- **Fairytale** — surface: Randi's charming-prince fantasy → charge: the flawless man reaches nothing — proof Pace is irreplaceable; the acceptable lie. (ironic/ambiguous/layered)

**Anti-pattern (rejected):** "Still My Shirt," "Wearing Him" — they name the prop/gesture, so they telegraph and go inert once read.

**When proposing titles:** lead with oblique/ironic frames; for each candidate, state the innocuous surface vs. the reread charge and which goals it hits; explicitly flag any candidate that names the central object/act (telegraphs) so it can be ruled out fast.

**Calibration:** not-telegraphing is the only disqualifier; the other goals (dual reading, detonate-on-reread, frame-not-the-act) are tradeoffs the author will knowingly spend for curiosity, playfulness, or charge. Present misses beyond the telegraph floor as tradeoffs, not grounds for a rename — recommend, then let the author weigh. Don't re-litigate retained titles (e.g. **The Pointing Game**, kept on purpose after review).
