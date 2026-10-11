"""Autopsy 2026-09-01 rolling-12 replays for shopbag and v4."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402

LIVE = ROOT / "artifacts/kaggle_runs/top_20260901"
OUR = "heralces"
SELL = ("WHEAT", "WOOL", "MILK", "MELON", "STRAWBERRY", "FERTILIZER", "TOMATO", "CARROT", "EGG")

SHOPBAG = [
    104553501, 104552870, 104550458, 104548685, 104546457, 104544660,
    104542554, 104540767, 104537682, 104534773, 104534234, 104522967,
]
V4 = [
    104549818, 104542146, 104538584, 104537690, 104536693, 104526598,
    104523244, 104513675, 104507580, 104501641, 104486982, 104483421,
]


def shops_at(steps, seat, t):
    obs = steps[t][seat].get("observation") or {}
    return list((obs.get("town") or {}).get("unlocked_shops") or [])


def buys(replay, seat):
    tot = Counter()
    land = []
    pastures = 0
    plants = Counter()
    for t, states in enumerate(replay["steps"]):
        for order in (states[seat].get("action") or {}).get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_ANIMAL":
                tot[str(order[1])] += int(order[2]) if len(order) > 2 else 1
            elif order[0] == "BUY_LAND":
                land.append(t)
            elif order[0] == "BUY_SEED":
                plants[str(order[1])] += int(order[2]) if len(order) > 2 else 1
        for unit in [(states[seat].get("action") or {}).get("farmer")] + list(
            (states[seat].get("action") or {}).get("hands") or []
        ):
            if unit and unit[0] == "BUILD_PASTURE":
                pastures += 1
    return tot, land, pastures, plants


def one(eid: int) -> dict:
    path = LIVE / f"episode-{eid}-replay.json"
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    seat = teams.index(OUR)
    opp = 1 - seat
    report = summarize(replay, seat, None)
    mq = report["market_order_quantities"]
    our_sig = report["final_public_signatures"][seat]
    opp_sig = report["final_public_signatures"][opp]
    us_buy, land, pastures, _plants = buys(replay, seat)
    opp_buy, opp_land, opp_pastures, _ = buys(replay, opp)
    steps = replay["steps"]
    s72 = shops_at(steps, seat, 72) if len(steps) > 72 else []
    s144 = shops_at(steps, seat, 144) if len(steps) > 144 else []
    s216 = shops_at(steps, seat, 216) if len(steps) > 216 else []
    kenjo = bool(s72) and s72[0] == "YARN_STORE"
    rec = {
        "id": eid,
        "opp": teams[opp],
        "seed": replay["info"].get("seed"),
        "margin": report["margin"],
        "win": report["margin"] > 0,
        "tie": report["margin"] == 0,
        "clone": report["clone_gate"]["latched"],
        "max_near": report["clone_gate"]["maximum_near_streak"],
        "kenjo_route": kenjo,
        "shops72": s72,
        "shops144": s144,
        "shops216": s216,
        "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
        "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
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
        "straw": [int(mq[seat].get("SELL:STRAWBERRY", 0)), int(mq[opp].get("SELL:STRAWBERRY", 0))],
        "rewards": report["rewards"],
    }
    return rec


def dump(label, ids):
    rows = []
    print("=" * 70)
    print(label)
    for eid in ids:
        rec = one(eid)
        rows.append(rec)
        mark = "W" if rec["win"] else ("T" if rec["tie"] else "L")
        print(
            f"{eid} {mark} {rec['margin']:+7.0f} vs {rec['opp']!r} "
            f"clone={int(rec['clone'])} kenjo={int(rec['kenjo_route'])} "
            f"near={rec['max_near']} shops72={rec['shops72']} "
            f"buy_us={rec['buy_us']} buy_opp={rec['buy_opp']} "
            f"pasture={rec['pasture']} wheat={rec['wheat']} wool={rec['wool']}"
        )
    return rows


def main() -> None:
    shopbag = dump("shopbag rolling12", SHOPBAG)
    v4 = dump("v4 rolling12", V4)
    out = ROOT / "experiments/20260901_rolling12_autopsy.json"
    out.write_text(json.dumps({"shopbag": shopbag, "v4": v4}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
