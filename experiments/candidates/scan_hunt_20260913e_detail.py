"""Static V39 writefile flags vs V38/live cuts. No cell exec. No extract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB = ROOT / "artifacts/public_sources/_hunt_20260913e/notebookda72f457f5.ipynb"
V37 = "94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c"
V38 = "a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e"
CUT14 = "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
CUT15 = "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
CUT16 = "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    rest = None
    for i, cell in enumerate(nb.get("cells") or []):
        src = cell_source(cell)
        if src.lstrip().startswith("%%writefile"):
            _, _, rest = src.partition("\n")
            rest = rest.replace("\r\n", "\n")
            print("writefile_cell", i)
            break
    if rest is None:
        raise SystemExit("no writefile")
    sha = hashlib.sha256(rest.encode("utf-8")).hexdigest()
    print("sha256", sha)
    print("eq_v37", sha == V37)
    print("eq_v38", sha == V38)
    print("eq_cut14", sha == CUT14)
    print("eq_cut15", sha == CUT15)
    print("eq_cut16", sha == CUT16)
    keys = [
        "ROUTE_STEP",
        "FINAL_PLAN_STEP",
        "sale_horizon",
        "ADVANCE_START",
        "DECISIONS",
        "PROGRAM",
        "reselect",
        "ctypes",
        "CDLL",
        "agent.so",
        "step>=144",
        "step>=648",
        "216<=step<=227",
        "712",
        "288",
        "P3",
        "P4",
        "P5",
        "P6",
        "YARN_SECOND",
    ]
    print("payload_flags", {k: (k in rest) for k in keys})
    for needle in (
        "step>=144",
        "step>=648",
        "216<=step<=227",
        "sale_horizon",
        "ADVANCE_START",
        "if step<288",
        "712<=step<=718",
        "production-calendar",
        "V39",
        "V38",
    ):
        for line in rest.splitlines():
            if needle in line and len(line) < 220:
                print("LINE", needle, line[:220])
                break


if __name__ == "__main__":
    main()
