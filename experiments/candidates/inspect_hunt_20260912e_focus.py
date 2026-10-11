"""Readable source slices from 20260912d hunt. No cell exec."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260912e"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def dump_nb(rel: str) -> None:
    path = DIR / rel
    print("=" * 78)
    print(rel, "bytes", path.stat().st_size, "sha256", hashlib.sha256(path.read_bytes()).hexdigest())
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells") or []
    print("n_cells", len(cells))
    for i, cell in enumerate(cells):
        src = cell_source(cell)
        print(
            f"-- cell {i} {cell.get('cell_type')} {len(src)} exec={cell.get('execution_count')} outputs={len(cell.get('outputs') or [])} --"
        )
        lines = src.splitlines()
        if cell.get("cell_type") == "markdown":
            for line in lines[:18]:
                print(line[:220])
            continue
        if src.lstrip().startswith("%%writefile"):
            first = lines[0] if lines else ""
            rest = "\n".join(lines[1:])
            sha = hashlib.sha256(rest.replace("\r\n", "\n").encode("utf-8")).hexdigest()
            print("WRITEFILE", first[:120], "payload_sha256", sha, "payload_bytes", len(rest))
        shown = 0
        for line in lines:
            if len(line) > 240 and any(
                k in line for k in ("b85decode", "b64", "zlib", "lzma", "_DATA", "_INLINE", "PROGRAM", "gzip")
            ):
                print(line[:100] + " ...[payload truncated]...")
                shown += 1
                continue
            interesting = any(
                k in line
                for k in (
                    "%%writefile",
                    "ROUTE_STEP",
                    "FINAL_PLAN",
                    "ADVANCE_START",
                    "sale_horizon",
                    "reselect",
                    "later",
                    "ctypes",
                    "CDLL",
                    "agent.so",
                    "EXPECTED",
                    "def agent",
                    "PROGRAM",
                    "DECISIONS",
                    "open(",
                    "main.py",
                    "tarfile",
                    "gzip",
                    "zlib",
                    "b85",
                    "base64",
                    "144",
                    "216",
                    "226",
                    "288",
                    "360",
                    "432",
                    "576",
                    "648",
                    "712",
                )
            )
            if interesting or shown < 16:
                print(line[:220])
                shown += 1
                if shown > 80:
                    print("...[truncated]...")
                    break
        print("n_lines", len(lines))


def main() -> None:
    dump_nb("nusrati__2650-score/2650-score.ipynb")
    dump_nb("sunil123kumar__kaggriculture-v4/kaggriculture-v4.ipynb")
    dump_nb("zhincez__ten-ppo-runs-one-fake-win-zero-real-ones/ten-ppo-runs-one-fake-win-zero-real-ones.ipynb")
    dump_nb("zhincez__the-market-half-is-worth-zero-on-its-own/the-market-half-is-worth-zero-on-its-own.ipynb")


if __name__ == "__main__":
    main()
