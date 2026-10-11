"""Compact autopsy of newest shopbag publics. No upload."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402

LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
IDS = [
    103118692,
    103118565,
    103107429,
    103100831,
    103098542,
    103087386,
    103085035,
    103071706,
    103053960,
    103051746,
    103051723,
    103038310,
]
OUR = "heralces"
SELL = ("WHEAT", "WOOL", "MILK", "MELON", "STRAWBERRY", "FERTILIZER", "CARROT", "TOMATO", "EGG")


def main() -> None:
    rows = []
    for eid in IDS:
        path = LIVE / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        seat = teams.index(OUR)
        opp = 1 - seat
        report = summarize(replay, seat, None)
        mq = report["market_order_quantities"]
        our_sig = report["final_public_signatures"][seat]
        opp_sig = report["final_public_signatures"][opp]
        animals_us = Counter()
        animals_opp = Counter()
        pastures = [0, 0]
        for t, states in enumerate(replay["steps"]):
            for who, bag in ((seat, animals_us), (opp, animals_opp)):
                for order in (states[who].get("action") or {}).get("market") or []:
                    if order and order[0] == "BUY_ANIMAL":
                        bag[str(order[1])] += int(order[2]) if len(order) > 2 else 1
                for unit in [(states[who].get("action") or {}).get("farmer")] + list(
                    (states[who].get("action") or {}).get("hands") or []
                ):
                    if unit and unit[0] == "BUILD_PASTURE":
                        pastures[0 if who == seat else 1] += 1
        rec = {
            "id": eid,
            "opp": teams[opp],
            "margin": report["margin"],
            "win": report["margin"] > 0,
            "clone": report["clone_gate"]["latched"],
            "max_near": report["clone_gate"]["maximum_near_streak"],
            "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
            "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
            "Q": [our_sig["unlocked_quadrants"], opp_sig["unlocked_quadrants"]],
            "bought_us": dict(animals_us),
            "bought_opp": dict(animals_opp),
            "pastures": pastures,
            "sells_us": {k: int(mq[seat].get(f"SELL:{k}", 0)) for k in SELL},
            "sells_opp": {k: int(mq[opp].get(f"SELL:{k}", 0)) for k in SELL},
        }
        rows.append(rec)
        flag = "W" if rec["win"] else "L"
        print(
            f"{eid} {flag} {rec['margin']:+7.0f} {rec['opp']:20s} "
            f"clone={rec['clone']} sheep={rec['sheep']} cow={rec['cow']} "
            f"buy_us={rec['bought_us']} buy_opp={rec['bought_opp']} "
            f"pasture={rec['pastures']} wheat={rec['sells_us']['WHEAT']}/{rec['sells_opp']['WHEAT']} "
            f"wool={rec['sells_us']['WOOL']}/{rec['sells_opp']['WOOL']}"
        )
    wins = sum(1 for r in rows if r["win"])
    print("rolling12", wins, "-", len(rows) - wins, "mean", sum(r["margin"] for r in rows) / len(rows))
    out = ROOT / "experiments/20260830_shopbag_rolling12.json"
    out.write_text(json.dumps({"games": rows}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
