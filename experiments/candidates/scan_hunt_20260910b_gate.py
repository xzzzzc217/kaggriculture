"""Static later-block scan of 2026-09-10b gate hunt notebooks. No cell exec."""

from __future__ import annotations

import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910b_gate"
KEYS = [
    "%%writefile",
    "writefile",
    "agent.so",
    "ctypes",
    "CDLL",
    ".so",
    "reselect",
    "DECISIONS",
    "ROUTES",
    "later",
    "216",
    "226",
    "241",
    "360",
    "385",
    "433",
    "144",
    "648",
    "712",
    "BALANCED",
    "BUY_ANIMAL",
    "def agent",
    "gzip",
    "base64",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    paths = sorted(DIR.rglob("*.ipynb")) + sorted(DIR.rglob("*.py"))
    for path in paths:
        if path.suffix == ".py" and path.name.startswith("scan_"):
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        low = text.lower()
        writes = re.findall(r"%%writefile\s+(\S+)", text)
        print("=" * 72)
        print(path.parent.name, path.name, "bytes", len(raw), "writefiles", writes)
        if path.suffix == ".ipynb":
            notebook = json.loads(raw.decode("utf-8"))
            cells = notebook.get("cells") or []
            print("cells", len(cells), "FLAGS", [k for k in KEYS if k.lower() in low])
            for index, cell in enumerate(cells[:12]):
                src = cell_source(cell)
                first = [line for line in src.splitlines() if line.strip()][:7]
                if not first:
                    continue
                print(f"-- cell {index} {cell.get('cell_type')} {len(src)} --")
                for line in first:
                    print(line[:180])
            for index, cell in enumerate(cells):
                src = cell_source(cell)
                if "%%writefile" not in src and "EXPECTED_SOURCE_SHA256" not in src and "def agent(" not in src[:4000]:
                    continue
                interesting = []
                for line in src.splitlines():
                    if re.search(
                        r"216|226|241|360|385|433|648|712|reselect|YARN|DECISIONS|ctypes|CDLL|agent\.so|step ==|step>=|t ==",
                        line,
                    ):
                        interesting.append(line.strip()[:160])
                        if len(interesting) >= 12:
                            break
                if interesting:
                    print(f"  interesting cell {index}:")
                    for line in interesting:
                        print("   ", line)
        else:
            print("FLAGS", [k for k in KEYS if k.lower() in low])
            first = [line for line in text.splitlines() if line.strip()][:10]
            for line in first:
                print(line[:180])


if __name__ == "__main__":
    main()
