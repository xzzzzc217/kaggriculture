"""Autopsy shopbag public win/loss replays vs Crop Dusta card."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402

REPLAY_DIR = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
OUT = ROOT / "experiments/20260829_shopbag_public_autopsy.json"
OUR = "heralces"
SELL_ITEMS = (
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
)


def yarn_profile(steps, seat: int) -> dict:
    first_shop_step = None
    first_yarn_step = None
    shops_final: list[str] = []
    first_is_yarn = False
    for t, states in enumerate(steps):
        obs = states[seat].get("observation") or {}
        shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
        if shops and first_shop_step is None:
            first_shop_step = t
            first_is_yarn = shops[0] == "YARN_STORE"
        if "YARN_STORE" in shops and first_yarn_step is None:
            first_yarn_step = t
        if t == len(steps) - 1:
            shops_final = shops
    return {
        "first_shop_step": first_shop_step,
        "first_yarn_step": first_yarn_step,
        "first_shop_is_yarn": first_is_yarn,
        "yarn_count": int(Counter(shops_final)["YARN_STORE"]),
        "shop_counts": dict(Counter(shops_final)),
        "gate_fires": bool(first_yarn_step is not None and first_yarn_step < 217),
        "gate_vs_v189c_differs": bool(first_yarn_step is not None and not first_is_yarn and first_yarn_step < 217),
    }


def one(path: Path) -> dict:
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = list(replay.get("info", {}).get("TeamNames", []))
    seat = teams.index(OUR) if OUR in teams else 0
    opp = 1 - seat
    report = summarize(replay, seat, None)
    mq = report["market_order_quantities"]
    our_sig = report["final_public_signatures"][seat]
    opp_sig = report["final_public_signatures"][opp]
    sells = {item: int(mq[seat].get(f"SELL:{item}", 0)) for item in SELL_ITEMS}
    opp_sells = {item: int(mq[opp].get(f"SELL:{item}", 0)) for item in SELL_ITEMS}
    land = []
    animals = Counter()
    for t, states in enumerate(replay["steps"]):
        for order in (states[seat].get("action") or {}).get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_LAND":
                land.append(t)
            elif order[0] == "BUY_ANIMAL":
                animals[str(order[1]).upper()] += int(order[2]) if len(order) > 2 else 1
    yp = yarn_profile(replay["steps"], seat)
    return {
        "episode": report["episode_id"],
        "seed": report["seed"],
        "opp": teams[opp] if len(teams) > opp else "",
        "seat": seat,
        "margin": report["margin"],
        "win": report["margin"] > 0,
        "tie": report["margin"] == 0,
        "rewards": report["rewards"],
        "Q": [our_sig["unlocked_quadrants"], opp_sig["unlocked_quadrants"]],
        "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
        "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
        "melon": [our_sig["objects"].get("MELON", 0), opp_sig["objects"].get("MELON", 0)],
        "goose": [our_sig["objects"].get("GOOSE", 0), opp_sig["objects"].get("GOOSE", 0)],
        "clone": report["clone_gate"]["latched"],
        "max_near": report["clone_gate"]["maximum_near_streak"],
        "median_distance": report["clone_gate"]["median_distance"],
        "sells": sells,
        "opp_sells": opp_sells,
        "buy_land": land,
        "animals_bought": dict(animals),
        "yarn": yp,
    }


def main() -> None:
    games = []
    for path in sorted(REPLAY_DIR.glob("episode-*-replay.json")):
        rec = one(path)
        games.append(rec)
        mark = "W" if rec["win"] else ("T" if rec["tie"] else "L")
        print(
            mark,
            rec["episode"],
            rec["opp"],
            rec["margin"],
            "W",
            rec["sells"]["WHEAT"],
            rec["opp_sells"]["WHEAT"],
            "F",
            rec["sells"]["FERTILIZER"],
            rec["opp_sells"]["FERTILIZER"],
            "wool",
            rec["sells"]["WOOL"],
            rec["opp_sells"]["WOOL"],
            "shp",
            rec["sheep"],
            "clone",
            rec["clone"],
            "yarn",
            rec["yarn"]["first_yarn_step"],
            "firstY",
            rec["yarn"]["first_shop_is_yarn"],
            "differs",
            rec["yarn"]["gate_vs_v189c_differs"],
            "Q",
            rec["Q"],
            flush=True,
        )
    payload = {
        "n": len(games),
        "wtl": [
            sum(g["win"] for g in games),
            sum(g["tie"] for g in games),
            sum(1 for g in games if not g["win"] and not g["tie"]),
        ],
        "games": games,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
