"""Pick cut 16 newest-12 PUBLIC ids disjoint from 20260911b rolling set."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV = {
    107839952,
    107839705,
    107828353,
    107825481,
    107821475,
    107814299,
    107813885,
    107804995,
    107804802,
    107802193,
    107795450,
    107789318,
}
SID = 56151152


def main() -> None:
    payload = json.loads((ROOT / f"experiments/episodes_{SID}.json").read_text(encoding="utf-8"))
    eps = payload.get("episodes") or []
    public = [
        e
        for e in eps
        if e.get("state") == "COMPLETED" and e.get("type") == "EPISODE_TYPE_PUBLIC"
    ]
    public.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    w = t = l = 0
    margins = []
    for e in public:
        agents = e.get("agents") or []
        ours = next((a for a in agents if a.get("submissionId") == SID), None)
        opp = next((a for a in agents if a.get("submissionId") != SID), None)
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
    print(
        "n_eps",
        len(eps),
        "public",
        len(public),
        "WTL",
        w,
        t,
        l,
        "mean",
        (sum(margins) / len(margins) if margins else None),
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
    print("PICKED", ids)
    print("disjoint", set(ids).isdisjoint(PREV), "n", len(ids))
    for e in picked:
        agents = e.get("agents") or []
        ours = next((a for a in agents if a.get("submissionId") == SID), None)
        opp = next((a for a in agents if a.get("submissionId") != SID), None)
        print(
            e["id"],
            e.get("createTime"),
            "ours",
            ours.get("reward") if ours else None,
            "opp_r",
            opp.get("reward") if opp else None,
        )


if __name__ == "__main__":
    main()
