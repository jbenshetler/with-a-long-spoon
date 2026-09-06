# Cold Read — first-reader panel

Blind first-reader reactions to drafted chapters. Each model sees only the
cover-board title, the volume packet at that volume's opening, grounded memory
of earlier chapters, the current chapter's display title, and clean prose. It
never sees planning material, author intent, future chapters, project
instructions, git state, or the memory index.

The grounded lane is the only live instrument. The old sequential
carry-forward lane is retired because facts decayed across repeated summaries;
its files remain frozen under each model's `chained/` directory.

## Authority and roster

- `SPEC.md` owns the file and harness contract.
- `ensemble-config.toml` owns the active panel, fast probe, reader memory
  policy, ensemble sources, and matcher.
- `.claude/commands/wals-cold-read.md` is the panel runbook.
- `.claude/commands/wals-cold-read-provider.md` is the paid OpenRouter runbook.

The active panel has eight readers: Fable, Opus, Sol, GPT-5.5, Kimi, GLM, Qwen,
and DeepSeek. Sonnet and Terra are retired from panel voting; Terra may act as
the non-voting ensemble matcher. Chronology ratings, embedded reviews, and
cast-vote bootstrapping use only the active roster.

Every OpenRouter call requires specific author authorization. A standing panel
slot is not authorization to spend.

## Layout

```
reviews/cold-read/
  README.md
  SPEC.md
  ensemble-config.toml
  volume-packets.toml
  checkpoint-ensembles/core/
    checkpoints/ck-ch<NNN>.md
    claims/ck-ch<NNN>.json
    manifests/ck-ch<NNN>.json
    conflicts/ck-ch<NNN>.json
  <model-id>/
    <slug>.md
    checkpoints/ck-ch<NNN>.md
    oracle/
    chained/
```

One canonical directory per reader model. Experimental provenance belongs in a
review's metadata header, never a parallel pseudo-model directory. Reader
reaction bodies remain verbatim.

## Grounded memory

For chapter $N$, boundary $B$ is the configured checkpoint boundary strictly
before $N$. The prompt contains:

1. the resolved checkpoint through $B$;
2. raw clean prose for chapters $B+1$ through $N-1$;
3. the clean prose of chapter $N$.

Volume 1 native checkpoints are high-effort cold passes over the complete raw
clean source through the boundary. After Volume 1, every in-volume checkpoint
is one consolidation hop from the same frozen final native checkpoint of the
prior volume plus all raw prose in the current volume through that boundary.
Thus Volume 2 `ck-ch060` uses `ck-ch050` + raw ch 51..60, while `ck-ch070`
again uses `ck-ch050` + raw ch 51..70, not `ck-ch060`. Qwen and DeepSeek are
donor-memory readers: both use the quote-backed, cross-vendor `core` ensemble
and cannot mint native checkpoints. Their review headers pin the ensemble hash.

The ensemble admits ordinary claims only with at least two of four source
checkpoints and at least two vendors. Minimal entity facts have a
source-verified exception; impressions and interpretations still need
cross-vendor quorum. Exact supporting checkpoint excerpts and exact clean-scene
evidence are checked deterministically. Source disagreement is retained, not
flattened.

## Producing and validating

```
tools/cold_read_grounded.py --check --model-id <id> --scope <slug>
tools/checkpoint_extract.py --model <native-model> --to 50
tools/checkpoint_extract.py --reader-sequence \
  --seed-checkpoint reviews/cold-read/<model-id>/checkpoints/ck-ch050.md \
  --from 51 --to 60 \
  --model <native-model> \
  --out reviews/cold-read/<model-id>/checkpoints/ck-ch060.md
tools/checkpoint_ensemble.py build --ensemble core --through <B>
tools/checkpoint_ensemble.py check --ensemble core --through <B>
tools/cold_read_grounded.py --model <provider/model> --model-id <id> --scope <slug>
```

Checkpoint extraction is high effort. Reader reactions are low effort. Paid
provider reactions cap output at 18k tokens; paid checkpoint extraction caps it
at 80k. Invalid, incomplete, truncated, reasoning-only, missing-section, or
out-of-order output is archived as diagnostics and never enters the review
corpus.

For every later-volume boundary, use `--reader-sequence`,
`--seed-checkpoint <frozen-final-prior-volume-native-checkpoint>`, and the raw
current-volume range `--from <volume-start> --to <boundary>`. Every checkpoint
within that volume reuses the same seed rather than chaining from the previous
decade checkpoint. Its provenance must pin the seed identity/hash and exact raw
range fingerprint. At an ensemble boundary, all native sources must cover the
same seed and raw-source provenance before matching.

## Currency and interpretation

A changed source checkpoint, manuscript bundle, cleaner, extractor prompt,
matcher contract, or ensemble configuration invalidates the ensemble and every
dependent donor review. `check` fails closed. Replacing a paid review still
requires explicit `--fresh` authorization.

The existing Qwen/DeepSeek `My Pleasure` pilot reactions are preserved in their
canonical model roots with explicit Fable-donor provenance. They predate the
ensemble and are excluded from current-panel chronology ratings until an
author-authorized `--fresh` ensemble-backed read replaces them.

Qwen and DeepSeek's historical-memory assertions are correlated when inherited
only from their shared ensemble and count once for corroboration. Their
reactions to the raw recent window and current chapter remain independent.

Cold reads are reactions, not canon and not craft verdicts. They flag reader
effects for authorial judgment; they never rewrite prose automatically.
