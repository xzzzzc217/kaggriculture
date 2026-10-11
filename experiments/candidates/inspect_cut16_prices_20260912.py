"""Market prices on 09-12 cut16 rolling games (town.goods is empty here)."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/cut16_20260912")
OUR = "heralces"
IDS = [
    108002820,
    108000306,
    107994448,
    107990300,
    107990012,
    107989781,
    107988750,
    107978396,
    107973398,
    107970942,
    107959708,
    107948487,
]


def main() -> None:
    rolling = json.loads(Path("experiments/20260912_cut16_rolling.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in rolling["games"]}
    wool360 = {}
    wool432 = {}
    for eid in IDS:
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        rec = by_id[eid]
        flag = "W" if rec["win"] else "L"
        print("=" * 72)
        print(eid, flag, rec["opp"], rec["margin"], "clone", rec["clone"])
        for t in (216, 288, 360, 432, 576, 719):
            obs = replay["steps"][min(t, len(replay["steps"]) - 1)][seat].get("observation") or {}
            pr = (obs.get("market") or {}).get("prices") or {}
            if t == 360:
                wool360[eid] = pr.get("WOOL")
            if t == 432:
                wool432[eid] = pr.get("WOOL")
            print(
                f"  t={t:3d} WOOL={pr.get('WOOL')} WHEAT={pr.get('WHEAT')} "
                f"MILK={pr.get('MILK')} FERT={pr.get('FERTILIZER')}"
            )
    print("WOOL_360", wool360)
    print("WOOL_432", wool432)


if __name__ == "__main__":
    main()
