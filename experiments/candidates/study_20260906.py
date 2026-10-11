"""Fieldbook newest-12, keiz top-board, Yusuke reselect-vs-patch for 2026-09-06 packet."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments/candidates/yusuke_fieldbook"))
from fieldbook_logic import ROUTES  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "kaggriculture_analyze_episode", ROOT / "scripts" / "analyze_episode.py"
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
summarize = _mod.summarize

FB = ROOT / "artifacts/kaggle_runs/fieldbook_20260906"
TOP = ROOT / "artifacts/kaggle_runs/top_20260906"
OLD_Y = ROOT / "artifacts/kaggle_runs/top_20260905"
OUR = "heralces"
FB_GAMES = [
    105442209,
    105441370,
    105440855,
    105438192,
    105434714,
    105433902,
    105432943,
    105431376,
    105429650,
    105428753,
    105428617,
    105426158,
]
KEIZ = [105440807, 105437334, 105433863, 105433860]
YUSUKE_NEW = [105440805, 105437312]
YUSUKE_OLD = 105395079


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


def sheep_timeline(replay, seat):
    events = []
    tot = Counter()
    for t, states in enumerate(replay["steps"]):
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
                            "qty": qty,
                            "sheep_cum": tot["SHEEP"],
                            "shops": shops_at(replay["steps"], seat, t),
                        }
                    )
    extra = [e for e in events if e["sheep_cum"] > 5]
    return dict(tot), events, extra


def canon(action):
    if not action:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(h or ["PASS"]) for h in (action.get("hands") or [])],
        "market": [list(m) for m in (action.get("market") or [])],
    }


def market_without_sheep(market):
    return [m for m in market if not (m and m[0] == "BUY_ANIMAL" and str(m[1]) == "SHEEP")]


def count_diffs(a, b, lo, hi, ignore_sheep=False):
    farmer = hands = market = 0
    samples = []
    first = None
    for t in range(lo, min(hi, len(a), len(b))):
        ma, mb = a[t]["market"], b[t]["market"]
        if ignore_sheep:
            ma, mb = market_without_sheep(ma), market_without_sheep(mb)
        parts = []
        if a[t]["farmer"] != b[t]["farmer"]:
            farmer += 1
            parts.append("farmer")
        if a[t]["hands"] != b[t]["hands"]:
            hands += 1
            parts.append("hands")
        if ma != mb:
            market += 1
            parts.append("market")
        if parts:
            if first is None:
                first = t
            if len(samples) < 6:
                samples.append({"step": t, "parts": parts, "a_market": ma, "b_market": mb})
    return {"farmer": farmer, "hands": hands, "market": market, "first": first, "samples": samples}


def measure(team, eid, dest):
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
        "tie": report["margin"] == 0,
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
        "fert": [int(mq[seat].get("SELL:FERTILIZER", 0)), int(mq[opp].get("SELL:FERTILIZER", 0))],
        "melon": [int(mq[seat].get("SELL:MELON", 0)), int(mq[opp].get("SELL:MELON", 0))],
        "tomato": [int(mq[seat].get("SELL:TOMATO", 0)), int(mq[opp].get("SELL:TOMATO", 0))],
        "carrot": [int(mq[seat].get("SELL:CARROT", 0)), int(mq[opp].get("SELL:CARROT", 0))],
        "egg": [int(mq[seat].get("SELL:EGG", 0)), int(mq[opp].get("SELL:EGG", 0))],
        "rewards": report["rewards"],
        "extra_sheep_steps": extra,
    }


def autopsy_fieldbook():
    rows = []
    for eid in FB_GAMES:
        rec = measure(OUR, eid, FB)
        rec["buy_us"] = rec.pop("buy")
        rows.append(rec)
        flag = "W" if rec["win"] else ("T" if rec["tie"] else "L")
        print(
            f"{eid} {flag} {rec['margin']:+7.0f} {rec['opp'][:22]:22s} "
            f"clone={int(rec['clone'])} shop0={rec['shops72'][:1]} land={rec['land']} "
            f"buy_us={rec['buy_us']} buy_opp={rec['buy_opp']} pasture={rec['pasture']} "
            f"wheat={rec['wheat']} wool={rec['wool']} fert={rec['fert']} melon={rec['melon']}"
        )
    out = ROOT / "experiments/20260906_fieldbook_rolling12.json"
    out.write_text(json.dumps({"games": rows}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)
    return rows


def load_acts(path, team):
    replay = json.loads(path.read_text(encoding="utf-8"))
    seat = replay["info"]["TeamNames"].index(team)
    acts = [canon((st[seat].get("action") or {})) for st in replay["steps"][:719]]
    return replay, seat, acts


def main() -> None:
    autopsy_fieldbook()
    keiz_rows = []
    for eid in KEIZ:
        rec = measure("keiz", eid, TOP)
        keiz_rows.append(rec)
        extra = [(e["step"], e["qty"], e["sheep_cum"]) for e in rec["extra_sheep_steps"]]
        print(
            f"keiz {eid} {'W' if rec['win'] else 'L'} {rec['margin']:+7.0f} vs {rec['opp'][:18]:18s} "
            f"clone={int(rec['clone'])} land={rec['land']} buy={rec['buy']} wheat={rec['wheat'][0]} "
            f"melon={rec['melon'][0]} fert={rec['fert'][0]} extra={extra} shop0={rec['shops72'][:1]}"
        )
    (ROOT / "experiments/20260906_top10_games.json").write_text(
        json.dumps(keiz_rows, indent=2) + "\n", encoding="utf-8"
    )

    balanced = [canon(a) for a in ROUTES[0]]
    old_replay, old_seat, old_acts = load_acts(OLD_Y / f"episode-{YUSUKE_OLD}-replay.json", "Yusuke Hayashi")
    yusuke_cmp = []
    for eid in YUSUKE_NEW:
        replay, seat, acts = load_acts(TOP / f"episode-{eid}-replay.json", "Yusuke Hayashi")
        vs_old = count_diffs(acts, old_acts, 0, 267, ignore_sheep=False)
        vs_bal_prefix = count_diffs(acts, balanced, 0, 217)
        vs_bal_tail = count_diffs(acts, balanced, 217, 267, ignore_sheep=True)
        vs_old_tail = count_diffs(acts, old_acts, 217, 267, ignore_sheep=True)
        rec = {
            "id": eid,
            "opp": replay["info"]["TeamNames"][1 - seat],
            "shops72": shops_at(replay["steps"], seat, 72),
            "shops216": shops_at(replay["steps"], seat, 216),
            "vs_old_tape_0_266": {k: vs_old[k] for k in ("farmer", "hands", "market", "first")},
            "vs_old_tape_217_266_no_sheep": {k: vs_old_tail[k] for k in ("farmer", "hands", "market", "first")},
            "vs_balanced_0_216": {k: vs_bal_prefix[k] for k in ("farmer", "hands", "market", "first")},
            "vs_balanced_217_266_no_sheep": {k: vs_bal_tail[k] for k in ("farmer", "hands", "market", "first")},
            "balanced_tail_samples": vs_bal_tail["samples"][:4],
        }
        yusuke_cmp.append(rec)
        print(
            f"Yusuke {eid} shop0={rec['shops72'][:1]} vs_old_0_266={rec['vs_old_tape_0_266']} "
            f"vs_BAL_prefix={rec['vs_balanced_0_216']} vs_BAL_tail_no_sheep={rec['vs_balanced_217_266_no_sheep']}"
        )

    # four old games pairwise already known identical; record old vs BALANCED
    vs_bal_old = count_diffs(old_acts, balanced, 0, 217)
    vs_bal_old_tail = count_diffs(old_acts, balanced, 217, 267, ignore_sheep=True)
    payload = {
        "reference_episode": YUSUKE_OLD,
        "reference_shops72": shops_at(old_replay["steps"], old_seat, 72),
        "vs_balanced_0_216": {k: vs_bal_old[k] for k in ("farmer", "hands", "market", "first")},
        "vs_balanced_217_266_no_sheep": {k: vs_bal_old_tail[k] for k in ("farmer", "hands", "market", "first")},
        "balanced_tail_samples": vs_bal_old_tail["samples"][:6],
        "newest_two": yusuke_cmp,
        "pairwise_old_four_identical_0_266": True,
        "verdict": (
            "Neither later-block reselect after 216 nor a Fieldbook BALANCED-tail patch. "
            "Yusuke live 55975994 is one shop-independent action stream through step 266 "
            "(four 09-05 games pairwise identical; two newest games match that tape). "
            "Prefix already differs from Fieldbook BALANCED from step 1 "
            f"(farmer={vs_bal_old['farmer']} hands={vs_bal_old['hands']} market={vs_bal_old['market']}). "
            "After 216, farmer/hands/market still diverge from BALANCED beyond the extra SHEEP buys "
            f"(farmer={vs_bal_old_tail['farmer']} hands={vs_bal_old_tail['hands']} market={vs_bal_old_tail['market']}, first={vs_bal_old_tail['first']}). "
            "Extra SHEEP on that tape: 227/242/266 after a 5th sheep at 218."
        ),
        "is_balanced_tail_patch": False,
        "is_later_block_reselect": False,
    }
    out = ROOT / "experiments/20260906_yusuke_reselect_vs_patch.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("VERDICT", payload["verdict"])
    print("WROTE", out)


if __name__ == "__main__":
    main()
