# Capture/retention panel — SPEC (v1)

*Committed 2026-09-07. Measures **capture and retention** across the free-sample
stretch: persona-conditioned blind readers take the first four chapters
(`the-bench`, `standards`, `the-pointing-game`, `see-you-later`) sequentially
in one sitting, with a hard STOP/CONTINUE gate after each chapter. Purpose: find
where target readers would put the book down, before the sample goes public
(`meta-plan-free-sample.md`).*

## Instrument

Each read = one persona × one model × one arm, on the clean lanes (same
isolation as the authorship audit; `tools/capture_panel.py`). The reader gets
the core reader frame (`prompts/core.md`) + a persona block (`personas/*.md`)
as the ENTIRE system prompt, then [arm-dependent jacket +] the four chapters.
After each chapter: DECISION (STOP/CONTINUE), CAPTURE 0–10, ALMOST-STOPPED
(the exact moment, quoted — the actionable output even when they continue),
WHY in persona voice. A STOP ends the read (no later gates). Finishers answer
the conversion questions (would-pay at $9.99, mailing list, tell-a-friend
paragraph).

**Honesty mechanism:** models are completion-biased, so the frame weaponizes
the real economics — infinite free alternatives one click away; stopping is
the default; the book must earn each next chapter. Gradient (CAPTURE) and
ALMOST-STOPPED give signal even when outright stops are rare. Read the results
as a survival curve + ranked almost-stopped moments; single-read stops are
noise, convergent ones are findings (same convergence discipline as the
authorship audit).

## Personas (versioned in `personas/`; run header records SHA)

1. `romance-graduate` — outgrown spicy romance, won't give up the heat
   (primary vector, `meta-plan-distribution.md` §4).
2. `fsog-refugee` — wants the FSoG intensity with real consent and warmth
   (the crossover strategy, `meta-plan-pen-name.md`).
