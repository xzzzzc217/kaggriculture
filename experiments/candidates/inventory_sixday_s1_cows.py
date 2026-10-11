"""Print every cow/sheep buy step in segment 1."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "yusuke_sixday"))
from sixday_logic import DECODED_SEGMENTS, ITEMS, MARKET_OPS, SIX_DAY_TURNS


def main() -> None:
    for route, tape in enumerate(DECODED_SEGMENTS[1]):
        print("s1 r", route)
        for local, act in enumerate(tape):
            step = SIX_DAY_TURNS + local
            for op, item, qty in act["orders"]:
                if MARKET_OPS[op] == "BUY_ANIMAL":
                    print(f"  {step} BUY {ITEMS[item]} {qty}")


if __name__ == "__main__":
    main()
