# Currency Audit — drift ledger

Restartable audit that each `meta/` document is **current**: (a) filename / scene-title references resolve to real files/chapters, and (b) content agrees with the domain authorities. Findings only — **no fixes are applied from this pass**; each is a proposal you gate by risk × certainty.

## Method

One sub-agent per document, fresh context. Each reads its target in full and checks it against the masters below + filename/title currency, then returns findings. Findings are assembled here by the main session (agents do not write this file, to avoid write races). A document is not marked `checked` until its section is populated.

## Masters (who wins, by domain)

- **`meta-plan-chronology.md`** — **date / story-order / scene-inventory** master. Wins on any date, ordering, or "does this scene exist / what's it called" question.
- **`meta-arch-bible.md`** — **character + best-phrasings + Global Craft Rules** master.
- **`meta-thesis.md`** — **structural-argument** master (the three appetites, the bargain, consent-as-freedom).
- **`meta-arch-<name>.md`** — per-character **architecture ("why")** master for that character.
- **`meta-plan-pace-house.md`** — **set / spatial-continuity** master (where things are).
- **`meta-rules.md`** + **`style/style-rules.toml`, `style/style-allow.toml`** — **prose-style + reserved-word** canon (never-name, `undone/undid`, seen-vs-chosen).
- **`meta-craft-<name>.md`** — owns **surface rendering / voice** for that character (subordinate to bible/arch on doctrine).

## Precedence rule (conflict resolution)

Chronology wins dates/order/inventory; bible wins character + Global Craft Rules; arch wins the "why"; pace-house wins spatial; craft owns surface rendering. **Where a craft/target doc looks like a deliberate *newer* decision that supersedes an older master, flag it — do not overrule** (CLAUDE.md: docs "silently supersede on content"; these are authorial calls).

## Rubric

**Risk** (impact if the drift stays):
- `high` — breaks canon/continuity or would propagate a factual error into prose: wrong date/order, wrong character fact, a named-forbidden breach, or a filename tooling/links depend on.
- `med` — could mislead a future drafting/prep session or steer a wrong choice, but not immediately canon-breaking.
- `low` — cosmetic/navigational (stale wikilink, outdated cross-ref label); no doctrinal impact.

