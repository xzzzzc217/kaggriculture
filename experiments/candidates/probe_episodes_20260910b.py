"""Probe EpisodeService + leaderboard endpoints for ymg_aq."""

from __future__ import annotations

import json
from pathlib import Path

import requests

TEAM_ID = 16732403
ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    s = requests.Session()
    s.headers["User-Agent"] = "kaggriculture-local-audit"
    trials = [
        ("api_i_teamId", "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes", {"teamId": TEAM_ID}),
        ("api_i_TeamId", "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes", {"TeamId": TEAM_ID}),
        ("requests_TeamId", "https://www.kaggle.com/requests/EpisodeService/ListEpisodes", {"TeamId": TEAM_ID}),
        ("requests_teamId", "https://www.kaggle.com/requests/EpisodeService/ListEpisodes", {"teamId": TEAM_ID}),
        ("api_i_ids", "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes", {"ids": [TEAM_ID]}),
        ("requests_Ids", "https://www.kaggle.com/requests/EpisodeService/ListEpisodes", {"Ids": [TEAM_ID]}),
    ]
    for name, url, body in trials:
        r = s.post(url, json=body, timeout=60)
        text = r.text[:400].replace("\n", " ")
        print(f"{name} status={r.status_code} len={len(r.content)} body={text}", flush=True)

    # competition metadata
    r = s.get("https://www.kaggle.com/api/v1/competitions/kaggriculture", timeout=60)
    print("comp_v1", r.status_code, r.text[:500], flush=True)

    # LeaderboardService guesses
    lb_bodies = [
        {"competitionName": "kaggriculture"},
        {"competitionId": 102312},
        {"CompetitionName": "kaggriculture"},
    ]
    lb_urls = [
        "https://www.kaggle.com/api/i/competitions.LeaderboardService/GetLeaderboard",
        "https://www.kaggle.com/api/i/competitions.CompetitionService/GetLeaderboard",
    ]
    for url in lb_urls:
        for body in lb_bodies:
            r = s.post(url, json=body, timeout=60)
            print("LB", url.split("/")[-1], body, r.status_code, r.text[:200].replace("\n", " "), flush=True)


if __name__ == "__main__":
    main()
