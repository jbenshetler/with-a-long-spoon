#!/usr/bin/env python3
"""Renumber capture-DAG gate files after a structural edit to the chronology.

A gate's chapter identity lives in its FILENAME and nowhere else the tools read
(capture_dag writes `gate-ch{n:03d}.md`; capture_stats parses the number back out
of the name). Reader-sequence numbers come from the chronology, so inserting,
removing or merging a chapter renumbers every later chapter and silently
invalidates every gate filename above the edit. Nothing in the harness notices.

This tool does the repair deterministically:

  --check    build the full plan, prove its invariants, mutate nothing
  --apply    execute the plan (two-phase, so no rename can collide mid-run)

Position is the MOVER; recorded identity is the VERIFIER. That is correct only
because a prior identity-keyed pass normalised the filenames, so the baseline is
trusted and exactly one structural edit has happened since. If identity and
position ever disagree, the run halts with the list and changes nothing.

Usage
  tools/renumber_gates.py --removed 54 --removed-policy delete --check
  tools/renumber_gates.py --inserted 43 --check
  tools/renumber_gates.py --merged 21 22 --preserve-prose-sha 332b2e10547e --check

For a reviewed diptych, --merged FIRST SECOND preserves a merged read already
at FIRST only when its title and an explicitly supplied prose hash agree.
Both obsolete standalone reads are retired; lanes without a merged read keep
a gap at FIRST. Later gates shift once. Checkpoints and reader-written text
are never renumbered by this tool.
If a tree also contains later gates already aligned to the current inventory,
--keep-aligned preserves those title matches; destination collisions still halt.
"""
import argparse, collections, glob, os, re, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import volume_scenes  # noqa: E402  (same inventory; no reader/API dependencies)

GATE_RE = re.compile(r"gate-ch(\d+)\.md$")
TITLE_RE = re.compile(r"^GATE\s+\d+\s*[—\-–]\s*(.+?)\s*$", re.M)
HEADER_RE = re.compile(r"(· gate ch)\d+( ·)")
DELETE = "DELETE"

# Model-mistyped `GATE n — Title` lines on gates that ARE in the correct slot.
# Recorded in reviews/capture-panel/SPEC.md ("Gate renumbering"): the title line
# is the model's own output and is never edited, so a handful disagree with the
# filename while the file is where it belongs. Keyed by (lane, true slug, title)
# so the exception survives a later renumbering.
KNOWN_MISTYPES = {
    ("claude-fable-5-1/dag/fsog-refugee", "gone", "Sorority"),
}


def reader_slugs():
    return [s for vol in volume_scenes.volume_ordinals()
            for s in volume_scenes.volume_slugs(vol, drafted_only=True)]


def known_mistype(path, title, true_slug):
    lane = "/".join(path.split("/")[2:5])
    return (lane, true_slug, title) in KNOWN_MISTYPES


def norm(t):
    t = t.lower().strip()
    t = re.sub(r"^(the|a|an)\s+", "", t)
    return re.sub(r"[^a-z0-9]+", "", t)


def title_index(chronology="meta/meta-plan-chronology.md"):
    """display title -> slug, from the chronology's own entry headings."""
    lines = Path(chronology).read_text(encoding="utf-8").split("\n")
    out = {}
    for i, line in enumerate(lines):
        m = re.match(r"^### \[(?:SCENE|VIGNETTE)\]\s+(.+?)\s*$", line)
        if not m:
            continue
        title = re.sub(r"\s*\(.*?\)\s*$", "", m.group(1))
        for j in range(i + 1, min(i + 4, len(lines))):
            sm = re.search(r"slug:\s*([a-z0-9-]+)", lines[j])
            if sm:
                out[norm(title)] = sm.group(1)
                break
    return out


# Lane scope (--lanes): "<model>/<persona>" globs. Default is every lane. Scoping
# exists for a tree whose lanes are not all at the same baseline (2026-10-25: the
# Turned Up merge was never propagated to the non-romance-graduate lanes), where
# a position-moving edit is only correct on the lanes that are aligned.
LANES = ["*/*"]


def gate_files():
    for pat in LANES:
        model, persona = pat.split("/")
        for p in sorted(glob.glob(f"reviews/capture-panel/{model}/dag/{persona}/gate-ch*.md")):
            if "/.failed/" in p:
                continue
            yield p


def lane_of(path):
    parts = path.split("/")
    return parts[2], parts[4]          # model, persona


