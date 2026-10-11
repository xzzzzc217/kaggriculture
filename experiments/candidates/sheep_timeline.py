"""Compare BUY_ANIMAL / pasture timelines: us vs Yusuke/MtN/Hanserong."""

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


def main() -> None:
    for label, (name, team) in GAMES.items():
        path = LIVE / name
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        us = teams.index(team)
        opp = 1 - us
        print("=" * 60, label, teams)
        for who, tag in ((us, "US"), (opp, "OPP")):
            animals = []
            land = []
            pastures = 0
            for t, states in enumerate(replay["steps"]):
                for order in (states[who].get("action") or {}).get("market") or []:
                    if not order:
                        continue
                    if order[0] == "BUY_ANIMAL":
                        animals.append((t, order[1], int(order[2]) if len(order) > 2 else 1))
                    elif order[0] == "BUY_LAND":
                        land.append(t)
                for unit in [(states[who].get("action") or {}).get("farmer")] + list(
                    (states[who].get("action") or {}).get("hands") or []
                ):
                    if unit and unit[0] == "BUILD_PASTURE":
                        pastures += 1
            tot = Counter()
            for _, a, q in animals:
                tot[a] += q
            print(tag, "buys", tot, "land", land, "BUILD_PASTURE", pastures)
            print("  timeline", animals)


if __name__ == "__main__":
    main()
