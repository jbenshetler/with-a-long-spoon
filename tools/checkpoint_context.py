#!/usr/bin/env python3
"""Assemble the AUTHORING CONTEXT for drafting a chapter: the most-recent decade
memory checkpoint (projected to the authoring keep-set) + the full clean prose of
every chapter since that checkpoint.

Read-time assembly only — it never mints a *new* consolidated checkpoint, so nothing
decays across a summary-of-a-summary chain. The decade checkpoint is read verbatim
(already panel-QA'd) and the recent window is real prose at full fidelity:

    boundary  B = ((N-1)//10)*10           # last decade checkpoint before chapter N
    context     = project(ck-ch{B})         # verbatim memory, reader-reaction sliced off
                + clean prose ch B+1..N-1    # full-fidelity recent window

The projection DROPS reader-reaction sections (default: Impression) so the drafting
model never *sees* them — withholding beats instructing it to ignore. The keep-set is
a config default (DEFAULT_KEEP) and overridable per run (--keep / --drop).

This is the authoring sibling of tools/cold_read_grounded.py (same boundary math and
checkpoint_bundle prose window), minus the reader prompt, plus the slicer. It emits
only the checkpoint + recent chapters; the AGENTS.md load-rule reads the meta/ canon
docs first, on its own, then runs this.

If the decade checkpoint is missing it is minted first: for codex/OpenAI-family models
via checkpoint_extract.py (reads prose 1..B — takes a while); Claude-family checkpoints
(opus/fable) are minted by a blind-extractor subagent that a CLI cannot spawn, so the
tool prints the exact steps and exits for the caller to mint, then re-run.

Usage:
  tools/checkpoint_context.py --to 60                     # opus (default), drafting ch60
  tools/checkpoint_context.py --to 60 --model gpt-5.6-terra
  tools/checkpoint_context.py --to 60 --check             # report the plan, emit nothing
  tools/checkpoint_context.py --to 60 --keep who,relationships,irony,motifs,symbolism,open,story
  tools/checkpoint_context.py --to 60 --drop impression,story
  tools/checkpoint_context.py --to 60 --no-mint           # never mint; fail if absent
Output (stdout): the assembled authoring context. Order/inventory: volume_scenes.py.
Runs under bare python3 (imports no tomllib); minting shells out to checkpoint_extract.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402  (clean prose window + reader_slugs; imports volume_scenes)

DECADE = 10
# Exit code the assistant catches: a checkpoint must be minted by a blind-extractor
# subagent (Claude models) that a CLI can't spawn, or the caller declined to pass a
# mint flag non-interactively. Distinct from 1 (hard error) so the load-rule can react.
MINT_NEEDED = 2

# Canonical checkpoint sections -> CLI alias. DEFAULT_KEEP is the authoring keep-set;
# edit it (or pass --keep/--drop) to re-cut. "impression" is dropped by default: it is
# pure reader reaction and the section most likely to be mistaken for canon by a
# drafting model. An UNRECOGNIZED section is kept (and warned) — safer to over-include
# than to silently drop something a future checkpoint schema adds.
SECTIONS = {
    "who":           "who's who",
    "relationships": "relationships",
    "irony":         "what i know that they don't",
    "motifs":        "motifs & images",
    "symbolism":     "symbolism",
    "open":          "open questions",
    "story":         "story so far",
    "impression":    "impression",
}
DEFAULT_KEEP = ["who", "relationships", "irony", "motifs", "symbolism", "open", "story"]


def boundary(n: int, decade: int = DECADE) -> int:
    """Last decade checkpoint strictly before chapter n (0 if none). `decade` is the
    checkpoint stride: 10 by default, but a post-Vol1 chapter with no decade checkpoint
    yet past ck-ch050 runs with --decade 50 so the boundary stays at ck-ch050 and the
    recent window is the raw prose of the current volume so far (the interim scheme,
    until the next volume-seam checkpoint is minted — see meta-tooling-checkpoints.md)."""
    return ((n - 1) // decade) * decade


def ck_path(model: str, b: int) -> Path:
    return REPO / f"reviews/cold-read/{model}/checkpoints/ck-ch{b:03d}.md"


def is_claude(model: str) -> bool:
    return model.startswith("claude")


# ---- checkpoint projection (the slicer) -----------------------------------------

def _split_sections(text: str):
    """Return (preamble, [(heading_line, [body_lines]), ...]) splitting on `### `."""
    lines = text.splitlines()
    i = 0
    pre: list[str] = []
    while i < len(lines) and not lines[i].startswith("### "):
        pre.append(lines[i])
        i += 1
    secs: list[tuple[str, list[str]]] = []
    head: str | None = None
    body: list[str] = []
    for ln in lines[i:]:
        if ln.startswith("### "):
            if head is not None:
                secs.append((head, body))
            head, body = ln, []
        else:
            body.append(ln)
    if head is not None:
        secs.append((head, body))
    return "\n".join(pre), secs


def _section_key(heading: str) -> str | None:
    norm = heading[4:].strip().lower().rstrip(".")
    for key, canon in SECTIONS.items():
        if norm == canon:
            return key
    for key, canon in SECTIONS.items():
        if canon in norm or norm in canon:
            return key
    return None


def project(text: str, keep: list[str]) -> str:
    """Reassemble the checkpoint keeping only sections whose canonical key is in `keep`."""
    pre, secs = _split_sections(text)
    blocks: list[str] = []
    if pre.strip():
        blocks.append(pre.strip())
    for head, body in secs:
        key = _section_key(head)
        if key is None:
            print(f"[warn] unrecognized checkpoint section kept: {head!r}", file=sys.stderr)
            keep_it = True
        else:
            keep_it = key in keep
        if keep_it:
            blocks.append((head + "\n" + "\n".join(body)).rstrip())
    return "\n\n".join(blocks).strip() + "\n"


# ---- minting (self-heal) --------------------------------------------------------

def _ask(msg: str):
    """y/N prompt → True/False, or None when we can't ask (non-interactive stdin)."""
    if not sys.stdin.isatty():
        return None
    try:
        return input(msg).strip().lower() in ("y", "yes")
    except EOFError:
        return None


