# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is **not a codebase.** It is the working repository for *With a Long Spoon*, a novel-length work of psychological literary erotica written in chapters. There is nothing to build, lint, or test. "Architecture" below means the novel's structural argument and document hierarchy; "working conventions" replace build commands. Comp shelf: Gaitskill, Duras's *The Lover*, Salter's *A Sport and a Pastime*, *Story of O* — literary erotica where the structural argument and character interiority carry the load that plot mechanics carry in genre.

## Repository layout

- `meta/` — the planning corpus: thesis, per-character architecture, the relationship bible, the scene plan, and the SATC/threesome track docs. This is where the novel is *designed*.
- `scenes/` — drafted prose. Currently `the-bench.md` and `the-fitting.md`. New chapters land here.

There is no prose draft of most scenes yet; `meta/` is far ahead of `scenes/`. Most work is either (a) developing a planned scene into prose or (b) refining the architecture.

## Document authority — read in this order, trust in this order

The corpus has accreted across numbered "Sessions" and document versions, so **newer documents silently supersede older ones and the filenames lie about currency.** Before acting on any plot/structure detail, reconcile against the most recent source. Known hazard: `meta/summary.md` is labeled "Session 5" and refers to a "v5" document map, but `meta/scene-plan-chronology.md` is "v8" and states it *supersedes summary_v7*. **The chronology doc is the newer scene inventory; the summary's inventory is stale where they conflict.** When in doubt, the higher version number and the `[NEW]` markers win — and flag the conflict rather than silently picking one.

Authoritative-by-domain (each doc owns its subject; don't relitigate it elsewhere):

- `meta/scene-plan-chronology.md` — **current scene order and inventory** (v8). Story order = list order. Carries live `[NEW]` beats and a "continuity flags to resolve" section at the bottom — check it before placing or reordering scenes.
- `meta/summary.md` — master concept overview and document map. Front door for orientation; **inventory section is superseded** (see above).
- `meta/character-relationship-bible.md` — authoritative on character, best phrasings to preserve, and the **Global Craft Rules** (the non-negotiables below live here in full).
- `meta/novel_thesis_v5.md` — the structural argument: the three destructive appetites, the bargain, why each character half-sees. The "why" under everything.
- `meta/pace_architecture_v5.md`, `meta/randi_architecture_v3.md`, `meta/vivienne_architecture_v4.md` — deep per-character architecture. Sections in the Vee doc are tagged `ARCHITECTURE` (fixed) vs `WEATHER` (mutable surface) — respect the distinction.
- `meta/satc-track-scenes.md` — authoritative on the Randi/Vee confidante track: the verbal and physical (goodbye-kiss) staircases, the format-break scenes, how to vary the brunches, and its own DOs/DON'Ts.
- `meta/threesome-reveal.md` — authoritative on the climax: the two-tier blindfold structure, the kiss-as-sole-channel-of-identity, the reveal image, the closed (not ajar) ending.
- `meta/notes-the-fitting.md` — scene-specific companion notes (the no-tag-shirt plant the Fitting pays off; the Shoe-Shopping scene to develop after it). Pattern for how scene-local notes are kept.

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
- **Filenames** are kebab-case in `scenes/`; `meta/` mixes kebab-case and snake_case with version suffixes (`_v5`, `_v3`). Follow the convention of the directory you're adding to.
