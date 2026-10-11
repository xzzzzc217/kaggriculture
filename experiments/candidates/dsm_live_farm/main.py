"""DSM-style live farm. Crop-first NW melon + SW tomatoes + small herd."""
from __future__ import annotations

CROPS = {
    "WHEAT": {"first_yield_day": 2},
    "TOMATO": {"first_yield_day": 8},
    "STRAWBERRY": {"first_yield_day": 10},
    "MELON": {"first_yield_day": 10},
}
SHED = ((4, 4), (5, 4), (4, 5), (5, 5))
TOMATO = ((0, 0), (1, 1), (1, 2), (0, 6), (1, 6), (0, 7), (1, 7), (0, 8), (0, 9), (1, 9))
RESERVED = set(TOMATO)


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _walk(pos, target):
    x, y = pos
    tx, ty = target
    if x != tx:
        return ["EAST" if x < tx else "WEST"]
    if y != ty:
        return ["SOUTH" if y < ty else "NORTH"]
    return None


def _tile(farm, pos):
    x, y = pos
    tiles = farm["tiles"]
    if y < 0 or y >= len(tiles) or x < 0 or x >= len(tiles[y]):
        return "LOCKED"
    return tiles[y][x]


def _scan(farm, day):
    animals = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    pastures, coops, hungry, uncared, fert = [], [], [], [], []
    water, harvest, empties = [], [], []
    tomatoes = 0
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            pos = (x, y)
            if tile is None:
                empties.append(pos)
                continue
            if tile == "LOCKED" or not isinstance(tile, dict):
                continue
            animal = tile.get("animal")
            if animal in animals:
                animals[animal] += 1
                if not tile.get("fed_today"):
                    hungry.append(pos)
                if not tile.get("cared_today"):
                    uncared.append(pos)
                if tile.get("fertilizer_available"):
                    fert.append(pos)
                if int(tile.get("yield_units") or 0) > 0:
                    harvest.append(pos)
            if tile.get("kind") == "PASTURE" and not animal:
                pastures.append(pos)
            if tile.get("kind") == "COOP" and not animal:
                coops.append(pos)
            if tile.get("crop") == "TOMATO":
                tomatoes += 1
            if tile.get("kind") == "PLANT":
                crop = tile.get("crop")
                age = day - int(tile.get("planted_day") or 0)
                first = CROPS.get(crop, {}).get("first_yield_day", 0)
                if int(tile.get("yield_units") or 0) > 0 and age >= first:
                    harvest.append(pos)
                elif not tile.get("watered_today"):
                    water.append(pos)
    return locals()


def _nearest(pos, targets, claimed):
    best = None
    best_d = None
    for t in targets:
        if t in claimed:
            continue
        d = abs(pos[0] - t[0]) + abs(pos[1] - t[1])
        if best_d is None or d < best_d:
            best, best_d = t, d
    return best


def _carried(private):
    tot = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for bag in private.get("inventories") or []:
        if isinstance(bag, dict):
            for k in tot:
                tot[k] += int(bag.get(k) or 0)
    return tot


