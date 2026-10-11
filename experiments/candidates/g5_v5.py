"""G5 for moon_shopbag_v5. No upload."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/moon_shopbag_v5/main.py"
STREAMS = {
    "subin_97399969": (
        ROOT / "artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json",
        0,
        17659,
    ),
    "james_95677563": (
        ROOT / "artifacts/kaggle_runs/submission_55658542/episodes/95677563.json",
        0,
        51097,
    ),
}


def main() -> None:
    out = {}
    for key, (path, seat, base) in STREAMS.items():
        report = play(AGENT, path, seat, 720)
        rec = {
            "margin": report["margin"],
            "base": base,
            "delta": report["margin"] - base,
            "win": bool(report["win"]),
            "statuses": report["statuses"],
        }
        out[key] = rec
        print(key, rec, flush=True)
    dest = ROOT / "experiments/candidates/moon_shopbag_v5/g5.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
