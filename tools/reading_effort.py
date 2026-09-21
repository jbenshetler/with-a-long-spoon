#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"    # stdlib tomllib, as na.py (rulings are TOML)
# dependencies = [
#   "spacy>=3.8,<3.9",
#   "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""Measure the reading effort a sentence charges the reader, and flag the
structures where an idea has been split when it did not have to be.

The defect class, from human reader feedback on `the-bench.md` (2026-09-20):
one idea gets divided across stacked subordinate clauses, or across a sentence
boundary, when a rearrangement would carry the same content at lower cost. The
prose is not *wrong* anywhere; it just makes the reader hold more open than the
sentence pays back.

This is deterministic: a fixed spaCy dependency parse (en_core_web_sm 3.8.0, no
sampling, no network at run time after the first install) plus arithmetic over
the parse. The same file scores the same every run.

What it measures, and why each is a cost the reader actually pays:

  open      Peak OPEN DEPENDENCIES — the most unresolved syntactic arcs
            spanning any single point in the sentence. The closest thing to a
            working-memory gauge: how many threads the reader is holding at the
            hardest moment. This is the headline number.
  depth     CLAUSE EMBEDDING DEPTH — clausal links (advcl/relcl/ccomp/xcomp/
            acl/csubj/verbal pcomp) on the longest root-to-leaf path. Six here
            means the idea was handed down through six subordinations.
            Coordination (`conj`) is deliberately NOT counted: "A and B" is
            cheap, and this book's long coordinate sentences read fast.
  mdd       MEAN DEPENDENCY DISTANCE — average linear gap between a word and
            its head (Liu 2008). Integration cost, averaged over the sentence.
  sv        Longest SUBJECT-VERB distance: how far a subject waits for its
            predicate.
  predelay  Words before the main verb (ROOT) lands — left-branching load, the
            costliest kind, since nothing can be discharged until it arrives.

And four flag classes — the structures where rearrangement is usually free:

  chain     Deep subordination stack (an idea passed down N clause levels).
  suspend   A dash/paren interruption the main clause RESUMES after, so the
            reader has to hold and re-find the thread.
  strand    A modifier whose head is far back with another finite clause in
            between: the reader must reattach across an intervening clause.
  split     An idea continued into the next sentence — a verbless fragment, or
            a sentence opening on a connective, after a long sentence. The
            "split across multiple sentences" half of the feedback.

Like `echo_harvest.py` and `orphan_refs.py` this FLAGS, NEVER FIXES, and it
over-flags on purpose. High effort is not a defect: suspension is a real device
(the reader holds the sentence the way the character holds still), fragments
are this book's registering-beat, and the accretive tail is a deliberate voice.
Separating a load the prose earns from one it does not is the author's ruling.
Scores are RELATIVE TO THIS BOOK — every number is reported against the corpus
baseline, so "hard" means hard for this author, not hard for an arbitrary index.

Usage:
    tools/reading_effort.py the-bench              # one chapter vs. the corpus
    tools/reading_effort.py the-bench --top 40
    tools/reading_effort.py the-bench --class suspend,strand
    tools/reading_effort.py the-bench --explain 49 # why that sentence is heavy
    tools/reading_effort.py --corpus               # rank every chapter
    tools/reading_effort.py the-bench --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCENES = REPO / "scenes"
AUDITS = REPO / "audits" / "reading-effort"
CACHE = AUDITS / "cache.json"          # machine scratch, gitignored
RULINGS = AUDITS / "rulings.toml"      # author decisions, tracked in git
# Bump when a metric or threshold changes: cached rows computed under the old
# rules must not be mixed into a new baseline.
ALGO = "v6"

# ---------------------------------------------------------------------------
# Thresholds. Each is the point above which a structure starts costing enough
# to be worth the author's eye; the penalty is the EXCESS over the threshold,
# so a sentence one notch over barely registers. Calibrated against this
# corpus (see --corpus percentiles), not against general English.
# ---------------------------------------------------------------------------
T_OPEN = 7          # peak open dependencies
T_DEPTH = 4         # clause embedding depth
T_PREDELAY = 12     # words before the main verb
T_SV = 10           # subject-verb distance
T_SUSPEND = 8       # words inside a resumed interruption
T_RESUME = 3        # words of main clause after it, to count as "resumed"
T_STRAND = 8        # head-to-modifier gap for a stranded modifier
T_STRAND_SPAN = 3   # …and the modifier must itself be this many words
T_LONG_PRIOR = 18   # a prior sentence this long makes a following fragment a
                    # candidate for rejoining rather than a deliberate beat
T_FRAGMENT = 8      # below this a verbless sentence is a beat, not a split
T_BREATHER = 10     # a sentence this short (and shallow) is where the reader
                    # sets the load down
WINDOW_WORDS = 220  # fatigue window: roughly a screen / a long paragraph pair

W_OPEN, W_DEPTH, W_PREDELAY, W_SV = 2.0, 3.0, 0.5, 0.4
W_SUSPEND, W_STRAND = 0.8, 4.0

# Clausal dependency labels: each one is a whole predication hung off another.
# `conj` is excluded on purpose (coordination is cheap; see module docstring).
CLAUSAL = {"advcl", "relcl", "ccomp", "xcomp", "acl", "csubj", "csubjpass"}
STRAND_DEPS = {"prep", "advcl", "acl", "appos", "npadvmod"}
FINITE_TAGS = {"VBD", "VBP", "VBZ", "MD"}
OPEN_DASH = {"—", "–", "("}
CLOSE_DASH = {"—", "–", ")"}
CONNECTIVE_OPENERS = {
    "and", "but", "or", "nor", "yet", "so", "because", "which", "though",
    "although", "then", "except", "while", "since", "unless", "until", "not",
}


