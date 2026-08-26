"""Print notebook cell headers without executing notebook code."""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260824b"


def main() -> None:
    for path in sorted(DIR.glob("*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        print("=" * 60)
        print(path.name, "cells", len(notebook.get("cells", [])))
        for index, cell in enumerate(notebook.get("cells", [])):
            source = cell.get("source") or ""
            if isinstance(source, list):
                source = "".join(source)
            first = source.strip().splitlines()[:10]
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} chars --")
            for line in first:
                print(line[:220])


if __name__ == "__main__":
    main()
