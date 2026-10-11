"""Wool/cash/herd on 09-11b cut16 rolling heavy losses."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut16_20260911b")
OUR = "heralces"
IDS = [107814299, 107821475, 107828353, 107804802, 107795450, 107789318]


def obs_at(replay, seat, t):
    t = min(t, len(replay["steps"]) - 1)
    return replay["steps"][t][seat].get("observation") or {}


def farm_money(obs, seat):
    farms = obs.get("farms") or [{}, {}]
    return float((farms[seat] or {}).get("money") or 0)


def prices(obs):
    goods = (obs.get("town") or {}).get("goods") or {}
    if isinstance(goods, dict):
        out = {}
        for key in ("WOOL", "WHEAT", "MILK"):
            good = goods.get(key) or {}
            out[key] = good.get("price") if isinstance(good, dict) else None
        return out
    out = {}
    if isinstance(goods, list):
        for good in goods:
            if isinstance(good, dict) and good.get("name") in ("WOOL", "WHEAT", "MILK"):
                out[good["name"]] = good.get("price")
    return out


def main() -> None:
    rolling = json.loads(Path("experiments/20260911b_cut16_rolling.json").read_text(encoding="utf-8"))
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
        for t in (216, 288, 360, 432, 576, 719):
            obs = obs_at(replay, seat, t)
            pr = prices(obs)
            print(
                f"  t={t:3d} cash={farm_money(obs, seat):8.0f}/{farm_money(obs, opp):8.0f} "
                f"WOOL={pr.get('WOOL')} WHEAT={pr.get('WHEAT')} MILK={pr.get('MILK')}"
            )


if __name__ == "__main__":
    main()
