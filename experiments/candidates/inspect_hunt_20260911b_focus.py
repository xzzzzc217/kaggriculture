"""Readable source slices from 20260911b hunt. No cell exec, no payload decode."""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260911b"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def dump_nb(rel: str) -> None:
    path = DIR / rel
    print("=" * 70)
    print(rel, path.stat().st_size)
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells") or []
    print("n_cells", len(cells))
    for i, cell in enumerate(cells):
        src = cell_source(cell)
        print(f"-- cell {i} {cell.get('cell_type')} {len(src)} --")
        lines = src.splitlines()
        if cell.get("cell_type") == "markdown":
            for line in lines[:18]:
                print(line[:200])
            continue
        if src.lstrip().startswith("%%writefile"):
            # skip long b85/gzip payload lines
            shown = 0
            for line in lines:
                if len(line) > 240 and any(k in line for k in ("b85decode", "b64", "zlib", "lzma", "_DATA", "_INLINE")):
                    print(line[:120] + " ...[payload truncated]...")
                    continue
                print(line[:220])
                shown += 1
                if shown > 80:
                    print("...[truncated writefile]...")
                    break
            continue
        for line in lines[:40]:
            print(line[:220])
        if len(lines) > 40:
            print(f"...[{len(lines)-40} more lines]...")


def main() -> None:
    dump_nb("yhay81__shop-router-0911-simple/shop-router-0911-simple.ipynb")
    dump_nb("lucifer19__harvest-nocturne-v2-a-lighter-start/harvest-nocturne-v2-a-lighter-start.ipynb")
    dump_nb("xuantianfengwu__kaggriculture-preempt-selector/kaggriculture-preempt-selector.ipynb")
    dump_nb("leoprovorov__two-coins-at-high-noon-small-improvement/two-coins-at-high-noon-small-improvement.ipynb")
    py = DIR / "ziyiming__kaggriculture-medal-r2-shoprouter/kaggriculture-medal-r2-shoprouter.py"
    print("=" * 70)
    print("ziyiming leftover", py.stat().st_size)
    text = py.read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(text.splitlines()[:80], 1):
        if len(line) > 240:
            print(f"{i}: {line[:120]} ...[payload]...")
        else:
            print(f"{i}: {line}")


if __name__ == "__main__":
    main()
