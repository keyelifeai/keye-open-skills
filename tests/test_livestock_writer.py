"""Run the portable writer regressions with fictional temporary data in CI."""
from pathlib import Path
import subprocess
import sys
import unittest


class LivestockWriterTests(unittest.TestCase):
    def test_portable_scripts(self):
        root = Path(__file__).resolve().parents[1]
        for script in ("test_skill.py", "trigger_eval.py"):
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, "-B", str(root / "skills/keye-livestock-writer/scripts" / script)],
                    cwd=root, text=True, capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
