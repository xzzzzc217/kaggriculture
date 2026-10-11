"""Headers from a hunt directory. No cell exec."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    directory = Path(sys.argv[1])
    paths = sorted(directory.glob("*.ipynb")) + sorted(directory.glob("**/*.ipynb"))
    seen = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        print("=" * 70)
        print(path.name, "bytes", len(raw), "cells", len(notebook.get("cells", [])))
        for index, cell in enumerate(notebook.get("cells", [])[:8]):
            source = cell_source(cell)
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
            for line in source.strip().splitlines()[:14]:
                print(line[:220])
        text = raw.decode("utf-8", errors="ignore")
        print(
            "writefile",
            "%%writefile" in text,
            "b85",
            "b85decode" in text,
            "PAYLOAD",
            "PAYLOAD" in text,
            "ARCHIVE",
            "ARCHIVE_B64" in text or "ARCHIVE" in text,
        )
        shas = re.findall(r"[a-f0-9]{64}", text.lower())
        for digest in list(dict.fromkeys(shas))[:8]:
            print(" sha", digest)


if __name__ == "__main__":
    main()
