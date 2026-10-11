"""Recorded-seat clone screen for moon_shopbag_v1. No upload."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/moon_shopbag_v1/main.py"
PUB = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"
OUT = ROOT / "experiments/candidates/moon_shopbag_v1/clone_screen.json"

STREAMS = {
    "prvsiyan_100348898": {
        "replay": PUB / "episode-100348898-replay.json",
        "seat": 1,
        "v189c_margin": 5964,
    },
    "fufufukakaka_100504057": {
        "replay": PUB / "episode-100504057-replay.json",
        "seat": 0,
        "v189c_margin": 6937,
    },
    "masayoshi_100444645": {
        "replay": PUB / "episode-100444645-replay.json",
        "seat": 0,
        "v189c_margin": 7511,
    },
}


def main() -> None:
    rows = {}
    wins = 0
    for key, spec in STREAMS.items():
        report = play(AGENT, spec["replay"], spec["seat"], 720)
        rec = {
            "margin": report["margin"],
            "v189c_margin": spec["v189c_margin"],
            "delta_vs_v189c": report["margin"] - spec["v189c_margin"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
        }
        wins += int(rec["win"])
        rows[key] = rec
        print(key, rec, flush=True)
    payload = {"agent": "moon_shopbag_v1", "clone_wins": wins, "n": len(STREAMS), "rows": rows}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, "clone", wins, "/", len(STREAMS))


if __name__ == "__main__":
    main()
