"""Screen file agents against frozen low-fert live streams. Does not touch main.py."""

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
}

AGENTS = {
    "boatlee_v21": ROOT / "experiments/candidates/boatlee_v21_r1/main.py",
    "h2": ROOT / "main.py",
    "moon_v127": ROOT / "experiments/candidates/prvsiyan_moon_rerun/main.py",
    "top10": ROOT / "experiments/candidates/indarkarhana_top10/main.py",
    "thunder_2948": ROOT / "experiments/candidates/indarkarhana_thunder_2948/main.py",
    "flexonafft": ROOT / "experiments/candidates/flexonafft_rerun/main.py",
}


def main() -> None:
    out = {"date": "2026-08-24", "screens": []}
    t0 = time.perf_counter()
    for aname, apath in AGENTS.items():
        row = {"agent": aname, "path": str(apath), "sha_exists": apath.exists()}
        if not apath.exists():
            out["screens"].append(row)
            print(row, flush=True)
            continue
        for sname, spec in STREAMS.items():
            try:
                report = play(apath, spec["replay"], spec["seat"], 720)
                rec = {
                    "margin": report["margin"],
                    "scores": [report["own_reward"], report["opponent_reward"]],
                    "win": bool(report["win"]),
                    "statuses": report["statuses"],
                    "live_margin": spec["live_margin"],
                    "beats_live_boatlee": report["margin"] > spec["live_margin"],
                }
            except Exception as exc:  # noqa: BLE001
                rec = {"error": f"{type(exc).__name__}: {exc}"}
            row[sname] = rec
            print(aname, sname, rec, flush=True)
        out["screens"].append(row)
    out["elapsed"] = time.perf_counter() - t0
    dest = Path(__file__).resolve().parent / "lowfert_screen_20260824.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
