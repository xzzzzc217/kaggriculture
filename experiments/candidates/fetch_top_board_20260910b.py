"""ymg_aq current sub via ListTeamPublicSubmissions, then EpisodeService + replays."""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests
from kaggle.api.kaggle_api_extended import KaggleApi
from kagglesdk.competitions.types.competition_api_service import (
    ApiGetLeaderboardRequest,
    ApiListSubmissionEpisodesRequest,
    ApiListTeamPublicSubmissionsRequest,
)

ROOT = Path(__file__).resolve().parents[2]
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
REPLAY_URL = "https://www.kaggleusercontent.com/episodes/{id}.json"
TEAM_ID = 16732403
TEAM = "ymg_aq"
DEST = ROOT / "artifacts/kaggle_runs/top_20260910b"
SKIP_IDS = {
    106976067,
    106976069,
    106976065,
    106958424,
    107493475,
    107487687,
    107482596,
    107481864,
}


def episode_state_name(value) -> str:
    name = getattr(value, "name", None)
    if name:
        if name == "COMPLETED":
            return "COMPLETED"
        if name.endswith("COMPLETED"):
            return "COMPLETED"
        return name
    return str(value)


def episode_type_name(value) -> str:
    name = getattr(value, "name", None)
    if name:
        return name
    return str(value)


def main() -> None:
    api = KaggleApi()
    api.authenticate()
    with api.build_kaggle_client() as kaggle:
        lb_req = ApiGetLeaderboardRequest()
        lb_req.competition_name = "kaggriculture"
        lb_req.override_public = True
        lb_req.page_size = 25
        lb = kaggle.competitions.competition_api_client.get_leaderboard(lb_req)
        print("LB n", len(lb.submissions or []), flush=True)
        for i, row in enumerate(lb.submissions or [], 1):
            print(i, row.team_id, row.team_name, row.score, row.submission_date, flush=True)

        sub_req = ApiListTeamPublicSubmissionsRequest()
        sub_req.team_id = TEAM_ID
        subs_resp = kaggle.competitions.competition_api_client.list_team_public_submissions(sub_req)
        subs = list(subs_resp.submissions or [])
        print("n_subs", len(subs), flush=True)
        for s in subs:
            print("sub", s.id, s.public_score, s.date_submitted, flush=True)
        if not subs:
            raise SystemExit("no public submissions for ymg_aq")
        current = max(subs, key=lambda x: int(x.id or 0))
        sub_id = int(current.id)
        print("CURRENT_SUB", sub_id, current.public_score, current.date_submitted, flush=True)

        # Official EpisodeService (same shape as prior packets).
        sess = requests.Session()
        sess.headers["User-Agent"] = "kaggriculture-local-audit"
        r = sess.post(LIST_URL, json={"submissionId": sub_id}, timeout=60)
        print("ListEpisodes submissionId", sub_id, "status", r.status_code, flush=True)
        r.raise_for_status()
        payload = r.json()
        out = ROOT / "experiments" / f"episodes_sub_{sub_id}_ymg_aq.json"
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print("WROTE", out, "n", len(payload.get("episodes") or []), flush=True)

        eps = payload.get("episodes") or []
        public = [
            e
            for e in eps
            if e.get("state") == "COMPLETED"
            and e.get("type") == "EPISODE_TYPE_PUBLIC"
            and int(e.get("id") or 0) not in SKIP_IDS
        ]
        public.sort(key=lambda e: e.get("createTime") or "", reverse=True)
        print("n_public_completed", len(public), "of", len(eps), flush=True)
        picked = public[:4]
        if len(picked) < 3:
            # Fallback: SDK list_submission_episodes
            ep_req = ApiListSubmissionEpisodesRequest()
            ep_req.submission_id = sub_id
            sdk_eps = kaggle.competitions.competition_api_client.list_submission_episodes(ep_req)
            print("SDK episodes", len(sdk_eps.episodes or []), flush=True)
            fallback = []
            for e in sdk_eps.episodes or []:
                rec = {
                    "id": int(e.id),
                    "createTime": str(e.create_time),
                    "endTime": str(e.end_time),
                    "state": episode_state_name(e.state),
                    "type": episode_type_name(e.type),
                    "agents": [
                        {
                            "submissionId": a.submission_id,
                            "index": a.index,
                            "reward": a.reward,
                            "teamId": a.team_id,
                            "teamName": a.team_name,
                        }
                        for a in (e.agents or [])
                    ],
                }
                fallback.append(rec)
            public = [
                e
                for e in fallback
                if "COMPLETED" in str(e.get("state"))
                and "PUBLIC" in str(e.get("type"))
                and int(e.get("id") or 0) not in SKIP_IDS
            ]
            public.sort(key=lambda e: e.get("createTime") or "", reverse=True)
            picked = public[:4]
            sdk_out = ROOT / "experiments" / f"episodes_sub_{sub_id}_ymg_aq_sdk.json"
            sdk_out.write_text(json.dumps({"episodes": fallback}, indent=2) + "\n", encoding="utf-8")
            print("WROTE", sdk_out, flush=True)

        print("PICKED", [e["id"] for e in picked], flush=True)
        for e in picked:
            print(e["id"], e.get("createTime"), e.get("agents"), flush=True)

        DEST.mkdir(parents=True, exist_ok=True)
        for e in picked:
            eid = int(e["id"])
            path = DEST / f"episode-{eid}-replay.json"
            if path.exists() and path.stat().st_size > 1000:
                print("have", eid, path.stat().st_size, flush=True)
                continue
            rr = sess.get(REPLAY_URL.format(id=eid), timeout=180)
            print(eid, rr.status_code, len(rr.content), flush=True)
            rr.raise_for_status()
            path.write_bytes(rr.content)
            time.sleep(0.6)
        print("done", DEST, flush=True)

        # Compact API snapshot for the hunt report.
        api_rows = []
        for i, row in enumerate(lb.submissions or [], 1):
            api_rows.append(
                {
                    "teamId": row.team_id,
                    "rank": i,
                    "displayScore": row.score,
                    "teamName": row.team_name,
                    "submissionDate": str(row.submission_date),
                }
            )
        api_out = {
            "n": None,
            "csv": "artifacts/kaggle_runs/lb_20260910b/kaggriculture-publicleaderboard-2026-09-10T20:08:14.csv",
            "top20": api_rows[:20],
            "picked": {
                "team": TEAM,
                "teamId": TEAM_ID,
                "submissionId": sub_id,
                "score": current.public_score,
                "dateSubmitted": str(current.date_submitted),
                "rank": 2,
            },
        }
        api_path = ROOT / "experiments/20260910b_public_leaderboard_api.json"
        api_path.write_text(json.dumps(api_out, indent=2) + "\n", encoding="utf-8")
        print("WROTE", api_path, flush=True)


if __name__ == "__main__":
    main()
