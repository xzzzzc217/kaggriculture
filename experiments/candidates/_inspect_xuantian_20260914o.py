"""Static inspect of xuantianfengwu hour-4 financing-allocator. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB = (
    ROOT
    / "artifacts/public_sources/_hunt_20260914o"
    / "xuantianfengwu__kaggriculture-hour-4-financing-allocator"
    / "kaggriculture-hour-4-financing-allocator.ipynb"
)
CUT14 = "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
CUT15 = "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
CUT16 = "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"
KNOWN = {
    "728fdfb4": "ahmed_v42",
    "8951ff93": "ahmed_v41",
    "546c4224": "ahmed_v40",
    "708c7485": "v39_reprint",
    "a2047ebd": "ahmed_v38",
    "62a80706": "rohitt94",
    "ea4c28e6": "aurax7_v5",
    "31ee22dc": "lime0001_t23",
    "85c8b532": "alperen_scored",
    "3b8a1d4d": "xuantian_r10",
    "d12f2987": "xuantian_allocator",
    "b49709bd": "xuantian_llc",
    "f4e3935c": "guru_fully_dynamic",
    "77cf6772": "yhay81_0913",
    "acf7c664": "cut14",
    "b87a27ed": "cut15",
    "26ffba52": "cut16",
    "5dc0c68c": "timed_six_cow",
    "1c98c297": "prvsiyan_ledger",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    raw = NB.read_bytes()
    nb = json.loads(raw.decode("utf-8"))
    print("bytes", len(raw), "cells", len(nb.get("cells") or []))
    text = raw.decode("utf-8", errors="ignore")
    flags = [
        "%%writefile",
        "agent.so",
        "ctypes",
        "CDLL",
        "reselect",
        "ROUTE_STEP",
        "FINAL_PLAN_STEP",
        "sale_horizon",
        "ADVANCE_START",
        "PROGRAM",
        "DECISIONS",
        "Path.write_text",
        "open(",
        "submission.py",
        "main.py",
        "Shop0909",
        "144",
        "216",
        "226",
        "227",
        "288",
        "360",
        "432",
        "576",
        "648",
        "712",
        "COW",
        "HOUR",
        "financing",
    ]
    print("flags", [f for f in flags if f in text])
    for digest in list(dict.fromkeys(re.findall(r"[a-f0-9]{64}", text.lower())))[:24]:
        tag = KNOWN.get(digest[:8], "")
        if digest == CUT14:
            tag = "CUT14"
        if digest == CUT15:
            tag = "CUT15"
        if digest == CUT16:
            tag = "CUT16"
        print(" sha", digest, tag)
    for index, cell in enumerate(nb.get("cells") or []):
        src = cell_source(cell)
        kind = cell.get("cell_type")
        head = src.strip().splitlines()[:4]
        print(f"-- cell {index} {kind} chars={len(src)} head={head}")
        if src.lstrip().startswith("%%writefile"):
            first, _, rest = src.partition("\n")
            name = first.split("%%writefile", 1)[-1].strip()
            payload = rest.replace("\r\n", "\n")
            if not payload.endswith("\n"):
                payload += "\n"
            digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            out = NB.parent / name
            out.write_bytes(payload.encode("utf-8"))
            print("WRITEFILE", name, "bytes", len(payload.encode("utf-8")), "sha256", digest)
            print("known", KNOWN.get(digest[:8], "NEW"))
            print("ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
            for needle in (
                "if step",
                "elif step",
                "ROUTE_STEP",
                "FINAL_PLAN",
                "reselect",
                "PROGRAM",
                "216",
                "226",
                "227",
                "240",
                "241",
                "242",
                "265",
                "266",
                "288",
                "360",
                "432",
                "576",
                "648",
                "712",
                "HOUR",
                "COW",
            ):
                lines = [ln for ln in payload.splitlines() if needle in ln]
                if lines:
                    print(f"  lines[{needle}] n={len(lines)}")
                    for ln in lines[:20]:
                        print("   ", ln[:220])
            try:
                tree = ast.parse(payload)
                print("ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)))
            except SyntaxError as exc:
                print("ast_ok", False, exc)
        elif "writefile" in src.lower() or "main.py" in src or "submission.py" in src:
            print("  mention writefile/main/submission")
            for ln in src.splitlines()[:30]:
                if any(k in ln.lower() for k in ("writefile", "main.py", "submission", "sha", "step")):
                    print("   ", ln[:220])


if __name__ == "__main__":
    main()
