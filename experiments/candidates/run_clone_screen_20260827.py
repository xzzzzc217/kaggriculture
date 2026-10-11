"""Screen new unique agents vs shops' 2026-08-27 clone blowouts. No upload."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"
PUB = ROOT / "artifacts/kaggle_runs/submission_55744278/public12e"

STREAMS = {
    "prvsiyan_100348898": {
        "replay": PUB / "episode-100348898-replay.json",
        "seat": 1,
        "shops_margin": -14190,
    },
    "fufufukakaka_100504057": {
        "replay": PUB / "episode-100504057-replay.json",
        "seat": 0,
        "shops_margin": -13387,
    },
    "masayoshi_100444645": {
        "replay": PUB / "episode-100444645-replay.json",
        "seat": 0,
        "shops_margin": -9937,
    },
}

G5 = {
    "subin_97399969": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json",
        "seat": 0,
        "h2_margin": -7107,
    },
    "james_95677563": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55658542/episodes/95677563.json",
        "seat": 0,
        "h2_margin": -8551,
    },
}

AGENTS = {
    "shops_v43": CAND / "llccqq624_shops" / "main.py",
    "llccqq624_pqs": CAND / "llccqq624_pqs" / "main.py",
    "kaitofukami_v48": CAND / "kaitofukami_v48" / "main.py",
    "shop_guard": CAND / "shop_guard" / "main.py",
    "yamakawanin_v21": CAND / "yamakawanin_v21" / "main.py",
    "evelyn_scheduler_v1": CAND / "evelyn_scheduler_v1" / "main.py",
    "lixiuqixiaoke_v24": CAND / "lixiuqixiaoke_v24" / "main.py",
}


def screen_one(name: str, path: Path, streams: dict) -> dict:
    row = {"agent": name, "path": str(path), "exists": path.exists()}
    if not path.exists():
        return row
    wins = 0
    n = 0
    for key, spec in streams.items():
        try:
            report = play(path, spec["replay"], spec["seat"], 720)
            rec = {
                "margin": report["margin"],
                "scores": [report["own_reward"], report["opponent_reward"]],
                "win": bool(report["win"]),
                "tie": bool(report["tie"]),
                "statuses": report["statuses"],
                "runtime_seconds": round(report["runtime_seconds"], 2),
            }
            n += 1
            wins += int(rec["win"])
        except Exception as exc:  # noqa: BLE001
            rec = {"error": f"{type(exc).__name__}: {exc}"}
        row[key] = rec
        print(f"{name} {key} {rec}", flush=True)
    row["wins"] = wins
    row["n"] = n
    return row


def main() -> None:
    started = time.perf_counter()
    out = {"date": "2026-08-27", "clone": [], "g5": []}
    print("==== CLONE BLOWOUTS ====", flush=True)
    for name, path in AGENTS.items():
        row = screen_one(name, path, STREAMS)
        out["clone"].append(row)
    print("==== G5 ====", flush=True)
    for name, path in AGENTS.items():
        if name == "shops_v43":
            continue
        row = screen_one(name, path, G5)
        out["g5"].append(row)
    out["elapsed_seconds"] = round(time.perf_counter() - started, 1)
    dest = CAND / "clone_screen_20260827.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest, "elapsed", out["elapsed_seconds"], flush=True)


if __name__ == "__main__":
    main()
