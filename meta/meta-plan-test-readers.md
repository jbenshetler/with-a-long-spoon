# Test-reader plan — Volume 1

*Recorded 2026-08-15. The human whole-book beta read, distinct from the LLM
cold-read panel (`reviews/`) and the completed editorial passes
(`meta-plan-editorial-checklist.md`). Owns the screener, recruit copy, channel
layers, and question set. Distribution context: `meta-plan-distribution.md` §5;
funnel-vs-recruitment boundary: `meta-plan-free-sample.md`.*

## Why a human read now, and what it's for

The book is written, structurally edited, continuity-checked, and line-edited;
the LLM panel (per-scene) and the author's context-retaining LLM readers have
already delivered the line-level and broad-craft signal (e.g. "Pace reads too
manipulative in the first three chapters"). **So the editorial value of test
readers is largely spent — do not run this pass to hunt typos, continuity, or
prose fixes.** Its job is the layer the pipeline structurally *cannot* produce:

1. **Felt emotional arc** — where the warmth curdles, whether the closed/costly
   ending devastates or thuds, the migration from Cassie to Vee as *lived* rather
   than per-scene (thesis-owned; do not restate here).
2. **Arousal** — does the erotica work *as* erotica. An LLM cannot report this;
   humans are the only instrument for it, and it's non-negotiable for the genre.
3. **Reader-implication** — complicit / seen vs. watching from arm's length (the
   con-misread failure the packaging fights, `meta-plan-distribution.md` §4).
4. **Drop-off behavior** — where a real reader skims, stalls, or would DNF.
   Humans quit; LLMs read every word. Behavior beats self-assessment.
5. **Target-market fit** — does the graduating spicy-romance reader respond as
   designed, or misfile it as dark romance / feel betrayed by the ending.
6. **Social proof** — seeds early reviews and the quotable "the writing, though"
   the ARC-to-creator BookTok model runs on. Not QA; a launch asset.

## Channel layers (recruit → collect → deliver)

The anonymous serialization funnels (Literotica/AO3) **cannot** supply
identifiable, contactable readers — they convert strangers into list
subscribers, nothing more (`meta-plan-free-sample.md`). So the test-reader
pipeline is its own infrastructure, on the adult-friendly platforms already
endorsed in distribution §5:

- **Recruit** → **BookSprout / BookSirens** — erotica-open reviewer
  marketplaces; readers self-select in *because* they read the category (the
  first screen, for free). BookSprout is net-new to the plan; BookSirens is the
  other erotica-open review channel named in the ALLi market commentary.
- **Collect** → **StoryOrigin Beta Copies** — upload once, invite a team, gather
  **chapter-by-chapter** feedback in one dashboard. This is the surface the
  question set below is built for (per-chapter behavioral prompts + a whole-book
  exit set).
- **Deliver** → **BookFunnel** — for the firewalled, unpublished manuscript:
  per-reader email watermark ("Scarlet Letter"-style) and **Restricted** delivery
  (read only in-app/cloud, no EPUB/PDF handed over). Use if StoryOrigin's own
  delivery isn't locked down enough for an unpublished book.

**Before spending money:** confirm each platform's current mature-content /
adult-tier ToS directly — all three are used for erotica *in practice* but none
published an explicit blessing when checked (2026-08-15); they may age-gate or
tier rather than ban.

## Recruit cohort — size and shape

- **~8–15 finishers, not 50 sign-ups.** Over-recruit ~2–3× (betas evaporate),
  stagger start dates so you're not blocked on the whole cohort.
- **Deliberately seed 1–2 critical/lukewarm readers** — volunteer betas skew
  enthusiastic; you need someone predisposed to be picky, or a genre reader
  *tired* of the tropes, to find the friction the fans forgive.
- **Firewall discipline:** recruit and correspond only through the pen-name
  domain email (`helen@helenriversbooks.com`), never a personal address, never a
  personal network (breaks the firewall *or* yields non-target friends).

## Intake screener (pass/fail — run before sending the manuscript)

Purpose: qualify for genre literacy and ending-tolerance, so "wrong reader"
noise is separated from real signal *before* the read, not after.

