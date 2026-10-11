"""Deeper static notes for 20260910b hunt. No cell exec."""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910b"


def src(cell):
    s = cell.get("source") or ""
    return "".join(s) if isinstance(s, list) else str(s)


def dump(name: str, needles: list[str], around: int = 2) -> None:
    path = next(DIR.glob(name + "/**/*.ipynb"))
    nb = json.loads(path.read_text(encoding="utf-8"))
    print("=" * 78)
    print(path.parent.name)
    for i, cell in enumerate(nb.get("cells") or []):
        text = src(cell)
        low = text.lower()
        if cell.get("cell_type") == "markdown" and i < 3:
            print(f"-- md {i} --")
            for line in text.strip().splitlines()[:8]:
                print(line[:200])
        if any(n.lower() in low for n in needles):
            print(f"-- hit cell {i} {cell.get('cell_type')} {len(text)} --")
            lines = text.splitlines()
            for j, line in enumerate(lines):
                if any(n.lower() in line.lower() for n in needles):
                    lo = max(0, j - around)
                    hi = min(len(lines), j + around + 1)
                    for k in range(lo, hi):
                        print(f"{k:4d}|{lines[k][:220]}")
                    print("    ...")


def main() -> None:
    dump(
        "ahmedberatozer__notebook20e618e50b",
        ["216<=step", "step==432", "DECISIONS", "226", "360", "433", "288", "reselect", "ctypes", "CDLL"],
        1,
    )
    dump(
        "shashwat12a__kaggriculture-rl-model",
        ["agent", "writefile", "PPO", "RL", "main.py", "kaggle_environments"],
        1,
    )
    dump(
        "lucifer19__harvest-nocturne-the-market-has-a-rhythm",
        ["%%writefile", "def agent", "CDLL", "ctypes", "later", "288", "216", "Harvest Nocturne"],
        1,
    )
    dump(
        "mzcao7__kaggriculture-forkable-baseline-paired-tests",
        ["%%writefile", "later", "reselect", "144", "216", "V7"],
        1,
    )
    dump(
        "boatlee__v29-r1-adaptive-market-hysteresis",
        ["PAYLOAD", "writefile", "later", "216", "226"],
        1,
    )
    dump(
        "dmitriigluzdov__kaggriculture-two-coins-one-sheep-lb-2700",
        ["CDLL", "ctypes", "agent.so", "ADVANCE_START", "ROUTE_STEP"],
        1,
    )
    dump(
        "yamakawanin__kaggriculture-2312-9-q30-v2a",
        ["reselect", "DECISIONS", "later-block", "216 <= step", "P3_YARN"],
        1,
    )


if __name__ == "__main__":
    main()
