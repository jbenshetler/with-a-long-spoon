#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai>=1.40", "openai-codex", "numpy",
#   "spacy>=3.8,<3.9",
#   "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""Figure sweep: repeated metaphors and similes across the whole book.

Readers remember a figure. A second "like a missed stair", or the lamp that is
Randi's attention in one chapter and Vee's presence in another, spends the
first one. The word-based instruments cannot see this:
  - the style linter knows only the phrases someone wrote a rule for;
  - echo_harvest.py matches wording inside one chapter;
  - an rg sweep for "stair" returns ~35 hits, 6 of them figures, and still
    misses "climbing the same stair".
A figure returns as the same PICTURE in different words, or as the same
FEELING in a different picture. Finding either takes a reader, so step 1 is a
model. Everything after it is deterministic.

THREE STEPS

  1. extract   per chapter, in line-numbered windows, one model at a time:
               every figure with its picture, its VEHICLES (every concrete
               noun it borrows), its SENSATION (from a fixed list), who it
               describes, POV, and the line. Each quote is verified against
               the prose; an unverifiable quote is kept but marked.
  2. group     local and deterministic, no model calls: the models' figures
               are unioned (a figure either found counts); vehicle nouns are
               lemmatized (spaCy) and near-synonyms merged by embedding
               (Ollama nomic-embed-text, cosine >= VEHICLE_SIM) into picture
               families; the sensation tag is the feeling family.
  3. report    families with figures in 2+ chapters: picture families first,
               those spread over 2+ people first, then by how rarely the book
               uses the noun literally. Families the author has ruled
               designed (audits/figures/designed.md) are listed apart.

  score        recall against audits/figures/gold.md (FIND lines must be
               found, LITERAL lines must not), and whether each gold group
               shares one family.

Why the fixed sensation list: free-text feeling labels do not cluster. On the
gold drop group, embeddings put the drop phrases at 0.53 to each other and
0.44 to unrelated feelings, overlapping. Asking for the bodily sensation from
a closed list puts "missed stair", "floor went out" and "high-board drop" in
one tag by construction.

FLAGS, never findings. The book runs on designed returns (doors, the
deadbolt, warmth); the author rules every family. Subscription lanes only by
default (claude-* and codex); a provider/model id is OpenRouter, paid, and
needs the author's authorization for each run.

Usage:
    tools/figure_harvest.py extract --model gpt-6.1-terra --gold          # gold chapters
    tools/figure_harvest.py extract --model claude-sonnet-5-5 --gold
    tools/figure_harvest.py group                                         # union of both
    tools/figure_harvest.py score
    tools/figure_harvest.py extract --model gpt-6.1-terra --volume 2      # one volume
    tools/figure_harvest.py group --through 2                             # volumes 1-2
    tools/figure_harvest.py report --through 2
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import volume_scenes  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "audits" / "figures"
PROMPTS = ROOT / "prompts"
GOLD = ROOT / "gold.md"
DESIGNED = ROOT / "designed.md"

DEFAULT_MODELS = ("claude-sonnet-5-5", "gpt-6.1-terra")   # author ruling 2026-10-27
WINDOW = 120      # lines of prose per extraction call
OVERLAP = 6       # lines repeated at each window edge so no sentence is split
NEAR = 4          # a quote may sit this many lines from where the model put it


# ----------------------------------------------------------------- paths

def model_dir(model_id: str) -> Path:
    return ROOT / model_id.replace("/", "--")


def chapter_path(model_id: str, slug: str) -> Path:
    return model_dir(model_id) / "chapters" / f"{slug}.json"


def report_path(model_id: str) -> Path:
    return model_dir(model_id) / "report.md"


def drafted_slugs() -> list[str]:
    return [s["slug"] for s in volume_scenes.all_scenes() if s.get("drafted")]


def load_prompt(name: str) -> str:
    p = PROMPTS / f"{name}.md"
    if not p.exists():
        raise SystemExit(f"missing prompt: {p}")
    return p.read_text(encoding="utf-8")


# ----------------------------------------------------------------- lanes

