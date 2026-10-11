"""Download selected episode JSON from the public CDN."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
URL = "https://www.kaggleusercontent.com/episodes/{id}.json"

IDS = [int(x) for x in sys.argv[1:]]
if not IDS:
    IDS = [
        102114403,
        102085185,
        102007365,
        101726002,
        101687850,
        101676670,
        101663251,
        101772974,
        101658778,
        101703559,
        102083141,
        101864457,
        101909253,
        102058617,
        101940431,
        101681235,
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
        time.sleep(0.6)
    print("done", DEST)


if __name__ == "__main__":
    main()
