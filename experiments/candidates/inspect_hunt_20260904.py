"""Headers from 2026-09-04 hunt notebooks. No cell exec."""

from __future__ import annotations

import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260904"


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
            "b85",
            "b85decode" in text,
            "PAYLOAD",
            "PAYLOAD" in text,
            "agent.so",
            "agent.so" in text,
            "reselect",
            "reselect" in text.lower(),
            "8c9s",
            "8c9s" in text.lower(),
        )
        shas = re.findall(r"[a-f0-9]{64}", text.lower())
        for digest in list(dict.fromkeys(shas))[:6]:
            print(" sha", digest)
        for index, cell in enumerate(notebook.get("cells", [])[:6]):
            source = cell_source(cell)
            first = source.strip().splitlines()[:10]
            if not first:
                continue
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
            for line in first:
                print(line[:220])


if __name__ == "__main__":
    main()
