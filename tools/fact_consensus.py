#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Consensus fact memory: three slot extractors, 2-of-3 agreement (author ruling 2026-11-01).

Why not the `core` ensemble: it pins exact model ids in its manifests, and each source's
later-volume checkpoints are seeded from that same model's earlier ones, so replacing a
model means minting its whole history first (core has waited on a rebuild since
2026-10-11). Here:

- SLOTS, not models. `[facts.slots]` maps anthropic/openai/google to whichever model fills
  the slot now. Each artifact records who filled each slot when it was minted, and is
  judged current only by the prose hash — never against today's config — so swapping
  opus for sonnet changes the next mint and invalidates nothing.
- NO LINEAGE. Every slot extracts from raw prose ch1..B, every time (all three families
  have 1M windows), so a newly swapped model needs no history.
- FACTS AS CLAIMS. Each slot writes `SECTION | ch<n> | fact | "quote"`; code verifies every
  quote against the prose and discards claims whose quote is not on the page.
- AGREEMENT. A matcher groups same-fact claims across slots (it only groups; it never
  writes). Code admits a group only with members from >= quorum distinct slots, and the
  admitted text is one member's own words (the shortest: least added). A failed slot
  degrades the build (quorum among the rest), it does not fail it.
- AUDIT. Two models can share a reading; the evidence audit (checkpoint_audit.py) runs as
  a last pass, and consumers read its fact-only projection.

Output: reviews/cold-read/fact-consensus/ck-ch<B>.md (+ .json provenance, slots/ raw).

Usage:
  tools/fact_consensus.py --to 10             # build ck-ch010 (google slot is PAID)
  tools/fact_consensus.py --to 10 --force     # rebuild, reusing cached slot extractions
  tools/fact_consensus.py --to 10 --reextract # rebuild, calling every slot again
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_audit  # noqa: E402
import checkpoint_bundle  # noqa: E402
import cold_read_config  # noqa: E402

ROOT = REPO / "reviews" / "cold-read" / "fact-consensus"
EXTRACT_PROMPT = REPO / "reviews" / "cold-read" / "fact-extract-prompt.md"
MATCH_PROMPT = REPO / "reviews" / "cold-read" / "fact-match-prompt.md"
SECTIONS = {"WHO": "Who's who", "REL": "Relationships",
            "KNOW": "What I know that they don't", "MOTIF": "Motifs & images",
            "STORY": "Story so far"}
CLAIM_RE = re.compile(r"^\W*(POV|WHO|REL|KNOW|MOTIF|STORY)\s*\|\s*ch\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+)$",
                      re.I)
GROUP_TOKEN = re.compile(r"\b([A-D])(\d+)\b")
OR_MAX_OUTPUT = 80000
# Sections whose facts carry the page's own words beneath them (gestures, objects, people,
# relationships: where the specifics carry the meaning). STORY stays bare; it is the bulk.
QUOTED_SECTIONS = {"MOTIF", "WHO", "REL"}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def settings() -> dict:
    return dict(cold_read_config.load_config()["facts"])


def call(model: str, system: str, prompt: str, label: str) -> str:
    """One model call on the model's own lane (subscription, codex, or paid OpenRouter)."""
    import authorship_audit
    if model.startswith(authorship_audit.CLAUDE_PREFIX):
        return authorship_audit.run_claude(model, system, prompt, label)
    import cold_read
    routes = cold_read_config.openrouter_models()
    if model in routes:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY not set")
        fn = cold_read.make_openrouter_agent_fn(
            system_prompt=system, api_key=key, policy="capture", effort="medium",
            timeout=3600, max_output_tokens=OR_MAX_OUTPUT)
        # A cut-off response is a failure, not a thin slot: argon at ch70 returned 146
        # lines ending mid-sentence with in=0 out=0 billed. Retry once, then fail the slot.
        why = ""
        for _attempt in range(2):
            r = fn(prompt=prompt, model=routes[model], label=label) or {}
            u = r.get("usage") or {}
            if u.get("output") and u.get("finishReason") in ("stop", "end_turn", None):
                return r.get("output") or ""
            why = f"finish={u.get('finishReason')} out={u.get('output')}"
            print(f"  {label}: incomplete response ({why}); retrying", flush=True)
        raise RuntimeError(f"incomplete response twice ({why})")
    f, close = cold_read.make_codex_agent_fn(system_prompt=system, effort="medium")
    try:
        return (f(prompt=prompt, model=model, label=label) or {}).get("output") or ""
    finally:
        close()


