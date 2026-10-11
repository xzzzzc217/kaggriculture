"""Milan 102248386 animal/pasture timeline (Yusuke base tape)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

PATH = Path("artifacts/kaggle_runs/submission_55840543/extracted/episode-102248386-replay.json")


def main() -> None:
    replay = json.loads(PATH.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    print("teams", teams, "seed", replay["info"].get("seed"))
    seat = teams.index("Milan Leonard") if "Milan Leonard" in teams else 0
    animals = []
    pastures = 0
    land = []
    for t, states in enumerate(replay["steps"]):
        state = states[seat]
        for order in (state.get("action") or {}).get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_ANIMAL":
                animals.append((t, order[1], int(order[2]) if len(order) > 2 else 1))
            elif order[0] == "BUY_LAND":
                land.append(t)
        for unit in [(state.get("action") or {}).get("farmer")] + list(
            (state.get("action") or {}).get("hands") or []
        ):
            if unit and unit[0] == "BUILD_PASTURE":
                pastures += 1
    tot = Counter()
    for _, a, q in animals:
        tot[a] += q
    print("buys", dict(tot), "land", land, "BUILD_PASTURE", pastures)
    print("timeline", animals)


if __name__ == "__main__":
    main()
