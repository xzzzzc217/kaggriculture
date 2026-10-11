"""Statically extract Yusuke two-shop demo agent. No cell exec."""

from __future__ import annotations

import hashlib
import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB = ROOT / "artifacts/public_sources/_hunt_20260830b/public-match-history-router-rating-2929-aug-30.ipynb"
OUT = ROOT / "experiments/candidates/yusuke_shopforge_demo"
README = """# Yusuke ShopForge two-shop demo (static extract)

Source: `yhay81/public-match-history-router-rating-2929-aug-30` cells 7+8.
Notebook says this is **not** the submitted ShopForge CR2 (68-18, LB 2929).
It is the reduced 10-history / 23-pair two-shop router over public Milan/Kenjo/Shuwen tapes.

Do not upload unless it 2/3-flips frozen MtN/Yusuke/Hanserong and keeps clone/G5.
"""


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    cells = nb.get("cells") or []
    code = []
    for index in (7, 8):
        cell = cells[index]
        if cell.get("cell_type") != "code":
            raise SystemExit(f"cell {index} is not code")
        code.append(cell_source(cell).rstrip() + "\n")
    text = "\n".join(code)
    if "def agent(" not in text or "_ROUTES_DATA" not in text:
        raise SystemExit("missing agent or routes")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "main.py"
    raw = text.encode("utf-8").replace(b"\r\n", b"\n")
    if not raw.endswith(b"\n"):
        raw += b"\n"
    target.write_bytes(raw)
    py_compile.compile(str(target), doraise=True)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (OUT / "README.md").write_text(README, encoding="utf-8")
    print("path", target)
    print("bytes", target.stat().st_size)
    print("sha256", digest)
    print("has_agent", "def agent(" in text)
    print("routes_marker", "_ROUTES_DATA" in text)


if __name__ == "__main__":
    main()
