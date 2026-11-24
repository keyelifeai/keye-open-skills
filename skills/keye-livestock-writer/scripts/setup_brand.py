#!/usr/bin/env python3
"""Create brand.json and output directories locally, without overwriting existing configuration."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from common import DEFAULT_WORKSPACE, single_line_text, workspace_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brand-name", required=True, type=single_line_text)
    parser.add_argument("--main-products", required=True, type=single_line_text)
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    args = parser.parse_args()
    created = []
    brand_written = False
    try:
        workspace = workspace_path(args.workspace)
        config = workspace / "brand.json"
        if config.exists() or config.is_symlink():
            raise FileExistsError("refusing overwrite: brand.json; reuse this workspace or choose another")
        for directory in (workspace, workspace / "work", workspace / "articles"):
            if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
                raise ValueError(f"output must be a real directory: {directory}")
        # Prepare directories before committing the brand configuration.
        for directory in (workspace, workspace / "work", workspace / "articles"):
            if not directory.exists():
                directory.mkdir(parents=True)
                created.append(directory)
        brand = {"schema_version": 1, "brand_name": args.brand_name, "main_products": args.main_products}
        with config.open("x", encoding="utf-8") as handle:
            brand_written = True
            handle.write(json.dumps(brand, ensure_ascii=False, indent=2) + "\n")
    except (OSError, ValueError) as exc:
        if brand_written:
            config.unlink()
        for directory in reversed(created):
            directory.rmdir()
        print(f"SETUP FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"SETUP PASS: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
