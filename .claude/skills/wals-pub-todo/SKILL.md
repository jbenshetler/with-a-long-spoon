---
name: wals-pub-todo
description: >-
  Generate the current list of remaining steps to get from where the book is
  now to fully published — manuscript, packaging, legal, the human beta round,
  wide release, and launch. Probes the repo for live state rather than reading
  a stored checklist, so the answer reflects today's prose, today's reviews,
  and today's git history. Use whenever the author asks what's left, what's
  blocking publication, what still has to happen before test/ARC readers, or
  for a publication status report. Reports only — never edits prose, never
  records a decision.
---

# wals-pub-todo — what's left to fully published

**This skill generates a report. It does not change the book.** No prose edits,
no `reviewed:` dates, no ticking checkboxes, no recording rulings. If the run
surfaces a decision the author then makes, writing it into `meta/` is a
separate, explicitly-authorized step.

## The one rule that makes this skill worth running

**Do not answer from the checklist.** `meta-plan-editorial-checklist.md` and
`meta-plan-editorial-status-vol1.md` are hand-maintained and go stale the
moment prose lands — a row can read `[x]` while the thing it certifies was
invalidated three commits ago. The value here is **probing ground truth and
reconciling it against what the docs claim**, then reporting the divergence.
Per the Prime Rule, every factual claim in the output traces to a probe result
or a quoted doc line, never to memory or to an earlier turn in the session.

Where a doc and a probe disagree, **report both and name the conflict** — do
not silently pick one. That is an authorial call.

## Scope argument

- *(no arg)* or `vol1` — Volume One, the lane that actually leads to publication. **Default.**
- `vol2` — Volume Two's parallel state (still drafting; expect most gates unstarted).
- `all` — both, plus series-wide items.
- `brief` — top blockers only, no phase detail. Combinable: `vol1 brief`.

## Step 1 — run the probe suite

Run these in parallel batches. They are cheap, read-only, and none require
network beyond the DNS check. **Never run a probe that spends paid API tokens**
(no cold-read or capture-panel *runs* — this skill only reads their artifacts).

```bash
# Inventory + build integrity
git status --short
tools/build_epub.py --list                      # Vol 1 roster; flags missing prose
tools/build_epub.py --volume TWO --list         # Vol 2, only when scope includes it
tools/lint_titles.py --all
ls -l images/cover.png                          # cover symlink target (images/ is gitignored)

# Per-chapter review coverage (author-recorded only — never invent a date)
rg -n '◆ VOLUME' meta/meta-plan-chronology.md   # volume band line numbers, to scope the next probe
rg -n 'slug: ' meta/meta-plan-chronology.md | rg -v 'reviewed:'
#   Then DISCARD the [EVENT] rows. Calendar landmarks (halloween, thanksgiving-break,
#   christmas-break …) carry no `reviewed:` by design — pills show on SCENE/VIGNETTE only.
#   What's left is the real gap.

# Doc-claimed status
rg -n '^\- \[ \]' meta/meta-plan-editorial-checklist.md
rg -n 'unstarted|in-process' meta/meta-plan-editorial-status-vol1.md

# Cover open questions — MUST be section-scoped; a bare '^[0-9]+\.' match pulls in
# every numbered list in the file. Items wrapped in ~~strikethrough~~ are decided.
rg -n -A12 '^## Open questions' meta/meta-cover.md

# Cover ASSET, not just the spec — the symlink can point at a render that predates
# the current decisions. Compare its target + mtime against meta-cover.md's build state.
ls -l images/cover.png
```

> **Shell-snippet hazard:** this file is a skill body, and a `$0` / `$1` in a
> bash snippet can be clobbered by argument substitution at invocation time
> (an `awk '{print $0}'` here silently became `awk '{print vol1}'`). **Write
> probes that contain no `$n` tokens** — prefer `rg` over `awk`/`sed` field
> references, and if a positional is unavoidable, put the probe in a script
> under this skill's directory and call that instead.