def parse_claims(text: str, page_norm: str) -> tuple[list[dict], int]:
    """(claims whose quote is on the page, total parsed)."""
    out, total = [], 0
    for line in text.splitlines():
        m = CLAIM_RE.match(line.strip())
        if not m:
            continue
        total += 1
        sec, ch, fact, quote = m.groups()
        if checkpoint_audit.verify(quote, page_norm):
            out.append({"section": sec.upper(), "ch": int(ch), "text": fact.strip(),
                        "quote": quote.strip().strip('"“”')})
    return out, total


def slot_raw_path(b: int, slot: str, model: str, kind: str = "facts") -> Path:
    """One cache file per slot AND model: a fallback must not overwrite the first
    model's output (it did at ch20, and the rebuild re-paid glm)."""
    mid = "" if kind == "facts" else f"{kind}."
    return ROOT / "slots" / f"ck-ch{b:03d}.{mid}{slot}.{model}.txt"


def extract(slot: str, model: str, b: int, page: str, page_sha: str, force: bool,
            kind: str = "facts") -> str:
    """The slot's raw claim list, reused if already minted from this exact prose by this model."""
    if kind == "readings":
        return extract_readings(slot, model, b, page, page_sha, force)
    p = slot_raw_path(b, slot, model)
    legacy = ROOT / "slots" / f"ck-ch{b:03d}.{slot}.txt"   # pre-2026-11-01 name
    if not p.exists() and legacy.exists() and f"model {model} " in legacy.read_text(
            encoding="utf-8").split("\n", 1)[0]:
        legacy.rename(p)
    head = f"# slot {slot} · model {model} · bundle-sha256 {page_sha} · prompt-sha256 " \
           f"{sha(EXTRACT_PROMPT.read_text(encoding='utf-8'))}"
    if p.exists() and not force and p.read_text(encoding="utf-8").startswith(head):
        return p.read_text(encoding="utf-8")
    system = EXTRACT_PROMPT.read_text(encoding="utf-8")
    prompt = (f"===== THE NOVEL, CHAPTERS 1–{b} =====\n\n{page}\n\n"
              f"Write the facts of chapters 1–{b} now, one per line.")
    try:
        raw = call(model, system, prompt, f"facts·{slot}·{model}·ch{b:03d}")
        ranges = f"1-{b}"
    except Exception as e:  # noqa: BLE001
        if "maximum length" not in str(e):
            raise
        # The codex lane caps a message at 1,048,576 characters (~262k tokens), well under
        # the model's window; sol hit it at ch60. Every claim names its chapter, so the book
        # can be read in chapter ranges and the claims joined: still raw prose, no lineage.
        raw, spans = [], []
        for lo, hi in chunk_ranges(b):
            part = checkpoint_bundle.build_reader_bundle(hi, start=lo)
            ask = (f"===== THE NOVEL, CHAPTERS {lo}–{hi} =====\n\n{part}\n\n"
                   f"Write the facts of chapters {lo}–{hi} now, one per line.")
            raw.append(call(model, system, ask, f"facts·{slot}·{model}·ch{b:03d}·{lo}-{hi}"))
            spans.append(f"{lo}-{hi}")
        raw, ranges = "\n".join(raw), ",".join(spans)
        print(f"  slot {slot} ({model}): read in chapter ranges {ranges}", flush=True)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"{head} · ranges {ranges} · {date.today().isoformat()}\n\n{raw.strip()}\n",
                 encoding="utf-8")
    print(f"  slot {slot} ({model}): {len(raw.splitlines())} lines", flush=True)
    return p.read_text(encoding="utf-8")


