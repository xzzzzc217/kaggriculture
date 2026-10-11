"""Print payload hints from 2026-08-27 hunt notebooks. Never executes cells."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUNT = ROOT / "artifacts/public_sources/_hunt_20260827"
HINTS = (
    "BLOB",
    "PAYLOAD",
    "SOURCE_B85",
    "SOURCE",
    "%%writefile",
    "EXPECTED",
    "def agent",
    "b85decode",
    "b64decode",
    "zlib.decompress",
    "main.py",
    "SHA",
    "sha256",
)


def cell_text(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def scan_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    print("=" * 72)
    print(path.parent.name, "/", path.name, "cells", len(notebook.get("cells", [])))
    for index, cell in enumerate(notebook.get("cells", [])):
        source = cell_text(cell)
        first = source.strip().splitlines()[:12]
        hits = [h for h in HINTS if h in source]
        if not hits and cell.get("cell_type") != "code":
            continue
        if not hits and index > 2:
            continue
        print(f"-- cell {index} {cell.get('cell_type')} {len(source)} chars hits={hits} --")
        for line in first:
            print(line[:240])


def scan_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    print("=" * 72)
    print(path.parent.name, "/", path.name, "bytes", path.stat().st_size)
    hits = [h for h in HINTS if h in text]
    print("hits", hits)
    print("\n".join(text.splitlines()[:25])[:2000])


def main() -> None:
    for path in sorted(HUNT.rglob("*")):
        if path.suffix == ".ipynb":
            scan_notebook(path)
        elif path.suffix == ".py":
            scan_py(path)


if __name__ == "__main__":
    main()
