"""Deep-dive Crop Dusta public-12 replays: sell mix, shops, land, live vs tape."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402

REPLAY_DIR = ROOT / "artifacts/kaggle_runs/crop_dusta/extracted"
OUT = ROOT / "experiments/20260828_crop_dusta_strategy.json"
NB = (
    ROOT
    / "artifacts/public_sources/_hunt_20260824b/a-week-four-x-ray-of-the-top-twelve.ipynb"
)

SHOP_DEMAND = {
    "BAKERY": {"EGG": 1, "WHEAT": 1},
    "PIZZA_SHOP": {"MILK": 1, "TOMATO": 1, "WHEAT": 1},
    "BRUNCH_SPOT": {"EGG": 1, "WHEAT": 1, "STRAWBERRY": 1},
    "YARN_STORE": {"WOOL": 2},
    "ICE_CREAM_SHOP": {"STRAWBERRY": 1, "MILK": 1, "WHEAT": 1},
    "PET_CAFE": {"CARROT": 2},
    "SMOOTHIE_SHOP": {"STRAWBERRY": 1, "MILK": 1},
    "FARMERS_MARKET": {"WHEAT": 1, "CARROT": 1, "TOMATO": 1, "STRAWBERRY": 1},
}

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


def shop_demand(shops: list[str]) -> dict[str, int]:
    demand: dict[str, int] = defaultdict(int)
    for name in shops:
        for item, units in SHOP_DEMAND.get(name, {}).items():
            demand[item] += units
    return dict(demand)


def action_prefix_hash(actions: list[str], n: int) -> str:
    blob = "".join(actions[:n]).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def deep_one(path: Path) -> dict:
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = list(replay.get("info", {}).get("TeamNames", []))
    seat = teams.index("Crop Dusta") if "Crop Dusta" in teams else 0
    opp = 1 - seat
    report = summarize(replay, seat, None)
    steps = replay["steps"]

    plants = [Counter(), Counter()]
    animals = [Counter(), Counter()]
    land_steps = [[], []]
    hire_days = [Counter(), Counter()]
    builds = [Counter(), Counter()]
    action_canon = []
    wheat_day = [0] * 30
    tomato_day = [0] * 30
    carrot_day = [0] * 30
    egg_day = [0] * 30
    melon_day = [0] * 30
    shop_names_seen: set[str] = set()
    shops_final: list[str] = []
    shops_by_day: list[list[str]] = []
    money_day: list[dict] = []

    for t, states in enumerate(steps):
        day = min(t // 24, 29)
        obs = states[seat].get("observation") or {}
        town = obs.get("town") or {}
        shops = list(town.get("unlocked_shops") or [])
        shop_names_seen.update(shops)
        if t % 24 == 0:
            shops_by_day.append(shops)
        if t == len(steps) - 1:
            shops_final = shops
        farms = obs.get("farms") or []
        if t % 24 == 23 or t == len(steps) - 1:
            money_day.append(
                {
                    "day": day + 1,
                    "us": float((farms[seat] or {}).get("money", 0.0)),
                    "opp": float((farms[opp] or {}).get("money", 0.0)),
                }
            )
        for who, state in enumerate(states):
            action = state.get("action") or {}
            if who == seat:
                canon = json.dumps(action, sort_keys=True, separators=(",", ":"))
                action_canon.append(canon if action else "")
            farmer = action.get("farmer") or ["PASS"]
            if farmer and farmer[0] == "PLANT" and len(farmer) > 1:
                plants[who][str(farmer[1]).upper()] += 1
            if farmer and farmer[0] in {"BUILD_COOP", "BUILD_PASTURE", "DIG"}:
                builds[who][farmer[0]] += 1
            for hand in action.get("hands") or []:
                if not hand:
                    continue
                if hand[0] == "PLANT" and len(hand) > 1:
                    plants[who][str(hand[1]).upper()] += 1
                if hand[0] in {"BUILD_COOP", "BUILD_PASTURE", "DIG"}:
                    builds[who][hand[0]] += 1
            for order in action.get("market") or []:
                if not order:
                    continue
                op = str(order[0])
                item = str(order[1]).upper() if len(order) > 1 else ""
                qty = int(order[2]) if len(order) > 2 else 1
                if op == "BUY_LAND":
                    land_steps[who].append(t)
                elif op == "HIRE":
                    hire_days[who][day + 1] += 1
                elif op == "BUY_ANIMAL":
                    animals[who][item] += qty
                elif op == "BUY_SEED":
                    plants[who][f"SEED:{item}"] += qty
                elif op == "SELL" and who == seat:
                    if item == "WHEAT":
                        wheat_day[day] += qty
                    elif item == "TOMATO":
                        tomato_day[day] += qty
                    elif item == "CARROT":
                        carrot_day[day] += qty
                    elif item == "EGG":
                        egg_day[day] += qty
                    elif item == "MELON":
                        melon_day[day] += qty

    mq = report["market_order_quantities"]
    mc = report["market_order_counts"]
    our_sig = report["final_public_signatures"][seat]
    opp_sig = report["final_public_signatures"][opp]
    sells = {item: int(mq[seat].get(f"SELL:{item}", 0)) for item in SELL_ITEMS}
    opp_sells = {item: int(mq[opp].get(f"SELL:{item}", 0)) for item in SELL_ITEMS}
    buys = {
        "WHEAT": int(mq[seat].get("BUY_PRODUCT:WHEAT", 0)),
        "FERTILIZER": int(mq[seat].get("BUY_PRODUCT:FERTILIZER", 0)),
    }
    demand = shop_demand(shops_final)
    n_actions = sum(1 for a in action_canon if a and a != "{}")
    return {
        "episode": report["episode_id"],
        "seed": report["seed"],
        "opp": teams[opp] if len(teams) > opp else "",
        "seat": seat,
        "margin": report["margin"],
        "win": report["margin"] > 0,
        "rewards": report["rewards"],
        "Q": our_sig["unlocked_quadrants"],
        "hands": our_sig["hands"],
        "board": our_sig["objects"],
        "opp_board": opp_sig["objects"],
        "clone": {
            "latched": report["clone_gate"]["latched"],
            "max_near": report["clone_gate"]["maximum_near_streak"],
            "median_distance": report["clone_gate"]["median_distance"],
        },
        "sells": sells,
        "opp_sells": opp_sells,
        "buys": buys,
        "buy_land_steps": land_steps[seat],
        "buy_land_n": len(land_steps[seat]),
        "opp_buy_land_n": len(land_steps[opp]),
        "hire_days": dict(hire_days[seat]),
        "max_hires_one_day": max(hire_days[seat].values()) if hire_days[seat] else 0,
        "plants": dict(plants[seat]),
        "animals_bought": dict(animals[seat]),
        "builds": dict(builds[seat]),
        "shops_final": shops_final,
        "shop_counts": dict(Counter(shops_final)),
        "shop_names_seen": sorted(shop_names_seen),
        "shop_demand_per_tick": demand,
        "hashes": {
            "n_logged": n_actions,
            "h24": action_prefix_hash(action_canon, 24),
            "h100": action_prefix_hash(action_canon, 100),
            "h400": action_prefix_hash(action_canon, 400),
            "full": action_prefix_hash(action_canon, len(action_canon)),
        },
        "wheat_by_day": wheat_day,
        "tomato_by_day": tomato_day,
        "carrot_by_day": carrot_day,
        "egg_by_day": egg_day,
        "melon_by_day": melon_day,
        "money_day": money_day,
        "market_order_counts": mc[seat],
        "land_vs_opp": {"us": land_steps[seat], "opp": land_steps[opp]},
    }


def destbreso_cards() -> dict:
    if not NB.exists():
        return {"error": "notebook missing"}
    notebook = json.loads(NB.read_text(encoding="utf-8"))
    hits = []
    for i, cell in enumerate(notebook.get("cells", [])):
        source = cell.get("source") or ""
        if isinstance(source, list):
            source = "".join(source)
        if "Crop Dusta" in source or "crop dusta" in source.lower():
            hits.append({"cell": i, "type": cell.get("cell_type"), "text": source[:6000]})
    return {"n_hits": len(hits), "hits": hits}


def correlate(games: list[dict], shop_key: str, sell_item: str) -> dict:
    xs = []
    ys = []
    for g in games:
        xs.append(int(g["shop_counts"].get(shop_key, 0)))
        ys.append(int(g["sells"].get(sell_item, 0)))
    if not xs:
        return {}
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    var_x = sum((x - mean_x) ** 2 for x in xs)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    r = (cov / (var_x ** 0.5 * (sum((y - mean_y) ** 2 for y in ys) ** 0.5))) if var_x and any(y != mean_y for y in ys) else None
    by_count: dict[str, list[int]] = defaultdict(list)
    for x, y in zip(xs, ys):
        by_count[str(x)].append(y)
    return {
        "shop": shop_key,
        "sell": sell_item,
        "r": None if r is None else round(r, 3),
        "mean_sell_by_shop_count": {k: round(sum(v) / len(v), 1) for k, v in sorted(by_count.items(), key=lambda kv: int(kv[0]))},
        "pairs": list(zip(xs, ys)),
    }


def main() -> None:
    cards = destbreso_cards()
    games = []
    for path in sorted(REPLAY_DIR.glob("episode-*-replay.json")):
        rec = deep_one(path)
        games.append(rec)
        print(
            rec["episode"],
            "W" if rec["win"] else "L",
            rec["margin"],
            "Q",
            rec["Q"],
            "land",
            rec["buy_land_n"],
            rec["buy_land_steps"],
            "W",
            rec["sells"]["WHEAT"],
            "T",
            rec["sells"]["TOMATO"],
            "C",
            rec["sells"]["CARROT"],
            "E",
            rec["sells"]["EGG"],
            "M",
            rec["sells"]["MELON"],
            "shops",
            rec["shop_counts"],
            "hash24",
            rec["hashes"]["h24"],
            "full",
            rec["hashes"]["full"],
            flush=True,
        )

    hashes_full = [g["hashes"]["full"] for g in games]
    hashes_h24 = [g["hashes"]["h24"] for g in games]
    hashes_h100 = [g["hashes"]["h100"] for g in games]
    summary = {
        "n": len(games),
        "wtl": [
            sum(1 for g in games if g["win"]),
            sum(1 for g in games if g["margin"] == 0),
            sum(1 for g in games if not g["win"] and g["margin"] != 0),
        ],
        "mean_margin": sum(g["margin"] for g in games) / len(games),
        "unique_full_sha": len(set(hashes_full)),
        "unique_h24": len(set(hashes_h24)),
        "unique_h100": len(set(hashes_h100)),
        "live": len(set(hashes_full)) == len(games),
        "Q_set": sorted({g["Q"] for g in games}),
        "land_n_set": sorted({g["buy_land_n"] for g in games}),
        "sheep_set": sorted({g["board"].get("SHEEP", 0) for g in games}),
        "cow_set": sorted({g["board"].get("COW", 0) for g in games}),
        "melon_board_set": sorted({g["board"].get("MELON", 0) for g in games}),
        "sell_ranges": {
            item: {
                "min": min(g["sells"][item] for g in games),
                "max": max(g["sells"][item] for g in games),
                "mean": round(sum(g["sells"][item] for g in games) / len(games), 1),
            }
            for item in SELL_ITEMS
        },
        "opp_sell_ranges": {
            item: {
                "min": min(g["opp_sells"][item] for g in games),
                "max": max(g["opp_sells"][item] for g in games),
                "mean": round(sum(g["opp_sells"][item] for g in games) / len(games), 1),
            }
            for item in SELL_ITEMS
        },
        "mean_wheat_by_day": [
            round(sum(g["wheat_by_day"][d] for g in games) / len(games), 1) for d in range(30)
        ],
        "mean_tomato_by_day": [
            round(sum(g["tomato_by_day"][d] for g in games) / len(games), 1) for d in range(30)
        ],
        "mean_carrot_by_day": [
            round(sum(g["carrot_by_day"][d] for g in games) / len(games), 1) for d in range(30)
        ],
        "mean_egg_by_day": [
            round(sum(g["egg_by_day"][d] for g in games) / len(games), 1) for d in range(30)
        ],
        "mean_melon_by_day": [
            round(sum(g["melon_by_day"][d] for g in games) / len(games), 1) for d in range(30)
        ],
        "shop_item_corr": [
            correlate(games, "PIZZA_SHOP", "TOMATO"),
            correlate(games, "FARMERS_MARKET", "TOMATO"),
            correlate(games, "PET_CAFE", "CARROT"),
            correlate(games, "FARMERS_MARKET", "CARROT"),
            correlate(games, "BAKERY", "EGG"),
            correlate(games, "BRUNCH_SPOT", "EGG"),
            correlate(games, "YARN_STORE", "WOOL"),
            correlate(games, "ICE_CREAM_SHOP", "STRAWBERRY"),
            correlate(games, "SMOOTHIE_SHOP", "STRAWBERRY"),
            correlate(games, "PIZZA_SHOP", "MILK"),
            correlate(games, "ICE_CREAM_SHOP", "MILK"),
            correlate(games, "YARN_STORE", "WHEAT"),
            correlate(games, "BAKERY", "WHEAT"),
            correlate(games, "FARMERS_MARKET", "WHEAT"),
        ],
        "losses": [g for g in games if not g["win"]],
        "shop_names_union": sorted({n for g in games for n in g["shop_names_seen"]}),
    }
    payload = {"destbreso": cards, "summary": summary, "games": games}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT)
    print(json.dumps(summary, indent=2, default=str)[:8000])


if __name__ == "__main__":
    main()
