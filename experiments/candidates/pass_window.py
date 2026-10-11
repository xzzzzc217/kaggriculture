"""Dump every unit command in the 254-262 PASS window on shopbag vs Yusuke."""

from __future__ import annotations

import json
from pathlib import Path

PATH = Path("artifacts/kaggle_runs/submission_55840543/extracted/episode-102538447-replay.json")


def dump(replay, seat, tag):
    print("=" * 70, tag)
    for t in range(254, 263):
        states = replay["steps"][t]
        state = states[seat]
        obs = state.get("observation") or {}
        farm = (obs.get("farms") or [None, None])[seat] or {}
        action = state.get("action") or {}
        farmer = farm.get("farmer")
        hands = list(farm.get("hands") or [])
        cmds = [action.get("farmer")] + list(action.get("hands") or [])
        print(f"-- t={t} money={farm.get('money')} farmer={farmer} {cmds[0]}")
        for i, (pos, cmd) in enumerate(zip(hands, cmds[1:])):
            print(f"   h{i:02d} {pos} {cmd}")
        print("   market", action.get("market"))


def main() -> None:
    replay = json.loads(PATH.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    us = teams.index("heralces")
    dump(replay, us, "US")
    dump(replay, 1 - us, "Yusuke")


if __name__ == "__main__":
    main()