def make_agent(model: str, effort: str, label: str):
    """Same lanes as fact_audit.py; never a second harness."""
    import cold_read
    import fact_audit
    system = load_prompt("system")
    if model.startswith("claude-"):
        cwd = ROOT / ".work" / model / label
        cwd.mkdir(parents=True, exist_ok=True)
        return fact_audit.make_claude_agent(system, effort, cwd), (lambda: None)
    if "/" in model:
        import os
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("OpenRouter model needs OPENROUTER_API_KEY set")
        print(f"[auth] openrouter — billing PER TOKEN (author-authorized) · {model}",
              file=sys.stderr)
        return (cold_read.make_openrouter_agent_fn(
            system_prompt=system, policy="fact", effort=effort, api_key=key),
            (lambda: None))
    return cold_read.make_codex_agent_fn(system_prompt=system, effort=effort)


def parse_json(text: str):
    """Models wrap JSON in prose or fences. Take the outermost array/object."""
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    for open_c, close_c in (("[", "]"), ("{", "}")):
        a, b = text.find(open_c), text.rfind(close_c)
        if a != -1 and b > a:
            try:
                return json.loads(text[a:b + 1])
            except json.JSONDecodeError:
                continue
    # Salvage object by object. A model that emits one malformed object
    # (claude-sonnet-5-5 writes `"line":15",`) must not lose the whole window.
    items, bad = [], 0
    for m in re.finditer(r"\{[^{}]*\}", text):
        obj = re.sub(r'("line"\s*:\s*\d+)"', r"\1", m.group(0))
        try:
            items.append(json.loads(obj))
        except json.JSONDecodeError:
            bad += 1
    if items:
        if bad:
            print(f"  [salvage] kept {len(items)} objects, skipped {bad} malformed",
                  file=sys.stderr)
        return items
    raise ValueError("no JSON in reply")


# ----------------------------------------------------------------- step 1

def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"').replace("*", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def locate(lines: list[str], quote: str, hint: int) -> int | None:
    """1-based line holding the quote, nearest the model's line; else None."""
    q = norm(quote)
    if not q:
        return None
    order = sorted(range(len(lines)), key=lambda i: abs(i + 1 - hint))
    for i in order:
        if q in norm(lines[i]):
            return i + 1
    return None


def windows(n: int) -> list[tuple[int, int]]:
    out, start = [], 0
    while start < n:
        end = min(n, start + WINDOW)
        out.append((max(0, start - OVERLAP), min(n, end + OVERLAP)))
        start = end
    return out


def extract_chapter(agent_fn, model: str, slug: str) -> dict:
    raw = (REPO / "scenes" / f"{slug}.md").read_text(encoding="utf-8")
    lines = raw.splitlines()
    template = load_prompt("extract")
    found: dict[tuple[int, str], dict] = {}
    unverified = []
    failed: list[str] = []
    for a, b in windows(len(lines)):
        numbered = "\n".join(f"{i + 1}\t{lines[i]}" for i in range(a, b)
                             if lines[i].strip())
        prompt = template.replace("{{SLUG}}", slug).replace("{{TEXT}}", numbered)
        reply = agent_fn(prompt=prompt, model=model, label=f"fig-{slug}-{a}")
        text = reply.get("output") or ""
        raw_dir = ROOT / ".work" / model.replace("/", "--") / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / f"{slug}-{a + 1:04d}.txt").write_text(text, encoding="utf-8")
        try:
            items = parse_json(text)
        except ValueError:
            items = None
        if isinstance(items, dict):
            items = next((v for v in items.values() if isinstance(v, list)), None)
        if not isinstance(items, list) or (not items and len(text.strip()) > 20):
            # An empty or unreadable reply for a window of prose is a failure,
            # not "no figures": saving it would make the rerun skip the chapter.
            failed.append(f"{a + 1}-{b}")
            print(f"  [warn] {slug} lines {a + 1}-{b}: no usable figures in reply "
                  f"(raw kept in {raw_dir.name}/)", file=sys.stderr)
            continue
        for it in items:
            if not isinstance(it, dict):
                continue
            quote = str(it.get("quote", "")).strip()
            try:
                hint = int(it.get("line", 0))
            except (TypeError, ValueError):
                hint = 0
            line = locate(lines, quote, hint)
            rec = {
                "slug": slug,
                "line": line or hint,
                "verified": line is not None,
                "quote": quote,
                "picture": str(it.get("picture", "")).strip().lower(),
                "feeling": str(it.get("feeling", "")).strip().lower(),
                "vehicles": [str(v).strip().lower() for v in (it.get("vehicles") or [])
                             if str(v).strip()],
                "sensation": str(it.get("sensation", "")).strip().lower(),
                "applies_to": str(it.get("applies_to", "")).strip(),
                "pov": str(it.get("pov", "")).strip(),
                "kind": str(it.get("kind", "")).strip().lower(),
                "literal_maybe": bool(it.get("literal_maybe", False)),
            }
            if not line:
                unverified.append(rec)
                continue
            found.setdefault((line, norm(quote)), rec)   # window overlap dedupe
    figs = sorted(found.values(), key=lambda r: r["line"]) + unverified
    sha = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return {"slug": slug, "model": model, "date": date.today().isoformat(),
            "prose_sha": sha, "failed_windows": failed, "figures": figs}


