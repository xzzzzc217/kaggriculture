"""Measure Jesse Bullard plus Yusuke/Fieldbook extra-sheep buy steps."""

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

TOP = ROOT / "artifacts/kaggle_runs/top_20260905"
FB = ROOT / "artifacts/kaggle_runs/fieldbook_20260905"

JESSE = [105398564, 105398563, 105395068, 105391580]
YUSUKE = [105395079, 105391598, 105388041, 105384084]
FB_GAMES = [
    105398589,
    105397154,
    105394980,
    105394617,
    105394546,
    105394233,
    105394115,
    105390780,
    105390647,
    105388499,
    105385931,
    105385215,
]


def shops_at(steps, seat, t):
    if t >= len(steps):
        t = len(steps) - 1
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


def sheep_timeline(replay, seat):
    steps = replay["steps"]
    events = []
    tot = Counter()
    for t, states in enumerate(steps):
        for order in (states[seat].get("action") or {}).get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_ANIMAL":
                kind = str(order[1])
                qty = int(order[2]) if len(order) > 2 else 1
                tot[kind] += qty
                if kind == "SHEEP":
                    events.append(
                        {
                            "step": t,
                            "day": t // 24 + 1,
                            "qty": qty,
                            "sheep_cum": tot["SHEEP"],
                            "cow_cum": tot["COW"],
                            "shops": shops_at(steps, seat, t),
                        }
                    )
    extra = [e for e in events if e["sheep_cum"] > 5]
    return dict(tot), events, extra


def measure_team(team: str, eid: int, dest: Path) -> dict:
    replay = json.loads((dest / f"episode-{eid}-replay.json").read_text(encoding="utf-8"))
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
    _, _, extra = sheep_timeline(replay, seat)
    return {
        "team": team,
        "id": eid,
        "opp": teams[opp],
        "n_steps": len(steps),
        "statuses": report["statuses"],
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
        "rewards": report["rewards"],
        "extra_sheep_steps": extra,
    }


def main() -> None:
    jesse_rows = []
    for eid in JESSE:
        rec = measure_team("Jesse Bullard", eid, TOP)
        jesse_rows.append(rec)
        extra = [(e["step"], e["qty"], e["sheep_cum"], e["shops"]) for e in rec["extra_sheep_steps"]]
        print(
            f"Jesse {eid} {'W' if rec['win'] else 'L'} {rec['margin']:+7.0f} vs {rec['opp'][:18]:18s} "
            f"clone={int(rec['clone'])} land={rec['land']} buy={rec['buy']} wheat={rec['wheat'][0]} "
            f"melon={rec['melon'][0]} fert={rec['fert'][0]} extra={extra} shop0={rec['shops72'][:1]}"
        )

    yusuke_rows = []
    for eid in YUSUKE:
        rec = measure_team("Yusuke Hayashi", eid, TOP)
        yusuke_rows.append(rec)
        extra = [(e["step"], e["qty"], e["sheep_cum"], e["shops"]) for e in rec["extra_sheep_steps"]]
        print(
            f"Yusuke {eid} buy={rec['buy']} shop0={rec['shops72'][:1]} extra={extra}"
        )

    fb_9c9s = []
    for eid in FB_GAMES:
        path = FB / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        us = teams.index("heralces")
        for seat, label in ((us, "heralces"), (1 - us, teams[1 - us])):
            buy, _events, extra = sheep_timeline(replay, seat)
            if buy.get("SHEEP", 0) >= 9:
                rec = {
                    "id": eid,
                    "team": label,
                    "role": "us" if seat == us else "opp",
                    "buy": buy,
                    "shops72": shops_at(replay["steps"], seat, 72),
                    "extra_sheep_steps": extra,
                }
                fb_9c9s.append(rec)
                print(
                    f"FB {eid} {label[:18]:18s} {rec['role']} buy={buy} "
                    f"extra={[(e['step'], e['qty'], e['sheep_cum'], e['shops']) for e in extra]}"
                )

    out_games = ROOT / "experiments/20260905_top10_games.json"
    out_games.write_text(json.dumps(jesse_rows + yusuke_rows, indent=2) + "\n", encoding="utf-8")
    out_sheep = ROOT / "experiments/20260905_9c9s_sheep_steps.json"
    out_sheep.write_text(
        json.dumps(
            {
                "yusuke_live": [
                    {
                        "id": r["id"],
                        "opp": r["opp"],
                        "buy": r["buy"],
                        "shops72": r["shops72"],
                        "extra_sheep_steps": r["extra_sheep_steps"],
                    }
                    for r in yusuke_rows
                ],
                "jesse": [
                    {
                        "id": r["id"],
                        "buy": r["buy"],
                        "extra_sheep_steps": r["extra_sheep_steps"],
                    }
                    for r in jesse_rows
                ],
                "fieldbook_9c9s": fb_9c9s,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("WROTE", out_games)
    print("WROTE", out_sheep)


if __name__ == "__main__":
    main()
