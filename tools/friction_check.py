#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Rank a chapter's reader complaints by concentration, corroboration and counter-praise.

The mirror of `praise_check.py`. That tool weighs the praise behind a cut; this
one weighs the complaint. The problem it answers: the Anthropic reader lanes
(claude-*: opus, sonnet, fable) produce about the same volume of criticism on
every chapter, so criticism alone does not separate a real defect from a
trained-in reviewer complaint ("a touch on the nose", "the author's hand").
The working assumption is that real critique CONCENTRATES — independent reads
(different models, personas, memory eras) land on the same passage — and is
CORROBORATED by other model families, while trained-in complaint SCATTERS.

Corpus (reactions, not canon), one file = one independent READ, keyed
(model, source, persona):
  * cold reads      reviews/cold-read/<model>/<slug>.md          (source "cold")
  * capture gates   reviews/capture-panel/<model>/<dag|dag-v3>/<persona>/gate-chNNN.md
  * --include-experiments adds reviews/capture-panel/split-experiments/<exp>/…
    (source "<dag>:<exp>").
Only model directories whose id maps to a known family are read.

Extraction. A complaint is only countable if it points at the page, so the
unit is a QUOTE: text in straight/curly double quotes or a *single-star* italic
span, at least MIN_QUOTE_WORDS words (MIN_QUOTE_WORDS_FIELD inside an
ALMOST-STOPPED field), verified against scenes/<slug>.md with punctuation and
case ignored. A quote need not be exact: the longest contiguous run of its
words found in the chapter is used if it is at least that many words, holds at
least MIN_CONTENT content words, and covers PARTIAL_FRACTION of the quote
(reviewers trim and misquote). The verified run anchors to a scene line.

Classification (transparent; lexicon in COMPLAINT_STRONG / COMPLAINT_WEAK /
PRAISE below — edit freely). The sentence holding the quote is classified with
the quoted words masked out, so the prose's own words never count as a cue:
  * a negated cue ("no friction", "didn't land") is dropped, except negated
    praise ("doesn't land", "not earned"), which becomes a strong complaint;
  * strong complaint + praise           -> mixed   ("runs long but earns it")
  * strong or weak complaint, no praise -> complaint
  * weak complaint + praise             -> praise
  * praise only                         -> praise
  * nothing                             -> the next sentence, if it carries no
                                           quote of its own, is classified instead
                                           (strong cues and praise only)
Paragraph context overrides: a paragraph opening with a CONTEXT_COMPLAINT
label (Friction:, Gripes., ALMOST-STOPPED:) or sitting under a heading that
names friction is complaint (mixed if a praise cue is present);
one opening with a CONTEXT_PRAISE label (+ LOVE:) is praise (mixed if a strong
complaint cue is present). Capture-ledger "+ GRUDGE:" lines are NOT complaint
context: the prompt defines a grudge as held "against the book or a
character", and most are against a character, so they are classified on their
own words like any other line. A read's stance on a passage is the union of its
quotes: complaint+praise -> mixed.

Grouping. Quotes whose anchors share or overlap scene lines are one PASSAGE.
Scene lines are paragraphs, so a passage is a paragraph (or a run of them).

Scoring per passage.
  complaint_reads   distinct reads whose stance is complaint, by family
                    (mixed reads are counted separately and do not score)
  concentration     Anthropic complaint reads on this passage divided by the
                    chapter's Anthropic base rate = Anthropic (read, passage)
                    complaint pairs / passages with >= 1 Anthropic complaint
  corroboration     non-Anthropic families with a complaint read here
  counter_praise    reads praising the passage, by family

Verdicts, checked in this order:
  CONTESTED  >= 1 complaint read, and more families praise it than complain
  REAL       Anthropic-concentrated and corroboration >= 1; or >= 2
             non-Anthropic families complain (agreement that does not lean on
             the Anthropic lanes at all)
  TASTE      Anthropic-concentrated, no other family complains
  NOISE      everything else: a single read, or complaint that does not
             concentrate
  where Anthropic-concentrated = >= CONC_MIN_READS Anthropic complaint reads
  and concentration >= CONC_MIN_RATIO.