**Certainty** (is this real drift vs. intentional?):
- `high` — verified against a master; unambiguous (a filename that doesn't exist; a date contradicting chronology).
- `med` — conflicts with an authority but could be intentional supersession or nuance; needs author judgment.
- `low` — worth a look, plausibly fine or context-dependent.

**Grounding** — every finding cites the authority (path + quoted line) that establishes what's correct.

## Finding format

Each finding: `[risk/certainty]` — location (doc:line) — the claim → the problem → **Correct:** grounding (source + quote) → **Proposed fix:** exact before/after.

---

## Phases & status

| Phase | Scope | Status |
|---|---|---|
| 1 | Craft docs (3) | **done 2026-07-19 — 10 findings (high 1, med 5, low 4)** |
| S | **Rename sweep** — known renames across the whole repo (incl. `CLAUDE.md`) | **done 2026-07-19 — 26 refs (5 in-scope, 21 in agent-memory cache)** |
| 2 | Arch docs (pace, randi, vivienne, cassie, cassie-randi, sheri) | **done 2026-07-19 — 20 findings (high 0, med 6, low 14)** |
| 3 | Plan docs (satc-tracks, pace-house, schedule, dress-cluster, help-harm-dials, scrunchie-gaslight, summer) + thesis/bible/rules self-consistency | **done 2026-07-19 — 49 findings (high 2, med 23, low 24)** |
| N | **Pace neuro-framing reconciliation** — Pace neurotypical (introvert-charismatic); device softened to temperament-in-behavior | **done 2026-07-19 — bible :133/137/327 + 14 mechanical ripple swaps (CLAUDE.md, craft-pace, brief, among-friends/under-the-rug/recognized-method notes, DOCUMENTS.md, style-rules.toml). JUDGMENT resolved 2026-07-20 (author call): regrounded bible :163/:164/:178 as **choice-become-habit** — a habituated/trained non-reading, explicitly "not an innate deficit or wiring"; tragedy mechanic (he genuinely whiffs the cipher) preserved. Vee's metaphorical "wiring" left intact. **Workstream N COMPLETE.** Note: `style-rules.toml:183` `never-name` regex still lists the diagnostic terms — correct (those must still never hit the page).** |
| M | **Meta-doc filename rename sweep** — dead pre-`meta-*` pointers (`novel_thesis.md`, `pace_architecture.md`, `randi_architecture.md`, `vivienne_architecture.md`, `help-harm-dials.md`, `character-relationship-bible.md`, `scene-plan-chronology.md`, `open-questions.md`) | **in progress (apply agent 2026-07-20)** |
| ! | **Dead `summary.md`** — RESOLVED: `meta/meta-plan-summary.md` was a *condensed overview* that DEFERRED physical/wardrobe/food + room-meaning detail TO the bible ("condensed — full detail in the Character Bible"); deleted in `a81560b` (three-volume restructure). The bible's "supplements summary.md (full detail)" pointer is circular. Refs redirect → `meta-arch-bible.md` (apply agent). | **resolved 2026-07-20** |
| 4 | Topical notes (threesome-reveal, taste-thread, erotic-register, tender-relief, scar-reveal, …) | pending |
| 5 | Per-scene notes (`meta-note-<slug>`, ~45) — currency + prose cross-check | pending |
| 6 | Per-scene condensed (`meta-condensed-<slug>`, ~68) — **orphan/removal check ONLY** (regenerable; do not audit content — only flag if the scene is gone/renamed and the brief should be removed or regenerated) | pending |
| 7 | `DOCUMENTS.md` inventory accuracy | pending |

Restart: re-run any doc whose section below is absent or marked `pending`. Same-doc re-run is idempotent (findings replace).

## Applied changes log

**2026-07-19, batch 1 (Phase-1 safe currency):** `meta-craft-pace.md:44,90`; `meta-craft-randi.md:49,172,187` (see Phase 1 note).

**2026-07-19, batch 2 (rename fixes + low-risk + author-resolved conflicts):**
- Rename fixes (in-scope): `CLAUDE.md:125` (`meta-condensed-a-round.md`), `:155` (`scenes/a-round.md`), `:161` (teaching example → "The Practice Room"/`practice-room`); `meta-note-leave-no-trace.md:9` (`{{Two Towels}} → {{A Round}}`); `tools/chronology_html.py:402` (comment → `famished.md`).
- Low-risk copy/pointer: `meta-arch-vivienne.md:87` (cabin date → "~late Feb / early March"), `:187` ("come back for her panties"); `meta-arch-cassie-randi.md:55` (dangling flag → todo item 5), `:61` (miscited "Bible rule" → craft rule).
- Cache purge: 11 stale untracked `.claude/agent-memory/lore-keeper/` files deleted (regenerable; no git/canon impact).
- **Author-resolved conflicts:** (1) **Pace neurotypical** — `meta-arch-bible.md:133,137,327` reframed introvert-charismatic, not neurodivergent (see workstream N for ripple). (2) **Chi Latte** — `meta-arch-cassie.md:98,104` now Greek-coded exclusion ground (aligned to cassie-randi). (3) **Vee's hair** — `meta-arch-vivienne.md:49` + `meta-craft-vivienne.md:112` → "to her shoulder blades".
- Ledger self-fix: literal double-brace title tokens neutralized so `lint_titles --all` passes.

**Deferred prose flags (do not edit prose in this audit):**
- `see-you-later.md` — the line "no particular feelings about the yellow one on Draper" now reads as Cassie's light cover; with Chi Latte recanonized as Greek-coded exclusion, confirm whether the prose should register the exclusion more (author call).
- `meta-craft-randi.md:187` Fairytale render-note vs the drafted NYE framing (`fairytale.md`).

**Still-open (author-decision) findings not yet resolved:** cassie:96 enmity-root off-page; cassie-randi:30 "mutual enmity" vs asymmetry; `how-its-done` status (chronology "complete" vs condensed/arch "opening movement only"); pace:75 "twenty-year-old"; pace:117/thesis "fifteen years"; arch-sheri title-marking + age; cassie:46 scene-map lag; aspiration-vs-envy craft nuance (`meta-craft-vivienne.md:53`).

---

## Phase 1 — Craft docs

**✓ Applied 2026-07-19 (5 safe currency fixes):** `meta-craft-pace.md:44` (brace `{{The Deep End}}`), `:90` (`fitting`→`a-round`); `meta-craft-randi.md:172` (dress-barb→`in-her-place.md`), `:187` (Fairytale→drafted `fairytale.md`), `:49` (dropped the false `meta-rules.md` lanes citation). `lint_titles.py` passes. Remaining Phase-1 items are flag-for-decision (below): pace:90 touch-recognition clause, randi:104 cup-debut vs bible, vivienne:136 fitting-pointer, pace:165 "fine", vivienne:53 aspiration-vs-envy. Deferred prose pass: randi:187 render-note vs the drafted NYE framing.

### meta-craft-pace.md
_status: checked 2026-07-19 — 4 findings (high 1, med 1, low 2)_

Scope: owns Pace's on-page surface rendering (POV positioning, hot-fantasist interior, play/teasing register, body-as-gated-reveal, chivalric-grammar/vow enactment, behavioral signatures, humanizing-failing deployment); defers to bible/arch for character and the "why."

#### Currency
- **[high/high]** `meta-craft-pace.md:90` — "his kiss-entry signature (`the-bench`, `fitting`)": the slug `fitting` is stale; there is no `scenes/fitting.md`. The Fitting scene is now titled **A Round**, slug `a-round.md`. **Correct:** `meta-plan-chronology.md:89-90` — "### [SCENE] A Round … `a-round.md`". **Proposed fix:** `(`the-bench`, `fitting`)` → `(`the-bench`, `a-round`)`.
- **[low/high]** `meta-craft-pace.md:44` — "Pool, {{Jitterbug}}, the Deep End run on it": "the Deep End" is a real chapter (`{{The Deep End}}`) but used bare, so not machine-distinguishable per the double-brace title convention. (Bare "Pool" not flagged — chronology uses the same bare shorthand.) **Correct:** `meta-plan-chronology.md:59` — "protects **{{The Deep End}}**". **Proposed fix:** `the Deep End` → `{{The Deep End}}`.

#### Doctrine
- **[med/high]** `meta-craft-pace.md:90` — "the contrast is load-bearing for the **threesome touch-recognition** (Vee triangulating identity in the dark)": contradicts the climax authority, which forecloses touch as an identity channel (identity runs through the kiss alone). Installs a recognition route the reveal doc rules out; could misdirect threesome prep. **Correct:** `meta-note-threesome-reveal.md:95` "### The kiss = the SOLE channel of identity"; `:93` "**No amount of touch can identify Randi**"; `:129` "The damp hand-clasp — a planted rhyme, **not a channel**." **Proposed fix:** flag for author decision — the kiss-entry gesture is legitimately craft-owned, but the "touch-recognition / triangulating identity" clause should be cut or re-scoped to body-memory/rhyme (per the hand-clasp model), not identity.
- **[low/med]** `meta-craft-pace.md:165` — "He is, by every observable metric, **fine**. The **fine** is the cost.": surface tension with the reserved-word canon (`fine` belongs to lesser/ordinary men, never Pace). Reads as a *deliberate* deployment of exactly that diminishment charge (future-attenuated Pace reduced to "fine" is the tragedy), consistent with the bible's "fine men, fine sex … crackers" — likely intentional. **Correct:** `meta-arch-bible.md:79` "twenty years of **fine** men, **fine** sex … all crackers"; reserved-word note. **Proposed fix:** flag for author decision — confirm sanctioned thematic use (recommend keep); no change unless you want the reserved-word rule stated as absolute.

_Verified clean: `lint_titles.py` passes; all filename refs exist; doctrine spot-checks accurate (hot-fantasist/severe-discipline, 95% rule, no-filing/embodied-present, vow's three sentences + deeds-not-words, coded-channel-blindness, playful heat-kind, bench casts Randi not Vee). No date claims._

### meta-craft-randi.md
_status: checked 2026-07-19 — 4 findings (high 0, med 3, low 1)_

Scope: owns Randi's on-page surface rendering (warmth-as-instrument speech engine, three-smiles taxonomy, reserved-vocabulary guard [seeing=Pace / recognition=Randi], cup/locked-door body tells, physical description, how-to-render for the SATC scenes, self-subjugation, Fairytale, closing image); arch/bible/thesis own the "why."

#### Currency
- **[med/high]** `meta-craft-randi.md:172` — "First rung: the dress-barb vignette": names a **retired scene**. `sweet-dress-barb.md` and its condensed brief were retired and grown into `in-her-place.md`. **Correct:** `meta-arch-randi.md:78` "Entry rung: `scenes/in-her-place.md` (spring; the fall Randi/Pace material relocated and grown into a full scene)"; `meta-note-in-her-place.md:3,77`. **Proposed fix:** `First rung: the dress-barb vignette` → `First rung (entry): `in-her-place.md` (the retired fall `sweet-dress-barb.md`, grown into a full scene)`.
- **[med/high]** `meta-craft-randi.md:187` — "*(Unwritten scene; see `meta-plan-chronology.md` for plan…)*" for Fairytale: Fairytale is **drafted** (`fairytale.md`, 145-line scene). **Correct:** `meta-plan-chronology.md:208` "…Draft complete · `fairytale.md` · Randi's POV — mirror aperture". **Proposed fix:** `(Unwritten scene; see `meta-plan-chronology.md` for plan.` → `(Drafted: `fairytale.md`; see `meta-plan-chronology.md`.` — AND flag: the "How to Render It" guidance (dinner-then-return) should be reconciled against the drafted page (ski-resort / NYE framing) in a later prose pass. **Related:** `meta-arch-randi.md:214` carries the identical stale "Unwritten" claim — sweep in Phase 2.
- **[low/high]** `meta-craft-randi.md:49` — "(the friend/listener lanes, `meta-rules.md`)": the pointer does not resolve — the friend/listener-lanes rule appears in **no** `meta/` doc (only in lore-keeper memory [[randi-friend-pace-listener-lanes]]). **Correct:** rule not present in `meta-rules.md`. **Proposed fix:** flag for author decision — drop the citation, or (better) record the lanes rule in a real doc and point there.

#### Doctrine
- **[med/med]** `meta-craft-randi.md:104` — "Debuts at the bench … teaches the gesture its meaning" (the cup): conflicts with the bible on the cup's debut scene, but **agrees** with `meta-rules.md` and is chronologically sound (Bench = week 1; the engineered meet-cute is much later). **Correct (conflict):** `meta-arch-bible.md:222` "The compulsion debuts at the engineered meet-cute…" vs `meta-rules.md:81` "Cup debuts at the bench." **Proposed fix:** flag for author decision — reads as a **newer** craft decision (bench-as-debut, matching meta-rules) superseding the older bible paragraph; recommend updating `meta-arch-bible.md:222` to the bench (not changing the craft doc). If the bible means first *narrative-present* appearance, add that distinction to both docs.

_Verified clean: reserved vocabulary + seeing-register split (matches bible:335, meta-rules:74); "gorgeous" reserved (satc-tracks); cup fire/no-fire mechanics; physical description/Art Deco/bracelet (bible:196,249); self-subjugation high rung = `ignition-scalding.md`; never-name/undone canon; all filenames exist; `lint_titles.py` passes; no in-world dates._

### meta-craft-vivienne.md
_status: checked 2026-07-19 — 2 findings (high 0, med 1, low 1)_

Scope: owns Vee's on-page surface rendering (voice/register + regression-down, the shame-arousal loop, involuntary-signal nerve, physical description — Art Nouveau grammar, curvy-not-heavy, scent — and the prose commitments); defers the "why" to arch and character/Global Craft Rules to the bible.

#### Currency
- **[med/med]** `meta-craft-vivienne.md:136` — "*(The fitting as template for this: `two-towels.md`.)*": the pointer labeled "the fitting" points to the tour/offer scene, not the fitting proper. Per chronology, **A Round** *is* "The fitting itself. He measures her down to just her panties…" (`a-round.md`); **Two Towels** is the first-visit tour whose plant "sets up the fitting." Commitment 1 is about goods "rendered at full force" — the measuring/shame-arousal scene (`a-round.md`) is the stronger template. Reads like pre-split drift (the doc uses "the Fitting" for the satin-soaked measuring at `:116`, which is a-round.md content). **Correct:** `meta-plan-chronology.md:90-91` "### [SCENE] A Round … `a-round.md` … The fitting itself. He measures her…"; `:87` "the offer that sets up the fitting." **Proposed fix:** flag for author decision — update pointer to `a-round.md`, or if `two-towels` was chosen deliberately as the warm-goods template, reword "The fitting as template" so it doesn't mislabel the tour as the fitting.

#### Doctrine
- **[low/med]** `meta-craft-vivienne.md:53` — "**Aspiration, not envy.** … she never … curdles into envy or competition.": surface-worded absolute sits against the bible's architectural claim of a real (mutual, misread) envy. **Correct:** `meta-arch-bible.md:224` "**Vee envies what she misreads as Randi's composure** … Neither sees the other's envy." **Proposed fix:** flag for author decision — almost certainly *intentional and correct*: craft owns surface (render the draw as generous aspiration), while the bible's "envy" is deep author-knowledge Vee never sees; memory notes [[randi-never-self-denigrates]] ratify aspiration as current canon. Optional: add a one-clause nod that a structural envy she never perceives runs underneath, so the doc doesn't read as denying the bible's architecture.

_Verified clean: `lint_titles.py` passes (101 titles); all filename refs exist; `{{We Find Out}}` resolves; bare "the fitting" correctly used as event not chapter-title; `how-its-done.md` ref checks out; no name/age misuse (doc makes no Peter/Pace or age claims)._

---

## Rename sweep

### repo-wide known-rename sweep
_status: checked 2026-07-19 — 26 stale refs across 15 files (high 6, med 16, low 4)_

**Headline:** the tracked canon/prose layer is nearly clean (tooling `check_renames.py` + `lint_titles.py` covers it; "the fitting"/"First Night" *event* usages are legitimate and whitelisted). **Only 5 in-scope stale refs.** The other 21 sit in the **unversioned `.claude/agent-memory/lore-keeper/` cache** — regenerable, not canon, but they mislead future lore-keeper delegations.

**Confirmed targets:** Two Towels (`two-towels.md`, first visit/tour/offer) + A Round (`a-round.md`, the measuring); Famished (`famished.md`); A Recognized Method (`recognized-method.md`); In Her Place (`in-her-place.md`); The Usual (`the-usual.md`); Old Acquaintances (`old-acquaintances.md`); How It's Done (`how-its-done.md` = old "Vee Tells Randi About the Fitting Brunch"). Note: "Green Sheets — The Gift" (`chronology:341`) is a *distinct still-current scene*; "Green Sheets" as In Her Place's former title appears only historically — no stale hits.

#### In-scope (tracked layer) — 5 refs
- **[med/high]** `CLAUDE.md:155` — "`scenes/fitting.md`" no longer exists. **Proposed fix:** → `scenes/a-round.md` (or `two-towels.md`).
- **[low/high]** `CLAUDE.md:125` — "`meta-condensed-fitting.md`" does not exist. **Proposed fix:** → `meta-condensed-a-round.md`.
- **[med/high]** `CLAUDE.md:161` — the article-drop teaching example 'title "The Fitting" / slug `fitting`' is stale/misleading. **Proposed fix:** → a live pair, e.g. 'title "The Practice Room" / slug `practice-room`'.
- **[med/med]** `meta-note-leave-no-trace.md:9` — reading-order chain has a bare stale "Fitting" slot amid braced titles. **Proposed fix:** `→ Fitting →` → `→ {{Two Towels}} → {{A Round}} →`.
- **[low/high]** `tools/chronology_html.py:402` — code comment example "`scenes/first-night.md`" (nonexistent; cosmetic, no runtime effect). **Proposed fix:** → `scenes/famished.md`.

#### Out-of-scope — `.claude/agent-memory/lore-keeper/` cache — 21 refs across 11 files
Regenerable cache, not canon (low canonical risk) but **med risk of misleading future lore-keeper lookups**. Highest concentration: `induction-dress.md` (~8), `first-satc-brunch-cartier-seed.md` (~6). Recurring stale tokens: `the-fitting.md`→`two-towels.md`/`a-round.md` (context), `first-night.md`→`famished.md`, `brunch-fitting-randi.md`→`how-its-done.md`, `Vee — Christmas`→Old Acquaintances, `sweet-dress-barb`/"Sweet"→In Her Place (drafted, fall→spring), "Cheeseburgers"→The Usual (now booth face-to-face; counter/no-eye-contact rationale retired). Several `high/high` (e.g. `vee-parents-established.md:104,109`, `pace_randi_vee_scheduling.md:19`, `randi_pace_fall_dynamic.md:20`, `sheri_canon_placement.md:14`). **Recommendation:** purge/regenerate these caches rather than hand-edit — they're derived and outside `check_renames.py`/`lint_titles.py` reach. This is the same drift reservoir as the auto-memory store fixed earlier this session.

_Deliberately NOT flagged (verified legitimate): "the fitting"/"First Night" as the in-world *events*; `check_renames.py` + `lint_titles.py` own pattern/alias definitions; "bacon cheeseburgers" (food); "green sheets" (object/thread + the current Gift scene); "This is still my shirt" (dialogue); CLAUDE.md's rename-history worked-examples list._

---

## Phase 2 — Arch docs

### meta-arch-pace.md
_status: checked 2026-07-19 — 2 findings (high 0, med 0, low 2)_

Scope: owns the deep "why" of Pace — formation, transgression-as-cognition appetite, consent welded to arousal, the after-register hamartia + origin-as-choice, chivalric grammar + the vow, declined honorable exits, slow attenuation. Surface companion: `meta-craft-pace.md`.

#### Currency
- none found. `lint_titles.py` passes (no double-brace title refs); all filename refs exist; no stale scene names; "left for school at fifteen" matches `bible:127`; the two-relationship split matches `meta-note-first-love.md`.

#### Doctrine
- **[low/low]** `meta-arch-pace.md:75` — "almost no **twenty-year-old** woman with Vee's appetite would say no": Vee is canonically **21**. Reads as a rhetorical demographic category, not a claim about Vee, so likely harmless, but grazes the peer-age guard. **Correct:** `meta-arch-bible.md:129` "Vee and Randi, both 21 … peers". **Proposed fix:** flag for author decision — leave if generalization intended, or "twenty-year-old" → "twenty-one-year-old"/"young".
- **[low/low]** `meta-arch-pace.md:117` — "the choice has been **running for fifteen years**": numerically implausible vs the ages (Pace 22; choice deployed ~age 15–17 → ~5–7 yrs). **NOT drift against a master** — the thesis carries identical phrasing. **Correct:** `meta-thesis.md:105` "fifteen years of compounding"; `:109` "fifteen years deep". **Proposed fix:** flag for author decision — deliberate shorthand (keep in both) OR a shared slip to fix in `meta-arch-pace.md` **and** `meta-thesis.md` together (do not fix one alone).

### meta-arch-randi.md
_status: checked 2026-07-19 — 3 findings (high 0, med 1, low 2)_

Scope: Randi's "why"-architecture (locked need-engine, want/need hinge, being-seen fork, sadism-as-inverted-need, Fairytale half-seeing). Aligns tightly with thesis/bible; surface companion `meta-craft-randi.md`.

#### Currency
- **[med/high]** `meta-arch-randi.md:213-215` — "## Fairytale …" / "*(Unwritten; see `meta-plan-chronology.md` for scene plan.)*": **stale — the scene is drafted** (`fairytale.md`). **Correct:** `meta-plan-chronology.md:208` "Thu Dec 31 · Draft complete · `fairytale.md` · Randi's POV — mirror aperture". **Proposed fix:** `*(Unwritten; see `meta-plan-chronology.md` for scene plan.)*` → `*(Scene draft: `fairytale.md`; craft in `meta-note-fairytale.md`.)*` — and flag: reconcile the section's forward-looking framing against the drafted prose (deferred). [Companion to the `meta-craft-randi.md:187` Fairytale finding — sweep both.]
- **[low/low]** `meta-arch-randi.md:140` — "*(First SATC extraction draft: `how-its-done.md` — opening movement only; second movement drafted separately.)*": disagrees with chronology, which marks it fully drafted; but matches `meta-condensed-how-its-done.md:3`. **The mismatch is chronology-vs-condensed, not arch-only.** **Correct:** `meta-plan-chronology.md:100` "Sun Oct 11 · Draft complete · `how-its-done.md`". **Proposed fix:** flag for author decision — reconcile "opening movement only" across arch/condensed/chronology so one status governs; no arch-only edit safe until settled.
- **[low/low]** `meta-arch-randi.md:213` — bare heading `## Fairytale …` while the same scene is `{{Fairytale}}` at :209/229/239/241: inconsistent title-marking of a cross-ref (lint still passes). **Proposed fix:** flag for author decision — house-style call on bracing a scene name used as a section heading.

#### Doctrine
- none found. Core claim, need-engine, want/need hinge, being-seen fork, sadism-as-inverted-need, Fairytale half-seeing all match `meta-thesis.md` + bible. Cup material asserts *valence* only (not a debut point), so it does **not** enter the bible:222-vs-meta-rules:81 debut conflict. "engineered meet-cute" (:215) correctly denotes Vee's, not Randi's. Ages match.

### meta-arch-vivienne.md
_status: checked 2026-07-19 — 4 findings (high 0, med 1, low 3)_

Scope: Vee's "why"-architecture (appetite, shame wound, arc, half-seeing). Surface companion `meta-craft-vivienne.md`.

#### Currency
- **[low/high]** `meta-arch-vivienne.md:187` — "She does not **take for** her panties. The artifact stays.": garbled sentence (dropped/duplicated word); canon (she leaves the panties; artifact stays) is correct per `meta-note-threesome-reveal.md`. **Proposed fix:** "does not take for her panties" → "does not come back for her panties" (flag: confirm intended verb).
- **[low/med]** `meta-arch-vivienne.md:87` — "Installed at the cabin (**~late Feb**…)": marginally narrows the source range. **Correct:** `meta-plan-chronology.md:~322` "~late February or early March"; `meta-note-grace.md:3` "~late Feb / early March." **Proposed fix:** "~late Feb" → "~late Feb / early March".

#### Doctrine
- **[med/med]** `meta-arch-vivienne.md:49` — "**Long,** curling hair worn loose": direct **arch↔craft conflict** — craft says shoulder-length; bible is silent on length. A scene drafted from arch vs craft would differ. **Correct:** `meta-craft-vivienne.md:112` "**Shoulder-length** hair worn loose, warm dark red…". **Proposed fix:** flag for author decision — pick one length, reconcile arch:49 ↔ craft:112 (bible silent, either can become canon).
- **[low/med]** (adjacent, not in target) — the mutual-envy tension is **absent from arch-vivienne**; it lives between `meta-arch-bible.md:227` ("Vee envies … Randi's composure") and `meta-craft-vivienne.md:53` ("Aspiration, not envy"). Noted only because the brief asked; arch-vivienne needs no change. [Same item as the Phase-1 vivienne:53 finding.]

_Verified clean: all 13 filename refs resolve; `lint_titles.py` passes; no stale renames (uses `a-round.md` / "the fitting"-as-event correctly); ages/height/family match bible; thesis alignment holds (shame-as-fuel, consent-as-freedom, cultivation-mistaken-for-discovery)._

### meta-arch-sheri.md
_status: checked 2026-07-19 — 4 findings (high 0, med 1, low 3)_

Scope: Sheri's architecture (the bike friendship; the no-cost-social-configuration; her function in Pace's holiday/estrangement arc).

#### Currency
- **[low/high]** `meta-arch-sheri.md:56,68,104` — mixes backticked `` `Another Round` ``/`` `The Usual` `` with `{{Another Round}}` for chapter-title refs. **Correct:** CLAUDE.md double-brace title doctrine (braces for title-refs; backticks for slugs). **Proposed fix:** flag — incremental adoption sanctioned; if touched, normalize title-refs to `{{Another Round}}`/`{{The Usual}}`.
- **[low/med]** `meta-arch-sheri.md` (whole doc) — never references `sheri-first-ride.md`, Sheri's first drafted on-page appearance. **Correct:** `meta-plan-chronology.md:139-140` "[VIGNETTE] Sheri — First Ride · Draft complete · `sheri-first-ride.md`". **Proposed fix:** flag — add a one-line pointer to `sheri-first-ride.md`.
- **[low/low]** `meta-arch-sheri.md:9` — "~20, a psych undergrad": age uncorroborated by any authority (bible SHERI section gives none); consistent with peer band but unanchored. **Proposed fix:** flag — confirm ~20; if canon, note in bible's SHERI quick-ref.

#### Doctrine
- **[med/med]** `meta-arch-sheri.md:106` — "(The old 'no-eye-contact spares him' rationale is retired — he is **introvert-charismatic, not autistic**.)": **contradicts the bible's still-standing neuro framing**, but the **chronology corroborates the sheri doc** (`:217` "introvert-charismatic, not autistic, and eye-avoidance would poison the decency"). Reads as a **deliberate supersession the bible hasn't absorbed** — and it touches the core "neurodivergence NEVER NAMED" device. **Correct (stale side):** `meta-arch-bible.md:137` "On the spectrum with ADHD hyperfocus"; `:133` "no eye contact = the only social configuration that costs him nothing". **Proposed fix:** flag for author decision — precedence gives bible authority on character, but chronology + sheri jointly retire the autistic/eye-contact framing; reconcile by updating **the bible** (`:133,:137,:151`) or explicitly confirm the bible stands. **Do not silently edit either.** ⇒ HIGH-PRIORITY: affects Pace's foundational framing across many docs. **[RESOLVED 2026-07-19: author confirmed Pace neurotypical; bible corrected; see workstream N.]**

---

## Phase 3 — Plan docs + master self-consistency

### meta-plan-schedule.md
_status: checked 2026-07-19 — 3 findings (high 0, med 1, low 2)_
- **[med/high]** `:97-100` — {{Standards}} worked example "(≈ Sep 2.)" is a **Wednesday** and contradicts chronology (Standards = Sat Sep 5). **Correct:** `chronology:38` "Sat Sep 5". **Fix:** `(≈ Sep 2.)` → `(≈ Sep 5.)` (the "Saturday morning" tag is right).
- **[low/med]** `:72` — labels Dec 19–Jan 17 "Winter break"; chronology says "Christmas break" (dates identical). **Fix:** flag — align label or leave.
- Neuro: clean. Verified: all dates/weekdays compute and match chronology; lint clean.

### meta-plan-dress-cluster.md
_status: checked 2026-07-19 — 3 findings (high 0, med 2, low 1)_
- **[med/high]** `:3` — "`two-towels.md` (the making, which leaves the dress unfinished)": the *making/fitting* is **A Round**, not Two Towels (the offer). **Correct:** `chronology:91`. **Fix:** → `a-round.md` (or split: two-towels=offer, a-round=making).
- **[med/high]** `:45` — Grain #2 "killed on contact … or from a sister": **superseded** — current canon has recognition *fire* then be overridden by flattery; "from a sister" gone (online-found/buyable). **Correct:** `meta-plan-scrunchie-gaslight.md:25`; `chronology:311`. **Fix:** delete the reference-copy mechanism and point to scrunchie-gaslight, or rewrite to fires-then-flattery.
- **[low/med]** `:38` — Grain #1 "~mid–late Feb" drifts looser than owner doc ("late Feb"). **Fix:** flag — tighten to "late Feb" if wanted.

### meta-thesis.md (master self-consistency)
_status: checked 2026-07-19 — 2 findings (high 0, med 1, low 1)_
- **[med/med]** `:105,:109` — "fifteen years of compounding / refusal fifteen years deep": numerically odd vs age canon (Pace 22). **Shared figure** with `meta-arch-pace.md:117` (verbatim) — **do NOT fix one alone**. **Fix:** flag joint author decision (deliberate shorthand vs shared slip). [pairs with pace:117]
- **[low/high]** neuro: **thesis is already clean** — no neurodivergent framing; the choice-become-habit framing is neurotypical-consistent (bible:137/:143 "practicing, not failing to perceive"). ⇒ workstream N: thesis needs no change.

### meta-plan-summer.md
_status: checked 2026-07-19 — 2 findings (high 0, med 1, low 1)_
- **[med/med]** `:36` — "the Bench" as "erotic apex / last full bloom" points at the WRONG chapter: the apex is **{{Vee on the Bench}}** (`vee-on-the-bench.md`), distinct from **The Bench** (Pace/Randi). **Correct:** `chronology:389-391`. **Fix:** `the Bench` → `{{Vee on the Bench}}`. [also resolves the bare-title low/med]
- Neuro: clean (no Pace-interiority framing).

### meta-plan-pace-house.md — MOST DRIFTED (10 findings)
_status: checked 2026-07-19 — 10 findings (high 0, med 7, low 3)_
- **New class — stale meta-doc pointers:** **[med/high]** `:5,10,193` `character-relationship-bible.md` → `meta-arch-bible.md`; **[med/med]** `:6,10,194` `summary.md` (dead file) → likely `meta-arch-bible.md` (confirm); **[med/high]** `:46,197` `randi_architecture.md` → `meta-arch-randi.md`.
- **[PLAN] tags that are now drafted [PAGE]:** **[med/high]** `:116,119` Office; `:121,124` Woodshop; **[med/high]** `:98,112` Vee's top-drawer + mirror-ritual (drafted in `the-top-drawer.md`); **[low/high]** `:70` KitchenAid. **Fix:** retag `[PLAN]`→`[PAGE]`, cite `two-towels.md`/`the-top-drawer.md` (spring gaslight grains stay `[PLAN]`).
- **[med/high]** `:8-9` `[PAGE]` source list incomplete — add `two-towels.md` + `a-round.md`.
- **[med/high]** `:137,144` the fitting cited to `dress-pickup.md` — the fitting proper is `a-round.md`; keep dress-pickup only for pickup-day bullets.
- **[low/low]** `:50` cabin date "~late Feb" → "~late Feb / early March".
- Neuro: clean ("retreat" = privacy/cost, matches corrected bible:137).

### meta-plan-satc-tracks.md
_status: checked 2026-07-19 — 3 findings (high 0, med 1, low 2)_
- **[med/high]** `:322` — "since **4 weeks** before he met Vee": undercounts; Randi/Pace opened ~mid-Aug, meet-cute Thu Sep 24 = ~6 weeks. Load-bearing (disposability-ledger wound). **Correct:** `bible:202`, `arch-randi:96`, `chronology:53`. **Fix:** → "since ~6 weeks before he met Vee".
- **[low/med]** `:351` — "confirm spring stats class co-enrolls Vee+Randi+Cassie" now canon (`chronology:185`). **Fix:** drop/downgrade the open-question.
- **[low/med]** `:68` — verbal-staircase rung 1 "Coffee after class" has no scene home (folded into `{{Dear}}`/`{{See You Later}}`, chronology:47,70). **Fix:** flag — confirm mapping.
- Neuro: clean.

### meta-plan-help-harm-dials.md
_status: checked 2026-07-19 — 6 findings (high 0, med 2, low 4)_
- **[med/high]** `:3,:239` — cites dead `novel_thesis.md` → `meta-thesis.md`. [meta-doc-rename class]
- **[med/high]** `:245` — "Working rule 23 in the thesis" miscited/renumbered vs current thesis rule 23. **Fix:** re-verify number & requote current text (or cite by section).
- **[low/med]** `:241` — rule 20 paraphrase adds "in registers each party can detect" (not in current rule 20; closer to rule 21). **Fix:** trim/attribute.
- **[low/high]** `:255-261` — "Future Additions … not yet inventoried" partly drafted (`still-life.md`, `shoe-shopping-randi.md`). **Fix:** living-doc backlog; inventory when next touched.
- **[low/med]** `:33` — "hunger … installed the first night" overshoots cracker-and-meal (the *specifications* were installed; hunger pre-existed). **Correct:** `bible:54`. **Fix:** soften to "specifications … installed".
- **[low/low]** `:93,:171` — "apparatus does not see": neuro-adjacent but **reconcilable** (harm-one non-asking is canon, not perceptual deficit). Watch.

### meta-plan-scrunchie-gaslight.md
_status: checked 2026-07-19 — 4 findings (high 1, med 1, low 2)_
- **[high/high]** `:27` — Grain #3 "cover holds / she credits Pace and takes it" is **superseded**: current canon is the **no-absorber collapse** (the Pace-refill story arrives, dies on the drawer's grammar [he never touches it], and defaults to "I must be wrong"). **Correct:** `chronology:371,474,375`. **Fix:** revise to the no-absorber-collapse model.
- **[med/med]** `:9,25` — frames the taking as conscious strategy ("real objective / training her early"). Current canon = involuntary "**compulsive leak, not strategy**". **Correct:** `meta-condensed-randi-takes-scrunchies.md:17`; arch-randi middle register. **Fix:** reframe as the mechanism's *function on Vee*, not Randi's design.
- **[low/med]** `:15-20` — arithmetic table labels the off-page ~6-taken drop as Grain #1; chronology splits them (the take = unnamed `[EVENT]` `:303`; Grain #1 = Vee's flicker `:305-307`). **Fix:** split move from grain label.
- **[low/low]** `:11` — "Pace would never track the count": clean (gender/attention-framed, not neuro). Keep gender-framed.
- Currency: clean (files exist, lint passes, grain dates match).

### meta-plan-scrunchie-gaslight.md
_status: pending_

### meta-arch-bible.md (master self-consistency)
_status: checked 2026-07-19 — 9 findings (high 1, med 5, low 3); Randi meet-cute lock confirmed intact_
- **[high/high]** `:7-9` — the "four-document core" header cites **five dead filenames** (`novel_thesis.md`, `pace_architecture.md`, `randi_architecture.md`, `vivienne_architecture.md`, `help-harm-dials.md`) → `meta-thesis.md`, `meta-arch-pace.md`, `meta-arch-randi.md`, `meta-arch-vivienne.md`, `meta-plan-help-harm-dials.md`. [meta-doc-rename class — mechanical]
- **[med/high]** `:11,68,127,196` — dead pointers: `scene-plan-chronology.md`→`meta-plan-chronology.md`, `open-questions.md`→`meta-todo-open-questions.md`; and **`summary.md` ×4 is DEAD with no on-disk equivalent** (held physical/wardrobe/food detail). **Fix:** rename the first two; **flag `summary.md`** for author — where did that content go?
- **[low/med]** `:133` — `` `Among Friends` `` → `{{Among Friends}}`.
- **[med/high]** `:222` — cup "debuts at the engineered meet-cute" is **stale** → the **bench** (`meta-rules.md:81`, `meta-craft-randi.md:104`, timeline). **Fix:** update bible to bench. [pairs rules:81]
- **[med/med]** `:222` — cup mechanic rendered "grip/lift-don't-drink" vs craft's **nail-press-under-the-fingernail** (`meta-craft-randi.md:95`). **Fix:** reconcile bible to craft.
- **NEURO (workstream N):** `:141` "neurological comfort" → mechanical (neuro pass); **`:163` "(wiring)" aptitude** = JUDGMENT (reframe as learned); **`:178` coded-channel blindness as "circuit/deficit … MORE literal under stress"** = JUDGMENT, the **largest open reconciliation item** (author decides re-grounding, not a word-swap); `:137` eyes-on-thing + `:133/174` hyperfocus retained = intentional, no change.
- **[low/high]** `:206/:222` — Randi meet-cute lock (un-engineered) intact vs Vee's engineered. No finding.

### meta-rules.md (master self-consistency)
_status: checked 2026-07-19 — 7 findings (high 0, med 2, low 5)_
- **[med/high]** `:81` — "Cup debuts at the bench" is CURRENT/correct — corroborates `bible:222` is the stale side. **Do NOT change meta-rules.**
- **[med/high]** `style/style-rules.toml:186` — "Pace's neurodivergence is NEVER named" is stale; meta-rules PACE § has no temperament-never-labeled item. **Fix (neuro pass):** reword toml to temperament; consider a PACE checklist item.
- **[low/med]** `:137,171` — brace section headers `{{The Bench}}`/`{{The Pointing Game}}`/`{{Turned Up}}` (object/event uses at :144/155/160 stay bare).
- **[low/med]** `:177,179` — "The fitting detonates it": event-sense (preserve) or `{{A Round}}` if title-sense — confirm.
- **[low/med]** `:73-75` — seen/chosen reserved split not encoded in `style-rules.toml` (enforcement gap only).
- **[low/med]** `:157` — good-prose exemplar uses "the way" (a flagged linter tic); "fine" reserved word uncodified in both versioned docs. **Fix:** reconcile exemplar; consider codifying "fine".
- **[low/high]** `:42-43` — neuro clean (musician-improvising framing = neurotypical-consistent).

### meta-rules.md (master self-consistency)
_status: pending_

### meta-arch-cassie.md
_status: checked 2026-07-19 — 4 findings (high 0, med 1, low 3)_

Scope: Cassie's architecture (the Cassandra device; anti-Greek stance; the venue-exclusion mechanism from her side).

#### Currency
- **[low/med]** `meta-arch-cassie.md:46` — Function list gives only "Statistics project (`outlier.md`)" for the Cassandra beat; scene-map lags the drafted corpus (`stats-simpsons-paradox.md`, `turned-up.md` are now drafted Cassie-Cassandra beats). **Correct:** `meta-plan-chronology.md:121` "Pairs with {{Turned Up}} (…Cassie's Cassandra role)." **Proposed fix:** flag — if Function/tells meant to be current, add the stats-Simpson/Turned-Up pairing.

#### Doctrine
- **[med/high]** `meta-arch-cassie.md:98,104` — "a glossy coffee shop she'll sit in for Vee with no particular feeling" / Draper "yellow place … no particular feelings about the venue": **bilateral conflict** with the cassie-randi master, which casts that same Chi Latte as the Greek-coded exclusion instrument. Drafted scene (`see-you-later.md:73`) supports the *softer* reading, yet the venue is unambiguously Greek-coded on the page. **Correct:** `meta-arch-cassie-randi.md:53` "a place Cassie would never go … exclusion built into the choice of venue." **Proposed fix:** flag for author decision — reconcile whether Chi Latte excludes Cassie *by design* (cassie-randi) or is *neutral/logistical* (cassie + drafted scene). ⇒ paired with the cassie-randi:53 finding; likely edit is on cassie-randi's side or a shared note. [Same conflict, both sides flagged.]
- **[low/med]** `meta-arch-cassie.md:96` — "in high school, the Greek type mistreated her friends … under-writes the instant mutual enmity": supplies a causal origin the character docs mark as needing none. **Correct:** `meta-arch-bible.md:257` / `meta-arch-cassie-randi.md:30` "needs no explanation." **Proposed fix:** flag — likely intentional (author-knowledge, off-page); confirm the high-school root stays off-page only.

_Verified clean: all filename refs resolve; `lint_titles.py` passes (cites scenes by filename, no double-brace title); dates check out ("laid off in 2020" = chronology:185; toenails game = chronology:108); `meta-craft-cassie.md` correctly forward-referenced as not-yet-existing._

### meta-arch-cassie-randi.md
_status: checked 2026-07-19 — 4 findings (high 0, med 2, low 2)_

Scope: the Cassie↔Randi relational architecture (asymmetric enmity, venue-exclusion mechanism, dress-code lunch concept).

#### Currency
- **[med/med]** `meta-arch-cassie-randi.md:55` — "See `meta-plan-chronology.md` continuity flag and `meta-todo-doc-updates.md`.": **dangling pointer** — the chronology has no dress-code continuity flag (current flag 16 is "Spring underplanned"). Live tracker is `meta-todo-doc-updates.md:19` item 5 (which itself carries the same stale "(chronology flag 16)" pointer). **Proposed fix:** → "See `meta-todo-doc-updates.md` item 5 (placement pending; no live chronology flag)." [Pattern: stale continuity-flag numbers — sweep in Phase 3.]

#### Doctrine
- **[med/med]** `meta-arch-cassie-randi.md:53` — "the Greek-coded coffee shop on Draper — **a place Cassie would never go.**": overstates against the cassie master, which guards this exact point. **Correct:** `meta-arch-cassie.md:98` "A glossy coffee shop she'll sit in for Vee with no particular feeling; an actual sorority haunt she declines." (Drafted scene: Cassie declines for a *lab at noon*, not venue aversion.) **Proposed fix:** flag — soften "never go" to align with the glossy-vs-sorority-haunt distinction.
- **[low/med]** `meta-arch-cassie-randi.md:30` — "**Instant mutual enmity**": internal tension with the doc's own line 39 ("Randi … pure dismissal", not enmity). Inherited from `meta-arch-cassie.md:96` but overstates Randi's pole as this doc recharacterizes it. **Proposed fix:** flag — keep as inherited shorthand or retune to "one-way dislike (Cassie's), met by dismissal (Randi's)".
- **[low/med]** `meta-arch-cassie-randi.md:61` — "(Bible rule: Randi's power wears warmth, not coolness.)": rule is genuine but **not in the bible**. **Correct:** `meta-brief.md:46`, `meta-craft-randi.md:30`, `meta-rules.md:68`. **Proposed fix:** → "(Craft rule — `meta-craft-randi.md`, The Speech Engine: …)". [Pattern: miscited-authority — cf. the Phase-1 randi:49 lanes citation.]

_Verified consistent: all six load-bearing quotes check out in-source ("Goodbye, Vee", "It's coffee, weirdo" [Vee], flat "Cassie", great-aunt line, "You saw it and I didn't", "She's a lot"→Sheri); great-aunt framing matches cassie master + chronology flags 5/23; all filenames exist; lint clean; no dates._

### meta-arch-sheri.md
_status: pending_
