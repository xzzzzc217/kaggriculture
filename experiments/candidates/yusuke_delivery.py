"""Dump Yusuke extra-sheep delivery motions after 218/242/266 buys."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
PATH = LIVE / "episode-102538447-replay.json"


def dump_seat(replay, seat, tag, windows):
    print("=" * 70, tag)
    for start, end in windows:
        for t in range(start, end):
            states = replay["steps"][t]
            state = states[seat]
            obs = state.get("observation") or {}
            farms = obs.get("farms") or []
            farm = farms[seat] if seat < len(farms) else {}
            action = state.get("action") or {}
            market = [o for o in (action.get("market") or []) if o and o[0] in ("BUY_ANIMAL", "BUY_LAND")]
            farmer_pos = farm.get("farmer")
            farmer_cmd = action.get("farmer")
            hands = list(farm.get("hands") or [])
            cmds = list(action.get("hands") or [])
            interesting = []
            for i, (pos, cmd) in enumerate(zip(hands, cmds)):
                if cmd and cmd[0] in (
                    "PASS",
                    "BUILD_PASTURE",
                    "PLACE",
                    "PICKUP",
                    "MOVE",
                    "NORTH",
                    "SOUTH",
                    "EAST",
                    "WEST",
                ):
                    if cmd[0] in ("PLACE", "PICKUP", "BUILD_PASTURE") or (
                        cmd[0] in ("NORTH", "SOUTH", "EAST", "WEST") and t in range(start, min(start + 6, end))
                    ):
                        interesting.append((i, pos, cmd))
            if market or (farmer_cmd and farmer_cmd[0] in ("PICKUP", "PLACE", "BUILD_PASTURE")) or interesting:
                print(
                    f"t={t} money={farm.get('money')} farmer={farmer_pos} {farmer_cmd} "
                    f"market={market} extra={interesting[:8]}"
                )


def main() -> None:
    replay = json.loads(PATH.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    us = teams.index("heralces")
    opp = 1 - us
    windows = [(216, 230), (240, 250), (253, 272)]
    dump_seat(replay, us, "US shopbag", windows)
    dump_seat(replay, opp, "OPP Yusuke", windows)


if __name__ == "__main__":
    main()
