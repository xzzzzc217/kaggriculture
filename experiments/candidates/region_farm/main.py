"""Region-owned production engine. Not a tape, not a metav4 overlay.

DSM opening 0-8, then workers stay in a zone: herd around the shed, NE
strawberries, SW wheat+berries. Greedy nearest-target farms fail because
the whole crew chases hungry cows and never finishes SW watering.
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
    (4, 2), (5, 2), (6, 2), (7, 2),
    (4, 3), (5, 3), (6, 3),
    (4, 4), (5, 4), (6, 4), (7, 4),
    (3, 2),
)
SHEEP_TILES = ((3, 3), (2, 4), (3, 4), (4, 3), (7, 4))
TOMATO_TILES = ((0, 8), (0, 9), (1, 9), (1, 8), (0, 7), (1, 7))
FIRST_YIELD = {"WHEAT": 2, "CARROT": 2, "TOMATO": 8, "STRAWBERRY": 10, "MELON": 10}
HERD_SET = set(COW_TILES) | set(SHEEP_TILES) | set(SHED)

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
_LAST = {}


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
    prev = _LAST.get(player)
    if prev is None or step < prev or hour == 0:
        _STICKY[player] = {}
    _LAST[player] = step
    return _STICKY[player]


def _zone(pos):
    x, y = pos
    if x < 5 and y >= 5:
        return "SW"
    if x >= 5 and y < 5:
        return "NE"
    return "NW"


def _role(i, n, quads):
    if i == 0:
        return "HERD"
    hi = i - 1
    if hi < 5:
        return "HERD"
    if "SW" in quads and hi >= 8:
        return "SW"
    return "NE"


def _scan(farm, day, quads):
    animals = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    pastures, hungry, uncared, fert = [], [], [], []
    water, harvest, weeds = [], [], []
    berries = tomatoes = melons = wheatn = 0
    plants = []
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            pos = (x, y)
            if tile is None or tile == "LOCKED" or not isinstance(tile, dict):
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
            if kind == "WEED":
                weeds.append(pos)
            if kind == "PLANT":
                plants.append(pos)
                crop = tile.get("crop")
                if crop == "STRAWBERRY":
                    berries += 1
                elif crop == "TOMATO":
                    tomatoes += 1
                elif crop == "MELON":
                    melons += 1
                elif crop == "WHEAT":
                    wheatn += 1
                age = day - int(tile.get("planted_day") or 0)
                first = FIRST_YIELD.get(crop, 0)
                if int(tile.get("yield_units") or 0) > 0 and (crop not in FIRST_YIELD or age >= first):
                    harvest.append(pos)
                if not tile.get("watered_today"):
                    water.append(pos)
    return {
        "animals": animals, "pastures": pastures, "hungry": hungry, "uncared": uncared,
        "fert": fert, "water": water, "harvest": harvest, "weeds": weeds,
        "berries": berries, "tomatoes": tomatoes, "melons": melons, "wheat": wheatn,
        "plants": plants, "quads": quads,
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
    if pizza >= 2 and milk >= 80:
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


def _berry_sites(quads):
    reserved = HERD_SET | set(EARLY_WHEAT) | set(MELON_TILES) | set(TOMATO_TILES)
    sites = list(PERM_BERRY)
    if "NE" in quads:
        sites.extend((x, y) for x in range(5, 10) for y in range(0, 5) if (x, y) not in reserved)
    if "SW" in quads:
        sites.extend((x, y) for x in range(2, 5) for y in range(5, 9) if (x, y) not in reserved)
    out, seen = [], set()
    for p in sites:
        if p in seen or not _unlocked(p, quads):
            continue
        seen.add(p)
        out.append(p)
    return out


def _wheat_sites(quads, day):
    reserved = HERD_SET
    sites = list(EARLY_WHEAT)
    if "SW" in quads:
        sites.extend((x, y) for x in range(0, 2) for y in range(5, 10))
        sites.extend((x, 9) for x in range(2, 5))
    if day >= 20:
        sites.extend(_berry_sites(quads))
    out, seen = [], set()
    for p in sites:
        if p in seen or p in reserved or not _unlocked(p, quads):
            continue
        seen.add(p)
        out.append(p)
    return out


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
    sell("STRAWBERRY", 4, 1)
    sell("MELON", 2, 1)
    sell("TOMATO", 3, 1)
    sell("MILK", 6, 1)
    sell("WOOL", 3, 1)
    sell("EGG", 3, 1)
    fert_x = int(shed.get("FERTILIZER") or 0) - 1
    if fert_x > 0:
        sell("FERTILIZER", min(fert_x, 8), 1)

    wheat = int(shed.get("WHEAT") or 0)
    cash_floor = 200 if day < 8 else 150
    hires = int(farm.get("hires_today") or 0)
    hands = len(farm.get("hands") or [])
    if (hands < 6 or money < 150 or (day < 10 and money < 1000)) and wheat > n_an:
        sell("WHEAT", max(1, wheat - n_an), 1)
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
    if int(shed.get("COW") or 0) == 0 and carried["COW"] == 0 and day >= 2 and cows < want_c and money - spent >= cash_floor + 800 and px("MILK") >= 70 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "COW", 1])
        spent += 400
    if int(shed.get("SHEEP") or 0) == 0 and carried["SHEEP"] == 0 and day >= 3 and sheep < want_s and money - spent >= cash_floor + 900 and px("WOOL") >= 70 and len(orders) < 10:
        orders.append(["BUY_ANIMAL", "SHEEP", 1])
        spent += 500
    if int(seeds.get("MELON") or 0) < 6 and day < 20 and money - spent >= cash_floor + 160 and len(orders) < 10:
        orders.append(["BUY_SEED", "MELON", 2])
        spent += 160
    berry_need = 16 if "NE" in quads else 4
    have_b = int(seeds.get("STRAWBERRY") or 0)
    if have_b < berry_need and money - spent >= cash_floor + 200 and len(orders) < 10:
        n = 4 if money - spent >= 2000 else 2
        n = min(n, berry_need - have_b, int((money - spent - cash_floor) // 100))
        if n > 0:
            orders.append(["BUY_SEED", "STRAWBERRY", n])
            spent += 100 * n
    wheat_need = 12 if "SW" in quads else 8
    if int(seeds.get("WHEAT") or 0) < wheat_need and money - spent >= cash_floor + 40 and len(orders) < 10:
        n = min(8, wheat_need - int(seeds.get("WHEAT") or 0))
        orders.append(["BUY_SEED", "WHEAT", n])
        spent += 10 * n
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
    if kind == "FERTILIZE":
        return ["FERTILIZE"] if inv.get("FERTILIZER") else None
    if kind == "DIG":
        return ["DIG"]
    if kind == "PLANT":
        return ["PLANT", seed]
    if kind == "BUILD_P":
        return ["BUILD_PASTURE"]
    return None


def _in_role(pos, role):
    z = _zone(pos)
    if role == "HERD":
        return z == "NW" or pos in HERD_SET or (z == "NE" and pos in HERD_SET)
    if role == "NE":
        return z == "NE" and pos not in HERD_SET
    if role == "SW":
        return z == "SW"
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
    berry_sites = _berry_sites(quads)
    wheat_sites = _wheat_sites(quads, day)

    def set_job(i, kind, target, seed=None):
        sticky[i] = (kind, target[0], target[1], seed)
        claimed.add(target)

    def clear_job(i):
        sticky.pop(i, None)

    def jobs_for(role):
        water = [p for p in scan["water"] if _in_role(p, role)]
        harvest = [p for p in scan["harvest"] if _in_role(p, role)]
        weeds = [p for p in scan["weeds"] if _in_role(p, role)]
        if role == "HERD":
            hungry = list(scan["hungry"])
            fert = list(scan["fert"])
            uncared = list(scan["uncared"])
            melon_e = [p for p in MELON_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
            wheat_e = [p for p in EARLY_WHEAT if _unlocked(p, quads) and _tile(farm, p) is None]
            berry_e = [p for p in PERM_BERRY if _tile(farm, p) is None]
            return [
                ("FEED", hungry, True, None),
                ("FERT", fert, False, None),
                ("HARVEST", harvest, False, None),
                ("WATER", water, False, None),
                ("PLANT", wheat_e, False, "WHEAT"),
                ("CARE", uncared, False, None),
                ("PLANT", melon_e, False, "MELON"),
                ("PLANT", berry_e, False, "STRAWBERRY"),
                ("DIG", weeds, False, None),
            ]
        if role == "NE":
            berry_e = [p for p in berry_sites if _zone(p) == "NE" and _tile(farm, p) is None]
            fertz = []
            if day >= 12:
                for p in berry_sites:
                    if _zone(p) != "NE":
                        continue
                    t = _tile(farm, p)
                    if isinstance(t, dict) and t.get("crop") == "STRAWBERRY" and int(t.get("fertilized_until_day") or -1) < day:
                        fertz.append(p)
            plant = ("PLANT", berry_e, False, "STRAWBERRY") if day < 20 else ("PLANT", berry_e, False, "WHEAT")
            return [
                ("WATER", water, False, None),
                ("HARVEST", harvest, False, None),
                ("DIG", weeds, False, None),
                plant,
                ("FERTILIZE", fertz, False, None),
            ]
        berry_e = [p for p in berry_sites if _zone(p) == "SW" and _tile(farm, p) is None]
        wheat_e = [p for p in wheat_sites if _zone(p) == "SW" and _tile(farm, p) is None]
        jobs = [
            ("WATER", water, False, None),
            ("HARVEST", harvest, False, None),
            ("DIG", weeds, False, None),
            ("PLANT", wheat_e, False, "WHEAT"),
        ]
        if day < 20:
            jobs.append(("PLANT", berry_e, False, "STRAWBERRY"))
        return jobs

    # Carrying animals: farmer/herd only.
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

    # Herd pickup wheat.
    if scan["hungry"] and int(shed.get("WHEAT") or 0) > 0:
        sent = 0
        for i, pos in enumerate(positions):
            if sent >= 3 or cmds[i] != ["PASS"]:
                continue
            if _role(i, n, quads) != "HERD":
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

    # Honor sticky if still in-role.
    for i, pos in enumerate(positions):
        if cmds[i] != ["PASS"]:
            continue
        job = sticky.get(i)
        if not job:
            continue
        kind, tx, ty, seed = job
        target = (tx, ty)
        role = _role(i, n, quads)
        if not _in_role(target, role) and kind != "FEED":
            clear_job(i)
            continue
        if target in claimed:
            clear_job(i)
            continue
        tile = _tile(farm, target)
        valid = True
        if kind == "WATER":
            valid = isinstance(tile, dict) and tile.get("kind") == "PLANT" and not tile.get("watered_today")
        elif kind == "PLANT":
            valid = tile is None and int(seed_left.get(seed) or 0) > 0
        elif kind == "FEED":
            valid = target in scan["hungry"]
        elif kind == "HARVEST":
            valid = target in scan["harvest"]
        elif kind == "DIG":
            valid = isinstance(tile, dict) and tile.get("kind") == "WEED"
        elif kind == "FERT":
            valid = target in scan["fert"]
        elif kind == "FERTILIZE":
            valid = isinstance(tile, dict) and tile.get("crop") == "STRAWBERRY" and inventories[i].get("FERTILIZER")
        elif kind == "CARE":
            valid = target in scan["uncared"]
        elif kind == "BUILD_P":
            valid = tile is None
        if not valid:
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

    def assign_role(role, kind, targets, require_wheat=False, seed=None, limit=99):
        placed = 0
        order = []
        for i, pos in enumerate(positions):
            if cmds[i] != ["PASS"] or _role(i, n, quads) != role:
                continue
            if require_wheat and not inventories[i].get("WHEAT"):
                continue
            if seed and int(seed_left.get(seed) or 0) <= 0:
                continue
            if kind == "FERTILIZE" and not inventories[i].get("FERTILIZER"):
                continue
            order.append(i)
        order.sort(key=lambda i: 0 if positions[i] in targets and positions[i] not in claimed else 1)
        for i in order:
            if placed >= limit or cmds[i] != ["PASS"]:
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
            act = _act(kind, inventories[i], seed)
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

    for role in ("HERD", "NE", "SW"):
        for kind, targets, req_w, seed in jobs_for(role):
            if not targets:
                continue
            lim = 8 if kind in ("WATER", "FEED", "HARVEST") else 4
            assign_role(role, kind, targets, require_wheat=req_w, seed=seed, limit=lim)

    # Nearby fertilize: herd/NE workers holding fert, strawberry within 2.
    if day >= 12:
        ft = []
        for p in berry_sites:
            t = _tile(farm, p)
            if isinstance(t, dict) and t.get("crop") == "STRAWBERRY" and int(t.get("fertilized_until_day") or -1) < day:
                ft.append(p)
        for i, pos in enumerate(positions):
            if cmds[i] != ["PASS"] or not inventories[i].get("FERTILIZER"):
                continue
            if pos in ft:
                cmds[i] = ["FERTILIZE"]
                continue
            t = _nearest(pos, ft, set())
            if t and abs(pos[0] - t[0]) + abs(pos[1] - t[1]) <= 2:
                cmds[i] = _walk(pos, t) or ["FERTILIZE"]

    cow_empty = [p for p in COW_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
    sheep_empty = [p for p in SHEEP_TILES if _unlocked(p, quads) and _tile(farm, p) is None]
    if scan["animals"]["COW"] < 12 and len(scan["pastures"]) < 3:
        assign_role("HERD", "BUILD_P", cow_empty, limit=1)
    if scan["animals"]["SHEEP"] < 5 and len(scan["pastures"]) < 3:
        assign_role("HERD", "BUILD_P", sheep_empty, limit=1)

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
