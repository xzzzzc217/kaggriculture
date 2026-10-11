"""Map empty pastures and nearby PASS hands at extra-sheep steps."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
PATH = LIVE / "episode-102538447-replay.json"
TEAM = "heralces"
STEPS = (218, 223, 242, 250, 255, 258, 266, 267, 268, 269, 270)


def main() -> None:
    replay = json.loads(PATH.read_text(encoding="utf-8"))
    us = replay["info"]["TeamNames"].index(TEAM)
    for t in STEPS:
        states = replay["steps"][t]
        state = states[us]
        obs = state.get("observation") or {}
        farms = obs.get("farms") or []
        farm = farms[us] if us < len(farms) else {}
        tiles = farm.get("tiles") or []
        empty = []
        occupied = []
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row or []):
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                    if "animal" in tile:
                        occupied.append(((x, y), tile.get("animal")))
                    else:
                        empty.append((x, y))
        farmer = farm.get("farmer")
        hands = list(farm.get("hands") or [])
        action = state.get("action") or {}
        units = [action.get("farmer")] + list(action.get("hands") or [])
        print("=" * 60, "t", t, "money", farm.get("money"))
        print("empty pastures", empty)
        print("occupied", occupied)
        print("farmer pos", farmer, "cmd", units[0])
        for i, (pos, cmd) in enumerate(zip(hands, units[1:])):
            if cmd and cmd[0] in ("PASS", "BUILD_PASTURE", "PLACE", "PICKUP", "MOVE") or (
                cmd and cmd[0] == "PASS"
            ):
                if cmd and cmd[0] != "WATER" and cmd[0] != "HARVEST" and cmd[0] != "FEED" and cmd[0] != "CARE":
                    print(f"  hand{i} pos={pos} cmd={cmd}")
        passes = sum(1 for cmd in units if cmd and cmd[0] == "PASS")
        print("PASS count", passes, "n_hands", len(hands), "nmarket", len(action.get("market") or []))


if __name__ == "__main__":
    main()
