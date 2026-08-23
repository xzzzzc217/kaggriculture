"""Summarize a downloaded Kaggriculture replay and optional agent log."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SIGNATURE_KEYS = tuple(
    sorted(
        (
            "WHEAT",
            "CARROT",
            "TOMATO",
            "STRAWBERRY",
            "MELON",
            "COW",
            "SHEEP",
            "GOOSE",
            "PASTURE",
            "COOP",
            "WEED",
        )
    )
)


def public_signature(farm: dict[str, Any]) -> tuple[int, int, tuple[int, ...]]:
    counts = dict.fromkeys(SIGNATURE_KEYS, 0)
    for row in farm.get("tiles", []) or []:
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            for field in ("crop", "animal", "kind"):
                value = str(tile.get(field, "")).upper()
                if value in counts:
                    counts[value] += 1
                    break
    return (
        len(farm.get("hands", []) or []),
        len(farm.get("unlocked_quadrants", []) or []),
        tuple(counts[key] for key in SIGNATURE_KEYS),
    )


def clone_distance(farms: list[dict[str, Any]]) -> float:
    if len(farms) < 2:
        return math.inf
    left = public_signature(farms[0])
    right = public_signature(farms[1])
    return (
        abs(left[0] - right[0])
        + 3 * abs(left[1] - right[1])
        + sum(abs(a - b) for a, b in zip(left[2], right[2], strict=True))
    )


def flatten_logs(payload: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not isinstance(payload, list):
        return rows
    for step in payload:
        if isinstance(step, list):
            rows.extend(row for row in step if isinstance(row, dict))
        elif isinstance(step, dict):
            rows.append(step)
    return rows


def summarize(replay: dict[str, Any], player: int, log_payload: Any | None) -> dict[str, Any]:
    steps = replay["steps"]
    opponents = 1 - player
    market_counts = [Counter(), Counter()]
    market_quantities = [defaultdict(int), defaultdict(int)]
    action_counts = [Counter(), Counter()]
    money_checkpoints: list[dict[str, Any]] = []
    distances: list[float] = []
    near_streak = 0
    maximum_near_streak = 0
    latch_step: int | None = None

    for step_index, states in enumerate(steps):
        observation = states[player].get("observation") or {}
        farms = observation.get("farms") or []
        distance = clone_distance(farms)
        distances.append(distance)
        if distance <= 2.0:
            near_streak += 1
        else:
            near_streak = 0
        maximum_near_streak = max(maximum_near_streak, near_streak)
        if latch_step is None and step_index >= 48 and near_streak >= 24:
            latch_step = step_index

        if step_index % 24 == 23 or step_index == len(steps) - 1:
            money_checkpoints.append(
                {
                    "step": step_index,
                    "day": step_index // 24 + 1,
                    "player_money": float(farms[player].get("money", 0.0)),
                    "opponent_money": float(farms[opponents].get("money", 0.0)),
                }
            )

        for seat, state in enumerate(states):
            action = state.get("action") or {}
            farmer = action.get("farmer") or ["PASS"]
            action_counts[seat][f"farmer:{farmer[0]}"] += 1
            for hand in action.get("hands") or []:
                if hand:
                    action_counts[seat][f"hand:{hand[0]}"] += 1
            for order in action.get("market") or []:
                if not order:
                    continue
                operation = str(order[0])
                item = str(order[1]) if len(order) > 1 else ""
                quantity = int(order[2]) if len(order) > 2 else 1
                market_counts[seat][f"{operation}:{item}"] += 1
                market_quantities[seat][f"{operation}:{item}"] += quantity

    final_states = steps[-1]
    final_observation = final_states[player]["observation"]
    final_farms = final_observation["farms"]
    final_private = final_observation.get("private") or {}
    final_rewards = [float(state.get("reward", 0.0)) for state in final_states]

    logs = flatten_logs(log_payload)
    durations = [float(row.get("duration", 0.0) or 0.0) for row in logs]
    nonempty_stderr = [str(row.get("stderr")) for row in logs if row.get("stderr")]
    nonempty_stdout = [str(row.get("stdout")) for row in logs if row.get("stdout")]

    return {
        "episode_id": int(replay.get("info", {}).get("EpisodeId", replay.get("id", 0))),
        "seed": int(replay.get("info", {}).get("seed", 0)),
        "player": player,
        "teams": replay.get("info", {}).get("TeamNames", []),
        "steps": len(steps),
        "statuses": [str(state.get("status")) for state in final_states],
        "rewards": final_rewards,
        "margin": final_rewards[player] - final_rewards[opponents],
        "clone_gate": {
            "threshold": 2.0,
            "streak_required": 24,
            "maximum_near_streak": maximum_near_streak,
            "latched": latch_step is not None,
            "latch_step": latch_step,
            "minimum_distance": min(distances),
            "median_distance": sorted(distances)[len(distances) // 2],
            "final_distance": distances[-1],
        },
        "money_checkpoints": money_checkpoints,
        "final_public_signatures": [
            {
                "hands": signature[0],
                "unlocked_quadrants": signature[1],
                "objects": dict(zip(SIGNATURE_KEYS, signature[2], strict=True)),
            }
            for signature in map(public_signature, final_farms)
        ],
        "player_final_private": {
            "shed": final_private.get("shed", {}),
            "seeds": final_private.get("seeds", {}),
            "inventories": final_private.get("inventories", []),
        },
        "market_order_counts": [dict(counter.most_common()) for counter in market_counts],
        "market_order_quantities": [dict(counter) for counter in market_quantities],
        "field_action_counts": [dict(counter.most_common()) for counter in action_counts],
        "runtime": {
            "records": len(logs),
            "mean_seconds": sum(durations) / len(durations) if durations else None,
            "max_seconds": max(durations) if durations else None,
            "stderr_records": len(nonempty_stderr),
            "stdout_records": len(nonempty_stdout),
            "stderr_samples": nonempty_stderr[:5],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("replay", type=Path)
    parser.add_argument("--player", type=int, choices=(0, 1), required=True)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    replay = json.loads(args.replay.read_text(encoding="utf-8"))
    log_payload = json.loads(args.log.read_text(encoding="utf-8")) if args.log else None
    report = summarize(replay, args.player, log_payload)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
