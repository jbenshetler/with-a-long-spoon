# Close-third pass status — all volumes

Progress log for `/wals-close-third` (explain-after-showing, narrator
interpretation, close-third slippage). One row per drafted chapter, epub order
(`tools/chapter_dates.py`). States:

- **pending** — not yet read.
- **proposed** — batch written to `audits/close-third/<slug>.md` and shown to
  the author; no rulings yet.
- **reviewed** — author ruled on every item; edits applied and the rulings
  recorded in `meta/meta-triage-<slug>.md`. Row gives the date, the tally
  (applied / declined / left alone) and the commit.

Restart: finish the first `proposed` chapter with the author, else read the
first `pending` one. Chapter numbers follow the chronology; if chapters merge or
move, renumber the rows from `tools/chapter_dates.py` and keep the states.
Work volume by volume (`meta-plan-editorial-checklist.md`, Volumes): Volumes 1
and 2 are in pre-publication cleanup; Volume 3 enters when its drafting is
complete.

### Volume 1 — *A Polite Invitation* (22 chapters)

 1. the-bench — pending
 2. standards — pending
 3. the-pointing-game — pending
 4. see-you-later — pending
 5. substitution — reviewed 2026-10-25 (embodiment pass, before this skill; `a79bb2d7`)
 6. tannin — pending
 7. water-wings — pending
 8. may-i-choose — pending
 9. dear — reviewed 2026-10-26 (8 proposed: 7 applied, 1 declined, 4 left alone; capture follow-ups added 4 more; `1ceac9c9`)
10. leave-no-trace — pending
11. swim-lanes — pending
12. what-to-wear — pending
13. two-towels — reviewed 2026-10-26 (11 proposed: 4 applied, 3 kept, 4 withdrawn; `616ba975`)
14. a-round — reviewed 2026-10-26 (4 proposed: 2 applied, 2 withdrawn; :202 filter-verbs acked; `616ba975`)
15. how-its-done — reviewed 2026-10-26 (2 proposed: 2 applied; `a2591886`; :338 "very" cut later)
16. famished — reviewed 2026-10-26 (7 proposed: 4 applied, 3 kept; `736a1679`)
17. fed — reviewed 2026-10-26 (aggressive list of 25; 6 walked: 1 changed, 5 kept; 19 not walked; `8cdc01f1`; follow-up: :109 rewritten, :119 trimmed, :119 Pace sentence kept; `8e10f902`)
18. portion — reviewed 2026-10-26 (2 proposed, 2 questions, 2 borderline: 6 changed — :85, :81, :79, :37 cut; :65 reworked; :69 rewritten, jealousy guard amended; `c53377df`)
19. peekaboo — reviewed 2026-10-26 (2 proposed, 2 questions, 2 borderline: 4 changed — :49, :7 cut; :99 trimmed and rephrased; :9, :41 kept; `5a62d7e9`)
20. sorority — reviewed 2026-10-27 (3 proposed: 3 applied; 2 questions: both left; 6 borderline: 2 cut, 4 kept; `5f4b13e1`)
21. gone — reviewed 2026-10-27 (1 proposed: 1 applied — :67 cut; 1 question: left; 2 borderline: both kept; `7d87cc5a`)
22. rock — reviewed 2026-10-27 (6 proposed: 6 applied; 1 question: left; 6 borderline: 3 cut (:211, :265, :91 second clause), 3 kept; 2 trims applied; `66aaaec5`)

### Volume 2 — *A Warm Reception* (25 chapters)

23. lesson — pending
24. broken-in — pending
25. space — pending
26. recognized-method — pending
27. practice-room — pending
28. the-induction — pending
29. we-find-out — pending
30. made-up — pending
31. one-bite — pending
32. above-him — pending
33. school-nights — pending
34. in-his-hands — pending
35. all-the-time — pending
36. four — pending
37. outlier — pending
38. new-ordinary — pending
39. cropped — pending
40. under-the-rug — pending
41. bare — pending
42. believe-me — pending
43. fairytale — pending
44. old-acquaintances — pending
45. the-usual — pending
46. my-friend-randi — pending
47. nothing-underneath — pending

### Volume 3 — *A Proper Serving* (24 chapters)

48. missed-a-spot — pending
49. back — pending
50. unpacking — pending
51. across — pending
52. covering — pending
53. among-friends — pending
54. clean-plate — pending
55. reach — pending
56. my-pleasure — pending
57. another-round — pending
58. hangover — pending
59. between — pending
60. barely-stings — pending
61. still-life — pending
62. on-her-floor — pending
63. boyfriend — pending
64. coming-due — pending
65. some-of-mine — pending
66. gesso — pending
67. burn — pending
68. grace — pending
69. postcard — pending
70. in-her-place — pending
71. vee-on-the-bench — pending

### Volume 4 — *A Hot Meal* (1 chapter)

72. ignition-scalding — pending
