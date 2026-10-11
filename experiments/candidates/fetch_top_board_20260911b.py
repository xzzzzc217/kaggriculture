"""Majkel1337 current scoring/newest sub, EpisodeService + 4 new replays."""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests
from kaggle.api.kaggle_api_extended import KaggleApi
from kagglesdk.competitions.types.competition_api_service import (
    ApiGetLeaderboardRequest,
    ApiListTeamPublicSubmissionsRequest,
)

ROOT = Path(__file__).resolve().parents[2]
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
REPLAY_URL = "https://www.kaggleusercontent.com/episodes/{id}.json"
TEAM_ID = 16718819
TEAM = "Majkel1337"
DEST = ROOT / "artifacts/kaggle_runs/top_20260911b"
SKIP_IDS = {
    107756968,
    107751894,
    107746036,
    107740777,
    107582281,
    107581290,
    107580344,
    107579345,
}


def main() -> None:
    api = KaggleApi()
    api.authenticate()
    with api.build_kaggle_client() as kaggle:
        lb_req = ApiGetLeaderboardRequest()
        lb_req.competition_name = "kaggriculture"
        lb_req.override_public = True
        lb_req.page_size = 25
        lb = kaggle.competitions.competition_api_client.get_leaderboard(lb_req)
        live_rows = []
        for i, row in enumerate(lb.submissions or [], 1):
            rec = {
                "rank": i,
                "teamId": row.team_id,
                "teamName": row.team_name,
                "score": row.score,
                "submissionDate": str(row.submission_date),
            }
            live_rows.append(rec)
            print(i, row.team_id, row.team_name, row.score, row.submission_date, flush=True)

        sub_req = ApiListTeamPublicSubmissionsRequest()
        sub_req.team_id = TEAM_ID
        subs_resp = kaggle.competitions.competition_api_client.list_team_public_submissions(sub_req)
        subs = list(subs_resp.submissions or [])
        print("n_subs", len(subs), flush=True)
        for s in subs:
            print("sub", s.id, s.public_score, s.date_submitted, flush=True)
        if not subs:
            raise SystemExit("no public submissions for Majkel1337")
        # Prefer the higher COMPLETE public_score as the scoring partner; still measure newest games on max-id if that is live.
        by_score = max(subs, key=lambda x: float(x.public_score or 0))
        current = max(subs, key=lambda x: int(x.id or 0))
        sub_id = int(current.id)
        print("CURRENT_SUB", sub_id, current.public_score, current.date_submitted, flush=True)
        print("SCORING_SUB", by_score.id, by_score.public_score, by_score.date_submitted, flush=True)

        sess = requests.Session()
        sess.headers["User-Agent"] = "kaggriculture-local-audit"
        r = sess.post(LIST_URL, json={"submissionId": sub_id}, timeout=60)
        print("ListEpisodes", sub_id, r.status_code, flush=True)
        r.raise_for_status()
        payload = r.json()
        out = ROOT / "experiments" / f"episodes_sub_{sub_id}_majkel1337.json"
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
        picked = public[:4]
        print("PICKED", [e["id"] for e in picked], flush=True)

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
            time.sleep(0.35)

        api_path = ROOT / "experiments/20260911b_public_leaderboard_api.json"
        existing = {}
        if api_path.exists():
            existing = json.loads(api_path.read_text(encoding="utf-8"))
        existing["live_getleaderboard_top20"] = live_rows[:20]
        existing["picked"] = {
            "team": TEAM,
            "teamId": TEAM_ID,
            "submissionId": sub_id,
            "csv_rank": 1,
            "public_score": current.public_score,
            "scoring_sub_id": int(by_score.id),
            "scoring_sub_score": by_score.public_score,
            "dateSubmitted": str(current.date_submitted),
            "picked_ids": [int(e["id"]) for e in picked],
        }
        api_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        print("UPDATED", api_path, flush=True)


if __name__ == "__main__":
    main()
