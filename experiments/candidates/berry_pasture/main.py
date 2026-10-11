"""Strawberry-pasture farm from gold-board DSM layouts. Not a metav4 wrap."""
from __future__ import annotations

SHED = ((4, 4), (5, 4), (4, 5), (5, 5))
MELON_TILES = (
    (1, 0), (3, 0), (4, 0), (3, 1), (4, 1),
    (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3), (1, 4),
)
EARLY_WHEAT = ((2, 0), (0, 1), (2, 1), (0, 2), (0, 3), (0, 4))
PERM_BERRY = ((0, 0), (1, 1))
COW_TILES = (
    (4, 2), (4, 4),
    (5, 2), (6, 2), (7, 2),
    (5, 3), (6, 3), (7, 3),
    (5, 4), (6, 4), (7, 4), (8, 4),
)
SHEEP_TILES = (
    (4, 3), (2, 4), (3, 4),
    (4, 5), (4, 6), (4, 7), (4, 8),
    (3, 5), (2, 5), (3, 6),
)
TOMATO_TILES = ((0, 8), (0, 9), (1, 9), (1, 8), (0, 7), (1, 7))
FIRST_YIELD = {"WHEAT": 2, "CARROT": 2, "TOMATO": 8, "STRAWBERRY": 10, "MELON": 10}


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


def _unlocked(pos, quads):
    x, y = pos
    if x < 5 and y < 5:
        return "NW" in quads
    if x >= 5 and y < 5:
        return "NE" in quads
    if x < 5 and y >= 5:
        return "SW" in quads
    return "SE" in quads


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
    tot = {"COW": 0, "SHEEP": 0, "GOOSE": 0, "WHEAT": 0}
    for bag in private.get("inventories") or []:
        if not isinstance(bag, dict):
            continue
        for k in tot:
            tot[k] += int(bag.get(k) or 0)
    return tot


def _scan(farm, day, quads):
    animals = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    pastures, coops, hungry, uncared, fert = [], [], [], [], []
    water, harvest, empties, weeds = [], [], [], []
    berries = tomatoes = melons = 0
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            pos = (x, y)
            if tile is None:
                empties.append(pos)
                continue
            if tile == "LOCKED" or not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
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
            if kind == "PASTURE" and not animal:
                pastures.append(pos)
            if kind == "COOP" and not animal:
                coops.append(pos)
            if kind == "WEED":
                weeds.append(pos)
            if kind == "PLANT":
                crop = tile.get("crop")
                if crop == "STRAWBERRY":
                    berries += 1
                elif crop == "TOMATO":
                    tomatoes += 1
                elif crop == "MELON":
                    melons += 1
                age = day - int(tile.get("planted_day") or 0)
                first = FIRST_YIELD.get(crop, 0)
                if int(tile.get("yield_units") or 0) > 0 and (crop not in FIRST_YIELD or age >= first):
                    harvest.append(pos)
                if not tile.get("watered_today"):
                    water.append(pos)
    return {
        "animals": animals,
        "pastures": pastures,
        "coops": coops,
        "hungry": hungry,
        "uncared": uncared,
        "fert": fert,
        "water": water,
        "harvest": harvest,
        "empties": empties,
        "weeds": weeds,
        "berries": berries,
        "tomatoes": tomatoes,
        "melons": melons,
        "quads": quads,
    }


def _shop_counts(shops):
    c = {}
    for name in shops:
        c[name] = c.get(name, 0) + 1
    return c


def _rival_herd(obs, me):
    farms = obs.get("farms") or []
    if len(farms) < 2:
        return 0, 0
    other = farms[1 - me]
    cows = sheep = 0
    for row in other.get("tiles") or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("animal") == "COW":
                cows += 1
            elif tile.get("animal") == "SHEEP":
                sheep += 1
    return cows, sheep


def _want_cows(day, quads, prices, shops, rival_cows):
    milk = int(prices.get("MILK") or 0)
    pizza = shops.get("PIZZA_SHOP", 0) + shops.get("ICE_CREAM_SHOP", 0)
    if milk < 40 or rival_cows >= 8:
        return 2
    if milk >= 100 and rival_cows <= 4 and day >= 8:
        return 10
    if pizza >= 2 and milk >= 80 and ("NE" in quads or day >= 10):
        return 6
    if day >= 8 and milk >= 80:
        return 4
    return 2


