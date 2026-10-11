"""Print compact rolling-12 rows for the 20260912b packet."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
games = json.loads((ROOT / "experiments/20260912b_cut16_rolling.json").read_text(encoding="utf-8"))["games"]


def herd(buy: dict) -> str:
    c = int(buy.get("COW") or 0)
    s = int(buy.get("SHEEP") or 0)
    g = int(buy.get("GOOSE") or 0)
    return f"{c}c{s}s{g}g"


for rec in games:
    flag = "W" if rec["win"] else ("T" if rec["tie"] else "L")
    print(
        rec["id"],
        flag,
        int(rec["margin"]),
        rec["opp"],
        "clone",
        int(rec["clone"]),
        "us",
        herd(rec["buy_us"]),
        "opp",
        herd(rec["buy_opp"]),
        "shops72",
        rec["shops72"],
        "sheep_us",
        rec["sheep_steps_us"],
        "wheat",
        rec["wheat"],
        "wool",
        rec["wool"],
        "cash24",
        rec["cash_24"],
    )
