# Line edit — status (Volume One, epub order)

States: pending → edited → reviewed. Reports at `audits/line-edit/<slug>.md`.
Echo rulings ledger: `audits/line-edit/echo-rulings.md` (Stage 0 gate — rule
the echo shortlist with the author before per-chapter editing starts).

## OUTSTANDING — within-chapter echo pass (opened 2026-09-14, not started)

**Every chapter below reads `reviewed`, but only on one axis.** Stage 0's
harvester required an n-gram to span 2+ chapters (`len(fs) >= 2`), so the
completed line edit measured **cross-chapter** repetition only and is
structurally blind to a phrase over-repeated *inside* a single chapter — which
is the commoner failure, since a reach-phrase recurs most densely while the
writer is inside one scene.

Found the hard way: "the small breath of a laugh" ran 4× in `the-bench`,
cleared every distinctiveness filter, and was rejected solely for living in one
file. Two `glm-5.3` capture reads flagged it by counting; no tool did. Section 4
of `echo-inventory.md` and `echo_harvest.py --scene <slug>` now cover this axis
(added same day, with the widened `a-small` linter rule).

**Scope at open: 49 candidates across 18 of 74 drafted chapters.** 25 have
their closest pair inside 300 words — cluster-shaped, the kind an ear catches.
Heavily concentrated:

| Chapter | Candidates |
|---|---|
| vee-on-the-bench | 14 |
| the-bench | 11 |
| a-round | 4 |
| among-friends | 3 |
| leave-no-trace, lesson, substitution | 2 each |
| 11 others | 1 each |

Half of it sits in the two long bench set-pieces — longest chapters, most
sustained single-scene physical writing. `vee-on-the-bench` is Volume Two and
outside the table below. A pass on those two would clear ~51% of the inventory.

Discipline when it runs (`CLAUDE.md`, Style checking): flags, never findings.
The book runs on designed repetition, and **cut instances rather than paraphrase
them** — the fix for a phrase used five times is usually to use it twice, not to
find five different ways to say it.

`the-bench` had its own within-chapter pass on 2026-09-14 (5 → 2 uses of the
laugh phrase); its remaining 11 candidates are unruled.

| # | Chapter | Slug | State |
|---|---|---|---|
| 1 | The Bench | the-bench | reviewed |
| 2 | Standards | standards | reviewed |
| 3 | The Pointing Game | the-pointing-game | reviewed |
| 4 | See You Later | see-you-later | reviewed |
| 5 | Substitution | substitution | reviewed |
| 6 | The Long Way | long-way | reviewed |
| 7 | Water Wings | water-wings | reviewed |
| 8 | May I Choose | may-i-choose | reviewed |
| 9 | Off Six-Fourteen | off-six-fourteen | reviewed |
| 10 | Dear | dear | reviewed |
| 11 | Leave No Trace | leave-no-trace | reviewed |
| 12 | Rye | rye | reviewed |
| 13 | What to Wear | what-to-wear | reviewed |
| 14 | Two Towels | two-towels | reviewed |
| 15 | A Round | a-round | reviewed |
| 16 | Turned Up | turned-up | reviewed |
| 17 | How It's Done | how-its-done | reviewed |
| 18 | Famished | famished | reviewed |
| 19 | Toenails | toenails | reviewed |
| 20 | Fed | fed | reviewed |
| 21 | Peekaboo | peekaboo | reviewed |
| 22 | All Told | all-told | reviewed |
| 23 | Sorority | sorority | reviewed |
| 24 | Gone | gone | reviewed |
| 25 | Rock | rock | reviewed |
| 26 | Lesson | lesson | reviewed |
| 27 | Broken In | broken-in | reviewed |
| 28 | Hills and Valleys | hills-and-valleys | reviewed |
| 29 | A Recognized Method | recognized-method | reviewed |
| 30 | The Practice Room | practice-room | reviewed |
| 31 | The Induction | the-induction | reviewed |
| 32 | We Find Out | we-find-out | reviewed |
| 33 | Made-Up | made-up | reviewed |
| 34 | One Bite | one-bite | reviewed |
| 35 | Above Him | above-him | reviewed |
| 36 | School Nights | school-nights | reviewed |
| 37 | In His Hands | in-his-hands | reviewed |
| 38 | All the Time | all-the-time | reviewed |
| 39 | The Outlier | outlier | reviewed |
| 40 | The New Ordinary | new-ordinary | reviewed |
| 41 | Cropped | cropped | reviewed |
| 42 | Seconds | seconds | reviewed |
| 43 | Under the Rug | under-the-rug | reviewed |
| 44 | Bare | bare | reviewed |
| 45 | Believe Me | believe-me | reviewed |
| 46 | Fairytale | fairytale | reviewed |
| 47 | Old Acquaintances | old-acquaintances | reviewed |
| 48 | The Usual | the-usual | reviewed |
| 49 | My Friend Randi | my-friend-randi | reviewed |
| 50 | Nothing Underneath | nothing-underneath | reviewed |
