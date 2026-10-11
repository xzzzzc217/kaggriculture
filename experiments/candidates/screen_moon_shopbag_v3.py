"""Recorded-seat screen for moon_shopbag_v3. No upload."""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/moon_shopbag_v3/main.py"
LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
CLONE = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"
OUT = ROOT / "experiments/candidates/moon_shopbag_v3/screen.json"

STREAMS = {
    "prvsiyan_clone": {
        "replay": CLONE / "episode-100348898-replay.json",
        "seat": 1,
        "shopbag": 5964,
    },
    "fufu_clone": {
        "replay": CLONE / "episode-100504057-replay.json",
        "seat": 0,
        "shopbag": 6937,
    },
    "masa_clone": {
        "replay": CLONE / "episode-100444645-replay.json",
        "seat": 0,
        "shopbag": 7511,
    },
    "mtn_11sheep": {
        "replay": LIVE / "episode-102571934-replay.json",
        "seat": 1,
        "shopbag": -17420,
    },
    "yusuke_11sheep": {
        "replay": LIVE / "episode-102538447-replay.json",
        "seat": 1,
        "shopbag": -13434,
    },
    "hanserong_11sheep": {
        "replay": LIVE / "episode-102007365-replay.json",
        "seat": 1,
        "shopbag": -14707,
    },
    "hanserong_clone_L": {
        "replay": LIVE / "episode-103118692-replay.json",
        "seat": 1,
        "shopbag": -11247,
    },
    "lynxx_win": {
        "replay": LIVE / "episode-103051723-replay.json",
        "seat": 1,
        "shopbag": 9240,
    },
}


def main() -> None:
    py_compile.compile(str(AGENT), doraise=True)
    rows = {}
    wins = 0
    for key, spec in STREAMS.items():
        if not spec["replay"].exists():
            print("MISSING", spec["replay"], flush=True)
            continue
        report = play(AGENT, spec["replay"], spec["seat"], 720)
        rec = {
            "margin": report["margin"],
            "shopbag": spec["shopbag"],
            "delta": report["margin"] - spec["shopbag"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
            "runtime": round(report["runtime_seconds"], 2),
        }
        wins += int(rec["win"])
        rows[key] = rec
        print(key, rec, flush=True)
    payload = {"agent": "moon_shopbag_v3", "wins": wins, "n": len(rows), "rows": rows}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, "wins", wins, "/", len(rows))


if __name__ == "__main__":
    main()
