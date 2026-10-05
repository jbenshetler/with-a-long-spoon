# Cross-chapter echo triage — designed vs. accidental

Work queue for **returning phrases, gestures and images across chapters**, and the
record of what has been ruled. Within-chapter repetition is a different instrument
(`tools/echo_harvest.py`); the closed-vocabulary style linter (`style/style-rules.toml`,
echo-rulings #59/#60/#63) is a third. This doc covers only the **cross-chapter** layer,
which neither of those can see.

**Source of the list.** The `line-editor` persona's whole-volume read —
`reviews/capture-panel/claude-fable-5-1/line-editor--volume.md`, **ACROSS THE VOLUME**
section, first run 2026-09-30. Regenerate with
`tools/capture_panel.py --volume --models <m> --personas line-editor --force`; contract
in `reviews/capture-panel/SPEC.md`. **That record covers Book A only (ch1–27). Book B
(ch28–55) has never had a whole-volume line-editor pass** — the cross-chapter returns in
the second half are entirely unexamined. The existing record is also stale by the seam
rule (twelve chapters changed in the 2026-10-03/04 tell pass), so re-run it rather than
patching it.

**A regex sweep is not a substitute for the persona.** The tell pass below was run with
`rg` after the line-editor had already named the finding, and the sweep *still* missed two
instances — `fed.md:65` ("turned her flute on the cloth," no hand word) and
`how-its-done.md:80` ("her thumb had found the base of her water glass and was working
the edge of it," no "turn" + vessel adjacency). Both were in the persona's record. Use the
persona to find the category, then `rg` to enumerate it, then read each instance in
context.

---

## Method (worked example: the glass tell, 2026-10-03/04)

1. **Find the category** — a whole-volume `line-editor` read names the bleed.
2. **Enumerate with `rg`**, several patterns, not one: the gesture's verbs *and* its
   objects *and* the body parts, separately. Expect to miss some; cross-check against the
   persona's own list.
3. **Read every hit in context** and classify by **POV** and by **trigger**, not by
   phrasing.
4. **Assign per character**, then vary the wording instance by instance — the gesture
   recurs, the sentence must not.
5. **The author rules every assignment.** Flag, never fix: this is characterization, and
   a repeat is as likely to be designed as accidental.
6. Record the ruling in the owning craft doc, then lint + `orphan_refs.py`.

---

## Ruled

- **The glass fidget is Randi's alone** (author rulings 2026-10-03/04). Two distinct
  gestures: the **nail-press** (jealousy or insecurity, particularly about Vee enjoying
  being truly seen) and **turning the glass** (the separate, lesser charge — e.g.
  arousal). Never Vee's, never Pace's. Full contract and instance ledger in
  `meta-craft-randi.md`, The Cup. Vee's tells moved into her own body:
  `meta-craft-vivienne.md`, Behavioral Signatures.
- **`space.md:61` / `tannin.md:55` — accidental** (author ruling 2026-10-03). Six shared
  elements, ch30 repeating ch7; `space.md:61` recast.
- **Repeated staging and venue is the intended structure** (author ruling 2026-09-28) —
  characters returning to the same rooms to eat, have sex, or talk about it is not a
  finding, and persona complaints about it were an artifact of persona tuning, since
  reverted. Do not re-raise.

## Pending — bleeds between characters

The action queue: a phrase or gesture established as one character's that later appears in
another's hands. Each needs a designed/accidental ruling. Chapter numbers are Book A
reader sequence.

- **"There you are"** — Pace's, ch1 ("There you are, Randi.") → Randi's entrance to Vee's
  row, ch4 ("*There* you are.").
- **Kneeling to take a woman's shoe off and hold her foot** — Pace's, ch1 and ch12 →
  Randi, ch25 ("lifted Vee's foot onto her knee and slipped the flat off"), down to the
  "Mm" over the nail.
- **"She's not ready … on her own"** — Pace's, ch23 → handed straight back by Randi, ch26.
- **"coming in late, on purpose"** — Vee's private daydream, ch24 → spoken to her as
  advice by Randi, ch25.
- **Wearing his cloth to his table after** — Vee's, ch20 (the top sheet) → Randi, ch26
  (his undershirt); Pace imagines both of them there at once.
- **"handed the evening to him"** — Randi's, ch1 and ch3 → Vee, ch9 ("the relief of
  handing the choice across the table"). The line-editor calls this "the book's one verb
  for consent."
- **"Mm."** — Cassie's, ch5 → Randi ch11/ch22/ch25, Pace ch12/ch17. The whole cast has one
  noise for withholding.
- **The name-bit** — Randi's, ch4 ("Yes, like the adjective. No, it's not a coincidence.")
  → tried on by Vee, ch5. Possibly designed (Vee borrowing Randi's move).
- **"The wanting got there before the plan did."** — Vee's, ch19 → ch25; and ch4's "felt
  the *yes* arrive … fully formed, ahead of everything" and ch3's Randi "the bare arrival
  of a thing already true before she got to it" are the same shape on both women.
- **"Hi," she said. "Hi," he said.** — the doorway exchange, Randi and Pace ch1, word for
  word for Vee at ch9, ch16, ch20.
- **Vee rising onto her toes** — ch17 → ch24, ch25. Within one character, but check the
  third instance.

## Pending — two instances the tell pass left for ruling

- **`fed.md:65`** — Vee: *"I wanted it," she said, and turned her flute on the cloth. "And
  I took it. For once."* Her last glass fidget. My reading is that the occasion is
  mother-judgment (she has just claimed her own appetite out loud, the exact ground the
  *floozie* voice patrols), so **hand to collarbone**; it is not obviously arousal or
  insecurity. Unruled.
- **`substitution.md:67`, `:149`, `:173`** — Randi's hand to the coffee cup at the
  engineered meet-cute, three times in one chapter: holding it, bringing it up twice with
  no sip, the other hand in her lap, Vee registering "the small busy-ness" and supplying
  "she's bored." The trigger is canonical (`meta-arch-bible.md:237` names the meet-cute as
  a recurrence site) and the misreading is the payload, but none of the three is rendered
  as a press. Open question: does one of them become an explicit press, since this is
  where the reader first learns the gesture, or does the deniable register do the work
  better here?

## Designed, for reference — do not re-raise without cause

The line-editor also catalogued the book's **intra-character** returns. These are the
seeded threads and belong to the Bible's *Running threads to seed* registry
(`meta-arch-bible.md:396`) and the arch docs; they are listed here only so a future pass
does not mistake them for findings: Randi locking the door behind her (ch1, 7, 14, 23);
Randi's *"Tell me"* (ch7, 14, 23 by absence, 26); *"Love you, girl"* → *"See you soon,
gorgeous"* (ch4, 11, 19, 22); Randi's hug with the hand flat between Vee's shoulder blades
(ch4, 11); Randi's goodbye kiss at the hinge of the jaw (ch19, 22); the mother's
*floozies* wearing through (ch4, 12, 17, 20, 24); Pace's *"May I"* (ch5, 9, 11, 18);
Randi's chill after (ch14, 23, 26); Pace's *"It was the want, he thought"* (ch14, 23);
Vee reading the right side of the menu first (ch19, 22); Randi's citrus-and-something-
colder perfume (ch1, 4, 7, 14, 23); the house's needle-drop (ch1, 7, 14, 23, 26); the
six-year-old-and-dinosaurs figure (ch11, 16); the cardigan over the better shirt (ch4, 11,
26); Cassie's window cracked its two inches (ch10, 13, 21); Pace soothing a small hurt with
his palm and kissing it (ch1, 17); *hers* as Pace's ethic in a possessive (ch1, 7, 23, 26);
*"She had never in her life been so happy"* → *"She had never been so fortunate, or so
happy"* (ch21, 27, deliberate); *like a lamp* (ch11, 25, 26); the small bowl he slices her
apples into (ch1, 23); *cocoa-brown* (ch1, 14); *a decade of dance* (ch1, 3); clothes
*like an apology* (ch11, 24, 25); *and she let it* (ch11, 15, 19, 24); blue toenails
against frosted plum (ch1, 26 / ch20, 22, 25); *Daphne* (ch1, 27).
