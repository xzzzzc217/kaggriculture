"""Market prices on 09-10b cut15 rolling games."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut15_20260910b")
OUR = "heralces"
IDS = [
    107579117,
    107578892,
    107574623,
    107572566,
    107571704,
    107571691,
    107571612,
    107572010,
    107570298,
    107570515,
    107569607,
    107568611,
]


def obs_at(replay, seat, t):
    t = min(t, len(replay["steps"]) - 1)
    return replay["steps"][t][seat].get("observation") or {}


def main() -> None:
    for eid in IDS:
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        print("=" * 72, eid, teams)
        for t in (24, 144, 216, 288, 360, 432, 576, 719):
            obs = obs_at(replay, seat, t)
            prices = ((obs.get("market") or {}).get("prices") or {})
            inv = ((obs.get("market") or {}).get("inventory") or {})
            print(
                f"  t={t:3d} wool={prices.get('WOOL')} wheat={prices.get('WHEAT')} "
                f"milk={prices.get('MILK')} fert={prices.get('FERTILIZER')} "
                f"carrot={prices.get('CARROT')} melon={prices.get('MELON')} egg={prices.get('EGG')} "
                f"inv_w={inv.get('WHEAT')} inv_wool={inv.get('WOOL')} inv_milk={inv.get('MILK')}"
            )


if __name__ == "__main__":
    main()
