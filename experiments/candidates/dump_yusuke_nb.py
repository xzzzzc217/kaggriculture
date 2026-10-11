"""Dump Yusuke ShopForge notebook cells. No cell exec."""

from __future__ import annotations

import json
from pathlib import Path

P = Path("artifacts/public_sources/_hunt_20260830b/public-match-history-router-rating-2929-aug-30.ipynb")


def main() -> None:
    nb = json.loads(P.read_text(encoding="utf-8"))
    print("cells", len(nb.get("cells", [])), "bytes", P.stat().st_size)
    for i, c in enumerate(nb.get("cells", [])):
        src = c.get("source") or ""
        if isinstance(src, list):
            src = "".join(src)
        print("=" * 70)
        print(f"CELL {i} {c.get('cell_type')} len={len(src)}")
        lines = src.strip().splitlines()
        show = lines if len(lines) <= 80 else lines[:50] + [f"... {len(lines) - 60} more ..."] + lines[-10:]
        for line in show:
            print(line[:220])


if __name__ == "__main__":
    main()
