"""Summarize shopbag ListEpisodes metadata: W/T/L and score path."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
payload = json.loads((ROOT / "experiments/episodes_55840543.json").read_text(encoding="utf-8"))
episodes = payload["episodes"]
teams = {t["id"]: t.get("teamName") or t.get("name") for t in payload.get("teams") or []}
# teams might be list of dicts
if payload.get("teams") and isinstance(payload["teams"][0], dict):
    print("team keys", list(payload["teams"][0].keys()))
    print("n teams", len(payload["teams"]))

subs = payload.get("submissions") or []
print("n subs", len(subs))
if subs:
    print("sub keys", list(subs[0].keys()))
    for s in subs[:8]:
        print(" sub", {k: s.get(k) for k in list(s)[:8]})

OUR = 55840543
rows = []
for ep in episodes:
    if ep.get("state") != "COMPLETED":
        continue
    if ep.get("type") != "EPISODE_TYPE_PUBLIC":
        continue
    agents = ep.get("agents") or []
    ours = next((a for a in agents if a.get("submissionId") == OUR), None)
    opp = next((a for a in agents if a.get("submissionId") != OUR), None)
    if ours is None or opp is None:
        continue
    our_r = float(ours.get("reward") or 0)
    opp_r = float(opp.get("reward") or 0)
    rows.append(
        {
            "id": ep["id"],
            "end": ep.get("endTime"),
            "our_reward": our_r,
            "opp_reward": opp_r,
            "margin": our_r - opp_r,
            "win": our_r > opp_r,
            "tie": our_r == opp_r,
            "seat": 0 if agents[0].get("submissionId") == OUR else 1,
            "opp_sub": opp.get("submissionId"),
            "opp_team": opp.get("teamId"),
            "score_before": ours.get("initialScore"),
            "score_after": ours.get("updatedScore"),
        }
    )

rows.sort(key=lambda r: r["end"] or "", reverse=True)
w = sum(r["win"] for r in rows)
t = sum(r["tie"] for r in rows)
l = len(rows) - w - t
print("public COMPLETE", len(rows), "WTL", w, t, l, "mean_margin", sum(r["margin"] for r in rows) / len(rows) if rows else None)
losses = [r for r in rows if not r["win"] and not r["tie"]]
ties = [r for r in rows if r["tie"]]
print("n_losses", len(losses), "n_ties", len(ties))
print("latest 15:")
for r in rows[:15]:
    mark = "W" if r["win"] else ("T" if r["tie"] else "L")
    print(mark, r["id"], r["margin"], "seat", r["seat"], "opp_sub", r["opp_sub"], r["end"])
print("all losses:")
for r in losses:
    print("L", r["id"], r["margin"], "seat", r["seat"], "opp_team", r["opp_team"], "opp_sub", r["opp_sub"], r["end"])

out = {"n": len(rows), "wtl": [w, t, l], "rows": rows, "losses": losses}
(ROOT / "experiments/20260829_shopbag_episodes_meta.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("WROTE meta")
