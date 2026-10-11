"""Animal timelines for Yusuke's published specialist episodes."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
GAMES = {
    "kenjo_102078489": ("episode-102078489-replay.json", "Kenjo1209"),
    "kenjo_102125420": ("episode-102125420-replay.json", "Kenjo1209"),
    "shuwen_101580708": ("episode-101580708-replay.json", "Shuwen"),
}


def main() -> None:
    for label, (name, needle) in GAMES.items():
        path = LIVE / name
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = next(i for i, t in enumerate(teams) if needle.lower() in t.lower())
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
        print("=" * 60, label, teams, "seat", seat)
        print("buys", dict(tot), "land", land, "BUILD_PASTURE", pastures)
        print("timeline", animals)


if __name__ == "__main__":
    main()
