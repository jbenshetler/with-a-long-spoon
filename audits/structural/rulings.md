# Structural edit — author rulings

*Rulings on findings from `tools/structural_edit.py`. The reconcile stage reads
this file. Standing standards apply to every volume; per-finding rulings name
the target and finding id.*

## Standing standards

- **Every volume satisfies and hooks** (author ruling 2026-11-19). A reader must
  be satisfied at the end of each volume, and the volume must end with a hook
  into the next one.
- **Architecture docs yield to later rulings** (author, 2026-11-19). The plot has
  changed and the author has overruled `meta-arch-*` often; the chronology and
  dated rulings win.
- **Weighing the structural editors against the capture panel** (author ruling
  2026-11-22). The two instruments see different things, so trust each where it can see:
  - **Repetition, templates and echoes across chapters: the structural editors.** A
    capture reader holds the earlier chapters only as a fact checkpoint plus the raw
    prose since the last decade boundary (`tools/capture_dag.py:9-12`), so a sentence
    or scene shape repeated from outside that window is invisible to it. A high capture
    score is not evidence against a repetition finding.
  - **Momentum, and whether a reader stops: the capture panel,** read as each reader's
    z against her own mean and her ALMOST-STOPPED/WHY lines. Raw CAPTURE scores sit
    near the ceiling and rise with position in the volume (Vol 1: 7.8–9.8; r = 0.45
    with chapter number), so a low score is signal and a 9 against a 10 is not.
  - **Macro allocation** (how much of a volume one object or thread takes): **the
    structural editors only.** Capture can show no single chapter loses the reader,
    nothing more.
  - **Both agree: act.** Structural drag of 2+ editors on a chapter whose capture z is
    also low (Vol 1: ch7, ch12) is the strongest signal either instrument gives.
  - **They disagree on a pacing or sag claim:** check whether the finding is really
    repetition (then the structural read stands) or local momentum (then capture
    stands). Structural editors read a whole volume in one sitting and are prompted to
    find problems; their read stands for the binge reader, not the chapter-a-night one.
  - Neither instrument is calibrated against people. A human beta round is the test
    that weights them.

## Volume 1

- **vol1 C1 — the soft ending** (dress and induction build, Rock closes on
  contentment): **defect** (author ruling 2026-11-19).
- **vol1 C1 (2026-11-20 consensus) — debrief stacks:** acted on; final ruling
  waits on a re-run of the structural editor. Actions: {{Remembrance}} (ch16)
  breaks the fitting stack from the Friday stack; the hike chain is cut to one
  full telling ({{Leave No Trace}} :295 keeps only Vee's read of his motive;
  {{What to Wear}} :31 narrates the shirt in summary). The dinner and Friday
  stacks stay: the Cassie/Randi gap is the arc.
- **vol1 C5 — duplicate final-chapter blocking:** fixed at `684efc00`
  ({{Nachtmusik}} :85).
- **vol1 C10 — Pace never uneasy about deceiving Vee:** acted on in
  {{Remembrance}} (he sees the disclosure, *"I could just tell her,"* and is
  steered off it into the gift logic); final ruling waits on the re-run.
- **vol1 C9 — the passcode paid without setup:** not a defect (author ruling
  2026-11-20). A loved one's birthday is a common passcode, and learning a
  girlfriend's birthday sits below the detail the book renders. No Nachtmusik
  cold reader flagged it; the finding came from the diagnose prompt's
  "paid without setup" priming.
- **vol1 C16 — the timeline read from scattered markers:** answered by the reader-facing
  date lines the book ships with (author ruling 2026-11-21; date lines per the 2026-10-25
  ruling). The editors read an undated manuscript; no prose change.
- **vol1 C2 — the climax with both orchestrators offstage:** designed and landing; no
  change (author ruling 2026-11-21). The Induction is Vee's own climax; the volume sells
  a plan she cannot see, not a knowing triangle. The Nachtmusik reunion is the means of
  the theft, and no current cold read finds it long.
- **vol1 C7 — Cassie becomes only a confidante:** already ruled; Cassie stays passive
  (author ruling 2026-11-21). Her warnings stay active about Randi, whom she sees and
  reads by cue; about Pace they are soft, since she has met him only at the coffee-shop
  meet-cute and knows him through what Vee tells her until Volume 3. She does not
  criticize Pace: that would drive a real wedge between her and Vee. Audit each Cassie
  chapter for its unheeded true sentence on those terms.
- **vol1 C8 — the Brooke/Standards threat planted and left untouched:** acted on
  (author ruling 2026-11-21). Brooke now recurs as an active constraint on Randi in
  {{Dear}}, {{Fed}}, {{Gone}}, {{The Induction}} and {{Nachtmusik}}. The exposure itself
  is Volume 2's ({{Inversion}}); in Volume 1 the threat is a tightening constraint, never
  a reveal. Final ruling waits on the next structural re-run.
- **vol1 C10 (2026-11-21 consensus) — Pace's POV slips into Randi's head:** the slip
  at {{The Bench}} :143 is fixed (author ruling 2026-11-21): cut to what Pace sees, *"a
  matching set, pale, expensive."* The bathroom handover to Randi's POV (sol's B13) is
  designed (`meta-note-the-bench.md:10`); no change.
