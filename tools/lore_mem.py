#!/usr/bin/env python3
"""lore_mem.py — inspect and clear the lore-keeper subagent's persistent memory.

The lore-keeper keeps hand-authored notes under .claude/agent-memory/lore-keeper/.
Unlike the na.py search *index* (which `reindex` rebuilds from disk and self-heals
on renames/deletes), these notes are NOT derived from disk — so a renamed or deleted
scene can leave a stale pointer here that nothing purges automatically. This tool
finds and clears those.

Subcommands:
  check              flag notes that reference a *.md file no longer on disk
  list               list notes with sizes
  grep TERM          show notes/lines containing TERM (case-insensitive)
  forget TERM        show notes referencing TERM;
                       --to NEW   rewrite TERM -> NEW in place
                       --delete   remove note files containing TERM  (needs --yes)
  wipe --all         delete every note (git rm for tracked files)     (needs --yes)

Git note: the memory dir is git-ignored, but a few notes may be tracked-despite-ignore
(committed before the ignore rule). Deletions are git-aware: tracked files go through
`git rm`, everything else is a plain unlink.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AGENT = "lore-keeper"
MD_REF = re.compile(r"[\w./-]+\.md")


def mem_dir(agent: str) -> Path:
    return REPO_ROOT / ".claude" / "agent-memory" / agent


def notes(agent: str) -> list[Path]:
    d = mem_dir(agent)
    return sorted(d.glob("*.md")) if d.is_dir() else []


def human(n: int) -> str:
    f = float(n)
    for unit in ("B", "K", "M"):
        if f < 1024 or unit == "M":
            return f"{f:.0f}{unit}" if unit == "B" else f"{f:.1f}{unit}"
        f /= 1024
    return f"{f:.1f}M"


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True
    )


def is_tracked(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT)
    return git("ls-files", "--error-unmatch", str(rel)).returncode == 0


def remove(path: Path) -> str:
    """Delete a note, git-aware. Returns 'git rm' or 'rm' for reporting."""
    if is_tracked(path):
        git("rm", "-f", "--quiet", str(path.relative_to(REPO_ROOT)))
        return "git rm"
    path.unlink()
    return "rm"


# --- disk index for staleness -------------------------------------------------

def disk_md_basenames() -> set[str]:
    return {
        p.name
        for p in REPO_ROOT.rglob("*.md")
        if ".git" not in p.parts
    }


def ref_resolves(ref: str, known: set[str]) -> bool:
    if Path(ref).name in known:
        return True
    return (REPO_ROOT / ref).exists()


def rename_hint(ref: str, known: set[str]) -> str:
    """If dropping a leading article from the basename lands on a real file,
    the ref is probably a stale rename rather than a planned-undrafted scene."""
    name = Path(ref).name
    for art in ("the-", "a-"):
        if name.startswith(art) and name[len(art):] in known:
            return name[len(art):]
    return ""


# --- subcommands --------------------------------------------------------------

def cmd_check(args) -> int:
    known = disk_md_basenames()
    stale: list[tuple[Path, int, str, str]] = []
    for note in notes(args.agent):
        for i, line in enumerate(note.read_text().splitlines(), 1):
            for ref in MD_REF.findall(line):
                if not ref_resolves(ref, known):
                    stale.append((note, i, ref, line.strip()))
    if not stale:
        print(f"ok — no stale .md references in {args.agent} memory")
        return 0
    renamed = sum(1 for _, _, ref, _ in stale if rename_hint(ref, known))
    print(f"dangling .md references in {args.agent} memory ({len(stale)}):\n")
    for note, i, ref, line in stale:
        rel = note.relative_to(REPO_ROOT)
        hint = rename_hint(ref, known)
        tag = f"  (renamed? -> {hint})" if hint else ""
        print(f"  {rel}:{i}  ->  {ref}{tag}")
        print(f"      {line}")
    print(
        f"\n  {len(stale)} dangling, {renamed} look like renames (article-stripped "
        "match on disk).\n  The rest may be planned-not-yet-drafted scenes the memory "
        "legitimately\n  references — eyeball before forgetting.\n"
        f"  fix a rename: lore_mem.py forget {stale[0][2]} --to <new-name>.md"
    )
    return 1


def cmd_list(args) -> int:
    ns = notes(args.agent)
    if not ns:
        print(f"(no notes in {args.agent} memory)")
        return 0
    total = 0
    for note in ns:
        size = note.stat().st_size
        total += size
        tag = " [tracked]" if is_tracked(note) else ""
        print(f"  {human(size):>7}  {note.name}{tag}")
    print(f"\n  {len(ns)} notes, {human(total)} total  ({mem_dir(args.agent)})")
    return 0


def cmd_grep(args) -> int:
    term = args.term.lower()
    hits = 0
    for note in notes(args.agent):
        for i, line in enumerate(note.read_text().splitlines(), 1):
            if term in line.lower():
                print(f"  {note.name}:{i}  {line.strip()}")
                hits += 1
    print(f"\n  {hits} line(s) match {args.term!r}")
    return 0 if hits else 1


def _notes_containing(agent: str, term: str) -> list[tuple[Path, int]]:
    """Return (note, match_count) for notes containing term (case-insensitive)."""
    out = []
    low = term.lower()
    for note in notes(agent):
        c = note.read_text().lower().count(low)
        if c:
            out.append((note, c))
    return out


def cmd_forget(args) -> int:
    if args.to and args.delete:
        print("error: use either --to or --delete, not both", file=sys.stderr)
        return 2
    matches = _notes_containing(args.agent, args.term)
    if not matches:
        print(f"no notes reference {args.term!r} — nothing to forget")
        return 0

    if args.to:
        changed = 0
        for note, _ in matches:
            text = note.read_text()
            new = text.replace(args.term, args.to)
            if new != text:
                note.write_text(new)
                changed += text.count(args.term)
                print(f"  rewrote {note.name}: {args.term!r} -> {args.to!r}")
        print(f"\n  {changed} occurrence(s) rewritten in {len(matches)} note(s)")
        return 0

    if args.delete:
        if not args.yes:
            print(
                f"would delete {len(matches)} note(s) containing {args.term!r}:",
                file=sys.stderr,
            )
            for note, c in matches:
                print(f"  {note.name}  ({c} hit(s))", file=sys.stderr)
            print("\nre-run with --yes to delete", file=sys.stderr)
            return 2
        for note, _ in matches:
            how = remove(note)
            print(f"  {how}  {note.name}")
        print(f"\n  deleted {len(matches)} note(s)")
        return 0

    # report mode
    print(f"notes referencing {args.term!r}:")
    for note, c in matches:
        print(f"  {note.name}  ({c} hit(s))")
    print(
        f"\n  {len(matches)} note(s). "
        "Rewrite with --to <new>, or remove with --delete --yes."
    )
    return 0


def cmd_wipe(args) -> int:
    if not args.all:
        print("error: refusing to wipe without --all", file=sys.stderr)
        return 2
    ns = notes(args.agent)
    if not ns:
        print(f"(no notes in {args.agent} memory — nothing to wipe)")
        return 0
    if not args.yes:
        print(
            f"would delete ALL {len(ns)} note(s) in {args.agent} memory:",
            file=sys.stderr,
        )
        for note in ns:
            tag = " [tracked]" if is_tracked(note) else ""
            print(f"  {note.name}{tag}", file=sys.stderr)
        print("\nre-run with --all --yes to wipe", file=sys.stderr)
        return 2
    for note in ns:
        how = remove(note)
        print(f"  {how}  {note.name}")
    print(f"\n  wiped {len(ns)} note(s) from {args.agent} memory")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        prog="lore_mem.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--agent", default=DEFAULT_AGENT,
        help=f"agent-memory subdir (default: {DEFAULT_AGENT})",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="flag notes referencing a *.md no longer on disk")
    sub.add_parser("list", help="list notes with sizes")

    g = sub.add_parser("grep", help="show notes/lines containing TERM")
    g.add_argument("term")

    f = sub.add_parser("forget", help="report/rewrite/delete notes referencing TERM")
    f.add_argument("term")
    f.add_argument("--to", metavar="NEW", help="rewrite TERM -> NEW in place")
    f.add_argument("--delete", action="store_true", help="delete notes containing TERM")
    f.add_argument("--yes", action="store_true", help="confirm a destructive op")

    w = sub.add_parser("wipe", help="delete every note (needs --all --yes)")
    w.add_argument("--all", action="store_true", help="required: wipe everything")
    w.add_argument("--yes", action="store_true", help="required: confirm")

    args = p.parse_args()
    return {
        "check": cmd_check,
        "list": cmd_list,
        "grep": cmd_grep,
        "forget": cmd_forget,
        "wipe": cmd_wipe,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
