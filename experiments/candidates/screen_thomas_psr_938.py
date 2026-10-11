"""Recorded-seat clone 3-0 and G5 for Thomas 93.8% later-block router. No upload."""

from __future__ import annotations

import hashlib
import json
import py_compile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/thomastschinkel_psr_938/main.py"
CLONE = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"
OUT = ROOT / "experiments/candidates/thomastschinkel_psr_938/screen.json"

STREAMS = {
    "prvsiyan_clone": {
        "replay": CLONE / "episode-100348898-replay.json",
        "seat": 1,
        "base": 5964,
    },
    "fufu_clone": {
        "replay": CLONE / "episode-100504057-replay.json",
        "seat": 0,
        "base": 6937,
    },
    "masa_clone": {
        "replay": CLONE / "episode-100444645-replay.json",
        "seat": 0,
        "base": 7511,
    },
    "subin_97399969": {
        "replay": ROOT
        / "artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json",
        "seat": 0,
        "base": 17659,
    },
    "james_95677563": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55658542/episodes/95677563.json",
        "seat": 0,
        "base": 51097,
    },
}


def main() -> None:
    py_compile.compile(str(AGENT), doraise=True)
    rows: dict[str, dict] = {}
    missing: list[str] = []
    for key, spec in STREAMS.items():
        replay = spec["replay"]
        if not replay.exists():
            missing.append(str(replay))
            print("MISSING", replay, flush=True)
            continue
        report = play(AGENT, replay, spec["seat"], 720)
        rec = {
            "margin": report["margin"],
            "base": spec["base"],
            "delta": report["margin"] - spec["base"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "tie": bool(report["tie"]),
            "statuses": report["statuses"],
            "runtime": round(report["runtime_seconds"], 2),
            "episode_id": report["episode_id"],
        }
        rows[key] = rec
        print(key, rec, flush=True)
    payload = {
        "agent": "thomastschinkel_psr_938",
        "windows_agent_so": False,
        "agent_path": str(AGENT.as_posix()),
        "main_sha256": hashlib.sha256(AGENT.read_bytes()).hexdigest(),
        "n": len(rows),
        "wins": sum(1 for row in rows.values() if row["win"]),
        "missing": missing,
        "rows": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, "wins", payload["wins"], "/", payload["n"])


if __name__ == "__main__":
    main()
