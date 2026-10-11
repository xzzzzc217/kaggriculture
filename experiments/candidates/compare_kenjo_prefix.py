"""Compare Kenjo 102125420 vs shopbag prefixes. No upload."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")
KENJO = LIVE / "episode-102125420-replay.json"
SHOPBAG_YARN = LIVE / "episode-102538447-replay.json"
SHOPBAG_NOYARN = LIVE / "episode-103118692-replay.json"


def actions(path: Path, team_needle: str) -> list:
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    seat = next(i for i, t in enumerate(teams) if team_needle.lower() in t.lower())
    out = []
    for t in range(len(replay["steps"]) - 1):
        out.append(replay["steps"][t + 1][seat].get("action") or {})
    print(path.name, teams, "seat", seat, "n", len(out))
    return out


def digest(rows) -> str:
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def eq_until(a, b, n) -> int:
    same = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if json.dumps(x, sort_keys=True) != json.dumps(y, sort_keys=True):
            return i
        same = i + 1
        if same >= n:
            break
    return same


def main() -> None:
    kenjo = actions(KENJO, "Kenjo")
    yarn = actions(SHOPBAG_YARN, "heralces")
    noyarn = actions(SHOPBAG_NOYARN, "heralces")
    print("len", len(kenjo), len(yarn), len(noyarn))
    print("shopbag yarn vs noyarn first-diff", eq_until(yarn, noyarn, 720))
    print("kenjo vs shopbag-yarn first-diff", eq_until(kenjo, yarn, 720))
    print("kenjo vs shopbag-noyarn first-diff", eq_until(kenjo, noyarn, 720))
    for n in (24, 72, 100, 144, 151, 218, 266):
        print(
            f"h{n}",
            "kenjo",
            digest(kenjo[:n]),
            "yarn",
            digest(yarn[:n]),
            "noyarn",
            digest(noyarn[:n]),
        )


if __name__ == "__main__":
    main()
