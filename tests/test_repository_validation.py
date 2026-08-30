from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
    def test_repository_passes_publication_checks(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/validate_repository.py", str(REPOSITORY_ROOT)],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_repository_validation_does_not_write_skill_caches(self) -> None:
        subprocess.run(
            ["python3", "scripts/validate_repository.py", str(REPOSITORY_ROOT)],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            check=True,
            text=True,
        )

        cache_directories = list((REPOSITORY_ROOT / "skills").rglob("__pycache__"))
        self.assertEqual(cache_directories, [])


if __name__ == "__main__":
    unittest.main()
