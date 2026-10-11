"""Recorded-seat probe: s4 route 3 when behind with milk still priced."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/yusuke_sixday/probe_cut13_main.py"
GAMES = [
    {
        "name": "Deskbo",
        "replay": ROOT / "artifacts/kaggle_runs/sixday_20260907/episode-105744091-replay.json",
        "seat": 1,
        "live_margin": -15628,
    },
    {
        "name": "Stefano",
        "replay": ROOT / "artifacts/kaggle_runs/sixday_20260908/episode-105798735-replay.json",
        "seat": 0,
        "live_margin": -21909,
    },
    {
        "name": "fufu",
        "replay": ROOT / "artifacts/kaggle_runs/sixday_20260908/episode-105790145-replay.json",
        "seat": 0,
        "live_margin": -11025,
    },
]


def main() -> None:
    rows = []
    for spec in GAMES:
        report = play(AGENT, spec["replay"], spec["seat"], 720)
        rec = {
            "name": spec["name"],
            "margin": report["margin"],
            "live": spec["live_margin"],
            "delta": report["margin"] - spec["live_margin"],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
        }
        rows.append(rec)
        print(rec, flush=True)
    out = ROOT / "experiments/20260908_cut13_probe.json"
    out.write_text(json.dumps({"rows": rows}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    main()
