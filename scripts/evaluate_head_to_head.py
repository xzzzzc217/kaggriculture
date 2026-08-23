"""Run deterministic full-season, both-seat matches between two file agents."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

from kaggle_environments import make


def play(candidate: str, opponent: str, seed: int, seat: int, steps: int) -> dict:
    players = [candidate, opponent] if seat == 0 else [opponent, candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": steps, "seed": seed},
        debug=False,
    )
    started = time.perf_counter()
    env.run(players)
    runtime_seconds = time.perf_counter() - started
    final = env.steps[-1]
    statuses = [str(state.status) for state in final]
    if statuses != ["DONE", "DONE"]:
        raise RuntimeError(f"episode failed: seed={seed}, seat={seat}, statuses={statuses}")

    rewards = [float(state.reward) for state in final]
    own_reward = rewards[seat]
    opponent_reward = rewards[1 - seat]
    return {
        "seed": seed,
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
    parser.add_argument("opponent", help="Path to the opponent's root main.py")
    parser.add_argument("--candidate", default=str(Path(__file__).resolve().parents[1] / "main.py"))
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    candidate = str(Path(args.candidate).resolve())
    opponent = str(Path(args.opponent).resolve())
    games = [
        play(candidate, opponent, seed, seat, args.steps)
        for seed in args.seeds
        for seat in (0, 1)
    ]
    wins = sum(game["win"] for game in games)
    pairs = [
        {
            "seed": seed,
            "paired_margin": sum(game["margin"] for game in games if game["seed"] == seed),
        }
        for seed in args.seeds
    ]
    summary = {
        "candidate": candidate,
        "opponent": opponent,
        "games": len(games),
        "wins": wins,
        "ties": sum(game["tie"] for game in games),
        "win_rate": wins / len(games),
        "wilson_95_lower": wilson_lower_bound(wins, len(games)),
        "mean_margin": sum(game["margin"] for game in games) / len(games),
        "worst_margin": min(game["margin"] for game in games),
        "paired_positive": sum(pair["paired_margin"] > 0 for pair in pairs),
        "paired_zero": sum(pair["paired_margin"] == 0 for pair in pairs),
        "paired_negative": sum(pair["paired_margin"] < 0 for pair in pairs),
        "mean_runtime_seconds": sum(game["runtime_seconds"] for game in games) / len(games),
        "pairs": pairs,
        "results": games,
    }
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
