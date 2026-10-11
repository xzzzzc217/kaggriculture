"""Measure Majkel1337 (CSV/live #1) from official replay JSON. New ids vs 09-13v."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
_spec = importlib.util.spec_from_file_location(
    "kaggriculture_analyze_episode", ROOT / "scripts" / "analyze_episode.py"
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
summarize = _mod.summarize

TOP = ROOT / "artifacts/kaggle_runs/top_20260914c"


def shops_at(steps, seat, t):
    t = min(t, len(steps) - 1)
    obs = steps[t][seat].get("observation") or {}
    return list((obs.get("town") or {}).get("unlocked_shops") or [])


def buys(replay, seat):
    tot = Counter()
    land = []
    pastures = 0
    for t, states in enumerate(replay["steps"]):
        for order in (states[seat].get("action") or {}).get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_ANIMAL":
                tot[str(order[1])] += int(order[2]) if len(order) > 2 else 1
            elif order[0] == "BUY_LAND":
                land.append(t)
        for unit in [(states[seat].get("action") or {}).get("farmer")] + list(
            (states[seat].get("action") or {}).get("hands") or []
        ):
            if unit and unit[0] == "BUILD_PASTURE":
                pastures += 1
    return tot, land, pastures


def herd_str(buy: dict) -> str:
    c = int(buy.get("COW") or 0)
    s = int(buy.get("SHEEP") or 0)
    g = int(buy.get("GOOSE") or 0)
    return f"{c}c{s}s{g}g"


def main() -> None:
    api = json.loads((ROOT / "experiments/20260914c_public_leaderboard_api.json").read_text(encoding="utf-8"))
    ids = list((api.get("picked") or {}).get("picked_ids") or [])
    if not ids:
        ids = [int(p.name.split("-")[1]) for p in sorted(TOP.glob("episode-*-replay.json"))]
    games = [("Majkel1337", eid) for eid in ids]
    rows = []
    for team, eid in games:
        path = TOP / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(team)
        opp = 1 - seat
        report = summarize(replay, seat, None)
        mq = report["market_order_quantities"]
        our_sig = report["final_public_signatures"][seat]
        opp_sig = report["final_public_signatures"][opp]
        us_buy, land, pastures = buys(replay, seat)
        opp_buy, opp_land, opp_pastures = buys(replay, opp)
        steps = replay["steps"]
        rec = {
            "team": team,
            "id": eid,
            "opp": teams[opp],
            "n_steps": len(steps),
            "statuses": report["statuses"],
            "margin": report["margin"],
            "win": report["margin"] > 0,
            "tie": report["margin"] == 0,
            "clone": report["clone_gate"]["latched"],
            "max_near": report["clone_gate"]["maximum_near_streak"],
            "shops72": shops_at(steps, seat, 72),
            "shops144": shops_at(steps, seat, 144),
            "buy": dict(us_buy),
            "buy_opp": dict(opp_buy),
            "pasture": [pastures, opp_pastures],
            "land": land,
            "land_opp": opp_land,
            "Q": [our_sig["unlocked_quadrants"], opp_sig["unlocked_quadrants"]],
            "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
            "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
            "goose": [our_sig["objects"].get("GOOSE", 0), opp_sig["objects"].get("GOOSE", 0)],
            "wheat": [int(mq[seat].get("SELL:WHEAT", 0)), int(mq[opp].get("SELL:WHEAT", 0))],
            "wool": [int(mq[seat].get("SELL:WOOL", 0)), int(mq[opp].get("SELL:WOOL", 0))],
            "milk": [int(mq[seat].get("SELL:MILK", 0)), int(mq[opp].get("SELL:MILK", 0))],
            "fert": [int(mq[seat].get("SELL:FERTILIZER", 0)), int(mq[opp].get("SELL:FERTILIZER", 0))],
            "melon": [int(mq[seat].get("SELL:MELON", 0)), int(mq[opp].get("SELL:MELON", 0))],
            "herd": herd_str(us_buy),
            "rewards": report["rewards"],
        }
        rows.append(rec)
        print(
            f"{eid} {'W' if rec['win'] else 'L'} {rec['margin']:+.0f} vs {rec['opp']} "
            f"land={rec['land']} herd={rec['herd']} wheat={rec['wheat'][0]} "
            f"clone={int(rec['clone'])} Q={rec['Q']} shops72={rec['shops72']} "
            f"shops144={rec['shops144']}",
            flush=True,
        )
    out = ROOT / "experiments/20260914c_top10_games.json"
    out.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
