"""Compare Deskbo loss vs Stanislav 11-cow win at reselect steps."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "artifacts/kaggle_runs/sixday_20260907"
OUR = "heralces"


def obs(steps, seat, t):
    return (steps[min(t, len(steps) - 1)][seat].get("observation") or {})


def money(steps, seat, t):
    farms = obs(steps, seat, t).get("farms") or [{}, {}]
    return float((farms[seat] or {}).get("money") or 0), float((farms[1 - seat] or {}).get("money") or 0)


def prices(steps, seat, t):
    market = obs(steps, seat, t).get("market") or {}
    return dict((market.get("prices") or {}))


def shops(steps, seat, t):
    town = obs(steps, seat, t).get("town") or {}
    return list(town.get("unlocked_shops") or [])


def cows_on_board(steps, seat, t, who):
    farms = obs(steps, seat, t).get("farms") or [{}, {}]
    tiles = (farms[who] or {}).get("tiles") or []
    n = 0
    for row in tiles:
        for tile in row or []:
            if isinstance(tile, dict) and tile.get("animal") == "COW":
                n += 1
    return n


def main() -> None:
    for eid in (105744091, 105743208):
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        steps = replay["steps"]
        print("=" * 72)
        print(eid, teams, "n", len(steps))
        for t in (0, 144, 216, 249, 288, 432, 576, 719):
            ours, theirs = money(steps, seat, t)
            pr = prices(steps, seat, t)
            print(
                f" t={t:3d} cash {ours:.0f}/{theirs:.0f} gap {ours-theirs:+.0f}"
                f" cows {cows_on_board(steps, seat, t, seat)}/{cows_on_board(steps, seat, t, opp)}"
                f" wool={pr.get('WOOL')} milk={pr.get('MILK')} straw={pr.get('STRAWBERRY')}"
                f" wheat={pr.get('WHEAT')} shops={shops(steps, seat, t)}"
            )


if __name__ == "__main__":
    main()
