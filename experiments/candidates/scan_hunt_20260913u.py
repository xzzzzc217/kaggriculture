"""Static hunt scan for 20260913u. No cell exec. No re-extract of rejected kernels."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260913u"
PREV = ROOT / "artifacts/public_sources/_hunt_20260913t"


def main() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    prev = sorted(p.relative_to(PREV).as_posix() for p in PREV.rglob("*") if p.is_file()) if PREV.exists() else []
    now = sorted(p.relative_to(DIR).as_posix() for p in DIR.rglob("*") if p.is_file())
    print("prev_hunt_files", prev)
    print("this_hunt_files", now)
    print("new_files_vs_13n", sorted(set(now) - set(prev)))
    root = ROOT / "main.py"
    print("root_main_sha256", hashlib.sha256(root.read_bytes()).hexdigest())
    print("notebooks", [p.relative_to(DIR).as_posix() for p in DIR.rglob("*.ipynb")])


if __name__ == "__main__":
    main()
