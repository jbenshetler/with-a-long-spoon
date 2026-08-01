# Cover design — Volume 1

*Owns everything on and about the cover object — concept, art, text hierarchy, production specs. `meta-blurb.md` owns the words (jacket/ad copy, positioning, the volume-title decision and its rationale); this doc owns how the cover renders them. Status: concept settled, details in prototype. Decisions marked; open questions at the bottom. The SVG master feeds the epub build pipeline (rasterize once at export — see Production).*

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

## Sleep mask vs. flower (leaning mask; A/B with test readers)

- **Mask** = what is *done to* Vee; names her as the object of the design; required for the balancing-on-the-blindfold statement; the cohort's home iconography (genre-legible). **Keep unless the A/B says otherwise.**
- **Flower** = what Vee *is* (Art Nouveau, unmolded, the only living thing among two manufactured objects — the thesis from another angle). Costs the blindfold-in-the-geometry; signals romance more than erotica.
- If the mask rendering reads "spa eye-pillow": fix in drafting (tie at the back, slight sheen), not by replacement.
- **A/B protocol:** two bottom circles, same everything else, ask cold: *"what does this book promise?"* Expected: mask wins genre-promise, flower wins prettiness — want the first.

---

## Background (open; prototype all four, judge at 100px in a row)

Excluded: **green** (jealousy/money to a browsing stranger — and the green-sheets claiming can't be known from outside), **white/gray** (flat, lifeless), **oxblood/wine** (sumptuous but destroys the red circle's singularity — rule out deliberately when suggested).

Ranked candidates — all are one `<filter>` swap in the same SVG master:

1. **Blue-black Perlin + lamplight vignette** (current ground + faint warm radial glow behind the triangle). Canon atmosphere (the bench scenes are lamplit); lifts the dark circles off the ground without changing their fills — solves the thumbnail-mush structurally; heat held inside a cold frame.
2. **Woodgrain in warm black** — the cover surface becomes, sub-threshold, *the bench*: the material everything rests on. Same discipline as the cage: at the almost-isn't level; consciously-"wood" says craftsman/cabin. Procedural: `feTurbulence` + `feDisplacementMap` over fine stripes.
3. **Aubergine / deep plum** — erotic-luxe middle; gold-on-aubergine is classic luxury. Keep near black-with-a-bruise; saturated purple drifts to paranormal-romance shelf grammar.
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

## Open questions

1. Mask vs. flower — A/B with the Volume 1 test readers.
2. Background — pick from the four prototypes at thumbnail size.
3. Title typography — untouched so far; decides the whole register. (What the text *says* and its hierarchy are decided — see Cover text — this question is purely typeface/treatment.)
4. ~~Whether the cover carries the tagline~~ — **decided 2026-07-30: no** (see Cover text).
