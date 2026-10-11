"""Wool/cash/herd/land/animal tape on 09-13v cut16 rolling games."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut16_20260914h")
OUR = "heralces"
ROLLING = Path("experiments/20260914h_cut16_rolling.json")


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
    for key in ("WOOL", "WHEAT", "MILK"):
        town_p = None
        if isinstance(goods, dict):
            good = goods.get(key) or {}
            town_p = good.get("price") if isinstance(good, dict) else good
        elif isinstance(goods, list):
            for good in goods:
                if isinstance(good, dict) and good.get("name") == key:
                    town_p = good.get("price")
                    break
        out[key] = town_p if town_p is not None else mprices.get(key)
    return out


def animal_buys(replay, seat):
    rows = []
    tot = Counter()
    for t, states in enumerate(replay["steps"]):
        for order in (states[seat].get("action") or {}).get("market") or []:
            if order and order[0] == "BUY_ANIMAL":
                kind = str(order[1])
                qty = int(order[2]) if len(order) > 2 else 1
                tot[kind] += qty
                rows.append({"step": t, "qty": qty, "kind": kind, "cum": dict(tot)})
    return rows


def buy_land_tape(replay, seat):
    steps = replay["steps"]
    rows = []
    for t, states in enumerate(steps):
        action = states[seat].get("action") or {}
        for order in action.get("market") or []:
            if order and order[0] == "BUY_LAND":
                seen = obs_at(replay, seat, max(0, t - 1))
                farms = seen.get("farms") or [{}, {}]
                q = len((farms[seat] or {}).get("unlocked_quadrants") or [])
                money = float((farms[seat] or {}).get("money") or 0)
                rows.append({"step": t, "prev_Q": q, "cash_prev": money})
    applied = []
    prev_q = None
    for t in range(len(steps)):
        q = farm_q(obs_at(replay, seat, t), seat)
        if prev_q is not None and q != prev_q:
            applied.append({"obs": t, "from": prev_q, "to": q})
        prev_q = q
    return rows, applied


def herd_str(buy):
    c = int(buy.get("COW", 0))
    s = int(buy.get("SHEEP", 0))
    g = int(buy.get("GOOSE", 0))
    parts = [f"{c}c{s}s"]
    if g:
        parts[0] = f"{c}c{s}s{g}g"
    return parts[0]


def main() -> None:
    rolling = json.loads(ROLLING.read_text(encoding="utf-8"))
    games = rolling["games"]
    wool = {}
    for rec in games:
        eid = rec["id"]
        path = LIVE / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        us_buys = animal_buys(replay, seat)
        opp_buys = animal_buys(replay, opp)
        land_act, land_app = buy_land_tape(replay, seat)
        land_opp_act, land_opp_app = buy_land_tape(replay, opp)
        flag = "W" if rec["win"] else ("T" if rec["tie"] else "L")
        print("=" * 72)
        print(
            eid,
            flag,
            rec["opp"],
            rec["margin"],
            "clone",
            rec["clone"],
            "max_near",
            rec["max_near"],
            "land",
            rec["land"],
            "land_opp",
            rec["land_opp"],
            "Q",
            rec["Q"],
            "herd",
            herd_str(rec["buy_us"]),
            "vs",
            herd_str(rec["buy_opp"]),
            "cash24",
            rec["cash_24"],
            "shops72",
            rec["shops72"],
            "statuses",
            rec["statuses"],
        )
        print("  sheep_us", rec["sheep_steps_us"])
        print("  sheep_opp", rec["sheep_steps_opp"])
        print("  land_act", land_act, "land_app", land_app)
        print("  land_opp_act", land_opp_act, "land_opp_app", land_opp_app)
        after216_us = [b for b in us_buys if b["step"] >= 216]
        after216_opp = [b for b in opp_buys if b["step"] >= 216]
        print("  us_after216", after216_us)
        print("  opp_after216", after216_opp)
        print("  us_all_animals", us_buys)
        print("  opp_all_animals", opp_buys)
        wool[eid] = {}
        for t in (216, 288, 360, 432, 576, 719):
            obs = obs_at(replay, seat, t)
            pr = prices(obs)
            wool[eid][t] = pr.get("WOOL")
            print(
                f"  t={t:3d} cash={farm_money(obs, seat):8.0f}/{farm_money(obs, opp):8.0f} "
                f"Q={farm_q(obs, seat)}/{farm_q(obs, opp)} "
                f"WOOL={pr.get('WOOL')} WHEAT={pr.get('WHEAT')} MILK={pr.get('MILK')}"
            )
    print("WOOL_360", {eid: vals.get(360) for eid, vals in wool.items()})
    print("WOOL_432", {eid: vals.get(432) for eid, vals in wool.items()})


if __name__ == "__main__":
    main()
