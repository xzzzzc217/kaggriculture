"""Headers + SHA hints from 2026-08-30 hunt notebooks. No cell exec."""

from __future__ import annotations

import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260830"


def main() -> None:
    for path in sorted(DIR.glob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        print("=" * 60)
        print(path.name, "bytes", len(raw), "cells", len(notebook.get("cells", [])))
        meta = notebook.get("metadata") or {}
        for key, value in meta.items():
            if isinstance(value, dict) and any("sha" in str(k).lower() for k in value):
                print(" meta", key, {k: value[k] for k in value if "sha" in str(k).lower() or k in ("public_name", "engine")})
        for index, cell in enumerate(notebook.get("cells", [])[:6]):
            source = cell.get("source") or ""
            if isinstance(source, list):
                source = "".join(source)
            first = source.strip().splitlines()[:12]
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} chars --")
            for line in first:
                print(line[:220])
        text = raw.decode("utf-8", errors="ignore")
        shas = re.findall(r"[a-f0-9]{64}", text.lower())
        print("hex64 unique", len(set(shas)))
        for s in list(dict.fromkeys(shas))[:8]:
            print(" sha", s)
        if "%%writefile" in text:
            print(" has_writefile")
        if "b85decode" in text or "PAYLOAD" in text:
            print(" has_payload")


if __name__ == "__main__":
    main()
