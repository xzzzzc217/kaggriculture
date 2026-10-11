"""Static hunt scan for 20260913c. No cell exec. No re-extract of rejected kernels."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260913c"
PREV = ROOT / "artifacts/public_sources/_hunt_20260913b"


def main() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    prev = sorted(p.relative_to(PREV).as_posix() for p in PREV.rglob("*") if p.is_file())
    now = sorted(p.relative_to(DIR).as_posix() for p in DIR.rglob("*") if p.is_file())
    print("prev_hunt_files", prev)
    print("this_hunt_files", now)
    print("new_files_vs_13b", sorted(set(now) - set(prev)))
    root = ROOT / "main.py"
    print("root_main_sha256", hashlib.sha256(root.read_bytes()).hexdigest())
    nbs = list(DIR.rglob("*.ipynb"))
    print("notebooks", [p.as_posix() for p in nbs])
    six = DIR / "xuantianfengwu__kaggriculture-timed-six-cow" / "submission.py"
    if six.exists():
        print("timed_six_cow_writefile_sha256", hashlib.sha256(six.read_bytes()).hexdigest())
    prv = DIR / "prvsiyan__kaggriculture-market-ledger-seasonal-counterplay"
    for py in sorted(prv.glob("*.py")) if prv.exists() else []:
        print(py.name, "sha256", hashlib.sha256(py.read_bytes()).hexdigest(), "bytes", py.stat().st_size)


if __name__ == "__main__":
    main()