def build_plan(removed, inserted, policy, merged=None, preserve_shas=(), keep_aligned=False):
    slugs = reader_slugs()
    slug2num = {s: i + 1 for i, s in enumerate(slugs)}
    t2s = title_index()
    for s in slugs:
        t2s.setdefault(norm(s), s)

    plan, halts, typos, verified, untitled = {}, [], [], 0, 0
    for path in gate_files():
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        m = TITLE_RE.search(text)
        slug = t2s.get(norm(m.group(1))) if m else None
        claimed = slug2num.get(slug) if slug else None

        if merged is not None:
            first, second = merged
            if first <= cur <= second:
                if cur == first and claimed == first:
                    sha = re.search(r"prose-sha ~?([0-9a-f]{12})\b", text.split("\n", 1)[0])
                    if sha and sha.group(1) in preserve_shas:
                        verified += 1
                    else:
                        halts.append(("unverified-merged-read", path,
                                      "supply its reviewed --preserve-prose-sha"))
                else:
                    plan[path] = DELETE
                    if claimed is not None and claimed != first:
                        halts.append(("merge-position-holds-other-live-read", path,
                                      m.group(1), claimed))
                continue
            want = cur - 1 if cur > second else cur
            # Some lanes were already extended against the new inventory.
            # Preserve those only on explicit opt-in, with a matching identity;
            # normal destination validation still catches any collision.
            if keep_aligned and cur > second and claimed == cur:
                verified += 1
                continue
        elif removed is not None:
            want = cur - 1 if cur > removed else cur
        else:
            want = cur + 1 if cur >= inserted else cur

        if removed is not None and cur == removed:
            # the position the edit deleted: nothing legitimately lives here
            plan[path] = DELETE
            if claimed is not None and claimed != cur:
                halts.append(("deleted-position-holds-live-read", path, cur,
                              m.group(1), claimed))
            continue

        if want != cur:
            plan[path] = want
        if claimed is None:
            untitled += 1
        elif claimed == want:
            verified += 1
        elif 1 <= want <= len(slugs) and known_mistype(path, m.group(1), slugs[want - 1]):
            verified += 1
        elif want == cur:
            typos.append((path, cur, m.group(1), claimed))
        else:
            halts.append(("identity-vs-position", path, cur, want,
                          m.group(1), claimed))
    return plan, halts, typos, verified, untitled


def retirement_paths(plan, policy, name=None, merged=None):
    if policy != "retire":
        return {}
    slug = reader_slugs()[merged[0] - 1] if merged else None
    out = {}
    for path, want in plan.items():
        if want != DELETE:
            continue
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        basename = name or ("read-merged-%s-ch%03d.md" % (slug, cur)
                            if merged else "read-removed-chapter.md")
        out[path] = os.path.join(os.path.dirname(path), basename)
    return out


def validate(plan, retirements=None):
    """The check that makes mid-run collisions impossible."""
    errs = []
    by_lane = collections.defaultdict(lambda: {"occupied": {}, "dest": {}, "vacating": set()})
    for path in gate_files():
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        by_lane[lane_of(path)]["occupied"][cur] = path
    for path, want in plan.items():
        L = by_lane[lane_of(path)]
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        L["vacating"].add(cur)
        if want == DELETE:
            continue
        if os.path.exists(path + ".renumber-tmp"):
            errs.append("temporary path already exists: %s.renumber-tmp" % path)
        if want in L["dest"]:
            errs.append("two sources claim %s/%s ch%03d: %s and %s"
                        % (lane_of(path) + (want, L["dest"][want], path)))
        L["dest"][want] = path
    for lane, L in by_lane.items():
        for want, src in L["dest"].items():
            holder = L["occupied"].get(want)
            if holder is not None and want not in L["vacating"]:
                errs.append("%s/%s ch%03d is the destination of %s but is occupied "
                            "by an unplanned file %s" % (lane + (want, src, holder)))
    seen = set()
    for dest in (retirements or {}).values():
        if dest in seen or os.path.exists(dest):
            errs.append("retirement destination already occupied: %s" % dest)
        seen.add(dest)
    return errs


def apply_plan(plan, retirements):
    """Apply an already validated plan without changing reader-written text."""
    tmp = []
    for path, want in sorted(plan.items()):
        if want == DELETE:
            continue
        t = path + ".renumber-tmp"
        os.rename(path, t)
        tmp.append((t, path, want))
    for path, want in plan.items():
        if want == DELETE:
            if path in retirements:
                os.rename(path, retirements[path])
            else:
                os.remove(path)
    headers = 0
    for t, path, want in tmp:
        dest = GATE_RE.sub("gate-ch%03d.md" % want, path)
        os.rename(t, dest)
        s = Path(dest).read_text(encoding="utf-8")
        head, separator, body = s.partition("\n")
        head, k = HEADER_RE.subn(lambda mm: "%s%03d%s" % (mm.group(1), want, mm.group(2)),
                                 head, count=1)
        s2 = head + separator + body
        if k:
            Path(dest).write_text(s2, encoding="utf-8")
            headers += 1
    return headers


