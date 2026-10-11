"""Measure Giulio / Knight / sbol / Crop Dusta / Yusuke from official replay JSON."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402

LIVE = ROOT / "artifacts/kaggle_runs/top_20260904"
GAMES = [
    ("Giulio Ravasio", 105352975),
    ("Giulio Ravasio", 105352101),
    ("Giulio Ravasio", 105352096),
    ("Giulio Ravasio", 105348549),
    ("Knight of Favonius", 105352143),
    ("Knight of Favonius", 105352100),
    ("Knight of Favonius", 105352099),
    ("Knight of Favonius", 105348550),
    ("sbol ball", 105351728),
    ("sbol ball", 105349460),
    ("sbol ball", 105345918),
    ("sbol ball", 105345853),
    ("Crop Dusta", 105352097),
    ("Crop Dusta", 105348551),
    ("Crop Dusta", 105345024),
    ("Crop Dusta", 105341443),
    ("Yusuke Hayashi", 105353065),
    ("Yusuke Hayashi", 105351792),
    ("Yusuke Hayashi", 105350403),
    ("Yusuke Hayashi", 105349475),
]


def shops_at(steps, seat, t):
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


def main() -> None:
    rows = []
    for team, eid in GAMES:
        path = LIVE / f"episode-{eid}-replay.json"
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
        s72 = shops_at(steps, seat, 72) if len(steps) > 72 else []
        rec = {
            "team": team,
            "id": eid,
            "opp": teams[opp],
            "margin": report["margin"],
            "win": report["margin"] > 0,
            "clone": report["clone_gate"]["latched"],
            "max_near": report["clone_gate"]["maximum_near_streak"],
            "shops72": s72,
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
            "tomato": [int(mq[seat].get("SELL:TOMATO", 0)), int(mq[opp].get("SELL:TOMATO", 0))],
            "carrot": [int(mq[seat].get("SELL:CARROT", 0)), int(mq[opp].get("SELL:CARROT", 0))],
            "egg": [int(mq[seat].get("SELL:EGG", 0)), int(mq[opp].get("SELL:EGG", 0))],
            "straw": [int(mq[seat].get("SELL:STRAWBERRY", 0)), int(mq[opp].get("SELL:STRAWBERRY", 0))],
            "rewards": report["rewards"],
        }
        rows.append(rec)
        flag = "W" if rec["win"] else ("T" if rec["margin"] == 0 else "L")
        print(
            f"{team[:18]:18s} {eid} {flag} {rec['margin']:+7.0f} vs {rec['opp'][:18]:18s} "
            f"clone={int(rec['clone'])} land={land} buy={rec['buy']} "
            f"pasture={rec['pasture'][0]} wheat={rec['wheat'][0]} wool={rec['wool'][0]} "
            f"fert={rec['fert'][0]} melon={rec['melon'][0]} goose={rec['goose'][0]} "
            f"shop0={s72[:1]}"
        )
    out = ROOT / "experiments/20260904_top10_games.json"
    out.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
