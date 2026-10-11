"""Who stands on (7,4) and (6,2) across the season, and do PASS hands match on other games?"""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
GAMES = [
    ("yusuke_yarn", "episode-102538447-replay.json", "heralces"),
    ("hanserong_clone", "episode-103118692-replay.json", "heralces"),
    ("mtn_yarn", "episode-102571934-replay.json", "heralces"),
    ("lynxx_win", "episode-103051723-replay.json", "heralces"),
]


def tile_log(replay, seat, target):
    hits = []
    for t, states in enumerate(replay["steps"]):
        state = states[seat]
        obs = state.get("observation") or {}
        farm = (obs.get("farms") or [None, None])[seat] or {}
        action = state.get("action") or {}
        farmer = tuple(farm.get("farmer") or [])
        cmds = [action.get("farmer")] + list(action.get("hands") or [])
        positions = [tuple(farm.get("farmer") or [])] + [tuple(p or []) for p in (farm.get("hands") or [])]
        for i, (pos, cmd) in enumerate(zip(positions, cmds)):
            if pos == target:
                hits.append((t, i - 1, cmd))
    return hits


def pass_check(replay, seat):
    ok = True
    details = []
    for t in range(255, 263):
        state = replay["steps"][t][seat]
        obs = state.get("observation") or {}
        farm = (obs.get("farms") or [None, None])[seat] or {}
        action = state.get("action") or {}
        hands = list(farm.get("hands") or [])
        cmds = list(action.get("hands") or [])
        h04 = (tuple(hands[4] or []), cmds[4] if len(cmds) > 4 else None) if len(hands) > 4 else None
        h10 = (tuple(hands[10] or []), cmds[10] if len(cmds) > 10 else None) if len(hands) > 10 else None
        details.append((t, h04, h10))
        if not h04 or h04[0] != (4, 4) or (h04[1] or ["PASS"])[0] != "PASS":
            ok = False
        if not h10 or h10[0] != (4, 4) or (h10[1] or ["PASS"])[0] != "PASS":
            ok = False
    return ok, details


def main() -> None:
    for label, name, team in GAMES:
        path = LIVE / name
        if not path.exists():
            print("MISSING", path)
            continue
        replay = json.loads(path.read_text(encoding="utf-8"))
        seat = replay["info"]["TeamNames"].index(team)
        print("=" * 70, label, replay["info"]["TeamNames"])
        ok, details = pass_check(replay, seat)
        print("h04+h10 PASS at (4,4) 255-262", ok)
        if not ok:
            for row in details:
                print(" ", row)
        for target in ((7, 4), (6, 2), (3, 2)):
            hits = tile_log(replay, seat, target)
            kinds = {}
            for t, idx, cmd in hits:
                op = (cmd or ["PASS"])[0]
                kinds[op] = kinds.get(op, 0) + 1
            print(target, "n", len(hits), "ops", kinds, "first", hits[:6], "last", hits[-4:])


if __name__ == "__main__":
    main()