Mechanical, free, deterministic. Like praise_check it FLAGS, never finds: the
classifier is a lexicon, and a quote can be cited in passing. Read the
snippets. The author rules.

Usage:
    tools/friction_check.py --slug sorority
    tools/friction_check.py --volume 1 --top 3
    tools/friction_check.py --slug sorority --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "reviews"
COLD = REVIEWS / "cold-read"
PANEL = REVIEWS / "capture-panel"
EXPERIMENTS = PANEL / "split-experiments"
sys.path.insert(0, str(ROOT / "tools"))

# --------------------------------------------------------------------------
# Tunables
# --------------------------------------------------------------------------

MIN_QUOTE_WORDS = 4          # quoted span, in words, to count at all
MIN_QUOTE_WORDS_FIELD = 3    # inside an ALMOST-STOPPED field ("You lucky slut.")
MIN_CONTENT = 2              # non-stopwords the verified run must hold
PARTIAL_FRACTION = 0.6       # verified run / quote length, for a misquote
CONC_MIN_READS = 2           # Anthropic complaint reads to be "concentrated"
CONC_MIN_RATIO = 1.5         # ... and at least this times the chapter base rate

ANTHROPIC = "Anthropic"
FAMILIES = {           # model-id prefix -> family
    "claude-": ANTHROPIC,
    "gpt-": "OpenAI",
    "gemini-": "Google",
    "glm-": "Zhipu",
    "deepseek-": "DeepSeek",
    "muse-": "Meta",
    "kimi-": "Moonshot",
    "qwen-": "Alibaba",
}

# --------------------------------------------------------------------------
# Lexicon. Regexes, matched case-insensitively against the sentence with its
# quotes masked out. STRONG complaint cues name a craft fault; WEAK ones are
# ambiguous ("again", "winced" can be about the plot) and yield to praise.
# --------------------------------------------------------------------------

