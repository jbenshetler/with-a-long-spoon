#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Find references orphaned by an edit — text that still points at something
the revision removed.

The defect class, from `the-pointing-game.md`: commit ade99b4b cut the whole
paragraph introducing a passer-by "in a camel coat too warm for the afternoon",
including Randi's verdict "She'd be a project." A later sentence still reads
"the closed camel-coat project would never laugh at anything in public" — a
callback to a character and a coinage the reader now never sees.

No reader-side instrument can catch this. Read as it now stands the sentence
parses fine as an archetype; the evidence is not in the text, it is in the
diff. So this is git archaeology, not a model: for every commit touching a
scene, take the distinctive terms that the commit REMOVED and did not re-add,
and report the ones that still appear in the chapter today.

Deliberately mechanical and deterministic — it costs nothing, so it can run as
a pre-commit warning. Like the style linter it FLAGS, never fixes, and it
over-flags on purpose: a surviving term is often a legitimate ordinary use.
The author judges.

Usage:
    tools/orphan_refs.py                  # Volume One, whole history
    tools/orphan_refs.py --volume 2
    tools/orphan_refs.py --staged         # pre-commit mode: only staged scenes
    tools/orphan_refs.py --max-df 3       # tighten/loosen the rarity filter
    tools/orphan_refs.py --slugs X --ack --fp <hash> --note "why"
                                          # record a ruling; the hash is the [#…] tag.
                                          # Without --fp, acks EVERY hit in scope.
    tools/orphan_refs.py --show-suppressed # re-show acknowledged hits, marked ✓
    tools/orphan_refs.py --unack --fp <hash>   # reverse (or --slugs X for a chapter)
    tools/orphan_refs.py --prune-allow [--yes] # drop rulings that match no hit in
                                          # the chapters scanned; dry run without --yes
    Rulings live in audits/orphan-refs/orphan-allow.toml (versioned; --allow overrides).

--ack records an authorial decision — run it only after the author has signed
off on each hit. FLAGS, never findings.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tomllib
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import volume_scenes  # noqa: E402  (stdlib-only)

# Unigrams this common carry no referential weight even when rare in the corpus.
STOP = set("""a an the and or but so then than that this these those of in on at to for with
from by as is was were be been being it its it's he she they them his her their you your i me my
we us our not no nor if when while after before again once here there all any both each few more
most other some such only own same too very can will just should now what which who whom whose how
why where said says say into out up down over under through about against between during without
within along across behind beyond off near upon around back still even also like unless until
because since though although whether one two three first last next another every""".split())

WORD_RE = re.compile(r"[a-z0-9']+")


def norm(text: str) -> list[str]:
    """Lowercase word tokens. Hyphens become breaks so `camel-coat` and
    `camel coat` are the same two tokens — the camel case turns on exactly
    that, since the edit removed the spaced form and the hyphenated one
    survived."""
    return WORD_RE.findall(text.lower().replace("-", " ").replace("—", " "))


def terms(text: str) -> set[str]:
    """Distinctive unigrams plus every bigram. Bigrams carry most of the
    signal: `camel coat` is specific where `camel` and `coat` are not."""
    toks = norm(text)
    out = {t for t in toks if t not in STOP and len(t) > 2}
    out |= {f"{a} {b}" for a, b in zip(toks, toks[1:])}
    return out


DEFINITE = {"the", "that", "those", "this", "these", "her", "his", "their",
            "its", "another", "same", "other"}


def is_definite(line: str, term: str) -> bool:
    """Does this occurrence point BACK at something?

    A dangling reference is definite — "the closed camel-coat project" assumes
    a project the reader has met. An indefinite or bare use ("a camel coat",
    "live inside") introduces or merely describes, and is not evidence of a
    missing antecedent. This is the filter that separates the real orphan from
    every ordinary phrase a revision happened to touch.
    """
    toks = norm(line)
    want = term.split()
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            # allow intervening adjectives: "the closed camel-coat project"
            if any(w in DEFINITE for w in toks[max(0, i - 2):i]):
                return True
    return False


INDEF = {"a", "an"}


def introduced_in(text: str, term: str) -> bool:
    """Did this text INTRODUCE the term — "a camel coat", "an old bench"?

    This is the other half of the defect and the one that makes it precise.
    An orphan is not merely a phrase a revision touched; it is an antecedent
    that was cut. The signature is an indefinite introduction in the removed
    text ("in a camel coat too warm for the afternoon") paired with a definite
    callback that survived ("the closed camel-coat project"). Requiring both
    ends drops the ordinary verb-phrase churn that any rewrite produces.
    """
    toks = norm(text)
    want = term.split()
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            if any(w in INDEF for w in toks[max(0, i - 3):i]):
                return True
    return False


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True).stdout


