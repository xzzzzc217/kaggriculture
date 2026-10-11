"""Download cut 16 newest-12 public replays (disjoint from 20260913n ids)."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "artifacts/kaggle_runs/cut16_20260913o"
PRIOR = [
    ROOT / "artifacts/kaggle_runs/cut16_20260913n",
    ROOT / "artifacts/kaggle_runs/cut16_20260913m",
    ROOT / "artifacts/kaggle_runs/cut16_20260913l",
    ROOT / "artifacts/kaggle_runs/cut16_20260913k",
    ROOT / "artifacts/kaggle_runs/cut16_20260913j",
    ROOT / "artifacts/kaggle_runs/cut16_20260913i",
    ROOT / "artifacts/kaggle_runs/cut16_20260913h",
    ROOT / "artifacts/kaggle_runs/cut16_20260913g",
    ROOT / "artifacts/kaggle_runs/cut16_20260913f",
    ROOT / "artifacts/kaggle_runs/cut16_20260913e",
    ROOT / "artifacts/kaggle_runs/cut16_20260913d",
    ROOT / "artifacts/kaggle_runs/cut16_20260913c",
    ROOT / "artifacts/kaggle_runs/cut16_20260913b",
    ROOT / "artifacts/kaggle_runs/cut16_20260913",
    ROOT / "artifacts/kaggle_runs/cut16_20260912e",
    ROOT / "artifacts/kaggle_runs/cut16_20260912d",
    ROOT / "artifacts/kaggle_runs/cut16_20260912c",
    ROOT / "artifacts/kaggle_runs/cut16_20260912b",
    ROOT / "artifacts/kaggle_runs/cut16_20260912",
]
URL = "https://www.kaggleusercontent.com/episodes/{id}.json"
API = ROOT / "experiments/20260913o_public_leaderboard_api.json"


def main() -> None:
    api = json.loads(API.read_text(encoding="utf-8"))
    ids = list((api.get("cut16") or {}).get("rolling_ids") or [])
    if len(ids) != 12:
        raise SystemExit(f"expected 12 rolling ids, got {ids}")
    DEST.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = "kaggriculture-local-audit"
    for eid in ids:
        path = DEST / f"episode-{eid}-replay.json"
        if path.exists() and path.stat().st_size > 1000:
            print("have", eid, path.stat().st_size, flush=True)
            continue
        copied = False
        for src_dir in PRIOR:
            src = src_dir / f"episode-{eid}-replay.json"
            if src.exists() and src.stat().st_size > 1000:
                shutil.copy2(src, path)
                print("copy", eid, src_dir.name, path.stat().st_size, flush=True)
                copied = True
                break
        if copied:
            continue
        r = session.get(URL.format(id=eid), timeout=180)
        print(eid, r.status_code, len(r.content), flush=True)
        r.raise_for_status()
        path.write_bytes(r.content)
        time.sleep(0.3)
    print("done", DEST)


if __name__ == "__main__":
    main()
