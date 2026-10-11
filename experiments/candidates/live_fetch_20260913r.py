"""Fetch ListEpisodes for cut16/shopbag into live folder. No overwrite of 13q artifacts."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "artifacts/kaggle_runs/lb_20260913r_live"
ZPATH = LIVE / "kaggriculture.zip"
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
SID = 56151152
SHOP = 56151155
PREV_13Q = {
    108534412,
    108504670,
    108472548,
    108461768,
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
    108371627,
    108369265,
    108366745,
}


def last_updated(payload: dict, sub_id: int) -> tuple[float | None, int | None, str | None]:
    eps = [
        e
        for e in (payload.get("episodes") or [])
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
    ]
    eps.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    for episode in eps:
        for agent in episode.get("agents") or []:
            if int(agent.get("submissionId") or 0) == sub_id and agent.get("updatedScore") is not None:
                return float(agent["updatedScore"]), int(episode["id"]), episode.get("createTime")
    return None, None, None


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
    csv_path = LIVE / name.replace(":", "-")
    csv_path.write_text(data, encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(data)))
    print("csv", name, "n_teams", len(rows), flush=True)
    print("--- TOP 12 ---", flush=True)
    for i, r in enumerate(rows[:12], 1):
        print(
            f"{i:2d} {float(r['Score']):8.1f} {r['TeamName']!r:30s} "
            f"teamId={r['TeamId']} last={r['LastSubmissionDate']}",
            flush=True,
        )
    print("gold21", rows[20]["TeamName"], rows[20]["Score"], flush=True)
    print("rank10", rows[9]["TeamName"], rows[9]["Score"], flush=True)
    for i, r in enumerate(rows, 1):
        if "heralces" in (r["TeamName"] or "").lower():
            print("heralces", i, r["Score"], r["TeamName"], r["TeamId"], flush=True)
            break

    sess = requests.Session()
    sess.headers["User-Agent"] = "kaggriculture-local-audit"
    summary = {}
    for sid, label in ((SID, "cut16"), (SHOP, "shopbag")):
        rr = sess.post(LIST_URL, json={"submissionId": sid}, timeout=60)
        print("ListEpisodes", label, sid, rr.status_code, flush=True)
        rr.raise_for_status()
        payload = rr.json()
        (LIVE / f"episodes_{sid}.json").write_text(json.dumps(payload) + "\n", encoding="utf-8")
        n_pub, wtl, mean = public_wtl(payload, sid)
        score, eid, ctime = last_updated(payload, sid)
        public = [
            e
            for e in (payload.get("episodes") or [])
            if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
        ]
        public.sort(key=lambda e: e.get("createTime") or "", reverse=True)
        newest12 = [int(e["id"]) for e in public[:12]]
        picked = []
        for e in public:
            eid2 = int(e["id"])
            if eid2 in PREV_13Q:
                continue
            picked.append(eid2)
            if len(picked) == 12:
                break
        print(label, "n_public", n_pub, "WTL", wtl, "mean", mean, "updated", score, "ep", eid, ctime, flush=True)
        print(label, "newest12", newest12, flush=True)
        print(label, "newest12_equals_13q", newest12 == list(sorted(PREV_13Q, reverse=True)), flush=True)
        print(
            label,
            "picked_disjoint_13q",
            picked,
            "n",
            len(picked),
            "disjoint",
            set(picked).isdisjoint(PREV_13Q),
            flush=True,
        )
        summary[label] = {
            "n_public": n_pub,
            "wtl": wtl,
            "mean": mean,
            "updated": score,
            "newest_ep": eid,
            "newest12": newest12,
            "picked": picked,
        }
        if label == "cut16":
            n_val = sum(
                1
                for e in (payload.get("episodes") or [])
                if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_VALIDATION"
            )
            print("n_validation", n_val, flush=True)
            for e in public[:20]:
                agents = e.get("agents") or []
                ours = next((a for a in agents if a.get("submissionId") == sid), None)
                opp = next((a for a in agents if a.get("submissionId") != sid), None)
                r = ours.get("reward") if ours else None
                o = opp.get("reward") if opp else None
                m = (r - o) if r is not None and o is not None else None
                flag = "W" if m is not None and m > 0 else ("T" if m == 0 else "L")
                print(
                    " ",
                    e["id"],
                    flag,
                    m,
                    e.get("createTime"),
                    (opp or {}).get("teamName"),
                    "IN13Q" if int(e["id"]) in PREV_13Q else "NEW",
                    flush=True,
                )
    (LIVE / "fetch_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("WROTE", LIVE / "fetch_summary.json", flush=True)


if __name__ == "__main__":
    main()
