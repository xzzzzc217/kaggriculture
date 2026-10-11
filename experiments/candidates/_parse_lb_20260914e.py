"""Parse live LB zip for 20260914e."""

from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

Z = Path(r"D:\kaggle\kaggriculture\artifacts\kaggle_runs\lb_20260914e_live\kaggriculture.zip")
with zipfile.ZipFile(Z) as z:
    print("members", z.namelist())
    name = z.namelist()[0]
    data = z.read(name).decode("utf-8")
csv_path = Z.parent / name.replace(":", "-")
csv_path.write_text(data, encoding="utf-8")
rows = list(csv.DictReader(io.StringIO(data)))
print("csv", name, "n_teams", len(rows))
print("--- TOP 15 ---")
for i, r in enumerate(rows[:15], 1):
    print(
        f"{i:2d} {float(r['Score']):8.1f} {r['TeamName']!r:30s} "
        f"teamId={r['TeamId']} last={r['LastSubmissionDate']}"
    )
print("gold21", rows[20]["TeamName"], rows[20]["Score"])
print("rank10", rows[9]["TeamName"], rows[9]["Score"])
for i, r in enumerate(rows, 1):
    if "heralces" in (r["TeamName"] or "").lower():
        print("heralces", i, r["Score"], r["TeamName"], r["TeamId"], r["LastSubmissionDate"])
        break
print("csv_path", csv_path)
