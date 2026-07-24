# Cold Read — first-reader panel

Output of the `/cold-read` command: a blind, sequential reader's reaction to each
drafted chapter, plus an arc-level `SYNTHESIS.md`.

Each `<slug>.md` here is written by a `blind-reader` subagent that saw **only** the
chapter's title, its full text, and a carry-forward summary of the reader's
experience through the previous chapters — never the planning corpus, thesis, or
character bible. It is the instrument for the book's central craft rule ("earn the
dark by being light"): a first-time reader should fall for Pace as hard as Vee does
and should *not* suspect Randi until the pattern earns it. These files measure
whether that's landing.

Each file has two parts:

- **`## Reader reaction`** — the deliverable: how the chapter lands, to this point.
- **`## Carry-forward state`** — plumbing: the experiential reader-memory fed to the
  next chapter's reader. Editing the source scene re-arms this and makes every
  downstream file stale (the command warns you).

These are reader reactions, not canon and not craft verdicts — the judgment stays
with the author. Files are living (overwritten on re-review); git keeps history.
