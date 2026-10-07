#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Verify the line-editor's NOTES quotes against the chapter text.

Each NOTES line opens with a quoted string that the persona was told to copy
exactly. This checks every quote as a normalized substring of the clean chapter
prose (and, for a *repeat* pointing back, of the named earlier chapter when it
can be found). Misses are reported, never removed — the paraphrase rate is
itself a finding about the instrument.

  tools/notes_verify.py --model claude-fable-5-1 --persona line-editor --chapter 30
  tools/notes_verify.py --gate reviews/capture-panel/<model>/dag/<persona>/gate-ch030.md
"""
from __future__ import annotations
import argparse, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import checkpoint_bundle  # noqa: E402

QUOTE_RE = re.compile(r'^\s*[-*]\s*[“"]([^”"]{3,}?)[”"]\s*[—–-]', re.M)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", " ").replace("–", " ").replace("…", " ").replace("...", " ")
    s = re.sub(r"[*_]", "", s)
    s = re.sub(r"[^\w' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


INTERPRETIVE = {"explains", "told-after-shown", "editorial"}
NOTE_RE = re.compile(r'^\s*[-*]\s*[“"]([^”"]{3,}?)[”"]\s*[—–-]\s*([a-z-]+)\s*[—–-]', re.M)


def reader_corpus() -> list[tuple[str, int | None, str]]:
    """(path, chapter-number-or-None, normalized text) for every other reader's output.

    Cold reads are per chapter (<model>/<slug>.md); capture gates carry their chapter in
    the filename; whole-volume records cover every chapter (None)."""
    slugs = checkpoint_bundle.reader_slugs()
    by_slug = {sl: i + 1 for i, sl in enumerate(slugs)}
    out = []
    for p in list((ROOT / "reviews/cold-read").rglob("*.md")) + list((ROOT / "reviews/capture-panel").rglob("*.md")):
        sp = str(p)
        if any(k in sp for k in ("line-editor", "/checkpoints/", "/prompts/", "/personas/", "checkpoint-ensembles", "ck-ch")) or p.name == "SPEC.md":
            continue
        n = None
        m = re.search(r"gate-ch(\d+)", p.name)
        if m:
            n = int(m.group(1))
        elif p.parent.parent.name == "cold-read" or p.parent.name in by_slug or p.stem in by_slug:
            n = by_slug.get(p.stem)
            if n is None and "cold-read" in sp:
                continue  # a cold read of a chapter outside the reader sequence
        elif "--volume" in p.name:
            n = None
        else:
            continue
        out.append((sp, n, norm(p.read_text(errors="ignore"))))
    return out


def uptake(quote: str, chapter: int, corpus) -> tuple[int, int]:
    """(files quoting a 6-word run of the line, files that covered the chapter)."""
    words = norm(quote).split()
    probes = [" ".join(words[i:i + 6]) for i in range(0, max(1, len(words) - 5), 3)] or [" ".join(words)]
    covered = [(p, t) for p, n, t in corpus if n is None or n == chapter]
    hit = sum(1 for p, t in covered if any(pr in t for pr in probes))
    return hit, len(covered)


def uptake_report(items: list[tuple[int, str, str]]) -> None:
    """items: (chapter, tag, quote). Prints interpretive flags ranked by reader uptake."""
    corpus = reader_corpus()
    rows = []
    for ch, tag, q in items:
        if tag not in INTERPRETIVE:
            continue
        k, n = uptake(q, ch, corpus)
        rows.append((k, n, ch, tag, q))
    rows.sort(key=lambda r: (r[0] / r[1] if r[1] else -1, -r[2]))
    print(f"\nREADER UPTAKE — interpretive flags ({len(rows)}), files quoting a 6-word run / files that covered the chapter")
    for k, n, ch, tag, q in rows:
        mark = "·" if n < 6 else ("○" if k == 0 else "●")
        note = " (too few readers on file to judge)" if n < 6 else (" — NO UPTAKE" if k == 0 else "")
        print(f"  {mark} {k:2d}/{n:<3d} ch{ch:02d} {tag:16s} “{q[:80]}”{note}")


def notes_block(text: str) -> str:
    m = re.search(r"^NOTES\b.*?(?=^GATE\b)", text, re.M | re.S)
    return m.group(0) if m else ""


def verify_volume(rec: Path) -> int:
    text = rec.read_text(encoding="utf-8")
    slugs = checkpoint_bundle.reader_slugs()
    cache: dict[int, str] = {}

    def chap(i: int) -> str:
        if i not in cache:
            cache[i] = norm(checkpoint_bundle.clean_scene_text(slugs[i - 1]))
        return cache[i]

    def found(q: str, i: int) -> bool:
        nq = norm(q)
        frags = [f for f in re.split(r"\s{2,}| \.\.\. ", nq) if f]
        return all(f in chap(i) for f in frags) if frags else False

    ok = miss = 0
    blocks = re.split(r"^(?=CHAPTER \d+)", text, flags=re.M)
    for b in blocks:
        m = re.match(r"CHAPTER (\d+)", b)
        if not m:
            continue
        n = int(m.group(1))
        body = b.split("ACROSS THE VOLUME")[0]
        for q in QUOTE_RE.findall(body):
            hit = found(q, n); where = f"ch{n:02d}"
            if not hit:
                for i in range(n - 1, 0, -1):
                    if found(q, i):
                        hit, where = True, f"ch{i:02d} (earlier; noted at ch{n:02d})"; break
            ok += hit; miss += (not hit)
            if not hit:
                print(f"  ✗ ch{n:02d} NOT ON PAGE  “{q[:90]}”")
    print(f"per-chapter NOTES: {ok} verified · {miss} missed of {ok+miss}")
    m = re.search(r"^ACROSS THE VOLUME(.*?)(?=^VERDICT|\Z)", text, re.M | re.S)
    if m:
        aok = amiss = 0
        for line in m.group(1).splitlines():
            qm = re.match(r'\s*[-*]\s*[“"]([^”"]{3,}?)[”"]', line)
            if not qm:
                continue
            q = qm.group(1)
            chs = sorted({int(x) for x in re.findall(r"ch\s?(\d+)", line)})
            # per-chapter variant: a quote inside the parenthetical right after "chN (" wins over the head quote
            def q_for(i: int) -> list[str]:
                m2 = re.search(r"ch\s?%d\s*\(([^)]*)\)" % i, line)
                if m2:
                    inner = re.findall(r'[“"]([^”"]{3,}?)[”"]', m2.group(1))
                    if inner:
                        return inner
                return [q]
            hits = [i for i in chs if 1 <= i <= len(slugs) and any(found(x, i) for x in q_for(i))]
            misses = [i for i in chs if i not in hits]
            aok += len(hits); amiss += len(misses)
            flag = "✓" if not misses else "✗"
            print(f"  {flag} “{q[:60]}” — named {chs} — on page in {hits}" + (f" — NOT in {misses}" if misses else ""))
        print(f"ACROSS THE VOLUME: {aok} chapter-claims verified · {amiss} not on that page")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate")
    ap.add_argument("--model")
    ap.add_argument("--persona", default="line-editor")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--uptake", action="store_true",
                    help="after verifying, rank the interpretive flags (explains / told-after-shown / editorial) "
                         "by how many other readers quoted the line; zero uptake with enough readers on file is the signal")
    ap.add_argument("--volume", help="a <persona>--volume.md record: verify every CHAPTER block "
                                     "against its own chapter and ACROSS THE VOLUME against the named chapters")
    a = ap.parse_args()
    if a.volume:
        rc = verify_volume(Path(a.volume).resolve())
        if a.uptake:
            text = Path(a.volume).read_text(encoding="utf-8"); items = []; ch = None
            for line in text.splitlines():
                m = re.match(r"CHAPTER (\d+)", line)
                if m: ch = int(m.group(1)); continue
                if line.startswith("ACROSS THE VOLUME"): break
                q = NOTE_RE.match(line)
                if q and ch: items.append((ch, q.group(2), q.group(1)))
            uptake_report(items)
        return rc
    if a.gate:
        gate = Path(a.gate).resolve()
        n = int(re.search(r"gate-ch(\d+)", gate.name).group(1))
    else:
        if not (a.model and a.chapter):
            ap.error("--gate, or --model and --chapter")
        n = a.chapter
        gate = ROOT / "reviews/capture-panel" / a.model / "dag" / a.persona / f"gate-ch{n:03d}.md"
    text = gate.read_text(encoding="utf-8")
    block = notes_block(text)
    if not block:
        print(f"{gate}: no NOTES block"); return 1
    slugs = checkpoint_bundle.reader_slugs()
    chap = norm(checkpoint_bundle.clean_scene_text(slugs[n - 1]))
    earlier = {i + 1: None for i in range(n - 1)}
    quotes = QUOTE_RE.findall(block)
    if not quotes:
        print(f"{gate}: NOTES present, no quotes parsed"); return 1
    ok = miss = 0
    for q in quotes:
        nq = norm(q)
        # allow a short ellipsis-joined quote: every fragment must appear
        frags = [f for f in re.split(r"\s{2,}| \.\.\. ", nq) if f]
        hit = all(f in chap for f in frags) if frags else nq in chap
        where = f"ch{n:02d}"
        if not hit:
            for i in range(n - 1, 0, -1):
                if earlier[i] is None:
                    earlier[i] = norm(checkpoint_bundle.clean_scene_text(slugs[i - 1]))
                if all(f in earlier[i] for f in frags):
                    hit, where = True, f"ch{i:02d} (earlier)"
                    break
        ok += hit; miss += (not hit)
        print(f"  {'✓' if hit else '✗'} {where if hit else 'NOT ON PAGE':14s} “{q[:90]}”")
    print(f"{gate.relative_to(ROOT)}: {ok} verified · {miss} missed of {ok+miss}")
    if a.uptake:
        uptake_report([(n, t, q) for q, t in NOTE_RE.findall(block)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
