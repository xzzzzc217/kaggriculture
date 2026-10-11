"""Glut-aware live farm.

DSM opening, then sticky jobs. When a rival floors berry/milk/wool, stop
planting those premiums, keep the shed from overflowing (sell at $1 rather
than discard), and fill empty land with wheat/carrots/tomatoes.
"""
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
    (3, 3), (7, 4),
)
TOMATO_TILES = ((0, 8), (0, 9), (1, 9), (1, 8), (0, 7), (1, 7))
FIRST_YIELD = {"WHEAT": 2, "CARROT": 2, "TOMATO": 8, "STRAWBERRY": 10, "MELON": 10}

OPENING = [
    {"f": ["PASS"], "h": [], "m": []},
    {"f": ["PASS"], "h": [], "m": [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5]]},
    {"f": ["PICKUP", "COW", 1], "h": [], "m": [["SELL", "WHEAT", 1], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["BUY_ANIMAL", "COW", 1], ["BUY_ANIMAL", "SHEEP", 3]]},
    {"f": ["BUILD_PASTURE"], "h": [["PICKUP", "SHEEP", 1], ["PICKUP", "SHEEP", 1], ["PICKUP", "COW", 1], ["PICKUP", "SHEEP", 1]], "m": [["SELL", "WHEAT", 1]]},
    {"f": ["PLACE", "COW", 1], "h": [["NORTH"], ["NORTH"], ["NORTH"], ["WEST"]], "m": [["SELL", "WHEAT", 1], ["BUY_PRODUCT", "WHEAT", 1]]},
    {"f": ["PICKUP", "WHEAT", 3], "h": [["WEST"], ["WEST"], ["NORTH"], ["BUILD_PASTURE"]], "m": [["SELL", "WHEAT", 1], ["BUY_PRODUCT", "WHEAT", 1]]},
    {"f": ["FEED"], "h": [["BUILD_PASTURE"], ["WEST"], ["NORTH"], ["PLACE", "SHEEP", 1]], "m": [["SELL", "WHEAT", 1], ["BUY_PRODUCT", "WHEAT", 1]]},
    {"f": ["WEST"], "h": [["PLACE", "SHEEP", 1], ["BUILD_PASTURE"], ["WEST"], ["CARE"]], "m": [["BUY_SEED", "MELON", 2], ["BUY_PRODUCT", "WHEAT", 1]]},
    {"f": ["FEED"], "h": [["CARE"], ["PLACE", "SHEEP", 1], ["BUILD_PASTURE"], ["WEST"]], "m": []},
]

_STICKY = {}
_LAST_STEP = {}


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


def _sticky_map(player, step, hour):
    prev = _LAST_STEP.get(player)
    if prev is None or step < prev or hour == 0:
        _STICKY[player] = {}
    _LAST_STEP[player] = step
    return _STICKY[player]


