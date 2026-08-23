"""Run a small deterministic two-seat local league for the current agent."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

from kaggle_environments import make

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import agent  # noqa: E402


def play(seed: int, opponent: str, seat: int, steps: int) -> dict:
    players = [agent, opponent] if seat == 0 else [opponent, agent]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": steps, "seed": seed},
        debug=True,
    )
    started = time.perf_counter()
    env.run(players)
    runtime_seconds = time.perf_counter() - started
    final = env.steps[-1]
    statuses = [state.status for state in final]
    if statuses != ["DONE", "DONE"]:
        raise RuntimeError(f"episode failed: seed={seed}, opponent={opponent}, {statuses=}")

    rewards = [float(state.reward) for state in final]
    own_reward = rewards[seat]
    opponent_reward = rewards[1 - seat]
    return {
        "seed": seed,
        "opponent": opponent,
        "seat": seat,
        "steps": len(env.steps),
        "own_reward": own_reward,
        "opponent_reward": opponent_reward,
        "margin": own_reward - opponent_reward,
        "win": own_reward > opponent_reward,
        "tie": own_reward == opponent_reward,
        "runtime_seconds": runtime_seconds,
    }


def wilson_lower_bound(wins: int, games: int, z: float = 1.96) -> float:
    if games <= 0:
        return 0.0
    rate = wins / games
    denominator = 1 + z * z / games
    centre = rate + z * z / (2 * games)
    radius = z * math.sqrt(rate * (1 - rate) / games + z * z / (4 * games * games))
    return (centre - radius) / denominator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=96)
    parser.add_argument("--seeds", type=int, nargs="+", default=[20260821, 20260822])
    args = parser.parse_args()

    games = [
        play(seed, opponent, seat, args.steps)
        for seed in args.seeds
        for opponent in ("pass", "random", "starter")
        for seat in (0, 1)
    ]
    summary = {
        "games": len(games),
        "wins": sum(game["win"] for game in games),
        "ties": sum(game["tie"] for game in games),
        "win_rate": sum(game["win"] for game in games) / len(games),
        "wilson_95_lower": wilson_lower_bound(sum(game["win"] for game in games), len(games)),
        "mean_margin": sum(game["margin"] for game in games) / len(games),
        "worst_margin": min(game["margin"] for game in games),
        "mean_runtime_seconds": sum(game["runtime_seconds"] for game in games) / len(games),
        "seat_win_rate": {
            str(seat): sum(game["win"] for game in games if game["seat"] == seat)
            / sum(game["seat"] == seat for game in games)
            for seat in (0, 1)
        },
        "results": games,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
