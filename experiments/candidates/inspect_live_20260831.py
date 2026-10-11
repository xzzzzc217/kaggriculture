"""Parse 2026-08-31 LB + v4 episode W-T-L."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LB_ZIP = ROOT / "artifacts/kaggle_runs/lb_20260831/kaggriculture.zip"
EPS = ROOT / "experiments/episodes_55887331.json"
OUR = 55887331
NEED = (
    "Yusuke",
    "MtN",
    "Hanserong",
    "Crop Dusta",
    "Milan",
    "Subramanya",
    "Ryo",
    "Jiro",
    "Kenjo",
    "Pavlo",
    "heralces",
    "Lynxx",
    "nir afek",
    "Tom3",
    "chupaletas",
    "tiki",
    "Boredom",
    "Remielle",
)


def score(row: dict):
    for key, value in row.items():
        if key.lower() == "score":
            try:
                return float(value)
            except ValueError:
                return None
    return None


def team_name(teams: dict, tid) -> str:
    t = teams.get(tid) or {}
    return t.get("teamName") or t.get("name") or str(tid)


def main() -> None:
    with zipfile.ZipFile(LB_ZIP) as z:
        name = z.namelist()[0]
        data = z.read(name).decode("utf-8")
    print("csv", name)
    rows = list(csv.DictReader(io.StringIO(data)))
    ranked = [(i, row, score(row)) for i, row in enumerate(rows, 1)]
    print("n", len(rows))
    print("TOP15")
    for i, row, s in ranked[:15]:
        print(f"{i:3d} {s:8.1f} {row.get('TeamName')}")
    print("GOLD21", ranked[20][2], ranked[20][1].get("TeamName"))
    print("RANK10", ranked[9][2], ranked[9][1].get("TeamName"))
    for i, row, s in ranked:
        if "heralces" in str(row.get("TeamName") or "").lower():
            print("HER", i, s)
            break
    print("NAMED")
    for i, row, s in ranked:
        team = str(row.get("TeamName") or "")
        if any(n.lower() in team.lower() for n in NEED):
            print(f"{i:4d} {s:8.1f} {team}")

    payload = json.loads(EPS.read_text(encoding="utf-8"))
    eps = payload["episodes"]
    teams = {t["id"]: t for t in payload.get("teams") or []}
    pub = [
        e
        for e in eps
        if e.get("type") == "EPISODE_TYPE_PUBLIC" and e.get("state") == "COMPLETED"
    ]
    pub.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    print("public completed", len(pub))

    def rec(e):
        agents = e.get("agents") or []
        ours = next(a for a in agents if a.get("submissionId") == OUR)
        opp = next(a for a in agents if a.get("submissionId") != OUR)
        m = (ours.get("reward") or 0) - (opp.get("reward") or 0)
        w = "W" if m > 0 else ("T" if m == 0 else "L")
        return w, m, ours, opp, e

    def dump(label, games):
        wtl = Counter()
        margins = []
        print("---", label, "---")
        for w, m, ours, opp, e in games:
            wtl[w] += 1
            margins.append(m)
            print(
                f"{e['id']} {str(e.get('createTime', ''))[:19]} {w} {m:+7.0f} "
                f"us={ours.get('reward')} opp={opp.get('reward')} "
                f"oppTeam={team_name(teams, opp.get('teamId'))} "
                f"{ours.get('initialScore'):.1f}->{ours.get('updatedScore'):.1f}"
            )
        mean = sum(margins) / len(margins) if margins else None
        print(label, "wtl", dict(wtl), "mean", mean)

    dump("rolling12", [rec(e) for e in pub[:12]])
    dump("all", [rec(e) for e in pub])


if __name__ == "__main__":
    main()
