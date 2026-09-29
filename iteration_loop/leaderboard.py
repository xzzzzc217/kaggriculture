"""Gold-place cutoff for Kaggriculture.

For a field of at least 250 teams, gold is the best ranks within
``10 + 0.2%`` of teams. A field of 9967 teams cuts gold at rank 29.
"""

from __future__ import annotations

import csv
import io

MIN_MEDAL_FIELD = 250
TEAM_NAME = "heralces"


def gold_rank_cutoff(team_count: int) -> int:
    if team_count < MIN_MEDAL_FIELD:
        raise ValueError(
            f"gold places are defined for a field of at least {MIN_MEDAL_FIELD} teams, "
            f"got {team_count}"
        )
    return 10 + (team_count * 2) // 1000


def team_in_gold(rank: int, team_count: int) -> bool:
    if rank < 1:
        return False
    return rank <= gold_rank_cutoff(team_count)


def heralces_from_csv(csv_text: str, team: str = TEAM_NAME) -> dict[str, object]:
    """Read a Kaggle leaderboard CSV. Rank 1 is the first data row if no rank column."""
    reader = csv.DictReader(io.StringIO(csv_text.lstrip("\ufeff").strip()))
    if not reader.fieldnames:
        raise RuntimeError("leaderboard CSV has no header")
    normalized = {name.lower(): name for name in reader.fieldnames if name}
    team_field = next(
        (
            normalized[name]
            for name in ("teamname", "team name", "team", "displayname")
            if name in normalized
        ),
        None,
    )
    if team_field is None:
        raise RuntimeError(f"leaderboard CSV has no team column: {reader.fieldnames}")
    rank_field = next(
        (normalized[name] for name in ("rank", "#") if name in normalized),
        None,
    )
    score_field = next(
        (normalized[name] for name in ("score", "publicscore") if name in normalized),
        None,
    )
    rows = list(reader)
    found: dict[str, object] | None = None
    for index, row in enumerate(rows, start=1):
        rank = int(float(row[rank_field])) if rank_field else index
        if str(row[team_field]).strip().lower() == team.lower():
            found = {
                "team": str(row[team_field]).strip(),
                "rank": rank,
                "score": row[score_field] if score_field else None,
            }
            break
    team_count = len(rows)
    cutoff = gold_rank_cutoff(team_count) if team_count >= MIN_MEDAL_FIELD else None
    in_gold = bool(found and cutoff is not None and team_in_gold(int(found["rank"]), team_count))
    return {
        "team_count": team_count,
        "gold_cutoff": cutoff,
        "team": None if found is None else found["team"],
        "rank": None if found is None else found["rank"],
        "score": None if found is None else found["score"],
        "in_gold": in_gold,
    }