def verify():
    """Standing consistency check: does each gate sit where its own content says?"""
    slugs = reader_slugs()
    slug2num = {s: i + 1 for i, s in enumerate(slugs)}
    t2s = title_index()
    for s in slugs:
        t2s.setdefault(norm(s), s)
    ok = bad = untitled = known = 0
    rows = []
    for path in gate_files():
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        m = TITLE_RE.search(text)
        claimed = slug2num.get(t2s.get(norm(m.group(1)))) if m else None
        hm = re.search(r"· gate ch(\d+) ·", text)
        header = int(hm.group(1)) if hm else None
        if claimed is None:
            untitled += 1
        elif claimed == cur:
            ok += 1
        elif 1 <= cur <= len(slugs) and known_mistype(path, m.group(1), slugs[cur - 1]):
            known += 1
        else:
            bad += 1
            rows.append((path, cur, m.group(1), claimed))
        if header is not None and header != cur:
            rows.append((path, cur, "header says ch%03d" % header, header))
    print("gates            : %d" % (ok + bad + untitled + known))
    print("identity matches : %d" % ok)
    print("no title line    : %d  (position trusted)" % untitled)
    print("known mistypes   : %d  (correct slot, model typo)" % known)
    print("MISMATCHES       : %d" % len(rows))
    for r in rows:
        print("  ", r[0].replace("reviews/capture-panel/", ""), "ch%03d" % r[1], repr(r[2]), "->", r[3])
    return 1 if rows else 0


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--verify", action="store_true",
                   help="no edit: check every gate's recorded identity against its filename")
    g.add_argument("--removed", type=int, metavar="N",
                   help="a reader position deleted from the sequence (e.g. a merge)")
    g.add_argument("--inserted", type=int, metavar="N",
                   help="a reader position inserted into the sequence")
    g.add_argument("--merged", type=int, nargs=2, metavar=("FIRST", "SECOND"),
                   help="merge adjacent chapters into FIRST, preserving verified new reads")
    ap.add_argument("--preserve-prose-sha", action="append", default=[],
                    help="reviewed merged-prose hash to preserve at FIRST (repeatable)")
    ap.add_argument("--keep-aligned", action="store_true",
                    help="with --merged, preserve later gates whose title already matches their position")
    ap.add_argument("--removed-policy", choices=["delete", "retire"], default="retire",
                    help="what to do with gates sitting at a --removed position")
    ap.add_argument("--retire-name", help="retired basename; merges default to unique names per source")
    ap.add_argument("--lanes", nargs="+", metavar="MODEL/PERSONA",
                    help="restrict to these lanes (globs, e.g. '*/romance-graduate'); default all")
    m = ap.add_mutually_exclusive_group()
    m.add_argument("--check", action="store_true")
    m.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.lanes:
        if any(x.count("/") != 1 for x in a.lanes):
            ap.error("--lanes takes MODEL/PERSONA globs")
        global LANES
        LANES = a.lanes

    if a.verify:
        return verify()
    if a.merged and (a.merged[0] < 1 or a.merged[1] != a.merged[0] + 1
                     or a.merged[0] > len(reader_slugs())):
        ap.error("--merged requires adjacent positive positions FIRST SECOND")
    if a.preserve_prose_sha and not a.merged:
        ap.error("--preserve-prose-sha requires --merged")
    if a.keep_aligned and not a.merged:
        ap.error("--keep-aligned requires --merged")
    if any(not re.fullmatch(r"[0-9a-f]{12}", s) for s in a.preserve_prose_sha):
        ap.error("--preserve-prose-sha must be a 12-character lowercase hex hash")
    if not (a.check or a.apply):
        ap.error("one of --check or --apply is required with --removed/--inserted/--merged")

    plan, halts, typos, verified, untitled = build_plan(a.removed, a.inserted,
                                                        a.removed_policy, a.merged,
                                                        a.preserve_prose_sha,
                                                        a.keep_aligned)
    moves = {p: w for p, w in plan.items() if w != DELETE}
    gone = [p for p, w in plan.items() if w == DELETE]
    retirements = retirement_paths(plan, a.removed_policy, a.retire_name, a.merged)
    errs = validate(plan, retirements)

    print("gates scanned         : %d" % sum(1 for _ in gate_files()))
    print("moves                 : %d  (identity-verified %d, untitled %d)"
          % (len(moves), verified, untitled))
    print("at removed position   : %d  -> %s" % (len(gone), a.removed_policy))
    print("identity/position OK  : %s" % ("yes" if not halts else "NO"))
    print("plan invariants       : %s" % ("ok" if not errs else "FAILED"))
    for t in typos:
        print("  note: title disagrees but position is correct (model mistype): "
              "%s ch%03d says %r (that title sits at %d)"
              % (t[0].replace("reviews/capture-panel/", ""), t[1], t[2], t[3]))
    for h in halts:
        print("  HALT", h)
    for e in errs:
        print("  INVARIANT", e)
    if halts or errs:
        print("\nnothing changed.")
        return 1
    if a.check:
        print("\n--check: nothing changed.")
        return 0

    headers = apply_plan(plan, retirements)
    print("\napplied: %d moved, %d headers rewritten, %d %sd"
          % (len(moves), headers, len(gone), a.removed_policy))
    return 0


if __name__ == "__main__":
    sys.exit(main())
