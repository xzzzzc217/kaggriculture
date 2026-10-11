from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Literal

# ---------------------------------------------------------------------------
# MODULE: constants.py
# ---------------------------------------------------------------------------

TOTAL_DAYS: int = 30
TURNS_PER_DAY: int = 24
MAX_MARKET_ORDERS: int = 10
BOARD_SIZE: int = 10
I0: int = 10_000

# Interleaved by distance rings from shed junction across NW, NE, SW (total 18 pasture slots)
PASTURE_CLUSTER: list[tuple[int, int]] = [
    # Ring 0: Shed corner tiles (dist 0)
    (4, 4), (5, 4), (4, 5),
    # Ring 1: Immediate shed neighbors (dist 1)
    (4, 3), (3, 4), (5, 3), (6, 4), (3, 5), (4, 6),
    # Ring 2: Secondary cluster tiles (dist 2)
    (3, 3), (4, 2), (2, 4), (6, 3), (5, 2), (7, 4), (2, 5), (3, 6), (4, 7),
]
SHED_TILES: list[tuple[int, int]] = [(4, 4), (5, 4), (4, 5), (5, 5)]
SHED_TILES_SET: frozenset[tuple[int, int]] = frozenset(SHED_TILES)

MILK_SUPPORT_SHOPS: tuple[str, ...] = ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
EGG_SUPPORT_SHOPS: tuple[str, ...] = ("BAKERY", "BRUNCH_SPOT")

SELLABLE_ITEMS: tuple[str, ...] = (
    "FERTILIZER", "MILK", "WOOL", "EGG",
    "MELON", "STRAWBERRY", "CARROT", "TOMATO", "WHEAT",
)

SHOP_DEMANDS: dict[str, dict[str, float]] = {
    "BAKERY":         {"EGG": 6.0, "WHEAT": 6.0},
    "PIZZA_SHOP":     {"MILK": 6.0, "TOMATO": 6.0, "WHEAT": 6.0},
    "BRUNCH_SPOT":    {"EGG": 6.0, "WHEAT": 6.0, "STRAWBERRY": 6.0},
    "YARN_STORE":     {"WOOL": 12.0},
    "ICE_CREAM_SHOP": {"STRAWBERRY": 6.0, "MILK": 6.0, "WHEAT": 6.0},
    "PET_CAFE":       {"CARROT": 12.0},
    "SMOOTHIE_SHOP":  {"STRAWBERRY": 6.0, "MILK": 6.0},
    "FARMERS_MARKET": {"WHEAT": 6.0, "CARROT": 6.0, "TOMATO": 6.0, "STRAWBERRY": 6.0},
}

TOWN_CENTER_FLAT: float = 1.0
LIQUIDATION_DAY: int = 28
MELON_LAST_PLANT_DAY: int = 18
STRAWBERRY_LAST_PLANT_DAY: int = 14
STRAWBERRY_LAND_HORIZON_DAYS: int = 3
WHEAT_LAST_PLANT_DAY: int = 26
PASTURE_RESERVATION_LAST_DAY: int = 16
STRAWBERRY_BASE_TARGET_BUSHES: int = 15
STRAWBERRY_BOOST_TARGET_BUSHES: int = 42
MAX_TOTAL_HERD: int = 18
MIN_PAYBACK_DAYS: int = 8
HAND_COST_PER_ANIMAL_DAY: float = 2.0
SEED_PURCHASE_CASH_RESERVE: float = 200.0
FEED_WHEAT_RESERVE: int = 4
FEED_WHEAT_RESERVE_MIN_RATIO: int = 2
FEED_WHEAT_SELL_RATIO: int = 4
N_FERTILIZER_HANDS: int = 2
FERTILIZER_PICKUP_BATCH: int = 4

CROPS: dict[str, dict[str, Any]] = {
    "WHEAT": {
        "seed_cost": 10, "base_price": 25,
        "first_yield_day": 2, "max_yield_day": 4,
        "max_units_base": 4, "max_units_fert": 6,
        "bonus_start_day": 2, "is_ongoing": False,
    },
    "CARROT": {
        "seed_cost": 20, "base_price": 35,
        "first_yield_day": 2, "max_yield_day": 3,
        "max_units_base": 3, "max_units_fert": 4,
        "bonus_start_day": 2, "is_ongoing": False,
    },
    "TOMATO": {
        "seed_cost": 50, "base_price": 60,
        "first_yield_day": 8, "max_yield_day": 11,
        "is_ongoing": True,
        "bonus_start_day": 8, "yield_days": [8, 9, 10, 11],
    },
    "STRAWBERRY": {
        "seed_cost": 100, "base_price": 120,
        "first_yield_day": 10, "max_yield_day": 16,
        "is_ongoing": True,
        "bonus_start_day": 10, "yield_days": [10, 12, 14, 16],
    },
    "MELON": {
        "seed_cost": 80, "base_price": 250,
        "first_yield_day": 10, "max_yield_day": 10,
        "is_ongoing": False,
        "bonus_start_day": 6, "max_units_base": 6, "max_units_fert": 6,
    },
}

ANIMALS: dict[str, dict[str, Any]] = {
    "GOOSE": {"cost": 300, "base_price": 50, "structure": "COOP", "first_yield_day": 4, "interval": 1, "product": "EGG"},
    "COW":   {"cost": 400, "base_price": 160, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "product": "MILK"},
    "SHEEP": {"cost": 500, "base_price": 200, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "product": "WOOL"},
}

