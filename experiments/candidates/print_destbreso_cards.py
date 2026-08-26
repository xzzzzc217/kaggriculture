"""Print destbreso markdown cards without executing notebook code."""

from __future__ import annotations

import json
from pathlib import Path

NB = (
    Path(__file__).resolve().parents[2]
    / "artifacts/public_sources/_hunt_20260824b/a-week-four-x-ray-of-the-top-twelve.ipynb"
)


def main() -> None:
    notebook = json.loads(NB.read_text(encoding="utf-8"))
    for index in (13, 16, 20, 24, 50, 51):
        cell = notebook["cells"][index]
        source = cell.get("source") or ""
        if isinstance(source, list):
            source = "".join(source)
        print("=" * 20, "cell", index, "=" * 20)
        print(source)


if __name__ == "__main__":
    main()
