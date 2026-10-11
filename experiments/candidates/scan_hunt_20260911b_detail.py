"""Per-cell flag context for 20260911b hunt. No cell exec."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260911b"
NEEDLES = [
    "ctypes.CDLL",
    "ctypes",
    "CDLL",
    "agent.so",
    "reselect",
    "later-block",
    "later_block",
    "DECISIONS",
    "EXPECTED_SOURCE_SHA256",
    "%%writefile",
    "ROUTE_STEP",
    "FINAL_PLAN_STEP",
    "ADVANCE_START",
    "sale_horizon",
    "if step == 144",
    "if step == 216",
    "if step>=216",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def show_ctx(text: str, needle: str, n: int = 2) -> None:
    start = 0
    found = 0
    while found < n:
        i = text.find(needle, start)
        if i < 0:
            break
        snippet = text[max(0, i - 40) : i + 90].replace("\n", " ")
        print("  ctx", needle, snippet[:160])
        start = i + len(needle)
        found += 1


def main() -> None:
    for path in sorted(DIR.rglob("*")):
        if path.suffix.lower() not in {".ipynb", ".py"} or path.name == "kernel-metadata.json":
            continue
        print("=" * 70)
        print(path.parent.name, path.name, path.stat().st_size)
        if path.suffix == ".py":
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle in NEEDLES:
                if needle in text:
                    print(" HIT", needle, "count", text.count(needle))
                    show_ctx(text, needle)
            continue
        notebook = json.loads(path.read_text(encoding="utf-8"))
        cells = notebook.get("cells") or []
        print("cells", len(cells), [c.get("cell_type") for c in cells])
        for index, cell in enumerate(cells):
            src = cell_source(cell)
            hits = [n for n in NEEDLES if n in src]
            if not hits:
                continue
            print(f" cell {index} {cell.get('cell_type')} {len(src)} hits={hits}")
            if src.lstrip().startswith("%%writefile"):
                first, _, rest = src.partition("\n")
                sha = hashlib.sha256(rest.replace("\r\n", "\n").encode("utf-8")).hexdigest()
                print("  writefile", first[:100], "sha", sha, "bytes", len(rest))
            if any(k in src for k in ("ctypes", "CDLL", "agent.so")):
                for line in src.splitlines():
                    if any(k in line for k in ("ctypes", "CDLL", "agent.so")):
                        print("  NATIVE", line[:200])
            if "reselect" in src.lower() or "later-block" in src.lower() or "later_block" in src:
                for line in src.splitlines():
                    low = line.lower()
                    if "reselect" in low or "later-block" in low or "later_block" in low:
                        print("  RESEL", line[:200])


if __name__ == "__main__":
    main()
