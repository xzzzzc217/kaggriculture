"""Cash, land, and BUY_LAND outcomes at six-day land-buy turns."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/sixday_20260908")
IDS = [105797728, 105791046, 105794752, 105798735, 105790145, 105795787]
MARKS = (0, 144, 150, 216, 265, 288, 432, 576, 719)


def obs(steps, seat, t):
    return (steps[min(t, len(steps) - 1)][seat].get("observation") or {})


def main() -> None:
    for eid in IDS:
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index("heralces")
        opp = 1 - seat
        steps = replay["steps"]
        print("=" * 72, eid, teams)
        for t, states in enumerate(steps):
            action = states[seat].get("action") or {}
            for order in action.get("market") or []:
                if order and order[0] == "BUY_LAND":
                    seen = obs(steps, seat, max(0, t - 1))
                    farms = seen.get("farms") or [{}, {}]
                    q = len((farms[seat] or {}).get("unlocked_quadrants") or [])
                    money = (farms[seat] or {}).get("money")
                    print(f"  BUY_LAND action@{t} (obs {t-1}) cash={money} Q={q} market={action.get('market')}")
        prev_q = None
        for t in range(len(steps)):
            farms = obs(steps, seat, t).get("farms") or [{}, {}]
            q = len((farms[seat] or {}).get("unlocked_quadrants") or [])
            if prev_q is not None and q != prev_q:
                print(f"  LAND applied by obs {t} Q {prev_q}->{q}")
            prev_q = q
        for t in MARKS:
            farms = obs(steps, seat, t).get("farms") or [{}, {}]
            prices = (obs(steps, seat, t).get("market") or {}).get("prices") or {}
            shed = (obs(steps, seat, t).get("private") or {}).get("shed") or {}
            print(
                f" t={t:3d} cash={float((farms[seat] or {}).get('money') or 0):.0f}"
                f"/{float((farms[opp] or {}).get('money') or 0):.0f}"
                f" Q={len((farms[seat] or {}).get('unlocked_quadrants') or [])}"
                f" woolp={prices.get('WOOL')} milkp={prices.get('MILK')}"
                f" shedW={shed.get('WHEAT',0)} shedM={shed.get('MILK',0)} shedWo={shed.get('WOOL',0)}"
            )


if __name__ == "__main__":
    main()
