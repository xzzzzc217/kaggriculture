"""Screen new unique hunt agents against frozen low-fert streams. Does not touch main.py."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

STREAMS = {
    "oceanmix_98031955": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55710781/dip/episode-98031955-replay.json",
        "seat": 1,
        "live_margin": -9800,
    },
    "kaileh57_98118767": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55710781/obs2/episode-98118767-replay.json",
        "seat": 0,
        "live_margin": -12982,
    },
    "alessandrozonta_98383311": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55710781/obs4/episode-98383311-replay.json",
        "seat": 1,
        "live_margin": -7389,
    },
}

AGENTS = {
    "h2": ROOT / "main.py",
    "mugundhjb_v21_guarder": ROOT / "experiments/candidates/mugundhjb_v21_guarder/main.py",
    "ecobot_v4": ROOT / "experiments/candidates/ecobot_v4/main.py",
    "llccqq624_counterbook": ROOT / "experiments/candidates/llccqq624_counterbook/main.py",
    "llccqq624_shops": ROOT / "experiments/candidates/llccqq624_shops/main.py",
}


def main() -> None:
    out = {"date": "2026-08-24", "screens": []}
    started = time.perf_counter()
    for name, path in AGENTS.items():
        row = {"agent": name, "path": str(path), "sha_exists": path.exists()}
        if not path.exists():
            out["screens"].append(row)
            print(row, flush=True)
            continue
        for stream_name, spec in STREAMS.items():
            try:
                report = play(path, spec["replay"], spec["seat"], 720)
                rec = {
                    "margin": report["margin"],
                    "scores": [report["own_reward"], report["opponent_reward"]],
                    "win": bool(report["win"]),
                    "tie": bool(report["tie"]),
                    "statuses": report["statuses"],
                    "live_margin": spec["live_margin"],
                    "beats_live_boatlee": report["margin"] > spec["live_margin"],
                    "runtime_seconds": report["runtime_seconds"],
                }
            except Exception as exc:  # noqa: BLE001
                rec = {"error": f"{type(exc).__name__}: {exc}"}
            row[stream_name] = rec
            print(name, stream_name, rec, flush=True)
        wins = [
            bool(row.get(key, {}).get("win"))
            for key in STREAMS
            if isinstance(row.get(key), dict)
        ]
        row["wins"] = sum(wins)
        row["n"] = len(wins)
        out["screens"].append(row)
    out["elapsed"] = time.perf_counter() - started
    dest = Path(__file__).resolve().parent / "lowfert_screen_b_20260824.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