def _claude_mint_steps(rel: Path, bundle_hint: str) -> str:
    return (
        f"Claude-family checkpoints are minted by a blind-extractor subagent (no API tokens),\n"
        f"which a CLI can't spawn — so the assistant runs it:\n"
        f"  1. {bundle_hint}\n"
        f"  2. Run a blind-extractor subagent (.claude/agents/blind-extractor.md as the system\n"
        f"     prompt, the bundle as the message) — consolidate cold, no prior checkpoint.\n"
        f"  3. Save its output to {rel} with the standard checkpoint header.\n"
        f"Then re-run this command.\n"
    )


def ensure_checkpoint(model: str, b: int, mint_mode: str, drafted_count: int):
    """Return the checkpoint Path, or None to proceed without it. Exits MINT_NEEDED when a
    checkpoint should be minted but the CLI can't (Claude subagent) or wasn't told to
    (non-interactive, no --mint/--no-mint) — the load-rule catches this and offers to mint.
    An undrafted decade (b > drafted_count) is a normal mid-draft state: it just proceeds
    on the recent prose, since editing will catch up."""
    path = ck_path(model, b)
    if path.exists():
        return path
    rel = path.relative_to(REPO)

    if b > drafted_count:
        print(f"[note] {rel} can't be minted yet — {drafted_count} chapters drafted, ch1..ch{b} "
              f"needed. Proceeding on recent prose only; a later editing pass will catch up.",
              file=sys.stderr)
        return None

    if mint_mode == "never":
        print(f"[missing] {rel} (--no-mint); proceeding without the checkpoint.", file=sys.stderr)
        return None

    accept = True if mint_mode == "always" else _ask(
        f"[missing] {rel}\nCreate this decade checkpoint now (reads ch1..ch{b})? [y/N] ")

    bundle_hint = f"tools/checkpoint_bundle.py --to {b} > /tmp/ck-bundle-{model}-ch{b:03d}.md"
    if accept is None:  # non-interactive, undecided: offer and hand off to the assistant
        sys.stderr.write(
            f"[missing] {rel} — offering to create it.\n"
            + (_claude_mint_steps(rel, bundle_hint) if is_claude(model)
               else f"Re-run with --mint to create it via checkpoint_extract (reads ch1..ch{b}),\n"
                    f"or --no-mint to proceed without it.\n"))
        raise SystemExit(MINT_NEEDED)
    if not accept:
        print(f"[skipped] {rel} not created; proceeding without the checkpoint.", file=sys.stderr)
        return None

    if is_claude(model):
        tmp = Path(f"/tmp/ck-bundle-{model}-ch{b:03d}.md")
        tmp.write_text(checkpoint_bundle.build_bundle(1, b, jacket=True, slugs=checkpoint_bundle.reader_slugs()))
        sys.stderr.write(f"[mint] bundle written to {tmp}.\n"
                         + _claude_mint_steps(rel, f"bundle ready at {tmp}"))
        raise SystemExit(MINT_NEEDED)

    print(f"[mint] {rel} absent — minting via checkpoint_extract (model={model}, --to {b}); "
          f"this reads {b} chapters at high effort and takes a while…", file=sys.stderr)
    subprocess.run([str(REPO / "tools/checkpoint_extract.py"),
                    "--model", model, "--to", str(b)], check=True)
    if not path.exists():
        raise SystemExit(f"[error] mint reported success but {rel} not found")
    return path


# ---- assembly -------------------------------------------------------------------

