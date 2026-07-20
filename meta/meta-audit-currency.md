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
| 4 | Topical / cross-scene notes (18 audited; erotic-register + tender-relief excluded as fresh) | **done 2026-07-20 — 46 findings (high 4, med 15, low 27); fixes applied: neuro-residue r2 (incl. follow-up `can't decode`×3 + perceive-then-avoid×2 in secret-plans/in-her-place/chronology/condensed-peaches) + currency + brace-migration + word-swap→chronology/sheri/todo. Still flagged (not applied): scrunchie-gaslight:27 no-absorber rewrite, spring-satc-bridge grid reorder, thesis Rule-N renumber (peaches/help-harm), bible:380 "Ignition-Scalding" title-form, chronology:525 anthro-signup context** |
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

**Flagged doctrine items — RESOLVED 2026-07-20 (one-at-a-time pass):** scrunchie-gaslight `:27` no-absorber collapse + `:9/:25` structural-effect (not conscious campaign) + "campaign" swept to thread/mechanism · spring-satc-bridge → **grid is canonical** (Agreement follows First Taste); ⇒ chronology-reorder flag raised · Rule-N citations (`peaches`, `help-harm-dials`) recited-by-concept · **"fifteen years"** (thesis:105/109 + pace:117) → number removed · `how-its-done` status (arch-randi:140 + condensed:3 → "Draft complete", verified against the scene) · `bible:380` "Ignition-Scalding" → `{{Scalding Jealousy Ignition}}` · `chronology:525` flag 26 signup → `{{All the Time}}` · **enmity** (cassie-randi:30 + cassie:96) → asymmetric (Cassie dislikes / Randi dismisses; root stays off-page) · `pace:75` "twenty-year-old" → "twenty-one-year-old" (+ recorded: the three age across the year — Pace 22→23, Vee/Randi 21→22) · **aspiration/envy** (bible:224) → revised: envy is Randi's alone; Vee *aspires* to Randi's charmed-life/composure (the cage), never envies.

**Still open (minor / author to apply):** the spring-satc-bridge **chronology reorder** (move the Threesome Agreement to *after* First Taste on the date-master) · `arch-sheri` title-marking (`{{The Usual}}`/`{{Another Round}}`) + Sheri's uncorroborated age (~20) · `cassie:46` scene-map lag (add the stats-Simpson/`{{Turned Up}}` Cassandra pairing) · `threesome-reveal:11` betrayal framing (no-action per audit) · deferred prose passes (`see-you-later.md` Chi Latte cover; `meta-craft-randi.md:187` Fairytale render vs the drafted NYE page).

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
_status: checked 2026-07-19 — 4 findings (high 1, med 1, low 2) · ✓ RESOLVED 2026-07-20: :27 → no-absorber collapse; :9/:25 conscious-strategy → structural-effect ("nobody plans this"); "campaign" swept to thread/mechanism (:3,:37); :11 gender-framed left as-is_
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

---

## Phase 4 — Topical / cross-scene notes
_(`meta-note-erotic-register.md` + `meta-note-tender-relief.md` excluded — created fresh this session, current.)_

### meta-note-first-love.md
_status: checked 2026-07-20 — 1 finding (low 1)_
- **[low/med]** `:12` — "a *different* blindness: he **can't decode** a bid routed through a proxy": "can't" is incapacity/innate-deficit-coded (the framing the reground removes); the doc elsewhere uses "misses/never decodes" and explicitly defers to bible/pace. **Correct:** `bible:178` "a *habituated* non-reading, not an innate deficit… trained, not innate". **Fix:** if touched, "can't decode" → "doesn't decode"/"misses". Currency: clean.

### meta-note-taste-thread.md
_status: checked 2026-07-20 — 3 findings (med 2, low 1)_
- **[med/high]** `:103` — defers "(Full design: `meta-condensed-the-peaches.md`.)": dead pointer (article-drop). **Correct:** on-disk `meta-condensed-peaches.md`. **Fix:** → `meta-condensed-peaches.md`. [chronology:422 shares this broken link — sweep]
- **[med/med]** `:3,43` — {{First Taste}} at "(~late spring)"; the dated chronology entry says ~early July (`chronology:418-419`), though `chronology:331` still says "late spring" (chronology self-split). **Fix:** reconcile → "~June/early July"; align `chronology:331`.
- **[low/high]** `:38` — Lip-Lick gracenote "(~Nov 1)"; host {{We Find Out}} re-dated to Fri Nov 6 (`chronology:482`). **Fix:** "~Nov 1" → "~Nov 6" (or drop the pin).
- Doctrine/neuro: clean.