# ---------------------------------------------------------------------------
# Loading prose
# ---------------------------------------------------------------------------
def load_prose(path: Path) -> list[tuple[int, str]]:
    """Scene body as (source line number, text) — minus the H1, the italic
    metadata block before the first ---, and horizontal rules. Same slice of
    the file `echo_harvest.py` reads, so the two instruments agree on what
    counts as the chapter."""
    lines = path.read_text(encoding="utf-8").split("\n")
    out, seen_rule = [], False
    for n, ln in enumerate(lines, start=1):
        if ln.startswith("#"):
            continue
        if ln.strip() == "---":
            seen_rule = True
            continue
        if not seen_rule:
            continue
        if ln.strip():
            out.append((n, ln.strip()))
    if not out:  # no rule in the file: take everything but headings
        out = [
            (n, ln.strip())
            for n, ln in enumerate(lines, start=1)
            if ln.strip() and not ln.startswith("#") and ln.strip() != "---"
        ]
    return out


def clean(text: str) -> str:
    """Strip markdown emphasis without moving any character the parser needs."""
    text = re.sub(r"\*\*?", "", text)
    text = re.sub(r"_(?=\w)|(?<=\w)_", "", text)
    return text


# Abbreviations that end in a period without ending a sentence.
ABBREV = r"(?<!\bMr)(?<!\bMrs)(?<!\bMs)(?<!\bDr)(?<!\bSt)(?<!\bJr)(?<!\bSr)"
# Terminal punctuation, any closing quote/paren, then space, then something
# that can start a sentence.
SENT_SPLIT = re.compile(
    ABBREV + r'(?<=[.!?…])["”’\')\]]*\s+(?=["“\'(\[—–]?[A-Z0-9])'
)


def split_sentences(text: str) -> list[str]:
    """Split a paragraph into sentences on terminal punctuation.

    We do NOT use spaCy's sentence segmentation. en_core_web_sm's parser
    invents boundaries inside this book's comma-spliced run-ons — it cuts
    the-bench.md:365 ("She cried out and the cry was not a trained cry, the cry
    was a sound from her, and he heard it land and he heard himself want to
    hear it again, …") into three — which would deflate every per-sentence
    measure precisely on the sentences this instrument exists to find. The
    reader's sentence ends at the full stop, so ours does too.
    """
    return [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]


def resolve_scene(token: str) -> Path:
    p = Path(token)
    for cand in (p, REPO / p, SCENES / p, SCENES / f"{token}.md"):
        if cand.is_file():
            return cand.resolve()
    sys.exit(f"reading_effort: no such scene: {token}")


# ---------------------------------------------------------------------------
# Per-sentence measurement
# ---------------------------------------------------------------------------
@dataclass
class Sent:
    slug: str
    line: int
    text: str
    dialogue: bool
    words: int
    open_deps: int = 0
    depth: int = 0
    mdd: float = 0.0
    sv: int = 0
    predelay: int = 0
    suspend: int = 0
    suspend_at: str = ""
    effort: int = 0        # total dependency distance: this sentence's raw
                           # integration cost, which grows with length — the
                           # right unit for fatigue, where the per-sentence
                           # averages are not.
    breather: bool = False  # a short, shallow sentence: the reader's relief
    parse: str = ""
    strands: list[str] = field(default_factory=list)
    split: str = ""
    score: float = 0.0
    flags: list[str] = field(default_factory=list)
    fp: str = ""           # sentence fingerprint; see "Persistence" below


QUOTES = '"“”'


def is_dialogue(text: str) -> bool:
    """A sentence that is mostly spoken line rather than narration — measured
    as the share of its characters sitting inside quotation marks, so
    `"Facedown," he said. "Hands on the grips."` counts but a long narrative
    sentence containing a short quoted phrase does not. Kept out of the
    baseline so a dialogue-heavy chapter doesn't read as 'easier' than a
    narration-heavy one."""
    t = text.strip()
    if not t or t[0] not in QUOTES:
        return False
    inside, depth, total = 0, 0, 0
    for ch in t:
        if ch in QUOTES:
            depth ^= 1
            continue
        if ch.isspace():
            continue
        total += 1
        inside += depth
    return total > 0 and inside / total >= 0.6


def arc_spans(doc):
    """(words, word-position map, arcs) for one sentence.

    An arc is (first position, second position, dependent, head): the reader
    meets one end and carries the connection until the other arrives. Shared by
    `measure` and `explain` so the number in the report and the profile behind
    it can never disagree.
    """
    toks = [t for t in doc if not t.is_punct and not t.is_space]
    pos = {t.i: k for k, t in enumerate(toks)}
    arcs = []
    for t in toks:
        if t.head.i != t.i and t.head.i in pos:
            a, b = sorted((pos[t.i], pos[t.head.i]))
            if b - a >= 1:
                arcs.append((a, b, t, t.head))
    return toks, pos, arcs


def open_profile(n_words: int, arcs) -> list[int]:
    """Open-arc count after each word — the running working-memory load."""
    events = [0] * (n_words + 1)
    for a, b, _, _ in arcs:
        events[a] += 1
        events[b] -= 1
    prof, run = [], 0
    for k in range(n_words):
        run += events[k]
        prof.append(run)
    return prof