def resolve_keep(keep_arg: str | None, drop_arg: str | None) -> list[str]:
    keep = list(DEFAULT_KEEP) if keep_arg is None else _aliases(keep_arg)
    for k in _aliases(drop_arg) if drop_arg else []:
        if k in keep:
            keep.remove(k)
    return keep


def _aliases(s: str) -> list[str]:
    out = []
    for tok in s.split(","):
        tok = tok.strip().lower()
        if not tok:
            continue
        if tok not in SECTIONS:
            raise SystemExit(f"[error] unknown section alias {tok!r}; known: {', '.join(SECTIONS)}")
        out.append(tok)
    return out


def _window_note(win_start: int, win_end: int, win_end_req: int, b: int) -> str:
    """Calm note when the recent window can't be fully filled — a normal mid-draft state,
    not an error: undrafted-ahead chapters get caught in a later editing pass."""
    if win_start <= win_end:
        return (f"[note] recent window would reach ch{win_end_req}; ch{win_end + 1}..ch{win_end_req} "
                f"not drafted yet — including ch{win_start}..ch{win_end}. Undrafted-ahead is fine "
                f"mid-draft.")
    return (f"[note] nothing drafted yet between ch{b} and ch{win_end_req + 1}; proceeding without "
            f"a recent-prose window. Undrafted-ahead is fine mid-draft.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--to", dest="n", type=int, required=True,
                    help="chapter being drafted (N); context covers everything before it")
    ap.add_argument("--model", default="claude-opus-4-8",
                    help="checkpoint model id (default: opus; e.g. claude-fable-5, gpt-5.6-terra)")
    ap.add_argument("--keep", default=None,
                    help="comma-separated section aliases to keep (overrides DEFAULT_KEEP)")
    ap.add_argument("--drop", default=None, help="comma-separated section aliases to drop")
    ap.add_argument("--decade", type=int, default=DECADE,
                    help="checkpoint stride (default 10; use 50 for a post-Vol1 chapter with "
                         "no decade checkpoint yet past ck-ch050 — boundary stays at ck-ch050 "
                         "and the window is the current volume's raw prose so far)")
    ap.add_argument("--check", action="store_true", help="report the load plan; emit nothing")
    mint = ap.add_mutually_exclusive_group()
    mint.add_argument("--mint", action="store_true",
                      help="create a missing checkpoint without asking (codex mints directly; "
                           "Claude hands off to a blind-extractor subagent)")
    mint.add_argument("--no-mint", action="store_true",
                      help="never create; proceed without a missing checkpoint")
    args = ap.parse_args()
    mint_mode = "always" if args.mint else "never" if args.no_mint else "ask"

    n = args.n
    if n < 1:
        raise SystemExit("[error] --to must be >= 1")
    b = boundary(n, args.decade)
    keep = resolve_keep(args.keep, args.drop)

    drafted = checkpoint_bundle.reader_slugs()
    win_start = b + 1
    win_end_req = n - 1
    win_end = min(win_end_req, len(drafted))
    truncated = win_end_req > len(drafted)

    if args.check:
        print(f"drafting chapter : {n}  (of {len(drafted)} drafted across all volumes)")
        print(f"checkpoint stride: {args.decade}")
        print(f"decade boundary  : B = {b}" + ("  (no checkpoint — pre-decade)" if b < DECADE else ""))
        if b >= DECADE:
            p = ck_path(args.model, b)
            print(f"checkpoint       : {p.relative_to(REPO)}  [{'present' if p.exists() else 'MISSING → mint'}]")
        print(f"keep sections    : {', '.join(keep)}")
        print(f"drop sections    : {', '.join(k for k in SECTIONS if k not in keep)}")
        if win_start > win_end:
            print(f"recent window    : (none drafted yet between ch{b} and ch{n})")
        else:
            print(f"recent window    : ch{win_start}..ch{win_end} (full clean prose)")
        if truncated:
            print(_window_note(win_start, win_end, win_end_req, b))
        return

    if truncated:
        print(_window_note(win_start, win_end, win_end_req, b), file=sys.stderr)

    out: list[str] = []
    if b >= DECADE:
        path = ensure_checkpoint(args.model, b, mint_mode, len(drafted))
        if path is not None:
            out.append(f"===== MEMORY CHECKPOINT (consolidated reader-memory through ch{b}) =====\n")
            out.append(project(path.read_text(), keep))

    if win_start <= win_end:
        window = checkpoint_bundle.build_bundle(win_start, win_end, jacket=False, slugs=drafted)
        out.append(f"\n===== RECENT CHAPTERS (ch{win_start}..ch{win_end}, full clean prose) =====\n")
        out.append(window)

    if not out:
        print(f"[note] chapter {n} has nothing before it — no context to assemble.", file=sys.stderr)
        return
    sys.stdout.write("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    main()