### meta-note-threesome-reveal.md (climax master)
_status: checked 2026-07-20 — 5 findings (med 2, low 3)_
- **[med/high]** `:19` — {{First Taste}} "(~late spring)" → chronology says ~early July (`chronology:417`, slot TBD). **Fix:** → "~early July [slot TBD]".
- **[med/high]** `:35` — cabin "Placement: after the friends dinner and after bondage/clamps have run": "after clamps" is stale — Nipple Clamps restructured into Secret Plans (~late March/April), now AFTER cabin (`chronology:357`). **Fix:** drop "/clamps".
- **[med/high]** `:185` — "he never had the equipment to know": stale innate-deficit; contradicts neurotypical canon. **Correct:** `meta-arch-pace.md:101,107` "not a missing capacity… He chose the available adaptation." **Fix:** → habit/aim register ("he'd trained himself not to look"). [innate-deficit residue class]
- **[low/med]** `:184` — "he lacked the equipment to see it": same; defensible as consent-apparatus-had-no-slot but reads as innate lack. **Fix:** tighten to habit/aim.
- **[low/med]** `:11` — three-way "betrayal" framing extends thesis (thesis reserves "betrayal" for Pace harm-two). Doc owns the climax; flag so it's not cited as thesis-verbatim.
- Internal/summer/chronology agreement: coherent; cabin placement self-flagged as open-Q #5.

### meta-note-first-weekend-back.md
_status: checked 2026-07-20 — 2 findings (low 2)_
- **[low/high]** `:21,37` — "Secret Plans" bare vs braced siblings; no chapter is titled bare "Secret Plans" (cluster = "Secret Plans — The Princess"). **Fix:** → `{{Secret Plans — The Princess}}` (incremental).
- **[low/med]** `:42` — "collapses to precise/formal under stress" frames the register-shift as passive; the stress-tell is canonical but should read as the **defended habit tightening** (active). **Correct:** `bible:178`. **Fix:** "collapses" → "tightens/pulls into" if edited. [innate-deficit-residue class, mild]
- Peter/porch-name regression + neuro: clean.

### meta-note-scar-reveal.md
_status: checked 2026-07-20 — 0 findings (clean)_ — all dates/claims reconcile (Rock ~late Oct, The Scar ~April, first love ~late summer); bike-drag origin matches bible:147; neuro clean (flatness = burial/suppression, not deficit).