COMPLAINT_STRONG = [
    r"\bdrag(s|ged|ging|gy)?\b", r"\bsag(s|ged|ging|gy)?\b",
    r"\b(too|over-?)long\b", r"\bruns? (a (touch|bit|little) |too )?long\b",
    r"\bgoes on (too|a beat|a bit)\b",
    r"\bon[- ]the[- ]nose\b", r"\bheavy[- ]handed\b",
    r"\bauthor'?s (hand|thumb|finger)\b", r"\bthe author\b",
    r"\bunderlin(e|ed|es|ing)\b", r"\btelegraph", r"\bover-?explain",
    r"\bspell(s|ed|ing)? (it|this|that)? ?out\b", r"\bcaption",
    r"\btidy\b", r"\btoo neat\b", r"\bconvenient", r"\bcontriv",
    r"\bclich", r"\btrope", r"\brepetiti", r"\brerun",
    r"\bclums", r"\bsmug\b", r"\beye[- ]?roll", r"\broll(ed)? my eyes",
    r"\bfelt managed\b", r"\b(pulled|knocked|threw|kicked) me out\b",
    r"\bfriction\b", r"\bgripe", r"\bsnag\b", r"\bnitpick", r"\bquibbl", r"\b(falls?|fell|felt|reads?|went|goes) flat\b", r"\bsigh(ed)?\b",
    r"\bfiller\b", r"\bpadding\b", r"\bpreach", r"\btapping the glass\b",
    r"\bdidn'?t need\b", r"\bforced\b", r"\bmechanical\b", r"\bpurple\b",
    r"\boverwr", r"\boverdone\b", r"\btoo much\b", r"\bannoy", r"\birritat",
    r"\bskimm?(ed|ing)?\b", r"\btedious", r"\bboring\b", r"\bbored\b",
    r"\bcringe", r"\bconspicuous", r"\binstruct(s|ed|ing)? me\b",
    r"\bwearing (on|thin)\b", r"\bwore thin\b", r"\bclunk",
    r"\bself-conscious", r"\bsignpost", r"\bwink(s|ing)?\b", r"\bnudg",
    r"\b(little|bit|touch) neat\b", r"\bmannered\b", r"\bshowing off\b",
    r"\bdad joke\b", r"\bdoesn'?t mean anything\b", r"\bmeaningless\b",
    r"\bthesis statement\b", r"\blecture slide\b", r"\bon the page as\b",
    r"\bwish(ed)? (it|the book|the author)\b", r"\bcould (lose|cut)\b",
]
COMPLAINT_WEAK = [
    r"\byet again\b", r"\b(the same|another|one more)\b[^.]{0,40}\bagain\b",
    r"\bexplain(s|ed|ing)?\b",
    r"\bwinc(e|ed|ing)\b", r"\bmanaged\b", r"\bstock\b", r"\bdevice\b",
    r"\blabel+(ed|s)?\b", r"\bstrain", r"\bthin\b", r"\bodd\b",
    r"\bconfus", r"\bmiss(ed)? (a|the) beat\b", r"\bheavy\b", r"\bweak(est|er)?\b",
    r"\breplay(s|ed)?\b", r"\bcut (it|this|that)\b",
]
PRAISE = [
    r"\blove[ds]?\b", r"\bperfect", r"\bgorgeous", r"\bearn(s|ed)?\b",
    r"\bland(s|ed)?\b", r"\bbest\b", r"\bdevastat", r"\bthrill", r"\bswoon",
    r"\bthe line\b", r"\bfunniest\b", r"\bhottest\b", r"\bbeautiful",
    r"\blovely\b", r"\bmoved me\b", r"\bgot me\b", r"\bdelight",
    r"\bbrilliant", r"\bexquisite", r"\bprecise", r"\bfavou?rite",
    r"\bstunning", r"\bwonderful", r"\bkilled me\b", r"\bchills\b",
    r"\bmy heart\b", r"\blaugh(ed)? out loud\b", r"\bgrinn?(ing|ed)?\b",
    r"\bworks\b", r"\bworked\b", r"\bsharp\b", r"\bexact(ly right)?\b",
    r"\bclever", r"\belegant", r"\bgreat\b", r"\b(is|was|so|really) good\b", r"\bhot\b", r"\bsexy\b", r"\btender",
]
# Praise cues negated this way are complaints ("doesn't land", "not earned").
NEGATION = re.compile(
    r"\b(no|not|never|nothing|without|hardly|barely|didn'?t|doesn'?t|don'?t|"
    r"isn'?t|wasn'?t|won'?t|can'?t|couldn'?t|fails? to|failed to)\W+(\w+\W+){0,2}$",
    re.I)

CONTEXT_COMPLAINT = re.compile(
    r"^(friction|gripes?|almost[- ]stopped|quibbles?|complaints?|"
    r"nitpicks?|what didn.t work|weak(ness|nesses)?|problems?|reservations?)\b",
    re.I)
CONTEXT_PRAISE = re.compile(r"^(loves?|loved|highlights?|what worked)\b", re.I)
FIELD = re.compile(r"^almost[- ]stopped\b", re.I)

STOP = set("""a an the and or but if then so of to in on at by for with from up down out
off over under into onto as is was were be been being am are it its it's this that these
those he she him her his hers they them their we us our you your i me my mine not no nor
had has have do did does done would could should will can may might must just only very
too all any some each every one two what which who whom whose when where why how there
here than like still even more most much many such own same back again ever never once
s t d ll re ve m""".split())

WORD = re.compile(r"[A-Za-z][A-Za-z'’]*")
QUOTE_RES = [
    re.compile(r'"([^"\n]+)"'),
    re.compile(r"“([^”\n]+)”"),
    re.compile(r"(?<![*\w])\*(?![*\s])([^*\n]+?)(?<![*\s])\*(?![*\w])"),
]
BOUNDARY = re.compile(r"[.!?…]+[\"”*)\]]*\s+")
_C_STRONG = [re.compile(p, re.I) for p in COMPLAINT_STRONG]
_C_WEAK = [re.compile(p, re.I) for p in COMPLAINT_WEAK]
_PRAISE = [re.compile(p, re.I) for p in PRAISE]


