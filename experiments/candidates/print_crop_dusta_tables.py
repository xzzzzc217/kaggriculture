"""Pretty-print Crop Dusta strategy JSON."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
payload = json.loads(
    (ROOT / "experiments/20260828_crop_dusta_strategy.json").read_text(encoding="utf-8")
)
summary = payload["summary"]
games = payload["games"]

print("H24 unique", summary["unique_h24"], "H100", summary["unique_h100"], "full", summary["unique_full_sha"])
print("mean wheat by day", summary["mean_wheat_by_day"])
print("mean melon by day", summary["mean_melon_by_day"])
print("--- shop correlations ---")
for row in summary["shop_item_corr"]:
    print(row["shop"], row["sell"], "r=", row["r"], row["mean_sell_by_shop_count"])

print("--- per game ---")
header = (
    f"{'ep':>10} {'R':>1} {'mar':>7} {'Wht':>5} {'Car':>4} {'Tom':>4} {'Egg':>4} "
    f"{'Mel':>4} {'Str':>4} {'Mlk':>4} {'Wol':>4} {'Fer':>4} {'shp':>3} {'cow':>3} land"
)
print(header)
for game in games:
    board = game["board"]
    sells = game["sells"]
    mark = "W" if game["win"] else "L"
    print(
        f"{game['episode']:>10} {mark} {game['margin']:7.0f} "
        f"{sells['WHEAT']:5} {sells['CARROT']:4} {sells['TOMATO']:4} {sells['EGG']:4} "
        f"{sells['MELON']:4} {sells['STRAWBERRY']:4} {sells['MILK']:4} {sells['WOOL']:4} "
        f"{sells['FERTILIZER']:4} {board.get('SHEEP', 0):3} {board.get('COW', 0):3} "
        f"{game['buy_land_steps']}"
    )

print("--- plants / animals / hire ---")
for game in games:
    print(
        game["episode"],
        "plants",
        game["plants"],
        "animals",
        game["animals_bought"],
        "builds",
        game["builds"],
        "maxhire",
        game["max_hires_one_day"],
        "hands",
        game["hands"],
        "h100",
        game["hashes"]["h100"],
    )

print("--- losses ---")
for game in games:
    if game["win"]:
        continue
    print("LOSS", game["episode"], game["opp"], game["margin"])
    print("  us ", game["sells"])
    print("  opp", game["opp_sells"])
    print("  shops", game["shop_counts"])
    print("  board", game["board"])
    print("  opp_board", game["opp_board"])
    print("  plants", game["plants"], "animals", game["animals_bought"])

print("--- h100 groups ---")
print(Counter(game["hashes"]["h100"] for game in games))
print("--- h24 groups ---")
print(Counter(game["hashes"]["h24"] for game in games))

print("--- hinge vs shop demand ---")
for game in games:
    demand = game["shop_demand_per_tick"]
    sells = game["sells"]
    print(
        game["episode"],
        "win" if game["win"] else "LOSS",
        "demand",
        {k: demand.get(k, 0) for k in ("TOMATO", "CARROT", "EGG", "WHEAT", "MILK", "WOOL", "STRAWBERRY")},
        "sell T/C/E",
        sells["TOMATO"],
        sells["CARROT"],
        sells["EGG"],
    )
