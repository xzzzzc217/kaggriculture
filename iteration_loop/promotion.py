"""Pure upload gate for one closed-loop cycle.

No engine I/O and no Kaggle calls. A cycle is upload-eligible only when its
own games show both-seat wins against a public opponent in the gold score
band and intact clone, fertilizer/wheat, and low-fertilizer screens.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

GOLD_SCORE_MIN = 2700.0
GOLD_SCORE_MAX = 3100.0
REQUIRED_SCREENS = ("clone", "fertilizer_wheat", "low_fertilizer")
NON_PROMOTING_OPPONENTS = frozenset({"mirror", "pass", "starter", "local_champion"})

_GOLD_REASONS = (
    "gold_band_not_public_opponent",
    "gold_band_score_outside",
    "gold_band_not_both_seat_wins",
)


def decide(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return the accept/reject decision for one cycle record.

    Pre-baked ``decision`` / ``upload_eligible`` fields are ignored. The
    result is computed only from ``games``.
    """
    games = [game for game in (record.get("games") or []) if isinstance(game, Mapping)]
    reasons: list[str] = []
    reasons.extend(_gold_reasons(games))
    reasons.extend(_screen_reasons(games))
    reasons.extend(_opponent_class_reasons(games))
    eligible = not reasons
    return {
        "decision": "accept" if eligible else "reject",
        "upload_eligible": eligible,
        "reasons": reasons,
    }


def _numeric(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def _in_gold_band(score: object) -> bool:
    return _numeric(score) and GOLD_SCORE_MIN <= float(score) <= GOLD_SCORE_MAX


def _winning_game(game: Mapping[str, Any]) -> bool:
    statuses = list(game.get("statuses") or [])
    rewards = game.get("rewards")
    seat = game.get("seat")
    if statuses != ["DONE", "DONE"]:
        return False
    if not isinstance(rewards, list) or len(rewards) != 2:
        return False
    if not all(_numeric(item) for item in rewards):
        return False
    if seat not in (0, 1):
        return False
    if not _numeric(game.get("own_reward")) or not _numeric(game.get("opponent_reward")):
        return False
    own = float(game["own_reward"])
    opponent = float(game["opponent_reward"])
    seat_index = int(seat)
    if float(rewards[seat_index]) != own or float(rewards[1 - seat_index]) != opponent:
        return False
    return bool(game.get("win") is True and own > opponent)


def _both_seats_won(group: list[Mapping[str, Any]]) -> bool:
    if not group or not all(_winning_game(game) for game in group):
        return False
    return {game.get("seat") for game in group} >= {0, 1}


def _gold_reasons(games: list[Mapping[str, Any]]) -> list[str]:
    gold = [game for game in games if game.get("screen") == "gold_band"]
    if not gold:
        return ["no_gold_band_games"]
    found: list[str] = []
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for game in gold:
        key = str(game.get("opponent_id") or game.get("opponent") or "opponent")
        groups.setdefault(key, []).append(game)
    for group in groups.values():
        classes = {str(game.get("opponent_class") or "") for game in group}
        if classes != {"public_gold"}:
            found.append("gold_band_not_public_opponent")
            continue
        if any(not _in_gold_band(game.get("opponent_public_score")) for game in group):
            found.append("gold_band_score_outside")
            continue
        if not _both_seats_won(group):
            found.append("gold_band_not_both_seat_wins")
    return [reason for reason in _GOLD_REASONS if reason in found]


def _screen_reasons(games: list[Mapping[str, Any]]) -> list[str]:
    reasons: list[str] = []
    for screen in REQUIRED_SCREENS:
        group = [game for game in games if game.get("screen") == screen]
        if not group:
            reasons.append(f"missing_screen_{screen}")
        elif not _both_seats_won(group):
            reasons.append(f"collapsed_screen_{screen}")
    return reasons


def _opponent_class_reasons(games: list[Mapping[str, Any]]) -> list[str]:
    wins = [game for game in games if game.get("win") is True]
    if not wins:
        return ["no_wins"]
    if all(str(game.get("opponent_class") or "") in NON_PROMOTING_OPPONENTS for game in wins):
        return ["wins_only_against_non_promoting_opponents"]
    return []