def document_frequency(slugs: list[str]) -> Counter:
    """How many chapters each term appears in. A term spread across the book is
    ambient texture; the interesting orphan is concentrated."""
    df: Counter = Counter()
    for s in slugs:
        p = REPO / "scenes" / f"{s}.md"
        if p.exists():
            df.update(terms(p.read_text(encoding="utf-8")))
    return df


def commits_for(path: str) -> list[str]:
    out = git("log", "--format=%H", "--", path)
    return [ln for ln in out.splitlines() if ln.strip()]


def diff_terms(sha: str, path: str) -> tuple[set[str], set[str], str]:
    """(removed terms, added terms, raw removed text) for one commit."""
    diff = git("show", "--format=", "--unified=0", sha, "--", path)
    removed, added = [], []
    for line in diff.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    cut = "\n".join(removed)
    return terms(cut), terms("\n".join(added)), cut


def _fingerprint(slug: str, term: str, norm_line: str) -> str:
    """Content-anchored fingerprint: (slug, term, normalized line text).
    Stable across line shifts; re-arms on edits. Line NUMBER and commit sha
    are deliberately NOT included."""
    fp_text = f"orphan\x00{slug}\x00{term}\x00{norm_line}"
    return hashlib.sha256(fp_text.encode("utf-8")).hexdigest()[:12]


def _toml_str(v: str) -> str:
    """Minimal TOML basic-string emitter for hand-written allowlist."""
    v = v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
    return f'"{v}"'


def load_allow(path: Path) -> dict[str, dict]:
    """fp -> entry. Missing file = empty allowlist (nothing suppressed yet)."""
    if not path.exists():
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        sys.exit(f"ERROR: cannot parse {path}: {e}")
    return {e["fp"]: e for e in data.get("ok", []) if e.get("fp")}


def save_allow(path: Path, entries: dict[str, dict]) -> None:
    """Rewrite the allowlist atomically (temp + os.replace), entries sorted for
    a stable git diff."""
    lines = [
        "# orphan-allow.toml — acknowledged orphan-refs hits (reviewed and accepted).",
        "# Each [[ok]] suppresses one (chapter, term, line) by content fingerprint:",
        "# stable across line shifts; editing the line re-arms it. `cut_by` (the commit",
        "# that orphaned the term) is context only — NOT part of the fingerprint.",
        "# Written by `orphan_refs.py --ack`; view hidden hits with `--show-suppressed`.",
        "# Entries for findings not currently flagged are KEPT on purpose; only --prune-allow removes them.",
        "",
    ]
    for e in sorted(entries.values(), key=lambda x: (x.get("slug", ""), x["term"], x["fp"])):
        lines.append("[[ok]]")
        lines.append(f'fp     = {_toml_str(e["fp"])}')
        lines.append(f'slug   = {_toml_str(e.get("slug", ""))}')
        lines.append(f'term   = {_toml_str(e["term"])}')
        lines.append(f'text   = {_toml_str(e.get("text", ""))}')
        lines.append(f'cut_by = {_toml_str(e.get("cut_by", ""))}')
        lines.append(f'note   = {_toml_str(e.get("note", ""))}')
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("\n".join(lines), encoding="utf-8")
    os.replace(tmp, path)


def _fp_match(fp: str, prefixes: list[str]) -> bool:
    """A --fp filter matches by prefix, so a short hash from the report works."""
    return any(fp.startswith(p) for p in prefixes)


def scan(slug: str, df: Counter, max_df: int, max_hits: int,
         definite_only: bool = True) -> list[dict]:
    path = f"scenes/{slug}.md"
    current = (REPO / path)
    if not current.exists():
        return []
    text = current.read_text(encoding="utf-8")
    live = terms(text)
    lines = text.splitlines()
    findings = []
    seen: set[str] = set()
    for sha in commits_for(path):
        removed, added, cut_text = diff_terms(sha, path)
        # Removed and NOT re-added by the same commit (else it merely moved),
        # yet still present in the chapter today.
        for t in sorted((removed - added) & live):
            if t in seen or df[t] > max_df:
                continue
            if definite_only and not introduced_in(cut_text, t):
                continue   # the cut did not introduce it; not an antecedent
            seen.add(t)
            hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
                    if not ln.startswith("#")
                    and t in " ".join(norm(ln))
                    and (not definite_only or is_definite(ln, t))]
            # An orphan is a LONE dangling reference. A term still used several
            # times is doing ordinary work; only the survivor-of-a-cut reads as
            # a callback to something gone.
            if not hits or len(hits) > max_hits:
                continue
            subject = git("show", "--format=%s", "-s", sha).strip()
            findings.append({"slug": slug, "term": t, "sha": sha[:8],
                             "subject": subject, "df": df[t], "hits": hits})
    return findings


