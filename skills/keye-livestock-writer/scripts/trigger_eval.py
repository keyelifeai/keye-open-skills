#!/usr/bin/env python3
"""Run a lightweight routing-contract regression for the skill description."""
from __future__ import annotations

import json
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_DIR / "SKILL.md"
CASES_PATH = SKILL_DIR / "evals" / "trigger-cases.json"

WRITING_ACTIONS = (
    "写一篇", "撰写", "起草", "列一个", "提纲", "改写", "改得", "修改", "润色", "审计", "复核", "核对每项主张",
    "write", "draft", "outline", "revise", "audit",
)
DOMAIN_TERMS = (
    "猪", "母猪", "仔猪", "家禽", "鸡", "蛋鸡", "肉鸡", "水产", "鱼", "虾", "牛", "犊牛", "反刍", "畜牧", "养殖",
    "羊", "育种", "养殖设备", "动物营养", "饲料", "微量元素", "livestock", "swine", "poultry", "aquaculture", "ruminant", "animal nutrition",
)
EXCLUDED_TASK_TERMS = (
    "兽医诊断", "诊断与用药", "用药方案", "配方计算", "广告文案", "促销文案", "宣传口号", "食谱", "菜谱",
    "veterinary diagnosis", "formula calculation", "advertising copy", "recipe",
)
REQUIRED_DESCRIPTION_GROUPS = (
    ("撰写", "writing"),
    ("畜牧", "livestock"),
    ("动物营养", "animal-nutrition"),
    ("证据景观", "evidence synthesis"),
    ("证据台账", "evidence audit"),
    ("兽医诊断", "veterinary diagnosis"),
    ("发布", "publishing"),
)


def description_from_skill(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if match is None:
        raise ValueError("SKILL.md frontmatter is missing")
    lines = match.group(1).splitlines()
    for index, line in enumerate(lines):
        if line == "description: |":
            values = []
            for following in lines[index + 1:]:
                if not following.startswith("  "):
                    break
                values.append(following.strip())
            if values:
                return " ".join(values)
    raise ValueError("description must use a non-empty block scalar")


def proxy_route(prompt: str) -> bool:
    normalized = prompt.casefold()
    if any(term in normalized for term in EXCLUDED_TASK_TERMS):
        return False
    return any(term in normalized for term in WRITING_ACTIONS) and any(term in normalized for term in DOMAIN_TERMS)


def load_cases() -> list[dict]:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("trigger cases must use schema_version 1")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("trigger cases must be a non-empty list")
    return cases


def main() -> int:
    failures = []
    try:
        description = description_from_skill(SKILL_MD.read_text(encoding="utf-8")).casefold()
        cases = load_cases()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"TRIGGER EVAL FAIL: {exc}")
        return 1

    for group in REQUIRED_DESCRIPTION_GROUPS:
        if not any(term in description for term in group):
            failures.append("description missing route concept: " + " / ".join(group))
    seen_ids = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {"id", "prompt", "expected_route"}:
            failures.append(f"invalid trigger case shape: {case}")
            continue
        case_id = case["id"]
        prompt = case["prompt"]
        expected = case["expected_route"]
        if not isinstance(case_id, str) or not case_id or case_id in seen_ids:
            failures.append(f"invalid or duplicate trigger case id: {case_id}")
            continue
        seen_ids.add(case_id)
        if not isinstance(prompt, str) or not prompt or not isinstance(expected, bool):
            failures.append(f"invalid trigger case values: {case_id}")
            continue
        observed = proxy_route(prompt)
        if observed != expected:
            failures.append(f"{case_id}: expected route={expected}, observed route={observed}")
    if failures:
        print("TRIGGER EVAL FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    positives = sum(bool(case["expected_route"]) for case in cases)
    print(f"TRIGGER EVAL PASS: cases={len(cases)} positive={positives} negative={len(cases) - positives}")
    print("This is a deterministic routing proxy, not a live Codex router measurement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
