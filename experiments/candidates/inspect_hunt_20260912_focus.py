"""Readable source slices from 20260912 hunt. No cell exec, no payload decode."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260912"
V34_0911 = (
    Path(__file__).resolve().parents[2]
    / "artifacts/public_sources/_hunt_20260911/ahmedberatozer__notebooka4fc70fd19/notebooka4fc70fd19.ipynb"
)


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
        print(f"-- cell {i} {cell.get('cell_type')} {len(src)} --")
        lines = src.splitlines()
        if cell.get("cell_type") == "markdown":
            for line in lines[:22]:
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
                    k in line for k in ("b85decode", "b64", "zlib", "lzma", "_DATA", "_INLINE", "PROGRAM")
                ):
                    print(line[:100] + " ...[payload truncated]...")
                    continue
                interesting = any(
                    k in line
                    for k in (
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
                        "216",
                        "226",
                        "227",
                        "242",
                        "266",
                        "288",
                        "360",
                        "432",
                        "433",
                        "576",
                        "648",
                        "712",
                        "def agent",
                        "SETTINGS",
                        "SALE_HORIZON",
                    )
                )
                if interesting or shown < 18:
                    print(line[:220])
                    shown += 1
                    if shown > 90:
                        print("...[truncated writefile]...")
                        break
            # real ctypes / agent.so not in long payload digits
            real_ctypes = bool(re.search(r"\bctypes\b", rest))
            real_cdll = "CDLL(" in rest or "cdll." in rest.lower()
            real_so = "agent.so" in rest or "agent.dylib" in rest
            print("REAL_CTYPES", real_ctypes, "REAL_CDLL", real_cdll, "REAL_AGENT_SO", real_so)
            print("reselect", "reselect" in rest.lower(), "later_block", "later-block" in rest.lower() or "later_block" in rest)
            continue
        for line in lines[:50]:
            print(line[:220])
        if len(lines) > 50:
            print(f"...[{len(lines)-50} more lines]...")


def main() -> None:
    dump_nb("ahmedberatozer__more-yield-smarter-labor/more-yield-smarter-labor.ipynb")
    dump_nb("ahmedberatozer__kaggriculture-v36-guarded-four-turn-sales/kaggriculture-v36-guarded-four-turn-sales.ipynb")
    dump_nb("hgh1024__kaggriculture-herd-safe-v2-sale-horizon-2/kaggriculture-herd-safe-v2-sale-horizon-2.ipynb")
    dump_nb("ahmedberatozer__kaggriculture-v34-observed-market-timing/kaggriculture-v34-observed-market-timing.ipynb")
    if V34_0911.exists():
        a = hashlib.sha256(
            (DIR / "ahmedberatozer__kaggriculture-v34-observed-market-timing/kaggriculture-v34-observed-market-timing.ipynb").read_bytes()
        ).hexdigest()
        b = hashlib.sha256(V34_0911.read_bytes()).hexdigest()
        print("V34_NB_SHA_0912", a)
        print("V34_NB_SHA_0911_notebooka4fc70fd19", b)
        print("V34_NOTEBOOK_IDENTICAL", a == b)


if __name__ == "__main__":
    main()
