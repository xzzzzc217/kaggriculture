"""When the Ramesh tape buys cows/sheep and sells wheat."""

from __future__ import annotations

import ast
import base64
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "experiments/candidates/prvsiyan_moon_v189c/decoded_ramesh.py"


def load_actions():
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
    for step, action in enumerate(actions):
        for order in action.get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_ANIMAL":
                print(f"step {step:3d} day {step//24+1:2d} BUY_ANIMAL {order}")
            if order[0] == "BUY_LAND":
                print(f"step {step:3d} day {step//24+1:2d} BUY_LAND")
            if order[0] == "BUY_SEED" and len(order) > 1 and order[1] in {"TOMATO", "CARROT"}:
                print(f"step {step:3d} day {step//24+1:2d} BUY_SEED {order}")


if __name__ == "__main__":
    main()
