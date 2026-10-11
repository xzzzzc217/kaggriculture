"""Recorded-seat screen: Yusuke two-shop demo vs 11-sheep class. No upload."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/yusuke_shopforge_demo/main.py"
LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
CLONE = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"
OUT = ROOT / "experiments/candidates/yusuke_shopforge_demo/screen_11sheep.json"

STREAMS = {
    "mtn_102571934": {
        "replay": LIVE / "episode-102571934-replay.json",
        "seat": 1,
        "shopbag_margin": -17420,
        "e776_margin": -14407,
    },
    "yusuke_102538447": {
        "replay": LIVE / "episode-102538447-replay.json",
        "seat": 1,
        "shopbag_margin": -13434,
        "e776_margin": -10750,
    },
    "hanserong_102007365": {
        "replay": LIVE / "episode-102007365-replay.json",
        "seat": 1,
        "shopbag_margin": -14707,
        "e776_margin": -13138,
    },
    "pavlo_102911051": {
        "replay": LIVE / "episode-102911051-replay.json",
        "seat": 1,
        "shopbag_margin": -8317,
        "e776_margin": 86,
    },
    "prvsiyan_clone_100348898": {
        "replay": CLONE / "episode-100348898-replay.json",
        "seat": 1,
        "shopbag_margin": 5964,
        "e776_margin": 9253,
    },
}


def main() -> None:
    rows = {}
    flips = 0
    for key, spec in STREAMS.items():
        if not spec["replay"].exists():
            print("MISSING", spec["replay"], flush=True)
            continue
        report = play(AGENT, spec["replay"], spec["seat"], 720)
        rec = {
            "margin": report["margin"],
            "shopbag_margin": spec["shopbag_margin"],
            "e776_margin": spec["e776_margin"],
            "delta_vs_shopbag": report["margin"] - spec["shopbag_margin"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
            "runtime": report["runtime_seconds"],
        }
        flips += int(rec["win"])
        rows[key] = rec
        print(key, rec, flush=True)
    payload = {
        "agent": "yusuke_shopforge_demo",
        "wins": flips,
        "n": len(rows),
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, "wins", flips, "/", len(rows))


if __name__ == "__main__":
    main()
