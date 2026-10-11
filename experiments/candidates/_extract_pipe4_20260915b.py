"""Static B85/gzip reconstruct of nathanjacob pipe-4. No cell exec."""

from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB = (
    ROOT
    / "artifacts/public_sources/_hunt_20260915b"
    / "nathanjacob__beyond-v43-what-the-top-clusters-do-on-turn-1"
    / "beyond-v43-what-the-top-clusters-do-on-turn-1.ipynb"
)
V43 = "919fc1d61050cd96f799979e49177ae3ac7bce98ec9835724238bea73f4a08ed"
V42 = "728fdfb4"


def main() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    src = "".join(nb["cells"][7]["source"])
    expected = re.search(r"EXPECTED_SHA256\s*=\s*'([a-f0-9]{64})'", src)
    b85 = re.search(r"B85_SOURCE\s*=\s*'([^']+)'", src)
    print("expected", expected.group(1) if expected else None)
    print("b85_len", len(b85.group(1)) if b85 else None)
    raw = gzip.decompress(base64.b85decode(b85.group(1)))
    digest = hashlib.sha256(raw).hexdigest()
    print("sha256_raw", digest, "match_expected", expected and digest == expected.group(1))
    payload = raw.decode("utf-8")
    if not payload.endswith("\n"):
        payload += "\n"
    digest_nl = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print("sha256_nl", digest_nl)
    out = NB.parent / "main.py"
    out.write_bytes(payload.encode("utf-8"))
    print("WROTE", out, "bytes", out.stat().st_size)
    print("ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
    print("ROUTE_STEP", "ROUTE_STEP" in payload, "PROGRAM", "PROGRAM" in payload)
    print("sale_horizon", "sale_horizon" in payload, "ADVANCE_START", "ADVANCE_START" in payload)
    print("reselect", "reselect" in payload.lower())
    print("144/648", payload.count("144"), payload.count("648"), "288", payload.count("288"), "712", payload.count("712"))
    print("v43_prefix", digest[:8] == V43[:8], "v42_prefix", digest[:8] == V42)
    for needle in (
        "if step>=144",
        "if step>=648",
        "if step==712",
        "216<=step<=227",
        "_R37_HORIZONS",
        "Shop0909",
        "C9",
        "BUY_PRODUCT WHEAT",
    ):
        print(needle, payload.count(needle))
    lines = [ln for ln in payload.splitlines() if "if step" in ln or "elif step" in ln]
    print("if-step n", len(lines))
    for ln in lines[:24]:
        print(" ", ln[:220])
    try:
        tree = ast.parse(payload)
        print("ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)))
    except SyntaxError as exc:
        print("ast_ok", False, exc)


if __name__ == "__main__":
    main()
