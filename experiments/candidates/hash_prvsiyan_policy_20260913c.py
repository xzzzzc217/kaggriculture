"""Static SHA of prvsiyan notebook policy string. No cell exec."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

NB = (
    Path(__file__).resolve().parents[2]
    / "artifacts/public_sources/_hunt_20260913c"
    / "prvsiyan__kaggriculture-market-ledger-seasonal-counterplay"
    / "kaggriculture-market-ledger-seasonal-counterplay.ipynb"
)


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    src = "".join(nb["cells"][2]["source"])
    marker = "policy = r'''"
    start = src.find(marker) + len(marker)
    end = src.rfind("'''")
    payload = src[start:end].replace("\r\n", "\n")
    print("policy_bytes", len(payload))
    print("policy_sha256", hashlib.sha256(payload.encode("utf-8")).hexdigest())
    print("def_agent", "def agent" in payload)
    print("reselect", "reselect" in payload.lower())
    print("ctypes", "ctypes" in payload)
    print("agent.so", "agent.so" in payload)
    print("ROUTE_STEP", "ROUTE_STEP" in payload)
    print("PROGRAM", "PROGRAM" in payload)
    print("sale_horizon", "sale_horizon" in payload)
    print("216", "216" in payload)


if __name__ == "__main__":
    main()
