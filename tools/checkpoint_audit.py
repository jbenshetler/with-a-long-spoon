#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Evidence audit of a grounded checkpoint's FACT sections (author ruling 2026-11-01).

The extractor contract allows readings in Impression, Symbolism, Open questions and
the relationship axes; the fact sections are supposed to hold facts. They don't
always: opus ck-ch040:113 put "The reader suspects Randi looked in it" into the
dramatic-irony ledger, which every capture lane then read as memory.

This tool splits the fact sections into sentences, asks a judge to label each one
against the raw prose of chapters 1..B (FACT with a verbatim quote, INFERENCE,
UNSUPPORTED, CONTRADICTED), and verifies every quote by code: a FACT whose quote is
not on the page is downgraded to UNSUPPORTED. The result is written beside the
checkpoint as audit-ck-ch<B>.json, keyed to the checkpoint's sha256.

No one acks anything. Consumers apply it deterministically: `projection()` returns
the fact sections with only the FACT sentences kept — what the capture harness feeds
its v3 readers. It runs automatically at the end of a mint (checkpoint_extract.py)
and on first use by capture_dag.py; mints are infrequent and the auditor lane is
subscription. The cold-read lane's own reads are unchanged.

Usage:
  tools/checkpoint_audit.py reviews/cold-read/claude-opus-5-5/checkpoints/ck-ch040.md
  tools/checkpoint_audit.py <ck> --report      # print the non-FACT sentences
  tools/checkpoint_audit.py <ck> --show        # print the projection
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import threading
import unicodedata
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import cold_read_config  # noqa: E402

PROMPT = REPO / "reviews" / "cold-read" / "checkpoint-audit-prompt.md"
FACT_SECTIONS = ["Who's who", "Relationships", "What I know that they don't",
                 "Motifs & images", "Story so far"]
LABELS = ("FACT", "TRIM", "INFERENCE", "UNSUPPORTED", "CONTRADICTED")
# Never split after these; "Dr. Marsh" is one name.
_ABBR = r"(?<!\bDr\.)(?<!\bMr\.)(?<!\bMrs\.)(?<!\bMs\.)(?<!\bSt\.)(?<!\bvs\.)(?<!\be\.g\.)(?<!\bi\.e\.)"
SENT_SPLIT = re.compile(_ABBR + r"(?<=[.!?…])([\"”’)\]*]*)\s+(?=[\"“*(\[]?[A-Z0-9])")
LINE_RE = re.compile(r"^(?P<ws>\s*)(?:(?P<label>U\d{3,4})\s+)?")
OUT_RE = re.compile(r"^\W*(U\d{3,4})\W+(" + "|".join(LABELS) + r")\b\s*(.*)$")
_locks: dict[str, threading.Lock] = {}
_guard = threading.Lock()


def auditor_model() -> str:
    return str(cold_read_config.load_config()["capture"].get(
        "fact_auditor", "claude-opus-5-5"))


def audit_path(ck: Path) -> Path:
    return ck.with_name(f"audit-{ck.stem}.json")