def _market(obs, farm, private, scan):
    step = int(obs.get("step", 0) or 0)
    day = int(obs.get("day", step // 24) or 0)
    hour = int(obs.get("hour", step % 24) or 0)
    money = float(farm.get("money") or 0)
    shed = dict(private.get("shed") or {})
    seeds = dict(private.get("seeds") or {})
    prices = ((obs.get("market") or {}).get("prices") or {})
    orders = []
    spent = 0.0
    if step == 0:
        return []
    if step == 1:
        return [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5]]

    def sell(item, cap, floor):
        qty = int(shed.get(item) or 0)
        if qty > 0 and int(prices.get(item) or 0) >= floor and len(orders) < 10:
            orders.append(["SELL", item, min(qty, cap)])

    n_an = scan["animals"]["COW"] + scan["animals"]["SHEEP"] + scan["animals"]["GOOSE"]
    extra = int(shed.get("WHEAT") or 0) - (n_an + 4)
    if extra > 0:
        sell("WHEAT", 4, 10)
    sell("MILK", 4, 25)
    sell("WOOL", 4, 30)
    sell("EGG", 4, 8)
    sell("TOMATO", 3, 15)
    if int(prices.get("MELON") or 0) >= 130:
        sell("MELON", 1, 130)
    sell("STRAWBERRY", 1, 40)
    fert_x = int(shed.get("FERTILIZER") or 0) - 6
    if fert_x > 0:
        sell("FERTILIZER", 2, 20)

    hires = int(farm.get("hires_today") or 0)
    hands = len(farm.get("hands") or [])
    want = 4 if day == 0 else 10
    if hour <= 2:
        p = 0
        while hands + p < want and len(orders) < 10:
            cost = _fib(hires + p)
            if money - spent < cost + 8:
                break
            orders.append(["HIRE"])
            spent += cost
            p += 1

    quads = len(farm.get("unlocked_quadrants") or ["NW"])
    if quads == 1 and day >= 6 and money - spent >= 3000 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        spent += 1000
    elif quads == 2 and day >= 12 and money - spent >= 8000 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        spent += 2000

    c = _carried(private)
    cows = scan["animals"]["COW"] + int(shed.get("COW") or 0) + c["COW"]
    sheep = scan["animals"]["SHEEP"] + int(shed.get("SHEEP") or 0) + c["SHEEP"]
    geese = scan["animals"]["GOOSE"] + int(shed.get("GOOSE") or 0) + c["GOOSE"]
    if cows < 4 and money - spent >= 500 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "COW", 1])
        spent += 400
    if sheep < 3 and money - spent >= 800 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "SHEEP", 1])
        spent += 500
    if day >= 8 and geese < 2 and money - spent >= 900 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "GOOSE", 1])
        spent += 300

    if int(shed.get("WHEAT") or 0) < n_an + 4 and money - spent >= 80 and len(orders) < 10:
        orders.append(["BUY_PRODUCT", "WHEAT", min(4, n_an + 4 - int(shed.get("WHEAT") or 0))])
        spent += 80
    if int(seeds.get("WHEAT") or 0) < 6 and money - spent >= 40 and len(orders) < 10:
        orders.append(["BUY_SEED", "WHEAT", 2])
        spent += 20
    if 1 <= day < 18 and int(seeds.get("MELON") or 0) < 5 and money - spent >= 160 and len(orders) < 10:
        orders.append(["BUY_SEED", "MELON", 2])
        spent += 160
    if day >= 12 and scan["tomatoes"] + int(seeds.get("TOMATO") or 0) < 10 and money - spent >= 80 and len(orders) < 10:
        orders.append(["BUY_SEED", "TOMATO", 2])
        spent += 100
    return orders[:10]


def _do(kind, inv):
    if kind == "FEED":
        return ["FEED"] if inv.get("WHEAT") else None
    if kind == "CARE":
        return ["CARE"]
    if kind == "HARVEST":
        return ["HARVEST"]
    if kind == "WATER":
        return ["WATER"]
    if kind == "FERT":
        return ["COLLECT_FERTILIZER"]
    if kind.startswith("PLANT_"):
        return ["PLANT", kind.split("_", 1)[1]]
    return None


