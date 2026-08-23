"""Replay-callback closed loop: file agent vs a recorded opponent stream.

Alignment is the live applied stream:
    actions[t] = replay.steps[t + 1][opponent].action
steps[0] dummy PASS is not used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from kaggle_environments import make


def load_opponent_actions(replay: dict, opponent_seat: int) -> list:
    steps = replay["steps"]
    dummy = {"farmer": ["PASS"], "hands": [], "market": []}
    applied = []
    for t in range(len(steps) - 1):
        applied.append(steps[t + 1][opponent_seat].get("action") or dummy)
    # Env calls the agent 720 times (steps 0..719). Pad with the last live action.
    if applied:
        applied.append(applied[-1])
    return applied


def play(agent_path: Path, replay_path: Path, seat: int, steps: int) -> dict:
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    opponent_seat = 1 - seat
    actions = load_opponent_actions(replay, opponent_seat)
    info = replay.get("info", {})
    seed = int(info.get("seed", 0))
    teams = list(info.get("TeamNames", []))

    def replay_agent(observation, configuration=None):
        del configuration
        if isinstance(observation, dict):
            step = int(observation.get("step", 0) or 0)
        else:
            step = int(getattr(observation, "step", 0) or 0)
        return actions[min(max(0, step), len(actions) - 1)]

    players = [str(agent_path), replay_agent] if seat == 0 else [replay_agent, str(agent_path)]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": steps, "seed": seed},
        debug=False,
    )
    started = time.perf_counter()
    env.run(players)
    runtime = time.perf_counter() - started
    final = env.steps[-1]
    statuses = [str(state.status) for state in final]
    rewards = [float(state.reward) for state in final]
    recorded = [float(state.get("reward", 0.0)) for state in replay["steps"][-1]]
    return {
        "episode_id": int(info.get("EpisodeId", replay.get("id", 0))),
        "replay_path": str(replay_path),
        "agent": str(agent_path),
        "agent_sha256": hashlib.sha256(agent_path.read_bytes()).hexdigest(),
        "seed": seed,
        "seat": seat,
        "our_team": teams[seat] if len(teams) > seat else "",
        "opponent_team": teams[opponent_seat] if len(teams) > opponent_seat else "",
        "teams": teams,
        "n_opponent_actions": len(actions),
        "recorded_rewards": recorded,
        "recorded_margin": recorded[seat] - recorded[opponent_seat],
        "rewards": rewards,
        "own_reward": rewards[seat],
        "opponent_reward": rewards[opponent_seat],
        "margin": rewards[seat] - rewards[opponent_seat],
        "win": rewards[seat] > rewards[opponent_seat],
        "tie": rewards[seat] == rewards[opponent_seat],
        "statuses": statuses,
        "runtime_seconds": runtime,
        "env_steps": len(env.steps),
        "opposite_seat_run": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--seat", type=int, default=0, choices=(0, 1))
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = play(args.agent.resolve(), args.replay.resolve(), args.seat, args.steps)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
