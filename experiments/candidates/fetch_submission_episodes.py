"""List public episodes for a submission via Kaggle EpisodeService."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"


def main() -> None:
    sub_id = int(sys.argv[1]) if len(sys.argv) > 1 else 55840543
    session = requests.Session()
    session.headers["User-Agent"] = "kaggriculture-local-audit"
    r = session.post(LIST_URL, json={"submissionId": sub_id}, timeout=60)
    print("status", r.status_code)
    r.raise_for_status()
    payload = r.json()
    out = Path("experiments") / f"episodes_{sub_id}.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    episodes = payload.get("episodes") or payload.get("result") or []
    if isinstance(payload, dict):
        print("keys", list(payload.keys())[:20])
    print("n", len(episodes) if isinstance(episodes, list) else type(episodes))
    if isinstance(episodes, list) and episodes:
        print("sample_keys", list(episodes[0].keys()) if isinstance(episodes[0], dict) else type(episodes[0]))
        print(json.dumps(episodes[0], indent=2)[:1500])
    print("WROTE", out)


if __name__ == "__main__":
    main()