def _want_sheep(day, quads, prices, shops, rival_sheep):
    wool = int(prices.get("WOOL") or 0)
    yarn = shops.get("YARN_STORE", 0)
    if wool < 40 or rival_sheep >= 8:
        return 2
    if wool >= 100 and rival_sheep <= 4 and day >= 8:
        return 8
    if yarn >= 2 and wool >= 80 and ("SW" in quads or day >= 12):
        return 6
    if day >= 10 and wool >= 80:
        return 3
    return 2


def _market(obs, farm, private, scan):
    step = int(obs.get("step", 0) or 0)
    day = int(obs.get("day", step // 24) or 0)
    hour = int(obs.get("hour", step % 24) or 0)
    me = int(obs.get("player", 0) or 0)
    money = float(farm.get("money") or 0)
    shed = dict(private.get("shed") or {})
    seeds = dict(private.get("seeds") or {})
    prices = ((obs.get("market") or {}).get("prices") or {})
    shops = _shop_counts(list((obs.get("town") or {}).get("unlocked_shops") or []))
    rival_cows, rival_sheep = _rival_herd(obs, me)
    orders = []
    spent = 0.0
    if step == 0:
        return []
    if step == 1:
        return [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5]]

    def px(item):
        return int(prices.get(item) or 0)

    def sell(item, cap, floor=1):
        qty = int(shed.get(item) or 0)
        if qty > 0 and px(item) >= floor and len(orders) < 10:
            take = min(qty, cap)
            orders.append(["SELL", item, take])
            shed[item] = qty - take

    n_an = scan["animals"]["COW"] + scan["animals"]["SHEEP"] + scan["animals"]["GOOSE"]
    # Drip-sell premium goods so we do not slam strawberry/melon/wool into the $1 floor.
    sell("STRAWBERRY", 3, 1)
    sell("MELON", 2, 1)
    sell("TOMATO", 3, 1)
    sell("MILK", 4, 1)
    sell("WOOL", 3, 1)
    sell("EGG", 3, 1)
    fert_x = int(shed.get("FERTILIZER") or 0) - 4
    if fert_x > 0:
        sell("FERTILIZER", min(fert_x, 4), 1)

    wheat = int(shed.get("WHEAT") or 0)
    # Never sell feed wheat while we have a herd. The old reserve oscillator
    # sold wheat at $8 and bought it back at $30–55.
    cash_floor = 200 if day < 8 else 150
    hires = int(farm.get("hires_today") or 0)
    hands = len(farm.get("hands") or [])
    if day == 0:
        want_h = 3
    elif day < 8:
        want_h = 6
    else:
        want_h = 8
    if hour <= 8 and money - spent > cash_floor + 20:
        extra = 0
        while hands + extra < want_h and len(orders) < 10:
            cost = _fib(hires + extra)
            if money - spent - cost < cash_floor:
                break
            orders.append(["HIRE"])
            spent += cost
            extra += 1

    quads = farm.get("unlocked_quadrants") or ["NW"]
    nq = len(quads)
    if nq == 1 and day >= 5 and money - spent >= 1200 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        spent += 1000
    elif nq == 2 and day >= 9 and money - spent >= 2500 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        spent += 2000

    carried = _carried(private)
    cows = scan["animals"]["COW"] + int(shed.get("COW") or 0) + carried["COW"]
    sheep = scan["animals"]["SHEEP"] + int(shed.get("SHEEP") or 0) + carried["SHEEP"]
    want_c = _want_cows(day, quads, prices, shops, rival_cows)
    want_s = _want_sheep(day, quads, prices, shops, rival_sheep)

    # Buy feed only while animal products pay for the wheat. vs metav4, milk/wool
    # hit the $1 floor and buying wheat is a death spiral.
    wheat_px = px("WHEAT") or 25
    feed_ok = max(px("MILK"), px("WOOL")) > 2 * wheat_px
    if feed_ok and n_an > 0 and wheat < n_an + 2 and money - spent >= wheat_px + cash_floor and len(orders) < 10:
        need = min(6, max(1, n_an + 2 - wheat))
        orders.append(["BUY_PRODUCT", "WHEAT", need])
        spent += wheat_px * need

    if int(shed.get("COW") or 0) == 0 and carried["COW"] == 0 and day >= 2 and cows < want_c and money - spent >= cash_floor + 800 and px("MILK") >= 70 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "COW", 1])
        spent += 400
    if int(shed.get("SHEEP") or 0) == 0 and carried["SHEEP"] == 0 and day >= 3 and sheep < want_s and money - spent >= cash_floor + 900 and px("WOOL") >= 70 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "SHEEP", 1])
        spent += 500

    if int(seeds.get("MELON") or 0) < 6 and day < 20 and money - spent >= cash_floor + 160 and len(orders) < 10:
        orders.append(["BUY_SEED", "MELON", 2])
        spent += 160
    berry_need = 6 if shops.get("BRUNCH_SPOT") or shops.get("SMOOTHIE_SHOP") or shops.get("ICE_CREAM_SHOP") or shops.get("FARMERS_MARKET") else 4
    if int(seeds.get("STRAWBERRY") or 0) < berry_need and money - spent >= cash_floor + 200 and len(orders) < 10:
        orders.append(["BUY_SEED", "STRAWBERRY", 2])
        spent += 200
    if int(seeds.get("WHEAT") or 0) < 8 and money - spent >= cash_floor + 40 and len(orders) < 10:
        orders.append(["BUY_SEED", "WHEAT", 4])
        spent += 40
    tomato_need = 2 + 2 * (shops.get("PIZZA_SHOP", 0) + shops.get("FARMERS_MARKET", 0))
    if day >= 10 and scan["tomatoes"] + int(seeds.get("TOMATO") or 0) < tomato_need and money - spent >= cash_floor + 100 and len(orders) < 10:
        orders.append(["BUY_SEED", "TOMATO", 2])
        spent += 100
    return orders[:10]