def orphan_ack(args, allow_path: Path, allow: dict[str, dict], in_scope: list[dict]) -> None:
    """Acknowledge every hit in scope (already narrowed by --fp). Hits already
    acknowledged keep their original entry and note — never overwritten."""
    if not args.note:
        sys.exit("ERROR: --ack requires --note")
    added = 0
    for h in in_scope:
        if h["fp"] in allow:
            continue
        allow[h["fp"]] = dict(fp=h["fp"], slug=h["slug"], term=h["term"],
                              text=" ".join(h["text"].split()), cut_by=h["sha"],
                              note=args.note)
        added += 1
    if added:
        save_allow(allow_path, allow)
    already = len(in_scope) - added
    print(f"acknowledged {added} hit{'s' if added != 1 else ''} "
          f"({already} already suppressed) → {allow_path.name}; "
          f"{len(allow)} total suppressed")


def orphan_unack(args, allow_path: Path) -> None:
    """Remove allowlist entries by --fp and/or --slugs. Requires a filter."""
    allow = load_allow(allow_path)
    if not (args.fp or args.slugs):
        sys.exit("ERROR: --unack needs a filter (--fp <hash> and/or --slugs <slug>).")
    slugs = set(args.slugs) if args.slugs else None
    keep, removed = {}, 0
    for fp, e in allow.items():
        hit = (not args.fp or _fp_match(fp, args.fp)) and (slugs is None or e.get("slug") in slugs)
        if hit:
            removed += 1
        else:
            keep[fp] = e
    if removed:
        save_allow(allow_path, keep)
    print(f"un-acknowledged {removed} entr{'y' if removed == 1 else 'ies'} "
          f"→ {allow_path.name}; {len(keep)} remain")


