# Orientation — structural engine, craft rules, scene-title engine

**Why this file exists (read this first).** This content used to live in `CLAUDE.md`.
It was moved out because `CLAUDE.md` is **automatically injected into every custom
subagent** (confirmed: only the built-in Explore/Plan agents skip it; there is no
per-agent exclusion). That injection was **leaking the novel's design into the
`blind-reader` cold-read instrument** — a reader that is supposed to know nothing but
the page was quoting the thesis, the Cassandra device, "produces with words what Pace
produces with the body," the blindfold reveal, etc., straight out of `CLAUDE.md`.

So this doc is the home for the **spoiler-grade orientation**: the core structural
engine, the non-negotiable craft rules, and the scene-title engine (with its
reread-charges). The main assistant loads it at session start (it is on the `Read`
list in `CLAUDE.md`) and can pull it via the `lore-keeper`. **It must never be
`@`-imported into `CLAUDE.md` or otherwise auto-loaded** — that would put it right back
into every subagent and re-open the leak. `meta/*.md` are not auto-loaded into
subagents; keep it that way.

This is a **summary/index**; the authoritative full versions live in the docs it
points to (`meta-thesis.md`, the Bible's Global Craft Rules, the SATC/threesome track
docs). When it conflicts with those, they win.

---

## Scene-participant confusions to guard against (continuity)

The most common misattribution: several Pace-POV scenes render the woman as an unnamed
"she." **"The Bench"** (the opening scene) is **Pace/Randi — Vee is absent** — and it is
distinct from the later **"Vee on the Bench."** Before crediting any contact/first/trait
to Vee, confirm POV/participants from the scene header and chronology entry. (This lives
here, not in `CLAUDE.md`, because the future scene title would spoil a blind first-reader.)

## Naming (the male lead's two names — spoiler-grade)

"Pace" is the D role / public self; **"Peter" is the hidden true self.** The split is
load-bearing — if Vee uses "Peter," it should land. This lives here rather than in
`CLAUDE.md` because "Peter" leaking into a blind first-reader pre-spoils the reveal.
(Vee / Vivienne Thorne and the Virginia Tech setting are fine to keep in `CLAUDE.md` —
they're jacket-level, not reveals.)

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
- **Scene-type-specific running threads** (moved here from `CLAUDE.md` 2026-08-05 — the named threads are spoiler-grade and must not leak into `blind-reader` via `CLAUDE.md` inheritance; a cold reader who knows a thread's *name* knows it's a device): **every sex scene** must run the seed-decision against the **taste thread** (`meta-note-taste-thread.md`) in addition to the general running-threads registry. Most scenes seed nothing — the point is to *decide*, not to plant every time.

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


## Comp shelf & register (moved from CLAUDE.md/AGENTS.md — kept out of the file blind subagents inherit)

Comp shelf: Gaitskill, Duras's *The Lover*, Salter's *A Sport and a Pastime*, Rice/Roquelaure's *Beauty* trilogy (the jacket comp) — literary erotica where the structural argument and character interiority carry the load that plot mechanics carry in genre. *Story of O* is an influence, never a comp — emotionally cold where this book is warmth-first (author ruling 2026-07; see `meta/meta-blurb.md`).
