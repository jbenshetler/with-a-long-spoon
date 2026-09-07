# Tooling — cross-volume authoring/reading memory (checkpoints)

*Design note for the checkpoint machinery: `tools/checkpoint_context.py` (authoring),
`tools/cold_read_grounded.py` (grounded cold read), `tools/checkpoint_extract.py`
(minting), `tools/checkpoint_bundle.py` (prose window). Not novel canon — tooling
design. Author ruling 2026-09-01.*

## The memory model

For a chapter N the assembled memory is always **one checkpoint + a bounded raw
window**:

    boundary B = ((N-1) // decade) * decade          # last decade checkpoint before N
    memory     = project(ck-ch{B})  +  raw prose ch(B+1)..(N-1)

The checkpoint is verbatim (already consolidated); the recent window is full-fidelity
prose. `checkpoint_context.py` additionally slices reader-reaction sections off the
checkpoint so a drafting model never sees them (`--keep`/`--drop`).

Chapter numbering is the **flat cross-volume drafted sequence** —
`checkpoint_bundle.reader_slugs()` = Vol 1 drafted + Vol 2 drafted + Vol 3 drafted,
in chronology order. The current operational inventory has 50 drafted Vol 1 entries.
The approved final inventory is **51** after the Tue Nov 10 lap vignette is drafted;
while that entry remains Unwritten, it is excluded from the reader sequence. This is
the single source of truth shared by the authoring and grounded-read lanes.

## The bug this note fixes (2026-09-01)

`checkpoint_context.py` and `checkpoint_bundle.build_bundle` used to resolve N against
`volume_one_slugs()` — a 50-entry universe. Post-Vol1 this **silently dropped all Vol2
prose**: `--to 60 --check` reported "recent window: (none drafted yet between ch50 and
ch60)" and emitted only ck-ch050, though ten drafted Vol2 chapters live in that gap.
The self-heal was also broken (`build_bundle(1,60)` → out-of-bounds). Fixed by pointing
both at `reader_slugs()` and adding a `--decade` stride to `checkpoint_context` (the
grounded lane already had it). Vol1 reads are unchanged.

## The running checkpoint past Vol1 — one chained hop per volume

The current operational Vol1 checkpoint, `ck-ch050`, is a **single grounded pass**
over the 50 drafted entries (zero hops, panel-QA'd, frozen). The approved final Vol1
checkpoint will become `ck-ch051` only when the Tue Nov 10 lap vignette is drafted and
enters the reader sequence. That cutover must be atomic; the current `ck-ch050` →
`ck-ch060` path remains valid until then. Past Vol1 we accept **exactly one
consolidation hop per volume** — the memory at any chapter is always ONE hop away
from a pristine, frozen prior-volume checkpoint, never a chain of hops within a volume.
The mint recipe for a decade checkpoint at boundary B in volume V:

    ck-ch{B} = consolidate(  frozen final checkpoint of volume (V-1)
                           + raw prose of volume V, from its start up to B )

- Every in-volume decade checkpoint chains off the **same frozen prior-volume
  checkpoint** (re-folding this volume's raw to date each decade) — so intra-volume
  chain depth stays 1 and total depth = (V − 1). Trade: mints re-read the current
  volume's raw each decade (offline, on a big-context codex model — fine), in exchange
  for no compounding drift within a volume.
- Chosen over the single-cumulative-stream alternative (keep minting global ck-ch060,
  ck-ch070… each chained off the previous checkpoint) because that re-consolidates Vol1
  every hop and lets verified Vol1 detail thin. Here Vol1's QA'd memory is preserved
  verbatim for the whole trilogy.

Worked example — the 12th chapter of Vol3:

    memory = ck-v3-ch10  +  raw Vol3 ch11
      ck-v3-ch10  = consolidate( ck-v2-final + raw Vol3 ch1..10 )   # one hop off Vol2
      ck-v2-final = consolidate( ck-v1-final + raw Vol2 all     )   # one hop off Vol1
      ck-v1-final = single-pass grounded mint of raw Vol1           # zero hops (frozen)

    chain depth from ch1 = 2 = one hop per volume past Vol1.

## Context budget (measured 2026-09-01; tok ≈ words × 1.35)

- A decade checkpoint: ~4.1k words ≈ **~5.5k tok** (plateaus ~5.5–8k).
- Avg scene: ~2.7k words ≈ ~3.7k tok. A ≤9-chapter window ≈ up to ~33k tok.
- **This model: ~6–8k (ck) + ≤33k (window) ≈ ~40k tok, flat** regardless of trilogy
  length. Leaves ample room for the `meta/` canon load inside Sonnet 5's window.
- Real assembly for ch060 (default decade 10): currently ck-ch050 + raw ch51..59; after the approved final-Vol1 cutover, ck-ch051 + raw ch52..59. Both are ≈ **~54k tok**.
- Contrast — the retired all-raw interim scheme (`--decade 50`, before ck060 existed):
  ck-ch050 + *all* raw Vol2. At the 16 drafted Vol2 scenes today ≈ ~118k tok; projected
  full Vol2 (~25–30 scenes) pushes raw-Vol2 past ~200k tok and busts a 200k window
  before canon is even added. **Not Sonnet-safe as Vol2 grows** — the reason for the
  seam-checkpoint model above.

## Current operational state and approved 51-chapter cutover

`ck-ch060` now exists and is valid for the current 50-drafted-entry Vol1 sequence:
`ck-ch050` + raw ch51..60. The planned lap vignette does not enter any bundle or
invalidate those frozen artifacts while its chronology status remains Unwritten.

When the lap vignette is drafted, migrate the seam in one change set:

1. Mark the vignette Draft complete and add its slug to the legacy `FALL_SCENES`
   manifest at the same chronology position.
2. Mint each native final-Vol1 `ck-ch051` as a raw ch1..51 single pass.
3. Change the explicit first-Vol2 seed policy from `60: 50` to `60: 51`; the ck060
   raw span becomes ch52..60. Update its recipes and seam-contract tests together.
4. Remint native ck060, rebuild the core ensemble, and treat dependent donor reviews
   as stale until rerun against the new core checkpoint.

`checkpoint_plan()` fails closed if the first-Vol2 seed no longer equals the drafted
Vol1 endpoint, preventing the planned insertion from silently leaving ck050 as the
active seam.
