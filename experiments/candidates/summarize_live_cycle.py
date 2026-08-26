"""One-shot live cycle helpers: leaderboard parse + compact replay summaries."""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_episode import summarize  # noqa: E402


def parse_leaderboard(zip_path: Path) -> dict:
    with zipfile.ZipFile(zip_path) as z:
        name = z.namelist()[0]
        data = z.read(name).decode("utf-8")
    csv_path = zip_path.parent / "leaderboard.csv"
    csv_path.write_text(data, encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))

    def score(row: dict) -> float | None:
        for key, value in row.items():
            if key.lower() == "score":
                try:
                    return float(value)
                except ValueError:
                    return None
        return None

    ranked = [(i, row, score(row)) for i, row in enumerate(rows, 1)]
    her = None
    named_need = (
        "OceanMix",
        "Black Mamba",
        "One-For-All",
        "Kaileh",
        "boatlee",
        "flexonafft",
        "stevenleehans",
        "Amey",
        "tetsutani",
        "Kaito",
        "prvsiyan",
        "heralces",
        "Amy Yuan",
        "MUGUNDH",
        "Jiachen",
        "destbreso",
        "Busyaprime",
        "One-For",
        "Pixs",
        "Audric",
        "CoorDi",
    )
    named = []
    for i, row, s in ranked:
        team = str(row.get("TeamName") or "")
        if any(n.lower() in team.lower() for n in named_need):
            named.append({"rank": i, "score": s, "team": team})
        if "heralces" in team.lower():
            her = {"rank": i, "score": s, "team": team, "row": row}
    return {
        "n_teams": len(rows),
        "gold21": {"rank": 21, "score": ranked[20][2], "team": ranked[20][1].get("TeamName")}
        if len(ranked) >= 21
        else None,
        "silver297": {
            "rank": 297,
            "score": ranked[296][2],
            "team": ranked[296][1].get("TeamName"),
        }
        if len(ranked) >= 297
        else None,
        "bronze595": {
            "rank": 595,
            "score": ranked[594][2],
            "team": ranked[594][1].get("TeamName"),
        }
        if len(ranked) >= 595
        else None,
        "top15": [
            {"rank": i, "score": s, "team": r.get("TeamName")} for i, r, s in ranked[:15]
        ],
        "heralces": her,
        "named": named,
    }


def compact_replay(path: Path, our_team: str = "heralces") -> dict:
    replay = json.loads(path.read_text(encoding="utf-8"))
    teams = list(replay.get("info", {}).get("TeamNames", []))
    if our_team in teams:
        seat = teams.index(our_team)
    else:
        seat = 0
    report = summarize(replay, seat, None)
    our_sig = report["final_public_signatures"][seat]
    opp_sig = report["final_public_signatures"][1 - seat]
    mq = report["market_order_quantities"]
    return {
        "episode": report["episode_id"],
        "seed": report["seed"],
        "opp": teams[1 - seat] if len(teams) > 1 - seat else "",
        "teams": teams,
        "seat": seat,
        "margin": report["margin"],
        "win": report["margin"] > 0,
        "tie": report["margin"] == 0,
        "rewards": report["rewards"],
        "statuses": report["statuses"],
        "Q": [our_sig["unlocked_quadrants"], opp_sig["unlocked_quadrants"]],
        "sheep": [our_sig["objects"].get("SHEEP", 0), opp_sig["objects"].get("SHEEP", 0)],
        "cow": [our_sig["objects"].get("COW", 0), opp_sig["objects"].get("COW", 0)],
        "melon": [our_sig["objects"].get("MELON", 0), opp_sig["objects"].get("MELON", 0)],
        "fert": [
            mq[seat].get("SELL:FERTILIZER", 0),
            mq[1 - seat].get("SELL:FERTILIZER", 0),
        ],
        "wheat": [mq[seat].get("SELL:WHEAT", 0), mq[1 - seat].get("SELL:WHEAT", 0)],
        "clone": report["clone_gate"]["latched"],
        "max_near": report["clone_gate"]["maximum_near_streak"],
        "median_distance": report["clone_gate"]["median_distance"],
        "path": str(path),
    }


def main() -> None:
    lb = parse_leaderboard(
        ROOT / "artifacts/leaderboard_snapshots/20260824_obs4/kaggriculture.zip"
    )
    print(json.dumps({"leaderboard": lb}, indent=2))
    dest_dir = ROOT / "artifacts/kaggle_runs/submission_55710781/obs4"
    rows = []
    for path in sorted(dest_dir.glob("episode-*-replay.json")):
        rec = compact_replay(path)
        rows.append(rec)
        print(json.dumps(rec))
    out = ROOT / "experiments/20260824_boatlee_obs4.json"
    out.write_text(json.dumps({"leaderboard": lb, "games": rows}, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT))
    main()