def measure(doc, slug: str, line: int) -> Sent:
    """Measure one sentence, parsed as its own Doc."""
    toks, pos, arcs = arc_spans(doc)
    text = doc.text.strip()
    s = Sent(slug=slug, line=line, text=text, dialogue=is_dialogue(text),
             words=len(toks))
    if len(toks) < 2:
        return s

    # --- peak open dependencies -------------------------------------------
    # Every arc is a thread the reader holds from the first of the pair until
    # the second arrives. The peak across the sentence is the working-memory
    # high-water mark. NOTE the raw count mixes cheap local arcs (det, amod,
    # resolved in a word or two) with expensive long-range ones; `mdd` and
    # `--explain` are what separate them.
    if arcs:
        s.open_deps = max(open_profile(len(toks), arcs))
        s.effort = sum(b - a for a, b, _, _ in arcs)
        s.mdd = round(s.effort / len(arcs), 2)

    # --- clause embedding depth -------------------------------------------
    for t in toks:
        d, cur, guard = 0, t, 0
        while cur.head.i != cur.i and guard < 200:
            if cur.dep_ in CLAUSAL or (cur.dep_ == "pcomp" and cur.pos_ == "VERB"):
                d += 1
            cur = cur.head
            guard += 1
        s.depth = max(s.depth, d)

    # --- subject-verb distance, main-verb delay ---------------------------
    for t in toks:
        if t.dep_ in ("nsubj", "nsubjpass") and t.head.i in pos:
            s.sv = max(s.sv, abs(pos[t.head.i] - pos[t.i]))
    # A sentence with no finite verb anywhere is a real fragment. Do NOT infer
    # this from the ROOT's part of speech: en_core_web_sm mis-roots very long
    # sentences (the 67-word one at the-bench.md:47 roots on an adverb), which
    # would report a perfectly finite sentence as verbless.
    finite = [t for t in toks if t.tag_ in FINITE_TAGS]
    root = next((t for t in doc if t.dep_ == "ROOT"), None)
    if root is not None and root.i in pos:
        s.predelay = pos[root.i]
        if root.pos_ not in ("VERB", "AUX") and finite:
            # parse didn't resolve: the structural numbers above are soft here
            s.parse = "uncertain"
    if not finite:
        s.split = "fragment"

    # --- suspension: an interruption the clause resumes after --------------
    # The author's device is the paired em dash. Cost is real only if the
    # sentence picks the original thread back up: material after the close
    # whose head sits before the open.
    marks = [t for t in doc if t.text in OPEN_DASH or t.text in CLOSE_DASH]
    for k in range(len(marks) - 1):
        a, b = marks[k], marks[k + 1]
        if a.text == "(" and b.text != ")":
            continue
        inner = [t for t in doc if a.i < t.i < b.i and not t.is_punct]
        after = [t for t in doc if t.i > b.i and not t.is_punct]
        if len(inner) < T_SUSPEND or len(after) < T_RESUME:
            continue
        resumes = any(t.head.i < a.i for t in after if t.head.i != t.i)
        if resumes and len(inner) > s.suspend:
            s.suspend = len(inner)
            nxt = " ".join(t.text for t in after[:6])
            s.suspend_at = f"resumes at “{nxt}…”"

    # --- stranded modifiers ------------------------------------------------
    # A modifier attached far back, with a whole other CLAUSE in between: the
    # reader has to skip that clause to reattach it. The worked case is
    #   "He brought his hands up the fronts of her thighs, and the pale skin
    #    went faintly gold where …, over the small rounded hip bones …"
    # where "over …" reaches back past an intervening coordinate clause.
    #
    # The intervening verb must head a clause at the same level or higher (a
    # sibling/coordinate/main clause) — NOT one nested inside the modifier's
    # own head phrase. Without that test this fires on every relative clause:
    # "He held her the way she'd placed him, in no more of a hurry…" is easy
    # prose, and "placed" sits harmlessly inside "the way …".
    for t in toks:
        if t.dep_ not in STRAND_DEPS:
            continue
        h = t.head
        if h.i >= t.i or t.i - h.i < T_STRAND:
            continue
        if len(list(t.subtree)) < T_STRAND_SPAN:
            continue  # a one- or two-word tail is cheap to reattach
        ancestors = {a.i for a in t.ancestors}
        h_ancestors = {a.i for a in h.ancestors} | {h.i}
        between = [
            v for v in doc
            if h.i < v.i < t.i
            and v.tag_ in FINITE_TAGS
            and v.dep_ not in ("aux", "auxpass")   # an auxiliary is not a clause
            and v.i not in ancestors
            and (v.dep_ == "ROOT" or v.head.i in h_ancestors)
        ]
        if between:
            s.strands.append(
                f"“{t.text} …” → “{h.text}” "
                f"({t.i - h.i} words back, past the clause at “{between[-1].text}”)"
            )

    # --- score -------------------------------------------------------------
    s.score = round(
        W_OPEN * max(0, s.open_deps - T_OPEN)
        + W_DEPTH * max(0, s.depth - T_DEPTH)
        + W_PREDELAY * max(0, s.predelay - T_PREDELAY)
        + W_SV * max(0, s.sv - T_SV)
        + W_SUSPEND * max(0, s.suspend - T_SUSPEND)
        + W_STRAND * len(s.strands),
        1,
    )
    # A short, shallow sentence — "She straddled him." — is where the reader
    # sets the load down. Dialogue counts: a spoken exchange is relief too.
    s.breather = (s.words <= T_BREATHER or s.dialogue) and s.open_deps <= 4

    if s.depth >= T_DEPTH:
        s.flags.append("chain")
    if s.suspend:
        s.flags.append("suspend")
    if s.strands:
        s.flags.append("strand")
    if s.open_deps >= T_OPEN or s.predelay >= T_PREDELAY:
        s.flags.append("load")
    return s


