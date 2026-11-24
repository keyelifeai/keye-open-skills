"""Portable brand configuration and output-boundary helpers (standard library only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE = Path("livestock-writing")


def single_line_text(value: str) -> str:
    if not value.strip() or any(not char.isprintable() for char in value):
        raise argparse.ArgumentTypeError("value must be non-empty printable single-line text")
    return value


def load_brand(path: Path) -> dict:
    if path.is_symlink():
        raise ValueError("brand config must not be a symlink")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema_version", "brand_name", "main_products"}:
        raise ValueError("brand config requires schema_version, brand_name and main_products only")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("unsupported brand schema_version")
    for key in ("brand_name", "main_products"):
        if not isinstance(data[key], str):
            raise ValueError(f"brand config {key} must be text")
        try:
            single_line_text(data[key])
        except argparse.ArgumentTypeError as exc:
            raise ValueError(f"brand config {key}: {exc}") from exc
    return data


def workspace_path(workspace: Path) -> Path:
    if workspace.is_symlink():
        raise ValueError("workspace must not be a symlink")
    resolved = workspace.resolve()
    if resolved == SKILL_DIR or SKILL_DIR in resolved.parents:
        raise ValueError("workspace must be outside the installed skill")
    return resolved


def workspace_errors(workspace: Path) -> list[str]:
    failures = []
    if not workspace.is_dir() or workspace.is_symlink():
        return ["workspace must be a real directory"]
    for name in ("work", "articles"):
        path = workspace / name
        if not path.is_dir() or path.is_symlink():
            failures.append(f"workspace {name}/ must be a real directory")
    return failures