def boundary_of(ck: Path) -> int:
    m = re.search(r"ck-ch(\d+)", ck.name)
    if not m:
        raise ValueError(f"not a checkpoint file: {ck.name}")
    return int(m.group(1))


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'",
                                   "—": "-", "–": "-", "…": "..."}))
    s = re.sub(r"[*_`\\]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def sentences(line: str) -> list[str]:
    """Split one line into sentences, keeping each piece's trailing closers."""
    out, last = [], 0
    for m in SENT_SPLIT.finditer(line):
        out.append(line[last:m.end(1)])
        last = m.end()
    out.append(line[last:])
    return [s for s in out if s.strip()]


def parse(body: str, structural: bool = True) -> list[dict]:
    """Every line of the checkpoint body, with its section, and — for fact lines —
    its sentence units. Axis lines (`a ↔ b`) are readings by contract."""
    rows, section = [], None
    for raw in body.splitlines():
        if raw.startswith("### "):
            section = raw[4:].strip()
            rows.append({"text": raw, "section": section, "kind": "heading"})
            continue
        # A `  > "…"` line under a consensus fact is the page's own words, verified when
        # the claim was parsed: structure, not a claim to audit.
        if re.match(r"^\s*>\s", raw):
            rows.append({"text": raw, "section": section, "kind": "quote"})
            continue
        label_only = re.fullmatch(r"\s*(?:[-*]\s+)?\*\*[^*]+\*\*:?\s*", raw)
        fact = (section in FACT_SECTIONS and "↔" not in raw and raw.strip()
                and not (structural and label_only))
        if not fact:
            rows.append({"text": raw, "section": section, "kind": "other"})
            continue
        prefix = re.match(r"^\s*(?:[-*]\s+|\d+\.\s+)?", raw).group(0)  # always matches
        rows.append({"text": raw, "section": section, "kind": "fact", "prefix": prefix,
                     "units": sentences(raw[len(prefix):])})
    return rows


def units(rows: list[dict]) -> list[tuple[str, str, str]]:
    out, k = [], 0
    for r in rows:
        if r["kind"] != "fact":
            continue
        for u in r["units"]:
            k += 1
            out.append((f"U{k:03d}", r["section"], u.strip()))
    return out


def words(s: str) -> str:
    """Letters and digits only: a quote is verified on its words, not its punctuation
    (glm wrote `Trade, she said.` for the page's `"Trade," she said.`)."""
    return " " + " ".join(re.findall(r"[a-z0-9]+(?:'[a-z]+)?", norm(s))) + " "


def verify(quote: str, page_words: str) -> bool:
    """`page_words` is words(page). Each run between ellipses must be on the page."""
    pieces = [words(p) for p in re.split(r"\.\.\.|…|\[\.\.\.\]", quote)]
    pieces = [p for p in pieces if len(p.split()) >= 2]
    if sum(len(p.split()) for p in pieces) < 3:
        return False
    return all(p in page_words for p in pieces)


def finalize(us: list[tuple[str, str, str]], out: str, page: str) -> list[dict]:
    """Turn the auditor's lines into verified labels. Deterministic: re-runnable from
    the stored raw output (`--reparse`) when this code changes."""
    got = {}
    for line in out.splitlines():
        if m := OUT_RE.match(line.strip()):
            got[m.group(1)] = (m.group(2), m.group(3).strip())
    page_norm = words(page)
    results, missing = [], 0
    for i, s, t in us:
        label, rest = got.get(i, ("MISSING", ""))
        missing += label == "MISSING"
        kept = None
        if label == "TRIM":
            m = re.match(r"\{(.*?)\}\s*(.*)$", rest)
            kept, quote = (m.group(1).strip(), m.group(2)) if m else (None, rest)
        else:
            quote = rest
        ok = verify(quote, page_norm) if label in ("FACT", "TRIM", "CONTRADICTED") else None
        final = label
        if label == "FACT" and not ok:
            # A short line of dialogue is its own evidence when it is on the page verbatim.
            claim = words(t)
            ok = len(claim.split()) >= 2 and claim in page_norm
        if label in ("FACT", "TRIM") and not ok:
            final = "UNSUPPORTED"
        # A trim may only delete: the kept text must be a contiguous run of the claim.
        if final == "TRIM" and not (kept and len(kept.split()) >= 2
                                    and norm(kept) in norm(t)):
            final = "INFERENCE"
        results.append({"id": i, "section": s, "text": t, "label": label,
                        "kept": kept, "quote": quote, "quote_verified": ok,
                        "final": final})
    if missing > len(us) // 10:
        raise RuntimeError(f"{missing}/{len(us)} claims unlabelled — re-run the audit")
    return results


def run_audit(ck: Path, auditor: str | None = None, force: bool = False) -> dict:
    """Audit `ck` (or return the current audit). Thread-safe per checkpoint."""
    key = str(ck.resolve())
    with _guard:
        lock = _locks.setdefault(key, threading.Lock())
    with lock:
        raw = ck.read_text(encoding="utf-8")
        ck_sha = sha(raw)
        ap = audit_path(ck)
        if ap.exists() and not force:
            cur = json.loads(ap.read_text(encoding="utf-8"))
            if cur.get("checkpoint_sha256") == ck_sha:
                return cur
        auditor = auditor or auditor_model()
        b = boundary_of(ck)
        body = checkpoint_bundle.checkpoint_body(raw)
        us = units(parse(body))
        page = checkpoint_bundle.build_reader_bundle(b, start=1)
        system = PROMPT.read_text(encoding="utf-8")
        claims = "\n".join(f"{i} [{s}] {t}" for i, s, t in us)
        prompt = (f"===== THE NOVEL, CHAPTERS 1–{b} =====\n\n{page}\n\n"
                  f"===== CLAIMS ({len(us)}) =====\n\n{claims}\n\n"
                  f"Label all {len(us)} claims now, U001 through U{len(us):03d}.")
        import capture_dag
        fn, close = capture_dag.make_agent(auditor, "medium")
        try:
            out = fn(system, prompt, f"audit·{auditor}·{ck.name}")
        finally:
            close()
        results = finalize(us, out, page)
        counts = {}
        for r in results:
            counts[r["final"]] = counts.get(r["final"], 0) + 1
        doc = {"checkpoint": str(ck.relative_to(REPO)), "checkpoint_sha256": ck_sha,
               "auditor": auditor, "prompt_sha256": sha(system), "date": date.today().isoformat(),
               "bundle_sha256": sha(page), "counts": counts, "units": results,
               "raw_output": out}
        ap.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  audit {ck.name}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
              + f" (auditor {auditor})", flush=True)
        return doc