def hotspots(sents: list[Sent], window_words: int = WINDOW_WORDS) -> list[dict]:
    """Find the stretches where the load never lets up.

    Reading fatigue is cumulative, not per-sentence: one 60-word sentence
    between two short ones is rhythm, and this book uses that deliberately.
    What tires a reader is a run of consecutive heavy sentences with no
    breather — and in a long chapter there is more of it to survive.

    So we slide a fixed-width window (in WORDS, not sentences, so a passage of
    four long sentences is compared fairly against one of twelve short ones)
    and score each by effort per word — total dependency distance over the
    window, i.e. the mean integration cost the reader pays per word read.
    Dialogue and short beats are included, because they are exactly the relief
    that makes a passage survivable; a window with none scores high honestly.
    """
    if not sents:
        return []
    out: list[dict] = []
    n = len(sents)
    start = 0
    while start < n:
        words = effort = 0
        end = start
        while end < n and words < window_words:
            words += sents[end].words
            effort += sents[end].effort
            end += 1
        if words >= window_words * 0.6:
            span = sents[start:end]
            out.append({
                "start": start, "end": end,
                "line_from": span[0].line, "line_to": span[-1].line,
                "words": words,
                "per_word": round(effort / words, 2) if words else 0.0,
                "breathers": sum(1 for s in span if s.breather),
                "longest_dry_run": max_dry_run(span),
                "flags": [f for s in span for f in s.flags],
            })
        start += 1  # slide by one sentence; overlaps pruned at report time
    return out


def max_dry_run(span: list[Sent]) -> int:
    """Longest run of consecutive sentences with no breather in it."""
    best = run = 0
    for s in span:
        run = 0 if s.breather else run + 1
        best = max(best, run)
    return best


def prune_overlaps(spots: list[dict], keep: int) -> list[dict]:
    """Highest-scoring windows first, dropping any that overlap one already
    taken — so the report names distinct passages, not one peak N times."""
    chosen: list[dict] = []
    for sp in sorted(spots, key=lambda d: -d["per_word"]):
        if all(sp["end"] <= c["start"] or sp["start"] >= c["end"] for c in chosen):
            chosen.append(sp)
        if len(chosen) >= keep:
            break
    return sorted(chosen, key=lambda d: d["start"])


def mark_splits(sents: list[Sent]) -> None:
    """The cross-sentence half of the feedback: an idea carried into the next
    sentence when the two could have been one. Two shapes — a verbless
    fragment, and a sentence opening on a connective — each counted only when
    the sentence BEFORE it was long enough that the break looks like accretion
    rather than a deliberate short beat after a short beat."""
    for i, s in enumerate(sents):
        prev = sents[i - 1] if i else None
        if not prev or prev.words < T_LONG_PRIOR or s.dialogue or prev.dialogue:
            continue
        first = re.sub(r"^[^\w]+", "", s.text).split(" ")[0].lower().strip(",")
        if s.split == "fragment":
            # A SHORT verbless sentence is this book's registering-beat — "The
            # chest." / "Not lower — up." / "Then nothing." — deliberate voice,
            # not a split idea, so it is not flagged at all. A LONG one is an
            # idea that got detached from the sentence it belongs to and can
            # usually be rejoined.
            if s.words < T_FRAGMENT:
                s.split = ""
                continue
            s.split = f"{s.words}-word verbless sentence after a {prev.words}-word one"
            s.flags.append("split")
            s.score += 2.0
        elif first in CONNECTIVE_OPENERS:
            s.split = f"opens on “{first}” after a {prev.words}-word sentence"
            s.flags.append("split")
            s.score += 1.5