- **vol1 C5 — the bench never used again, and gone from the bedroom:** acted on (author
  ruling 2026-11-21). In {{Fed}} Vee tells Randi about the one ungainly table among his
  spare Arts and Crafts pieces and takes it for his first design; Randi goes bright and
  leaves the table fast (opus's A7: the bench is in the room and Vee has seen it; sol's
  B3: the bench still shapes Randi, appetite and wound unsorted). Rock and Peekaboo are
  not touched. The bench's use waits for {{Vee on the Bench}}.
- **vol1 C3 — Pace's misreading of Randi the same beat each time:** {{Swim Lanes}} and
  {{Remembrance}} designed and landing; {{Portion}} fixed (author ruling 2026-11-21). At
  `portion.md:91` he had forgotten the table's conclusion (Friday stung her); now he sees
  she has never been with him like that, that it is more than Friday, and keeps silent
  out of respect for her pride. The rule is recorded in `meta-craft-pace.md` ("He sees,
  and chooses").
- **vol1 C4 — the Pace–Randi evenings run on a template; {{Gone}} adds little:** the
  ritual is designed (the music keys the woman, the deadbolt is her habit, and the
  {{Portion}} / {{Gone}} / {{Nachtmusik}} variations need a baseline); the repeated
  *wording* was the defect, concentrated in {{Swim Lanes}}, {{Remembrance}} and
  {{Portion}}. Acted on (author ruling 2026-11-21): Swim Lanes keeps the full arrival;
  Remembrance has the deadbolt go over unheard and the taillights taken by the cut;
  Portion has Randi an hour late, Pace in the shower, the playlist rolling on to
  *Violator*. Randi's arrival times to Pace vary (early, on time, late), against her
  always being early for Vee; when she is off time, someone remarks on it, and Pace
  never takes it as a slight. {{Gone}} stays (capture 8–10 on every lane); its
  three-in-a-row hand at his face is cut to the one at the confession (`gone.md:41`).
  B11 (sex restores equilibrium) and B15 ({{Nachtmusik}}'s reunion delays the phone)
  left standing: Nachtmusik is where sex stops restoring it.
- **vol1 C6 — Vee's line has no reversal:** the unbroken rise is the volume's design
  (*A Polite Invitation*; the stakes are the reader's foreknowledge, and her first
  reversal opens Volume 2 at {{Lesson}}). Acted on in part (author ruling 2026-11-21):
  the one cost she feels herself, the {{Sorority}} credit card, now presses inside the
  volume — {{The Induction}} opens alone in the dorm on the receipt lying unread on the
  heels' tissue, and January's books she doesn't know how she'll buy. No price is ever
  rendered. She pays it with her Christmas money, recalled at {{Across}}.
- **vol1 C1 — the Randi–Vee line never comes to a head:** the slow staircase is the
  design (the jacket sells a want Vee never lets herself notice; the threesome is a
  Volume Five payoff); Randi faces it in front of Pace at {{Remembrance}} ("Me") and
  {{Gone}} ("She got past me"); {{Nachtmusik}}'s phone is the irreversible triangular
  event. Acted on at the climax (author ruling 2026-11-21): on the second long step of
  {{The Induction}}'s walk the shoe catches her "firm as a hand," the buckle "where
  Randi's two fingers had been," and her nipples draw up tight; that is the second
  Cassie photographs (the black straps now in the frame). Walking out, her step catches
  on the shoes, and Cassie: "Careful. You'll get hurt." In {{Nachtmusik}} Randi reads
  the arousal in the photo and misattributes it: "Somewhere on that stage she had been
  thinking about him." Nobody notices; Vee doesn't know Randi has the photo.
- **vol1 C9 — the passcode reveal is not set up:** no chapter reader stumbled; the
  structural editors did. Planted (author ruling 2026-11-22): at {{Fed}} the waiter
  cards them and Randi takes Vee's license before Vee can ("Lemme see"), reads the
  date, and assigns her a sign — a Leo, "Leos never do anything in twos if they can do
  it in threes." No digits on the page. The failed first try at `nachtmusik.md:109`
  already shows the code was changed.
- **vol1 sol F10 — Meg, Kayla and Theo vanish after Chapter 12:** left standing
  (author ruling 2026-11-22). They return at {{Lesson}}, Volume 2's opener; the
  friend-world thinning as Vee's life bends is the design, and Cassie stays present
  through {{The Induction}}.
- **vol1 C5 (2026-11-22 consensus) — the Randi–Vee meals share one template:** the
  template is the design (author ruling 2026-11-22; `meta-plan-satc-tracks.md:13`).
  The repeated meal shows Randi habituating Vee to what is "normal" and lets the
  reader measure how the Vee–Randi relationship changes from one meal to the next,
  as the Cassie/Randi pairs measure the difference between the two friendships; real
  people also keep routines. The meals stay. **Act on the near-identical sentences:**
  most are mistakes or better cut (the goodbye hug at `see-you-later.md:129` and
  `dear.md:199`; the price-reading at `how-its-done.md:225` and `fed.md:53`). Randi's
  invented-story openers each do a job and stay unless a pass finds one that doesn't;
  they carry less weight than the meals themselves.
- **vol1 C4 (2026-11-22 consensus), Fed's induction decline:** Brooke's officers'
  meeting is real; Randi is not lying (author ruling 2026-11-22). The cookie-penance
  story stays, as fun and characterization. Capture readers suspecting a lie
  (glm, argon, `gate-ch018.md`) is a side effect, not a defect.
