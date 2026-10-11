"""Print hunt notebook cell headers and SHA. No cell exec."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260914k"
NEEDLES = [
    "%%writefile",
    "agent.so",
    "ctypes",
    "CDLL",
    "reselect",
    "ROUTE_STEP",
    "FINAL_PLAN",
    "sale_horizon",
    "ADVANCE_START",
    "PROGRAM",
    "DECISIONS",
    "PufferLib",
    "BUY_ANIMAL",
    "main.py",
    "def agent",
    "kaggle_environments",
]


def main() -> None:
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        text = raw.decode("utf-8", errors="ignore")
        print("=" * 60)
        print(
            path.relative_to(DIR).as_posix(),
            "bytes",
            len(raw),
            "sha256",
            hashlib.sha256(raw).hexdigest(),
            "cells",
            len(notebook.get("cells") or []),
        )
        print("needles", [n for n in NEEDLES if n in text])
        for index, cell in enumerate(notebook.get("cells") or []):
            src = cell.get("source") or ""
            if isinstance(src, list):
                src = "".join(src)
            first = " | ".join(src.strip().splitlines()[:2])[:180]
            print(f"  c{index} {cell.get('cell_type')} {len(src)} {first}")


if __name__ == "__main__":
    main()
