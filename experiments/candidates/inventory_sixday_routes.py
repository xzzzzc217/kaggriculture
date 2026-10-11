"""Dump animal buys and product sells for every six-day segment/route."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "yusuke_sixday"))
from sixday_logic import DECODED_SEGMENTS, ITEMS, MARKET_OPS, SIX_DAY_TURNS


def main() -> None:
    for seg, routes in enumerate(DECODED_SEGMENTS):
        for route, tape in enumerate(routes):
            buys: Counter[str] = Counter()
            sells: Counter[str] = Counter()
            cow_steps: list[tuple[int, int]] = []
            sheep_steps: list[tuple[int, int]] = []
            for local, act in enumerate(tape):
                step = seg * SIX_DAY_TURNS + local
                for op, item, qty in act["orders"]:
                    name = MARKET_OPS[op]
                    iname = ITEMS[item]
                    if name == "BUY_ANIMAL":
                        buys[iname] += qty
                        if iname == "COW":
                            cow_steps.append((step, qty))
                        elif iname == "SHEEP":
                            sheep_steps.append((step, qty))
                    elif name == "SELL":
                        sells[iname] += qty
                    elif name == "BUY_LAND":
                        buys["LAND"] += 1
            print(
                f"s{seg} r{route} BUY {dict(buys)} "
                f"SELL milk={sells.get('MILK', 0)} wool={sells.get('WOOL', 0)} "
                f"wheat={sells.get('WHEAT', 0)} straw={sells.get('STRAWBERRY', 0)} "
                f"cow_sell={sells.get('COW', 0)}"
            )
            after216 = [row for row in cow_steps if row[0] >= 216]
            after288 = [row for row in cow_steps if row[0] >= 288]
            if after216:
                print("  cow after 216", after216)
            if after288:
                print("  cow after 288", after288)
            sheep_after = [row for row in sheep_steps if row[0] >= 200]
            if sheep_after:
                print("  sheep after 200", sheep_after)


if __name__ == "__main__":
    main()
