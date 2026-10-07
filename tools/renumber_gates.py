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
"""
import argparse, collections, glob, io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capture_dag  # noqa: E402

GATE_RE = re.compile(r"gate-ch(\d+)\.md$")
TITLE_RE = re.compile(r"^GATE\s+\d+\s*[—\-–]\s*(.+?)\s*$", re.M)
HEADER_RE = re.compile(r"(· gate ch)\d+( ·)")
DELETE = "DELETE"

# Model-mistyped `GATE n — Title` lines on gates that ARE in the correct slot.
# Recorded in reviews/capture-panel/SPEC.md ("Gate renumbering"): the title line
# is the model's own output and is never edited, so a handful disagree with the
# filename while the file is where it belongs. Keyed by (path suffix, title).
KNOWN_MISTYPES = {
    ("claude-fable-5-1/dag/fsog-refugee/gate-ch026.md", "Sorority"),
}


def norm(t):
    t = t.lower().strip()
    t = re.sub(r"^(the|a|an)\s+", "", t)
    return re.sub(r"[^a-z0-9]+", "", t)


def title_index(chronology="meta/meta-plan-chronology.md"):
    """display title -> slug, from the chronology's own entry headings."""
    lines = io.open(chronology, encoding="utf-8").read().split("\n")
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


def gate_files():
    for p in sorted(glob.glob("reviews/capture-panel/*/dag/*/gate-ch*.md")):
        if "/.failed/" in p:
            continue
        yield p


def lane_of(path):
    parts = path.split("/")
    return parts[2], parts[4]          # model, persona


def build_plan(removed, inserted, policy):
    slugs = capture_dag.slugs()
    slug2num = {s: i + 1 for i, s in enumerate(slugs)}
    t2s = title_index()
    for s in slugs:
        t2s.setdefault(norm(s), s)

    plan, halts, typos, verified, untitled = {}, [], [], 0, 0
    for path in gate_files():
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        text = io.open(path, encoding="utf-8", errors="replace").read()
        m = TITLE_RE.search(text)
        slug = t2s.get(norm(m.group(1))) if m else None
        claimed = slug2num.get(slug) if slug else None

        if removed is not None and cur == removed:
            # the position the edit deleted: nothing legitimately lives here
            plan[path] = DELETE
            if claimed is not None and claimed != cur:
                halts.append(("deleted-position-holds-live-read", path, cur,
                              m.group(1), claimed))
            continue

        if removed is not None:
            want = cur - 1 if cur > removed else cur
        else:
            want = cur + 1 if cur >= inserted else cur

        if want != cur:
            plan[path] = want
        if claimed is None:
            untitled += 1
        elif claimed == want:
            verified += 1
        elif want == cur:
            typos.append((path, cur, m.group(1), claimed))
        else:
            halts.append(("identity-vs-position", path, cur, want,
                          m.group(1), claimed))
    return plan, halts, typos, verified, untitled


def validate(plan):
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
        if want is DELETE:
            continue
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
    return errs


def verify():
    """Standing consistency check: does each gate sit where its own content says?"""
    slugs = capture_dag.slugs()
    slug2num = {s: i + 1 for i, s in enumerate(slugs)}
    t2s = title_index()
    for s in slugs:
        t2s.setdefault(norm(s), s)
    ok = bad = untitled = known = 0
    rows = []
    for path in gate_files():
        cur = int(GATE_RE.search(os.path.basename(path)).group(1))
        text = io.open(path, encoding="utf-8", errors="replace").read()
        m = TITLE_RE.search(text)
        claimed = slug2num.get(t2s.get(norm(m.group(1)))) if m else None
        hm = re.search(r"· gate ch(\d+) ·", text)
        header = int(hm.group(1)) if hm else None
        if claimed is None:
            untitled += 1
        elif claimed == cur:
            ok += 1
        elif (path.replace("reviews/capture-panel/", ""), m.group(1)) in KNOWN_MISTYPES:
            known += 1
        else:
            bad += 1
            rows.append((path, cur, m.group(1), claimed))
        if header is not None and header != cur:
            rows.append((path, cur, "header says ch%03d" % header, header))
    print("gates            : %d" % (ok + bad + untitled))
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
    ap.add_argument("--removed-policy", choices=["delete", "retire"], default="retire",
                    help="what to do with gates sitting at a --removed position")
    ap.add_argument("--retire-name", default="read-removed-chapter.md")
    m = ap.add_mutually_exclusive_group()
    m.add_argument("--check", action="store_true")
    m.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if a.verify:
        return verify()
    if not (a.check or a.apply):
        ap.error("one of --check or --apply is required with --removed/--inserted")

    plan, halts, typos, verified, untitled = build_plan(a.removed, a.inserted,
                                                        a.removed_policy)
    moves = {p: w for p, w in plan.items() if w is not DELETE}
    gone = [p for p, w in plan.items() if w is DELETE]
    errs = validate(plan)

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

    tmp = []
    for path, want in sorted(moves.items()):
        t = path + ".renumber-tmp"
        os.rename(path, t)
        tmp.append((t, path, want))
    for path in gone:
        if a.removed_policy == "delete":
            os.remove(path)
        else:
            dest = os.path.join(os.path.dirname(path), a.retire_name)
            os.rename(path, dest)
    headers = 0
    for t, path, want in tmp:
        dest = GATE_RE.sub("gate-ch%03d.md" % want, path)
        os.rename(t, dest)
        s = io.open(dest, encoding="utf-8").read()
        # the italic provenance header is OURS and must not lie; the model's
        # own `GATE n — Title` line is its output and is never touched.
        s2, k = HEADER_RE.subn(lambda mm: "%s%03d%s" % (mm.group(1), want, mm.group(2)),
                               s, count=1)
        if k:
            io.open(dest, "w", encoding="utf-8").write(s2)
            headers += 1
    print("\napplied: %d moved, %d headers rewritten, %d %sd"
          % (len(tmp), headers, len(gone), a.removed_policy))
    return 0


if __name__ == "__main__":
    sys.exit(main())
