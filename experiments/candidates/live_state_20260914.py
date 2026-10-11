"""Parse LB zip, shopbag ListEpisodes, pick cut16 newest-12 disjoint from 13l."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
ZPATH = ROOT / "artifacts/kaggle_runs/lb_20260914/kaggriculture.zip"
OUT_API = ROOT / "experiments/20260914_public_leaderboard_api.json"
SID = 56151152
SHOP = 56151155
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
PREV = {
    108608562,
    108604498,
    108586169,
    108550653,
    108545775,
    108520439,
    108509931,
    108489181,
    108484081,
    108445221,
    108441448,
    108441305,
}
PRIOR = [
    ROOT / "experiments/20260904_top10_games.json",
    ROOT / "experiments/20260905_top10_games.json",
    ROOT / "experiments/20260906_top10_games.json",
    ROOT / "experiments/20260909_top10_games.json",
    ROOT / "experiments/20260910_top10_games.json",
    ROOT / "experiments/20260911_top10_games.json",
    ROOT / "experiments/20260911b_top10_games.json",
    ROOT / "experiments/20260912_top10_games.json",
    ROOT / "experiments/20260912b_top10_games.json",
    ROOT / "experiments/20260912c_top10_games.json",
    ROOT / "experiments/20260912d_top10_games.json",
    ROOT / "experiments/20260912e_top10_games.json",
    ROOT / "experiments/20260913_top10_games.json",
    ROOT / "experiments/20260913b_top10_games.json",
    ROOT / "experiments/20260913c_top10_games.json",
    ROOT / "experiments/20260913d_top10_games.json",
    ROOT / "experiments/20260913e_top10_games.json",
    ROOT / "experiments/20260913f_top10_games.json",
    ROOT / "experiments/20260913g_top10_games.json",
    ROOT / "experiments/20260913h_top10_games.json",
    ROOT / "experiments/20260913i_top10_games.json",
    ROOT / "experiments/20260913j_top10_games.json",
    ROOT / "experiments/20260913k_top10_games.json",
    ROOT / "experiments/20260913l_top10_games.json",
    ROOT / "experiments/20260913m_top10_games.json",
    ROOT / "experiments/20260913n_top10_games.json",
    ROOT / "experiments/20260913o_top10_games.json",
    ROOT / "experiments/20260913p_top10_games.json",
    ROOT / "experiments/20260913q_top10_games.json",
    ROOT / "experiments/20260913v_top10_games.json",
    ROOT / "experiments/20260913u_top10_games.json",
    ROOT / "experiments/20260913t_top10_games.json",
    ROOT / "experiments/20260913s_top10_games.json",
    ROOT / "experiments/20260913r_top10_games.json",
]


def last_updated(payload: dict, sub_id: int) -> float | None:
    eps = [
        e
        for e in (payload.get("episodes") or [])
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
    ]
    eps.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    for episode in eps:
        for agent in episode.get("agents") or []:
            if int(agent.get("submissionId") or 0) == sub_id and agent.get("updatedScore") is not None:
                return float(agent["updatedScore"])
    return None


def public_wtl(payload: dict, sub_id: int) -> tuple[int, list[int], float | None]:
    public = [
        e
        for e in (payload.get("episodes") or [])
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
    ]
    w = t = l = 0
    margins: list[float] = []
    for e in public:
        agents = e.get("agents") or []
        ours = next((a for a in agents if a.get("submissionId") == sub_id), None)
        opp = next((a for a in agents if a.get("submissionId") != sub_id), None)
        if ours is None or opp is None:
            continue
        r, o = ours.get("reward"), opp.get("reward")
        if r is None or o is None:
            continue
        m = r - o
        margins.append(m)
        if m > 0:
            w += 1
        elif m == 0:
            t += 1
        else:
            l += 1
    mean = round(sum(margins) / len(margins), 1) if margins else None
    return len(public), [w, t, l], mean


def main() -> None:
    with zipfile.ZipFile(ZPATH) as z:
        print("members", z.namelist(), flush=True)
        name = z.namelist()[0]
        data = z.read(name).decode("utf-8")
    csv_path = ZPATH.parent / name.replace(":", "-")
    csv_path.write_text(data, encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    print("csv", name, "n_teams", len(rows), flush=True)
    measured: set[str] = set()
    for path in PRIOR:
        if not path.exists():
            continue
        for row in json.loads(path.read_text(encoding="utf-8")):
            measured.add(row["team"])
    pick = None
    csv_top = []
    print("--- TOP 15 ---", flush=True)
    for i, r in enumerate(rows[:15], 1):
        miss = r["TeamName"] not in measured
        print(
            f"{i:2d} {float(r['Score']):8.1f} {r['TeamName']!r:30s} "
            f"teamId={r['TeamId']} last={r['LastSubmissionDate']} "
            f"{'MISSING' if miss else 'measured'}",
            flush=True,
        )
        csv_top.append(
            {
                "rank": i,
                "teamId": int(r["TeamId"]),
                "teamName": r["TeamName"],
                "score": r["Score"],
                "lastSubmissionDate": r["LastSubmissionDate"],
                "missing_from_04_13l": miss,
            }
        )
        if pick is None and miss:
            pick = (i, r)
    her = None
    her_rank = None
    for i, r in enumerate(rows, 1):
        if "heralces" in (r["TeamName"] or "").lower():
            her = r
            her_rank = i
            print("heralces", i, dict(r), flush=True)
            break
    gold21 = rows[20]
    print("gold21", gold21["TeamName"], gold21["Score"], flush=True)
    if pick:
        print("PICK", pick[0], dict(pick[1]), flush=True)
    else:
        print("PICK none-missing; re-measure rank1", rows[0]["TeamName"], flush=True)

    payload = json.loads((ROOT / f"experiments/episodes_{SID}.json").read_text(encoding="utf-8"))
    n_pub, wtl, mean = public_wtl(payload, SID)
    cut16_score = last_updated(payload, SID)
    public = [
        e
        for e in (payload.get("episodes") or [])
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
    ]
    public.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    print("cut16 n_public", n_pub, "WTL", wtl, "mean", mean, "updated", cut16_score, flush=True)
    n_val = sum(
        1
        for e in (payload.get("episodes") or [])
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_VALIDATION"
    )
    print(
        "n_validation",
        n_val,
        "newest",
        public[0]["id"] if public else None,
        public[0].get("createTime") if public else None,
        flush=True,
    )
    picked = []
    for e in public:
        eid = int(e["id"])
        if eid in PREV:
            continue
        picked.append(e)
        if len(picked) == 12:
            break
    ids = [int(e["id"]) for e in picked]
    print("PICKED", ids, "disjoint", set(ids).isdisjoint(PREV), flush=True)
    pw = pt = pl = 0
    pm: list[float] = []
    for e in picked:
        agents = e.get("agents") or []
        ours = next((a for a in agents if a.get("submissionId") == SID), None)
        opp = next((a for a in agents if a.get("submissionId") != SID), None)
        r = ours.get("reward") if ours else None
        o = opp.get("reward") if opp else None
        m = (r - o) if r is not None and o is not None else None
        if m is not None:
            pm.append(m)
            if m > 0:
                pw += 1
            elif m == 0:
                pt += 1
            else:
                pl += 1
        flag = "W" if m is not None and m > 0 else ("T" if m == 0 else "L")
        opp_name = None
        if opp:
            opp_name = opp.get("teamName") or opp.get("submissionId")
        print(e["id"], flag, m, e.get("createTime"), opp_name, flush=True)
    print("picked WTL", pw, pt, pl, "mean", round(sum(pm) / len(pm), 1) if pm else None, flush=True)

    sess = requests.Session()
    sess.headers["User-Agent"] = "kaggriculture-local-audit"
    rr = sess.post(LIST_URL, json={"submissionId": SHOP}, timeout=60)
    print("ListEpisodes_shopbag", rr.status_code, len(rr.content), flush=True)
    rr.raise_for_status()
    shop_payload = rr.json()
    (ROOT / f"experiments/episodes_{SHOP}.json").write_text(
        json.dumps(shop_payload, indent=2) + "\n", encoding="utf-8"
    )
    shop_score = last_updated(shop_payload, SHOP)
    n_shop, shop_wtl, shop_mean = public_wtl(shop_payload, SHOP)
    print("shopbag n_public", n_shop, "WTL", shop_wtl, "mean", shop_mean, "updated", shop_score, flush=True)

    payload_out = {
        "n": len(rows),
        "csv": str(csv_path.as_posix()),
        "csv_time": name.split("kaggriculture-publicleaderboard-")[-1].replace(".csv", ""),
        "csv_top15": csv_top,
        "picked": None
        if pick is None
        else {
            "team": pick[1]["TeamName"],
            "teamId": int(pick[1]["TeamId"]),
            "csv_rank": pick[0],
            "csv_score": pick[1]["Score"],
            "lastSubmissionDate": pick[1]["LastSubmissionDate"],
        },
        "heralces_csv": {
            "rank": her_rank,
            "teamId": int(her["TeamId"]) if her else None,
            "score": her["Score"] if her else None,
            "lastSubmissionDate": her["LastSubmissionDate"] if her else None,
        },
        "gold21_csv": {"rank": 21, "team": gold21["TeamName"], "score": gold21["Score"]},
        "rank1": {
            "team": rows[0]["TeamName"],
            "score": rows[0]["Score"],
            "teamId": int(rows[0]["TeamId"]),
        },
        "rank10": {
            "team": rows[9]["TeamName"],
            "score": rows[9]["Score"],
            "teamId": int(rows[9]["TeamId"]),
        },
        "cut16": {
            "submissionId": SID,
            "n_public": n_pub,
            "n_validation": n_val,
            "wtl": wtl,
            "mean_margin": mean,
            "updatedScore": cut16_score,
            "rolling_ids": ids,
            "rolling_wtl": [pw, pt, pl],
            "rolling_mean": round(sum(pm) / len(pm), 1) if pm else None,
        },
        "shopbag": {
            "submissionId": SHOP,
            "n_public": n_shop,
            "wtl": shop_wtl,
            "mean_margin": shop_mean,
            "updatedScore": shop_score,
        },
        "submissions_api": {
            "cut16": {"id": SID, "status": "COMPLETE", "publicScore": 1654.7},
            "shopbag": {"id": SHOP, "status": "COMPLETE", "publicScore": 1309.4},
        },
    }
    OUT_API.write_text(json.dumps(payload_out, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT_API, flush=True)


if __name__ == "__main__":
    main()