def words(text: str) -> list[str]:
    return [w.lower().replace("’", "'") for w in WORD.findall(text)]


def family(model: str) -> str | None:
    for pre, fam in FAMILIES.items():
        if model.startswith(pre):
            return fam
    return None


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------

def _hits(pats, text: str) -> tuple[int, int]:
    """(un-negated hits, negated hits)."""
    pos = neg = 0
    for p in pats:
        for m in p.finditer(text):
            if NEGATION.search(text[max(0, m.start() - 40):m.start()]):
                neg += 1
            else:
                pos += 1
    return pos, neg


def classify(sentence: str, context: str = "", weak_cues: bool = True) -> str:
    """complaint | praise | mixed | neutral, for a sentence with quotes masked.
    weak_cues=False ignores COMPLAINT_WEAK (used for the look-ahead sentence)."""
    strong, _ = _hits(_C_STRONG, sentence)
    weak = _hits(_C_WEAK, sentence)[0] if weak_cues else 0
    praise, neg_praise = _hits(_PRAISE, sentence)
    strong += neg_praise
    if context == "complaint":
        return "mixed" if praise else "complaint"
    if context == "praise":
        return "mixed" if strong else "praise"
    if strong and praise:
        return "mixed"
    if strong or (weak and not praise):
        return "complaint"
    if praise:
        return "praise"
    return "neutral"


def paragraph_context(line: str, section: str) -> str:
    head = line.lstrip("*+-~> \t")
    if CONTEXT_COMPLAINT.match(head):
        return "complaint"
    if CONTEXT_PRAISE.match(head):
        return "praise"
    return section


# --------------------------------------------------------------------------
# The chapter
# --------------------------------------------------------------------------

class Scene:
    """Flat word list of a chapter with a line number per word, and a 3-gram index."""

    def __init__(self, text: str):
        self.lines = text.splitlines()
        self.w: list[str] = []
        self.ln: list[int] = []
        for i, line in enumerate(self.lines, 1):
            for x in words(line):
                self.w.append(x)
                self.ln.append(i)
        self.idx: dict[tuple, list[int]] = defaultdict(list)
        for p in range(len(self.w) - 2):
            self.idx[tuple(self.w[p:p + 3])].append(p)

    def verify(self, quote: str, min_words: int = MIN_QUOTE_WORDS):
        """(first_line, last_line, matched_words) for the longest run of the quote
        found in the chapter, or None if it does not qualify."""
        q = words(quote)
        if len(q) < min_words:
            return None
        best = (0, -1)
        for i in range(len(q) - 2):
            for p in self.idx.get(tuple(q[i:i + 3]), ()):
                k = 3
                while i + k < len(q) and p + k < len(self.w) and self.w[p + k] == q[i + k]:
                    k += 1
                if k > best[0]:
                    best = (k, p)
        k, p = best
        if k < min_words or (k < len(q) and k < PARTIAL_FRACTION * len(q)):
            return None
        run = self.w[p:p + k]
        if sum(x not in STOP for x in run) < MIN_CONTENT:
            return None
        return self.ln[p], self.ln[p + k - 1], " ".join(run)


# --------------------------------------------------------------------------
# Reads
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Read:
    model: str
    source: str     # cold | dag | dag-v3 | dag-v3:<experiment>
    persona: str    # 'cold' for cold reads
    path: Path

    @property
    def family(self) -> str:
        return family(self.model) or "?"

    @property
    def label(self) -> str:
        return self.model + ("" if self.source == "cold" else f" {self.source}/{self.persona}")


@dataclass
class Hit:
    read: Read
    lines: tuple[int, int]
    quote: str
    stance: str
    snippet: str
    file_line: int


def chapter_number(slug: str) -> int | None:
    try:
        import volume_scenes  # noqa: PLC0415
        return volume_scenes.chapter_number(slug)
    except Exception:
        return None


