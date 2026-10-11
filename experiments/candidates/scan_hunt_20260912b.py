"""Static JSON/payload scan of 20260912b hunt. No cell exec."""

from __future__ import annotations

import base64
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260912b"
CUT14 = ROOT / "experiments/candidates/y3uanm_router_v5/main.py"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefile_rest(source: str) -> str | None:
    if not source.lstrip().startswith("%%writefile"):
        return None
    _, _, rest = source.partition("\n")
    return rest.replace("\r\n", "\n")


def main() -> None:
    cut14 = hashlib.sha256(CUT14.read_bytes()).hexdigest()
    print("cut14_main", cut14)

    ypath = DIR / "y3uanm__kaggriculture-safe-baseline-rollback-v20/kaggriculture-safe-baseline-rollback-v20.ipynb"
    ynb = json.loads(ypath.read_text(encoding="utf-8"))
    for cell in ynb["cells"]:
        rest = writefile_rest(cell_source(cell))
        if rest is None:
            continue
        sha = hashlib.sha256(rest.encode("utf-8")).hexdigest()
        print("y3uanm_v20_writefile", sha, "bytes", len(rest), "eq_cut14", sha == cut14)
        print("DECISIONS", "DECISIONS = (" in rest, "226" in rest, "360" in rest, "433" in rest)

    cpath = DIR / "crystalbaby__kaggriculture-dynamic-route-agent/kaggriculture-dynamic-route-agent.ipynb"
    cnb = json.loads(cpath.read_text(encoding="utf-8"))
    src = cell_source(cnb["cells"][0])
    marker = 'agent_b85 = "'
    start = src.find(marker)
    assert start >= 0
    start += len(marker)
    end = src.find('"', start)
    blob = src[start:end]
    raw = zlib.decompress(base64.b85decode(blob.encode("ascii")))
    text = raw.decode("utf-8", errors="replace")
    sha = hashlib.sha256(raw).hexdigest()
    print("crystalbaby_decompressed", sha, "bytes", len(raw))
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
        "144",
        "216",
        "226",
        "288",
        "360",
        "432",
        "433",
        "576",
        "648",
        "712",
    ]
    print("crystalbaby_flags", {k: (k in text) for k in keys})
    for i, line in enumerate(text.splitlines()[:40], 1):
        if line.strip():
            print(f"CB {i}: {line[:200]}")
    # later-block-ish assignments
    for line in text.splitlines():
        if any(
            k in line
            for k in (
                "ROUTE_STEP",
                "FINAL_PLAN_STEP",
                "ADVANCE_START",
                "sale_horizon",
                "DECISIONS",
                "PROGRAM",
                "reselect",
            )
        ) and len(line) < 220:
            print("CB HIT", line)


if __name__ == "__main__":
    main()