**Cold-read coverage** — compare the roster against `reviews/cold-read/<model>/`
for the eight-model panel in `reviews/cold-read/ensemble-config.toml` (that file
is the authoritative roster; don't hardcode model names here). Expect the four
subscription-lane models at or near full coverage and the OpenRouter models
thin — thin coverage on a paid lane is *not* a blocker, it's a cost decision.

Two filters, or the numbers are nonsense: **iterate directories only**
(`reviews/cold-read/` also holds `README.md`, `SPEC.md`, `principals.toml`,
`oracle-runs/` …, each of which will otherwise report as a model "missing"
all 52 chapters), and **drop the retired voters** — `claude-sonnet-5` and
`gpt-5.6-terra` are off the panel per `CLAUDE.md`, so their gaps are expected,
not findings.

**Capture-panel staleness** — do **not** reach for git dates here. Every gate
record stamps the `prose-sha` of the chapter it actually read, and the harness
verifies it for you:

```bash
tools/capture_dag.py --models claude-fable-5 claude-opus-4-8 gpt-5.5 gpt-5.6-sol --check-stale
```

`--check-stale` prints the report and **returns before any model call** — it
spends nothing, so it is safe to run every time. It names the changed chapters
and tiers the exposure:

- **direct** — the gate's own chapter changed; re-read only if the edit was substantive.
- **window** — the changed chapter sat in that gate's raw prose window.
- **checkpoint** — it only fed the carry-forward; usually ignorable for a style edit.

Gates minted before sha-tracking report as *unverifiable*, not stale.

**Report staleness as a warning, never as a blocker.** That is the harness's
own ruling, in comments at the call site: *"Staleness is a warning, never a
gate. A style edit to an early chapter must not force a re-read of every
downstream chapter."* A newly-drafted chapter that no gate has ever covered is
the one case worth raising on its own, and even then it is a `DECIDE`, not an
`OPEN` blocker.

Two structural notes that have misled a previous pass: the per-model `dag/`
directories hold hundreds of `gate-ch*.md` records **two levels down**
(`dag/<persona>/gate-chNNN.md`) — a `maxdepth 2` file count reports them as
empty. And `reviews/capture-panel/horizon-book-two-current-raw/` is a separate
Book Two run; exclude it from Volume One reasoning.

**Pen-name infrastructure** — registration is what makes the pen name final and
unblocks firewall-disciplined recruiting:

```bash
for d in helenriversbooks.com readhelenrivers.com; do dig +short NS $d; dig +short MX $d; done
```

MX records present = mail provisioned, not merely reserved. A domain resolving
on Cloudflare does **not** mean it's the author's — check `meta-plan-pen-name.md`
for which domains were ever recorded as third-party.

## Step 2 — read the owning docs

Fan out **parallel `lore-keeper` subagents**, one focused question each, rather
than pulling these into the main context. Each doc owns its subject:

| Domain | Owner |
|---|---|
| Editorial passes, definitions | `meta-plan-editorial-checklist.md` |
| Vol 1 per-pass status | `meta-plan-editorial-status-vol1.md` |
| Human beta round (recruit/collect/deliver, screener, question set) | `meta-plan-test-readers.md` |
| Packaging spec, jacket copy, epub metadata description | `meta-blurb.md` |
| Cover — build state and open questions | `meta-cover.md` |
| Pen name, domains, firewall | `meta-plan-pen-name.md` |
| Legal findings, ask-the-lawyer rows | `meta-plan-legal-read.md` |
| Counsel sourcing, ALLi consult | `meta-plan-lawyer.md` |
| Lane, store strategy, metadata discipline, wide-release next steps | `meta-plan-distribution.md` (§6 = open items) |
| Funnel, serialization, free-sample cutoff | `meta-plan-free-sample.md` |
| Creator seeding, ARC-to-creator, clips | `meta-plan-booktok.md` (§10 = open items) |
| Live prose-side TODOs | `meta-todo-open-questions.md`, `meta-todo-doc-updates.md` |
| Scene inventory, order, continuity flags | `meta-plan-chronology.md` |

**Later sections supersede earlier ones inside the same file.** `meta-blurb.md`
in particular carries stale early lines that a later decided section overrides.
Reconcile before reporting, and flag the lineage.

## Step 3 — classify

Sort every open item into one phase, and mark **what it blocks**, not just that
it's open. An item is only a *blocker* for a phase if that phase cannot start
without it.

1. **Manuscript** — drafted, per-scene reviewed, six editorial passes (developmental, continuity/logic audit, style-tic, true line edit, copyedit, timeline sweep).
2. **Packaging** — cover, jacket/blurb copy, epub assembly, typeset proofread.
3. **Legal & platform risk** — content read, ask-the-lawyer rows, platform ToS posture.
4. **Beta / test-reader round** — pen-name infra, platform accounts, screener, delivery, synthesis structure.
5. **Wide release** — retailer/aggregator setup, categories & keywords, metadata discipline, price, wide-release front/back matter, content warning.
6. **Launch & acquisition** — free sample/funnel, mailing-list CTA, creator seeding, ARC-to-creator.

### Classification traps — each of these has burned a previous pass

- **Test-epub ≠ wide-release packaging.** Dedication, acknowledgments, author bio, series page, and the mailing-list CTA are *deliberately absent* from the test epub. Reporting them as beta blockers is wrong; they belong to phase 5.
- **Volume 2/3 items are not Volume 1 blockers.** Several open items are explicitly parked as "not in the beta package." Exclude them from the Vol 1 lane and say why.
- **`reviewed:` is author-recorded.** A chapter with no date is genuinely unreviewed *or* untracked — report the gap, never infer or invent a date. Recently-drafted chapters are the usual cause.
- **Style-linter hits are never publication blockers.** `na.py style` over-flags by design and most rules police overuse. Do not run it as a gate and do not put its counts in the report.
- **Reviews are reactions, not canon.** Cold reads and capture reads never establish a fact about the book; they establish that a reader reacted. Don't promote one to a required fix.
- **A closed legal row can still have a publication-time tail.** "Closed for beta, re-run at publication" is a phase-5 item, not an open phase-3 blocker.
- **Cross-phase coupling is the useful output.** Call it out explicitly when closing one item makes another load-bearing — e.g. a recruit channel whose acceptance criteria require a finished cover pulls the cover from phase 2 into the beta critical path.

## Step 4 — report

Group by phase, in order. Under each, one line per item:

```
[STATUS] item — one clause on what's actually left · blocks: <phase/step> · src: <file:line or probe>
```

`STATUS` is one of `DONE` · `OPEN` · `STALE` (done once, invalidated since) ·
`DECIDE` (waiting on an authorial call, not on work) · `DEFERRED` (real, but
scheduled for a later phase).

Then close with:

- **Critical path** — the shortest ordered sequence to the next milestone, respecting the couplings found in step 3.
- **Waiting on the author** — every `DECIDE`, collected, since these are the only items that cannot be worked around.
- **Conflicts found** — any doc-vs-probe or doc-vs-doc divergence, with both sides quoted. Never resolve one silently.

Keep it scannable. The author reads this to decide what to do next, not to
audit the corpus — push evidence into the `src:` field rather than the prose.

### Optional snapshot

If the author asks to keep the output, write it to `build/pub-todo.md`
(`build/` is gitignored). **Never write it into `meta/`** — a generated
snapshot competing with the hand-maintained status docs is exactly the
staleness this skill exists to defeat.