# ---------------------------------------------------------------------------
# Corpus pass + cache
# ---------------------------------------------------------------------------
def file_key(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()[:16]


def analyze(path: Path, nlp) -> list[Sent]:
    """Parse each sentence as its own doc, on OUR boundaries (see
    `split_sentences`), so the parser cannot redraw them."""
    slug = path.stem
    pairs: list[tuple[int, str]] = []
    for line, raw in load_prose(path):
        for sent_text in split_sentences(clean(raw)):
            pairs.append((line, sent_text))
    out = [
        measure(doc, slug, line)
        for (line, _), doc in zip(
            pairs, nlp.pipe([t for _, t in pairs], batch_size=200)
        )
    ]
    mark_splits(out)
    for s in out:
        # One ruling per sentence, not per structure: you revise the sentence,
        # which re-arms everything about it anyway.
        s.fp = fingerprint("effort", s.text)
    return out


# ---------------------------------------------------------------------------
# Persistence: a worklist you can pick up next session, and the rulings that
# keep settled findings settled.
#
# Fingerprints use the SAME scheme as the style linter's --ack allowlist
# (`na.py::_fingerprint`): sha256("<rule>\x00<sentence>")[:12], with the file
# path deliberately excluded so the decision rides with the prose and survives
# line shifts, reflow and renames — and RE-ARMS the moment the sentence's
# wording changes.
#
# That re-arming is why there is only one action, `--ack` (leave it standing),
# and no "done" state to maintain: if you revise a flagged sentence its
# fingerprint changes and the finding disappears on its own. The only thing
# worth recording is the decision NOT to change something, so that next
# session — or the next pass — doesn't re-litigate it.
# ---------------------------------------------------------------------------
def fingerprint(rule_id: str, sentence: str) -> str:
    return hashlib.sha256(
        f"{rule_id}\x00{sentence}".encode("utf-8")
    ).hexdigest()[:12]


def toml_str(v: str) -> str:
    v = (v.replace("\\", "\\\\").replace('"', '\\"')
          .replace("\n", "\\n").replace("\t", "\\t"))
    return f'"{v}"'


def load_rulings() -> dict[str, dict]:
    """fp -> entry. Missing file = nothing settled yet."""
    if not RULINGS.is_file():
        return {}
    try:
        import tomllib
        with RULINGS.open("rb") as fh:
            data = tomllib.load(fh)
    except Exception as exc:  # noqa: BLE001 - a malformed ruling file is the
        sys.exit(f"reading_effort: cannot read {RULINGS}: {exc}")
    return {e["fp"]: e for e in data.get("standing", []) if "fp" in e}


def save_ruling(fp: str, sents: list[Sent], note: str, slug: str) -> None:
    hit = next((s for s in sents if s.fp == fp), None)
    if hit is None:
        sys.exit(f"reading_effort: no finding [#{fp}] in {slug}")
    existing = load_rulings()
    if fp in existing:
        print(f"[#{fp}] already standing — {existing[fp].get('note', '')}")
        return
    AUDITS.mkdir(parents=True, exist_ok=True)
    header = ""
    if not RULINGS.is_file():
        header = (
            "# rulings.toml — reading-effort findings reviewed and LEFT STANDING.\n"
            "#\n"
            "# Each [[standing]] suppresses one finding by sentence fingerprint:\n"
            "# stable across line shifts and renames; editing the sentence\n"
            "# re-arms it. There is no 'fixed' state — a revised sentence\n"
            "# fingerprints differently and stops being flagged on its own.\n"
            "#\n"
            "# Written by `reading_effort.py <scene> --ack --fp <hash> "
            "--note '…'`.\n"
            "# Show suppressed findings again with --show-acked.\n"
        )
    with RULINGS.open("a", encoding="utf-8") as fh:
        fh.write(header)
        fh.write("\n[[standing]]\n")
        fh.write(f"fp    = {toml_str(fp)}\n")
        fh.write(f"file  = {toml_str(f'scenes/{slug}.md')}\n")
        fh.write(f"flags = {toml_str(','.join(hit.flags))}\n")
        fh.write(f"text  = {toml_str(hit.text)}\n")
        fh.write(f"note  = {toml_str(note)}\n")
    print(f"[#{fp}] left standing — recorded in {RULINGS.relative_to(REPO)}")


def drop_ruling(fp: str) -> None:
    """Reverse an --ack. Rewrites the file from the parsed entries rather than
    editing text, so the result is always well-formed TOML."""
    entries = load_rulings()
    if fp not in entries:
        sys.exit(f"reading_effort: [#{fp}] is not standing")
    del entries[fp]
    if not entries:
        RULINGS.unlink()
        print(f"[#{fp}] re-armed; no rulings left, removed "
              f"{RULINGS.relative_to(REPO)}")
        return
    body = [
        "# rulings.toml — reading-effort findings reviewed and LEFT STANDING.",
        "# Written by `reading_effort.py <scene> --ack --fp <hash> --note '…'`;",
        "# reverse with --unack --fp <hash>. Editing a sentence re-arms it.",
    ]
    for e in entries.values():
        body.append("\n[[standing]]")
        for k in ("fp", "file", "flags", "text", "note"):
            if k in e:
                body.append(f"{k:<5} = {toml_str(e[k])}")
    RULINGS.write_text("\n".join(body) + "\n", encoding="utf-8")
    print(f"[#{fp}] re-armed")


def write_worklist(target: list[Sent], slug: str, rulings: dict,
                   spots: list[dict], stats: list[str]) -> Path:
    """The durable artifact: one file per chapter, regenerated each run.

    Machine output — the author's decisions live in rulings.toml, NOT here,
    because this file is overwritten. Same split as
    `echo-inventory.md` (generated) vs `echo-rulings.md` (authored).
    """
    AUDITS.mkdir(parents=True, exist_ok=True)
    out = AUDITS / f"{slug}.md"
    nar = [s for s in target if not s.dialogue]
    open_f = [s for s in nar if s.flags and s.score > 0 and s.fp not in rulings]
    settled = [s for s in nar if s.flags and s.score > 0 and s.fp in rulings]
    open_f.sort(key=lambda s: -s.score)

    L = [f"# Reading effort — {slug}", ""]
    L.append(f"_Generated by `tools/reading_effort.py {slug} --save`. "
             f"Machine output: regenerate, don't hand-edit._")
    L.append(f"_Decisions go in `audits/reading-effort/rulings.toml` via "
             f"`--ack --fp <hash> --note \"why\"` — a revised sentence drops "
             f"off this list by itself._")
    L.append("")
    L.extend(stats)
    L.append("")
    L.append(f"## Worklist — {len(open_f)} open, {len(settled)} left standing")
    L.append("")
    for s in open_f:
        bits = [f"{s.words}w", f"open {s.open_deps}", f"depth {s.depth}",
                f"mdd {s.mdd}"]
        if s.predelay >= T_PREDELAY:
            bits.append(f"verb at word {s.predelay}")
        L.append(f"### `[#{s.fp}]` {slug}.md:{s.line} — score {s.score}")
        L.append("")
        L.append(f"`{' · '.join(bits)}` — {', '.join(s.flags)}")
        L.append("")
        body = re.sub(r"\s+", " ", s.text)
        L.append(f"> {body}")
        L.append("")
        if s.suspend:
            L.append(f"- **suspend**: {s.suspend} words held inside the "
                     f"interruption, {s.suspend_at}")
        for st in s.strands:
            L.append(f"- **strand**: {st}")
        if "split" in s.flags:
            L.append(f"- **split**: {s.split}")
        if "chain" in s.flags and s.depth >= T_DEPTH:
            L.append(f"- **chain**: idea passed down {s.depth} clause levels")
        if s.parse:
            L.append("- **note**: parser could not resolve the main verb; "
                     "structural numbers approximate")
        L.append(f"- inspect: `tools/reading_effort.py {slug} "
                 f"--explain {s.line}`")
        L.append("")
    if settled:
        L.append("## Left standing")
        L.append("")
        for s in settled:
            L.append(f"- `[#{s.fp}]` {slug}.md:{s.line} — "
                     f"{rulings[s.fp].get('note', '(no note)')}")
        L.append("")
    if spots:
        L.append("## Fatigue hotspots")
        L.append("")
        L.append("| effort/word | lines | words | breathers | longest dry run |")
        L.append("|---|---|---|---|---|")
        for sp in spots:
            L.append(f"| {sp['per_word']} | {sp['line_from']}–{sp['line_to']} "
                     f"| {sp['words']} | {sp['breathers']} "
                     f"| {sp['longest_dry_run']} |")
        L.append("")
    out.write_text("\n".join(L), encoding="utf-8")
    return out


def load_cache() -> dict:
    if CACHE.is_file():
        try:
            return json.loads(CACHE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache), encoding="utf-8")