MARKET_PARAMS: dict[str, dict[str, Any]] = {
    "WHEAT":       {"base": 25,  "T": 400, "below_func": "sqrt",  "below_target": 0.80, "above_func": "log",    "above_target": 0.20},
    "CARROT":      {"base": 35,  "T": 450, "below_func": "hinge", "below_target": 1.00, "above_func": "sqrt",   "above_target": 0.70},
    "TOMATO":      {"base": 60,  "T": 200, "below_func": "hinge", "below_target": 0.40, "above_func": "sqrt",   "above_target": 0.60},
    "STRAWBERRY":  {"base": 120, "T": 100, "below_func": "sqrt",  "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON":       {"base": 250, "T": 300, "below_func": "log",   "below_target": 0.20, "above_func": "sq",     "above_target": 3.60},
    "EGG":         {"base": 50,  "T": 332, "below_func": "hinge", "below_target": 0.40, "above_func": "log",    "above_target": 0.20},
    "MILK":        {"base": 160, "T": 122, "below_func": "sqrt",  "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL":        {"base": 200, "T": 105, "below_func": "log",   "below_target": 0.20, "above_func": "sq",     "above_target": 3.20},
    "FERTILIZER":  {"base": 100, "T": 200, "below_func": "linear","below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}

FIBONACCI_HIRE_COSTS: tuple[int, ...] = (
    1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765,
)

class _Constants:
    def __getattr__(self, name: str) -> Any:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(f'Constant {name!r} is not defined') from None

c = _Constants()


# ---------------------------------------------------------------------------
# MODULE: market.py
# ---------------------------------------------------------------------------

def total_hire_cost(count: int, already_hired: int) -> int:
    if count < 0 or already_hired < 0 or already_hired + count > len(c.FIBONACCI_HIRE_COSTS):
        raise ValueError(
            f"Invalid hire range: count={count}, already_hired={already_hired}, max_limit={len(c.FIBONACCI_HIRE_COSTS)}"
        )
    return sum(c.FIBONACCI_HIRE_COSTS[already_hired : already_hired + count])


def _shape(func: str, x: float, t: float) -> float:
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(max(0.0, x))
    if func == "log":
        return math.log(1.0 + max(0.0, x))
    if func == "hinge":
        u = x / max(1.0, t)
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    raise ValueError(f"Unknown shape function: {func!r}")


def market_price(item: str, inv: int) -> int:
    if item not in c.MARKET_PARAMS:
        raise ValueError(f"Unknown market item: {item!r}")
    p = c.MARKET_PARAMS[item]
    base = float(p["base"])
    t = float(p["T"])
    if inv == c.I0:
        return int(round(base))
    if inv < c.I0:
        x = float(c.I0 - inv)
        denom = _shape(p["below_func"], t, t)
        amp = (p["below_target"] * base) / denom if denom > 0 else 0.0
        return max(1, int(round(base + amp * _shape(p["below_func"], x, t))))
    x = float(inv - c.I0)
    denom = _shape(p["above_func"], t, t)
    amp = (p["above_target"] * base) / denom if denom > 0 else 0.0
    return max(1, int(round(base - amp * _shape(p["above_func"], x, t))))


def get_price(item: str, market_inv: dict[str, int]) -> int:
    return market_price(item, market_inv.get(item, c.I0))


# ---------------------------------------------------------------------------
# MODULE: navigation.py
# ---------------------------------------------------------------------------

def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def quad_of(pos: tuple[int, int]) -> str:
    half = c.BOARD_SIZE // 2
    if pos[1] < half:
        return "NE" if pos[0] >= half else "NW"
    return "SE" if pos[0] >= half else "SW"


def is_on_shed_tile(pos: tuple[int, int]) -> bool:
    return pos in c.SHED_TILES_SET


def closest_shed_pos(pos: tuple[int, int]) -> tuple[int, int]:
    return min(c.SHED_TILES, key=lambda s: manhattan(pos, s))


def bfs_step(start: tuple[int, int], goal: tuple[int, int]) -> str | None:
    if start == goal:
        return None
    dx, dy = goal[0] - start[0], goal[1] - start[1]
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def go_shed_or_drop(pos: tuple[int, int]) -> list[Any]:
    if is_on_shed_tile(pos):
        return ["DROP"]
    return [bfs_step(pos, closest_shed_pos(pos)) or "PASS"]


# ---------------------------------------------------------------------------
# MODULE: farm.py
# ---------------------------------------------------------------------------

@dataclass(slots=True, frozen=True)
class AnimalCensus:
    field_cows: int
    field_sheep: int
    field_geese: int
    shed_cows: int
    shed_sheep: int
    shed_geese: int
    carried_cows: int
    carried_sheep: int
    carried_geese: int

    @property
    def total_cows(self) -> int:
        return self.field_cows + self.shed_cows + self.carried_cows

    @property
    def total_sheep(self) -> int:
        return self.field_sheep + self.shed_sheep + self.carried_sheep

    @property
    def total_geese(self) -> int:
        return self.field_geese + self.shed_geese + self.carried_geese

    @property
    def total(self) -> int:
        return self.total_cows + self.total_sheep

    @property
    def total_all(self) -> int:
        return self.total + self.total_geese

    @property
    def on_field(self) -> int:
        return self.field_cows + self.field_sheep + self.field_geese

    @property
    def in_shed(self) -> int:
        return self.shed_cows + self.shed_sheep + self.shed_geese

    @property
    def n_feedable(self) -> int:
        return self.on_field + self.in_shed


def count_animal_census(
    farm_state: dict[str, Any],
    shed: dict[str, int],
    inventories: list[dict[str, int]],
) -> AnimalCensus:
    return AnimalCensus(
        field_cows=sum(1 for a in farm_state["animals"] if a["animal"] == "COW"),
        field_sheep=sum(1 for a in farm_state["animals"] if a["animal"] == "SHEEP"),
        field_geese=sum(1 for a in farm_state["animals"] if a["animal"] == "GOOSE"),
        shed_cows=shed.get("COW", 0),
        shed_sheep=shed.get("SHEEP", 0),
        shed_geese=shed.get("GOOSE", 0),
        carried_cows=sum(inv.get("COW", 0) for inv in inventories),
        carried_sheep=sum(inv.get("SHEEP", 0) for inv in inventories),
        carried_geese=sum(inv.get("GOOSE", 0) for inv in inventories),
    )


def kept_feedable_count(census: AnimalCensus, retained_caps: dict[str, int] | None) -> int:
    """On-field + in-shed animals that survive a cull's retained_caps, per species."""
    caps = retained_caps if retained_caps is not None else {}
    return (
        min(census.field_cows + census.shed_cows, caps.get("COW", 999))
        + min(census.field_sheep + census.shed_sheep, caps.get("SHEEP", 999))
        + min(census.field_geese + census.shed_geese, caps.get("GOOSE", 999))
    )


def wheat_feed_thresholds(
    census: AnimalCensus, retained_caps: dict[str, int] | None, day: int
) -> tuple[int, int]:
    """Buy floor and sell ceiling for shed wheat, with a deliberate dead zone."""
    if day >= c.LIQUIDATION_DAY:
        return 0, 0
    n_kept = kept_feedable_count(census, retained_caps)
    floor = max(c.FEED_WHEAT_RESERVE, n_kept * c.FEED_WHEAT_RESERVE_MIN_RATIO)
    ceiling = max(c.FEED_WHEAT_RESERVE * c.FEED_WHEAT_SELL_RATIO, n_kept * c.FEED_WHEAT_SELL_RATIO)
    return floor, ceiling


def parse_farm_state(tiles: list[list[Any]], day: int) -> dict[str, Any]:
    state: dict[str, Any] = {
        "animals": [],
        "empty_pastures": [],
        "empty_coops": [],
        "plants": [],
        "weeds": [],
        "empty_tiles": [],
        "unlocked_count": 0,
    }

    for y in range(c.BOARD_SIZE):
        for x in range(c.BOARD_SIZE):
            tile = tiles[y][x]
            pos = (x, y)

            if tile == "LOCKED":
                continue
            state["unlocked_count"] += 1

            if tile is None:
                state["empty_tiles"].append(pos)
                continue

            if not isinstance(tile, dict):
                raise TypeError(f"Unexpected tile structure at {pos}: {tile!r}")

            kind = tile.get("kind")
            if kind == "WEED":
                state["weeds"].append(pos)
            elif kind in ("PASTURE", "COOP"):
                animal = tile.get("animal")
                if animal is None:
                    if kind == "COOP":
                        state["empty_coops"].append(pos)
                    else:
                        state["empty_pastures"].append(pos)
                else:
                    state["animals"].append({
                        "pos": pos,
                        "animal": animal,
                        "fed_today": tile.get("fed_today", False),
                        "consecutive_unfed": tile.get("consecutive_unfed", 0),
                        "cared_today": tile.get("cared_today", False),
                        "fertilizer_available": tile.get("fertilizer_available", False),
                        "yield_units": tile.get("yield_units", 0),
                    })
            elif kind == "PLANT":
                crop = tile.get("crop")
                if crop is None or crop not in c.CROPS:
                    raise ValueError(f"Unknown or missing crop {crop!r} at {pos}: {tile}")
                planted_day = tile.get("planted_day", day)
                age = day - planted_day
                spec = c.CROPS[crop]
                yu = tile.get("yield_units", 0)
                watered = tile.get("watered_today", False)
                fert_until = tile.get("fertilized_until_day", -1)

                if spec["is_ongoing"]:
                    is_expired = age >= spec["yield_days"][-1] + 1
                else:
                    is_expired = age >= spec["max_yield_day"] + 1

                fert_due = False
                if spec["is_ongoing"]:
                    upcoming_ages = [d for d in spec["yield_days"] if d >= age]
                    if upcoming_ages:
                        days_to_yield = upcoming_ages[0] - age
                        yield_day = day + days_to_yield
                        fert_due = days_to_yield <= 1 and fert_until < yield_day

                state["plants"].append({
                    "pos": pos,
                    "crop": crop,
                    "age": age,
                    "watered_today": watered,
                    "yield_units": yu,
                    "fertilize_due": fert_due,
                    "is_expired": is_expired,
                    "is_ongoing": spec["is_ongoing"],
                    "first_yield_day": spec["first_yield_day"],
                    "max_yield_day": spec["max_yield_day"],
                })
            else:
                raise ValueError(f"Unknown tile kind {kind!r} at {pos}: {tile}")

    return state


def planted_count(farm_state: dict[str, Any], crop: str) -> int:
    return sum(1 for p in farm_state["plants"] if p["crop"] == crop)


def committed_count(farm_state: dict[str, Any], seeds: dict[str, int], crop: str) -> int:
    return planted_count(farm_state, crop) + seeds.get(crop, 0)


def count_fertilize_due(farm_state: dict[str, Any]) -> int:
    return sum(1 for p in farm_state["plants"] if p["fertilize_due"])


def live_reserved_pastures(
    cluster: list[tuple[int, int]],
    unlocked_quads: list[str],
    target_slots: int,
    day: int,
) -> frozenset[tuple[int, int]]:
    if day > c.PASTURE_RESERVATION_LAST_DAY:
        return frozenset()
    quad_cap = 4 if len(unlocked_quads) == 1 else min(c.MAX_TOTAL_HERD, len(unlocked_quads) * 6)
    effective_target = max(target_slots, quad_cap)
    reserved: set[tuple[int, int]] = set()
    for pos in cluster:
        if len(reserved) >= effective_target:
            break
        if quad_of(pos) in unlocked_quads:
            reserved.add(pos)
    return frozenset(reserved)


def coop_capacity(farm_state: dict[str, Any]) -> int:
    """Geese that can already be housed by structures standing on the
    ground: built-and-empty coops, plus coops a goose already occupies."""
    return len(farm_state["empty_coops"]) + sum(
        1 for a in farm_state["animals"] if a["animal"] == "GOOSE"
    )


def live_reserved_coops(
    farm_state: dict[str, Any],
    exclude: frozenset[tuple[int, int]] | set[tuple[int, int]],
    target_geese: int,
    day: int = 0,
    unlocked_quads: list[str] | None = None,
) -> frozenset[tuple[int, int]]:
    """Reserve empty tiles closest to the shed for a pending goose target."""
    if day >= c.LIQUIDATION_DAY or (unlocked_quads is not None and len(unlocked_quads) < 2):
        return frozenset()
    need = target_geese - coop_capacity(farm_state)
    if need <= 0:
        return frozenset()
    candidates = sorted(
        (pos for pos in farm_state["empty_tiles"] if pos not in exclude),
        key=lambda p: manhattan(p, c.SHED_TILES[0]),
    )
    return frozenset(candidates[:need])


# ---------------------------------------------------------------------------
# MODULE: dispatch.py
# ---------------------------------------------------------------------------

"""Workforce dispatch — daily VRP planner (parallel cheapest insertion) + fail-fast executor."""




# ---------------------------------------------------------------------------
# Shed access geometry
# ---------------------------------------------------------------------------
_SHED_ACCESS: tuple[tuple[int, int], ...] = tuple(c.SHED_TILES)
_SHED_ACCESS_SET: frozenset[tuple[int, int]] = c.SHED_TILES_SET
_SHED_CENTER: tuple[int, int] = c.SHED_TILES[0]

_MOVES: dict[str, tuple[int, int]] = {
    "EAST": (1, 0),
    "WEST": (-1, 0),
    "SOUTH": (0, 1),
    "NORTH": (0, -1),
}

# ---------------------------------------------------------------------------
# Urgency scale & Premium delivery config
# ---------------------------------------------------------------------------
_URG_FEED_CRITICAL: int = 100
_URG_PLACE: int = 95
_URG_FEED: int = 90
_URG_WATER: int = 80
_URG_HARVEST_PREMIUM: int = 75  # priority-tier boundary for premium rounds — see _solve_day
_URG_PLANT_PRIORITY: int = 72
_URG_HARVEST: int = 70
_URG_PLANT: int = 68
_URG_CARE: int = 65
_URG_FERTILIZE: int = 55
_URG_COLLECT_FERTILIZER: int = 50
_URG_BUILD_IDLE: int = 40
_URG_DIG_EXPIRED: int = 30
_URG_DIG_WEED: int = 20

# Crops that must reach the shed the SAME DAY they are harvested (steep glut curve —
# selling all at once late in the day tanks the price; regular crops ride home for free
# via the engine's end-of-day inventory drop). Mechanism: any route that picks up premium
# cargo pays a projected final-DROP surcharge during insertion (so the detour always fits
# the budget), and `_append_drops` materializes exactly one DROP at the route's end.
# The whole route executes within the day, so premium produce is in the shed by daytime.
_PREMIUM_DROP_CROPS: frozenset[str] = frozenset(("MELON", "STRAWBERRY"))
_ANIMAL_SPECIES: tuple[str, ...] = ("COW", "SHEEP", "GOOSE")
_PASTURE_SPECIES: tuple[str, ...] = ("COW", "SHEEP")


def _plant_ready_to_harvest(p: dict[str, Any], day: int) -> bool:
    return p["yield_units"] > 0 and (
        p["is_ongoing"]
        or p["age"] >= p["max_yield_day"]
        or day >= c.LIQUIDATION_DAY
    )


def _ready_premium_bushes(farm_state: dict[str, Any], day: int) -> list[dict[str, Any]]:
    """Melon/strawberry bushes ready to pick — routed via _plan_premium_rounds, never
    through build_task_catalog (bush-count pairing has no notion of yield_units)."""
    return [
        p for p in farm_state["plants"]
        if not p["is_expired"] and p["crop"] in _PREMIUM_DROP_CROPS and _plant_ready_to_harvest(p, day)
    ]


# ---------------------------------------------------------------------------
# Task catalog & Atomic builders
# ---------------------------------------------------------------------------

@dataclass(slots=True, frozen=True)
class Task:
    urgency: int
    pos: tuple[int, int]
    actions: tuple[list[Any], ...]     # atomic sequence executed at one stop
    need: tuple[str, ...] = ()         # OR-alternatives; solver picks the cheapest available
    produces: tuple[str, int] | None = None  # (item, qty) — set only on HARVEST/COLLECT_FERTILIZER


def _plant_task(urgency: int, pos: tuple[int, int], crop: str) -> Task:
    return Task(urgency, pos, (["PLANT", crop], ["WATER"]))


def _harvest_actions(watered_today: bool, day: int) -> list[list[Any]]:
    """WATER-then-HARVEST if not watered today (and pre-liquidation), else HARVEST alone.
    Shared by the regular catalog harvest task and premium round blocks."""
    return [["WATER"], ["HARVEST"]] if not watered_today and day < c.LIQUIDATION_DAY else [["HARVEST"]]


def _harvest_task(
    urgency: int, pos: tuple[int, int], watered_today: bool, day: int,
    crop: str, qty: int,
) -> Task:
    """WATER + same-day HARVEST as one atomic stop."""
    return Task(urgency, pos, tuple(_harvest_actions(watered_today, day)), produces=(crop, qty))


def _build_and_place_task(
    urgency: int, pos: tuple[int, int], build_action: str, species: tuple[str, ...]
) -> Task:
    return Task(urgency, pos, ([build_action], ["PLACE"]), need=species)


def select_target_crops(day: int, seeds_stock: dict[str, int]) -> list[str]:
    if day > c.WHEAT_LAST_PLANT_DAY:
        return []
    if day >= 21:
        return ["WHEAT"] if seeds_stock.get("WHEAT", 0) > 0 else []
    # Before day 13 melon goes first; afterwards strawberry's earlier deadline takes priority.
    premium_order = ("MELON", "STRAWBERRY") if day <= 12 else ("STRAWBERRY", "MELON")
    deadlines = {"MELON": c.MELON_LAST_PLANT_DAY, "STRAWBERRY": c.STRAWBERRY_LAST_PLANT_DAY}
    return [
        crop for crop in (*premium_order, "WHEAT")
        if seeds_stock.get(crop, 0) > 0 and day <= deadlines.get(crop, c.WHEAT_LAST_PLANT_DAY)
    ]


def compute_needed_pastures(
    farm_state: dict[str, Any],
    census: AnimalCensus,
) -> list[tuple[int, int]]:
    needed: list[tuple[int, int]] = []
    planted = {p["pos"] for p in farm_state["plants"]}
    occupied_pastures = census.field_cows + census.field_sheep
    for p_pos in c.PASTURE_CLUSTER:
        if len(needed) + occupied_pastures + len(farm_state["empty_pastures"]) >= census.total:
            break
        if p_pos in farm_state["empty_tiles"] or p_pos in farm_state["weeds"] or p_pos in planted:
            needed.append(p_pos)
    return needed


def _resolve_structure_action(
    pos: tuple[int, int],
    farm_state: dict[str, Any],
    planted_positions: dict[tuple[int, int], dict[str, Any]],
    build_action: str,
) -> list[Any] | None:
    if pos in farm_state["weeds"]:
        return ["DIG"]
    if pos in planted_positions:
        p = planted_positions[pos]
        if p["yield_units"] > 0 or (not p["is_ongoing"] and p["age"] >= p["first_yield_day"] - 1):
            return None
        return ["DIG"]
    if pos in farm_state["empty_tiles"]:
        return [build_action]
    return None


def _kept_animal_positions(
    farm_state: dict[str, Any],
    retained_caps: dict[str, int] | None,
) -> set[tuple[int, int]]:
    caps = retained_caps if retained_caps is not None else {}
    kept: set[tuple[int, int]] = set()
    for species in _ANIMAL_SPECIES:
        cap = caps.get(species, 999)
        if cap <= 0:
            continue
        species_animals = [a for a in farm_state["animals"] if a["animal"] == species]
        species_animals.sort(key=lambda a: (a["fed_today"], manhattan(a["pos"], _SHED_CENTER)))
        kept.update(a["pos"] for a in species_animals[:cap])
    return kept


def build_task_catalog(
    farm_state: dict[str, Any],
    shed: dict[str, int],
    seeds_stock: dict[str, int],
    needed_pastures: list[tuple[int, int]],
    all_units: list[tuple[tuple[int, int], dict[str, int]]],
    day: int,
    hour: int,
    hints: dict[str, Any],
    unlocked_quads: list[str],
    retained_caps: dict[str, int] | None = None,
) -> list[Task]:
    tasks: list[Task] = []
    kept_animals = _kept_animal_positions(farm_state, retained_caps)

    carried: dict[str, int] = {
        sp: sum(inv.get(sp, 0) for _, inv in all_units) for sp in _ANIMAL_SPECIES
    }
    wheat_available = shed.get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for _, inv in all_units)
    fert_available = shed.get("FERTILIZER", 0) + sum(inv.get("FERTILIZER", 0) for _, inv in all_units)

    res_pasture = live_reserved_pastures(c.PASTURE_CLUSTER, unlocked_quads, hints["reserved_grazer_slots"], day=day)
    needed_structs = set(needed_pastures)
    res_coops = live_reserved_coops(
        farm_state, res_pasture | needed_structs, hints["reserved_geese_slots"], day=day, unlocked_quads=unlocked_quads
    )

    # 1. Animal care
    for a in farm_state["animals"]:
        pos = a["pos"]
        product = c.ANIMALS[a["animal"]]["product"]
        if pos not in kept_animals:
            if a["yield_units"] > 0:
                tasks.append(Task(_URG_HARVEST, pos, (["HARVEST"],), produces=(product, a["yield_units"])))
            if a["fertilizer_available"]:
                tasks.append(Task(_URG_COLLECT_FERTILIZER, pos, (["COLLECT_FERTILIZER"],), produces=("FERTILIZER", 1)))
            continue
        if not a["fed_today"] and wheat_available > 0:
            urg = _URG_FEED_CRITICAL if a["consecutive_unfed"] >= 1 else _URG_FEED
            tasks.append(Task(urg, pos, (["FEED"],), need=("WHEAT",)))
        if not a["cared_today"]:
            tasks.append(Task(_URG_CARE, pos, (["CARE"],)))
        if a["fertilizer_available"]:
            tasks.append(Task(_URG_COLLECT_FERTILIZER, pos, (["COLLECT_FERTILIZER"],), produces=("FERTILIZER", 1)))
        if a["yield_units"] > 0:
            tasks.append(Task(_URG_HARVEST, pos, (["HARVEST"],), produces=(product, a["yield_units"])))

    # 2. Animal placement — waiting = shed stock + carried, only while under the retained cap
    caps = retained_caps if retained_caps is not None else {}
    field_count = {sp: sum(1 for a in farm_state["animals"] if a["animal"] == sp) for sp in _ANIMAL_SPECIES}
    waiting = {
        sp: (shed.get(sp, 0) + carried[sp]) if field_count[sp] < caps.get(sp, 999) else 0
        for sp in _ANIMAL_SPECIES
    }
    pasture_waiting = waiting["COW"] + waiting["SHEEP"]
    geese_waiting = waiting["GOOSE"]

    for spots_key, n_waiting, species in (
        ("empty_pastures", pasture_waiting, _PASTURE_SPECIES),
        ("empty_coops", geese_waiting, ("GOOSE",)),
    ):
        if n_waiting > 0 and farm_state[spots_key]:
            spots = sorted(
                farm_state[spots_key],
                key=lambda p: (manhattan(p, _SHED_CENTER), p[1], p[0]),
            )
            for pos in spots[:n_waiting]:
                tasks.append(Task(_URG_PLACE, pos, (["PLACE"],), need=species))

    # 3. Crops — melon/strawberry are excluded here entirely; _plan_premium_rounds
    #    handles them as bush-pair-then-DROP blocks, not individual Tasks.
    for p in farm_state["plants"]:
        if p["is_expired"]:
            tasks.append(Task(_URG_DIG_EXPIRED, p["pos"], (["DIG"],)))
        elif _plant_ready_to_harvest(p, day):
            if p["crop"] not in _PREMIUM_DROP_CROPS:
                tasks.append(_harvest_task(_URG_HARVEST, p["pos"], p["watered_today"], day, p["crop"], p["yield_units"]))
        elif not p["watered_today"] and day < c.LIQUIDATION_DAY:
            tasks.append(Task(_URG_WATER, p["pos"], (["WATER"],)))

        if p["fertilize_due"] and fert_available > 0:
            tasks.append(Task(_URG_FERTILIZE, p["pos"], (["FERTILIZE"],), need=("FERTILIZER",)))

    # 4. Weeds
    if day <= c.WHEAT_LAST_PLANT_DAY:
        for pos in farm_state["weeds"]:
            tasks.append(Task(_URG_DIG_WEED, pos, (["DIG"],)))

    # 5. Crop planting — one queue, one slicing loop: (crop, urgency, limit)
    if hour < c.TURNS_PER_DAY - 1:
        plantable = [
            pos for pos in farm_state["empty_tiles"]
            if pos not in res_pasture and pos not in needed_structs and pos not in res_coops
        ]
        plantable.sort(key=lambda p: (manhattan(p, _SHED_CENTER), p[1], p[0]))
        target_crops = select_target_crops(day, seeds_stock)

        plant_queue: list[tuple[str, int, int]] = [
            (crop, _URG_PLANT_PRIORITY, seeds_stock.get(crop, 0))
            for crop in ("MELON", "STRAWBERRY")
            if crop in target_crops
        ]
        crop_limits = hints.get("crop_limits", {})
        plant_queue += [
            (pivot, _URG_PLANT, min(seeds_stock.get(pivot, 0), crop_limits.get(pivot, 0)))
            for pivot in ("CARROT", "TOMATO")
        ]
        plant_queue += [
            (crop, _URG_PLANT, seeds_stock.get(crop, 0))
            for crop in target_crops
            if crop not in _PREMIUM_DROP_CROPS
        ]

        for crop, urg, limit in plant_queue:
            if not plantable:
                break
            n = min(len(plantable), limit)
            if n > 0:
                tasks.extend(_plant_task(urg, pos, crop) for pos in plantable[:n])
                plantable = plantable[n:]

    # 6. Pasture & coop construction
    planted_positions = {p["pos"]: p for p in farm_state["plants"]}
    pasture_leftover = max(0, pasture_waiting - len(farm_state["empty_pastures"]))
    n_bundled = 0
    for pos in needed_pastures:
        act = _resolve_structure_action(pos, farm_state, planted_positions, "BUILD_PASTURE")
        if act is None:
            continue
        if act == ["BUILD_PASTURE"] and n_bundled < pasture_leftover:
            tasks.append(_build_and_place_task(_URG_PLACE, pos, "BUILD_PASTURE", _PASTURE_SPECIES))
            n_bundled += 1
        else:
            tasks.append(Task(_URG_BUILD_IDLE, pos, (act,)))

    needed_new_coops = max(0, geese_waiting - len(farm_state["empty_coops"]))
    if needed_new_coops > 0:
        coop_candidates = [
            pos for pos in farm_state["empty_tiles"]
            if pos not in res_pasture and pos not in needed_structs
        ]
        coop_candidates.sort(key=lambda p: manhattan(p, _SHED_CENTER))
        for pos in coop_candidates[:needed_new_coops]:
            tasks.append(_build_and_place_task(_URG_PLACE, pos, "BUILD_COOP", ("GOOSE",)))

    tasks.sort(key=lambda t: (-t.urgency, manhattan(t.pos, _SHED_CENTER), t.pos[1], t.pos[0], str(t.actions)))
    return tasks


# ---------------------------------------------------------------------------
# VRP solver & Executor
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class _Stop:
    pos: tuple[int, int]
    actions: list[list[Any]]
    produces: tuple[str, int] | None = None


@dataclass(slots=True)
class _Route:
    start: tuple[int, int]
    stops: list[_Stop] = field(default_factory=list)
    cost: int = 0
    carried: dict[str, int] = field(default_factory=dict)
    pickup_of: dict[str, int] = field(default_factory=dict)
    # Index before which insertion is allowed. None = fully open. Set once a premium
    # block/flush-drop is appended, so later passes can only insert *before* that
    # locked tail — never split a committed bush-pair-then-DROP trip.
    insertable_upto: int | None = None


def _route_cost(route: _Route) -> int:
    total = 0
    pos = route.start
    for s in route.stops:
        total += manhattan(pos, s.pos) + len(s.actions)
        pos = s.pos
    return total


def _drop_cost(pos: tuple[int, int]) -> int:
    """Turns to reach the nearest shed tile from pos and issue DROP (1 if already there)."""
    _, d = _best_pickup_tile(pos, None)
    return d + 1


def _rebuild_pickups(route: _Route) -> dict[str, int]:
    pickup_of: dict[str, int] = {}
    for idx, stop in enumerate(route.stops):
        for line in stop.actions:
            if line[0] == "PICKUP" and line[1] not in pickup_of:
                pickup_of[line[1]] = idx
    return pickup_of


def _best_pickup_tile(prev: tuple[int, int], nxt: tuple[int, int] | None) -> tuple[tuple[int, int], int]:
    base = manhattan(prev, nxt) if nxt is not None else 0
    best_p: tuple[int, int] = _SHED_ACCESS[0]
    best_d = math.inf
    for p in _SHED_ACCESS:
        d = manhattan(prev, p) + (manhattan(p, nxt) if nxt is not None else 0) - base
        if d < best_d:
            best_d, best_p = d, p
    return best_p, int(best_d)


_Mode = Literal["plain", "carried", "bump", "extend", "new"]


@dataclass(slots=True)
class _Candidate:
    cost: int
    insert_at: int
    item: str | None
    mode: _Mode
    pickup_idx: int = -1
    pickup_pos: tuple[int, int] | None = None


def _eval_route(
    route: _Route,
    task: Task,
    shed_stock: dict[str, int],
) -> _Candidate | None:
    stops = route.stops
    n = len(stops)
    limit = route.insertable_upto if route.insertable_upto is not None else n
    start = route.start

    # Cheapest shed detour for a PICKUP inserted before each position (prefix minimum).
    pref_cost = [math.inf] * (n + 1)
    pref_k = [-1] * (n + 1)
    best = math.inf
    best_k = -1
    for k in range(n):
        prev = start if k == 0 else stops[k - 1].pos
        _, d = _best_pickup_tile(prev, stops[k].pos)
        d += 1
        if d < best:
            best, best_k = d, k
        pref_cost[k + 1] = best
        pref_k[k + 1] = best_k

    earliest_pickup = min(route.pickup_of.values(), default=None)
    items: tuple[str | None, ...] = task.need if task.need else (None,)
    task_cost = len(task.actions)
    best_cand: _Candidate | None = None

    # `limit` stops at the first stop of a locked premium block (if any), so a bush-pair
    # -then-DROP trip already committed by _plan_premium_rounds never gets split here.
    for i in range(limit + 1):
        prev = start if i == 0 else stops[i - 1].pos
        nxt = stops[i].pos if i < n else None

        back_leg = manhattan(task.pos, nxt) - manhattan(prev, nxt) if nxt is not None else 0
        d_task = manhattan(prev, task.pos) + back_leg + task_cost

        for item in items:
            if item is None:
                cand = _Candidate(d_task, i, None, "plain")
            elif route.carried.get(item, 0) > 0:
                cand = _Candidate(d_task, i, item, "carried")
            elif shed_stock.get(item, 0) <= 0:
                continue
            elif (j := route.pickup_of.get(item)) is not None and j < i:
                cand = _Candidate(d_task, i, item, "bump")
            elif earliest_pickup is not None and earliest_pickup < i:
                cand = _Candidate(d_task + 1, i, item, "extend")
            else:
                d_new = pref_cost[i]
                k_new = pref_k[i]
                p_new: tuple[int, int] | None = None
                p_det, d_det = _best_pickup_tile(prev, task.pos)
                d_det += 1
                if d_det <= d_new:
                    d_new, k_new, p_new = d_det, i, p_det
                if math.isinf(d_new):
                    continue
                cand = _Candidate(d_task + d_new, i, item, "new", pickup_idx=k_new, pickup_pos=p_new)

            if best_cand is None or cand.cost < best_cand.cost:
                best_cand = cand

    return best_cand


def _commit(
    route: _Route,
    task: Task,
    cand: _Candidate,
    shed_stock: dict[str, int],
) -> None:
    stops = route.stops
    n_before = len(stops)
    insert_at = cand.insert_at
    item = cand.item

    if cand.mode == "new":
        assert item is not None, f"mode=new requires item, task={task}"
        pickup_pos = cand.pickup_pos
        if pickup_pos is None:
            prev = route.start if cand.pickup_idx == 0 else stops[cand.pickup_idx - 1].pos
            pickup_pos, _ = _best_pickup_tile(prev, stops[cand.pickup_idx].pos)
        stops.insert(cand.pickup_idx, _Stop(pickup_pos, [["PICKUP", item, 1]]))
        insert_at += 1
        shed_stock[item] -= 1
    elif cand.mode == "bump":
        assert item is not None, f"mode=bump requires item, task={task}"
        j = route.pickup_of[item]
        for line in stops[j].actions:
            if line[0] == "PICKUP" and line[1] == item:
                line[2] += 1
                break
        shed_stock[item] -= 1
    elif cand.mode == "extend":
        assert item is not None, f"mode=extend requires item, task={task}"
        j = min(route.pickup_of.values())
        stops[j].actions.append(["PICKUP", item, 1])
        shed_stock[item] -= 1
    elif cand.mode == "carried":
        assert item is not None, f"mode=carried requires item, task={task}"
        route.carried[item] -= 1

    stop_actions: list[list[Any]] = [
        ["PLACE", item] if a[0] == "PLACE" and len(a) == 1 and item is not None else list(a)
        for a in task.actions
    ]
    stops.insert(insert_at, _Stop(task.pos, stop_actions, produces=task.produces))

    if route.insertable_upto is not None:
        route.insertable_upto += len(stops) - n_before

    route.cost = _route_cost(route)
    route.pickup_of = _rebuild_pickups(route)


def _init_routes(all_units: list[tuple[tuple[int, int], dict[str, int]]]) -> list[_Route]:
    return [
        _Route(start=pos, carried={k: v for k, v in inv.items() if v > 0})
        for pos, inv in all_units
    ]


def _plan_routes(
    routes: list[_Route],
    catalog: list[Task],
    shed_stock: dict[str, int],
    budget_list: list[int],
) -> None:
    for task in catalog:
        best_cand: tuple[int, int, _Candidate] | None = None
        for r_idx, route in enumerate(routes):
            cand = _eval_route(route, task, shed_stock)
            if cand is None:
                continue
            if route.cost + cand.cost > budget_list[r_idx]:
                continue
            if best_cand is None or cand.cost < best_cand[0]:
                best_cand = (cand.cost, r_idx, cand)
        if best_cand is None:
            continue
        _, r_idx, cand = best_cand
        _commit(routes[r_idx], task, cand, shed_stock)


def _append_drops(routes: list[_Route], budget_list: list[int]) -> None:
    """Opportunistic final DROP for routes carrying sellable cargo that isn't dropped
    yet. Premium cargo is dropped as soon as its harvest round completes (see
    _plan_premium_rounds / _flush_carried_premium) — a route whose last stop is
    already a DROP is skipped, so it never gets a second one.
    """
    for r_idx, route in enumerate(routes):
        if not route.stops or route.stops[-1].actions[-1][0] == "DROP":
            continue

        has_cargo = any(
            line[0] in ("HARVEST", "COLLECT_FERTILIZER") for s in route.stops for line in s.actions
        ) or any(route.carried.get(it, 0) > 0 for it in c.SELLABLE_ITEMS)
        if not has_cargo:
            continue

        last = route.stops[-1]
        delta = _drop_cost(last.pos)
        if route.cost + delta > budget_list[r_idx]:
            continue

        if last.pos in _SHED_ACCESS_SET:
            last.actions.append(["DROP"])
        else:
            p, _ = _best_pickup_tile(last.pos, None)
            route.stops.append(_Stop(p, [["DROP"]]))
        route.cost = _route_cost(route)


def _flush_carried_premium(routes: list[_Route]) -> None:
    """A route entering the hour already carrying melon/strawberry (left over from an
    interrupted trip — build_day_plan replans from live inventory every hour) must drop
    it before taking on anything else; same-day delivery can't wait for the opportunistic
    end-of-route drop. Unconditional: if budget truly can't cover it, build_day_plan's
    final budget assertion will say so loudly rather than silently deferring premium cargo.
    DROP empties everything the unit carries, so carried-inventory bookkeeping resets too.
    """
    for route in routes:
        if not any(route.carried.get(crop, 0) > 0 for crop in _PREMIUM_DROP_CROPS):
            continue
        if route.insertable_upto is None:
            route.insertable_upto = len(route.stops)
        tail = route.stops[-1].pos if route.stops else route.start
        drop_pos, _ = _best_pickup_tile(tail, None)
        route.stops.append(_Stop(drop_pos, [["DROP"]]))
        route.cost = _route_cost(route)
        route.carried.clear()


def _pair_premium_bushes(ready: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Nearest-neighbor pairing: repeatedly take a bush and match it with whichever
    remaining bush is closest. One trailing solo block if the count is odd."""
    pool = list(ready)
    blocks: list[list[dict[str, Any]]] = []
    while pool:
        a = pool.pop()
        if not pool:
            blocks.append([a])
            break
        j = min(range(len(pool)), key=lambda i: manhattan(a["pos"], pool[i]["pos"]))
        blocks.append([a, pool.pop(j)])
    return blocks


def _block_cost(
    tail: tuple[int, int], block: list[dict[str, Any]], day: int
) -> tuple[int, list[dict[str, Any]]]:
    """Cheapest way to run this 1-2 bush block from tail, ending with DROP. For a pair,
    tries both visiting orders and keeps the cheaper one."""
    orders = (block,) if len(block) == 1 else (block, block[::-1])
    best_cost = math.inf
    best_order = block
    for order in orders:
        pos = tail
        cost = 0
        for bush in order:
            cost += manhattan(pos, bush["pos"]) + len(_harvest_actions(bush["watered_today"], day))
            pos = bush["pos"]
        cost += _drop_cost(pos)
        if cost < best_cost:
            best_cost, best_order = cost, order
    return int(best_cost), list(best_order)


def _plan_premium_rounds(
    routes: list[_Route],
    ready_premium: list[dict[str, Any]],
    day: int,
    budget_list: list[int],
) -> None:
    """Assign bush-pair harvest+DROP blocks to whichever route runs them cheapest.
    Bushes are paired by mutual proximity first (independent of route assignment), then
    each block is appended at the tail of the cheapest-fitting route — always exactly
    2 bushes (1 if odd-one-out) per trip, no yield-unit counting. A block that fits no
    route's remaining budget this hour is simply skipped — the bush stays ready and is
    retried next hour, same as any other budget-starved catalog task.
    """
    for block in _pair_premium_bushes(ready_premium):
        best: tuple[int, int, list[dict[str, Any]]] | None = None  # (cost, route_idx, order)
        for r_idx, route in enumerate(routes):
            tail = route.stops[-1].pos if route.stops else route.start
            cost, order = _block_cost(tail, block, day)
            if route.cost + cost > budget_list[r_idx]:
                continue
            if best is None or cost < best[0]:
                best = (cost, r_idx, order)
        if best is None:
            continue
        _, r_idx, order = best
        route = routes[r_idx]
        if route.insertable_upto is None:
            route.insertable_upto = len(route.stops)
        for bush in order:
            route.stops.append(_Stop(
                bush["pos"], list(_harvest_actions(bush["watered_today"], day)),
                produces=(bush["crop"], bush["yield_units"]),
            ))
        drop_pos, _ = _best_pickup_tile(order[-1]["pos"], None)
        route.stops.append(_Stop(drop_pos, [["DROP"]]))
        route.cost = _route_cost(route)


def _solve_day(
    catalog: list[Task],
    ready_premium: list[dict[str, Any]],
    all_units: list[tuple[tuple[int, int], dict[str, int]]],
    shed: dict[str, int],
    budget_list: list[int],
    day: int,
) -> list[_Route]:
    """Three ordered passes: critical tasks (urgency above the premium tier), premium
    bush rounds (same-day melon/strawberry delivery), then the rest of the catalog.
    Premium rounds stay a separate pass — not folded into the generic cheapest-insertion
    solver — because a bush-pair-then-DROP trip is a fixed block, not a single-point
    insertion like every other Task; `_Route.insertable_upto` keeps the later pass from
    inserting into the middle of that block.
    """
    routes = _init_routes(all_units)
    shed_stock = dict(shed)

    critical = [t for t in catalog if t.urgency > _URG_HARVEST_PREMIUM]
    rest = [t for t in catalog if t.urgency <= _URG_HARVEST_PREMIUM]

    _plan_routes(routes, critical, shed_stock, budget_list)
    _flush_carried_premium(routes)
    _plan_premium_rounds(routes, ready_premium, day, budget_list)
    _plan_routes(routes, rest, shed_stock, budget_list)
    _append_drops(routes, budget_list)
    return routes


def required_hand_count(
    catalog: list[Task],
    ready_premium: list[dict[str, Any]],
    base_units: list[tuple[tuple[int, int], dict[str, int]]],
    shed: dict[str, int],
    max_hands: int,
    day: int,
) -> int:
    if len(base_units) > max_hands + 1:
        raise ValueError(f"base_units ({len(base_units)}) exceeds max allowed team ({max_hands + 1})")
    if not catalog and not ready_premium:
        return 0

    budget = c.TURNS_PER_DAY - 1
    current_units_count = len(base_units)
    max_team_size = current_units_count + max_hands
    target = len(catalog) + len(ready_premium)

    for team_size in range(current_units_count, max_team_size + 1):
        units = base_units + [
            (_SHED_ACCESS[i % len(_SHED_ACCESS)], {})
            for i in range(current_units_count, team_size)
        ]
        routes = _solve_day(catalog, ready_premium, units, shed, [budget] * len(units), day)
        inserted = sum(
            1 for r in routes for s in r.stops if s.actions[0][0] not in ("PICKUP", "DROP")
        )
        if inserted == target:
            return team_size - current_units_count

    return max_hands


# ---------------------------------------------------------------------------
# Day plan & Fail-fast executor
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class DayPlan:
    day: int
    routes: dict[int, list[list[Any]]]


def _materialize(route: _Route) -> list[list[Any]]:
    queue: list[list[Any]] = []
    pos = route.start
    for stop in route.stops:
        while pos != stop.pos:
            step = bfs_step(pos, stop.pos)
            if step is None:
                raise AssertionError(
                    f"bfs_step: no path {pos} -> {stop.pos}, route.start={route.start}"
                )
            queue.append([step])
            dx, dy = _MOVES[step]
            pos = (pos[0] + dx, pos[1] + dy)
        queue.extend(stop.actions)
    return queue


def build_day_plan(
    all_units: list[tuple[tuple[int, int], dict[str, int]]],
    farm_state: dict[str, Any],
    shed: dict[str, int],
    seeds: dict[str, int],
    day: int,
    hour: int,
    needed_pastures: list[tuple[int, int]],
    hints: dict[str, Any],
    unlocked_quads: list[str],
    retained_caps: dict[str, int] | None = None,
    pending_hires: int = 0,
) -> DayPlan:
    effective_hour = max(1, hour)
    budget = c.TURNS_PER_DAY - effective_hour

    full_units = list(all_units)
    budgets = [budget] * len(all_units) + [budget - 1] * pending_hires
    for i in range(pending_hires):
        spawn_pos = _SHED_ACCESS[(len(all_units) + i) % len(_SHED_ACCESS)]
        full_units.append((spawn_pos, {}))

    routes = _init_routes(full_units)
    if budget > 0 and full_units:
        catalog = build_task_catalog(
            farm_state, shed, dict(seeds), needed_pastures,
            full_units, day, effective_hour, hints=hints, unlocked_quads=unlocked_quads,
            retained_caps=retained_caps,
        )
        ready_premium = _ready_premium_bushes(farm_state, day)
        routes = _solve_day(catalog, ready_premium, full_units, shed, budgets, day)

    materialized = {ui: _materialize(r) for ui, r in enumerate(routes)}

    for ui, queue in materialized.items():
        if len(queue) > budgets[ui]:
            raise AssertionError(
                f"day={day} hour={hour} unit={ui}: materialized {len(queue)} actions "
                f"exceeds budget={budgets[ui]} (estimated route.cost={routes[ui].cost}), "
                f"stops={routes[ui].stops}"
            )

    return DayPlan(day=day, routes=materialized)


def next_action(unit_idx: int, day: int, plan: DayPlan) -> list[Any]:
    if plan.day != day:
        raise ValueError(f"Stale day plan: built for day {plan.day}, current day is {day}")
    if unit_idx not in plan.routes:
        raise ValueError(
            f"Unit {unit_idx} has no route in the day-{day} plan — a hand was "
            "likely hired after the plan was built."
        )
    queue = plan.routes[unit_idx]
    if not queue:
        return ["PASS"]
    return queue.pop(0)


# ---------------------------------------------------------------------------
# MODULE: evaluator.py
# ---------------------------------------------------------------------------

"""Unified economic evaluator — single decision point for all market actions in eco7.

Combines economic valuation, market order generation, and dispatch hinting
into a single, cohesive pipeline without duplicate guards or hardcoded day limits.
"""





# ---------------------------------------------------------------------------
# Output contract: evaluator → dispatch
# ---------------------------------------------------------------------------

@dataclass(slots=True, frozen=True)
class DispatchHints:
    """Minimal contract evaluator → dispatch."""
    reserved_grazer_slots: int
    reserved_geese_slots: int
    crop_limits: dict[str, int]


@dataclass(slots=True, frozen=True)
class TurnDecision:
    """Complete evaluator output for one game tick."""
    market_orders: list[list[Any]]
    hints: DispatchHints
    retained_caps: dict[str, int]
    needed_pastures: list[tuple[int, int]]


# ---------------------------------------------------------------------------
# Evaluator State (Persisted across turns)
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class DriftState:
    prev_inv: dict[str, int] = field(default_factory=dict)
    prev_day: int = -1
    observed: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class CullState:
    last_day: int = -1
    negative_days: dict[str, int] = field(default_factory=dict)
    downsized: set[str] = field(default_factory=set)
    retained_caps: dict[str, int] = field(default_factory=dict)


@dataclass(slots=True)
class EvalState:
    drift: DriftState = field(default_factory=DriftState)
    cull: CullState = field(default_factory=CullState)


# ---------------------------------------------------------------------------
# Candidate Valuation
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class CandidateScore:
    kind: str
    item: str
    cost: float
    daily_profit: float
    npv: float


def compute_daily_demand(unlocked_shops: list[str]) -> dict[str, float]:
    demand: dict[str, float] = {item: c.TOWN_CENTER_FLAT for item in c.SELLABLE_ITEMS}
    demand.pop("FERTILIZER", None)
    for shop in unlocked_shops:
        for item, qty in c.SHOP_DEMANDS.get(shop, {}).items():
            demand[item] = demand.get(item, 0.0) + qty
    return demand


def update_drift_tracker(day: int, market_inv: dict[str, int], state: DriftState) -> dict[str, float]:
    if day != state.prev_day:
        if state.prev_day >= 0:
            for item in c.SELLABLE_ITEMS:
                if item in state.prev_inv and item in market_inv:
                    state.observed[item] = float(state.prev_inv[item] - market_inv[item])
        state.prev_inv = dict(market_inv)
        state.prev_day = day
    return state.observed


def effective_drift(demand: dict[str, float], observed: dict[str, float]) -> dict[str, float]:
    return {
        item: max(demand.get(item, 0.0), 0.6 * observed.get(item, 0.0))
        for item in c.SELLABLE_ITEMS
    }


def herd_feed_cost(
    herd: int, drift: dict[str, float], market_inv: dict[str, int], horizon: int = 8
) -> float:
    w_drift = drift.get("WHEAT", 0.0) + float(herd)
    projected = max(1, market_inv.get("WHEAT", c.I0) - int(w_drift * horizon))
    return float(market_price("WHEAT", projected))


def expected_price(
    item: str,
    lag: int,
    market_inv: dict[str, int],
    drift: dict[str, float],
    additional_supply_units: float = 0.0,
) -> int:
    net_drift = drift.get(item, 0.0) - additional_supply_units
    projected_inv = market_inv.get(item, c.I0) - int(net_drift * lag)
    return market_price(item, max(1, projected_inv))


def demand_multiplier(item: str, demand: dict[str, float], market_inv: dict[str, int]) -> float:
    d = demand.get(item, 0.0)
    scarcity = c.I0 - market_inv.get(item, c.I0)
    if d >= 12.0:
        return 1.6
    if d >= 6.0:
        return 1.3
    if scarcity > 0.6 * c.MARKET_PARAMS[item]["T"]:
        return 1.4
    return 1.0


def evaluate_animal(
    species: str,
    day: int,
    total_herd: int,
    current_species_count: int,
    drift: dict[str, float],
    market_inv: dict[str, int],
    demand: dict[str, float],
) -> CandidateScore:
    spec = c.ANIMALS[species]
    cost = float(spec["cost"])
    item = spec["product"]
    lag = spec["first_yield_day"]
    interval = spec["interval"]
    days_left = c.TOTAL_DAYS - day - lag

    if days_left <= 0:
        return CandidateScore(species, item, cost, 0.0, -1.0)

    harvests = days_left // interval
    lifetime_units = harvests * interval
    own_supply = current_species_count * 1.0
    p = expected_price(item, lag, market_inv, drift, own_supply)
    revenue = lifetime_units * p * demand_multiplier(item, demand, market_inv)

    fert_price = float(get_price("FERTILIZER", market_inv))
    fert_revenue = (c.TOTAL_DAYS - day) * fert_price

    feed_price = herd_feed_cost(total_herd + 1, drift, market_inv)
    feed_cost = (c.TOTAL_DAYS - day) * feed_price
    labor_cost = (c.TOTAL_DAYS - day) * c.HAND_COST_PER_ANIMAL_DAY
    npv = revenue + fert_revenue - cost - feed_cost - labor_cost

    daily_profit = npv / max(1, c.TOTAL_DAYS - day)
    return CandidateScore(species, item, cost, daily_profit, npv)


def evaluate_fixed_crop(
    crop: str,
    day: int,
    drift: dict[str, float],
    market_inv: dict[str, int],
    demand: dict[str, float],
    current_crop_units: float = 0.0,
) -> CandidateScore:
    spec = c.CROPS[crop]
    cost = float(spec["seed_cost"])
    yield_days = spec["yield_days"]
    last_plant_day = c.STRAWBERRY_LAST_PLANT_DAY if crop == "STRAWBERRY" else c.TOTAL_DAYS - yield_days[0] - 2

    if day > last_plant_day:
        return CandidateScore(crop, crop, cost, 0.0, -1.0)

    valid_harvests = sum(1 for k in yield_days if day + k <= c.TOTAL_DAYS - 1)
    if valid_harvests <= 0:
        return CandidateScore(crop, crop, cost, 0.0, -1.0)

    expected_units = valid_harvests * 1.5
    lag = yield_days[0]
    p = expected_price(crop, lag, market_inv, drift, current_crop_units)
    revenue = expected_units * p * demand_multiplier(crop, demand, market_inv)
    npv = revenue - cost

    lifespan = min(c.TOTAL_DAYS - day, yield_days[-1] + 1)
    daily_profit = npv / max(1, lifespan)
    return CandidateScore(crop, crop, cost, daily_profit, npv)


def evaluate_replant_crop(
    crop: str,
    day: int,
    drift: dict[str, float],
    market_inv: dict[str, int],
    demand: dict[str, float],
    current_crop_units: float = 0.0,
) -> CandidateScore:
    spec = c.CROPS[crop]
    cost = float(spec["seed_cost"])
    grow_days = spec["max_yield_day"]
    yield_units = float(spec["max_units_base"])

    if crop == "MELON" and day > c.MELON_LAST_PLANT_DAY:
        return CandidateScore(crop, crop, cost, 0.0, -1.0)
    if crop == "WHEAT" and day > c.WHEAT_LAST_PLANT_DAY:
        return CandidateScore(crop, crop, cost, 0.0, -1.0)
    if day > c.TOTAL_DAYS - grow_days - 1:
        return CandidateScore(crop, crop, cost, 0.0, -1.0)

    p = expected_price(crop, grow_days, market_inv, drift, current_crop_units)
    revenue = yield_units * p * demand_multiplier(crop, demand, market_inv)
    profit_per_cycle = revenue - cost

    daily_profit = profit_per_cycle / max(1, grow_days)
    npv = daily_profit * (c.TOTAL_DAYS - day)
    return CandidateScore(crop, crop, cost, daily_profit, npv)


_DAILY_AP_USAGE: dict[str, float] = {
    "COW": 3.3,
    "SHEEP": 3.25,
    "GOOSE": 4.0,
    "STRAWBERRY": 1.5,
    "TOMATO": 1.5,
    "CARROT": 1.6,
    "WHEAT": 1.5,
}


def estimate_marginal_ap_cost(
    item_kind: str,
    acc_cows: int,
    acc_sheep: int,
    acc_geese: int,
    acc_crops: dict[str, int],
    day: int,
) -> float:
    """Estimates the marginal daily hiring cost if adding item_kind causes
    the required daily Action Points to cross a worker boundary."""
    current_ap = (
        acc_cows * _DAILY_AP_USAGE["COW"]
        + acc_sheep * _DAILY_AP_USAGE["SHEEP"]
        + acc_geese * _DAILY_AP_USAGE["GOOSE"]
        + sum(count * _DAILY_AP_USAGE.get(crop, 1.5) for crop, count in acc_crops.items())
    )
    wheat_basis = max(15, acc_cows + acc_sheep + acc_geese)
    current_ap += wheat_basis * _DAILY_AP_USAGE["WHEAT"]

    hands_before = max(0, math.ceil(current_ap / 22.0) - 1)

    item_ap = _DAILY_AP_USAGE.get(item_kind, 1.5)
    new_ap = current_ap + item_ap
    hands_after = max(0, math.ceil(new_ap / 22.0) - 1)

    if hands_after > hands_before:
        marginal_hire = total_hire_cost(hands_after, 0) - total_hire_cost(hands_before, 0)
        return float(marginal_hire)

    return 0.0


# ---------------------------------------------------------------------------
# Cull Management
# ---------------------------------------------------------------------------

_CULL_CONSECUTIVE_DAYS: int = 2
_CULL_SPECIES: tuple[str, ...] = ("COW", "SHEEP", "GOOSE")


def update_cull_state(
    day: int,
    drift: dict[str, float],
    market_inv: dict[str, int],
    census: AnimalCensus,
    state: CullState,
) -> dict[str, int]:
    if day == state.last_day:
        return dict(state.retained_caps)
    state.last_day = day

    if day >= c.LIQUIDATION_DAY:
        for species in _CULL_SPECIES:
            state.retained_caps[species] = 0
        return dict(state.retained_caps)

    counts = {
        "COW": census.total_cows,
        "SHEEP": census.total_sheep,
        "GOOSE": census.total_geese,
    }

    for species in _CULL_SPECIES:
        spec = c.ANIMALS[species]
        item = spec["product"]
        lag = spec["first_yield_day"]
        rate = 1.0 / float(spec["interval"])
        projected = max(1, market_inv.get(item, c.I0) - int(drift.get(item, 0.0) * lag))
        fert_price = float(get_price("FERTILIZER", market_inv))
        revenue_day = (market_price(item, projected) * rate) + fert_price
        cost_day = float(get_price("WHEAT", market_inv)) + c.HAND_COST_PER_ANIMAL_DAY
        profit = revenue_day - cost_day

        if species in state.downsized:
            if species not in state.retained_caps:
                state.retained_caps[species] = max(1, math.ceil(counts[species] * 0.5))
            continue

        if counts[species] <= 0:
            state.negative_days[species] = 0
            state.retained_caps[species] = 999
            continue

        if profit < 0.0:
            state.negative_days[species] = state.negative_days.get(species, 0) + 1
            if state.negative_days[species] >= _CULL_CONSECUTIVE_DAYS:
                state.retained_caps[species] = max(1, math.ceil(counts[species] * 0.5))
                state.downsized.add(species)
                state.negative_days[species] = 0
            else:
                state.retained_caps[species] = 999
        else:
            state.negative_days[species] = 0
            state.retained_caps[species] = 999

    return dict(state.retained_caps)


# ---------------------------------------------------------------------------
# Market Trading Logic (Sells, Purchases, Reserves)
# ---------------------------------------------------------------------------

_THROTTLED_SELL_ITEMS: frozenset[str] = frozenset(("MELON", "WOOL", "STRAWBERRY", "WHEAT"))
_SELL_PRICE_DROP_LIMIT: float = 0.15


def _throttled_qty(item: str, qty: int, market_inv: dict[str, int], day: int) -> int:
    if day >= c.LIQUIDATION_DAY:
        return qty
    if item not in _THROTTLED_SELL_ITEMS:
        return qty
    p_now = get_price(item, market_inv)
    if p_now <= 1:
        return qty
    inv_now = market_inv.get(item, c.I0)
    lo, hi, best = 1, qty, 1
    while lo <= hi:
        mid = (lo + hi) // 2
        p_after = get_price(item, {**market_inv, item: inv_now + mid})
        if (p_now - p_after) / p_now <= _SELL_PRICE_DROP_LIMIT:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def _plan_sells(
    day: int,
    hour: int,
    shed: dict[str, int],
    farm_state: dict[str, Any],
    market_inv: dict[str, int],
    inventories: list[dict[str, int]],
    census: AnimalCensus,
    retained_caps: dict[str, int] | None = None,
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    revenue: float = 0.0

    carried_sells: dict[str, int] = defaultdict(int)
    if day >= 29 and hour >= 15:
        for inv in inventories:
            for item, q in inv.items():
                if q > 0 and item not in ("COW", "SHEEP", "GOOSE"):
                    carried_sells[item] += q

    fert_due_count = count_fertilize_due(farm_state)
    fert_in_shed = shed.get("FERTILIZER", 0) + carried_sells.get("FERTILIZER", 0)
    fert_capacity = c.N_FERTILIZER_HANDS * c.FERTILIZER_PICKUP_BATCH
    fert_reserve = 0 if day >= c.LIQUIDATION_DAY else min(fert_due_count, fert_capacity)
    fert_to_sell = max(0, fert_in_shed - fert_reserve)
    if fert_to_sell > 0:
        orders.append(["SELL", "FERTILIZER", fert_to_sell])
        revenue += fert_to_sell * get_price("FERTILIZER", market_inv)

    for item in ("MELON", "STRAWBERRY", "MILK", "WOOL", "EGG", "CARROT", "TOMATO"):
        q = shed.get(item, 0) + carried_sells.get(item, 0)
        if q > 0:
            sell_qty = _throttled_qty(item, q, market_inv, day)
            if sell_qty > 0:
                orders.append(["SELL", item, sell_qty])
                revenue += sell_qty * get_price(item, market_inv)

    wheat_in_shed = shed.get("WHEAT", 0) + carried_sells.get("WHEAT", 0)
    _, sell_ceiling = wheat_feed_thresholds(census, retained_caps, day)
    if wheat_in_shed > sell_ceiling and day > 0:
        excess = wheat_in_shed - sell_ceiling
        sell_qty = _throttled_qty("WHEAT", excess, market_inv, day)
        if sell_qty > 0:
            orders.append(["SELL", "WHEAT", sell_qty])
            revenue += sell_qty * get_price("WHEAT", market_inv)

    return orders, revenue


def get_desired_hires(
    day: int,
    catalog: list[Task],
    ready_premium: list[dict[str, Any]],
    base_units: list[tuple[tuple[int, int], dict[str, int]]],
    shed: dict[str, int],
    unlocked_quads_count: int,
) -> int:
    """Workforce (hands) needed today, sized directly off the real task catalog via
    required_hand_count."""
    if day < 0 or day >= c.TOTAL_DAYS:
        raise ValueError(f"Invalid day: {day}")

    max_hands = 11 if unlocked_quads_count < 3 else 12
    desired = required_hand_count(catalog, ready_premium, base_units, shed, max_hands, day)

    return max(0, min(max_hands, desired))


def _plan_seed_buy(
    orders: list[list[Any]], crop: str, want: int, budget: float, cost: float
) -> tuple[float, float, int]:
    if want <= 0:
        return budget, cost, 0
    price = c.CROPS[crop]["seed_cost"]
    bought = min(want, int(budget // price))
    if bought <= 0:
        return budget, cost, 0
    orders.append(["BUY_SEED", crop, bought])
    spend = bought * price
    return budget - spend, cost + spend, bought


# ---------------------------------------------------------------------------
# Main Evaluator Pipeline
# ---------------------------------------------------------------------------

def evaluate_turn(
    obs: dict[str, Any],
    state: EvalState,
) -> TurnDecision:
    """Single entry point for all economic decision making."""
    player = obs["player"]
    day = obs["day"]
    hour = obs["hour"]

    me = obs["farms"][player]
    private = obs["private"]
    market = obs["market"]
    unlocked_shops = obs["town"]["unlocked_shops"]

    money = float(me["money"])
    tiles = me["tiles"]
    unlocked_quads = me["unlocked_quadrants"]
    shed = private["shed"]
    seeds = private["seeds"]
    market_inv = market["inventory"]
    inventories = private["inventories"]
    hires_today = me["hires_today"]

    farmer_pos = (me["farmer"][0], me["farmer"][1])
    all_units: list[tuple[tuple[int, int], dict[str, int]]] = [(farmer_pos, inventories[0])]
    all_units.extend(
        ((h[0], h[1]), inventories[idx + 1]) for idx, h in enumerate(me["hands"])
    )

    # 1. Parsing & Census
    farm_state = parse_farm_state(tiles, day)
    census = count_animal_census(farm_state, shed, inventories)
    needed_pastures = compute_needed_pastures(farm_state, census)

    # 2. Economy & Demand tracking
    demand = compute_daily_demand(unlocked_shops)
    observed = update_drift_tracker(day, market_inv, state.drift)
    drift = effective_drift(demand, observed)
    retained_caps = update_cull_state(day, drift, market_inv, census, state.cull)
    downsized_species = frozenset(state.cull.downsized)

    orders: list[list[Any]] = []
    budget = money

    # Single cash reserve — computed once, used everywhere
    cash_reserve = c.SEED_PURCHASE_CASH_RESERVE if 4 <= day < c.LIQUIDATION_DAY else 0.0

    # Opening Day Rush (Hour 0)
    if day == 0 and hour == 0:
        if shed.get("SHEEP", 0) == 0 and len(farm_state["animals"]) == 0:
            orders.extend([["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"]])
            orders.append(["BUY_ANIMAL", "SHEEP", 2])
            orders.append(["BUY_ANIMAL", "COW", 2])
            orders.append(["BUY_SEED", "MELON", 12])
            orders.append(["BUY_SEED", "WHEAT", 9])
            orders.append(["BUY_PRODUCT", "WHEAT", 4])
            hints = DispatchHints(
                reserved_grazer_slots=4,
                reserved_geese_slots=0,
                crop_limits={"MELON": 12, "WHEAT": 9},
            )
            return TurnDecision(
                market_orders=orders[:c.MAX_MARKET_ORDERS],
                hints=hints,
                retained_caps=retained_caps,
                needed_pastures=needed_pastures,
            )

    # 3. Process Sales (Revenue Injection)
    sell_orders, revenue = _plan_sells(
        day, hour, shed, farm_state, market_inv, inventories, census, retained_caps=retained_caps
    )
    orders.extend(sell_orders)
    budget += revenue

    # 4. Emergency Feed Backup (Wheat purchase if under floor)
    n_kept_feedable = kept_feedable_count(census, retained_caps)
    if n_kept_feedable > 0 and day < c.LIQUIDATION_DAY:
        buy_floor, _ = wheat_feed_thresholds(census, retained_caps, day)
        wheat_avail = shed.get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in inventories)
        if wheat_avail < buy_floor:
            wp = get_price("WHEAT", market_inv)
            can_buy = min(buy_floor - wheat_avail, int(max(0.0, budget - cash_reserve) // max(1, wp)))
            if can_buy > 0:
                orders.append(["BUY_PRODUCT", "WHEAT", can_buy])
                budget -= float(wp * can_buy)

    # 5. Greedy Strategic Target Allocation (Planner core merged)
    acc_cows = census.total_cows
    acc_sheep = census.total_sheep
    acc_geese = census.total_geese
    acc_crops: dict[str, int] = {}

    target_quad_count = len(unlocked_quads)
    planned_pasture_cap = (
        acc_cows + acc_sheep
        if day > c.PASTURE_RESERVATION_LAST_DAY
        else sum(1 for p in c.PASTURE_CLUSTER if quad_of(p) in unlocked_quads)
    )
    planned_coop_cap = target_quad_count * 2
    planned_tile_capacity = target_quad_count * 25

    straw_demand = demand.get("STRAWBERRY", 0.0)
    has_high_straw_demand = straw_demand >= 7.0
    straw_target_base = c.STRAWBERRY_BOOST_TARGET_BUSHES if has_high_straw_demand else c.STRAWBERRY_BASE_TARGET_BUSHES
    if day <= c.STRAWBERRY_LAST_PLANT_DAY:
        acc_crops["STRAWBERRY"] = straw_target_base

    egg_demand = demand.get("EGG", 0.0)
    wool_demand = demand.get("WOOL", 0.0)
    milk_demand = demand.get("MILK", 0.0)

    for _ in range(60):
        candidates: list[CandidateScore] = []
        total_herd = acc_cows + acc_sheep + acc_geese
        total_grazers = acc_cows + acc_sheep

        def add_cand(cand: CandidateScore) -> None:
            ap_cost = estimate_marginal_ap_cost(cand.kind, acc_cows, acc_sheep, acc_geese, acc_crops, day)
            if ap_cost > 0.0:
                days_left = max(1, c.TOTAL_DAYS - day)
                cand = CandidateScore(
                    kind=cand.kind,
                    item=cand.item,
                    cost=cand.cost,
                    daily_profit=cand.daily_profit - ap_cost,
                    npv=cand.npv - (ap_cost * days_left),
                )
            if cand.npv > 0.0 and cand.daily_profit > 0.0:
                candidates.append(cand)

        # Evaluate Animals (Unified NPV & Capacity Checks)
        if total_grazers < planned_pasture_cap and total_herd < c.MAX_TOTAL_HERD:
            if "COW" not in downsized_species:
                cow_cap = retained_caps.get("COW", 999) if retained_caps is not None else 999
                milk_shops_count = sum(1 for s in unlocked_shops if s in c.MILK_SUPPORT_SHOPS)
                max_cows_allowed = 2 if milk_shops_count == 0 else (6 if milk_shops_count == 1 else min(14, 2 + milk_shops_count * 4))

                if acc_cows < cow_cap and acc_cows < max_cows_allowed:
                    add_cand(evaluate_animal("COW", day, total_herd, acc_cows, drift, market_inv, demand))

            if "SHEEP" not in downsized_species:
                sheep_cap = retained_caps.get("SHEEP", 999) if retained_caps is not None else 999
                yarn_shops_count = sum(1 for s in unlocked_shops if s == "YARN_STORE")
                max_sheep_base = 2 if yarn_shops_count == 0 else (4 if yarn_shops_count == 1 else min(8, yarn_shops_count * 4))
                cow_npv_negative = evaluate_animal("COW", day, total_herd, acc_cows, drift, market_inv, demand).npv <= 0.0
                expand_sheep = cow_npv_negative and (yarn_shops_count > 0 or wool_demand >= 6.0)
                max_sheep_allowed = c.MAX_TOTAL_HERD if expand_sheep else max_sheep_base

                if acc_sheep < sheep_cap and acc_sheep < max_sheep_allowed:
                    add_cand(evaluate_animal("SHEEP", day, total_herd, acc_sheep, drift, market_inv, demand))

        egg_shops_count = sum(1 for s in unlocked_shops if s in c.EGG_SUPPORT_SHOPS)
        if egg_shops_count > 0 and acc_geese < planned_coop_cap and total_herd < c.MAX_TOTAL_HERD:
            if "GOOSE" not in downsized_species:
                goose_cap = retained_caps.get("GOOSE", 999) if retained_caps is not None else 999
                if acc_geese < goose_cap and acc_geese < int(egg_demand):
                    add_cand(evaluate_animal("GOOSE", day, total_herd, acc_geese, drift, market_inv, demand))

        # Evaluate Crops
        wheat_tiles_needed = max(15, int((acc_cows + acc_sheep + acc_geese) * 1.0))
        available_crop_tiles = max(0, planned_tile_capacity - planned_pasture_cap - planned_coop_cap - wheat_tiles_needed)

        if day <= c.STRAWBERRY_LAST_PLANT_DAY:
            straw_count = acc_crops.get("STRAWBERRY", 0)
            if straw_count < straw_target_base:
                add_cand(evaluate_fixed_crop(
                    "STRAWBERRY", day, drift, market_inv, demand, current_crop_units=float(straw_count) * 0.46
                ))

        total_secondary_crops = sum(v for k, v in acc_crops.items() if k != "STRAWBERRY")

        if demand.get("TOMATO", 0.0) >= 6.0 and total_secondary_crops < available_crop_tiles:
            tomato_count = acc_crops.get("TOMATO", 0)
            if tomato_count < 8:
                add_cand(evaluate_fixed_crop(
                    "TOMATO", day, drift, market_inv, demand, current_crop_units=float(tomato_count) * 0.5
                ))

        if demand.get("CARROT", 0.0) >= 6.0 and total_secondary_crops < available_crop_tiles:
            carrot_count = acc_crops.get("CARROT", 0)
            if carrot_count < 8:
                add_cand(evaluate_replant_crop(
                    "CARROT", day, drift, market_inv, demand, current_crop_units=float(carrot_count) * 1.17
                ))

        if not candidates:
            break

        best = max(candidates, key=lambda c_cand: c_cand.daily_profit)
        if best.daily_profit <= 0.0:
            break

        if best.kind == "COW":
            acc_cows += 1
        elif best.kind == "SHEEP":
            acc_sheep += 1
        elif best.kind == "GOOSE":
            acc_geese += 1
        else:
            acc_crops[best.kind] = acc_crops.get(best.kind, 0) + 1

    # Land Purchase Target Calculation
    straw_days_left = c.STRAWBERRY_LAST_PLANT_DAY - day
    straw_land_need = planted_count(farm_state, "STRAWBERRY") if straw_days_left <= c.STRAWBERRY_LAND_HORIZON_DAYS else acc_crops.get("STRAWBERRY", 0)
    other_crop_tiles = sum(v for k, v in acc_crops.items() if k != "STRAWBERRY")
    wheat_basis = max(15, int((acc_cows + acc_sheep + acc_geese) * 1.0))
    total_needed_tiles = acc_cows + acc_sheep + acc_geese + other_crop_tiles + straw_land_need + wheat_basis
    current_tile_capacity = len(unlocked_quads) * 25

    target_quads = len(unlocked_quads)
    if len(unlocked_quads) < 3:
        next_cost = 1000.0 if len(unlocked_quads) == 1 else (2000.0 if len(unlocked_quads) == 2 else 4000.0)
        has_land_budget = budget >= next_cost + cash_reserve
        real_empty_tiles = len(farm_state.get("empty_tiles", []))
        # Buy land when current land is actually running out, not when plans
        # aspirationally exceed capacity.  80% utilization = time to expand.
        utilization = 1.0 - (real_empty_tiles / max(1, current_tile_capacity))
        is_capacity_constrained = (
            (total_needed_tiles >= current_tile_capacity and utilization >= 0.8)
            or real_empty_tiles <= 2
            or (acc_cows + acc_sheep) > sum(1 for p in c.PASTURE_CLUSTER if quad_of(p) in unlocked_quads)
            or acc_geese > len(unlocked_quads) * 2
        )
        if has_land_budget and is_capacity_constrained:
            target_quads = len(unlocked_quads) + 1

    # 6. Hiring Decisions (Hour 0 or 1)
    hints = DispatchHints(
        reserved_grazer_slots=acc_cows + acc_sheep,
        reserved_geese_slots=acc_geese,
        crop_limits=dict(acc_crops),
    )
    hints_dict = {
        "reserved_grazer_slots": hints.reserved_grazer_slots,
        "reserved_geese_slots": hints.reserved_geese_slots,
        "crop_limits": hints.crop_limits,
    }

    if hour in (0, 1):
        catalog = build_task_catalog(
            farm_state, shed, dict(seeds), needed_pastures,
            all_units, day, hour, hints=hints_dict, unlocked_quads=unlocked_quads,
            retained_caps=retained_caps,
        )
        ready_premium = _ready_premium_bushes(farm_state, day)
        desired = get_desired_hires(day, catalog, ready_premium, all_units, shed, len(unlocked_quads))
        new_hires = max(0, desired - hires_today)
        hire_orders: list[list[Any]] = []
        while new_hires > 0:
            hcost = total_hire_cost(new_hires, hires_today)
            if budget >= hcost:
                hire_orders.extend([["HIRE"] for _ in range(new_hires)])
                budget -= float(hcost)
                break
            new_hires -= 1
        orders = hire_orders + orders

    res_pasture = live_reserved_pastures(c.PASTURE_CLUSTER, unlocked_quads, hints.reserved_grazer_slots, day=day)
    needed_structs = set(needed_pastures)
    res_coops = live_reserved_coops(
        farm_state, res_pasture | needed_structs, hints.reserved_geese_slots, day=day, unlocked_quads=unlocked_quads
    )

    # 7. Execute Animal Purchases
    total_bought_this_tick = 0
    total_grazers_bought_this_tick = 0
    current_grazers = census.total_cows + census.total_sheep
    current_total = census.total_all

    animal_targets = ((("COW", acc_cows), ("SHEEP", acc_sheep), ("GOOSE", acc_geese)))
    animal_orders: list[list[Any]] = []

    for species, target in animal_targets:
        if species in downsized_species:
            continue
        if species == "GOOSE" and len(unlocked_quads) < 2:
            continue
        cap = retained_caps.get(species, 999) if retained_caps is not None else 999
        have = census.total_geese if species == "GOOSE" else (census.total_sheep if species == "SHEEP" else census.total_cows)
        effective_target = min(target, cap)
        if species == "GOOSE":
            effective_target = min(effective_target, coop_capacity(farm_state) + len(res_coops))
        deficit = effective_target - have
        if deficit <= 0:
            continue

        price = c.ANIMALS[species]["cost"]
        remaining_herd_slots = max(0, c.MAX_TOTAL_HERD - (current_total + total_bought_this_tick))
        max_buyable = min(remaining_herd_slots, max(0, c.MAX_TOTAL_HERD - (current_grazers + total_grazers_bought_this_tick))) if species in ("COW", "SHEEP") else remaining_herd_slots
        want = min(2, deficit, max_buyable, int(max(0.0, budget - cash_reserve) // price))
        if want > 0:
            animal_orders.append(["BUY_ANIMAL", species, want])
            budget -= float(want * price)
            total_bought_this_tick += want
            if species in ("COW", "SHEEP"):
                total_grazers_bought_this_tick += want

    # 8. Execute Land Purchases
    land_orders: list[list[Any]] = []
    want_land = target_quads > len(unlocked_quads)
    if "NE" not in unlocked_quads and want_land and budget >= 1000 + cash_reserve:
        land_orders.append(["BUY_LAND"])
        budget -= 1000.0
    elif "SW" not in unlocked_quads and "NE" in unlocked_quads and want_land and budget >= 2000 + cash_reserve:
        land_orders.append(["BUY_LAND"])
        budget -= 2000.0
    elif "SE" not in unlocked_quads and "SW" in unlocked_quads and target_quads >= 4 and budget >= 4000 + cash_reserve:
        land_orders.append(["BUY_LAND"])
        budget -= 4000.0

    # 9. Execute Seed Purchases
    spendable = max(0.0, budget - cash_reserve)
    seed_cost = 0.0
    empty_count = sum(
        1 for pos in farm_state["empty_tiles"]
        if pos not in res_pasture and pos not in needed_structs and pos not in res_coops
    )
    initial_empty = empty_count

    # Feed Wheat Guarantee
    if 4 <= day <= c.WHEAT_LAST_PLANT_DAY:
        curr_wheat = committed_count(farm_state, seeds, "WHEAT")
        if curr_wheat < census.n_feedable and empty_count > 0:
            spendable, seed_cost, bought = _plan_seed_buy(
                orders, "WHEAT", min(census.n_feedable - curr_wheat, empty_count), spendable, seed_cost
            )
            empty_count = max(0, empty_count - bought)

    # Priority Strawberry Seeds
    straw_target = acc_crops.get("STRAWBERRY", 0)
    total_straw = committed_count(farm_state, seeds, "STRAWBERRY")
    if day <= c.STRAWBERRY_LAST_PLANT_DAY and total_straw < straw_target and empty_count > 0:
        spendable, seed_cost, bought = _plan_seed_buy(
            orders, "STRAWBERRY", min(straw_target - total_straw, empty_count), spendable, seed_cost
        )
        empty_count = max(0, empty_count - bought)

    # Secondary Crop Seeds
    if acc_crops:
        straw_done = committed_count(farm_state, seeds, "STRAWBERRY")
        for crop, target in acc_crops.items():
            if crop == "STRAWBERRY" or crop not in c.CROPS or target <= 0:
                continue
            # Secondary seeds gate: buy when strawberry target is covered OR when
            # secondary crop has higher NPV than remaining strawberry gap.
            if straw_done < straw_target:
                straw_npv = evaluate_fixed_crop(
                    "STRAWBERRY", day, drift, market_inv, demand,
                    current_crop_units=float(straw_done) * 0.46,
                ).npv
                crop_npv = (
                    evaluate_fixed_crop(crop, day, drift, market_inv, demand).npv
                    if c.CROPS[crop].get("is_ongoing") else
                    evaluate_replant_crop(crop, day, drift, market_inv, demand).npv
                )
                if straw_npv > crop_npv:
                    continue
            spec = c.CROPS[crop]
            lag = spec["first_yield_day"] if spec["is_ongoing"] else spec["max_yield_day"]
            if day > c.TOTAL_DAYS - lag - 1:
                continue
            curr = committed_count(farm_state, seeds, crop)
            if curr < target:
                spendable, seed_cost, bought = _plan_seed_buy(orders, crop, target - curr, spendable, seed_cost)
                empty_count = max(0, empty_count - bought)

    # Continuous Wheat Flow
    if 4 <= day <= c.WHEAT_LAST_PLANT_DAY:
        if day < c.WHEAT_LAST_PLANT_DAY or (day == c.WHEAT_LAST_PLANT_DAY and hour < 12):
            wheat_buffer = 0 if len(unlocked_quads) < 2 else 15
            want_wheat = max(0, initial_empty + wheat_buffer - seeds.get("WHEAT", 0))
            spendable, seed_cost, _ = _plan_seed_buy(orders, "WHEAT", want_wheat, spendable, seed_cost)
    elif 1 <= day <= 3:
        want_wheat = max(0, initial_empty - seeds.get("WHEAT", 0))
        spendable, seed_cost, _ = _plan_seed_buy(orders, "WHEAT", want_wheat, spendable, seed_cost)

    budget -= seed_cost

    orders.extend(land_orders)
    orders.extend(animal_orders)

    return TurnDecision(
        market_orders=orders[:c.MAX_MARKET_ORDERS],
        hints=hints,
        retained_caps=retained_caps,
        needed_pastures=needed_pastures,
    )


# ---------------------------------------------------------------------------
# MODULE: main.py
# ---------------------------------------------------------------------------

"""Kaggle Agent Entry Point — EcoBot v7 Unified Evaluator."""





@dataclass(slots=True)
class AgentMemory:
    eval_state: EvalState = field(default_factory=EvalState)
    day_plan: DayPlan | None = None


_MEMORIES: dict[int, AgentMemory] = {}


def agent(obs: dict[str, Any]) -> dict[str, Any]:
    global _MEMORIES
    player = obs["player"]
    if obs.get("step") == 0 or (obs.get("day") == 0 and obs.get("hour") == 0) or player not in _MEMORIES:
        _MEMORIES[player] = AgentMemory()

    mem = _MEMORIES[player]
    day = obs["day"]
    hour = obs["hour"]

    me = obs["farms"][player]
    private = obs["private"]
    inventories = private["inventories"]

    farmer_pos = (me["farmer"][0], me["farmer"][1])
    all_units: list[tuple[tuple[int, int], dict[str, int]]] = [(farmer_pos, inventories[0])]
    all_units.extend(((h[0], h[1]), inventories[idx + 1]) for idx, h in enumerate(me["hands"]))

    # 1. Unified evaluator — single call produces market orders + dispatch hints
    decision = evaluate_turn(obs, mem.eval_state)

    # 2. Units & Field Actions
    if hour == 0:
        actions = [["PASS"] for _ in all_units]
    else:
        if mem.day_plan is None or mem.day_plan.day != day:
            farm_state = parse_farm_state(me["tiles"], day)
            pending_hires = max(0, me["hires_today"] - len(me["hands"])) + sum(
                1 for o in decision.market_orders if o[0] == "HIRE"
            )
            hints_dict = {
                "reserved_grazer_slots": decision.hints.reserved_grazer_slots,
                "reserved_geese_slots": decision.hints.reserved_geese_slots,
                "crop_limits": decision.hints.crop_limits,
            }
            mem.day_plan = build_day_plan(
                all_units, farm_state, private["shed"], private["seeds"],
                day, hour, decision.needed_pastures,
                hints=hints_dict,
                unlocked_quads=me["unlocked_quadrants"],
                retained_caps=decision.retained_caps,
                pending_hires=pending_hires,
            )
        actions = [
            next_action(ui, day, mem.day_plan)
            for ui in range(len(all_units))
        ]

    return {
        "farmer": actions[0],
        "hands": actions[1:],
        "market": decision.market_orders,
    }