def find_reads(slug: str, include_experiments: bool = False) -> list[Read]:
    reads = []
    if COLD.is_dir():
        for d in sorted(COLD.iterdir()):
            p = d / f"{slug}.md"
            if d.is_dir() and family(d.name) and p.is_file():
                reads.append(Read(d.name, "cold", "cold", p))
    n = chapter_number(slug)
    if n:
        gate = f"gate-ch{n:03d}.md"
        for p in sorted(PANEL.glob(f"*/*/*/{gate}")):
            model, src, persona = p.parts[-4:-1]
            if family(model) and src.startswith("dag"):
                reads.append(Read(model, src, persona, p))
        if include_experiments:
            for p in sorted(EXPERIMENTS.glob(f"*/*/*/*/{gate}")):
                exp, model, src, persona = p.parts[-5:-1]
                if family(model) and src.startswith("dag"):
                    reads.append(Read(model, f"{src}:{exp}", persona, p))
    return reads


def body_lines(read: Read) -> list[tuple[int, str]]:
    """(file line number, text) for the part of the file that is reaction."""
    lines = read.path.read_text(errors="replace").splitlines()
    sectioned = read.source == "cold" and any(l.startswith("## ") for l in lines)
    out, on = [], not sectioned
    for i, line in enumerate(lines, 1):
        if sectioned and line.startswith("## "):
            on = line.lower().startswith("## reader reaction")
            continue
        if not on:
            continue
        s = line.strip()
        if s.startswith("*") and s.endswith("*") and " · " in s:   # provenance header
            continue
        out.append((i, line))
    return out


def mask(text: str) -> tuple[str, list[tuple[int, int, str]]]:
    """Replace quoted inner text with '§' and return the quote spans."""
    spans = []
    for rx in QUOTE_RES:
        for m in rx.finditer(text):
            if any(a <= m.start(1) < b for a, b, _ in spans):
                continue
            spans.append((m.start(1), m.end(1), m.group(1)))
    chars = list(text)
    for a, b, q in spans:
        # keep the quote's own closing punctuation so "…he said." ends a sentence
        b -= len(q) - len(q.rstrip(".!?…"))
        for j in range(a, b):
            chars[j] = "§"
    return "".join(chars), sorted(spans)


def sentences(masked: str) -> list[tuple[int, int]]:
    cuts = [0] + [m.end() for m in BOUNDARY.finditer(masked)] + [len(masked)]
    return [(a, b) for a, b in zip(cuts, cuts[1:]) if b > a]


def extract(read: Read, scene: Scene) -> list[Hit]:
    hits: list[Hit] = []
    section = ""
    for fl, line in body_lines(read):
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or re.fullmatch(r"\*\*[^*]+\*\*:?", s):
            section = "complaint" if re.search(r"friction|gripe|complain|weakness", s, re.I) else ""
            continue
        ctx = paragraph_context(s, section)
        is_field = bool(FIELD.match(s.lstrip("*+-~> ")))
        masked, spans = mask(line)
        sents = sentences(masked)
        verified = []
        for a, b, q in spans:
            v = scene.verify(q, MIN_QUOTE_WORDS_FIELD if is_field else MIN_QUOTE_WORDS)
            if v:
                si = next(k for k, (x, y) in enumerate(sents) if x <= a < y)
                verified.append((si, v))
        quoted = {si for si, _ in verified}
        for si, (l1, l2, run) in verified:
            x, y = sents[si]
            stance = classify(masked[x:y], ctx)
            if stance == "neutral" and si + 1 < len(sents) and si + 1 not in quoted:
                nx, ny = sents[si + 1]
                stance = classify(masked[nx:ny], weak_cues=False)
            hits.append(Hit(read, (l1, l2), run, stance,
                            line[x:y].strip(), fl))
    return hits


# --------------------------------------------------------------------------
# Passages and scoring
# --------------------------------------------------------------------------

