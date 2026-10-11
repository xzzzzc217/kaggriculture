"""Parse lb_20260911 zip; print top board, heralces, missing high-rank team."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZPATH = ROOT / "artifacts/kaggle_runs/lb_20260911/kaggriculture.zip"
OUT_API = ROOT / "experiments/20260911_public_leaderboard_api.json"
PRIOR = [
    ROOT / "experiments/20260904_top10_games.json",
    ROOT / "experiments/20260905_top10_games.json",
    ROOT / "experiments/20260906_top10_games.json",
    ROOT / "experiments/20260909_top10_games.json",
    ROOT / "experiments/20260910_top10_games.json",
]


def main() -> None:
    with zipfile.ZipFile(ZPATH) as z:
        print("members", z.namelist())
        name = z.namelist()[0]
        data = z.read(name).decode("utf-8")
    # Windows cannot write filenames containing ':'.
    csv_path = ZPATH.parent / name.replace(":", "-")
    csv_path.write_text(data, encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    print("csv", name)
    print("n_teams", len(rows), "cols", list(rows[0].keys()))
    measured: set[str] = set()
    for path in PRIOR:
        for row in json.loads(path.read_text(encoding="utf-8")):
            measured.add(row["team"])
    print("measured_04_10", sorted(measured))
    print("--- TOP 15 ---")
    pick = None
    csv_top = []
    for i, r in enumerate(rows[:15], 1):
        miss = r["TeamName"] not in measured
        print(
            f"{i:2d} {float(r['Score']):8.1f} {r['TeamName']!r:30s} "
            f"teamId={r['TeamId']} last={r['LastSubmissionDate']} "
            f"{'MISSING' if miss else 'measured'}"
        )
        csv_top.append(
            {
                "rank": i,
                "teamId": int(r["TeamId"]),
                "teamName": r["TeamName"],
                "score": r["Score"],
                "lastSubmissionDate": r["LastSubmissionDate"],
                "missing_from_04_10": miss,
            }
        )
        if pick is None and miss:
            pick = (i, r)
    print("--- heralces ---")
    her = None
    her_rank = None
    for i, r in enumerate(rows, 1):
        if "heralces" in (r["TeamName"] or "").lower():
            her = r
            her_rank = i
            print(i, dict(r))
            break
    gold21 = rows[20]
    print("gold21", gold21["TeamName"], gold21["Score"])
    if pick:
        print("PICK", pick[0], dict(pick[1]))
    payload = {
        "n": len(rows),
        "csv": str(csv_path.as_posix()),
        "csv_time": name.split("kaggriculture-publicleaderboard-")[-1].replace(".csv", ""),
        "csv_top15": csv_top,
        "picked": None
        if pick is None
        else {
            "team": pick[1]["TeamName"],
            "teamId": int(pick[1]["TeamId"]),
            "csv_rank": pick[0],
            "csv_score": pick[1]["Score"],
            "lastSubmissionDate": pick[1]["LastSubmissionDate"],
        },
        "heralces_csv": {
            "rank": her_rank,
            "teamId": int(her["TeamId"]) if her else None,
            "score": her["Score"] if her else None,
            "lastSubmissionDate": her["LastSubmissionDate"] if her else None,
        },
        "gold21_csv": {
            "rank": 21,
            "team": gold21["TeamName"],
            "score": gold21["Score"],
        },
        "rank1": {
            "team": rows[0]["TeamName"],
            "score": rows[0]["Score"],
            "teamId": int(rows[0]["TeamId"]),
        },
    }
    OUT_API.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT_API)


if __name__ == "__main__":
    main()