# Knowledge-gap rule B (author ruling 2026-11-01). The page shows an event without a
# character present; "X does not know" is a deduction, so the audit calls it INFERENCE —
# but it is the dramatic irony a reader carries. In a consensus artifact, such a claim is
# kept when >= 2 slots wrote it independently with a verified quote AND it is in plain
# knowledge form. The form check is what keeps readings out: predictions ("will never
# know"), generalisations ("Retellings drift") and reader talk ("The reader suspects")
# do not match. UNSUPPORTED and CONTRADICTED are never overridden.
KNOWLEDGE_FORM = re.compile(
    r"^[A-Z][\w'’-]+(?:\s+and\s+[A-Z][\w'’-]+)?\s+(?:already\s+|still\s+|now\s+)?"
    r"(?:(?:does|do|did)\s+not\s+know|(?:doesn't|don't|didn't)\s+know|knows|know|knew|"
    r"(?:was|were|is|are)\s+not\s+told|(?:does\s+not|doesn't|did\s+not|didn't)\s+realize|"
    r"thinks|believes|assumes)\b")


def knowledge_keeps(ck: Path) -> set[str]:
    """Normalised texts of consensus KNOW claims that rule B keeps (empty if `ck` is
    not a consensus artifact)."""
    side = ck.with_suffix(".json")
    if not side.exists():
        return set()
    try:
        doc = json.loads(side.read_text(encoding="utf-8"))
    except ValueError:
        return set()
    return {norm(c["text"]).rstrip(".") for c in doc.get("admitted", [])
            if c.get("section") == "KNOW" and len(c.get("support", [])) >= 2
            and KNOWLEDGE_FORM.match(c["text"].strip())}


