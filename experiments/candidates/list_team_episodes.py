"""List public episodes for a team via EpisodeService."""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from pathlib import Path

import requests

LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
ROOT = Path(__file__).resolve().parents[2]
LB_ZIP = ROOT / "artifacts/kaggle_runs/lb_20260831b/kaggriculture.zip"


def team_id(name: str) -> int:
    with zipfile.ZipFile(LB_ZIP) as z:
        data = z.read(z.namelist()[0]).decode("utf-8")
    for row in csv.DictReader(io.StringIO(data)):
        if (row.get("TeamName") or "").lower() == name.lower():
            return int(row["TeamId"])
    raise SystemExit(f"team not found: {name}")


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "A Poor Vul"
    tid = team_id(name)
    print("teamId", tid, name)
    session = requests.Session()
    session.headers["User-Agent"] = "kaggriculture-local-audit"
    r = session.post(LIST_URL, json={"teamId": tid}, timeout=60)
    print("status", r.status_code)
    r.raise_for_status()
    payload = r.json()
    out = ROOT / "experiments" / f"episodes_team_{tid}.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    eps = payload.get("episodes") or []
    subs = payload.get("submissions") or []
    print("n_eps", len(eps), "n_subs", len(subs), "keys", list(payload.keys())[:12])
    if subs:
        s = max(subs, key=lambda x: x.get("id", 0))
        print("newest_sub", {k: s.get(k) for k in ("id", "dateSubmitted", "publicScore", "teamName", "name") if k in s or True})
        print("sub_keys", list(s.keys())[:25])
        print(json.dumps({k: s[k] for k in list(s)[:15]}, indent=2)[:1200])
    print("WROTE", out)


if __name__ == "__main__":
    main()
