"""Static b85+zlib hash of zhincez plateau agent. No cell exec, no extract to candidates/."""

from __future__ import annotations

import base64
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = (
    ROOT
    / "artifacts/public_sources/_hunt_20260912c"
    / "zhincez__the-base-schedule-is-a-plateau-not-a-lever"
    / "the-base-schedule-is-a-plateau-not-a-lever.ipynb"
)
KNOWN = {
    "v37": "94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c",
    "cut14": "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e",
    "cut15": "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522",
    "cut16": "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d",
    "v38": "a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    nb = json.loads(PATH.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][5])
    marker = 'AGENT_B85 = """'
    start = src.find(marker)
    assert start >= 0
    start += len(marker)
    end = src.find('"""', start)
    blob = src[start:end]
    raw = zlib.decompress(base64.b85decode(blob.strip().encode("ascii")))
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    print("decompressed_sha", sha, "bytes", len(raw))
    print("expected", "07f6c80605271b028b3aebc803180fd8b1bf3162a2d394bb30fe65b8d943d1f5")
    print("match_expected", sha == "07f6c80605271b028b3aebc803180fd8b1bf3162a2d394bb30fe65b8d943d1f5")
    for name, known in KNOWN.items():
        print("eq", name, sha == known)
    keys = [
        "ROUTE_STEP",
        "FINAL_PLAN_STEP",
        "sale_horizon",
        "ADVANCE_START",
        "DECISIONS",
        "PROGRAM",
        "reselect",
        "ctypes",
        "CDLL",
        "agent.so",
        "%%writefile",
        "def agent",
        "step >= 144",
        "step>=144",
        "step >= 72",
        "step>=72",
        "day 3",
        "day6",
        "216",
        "226",
        "227",
        "288",
        "360",
        "432",
        "433",
        "576",
        "648",
        "712",
    ]
    print("flags", {k: (k in text) for k in keys})
    for i, line in enumerate(text.splitlines()[:50], 1):
        if line.strip():
            print(f"Z {i}: {line[:200]}")
    print("--- HITS ---")
    n = 0
    for line in text.splitlines():
        if any(
            k in line
            for k in (
                "ROUTE_STEP",
                "FINAL_PLAN",
                "ADVANCE_START",
                "sale_horizon",
                "DECISIONS",
                "PROGRAM",
                "reselect",
                "ctypes",
                "CDLL",
                "agent.so",
                "step >=",
                "step>=",
                "day 3",
                "day 6",
                "DAY3",
                "DAY6",
                "switch",
                "route",
            )
        ) and len(line) < 220:
            print("HIT", line[:220])
            n += 1
            if n >= 60:
                print("...more...")
                break


if __name__ == "__main__":
    main()