### meta-note-peaches.md
_status: checked 2026-07-20 — 5 findings (high 1, med 3, low 1) · ✓ 2026-07-20: :29/:31 non-perception reframe (Phase-4 batch); Rule-N citations recited-by-concept (:35/39 no-native-armor, :46/56 never-surface; `help-harm-dials:245` deception-transcendence)_
- **[high/med]** `:29,31` — frames Pace as perceiving the coded apology-bid and "**defers emotional integration**/steps around it" from discomfort → **contradicts** the coded-channel mechanic (he never perceives the cipher; answers the surface literally). Motivated-avoidance would make him a knowing manipulator. **Correct:** `bible:178` "never hears the cipher… never registers there's a cipher under it." **Fix:** reframe from motivated-deferral to non-perception of the encoded layer (keep the deed-as-later-apology; the deficit-denial at the note is already correct). [innate-deficit-residue's inverse — over-correcting into knowing-avoidance]
- **[med/high]** `:64` — "the **late-August** threesome reveal" → reveal is ~early August (`chronology:433-434`). **Fix:** → early-August.
- **[med/med]** `:35,39` — "Rule-5" miscited (current thesis Rule 5 = "grievance and gift are the same object"; the intended point is body-before-mind/no-native-armor). **Fix:** cite by concept or correct number. [thesis rule-renumber class — cf. help-harm-dials:245]
- **[med/med]** `:46,56` — "Rule 3" miscited (current Rule 3 = "no coercion beats"; the never-surface principle is Rule 15). **Fix:** recite by concept / renumber.
- **[low/low]** `:33` — "canned-peach thing" conflates the fresh/grilled-peach refusal with the separate canned-peaches class-misread (`bible:137` vs `:317`). **Fix:** clarify if kept.

### meta-note-on-top.md
_status: checked 2026-07-20 — 1 finding (low 1)_
- **[low/high]** `:53,55,66,162,168` — cross-refs `Restrained`/`Vee on the Bench`/`On Top` backticked-bare, not double-brace-marked (self-ref `On Top` stays bare). **Fix:** migrate cross-refs (incremental). Doctrine/agency/neuro: clean.

### meta-note-desirability-thread.md
_status: checked 2026-07-20 — 1 finding (low 1)_
- **[low/high]** `:7` — quotes Randi's eyes as "built her **whole** adult life around being looked at for"; source (`meta-craft-randi.md`) has no "whole". **Fix:** drop "whole" or unquote. Dates/doctrine/neuro: clean.

### meta-note-music-thread.md
_status: checked 2026-07-20 — 2 findings (low 2)_
- **[low/high]** `:39,43` — "Ignition-Scalding" bare/hyphenated vs braced siblings; canonical `{{Ignition Scalding}}` (`chronology:409` "Scalding Jealousy Ignition"). **Fix:** brace. (slug `ignition-scalding.md` at :21 is fine.)
- **[low/med]** `:45` — "~mid-Nov SATC brunch"; {{All the Time}} is "~mid-to-late November" (`chronology:180`). **Fix:** align. Music beats/neuro: clean.

### meta-note-forbidden-kiss.md
_status: checked 2026-07-20 — 1 finding (low 1)_
- **[low/med]** `:44,46-48` — states placement/downstream but omits the *committed* motivation (Vee tells Pace she kissed Randi at the mixer → motivates the coated kiss + gives "I'm not gay" its referent). **Correct:** `meta-note-taste-thread.md:47`; `chronology:271`. **Fix:** add a one-line motivation cross-ref (open-Q #26). Kiss-logic/neuro: clean (in lane).

### meta-note-anthro.md
_status: checked 2026-07-20 — 2 findings (low 2)_
- **[low/high]** `:28,30` — `All the Time`/`Among Friends` bare/backticked, not double-brace-marked. **Fix:** brace cross-refs (leave file-slugs).
- **[low/med]** `:30` — signup "plants in All the Time" is the CURRENT side; `chronology:525` flag 26 still says "plants in Gesso" (stale straggler). **Fix:** flag `chronology:525` (out of scope here). Major/neuro: clean (anthro = elective, not Vee's major).

### meta-note-spring-satc-bridge.md
_status: checked 2026-07-20 — 2 findings (med 1, low 1) · ✓ RESOLVED 2026-07-20 (author call): **GRID IS CANONICAL** — Agreement follows Vee's First Taste / self-taste threshold; the grid + `:85` note stand. ⇒ **NEW chronology-reorder flag (author to apply on the date-master, not done here):** `chronology:405` places The Threesome — Agreement (~early-mid June) BEFORE First Taste (~early July); per the grid the Agreement must move to **after** First Taste — reconsider the intervening Scalding / bench-retell / Vol 2-3 break stretch that currently sits between them._
- **[med/high]** `:62-73,85-86` — revised spring grid orders the **Bench retell** + {{First Taste}} BEFORE the **Threesome Agreement**; chronology orders Agreement (~early-mid June) BEFORE bench-retell (~late June) and First Taste (~early July). Grid predates the Vol2/Vol3 restructure. **Correct:** `chronology:405-406,413-418`. **Fix:** reconcile grid rows 7-10 (Agreement first); First-Taste half is itself slot-TBD. [likely supersession]
- **[low/med]** `:70` — row pairs {{Vee on the Bench}} (Pace) with the Bench-retell (SATC) as adjacent; chronology splits them across the Vol2/Vol3 curtain (the gap "loads the scald"). **Fix:** annotate the row. Neuro: clean.

### meta-note-another-round.md
_status: checked 2026-07-20 — 2 findings (low 2)_
- **[low/high]** `:15` — `` `The Usual` `` backticked, not `{{The Usual}}` (same class as arch-sheri:200). **Fix:** brace (incremental).
- **[low/low]** `:55` — placement omits the {{Among Friends}} co-anchor (`chronology:242`). **Fix:** optional add. Doctrine/neuro/Sheri: clean (patent-to-empty-room = current canon, not autistic).

### meta-note-the-found-hair.md
_status: checked 2026-07-20 — 3 findings (high 1, med 1, low 1)_
- **[high/high]** `:22,42` — "the last trace before the **early-May** threesome": the reveal moved to **~early August** (`chronology:434,7`). **Fix:** "early-May" → "early-August" (both lines); late-April placement holds.
- **[med/high]** `:19-22` — grain #3 rendered as **no-absorber collapse** = CURRENT (matches `chronology:474`), but **conflicts with its owning doc** `scrunchie-gaslight:27` (still "cover holds / credits Pace"). **Fix:** found-hair is correct; update `scrunchie-gaslight:27` (confirms the Phase-3 high finding). Do NOT change found-hair.
- **[low/low]** `:9` — "the dress-cluster doc" unnamed → `meta-plan-dress-cluster.md`. **Fix:** optional. Neuro: clean.

### meta-note-secret-plans.md
_status: checked 2026-07-20 — 3 findings (med 1, low 2)_
- **[med/high]** `:124` — cites `meta-plan-summary.md` twice (deleted); the "deliberately left … nipple clamps" content survives only in the bible. **Correct:** `meta-arch-bible.md:70`. **Fix:** drop the summary.md mentions; retarget to `meta-arch-bible.md:70`. [summary.md straggler beyond bible/pace-house]
- **[low/high]** `:118` — Randi→Pace joke "~April, slot TBD (flag 16)" contradicts the doc's own :83-84 (rehomed into `in-her-place.md`, Draft complete). **Fix:** → "rehomed into `in-her-place.md` (~April), no longer standalone".
- **[low/med]** `:71-76,86` — link-4 frames Randi's line as the "secret plans" phrase; drafted line is "I have secrets of my own" (`in-her-place.md:123`). **Fix:** flag only (within tolerance). Stats-mirror/clamp-sensation/neuro: clean.

### meta-note-vee-reads-randi.md
_status: checked 2026-07-20 — 2 findings (low 2)_
- **[low/med]** `:25` — "faintly unsettling" is the nearest the note gets to the barred **wary** register (aspiration-only for Vee-reads-Randi). In-bounds (unease attaches to the *phenomenon of control*, not Randi-as-person) but slidable. **Correct:** `meta-craft-randi.md:49`. **Fix:** anchor the aspiration guard or trim.
- **[low/med]** `:27` — "before the warmth takes over" (cold-appraisal-at-first-encounter) is superseded by `:31` (post-warmth close-study) and conflicts with See You Later canon (Vee taken instantly). **Fix:** reconcile :27 to :31. (Note: the mutual-envy framing at `:29` verified **live canon**, not stale.)

### meta-note-the-pointing-game-pace-misread.md
_status: checked 2026-07-20 — 4 findings (high 1, med 2, low 1)_ — **PROTECTED note; highest innate-deficit residue**
- **[high/high]** `:25` — "peak present-moment perception, **no access to** what a present moment becomes": "no access" = missing-capacity framing. **Correct:** `meta-arch-pace.md:101` "not a missing capacity… could run it if a problem demanded… not a missing organ"; `bible:163/178`. **Fix:** → "the after-reading that **does not run**…" (operation never triggers, not a missing faculty).
- **[med/med]** `:25` — "the same **faculty**" reifies as innate wiring. **Correct:** `meta-craft-pace.md:159` "the same **condition**"; `:56` "his competence is the blindness." **Fix:** → "same condition — his real-time competence leaves the after-reading nothing to run on."
- **[med/med]** `:19,23,25,33` — the misread characterized only as constitutional "signature failure/his specific blindness," no practiced/habituated framing → a protected note could be read as endorsing innate framing. **Correct:** `bible:143` "practicing, not failing to perceive"; `meta-arch-pace.md:97,105`. **Fix:** add a clause anchoring it as a *habituated non-reading*.
- **[low/high]** `:3,25,27` — stale scene line-anchors (the-pointing-game.md drifted: 117→125, 121-125→129-133, 67-69→79/129). **Fix:** update or make approximate.

### meta-note-among-friends.md
_status: checked 2026-07-20 — 4 findings (high 1, med 3)_ — **neuro word-swapped but mechanics unswept**
- **[high/high]** `:9` — "given in **the only grammar he has** — deed, not word": frames the deed-channel as innate limitation, but `meta-arch-pace.md:135` marks "the only grammar he has" as **Pace's own rationalization/blind spot**, not author-frame. **Fix:** reframe as choice-become-habit OR attribute to Pace's belief (free-indirect).
- **[med/high]** `:9` — "his **sensory overload** misread as rejection": retired clinical term. **Correct:** `meta-note-the-usual.md:5-7` "drained not disabled." **Fix:** → the loud room defeating him.
- **[med/high]** `:42` — "a loud room **breaks his apparatus**" / "the Chili's **overload**": mechanical-circuit framing. **Fix:** → the room defeats him (keep "passes in short structured doses at a cost" — current canon).
- **[med/med]** `chronology:239,:197` — still say "**neurodivergence**" (the word-swap didn't reach chronology/condensed briefs). **Fix:** extend the neuro word-swap to chronology + condensed. [neuro-residue class]

---

### Phase 4 — emergent patterns (feed follow-up sweeps)
1. **Neuro-residue (round 2)** — the word-swap/reground didn't fully propagate: innate-deficit/"apparatus/overload/no-access/only-grammar/can't/never-had-the-equipment" phrasing survives in `first-love:12`, `threesome-reveal:184-185`, `pointing-game-misread:25`, `among-friends:9/42`, `first-weekend-back:42`; `peaches:29` over-corrected the other way (perceives-then-avoids). Plus `chronology:239/197` + condensed briefs still say "neurodivergence." → a round-2 sweep to habituated-non-reading + extend the word-swap.
2. **Reveal-date drift** — "late spring / early-May / late-August" for the threesome → **~early August** (`chronology:434`): `found-hair:22/42`, `threesome-reveal:19`, `peaches:64`.
3. **Backtick→brace title migration** (incremental, low) — `on-top`, `music-thread`, `anthro`, `another-round`, `first-weekend-back`.
4. **Thesis "Rule N" renumber** — bare rule-number citations stale: `peaches:35/46`, `help-harm-dials:245`. → cite by concept.
5. **scrunchie-gaslight:27** no-absorber rewrite confirmed by `found-hair`.
6. **summary.md straggler** — `secret-plans:124` (beyond the bible/pace-house already fixed).
7. **`meta-condensed-the-peaches.md` dead pointer** — `taste-thread:103` + `chronology:422`.

---

## Phase 5 — Per-scene notes (drafted scenes)
_Currency + light prose cross-check vs the drafted scene. Wave 1 (12): all-the-time, barely-stings, burn, fairytale, fed, grace, in-her-place, in-his-hands, leave-no-trace, my-friend-randi, old-acquaintances, outlier. Wave 2 (12): practice-room, recognized-method, rock, see-you-later, sheri-first-ride, still-life, the-bench, the-usual, turned-up, vee-on-the-bench, water-wings, we-find-out._

**✓ Wave-1 mechanical fixes applied 2026-07-20:** stale-status (my-friend-randi/old-acquaintances/leave-no-trace/grace) · misquotes→drafted line (all-the-time/fed/fairytale) · factual (old-acquaintances borrowed-off-dorm + near-real-time + gorgeous; all-the-time Wardy; barely-stings Sondra/indifferent; burn Cabin→{{Grace}}) · date (grace First Taste→early July) · braces ({{The Outlier}}/{{The Bench}}/{{A Round}}/{{What to Wear}}) · **inverted "gorgeous" doctrine reframed** (old-acquaintances — gorgeous is the true line, not withheld) · cross-doc stragglers (`satc-tracks:71` bullshit-look→named-catch; `chronology:331` ask-quote). Editorial reconciliations flagged (not applied). Wave-2 fixes still to apply.
**Note (author):** canonical title is **"The Outlier"** (`{{The Outlier}}`), not "Outlier" — the article is required or the brace won't resolve. `satc-tracks:145` has a second general-register "bullshit look" left as-is (not the {{Fed}} rung).

### meta-note-my-friend-randi.md — 4 (high 1, med 1, low 2)
- **[high/high]** `:3` — status "Architecture complete, **prose not drafted**": the scene IS drafted. **Correct:** `chronology:224` "Draft complete · `my-friend-randi.md`". **Fix:** → "draft complete".
- **[med/med]** `:15` — omits a whole drafted **second movement**: Randi retells the John/skiing {{Fairytale}} story, surface-only ("everywhere but the bedroom…", `my-friend-randi.md:95-119`). **Fix:** add a bullet covering the reciprocal Fairytale-retelling.
- **[low]** `:41` — the prescriptive "worked example" double-register lines aren't the shipped lines (`my-friend-randi.md:51`); flag only.
- Currency/doctrine: clean (friend-lane clean — "confidante", never "listener"; no neuro residue).

### meta-note-fairytale.md — 3 (med 1, low 2)
- **[med/med]** `:43` — "{{Gesso}} **mid-November** mention (Randi off-grid) load-bearing setup": phantom + mis-dated — Gesso is now **~late Jan** and no off-grid/Gstaad mention exists anywhere (rg-confirmed). **Fix:** re-home the intended mid-Nov setup, or downgrade to "needed setup (unwritten)".
- **[low]** `:32` — beat-9 quote "A performance she could do in her sleep / operating the equipment" isn't on the page; drafted = "good sandwich eaten fast" (`fairytale.md:117`). **Fix:** update quote or drop quotes.
- **[low]** `:13,15,41` — bare title refs (`Outlier`×2, `Bench`). **Fix:** brace (incremental).

### meta-note-all-the-time.md — 2 (med 1, low 1)
- **[med/med]** `:21` — Cassie peeled off by "locked pre-nursing track can't fit elective"; the drafted scene uses "already did hers, with oddball Wardy" (`all-the-time.md:129`; `chronology:180` carries both). **Fix:** add the already-completed/Wardy mechanism.
- **[low/high]** `:17` — quote "you only gave him half of you?" → drafted "you only gave him *half?*" (`:111`). **Fix.**

### meta-note-barely-stings.md — 4 (low 4)
- **[low/high]** `:83` — esthetician "[name]" now canon **Sondra** (`barely-stings.md:31`; `chronology:254`). **Fix:** placeholder → Sondra.
- **[low/med]** `:28` — tech "goes serious — reads as **severe**"; prose renders **indifferent/level** (`:39`, matches the note's own engine). **Fix:** "severe" → indifferent.
- **[low/med]** `:39` — restrained-arousal "what will she see?" worry placed in the labia-strips finish; prose lands it earlier (`:61`). **Fix:** flag beat-placement.
- **[low/med]** `:59` — "all the best dressmakers start on the left side" cited as a Randi anchor but appears in no drafted scene. **Fix:** flag (illustrative gloss, not citable).

### meta-note-burn.md — 1 (low 1)
- **[low/low]** `:69,72` — refers to the next scene as both `{{Grace}}` and bare "Cabin" (the cabin is *inside* Grace, `chronology:329`). **Fix:** normalize to "{{Grace}} (the cabin trip)". Prose fidelity otherwise excellent.

### meta-note-outlier.md — 1 (low 1)
- **[low/low]** `:18` — MIRH "auto-truncated (an LLC has no ticker)" vs prose "four letters, her own shorthand" (`outlier.md:55`). **Fix:** flag — soften mechanism. Fall placement + economics major confirmed; clean otherwise.

### meta-note-in-his-hands.md — 0 (clean)
_Every quoted anchor matches the drafted scene; the precise/formal stress-tell is current neurotypical canon._

### meta-note-in-her-place.md — 5 (med 2, low 3) — **note predates the final draft**
- **[med/high]** `:21-53` — the scene walk-through/conversion-map name no physical menu, but the **drafted spine is now nipple clamps + spanking** (`in-her-place.md:37-77`; `chronology:366` — the clamp-thread payoff). **Fix:** add clamps/spanking to the scene + conversion sections.
- **[med/high]** `:24,52` — claims the "*she always locked it… stopped noticing that he noticed*" deadbolt line relocates here surfacing *after* the reveal; drafted bolt is at `:9` *before*, as delight ("He grinned"), no snag. **Fix:** reconcile the KEEP/relocation + "faint early tremor" (`:19`) to as-drafted.
- **[low]** `:25,80` — "hand on the green during comparison-fishing"; drafted green-contact is toenails at orgasm (`:97`). **Fix:** reconcile.
- **[low]** `:31` — aftercare "blanket, smoothing her hair"; drafted is "hands flat and slow on her back" (`:105`). **Fix:** adjust.
- **[low]** `:69` — stale VERIFY item ("stride breaking" callback) absent from draft → retire. Neuro (`:33`) already fixed; clean.

### meta-note-fed.md — 4 (med 3, low 1)
- **[med]** `:44,46` — quotes Randi's "…live vicariously through you" as "keep verbatim, the sharpest double-register line"; drafted dropped it → "Give me something to live on… I'm running on fumes" (`fed.md:15,25`). **Fix:** stale line-anchor — update or restore.
- **[med]** `:50` — attributes to `toenails.md` "lifted out… clean as you lift a stitch"; drafted is "clean as… a ladle takes soup" (`toenails.md:21`). **Fix:** correct misquote.
- **[med]** `:62` — the note/scene use the **named-catch** device (replacing the "bullshit look"), but the sibling **`satc-tracks:71` still says "the bullshit look"** → cross-doc supersession; note is current. **Fix:** reconcile `satc-tracks` rung-#4 to named-catch. [new finding on satc-tracks]
- **[low]** `:64` — a labeled "candidate" catch line not realized verbatim; mechanism preserved — informational. Neuro: clean.

### meta-note-old-acquaintances.md — 6 (high 2, med 3, low 1) — **pre-draft note; doctrine inverted**
- **[high/high]** `:55,103,114` — the "*gorgeous* rule" is **inverted**: note says *gorgeous* is *withheld* when Randi's lying (reaching for "*angel*, not *gorgeous*"); the draft **spends** *gorgeous* as "the one true line she means" (`fairytale.md:143`; `old-acquaintances.md:31`). **Fix:** reframe — *gorgeous* is the truth breaking through the false gloss, not withheld.
- **[high/high]** `:66` — tuned exchange ends "miss your face most though 💋" (no *gorgeous*) as a withheld-word tell; draft spends *gorgeous*. **Fix:** add *gorgeous*, retire the angel-not-gorgeous framing.
- **[med]** `:3` — status "Vignette · **Unwritten**"; drafted (`chronology:212`). **Fix:** → Drafted. [stale-status class]
- **[med]** `:42` — photo "borrowed from **Randi** (both seducers on her body)"; canon is **dorm** (`old-acquaintances.md:19`; `lesson.md:19`). **Fix:** → dorm; the "both seducers" reading is false.
- **[med]** `:57,64,68,103` — a "**twelve-hour delay**" ("Randi can't be reached"); draft is near-real-time (Randi replies same night, `:27,29`). **Fix:** retire the delay.
- **[low]** `:92` — stale "Fairytale in progress on a separate branch / sync at merge"; Fairytale is merged + already word-identical. **Fix:** drop branch/merge language.

### meta-note-leave-no-trace.md — 8 (high 1, med 4, low 3) — **pre-draft note; scene drafted+reviewed**
- **[high]** `:3,76` — "The scene is **unwritten**"; drafted + reviewed 2026-07-15 (`chronology:74`). **Fix:** → companion to drafted scene. [stale-status class]
- **[med]** `:39` — silk-naming "must ride the walking, on the move"; drafted as a **seated summit** beat (`leave-no-trace.md:121-137`; flag 11). **Fix:** walking → seated summit.
- **[med]** `:33` — care-food "sliced fruit"; drafted is **cherries** + the two cutting-voice defusion installs (blister; leave-nothing) the note omits (`:47-67`,`:107-117`). **Fix:** → cherries; add the defusion beats.
- **[med]** `:18,39,65` — names the shade "**poured wine**"; resolved canon is **russet/brick-red** only (wine is Pace's Fitting variant) (flag 11; `:127`). **Fix:** → russet/brick-red.
- **[med]** `:65` — Fitting payoff "he **matches her coloring**"; superseded — he **offers** a variant, Vee consents (flag 11; condensed). **Fix:** → offers-a-variant.
- **[low]** `:9` — reading-order omits `{{What to Wear}}` between Rye and Two Towels. **Fix:** insert.
- **[low]** `:35,64` — "no-tag **hiking shirt**"; drafted is a **gym-bag flannel** (`:169`). **Fix:** → gym-bag flannel.
- **[low]** `:75` — "(To be drafted.)" but already on-page (`:11`). **Fix:** drop.

### meta-note-grace.md — 12 (med 5, low 7) — **pre-draft note; scene drafted**
- **[med]** `:3` — status "Scene · **Unwritten**" + forward-tense throughout; drafted (`chronology:330`). **Fix:** → Drafted. [stale-status class]
- **[med]** `:140` — "daylight-blazon / plum / key-line **note-only, not yet threaded**"; all three are on the page (`grace.md:99,105,95`). **Fix:** remove the TODO.
- **[med]** `:38` — opening-integration blocked pre-blazon; draft relocates it to a **cheval-mirror** set-piece ("Look at you… Tell me what you see", `grace.md:117-139`), unrecorded. **Fix:** update to the mirror-mediated version.
- **[med]** `:49,136` — {{First Taste}} "~late spring" → **~early July** (`chronology:331`). **Fix.**
- **[med]** `:32,53` — "the Fitting / anti-Fitting" chapter cross-ref → `{{A Round}}` (the measure-and-withdraw beat). **Fix:** brace.
- **[low×7]** `:73,117` "another adventure" → "an adventure" (`grace.md:113`) · `:140` blindfold-propagation already done · `:66` key-guard already satisfied · `:71` shower-order compression (non-conflict) · `:15` a mirror facial-tell the note said to CUT is on the page (`grace.md:123`) — **flag: reveal-arming vs telegraph?** · `:11` "the only register he has / **can't answer in words**" is innate-deficit-adjacent — flag: frame as chosen grammar/vow, not incapacity · **`chronology:331` "ask" quote** ("Would you show me how you touch yourself?") is stale vs the drafted/note "Go ahead… Show me" — flag chronology straggler (note is current).

**Phase-5 pattern (emerging): pre-draft notes never reconciled to their drafted scenes** — stale "unwritten/prose-not-drafted" status (`my-friend-randi:3`, `old-acquaintances:3`, `leave-no-trace:3`, `recognized-method:3`, `grace:3`) + superseded directives/quotes. A batch of these want a reconcile-to-the-drafted-scene pass, not just currency.

_Two more Phase-5 themes: (a) **neuro-residue the reground didn't reach** in per-scene docs (`recognized-method:15` "the never-named temperament", `sheri-first-ride:28` "deficit", scene `rock.md:117` "too literal") — a residue-tail sweep wanted. (b) **scene-side prose staleness** (we don't edit prose — author flags): `still-life.md:3` "week before the break"/harvest frame (should read late-Jan), `see-you-later.md:33` "Monday-morning stats" (breaks the Wed timing)._

### meta-note-see-you-later.md — 2 (med 1, low 1)
- **[med]** `:21-26` — Plants list **omits the Chi Latte venue-exclusion** (just-recanonized: Greek-coded ground; this scene is its *first enactment* — Cassie's lab-decline = opting off, not merely a Cassandra beat). **Fix:** add venue-exclusion (reread-only, taste-on-first-pass) to the seeds; reframe Cassie's decline.
- **[low]** scene-side `see-you-later.md:33` "Monday-morning stats" contradicts the Wed timing — prose flag.

### meta-note-turned-up.md — 1 (med 1)
- **[med]** `:3` — braced **self-title** `{{Turned Up}}` (the self-title sweep missed this file). **Fix:** → bare `Turned Up` (the `{{A Round}}` cross-refs stay braced).

### meta-note-recognized-method.md — 5 (med 3, low 2)
- **[med]** `:3` — "companion to the **unwritten scene** … **unrendered** craft"; drafted (`chronology:144`). **Fix:** → companion to `recognized-method.md`.
- **[med]** `:32` — "wet hand … cold on sleep-skin" tickle; drafted is **dry** tickle (`:91`), the **wet** hand is the swat (`:101`), warm not cold. **Fix:** dry-tickle / wet-swat.
- **[med]** `:15` — "(the never-named **temperament**)" glosses his non-comprehension as innate. **Fix:** reframe to choice-become-habit / plain info-gap (he didn't witness the blonde). [neuro residue]
- **[low]** `:37` — "inverting **the Fitting**" → `{{A Round}}` / lowercase event.
- **[low]** `:31` — "Soaking, Pace" → drafted "Soaking," (name dropped, `:89`).

### meta-note-rock.md — 2 (med 1, low 1)
- **[med]** `:76` — placement "after {{Shoe Shopping}} (Oct 19), before {{School Nights}} (Oct 23)" is stale. **Correct:** `chronology:124` Shoe Shopping ~Oct 24; Rock's next entry is `{{Lesson}}` ~Oct 29. **Fix:** → "after {{Shoe Shopping}} (~Oct 24), before {{Lesson}} (~Oct 29)".
- **[low]** scene-side `rock.md:117` "too literal not to first check" — innate-literal residue; prose flag.

### meta-note-still-life.md — 5 (med 2, low 1)
- **[med]** `:56` — the note's own guard "no harvest-table tie (late Jan now)" is contradicted by the **draft**: `still-life.md:3` "the week before the break, the markets piled high." **Scene is the stale side** (note+chronology = late Jan). **Fix:** prose flag — strip the pre-break/harvest frame from `still-life.md:3`.
- **[med]** `:19,49,56` — blanket "No peach here" is broader than canon; `chronology:259` carves out "counter peaches are texture only" (the draft's brandied peaches are allowed). **Fix:** add the carve-out to the note guard.
- **[low]** `:17,34-48` — photo/sex/afterglow beats absent from the *partial* draft — consistent (note documents intended-unwritten), no drift.

### meta-note-sheri-first-ride.md — 3 (med 2, low 1)
- **[med]** `:10` — "Oct 26 morning slot" stale (Oct 26 = Monday, breaks the Thu-blowup/Sat framing). **Correct:** `chronology:140` ~Sat Oct 31. **Fix:** → Oct 31.
- **[med]** `:28` — "Pace's **deficit** is missing meaning encoded…" — substance current, but "deficit" is retired wiring language. **Fix:** → "habituated non-reading/trained blind spot". [neuro residue]
- **[low]** `:9,43` — `` `Another Round` `` backtick → `{{Another Round}}`.

### meta-note-the-bench.md — 3 (med 2, low 1)
- **[med]** `:23,39` — "Edging Improvements / Planned / In Progress" sections present material that is **already landed** in the completed draft as pending. **Fix:** relabel shipped/locked.
- **[med]** `:5` — "last name unknown to her own sorority sisters" cited as *Randi's* withheld name; in the draft it's **Pace's** last name (relationship-concealment, `the-bench.md:509`). **Fix:** recast or drop from the withheld-her-name parallel.
- **[low]** `:36` — quote "the way the muscle inside pulled…"; draft drops "the way" (`:357`).

### meta-note-the-usual.md — 4 (low 4)
- **[low]** `:25` — `` `Another Round` `` backtick → `{{Another Round}}` (×2).
- **[low]** `:20` — "you don't get clever at a graveside" isn't a scene line (drafted "nothing clever he could lay over it", `:45`) — unquote/gloss.
- **[low]** `:37` — "a Christmas neither of them was driving home for" not verbatim — note-coinage.
- **[low]** `:38` — "the philosophy of my food" → drafted "philosophy of your food" (`:115`).
- _Doctrine clean; retired counter/no-eye-contact rationale correctly marked retired._

### meta-note-practice-room.md — 5 (high 1, med 1, low 3)
- **[high]** `:3` — "the **unwritten scene**"; drafted (`chronology:148`). **Fix:** → the drafted scene.
- **[med]** `:18,56` — drafted opener/close "Okay. The shoes. Tell me everything." / "All better?" **supersede** the old "Your turn" / "I hope everything is alright" — but that's **not propagated** to `satc-tracks` (rung 1) + `chronology:149`. **Fix:** propagate the new lines. [cross-doc straggler]
- **[low]** `:55` — "latch" → drafted "bolt" (`:121`).
- **[low]** `:11` — continuous-vs-discrete "reserved March" → April/spring (Secret Plans, TBD).
- **[low]** `:11` — "outlier" keyword resonance with `{{The Outlier}}` — author glance (likely deliberate). Neuro clean.

### meta-note-water-wings.md — 5 (high 1, med 3, low 1)
- **[high]** `:3` — "Architecture complete, **prose not drafted**"; drafted (`chronology:58`). **Fix:** → Draft complete.
- **[med]** `:31,51` — beat-2 content "stripper's body / hidden since fourteen / sleek like Randi" and the "stripper's-body self-label **early appearance here**" are **not in this scene** — relocated (`a-round.md:26` self-label; full form `nothing-underneath.md`). **Fix:** reconcile the note to what Water Wings actually renders; re-anchor the thread's early appearance to `{{A Round}}`.
- **[med]** `:32` — the note's Cassie-seal→Kayla NB is **current**, but `chronology:59` + `meta-condensed-water-wings.md` still say "Cassie pops it" → external drift. **Fix:** flag chronology:59 + condensed (note is right). [cross-doc straggler]
- **[low]** `:7,50` — "the Fitting" (chapter-sense) → `{{A Round}}`.

### meta-note-we-find-out.md — 3 (med 1, low 2)
- **[med]** `:13` — wikilink `[[meta-condensed-practice-room]]` for the brat plant; it lives in `[[meta-note-practice-room]]`. **Fix:** repoint.
- **[low]** `:21` — "*shame wants a witness, and there was none*" is a paraphrase-in-quotes (draft `:95` is longer). **Fix:** unquote/align.
- **[low]** `:29` — "chase banter deliberately thin, to be built out" but the scene is Draft complete. **Fix:** reconcile/retire.

### meta-note-vee-on-the-bench.md — 6 (med 1, low 5)
- **[med]** `:79` — "remembers her the way you **remember a person still in the room**": object-permanence/present-cognition figure reads neuro-adjacent under "introvert-charismatic, not autistic." **Fix:** flag — author decide reword to a vividness image. [neuro residue]
- **[low×5]** `:143` bare "Ignition"/"Peaches" → brace · `:30-46` omits the drafted cold-open (Thursday wanting + tell-first rule) · `:34` box "on the table from arrival" vs drafted produced-later (`:33`) · `:141` "both asleep" vs drafted only-Vee (`:491`) · `:13` paraphrase-in-quotes.

---

**Phase 5 done — 24 notes, ~94 findings (high ~6, med ~40, low ~48).** Dominant patterns (for the wrap): (1) **pre-draft notes lag their drafted scenes** — stale "unwritten" status + superseded directives/quotes; (2) **neuro-residue tail** the reground didn't reach (`recognized-method:15`, `sheri-first-ride:28`, `vee-on-the-bench:79`; scene `rock.md:117`); (3) **scene-side prose staleness** (author flags, no prose edits here): `still-life.md:3`, `see-you-later.md:33`, `rock.md:117`; (4) **cross-doc stragglers where the note/scene is current but siblings lag**: `satc-tracks:71` (bullshit-look), `satc-tracks`+`chronology:149` (Your-turn/I-hope-everything-is-alright), `chronology:59`+`condensed-water-wings` (Cassie-seal→Kayla), `chronology:331` (ask quote); (5) misquotes/paraphrases-in-quotes + backtick/self-title brace nits.

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