def projection(ck: Path, audit: dict | None) -> tuple[str, str]:
    """(fact-only text, note). With an audit, only FACT sentences survive; without
    one, the fact sections are kept whole (and the note says so)."""
    raw = ck.read_text(encoding="utf-8")
    rows = parse(checkpoint_bundle.checkpoint_body(raw))
    # Decisions are keyed by the claim's own text, never its position, so a change
    # to how lines are split can't move a label onto the wrong sentence.
    keep, trims = None, {}
    if audit and audit.get("checkpoint_sha256") == sha(raw):
        rule_b = knowledge_keeps(ck)
        keep = {norm(u["text"]) for u in audit["units"]
                if u["final"] in ("FACT", "TRIM")
                or (u["final"] == "INFERENCE" and rule_b
                    and norm(u["text"]).split(" (ch")[0].rstrip(".") in rule_b)}
        trims = {norm(u["text"]): u["kept"] for u in audit["units"] if u["final"] == "TRIM"}
    out, k, section, dropped, last_kept = [], 0, None, 0, False
    for r in rows:
        if r["kind"] == "heading":
            section = r["section"]
            if section in FACT_SECTIONS:
                out.append(r["text"])
            continue
        if section not in FACT_SECTIONS:
            continue
        if r["kind"] == "quote":
            if last_kept:          # a quote follows its fact; an orphan is dropped
                out.append(r["text"])
            continue
        if r["kind"] == "other":
            if "↔" not in r["text"]:
                out.append(r["text"])
            continue
        kept = []
        for u in r["units"]:
            k += 1
            uid = norm(u)
            if keep is None or uid in keep:
                part = trims.get(uid)
                if part:
                    part = part.rstrip(" ,;:—-")
                    kept.append(part if part.endswith((".", "!", "?", '"', "”")) else part + ".")
                else:
                    kept.append(u.strip())
            else:
                dropped += 1
        last_kept = bool(kept)
        if kept:
            out.append(r["prefix"] + " ".join(kept))
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    note = (f"audited, {dropped} non-fact sentence(s) dropped, {len(trims)} trimmed"
            if keep is not None
            else "UNAUDITED fact sections")
    return text, note


def reparse(ck: Path) -> dict:
    """Re-score a stored audit from its raw output (no model call)."""
    ap = audit_path(ck)
    doc = json.loads(ap.read_text(encoding="utf-8"))
    raw = ck.read_text(encoding="utf-8")
    if doc.get("checkpoint_sha256") != sha(raw) or "raw_output" not in doc:
        raise SystemExit(f"{ap.name} is not current for {ck.name}; run the audit")
    b = boundary_of(ck)
    us = [(u["id"], u["section"], u["text"]) for u in doc["units"]]
    doc["units"] = finalize(us, doc["raw_output"],
                            checkpoint_bundle.build_reader_bundle(b, start=1))
    doc["counts"] = {}
    for r in doc["units"]:
        doc["counts"][r["final"]] = doc["counts"].get(r["final"], 0) + 1
    ap.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  reparsed {ck.name}: " + ", ".join(f"{k} {v}" for k, v in sorted(doc["counts"].items())))
    return doc


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("checkpoint", type=Path)
    ap.add_argument("--auditor", help="model id (default [capture].fact_auditor)")
    ap.add_argument("--force", action="store_true", help="re-audit even if current")
    ap.add_argument("--report", action="store_true", help="print the non-FACT sentences")
    ap.add_argument("--show", action="store_true", help="print the projection")
    ap.add_argument("--reparse", action="store_true",
                    help="re-score the stored audit from its raw output, no model call")
    args = ap.parse_args()
    ck = args.checkpoint.resolve()
    doc = reparse(ck) if args.reparse else run_audit(ck, args.auditor, args.force)
    if args.report:
        for u in doc["units"]:
            if u["final"] != "FACT":
                extra = f'  [{u["label"]} rejected]' if u["label"] != u["final"] else ""
                kept = f'  → kept: {u["kept"]}' if u["final"] == "TRIM" else ""
                print(f'{u["id"]} {u["final"]:12} [{u["section"]}] {u["text"]}{kept}{extra}')
    if args.show:
        print(projection(ck, doc)[0])


if __name__ == "__main__":
    main()
