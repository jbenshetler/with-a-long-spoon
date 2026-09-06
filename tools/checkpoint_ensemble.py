#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
"""Build and verify quote-backed, cross-vendor checkpoint ensembles."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpoint_bundle  # noqa: E402
import cold_read  # noqa: E402
import cold_read_config  # noqa: E402

MATCHER_DEF = REPO / ".claude" / "agents" / "checkpoint-ensemble-matcher.md"
EXTRACTOR_DEF = REPO / ".claude" / "agents" / "blind-extractor.md"
CONFIG_PATH = cold_read_config.CONFIG_PATH

SECTIONS = (
    "Who's who",
    "Relationships",
    "What I know that they don't",
    "Motifs & images",
    "Symbolism",
    "Open questions",
    "Story so far",
    "Impression",
)
CLAIM_TYPES = {
    "entity",
    "event",
    "state",
    "knowledge",
    "motif",
    "symbolism",
    "open_question",
    "story",
    "impression",
}
FACT_TYPES = {"entity", "event", "state", "knowledge", "story"}
IMMUTABLE_TYPES = {"entity", "event"}
TEMPORAL_TYPES = CLAIM_TYPES - IMMUTABLE_TYPES


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def checkpoint_body(raw: str) -> str:
    marker = "\n---\n\n"
    return raw.split(marker, 1)[1].strip() if marker in raw else raw.strip()


def metadata_value(raw: str, key: str) -> str | None:
    header = raw.split("\n---\n", 1)[0]
    match = re.search(rf"(?:^| · ){re.escape(key)}: ([^·*\n]+)", header)
    return match.group(1).strip() if match else None


def paths_for(name: str, boundary: int) -> dict[str, Path]:
    root = cold_read_config.REVIEWS_ROOT / "checkpoint-ensembles" / name
    stem = f"ck-ch{boundary:03d}"
    return {
        "root": root,
        "checkpoint": root / "checkpoints" / f"{stem}.md",
        "claims": root / "claims" / f"{stem}.json",
        "manifest": root / "manifests" / f"{stem}.json",
        "conflicts": root / "conflicts" / f"{stem}.json",
    }

def persist_matcher_attempt(
    name: str,
    boundary: int,
    *,
    model: str,
    result: dict[str, Any],
) -> Path:
    """Persist the exact matcher response before any parsing or validation."""
    root = paths_for(name, boundary)["root"] / "matcher-attempts"
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"ck-ch{boundary:03d}-{int(time.time() * 1000)}.json"
    path.write_bytes(
        json_bytes(
            {
                "version": 1,
                "ensemble": name,
                "boundary": boundary,
                "model": model,
                "response_id": result.get("id"),
                "usage": result.get("usage"),
                "raw_output": result.get("output") or "",
            }
        )
    )
    return path


def source_records(name: str, boundary: int) -> tuple[list[dict[str, Any]], str, dict[str, str | int]]:
    settings = cold_read_config.ensemble_settings(name)
    source_defs = settings.get("sources") or []
    if not source_defs:
        raise SystemExit(f"ensemble {name} has no sources")

    bundle = checkpoint_bundle.build_reader_bundle(boundary)
    extractor_prompt = cold_read.load_agent_prompt(EXTRACTOR_DEF)
    current_fingerprints = checkpoint_bundle.source_fingerprints(bundle, extractor_prompt)
    records: list[dict[str, Any]] = []
    problems: list[str] = []

    for source in source_defs:
        model_id = str(source["model_id"])
        vendor = str(source["vendor"])
        path = cold_read_config.REVIEWS_ROOT / model_id / "checkpoints" / f"ck-ch{boundary:03d}.md"
        if not path.exists():
            problems.append(f"{model_id}: missing {path.relative_to(REPO)}")
            continue
        raw = path.read_text(encoding="utf-8")
        declared = metadata_value(raw, "source-sha256")
        if not declared:
            problems.append(f"{model_id}: checkpoint predates source fingerprints; remint it")
        elif declared != current_fingerprints["source_sha256"]:
            problems.append(
                f"{model_id}: stale source {declared[:12]} != current "
                f"{str(current_fingerprints['source_sha256'])[:12]}; remint it"
            )
        records.append(
            {
                "model_id": model_id,
                "vendor": vendor,
                "path": path,
                "raw": raw,
                "body": checkpoint_body(raw),
                "sha256": sha256_bytes(path.read_bytes()),
                "source_sha256": declared,
            }
        )

    if problems:
        raise SystemExit("source checkpoints are not ensemble-compatible:\n  " + "\n  ".join(problems))
    declared_sources = {record["source_sha256"] for record in records}
    if len(declared_sources) != 1:
        raise SystemExit("source checkpoints do not share one manuscript fingerprint")
    return records, bundle, current_fingerprints


def matcher_schema() -> dict[str, Any]:
    return {
        "claims": [
            {
                "section": list(SECTIONS),
                "type": "entity|event|state|knowledge|motif|symbolism|open_question|story|impression",
                "entity_subtype": "identity|alias|gender|presence|role, only for entity claims",
                "slot": "stable semantic slot; required for every claim",
                "competing": False,
                "text": "concise checkpoint statement without a leading bullet",
                "valid_from": 1,
                "superseded_at": None,
                "support": [
                    {"model": "source model id", "quote": "exact checkpoint substring"}
                ],
                "scene_evidence": [
                    {"slug": "exact chapter slug", "quote": "exact clean-scene substring"}
                ],
            }
        ],
        "conflicts": [
            {
                "topic": "concise topic",
                "sources": [
                    {"model": "source model id", "quote": "exact checkpoint substring"}
                ],
                "note": "what conflicts; do not resolve it",
            }
        ],
        "prior_ledger_sha256": None,
    }


def matcher_prompt(name: str, boundary: int, sources: list[dict[str, Any]], bundle: str) -> str:
    settings = cold_read_config.ensemble_settings(name)
    chapters = [
        {
            "number": index,
            "slug": slug,
            "title": checkpoint_bundle.display_title(slug),
        }
        for index, slug in enumerate(checkpoint_bundle.reader_slugs()[:boundary], start=1)
    ]
    source_roster = [
        {"model_id": record["model_id"], "vendor": record["vendor"]}
        for record in sources
    ]
    prior_path, prior = previous_ledger(name, boundary)
    prior_sha256 = sha256_bytes(prior_path.read_bytes()) if prior_path else None
    parts = [
        "BOUNDARY AND POLICY:\n"
        + json.dumps(
            {
                "ensemble": name,
                "boundary": boundary,
                "quorum": settings["quorum"],
                "cross_vendor": settings["cross_vendor"],
                "source_roster": source_roster,
                "chapters": chapters,
                "prior_ledger_sha256": prior_sha256,
            },
            ensure_ascii=False,
            indent=2,
        ),
        "OUTPUT SCHEMA:\n" + json.dumps(matcher_schema(), ensure_ascii=False, indent=2),
    ]
    if prior:
        parts.append(
            "===== PRIOR ACTIVE ENSEMBLE LEDGER =====\n"
            + json.dumps(
                {
                    "sha256": prior_sha256,
                    "boundary": prior["boundary"],
                    "claims": prior.get("claims", []),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    for record in sources:
        parts.append(
            f"===== SOURCE CHECKPOINT: {record['model_id']} · vendor={record['vendor']} =====\n"
            + record["body"]
        )
    parts.append("===== FULL CLEAN SOURCE BUNDLE FOR FACT VERIFICATION =====\n" + bundle)
    return "\n\n".join(parts)


def parse_matcher_output(text: str) -> dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate)
        candidate = re.sub(r"\s*```$", "", candidate)
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ValueError(f"matcher did not return valid JSON: {exc}") from exc
    if isinstance(value, dict) and isinstance(value.get("matcher_payload"), dict):
        value = value["matcher_payload"]
    if not isinstance(value, dict) or not isinstance(value.get("claims"), list):
        raise ValueError("matcher output must be an object with a claims array")
    if not isinstance(value.get("conflicts", []), list):
        raise ValueError("matcher conflicts must be an array")
    value.setdefault("conflicts", [])
    return value


def scene_map(boundary: int) -> dict[str, str]:
    return {
        slug: checkpoint_bundle.clean_scene_text(slug)
        for slug in checkpoint_bundle.reader_slugs()[:boundary]
    }


def _quote_key(text: str) -> tuple[str, list[int]]:
    translated = {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "—": "-",
        "–": "-",
        "…": "...",
    }
    chars: list[str] = []
    positions: list[int] = []
    for index, char in enumerate(text):
        if char.isspace() or char in "*_`":
            continue
        replacement = translated.get(char, char)
        for normalized in replacement:
            chars.append(normalized)
            positions.append(index)
    return "".join(chars), positions


def resolve_quote(haystack: str, proposed: str, minimum: int) -> str | None:
    """Return an exact source substring; tolerate typography/markdown/whitespace only."""
    if len(proposed.strip()) < minimum:
        return None
    if proposed in haystack:
        return proposed
    haystack_key, positions = _quote_key(haystack)
    proposed_key, _ = _quote_key(proposed)
    if len(proposed_key) < minimum:
        return None
    start = haystack_key.find(proposed_key)
    if start < 0 or haystack_key.find(proposed_key, start + 1) >= 0:
        return None
    return haystack[positions[start] : positions[start + len(proposed_key) - 1] + 1]


def resolve_scene_slug(slug: str, scenes: dict[str, str]) -> str | None:
    if slug in scenes:
        return slug
    key = re.sub(r"^(?:the|a|an)-", "", slug)
    matches = [candidate for candidate in scenes if re.sub(r"^(?:the|a|an)-", "", candidate) == key]
    return matches[0] if len(matches) == 1 else None


def validate_claims(
    payload: dict[str, Any],
    *,
    name: str,
    boundary: int,
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    settings = cold_read_config.ensemble_settings(name)
    quorum = int(settings["quorum"])
    source_by_model = {record["model_id"]: record for record in sources}
    scenes = scene_map(boundary)
    errors: list[str] = []
    accepted: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for index, raw_claim in enumerate(payload.get("claims", []), start=1):
        label = f"claim {index}"
        if not isinstance(raw_claim, dict):
            errors.append(f"{label}: not an object")
            continue
        claim = dict(raw_claim)
        section = claim.get("section")
        claim_type = claim.get("type")
        text = str(claim.get("text") or "").strip().lstrip("- ").strip()
        slot = str(claim.get("slot") or "").strip()
        valid_from = claim.get("valid_from")
        superseded_at = claim.get("superseded_at")
        support = claim.get("support") or []
        evidence = claim.get("scene_evidence") or []
        entity_subtype = str(claim.get("entity_subtype") or "").strip()
        competing = claim.get("competing") is True
        carried_from = claim.get("carried_from_boundary")
        if isinstance(valid_from, str) and valid_from.isdigit():
            valid_from = int(valid_from)

        if section not in SECTIONS:
            errors.append(f"{label}: invalid section {section!r}")
        if claim_type not in CLAIM_TYPES:
            errors.append(f"{label}: invalid type {claim_type!r}")
        if not text or "\n### " in text or len(text) > 1200:
            errors.append(f"{label}: invalid text")
        if not slot:
            errors.append(f"{label}: claim needs a stable slot")
        if not isinstance(valid_from, int) or not (1 <= valid_from <= boundary):
            errors.append(f"{label}: valid_from must be within 1..{boundary}")
        if superseded_at is not None:
            errors.append(f"{label}: rendered checkpoint may contain only active claims")

        models: set[str] = set()
        vendors: set[str] = set()
        valid_support: list[dict[str, str]] = []
        if carried_from is not None:
            if not isinstance(carried_from, int) or carried_from >= boundary:
                errors.append(f"{label}: invalid prior-boundary carry marker")
        else:
            if not isinstance(support, list):
                errors.append(f"{label}: support must be a list")
                support = []
            for item in support:
                if not isinstance(item, dict):
                    continue
                model = str(item.get("model") or "")
                proposed = str(item.get("quote") or "")
                record = source_by_model.get(model)
                if record is None:
                    continue
                quote = resolve_quote(record["body"], proposed, 20)
                if quote is None or model in models:
                    continue
                models.add(model)
                vendors.add(record["vendor"])
                valid_support.append({"model": model, "quote": quote})
        claim["support"] = valid_support if carried_from is None else support

        valid_evidence_items: list[dict[str, str]] = []
        if not isinstance(evidence, list):
            errors.append(f"{label}: scene_evidence must be a list")
            evidence = []
        for item in evidence:
            if not isinstance(item, dict):
                continue
            proposed_slug = str(item.get("slug") or "")
            slug = resolve_scene_slug(proposed_slug, scenes)
            if slug is None:
                continue
            quote = resolve_quote(scenes[slug], str(item.get("quote") or ""), 12)
            if quote is not None:
                valid_evidence_items.append({"slug": slug, "quote": quote})
        claim["scene_evidence"] = valid_evidence_items
        valid_evidence = len(valid_evidence_items)

        entity_exception_types = {"identity", "alias", "gender", "presence", "role"}
        entity_slot = re.fullmatch(
            r"entity:[a-z0-9][a-z0-9:-]*:(identity|alias|gender|presence|role)",
            slot,
        )
        entity_exception = (
            claim_type == "entity"
            and entity_subtype in entity_exception_types
            and entity_slot is not None
            and entity_slot.group(1) == entity_subtype
            and len(models) == 1
            and valid_evidence > 0
        )
        if claim_type == "entity" and len(models) == 1 and not entity_exception:
            errors.append(
                f"{label}: one-source entity exception needs a matching "
                "entity:<subject>:<identity|alias|gender|presence|role> slot and subtype"
            )
        if carried_from is None and not entity_exception:
            if len(models) < quorum:
                errors.append(f"{label}: {len(models)} valid source(s), needs {quorum}")
            if settings.get("cross_vendor") and len(vendors) < 2:
                errors.append(f"{label}: support lacks cross-vendor agreement")
        if claim_type in FACT_TYPES and valid_evidence == 0:
            errors.append(f"{label}: factual claim lacks exact clean-scene evidence")

        identity = {
            "section": section,
            "type": claim_type,
            "slot": slot,
            "text": text,
            "valid_from": valid_from,
        }
        claim_id = sha256_bytes(json_bytes(identity))[:20]
        if claim.get("id") not in (None, claim_id):
            errors.append(f"{label}: claim id does not match normalized content")
        if claim_id in seen_ids:
            errors.append(f"{label}: duplicate normalized claim {claim_id}")
        seen_ids.add(claim_id)
        claim["id"] = claim_id
        claim["text"] = text
        claim["slot"] = slot
        claim["valid_from"] = valid_from
        claim["superseded_at"] = None
        claim["competing"] = competing
        accepted.append(claim)
    temporal_slots: dict[str, list[dict[str, Any]]] = {}
    immutable_slots: dict[str, list[dict[str, Any]]] = {}
    for claim in accepted:
        if claim["type"] in TEMPORAL_TYPES:
            temporal_slots.setdefault(claim["slot"], []).append(claim)
        elif claim["slot"]:
            immutable_slots.setdefault(claim["slot"], []).append(claim)
    for slot, claims in temporal_slots.items():
        if len(claims) < 2:
            continue
        competing_readings = all(
            claim["competing"] and claim["type"] in {"motif", "symbolism", "impression"}
            for claim in claims
        )
        if not competing_readings:
            errors.append(f"temporal slot {slot!r} has {len(claims)} active claims")
    for slot, claims in immutable_slots.items():
        if len(claims) > 1:
            errors.append(f"immutable slot {slot!r} has {len(claims)} active claims")

    if errors:
        raise ValueError("ensemble claim validation failed:\n  " + "\n  ".join(errors))

    order = {section: index for index, section in enumerate(SECTIONS)}
    accepted.sort(key=lambda claim: (order[claim["section"]], claim["type"], claim["slot"], claim["text"]))
    return {
        "version": 1,
        "ensemble": name,
        "boundary": boundary,
        "claims": accepted,
        "history": list(payload.get("history") or []),
    }


def admit_candidate_claims(
    payload: dict[str, Any],
    *,
    name: str,
    boundary: int,
    sources: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, int]]:
    """Admit valid claims individually, then fail closed on aggregate coverage."""
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for index, claim in enumerate(payload.get("claims", []), start=1):
        try:
            single = validate_claims(
                {"claims": [claim]}, name=name, boundary=boundary, sources=sources
            )
            accepted.extend(single["claims"])
        except ValueError as exc:
            rejected.append({"index": index, "error": str(exc), "claim": claim})

    ledger = validate_claims(
        {"claims": accepted}, name=name, boundary=boundary, sources=sources
    )
    ledger["prior_ledger_sha256"] = payload.get("prior_ledger_sha256")
    coverage = {
        section: sum(1 for claim in ledger["claims"] if claim["section"] == section)
        for section in SECTIONS
    }
    settings = cold_read_config.ensemble_settings(name)
    problems = []
    minimum = int(settings.get("minimum_claims", 1))
    if len(ledger["claims"]) < minimum:
        problems.append(f"{len(ledger['claims'])} admitted claims, needs at least {minimum}")
    missing_sections = [
        section for section in settings.get("required_sections", SECTIONS)
        if coverage.get(section, 0) == 0
    ]
    if missing_sections:
        problems.append("no admitted claim in: " + ", ".join(missing_sections))
    if problems:
        raise ValueError("ensemble coverage failed: " + "; ".join(problems))
    return ledger, rejected, coverage


def validate_conflicts(conflicts: list[Any], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_by_model = {record["model_id"]: record for record in sources}
    checked: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, conflict in enumerate(conflicts, start=1):
        if not isinstance(conflict, dict):
            errors.append(f"conflict {index}: not an object")
            continue
        source_items = conflict.get("sources") or []
        models: set[str] = set()
        for item in source_items:
            if not isinstance(item, dict):
                errors.append(f"conflict {index}: malformed source")
                continue
            model = str(item.get("model") or "")
            quote = str(item.get("quote") or "")
            record = source_by_model.get(model)
            if record is None or len(quote.strip()) < 20 or quote not in record["body"]:
                errors.append(f"conflict {index}: invalid exact quote for {model!r}")
            else:
                models.add(model)
        if len(models) < 2:
            errors.append(f"conflict {index}: needs at least two quoted sources")
        checked.append(dict(conflict))
    if errors:
        raise ValueError("ensemble conflict validation failed:\n  " + "\n  ".join(errors))
    return checked


def previous_ledger(name: str, boundary: int) -> tuple[Path | None, dict[str, Any] | None]:
    claims_dir = paths_for(name, boundary)["root"] / "claims"
    candidates: list[tuple[int, Path]] = []
    if claims_dir.is_dir():
        for path in claims_dir.glob("ck-ch*.json"):
            match = re.fullmatch(r"ck-ch(\d{3})\.json", path.name)
            if match and int(match.group(1)) < boundary:
                candidates.append((int(match.group(1)), path))
    if not candidates:
        return None, None
    _prior_boundary, path = max(candidates)
    return path, json.loads(path.read_text(encoding="utf-8"))


def merge_temporal_ledger(
    current: dict[str, Any], *, name: str, boundary: int
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Preserve omitted claims; supersede temporal claims only by validated slot replacement."""
    prior_path, prior = previous_ledger(name, boundary)
    if prior_path is None or prior is None:
        current["history"] = []
        return current, None

    expected_prior_sha = sha256_bytes(prior_path.read_bytes())
    if current.get("prior_ledger_sha256") != expected_prior_sha:
        raise ValueError(
            "matcher payload does not identify the prior ledger it was asked to reconcile"
        )

    active = list(current["claims"])
    active_ids = {claim["id"] for claim in active}
    current_by_slot: dict[str, list[dict[str, Any]]] = {}
    for claim in active:
        if claim.get("slot"):
            current_by_slot.setdefault(claim["slot"], []).append(claim)

    history = list(prior.get("history") or [])
    for old_claim in prior.get("claims") or []:
        slot_claims = current_by_slot.get(str(old_claim.get("slot") or ""), [])
        same_claim = any(claim.get("id") == old_claim.get("id") for claim in slot_claims)
        changed_claims = [
            claim for claim in slot_claims if claim.get("id") != old_claim.get("id")
        ]
        if old_claim.get("type") in IMMUTABLE_TYPES and changed_claims:
            raise ValueError(
                f"immutable slot {old_claim.get('slot')!r} changed at boundary {boundary}"
            )
        if old_claim.get("id") in active_ids or same_claim:
            continue
        replacements = changed_claims
        carried = dict(old_claim)
        if old_claim.get("type") in TEMPORAL_TYPES and replacements:
            carried["superseded_at"] = boundary
            history.append(carried)
            continue
        carried["carried_from_boundary"] = int(
            old_claim.get("carried_from_boundary") or prior["boundary"]
        )
        active.append(carried)
        active_ids.add(carried["id"])

    history_keys: set[tuple[str, int]] = set()
    deduped_history = []
    for claim in history:
        key = (str(claim.get("id")), int(claim.get("superseded_at") or boundary))
        if key not in history_keys:
            history_keys.add(key)
            deduped_history.append(claim)
    order = {section: index for index, section in enumerate(SECTIONS)}
    active.sort(key=lambda claim: (order[claim["section"]], claim["type"], claim["slot"], claim["text"]))
    current["claims"] = active
    current["history"] = deduped_history
    lineage = {
        "path": str(prior_path.relative_to(REPO)),
        "sha256": expected_prior_sha,
        "boundary": prior["boundary"],
    }
    return current, lineage


