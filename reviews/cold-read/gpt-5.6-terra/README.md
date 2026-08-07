# gpt-5.6-terra — a spliced reader

**This run has a seam.** Chapters 1–8 were read by `claude-fable-5`; chapter 9
(`off-six-fourteen`) onward by `gpt-5.6-terra`, seeded with fable's
`may-i-choose.md` carry-forward. Author decision, 2026-08-06: the Anthropic
token budget ran out mid-book and the read was continued on another model
rather than restarted.

Chapters 1–8 in this directory are **verbatim copies** of the fable files and
keep their original `model: claude-fable-5` metadata line — so any file's
author is readable from the file itself. They are duplicated here (rather than
symlinked or omitted) because the harness seeds carry-forward only from the
receiving model's own directory, and because a synthesis over this run needs
the whole chain present.

## Reading this run

Treat it as **one continuous reader whose brain was swapped at chapter 9**, not
as a clean per-model instrument:

- Chapters 1–8 are **not** terra's reactions. Do not cite them as terra's, and
  do not use them in a cross-model comparison of chapters 1–8 — they are the
  same text as `claude-fable-5/`, and counting them twice would manufacture
  false agreement between two "models."
- Chapter 9 is the seam. Terra inherits fable's ledger — its who's-who, motif
  trail, and open questions — but none of fable's taste. A discontinuity in
  register or attention at exactly chapter 9 is an **artifact of the splice**,
  not a finding about the chapter.
- Chapters 9+ are usable as terra's own reads, with the caveat that terra's
  priors were set by another reader.

See `../SPEC.md` ("Model substitution mid-run") for the general rule.

## Provenance

- Routed through the **OpenAI API directly** (`tools/cold_read_openai.py`), not
  OpenRouter. Pricing compared at $2/$4 per 1M (OpenAI) vs $1/$6 (OpenRouter);
  the corpus runs ~1.3–1.7:1 input:output, below the 2:1 break-even, so direct
  is both cheaper and needs no Chat Completions port.
- The fable chapters 1–8 are from commit `c6b56c9` (the fresh re-run under the
  corrected cover title and fixed Fall manifest). The **stale** July fable
  reads for chapters 9+ were deliberately not copied.
