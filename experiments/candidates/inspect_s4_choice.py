"""What s4 the live tree picks, plus Tatu early cash."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("experiments/candidates/yusuke_sixday")))
from sixday_logic import capture_features, select_segment_4, select_segment_4_live

ROOT = Path("artifacts/kaggle_runs")


def obs_at(replay, seat, t):
    return replay["steps"][t][seat].get("observation") or {}


def main() -> None:
    games = [
        (ROOT / "sixday_20260908" / "episode-105798735-replay.json", "Stefano"),
        (ROOT / "sixday_20260908" / "episode-105790145-replay.json", "fufu"),
        (ROOT / "sixday_20260907" / "episode-105744091-replay.json", "Deskbo"),
        (ROOT / "sixday_20260908" / "episode-105797728-replay.json", "Tatu"),
        (ROOT / "sixday_20260908" / "episode-105791046-replay.json", "Zimin"),
    ]
    for path, name in games:
        replay = json.loads(path.read_text(encoding="utf-8"))
        seat = replay["info"]["TeamNames"].index("heralces")
        print("=" * 72, name)
        for t in (0, 24, 72, 120, 144, 216, 432, 576):
            o = obs_at(replay, seat, t)
            if not o:
                print("  t", t, "no obs")
                continue
            farms = o.get("farms") or [{}, {}]
            feat = capture_features(o, seat)
            print(
                f"  t={t:3d} cash={feat['money']:.0f} gap={feat['cash_gap']:.0f}"
                f" Q={feat['land']:.0f} wheat_p={feat['price_wheat']:.0f}"
                f" wool_p={feat['price_wool']:.0f} milk_p={feat['price_milk']:.0f}"
                f" straw_p={feat['price_strawberry']:.0f} carrot_p={feat['price_carrot']:.0f}"
                f" fert_p={feat['price_fertilizer']:.0f} fert_shed={feat['fertilizer']:.0f}"
            )
        o576 = obs_at(replay, seat, 576)
        if o576:
            feat = capture_features(o576, seat)
            print(
                "  s4 tree",
                select_segment_4(feat),
                "live",
                select_segment_4_live(feat),
            )
        # animals on board at 144
        o144 = obs_at(replay, seat, 144)
        tiles = ((o144.get("farms") or [{}, {}])[seat] or {}).get("tiles") or []
        cows = sheep = 0
        for row in tiles:
            for tile in row or []:
                if isinstance(tile, dict):
                    if tile.get("animal") == "COW":
                        cows += 1
                    elif tile.get("animal") == "SHEEP":
                        sheep += 1
        print("  board at 144 cows/sheep", cows, sheep)


if __name__ == "__main__":
    main()
