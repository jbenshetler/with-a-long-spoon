#!/usr/bin/env python3
"""Shared cold-read panel, reader-memory, and ensemble configuration."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import tomllib

REPO = Path(__file__).resolve().parent.parent
REVIEWS_ROOT = REPO / "reviews" / "cold-read"
CONFIG_PATH = REVIEWS_ROOT / "ensemble-config.toml"


@lru_cache(maxsize=1)
def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("rb") as handle:
        config = tomllib.load(handle)
    if config.get("version") != 1:
        raise ValueError(f"unsupported cold-read config version: {config.get('version')!r}")
    return config


def panel_models(*, fast: bool = False) -> tuple[str, ...]:
    key = "fast" if fast else "models"
    return tuple(load_config()["panel"][key])


def panel_retired() -> tuple[str, ...]:
    return tuple(load_config()["panel"].get("retired", ()))


def capture_models() -> tuple[str, ...]:
    """The capture-DAG roster (`[capture].models`) — the single source of truth."""
    return tuple(load_config()["capture"]["models"])


def capture_retired() -> tuple[str, ...]:
    return tuple(load_config()["capture"].get("retired", ()))


def openrouter_models() -> dict[str, str]:
    """model id -> OpenRouter provider model, for every reader block that declares one."""
    readers = load_config().get("readers", {})
    return {mid: s["provider_model"] for mid, s in readers.items() if s.get("provider_model")}


def reader_settings(model_id: str) -> dict[str, Any]:
    readers = load_config().get("readers", {})
    direct = readers.get(model_id)
    if direct is not None:
        return dict(direct)
    for settings in readers.values():
        if settings.get("provider_model") == model_id:
            return dict(settings)
    return {}


def openrouter_routing(model_id: str | None = None) -> dict[str, Any]:
    """The provider-routing block sent with an OpenRouter call.

    The `[openrouter]` floor filters the endpoint pool by numeric precision;
    see that block's comment in ensemble-config.toml for why it is not
    optional. A reader may override `quantizations` in its own
    `[readers."<id>"]` block: the filter protects against *third-party
    resellers* serving an open-weight model at reduced precision, which is
    not a risk that exists for a first-party proprietary model with a single
    vendor. An empty list disables the filter for that reader.

    Passing no `model_id` returns the bare floor."""
    block = dict(load_config().get("openrouter", {}))
    block.pop("policy", None)
    if model_id:
        override = reader_settings(model_id).get("quantizations")
        if override is not None:
            if override:
                block["quantizations"] = list(override)
            else:
                block.pop("quantizations", None)
    return block


def openrouter_policy(tag: str) -> dict[str, Any]:
    """Call parameters for one use (`mint`, `read`, `judge`, `audit`, `capture`).

    Raises on an unknown tag rather than silently falling back to defaults —
    an unnamed policy is how per-tool drift got in."""
    policies = load_config().get("openrouter", {}).get("policy", {})
    if tag not in policies:
        raise KeyError(
            f"unknown openrouter policy {tag!r}; "
            f"known: {', '.join(sorted(policies)) or '(none)'}"
        )
    return dict(policies[tag])


def checkpoint_source(model_id: str) -> str:
    return str(reader_settings(model_id).get("checkpoint_source", "native"))


def can_mint_checkpoint(model_id: str) -> bool:
    return bool(reader_settings(model_id).get("can_mint_checkpoint", True))


def ensemble_settings(name: str) -> dict[str, Any]:
    try:
        return dict(load_config()["ensembles"][name])
    except KeyError as exc:
        raise ValueError(f"unknown checkpoint ensemble: {name}") from exc


def checkpoint_path(model_id: str, boundary: int) -> Path:
    source = checkpoint_source(model_id)
    filename = f"ck-ch{boundary:03d}.md"
    if source == "native":
        return REVIEWS_ROOT / model_id / "checkpoints" / filename
    if source.startswith("ensemble:"):
        name = source.split(":", 1)[1]
        return REVIEWS_ROOT / "checkpoint-ensembles" / name / "checkpoints" / filename
    raise ValueError(f"unsupported checkpoint source for {model_id}: {source}")


def checkpoint_manifest_path(model_id: str, boundary: int) -> Path | None:
    source = checkpoint_source(model_id)
    if not source.startswith("ensemble:"):
        return None
    name = source.split(":", 1)[1]
    return (
        REVIEWS_ROOT
        / "checkpoint-ensembles"
        / name
        / "manifests"
        / f"ck-ch{boundary:03d}.json"
    )


def checkpoint_provenance(model_id: str, boundary: int) -> str:
    source = checkpoint_source(model_id)
    if source == "native":
        return f"ck-ch{boundary:03d}"

    name = source.split(":", 1)[1]
    manifest_path = checkpoint_manifest_path(model_id, boundary)
    if manifest_path is None or not manifest_path.exists():
        return f"ensemble {name} ck-ch{boundary:03d}@missing"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = manifest.get("ensemble_sha256")
    if not digest:
        digest = hashlib.sha256(checkpoint_path(model_id, boundary).read_bytes()).hexdigest()
    return f"ensemble {name} ck-ch{boundary:03d}@{digest[:12]}"


if __name__ == "__main__":  # `tools/cold_read_config.py` — print the live rosters
    print("cold-read panel :", ", ".join(panel_models()))
    print("  fast probe    :", ", ".join(panel_models(fast=True)))
    print("  retired       :", ", ".join(panel_retired()))
    print("capture roster  :", ", ".join(capture_models()))
    print("  retired       :", ", ".join(capture_retired()))
    print("openrouter map  :", ", ".join(f"{k}={v}" for k, v in openrouter_models().items()))