def render_checkpoint(name: str, boundary: int, ledger: dict[str, Any], source_sha256: str) -> str:
    grouped = {section: [] for section in SECTIONS}
    for claim in ledger["claims"]:
        grouped[claim["section"]].append(claim)
    body: list[str] = []
    for section in SECTIONS:
        body.append(f"### {section}")
        claims = grouped[section]
        if claims:
            body.extend(f"- {claim['text']}" for claim in claims)
        else:
            body.append("- No claim met the ensemble admission rule at this boundary.")
        body.append("")
    return (
        f"# Checkpoint — through Chapter {boundary} (quote-backed ensemble)\n\n"
        f"*ensemble: {name} · span: ch001–ch{boundary:03d} · source-sha256: {source_sha256} · "
        "admission: 2-of-4 cross-vendor; source-verified entity exception; "
        "impressions require quorum*\n\n---\n\n"
        + "\n".join(body).rstrip()
        + "\n"
    )


def run_matcher(
    name: str,
    boundary: int,
    sources: list[dict[str, Any]],
    bundle: str,
    effort: str,
) -> tuple[dict[str, Any], Path]:
    settings = cold_read_config.ensemble_settings(name)
    model = str(settings["matcher_model"])
    system_prompt = cold_read.load_agent_prompt(MATCHER_DEF)
    prompt = matcher_prompt(name, boundary, sources, bundle)
    agent_fn, close = cold_read.make_codex_agent_fn(system_prompt=system_prompt, effort=effort)
    try:
        result = agent_fn(prompt=prompt, model=model, label=f"ensemble-{name}-ck{boundary:03d}")
    finally:
        close()
    attempt_path = persist_matcher_attempt(
        name, boundary, model=model, result=result
    )
    output = result.get("output") or ""
    if len(output.strip()) < 200:
        raise ValueError(
            f"suspiciously short matcher output ({len(output.strip())} chars); "
            f"raw response: {attempt_path}"
        )
    try:
        return parse_matcher_output(output), attempt_path
    except ValueError as exc:
        raise ValueError(f"{exc}; raw response: {attempt_path}") from exc


