# Editorial status — Volume 1 (*A Polite Invitation*)

Progress for Volume 1 against the passes defined in
`meta-plan-editorial-checklist.md`, in the same phase order. The checklist
defines each pass, its scope (chapter, volume or cross-volume) and what makes
it stale; this doc tracks where this volume stands. Each pass's own
`STATUS.md` holds the detail.

**Volume 1:** 22 drafted chapters, `the-bench`…`rock`
(`tools/volume_scenes.py`). **Stage:** pre-publication cleanup (author, 2026-10-27).

Statuses: **unstarted** · **in progress** · **complete** · **stale** (complete
once, then invalidated by later edits; re-run the delta).

Updated 2026-10-27.

| Phase | Pass | Status | Notes |
|---|---|---|---|
| 0 | Developmental edit | in progress | Every chapter has been through cold-read panels and triage. The October diptych merges ({{Fed}}, {{Dear}}, {{How It's Done}}) changed the inventory; **the structure has not been declared final**, which is Phase 0's exit. |
| 1 | Retell pass | complete | 2026-09-28 (`meta-plan-retell-pass.md`); all three event-Cassie-Randi stacks are in this volume. Later ruling 2026-10-23 for the merged {{Fed}}. |
| 1 | Line-editor whole-volume pass | stale | One run, 2026-09-29, fable-5-1, on this volume as bounded then (27 chapters, `the-bench`…`rock`); 121/121 quotes verified; five interpretive lines with no uptake, rulings pending. Stale by the 2026-10-03/04 tell pass and the merges. |
| 1 | Explain audit | complete | 2026-10-08, as Vol A (`4da9f20b`). |
| 1 | Close-third pass | in progress | 12 of 22 reviewed (`audits/close-third/STATUS.md`); next `lesson` is Volume 2, so the remaining Volume 1 chapters are ch1–4, 6–8 and 10–12. |
| 2 | True line edit | stale | Complete 2026-08-14 (`audits/line-edit/STATUS.md`). About 300 prose commits since, and the merges. |
| 2 | Figure sweep | unstarted | Tool and gold gate ready (2026-10-27); run deferred to pre-publication (author ruling). For this volume: `extract --volume 1` on both models, then `group --through 1`. |
| 2 | Reading-effort sweep | in progress | 2 of 22 swept (`the-bench`, `the-pointing-game`), 4 rulings, 31 convergent findings open (`audits/reading-effort/STATUS.md`). |
| 3 | Continuity and logic line audit | stale | Complete 2026-08-03 (`audits/line-audit/STATUS.md`). Stale by later edits and the merges. |
| 3 | Cross-chapter fact audit (Lane A) | unstarted | Reset 2026-10-09. Per-edit checks since are logged in `audits/fact-audit/STATUS.md`. |
| 3 | Date check | in progress | Headings built and enforced in pre-commit. Prose claims not built (open question #48). The 2026-08-03 timeline sweep is stale and keyed to old chapter numbers. |
| 3 | Orphaned-reference sweep (Lane B) | in progress | Swept 2026-09-19 with Volume 2; none of the 26 candidates ruled, the heaviest here (`the-bench` 10, `the-pointing-game` 6) (`audits/orphan-refs/STATUS.md`). |
| 3 | Ruling-anchor check | unstarted | `tools/ruling_anchors.py` built, not yet run in a revision round. |
| 4 | Copyedit against the style sheet | stale | Complete 2026-08-03; sheet at `style/style-sheet.md`. Stale for every chapter revised since. |
| 4 | Style-tic policing | in progress | Per-edit throughout; the whole-volume pre-publication run is not done. |
| 4 | Flat-interrogative sweep | in progress | 3 hits active in this volume (2026-10-27). Left flat pending the author's ack: `standards:131`. Elliptical questions need a read by eye. |
| 4 | Age-coded language sweep | unstarted |  |
| 5 | Capture/retention panel | in progress | Gates exist for ch1–22; chapter-local re-reads after revisions (e.g. {{Dear}} 2026-10-26). Re-run the stale gates (`capture_dag.py --check-stale`) before the beta round. |
| 6 | Legal and content read | complete | For the beta round (author ruling 2026-09-16); findings in `meta-plan-legal-read.md`. **Deferred to publication:** the Dr. Marsh archived-catalog leg and any counsel engagement (`meta-plan-lawyer.md`). |
| 6 | Front and back matter | unstarted | Author bio copy locked 2026-08-15; wiring it into `build_epub.py` remains. |
| 6 | Typesetting | in progress | Test epub via `wals-epub`. |
| 6 | Proofread after typesetting | unstarted |  |
| 7 | Beta / test-reader round | unstarted | Plan in `meta-plan-test-readers.md`. |
