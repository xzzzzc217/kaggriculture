# SPDX-License-Identifier: Apache-2.0
"""Python port of Yusuke six-day public-state trees + 144-turn blocks.

Reselects at 144 / 288 / 432 / 576 from public state only. Does not load
Linux agent.so. Tapes come from the local hunt C++ source, not a 227/242/266
sheep wrap of Fieldbook BALANCED.
"""

from __future__ import annotations

import copy
import math
from typing import Any

from sixday_tapes import ENCODED_SEGMENTS

ITEMS = (
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
    "GOOSE",
    "COW",
    "SHEEP",
)
PRODUCTS = ITEMS[:9]
CROPS = ITEMS[:5]
UNIT_OPS = (
    "PASS",
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST",
    "PICKUP",
    "DROP",
    "PLACE",
    "PLANT",
    "WATER",
    "HARVEST",
    "FERTILIZE",
    "DIG",
    "BUILD_COOP",
    "BUILD_PASTURE",
    "FEED",
    "COLLECT_FERTILIZER",
    "CARE",
)
MARKET_OPS = (
    "PASS",
    "HIRE",
    "BUY_LAND",
    "BUY_SEED",
    "BUY_PRODUCT",
    "BUY_ANIMAL",
    "SELL",
)
ITEM_ID = {name: index for index, name in enumerate(ITEMS)}
SEED_COST = (10, 20, 50, 100, 80)
ANIMAL_COST = (300, 400, 500)
LAND_PRICES = (1000, 2000, 4000)
SIX_DAY_TURNS = 144
OP_PLACE = 7
OP_PLANT = 8
OP_FERTILIZE = 11
OP_FEED = 15
M_NONE = 0
M_HIRE = 1
M_BUY_LAND = 2
M_BUY_SEED = 3
M_BUY_PRODUCT = 4
M_BUY_ANIMAL = 5
M_SELL = 6
WHEAT = 0
FERTILIZER = 8
GOOSE = 9
RESELECT_STEPS = (144, 288, 432, 576)


