"""Majkel1337 scoring/newest sub, EpisodeService + 4 new replays (20260913u)."""

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
DEST = ROOT / "artifacts/kaggle_runs/top_20260913u"
SKIP_IDS = {
    108584052,
    108577054,
    108076337,
    108071295,
    108570750,
    108563756,
    108557488,
    108081303,
    108550584,
    108544343,
    108092293,
    108087066,
    108538106,
    108531216,
    108525049,
    108098091,
    108518840,
    108512739,
    108109289,
    108104083,
    108506598,
    108500554,
    108121150,
    108115160,
    108494524,
    108488494,
    108483149,
    108453811,
    108477110,
    108470978,
    108464894,
    108459064,
    108447904,
    108441866,
    108436524,
    108127188,
    108430587,
    108425363,
    108419608,
    108133157,
    108414382,
    108409365,
    108404344,
    108139186,
    108399446,
    108395112,
    108390115,
    108372810,
    108385318,
    108381189,
    108377045,
    108377042,
    108368104,
    108363848,
    108359085,
    108145205,
    108354767,
    108349935,
    108349757,
    108345542,
    108340909,
    108336738,
    108332509,
    108327803,
    108323526,
    108318789,
    108314478,
    108151282,
    108309734,
    108305451,
    108300532,
    108158107,
    108295517,
    108290604,
    108285658,
    108164328,
    108280666,
    108275644,
    108270468,
    108171145,
    108264640,
    108259398,
    108183191,
    108177210,
    108253590,
    108248350,
    108242413,
    108189222,
    108236417,
    108230381,
    108224320,
    108195254,
    108218308,
    108212349,
    108207190,
    108201162,
    108005681,
    108001570,
    107997338,
    107992612,
    107846772,
    107840808,
    107840804,
    107835003,
    107756968,
    107751894,
    107746036,
    107740777,
    107582281,
    107581290,
    107580344,
    107579345,
    107493475,
    107487687,
    107482596,
    107481864,
    106976067,
    106976069,
    106976065,
    106958424,
    105440807,
    105437334,
    105433863,
    105433860,
    105398564,
    105398563,
    105395068,
    105391580,
    105395079,
    105391598,
    105388041,
    105384084,
    105352975,
    105352101,
    105352096,
    105348549,
    105352143,
    105352100,
    105352099,
    105348550,
    105351728,
    105349460,
    105345918,
    105345853,
    105352097,
    105348551,
    105345024,
    105341443,
    105353065,
    105351792,
    105350403,
    105349475,
}


def last_updated_score(payload: dict, team_id: int = TEAM_ID) -> float | None:
    eps = [
        e
        for e in (payload.get("episodes") or [])
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
    ]
    eps.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    for episode in eps:
        for agent in episode.get("agents") or []:
            if int(agent.get("teamId") or 0) == team_id and agent.get("updatedScore") is not None:
                return float(agent["updatedScore"])
    return None


def public_completed(payload: dict) -> list[dict]:
    eps = payload.get("episodes") or []
    public = [
        e
        for e in eps
        if e.get("state") == "COMPLETED"
        and e.get("type") == "EPISODE_TYPE_PUBLIC"
        and int(e.get("id") or 0) not in SKIP_IDS
    ]
    public.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    return public


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

        target_score = None
        if live_rows and live_rows[0]["teamName"] == TEAM:
            try:
                target_score = float(live_rows[0]["score"])
            except (TypeError, ValueError):
                target_score = None
        if target_score is None:
            target_score = 3249.6
        print("TARGET_SCORE", target_score, flush=True)

        sub_req = ApiListTeamPublicSubmissionsRequest()
        sub_req.team_id = TEAM_ID
        subs_resp = kaggle.competitions.competition_api_client.list_team_public_submissions(sub_req)
        subs = list(subs_resp.submissions or [])
        print("n_subs", len(subs), flush=True)
        for s in subs:
            print("sub", s.id, s.public_score, s.date_submitted, flush=True)
        if not subs:
            raise SystemExit("no public submissions for Majkel1337")

        by_score = max(subs, key=lambda x: float(x.public_score or 0))
        current = max(subs, key=lambda x: int(x.id or 0))
        print("CURRENT_SUB", current.id, current.public_score, current.date_submitted, flush=True)
        print("MAX_PUBLIC_SCORE_SUB", by_score.id, by_score.public_score, by_score.date_submitted, flush=True)

        sess = requests.Session()
        sess.headers["User-Agent"] = "kaggriculture-local-audit"

        listed = {}
        for s in (by_score, current):
            sub_id = int(s.id)
            if sub_id in listed:
                continue
            r = sess.post(LIST_URL, json={"submissionId": sub_id}, timeout=60)
            print("ListEpisodes", sub_id, r.status_code, flush=True)
            r.raise_for_status()
            payload = r.json()
            out = ROOT / "experiments" / f"episodes_sub_{sub_id}_majkel1337.json"
            out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            last = last_updated_score(payload)
            n_pub = len(
                [
                    e
                    for e in (payload.get("episodes") or [])
                    if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
                ]
            )
            print("WROTE", out, "n", len(payload.get("episodes") or []), "n_public", n_pub, "last_updated", last, flush=True)
            listed[sub_id] = {"payload": payload, "last": last, "sub": s}

        scoring_id = None
        for sub_id, rec in listed.items():
            last = rec["last"]
            pub = float(rec["sub"].public_score or 0)
            if last is not None and abs(last - target_score) < 1.0:
                scoring_id = sub_id
                print("MATCH_LAST_UPDATED", sub_id, last, flush=True)
            elif abs(pub - target_score) < 1.0:
                scoring_id = sub_id
                print("MATCH_PUBLIC_SCORE", sub_id, pub, flush=True)
        if scoring_id is None:
            closest = min(
                listed.items(),
                key=lambda kv: min(
                    abs((kv[1]["last"] or 0) - target_score),
                    abs(float(kv[1]["sub"].public_score or 0) - target_score),
                ),
            )
            scoring_id = closest[0]
            print(
                "NO_EXACT_TARGET; using closest",
                scoring_id,
                "last",
                closest[1]["last"],
                "public",
                closest[1]["sub"].public_score,
                flush=True,
            )

        payload = listed[scoring_id]["payload"]
        scoring_sub = listed[scoring_id]["sub"]
        public = public_completed(payload)
        print("n_public_completed_new", len(public), flush=True)
        picked = public[:4]
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
            time.sleep(0.35)

        api_path = ROOT / "experiments/20260913u_public_leaderboard_api.json"
        existing = {}
        if api_path.exists():
            existing = json.loads(api_path.read_text(encoding="utf-8"))
        existing["live_getleaderboard_top20"] = live_rows[:20]
        existing["picked"] = {
            "team": TEAM,
            "teamId": TEAM_ID,
            "submissionId": int(scoring_id),
            "csv_rank": 1,
            "public_score": scoring_sub.public_score,
            "scoring_sub_id": int(scoring_id),
            "scoring_sub_score": scoring_sub.public_score,
            "current_sub_id": int(current.id),
            "current_sub_public_score": current.public_score,
            "max_score_sub_id": int(by_score.id),
            "max_score_sub_score": by_score.public_score,
            "last_updated_score": listed[scoring_id]["last"],
            "dateSubmitted": str(scoring_sub.date_submitted),
            "picked_ids": [int(e["id"]) for e in picked],
        }
        api_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        print("UPDATED", api_path, flush=True)


if __name__ == "__main__":
    main()