def pov_consensus(lists: dict[str, list[dict]], quorum: int) -> dict[int, list[str]]:
    """Deterministic: chapter -> the point-of-view name(s) >= quorum slots agree on.
    POV is too load-bearing to leave to fuzzy matching (a POV folded into a compound
    claim was lost at ch8-10 in the first test)."""
    votes: dict[int, Counter] = {}
    for claims in lists.values():
        seen = set()
        for c in claims:
            if c["section"] != "POV":
                continue
            name = re.sub(r"[^\w ]", "", c["text"]).split()
            if not name:
                continue
            key = (c["ch"], name[0].capitalize())
            if key not in seen:
                seen.add(key)
                votes.setdefault(c["ch"], Counter())[key[1]] += 1
    return {ch: [n for n, k in v.most_common() if k >= quorum] for ch, v in votes.items()}


CHUNK_CHARS = 900_000


def chunk_ranges(b: int) -> list[tuple[int, int]]:
    """Consecutive chapter ranges covering 1..b, each bundle under CHUNK_CHARS."""
    out, lo = [], 1
    while lo <= b:
        hi = lo
        while hi < b and len(checkpoint_bundle.build_reader_bundle(hi + 1, start=lo)) < CHUNK_CHARS:
            hi += 1
        out.append((lo, hi))
        lo = hi + 1
    return out


def match(lists: dict[str, list[dict]], matcher: str, b: int) -> str:
    """Group same-fact claims chapter by chapter (one call over ~1,500 claims under-grouped:
    sol's "Vee trades her panties for Pace's shirt" was left alone at ch22). Ids stay
    global, so `admit` is unchanged. Calls run in parallel."""
    system = MATCH_PROMPT.read_text(encoding="utf-8")

    def one(ch):
        blocks = []
        for letter, claims in lists.items():
            rows = [f"{letter}{i + 1} [{c['section']}] {c['text']}"
                    for i, c in enumerate(claims) if c["section"] != "POV" and c["ch"] == ch]
            if rows:
                blocks.append(f"===== EXTRACTOR {letter} =====\n" + "\n".join(rows))
        if sum(1 for x in blocks) < 2:
            return ""
        prompt = (f"These claims are all about chapter {ch}.\n\n" + "\n\n".join(blocks)
                  + "\n\nGroup them now, one group per line.")
        return call(matcher, system, prompt, f"facts·match·{matcher}·ck{b:03d}·ch{ch:03d}")

    chapters = sorted({c["ch"] for cl in lists.values() for c in cl})
    with ThreadPoolExecutor(max_workers=6) as pool:
        outs = list(pool.map(one, chapters))
    return "\n".join(o.strip() for o in outs if o.strip())


def admit(lists: dict[str, list[dict]], groups_raw: str, quorum: int) -> list[dict]:
    """Deterministic: a group needs members from >= quorum distinct slots; the admitted
    text is the shortest member's own (each admitted text once)."""
    # A claim may back more than one group: a compound claim states several facts
    # (argon's "first sex… and she trades him her panties" was spent on the first one).
    seen_texts, admitted = set(), []
    for line in groups_raw.splitlines():
        ids = [(l, int(n)) for l, n in GROUP_TOKEN.findall(line)]
        members, letters = [], set()
        for letter, n in ids:
            if letter in lists and 1 <= n <= len(lists[letter]) and letter not in letters:
                members.append((letter, n))
                letters.add(letter)
        if len(letters) < quorum:
            continue
        cs = [lists[l][n - 1] for l, n in members]
        best = min(cs, key=lambda c: len(c["text"]))
        if best["text"] in seen_texts:
            continue
        seen_texts.add(best["text"])
        sec = Counter(c["section"] for c in cs).most_common(1)[0][0]
        # The page's own words carry the detail the shortest wording drops (author ruling
        # 2026-11-01: "a sharp edge under her thumbnail" lost argon's "water bottle cap…
        # into the nail bed"). The longest verified member quote is the book, not a reading.
        detail = max(cs, key=lambda c: len(c["quote"]))["quote"]
        admitted.append({"section": sec, "ch": min(c["ch"] for c in cs), "text": best["text"],
                         "quote": best["quote"], "detail_quote": detail,
                         "support": [f"{l}{n}" for l, n in members]})
    return admitted


