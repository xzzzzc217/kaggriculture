"""Batch G5 recorded-seat replay-callback screen. Does not touch root main.py."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

H2_SUBIN = -7107
H2_JAMES = -8551

STREAMS = {
    "subin": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json",
        "seat": 0,
        "h2_margin": H2_SUBIN,
    },
    "james": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55658542/episodes/95677563.json",
        "seat": 0,
        "h2_margin": H2_JAMES,
    },
}

AGENTS = [
    "tuannm3812_htdc_v12",
    "stevenleehans_e284",
    "stevenleehans_x544",
    "prvsiyan_moon_rerun",
    "flexonafft_rerun",
    "amey_premium_first_rerun",
    "v22r2_second_yarn_6c8",
    "v22r2_second_yarn_hold",
    "maverickss26_v1",
    "nekkon_replay_agent",
]


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    summary = {
        "date": "2026-08-23",
        "h2_g5_controls": {"subin_an_97399969": H2_SUBIN, "james_y_95677563": H2_JAMES},
        "screens": [],
    }
    started = time.perf_counter()
    for name in AGENTS:
        agent = out_dir / name / "main.py"
        row = {"agent": name, "path": str(agent), "exists": agent.exists()}
        if not agent.exists():
            summary["screens"].append(row)
            print(json.dumps(row), flush=True)
            continue
        for key, spec in STREAMS.items():
            try:
                report = play(agent, spec["replay"], spec["seat"], 720)
                margin = report["margin"]
                rec = {
                    "margin": margin,
                    "scores": [report["own_reward"], report["opponent_reward"]],
                    "win": bool(report["win"]),
                    "beats_h2": margin > spec["h2_margin"],
                    "statuses": report["statuses"],
                    "runtime_seconds": report["runtime_seconds"],
                }
            except Exception as exc:  # noqa: BLE001
                rec = {"error": f"{type(exc).__name__}: {exc}"}
            row[f"g5_{key}"] = rec
            print(f"{name} {key} {rec}", flush=True)
        subin = row.get("g5_subin", {})
        james = row.get("g5_james", {})
        row["pass_g5_both"] = bool(subin.get("win") and james.get("win"))
        row["beats_h2_both"] = bool(subin.get("beats_h2") and james.get("beats_h2"))
        summary["screens"].append(row)
    summary["elapsed_seconds"] = time.perf_counter() - started
    summary["moon_g5_survivor"] = [
        s["agent"] for s in summary["screens"] if s.get("pass_g5_both")
    ]
    dest = out_dir / "g5_hunt_20260823.json"
    dest.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)
    print(json.dumps({"survivors": summary["moon_g5_survivor"], "elapsed": summary["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