3. `consent-sensitive` — vigilant about predation-romanticizing; measures the
   **con-misread exposure** the docs flag for exactly these chapters (stays
   with dark content only if the book visibly knows what it's doing).
4. `dark-romance-control` — the WRONG reader ("wreck me with a bad man");
   should bounce. A book that captures her is failing the repel goal; her
   stops are successes.

## Arms

- `jacket` — Volume One jacket packet (`checkpoint_bundle.jacket_packet()`)
  precedes chapter one: the retail-sample funnel, with the designed
  complicated-love-not-a-con pre-framing in play.
- `cold` — chapters only: the Literotica-style funnel, no pre-framing.
  The delta between arms measures how much work the jacket actually does.

## Roster & scale

Full 8-model panel, paid lane author-authorized 2026-09-07 ("full panel
including paid"). 4 personas × 8 models × 2 arms = 64 reads. Personas are
simulations of readers, not readers — treat output as candidate signal for
authorial judgment, strongest where personas × models converge; the eventual
ground truth is the human test-reader cohort (`meta-plan-test-readers.md`).

## Run 1 results (2026-09-07 — 64 reads, full panel, both arms)

Survival (finished/8 · pay-yes · list-yes): romance-graduate jacket 8/8·8·8,
cold 8/8·8·7 · fsog-refugee jacket 8/8·8·8 (after one truncation re-run), cold
6/8·6·6 · consent-sensitive jacket 8/8·8·8, cold 8/8·7·5 · dark-romance-control
jacket 7/8·6·6, cold 5/8·3·3. **Six stops total**: 4 = control bouncing off
"safe Pace" in chs 1–2 (the filter working: "not the man I came here for");
2 = fsog-refugee **cold-arm only**, exiting chs 3–4 over Vee's uninformed /
Randi's managed consent — the premise, not the craft ("the third person's
consent is this far behind the couple's desire").

Key findings: (1) **the jacket is load-bearing for the FSoG refugee** — 8/8
with pre-framing vs 6/8 cold; the Literotica funnel should carry framing that
does the jacket's permission-work (→ `meta-plan-free-sample.md`). (2) **The
2026-09-07 pointing-game irony cue is the panel's most-cited trust line** —
"He took the body's answer for the true one. He usually did." cited by ~23
reads as the reason fsog/consent readers stayed ("a loaded gun on the wall";
"the author's thumb on the scale, marking his epistemology as a habit, not
wisdom"). (3) **Ch 2 `standards` is the universal capture dip** (9→7→9→8
book-shape; the "did not cry" stillness cluster cited ~25×) — no target
reader stopped there; monitor, don't fix. (4) **Control leak is genuine
attraction, not misread**: the 9 finishing controls stayed for Randi-as-
predator / daylight grooming ("my exact kink wearing a Sunday dress") —
a secondary audience the no-villain ending may later betray; keep them out of
targeting (already policy). Consent-sensitive persona granted trust
explicitly conditionally: the book reads as *knowing* — trust to be honored
downstream.

## Run 2 results (2026-09-07 — full-volume, two memory arms)

**Arms:** single-go perfect recall (4 models × 4 personas, `<persona>--volume.md`
+ `--volume-interview.md`) and the **capture DAG** (author-specified
cold-reader architecture: one run per chapter, reader-owned decade mints;
opus+sol × 4 personas; `dag/` trees + `--volume-dag.md` records).

- **Retention: the volume holds its target readers under realistic memory.**
  6/6 DAG target readers finished all 50 chapters; capture averages 7.3–8.9,
  DAG ≥ single-go almost everywhere. No convergent mid-book trough; the four
  scattered capture-5 gates are all **debrief/breather chapters** (What to
  Wear, Turned Up — "a debrief, not a scene"; hills-and-valleys; Made-Up) —
  convergent with the interviews' debrief-economy complaint. What re-arms a
  dipped reader is the con's continuity, never the romance.
- **The wrong-reader filter works better in the realistic instrument:** both
  DAG dark-romance controls stopped at ch 2 (vs mostly coasting to the Randi
  payoff under single-go perfect recall). Genre mismatch, not craft failure.
- **Comeuppance (interviews, tiered funnel):** 2/16 raised it unprompted at
  T1, 13/16 named it as debt at T2; Claude readers reframe at T3 ("convicted,
  not sentenced"), GPT readers stay bothered; **15/15 finishers still buy Book
  Two — as creditors**, with a universal tripwire: a second volume with Pace
  unbilled triggers loud exit and retroactive condemnation. The debt is a
  **Book Two design question, not a Vol 1 revision question**. Secondary T2
  inventory: Cassie owed an acting scene (2 readers); debrief density; more
  mass in the un-enchanted world (Kayla/Meg).
- **The mints confirm the thesis mechanism on readers:** trust-ledgers drift
  exactly as designed (tenderness trusted more *and* read as instrument;
  ck-050: "his hand reaching in place of the word now reads as the
  withholding it is"), and the FSoG reader's recurring fade — "I keep having
  to remind myself Pace and Randi are already a couple… which is, I suspect,
  exactly the trick being played on me too" — is the configuration receding
  in reader memory, i.e., the book's con working at the reader level.
- **Echo-economy flags from "what's fading"** (real production signals): the
  nude photo — "a gun on the mantel I haven't heard fire; I've half-lost
  track of it and I want to know if the book has too" — and Pace's real name
  "barely held — it hasn't mattered in chapters." Long-gap plants may want
  refresher beats; author's call.

## Pending cleanup (author, 2026-09-07 — execute AFTER the v2-rich DAG lands)

The first full-volume round is superseded: the single-go arm compressed 50
chapters of reaction into one output per reader, and the DAG v1 gates were
spec'd too terse. **After the `capture-dag-v2-rich` runs complete and are
verified:** delete `<model>/dag-v1-terse/` trees, the stale v1-assembled
`<persona>--volume-dag.md` records (re-assemble from v2), and the single-go
`<persona>--volume.md` files. **Keep:** the `--volume-interview.md` funnel
interviews (the comeuppance evidence — their findings and the run-2 numbers
above stay recorded in this SPEC even after their source records go), and the
4-chapter run-1 outputs. Do not execute before author confirmation on the day.

## Lane-blindness verification (canary probes, 2026-09-07)

Both lanes probed empirically with test-probe system prompts asking for an
exhaustive inventory of visible context. **No global `~/.codex/AGENTS.md` or
`~/.claude/CLAUDE.md` exists on this machine.** Codex lane (Sol/GPT-5.5):
clean — sandbox/tooling scaffolding only; no user identity, no project files,
no book information. Claude lane (Fable/Opus): **no project CLAUDE.md, no
memory, no repo skills, no book content** — but the CLI injects harness
scaffolding (tool/agent/global-skill lists, current date) **and the account
userEmail (`jeff.benshetler@gmail.com`)**. That email is the one boundary
leak: identity metadata, not book content, and it is a longstanding property
of the entire clean lane (same invocation as the cold-read corpus, author
ruling 2026-08-22) — documented here rather than silently accepted. Readers
receive nothing else beyond the packet the harness builds.

`reviews/capture-panel/<model-id>/<persona>--<arm>.md`. Not indexed by `na.py`
(no `## Reader reaction` section — instrument output, not a cold read).
