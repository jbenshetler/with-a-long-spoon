#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
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

Default source is the cross-vendor CONSENSUS memory (author ruling 2026-11-04), the
same memory the grounded cold-read panel and capture v3 read:
reviews/cold-read/fact-consensus/ck-ch<B>.reader.md (audited facts + agreed readings,
readings labelled as such). `--model consensus-facts` reads the facts-only
ck-ch<B>.md that capture v3 uses. Consensus checkpoints are never minted here: they
are built by tools/fact_consensus.py, whose Google/diversity slots are paid OpenRouter
lanes (author authorization required). A consensus checkpoint whose recorded
bundle-sha256 no longer matches the prose of ch1..B is reported STALE (same test as
capture_dag.fact_stale) and still loaded.

For a single-model checkpoint (`--model claude-opus-5-5` etc.): if the decade
checkpoint is missing it is minted first. Volume One checkpoints
read raw prose from the opening. A later-volume checkpoint consolidates the
frozen final checkpoint of the preceding volume plus raw current-volume prose;
every checkpoint in that volume uses the same frozen seed. Codex/OpenAI-family
models run via checkpoint_extract.py; Claude-family checkpoints use the
blind-extractor packet path, so the tool prints exact steps and exits.

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
import hashlib
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
    """Last decade checkpoint strictly before chapter n (0 if none)."""
    return ((n - 1) // decade) * decade


CONSENSUS = "consensus"              # facts + agreed readings (.reader.md)
CONSENSUS_FACTS = "consensus-facts"  # audited facts only (what capture v3 reads)


def is_consensus(model: str) -> bool:
    return model in (CONSENSUS, CONSENSUS_FACTS)


def ck_path(model: str, b: int) -> Path:
    if model == CONSENSUS:
        return REPO / f"reviews/cold-read/fact-consensus/ck-ch{b:03d}.reader.md"
    if model == CONSENSUS_FACTS:
        return REPO / f"reviews/cold-read/fact-consensus/ck-ch{b:03d}.md"
    return REPO / f"reviews/cold-read/{model}/checkpoints/ck-ch{b:03d}.md"


def is_stale(path: Path, b: int) -> bool | None:
    """Does the checkpoint's recorded bundle-sha256 still match the prose of ch1..b?
    None when the checkpoint records no bundle hash."""
    recorded = checkpoint_bundle.checkpoint_metadata(path.read_text(), "bundle-sha256")
    if not recorded:
        return None
    current = hashlib.sha256(
        checkpoint_bundle.build_reader_bundle(b, start=1).encode()).hexdigest()
    return recorded != current


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


def _claude_mint_steps(rel: Path, packet_hint: str) -> str:
    return (
        "Claude-family checkpoints are minted by a blind-extractor subagent "
        "(no API tokens),\nwhich a CLI can't spawn — so the assistant runs it:\n"
        f"  1. {packet_hint}\n"
        "  2. Run a blind-extractor subagent against every packet part in order; "
        "it must consolidate the supplied prior checkpoint and raw span.\n"
        f"  3. Save its output to {rel} with the packet's standard checkpoint header.\n"
        "Then re-run this command.\n"
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

    if is_consensus(model):
        if mint_mode == "never":
            print(f"[missing] {rel} (--no-mint); proceeding without the checkpoint.",
                  file=sys.stderr)
            return None
        sys.stderr.write(
            f"[missing] {rel} — consensus checkpoints are built by "
            f"tools/fact_consensus.py --to {b}\n(paid OpenRouter slots: needs the author's "
            f"authorization). Re-run with --no-mint to proceed without it.\n")
        raise SystemExit(MINT_NEEDED)

    if b > drafted_count:
        print(f"[note] {rel} can't be minted yet — {drafted_count} chapters drafted, ch1..ch{b} "
              f"needed. Proceeding on recent prose only; a later editing pass will catch up.",
              file=sys.stderr)
        return None

    if mint_mode == "never":
        print(f"[missing] {rel} (--no-mint); proceeding without the checkpoint.", file=sys.stderr)
        return None

    seed_boundary, raw_start = checkpoint_bundle.checkpoint_plan(b)
    if seed_boundary is not None and not ck_path(model, seed_boundary).exists():
        ensure_checkpoint(model, seed_boundary, mint_mode, drafted_count)

    source_description = (
        f"ck-ch{seed_boundary:03d} + raw ch{raw_start:03d}..ch{b:03d}"
        if seed_boundary is not None
        else f"raw ch001..ch{b:03d}"
    )
    accept = True if mint_mode == "always" else _ask(
        f"[missing] {rel}\nCreate this decade checkpoint now "
        f"(reads {source_description})? [y/N] "
    )
    packet_hint = (
        f"tools/cold_read_grounded.py --model-id {model} "
        f"--emit-bundle-packet {b}"
    )
    if accept is None:
        sys.stderr.write(
            f"[missing] {rel} — offering to create it.\n"
            + (
                _claude_mint_steps(rel, packet_hint)
                if is_claude(model)
                else "Re-run with --mint to create it via checkpoint_extract "
                f"(reads {source_description}),\nor --no-mint to proceed without it.\n"
            )
        )
        raise SystemExit(MINT_NEEDED)
    if not accept:
        print(f"[skipped] {rel} not created; proceeding without the checkpoint.", file=sys.stderr)
        return None

    if is_claude(model):
        sys.stderr.write(_claude_mint_steps(rel, packet_hint))
        raise SystemExit(MINT_NEEDED)

    extract_args = ["--model", model, "--from", str(raw_start), "--to", str(b)]
    if seed_boundary is not None:
        extract_args.extend(
            [
                "--reader-sequence",
                "--seed-checkpoint",
                str(ck_path(model, seed_boundary)),
            ]
        )
    print(
        f"[mint] {rel} absent — minting via checkpoint_extract "
        f"(model={model}, {source_description}); this takes a while…",
        file=sys.stderr,
    )
    subprocess.run([str(REPO / "tools/checkpoint_extract.py"), *extract_args], check=True)
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
    tgt = ap.add_mutually_exclusive_group(required=True)
    tgt.add_argument("--to", dest="n", type=int,
                     help="chapter being drafted (N, drafted reading order); context covers everything before it")
    tgt.add_argument("--scene", dest="scene",
                     help="scene slug; resolves N for you (drafted reading order — works even if the "
                          "target scene is itself undrafted). Prefer this over --to.")
    ap.add_argument("--model", default=CONSENSUS,
                    help="checkpoint source: consensus (default; facts + readings), "
                         "consensus-facts (facts only), or a model id for a single-model "
                         "checkpoint (e.g. claude-opus-5-5)")
    ap.add_argument("--keep", default=None,
                    help="comma-separated section aliases to keep (overrides DEFAULT_KEEP)")
    ap.add_argument("--drop", default=None, help="comma-separated section aliases to drop")
    ap.add_argument("--decade", type=int, default=DECADE,
                    help="checkpoint stride (default 10; override only for an explicit "
                         "legacy fallback when a required seam checkpoint has not been minted)")
    ap.add_argument("--check", action="store_true", help="report the load plan; emit nothing")
    mint = ap.add_mutually_exclusive_group()
    mint.add_argument("--mint", action="store_true",
                      help="create a missing checkpoint without asking (codex mints directly; "
                           "Claude hands off to a blind-extractor subagent)")
    mint.add_argument("--no-mint", action="store_true",
                      help="never create; proceed without a missing checkpoint")
    args = ap.parse_args()
    mint_mode = "always" if args.mint else "never" if args.no_mint else "ask"

    n = args.n if args.n is not None else checkpoint_bundle.volume_scenes.chapter_number(args.scene)
    if n < 1:
        raise SystemExit("[error] resolved chapter N must be >= 1")
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
            if not p.exists():
                state = "MISSING → fact_consensus.py (paid)" if is_consensus(args.model) else "MISSING → mint"
            else:
                stale = is_stale(p, b)
                state = "present" + (" · STALE: prose ch1..ch%d changed since it was built" % b
                                     if stale else "" if stale is False else " · no bundle hash recorded")
            print(f"checkpoint       : {p.relative_to(REPO)}  [{state}]")
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
            stale = is_stale(path, b)
            note = ""
            if stale:
                note = f" [STALE: prose ch1..ch{b} changed since it was built]"
                print(f"[warn] STALE FACTS — {path.relative_to(REPO)}{note}", file=sys.stderr)
            out.append(f"===== MEMORY CHECKPOINT (consolidated reader-memory through ch{b}){note} =====\n")
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
