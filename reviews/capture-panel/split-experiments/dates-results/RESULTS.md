# Dated chapter headings — capture-reader experiment results

**Question (author, 2026-10-24):** does a reader-facing date line under each chapter
and section heading (weekday, month, day; the year never shown) help or hurt? The author's
main concern is Thanksgiving through {{Gesso}} (ch43–71). Lines come from
`tools/chapter_dates.py`.

**Design.** Capture DAG, persona `romance-graduate`, 7 models, two arms per model:
`dates-undated` (control) and `dates-dated` (`capture_dag.py --experiment dates-dated --dated`).
Gates and carry-forward notes: the undated control was in the sibling `dates-undated/` tree, and the judging keys and scripts sat beside this file (all removed 2026-10-25; in git history at `1903b4fb`). **The dated arm was promoted to the real lanes on 2026-10-25** (`reviews/capture-panel/<model>/dag/romance-graduate/`, headers retagged `· dated`), replacing the older undated reads there. The book ships with date lines, and the real lanes now read dated by default.
Models: claude-opus-4-8, claude-opus-5, claude-opus-5-5, gemini-3.8-flash, gemini-4-argon,
glm-5.3, gpt-5.6-sol. Fable was held back (cost). Ch76 (Vee on the Bench) was not read: it
is due a substantial rewrite.

**Blind judging.** Each lane was relabeled `L###` and its header lines (which name the arm
and the model) were stripped. Judges scored each temporal claim against the chronology as
CORRECT / WRONG / VAGUE / UNSURE. The gate judge saw only the sentences with time language
in them (`gate-time-snippets.txt`); the notes judge saw whole carry-forward files. Keys are
in `*/KEY.json`.
- fall-1 (ch1–24): two Claude subagents (claude-opus-5-5, subscription). This is a
  same-model caveat: opus-5-5 is also one of the lanes it judged.
- spring (ch25–75): gemini-4-argon on OpenRouter, 7 calls, about $1.50 including three
  failed attempts (author-authorized). Author re-dates made after the run (Seconds → Mon
  Nov 30; Another Round's Friday opening) were accepted either way in the truth file.

## Capture (gate CAPTURE scores; `capture-scores.py`)

| Stretch | Undated | Dated |
|---|---|---|
| fall-1, ch1–24 | 8.47 | 8.42 |
| ch25–42 | 8.31 | 8.29 |
| ch43–71 (Thanksgiving–Gesso) | 8.50 | 8.51 |
| ch72–75 | 9.18 | 9.25 |

No stops in either arm. Per-model differences are within noise. No reader complained about
the date lines themselves.

## Timeline accuracy (blind judges)

| | fall-1 undated | fall-1 dated | spring undated | spring dated |
|---|---|---|---|---|
| Gate claims correct | 50 | 94 | 566 | 711 |
| Gate claims wrong (error rate) | 7 (12.3%) | 6 (6.0%) | 42 (6.9%) | 30 (4.0%) |
| Gate errors in ch43–71 | — | — | 20 | 11 |
| Note claims correct | 69 | 111 | 632 | 962 |
| Note claims wrong (error rate) | 3 (4.2%) | 2 (1.8%) | 11 (1.7%) | 8 (0.8%) |
| Exact dates or weekdays in notes | 36 | 73 | 295 | 593 |

- fall-1: every model improved. Spring: opus-4-8 (14% → 2%), opus-5 (8 → 4), opus-5-5
  (11 → 8) and argon (4 → 2) improved; flash and sol were near zero in both arms; glm got
  worse (4 → 8). Four of glm's seven dated errors are one ch28 gate repeating a single
  mistake.
- Remarks on how the book shows time: undated 5, dated 27. Most of the dated ones are the
  device working: the same-night catch at ch61 (three models independently), the New Year's
  Eve braid at ch49–50, Friday-then-brunch at ch47, the five nights away at ch42.
- What the dates expose: gaps. The Valentine's dance at ch72–73 (opus-5: "the book just
  drove past the one date it had set on the page"; it is the unwritten {{Safely Held}}), the
  Mar 11 → Apr 10 jump at ch74–75, the Thanksgiving crop at ch43, Seconds dated on the same
  Sunday as Cropped's dinner (fixed: Mon Nov 30), and Another Round's opening section filed
  under the taproom's Saturday (fixed: a Friday line plus a Saturday section line).
- Caveats: the spring notes judge answered briefly (about 1,100 output tokens per call), so
  that half is shallower than the gate half. Some judge "wrong" calls are themselves wrong
  (e.g. opus-5's "two nights after a party" at ch62 matches the prose).

## Possible prose ambiguities (wrong in both arms, so the prose may be the cause)

- ch28 {{Hills and Valleys}}: Vee's arrival placed "tomorrow night" by three undated lanes (opus-5-5, glm, opus-4-8) and one dated lane (glm). The phrase is Randi's, from {{Broken In}} on the Friday. Fixed 2026-10-25: the opening now names this Saturday ("and they rode this one").
- ch29 {{Recognized Method}}: NOT an ambiguity — a judge error. The prose has Vee stay to Monday morning (`recognized-method.md:157-159`, "Monday came at her sideways"); the truth file stopped at Sunday because the `days:` entry did. Fixed 2026-10-25. The "Monday morning" readings marked WRONG (argon, opus-5, both arms) were right.
- ch39 {{All the Time}}: the gap from the photo (Thu Nov 12) to brunch (Sat Nov 14) is read as "two weeks",
  "four days" or "six days". Cause: Randi's "two *weeks* old" (`:97`) is about the older pictures, and "since the morning after" (`:103`) is unpinned. Left as is (author ruling 2026-10-25): nothing later depends on the photo's age.

## Next

Cold-read panel test of the dated headings (second instrument). Cold-read packets need the
same date-line injection (`chapter_dates.dated_text`).
