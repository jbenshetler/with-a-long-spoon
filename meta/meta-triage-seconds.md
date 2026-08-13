# Triage — Seconds (line audit, 2026-08-03)

Sentence-by-sentence consistency/logic audit (`audits/line-audit/seconds.md`).
4 findings: 3 fixed, 1 left standing.

## Fixed

- **Hand "not moving" vs. later "stopped"/"began to move again"** (:5 vs :29/:31)
  — the explicit stillness claim at :5 broke the later beats. Cut the claim
  instead of touching the beats: :5 now "warm and rough, the steady weight…"
  ("rough" is firmly canon — gym bar + workbench; `meta-note-burn.md:51`). A
  resting hand's ambient motion now makes "stopped" and "again" read true.
- **"Her cheek against the place his mouth had just been"** (:39, echoed :43)
  — his mouth had just been on her own crown; unleanable. Re-anchored both to
  "his shoulder" (matches the coda's memory at :65). The head-kiss choreography
  kept intact deliberately — Vee's hair is symbolic (the warm red,
  untameable); a shoulder-kiss variant was considered and rejected as costing
  the hair beats at :39/:51.
- **"The basement laundry room"** (:55) — author ruled the Vawter laundry is
  **on Vee's floor, down the hall, not a basement** (cozy sweats-and-socks
  shuffle; recorded in `meta-note-among-friends.md`). Now "the dorm laundry
  room"; coda's "carried it up" (:63) → "carried it back down the hall."
  Kayla's hall-and-basket beat in {{Nothing Underneath}} is compatible.

## Left standing — do not re-litigate

- **Coda's "the sun coming up" while she said it** (:65) — memory-compression,
  in-register for a coda about reworking the event at a distance; "pre-dawn
  chill… sun coming up" frames the morning's span, not a timestamp.

---

# Triage — Seconds (cold-read feedback pass, 2026-07-29/30)

Panel: claude-fable-5, claude-opus-4-8, gpt-5.5, gpt-5.6-sol (read after {{Cropped}}, under the placeholder title "The Porch Scene"). Review files: `reviews/cold-read/*/seconds.md`.

## Fixed (commits `9b4c9f1`, `fc4dbbf`)

