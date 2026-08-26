"""G5 + compact smoke for llccqq624_shops. Does not touch root main.py."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/llccqq624_shops/main.py"

G5 = {
    "subin_97399969": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json",
        "seat": 0,
        "h2": -7107,
    },
    "james_95677563": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55658542/episodes/95677563.json",
        "seat": 0,
        "h2": -8551,
    },
}


def main() -> None:
    out = {"agent": str(AGENT), "g5": {}}
    t0 = time.perf_counter()
    for name, spec in G5.items():
        report = play(AGENT, spec["replay"], spec["seat"], 720)
        rec = {
            "margin": report["margin"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "beats_h2": report["margin"] > spec["h2"],
            "statuses": report["statuses"],
            "runtime_seconds": report["runtime_seconds"],
        }
        out["g5"][name] = rec
        print(name, rec, flush=True)
    out["elapsed"] = time.perf_counter() - t0
    dest = Path(__file__).resolve().parent / "shops_g5_20260824.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