def group(hits: list[Hit]) -> list[list[Hit]]:
    """Merge hits whose scene-line ranges share or overlap lines."""
    out: list[tuple[int, int, list[Hit]]] = []
    for h in sorted(hits, key=lambda h: h.lines):
        if out and h.lines[0] <= out[-1][1]:
            a, b, hs = out[-1]
            out[-1] = (a, max(b, h.lines[1]), hs + [h])
        else:
            out.append((h.lines[0], h.lines[1], [h]))
    return [hs for _, _, hs in out]


def stance_of(hs: list[Hit]) -> str:
    st = {h.stance for h in hs} - {"neutral"}
    if "mixed" in st or {"complaint", "praise"} <= st:
        return "mixed"
    return next(iter(st), "neutral")


VERDICT_ORDER = {"REAL": 0, "TASTE": 1, "CONTESTED": 2, "NOISE": 3}


def score(slug: str, reads: list[Read], scene: Scene) -> dict:
    hits = [h for r in reads for h in extract(r, scene)]
    passages = []
    for hs in group(hits):
        by_read: dict[Read, list[Hit]] = defaultdict(list)
        for h in hs:
            by_read[h.read].append(h)
        stances = {r: stance_of(v) for r, v in by_read.items()}
        passages.append({"hits": hs, "by_read": by_read, "stances": stances})

    def fam_count(p, want):
        c: dict[str, int] = defaultdict(int)
        for r, s in p["stances"].items():
            if s == want:
                c[r.family] += 1
        return dict(sorted(c.items()))

    a_pairs = a_passages = 0
    for p in passages:
        p["complaint"] = fam_count(p, "complaint")
        p["mixed"] = fam_count(p, "mixed")
        p["praise"] = fam_count(p, "praise")
        n = p["complaint"].get(ANTHROPIC, 0)
        a_pairs += n
        a_passages += bool(n)
    base = a_pairs / a_passages if a_passages else 0.0

    out = []
    for p in passages:
        comp, praise = p["complaint"], p["praise"]
        if not comp and not p["mixed"]:
            continue
        a = comp.get(ANTHROPIC, 0)
        ratio = a / base if base else 0.0
        others = [f for f in comp if f != ANTHROPIC]
        concentrated = a >= CONC_MIN_READS and ratio >= CONC_MIN_RATIO
        if comp and len(praise) > len(comp):
            verdict = "CONTESTED"
        elif (concentrated and others) or len(others) >= 2:
            verdict = "REAL"
        elif concentrated:
            verdict = "TASTE"
        else:
            verdict = "NOISE"
        l1 = min(h.lines[0] for h in p["hits"])
        l2 = max(h.lines[1] for h in p["hits"])
        quotes: dict[str, int] = defaultdict(int)
        for h in p["hits"]:
            if h.stance in ("complaint", "mixed"):
                quotes[h.quote] += 1
        evidence = []
        for r, s in p["stances"].items():
            if s not in ("complaint", "mixed"):
                continue
            h = next(h for h in p["by_read"][r] if h.stance == s or s == "mixed")
            evidence.append({"read": r.label, "family": r.family, "stance": s,
                             "snippet": h.snippet,
                             "file": f"{r.path.relative_to(ROOT)}:{h.file_line}"})
        evidence.sort(key=lambda e: (e["stance"] != "complaint", e["family"] != ANTHROPIC,
                                     e["family"], e["read"]))
        out.append({
            "verdict": verdict,
            "scene": f"scenes/{slug}.md:{l1}" + (f"-{l2}" if l2 != l1 else ""),
            "passage": max(quotes, key=lambda q: (quotes[q], len(q))) if quotes
                       else p["hits"][0].quote,
            "complaint_reads": sum(comp.values()),
            "complaint_by_family": comp,
            "mixed_by_family": p["mixed"],
            "praise_by_family": praise,
            "anthropic_complaint_reads": a,
            "concentration": round(ratio, 2),
            "corroboration": len(others),
            "evidence": evidence,
        })
    out.sort(key=lambda d: (VERDICT_ORDER[d["verdict"]], -d["corroboration"],
                            -d["concentration"], -d["complaint_reads"],
                            -sum(d["mixed_by_family"].values())))
    src: dict[str, int] = defaultdict(int)
    for r in reads:
        src[r.source.split(":")[0]] += 1
    return {"slug": slug, "chapter": chapter_number(slug), "reads": len(reads),
            "reads_by_source": dict(src), "quotes_verified": len(hits),
            "anthropic_base_rate": round(base, 2), "passages": out}