def corpus_by_chapter(nlp, cache: dict,
                      exclude: Path | None = None) -> dict[str, list[Sent]]:
    out: dict[str, list[Sent]] = {}
    dirty = False
    for p in sorted(SCENES.glob("*.md")):
        if exclude and p.resolve() == exclude:
            continue
        key = f"{ALGO}:{p.name}:{file_key(p)}"
        if key in cache:
            rows = [Sent(**r) for r in cache[key]]
        else:
            print(f"  parsing {p.name}…", file=sys.stderr)
            rows = analyze(p, nlp)
            cache[key] = [asdict(r) for r in rows]
            dirty = True
        out[p.stem] = rows
    if dirty:
        save_cache(cache)
    return out


def pct(values: list[float], v: float) -> int:
    if not values:
        return 0
    return round(100 * sum(1 for x in values if x <= v) / len(values))


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    k = min(len(xs) - 1, int(q * (len(xs) - 1)))
    return xs[k]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
METRICS = [
    ("words/sentence", "words", "{:.1f}"),
    ("peak open deps", "open_deps", "{:.1f}"),
    ("clause depth", "depth", "{:.2f}"),
    ("mean dep distance", "mdd", "{:.2f}"),
    ("subject–verb gap", "sv", "{:.2f}"),
    ("words before main verb", "predelay", "{:.2f}"),
]


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


LOCAL_ARC = 5   # an arc this short resolves before the reader feels it


def explain(path: Path, nlp, line_no: int, min_words: int = 10) -> None:
    """Word-by-word open-dependency profile for the sentences on one line.

    The summary numbers say a sentence is heavy; this says WHERE and WHAT is
    being held, which is what decides whether it's worth touching. A peak of 8
    made of short det/amod arcs costs the reader nothing; a peak of 8 holding
    the main clause open across fifty words is the real thing.
    """
    blocks = [(n, raw) for n, raw in load_prose(path) if n == line_no]
    if not blocks:
        sys.exit(f"reading_effort: no prose on line {line_no} of {path.name}")
    for n, raw in blocks:
        for text in split_sentences(clean(raw)):
            doc = nlp(text)
            toks, _, arcs = arc_spans(doc)
            if len(toks) < min_words or not arcs:
                continue
            prof = open_profile(len(toks), arcs)
            peak = max(prof)
            peak_k = prof.index(peak)
            print(f"\n{path.name}:{n} — {len(toks)} words, peak open {peak}, "
                  f"mdd {sum(b - a for a, b, _, _ in arcs) / len(arcs):.2f}\n")
            for k, t in enumerate(toks):
                mark = "  <-- PEAK" if k == peak_k else ""
                print(f"  {t.text:<18}{prof[k]:>2} {'█' * prof[k]}{mark}")
            held = sorted((b - a, t, h, t.dep_)
                          for a, b, t, h in arcs if a <= peak_k < b)
            far = [x for x in held if x[0] > LOCAL_ARC]
            print(f"\n  held open at “{toks[peak_k].text}”: {len(held)} arcs, "
                  f"{len(far)} of them long-range (> {LOCAL_ARC} words)")
            for span, t, h, dep in sorted(held, reverse=True):
                tag = "  ← the cost" if span > LOCAL_ARC else ""
                print(f"    {t.text!r} → {h.text!r}  ({dep}, {span} words){tag}")
            print()


def path_label(sents: list[Sent]) -> str:
    return f"{sents[0].slug}.md" if sents else "?"


