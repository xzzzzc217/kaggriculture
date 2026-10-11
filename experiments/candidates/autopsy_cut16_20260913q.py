"""Autopsy live cut 16 56151152 newest-12 publics (not the 09-13p cut16 id set)."""

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

LIVE = ROOT / "artifacts/kaggle_runs/cut16_20260913q"
OUR = "heralces"
API = ROOT / "experiments/20260913q_public_leaderboard_api.json"


def shops_at(steps, seat, t):
    t = min(t, len(steps) - 1)
    obs = steps[t][seat].get("observation") or {}
    return list((obs.get("town") or {}).get("unlocked_shops") or [])


def cash_at(steps, seat, t):
    t = min(t, len(steps) - 1)
    obs = steps[t][seat].get("observation") or {}
    farms = obs.get("farms") or [{}, {}]
    farm = farms[seat] if seat < len(farms) else {}
    return float((farm or {}).get("money") or 0)


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


def sheep_buy_steps(replay, seat):
    steps = []
    for t, states in enumerate(replay["steps"]):
        for order in (states[seat].get("action") or {}).get("market") or []:
            if order and order[0] == "BUY_ANIMAL" and order[1] == "SHEEP":
                qty = int(order[2]) if len(order) > 2 else 1
                steps.append({"step": t, "qty": qty})
    return steps


def main() -> None:
    api = json.loads(API.read_text(encoding="utf-8"))
    games = list((api.get("cut16") or {}).get("rolling_ids") or [])
    if len(games) != 12:
        raise SystemExit(f"expected 12 rolling ids, got {games}")
    rows = []
    for eid in games:
        path = LIVE / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        report = summarize(replay, seat, None)
        mq = report["market_order_quantities"]
        our_sig = report["final_public_signatures"][seat]
        opp_sig = report["final_public_signatures"][opp]
        us_buy, land, pastures = buys(replay, seat)
        opp_buy, opp_land, opp_pastures = buys(replay, opp)
        steps = replay["steps"]
        rec = {
            "team": OUR,
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
            "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
            "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
            "goose": [our_sig["objects"].get("GOOSE", 0), opp_sig["objects"].get("GOOSE", 0)],
            "Q": [our_sig["unlocked_quadrants"], opp_sig["unlocked_quadrants"]],
            "buy_us": dict(us_buy),
            "buy_opp": dict(opp_buy),
            "pasture": [pastures, opp_pastures],
            "land": land,
            "land_opp": opp_land,
            "wheat": [int(mq[seat].get("SELL:WHEAT", 0)), int(mq[opp].get("SELL:WHEAT", 0))],
            "wool": [int(mq[seat].get("SELL:WOOL", 0)), int(mq[opp].get("SELL:WOOL", 0))],
            "milk": [int(mq[seat].get("SELL:MILK", 0)), int(mq[opp].get("SELL:MILK", 0))],
            "fert": [int(mq[seat].get("SELL:FERTILIZER", 0)), int(mq[opp].get("SELL:FERTILIZER", 0))],
            "melon": [int(mq[seat].get("SELL:MELON", 0)), int(mq[opp].get("SELL:MELON", 0))],
            "tomato": [int(mq[seat].get("SELL:TOMATO", 0)), int(mq[opp].get("SELL:TOMATO", 0))],
            "carrot": [int(mq[seat].get("SELL:CARROT", 0)), int(mq[opp].get("SELL:CARROT", 0))],
            "egg": [int(mq[seat].get("SELL:EGG", 0)), int(mq[opp].get("SELL:EGG", 0))],
            "rewards": report["rewards"],
            "sheep_steps_us": sheep_buy_steps(replay, seat),
            "sheep_steps_opp": sheep_buy_steps(replay, opp),
            "cash_24": cash_at(steps, seat, 24),
            "cash_144": cash_at(steps, seat, 144),
        }
        rows.append(rec)
        flag = "W" if rec["win"] else ("T" if rec["tie"] else "L")
        print(
            f"{eid} {flag} {rec['margin']:+7.0f} {rec['opp'][:22]:22s} "
            f"n={rec['n_steps']} st={rec['statuses']} clone={int(rec['clone'])} "
            f"Q={rec['Q']} buy_us={rec['buy_us']} buy_opp={rec['buy_opp']} "
            f"wheat={rec['wheat']} wool={rec['wool']} milk={rec['milk']} "
            f"cash24={rec['cash_24']:.0f} land={rec['land']} shops72={rec['shops72']}",
            flush=True,
        )
    out = ROOT / "experiments/20260913q_cut16_rolling.json"
    out.write_text(json.dumps({"games": rows}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
