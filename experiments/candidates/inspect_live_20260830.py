"""Parse latest LB + shopbag episode W-T-L. No upload."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LB_ZIP = ROOT / "artifacts/kaggle_runs/lb_20260830b/kaggriculture.zip"
EPS = ROOT / "experiments/episodes_55840543.json"
OUR = 55840543
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
    "indarkarhana",
    "tetsutani",
    "Kaito",
    "prvsiyan",
    "boatlee",
    "destbreso",
    "MiMi",
    "Collin",
    "smsxgz",
    "Lynxx",
    "heralces",
    "Niklita",
    "Jiro2",
    "TK256",
    "nir afek",
    "Tom3",
    "chupaletas",
)


def score(row: dict) -> float | None:
    for key, value in row.items():
        if key.lower() == "score":
            try:
                return float(value)
            except ValueError:
                return None
    return None


def parse_lb() -> None:
    with zipfile.ZipFile(LB_ZIP) as z:
        name = z.namelist()[0]
        data = z.read(name).decode("utf-8")
    print("csv", name)
    rows = list(csv.DictReader(io.StringIO(data)))
    ranked = [(i, row, score(row)) for i, row in enumerate(rows, 1)]
    print("n", len(rows), "keys", list(rows[0].keys()))
    print("TOP15")
    for i, row, s in ranked[:15]:
        print(f"{i:3d} {s:8.1f} {row.get('TeamName')}")
    print("GOLD21", ranked[20][2], ranked[20][1].get("TeamName"))
    print("RANK10", ranked[9][2], ranked[9][1].get("TeamName"))
    for i, row, s in ranked:
        if "heralces" in str(row.get("TeamName") or "").lower():
            print("HER", i, s, {k: row[k] for k in row})
            break
    print("NAMED")
    for i, row, s in ranked:
        team = str(row.get("TeamName") or "")
        if any(n.lower() in team.lower() for n in NEED):
            print(f"{i:4d} {s:8.1f} {team}")


def team_name(teams: dict, tid) -> str:
    t = teams.get(tid) or {}
    return t.get("teamName") or t.get("name") or t.get("publicName") or str(tid)


def parse_eps() -> list[int]:
    payload = json.loads(EPS.read_text(encoding="utf-8"))
    eps = payload["episodes"]
    subs = {s["id"]: s for s in payload.get("submissions") or []}
    teams = {t["id"]: t for t in payload.get("teams") or []}
    print("n_eps", len(eps), "n_subs", len(subs), "n_teams", len(teams))
    if teams:
        sample = next(iter(teams.values()))
        print("team keys", list(sample.keys())[:25])
        print("team sample", {k: sample[k] for k in sample if "name" in k.lower() or k in ("id",)})
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
        our_r = ours.get("reward") or 0
        opp_r = opp.get("reward") or 0
        m = our_r - opp_r
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
                f"oppSub={opp.get('submissionId')} "
                f"{ours.get('initialScore'):.1f}->{ours.get('updatedScore'):.1f}"
            )
        mean = sum(margins) / len(margins) if margins else None
        print(label, "wtl", dict(wtl), "mean", mean)
        return wtl, mean

    dump("rolling12", [rec(e) for e in pub[:12]])
    dump("rolling20", [rec(e) for e in pub[:20]])
    wtl = Counter()
    margins = []
    for e in pub:
        w, m, *_ = rec(e)
        wtl[w] += 1
        margins.append(m)
    print("all public", dict(wtl), "n", len(pub), "mean", sum(margins) / len(margins))
    return [e["id"] for e in pub[:16]]


def main() -> None:
    parse_lb()
    newest = parse_eps()
    print("NEWEST_IDS", newest)


if __name__ == "__main__":
    main()
