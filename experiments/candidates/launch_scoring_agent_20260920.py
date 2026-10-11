"""Official-engine 720-turn launches of the shipped scoring Agent. Not a test double."""

from __future__ import annotations

import json
import math
from pathlib import Path

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[2]
SHIPPED = ROOT / "artifacts/submission/thomastschinkel_metav4_v13/main.py"
SCRATCH = Path(r"C:\Users\21398\AppData\Local\Temp\grok-goal-30badd27e438\implementer")


def launch(seat: int, seed: int) -> dict:
    players = [str(SHIPPED), "pass"] if seat == 0 else ["pass", str(SHIPPED)]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed},
        debug=False,
    )
    env.run(players)
    final = env.steps[-1]
    statuses = [str(state.status) for state in final]
    rewards = [float(state.reward) for state in final]
    rec = {
        "agent": str(SHIPPED),
        "seat": seat,
        "seed": seed,
        "episodeSteps": 720,
        "n_steps": len(env.steps),
        "statuses": statuses,
        "rewards": rewards,
        "own_reward": rewards[seat],
        "finite_own_reward": math.isfinite(rewards[seat]),
        "done_done": statuses == ["DONE", "DONE"],
    }
    if statuses != ["DONE", "DONE"] or not math.isfinite(rewards[seat]):
        raise RuntimeError(rec)
    return rec


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    rec1 = launch(seat=0, seed=20260921)
    (SCRATCH / "launch_1.json").write_text(json.dumps(rec1, indent=2) + "\n", encoding="utf-8")
    print("WROTE launch_1", rec1, flush=True)
    rec2 = launch(seat=1, seed=20260921)
    (SCRATCH / "launch_2.json").write_text(json.dumps(rec2, indent=2) + "\n", encoding="utf-8")
    print("WROTE launch_2", rec2, flush=True)


if __name__ == "__main__":
    main()
