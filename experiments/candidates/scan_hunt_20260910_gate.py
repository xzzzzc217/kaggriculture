"""Static later-block scan of 2026-09-10 gate hunt notebooks. No cell exec."""

from __future__ import annotations

import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910_gate"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefile_targets(text: str) -> list[str]:
    return re.findall(r"%%writefile\s+(\S+)", text)


def later_hits(text: str) -> list[str]:
    patterns = [
        r"step\s*[>=]{1,2}\s*2[1-9]\d",
        r"turn\s*[>=]{1,2}\s*2[1-9]\d",
        r"t\s*[>=]{1,2}\s*2[1-9]\d",
        r"\b2(?:1[7-9]|2\d|3\d|4\d|5\d|6\d|7\d|8\d|9\d|[3-6]\d{2})\b",
        r"reselect",
        r"later.?block",
        r"DECISIONS",
        r"YARN_STORE",
        r"prefix.?guard",
        r"ctypes",
        r"CDLL",
        r"agent\.so",
    ]
    hits: list[str] = []
    low = text
    for pat in patterns:
        found = re.findall(pat, low, flags=re.I)
        if found:
            uniq = sorted(set(found))[:12]
            hits.append(f"{pat}->{uniq}")
    return hits


def main() -> None:
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        notebook = json.loads(raw.decode("utf-8"))
        cells = notebook.get("cells") or []
        writes = writefile_targets(text)
        ctypes_hit = "ctypes" in text or "CDLL" in text or "agent.so" in text
        print("=" * 72)
        print(path.parent.name)
        print("bytes", len(raw), "cells", len(cells), "writefiles", writes, "ctypes/so", ctypes_hit)
        for index, cell in enumerate(cells):
            src = cell_source(cell)
            if "%%writefile" not in src and "EXPECTED_SOURCE_SHA256" not in src:
                continue
            first = [line for line in src.splitlines() if line.strip()][:12]
            print(f"  cell {index} {cell.get('cell_type')} {len(src)} first:")
            for line in first:
                print("   ", line[:160])
            if "def agent" in src or "make_agent" in src or "class " in src[:4000]:
                # sample later-block-ish lines
                interesting = []
                for line in src.splitlines():
                    if re.search(
                        r"216|226|241|360|385|433|648|712|reselect|YARN|DECISIONS|ctypes|CDLL|agent\.so|step ==|step>=|t ==",
                        line,
                    ):
                        interesting.append(line.strip()[:160])
                        if len(interesting) >= 18:
                            break
                if interesting:
                    print("  interesting:")
                    for line in interesting:
                        print("   ", line)


if __name__ == "__main__":
    main()
