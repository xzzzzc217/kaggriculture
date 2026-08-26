"""Compact summaries for shops public-12 and two new boatlee games."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.candidates.summarize_live_cycle import compact_replay  # noqa: E402


def dump(paths: list[Path], dest: Path) -> list[dict]:
    rows = []
    for path in paths:
        rec = compact_replay(path)
        rows.append(rec)
        print(
            rec["episode"],
            rec["opp"],
            "seat",
            rec["seat"],
            "margin",
            rec["margin"],
            "win" if rec["win"] else ("tie" if rec["tie"] else "loss"),
            "fert",
            rec["fert"],
            "clone",
            rec["clone"],
            "Q",
            rec["Q"],
            "statuses",
            rec["statuses"],
        )
    wins = sum(1 for r in rows if r["win"])
    ties = sum(1 for r in rows if r["tie"])
    losses = len(rows) - wins - ties
    mean = sum(r["margin"] for r in rows) / len(rows)
    summary = {
        "n": len(rows),
        "wtl": [wins, ties, losses],
        "mean_margin": mean,
        "games": rows,
    }
    dest.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("W/T/L", wins, ties, losses, "mean", round(mean, 1), "WROTE", dest)
    return rows


def main() -> None:
    shops_dir = ROOT / "artifacts/kaggle_runs/submission_55744278/public12b"
    dump(
        sorted(shops_dir.glob("episode-*-replay.json"), reverse=True),
        ROOT / "experiments/20260825_shops_public12b.json",
    )


if __name__ == "__main__":
    main()
