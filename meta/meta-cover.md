# Cover design — Volume 1

*Owns everything on and about the cover object — concept, art, text hierarchy, production specs. `meta-blurb.md` owns the words (jacket/ad copy, positioning, the volume-title decision and its rationale); this doc owns how the cover renders them. Status: concept settled; human build nearly complete (Blender triangle + all three medallions rendered, mask locked, purple/aubergine background register settled — exact variant still tuning, title type pending); build files live outside the repo — see *Production build*. Decisions marked; open questions at the bottom. The SVG master feeds the epub build pipeline (rasterize once at export — see Production).*

---

## The concept (settled)

Line-art, diagram style. An **equilateral triangle, wide side up** — inverted, balancing on its point — drawn in **thin gold lines outlined in fine black**. **Three equal circles packed inside**, each tangent to the triangle and to the other two:

- **Top left — Pace:** warm black ground, line art of a **woodworker's hand plane**.
- **Top right — Randi:** black ground, line art of a **diamond solitaire necklace**.
- **Bottom — Vee:** filled **warm red**, line art of a **sleep mask** (blindfold).

### Why the geometry works (keep these properties when iterating)

- **The stack rests on Vee's circle** — all three circles are *inside* the triangle; the red circle sits lowest, wedged into the descending point, with the two dark circles bearing down on top of it. The whole structure rests on the blindfold. The composition's best idea; nothing may cost it.
- **The red circle is the only heat on the cover.** The eye lands on Vee first. No other saturated element, ever — this rules out red-family backgrounds.
- **Three equal circles** = everyone consents, all parties equal on paper.
- **Every circle touches every other and the frame** — nothing locked, everything in contact. The configuration, honestly rendered.
- **The objects obey the title rubric translated to imagery** — innocuous going in (a tool, a jewel, an eye-pillow), detonating after (the plane shapes by removing one thin layer at a time — the staircase as a tool; the solitaire's collar-echo; the blindfold). Never trade an object for something legible-in-advance.

### The birdcage (sub-threshold, decided)

The thin gold lines quietly invoke a **gilded cage** — kept *below* the threshold where a browser would say the word "cage" (a legible cage pre-verdicts captivity and breaks earn-the-dark; the cover obeys the prose discipline — resonance, never exposition). And the book's cage **has no door**: nothing may close the form — no bar-lines between circles, no finial at the point, nothing latch-like. The gaps between circles and frame are the open doors.

**No spoon anywhere.** The proverb stays a reader's discovery; a spoon turns the cover into a rebus.

---

## Symbolic vs. photomontage (decided: symbolic)

1. **Post-FSoG, the object-on-dark-ground cover is genre grammar** for exactly this positioning — the discreet cover made the genre publicly readable; the cohort reads it as "erotica, adult, confident." Symbolic is the genre-native premium move, not a literary compromise.
2. A photomontage of three people telegraphs the threesome crassly, fixes three faces the prose deliberately leaves to the reader, and can't art-direct "warm AND ominous."
3. People-covers date; diagram covers age like the Laclos comparison they invoke.

---

## Sleep mask vs. flower (decided: mask — 2026-08-30)

**Decided: mask.** Two forces converged:

- **Craft** — **mask** = what is *done to* Vee; names her as the object of the design; required for the balancing-on-the-blindfold statement; the cohort's home iconography (genre-legible).
- **Production (the deciding constraint)** — no **flower** line art could be found or drawn that renders correctly in **constant-width gold lines consistent with the cloisonné** medallion treatment. The flower's organic, variable-width curves fight the engraved constant-line style the other two medallions (hand plane, solitaire) establish; it would not sit in the same register. The **flower**'s meaning (what Vee *is* — Art Nouveau, unmolded, the only living thing among two manufactured objects) was the pull toward it, but it costs the blindfold-in-the-geometry, signals romance over erotica, and — decisively — fails the cloisonné constant-line constraint.
- If the mask rendering ever reads "spa eye-pillow": fix in drafting (tie at the back, slight sheen — the disconnected head-band ribbons in the current render already do this), not by replacement.
- **The test-reader A/B is now confirm-not-reopen** (author was 95% before this ruling): if run at all, it asks *"what does this book promise?"* to *verify* the genre-promise read, not to relitigate mask vs. flower.

---

## Background (decided: purple/aubergine register — 2026-08-30; exact variant still tuning)

**Decided: the purple/aubergine register** (candidate 3 below). Two things settled it:
the **red-family grounds are out because red fights the red medallion** — any red
ground destroys Vee's circle as the cover's only heat (generalizes the earlier
oxblood/wine exclusion; see *Why the geometry works* — "the only heat on the cover…
rules out red-family backgrounds"); and the **other three candidates were prototyped
and failed** (blue-black Perlin, warm-black woodgrain, aged parchment — tested, none
carried it). The current build renders on plum velvet `#5A3C5F`. **Still open: the
exact purple variant** — tuning within the register, holding the option-3 guardrail
below (keep it near *black-with-a-bruise*; saturated purple drifts to
paranormal-romance shelf grammar).

Excluded (for the record): **green** (jealousy/money to a browsing stranger — and the green-sheets claiming can't be known from outside), **white/gray** (flat, lifeless), **oxblood/wine** and the **red family** (sumptuous but destroys the red circle's singularity — the deciding exclusion above).

Candidates as ranked during selection — all one `<filter>` swap in the same SVG master; **3 won, 1/2/4 tested-and-failed:**

1. **Blue-black Perlin + lamplight vignette** (current ground + faint warm radial glow behind the triangle). Canon atmosphere (the bench scenes are lamplit); lifts the dark circles off the ground without changing their fills — solves the thumbnail-mush structurally; heat held inside a cold frame.
2. **Woodgrain in warm black** — the cover surface becomes, sub-threshold, *the bench*: the material everything rests on. Same discipline as the cage: at the almost-isn't level; consciously-"wood" says craftsman/cabin. Procedural: `feTurbulence` + `feDisplacementMap` over fine stripes.
3. **Aubergine / deep plum — WINNER (decided 2026-08-30).** Erotic-luxe middle; gold-on-aubergine is classic luxury. Keep near black-with-a-bruise; saturated purple drifts to paranormal-romance shelf grammar — this guardrail governs the remaining exact-variant tuning.
4. **Aged parchment** (wildcard) — line art on paper, plate-from-an-old-book, Laclos-adjacent; red circle lands like a wax seal. Most literary, least erotica-native: wrong for the primary channel, candidate for a literary-facing variant. **The interior title-page treatment is ruled out** (tried and removed 2026-07): as a CSS background it fails reader theming (dark modes paint white text over the pale image) and pagination (partial/inconsistent renders in Calibre, bleed-over in Apple Books); as a baked image it locks the aspect ratio against variable viewports and freezes text against reader font scaling. Interior pages stay plain HTML; any title-page dressing comes from typography (an embedded title font), never from a page background.

---

## Cover text (decided 2026-07-30)

**Three text elements only** — what must survive the 100×160 render decides everything:

1. **Series line, small, at the top:** `WITH A LONG SPOON · BOOK ONE` — small caps, quiet; never the word "Series" (metadata language; reads self-published on a cover).
2. **Volume title, dominant:** *A Polite Invitation* — the element legible at thumbnail (title decision and rationale in `meta-blurb.md`, Genre & positioning).
3. **Author, bottom:** Helen Rivers — second-largest; smaller than the title while the name is unknown, grows across volumes.

**No tagline on the front** — illegible at thumbnail, and it's the blurb page's closing beat (it lives at the end of the blurb, in ads, and on a print back cover). This resolves former open question 4.

Retail title field (metadata, not art): *A Polite Invitation (With a Long Spoon, Book 1)*.

---

## Production

- **SVG is the master; raster is the deliverable.** Epub covers ship as JPEG/PNG (EPUB 3 permits SVG covers; reader support untrustworthy).
- **Ratio & sizes:** design at **1:1.6** (Amazon/KDP: 1600×2560 JPEG, <50MB — the primary deliverable); SVG viewBox in the same proportion (e.g. 1000×1600). Apple/Kobo/D2D prefer **2:3** (1600×2400) — a *re-crop*, not a rescale: keep compositional breathing room above/below the triangle so the master can give up ~7% of height untouched. Always re-render from SVG per target size; never scale a raster.
- **Thumbnail ladder** (render from master, view at actual size, in a row): 300×480 (product page) · 160×256 (search results) · **100×160 (library grid — the make-or-break render)** · 60×96 (mobile lists; only needs "distinct and not mud").
- **Grayscale test (e-ink Kindles, 16-level):** warm red and warm black can sit at similar *luminance* — if the red circle doesn't survive desaturation as a clearly lighter value, the composition loses its anchor on e-ink. Fix is value, not hue: brighten toward vermilion until the 100px grayscale render keeps Vee's circle unmistakable.
- **Perlin noise is native SVG:** `feTurbulence type="fractalNoise"` (low `baseFrequency` for slow cloudy variation; fixed `seed` for reproducibility; asymmetric x/y frequency for grain direction), tinted via `feColorMatrix`, composited over the base ground.
- **Approve the noise at export, not in the browser** — filter rendering differs between engines; the pipeline's renderer (Inkscape CLI or `resvg`; both handle `feTurbulence`) is the one whose output matters.
- **Thumbnail test at 100px:** thin gold + fine black outlines vanish in a library grid. The silhouette (triangle + three circles) and the red circle must carry the thumbnail; the objects are the full-size reward. Line weights may need to thicken for small renders. A gold skeleton with the dark circles fading may be the ghost-of-a-cage — acceptable only if chosen deliberately.
- **Watch the low-contrast pairing:** warm-black circles on any dark ground mush at thumbnail; the vignette (option 1) or rim-weight/fill-value adjustments are the levers.
- **Typography decides the register** on a diagram cover — the geometry is the image, but the title treatment says "literary" vs. "self-published." Budget care there.
- **Rasterization is a stage of the epub build pipeline** (planned — packaging spec in `meta-blurb.md`, Test-epub assembly).

---

## Production build — human-generated (nearly complete)

The AI comp (Generation prompt of record, below) is **proof-of-concept only.**
The shipping cover is built by hand:

- **Blender** — the machined-brass triangle and the three bas-relief medallions
  (the metal, the objects, the specular glint). All the 3D/metal work.
- **Illustrator** — typography and any line art.
- **Photoshop** — compositing (medallion renders + type + velvet ground into the
  final layout).

**Build state (2026-08-30): nearly complete.** Triangle + all three cloisonné
medallions (hand plane, diamond solitaire, sleep mask) are modeled and rendered on
the plum velvet ground — latest iteration `triangle-cloisonne-velvet-18.blend`,
render `render_full.png` (2026-08-27). **Remaining:** title **typography** (not yet
on the render — see Open Questions 3) and the **final composite** at target sizes.
The current render sits on plum velvet (`#5A3C5F`); the background choice itself is
still open (Open Questions 2).

**Where the build files live — deliberately outside this repo.** The Blender scenes,
renders, and working files are in **`~/clients/wals/cover/blender/`**, *not* under
this repo's version control. Rationale (author): each `.blend` / full render runs
~10 MB, so committing the iteration history would bloat the repo — and even **Git LFS
is a concern** at this size and churn. The repo keeps only the small AI PoC comps in
`images/` plus this spec; the **authoritative production source is the external
`cover/` tree**, which must be **backed up separately** — it is not protected by the
repo's git history.

Consequences:

- **AI-disclosure is now moot** — a hand-built cover needs no KDP AI-content
  disclosure, and the art regains normal copyright protection (purely
  AI-generated images get little to none).
- **Master-file note:** with the triangle and medallions now Blender renders, the
  earlier "SVG is the master" rule (Production) no longer holds as-is — the master
  is the **layered source** (Blender scene + Illustrator vector + Photoshop
  composite). Keep the type/line-art vector and re-export per target size (1:1.6
  Amazon, 2:3 Kobo/Apple); never scale the flattened raster. The thumbnail-ladder
  and grayscale/e-ink tests in Production still apply to the human render.

---

## Generation prompt of record — AI PoC only (Gemini Nano Banana 3 Pro, saved 2026-08-02)

**Proof-of-concept only — superseded by the human-generated build above.
Retained for reference; this AI comp is not the shipping cover.** The closest-yet
prompt for the AI-generated cover comps. Produced
`images/a-polite-invitation-cover-purple-3.png` (the current `images/cover.png`
PoC target). Known deviations after ~20 attempts: the generator refuses to render
the necklace as a true solitaire while retaining the small hollow separator
circles — the pendant reads as an ornate locket with a sparkle (accepted for
the test epub); a stray gold four-pointed sparkle artifact appears right of
the author name; the hand plane carries a verdigris tint. Prompt verbatim:

> A professional book cover on an edge-to-edge background of luxurious, rich plum-purple folded velvet (hex color #5A3C5F) with deep shadows and soft highlights in the fabric folds.
>
> Centrally placed in the lower-middle section is a prominent, inverted equilateral triangle emblem crafted from antique machined brass with a subtle metallic sheen. The triangle points downward.
>
> Inside the brass triangle, three main circular medallions are arranged:
>
> Top-Left Medallion: A rustic, warm brown patinated metal circle featuring a bas relief woodworkers hand plane in side profile.
>
> Top-Right Medallion: A glossy black enamel circle containing a delicate gold-line necklace with a classic round brilliant-cut diamond solitaire (not pendant) in a four-prong setting, hanging from a fine cable chain. A tiny, subtle specular light sparkle glints on the upper-right edge of the diamond. The diamond obscures part of the chain. Render the diamond in the same bas relief style on the black enamel ground, slightly antique finish of the other two medallions (the hand plane and the sleep mask). The diamond obscures the chain, it does not descent from it. This is not a pendant. The diamond does not hang below the chain. Use only the gold and black.
>
> Bottom Center Medallion: A deep crimson-red enamel circle featuring an etched gold-line silk sleep mask blindfold with the head band shown as disconnected ribbons
>
> Small, hollow circular brass frame cutouts separate the main medallions, allowing the purple velvet texture behind the emblem to show through. The artwork inside all three medallions uses a matching antique, engraved-line relief illustration style.
>
> Typography elements are rendered in elegant, raised machined brass lettering:
>
> Top Text: "WITH A LONG SPOON · BOOK ONE" in a small, quiet, spaced small-caps serif font centered near the top edge.
>
> Main Title: "A Polite Invitation" in a large, dominant, highly legible serif font centered directly above the central brass triangle.
>
> Author Name: "Helen Rivers" in a medium-sized serif font centered beneath the point of the triangle near the bottom edge.
>
> Font Description
> Use fonts Sabon Pro / Baskerville
> Material Rendering: Finished with a 3D bevel and bevel-and-emboss treatment in antique machined brass, featuring a soft top-down highlight and dark ambient occlusion shadows.
>
> No external borders, frame margins, or ragged edges. Clean, high-resolution book cover layout with a 10:16 aspect ratio.

---

## Open questions

1. ~~Mask vs. flower~~ — **decided 2026-08-30: mask** (see *Sleep mask vs. flower*; the flower failed the cloisonné constant-line constraint). Test-reader A/B, if run, is confirm-not-reopen.
2. ~~Background~~ — **decided 2026-08-30: purple/aubergine register** (red-family fights the red medallion; other candidates tested and failed — see *Background*). Only the **exact purple variant** is still being tuned.
3. Title typography — untouched so far; decides the whole register. (What the text *says* and its hierarchy are decided — see Cover text — this question is purely typeface/treatment.)
4. ~~Whether the cover carries the tagline~~ — **decided 2026-07-30: no** (see Cover text).
