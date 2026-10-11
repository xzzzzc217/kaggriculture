"""Compare extra-cow Kenjo 102078489 prefix vs shopbag."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/submission_55840543/extracted")


def actions(path: Path, needle: str) -> list:
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    seat = next(i for i, t in enumerate(teams) if needle.lower() in t.lower())
    out = [turn[seat].get("action") or {} for turn in replay["steps"][1:]]
    shops = []
    seen = None
    for t, states in enumerate(replay["steps"]):
        obs = states[seat].get("observation") or {}
        cur = list((obs.get("town") or {}).get("unlocked_shops") or [])
        if cur != seen:
            shops.append((t, cur))
            seen = cur
    print(path.name, teams, "seat", seat, "n", len(out))
    print(" shops", shops[:6])
    return out


def digest(rows) -> str:
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def first_diff(a, b) -> int:
    for i, (x, y) in enumerate(zip(a, b)):
        if json.dumps(x, sort_keys=True) != json.dumps(y, sort_keys=True):
            return i
    return min(len(a), len(b))


def main() -> None:
    kenjo_yarn = actions(LIVE / "episode-102125420-replay.json", "Kenjo")
    kenjo_cow = actions(LIVE / "episode-102078489-replay.json", "Kenjo")
    shop_noyarn = actions(LIVE / "episode-103758970-replay.json", "heralces")
    shop_yarn = actions(LIVE / "episode-103772429-replay.json", "heralces")
    print("cow vs shop_noyarn first-diff", first_diff(kenjo_cow, shop_noyarn))
    print("cow vs yarn-kenjo first-diff", first_diff(kenjo_cow, kenjo_yarn))
    print("yarn-kenjo vs shop_yarn first-diff", first_diff(kenjo_yarn, shop_yarn))
    for n in (24, 72, 100, 144):
        print(
            f"h{n}",
            "cow",
            digest(kenjo_cow[:n]),
            "yarnK",
            digest(kenjo_yarn[:n]),
            "shop",
            digest(shop_noyarn[:n]),
        )


if __name__ == "__main__":
    main()