def _scan(farm, day, quads):
    animals = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    pastures, coops, hungry, uncared, fert = [], [], [], [], []
    water, harvest, empties, weeds = [], [], [], []
    berries = tomatoes = melons = wheat = 0
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
                elif crop == "WHEAT":
                    wheat += 1
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
        "wheat": wheat,
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
        return 5
    if yarn >= 2 and wool >= 80:
        return 5
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
    if step <= 8:
        return []

    def px(item):
        return int(prices.get(item) or 0)

    def sell(item, cap, floor=1):
        qty = int(shed.get(item) or 0)
        if qty > 0 and px(item) >= floor and len(orders) < 10:
            take = min(qty, cap)
            orders.append(["SELL", item, take])
            shed[item] = qty - take

    n_an = scan["animals"]["COW"] + scan["animals"]["SHEEP"] + scan["animals"]["GOOSE"]
    shed_n = sum(int(v or 0) for v in shed.values())
    # Overflow path: never let the shed sit full while harvests dump.
    overflow = shed_n >= 70 or day >= 28
    straw_px, milk_px, wool_px, melon_px = px("STRAWBERRY"), px("MILK"), px("WOOL"), px("MELON")
    sell("EGG", 8, 1 if overflow else 8)
    sell("TOMATO", 8, 1 if overflow else 12)
    sell("CARROT", 8, 1 if overflow else 10)
    sell("MILK", 8 if overflow or milk_px < 40 else 4, 1 if overflow or milk_px < 40 else 50)
    sell("WOOL", 8 if overflow or wool_px < 40 else 3, 1 if overflow or wool_px < 40 else 50)
    sell("STRAWBERRY", 8 if overflow or straw_px < 30 else 3, 1 if overflow or straw_px < 30 else 40)
    sell("MELON", 6 if overflow or melon_px < 50 else 2, 1 if overflow or melon_px < 50 else 80)
    fert_x = int(shed.get("FERTILIZER") or 0) - (0 if overflow else 2)
    if fert_x > 0:
        sell("FERTILIZER", min(fert_x, 8), 1)

    wheat = int(shed.get("WHEAT") or 0)
    cash_floor = 200 if day < 8 else 150
    hires = int(farm.get("hires_today") or 0)
    hands = len(farm.get("hands") or [])
    if (hands < 6 or money < 150) and wheat > n_an + 3:
        sell("WHEAT", wheat - n_an - 3, 1)
        wheat = int(shed.get("WHEAT") or 0)
    if day == 0:
        want_h, min_h = 4, 4
    elif day < 8:
        want_h, min_h = 8, 8
    else:
        want_h, min_h = 11, 8
    if hour <= 8:
        extra = 0
        while hands + extra < want_h and len(orders) < 10:
            cost = _fib(hires + extra)
            floor = 15 if hands + extra < min_h else cash_floor
            if money - spent - cost < floor:
                break
            orders.append(["HIRE"])
            spent += cost
            extra += 1

    quads = farm.get("unlocked_quadrants") or ["NW"]
    nq = len(quads)
    if nq == 1 and money - spent >= 1200 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        spent += 1000
    elif nq == 2 and day >= 8 and money - spent >= 2500 and len(orders) < 10:
        orders.append(["BUY_LAND"])
        spent += 2000

    carried = _carried(private)
    cows = scan["animals"]["COW"] + int(shed.get("COW") or 0) + carried["COW"]
    sheep = scan["animals"]["SHEEP"] + int(shed.get("SHEEP") or 0) + carried["SHEEP"]
    want_c = _want_cows(day, quads, prices, shops, rival_cows)
    want_s = min(5, _want_sheep(day, quads, prices, shops, rival_sheep))

    wheat_px = px("WHEAT") or 25
    feed_ok = max(px("MILK"), px("WOOL")) > 2 * wheat_px
    if feed_ok and n_an > 0 and wheat < n_an + 2 and money - spent >= wheat_px + cash_floor and len(orders) < 10:
        need = min(6, max(1, n_an + 2 - wheat))
        orders.append(["BUY_PRODUCT", "WHEAT", need])
        spent += wheat_px * need

    if milk_px < 45:
        want_c = min(want_c, 4)
    if wool_px < 45:
        want_s = min(want_s, 3)
    if int(shed.get("COW") or 0) == 0 and carried["COW"] == 0 and day >= 2 and cows < want_c and money - spent >= cash_floor + 800 and milk_px >= 45 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "COW", 1])
        spent += 400
    if int(shed.get("SHEEP") or 0) == 0 and carried["SHEEP"] == 0 and day >= 3 and sheep < want_s and money - spent >= cash_floor + 900 and wool_px >= 45 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "SHEEP", 1])
        spent += 500

    if straw_px >= 35 and int(seeds.get("MELON") or 0) < 6 and day < 20 and money - spent >= cash_floor + 160 and melon_px >= 80 and len(orders) < 10:
        orders.append(["BUY_SEED", "MELON", 2])
        spent += 160
    berry_need = 0 if straw_px < 35 else (16 if "NE" in quads else 4)
    have_b = int(seeds.get("STRAWBERRY") or 0)
    if have_b < berry_need and money - spent >= cash_floor + 200 and len(orders) < 10:
        n = 4 if money - spent >= 2000 else 2
        n = min(n, berry_need - have_b, int((money - spent - cash_floor) // 100))
        if n > 0:
            orders.append(["BUY_SEED", "STRAWBERRY", n])
            spent += 100 * n
    wheat_need = 16 if "SW" in quads or day >= 18 else 8
    if int(seeds.get("WHEAT") or 0) < wheat_need and money - spent >= cash_floor + 40 and len(orders) < 10:
        n = min(8, wheat_need - int(seeds.get("WHEAT") or 0))
        orders.append(["BUY_SEED", "WHEAT", n])
        spent += 10 * n
    tomato_need = 2 + 2 * (shops.get("PIZZA_SHOP", 0) + shops.get("FARMERS_MARKET", 0))
    if day >= 10 and scan["tomatoes"] + int(seeds.get("TOMATO") or 0) < tomato_need and money - spent >= cash_floor + 100 and len(orders) < 10:
        orders.append(["BUY_SEED", "TOMATO", 2])
        spent += 100
    return orders[:10]


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
    if kind == "FERTILIZE":
        return ["FERTILIZE"] if inv.get("FERTILIZER") else None
    return None


def _job_valid(kind, target, seed, farm, scan, inv, seed_left, day=0):
    tile = _tile(farm, target)
    if kind == "WATER":
        return isinstance(tile, dict) and tile.get("kind") == "PLANT" and not tile.get("watered_today")
    if kind == "PLANT":
        return tile is None and int(seed_left.get(seed) or 0) > 0
    if kind == "FEED":
        return target in scan["hungry"]
    if kind == "HARVEST":
        return target in scan["harvest"]
    if kind == "DIG":
        return isinstance(tile, dict) and tile.get("kind") == "WEED"
    if kind == "BUILD_P":
        return tile is None
    if kind == "CARE":
        return target in scan["uncared"]
    if kind == "FERT":
        return target in scan["fert"]
    if kind == "FERTILIZE":
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") == "STRAWBERRY"):
            return False
        if int(tile.get("fertilized_until_day") or -1) >= day:
            return False
        return bool(inv.get("FERTILIZER"))
    return False


def _commands(obs, farm, private, scan):
    day = int(obs.get("day", 0) or 0)
    hour = int(obs.get("hour", 0) or 0)
    step = int(obs.get("step", 0) or 0)
    player = int(obs.get("player", 0) or 0)
    quads = list(farm.get("unlocked_quadrants") or ["NW"])
    seed_left = dict(private.get("seeds") or {})
    shed = private.get("shed") or {}
    inventories = list(private.get("inventories") or [{}])
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in (farm.get("hands") or [])]
    while len(inventories) < len(positions):
        inventories.append({})
    n = len(positions)
    cmds = [["PASS"] for _ in range(n)]
    claimed = set()
    sticky = _sticky_map(player, step, hour)
    fert_tgts = []

    def set_job(i, kind, target, seed=None):
        sticky[i] = (kind, target[0], target[1], seed)
        claimed.add(target)

    def clear_job(i):
        sticky.pop(i, None)

    for i, inv in enumerate(inventories):
        kind = "COW" if inv.get("COW") else ("SHEEP" if inv.get("SHEEP") else None)
        if not kind:
            continue
        pos = positions[i]
        tile = _tile(farm, pos)
        clear_job(i)
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

    behind = len(scan["water"]) > max(4, n)
    for i, pos in enumerate(positions):
        if cmds[i] != ["PASS"]:
            continue
        job = sticky.get(i)
        if not job:
            continue
        kind, tx, ty, seed = job
        target = (tx, ty)
        if behind and kind in ("PLANT", "BUILD_P", "DIG", "CARE", "FERTILIZE"):
            clear_job(i)
            continue
        if target in claimed:
            clear_job(i)
            continue
        if not _job_valid(kind, target, seed, farm, scan, inventories[i], seed_left, day):
            clear_job(i)
            continue
        if kind == "FEED" and not inventories[i].get("WHEAT"):
            if int(shed.get("WHEAT") or 0) <= 0:
                clear_job(i)
                continue
            if pos in SHED:
                cmds[i] = ["PICKUP", "WHEAT", min(4, int(shed.get("WHEAT") or 0))]
            else:
                t = _nearest(pos, SHED, set())
                cmds[i] = _walk(pos, t) or ["PASS"] if t else ["PASS"]
            claimed.add(target)
            continue
        claimed.add(target)
        if pos == target:
            act = _act(kind, inventories[i], seed)
            if not act:
                clear_job(i)
                continue
            cmds[i] = act
            if kind == "PLANT":
                seed_left[seed] = int(seed_left.get(seed) or 0) - 1
                sticky[i] = ("WATER", tx, ty, None)
            else:
                clear_job(i)
        else:
            cmds[i] = _walk(pos, target) or ["PASS"]

    def assign(kind, targets, require_wheat=False, limit=99, seed=None):
        placed = 0
        order = []
        for i, pos in enumerate(positions):
            if cmds[i] != ["PASS"]:
                continue
            inv = inventories[i]
            if require_wheat and not inv.get("WHEAT"):
                continue
            if seed and int(seed_left.get(seed) or 0) <= 0:
                continue
            order.append(i)
        order.sort(key=lambda i: 0 if positions[i] in targets and positions[i] not in claimed else 1)
        for i in order:
            if placed >= limit or cmds[i] != ["PASS"]:
                continue
            inv = inventories[i]
            if require_wheat and not inv.get("WHEAT"):
                continue
            if seed and int(seed_left.get(seed) or 0) <= 0:
                continue
            pos = positions[i]
            if pos in targets and pos not in claimed:
                target = pos
            else:
                target = _nearest(pos, targets, claimed)
            if target is None:
                continue
            act = _act(kind, inv, seed)
            if pos == target:
                if not act:
                    continue
                cmds[i] = act
                claimed.add(target)
                if kind == "PLANT":
                    seed_left[seed] = int(seed_left.get(seed) or 0) - 1
                    sticky[i] = ("WATER", target[0], target[1], None)
                else:
                    clear_job(i)
            else:
                cmds[i] = _walk(pos, target) or ["PASS"]
                set_job(i, kind, target, seed)
            placed += 1

    if cmds[0] == ["PASS"]:
        take = None
        if scan["animals"]["COW"] < 12 and int(shed.get("COW") or 0) > 0:
            take = "COW"
        elif scan["animals"]["SHEEP"] < 5 and int(shed.get("SHEEP") or 0) > 0:
            take = "SHEEP"
        if take:
            if positions[0] in SHED:
                cmds[0] = ["PICKUP", take, 1]
            else:
                t = _nearest(positions[0], SHED, set())
                if t:
                    cmds[0] = _walk(positions[0], t) or ["PASS"]

    if scan["hungry"] and int(shed.get("WHEAT") or 0) > 0:
        sent = 0
        need = min(4, len(scan["hungry"]))
        for i, pos in enumerate(positions):
            if sent >= need or cmds[i] != ["PASS"]:
                continue
            if inventories[i].get("WHEAT"):
                continue
            if pos in SHED:
                cmds[i] = ["PICKUP", "WHEAT", min(4, int(shed.get("WHEAT") or 0))]
                sent += 1
            elif sent < 2:
                t = _nearest(pos, SHED, set())
                if t:
                    cmds[i] = _walk(pos, t) or ["PASS"]
                    sent += 1

    assign("FEED", scan["hungry"], require_wheat=True, limit=min(8, n))
    assign("WATER", scan["water"])
    plant_hv = [p for p in scan["harvest"] if isinstance(_tile(farm, p), dict) and _tile(farm, p).get("kind") == "PLANT"]
    animal_hv = [p for p in scan["harvest"] if p not in plant_hv]
    assign("HARVEST", plant_hv)
    assign("HARVEST", animal_hv)

    # Fertilize strawberries with fertilizer already in hand (collected last
    # turn). Feed/water/harvest already took those workers, so this does not
    # pull the milk crew.
    fert_tgts = []
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") != "PLANT" or tile.get("crop") != "STRAWBERRY":
                continue
            if int(tile.get("fertilized_until_day") or -1) >= day:
                continue
            fert_tgts.append((x, y))
    if fert_tgts and day >= 12:
        placed = 0
        for i, pos in enumerate(positions):
            if placed >= 4 or cmds[i] != ["PASS"]:
                continue
            if not inventories[i].get("FERTILIZER"):
                continue
            if pos in fert_tgts:
                cmds[i] = ["FERTILIZE"]
                placed += 1
                continue
            target = _nearest(pos, fert_tgts, set())
            if target is None:
                continue
            if abs(pos[0] - target[0]) + abs(pos[1] - target[1]) > 2:
                continue
            cmds[i] = _walk(pos, target) or ["FERTILIZE"]
            placed += 1

    assign("FERT", scan["fert"], limit=8)

    reserved = set(COW_TILES) | set(SHEEP_TILES) | set(EARLY_WHEAT) | set(MELON_TILES)
    berry_sites = list(PERM_BERRY)
    if "NE" in quads:
        berry_sites.extend((x, y) for x in range(5, 10) for y in range(0, 5) if (x, y) not in reserved)
    if "SW" in quads:
        berry_sites.extend((x, y) for x in range(2, 5) for y in range(5, 9) if (x, y) not in reserved and (x, y) not in TOMATO_TILES)
    wheat_sites = list(EARLY_WHEAT)
    if "SW" in quads:
        wheat_sites.extend((x, y) for x in range(0, 2) for y in range(5, 10))
        wheat_sites.extend((x, 9) for x in range(2, 5))
    if day >= 20:
        wheat_sites.extend(berry_sites)

    berry_empty = [p for p in berry_sites if _unlocked(p, quads) and _tile(farm, p) is None]
    wheat_empty = [p for p in wheat_sites if _unlocked(p, quads) and _tile(farm, p) is None and p not in reserved]
    weeds = [p for p in berry_sites + wheat_sites if isinstance(_tile(farm, p), dict) and _tile(farm, p).get("kind") == "WEED"]
    if weeds:
        assign("DIG", weeds, limit=4)

    if hour <= 16:
        early_wheat_empty = [p for p in EARLY_WHEAT if _unlocked(p, quads) and _tile(farm, p) is None]
        if early_wheat_empty and int(seed_left.get("WHEAT") or 0) > 0:
            assign("PLANT", early_wheat_empty, seed="WHEAT", limit=2)
        prices = ((obs.get("market") or {}).get("prices") or {})
        straw_px = int(prices.get("STRAWBERRY") or 0)
        if day < 20 and berry_empty and int(seed_left.get("STRAWBERRY") or 0) > 0 and straw_px >= 35:
            assign("PLANT", berry_empty, seed="STRAWBERRY", limit=4)
        elif berry_empty and int(seed_left.get("WHEAT") or 0) > 0:
            assign("PLANT", berry_empty, seed="WHEAT", limit=4)
        if wheat_empty and int(seed_left.get("WHEAT") or 0) > 0:
            assign("PLANT", wheat_empty, seed="WHEAT", limit=2)

    cow_empty = [p for p in COW_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
    sheep_empty = [p for p in SHEEP_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
    if scan["animals"]["COW"] < 12 and len(scan["pastures"]) < 3:
        assign("BUILD_P", cow_empty, limit=2)
    if scan["animals"]["SHEEP"] < 5 and len(scan["pastures"]) < 3:
        assign("BUILD_P", sheep_empty, limit=1)
    if hour <= 16:
        melon_empty = [p for p in MELON_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
        assign("PLANT", melon_empty, seed="MELON", limit=3)
        if day >= 10:
            tomato_empty = [p for p in TOMATO_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
            assign("PLANT", tomato_empty, seed="TOMATO", limit=2)
    assign("CARE", scan["uncared"], limit=8)
    assign("DIG", scan["weeds"], limit=4)

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


def _pad_hands(hands, n):
    hands = [list(h) for h in (hands or [])]
    while len(hands) < n:
        hands.append(["PASS"])
    return hands[:n]


def agent(observation, configuration=None):
    player = int(observation.get("player", 0) or 0)
    farm = observation["farms"][player]
    private = observation.get("private") or {}
    step = int(observation.get("step", 0) or 0)
    day = int(observation.get("day", 0) or 0)
    nh = len(farm.get("hands") or [])
    if step < len(OPENING):
        rec = OPENING[step]
        return {
            "farmer": list(rec["f"]),
            "hands": _pad_hands(rec.get("h"), nh),
            "market": [list(o) for o in (rec.get("m") or [])],
        }
    hour = int(observation.get("hour", step % 24) or 0)
    if hour == 0 and day == 1:
        return {
            "farmer": ["COLLECT_FERTILIZER"],
            "hands": _pad_hands([], nh),
            "market": [["HIRE"] for _ in range(8)],
        }
    quads = list(farm.get("unlocked_quadrants") or ["NW"])
    scan = _scan(farm, day, quads)
    cmds = _commands(observation, farm, private, scan)
    market = _market(observation, farm, private, scan)
    farmer = cmds[0] if cmds else ["PASS"]
    hands = _pad_hands(cmds[1:], nh)
    return {"farmer": farmer, "hands": hands, "market": market}
