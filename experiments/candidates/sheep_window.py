"""Inspect 200-280 extra-sheep window: money, empty pastures, tape actions."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
GAMES = {
    "yusuke_L": ("episode-102538447-replay.json", "heralces"),
    "mtn_L": ("episode-102571934-replay.json", "heralces"),
    "hanserong_L": ("episode-102007365-replay.json", "heralces"),
    "tk256_W": ("episode-101864457-replay.json", "heralces"),
}
WINDOW = range(200, 281)
FOCUS = (218, 223, 242, 266)


def farm_money(obs, seat):
    farms = obs.get("farms") or []
    if seat >= len(farms):
        return None
    return farms[seat].get("money")


def pasture_stats(obs, seat):
    farms = obs.get("farms") or []
    if seat >= len(farms):
        return {}
    tiles = farms[seat].get("tiles") or []
    empty_pasture = 0
    occupied = Counter()
    empty_unlocked = 0
    locked = 0
    pastures = 0
    for row in tiles:
        for tile in row or []:
            if tile == "LOCKED" or tile == "locked":
                locked += 1
                continue
            if tile is None:
                empty_unlocked += 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "PASTURE":
                pastures += 1
                animal = tile.get("animal")
                if animal:
                    occupied[animal] += 1
                else:
                    empty_pasture += 1
    return {
        "pastures": pastures,
        "empty_pasture": empty_pasture,
        "empty_unlocked": empty_unlocked,
        "occupied": dict(occupied),
        "locked": locked,
    }


def orders(state):
    action = state.get("action") or {}
    market = [list(o) for o in (action.get("market") or []) if o]
    units = [action.get("farmer")] + list(action.get("hands") or [])
    builds = sum(1 for u in units if u and u[0] == "BUILD_PASTURE")
    animals = [o for o in market if o and o[0] == "BUY_ANIMAL"]
    land = [o for o in market if o and o[0] == "BUY_LAND"]
    return market, animals, land, builds


def main() -> None:
    for label, (name, team) in GAMES.items():
        path = LIVE / name
        if not path.exists():
            print("MISSING", path)
            continue
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        us = teams.index(team)
        opp = 1 - us
        print("=" * 70, label, teams)
        for who, tag in ((us, "US"), (opp, "OPP")):
            print("--", tag)
            tot = Counter()
            extra = []
            for t in WINDOW:
                states = replay["steps"][t]
                obs = states[who].get("observation") or {}
                market, animals, land, builds = orders(states[who])
                for o in animals:
                    kind = o[1]
                    qty = int(o[2]) if len(o) > 2 else 1
                    tot[kind] += qty
                    extra.append((t, kind, qty))
                interesting = t in FOCUS or animals or land or builds
                if not interesting:
                    continue
                priv = obs.get("private") or {}
                shed = priv.get("shed") or {}
                shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
                stats = pasture_stats(obs, who)
                print(
                    f"  t={t:3d} money={farm_money(obs, who)} "
                    f"animals={animals} land={land} BUILD_PASTURE={builds} "
                    f"nmarket={len(market)} wheat_shed={shed.get('WHEAT')} "
                    f"shops={shops[:4]} {stats}"
                )
            print("  window buys", dict(tot), "timeline", extra)


if __name__ == "__main__":
    main()