def orphan_prune_allow(args, allow_path: Path, all_hits: list[dict],
                       slugs: list[str]) -> None:
    """List allow entries whose fp matches no current hit, and remove them only
    with --yes. SCOPED to the chapters actually scanned: an entry for a chapter
    outside --slugs/--volume was never looked at, so it is never a candidate —
    otherwise `--prune-allow --slugs X` would delete every other chapter's rulings."""
    allow = load_allow(allow_path)
    live = {h["fp"] for h in all_hits}
    scanned = set(slugs)
    to_remove = [fp for fp, e in allow.items()
                 if e.get("slug") in scanned and fp not in live]
    if not to_remove:
        print(f"orphan-prune: nothing to prune across {len(scanned)} chapter(s) "
              f"→ {allow_path.name}")
        return
    n = len(to_remove)
    verb = "removing" if args.yes else "would remove (re-run with --yes)"
    print(f"orphan-prune: {verb} {n} entr{'y' if n == 1 else 'ies'} that no longer "
          f"match{'es' if n == 1 else ''} a hit:")
    for fp in sorted(to_remove, key=lambda f: (allow[f].get("slug", ""), allow[f]["term"])):
        e = allow[fp]
        print(f"  {e.get('slug', '')}  «{e['term']}»  [{fp}]  {e.get('note', '')[:60]}")
    if args.yes:
        keep = {fp: e for fp, e in allow.items() if fp not in to_remove}
        save_allow(allow_path, keep)
        print(f"removed {n} → {allow_path.name}; {len(keep)} remain")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--volume", type=int, default=1)
    ap.add_argument("--slugs", nargs="*", help="limit to these chapters")
    ap.add_argument("--staged", action="store_true",
                    help="pre-commit mode: only staged scenes/*.md; never fails the commit")
    ap.add_argument("--any-reference", action="store_true",
                    help="also report indefinite/bare uses (much noisier)")
    ap.add_argument("--max-hits", type=int, default=2,
                    help="skip terms still used more than N times (default 2)")
    ap.add_argument("--max-df", type=int, default=3,
                    help="skip terms appearing in more than N chapters (default 3)")
    ap.add_argument("--allow", type=str,
                    help="path to orphan-allow.toml (default: audits/orphan-refs/orphan-allow.toml)")
    ap.add_argument("--ack", action="store_true",
                    help="acknowledge active hits in scope (respects --fp if given)")
    ap.add_argument("--fp", nargs="+",
                    help="filter by fingerprint prefix (with --ack or --unack)")
    ap.add_argument("--note", type=str,
                    help="reason for acknowledgment (required with --ack)")
    ap.add_argument("--unack", action="store_true",
                    help="remove entries by --fp and/or --slugs")
    ap.add_argument("--show-suppressed", action="store_true",
                    help="include suppressed hits in report")
    ap.add_argument("--prune-allow", action="store_true",
                    help="list/remove allow entries unmatched in current scan")
    ap.add_argument("--yes", action="store_true",
                    help="confirm removal with --prune-allow")
    args = ap.parse_args()

    # Determine allow path.
    allow_path = Path(args.allow) if args.allow else (REPO / "audits" / "orphan-refs" / "orphan-allow.toml")

    # --ack/--unack/--prune-allow are incompatible with --staged.
    if args.staged and (args.ack or args.unack or args.prune_allow):
        sys.exit("ERROR: --staged is incompatible with --ack, --unack, or --prune-allow")

    # --unack operates purely on the stored allowlist; no scan needed.
    if args.unack:
        return orphan_unack(args, allow_path)

    vol = volume_scenes.volume_slugs(args.volume, drafted_only=True)
    if args.staged:
        staged = [Path(p).stem for p in git("diff", "--cached", "--name-only").split()
                  if p.startswith("scenes/") and p.endswith(".md")]
        slugs = [s for s in vol if s in staged]
    elif args.slugs:
        slugs = [s for s in vol if s in args.slugs]
    else:
        slugs = vol
    if not slugs:
        return

    df = document_frequency(vol)
    allf = []
    for s in slugs:
        allf.extend(scan(s, df, args.max_df, args.max_hits, not args.any_reference))

    allow = load_allow(allow_path)

    # Expand findings into per-hit entries with fingerprints.
    all_hits = []
    for f in allf:
        for ln, txt in f["hits"]:
            fp = _fingerprint(f["slug"], f["term"], " ".join(txt.split()))
            hit_dict = {"slug": f["slug"], "term": f["term"], "sha": f["sha"],
                        "subject": f["subject"], "df": f["df"], "line": ln, "text": txt, "fp": fp}
            all_hits.append(hit_dict)

    # Filter by --fp if given.
    if args.fp:
        all_hits = [h for h in all_hits if _fp_match(h["fp"], args.fp)]

    # Separate active (not suppressed) and suppressed.
    active = [h for h in all_hits if h["fp"] not in allow]
    suppressed = [h for h in all_hits if h["fp"] in allow]

    if args.ack:
        # For --ack, pass active hits (already filtered by --fp if given).
        return orphan_ack(args, allow_path, allow, all_hits)

    if args.prune_allow:
        # For --prune-allow, need all hits (not filtered by --fp).
        if args.fp:
            sys.exit("ERROR: --prune-allow cannot be combined with --fp")
        return orphan_prune_allow(args, allow_path, all_hits, slugs)

    # Report mode. Keep the original finding order (same sort key as before the
    # allowlist existed, so sweeps stay comparable), and apply suppression per hit
    # BEFORE the two-hit display cap — a suppressed hit must never hide a live one.
    allf.sort(key=lambda f: (" " not in f["term"], f["df"], len(f["hits"])))
    shown_fps = {h["fp"] for h in all_hits}   # respects --fp in report mode
    findings_display = []
    for f in allf:
        hits = []
        for ln, txt in f["hits"]:
            fp = _fingerprint(f["slug"], f["term"], " ".join(txt.split()))
            if fp not in shown_fps:
                continue
            is_suppressed = fp in allow
            if is_suppressed and not args.show_suppressed:
                continue
            hits.append((ln, txt, fp, is_suppressed))
        # A finding whose every hit is suppressed drops out entirely — unless
        # --show-suppressed asked to see it, in which case it shows, marked ✓.
        if hits and (args.show_suppressed or any(not s for _, _, _, s in hits)):
            findings_display.append({**f, "hits": hits})

    # The header counts FINDINGS (as it always has), not hits.
    n_suppressed = len(suppressed)
    extra = (f"  ({n_suppressed} suppressed)" if n_suppressed else "")
    if not findings_display:
        print(f"orphan-refs: nothing flagged across {len(slugs)} chapter(s){extra}")
        return

    print(f"orphan-refs: {len(findings_display)} candidate(s) across {len(slugs)} chapter(s){extra}")
    print("  a term whose introducing text was cut, still referenced in the chapter")
    print("  FLAGS, never findings — an ordinary surviving use is common.\n")
    for f in findings_display:
        print(f"  {f['slug']}  «{f['term']}»  (in {f['df']} chapter(s))")
        print(f"    cut by {f['sha']}  {f['subject'][:70]}")
        for ln, txt, fp, is_suppressed in f["hits"][:2]:
            mark = "✓ " if is_suppressed and args.show_suppressed else ""
            print(f"    {mark}:{ln}  [#{fp}]  {txt[:150]}")
        print()
    if args.staged:
        print("  (warning only — this never blocks a commit)")


if __name__ == "__main__":
    main()
