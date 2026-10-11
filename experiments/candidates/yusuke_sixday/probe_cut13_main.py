"""Force last-block route 3 when behind with milk still priced. Probe only."""

from __future__ import annotations

import sixday_logic as sl

_ORIG = sl.select_segment_4_live


def select_segment_4_cut13(features: dict[str, float]) -> int:
    if features["cash_gap"] < 0 and features["price_milk"] > 150:
        return 3
    return _ORIG(features)


sl.select_segment_4_live = select_segment_4_cut13
agent = sl.make_agent()
main = agent