def build(name: str, boundary: int, *, claims_path: Path | None, effort: str) -> Path:
    sources, bundle, fingerprints = source_records(name, boundary)
    matcher_attempt: Path | None = None
    matcher_input: dict[str, str] | None = None
    if claims_path is not None:
        candidate_bytes = claims_path.read_bytes()
        candidate_sha = sha256_bytes(candidate_bytes)
        owned_input = (
            paths_for(name, boundary)["root"]
            / "matcher-inputs"
            / f"ck-ch{boundary:03d}-{candidate_sha[:12]}.json"
        )
        owned_input.parent.mkdir(parents=True, exist_ok=True)
        if owned_input.exists() and owned_input.read_bytes() != candidate_bytes:
            raise ValueError(f"owned matcher input hash collision: {owned_input}")
        owned_input.write_bytes(candidate_bytes)
        payload = parse_matcher_output(candidate_bytes.decode("utf-8"))
        matcher_mode = f"validated-file:{candidate_sha}"
        matcher_input = {
            "path": str(owned_input.relative_to(REPO)),
            "sha256": candidate_sha,
        }
    else:
        payload, matcher_attempt = run_matcher(name, boundary, sources, bundle, effort)
        matcher_mode = "codex-subscription"

    try:
        candidate_ledger, rejected_claims, coverage = admit_candidate_claims(
            payload, name=name, boundary=boundary, sources=sources
        )
        ledger, prior_lineage = merge_temporal_ledger(
            candidate_ledger, name=name, boundary=boundary
        )
        conflicts = validate_conflicts(payload.get("conflicts", []), sources)
    except ValueError as exc:
        failure_dir = Path("/tmp/ramdisk")
        failure_dir.mkdir(parents=True, exist_ok=True)
        failure_path = failure_dir / (
            f"ensemble-failure-{name}-ch{boundary:03d}-{int(time.time())}.json"
        )
        failure_path.write_text(
            json.dumps(
                {
                    "ensemble": name,
                    "boundary": boundary,
                    "error": str(exc),
                    "matcher_payload": payload,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        raise ValueError(f"{exc}\ndiagnostics: {failure_path}") from exc
    checkpoint = render_checkpoint(
        name, boundary, ledger, str(fingerprints["source_sha256"])
    )
    output_paths = paths_for(name, boundary)
    for key in ("checkpoint", "claims", "manifest", "conflicts"):
        output_paths[key].parent.mkdir(parents=True, exist_ok=True)

    claims_data = json_bytes(ledger)
    conflicts_data = json_bytes(
        {
            "version": 1,
            "ensemble": name,
            "boundary": boundary,
            "conflicts": conflicts,
            "rejected_claims": rejected_claims,
            "coverage": coverage,
        }
    )
    output_paths["checkpoint"].write_text(checkpoint, encoding="utf-8")
    output_paths["claims"].write_bytes(claims_data)
    output_paths["conflicts"].write_bytes(conflicts_data)

    settings = cold_read_config.ensemble_settings(name)
    manifest = {
        "version": 1,
        "ensemble": name,
        "boundary": boundary,
        "created_unix": int(time.time()),
        "matcher_model": settings["matcher_model"],
        "matcher_mode": matcher_mode,
        "matcher_prompt_sha256": sha256_bytes(MATCHER_DEF.read_bytes()),
        "config_sha256": sha256_bytes(CONFIG_PATH.read_bytes()),
        "matcher_attempt": (
            {
                "path": str(matcher_attempt.relative_to(REPO)),
                "sha256": sha256_bytes(matcher_attempt.read_bytes()),
            }
            if matcher_attempt
            else None
        ),
        "matcher_input": matcher_input,
        "source_sha256": fingerprints["source_sha256"],
        "bundle_sha256": fingerprints["bundle_sha256"],
        "cleaner_version": fingerprints["cleaner_version"],
        "extractor_sha256": fingerprints["extractor_sha256"],
        "sources": [
            {
                "model_id": record["model_id"],
                "vendor": record["vendor"],
                "path": str(record["path"].relative_to(REPO)),
                "checkpoint_sha256": record["sha256"],
                "source_sha256": record["source_sha256"],
            }
            for record in sources
        ],
        "claims_sha256": sha256_bytes(claims_data),
        "conflicts_sha256": sha256_bytes(conflicts_data),
        "coverage": coverage,
        "rejected_claims": len(rejected_claims),
        "ensemble_sha256": sha256_text(checkpoint),
        "prior_ledger": prior_lineage,
    }
    output_paths["manifest"].write_bytes(json_bytes(manifest))
    return output_paths["checkpoint"]


def check(name: str, boundary: int) -> Path:
    output_paths = paths_for(name, boundary)
    missing = [key for key in ("checkpoint", "claims", "manifest", "conflicts") if not output_paths[key].exists()]
    if missing:
        raise SystemExit("missing ensemble artifacts: " + ", ".join(missing))

    sources, _bundle, fingerprints = source_records(name, boundary)
    manifest = json.loads(output_paths["manifest"].read_text(encoding="utf-8"))
    claims = json.loads(output_paths["claims"].read_text(encoding="utf-8"))
    conflicts = json.loads(output_paths["conflicts"].read_text(encoding="utf-8"))
    checkpoint = output_paths["checkpoint"].read_text(encoding="utf-8")
    errors: list[str] = []

    expected_sources = {record["model_id"]: record["sha256"] for record in sources}
    actual_sources = {item["model_id"]: item["checkpoint_sha256"] for item in manifest.get("sources", [])}
    if actual_sources != expected_sources:
        errors.append("source checkpoint hashes changed")
    if manifest.get("source_sha256") != fingerprints["source_sha256"]:
        errors.append("source bundle fingerprint changed")
    if manifest.get("config_sha256") != sha256_bytes(CONFIG_PATH.read_bytes()):
        errors.append("ensemble configuration changed")
    if manifest.get("matcher_prompt_sha256") != sha256_bytes(MATCHER_DEF.read_bytes()):
        errors.append("matcher contract changed")
    for key, label in (
        ("matcher_input", "validated matcher input"),
        ("matcher_attempt", "raw matcher attempt"),
    ):
        provenance = manifest.get(key)
        if not provenance:
            continue
        provenance_path = Path(str(provenance.get("path")))
        if not provenance_path.is_absolute():
            provenance_path = REPO / provenance_path
        if not provenance_path.exists():
            errors.append(f"{label} is missing")
        elif sha256_bytes(provenance_path.read_bytes()) != provenance.get("sha256"):
            errors.append(f"{label} hash changed")
    if manifest.get("claims_sha256") != sha256_bytes(json_bytes(claims)):
        errors.append("claim ledger hash mismatch")
    if manifest.get("conflicts_sha256") != sha256_bytes(json_bytes(conflicts)):
        errors.append("conflict ledger hash mismatch")
    if manifest.get("ensemble_sha256") != sha256_text(checkpoint):
        errors.append("ensemble checkpoint hash mismatch")
    positions = [checkpoint.find(f"### {section}") for section in SECTIONS]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        errors.append("checkpoint sections missing or out of order")
    prior_lineage = manifest.get("prior_ledger")
    if prior_lineage:
        prior_path = REPO / str(prior_lineage.get("path"))
        if not prior_path.exists():
            errors.append("prior claim ledger is missing")
        elif sha256_bytes(prior_path.read_bytes()) != prior_lineage.get("sha256"):
            errors.append("prior claim ledger hash changed")
        else:
            prior = json.loads(prior_path.read_text(encoding="utf-8"))
            prior_ids = {claim.get("id") for claim in prior.get("claims", [])}
            for claim in claims.get("claims", []):
                if claim.get("carried_from_boundary") is not None and claim.get("id") not in prior_ids:
                    errors.append(f"carried claim {claim.get('id')} is absent from prior ledger")

    validate_claims(claims, name=name, boundary=boundary, sources=sources)
    validate_conflicts(conflicts.get("conflicts", []), sources)
    if errors:
        raise SystemExit("ensemble check failed:\n  " + "\n  ".join(errors))
    return output_paths["checkpoint"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("build", "check"):
        child = sub.add_parser(command)
        child.add_argument("--ensemble", default="core")
        child.add_argument("--through", type=int, required=True)
        if command == "build":
            child.add_argument("--claims", type=Path, default=None, help="validate supplied matcher JSON instead of calling the matcher")
            child.add_argument("--effort", choices=["none", "low", "medium", "high"], default="low")
    args = parser.parse_args()

    try:
        if args.command == "build":
            path = build(args.ensemble, args.through, claims_path=args.claims, effort=args.effort)
            print(f"built {path.relative_to(REPO)}")
        else:
            path = check(args.ensemble, args.through)
            print(f"valid {path.relative_to(REPO)}")
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
