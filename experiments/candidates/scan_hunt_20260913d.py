"""Static hunt scan for 20260913d. No cell exec. No re-extract of rejected kernels."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260913d"
PREV = ROOT / "artifacts/public_sources/_hunt_20260913c"


def main() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    prev = sorted(p.relative_to(PREV).as_posix() for p in PREV.rglob("*") if p.is_file())
    now = sorted(p.relative_to(DIR).as_posix() for p in DIR.rglob("*") if p.is_file())
    print("prev_hunt_files", prev)
    print("this_hunt_files", now)
    print("new_files_vs_13c", sorted(set(now) - set(prev)))
    root = ROOT / "main.py"
    print("root_main_sha256", hashlib.sha256(root.read_bytes()).hexdigest())
    print("no_notebooks_pulled", not any(DIR.rglob("*.ipynb")))


if __name__ == "__main__":
    main()