def check(slug: str, include_experiments: bool = False) -> dict:
    path = ROOT / "scenes" / f"{slug}.md"
    if not path.exists():
        raise SystemExit(f"no such chapter: {path.relative_to(ROOT)}")
    return score(slug, find_reads(slug, include_experiments), Scene(path.read_text()))


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def _fams(d: dict) -> str:
    return ", ".join(f"{k} {v}" for k, v in d.items()) or "-"


def report(res: dict, top: int, snippets: int) -> None:
    ch = f"ch{res['chapter']:03d} " if res["chapter"] else ""
    srcs = ", ".join(f"{k} {v}" for k, v in sorted(res["reads_by_source"].items()))
    print(f"\n== {ch}{res['slug']} — {res['reads']} reads ({srcs}); "
          f"{res['quotes_verified']} verified quotes; Anthropic base rate "
          f"{res['anthropic_base_rate']} complaint reads/passage")
    ps = res["passages"]
    if not ps:
        print("   (no complaints anchored to the page)")
        return
    for i, p in enumerate(ps[:top], 1):
        txt = p["passage"]
        txt = txt if len(txt) <= 90 else txt[:87] + "…"
        print(f"{i:>3}. {p['verdict']:<9} {p['scene']}  «{txt}»")
        print(f"     complain: {_fams(p['complaint_by_family'])} | "
              f"conc {p['concentration']}x ({p['anthropic_complaint_reads']} vs "
              f"{res['anthropic_base_rate']}) | corrob {p['corroboration']} | "
              f"mixed: {_fams(p['mixed_by_family'])} | praise: {_fams(p['praise_by_family'])}")
        for e in p["evidence"][:snippets]:
            s = e["snippet"]
            s = s if len(s) <= 150 else s[:147] + "…"
            tag = "" if e["stance"] == "complaint" else " [mixed]"
            print(f"       - {e['read']}{tag}: {s}  ({e['file']})")
        if len(p["evidence"]) > snippets:
            print(f"       … {len(p['evidence']) - snippets} more")
    if len(ps) > top:
        rest = defaultdict(int)
        for p in ps[top:]:
            rest[p["verdict"]] += 1
        print(f"     (+{len(ps) - top} more: " +
              ", ".join(f"{k} {v}" for k, v in sorted(rest.items(), key=lambda kv: VERDICT_ORDER[kv[0]])) + ")")


LEGEND = ("REAL = concentrated in Anthropic reads and echoed by another family, or "
          ">=2 other families; TASTE = concentrated, Anthropic-only; CONTESTED = more "
          "families praise than complain; NOISE = single or scattered. conc = Anthropic "
          "complaint reads here / chapter base rate.")


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--slug", help="one chapter")
    g.add_argument("--volume", help="every drafted chapter of volume N")
    ap.add_argument("--top", type=int, default=5, help="passages per chapter (text report)")
    ap.add_argument("--snippets", type=int, default=6, help="evidence lines per passage")
    ap.add_argument("--include-experiments", action="store_true",
                    help="also read capture-panel/split-experiments gates")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.slug:
        slugs = [args.slug]
    else:
        import volume_scenes  # noqa: PLC0415
        vol = int(args.volume) if args.volume.isdigit() else args.volume
        slugs = volume_scenes.volume_slugs(vol)
    results = [check(s, args.include_experiments) for s in slugs]

    if args.json:
        json.dump(results if args.volume else results[0], sys.stdout, indent=1,
                  ensure_ascii=False)
        print()
        return 0
    for r in results:
        report(r, args.top, args.snippets)
    print("\n" + LEGEND)
    print("FLAGS, not findings: the classifier is a lexicon and a quote can be cited "
          "in passing. Read each snippet; the author rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
