"""Inspect Yusuke 2929 and related notebooks. No cell exec."""

from __future__ import annotations

import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260830b"


def main() -> None:
    for path in sorted(DIR.glob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        print("=" * 70)
        print(path.name, "bytes", len(raw), "cells", len(notebook.get("cells", [])))
        for index, cell in enumerate(notebook.get("cells", [])[:10]):
            source = cell.get("source") or ""
            if isinstance(source, list):
                source = "".join(source)
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
            for line in source.strip().splitlines()[:18]:
                print(line[:240])
        text = raw.decode("utf-8", errors="ignore")
        print("writefile", "%%writefile" in text, "b85", "b85decode" in text, "PAYLOAD", "PAYLOAD" in text)
        shas = re.findall(r"[a-f0-9]{64}", text.lower())
        for s in list(dict.fromkeys(shas))[:8]:
            print(" sha", s)


if __name__ == "__main__":
    main()
