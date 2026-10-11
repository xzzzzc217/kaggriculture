"""Summarize Moon V189C inner Ramesh tape vs Crop Dusta shop-bag doctrine."""

from __future__ import annotations

import ast
import base64
import json
import zlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "experiments/candidates/prvsiyan_moon_v189c/decoded_ramesh.py"


def load_actions() -> list:
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "b85decode" and node.args:
                if isinstance(node.args[0], ast.Constant):
                    blob = zlib.decompress(base64.b85decode(node.args[0].value)).decode("utf-8")
                    return json.loads(blob)
    raise SystemExit("no actions")


def main() -> None:
    actions = load_actions()
    print("n_steps", len(actions))
    sells = Counter()
    sells_day = defaultdict(Counter)
    plants = Counter()
    animals = Counter()
    land = []
    hires = Counter()
    farmer_ops = Counter()
    for step, action in enumerate(actions):
        day = step // 24
        farmer = action.get("farmer") or ["PASS"]
        farmer_ops[farmer[0] if farmer else "PASS"] += 1
        if farmer and farmer[0] == "PLANT" and len(farmer) > 1:
            plants[str(farmer[1]).upper()] += 1
        for hand in action.get("hands") or []:
            if hand and hand[0] == "PLANT" and len(hand) > 1:
                plants[str(hand[1]).upper()] += 1
        for order in action.get("market") or []:
            if not order:
                continue
            op = str(order[0])
            item = str(order[1]).upper() if len(order) > 1 else ""
            qty = int(order[2]) if len(order) > 2 else 1
            if op == "SELL":
                sells[item] += qty
                sells_day[day][item] += qty
            elif op == "BUY_LAND":
                land.append(step)
            elif op == "BUY_ANIMAL":
                animals[item] += qty
            elif op == "HIRE":
                hires[day] += 1
            elif op == "BUY_SEED":
                plants[f"SEED:{item}"] += qty
    print("BUY_LAND", land)
    print("animals", dict(animals))
    print("plants", dict(plants))
    print("sells", dict(sells))
    print("max hires/day", max(hires.values()) if hires else 0, "days with hire", len(hires))
    print("wheat by day", [sells_day[d].get("WHEAT", 0) for d in range(30)])
    print("tomato by day", [sells_day[d].get("TOMATO", 0) for d in range(30)])
    print("carrot by day", [sells_day[d].get("CARROT", 0) for d in range(30)])
    print("egg by day", [sells_day[d].get("EGG", 0) for d in range(30)])
    print("melon by day", [sells_day[d].get("MELON", 0) for d in range(30)])
    print("wool by day", [sells_day[d].get("WOOL", 0) for d in range(30)])
    print("strawberry by day", [sells_day[d].get("STRAWBERRY", 0) for d in range(30)])
    print("milk by day", [sells_day[d].get("MILK", 0) for d in range(30)])
    print("fert by day", [sells_day[d].get("FERTILIZER", 0) for d in range(30)])
    print("farmer ops", dict(farmer_ops.most_common(12)))
    out = {
        "n": len(actions),
        "buy_land": land,
        "animals": dict(animals),
        "plants": dict(plants),
        "sells": dict(sells),
        "wheat_by_day": [sells_day[d].get("WHEAT", 0) for d in range(30)],
        "melon_by_day": [sells_day[d].get("MELON", 0) for d in range(30)],
        "tomato_by_day": [sells_day[d].get("TOMATO", 0) for d in range(30)],
        "carrot_by_day": [sells_day[d].get("CARROT", 0) for d in range(30)],
        "egg_by_day": [sells_day[d].get("EGG", 0) for d in range(30)],
    }
    dest = ROOT / "experiments/20260828_moon_v189c_tape.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
