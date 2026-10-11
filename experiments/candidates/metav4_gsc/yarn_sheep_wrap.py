# ---------------------------------------------------------------------------
# Extra sheep on yarn worlds (worker path, not a sale overlay).
# Metav4 yarn at t=216 is ~6 sheep; DSM yarn is ~10+. Convert the first two
# post-shop BUY_ANIMAL COW into SHEEP and reuse that unit's PICKUP/PLACE
# pasture path (same structure as cow). Do not bump qty (second animal sits
# in-hand and wipes nightly). Do not extra HIRE/LAND. Do not rewrite walks.
# Skip if the swap would overdraw cash (sheep 500 vs cow 400).
# ---------------------------------------------------------------------------
_XS_PARENT = agent
_XS = {}
_XS_ANIMAL = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
_XS_LAND = (1000, 2000, 4000)


def _xs_st(player, step):
    rec = _XS.get(player)
    if rec is None or step == 0 or step < rec["step"]:
        rec = {"step": -1, "converted": 0, "need_pick": 0}
        _XS[player] = rec
    rec["step"] = step
    return rec


def _xs_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _xs_cash_after(obs, farm, market):
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
            cash -= _XS_ANIMAL.get(o[1], 500) * max(1, int(o[2]))
        elif op == "BUY_LAND":
            cash -= _XS_LAND[min(2, land_i)]
            land_i += 1
        elif op in ("BUY_SEED", "BUY_PRODUCT") and len(o) >= 3:
            cash -= float(prices.get(o[1], 0) or 0) * int(o[2])
        elif op == "HIRE":
            cash -= _xs_fib(hires_today)
            hires_today += 1
    return cash


def _xs_rewrite(obs, action):
    step = int(obs["step"])
    if step < 144 or step > 270:
        return action
    shops = list((obs["town"]["unlocked_shops"] if obs["town"] is not None else []) or [])
    pair = tuple(shops[:2])
    if "YARN_STORE" not in pair:
        return action
    player = int(obs["player"])
    farm = obs["farms"][player]
    private = obs["private"]
    st = _xs_st(player, step)
    farmer = list(action.get("farmer") or ["PASS"])
    hands = [list(h) for h in (action.get("hands") or [])]
    units = [farmer] + hands
    market = [list(o) for o in (action.get("market") or [])]

    cap = 2 if "PIZZA_SHOP" in pair else 4
    if st["converted"] < cap:
        for o in market:
            if o and len(o) >= 3 and o[0] == "BUY_ANIMAL" and o[1] == "COW":
                qty = max(1, int(o[2]))
                o[1] = "SHEEP"
                if _xs_cash_after(obs, farm, market) < 0:
                    o[1] = "COW"
                    break
                st["converted"] += 1
                st["need_pick"] += qty
                break

    for u in units:
        if u and len(u) >= 2 and u[0] == "PICKUP" and u[1] == "COW" and st["need_pick"] > 0:
            u[1] = "SHEEP"
            st["need_pick"] -= 1

    positions = [tuple(farm["farmer"])] + [tuple(p) for p in (farm["hands"] or [])]
    inventories = [dict(inv or {}) for inv in (private["inventories"] or [])]
    while len(inventories) < len(units):
        inventories.append({})
    tiles = farm["tiles"]
    for i, u in enumerate(units):
        holding_sheep = int(inventories[i].get("SHEEP") or 0) > 0
        op = u[0] if u else "PASS"
        if holding_sheep and u and len(u) >= 2 and op == "PLACE" and u[1] == "COW":
            units[i] = ["PLACE", "SHEEP"]
            continue
        if not holding_sheep:
            continue
        pos = positions[i] if i < len(positions) else None
        tile = None
        if pos is not None:
            x, y = pos
            if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
                tile = tiles[y][x]
        if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and not tile.get("animal"):
            if op in ("PASS", "CARE", "FEED", "PLACE", "BUILD_PASTURE", "DIG"):
                units[i] = ["PLACE", "SHEEP"]

    return {"farmer": units[0], "hands": units[1:], "market": market[:10]}


def agent(observation, configuration=None, _parent=_XS_PARENT):
    action = _parent(observation, configuration)
    try:
        return _xs_rewrite(observation, action)
    except Exception:
        return action


agent = globals().pop("agent")