def report(target: list[Sent], base: dict[str, list[Sent]], slug: str, top: int,
           classes: set[str] | None, top_spots: int = 6,
           rulings: dict | None = None, show_acked: bool = False):
    rulings = rulings or {}
    nar = [s for s in target if not s.dialogue]
    # Chapter-level baseline: one number per chapter, so this chapter's
    # percentile answers "where does it sit among my other chapters" rather
    # than the far less useful "among all sentences ever written here".
    chapters = {k: [s for s in v if not s.dialogue] for k, v in base.items()}
    chapters = {k: v for k, v in chapters.items() if len(v) >= 20}
    bnar = [s for v in chapters.values() for s in v]
    print(f"\nREADING EFFORT — {slug}")
    print(f"  {len(nar)} narration sentences ({sum(s.words for s in nar)} words); "
          f"{len(target) - len(nar)} dialogue sentences excluded")
    print(f"  baseline: {len(chapters)} other chapters, "
          f"{len(bnar)} narration sentences\n")

    print(f"  {'(chapter means)':<24}{'this ch.':>10}{'corpus p50':>12}"
          f"{'p90':>8}{'pctile':>9}")
    for label, attr, fmt in METRICS:
        mine = mean([getattr(s, attr) for s in nar])
        per_chapter = [mean([getattr(s, attr) for s in v]) for v in chapters.values()]
        print(f"  {label:<24}{fmt.format(mine):>10}"
              f"{fmt.format(quantile(per_chapter, 0.5)):>12}"
              f"{fmt.format(quantile(per_chapter, 0.9)):>8}"
              f"{pct(per_chapter, mine):>8}%")

    # flag-class rates, chapter vs. corpus
    print()
    for cls, blurb in (
        ("chain", f"clause depth ≥ {T_DEPTH}"),
        ("suspend", f"resumed interruption ≥ {T_SUSPEND} words"),
        ("strand", f"modifier reattached ≥ {T_STRAND} words back"),
        ("load", f"peak open ≥ {T_OPEN} or main verb ≥ {T_PREDELAY} words in"),
        ("split", "idea continued into the next sentence"),
    ):
        mine = sum(1 for s in nar if cls in s.flags)
        rate = 100 * mine / len(nar) if nar else 0
        brate = 100 * sum(1 for s in bnar if cls in s.flags) / len(bnar) if bnar else 0
        arrow = "↑" if rate > brate * 1.15 else ("↓" if rate < brate * 0.85 else " ")
        print(f"  {cls:<9}{mine:>4} sentences  {rate:>5.1f}%   corpus {brate:>5.1f}% {arrow}"
              f"   ({blurb})")
    tw = sum(s.words for s in nar) or 1
    btw = sum(s.words for s in bnar) or 1
    print(f"\n  share of prose inside a flagged sentence: "
          f"{100 * sum(s.words for s in nar if s.flags) / tw:.1f}%"
          f"   (corpus {100 * sum(s.words for s in bnar if s.flags) / btw:.1f}%)")
    print(f"  longest 5% of sentences run "
          f"{quantile([float(s.words) for s in nar], 0.95):.0f}+ words"
          f"   (corpus {quantile([float(s.words) for s in bnar], 0.95):.0f}+)")

    # Compact form of the same figures, for the saved worklist header.
    stats = [
        "## Summary", "",
        f"- {len(nar)} narration sentences, "
        f"{sum(s.words for s in nar)} words",
        f"- prose inside a flagged sentence: "
        f"{100 * sum(s.words for s in nar if s.flags) / tw:.1f}% "
        f"(corpus {100 * sum(s.words for s in bnar if s.flags) / btw:.1f}%)",
    ] + [
        f"- {cls}: {sum(1 for s in nar if cls in s.flags)} sentences "
        f"({100 * sum(1 for s in nar if cls in s.flags) / len(nar):.1f}%, "
        f"corpus {100 * sum(1 for s in bnar if cls in s.flags) / len(bnar):.1f}%)"
        for cls in ("chain", "suspend", "strand", "load", "split")
    ]

    # --- fatigue profile ---------------------------------------------------
    # Every sentence, dialogue included: relief is part of the profile.
    spots = hotspots(target)
    pruned: list[dict] = []
    if spots:
        base_pw = [d["per_word"] for v in base.values() for d in hotspots(v)]
        mine_pw = [d["per_word"] for d in spots]
        dry = [max_dry_run(v) for v in base.values()]
        print(f"\n\nFATIGUE PROFILE — {sum(s.words for s in target)} words total, "
              f"{100 * sum(1 for s in target if s.breather) / len(target):.0f}% "
              f"of sentences are breathers "
              f"(corpus {100 * sum(1 for v in base.values() for s in v if s.breather) / sum(len(v) for v in base.values()):.0f}%)")
        print(f"  longest stretch anywhere with no breather: "
              f"{max_dry_run(target)} sentences "
              f"(corpus median {quantile([float(d) for d in dry], 0.5):.0f}, "
              f"worst {max(dry):.0f})")
        print(f"  windows of ~{WINDOW_WORDS} words, effort/word = mean integration "
              f"cost per word read:")
        print(f"    this chapter  median {quantile(mine_pw, 0.5):.2f}  "
              f"peak {max(mine_pw):.2f}")
        print(f"    all chapters  median {quantile(base_pw, 0.5):.2f}  "
              f"p90 {quantile(base_pw, 0.9):.2f}  "
              f"p99 {quantile(base_pw, 0.99):.2f}\n")
        pruned = prune_overlaps(spots, top_spots)
        for i, sp in enumerate(pruned, 1):
            cls = ", ".join(
                f"{c}×{sp['flags'].count(c)}"
                for c in ("suspend", "chain", "strand", "load")
                if sp["flags"].count(c)
            ) or "no single structure dominates"
            print(f"{i:>3}. effort/word {sp['per_word']:<6} "
                  f"{path_label(target)}:{sp['line_from']}–{sp['line_to']}   "
                  f"{sp['words']}w · {sp['breathers']} breathers · "
                  f"longest stretch without one: {sp['longest_dry_run']} sentences")
            print(f"     {cls}")
            heavy = sorted(target[sp["start"]:sp["end"]],
                           key=lambda s: -s.effort)[:2]
            for h in heavy:
                body = re.sub(r"\s+", " ", h.text)
                print(f"     · {h.words}w, open {h.open_deps}: "
                      f"{body[:150] + '…' if len(body) > 150 else body}")
            print()

    ranked = [s for s in nar if s.flags and s.score > 0]
    if classes:
        ranked = [s for s in ranked if classes & set(s.flags)]
    acked = [s for s in ranked if s.fp in rulings]
    if not show_acked:
        ranked = [s for s in ranked if s.fp not in rulings]
    ranked.sort(key=lambda s: -s.score)
    tail = (f"; {len(acked)} left standing (--show-acked)" if acked else "")
    print(f"\n\nHARDEST {min(top, len(ranked))} of {len(ranked)} flagged "
          f"— flags, not findings; the author rules on each{tail}\n")
    for i, s in enumerate(ranked[:top], 1):
        if s.fp in rulings:
            print(f"     (standing: {rulings[s.fp].get('note', '')})")
        bits = [f"open {s.open_deps}", f"depth {s.depth}", f"mdd {s.mdd}"]
        if s.predelay >= T_PREDELAY:
            bits.append(f"verb at word {s.predelay}")
        if s.sv >= T_SV:
            bits.append(f"subj–verb {s.sv}")
        print(f"{i:>3}. [{s.score:>5}] [#{s.fp}] {s.slug}.md:{s.line}   "
              f"{s.words}w · {' · '.join(bits)}")
        body = re.sub(r"\s+", " ", s.text)
        print(f"     {body if len(body) <= 300 else body[:297] + '…'}")
        if s.suspend:
            print(f"     → suspend: {s.suspend} words held inside the "
                  f"interruption, {s.suspend_at}")
        for st in s.strands:
            print(f"     → strand: {st}")
        if "split" in s.flags:
            print(f"     → split: {s.split}")
        if "chain" in s.flags and s.depth >= T_DEPTH:
            print(f"     → chain: idea passed down {s.depth} clause levels")
        if s.parse:
            print("     → note: the parser could not resolve this sentence's "
                  "main verb; its structural numbers are approximate "
                  "(itself a mild signal)")
        print()
    return stats, pruned


