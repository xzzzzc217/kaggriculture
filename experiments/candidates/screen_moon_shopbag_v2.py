"""Recorded-seat checks for wheat front-run wrap. No upload."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "experiments/candidates/moon_shopbag_v1/main.py"
V2 = ROOT / "experiments/candidates/moon_shopbag_v2/main.py"
LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
PUB = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"

STREAMS = {
    "tk256_102114403_loss": {
        "replay": LIVE / "episode-102114403-replay.json",
        "seat": 0,
        "live_margin": -125,
    },
    "collin_101676670_wheat": {
        "replay": LIVE / "episode-101676670-replay.json",
        "seat": 0,
        "live_margin": -13683,
    },
    "hanserong_102007365": {
        "replay": LIVE / "episode-102007365-replay.json",
        "seat": 1,
        "live_margin": -14707,
    },
    "ryo_102083141_win": {
        "replay": LIVE / "episode-102083141-replay.json",
        "seat": 0,
        "live_margin": 15193,
    },
    "prvsiyan_clone": {
        "replay": PUB / "episode-100348898-replay.json",
        "seat": 1,
        "live_margin": 5964,
    },
}


def main() -> None:
    for name, spec in STREAMS.items():
        r1 = play(V1, spec["replay"], spec["seat"], 720)
        r2 = play(V2, spec["replay"], spec["seat"], 720)
        print(
            name,
            "live",
            spec["live_margin"],
            "v1",
            r1["margin"],
            "v2",
            r2["margin"],
            "delta",
            r2["margin"] - r1["margin"],
            "v2_win",
            r2["win"],
            flush=True,
        )


if __name__ == "__main__":
    main()