def cmd_extract(args) -> None:
    if args.volume:
        targets = volume_scenes.volume_slugs(args.volume, drafted_only=True)
    else:
        targets = args.slugs or (gold_slugs() if args.gold else drafted_slugs())
    unknown = [s for s in targets if not (REPO / "scenes" / f"{s}.md").exists()]
    if unknown:
        raise SystemExit(f"no such scene: {', '.join(unknown)}")
    if not args.fresh:
        targets = [s for s in targets if not chapter_path(args.model_id, s).exists()]
    if not targets:
        print("[extract] nothing to do (use --fresh to redo)", file=sys.stderr)
        return
    print(f"[extract] {len(targets)} chapter(s) · {args.model} · jobs {args.jobs}",
          file=sys.stderr)
    local = threading.local()
    closers, lock = [], threading.Lock()

    def agent():
        if not hasattr(local, "fn"):
            fn, close = make_agent(args.model, args.effort,
                                   f"extract-{threading.get_ident()}")
            local.fn = fn
            with lock:
                closers.append(close)
        return local.fn

    def one(slug):
        data = extract_chapter(agent(), args.model, slug)
        if data["failed_windows"]:
            # Not saved: a partial chapter would be skipped by the next run.
            return (f"  [fail] {slug}: windows {', '.join(data['failed_windows'])} "
                    "returned nothing usable; not saved, rerun to retry")
        p = chapter_path(args.model_id, slug)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
        n = len(data["figures"])
        bad = sum(1 for f in data["figures"] if not f["verified"])
        return f"  {slug}: {n} figures" + (f" ({bad} unverified)" if bad else "")

    try:
        with ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futs = {ex.submit(one, s): s for s in targets}
            for f in as_completed(futs):
                try:
                    print(f.result(), file=sys.stderr)
                except Exception as e:  # keep going; the run is restartable
                    print(f"  [fail] {futs[f]}: {e}", file=sys.stderr)
    finally:
        for c in closers:
            c()


# ----------------------------------------------------------------- step 2

VEHICLE_SIM = 0.74   # nomic-embed-text cosine; set 2026-10-27 from a probe:
                     # lamp-light .75, lamp-bulb .77, stair-staircase .90 merge;
                     # light-sun .65, stair-ladder .66, stair-rail .47 do not.
EMBED_MODEL = "nomic-embed-text"
RARITY_FLOOR = 0.1   # figures per literal use of the noun; below this, the noun is mostly literal
GENERIC = {"thing", "way", "part", "bit", "kind", "something", "nothing", "one",
           "anything", "everything", "lot", "sort", "piece", "side", "end"}


def all_figures(model_id: str) -> list[dict]:
    out = []
    for p in sorted((model_dir(model_id) / "chapters").glob("*.json")):
        out.extend(json.loads(p.read_text(encoding="utf-8"))["figures"])
    return out


def union_dir(models: list[str], through: int | None = None) -> Path:
    name = "+".join(m.replace("/", "--") for m in models)
    return ROOT / (f"{name}--through-vol{through}" if through else name)


