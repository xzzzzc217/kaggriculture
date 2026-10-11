"""Parse lb_20260910b zip; print missing high-rank team."""

from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZPATH = ROOT / "artifacts/kaggle_runs/lb_20260910b/kaggriculture.zip"
MEASURED = {
    "Giulio Ravasio",
    "Knight of Favonius",
    "sbol ball",
    "Jesse Bullard",
    "keiz",
    "SpaTaro",
    "Otter Vibe",
}


def main() -> None:
    with zipfile.ZipFile(ZPATH) as z:
        print("members", z.namelist())
        name = z.namelist()[0]
        data = z.read(name).decode("utf-8")
    csv_path = ZPATH.parent / "leaderboard.csv"
    csv_path.write_text(data, encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    print("csv", name)
    print("n_teams", len(rows), "cols", list(rows[0].keys()))
    print("--- TOP 15 ---")
    pick = None
    for i, r in enumerate(rows[:15], 1):
        miss = "MISSING" if r["TeamName"] not in MEASURED else "measured"
        print(
            f"{i:2d} {float(r['Score']):8.1f} {r['TeamName']!r:30s} "
            f"teamId={r['TeamId']} last={r['LastSubmissionDate']} {miss}"
        )
        if pick is None and r["TeamName"] not in MEASURED:
            pick = (i, r)
    print("--- heralces ---")
    for i, r in enumerate(rows, 1):
        if "heralces" in (r["TeamName"] or "").lower():
            print(i, dict(r))
            break
    print("gold21", rows[20]["TeamName"], rows[20]["Score"])
    if pick:
        print("PICK", pick[0], dict(pick[1]))


if __name__ == "__main__":
    main()
