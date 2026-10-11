"""Headers from 2026-09-10 gate hunt notebooks. No cell exec."""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910_gate"
KEYS = [
    "%%writefile",
    "writefile",
    "agent.so",
    "ctypes",
    "CDLL",
    ".so",
    "reselect",
    "DECISIONS",
    "ROUTES",
    "later",
    "216",
    "226",
    "360",
    "433",
    "144",
    "648",
    "BALANCED",
    "BUY_ANIMAL",
    "def agent",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        low = text.lower()
        notebook = json.loads(raw.decode("utf-8"))
        cells = notebook.get("cells", [])
        flags = [key for key in KEYS if key.lower() in low]
        print("=" * 70)
        print(path.parent.name, "bytes", len(raw), "cells", len(cells))
        print("FLAGS", flags)
        for index, cell in enumerate(cells[:8]):
            source = cell_source(cell)
            first = source.strip().splitlines()[:8]
            if not first:
                continue
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
            for line in first:
                print(line[:200])


if __name__ == "__main__":
    main()
