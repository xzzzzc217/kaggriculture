"""Parse a downloaded public leaderboard zip."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

ZIP_PATH = Path("artifacts/leaderboard_snapshots/20260825_obs3/kaggriculture.zip")


def main() -> None:
    with zipfile.ZipFile(ZIP_PATH) as archive:
        print("members", archive.namelist())
        name = archive.namelist()[0]
        data = archive.read(name).decode("utf-8")
    dest = ZIP_PATH.parent / "leaderboard.csv"
    dest.write_text(data, encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    print("n_teams", len(rows), "cols", list(rows[0].keys()))

    def score(row: dict) -> float | None:
        for key, value in row.items():
            if key.lower() == "score":
                try:
                    return float(value)
                except ValueError:
                    return None
        return None

    ranked = [(i, row, score(row)) for i, row in enumerate(rows, 1)]
    print("gold21", ranked[20][2], ranked[20][1].get("TeamName"))
    print("silver297", ranked[296][2] if len(ranked) >= 297 else None)
    print("bronze595", ranked[594][2] if len(ranked) >= 595 else None)
    for i, row, value in ranked:
        team = str(row.get("TeamName") or "")
        if "heralces" in team.lower():
            print("HER", i, value, dict(row))
            break
    need = (
        "Kaileh",
        "OceanMix",
        "boatlee",
        "Jiachen",
        "Black Mamba",
        "One-For-All",
        "prvsiyan",
        "Kaito Fukami",
        "Amey Thakur",
    )
    for i, row, value in ranked:
        team = str(row.get("TeamName") or "")
        if any(n.lower() in team.lower() for n in need):
            print(f"{i:4d} {value:8.1f} {team}")
    # score at rank 578
    if len(ranked) >= 578:
        i, row, value = ranked[577]
        print("rank578", value, row.get("TeamName"))
    # who is near 1995 and 2108
    for i, row, value in ranked:
        if value is None:
            continue
        if 1990 <= value <= 2005 or 2100 <= value <= 2120:
            if i in {390, 394, 400, 500, 550, 570, 578, 580, 595, 600} or (
                1990 <= value <= 2000 and abs(i - 578) < 8
            ):
                print("near", i, value, row.get("TeamName"))


if __name__ == "__main__":
    main()
