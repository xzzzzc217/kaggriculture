"""Evaluate a file agent against recorded public strong-field action streams."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import pandas as pd
from kaggle_environments import make


def wilson_lower_bound(wins: int, games: int, z: float = 1.96) -> float:
    if games <= 0:
        return 0.0
    rate = wins / games
    denominator = 1 + z * z / games
    centre = rate + z * z / (2 * games)
    radius = z * math.sqrt(rate * (1 - rate) / games + z * z / (4 * games * games))
    return (centre - radius) / denominator


def select_rows(frame: pd.DataFrame, max_rows: int, offset: int) -> pd.DataFrame:
    ordered = frame.sort_values(
        ["opponent_rating", "episode_id"], ascending=[False, True]
    ).drop_duplicates("opponent_behaviour")
    return ordered.iloc[offset : offset + max_rows].copy()


def play(agent_path: str, row: object, steps: int) -> dict:
    actions = json.loads(row.opponent_actions)

    def replay_agent(observation: object, configuration: object = None) -> dict:
        del configuration
        if isinstance(observation, dict):
            step = int(observation.get("step", 0) or 0)
        else:
            step = int(getattr(observation, "step", 0) or 0)
        return actions[min(max(0, step), len(actions) - 1)]

    seat = int(row.your_seat)
    players = [agent_path, replay_agent] if seat == 0 else [replay_agent, agent_path]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": steps, "seed": int(row.seed)},
        debug=False,
    )
    started = time.perf_counter()
    env.run(players)
    runtime = time.perf_counter() - started
    final = env.steps[-1]
    statuses = [str(state.status) for state in final]
    if statuses != ["DONE", "DONE"]:
        raise RuntimeError(
            f"episode {row.episode_id} failed for seat {seat}: {statuses}"
        )
    rewards = [float(state.reward) for state in final]
    own_reward = rewards[seat]
    opponent_reward = rewards[1 - seat]
    return {
        "episode_id": int(row.episode_id),
        "seed": int(row.seed),
        "seat": seat,
        "opponent_team": str(row.opponent_team),
        "opponent_rating": float(row.opponent_rating),
        "opponent_behaviour": str(row.opponent_behaviour),
        "own_reward": own_reward,
        "opponent_reward": opponent_reward,
        "margin": own_reward - opponent_reward,
        "win": own_reward > opponent_reward,
        "tie": own_reward == opponent_reward,
        "recorded_bank_yours": float(row.recorded_bank_yours),
        "recorded_bank_opponent": float(row.recorded_bank_opponent),
        "recorded_seat_improvement": own_reward - float(row.recorded_bank_yours),
        "runtime_seconds": runtime,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", type=Path)
    parser.add_argument(
        "--agent",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "main.py",
    )
    parser.add_argument("--max-rows", type=int, default=12)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    frame = pd.read_parquet(args.benchmark)
    selected = select_rows(frame, args.max_rows, args.offset)
    agent_path = str(args.agent.resolve())
    results = [play(agent_path, row, args.steps) for row in selected.itertuples()]
    wins = sum(result["win"] for result in results)
    summary = {
        "agent": agent_path,
        "benchmark": str(args.benchmark.resolve()),
        "selection": "highest-rating row per 24-turn behaviour",
        "offset": args.offset,
        "games": len(results),
        "distinct_behaviours": len({result["opponent_behaviour"] for result in results}),
        "wins": wins,
        "ties": sum(result["tie"] for result in results),
        "win_rate": wins / len(results),
        "wilson_95_lower": wilson_lower_bound(wins, len(results)),
        "mean_margin": sum(result["margin"] for result in results) / len(results),
        "worst_margin": min(result["margin"] for result in results),
        "mean_recorded_seat_improvement": sum(
            result["recorded_seat_improvement"] for result in results
        )
        / len(results),
        "mean_opponent_rating": sum(result["opponent_rating"] for result in results)
        / len(results),
        "mean_runtime_seconds": sum(result["runtime_seconds"] for result in results)
        / len(results),
        "results": results,
    }
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
