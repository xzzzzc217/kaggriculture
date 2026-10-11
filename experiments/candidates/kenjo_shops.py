"""Print shop unlocks for Kenjo specialist vs our yarn/noyarn games."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
GAMES = [
    ("kenjo", "episode-102125420-replay.json", "Kenjo"),
    ("shopbag_yarn", "episode-102538447-replay.json", "heralces"),
    ("shopbag_noyarn", "episode-103118692-replay.json", "heralces"),
    ("shopbag_mtn", "episode-102571934-replay.json", "heralces"),
    ("shopbag_hans", "episode-102007365-replay.json", "heralces"),
]


def main() -> None:
    for label, name, needle in GAMES:
        replay = json.loads((LIVE / name).read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = next(i for i, t in enumerate(teams) if needle.lower() in t.lower())
        seen = []
        for t, states in enumerate(replay["steps"]):
            obs = states[seat].get("observation") or {}
            shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
            if shops != seen:
                print(label, "t", t, shops)
                seen = shops
        print("---")


if __name__ == "__main__":
    main()
