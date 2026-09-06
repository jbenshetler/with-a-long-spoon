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


def reader_settings(model_id: str) -> dict[str, Any]:
    readers = load_config().get("readers", {})
    direct = readers.get(model_id)
    if direct is not None:
        return dict(direct)
    for settings in readers.values():
        if settings.get("provider_model") == model_id:
            return dict(settings)
    return {}


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
