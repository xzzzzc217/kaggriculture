# ---------------------------------------------------------------------------
# Extra cows on pizza-only worlds (worker path). Pizza wants milk; skip yarn
# (sheep wrap) and brunch (geese wrap). Convert first two post-shop SHEEP
# buys to COW and reuse the pasture PICKUP/PLACE path. Same structure as
# sheep, no DIG/COOP. Do not extra HIRE/LAND. Do not rewrite walks.
# ---------------------------------------------------------------------------
_XC_PARENT = agent
_XC = {}
_XC_ANIMAL = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
_XC_LAND = (1000, 2000, 4000)


def _xc_st(player, step):
    rec = _XC.get(player)
    if rec is None or step == 0 or step < rec["step"]:
        rec = {"step": -1, "converted": 0, "need_pick": 0}
        _XC[player] = rec
    rec["step"] = step
    return rec


def _xc_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _xc_cash_after(obs, farm, market):
    cash = float(farm["money"])
    prices = obs["market"]["prices"] if obs["market"] is not None else {}
    quads = len(farm.get("unlocked_quadrants") or [])
    hires_today = int(farm.get("hires_today") or 0)
    land_i = max(0, quads - 1)
    for o in market:
        if not o:
            continue
        op = o[0]
        if op == "SELL" and len(o) >= 3:
            cash += int(o[2]) * float(prices.get(o[1], 0) or 0)
        elif op == "BUY_ANIMAL" and len(o) >= 3:
            cash -= _XC_ANIMAL.get(o[1], 500) * max(1, int(o[2]))
        elif op == "BUY_LAND":
            cash -= _XC_LAND[min(2, land_i)]
            land_i += 1
        elif op in ("BUY_SEED", "BUY_PRODUCT") and len(o) >= 3:
            cash -= float(prices.get(o[1], 0) or 0) * int(o[2])
        elif op == "HIRE":
            cash -= _xc_fib(hires_today)
            hires_today += 1
    return cash


def _xc_rewrite(obs, action):
    step = int(obs["step"])
    if step < 144 or step > 270:
        return action
    shops = list((obs["town"]["unlocked_shops"] if obs["town"] is not None else []) or [])
    pair = tuple(shops[:2])
    if "PIZZA_SHOP" not in pair:
        return action
    if "YARN_STORE" in pair or "BRUNCH_SPOT" in pair or "BAKERY" in pair:
        return action
    if pair[0] == "PIZZA_SHOP" and pair[1] == "PIZZA_SHOP":
        return action
    player = int(obs["player"])
    farm = obs["farms"][player]
    private = obs["private"]
    st = _xc_st(player, step)
    farmer = list(action.get("farmer") or ["PASS"])
    hands = [list(h) for h in (action.get("hands") or [])]
    units = [farmer] + hands
    market = [list(o) for o in (action.get("market") or [])]

    if st["converted"] < 2:
        for o in market:
            if o and len(o) >= 3 and o[0] == "BUY_ANIMAL" and o[1] == "SHEEP":
                qty = max(1, int(o[2]))
                o[1] = "COW"
                if _xc_cash_after(obs, farm, market) < 0:
                    o[1] = "SHEEP"
                    break
                st["converted"] += 1
                st["need_pick"] += qty
                break

    for u in units:
        if u and len(u) >= 2 and u[0] == "PICKUP" and u[1] == "SHEEP" and st["need_pick"] > 0:
            u[1] = "COW"
            st["need_pick"] -= 1

    positions = [tuple(farm["farmer"])] + [tuple(p) for p in (farm["hands"] or [])]
    inventories = [dict(inv or {}) for inv in (private["inventories"] or [])]
    while len(inventories) < len(units):
        inventories.append({})
    tiles = farm["tiles"]
    for i, u in enumerate(units):
        holding = int(inventories[i].get("COW") or 0) > 0
        op = u[0] if u else "PASS"
        if holding and u and len(u) >= 2 and op == "PLACE" and u[1] == "SHEEP":
            units[i] = ["PLACE", "COW"]
            continue
        if not holding:
            continue
        pos = positions[i] if i < len(positions) else None
        tile = None
        if pos is not None:
            x, y = pos
            if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
                tile = tiles[y][x]
        if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and not tile.get("animal"):
            if op in ("PASS", "CARE", "FEED", "PLACE", "BUILD_PASTURE", "DIG"):
                units[i] = ["PLACE", "COW"]

    return {"farmer": units[0], "hands": units[1:], "market": market[:10]}


def agent(observation, configuration=None, _parent=_XC_PARENT):
    action = _parent(observation, configuration)
    try:
        return _xc_rewrite(observation, action)
    except Exception:
        return action


agent = globals().pop("agent")
