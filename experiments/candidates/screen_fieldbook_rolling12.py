"""Fieldbook vs newest shopbag rolling-12 recorded streams. No upload."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay_callback import play  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / "experiments/candidates/yusuke_fieldbook/main.py"
LIVE = ROOT / "artifacts/kaggle_runs/top_20260901"
OUT = ROOT / "experiments/candidates/yusuke_fieldbook/rolling12_screen.json"

# seat 0 if heralces listed first in replay; we resolve per file.
STREAMS = {
    "mostafa_104553501": {"id": 104553501, "shopbag": -2676},
    "bandito_104552870": {"id": 104552870, "shopbag": -17060},
    "souju00_104548685": {"id": 104548685, "shopbag": -1170},
    "zhongyi_104546457": {"id": 104546457, "shopbag": -12940},
    "liaf_104542554": {"id": 104542554, "shopbag": -9935},
    "v4_jianyuan_104549818": {"id": 104549818, "shopbag": -9962},
}


def seat_of(path: Path) -> int:
    replay = json.loads(path.read_text(encoding="utf-8"))
    return replay["info"]["TeamNames"].index("heralces")


def main() -> None:
    rows = {}
    wins = 0
    flips = []
    for key, spec in STREAMS.items():
        path = LIVE / f"episode-{spec['id']}-replay.json"
        seat = seat_of(path)
        report = play(AGENT, path, seat, 720)
        rec = {
            "margin": report["margin"],
            "shopbag": spec["shopbag"],
            "delta": report["margin"] - spec["shopbag"],
            "win": bool(report["win"]),
            "statuses": report["statuses"],
            "scores": [report["own_reward"], report["opponent_reward"]],
            "seat": seat,
        }
        wins += int(rec["win"])
        if rec["win"] and spec["shopbag"] <= 0:
            flips.append(key)
        rows[key] = rec
        print(key, rec, flush=True)
    payload = {"wins": wins, "n": len(rows), "flips": flips, "rows": rows}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT, "wins", wins, "/", len(rows), "flips", flips)


if __name__ == "__main__":
    main()
