# Epub build and device status

*What the test epubs do today, per volume and per reading app. Procedure lives in
`meta-plan-editorial-checklist.md` (Phase 6, Typesetting and Proofread after
typesetting); the packaging spec lives in `meta-blurb.md` (Test-epub assembly);
the builder is `tools/build_epub.py` (skill `wals-epub`). This doc records state
only.*

---

## Builds

All five volumes build: `tools/build_epub.py --volume <N>` (Volumes Three–Five
with `--allow-missing` while drafting; unwritten chapters are left out and listed).

| Vol | Output | Cover | Contents |
|---|---|---|---|
| 1 | `build/a-polite-invitation.epub` | own | complete |
| 2 | `build/a-warm-reception.epub` | own | complete |
| 3 | `build/a-place-at-the-table.epub` | own | drafted chapters only |
| 4 | `build/a-proper-serving.epub` | own | drafted chapters only; jacket copy to revise |
| 5 | `build/a-hot-meal.epub` | own | drafted chapters only; jacket copy to revise |

- **Covers** are read in place from the cover repo
  (`../cover/output/<tag>/apple_1707x2560.jpg`), not copied in. The build
  aborts on a missing file, a Git LFS pointer, or a non-image. One cover inside
  the epub serves every reading app; per-store sizes matter only for store
  uploads. Covers are not final.
- **Series metadata** is in every build: EPUB 3 `belongs-to-collection`
  (series, position 1–5) and the Calibre `series` / `series_index` pair.
- **Custom metadata** (`wals:build`, `wals:recipient`) uses a declared
  `wals:` prefix, as EPUB 3 requires.
- **Validation:** XML well-formedness and internal links check clean in all
  five. EPUBCheck 5.4.0 is downloaded (`~/local/epubcheck-dl/`) but has not
  been run yet.

## Reading apps (iPhone)

| App | How loaded | Covers | Opens | Series grouping | Notes |
|---|---|---|---|---|---|
| Apple Books | sideload | all five | all five | — | Reference renderer |
| Kindle | Send to Kindle (email) | all five | yes | no | Personal documents never group; series grouping comes from the KDP catalog after publication |
| Google Play Books | upload at play.google.com/books, read in the app | all five | all five | — | Uploads need processing time before covers and opening work. Page numbers advance unevenly per swipe (computed pages, not screens) — expected for reflowable epub |
| Kobo | — | — | — | — | iOS app has no reliable sideload path; not tested |

## Open

- Run EPUBCheck on all five builds and fix what it reports.
- Check series grouping in Apple Books and Play Books.
- The on-device proofread (Phase 6 checklist) has not started.
- Volume Four and Five jacket copy to revise.
