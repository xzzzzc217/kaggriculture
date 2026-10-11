"""Download cut 16 newest-12 public replays (disjoint from 20260912 ids)."""

from __future__ import annotations

import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "artifacts/kaggle_runs/cut16_20260912b"
URL = "https://www.kaggleusercontent.com/episodes/{id}.json"
IDS = [
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
    108124312,
]


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = "kaggriculture-local-audit"
    for eid in IDS:
        path = DEST / f"episode-{eid}-replay.json"
        if path.exists() and path.stat().st_size > 1000:
            print("have", eid, path.stat().st_size, flush=True)
            continue
        r = session.get(URL.format(id=eid), timeout=180)
        print(eid, r.status_code, len(r.content), flush=True)
        r.raise_for_status()
        path.write_bytes(r.content)
        time.sleep(0.3)
    print("done", DEST)


if __name__ == "__main__":
    main()