def corpus_report(nlp, cache: dict, top: int) -> None:
    rows = []
    for p in sorted(SCENES.glob("*.md")):
        key = f"{ALGO}:{p.name}:{file_key(p)}"
        if key not in cache:
            print(f"  parsing {p.name}…", file=sys.stderr)
            cache[key] = [asdict(r) for r in analyze(p, nlp)]
        sents = [Sent(**r) for r in cache[key]]
        nar = [s for s in sents if not s.dialogue]
        if len(nar) < 20:
            continue
        total_w = sum(s.words for s in nar) or 1
        rows.append((
            p.stem, len(nar),
            mean([s.words for s in nar]),
            quantile([float(s.words) for s in nar], 0.95),
            mean([s.open_deps for s in nar]),
            100 * sum(1 for s in nar if s.flags) / len(nar),
            100 * sum(s.words for s in nar if s.flags) / total_w,
        ))
    save_cache(cache)
    rows.sort(key=lambda r: -r[6])
    print("\nREADING EFFORT — all chapters, ranked by share of prose inside "
          "flagged sentences\n")
    print("  (%words is the load a reader actually carries: one 60-word flagged\n"
          "   sentence weighs more than one clean 8-word one, which a per-sentence\n"
          "   rate hides in a chapter that alternates short beats with long ones.)\n")
    print(f"  {'chapter':<28}{'sents':>7}{'words/s':>9}{'p95 len':>9}"
          f"{'open':>7}{'%sents':>9}{'%words':>9}")
    for slug, n, w, p95, o, fs, fw in rows[:top]:
        print(f"  {slug:<28}{n:>7}{w:>9.1f}{p95:>9.0f}{o:>7.2f}"
              f"{fs:>8.1f}%{fw:>8.1f}%")
    print()


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Measure reading effort; flag split ideas. Flags, never fixes.")
    ap.add_argument("scene", nargs="?", help="scene slug or path")
    ap.add_argument("--corpus", action="store_true",
                    help="rank every chapter instead of detailing one")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--spots", type=int, default=6,
                    help="fatigue hotspots to report")
    ap.add_argument("--explain", type=int, metavar="LINE",
                    help="open-dependency profile for the sentences on LINE")
    ap.add_argument("--save", action="store_true",
                    help="write the worklist to audits/reading-effort/<slug>.md")
    ap.add_argument("--ack", action="store_true",
                    help="record a finding as reviewed and LEFT STANDING "
                         "(needs --fp; --note strongly advised)")
    ap.add_argument("--fp", metavar="HASH", help="finding fingerprint")
    ap.add_argument("--note", default="", help="why it stands")
    ap.add_argument("--unack", action="store_true",
                    help="reverse an --ack (needs --fp)")
    ap.add_argument("--show-acked", action="store_true",
                    help="include findings already left standing")
    ap.add_argument("--class", dest="classes", default="",
                    help="comma-separated: chain,suspend,strand,load,split")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    import spacy
    nlp = spacy.load("en_core_web_sm", exclude=["ner", "lemmatizer"])
    cache = {} if args.no_cache else load_cache()

    if args.corpus or not args.scene:
        corpus_report(nlp, cache, args.top or 100)
        return

    path = resolve_scene(args.scene)
    if args.explain:
        explain(path, nlp, args.explain)
        return
    target = analyze(path, nlp)
    if args.json:
        print(json.dumps([asdict(s) for s in target], indent=2))
        return

    if args.unack:
        if not args.fp:
            sys.exit("reading_effort: --unack needs --fp <hash>")
        drop_ruling(args.fp)
        return

    if args.ack:
        if not args.fp:
            sys.exit("reading_effort: --ack needs --fp <hash> "
                     "(the [#…] tag on the finding)")
        if not args.note:
            print("warning: recording a standing ruling with no --note; "
                  "next session won't know why", file=sys.stderr)
        save_ruling(args.fp, target, args.note, path.stem)
        return

    rulings = load_rulings()
    base = corpus_by_chapter(nlp, cache, exclude=path)
    classes = {c.strip() for c in args.classes.split(",") if c.strip()} or None
    stats, spots = report(target, base, path.stem, args.top, classes,
                          args.spots, rulings, args.show_acked)
    if args.save:
        out = write_worklist(target, path.stem, rulings, spots, stats)
        print(f"\nworklist → {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
