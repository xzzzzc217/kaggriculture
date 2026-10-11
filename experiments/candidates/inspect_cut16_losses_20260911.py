"""Cash, shops, prices, herds on 09-11 cut16 rolling losses."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut16_20260911")
OUR = "heralces"
IDS = [
    107751105,
    107746999,
    107741134,
    107729381,
    107722325,
    107712285,
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
    mprices = ((obs.get("market") or {}).get("prices") or {})
    out = {}
    for key in ("WOOL", "WHEAT", "MILK", "FERTILIZER"):
        good = goods.get(key) or {}
        town_p = good.get("price") if isinstance(good, dict) else None
        out[key] = town_p if town_p is not None else mprices.get(key)
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
    rolling = json.loads(Path("experiments/20260911_cut16_rolling.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in rolling["games"]}
    for eid in IDS:
        path = LIVE / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        rec = by_id[eid]
        print("=" * 72)
        print(
            eid,
            rec["opp"],
            rec["margin"],
            "clone",
            rec["clone"],
            "land",
            rec["land"],
            "Q",
            rec["Q"],
            "buy",
            rec["buy_us"],
            rec["buy_opp"],
            "sheep_us",
            rec["sheep_steps_us"],
            "cash24",
            rec["cash_24"],
        )
        buy_land = []
        for t, states in enumerate(replay["steps"]):
            for order in (states[seat].get("action") or {}).get("market") or []:
                if order and order[0] == "BUY_LAND":
                    prev = obs_at(replay, seat, max(0, t - 1) if t else 0)
                    buy_land.append((t, farm_money(prev, seat), farm_q(prev, seat)))
        print("  BUY_LAND", buy_land)
        for t in (24, 144, 151, 216, 266, 288, 360, 432, 576, 719):
            obs = obs_at(replay, seat, t)
            pr = prices(obs)
            print(
                f"  t={t:3d} cash={farm_money(obs, seat):8.0f}/{farm_money(obs, opp):8.0f} "
                f"Q={farm_q(obs, seat)}/{farm_q(obs, opp)} "
                f"us={animals(obs, seat)} opp={animals(obs, opp)} "
                f"WOOL={pr['WOOL']} WHEAT={pr['WHEAT']} MILK={pr['MILK']}"
            )


if __name__ == "__main__":
    main()
