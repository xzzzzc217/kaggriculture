"""Cash, shops, prices, and herds on 09-10 cut14 rolling losses."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut14_20260910")
OUR = "heralces"
IDS = [
    107493021,
    107489775,
    107474367,
    107469973,
    107469814,
    107464310,
    107453419,
]


def obs_at(replay, seat, t):
    t = min(t, len(replay["steps"]) - 1)
    return replay["steps"][t][seat].get("observation") or {}


def farm_money(obs, seat):
    farms = obs.get("farms") or [{}, {}]
    return float((farms[seat] or {}).get("money") or 0)


def farm_q(obs, seat):
    farms = obs.get("farms") or [{}, {}]
    return len((farms[seat] or {}).get("unlocked_quadrants") or [])


def prices(obs):
    goods = (obs.get("town") or {}).get("goods") or {}
    out = {}
    for key in ("WOOL", "WHEAT", "MILK", "FERTILIZER", "CARROT", "MELON", "EGG"):
        good = goods.get(key) or {}
        out[key] = good.get("price") if isinstance(good, dict) else None
    return out


def animals(obs, seat):
    farms = obs.get("farms") or [{}, {}]
    farm = farms[seat] or {}
    counts = Counter()
    for row in farm.get("tiles") or []:
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            kind = str(tile.get("animal") or tile.get("kind") or "").upper()
            if kind in ("COW", "SHEEP", "GOOSE"):
                counts[kind] += 1
    return dict(counts)


def sell_qty(replay, seat, item, until=None):
    total = 0
    last = len(replay["steps"]) if until is None else min(until, len(replay["steps"]))
    for states in replay["steps"][:last]:
        for order in (states[seat].get("action") or {}).get("market") or []:
            if order and order[0] == "SELL" and order[1] == item:
                total += int(order[2]) if len(order) > 2 else 1
    return total


def main() -> None:
    for eid in IDS:
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        print("=" * 72, eid, teams)
        print(" rewards", [state.get("reward") for state in replay["steps"][-1]], "n", len(replay["steps"]))
        for t, states in enumerate(replay["steps"]):
            for order in (states[seat].get("action") or {}).get("market") or []:
                if order and order[0] == "BUY_LAND":
                    prev = obs_at(replay, seat, max(0, t - 1) if t else 0)
                    print(
                        f"  BUY_LAND @{t} prev_cash={farm_money(prev, seat):.0f} "
                        f"prev_Q={farm_q(prev, seat)}"
                    )
        for t in (0, 24, 72, 144, 151, 216, 226, 266, 288, 360, 432, 433, 576, 719):
            obs = obs_at(replay, seat, t)
            price = prices(obs)
            print(
                f"  t={t:3d} cash={farm_money(obs, seat):.0f} opp={farm_money(obs, opp):.0f} "
                f"gap={farm_money(obs, seat) - farm_money(obs, opp):.0f} "
                f"Q={farm_q(obs, seat)}/{farm_q(obs, opp)} "
                f"us={animals(obs, seat)} opp={animals(obs, opp)} "
                f"wool_p={price['WOOL']} wheat_p={price['WHEAT']} milk_p={price['MILK']}"
            )
        print(
            "  sells_us wheat/wool/milk",
            sell_qty(replay, seat, "WHEAT"),
            sell_qty(replay, seat, "WOOL"),
            sell_qty(replay, seat, "MILK"),
        )
        print(
            "  sells_opp wheat/wool/milk",
            sell_qty(replay, opp, "WHEAT"),
            sell_qty(replay, opp, "WOOL"),
            sell_qty(replay, opp, "MILK"),
        )
        print(
            "  sells_opp_until216 wheat/wool",
            sell_qty(replay, opp, "WHEAT", 216),
            sell_qty(replay, opp, "WOOL", 216),
        )


if __name__ == "__main__":
    main()
