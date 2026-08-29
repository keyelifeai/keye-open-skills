#!/usr/bin/env python3
"""Run repository-specific publication checks for Keye's public Skills."""

from __future__ import annotations

import py_compile
import re
import sys
import tempfile
from pathlib import Path


EXPECTED_SKILLS = {
    "keye-network-optimizer",
    "keye-viral-dissect",
    "storm-deepresearch",
}
ALLOWED_FRONTMATTER_FIELDS = {
    "allowed-tools",
    "compatibility",
    "description",
    "license",
    "metadata",
    "name",
}
BLOCKED_ARTIFACTS = {
    "skills/content-creation/article-generation.md",
    "skills/development/code-review.md",
}
PROHIBITED_CLAIMS = {
    "30+": "unverified catalog size",
    "平均质量评分": "unverified average rating",
    "全部验证": "unverified validation claim",
    "5 分钟完成博士级": "unverified outcome claim",
    "40-60 小时": "unverified time-saving claim",
}
SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(skill_file: Path) -> tuple[dict[str, str], str]:
    content = skill_file.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("must start with YAML frontmatter")
    parts = content.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("frontmatter is not closed")

    frontmatter = parts[1]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key] = value.strip()
    return fields, frontmatter


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    try:
        fields, frontmatter = parse_frontmatter(skill_file)
    except ValueError as exc:
        return [f"{skill_file}: {exc}"]

    unexpected = set(fields) - ALLOWED_FRONTMATTER_FIELDS
    if unexpected:
        errors.append(f"{skill_file}: unexpected frontmatter fields {sorted(unexpected)}")
    if fields.get("name") != skill_dir.name:
        errors.append(f"{skill_file}: name must match directory")
    if not fields.get("description"):
        errors.append(f"{skill_file}: description is required")
    if fields.get("license") != "MIT":
        errors.append(f"{skill_file}: license must be MIT")
    if not re.search(r'^\s{2}version:\s*["\']?\d+\.\d+\.\d+["\']?\s*$', frontmatter, re.MULTILINE):
        errors.append(f"{skill_file}: metadata.version must be a semantic version string")
    if len(skill_file.read_text(encoding="utf-8").splitlines()) >= 500:
        errors.append(f"{skill_file}: keep SKILL.md under 500 lines")

    for target in MARKDOWN_LINK.findall(skill_file.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#")):
            continue
        normalized = target.split("#", 1)[0]
        if normalized and not (skill_dir / normalized).exists():
            errors.append(f"{skill_file}: missing referenced path {normalized}")

    with tempfile.TemporaryDirectory(prefix="keye-skill-bytecode-") as temp_dir:
        for index, python_file in enumerate(skill_dir.rglob("*.py")):
            try:
                py_compile.compile(
                    python_file,
                    cfile=str(Path(temp_dir) / f"{index}.pyc"),
                    doraise=True,
                )
            except py_compile.PyCompileError as exc:
                errors.append(f"{python_file}: {exc.msg}")
    return errors


def validate_repository(repository_root: Path) -> list[str]:
    errors: list[str] = []
    skill_dirs = {
        skill_file.parent.name: skill_file.parent
        for skill_file in (repository_root / "skills").glob("*/SKILL.md")
    }
    if set(skill_dirs) != EXPECTED_SKILLS:
        errors.append(
            "public Skill directories must be exactly "
            f"{sorted(EXPECTED_SKILLS)}, got {sorted(skill_dirs)}"
        )

    for relative_path in BLOCKED_ARTIFACTS:
        if (repository_root / relative_path).exists():
            errors.append(f"provenance-blocked artifact remains: {relative_path}")

    names: list[str] = []
    for skill_dir in skill_dirs.values():
        errors.extend(validate_skill(skill_dir))
        fields, _ = parse_frontmatter(skill_dir / "SKILL.md")
        names.append(fields.get("name", ""))
    if len(names) != len(set(names)):
        errors.append("Skill names must be unique")

    scan_paths = [
        repository_root / "README.md",
        repository_root / "CONTRIBUTING.md",
        repository_root / "skills",
    ]
    text_files: list[Path] = []
    for scan_path in scan_paths:
        if scan_path.is_file():
            text_files.append(scan_path)
        elif scan_path.exists():
            text_files.extend(
                path
                for path in scan_path.rglob("*")
                if path.is_file() and path.suffix.lower() in {".json", ".md", ".py", ".yaml", ".yml"}
            )

    for text_file in text_files:
        text = text_file.read_text(encoding="utf-8")
        relative_path = text_file.relative_to(repository_root)
        if "/Users/" in text or re.search(r"[A-Za-z]:\\Users\\", text):
            errors.append(f"{relative_path}: personal absolute path")
        for claim, reason in PROHIBITED_CLAIMS.items():
            if claim in text:
                errors.append(f"{relative_path}: {reason}: {claim}")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative_path}: suspected {label}")

    license_text = (repository_root / "LICENSE").read_text(encoding="utf-8")
    if not license_text.startswith("MIT License\n"):
        errors.append("LICENSE must contain the repository MIT license")
    return errors


def main() -> int:
    repository_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate_repository(repository_root)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Repository validation passed for {len(EXPECTED_SKILLS)} Skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
