"""G5 + lowfert recorded-seat gates for moon_shopbag_v1. No upload."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/moon_shopbag_v1/main.py"
OUT = ROOT / "experiments/candidates/moon_shopbag_v1/gates_g5_lowfert.json"

STREAMS = {
    "subin_97399969": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json",
        "seat": 0,
        "v189c_margin": 3514,
        "group": "g5",
    },
    "james_95677563": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55658542/episodes/95677563.json",
        "seat": 0,
        "v189c_margin": 51097,
        "group": "g5",
    },
    "oceanmix_98031955": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55710781/dip/episode-98031955-replay.json",
        "seat": 1,
        "v189c_margin": 9651,
        "group": "lowfert",
    },
    "kaileh57_98118767": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55710781/obs2/episode-98118767-replay.json",
        "seat": 0,
        "v189c_margin": 3567,
        "group": "lowfert",
    },
    "alessandrozonta_98383311": {
        "replay": ROOT / "artifacts/kaggle_runs/submission_55710781/obs4/episode-98383311-replay.json",
        "seat": 1,
        "v189c_margin": 15650,
        "group": "lowfert",
    },
}


def yarn_profile(replay_path: Path, seat: int) -> dict:
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    steps = replay["steps"]
    first_yarn_step = None
    first_shop_step = None
    shops_final: list[str] = []
    for t, states in enumerate(steps):
        obs = states[seat].get("observation") or {}
        shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
        if shops and first_shop_step is None:
            first_shop_step = t
        if "YARN_STORE" in shops and first_yarn_step is None:
            first_yarn_step = t
        if t == len(steps) - 1:
            shops_final = shops
    first_is_yarn = False
    if first_shop_step is not None:
        obs = steps[first_shop_step][seat].get("observation") or {}
        shops0 = list((obs.get("town") or {}).get("unlocked_shops") or [])
        first_is_yarn = bool(shops0) and shops0[0] == "YARN_STORE"
    return {
        "first_shop_step": first_shop_step,
        "first_yarn_step": first_yarn_step,
        "first_shop_is_yarn": first_is_yarn,
        "yarn_count": int(Counter(shops_final)["YARN_STORE"]),
        "shops_final": shops_final,
        "gate_differs_from_v189c": bool(
            first_yarn_step is not None and not first_is_yarn
        ),
    }


def main() -> None:
    rows = {}
    for key, spec in STREAMS.items():
        path = spec["replay"]
        if not path.exists():
            rows[key] = {"error": f"missing {path}"}
            print(key, "MISSING", path, flush=True)
            continue
        profile = yarn_profile(path, spec["seat"])
        report = play(AGENT, path, spec["seat"], 720)
        rec = {
            "group": spec["group"],
            "margin": report["margin"],
            "v189c_margin": spec["v189c_margin"],
            "delta_vs_v189c": report["margin"] - spec["v189c_margin"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
            "yarn": profile,
        }
        rows[key] = rec
        print(key, rec["margin"], "delta", rec["delta_vs_v189c"], "yarn", profile, flush=True)
    g5 = [k for k, s in STREAMS.items() if s["group"] == "g5"]
    low = [k for k, s in STREAMS.items() if s["group"] == "lowfert"]
    payload = {
        "agent": "moon_shopbag_v1",
        "g5_wins": sum(int(rows.get(k, {}).get("win", False)) for k in g5),
        "g5_n": len(g5),
        "lowfert_wins": sum(int(rows.get(k, {}).get("win", False)) for k in low),
        "lowfert_n": len(low),
        "any_gate_differs": any(
            isinstance(rows.get(k), dict)
            and rows[k].get("yarn", {}).get("gate_differs_from_v189c")
            for k in rows
        ),
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, payload["g5_wins"], "/", payload["g5_n"], "lowfert", payload["lowfert_wins"], "/", payload["lowfert_n"])


if __name__ == "__main__":
    main()
