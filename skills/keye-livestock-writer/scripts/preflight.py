#!/usr/bin/env python3
"""Read-only checks for the installed portable package and a user-selected brand workspace."""
from __future__ import annotations

import argparse
from pathlib import Path
from common import DEFAULT_WORKSPACE, SKILL_DIR, load_brand, workspace_errors, workspace_path

REQUIRED_FILES = (
    "SKILL.md", "README.md", "LICENSE", "agents/openai.yaml",
    "assets/article-brief-template.md", "assets/evidence-ledger-template.md",
    "assets/evidence-matrix-template.md", "assets/outline-template.md",
    "assets/review-checklist.md", "assets/search-log-template.md",
    "references/workflow.md", "references/writing-model.md",
    "references/evidence-and-brand-policy.md", "references/evidence-landscape.md",
    "scripts/common.py", "scripts/setup_brand.py", "scripts/init_article.py",
    "scripts/audit_article.py", "scripts/preflight.py", "scripts/test_skill.py",
    "scripts/trigger_eval.py", "evals/trigger-cases.json",
)


def package_errors() -> list[str]:
    return [f"missing or symlinked package file: {name}" for name in REQUIRED_FILES
            if not (SKILL_DIR / name).is_file() or (SKILL_DIR / name).is_symlink()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    args = parser.parse_args()
    failures = package_errors()
    try:
        workspace = workspace_path(args.workspace)
        failures.extend(workspace_errors(workspace))
        load_brand(workspace / "brand.json")
    except (OSError, ValueError) as exc:
        failures.append(str(exc))
    if failures:
        print("PREFLIGHT FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("PREFLIGHT PASS: portable package and brand workspace; no private sources required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
