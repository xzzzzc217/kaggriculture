"""Pick cut 16 newest-12 PUBLIC ids disjoint from 20260912d rolling set."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV = {
    108243488,
    108208866,
    108204278,
    108191120,
    108175982,
    108172639,
    108166009,
    108162165,
    108161412,
    108153141,
    108139022,
    108138037,
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
    val = [
        e
        for e in eps
        if e.get("state") == "COMPLETED" and e.get("type") != "EPISODE_TYPE_PUBLIC"
    ]
    print(
        "n_eps",
        len(eps),
        "public",
        len(public),
        "other",
        len(val),
        "WTL",
        w,
        t,
        l,
        "mean",
        (round(sum(margins) / len(margins), 1) if margins else None),
    )
    newest = public[0] if public else None
    if newest:
        ours = next((a for a in newest.get("agents") or [] if a.get("submissionId") == SID), None)
        print(
            "newest_public",
            newest.get("id"),
            newest.get("createTime"),
            "updatedScore",
            ours.get("updatedScore") if ours else None,
            "initialScore",
            ours.get("initialScore") if ours else None,
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
    print("disjoint_0912d", set(ids).isdisjoint(PREV), "n", len(ids))
    overlap = set(ids) & PREV
    print("overlap_0912d", sorted(overlap))
    for e in picked:
        agents = e.get("agents") or []
        ours = next((a for a in agents if a.get("submissionId") == SID), None)
        opp = next((a for a in agents if a.get("submissionId") != SID), None)
        r = ours.get("reward") if ours else None
        o = opp.get("reward") if opp else None
        m = (r - o) if r is not None and o is not None else None
        flag = "W" if m is not None and m > 0 else ("T" if m == 0 else "L")
        print(
            e["id"],
            flag,
            m,
            e.get("createTime"),
            "ours",
            r,
            "opp",
            o,
        )


if __name__ == "__main__":
    main()