def through_slugs(through: int | None) -> set[str] | None:
    """Chapters of volumes 1..N: a cross-volume pass checks volume N against
    itself and every earlier volume (meta-plan-editorial-checklist.md)."""
    if not through:
        return None
    return {s for o in volume_scenes.volume_ordinals() if o <= through
            for s in volume_scenes.volume_slugs(o, drafted_only=True)}


STOP = set("""a an the and or but of to in on at by for from with as like than
that this it its it's he she him her his hers they them their you your we our i me
my was were is are be been had has have do did not no so then there here up down
out over into onto off way all one some any just very too more most""".split())


def words(s: str) -> set[str]:
    """Content words only: shared function words ("the way you … a") made two
    different figures on one line look like the same figure (boyfriend:13)."""
    return set(re.findall(r"[a-z']+", norm(s))) - STOP


def same_figure(a: dict, b: dict) -> bool:
    if a["slug"] != b["slug"] or abs(a["line"] - b["line"]) > 1:
        return False
    wa, wb = words(a["quote"]), words(b["quote"])
    return len(wa & wb) / max(1, min(len(wa), len(wb))) >= 0.5


def load_union(models: list[str]) -> list[dict]:
    """Every verified figure any model found, one record per figure.

    Cross-vendor union is the point (the fact-audit lesson): a figure one model
    missed and another caught is still a figure the reader meets."""
    merged: list[dict] = []
    by_slug: dict[str, list[dict]] = {}
    for m in models:
        for f in all_figures(m):
            if not f.get("verified"):
                continue
            hit = next((g for g in by_slug.get(f["slug"], []) if same_figure(f, g)), None)
            if hit:
                if m not in hit["found_by"]:
                    hit["found_by"].append(m)
                hit["vehicles"] = sorted(set(hit["vehicles"]) | set(f.get("vehicles", [])))
                hit["literal_maybe"] = hit["literal_maybe"] and f.get("literal_maybe", False)
                continue
            g = dict(f, found_by=[m], vehicles=sorted(set(f.get("vehicles", []))))
            merged.append(g)
            by_slug.setdefault(f["slug"], []).append(g)
    return merged


_NLP = None


def nlp():
    global _NLP
    if _NLP is None:
        import spacy
        _NLP = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    return _NLP


def lemmas(phrase: str) -> list[str]:
    """Noun lemmas of a vehicle phrase: 'stair rails' -> ['stair', 'rail']."""
    out = [t.lemma_.lower() for t in nlp()(phrase)
           if t.pos_ in ("NOUN", "PROPN") and t.lemma_.lower() not in GENERIC]
    if not out:   # a bare word spaCy mis-tags out of context: keep it
        w = phrase.strip().lower()
        out = [w] if w and " " not in w and w not in GENERIC else []
    return out


def corpus_counts() -> dict[str, int]:
    """Noun-lemma counts over every drafted chapter, cached by prose hash.

    A vehicle noun the book uses everywhere literally (face, hand, room) is
    weak evidence of a repeated figure; a rare one (stair, lamp) is strong."""
    texts = [(REPO / "scenes" / f"{s}.md").read_text(encoding="utf-8")
             for s in drafted_slugs()]
    key = hashlib.sha256("\n".join(texts).encode()).hexdigest()[:16]
    cache = ROOT / ".work" / f"corpus-lemmas-{key}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    counts: dict[str, int] = {}
    for doc in nlp().pipe(texts, batch_size=4):
        for t in doc:
            if t.pos_ == "NOUN":
                k = t.lemma_.lower()
                counts[k] = counts.get(k, 0) + 1
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(counts))
    return counts


