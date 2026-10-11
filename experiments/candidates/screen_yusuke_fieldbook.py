"""Recorded-seat screen for Yusuke Fieldbook. No upload."""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/yusuke_fieldbook/main.py"
LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
CLONE = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"
OUT = ROOT / "experiments/candidates/yusuke_fieldbook/screen.json"

STREAMS = {
    "prvsiyan_clone": {"replay": CLONE / "episode-100348898-replay.json", "seat": 1, "base": 5964},
    "fufu_clone": {"replay": CLONE / "episode-100504057-replay.json", "seat": 0, "base": 6937},
    "masa_clone": {"replay": CLONE / "episode-100444645-replay.json", "seat": 0, "base": 7511},
    "loss_3junghun": {"replay": LIVE / "episode-103758970-replay.json", "seat": 0, "base": -5290},
    "loss_satoooh": {"replay": LIVE / "episode-103683078-replay.json", "seat": 0, "base": -3181},
    "loss_plantcity": {"replay": LIVE / "episode-103678738-replay.json", "seat": 0, "base": -4198},
    "loss_fernando": {"replay": LIVE / "episode-103649636-replay.json", "seat": 0, "base": -2605},
    "loss_liquidus": {"replay": LIVE / "episode-103591788-replay.json", "seat": 0, "base": -3662},
    "yarn_tk256": {"replay": LIVE / "episode-103772429-replay.json", "seat": 0, "base": 16611},
    "yarn2_tk256": {"replay": LIVE / "episode-103767960-replay.json", "seat": 0, "base": 17159},
    "hanserong_11": {"replay": LIVE / "episode-102007365-replay.json", "seat": 1, "base": 3879},
    "mtn_11": {"replay": LIVE / "episode-102571934-replay.json", "seat": 1, "base": -759},
    "yusuke_11": {"replay": LIVE / "episode-102538447-replay.json", "seat": 1, "base": -13434},
}


def main() -> None:
    py_compile.compile(str(AGENT), doraise=True)
    rows = {}
    wins = 0
    flips = []
    for key, spec in STREAMS.items():
        if not spec["replay"].exists():
            print("MISSING", spec["replay"], flush=True)
            continue
        report = play(AGENT, spec["replay"], spec["seat"], 720)
        rec = {
            "margin": report["margin"],
            "base": spec["base"],
            "delta": report["margin"] - spec["base"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
            "runtime": round(report["runtime_seconds"], 2),
        }
        wins += int(rec["win"])
        if rec["win"] and spec["base"] <= 0:
            flips.append(key)
        rows[key] = rec
        print(key, rec, flush=True)
    payload = {
        "agent": "yusuke_fieldbook",
        "sha256": "de668f7f72a552640fe0e615fff937990596a47cbe95ba6f6f3992d3fcba3ae8",
        "wins": wins,
        "n": len(rows),
        "flips": flips,
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, "wins", wins, "/", len(rows), "flips", flips)


if __name__ == "__main__":
    main()