def _commands(obs, farm, private, scan):
    day = int(obs.get("day", 0) or 0)
    seeds = private.get("seeds") or {}
    shed = private.get("shed") or {}
    inventories = list(private.get("inventories") or [{}])
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in (farm.get("hands") or [])]
    while len(inventories) < len(positions):
        inventories.append({})
    n = len(positions)
    cmds = [["PASS"] for _ in range(n)]
    claimed = set()

    def assign(kind, targets, require_wheat=False, limit=99):
        placed = 0
        for i, pos in enumerate(positions):
            if placed >= limit or cmds[i] != ["PASS"]:
                continue
            inv = inventories[i]
            if require_wheat and not inv.get("WHEAT"):
                continue
            if pos in targets and pos not in claimed:
                act = _do(kind, inv)
                if not act:
                    continue
                cmds[i] = act
                claimed.add(pos)
                placed += 1
        for i, pos in enumerate(positions):
            if placed >= limit or cmds[i] != ["PASS"]:
                continue
            inv = inventories[i]
            if require_wheat and not inv.get("WHEAT"):
                continue
            target = _nearest(pos, targets, claimed)
            if target is None:
                continue
            walk = _walk(pos, target)
            cmds[i] = walk or (_do(kind, inv) or ["PASS"])
            claimed.add(target)
            placed += 1

    for i, inv in enumerate(inventories):
        kind = "COW" if inv.get("COW") else ("SHEEP" if inv.get("SHEEP") else ("GOOSE" if inv.get("GOOSE") else None))
        if not kind:
            continue
        pos = positions[i]
        tile = _tile(farm, pos)
        struct = "COOP" if kind == "GOOSE" else "PASTURE"
        if tile is None:
            cmds[i] = ["BUILD_COOP"] if kind == "GOOSE" else ["BUILD_PASTURE"]
            continue
        if isinstance(tile, dict) and tile.get("kind") == struct and "animal" not in tile:
            cmds[i] = ["PLACE", kind, 1]
            continue
        spots = scan["coops"] if kind == "GOOSE" else scan["pastures"]
        near = [e for e in scan["empties"] if e not in RESERVED]
        near.sort(key=lambda e: abs(e[0] - 4) + abs(e[1] - 4))
        target = _nearest(pos, spots or near[:8], claimed)
        if target:
            cmds[i] = _walk(pos, target) or ["PASS"]
            claimed.add(target)

    want = {"COW": 4, "SHEEP": 3, "GOOSE": 2}
    if cmds[0] == ["PASS"]:
        take = None
        for animal, cap in want.items():
            if scan["animals"].get(animal, 0) < cap and int(shed.get(animal) or 0) > 0:
                take = animal
                break
        if take:
            if positions[0] in SHED:
                cmds[0] = ["PICKUP", take, 1]
            else:
                t = _nearest(positions[0], SHED, set())
                if t:
                    cmds[0] = _walk(positions[0], t) or ["PASS"]

    if scan["hungry"] and shed.get("WHEAT"):
        fed = 0
        for i, pos in enumerate(positions):
            if cmds[i] != ["PASS"] or i == 0:
                continue
            if inventories[i].get("WHEAT"):
                continue
            if fed >= len(scan["hungry"]):
                break
            if pos in SHED:
                cmds[i] = ["PICKUP", "WHEAT", min(3, int(shed.get("WHEAT") or 0))]
            else:
                t = _nearest(pos, SHED, set())
                if t:
                    cmds[i] = _walk(pos, t) or ["PASS"]
            fed += 1

    assign("HARVEST", scan["harvest"])
    assign("FEED", scan["hungry"], require_wheat=True)
    if day >= 12:
        assign("PLANT_TOMATO", [xy for xy in TOMATO if _tile(farm, xy) is None][:6], limit=3)
    assign("WATER", scan["water"])
    assign("CARE", scan["uncared"])
    assign("FERT", scan["fert"])

    crop_empties = [p for p in scan["empties"] if p not in RESERVED and p not in SHED and p[0] <= 7 and p[1] <= 4]
    crop_empties.sort(key=lambda p: abs(p[0] - 3) + abs(p[1] - 3))
    for crop in ("MELON", "WHEAT"):
        if int(seeds.get(crop) or 0) > 0 and crop_empties:
            assign("PLANT_" + crop, crop_empties[:16], limit=8)
            break

    for i, pos in enumerate(positions):
        if cmds[i] != ["PASS"]:
            continue
        inv = inventories[i]
        if pos in SHED:
            for item in ("MILK", "WOOL", "EGG", "MELON", "TOMATO", "STRAWBERRY", "FERTILIZER"):
                if inv.get(item):
                    cmds[i] = ["PLACE", item, int(inv[item])]
                    break
        elif any(inv.get(k) for k in ("MILK", "WOOL", "EGG", "MELON", "TOMATO", "STRAWBERRY", "FERTILIZER")):
            t = _nearest(pos, SHED, set())
            if t:
                cmds[i] = _walk(pos, t) or ["PASS"]
    return cmds


def agent(observation, configuration=None):
    player = int(observation.get("player", 0) or 0)
    farm = observation["farms"][player]
    private = observation.get("private") or {}
    day = int(observation.get("day", 0) or 0)
    try:
        scan = _scan(farm, day)
        cmds = _commands(observation, farm, private, scan)
        market = _market(observation, farm, private, scan)
    except Exception:
        nh = len(farm.get("hands") or [])
        return {"farmer": ["PASS"], "hands": [["PASS"] for _ in range(nh)], "market": []}
    nh = len(farm.get("hands") or [])
    farmer = cmds[0] if cmds else ["PASS"]
    hands = cmds[1:]
    if len(hands) < nh:
        hands.extend([["PASS"]] * (nh - len(hands)))
    else:
        hands = hands[:nh]
    return {"farmer": farmer, "hands": hands, "market": market}