def embed(texts: list[str]):
    import urllib.request
    import numpy as np
    vecs = []
    for i in range(0, len(texts), 256):
        req = urllib.request.Request(
            "http://localhost:11434/api/embed",
            data=json.dumps({"model": EMBED_MODEL, "input": texts[i:i + 256]}).encode(),
            headers={"Content-Type": "application/json"})
        try:
            vecs.extend(json.load(urllib.request.urlopen(req, timeout=300))["embeddings"])
        except OSError as e:
            raise SystemExit(f"Ollama embeddings unavailable ({e}); start `ollama serve`")
    v = np.array(vecs, dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def vehicle_families(lems: list[str], weight: dict[str, int]) -> dict[str, str]:
    """Union lemmas whose embeddings clear VEHICLE_SIM; name each family by its
    most-used member."""
    parent = {w: w for w in lems}

    def find(w):
        while parent[w] != w:
            parent[w] = parent[parent[w]]
            w = parent[w]
        return w
    if len(lems) > 1:
        v = embed(lems)
        sim = v @ v.T
        for i in range(len(lems)):
            for j in range(i + 1, len(lems)):
                if sim[i, j] >= VEHICLE_SIM:
                    parent[find(lems[i])] = find(lems[j])
    members: dict[str, list[str]] = {}
    for w in lems:
        members.setdefault(find(w), []).append(w)
    name = {}
    for ws in members.values():
        head = max(ws, key=lambda w: (weight.get(w, 0), -len(w)))
        for w in ws:
            name[w] = head
    return name


def cmd_group(args) -> None:
    figs = load_union(args.models)
    keep = through_slugs(args.through)
    if keep is not None:
        figs = [f for f in figs if f["slug"] in keep]
        unread = sorted(keep - {f["slug"] for f in figs})
        if unread:
            print(f"[group] warning: {len(unread)} chapter(s) of volumes 1-{args.through} "
                  f"have no figures yet: {', '.join(unread[:8])}"
                  + (" …" if len(unread) > 8 else ""), file=sys.stderr)
    if not figs:
        raise SystemExit("no extracted figures; run extract first")
    missing = [f for f in figs if "sensation" not in f]
    if missing:
        raise SystemExit(f"{len(missing)} figures predate the vehicles/sensation "
                         "fields; re-extract with --fresh")
    for f in figs:
        f["lemmas"] = sorted({l for v in f["vehicles"] for l in lemmas(v)})
    weight: dict[str, int] = {}
    for f in figs:
        for l in f["lemmas"]:
            weight[l] = weight.get(l, 0) + 1
    fam = vehicle_families(sorted(weight), weight)
    for f in figs:
        f["picture_families"] = sorted({fam[l] for l in f["lemmas"]})
        # GROUNDED: the noun is on the page ("missed stair" -> stair). An
        # inferred category ("object", "container") is the model's abstraction,
        # rare in the corpus only because the prose never says it, and it
        # floated to the top of the first report (2026-10-27).
        q = norm(f["quote"])
        qlem = {t.lemma_.lower() for t in nlp()(f["quote"])}
        f["grounded_families"] = sorted({fam[l] for l in f["lemmas"]
                                         if l in qlem or l in q})
    d = union_dir(args.models, args.through)
    d.mkdir(parents=True, exist_ok=True)
    (d / "groups.json").write_text(json.dumps(
        {"models": args.models, "date": date.today().isoformat(),
         "vehicle_sim": VEHICLE_SIM, "families": fam,
         "corpus": corpus_counts(), "figures": figs},
        indent=1, ensure_ascii=False), encoding="utf-8")
    both = sum(1 for f in figs if len(f["found_by"]) > 1)
    print(f"[group] {len(figs)} figures ({both} found by more than one model) · "
          f"{len(set(fam.values()))} picture families · {d / 'groups.json'}",
          file=sys.stderr)


# ----------------------------------------------------------------- step 3

def designed_families() -> dict[str, str]:
    """`- picture|sensation: <family> · <ruling>` lines, author-maintained."""
    out = {}
    if DESIGNED.exists():
        for m in re.finditer(r"^- (picture|sensation): ([^·\n]+?)\s*(?:·\s*(.*))?$",
                             DESIGNED.read_text(encoding="utf-8"), re.M):
            out[f"{m.group(1)}:{m.group(2).strip().lower()}"] = (m.group(3) or "").strip()
    return out


def person(applies_to: str) -> str:
    """'Vee's apology' -> 'Vee'; 'the room' -> 'the room'. People are what a
    reader tracks: one picture on two characters is the costly repeat."""
    w = applies_to.strip().split(" ")[0] if applies_to.strip() else ""
    w = re.sub(r"[’']s$", "", w)
    return w if w[:1].isupper() and w.lower() not in ("the", "a", "her", "his") else applies_to


def load_groups(models: list[str], through: int | None = None) -> dict:
    p = union_dir(models, through) / "groups.json"
    if not p.exists():
        raise SystemExit(f"no {p}; run group first")
    return json.loads(p.read_text(encoding="utf-8"))


def cmd_report(args) -> None:
    g = load_groups(args.models, args.through)
    order = {s: i for i, s in enumerate(drafted_slugs())}
    designed = designed_families()
    corpus, fam = g["corpus"], g["families"]
    members: dict[str, set] = {}
    for lem, head in fam.items():
        members.setdefault(head, set()).add(lem)
    groups: dict[str, list[dict]] = {}
    for f in g["figures"]:
        grounded = set(f.get("grounded_families", []))
        for pf in f["picture_families"]:
            kind = "picture" if pf in grounded else "inferred"
            groups.setdefault(f"{kind}:{pf}", []).append(f)
        if f["sensation"] and f["sensation"] != "none":
            groups.setdefault("sensation:" + f["sensation"], []).append(f)
    rows = []
    for key, figs in groups.items():
        chapters = {f["slug"] for f in figs}
        if len(chapters) < 2:
            continue
        people = {person(f["applies_to"]) for f in figs if f["applies_to"]}
        if key.startswith("picture:"):
            lit = sum(corpus.get(l, 0) for l in members.get(key[8:], {key[8:]}))
            rarity = len(figs) / (1 + lit)   # high: the noun is mostly figurative here
        else:
            rarity = 0.0
        rows.append((key, figs, chapters, people, rarity))
    section = {"picture": 0, "sensation": 1, "inferred": 2}
    # Spread is the cost: a picture met in 7 chapters is spent 6 times. Rarity
    # is a floor, not the key -- ranked by rarity alone, two-figure oddities
    # ("liquid", "reel") buried the stairs and the lamp (2026-10-27).
    rows.sort(key=lambda r: (r[0] in designed, section[r[0].split(":", 1)[0]],
                             r[0].startswith("picture:") and r[4] < RARITY_FLOOR,
                             -len(r[2]), -len(r[3]), -len(r[1])))
    scope = f" · volumes 1–{args.through}" if args.through else " · all drafted chapters"
    out = [f"# Figure sweep — {' + '.join(args.models)}{scope}\n",
           f"*{date.today().isoformat()} · families in 2+ chapters · picture families "
           f"on the page first (picture), then shared sensations, then pictures the "
           "models inferred but the prose never names (inferred); within each, most "
           "chapters first; a picture whose noun the book mostly uses literally "
           f"(rarity < {RARITY_FLOOR}) sinks to the end of its section · "
           "FLAGS, never findings: the author rules every family.*\n"]
    shown_designed = False
    for key, figs, chapters, people, rarity in rows:
        if key in designed and not shown_designed:
            out.append("\n---\n\n## Ruled designed (`designed.md`) — listed, not raised\n")
            shown_designed = True
        kind, name = key.split(":", 1)
        extra = (f" · members: {', '.join(sorted(members.get(name, {name})))}"
                 + (f" · rarity {rarity:.2f}" if kind == "picture" else "")
                 ) if kind != "sensation" else ""
        out.append(f"\n## {kind}: {name} — {len(figs)} figures, {len(chapters)} chapters, "
                   f"{len(people)} people{extra}\n")
        if key in designed and designed[key]:
            out.append(f"*Ruling: {designed[key]}*\n")
        for f in sorted(figs, key=lambda f: (order.get(f["slug"], 999), f["line"])):
            flag = " (literal?)" if f["literal_maybe"] else ""
            by = "" if len(f["found_by"]) > 1 else f" [{f['found_by'][0]} only]"
            out.append(f"- `{f['slug']}.md:{f['line']}` · {f['applies_to'] or '?'} · "
                       f"\"{f['quote']}\" — *{f['picture']}* / {f['sensation']}{flag}{by}")
    p = union_dir(args.models, args.through) / "report.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[report] {len(rows)} families · {p}", file=sys.stderr)