1. **What have you read and loved in the last year?** (Want names in the spicy /
   dark / literary-erotica band — a reader who can say "hotter than X, more
   interior than Y." No comps → can't give comparative signal → pass over.)
2. **How do you feel about a book that does *not* end happily-ever-after?**
   The single most important screen for this book. A reader who *needs* the HEA
   contract will punish the closed ending and report it as a flaw. **Recruit
   mostly readers open to a costly/closed ending, plus 1–2 self-identified
   HEA-loyalists, labeled as such** — so you can separate "this reader was never
   going to like the ending" from "the ending doesn't land."
3. **Are you comfortable with fully explicit content?** (Screens out the reader
   who'll flinch and give noise instead of arousal signal.)
4. **When you don't like a book, do you finish it or put it down?** (The
   DNF-honest reader gives you the drop-off behavior you actually need.)
5. **Can you finish ~[length] within [window], and answer a short set of
   questions as you go?** (Commitment + the aggregation contract.)

## Recruit blurb — Helen Rivers voice (first-person)

*For BookSprout/BookSirens listings and direct outreach. Honest about what it is
so the wrong reader self-deselects; carries the "outgrown the tropes but won't
give up the heat" self-selection.*

> I'm looking for a small team of early readers for **A Polite Invitation**, the
> first book of my debut trilogy — literary erotica for people who want the heat
> and the depth in the same book. It's fully explicit, it's about grown people
> making beautiful mistakes with their eyes open, and it does **not** hand you a
> tidy happily-ever-after — the feeling is taken as seriously as the sex, and it
> costs somebody something. If you've outgrown the tropes but you're not ready to
> give up the heat, this was written for you.
>
> What I need: read the whole book, answer a short set of questions as you go
> (nothing onerous — mostly *where did this land, where did you drift*), and keep
> the manuscript to yourself — it's unpublished. What you get: the book before
> anyone else, and a real hand in shaping the final version.
>
> Not for you if you need the guaranteed happy ending, or if fully explicit isn't
> your thing. No hard feelings — I'd rather match the right readers than the most.

## Question set — behavioral-first

Design rule, from the craft canon (**do not telegraph**): the priming questions
below would bias the read if handed over up front, so **split delivery** —
per-chapter *behavioral* prompts travel *with* the manuscript (they don't
prime); the *interpretive/emotional* prompts are revealed **after** each relevant
stretch or at the end. Favor **behavioral** over opinion: humans mis-narrate
their own experience ("pacing was fine" while their drop-off point says
otherwise), so ask what they *did*, not only what they thought.

### Per-chapter (upfront, behavioral — non-priming)
- Did you stop reading mid-chapter? If so, where, and why (bored / interrupted /
  needed to sit with it)?
- Anywhere you skimmed or skipped ahead? Mark it.
- If you weren't obligated to finish, is this a chapter you'd have quit at? Y/N +
  where.

### Whole-book exit set (post-read — interpretive)
- **Arousal (be blunt — it's erotica):** where did the heat *work*? Anywhere it
  went clinical or you checked out of it?
- **Implication:** reading it, were you *in* it — recognizing something of your
  own wanting — or watching from outside? Did that change across the book, and
  where?
- **Character read:** did you ever file any character as a villain or a predator?
  If so, who, and at what point — and did that reading ever change? (Silent on
  names/answers by design; this is the con-misread probe.)
- **Emotional arc:** where, if anywhere, did the warmth turn? Did the ending feel
  *earned* or like a cheat? Closest you can get to how it left you.
- **Drop-off, honestly:** the single place you were most likely to abandon it.
- **Retention / market:** would you read Book 2? Who — a specific friend — would
  you hand this to, and what would you say it is?

**Synthesis:** aggregate across readers on the fixed items (StoryOrigin's
dashboard makes per-chapter responses line up). A lone reaction is noise; a
*cluster* at one chapter — a shared drop-off, a shared "went clinical," a shared
villain-misread — is the signal to act on. Treat a lone HEA-loyalist's ending
complaint against the screen (expected; not a defect) before weighing it.
