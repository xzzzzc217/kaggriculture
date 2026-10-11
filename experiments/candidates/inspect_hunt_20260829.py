"""Headers + SHA hints from today's hunt notebooks. No cell exec."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260829"


def main() -> None:
    for path in sorted(DIR.glob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        print("=" * 60)
        print(path.name, "bytes", len(raw), "cells", len(notebook.get("cells", [])))
        meta = notebook.get("metadata") or {}
        print("meta_keys", list(meta.keys())[:20])
        for key, value in meta.items():
            if isinstance(value, dict) and any("sha" in str(k).lower() for k in value):
                print(" ", key, {k: value[k] for k in value if "sha" in str(k).lower() or k in ("public_name", "engine")})
        for index, cell in enumerate(notebook.get("cells", [])[:8]):
            source = cell.get("source") or ""
            if isinstance(source, list):
                source = "".join(source)
            first = source.strip().splitlines()[:8]
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} chars --")
            for line in first:
                print(line[:200])
        text = raw.decode("utf-8", errors="ignore")
        shas = re.findall(r"[a-f0-9]{64}", text.lower())
        print("hex64_count", len(shas), "unique", len(set(shas)))
        for s in list(dict.fromkeys(shas))[:6]:
            print(" sha", s)


if __name__ == "__main__":
    main()