# ----------------------------------------------------------------- score

GOLD_RE = re.compile(r"^- (FIND|LITERAL) ([\w-]+):(\d+) · ([\w-]+) · (.+)$", re.M)
FEELING_GROUPS = {"drop"}   # gold groups judged by sensation, not by picture


def gold_rows():
    return [(m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5).strip())
            for m in GOLD_RE.finditer(GOLD.read_text(encoding="utf-8"))]


def gold_slugs() -> list[str]:
    return sorted({r[1] for r in gold_rows()})


def match(figs: list[dict], slug: str, line: int, quote: str) -> dict | None:
    """A figure on the gold line (or near it) whose quote overlaps the gold quote."""
    q = words(quote)
    best, best_score = None, 0.0
    for f in figs:
        if f["slug"] != slug or not f.get("verified", True) or abs(f["line"] - line) > NEAR:
            continue
        fq = words(f["quote"])
        # Against the SHORTER quote: models quote the minimal span, gold may not.
        score = len(q & fq) / max(1, min(len(q), len(fq)))
        if score > best_score:
            best, best_score = f, score
    return best if best_score >= 0.5 else None


def cmd_score(args) -> None:
    gpath = union_dir(args.models, args.through) / "groups.json"
    grouped_ok = gpath.exists()
    figs = (json.loads(gpath.read_text())["figures"] if grouped_ok
            else [f for m in args.models for f in all_figures(m)])
    have = {f["slug"] for f in figs}
    hits, misses, false_pos, skipped = [], [], [], []
    by_group: dict[str, list[dict]] = {}
    for kind, slug, line, group, quote in gold_rows():
        if slug not in have:
            skipped.append(f"{slug}:{line}")
            continue
        m = match(figs, slug, line, quote)
        if kind == "FIND":
            (hits if m else misses).append((slug, line, group, quote))
            if m:
                by_group.setdefault(group, []).append(m)
        elif m and not m["literal_maybe"]:
            false_pos.append((slug, line, group, quote, m))
    total = len(hits) + len(misses)
    print(f"recall: {len(hits)}/{total}" + (f" ({len(hits) / total:.0%})" if total else ""))
    print(f"literal reported as figure: {len(false_pos)}")
    if skipped:
        print(f"not extracted yet (skipped): {', '.join(skipped)}")
    for slug, line, group, quote in misses:
        print(f"  MISS {slug}:{line} [{group}] {quote}")
    for slug, line, group, quote, m in false_pos:
        print(f"  LITERAL-AS-FIGURE {slug}:{line} [{group}] {quote} -> {m['quote']}")
    if not grouped_ok:
        print("grouping: not scored (run group first)")
        return
    print("grouping (every found member of a gold group should share one family):")
    for group, ms in sorted(by_group.items()):
        if group in FEELING_GROUPS:
            sets = [{f["sensation"]} for f in ms]
        else:
            sets = [set(f["picture_families"]) for f in ms]
        common = set.intersection(*sets) if sets else set()
        mark = "ok" if common else "SPLIT"
        detail = ", ".join(sorted(common)) if common else " | ".join(
            f"{f['slug']}:{f['line']}={'/'.join(sorted(s)) or '-'}" for f, s in zip(ms, sets))
        print(f"  {mark:5} {group}: {detail}")


# ----------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("extract")
    p.add_argument("--model", default="gpt-6.1-terra")
    p.add_argument("--model-id", default=None, help="output dir (default: --model)")
    p.add_argument("--effort", default="medium")
    p.add_argument("--slugs", nargs="*")
    p.add_argument("--gold", action="store_true", help="only chapters in gold.md")
    p.add_argument("--volume", type=int, help="every drafted chapter of this volume")
    p.add_argument("--fresh", action="store_true", help="redo existing chapters")
    p.add_argument("--jobs", type=int, default=4)
    for name in ("group", "report", "score"):
        q = sub.add_parser(name)
        q.add_argument("--models", nargs="+", default=list(DEFAULT_MODELS),
                       help="model result dirs to union")
        q.add_argument("--through", type=int, default=None,
                       help="only volumes 1..N (a volume's sweep includes every earlier one)")
    args = ap.parse_args()
    if args.cmd == "extract":
        args.model_id = args.model_id or args.model
    {"extract": cmd_extract, "group": cmd_group,
     "report": cmd_report, "score": cmd_score}[args.cmd](args)


if __name__ == "__main__":
    main()
