#!/usr/bin/env python3
"""Portable CLI regression tests using only temporary, fictional brand data."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS))
import audit_article as audit
import init_article as initializer

HEADER = "| " + " | ".join(audit.LEDGER_COLUMNS) + " |\n| " + " | ".join(["---"] * 7) + " |\n"


class PortableSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="livestock-portable-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "brand-one"
        self.cli("setup_brand.py", "--brand-name", '示例品牌: A #1 "研发"',
                 "--main-products", "饲料、设备与服务", expected=0)

    def cli(self, script, *args, expected=0, workspace=None):
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / script), *map(str, args),
                                 "--workspace", str(workspace or self.workspace)],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def init(self, mode="evidence-landscape", slug="test", workspace=None, expected=0):
        return self.cli("init_article.py", "--slug", slug, "--title", '技术判断: 标题 #1 "引号"',
                        "--species", "奶牛", "--life-stage", "泌乳期", "--audience", "技术负责人",
                        "--date", "2026-11-24", "--editorial-mode", mode,
                        workspace=workspace, expected=expected)

    def completed(self):
        self.init()
        run = self.workspace / "work/2026-11-24-test"
        article = self.workspace / "articles/2026-11-24-test.md"
        original = article.read_text(encoding="utf-8")
        frontmatter = original.split("---", 2)[1].replace("status: draft", "status: review")
        article.write_text("---" + frontmatter + "---\n\n# 审计结构样例\n\nC1：此处是虚构的结构测试。\n", encoding="utf-8")
        for name in ("brief.md", "search-log.md", "evidence-matrix.md", "outline.md", "review.md"):
            (run / name).write_text("# 结构测试\n\n人工审核保持开放。\n", encoding="utf-8")
        fields = ["C1：结构测试", "https://example.org/study#results", "external_url",
                  "review-required", "verified", "direct-evidence", "E1；待人工审核"]
        ledger = run / "evidence.md"
        self.write_ledger(ledger, fields)
        return article, ledger, fields

    def write_ledger(self, ledger, fields):
        ledger.write_text(HEADER + "| " + " | ".join(fields) + " |\n", encoding="utf-8")

    def test_preflight_and_all_editorial_modes(self):
        self.cli("preflight.py")
        for mode in initializer.EDITORIAL_MODES:
            with self.subTest(mode=mode):
                self.init(mode, mode)
                run = self.workspace / "work" / ("2026-11-24-" + mode)
                self.assertEqual({x.name for x in run.iterdir()},
                                 {"brand.json", "brief.md", "search-log.md", "evidence-matrix.md", "evidence.md", "outline.md", "review.md"})
                article = self.workspace / "articles" / (run.name + ".md")
                meta = audit.parse_frontmatter(article.read_text(encoding="utf-8"))
                self.assertEqual(meta["brand_name"], '示例品牌: A #1 "研发"')
                self.assertIn(meta["brand_name"], (run / "brief.md").read_text(encoding="utf-8"))
                self.cli("audit_article.py", article, run / "evidence.md", expected=1)

    def test_independent_relocated_package(self):
        copied = self.root / "relocated skill"
        shutil.copytree(SKILL_DIR, copied, ignore=shutil.ignore_patterns("__pycache__"))
        for name, args in (("preflight.py", []), ("init_article.py", ["--slug", "portable", "--title", "设备技术解释", "--species", "家禽", "--life-stage", "育成", "--audience", "场长"])):
            result = subprocess.run([sys.executable, "-B", str(copied / "scripts" / name), *args,
                                     "--workspace", str(self.workspace)], cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_default_workspace_and_two_brands(self):
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "setup_brand.py"),
                                 "--brand-name", "另一虚构品牌", "--main-products", "育种服务"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        second = self.root / "livestock-writing"
        self.init(workspace=second)
        meta = audit.parse_frontmatter((second / "articles/2026-11-24-test.md").read_text(encoding="utf-8"))
        self.assertEqual(meta["brand_name"], "另一虚构品牌")
        self.assertEqual(meta["main_products"], "育种服务")

    def test_overwrite_and_invalid_inputs(self):
        before = (self.workspace / "brand.json").read_bytes()
        self.cli("setup_brand.py", "--brand-name", "替换", "--main-products", "替换", expected=1)
        self.assertEqual(before, (self.workspace / "brand.json").read_bytes())
        self.init()
        self.init(expected=1)
        for slug in ("../escape", "bad/slug", "bad\\slug", "bad\u2028slug"):
            self.init(slug=slug, expected=2)
        self.cli("setup_brand.py", "--brand-name", "bad\nname", "--main-products", "饲料", expected=2)
        self.init(mode="unknown", expected=2)

    def test_missing_config_and_redirected_outputs(self):
        (self.workspace / "brand.json").unlink()
        self.cli("preflight.py", expected=1)
        self.init(expected=1)
        outside = self.root / "outside"
        outside.mkdir()
        shutil.rmtree(self.workspace / "work")
        (self.workspace / "work").symlink_to(outside, target_is_directory=True)
        self.cli("setup_brand.py", "--brand-name", "样例", "--main-products", "设备", expected=1)
        self.assertEqual(list(outside.iterdir()), [])

    def test_audit_complete_and_failures(self):
        article, ledger, fields = self.completed()
        self.cli("audit_article.py", article, ledger)
        original = article.read_text(encoding="utf-8")
        for old, new in (("status: review", "status: draft"), ("workflow_version:", "wrong_version:"),
                         ('brand_name:', 'wrong_brand:'), ("editorial_mode: evidence-landscape", "editorial_mode: unknown")):
            article.write_text(original.replace(old, new), encoding="utf-8")
            self.cli("audit_article.py", article, ledger, expected=1)
        article.write_text(original, encoding="utf-8")
        for index, value in ((2, "wiki_page"), (3, "public-safe"), (3, "do-not-use"),
                             (4, "unverified"), (5, "unsupported"), (1, "not-a-url"),
                             (1, "https://user:pass@example.org/study"),
                             (1, "https://example.org:70000/study")):
            altered = fields.copy()
            altered[index] = value
            self.write_ledger(ledger, altered)
            self.cli("audit_article.py", article, ledger, expected=1)
        self.write_ledger(ledger, fields)
        companion = ledger.parent / "search-log.md"
        companion.write_text("TODO", encoding="utf-8")
        self.cli("audit_article.py", article, ledger, expected=1)
        companion.unlink()
        self.cli("audit_article.py", article, ledger, expected=1)
        companion.symlink_to(article)
        self.cli("audit_article.py", article, ledger, expected=1)

    def test_local_evidence_and_brand_snapshot(self):
        article, ledger, fields = self.completed()
        source = self.root / "provided.md"
        source.write_text("# 方法\n虚构资料，仅用于结构测试。", encoding="utf-8")
        fields[1:3] = ["../provided.md#方法", "user_document"]
        self.write_ledger(ledger, fields)
        self.cli("audit_article.py", article, ledger)
        source.unlink()
        self.cli("audit_article.py", article, ledger, expected=1)
        self.write_ledger(ledger, [fields[0], "https://example.org/study", "external_url", *fields[3:]])
        snapshot = ledger.parent / "brand.json"
        brand = json.loads(snapshot.read_text(encoding="utf-8"))
        brand["brand_name"] = "其他品牌"
        snapshot.write_text(json.dumps(brand), encoding="utf-8")
        self.cli("audit_article.py", article, ledger, expected=1)

    def test_wrong_package_and_path_binding(self):
        article, ledger, fields = self.completed()
        original = article.read_text(encoding="utf-8")
        article.write_text(original.replace("work/2026-11-24-test/search-log.md", "work/other/search-log.md"), encoding="utf-8")
        self.cli("audit_article.py", article, ledger, expected=1)
        article.write_text(original, encoding="utf-8")
        outside = self.root / article.name
        shutil.copyfile(article, outside)
        self.cli("audit_article.py", outside, ledger, expected=1)
        redirected = self.root / "redirected-ledger.md"
        redirected.symlink_to(ledger)
        self.cli("audit_article.py", article, redirected, expected=1)
        broken = {"schema_version": 1, "brand_name": "", "main_products": "饲料"}
        (self.workspace / "brand.json").write_text(json.dumps(broken), encoding="utf-8")
        self.cli("preflight.py", expected=1)

    def test_write_failure_cleans_up_for_retry(self):
        original = initializer.write_new
        def failing(path, text, created):
            original(path, text, created)
            if path.name == "outline.md":
                raise OSError("simulated write failure")
        initializer.write_new = failing
        try:
            with self.assertRaises(OSError):
                initializer.create_package(self.workspace, "2026-11-24", "retry", "标题", "水产", "养成", "技术员")
        finally:
            initializer.write_new = original
        self.assertFalse((self.workspace / "work/2026-11-24-retry").exists())
        self.assertFalse((self.workspace / "articles/2026-11-24-retry.md").exists())
        self.init(slug="retry")

    def test_strict_metadata_and_canonical_table(self):
        for text in ('---\ntitle: "bad\\nvalue"\n---', '---\ntitle: a\ntitle: b\n---',
                     '---\ntitle: a: b\n---', '---\ntitle: |\n  bad\n---'):
            with self.assertRaises(ValueError):
                audit.parse_frontmatter(text)
        for ledger_text in ("| a | b |\n", HEADER + HEADER,
                            HEADER + "| incomplete | row |\n"):
            rows, failures = audit.rows_from_ledger(ledger_text)
            self.assertTrue(failures or any(len(fields) != 7 for _, fields in rows))


if __name__ == "__main__":
    unittest.main(verbosity=2)
