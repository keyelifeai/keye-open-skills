#!/usr/bin/env python3
"""Create a non-overwriting livestock article package from the bundled templates."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from common import SKILL_DIR, DEFAULT_WORKSPACE, load_brand, single_line_text, workspace_errors, workspace_path
from preflight import package_errors


ASSETS_DIR = SKILL_DIR / "assets"
EDITORIAL_MODES = ("evidence-landscape", "study-in-context", "technical-explainer")


def valid_slug(value: str) -> str:
    if not value or value in {".", ".."} or len(value) > 80:
        raise argparse.ArgumentTypeError("slug must be 1 to 80 characters and not a dot name")
    if "/" in value or "\\" in value or any(not char.isprintable() for char in value):
        raise argparse.ArgumentTypeError("slug must not contain separators or control characters")
    return value


def parse_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def render_asset(name: str, replacements: dict[str, str]) -> str:
    text = (ASSETS_DIR / name).read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def pre_render_outputs(
    run_name: str,
    title: str,
    species: str,
    life_stage: str,
    audience: str,
    date: str,
    brand: dict,
    editorial_mode: str = "evidence-landscape",
) -> tuple[dict[str, str], str]:
    values = {
        "BRAND_NAME": brand["brand_name"],
        "MAIN_PRODUCTS": brand["main_products"],
        "TITLE": title,
        "SPECIES": species,
        "LIFE_STAGE": life_stage,
        "AUDIENCE": audience,
        "EDITORIAL_MODE": editorial_mode,
    }
    work_files = {
        "brand.json": json.dumps(brand, ensure_ascii=False, indent=2) + "\n",
        "brief.md": render_asset("article-brief-template.md", values),
        "search-log.md": render_asset("search-log-template.md", values),
        "evidence-matrix.md": render_asset("evidence-matrix-template.md", values),
        "evidence.md": render_asset("evidence-ledger-template.md", values),
        "outline.md": render_asset("outline-template.md", values),
        "review.md": render_asset("review-checklist.md", values),
    }
    evidence_ledger = f"work/{run_name}/evidence.md"
    evidence_matrix = f"work/{run_name}/evidence-matrix.md"
    search_log = f"work/{run_name}/search-log.md"
    article = "\n".join([
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {date}",
        f"species: {json.dumps(species, ensure_ascii=False)}",
        f"life_stage: {json.dumps(life_stage, ensure_ascii=False)}",
        f"audience: {json.dumps(audience, ensure_ascii=False)}",
        'workflow_version: "public-1"',
        f"brand_name: {json.dumps(brand['brand_name'], ensure_ascii=False)}",
        f"main_products: {json.dumps(brand['main_products'], ensure_ascii=False)}",
        f"editorial_mode: {editorial_mode}",
        "status: draft",
        f"evidence_ledger: {json.dumps(evidence_ledger, ensure_ascii=False)}",
        f"evidence_matrix: {json.dumps(evidence_matrix, ensure_ascii=False)}",
        f"search_log: {json.dumps(search_log, ensure_ascii=False)}",
        "---",
        "",
        "# 待填写标题",
        "",
        "TODO：完成 brief、证据台账和提纲后再起草正文。",
        "",
    ])
    return work_files, article


def write_new(path: Path, text: str, created_files: list[Path]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        created_files.append(path)
        handle.write(text)


def create_package(
    workspace: Path,
    date: str,
    slug: str,
    title: str,
    species: str,
    life_stage: str,
    audience: str,
    editorial_mode: str = "evidence-landscape",
) -> Path:
    workspace = workspace_path(workspace)
    failures = package_errors() + workspace_errors(workspace)
    if failures:
        raise ValueError("; ".join(failures))
    brand = load_brand(workspace / "brand.json")
    work_root = workspace / "work"
    articles_root = workspace / "articles"
    run_name = f"{date}-{slug}"
    run_dir = work_root / run_name
    article_path = articles_root / f"{run_name}.md"
    if any(path.exists() or path.is_symlink() for path in (run_dir, article_path)):
        raise FileExistsError("refusing overwrite: " + ", ".join(str(path) for path in (run_dir, article_path) if path.exists() or path.is_symlink()))

    work_files, article = pre_render_outputs(run_name, title, species, life_stage, audience, date, brand, editorial_mode)
    created_files: list[Path] = []
    created_run_dir = False
    try:
        run_dir.mkdir()
        created_run_dir = True
        for name, text in work_files.items():
            write_new(run_dir / name, text, created_files)
        write_new(article_path, article, created_files)
    except OSError:
        for path in reversed(created_files):
            if path.exists() or path.is_symlink():
                path.unlink()
        if created_run_dir:
            try:
                run_dir.rmdir()
            except OSError:
                pass
        raise
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, type=valid_slug)
    parser.add_argument("--title", required=True, type=single_line_text)
    parser.add_argument("--species", required=True, type=single_line_text)
    parser.add_argument("--life-stage", required=True, type=single_line_text)
    parser.add_argument("--audience", required=True, type=single_line_text)
    parser.add_argument("--editorial-mode", choices=EDITORIAL_MODES, default="evidence-landscape")
    parser.add_argument("--date", type=parse_date, default=dt.date.today().isoformat())
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    args = parser.parse_args()
    for field in ("title", "species", "life_stage", "audience"):
        if not getattr(args, field).strip():
            parser.error(f"--{field.replace('_', '-')} must not be empty")
    try:
        run_dir = create_package(
            args.workspace,
            args.date,
            args.slug,
            args.title,
            args.species,
            args.life_stage,
            args.audience,
            args.editorial_mode,
        )
    except (OSError, ValueError) as exc:
        print(f"INIT FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"INIT PASS: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
