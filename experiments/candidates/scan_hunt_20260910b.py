"""Static JSON scan of 20260910b hunt notebooks. No cell exec."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910b"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefile_payloads(source: str) -> list[tuple[str, str]]:
    out = []
    if source.lstrip().startswith("%%writefile"):
        first, _, rest = source.partition("\n")
        name = first.split("%%writefile", 1)[-1].strip()
        if name.startswith("-a "):
            name = name[3:].strip()
        out.append((name, rest))
        return out
    for m in re.finditer(r"open\(['\"]([^'\"]+)['\"].*?['\"]w", source):
        out.append((m.group(1), source[:400]))
    return out


def main() -> None:
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        nb = json.loads(raw.decode("utf-8"))
        cells = nb.get("cells") or []
        text = "\n".join(cell_source(c) for c in cells)
        print("=" * 78)
        print(path.parent.name, "bytes", len(raw), "cells", len(cells))
        flags = {
            "writefile": "%%writefile" in text,
            "ctypes": "ctypes" in text,
            "CDLL": "CDLL" in text or "cdll" in text.lower(),
            "agent.so": "agent.so" in text,
            "dylib": ".dylib" in text,
            "reselect": "reselect" in text.lower(),
            "DECISIONS": "DECISIONS" in text,
            "ROUTE_STEP": "ROUTE_STEP" in text,
            "FINAL_PLAN": "FINAL_PLAN_STEP" in text,
            "later-block": "later-block" in text.lower() or "later_block" in text,
            "226": "226" in text,
            "360": "360" in text,
            "433": "433" in text,
            "144": "144" in text,
            "288": "288" in text,
            "432": "432" in text,
            "576": "576" in text,
            "227": "227" in text,
            "242": "242" in text,
            "266": "266" in text,
            "gzip": "gzip" in text.lower() or "zlib" in text.lower() or "b85" in text.lower(),
            "PufferLib": "PufferLib" in text or "puffer" in text.lower(),
        }
        print("FLAGS", {k: v for k, v in flags.items() if v})
        # writefile files + sha
        for i, cell in enumerate(cells):
            src = cell_source(cell)
            for name, payload in writefile_payloads(src):
                sha = hashlib.sha256(payload.replace("\r\n", "\n").encode("utf-8")).hexdigest()
                print(f"WRITEFILE cell={i} name={name!r} bytes={len(payload)} sha256={sha}")
                # interesting lines
                for line in payload.splitlines():
                    if any(
                        k in line
                        for k in (
                            "ROUTE_STEP",
                            "FINAL_PLAN",
                            "DECISIONS",
                            "ctypes",
                            "CDLL",
                            "agent.so",
                            "reselect",
                            "226",
                            "360",
                            "433",
                            "288",
                            "432",
                            "576",
                            "216",
                            "BUY_ANIMAL",
                            "def agent",
                        )
                    ):
                        if len(line) < 240:
                            print("  ", line)
        # CDLL/ctypes context
        for i, cell in enumerate(cells):
            src = cell_source(cell)
            if "CDLL" in src or "ctypes" in src or "agent.so" in src:
                print(f"NATIVE-HIT cell={i} {cell.get('cell_type')} {len(src)}")
                for line in src.splitlines():
                    if any(k in line.lower() for k in ("cdll", "ctypes", "agent.so", "dylib", ".so")):
                        print("  ", line[:240])
        # first markdown title
        for cell in cells[:2]:
            if cell.get("cell_type") == "markdown":
                print("TITLE", cell_source(cell).strip().splitlines()[0][:160])
                break


if __name__ == "__main__":
    main()
