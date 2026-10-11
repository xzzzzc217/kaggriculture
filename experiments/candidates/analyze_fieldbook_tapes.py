"""Decode Fieldbook PLAN_SCRIPTS: herd, land, sells. No env run."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments/candidates/yusuke_fieldbook"))
from fieldbook_logic import (  # noqa: E402
    ROUTES,
    ROUTE_NAMES,
    _compose,
)

OUT = ROOT / "experiments/20260901_fieldbook_tapes.json"
SELL_ITEMS = (
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
)


def summarize(actions: list) -> dict:
    sells = Counter()
    buys = Counter()
    land = []
    pastures = 0
    plants = Counter()
    animal_times = []
    for step, action in enumerate(actions):
        for order in action.get("market") or []:
            if not order:
                continue
            op = order[0]
            item = order[1] if len(order) > 1 else ""
            qty = int(order[2]) if len(order) > 2 else 1
            if op == "SELL":
                sells[item] += qty
            elif op == "BUY_ANIMAL":
                buys[item] += qty
                animal_times.append((step, item, qty))
            elif op == "BUY_LAND":
                land.append(step)
            elif op == "BUY_SEED":
                plants[item] += qty
        units = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
        for unit in units:
            if unit and unit[0] == "BUILD_PASTURE":
                pastures += 1
    wheat_day = [0] * 30
    tomato_day = [0] * 30
    carrot_day = [0] * 30
    egg_day = [0] * 30
    melon_day = [0] * 30
    for step, action in enumerate(actions):
        day = min(step // 24, 29)
        for order in action.get("market") or []:
            if not order or order[0] != "SELL":
                continue
            item = order[1]
            qty = int(order[2]) if len(order) > 2 else 1
            if item == "WHEAT":
                wheat_day[day] += qty
            elif item == "TOMATO":
                tomato_day[day] += qty
            elif item == "CARROT":
                carrot_day[day] += qty
            elif item == "EGG":
                egg_day[day] += qty
            elif item == "MELON":
                melon_day[day] += qty
    return {
        "sells": {k: sells[k] for k in SELL_ITEMS},
        "buy_animals": dict(buys),
        "land_steps": land,
        "pastures": pastures,
        "buy_seeds": dict(plants),
        "animal_timeline": animal_times,
        "wheat_by_day": wheat_day,
        "tomato_by_day": tomato_day,
        "carrot_by_day": carrot_day,
        "egg_by_day": egg_day,
        "melon_by_day": melon_day,
        "wheat_d12_15": sum(wheat_day[11:15]),
        "hinge_d29_30": {
            "TOMATO": tomato_day[28] + tomato_day[29],
            "CARROT": carrot_day[28] + carrot_day[29],
            "EGG": egg_day[28] + egg_day[29],
        },
    }


def main() -> None:
    rows = {}
    for index, name in ROUTE_NAMES.items():
        rec = summarize(ROUTES[index])
        rec["route_index"] = index
        rec["label"] = name
        rows[name] = rec
        print(
            name,
            "animals",
            rec["buy_animals"],
            "land",
            rec["land_steps"],
            "pastures",
            rec["pastures"],
            "wheat",
            rec["sells"]["WHEAT"],
            "wool",
            rec["sells"]["WOOL"],
            "milk",
            rec["sells"]["MILK"],
            "fert",
            rec["sells"]["FERTILIZER"],
            "melon",
            rec["sells"]["MELON"],
            "tomato",
            rec["sells"]["TOMATO"],
            "carrot",
            rec["sells"]["CARROT"],
            "egg",
            rec["sells"]["EGG"],
            "straw",
            rec["sells"]["STRAWBERRY"],
            flush=True,
        )
        print("  wheat_d12_15", rec["wheat_d12_15"], "hinge_d29_30", rec["hinge_d29_30"])
        print("  animals", rec["animal_timeline"])
    OUT.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
