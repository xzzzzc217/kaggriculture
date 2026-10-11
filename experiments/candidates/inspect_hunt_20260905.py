"""Headers from 2026-09-05 hunt notebooks. No cell exec."""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260905"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        print("=" * 70)
        print(path.relative_to(DIR), "bytes", len(raw), "cells", len(notebook.get("cells", [])))
        text = raw.decode("utf-8", errors="ignore")
        print(
            "writefile",
            "%%writefile" in text,
            "agent.so",
            "agent.so" in text,
            "9c9s",
            "9c9s" in text.lower(),
            "reselect",
            "reselect" in text.lower(),
        )
        for index, cell in enumerate(notebook.get("cells", [])[:5]):
            source = cell_source(cell)
            first = source.strip().splitlines()[:8]
            if not first:
                continue
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
            for line in first:
                print(line[:200])


if __name__ == "__main__":
    main()
