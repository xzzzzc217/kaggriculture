"""Autopsy v4 public win/loss/tie replays."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402

LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
OUR = "heralces"
GAMES = [
    103758970,
    103683078,
    103678738,
    103676756,
    103649636,
    103591788,
    103694403,
    103616248,
    103772429,
    103767960,
    103752578,
    103638762,
]
SELL = ("WHEAT", "WOOL", "MILK", "MELON", "STRAWBERRY", "FERTILIZER")


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
    for eid in GAMES:
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
        opp_buy, _, opp_pastures = buys(replay, opp)
        steps = replay["steps"]
        s72 = shops_at(steps, seat, 72) if len(steps) > 72 else []
        s144 = shops_at(steps, seat, 144) if len(steps) > 144 else []
        kenjo = bool(s72) and s72[0] == "YARN_STORE"
        rec = {
            "id": eid,
            "opp": teams[opp],
            "margin": report["margin"],
            "win": report["margin"] > 0,
            "tie": report["margin"] == 0,
            "clone": report["clone_gate"]["latched"],
            "max_near": report["clone_gate"]["maximum_near_streak"],
            "kenjo_route": kenjo,
            "shops72": s72,
            "shops144": s144,
            "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
            "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
            "Q": [our_sig["unlocked_quadrants"], opp_sig["unlocked_quadrants"]],
            "buy_us": dict(us_buy),
            "buy_opp": dict(opp_buy),
            "pasture": [pastures, opp_pastures],
            "land": land,
            "wheat": [int(mq[seat].get("SELL:WHEAT", 0)), int(mq[opp].get("SELL:WHEAT", 0))],
            "wool": [int(mq[seat].get("SELL:WOOL", 0)), int(mq[opp].get("SELL:WOOL", 0))],
            "milk": [int(mq[seat].get("SELL:MILK", 0)), int(mq[opp].get("SELL:MILK", 0))],
        }
        rows.append(rec)
        flag = "W" if rec["win"] else ("T" if rec["tie"] else "L")
        print(
            f"{eid} {flag} {rec['margin']:+7.0f} {rec['opp'][:22]:22s} "
            f"kenjo={int(kenjo)} clone={int(rec['clone'])} "
            f"shop0={s72[:1]} shop1={s144[1:2] if len(s144)>1 else []} "
            f"sheep={rec['sheep']} cow={rec['cow']} "
            f"buy_us={rec['buy_us']} buy_opp={rec['buy_opp']} "
            f"pasture={rec['pasture']} wheat={rec['wheat']} wool={rec['wool']}"
        )
    out = ROOT / "experiments/20260831_v4_autopsy.json"
    out.write_text(json.dumps({"games": rows}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