def _get(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def decode_action(encoded: str) -> dict[str, Any]:
    """Decode one C tape string into numeric units/orders."""
    nums = [int(part) for part in encoded.split()]
    if len(nums) < 2:
        raise ValueError("encoded tape missing counts")
    n_units, n_orders = nums[0], nums[1]
    cursor = 2
    units: list[tuple[int, int, int]] = []
    for _ in range(n_units):
        if cursor + 2 >= len(nums):
            raise ValueError("encoded tape truncated unit")
        units.append((nums[cursor], nums[cursor + 1], nums[cursor + 2]))
        cursor += 3
    orders: list[tuple[int, int, int]] = []
    for _ in range(n_orders):
        if cursor + 2 >= len(nums):
            raise ValueError("encoded tape truncated order")
        orders.append((nums[cursor], nums[cursor + 1], nums[cursor + 2]))
        cursor += 3
    if cursor != len(nums):
        raise ValueError("trailing encoded tape value")
    return {"units": units, "orders": orders}


def action_to_dict(action: dict[str, Any]) -> dict[str, Any]:
    units = list(action.get("units") or [])
    farmer = _unit_order(*(units[0] if units else (0, 0, 1)))
    hands = [_unit_order(*row) for row in units[1:]]
    market = []
    for row in action.get("orders") or []:
        order = _market_order(*row)
        if order is not None:
            market.append(order)
    return {"farmer": farmer, "hands": hands, "market": market}


def _unit_order(operation: int, argument: int, quantity: int) -> list[Any]:
    name = UNIT_OPS[operation] if 0 <= operation < len(UNIT_OPS) else "PASS"
    if name in {"PLANT", "PICKUP", "PLACE"}:
        item = ITEMS[argument] if 0 <= argument < len(ITEMS) else ITEMS[0]
        return [name, item] if quantity == 1 else [name, item, int(quantity)]
    return [name]


def _market_order(operation: int, item: int, quantity: int) -> list[Any] | None:
    name = MARKET_OPS[operation] if 0 <= operation < len(MARKET_OPS) else "PASS"
    if name == "PASS" or operation == M_NONE:
        return None
    if name in {"HIRE", "BUY_LAND"}:
        return [name]
    item_name = ITEMS[item] if 0 <= item < len(ITEMS) else ITEMS[0]
    return [name, item_name, int(quantity)]


DECODED_SEGMENTS: list[list[list[dict[str, Any]]]] = [
    [[decode_action(encoded) for encoded in route] for route in segment]
    for segment in ENCODED_SEGMENTS
]


def action_for(selected: list[int], step: int) -> dict[str, Any]:
    """Return a copy of the stored block action for this step and route vector."""
    if step < 0 or step >= 719:
        return {"units": [(0, 0, 1)], "orders": []}
    segment = min(step // SIX_DAY_TURNS, 4)
    route = selected[segment]
    local = step - segment * SIX_DAY_TURNS
    return copy.deepcopy(DECODED_SEGMENTS[segment][route][local])


def select_segment_1(features: dict[str, float]) -> int:
    if features["price_carrot"] <= 33:
        return 1
    if features["rival_weed_y_sum"] <= 3.5:
        return 0
    return 1


def select_segment_1_live(features: dict[str, float], shops: list[str]) -> int:
    """Published carrot/weed tree, with a shop-bag override when yarn is absent.

    No-yarn openings are the clone-seat failure class: the cow-leaning day-6
    block (route 1) stays later-block reselect and is not a BALANCED wrap.
    """
    if "YARN_STORE" not in shops:
        return 1
    return select_segment_1(features)


def select_segment_2(features: dict[str, float]) -> int:
    del features
    return 0


def select_segment_3(features: dict[str, float]) -> int:
    if features["fertilizer"] <= 23.5:
        if features["price_tomato"] <= 80.5:
            return 2 if features["price_milk"] <= 152 else 0
        return 0 if features["rival_weed_x_min"] <= 1.5 else 1
    if features["price_strawberry"] <= 232.5:
        return 0 if features["rival_weed_y_min"] <= 1.5 else 1
    return 0 if features["weed_x_sum_gap"] <= -3.5 else 1


def select_segment_4(features: dict[str, float]) -> int:
    if features["price_carrot"] <= 65.5:
        if features["price_wool"] <= 227.5:
            return 4 if features["price_fertilizer"] <= 12 else 0
        return 4 if features["price_strawberry"] <= 11.5 else 2
    if features["cash_gap"] <= 3935:
        return 3 if features["cash_gap"] <= 340.5 else 4
    return 4 if features["price_fertilizer"] <= 32.5 else 1


def select_segment_4_live(features: dict[str, float]) -> int:
    """Published last-block tree, with the strawberry-crash leaf unblocked.

    The C++ tree hides `price_strawberry <= 11.5 -> route 4` behind a high-wool
    gate. Take that leaf only when wool is still worth selling.
    """
    if features["price_strawberry"] <= 11.5 and features["price_wool"] > 32.5:
        return 4
    return select_segment_4(features)


SELECTORS = (
    None,
    select_segment_1,
    select_segment_2,
    select_segment_3,
    select_segment_4,
)


def _tile_kind(tile: Any) -> str:
    if tile is None:
        return "EMPTY"
    if isinstance(tile, str):
        return tile
    kind = _get(tile, "kind")
    crop = _get(tile, "crop")
    animal = _get(tile, "animal")
    if kind == "PLANT" or crop:
        return "PLANT"
    if animal is not None:
        return str(kind or "PASTURE")
    return str(kind or "EMPTY")


def weed_stats(farm: Any) -> dict[str, int]:
    result = {
        "tiles": 0,
        "x_sum": 0,
        "y_sum": 0,
        "x_min": -1,
        "x_max": -1,
        "y_min": -1,
        "y_max": -1,
    }
    tiles = list(_get(farm, "tiles", []) or [])
    for y, row in enumerate(tiles[:10]):
        for x, tile in enumerate(list(row or [])[:10]):
            if _tile_kind(tile) != "WEED":
                continue
            result["tiles"] += 1
            result["x_sum"] += x
            result["y_sum"] += y
            result["x_min"] = x if result["x_min"] < 0 else min(result["x_min"], x)
            result["x_max"] = max(result["x_max"], x)
            result["y_min"] = y if result["y_min"] < 0 else min(result["y_min"], y)
            result["y_max"] = max(result["y_max"], y)
    return result


def capture_features(observation: Any, seat: int) -> dict[str, float]:
    farms = list(_get(observation, "farms", []) or [])
    own = farms[seat] if seat < len(farms) else {}
    rival = farms[1 - seat] if len(farms) >= 2 else {}
    weed = weed_stats(own)
    rival_weed = weed_stats(rival)
    market = _get(observation, "market", {}) or {}
    prices = _get(market, "prices", {}) or {}
    private = _get(observation, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    seeds = _get(private, "seeds", {}) or {}
    inventories = list(_get(private, "inventories", []) or [])
    own_tiles = list(_get(own, "tiles", []) or [])
    empty_tiles = plant_tiles = animal_tiles = structure_tiles = 0
    for row in own_tiles[:10]:
        for tile in list(row or [])[:10]:
            kind = _tile_kind(tile)
            if kind in {"EMPTY", "SOIL", "None"} or tile is None:
                empty_tiles += 1
            elif kind == "PLANT":
                plant_tiles += 1
            elif kind in {"COOP", "PASTURE"}:
                animal = _get(tile, "animal") if not isinstance(tile, str) else None
                if animal is not None:
                    animal_tiles += 1
                else:
                    structure_tiles += 1
    hands = 0
    for carried in inventories:
        for item in ITEMS:
            hands += int(_get(carried or {}, item, 0) or 0)
    wheat = int(_get(shed, "WHEAT", 0) or 0)
    fertilizer = int(_get(shed, "FERTILIZER", 0) or 0)
    seed_total = sum(int(_get(seeds, name, 0) or 0) for name in CROPS)
    shed_total = sum(int(_get(shed, name, 0) or 0) for name in ITEMS)
    own_money = float(_get(own, "money", 0) or 0)
    rival_money = float(_get(rival, "money", 0) or 0)
    own_units = 1 + len(list(_get(own, "hands", []) or []))
    rival_units = 1 + len(list(_get(rival, "hands", []) or []))
    own_land = len(list(_get(own, "unlocked_quadrants", []) or []))
    rival_land = len(list(_get(rival, "unlocked_quadrants", []) or []))
    return {
        "money": own_money,
        "cash_gap": own_money - rival_money,
        "units": float(own_units),
        "unit_gap": float(own_units - rival_units),
        "land": float(own_land),
        "land_gap": float(own_land - rival_land),
        "shed": float(shed_total),
        "wheat": float(wheat),
        "fertilizer": float(fertilizer),
        "seeds": float(seed_total),
        "hands": float(hands),
        "empty_tiles": float(empty_tiles),
        "weed_tiles": float(weed["tiles"]),
        "plant_tiles": float(plant_tiles),
        "animal_tiles": float(animal_tiles),
        "structure_tiles": float(structure_tiles),
        "price_wheat": float(_get(prices, "WHEAT", 0) or 0),
        "price_carrot": float(_get(prices, "CARROT", 0) or 0),
        "price_tomato": float(_get(prices, "TOMATO", 0) or 0),
        "price_strawberry": float(_get(prices, "STRAWBERRY", 0) or 0),
        "price_melon": float(_get(prices, "MELON", 0) or 0),
        "price_egg": float(_get(prices, "EGG", 0) or 0),
        "price_milk": float(_get(prices, "MILK", 0) or 0),
        "price_wool": float(_get(prices, "WOOL", 0) or 0),
        "price_fertilizer": float(_get(prices, "FERTILIZER", 0) or 0),
        "rival_weed_tiles": float(rival_weed["tiles"]),
        "weed_tiles_gap": float(weed["tiles"] - rival_weed["tiles"]),
        "weed_x_sum": float(weed["x_sum"]),
        "weed_y_sum": float(weed["y_sum"]),
        "weed_x_min": float(weed["x_min"]),
        "weed_x_max": float(weed["x_max"]),
        "weed_y_min": float(weed["y_min"]),
        "weed_y_max": float(weed["y_max"]),
        "weed_x_span": float(0 if weed["x_min"] < 0 else weed["x_max"] - weed["x_min"]),
        "weed_y_span": float(0 if weed["y_min"] < 0 else weed["y_max"] - weed["y_min"]),
        "rival_weed_x_sum": float(rival_weed["x_sum"]),
        "rival_weed_y_sum": float(rival_weed["y_sum"]),
        "rival_weed_x_min": float(rival_weed["x_min"]),
        "rival_weed_x_max": float(rival_weed["x_max"]),
        "rival_weed_y_min": float(rival_weed["y_min"]),
        "rival_weed_y_max": float(rival_weed["y_max"]),
        "rival_weed_x_span": float(
            0 if rival_weed["x_min"] < 0 else rival_weed["x_max"] - rival_weed["x_min"]
        ),
        "rival_weed_y_span": float(
            0 if rival_weed["y_min"] < 0 else rival_weed["y_max"] - rival_weed["y_min"]
        ),
        "weed_x_sum_gap": float(weed["x_sum"] - rival_weed["x_sum"]),
        "weed_y_sum_gap": float(weed["y_sum"] - rival_weed["y_sum"]),
    }


def observation_step(observation: Any) -> int:
    raw = _get(observation, "step")
    if raw is not None:
        return int(raw)
    return int(_get(observation, "day", 0) or 0) * 24 + int(
        _get(observation, "hour", 0) or 0
    )


def observation_seat(observation: Any) -> int:
    return int(_get(observation, "player", 0) or 0)


def fib(index: int) -> int:
    first, second = 1, 1
    for _ in range(index):
        first, second = second, first + second
    return first


def planned_quantity(quantity: int) -> int:
    return max(1, quantity)


def _configuration(configuration: Any, key: str, default: Any) -> Any:
    return _get(configuration or {}, key, default)


def calculate_six_day_requirements(
    observation: Any,
    configuration: Any,
    seat: int,
    start: int,
    end: int,
    selected: list[int],
) -> dict[str, Any]:
    farms = list(_get(observation, "farms", []) or [])
    own = farms[seat] if seat < len(farms) else {}
    market = _get(observation, "market", {}) or {}
    prices = _get(market, "prices", {}) or {}
    hire_mult = int(_configuration(configuration, "farmHandCostMult", 1) or 1)
    seed_balance = [0] * 5
    item_balance = [0] * 12
    starting_seeds = [0] * 5
    starting_items = [0] * 12
    hires_by_day = [0] * 6
    quadrants = len(list(_get(own, "unlocked_quadrants", []) or []))
    purchase_budget = 0.0
    wheat_price = float(_get(prices, "WHEAT", 0) or 0)
    fert_price = float(_get(prices, "FERTILIZER", 0) or 0)
    for step in range(start, end):
        action = action_for(selected, step)
        for operation, argument, quantity in action["units"]:
            planned = planned_quantity(quantity)
            if operation == OP_PLANT and argument < 5:
                seed_balance[argument] -= 1
                starting_seeds[argument] = max(
                    starting_seeds[argument], -seed_balance[argument]
                )
            elif operation == OP_FEED:
                item_balance[WHEAT] -= 1
                starting_items[WHEAT] = max(starting_items[WHEAT], -item_balance[WHEAT])
            elif operation == OP_FERTILIZE:
                item_balance[FERTILIZER] -= 1
                starting_items[FERTILIZER] = max(
                    starting_items[FERTILIZER], -item_balance[FERTILIZER]
                )
            elif operation == OP_PLACE and argument < 12:
                item_balance[argument] -= planned
                starting_items[argument] = max(
                    starting_items[argument], -item_balance[argument]
                )
        for operation, item, quantity in action["orders"]:
            planned = planned_quantity(quantity)
            if operation == M_HIRE:
                day = min(5, max(0, (step - start) // 24))
                hires_by_day[day] += 1
            elif operation == M_BUY_LAND:
                extra = quadrants - 1
                if 0 <= extra < 3:
                    purchase_budget += LAND_PRICES[extra]
                    quadrants += 1
            elif operation == M_BUY_SEED and item < 5:
                purchase_budget += SEED_COST[item] * planned
                seed_balance[item] += planned
            elif operation == M_BUY_PRODUCT and item in {WHEAT, FERTILIZER}:
                price = wheat_price if item == WHEAT else fert_price
                purchase_budget += price * planned
                item_balance[item] += planned
            elif operation == M_BUY_ANIMAL and GOOSE <= item < 12:
                purchase_budget += ANIMAL_COST[item - GOOSE] * planned
                item_balance[item] += planned
    hires_today = int(_get(own, "hires_today", 0) or 0)
    for day, count in enumerate(hires_by_day):
        first_hire = hires_today if day == 0 else 0
        for index in range(count):
            purchase_budget += hire_mult * fib(first_hire + index)
    return {
        "purchase_budget": purchase_budget,
        "starting_seeds": starting_seeds,
        "starting_items": starting_items,
    }


def _owned_in_hands(observation: Any, item_name: str) -> int:
    private = _get(observation, "private", {}) or {}
    total = 0
    for carried in list(_get(private, "inventories", []) or []):
        total += max(0, int(_get(carried or {}, item_name, 0) or 0))
    return total


def _existing_sale(action: dict[str, Any], item: int) -> int:
    total = 0
    for operation, order_item, quantity in action["orders"]:
        if operation == M_SELL and order_item == item and quantity > 0:
            total += quantity
    return total


def _add_budget_sale(action: dict[str, Any], item: int, quantity: int, limit: int) -> bool:
    if quantity <= 0:
        return True
    for index, (operation, order_item, current) in enumerate(action["orders"]):
        if operation == M_SELL and order_item == item:
            action["orders"][index] = (operation, order_item, current + quantity)
            return True
    if len(action["orders"]) >= limit:
        return False
    action["orders"].append((M_SELL, item, quantity))
    return True


def apply_six_day_budget_guard(
    observation: Any,
    configuration: Any,
    seat: int,
    action: dict[str, Any],
    requirements: dict[str, Any],
    step: int,
) -> dict[str, Any]:
    if step % SIX_DAY_TURNS != 0:
        return action
    farms = list(_get(observation, "farms", []) or [])
    own = farms[seat] if seat < len(farms) else {}
    private = _get(observation, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    market = _get(observation, "market", {}) or {}
    prices = _get(market, "prices", {}) or {}
    available_cash = float(_get(own, "money", 0) or 0)
    for item, name in enumerate(PRODUCTS):
        sold = min(max(0, int(_get(shed, name, 0) or 0)), _existing_sale(action, item))
        available_cash += sold * float(_get(prices, name, 0) or 0)
    shortfall = requirements["purchase_budget"] - available_cash
    if shortfall <= 0.0:
        return action
    limit = max(0, min(16, int(_configuration(configuration, "maxMarketOrdersPerTurn", 10))))
    candidates: list[tuple[int, int, int]] = []
    for item, name in enumerate(PRODUCTS):
        price = int(float(_get(prices, name, 0) or 0))
        if price < 2:
            continue
        protected_total = requirements["starting_items"][item]
        protected_shed = max(0, protected_total - _owned_in_hands(observation, name))
        available = max(
            0,
            int(_get(shed, name, 0) or 0) - protected_shed - _existing_sale(action, item),
        )
        if available > 0:
            candidates.append((item, available, price))
    candidates.sort(key=lambda row: (-row[2], row[0]))
    added = 0
    for item, available, price in candidates:
        if shortfall <= 0.0:
            break
        needed = int(math.ceil(shortfall / price))
        quantity = min(available, needed)
        if not _add_budget_sale(action, item, quantity, limit):
            continue
        shortfall -= float(quantity * price)
        added += 1
    if added > 0:
        sales = [order for order in action["orders"] if order[0] == M_SELL]
        rest = [order for order in action["orders"] if order[0] != M_SELL]
        action["orders"] = sales + rest
    return action


def later_block_action(selected: list[int], step: int) -> dict[str, Any]:
    """Public dict action for tests; no observation, no budget guard."""
    return action_to_dict(action_for(selected, step))


def _shops(observation: Any) -> list[str]:
    town = _get(observation, "town", {}) or {}
    return [str(name) for name in list(_get(town, "unlocked_shops", []) or [])]


def _sales_first(action: dict[str, Any]) -> dict[str, Any]:
    market = list(action.get("market") or [])
    sales = [order for order in market if order and order[0] == "SELL"]
    rest = [order for order in market if not order or order[0] != "SELL"]
    action["market"] = sales + rest
    return action


def _endgame_dump(
    observation: Any, action: dict[str, Any], step: int, configuration: Any
) -> dict[str, Any]:
    """On the last two tape turns, sell remaining priced shed goods."""
    if step < 717:
        return action
    allowed = PRODUCTS
    private = _get(observation, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    prices = _get(_get(observation, "market", {}) or {}, "prices", {}) or {}
    limit = max(0, min(16, int(_configuration(configuration, "maxMarketOrdersPerTurn", 10))))
    remaining = {name: max(0, int(_get(shed, name, 0) or 0)) for name in allowed}
    market: list[list[Any]] = []
    for order in action.get("market") or []:
        order = list(order)
        if order and order[0] == "SELL" and len(order) >= 3 and order[1] in remaining:
            quantity = remaining[order[1]]
            remaining[order[1]] = 0
            if quantity <= 0:
                continue
            order[2] = quantity
        market.append(order)
    leftovers = []
    for name in PRODUCTS:
        quantity = remaining[name]
        price = float(_get(prices, name, 0) or 0)
        if quantity <= 0 or price < 2:
            continue
        leftovers.append((quantity, name, int(price)))
    leftovers.sort(key=lambda row: -row[2])
    for quantity, name, _price in leftovers:
        if len(market) >= limit:
            break
        market.append(["SELL", name, quantity])
    action["market"] = market[:limit]
    return action


class SixDayRuntime:
    """Stateful later-block reselect over the frozen six-day tapes."""

    def __init__(self) -> None:
        self.selected = [0, 0, 0, 0, 0]

    def act(self, observation: Any, configuration: Any = None) -> dict[str, Any]:
        step = observation_step(observation)
        seat = observation_seat(observation)
        if step == 0:
            self.selected = [0, 0, 0, 0, 0]
        if step < 0 or step >= 719:
            action = {"farmer": ["PASS"], "hands": [], "market": []}
        else:
            if step % SIX_DAY_TURNS == 0 and step != 0:
                segment = min(step // SIX_DAY_TURNS, 4)
                features = capture_features(observation, seat)
                if segment == 1:
                    self.selected[1] = select_segment_1_live(features, _shops(observation))
                elif segment == 4:
                    self.selected[4] = select_segment_4_live(features)
                else:
                    selector = SELECTORS[segment]
                    if selector is not None:
                        self.selected[segment] = selector(features)
            numeric = action_for(self.selected, step)
            if step % SIX_DAY_TURNS == 0:
                end = min(719, step + SIX_DAY_TURNS)
                requirements = calculate_six_day_requirements(
                    observation, configuration, seat, step, end, self.selected
                )
                numeric = apply_six_day_budget_guard(
                    observation, configuration, seat, numeric, requirements, step
                )
            action = action_to_dict(numeric)
        farms = list(_get(observation, "farms", []) or [])
        own = farms[seat] if seat < len(farms) else {}
        expected_hands = len(list(_get(own, "hands", []) or []))
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected_hands - len(hands)))])
        action["hands"] = hands[:expected_hands]
        action = _endgame_dump(observation, action, step, configuration)
        return _sales_first(action)


def make_agent() -> Any:
    runtime = SixDayRuntime()

    def policy(observation: Any, configuration: Any = None) -> dict[str, Any]:
        return runtime.act(observation, configuration)

    policy.runtime = runtime
    return policy
