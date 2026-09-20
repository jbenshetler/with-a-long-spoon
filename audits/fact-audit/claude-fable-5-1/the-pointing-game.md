# Fact audit — The Pointing Game

*model: claude-fable-5-1 · ch003 · 2026-09-20 · prose-sha ~1096cd31694e*

---

# Fact audit — Chapter 3, *The Pointing Game*

## FINDINGS

### 1. A candidate who is never on the page — "the closed camel-coat project" (within-chapter)

**WHERE**
> "…laughing at something with her whole body the way the polished girls and the matched pairs and the closed camel-coat project would never laugh at anything in public…"

**AGAINST** — the complete roster of women Pace points at in this chapter, none of whom wears a camel coat:
> "Leggings and an oversized quarter-zip in the Greek pastel, a canvas tote with a water bottle clipped to it, box-fresh white trainers…" (ponytail girl)
> "…both in the matched athleisure that read like a uniform — high-waisted, cropped, one in lavender and one in a sage…" (the pair)
> "…round wire glasses… a green knit beanie though it wasn't cold…" (library steps)
> "…a blazer and a white-blond blowout in loose curls…" (the one who ran the room)

And the chapter's own recap of the field a few lines earlier lists only three types: *"Not the expected, not the matched pairs, not the ones who ran the room."*

**WHY** The sentence refers back to a specific observed woman ("*the* closed camel-coat project") as though the reader has met her; no woman in a camel coat appears anywhere in the chapter (confirmed by `rg` — the only "camel" in this file is this line). This is the signature of an edit that re-dressed or removed a candidate and left one back-reference standing.

**CONFIDENCE** HIGH.

---

### 2. Time of day of the collision — Ch3 vs. Ch4 (cross-chapter, not in ledger)

**WHERE** (Ch3)
> "The path delivered them, eventually, to the broad doors of the dining cafeteria, where the four-o'clock current thickened…"
> (and, on the library stretch just before) "…the two of them easy in the four-o'clock sun…"

**AGAINST** (Ch4, `scenes/see-you-later.md:11`)
> "She'd been coming out of the dining hall with Meg from her floor… when a girl walked into her. … The girl was simply better than the morning around her: better lit, better put together…"

**WHY** Ch3 fixes the dining-hall collision at four in the afternoon; Ch4, recounting the same collision, places it in "the morning around her." Time of day is a checkable fact, not a date. (If "the morning" is meant as a loose figure for the day, both hold — hence not HIGH.)

**CONFIDENCE** MEDIUM.

---

### 3. Randi's sorority tenure — Ch3 vs. Ch22 (ledger C1)

**WHERE**
> "A decade of dance and three years of whatever sorority actually taught under the mixers and the letters…"

**AGAINST** (ledger §6, C1, quoting Ch22)
> "a sorority habit, four years of never being the one they waited on"

**WHY** Three completed years and four are not the same count; already ledgered as C1. A reading exists (Ch3 counts completed years; Ch22 counts the current senior year as the fourth), and Randi at 21 fits either.

**CONFIDENCE** MEDIUM. Reported only because this chapter supplies one side of the ledgered conflict.

---

## NOTED (not errors)

- **"Tuesday-afternoon current"** — weekday; out of scope, not examined.
- **"Four weeks in she'd learned he did things"** — no ledger fact fixes the relationship's length; the walnut bench of Ch1 having been built inside that window is a plausibility question, not a fact conflict.
- **"The bar with the older couples dancing"** as one of their prior outings — consistent with ledger ("Randi has danced with Pace [3, 47]"). It adds a third data point to ledger C9 (bartender: "he don't bring dates, as a rule" [26]), but "as a rule" tolerates exceptions and C9 is already logged as AMBIG; nothing new.
- **Vee's outfit** ("soft drapey thing in no particular color, a denim jacket… soft boots") vs. ledger cardigan-over-the-better-shirt [4] and tan cap-toe boots [27] — Ch4's cardigan is explicitly "this morning" (the next day, `see-you-later.md:107`); different days, different resolution. Not a conflict.
- **Vee "walking with another girl"** — ledger: Meg with Vee at the collision [4]. Consistent.
- **Randi's black hair, sleek tail, single scrunchie** — matches ledger. Randi's scrunchie is a separate object from Vee's green-dotted form [32, 35, 41]; not the same thing.
- **Vee's hair "loose to the shoulder blades," copper in sun; snub nose; cinnamon freckles across nose and cheeks** — matches [3, 21, 27, 32]; "curly" elsewhere is compatible with "loose."
- **Randi "reached for hers too"** (clothes, in bed) then later "had showered and put her face back on and dressed" — sequence is compatible (gathered clothes, then showered, then dressed). Not a contradiction.
- **Pace "had not wiped his face since the bed"** an hour-plus and a drive later — plausibility, not fact.
- **"Her name is Vee. And we've got a stats class together"** — Randi not having noticed Vee in a shared tiered lecture before is plausible; ledger [4] confirms the shared class. Consistent.
- **Pace watching from the light pole; Vee never registers him** — ledger [4] "Vee believes the collision was chance," [15] Vee believes Pace walked past Randi without looking. Nothing here contradicts; Vee never sees him.
- **"He had danced with her, felt the trained instrument of her under his hand"** — consistent with ledger [47] (Randi knows Pace's lead style).
- **Season cues** (summer-green grass, first cold nights, one maple turned) — season-level only; not checked further.
- **Randi refusing the cheeseburger / "Let's go feed you"** — consistent with the diet register of [1, 47]; no fact asserted.
- **"He gave her two more along that stretch"** — library-steps girl and the blazer girl = two. Internally consistent.
