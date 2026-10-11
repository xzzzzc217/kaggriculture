"""Cash, shops, prices, herds, and SELL forms on 09-10b cut15 rolling losses."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut15_20260910b")
OUR = "heralces"
IDS = [
    107579117,
    107578892,
    107571704,
    107571691,
    107571612,
    107570298,
    107568611,
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


def main() -> None:
    for eid in IDS:
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        print("=" * 72, eid, teams)
        print(" rewards", [st.get("reward") for st in replay["steps"][-1]], "n", len(replay["steps"]))
        buy_land = []
        sell_samples = []
        sell_ops = Counter()
        qty_by_item = Counter()
        n_sell = 0
        for t, states in enumerate(replay["steps"]):
            for order in (states[seat].get("action") or {}).get("market") or []:
                if not order:
                    continue
                if order[0] == "BUY_LAND":
                    prev = obs_at(replay, seat, max(0, t - 1) if t else 0)
                    buy_land.append((t, farm_money(prev, seat), farm_q(prev, seat)))
                if order[0] == "SELL":
                    n_sell += 1
                    sell_ops[tuple(str(x) for x in order)] += 1
                    item = str(order[1]) if len(order) > 1 else ""
                    qty = int(order[2]) if len(order) > 2 else 1
                    qty_by_item[item] += qty
                    if len(sell_samples) < 10:
                        sell_samples.append((t, order))
        print("  BUY_LAND", buy_land)
        print("  n_sell", n_sell, "qty_by_item", dict(qty_by_item))
        print("  sell_samples", sell_samples)
        print("  unique SELL forms", len(sell_ops), "top", sell_ops.most_common(8))
        opp_samples = []
        for t, states in enumerate(replay["steps"]):
            for order in (states[opp].get("action") or {}).get("market") or []:
                if order and order[0] == "SELL" and len(opp_samples) < 4:
                    opp_samples.append((t, order))
        print("  opp_sell_samples", opp_samples)
        for t in (0, 24, 72, 144, 151, 216, 266, 288, 360, 432, 576, 719):
            obs = obs_at(replay, seat, t)
            price = prices(obs)
            print(
                f"  t={t:3d} cash={farm_money(obs, seat):.0f} opp={farm_money(obs, opp):.0f} "
                f"Q={farm_q(obs, seat)}/{farm_q(obs, opp)} "
                f"us={animals(obs, seat)} opp={animals(obs, opp)} "
                f"wool_p={price['WOOL']} wheat_p={price['WHEAT']} milk_p={price['MILK']}"
            )


if __name__ == "__main__":
    main()