- **Coda over-explanation** (all four models, mild). Cut "her one attempt *to give him the opening he had needed for the answer she had been waiting for*" → "her one attempt." The opening-idea already recurs in "She would not give him the opening again."
- **"reliable-Pace model"** (both GPTs: too analytical for Vee's register; fable-5 quoted it approvingly — split panel). Softened to "what she knew about him," keeping the repair-work image.
- **Style thinning** (linter-driven, no reviewer stumbled): filter-verb run at the decision beat recast to direct images; "a small breath"→"once"; "a small silence"→"a silence"; "by the way he had positioned the second cup"→"from the second cup … positioned"; "in the way you think about something you do not yet know what to do with" cut. Four `the-way` uses acked as authorial (poem simile, rearranges-himself, heater aside, not-yet-thinking beat) in `style/style-allow.toml`.
- **Title** (3 of 4 called "The Porch Scene" flat/stage-direction; it was a placeholder). Renamed **Seconds** — detonations: no second offering of the sentence; his two breaths; the pre-placed second cup; and (arms only after the reveal) Vee as his second lover, the "together" she believes singular. Runner-up recorded: "Eating."
- **Plants/heater continuity** (author-caught, not reviewer). "For the plants" was pure invention — no plants in `meta-plan-pace-house.md`'s sun-porch inventory, and an impersonal overnight heater cut against warmth-made-for-her canon. Rewritten: heater turned down at night, fireplace warmth from the den through the archway, porch cool (justifies the quilt); pale moon over the black mountains replaces the sky-band; "fence"→mountains (house canon: woods → mountains beyond the glass).

## Left standing — do not re-litigate

- **Missed-vs-dodged irresolution** (all four felt it; several called it damning). Working as designed — understanding-and-routing, both readings operative (Bible: "The porch-scene register (worked example)"). The readers' inability to resolve it is the scene succeeding.
- **"What you do — what your body does" wince** (gpt-5.5 flinched). Designed: his answer routing her speech down the sex-channel is the scene's structure; sincere within his chivalric grammar.
- **Warmth absorbing the sternum-*wait*** (gpt-5.6-sol: "that doubleness is unsettling"). Designed — the mechanism the Christmas fight draws on.
- **Italicized "She had said her best sentence. He had not said the sentence back."** (opus: thesis-y, then withdrew — "it earned the plainness; I didn't resent it"). Stands.
- **`file/filed` verbs in the pile paragraph** (linter tic `file-verb`). Load-bearing — the pile is the point; all four readers cited it as a chill. Keep; ack on next `--ack` pass.
- **Bus-replay in the coda.** The old scene-file craft notes offered full compression as an option; rejected — every reviewer praised "The two things had not been the same shape." (See also `meta-todo-open-questions.md` §"coda after the break: KEEP".)

## Not actionable

- Wishes for Cassie/Randi intervention (plot desire, downstream scenes exist).
- Reviewer inferences about *why* Pace withholds (Randi, the vow) — reactions, not canon.

## Rulings recorded post-review (2026-07-30)

- **Music thread: silence.** The registry triggers for any scene at Pace's house; ruled silent here — the soundscape is his breaths and the *mm*.
- **Porch heat backstory** ruled coherent in `meta-plan-pace-house.md` (register + thermostat; warm for {{A Round}}, cool at night for {{Rock}}/{{Seconds}}).
- **Same-day sequencing with {{Cropped}} is intentional** — first reunion after Thanksgiving, Vee full of missing him and the who-are-we questions the break raised.
- **Moon rises over the mountains** (behind the nearer ridge) — line 17 aligned.
- **Coda re-grounded (author-directed):** the "would"-heavy flash-forward landed as a lived scene in the dorm **laundry room** (bus cut — on-campus resident, container ruled: physically inside, physically quiet); one prophetic *would* retained at the close. Pile now already-not-empty (canon: smaller porch-register moments precede this one, `meta-craft-pace.md`). Flannel deliberately kept out of the load.

---

# Triage — Seconds (line edit, 2026-08-13)

True line-edit pass (report in chat; no report file — single-chapter mode).
10 candidates surfaced: 7 applied, 2 left standing, 1 dropped as already-settled.

## Applied (see commit)

- Para 39 warmth-pile: the four-"warmth" / received-received-knew / "let the
  warmth do what warmth does" tail rewritten (author's own recast) →
  "She had come to expect his warmth these mornings, and her body knew what to
  do with it. She leaned her cheek against his shoulder and closed her eyes."
- Para 43: cut the "when the quilt is warm and the man is holding you and the
  sun has begun to come up" over-explaining tail — kept "where small *waits* go"
  (fable-5 praised the clause as "the book's method"); tail also recapped 47/51.
- Para 39: cut repeated "small specific" modifier (kept the para 35 instance).
- Paras 31 / 43 / 43: thinned three reflex "small"s (intentional press; slow way;
  the first of "small adjustment … small *wait*"). The **"small *wait*"** kept —
  fable-5-praised and load-bearing for the "small *waits* go" echo.
- Para 23: cut the middle "require her to find the words again" clause and the
  trailing "She did not have to search" (kept the find→found reversal).
- Para 5: cut the quilt-provenance tail ("because it had been on his bed before
  he had put it out here for the cooler months").
- Para 29: cut "after the first" (redundant with "a second breath"; the
  two-breaths beat itself is kimi-k3/terra/sol-praised and untouched).

## Left standing — do not re-litigate (re-open only on a text edit)

- **Para 41 layered "underneath"** ("underneath the warmth — underneath what her
  body was doing with the warmth — something else was beginning to move").
  Reads as intentional two-step descent, and the para-39 thin removed the
  warmth-pile it used to sit against; the second appositive now has a clean
  referent in 39's "her body knew what to do with it." (opus flagged the
  *sternum-wait/warmth doubleness* elsewhere — already left-standing above.)
- **"did not have a name" twice** (para 55 "a small thing it did not have a name
  for" / para 61 "The shape did not have a name"). Ruled the through-line, not a
  reach: the feeling has no name at the first flinch and still none at its final
  placement; the persistence of namelessness is the point. Para 55's residual
  `a-small` hit ("a small thing") therefore stands by design.

## Dropped — already settled by prior triage

- **Coda "triple-close"** (para 61 verdict / 63 scene-out / 65 recap). The
  coda structure, the single retained prophetic *would*, and specifically
  ":65 sun coming up" are all ruled left-standing above (line audit 2026-08-03
  + cold-read pass 2026-07-30). Not re-litigated.