def _commands(obs, farm, private, scan):
    day = int(obs.get("day", 0) or 0)
    hour = int(obs.get("hour", 0) or 0)
    quads = list(farm.get("unlocked_quadrants") or ["NW"])
    seeds = private.get("seeds") or {}
    shed = private.get("shed") or {}
    inventories = list(private.get("inventories") or [{}])
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in (farm.get("hands") or [])]
    while len(inventories) < len(positions):
        inventories.append({})
    n = len(positions)
    cmds = [["PASS"] for _ in range(n)]
    claimed = set()

    def assign(kind, targets, require_wheat=False, limit=99, seed=None):
        placed = 0
        for i, pos in enumerate(positions):
            if placed >= limit or cmds[i] != ["PASS"]:
                continue
            inv = inventories[i]
            if require_wheat and not inv.get("WHEAT"):
                continue
            if seed and int(seeds.get(seed) or 0) <= 0:
                continue
            if pos in targets and pos not in claimed:
                act = _act(kind, inv, seed)
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
            if seed and int(seeds.get(seed) or 0) <= 0:
                continue
            target = _nearest(pos, targets, claimed)
            if target is None:
                continue
            walk = _walk(pos, target)
            cmds[i] = walk or (_act(kind, inv, seed) or ["PASS"])
            claimed.add(target)
            placed += 1

    def _act(kind, inv, seed):
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
        if kind == "DIG":
            return ["DIG"]
        if kind == "PLANT":
            return ["PLANT", seed]
        if kind == "BUILD_P":
            return ["BUILD_PASTURE"]
        return None

    # Carrying an animal: build or place, never buy more while carrying (market already counts inventory).
    for i, inv in enumerate(inventories):
        kind = "COW" if inv.get("COW") else ("SHEEP" if inv.get("SHEEP") else None)
        if not kind:
            continue
        pos = positions[i]
        tile = _tile(farm, pos)
        if tile is None:
            cmds[i] = ["BUILD_PASTURE"]
            continue
        if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and "animal" not in tile:
            cmds[i] = ["PLACE", kind, 1]
            continue
        spots = list(scan["pastures"])
        plan = COW_TILES if kind == "COW" else SHEEP_TILES
        spots.extend([p for p in plan if _tile(farm, p) is None and _unlocked(p, quads)])
        target = _nearest(pos, spots, claimed)
        if target:
            cmds[i] = _walk(pos, target) or ["PASS"]
            claimed.add(target)

    # Pickup animals from shed onto planned tiles.
    if cmds[0] == ["PASS"]:
        take = None
        if scan["animals"]["COW"] < 12 and int(shed.get("COW") or 0) > 0:
            take = "COW"
        elif scan["animals"]["SHEEP"] < 10 and int(shed.get("SHEEP") or 0) > 0:
            take = "SHEEP"
        if take:
            if positions[0] in SHED:
                cmds[0] = ["PICKUP", take, 1]
            else:
                t = _nearest(positions[0], SHED, set())
                if t:
                    cmds[0] = _walk(positions[0], t) or ["PASS"]

    # Get wheat into inventories if animals are hungry.
    if scan["hungry"] and int(shed.get("WHEAT") or 0) > 0:
        for i, pos in enumerate(positions):
            if cmds[i] != ["PASS"]:
                continue
            if inventories[i].get("WHEAT"):
                continue
            if pos in SHED:
                cmds[i] = ["PICKUP", "WHEAT", min(4, int(shed.get("WHEAT") or 0))]
            else:
                t = _nearest(pos, SHED, set())
                if t:
                    cmds[i] = _walk(pos, t) or ["PASS"]

    assign("FEED", scan["hungry"], require_wheat=True)
    assign("HARVEST", scan["harvest"])
    # Water before planting: a seed unwatered on its plant day becomes a weed that night.
    assign("WATER", scan["water"])

    cow_empty = [p for p in COW_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
    sheep_empty = [p for p in SHEEP_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
    if scan["animals"]["COW"] < 12:
        assign("BUILD_P", cow_empty, limit=3)
    if scan["animals"]["SHEEP"] < 10:
        assign("BUILD_P", sheep_empty, limit=2)
    if hour <= 16:
        reserved = set(COW_TILES) | set(SHEEP_TILES) | set(EARLY_WHEAT)
        melon_empty = [p for p in MELON_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
        assign("PLANT", melon_empty, seed="MELON", limit=3)
        wheat_sw = [(x, y) for x in range(0, 4) for y in range(5, 8)]
        wheat_empty = [p for p in list(EARLY_WHEAT) + wheat_sw if _unlocked(p, quads) and _tile(farm, p) is None and p not in set(COW_TILES) | set(SHEEP_TILES)]
        assign("PLANT", wheat_empty, seed="WHEAT", limit=2)
        berry_sites = list(PERM_BERRY)
        if day >= 6:
            berry_sites.extend((x, y) for x in range(5, 10) for y in range(0, 5) if (x, y) not in reserved)
        if day >= 12:
            berry_sites.extend((x, y) for x in range(0, 5) for y in range(7, 10) if (x, y) not in reserved and (x, y) not in TOMATO_TILES)
        berry_empty = [p for p in berry_sites if _unlocked(p, quads) and _tile(farm, p) is None and p not in reserved]
        assign("PLANT", berry_empty, seed="STRAWBERRY", limit=3)
        if day >= 10:
            tomato_empty = [p for p in TOMATO_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
            assign("PLANT", tomato_empty, seed="TOMATO", limit=2)
    assign("CARE", scan["uncared"], limit=4)
    assign("FERT", scan["fert"], limit=2)
    assign("DIG", scan["weeds"], limit=4)

    # Drop produce at shed.
    drop_items = ("MILK", "WOOL", "EGG", "MELON", "TOMATO", "STRAWBERRY", "FERTILIZER")
    for i, pos in enumerate(positions):
        if cmds[i] != ["PASS"]:
            continue
        inv = inventories[i]
        if pos in SHED:
            for item in drop_items:
                if inv.get(item):
                    cmds[i] = ["PLACE", item, int(inv[item])]
                    break
        elif any(inv.get(k) for k in drop_items):
            t = _nearest(pos, SHED, set())
            if t:
                cmds[i] = _walk(pos, t) or ["PASS"]
    return cmds


def agent(observation, configuration=None):
    player = int(observation.get("player", 0) or 0)
    farm = observation["farms"][player]
    private = observation.get("private") or {}
    day = int(observation.get("day", 0) or 0)
    quads = list(farm.get("unlocked_quadrants") or ["NW"])
    scan = _scan(farm, day, quads)
    cmds = _commands(observation, farm, private, scan)
    market = _market(observation, farm, private, scan)
    nh = len(farm.get("hands") or [])
    farmer = cmds[0] if cmds else ["PASS"]
    hands = cmds[1:]
    if len(hands) < nh:
        hands.extend([["PASS"]] * (nh - len(hands)))
    else:
        hands = hands[:nh]
    return {"farmer": farmer, "hands": hands, "market": market}
