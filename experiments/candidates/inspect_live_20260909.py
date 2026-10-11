"""Cash, shops, and six-day route picks on 09-09 rolling losses."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("experiments/candidates/yusuke_sixday")))
from sixday_logic import (  # noqa: E402
    _shops,
    capture_features,
    select_segment_1_live,
    select_segment_3,
    select_segment_4,
    select_segment_4_live,
)

LIVE = Path("artifacts/kaggle_runs/sixday_20260909")
IDS = [
    106950143,
    106889156,
    106891732,
    106869362,
    106949244,
    106937090,
    106911627,
    106868762,
]


def obs_at(replay, seat, t):
    t = min(t, len(replay["steps"]) - 1)
    return replay["steps"][t][seat].get("observation") or {}


def main() -> None:
    for eid in IDS:
        replay = json.loads((LIVE / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index("heralces")
        print("=" * 72, eid, teams)
        for t in (0, 24, 72, 144, 150, 216, 265, 288, 432, 576, 719):
            o = obs_at(replay, seat, t)
            if not o:
                print("  t", t, "no obs")
                continue
            feat = capture_features(o, seat)
            shops = _shops(o)
            print(
                f"  t={t:3d} cash={feat['money']:.0f} gap={feat['cash_gap']:.0f} "
                f"Q={feat['land']:.0f} wool_p={feat['price_wool']:.0f} "
                f"milk_p={feat['price_milk']:.0f} wheat_p={feat['price_wheat']:.0f} "
                f"straw_p={feat['price_strawberry']:.0f} carrot_p={feat['price_carrot']:.0f} "
                f"fert_p={feat['price_fertilizer']:.0f} shops={shops}"
            )
        o144 = obs_at(replay, seat, 144)
        o432 = obs_at(replay, seat, 432)
        o576 = obs_at(replay, seat, 576)
        if o144:
            feat = capture_features(o144, seat)
            print("  s1 live", select_segment_1_live(feat, _shops(o144)))
        if o432:
            feat = capture_features(o432, seat)
            print("  s3", select_segment_3(feat))
        if o576:
            feat = capture_features(o576, seat)
            print("  s4 tree", select_segment_4(feat), "live", select_segment_4_live(feat))
        for t, states in enumerate(replay["steps"]):
            for order in (states[seat].get("action") or {}).get("market") or []:
                if order and order[0] == "BUY_LAND":
                    o = obs_at(replay, seat, max(0, t - 1) if t else 0)
                    farms = o.get("farms") or [{}, {}]
                    money = (farms[seat] or {}).get("money")
                    q = len((farms[seat] or {}).get("unlocked_quadrants") or [])
                    print(f"  BUY_LAND @{t} prev_cash={money} prev_Q={q}")


if __name__ == "__main__":
    main()