def render(admitted: list[dict], b: int, povs: dict[int, list[str]]) -> str:
    out = []
    titles = {i + 1: checkpoint_bundle.display_title(s)
              for i, s in enumerate(checkpoint_bundle.reader_slugs()[:b])}
    for code, name in SECTIONS.items():
        rows = sorted((c for c in admitted if c["section"] == code), key=lambda c: c["ch"])
        if not rows:
            continue
        out.append(f"### {name}\n")
        if code == "STORY":
            for ch in sorted({c["ch"] for c in rows} | set(povs)):
                pov = povs.get(ch)
                lead = f"({' then '.join(pov)} POV.) " if pov else ""
                text = " ".join(c["text"].rstrip(".") + "." for c in rows if c["ch"] == ch)
                out.append(f"**Ch{ch} {titles.get(ch, '')}.** {lead}{text}\n")
        else:
            for c in rows:
                out.append(f"- {c['text'].rstrip('.')}. (ch{c['ch']})")
                if code in QUOTED_SECTIONS and c.get("detail_quote"):
                    out.append(f'  > "{c["detail_quote"].strip(chr(34))}"')
            out.append("")
    return "\n".join(out).strip() + "\n"


def build(b: int, force: bool = False, reextract: bool = False) -> Path:
    cfg = settings()
    slots: dict[str, str] = dict(cfg["slots"])
    quorum = int(cfg.get("quorum", 2))
    matcher = str(cfg.get("matcher", "claude-opus-5-5"))
    page = checkpoint_bundle.build_reader_bundle(b, start=1)
    page_sha, page_norm = sha(page), checkpoint_audit.words(page)
    out_md = ROOT / f"ck-ch{b:03d}.md"
    if out_md.exists() and not force and f"bundle-sha256: {page_sha}" in out_md.read_text():
        print(f"  {out_md.relative_to(REPO)} is current", flush=True)
        return out_md

    def one(item):
        """A slot is a model or an ordered fallback chain; first success wins."""
        slot, chain = item
        chain = [chain] if isinstance(chain, str) else list(chain)
        errors = []
        for model in chain:
            try:
                raw = extract(slot, model, b, page, page_sha, reextract)
                # A slot that ignores the format fails, so the chain falls back: glm at
                # ch20 wrote 239 lines with no quotes, and 2 survived verification.
                body = [l for l in raw.splitlines()[1:] if l.strip()]
                good, _ = parse_claims(raw, page_norm)
                if len(good) < max(20, len(body) // 2):
                    raise RuntimeError(f"only {len(good)} of {len(body)} lines are "
                                       "quote-verified claims")
                return slot, model, raw, "; ".join(errors) or None
            except Exception as e:  # noqa: BLE001
                errors.append(f"{model}: {e}")
                print(f"  slot {slot}: {model} failed ({e}); trying next", flush=True)
        return slot, chain[-1], None, "; ".join(errors)

    with ThreadPoolExecutor(max_workers=len(slots)) as pool:
        got = list(pool.map(one, slots.items()))
    lists, prov, failed = {}, {}, []
    for letter, (slot, model, raw, err) in zip("ABCD", got):
        if raw is None:
            failed.append(f"{slot} ({model}): {err}")
            prov[slot] = {"model": model, "failed": err}
            print(f"  slot {slot} FAILED: {err}", flush=True)
            continue
        claims, total = parse_claims(raw, page_norm)
        lists[letter] = claims
        prov[slot] = {"model": model, "letter": letter, "parsed": total,
                      "verified": len(claims)}
        if err:
            prov[slot]["fell_back_from"] = err
        print(f"  slot {slot} ({model}): {len(claims)}/{total} claims verified", flush=True)
    if len(lists) < 2:
        raise SystemExit(f"fewer than two slots succeeded: {failed}")
    q = min(quorum, len(lists))
    groups_raw = match(lists, matcher, b)
    admitted = admit(lists, groups_raw, q)
    povs = pov_consensus(lists, q)
    by_letters = Counter(len(c["support"]) for c in admitted)
    degraded = " · DEGRADED (" + "; ".join(failed) + ")" if failed else ""
    slots_line = ", ".join(f"{s}={p['model']}" + (" (failed)" if "failed" in p else "")
                           for s, p in prov.items())
    header = (f"# Fact consensus — through Chapter {b}\n\n"
              f"*slots: {slots_line} · quorum {q} of {len(lists)} · matcher: {matcher} · "
              f"bundle-sha256: {page_sha} · {len(admitted)} facts admitted · "
              f"{date.today().isoformat()}{degraded}*\n\n---\n\n")
    out_md.write_text(header + render(admitted, b, povs), encoding="utf-8")
    out_md.with_suffix(".json").write_text(json.dumps({
        "boundary": b, "bundle_sha256": page_sha, "slots": prov, "quorum": q,
        "matcher": matcher, "extract_prompt_sha256": sha(EXTRACT_PROMPT.read_text()),
        "match_prompt_sha256": sha(MATCH_PROMPT.read_text()), "date": date.today().isoformat(),
        "support_sizes": dict(by_letters), "admitted": admitted, "pov": povs, "groups_raw": groups_raw,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    missing_pov = [ch for ch in range(1, b + 1) if not povs.get(ch)]
    if missing_pov:
        print(f"  WARNING: no POV consensus for ch{missing_pov}", flush=True)
    print(f"  admitted {len(admitted)} facts (support sizes {dict(by_letters)}) → "
          f"{out_md.relative_to(REPO)}", flush=True)
    checkpoint_audit.run_audit(out_md)
    return out_md



# ---------------------------------------------------------------------------
# Readings (author ruling 2026-11-02): Impression, Symbolism, Open questions, for the
# cold readers. Same slots, same no-lineage read of ch1..B, same quote verification and
# >= 2-slot agreement; opposed readings that each clear the bar are kept as COMPETING
# readings. Written to a separate ck-ch<B>.readings.md so the fact artifact (and its
# audit) never change, and capture readers never load it: their feelings are their own.
READINGS_PROMPT = ROOT.parent / "fact-readings-prompt.md"
READINGS_MATCH_PROMPT = ROOT.parent / "fact-readings-match-prompt.md"
READING_RE = re.compile(r"^\W*(IMPRESSION|SYMBOL|QUESTION)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*(.+)$",
                        re.I)


def extract_readings(slot: str, model: str, b: int, page: str, page_sha: str, force: bool) -> str:
    p = slot_raw_path(b, slot, model, "readings")
    head = (f"# readings · slot {slot} · model {model} · bundle-sha256 {page_sha} · "
            f"prompt-sha256 {sha(READINGS_PROMPT.read_text(encoding='utf-8'))}")
    if p.exists() and not force and p.read_text(encoding="utf-8").startswith(head):
        return p.read_text(encoding="utf-8")
    prompt = (f"===== THE NOVEL, CHAPTERS 1–{b} =====\n\n{page}\n\n"
              f"Write your readings as of the end of chapter {b} now, one per line.")
    # Readings need the whole book in view; a slot that cannot take it in one piece
    # fails (and the build degrades) rather than reading the book in halves.
    raw = call(model, READINGS_PROMPT.read_text(encoding="utf-8"), prompt,
               f"readings·{slot}·{model}·ch{b:03d}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"{head} · {date.today().isoformat()}\n\n{raw.strip()}\n", encoding="utf-8")
    print(f"  readings {slot} ({model}): {len(raw.splitlines())} lines", flush=True)
    return p.read_text(encoding="utf-8")


def parse_readings(text: str, page_words: str) -> tuple[list[dict], int]:
    out, total = [], 0
    for line in text.splitlines():
        m = READING_RE.match(line.strip())
        if not m:
            continue
        total += 1
        kind, key, reading, quote = m.groups()
        if not checkpoint_audit.verify(quote, page_words):
            continue
        key = key.strip()
        ch = int(re.sub(r"\D", "", key) or 0) if kind.upper() != "IMPRESSION" else 0
        out.append({"section": kind.upper(), "key": key if kind.upper() == "IMPRESSION"
                    else f"ch{ch}", "ch": ch, "text": reading.strip(),
                    "quote": quote.strip().strip('"“”')})
    return out, total


def match_readings(lists: dict[str, list[dict]], matcher: str, b: int) -> str:
    """One call per section; Impression lines carry their character so the matcher keeps
    people apart, and the prompt keeps opposed readings apart."""
    system = READINGS_MATCH_PROMPT.read_text(encoding="utf-8")

    def one(section):
        blocks = []
        for letter, rows in lists.items():
            got = [f"{letter}{i + 1} [{r['key']}] {r['text']}"
                   for i, r in enumerate(rows) if r["section"] == section]
            if got:
                blocks.append(f"===== READER {letter} =====\n" + "\n".join(got))
        if len(blocks) < 2:
            return ""
        return call(matcher, system, f"These are all {section} readings.\n\n"
                    + "\n\n".join(blocks) + "\n\nGroup them now, one group per line.",
                    f"readings·match·{matcher}·ck{b:03d}·{section.lower()}")

    with ThreadPoolExecutor(max_workers=3) as pool:
        outs = list(pool.map(one, ["IMPRESSION", "SYMBOL", "QUESTION"]))
    return "\n".join(o.strip() for o in outs if o.strip())


def render_readings(admitted: list[dict]) -> str:
    admitted_all = admitted
    out = []
    imp = [r for r in admitted if r["section"] == "IMPRESSION"]
    if imp:
        out.append("### Impression\n")
        by: dict[str, list[dict]] = {}
        for r in imp:
            by.setdefault(r["key"].split()[0].capitalize(), []).append(r)
        for who, rows in sorted(by.items(), key=lambda kv: -len(kv[1])):
            rows.sort(key=lambda r: -len(r["support"]))
            out.append(f"**{who}.**")
            for r in rows:
                out.append(f"- Read as: {r['text'].rstrip('.')}. ({len(r['support'])} readers)")
                for j in r["opposes"]:
                    out.append(f"  ⟷ competes with: {admitted_all[j]['text'].rstrip('.')}")
                out.append(f'  > "{r["detail_quote"].strip(chr(34))}"')
            out.append("")
    for code, name, lead in (("SYMBOL", "Symbolism", "Read as"), ("QUESTION", "Open questions", "Open")):
        rows = sorted((r for r in admitted if r["section"] == code), key=lambda r: r["ch"])
        if rows:
            out.append(f"### {name}\n")
            for r in rows:
                out.append(f"- {lead} (ch{r['ch']}): {r['text'].rstrip('.')}"
                           + ("" if r["text"].rstrip().endswith("?") else ".")
                           + f" ({len(r['support'])} readers)")
                out.append(f'  > "{r["detail_quote"].strip(chr(34))}"')
            out.append("")
    return "\n".join(out).strip() + "\n"


def build_readings(b: int, reextract: bool = False) -> Path:
    cfg = settings()
    slots: dict = dict(cfg["slots"])
    quorum = int(cfg.get("quorum", 2))
    matcher = str(cfg.get("matcher", "claude-opus-5-5"))
    page = checkpoint_bundle.build_reader_bundle(b, start=1)
    page_sha, page_words = sha(page), checkpoint_audit.words(page)

    def one(item):
        slot, chain = item
        chain = [chain] if isinstance(chain, str) else list(chain)
        errors = []
        for model in chain:
            try:
                raw = extract_readings(slot, model, b, page, page_sha, reextract)
                good, total = parse_readings(raw, page_words)
                body = [l for l in raw.splitlines()[1:] if l.strip()]
                if len(good) < max(10, len(body) // 2):
                    raise RuntimeError(f"only {len(good)} of {len(body)} lines are "
                                       "quote-verified readings")
                return slot, model, good, total, "; ".join(errors) or None
            except Exception as e:  # noqa: BLE001
                errors.append(f"{model}: {e}")
                print(f"  readings {slot}: {model} failed ({e}); trying next", flush=True)
        return slot, chain[-1], None, 0, "; ".join(errors)

    with ThreadPoolExecutor(max_workers=len(slots)) as pool:
        got = list(pool.map(one, slots.items()))
    lists, prov = {}, {}
    for letter, (slot, model, good, total, err) in zip("ABCD", got):
        prov[slot] = {"model": model, "letter": letter, "parsed": total,
                      "verified": len(good) if good else 0}
        if err:
            prov[slot]["errors"] = err
        if good:
            lists[letter] = good
            print(f"  readings {slot} ({model}): {len(good)}/{total} verified", flush=True)
    if len(lists) < 2:
        raise SystemExit("fewer than two slots produced readings")
    q = min(quorum, len(lists))
    groups_raw = match_readings(lists, matcher, b)
    admitted, seen = [], set()
    opposed_lines = [l for l in groups_raw.splitlines() if l.strip().upper().startswith("OPPOSED")]
    member_of: dict[str, int] = {}      # id -> index in `admitted`
    for line in groups_raw.splitlines():
        if line.strip().upper().startswith("OPPOSED"):
            continue
        members, letters = [], set()
        for letter, n in GROUP_TOKEN.findall(line):
            n = int(n)
            if letter in lists and 1 <= n <= len(lists[letter]) and letter not in letters:
                members.append((letter, n))
                letters.add(letter)
        if len(letters) < q:
            continue
        cs = [lists[l][n - 1] for l, n in members]
        if len({c["section"] for c in cs}) > 1:
            continue
        best = min(cs, key=lambda c: len(c["text"]))
        if best["text"] in seen:
            continue
        seen.add(best["text"])
        admitted.append({"section": cs[0]["section"], "key": best["key"],
                         "ch": min(c["ch"] for c in cs), "text": best["text"],
                         "detail_quote": max(cs, key=lambda c: len(c["quote"]))["quote"],
                         "support": [f"{l}{n}" for l, n in members], "opposes": []})
        for l, n in members:
            member_of[f"{l}{n}"] = len(admitted) - 1
    # Opposition is a LABEL, never a filter: every admitted reading stays, complementary or
    # not; a pair is marked only when both sides were admitted and they are about the same
    # person or thing.
    for line in opposed_lines:
        ids = [f"{l}{n}" for l, n in GROUP_TOKEN.findall(line)]
        idx = sorted({member_of[i] for i in ids if i in member_of})
        if len(idx) == 2:
            a, b2 = admitted[idx[0]], admitted[idx[1]]
            if a["section"] == b2["section"] and a["key"].split()[0].lower() == b2["key"].split()[0].lower():
                a["opposes"].append(idx[1]); b2["opposes"].append(idx[0])
    out_md = ROOT / f"ck-ch{b:03d}.readings.md"
    slots_line = ", ".join(f"{s}={p['model']}" for s, p in prov.items())
    header = (f"# Readings — through Chapter {b}\n\n*readings only, for cold readers; never "
              f"given to capture readers · slots: {slots_line} · quorum {q} of {len(lists)} · "
              f"matcher: {matcher} · bundle-sha256: {page_sha} · {len(admitted)} readings "
              f"admitted · {date.today().isoformat()}*\n\n---\n\n")
    out_md.write_text(header + render_readings(admitted), encoding="utf-8")
    out_md.with_suffix(".json").write_text(json.dumps({
        "boundary": b, "bundle_sha256": page_sha, "slots": prov, "quorum": q,
        "matcher": matcher, "prompt_sha256": sha(READINGS_PROMPT.read_text()),
        "match_prompt_sha256": sha(READINGS_MATCH_PROMPT.read_text()),
        "date": date.today().isoformat(), "admitted": admitted, "groups_raw": groups_raw,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  admitted {len(admitted)} readings → {out_md.relative_to(REPO)}", flush=True)
    return out_md


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--to", type=int, required=True, help="boundary chapter B")
    ap.add_argument("--force", action="store_true",
                    help="rebuild even if current; reuses cached slot extractions")
    ap.add_argument("--reextract", action="store_true",
                    help="also call every slot model again (paid for OpenRouter slots)")
    ap.add_argument("--readings", action="store_true",
                    help="build ck-ch<B>.readings.md (Impression, Symbolism, Open questions; "
                         "competing readings kept) instead of the facts")
    args = ap.parse_args()
    if args.readings:
        build_readings(args.to, args.reextract)
        return
    build(args.to, args.force or args.reextract, args.reextract)


if __name__ == "__main__":
    main()
