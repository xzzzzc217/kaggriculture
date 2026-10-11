"""Compact newest Crop Dusta games from the 8/28 official unpack."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.candidates.summarize_live_cycle import compact_replay  # noqa: E402

SRC = ROOT / "artifacts/kaggle_runs/episodes_20260828"
OUT = ROOT / "experiments/20260829_crop_dusta_public8.json"


def main() -> None:
    found: list[Path] = []
    for path in sorted(SRC.glob("*.json"), key=lambda p: int(p.stem), reverse=True):
        head = path.read_bytes()[:4000]
        if b"Crop Dusta" in head:
            found.append(path)
            if len(found) >= 8:
                break
    print("found", [p.name for p in found], flush=True)
    rows = []
    for path in found:
        rec = compact_replay(path, our_team="Crop Dusta")
        rows.append(rec)
        print(
            rec["episode"],
            rec["opp"],
            rec["margin"],
            "W",
            rec["wheat"],
            "F",
            rec["fert"],
            "shp",
            rec["sheep"],
            "clone",
            rec["clone"],
            flush=True,
        )
    w = sum(r["win"] for r in rows)
    t = sum(r["tie"] for r in rows)
    payload = {"n": len(rows), "wtl": [w, t, len(rows) - w - t], "games": rows}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
