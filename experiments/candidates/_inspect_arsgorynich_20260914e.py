"""Static inspect of arsgorynich v40-challenger. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = (
    ROOT
    / "artifacts/public_sources/_hunt_20260914e/arsgorynich__kaggriculture-v40-challenger/kaggriculture-v40-challenger.ipynb"
)
CUT14 = "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
CUT15 = "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
CUT16 = "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"
REJECTED = {
    "3dd123c5": "aurax7 v4",
    "ea4c28e6": "aurax7 v5",
    "77cf6772": "yhay81 0913",
    "546c4224": "ahmed V40",
    "8951ff93": "ahmed V41",
    "85c8b532": "alperen scored-agent",
    "d12f2987": "xuantianfengwu allocator",
    "3b8a1d4d": "xuantianfengwu r10",
    "31ee22dc": "lime0001 t23",
    "708c7485": "renji/guru V39",
    "a2047ebd": "Ahmed V38",
    "5dc0c68c": "timed-six-cow",
    "1c98c297": "prvsiyan market-ledger",
    "acf7c664": "cut14",
    "b87a27ed": "cut15",
    "26ffba52": "cut16",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    raw = PATH.read_bytes()
    notebook = json.loads(raw.decode("utf-8"))
    cells = notebook.get("cells") or []
    print("bytes", len(raw), "cells", len(cells), "n_lines_file", raw.count(b"\n") + 1)
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
        "PufferLib",
        "dataset",
        "kaggle datasets",
    ]
    print("flags", [f for f in flags if f in text])
    print("n_writefile", text.count("%%writefile"))
    sha_hits = list(dict.fromkeys(re.findall(r"[a-f0-9]{64}", text.lower())))
    print("n_sha64", len(sha_hits))
    for digest in sha_hits[:20]:
        tag = []
        if digest == CUT14:
            tag.append("CUT14")
        if digest == CUT15:
            tag.append("CUT15")
        if digest == CUT16:
            tag.append("CUT16")
        known = REJECTED.get(digest[:8])
        if known:
            tag.append(known)
        print(" sha", digest, " ".join(tag))
    for index, cell in enumerate(cells):
        src = cell_source(cell)
        head = src[:120].replace("\n", " | ")
        print(f"cell{index} type={cell.get('cell_type')} n={len(src)} head={head!r}")
        if not src.lstrip().startswith("%%writefile"):
            continue
        first, _, rest = src.partition("\n")
        name = first.split("%%writefile", 1)[-1].strip()
        payload = rest.replace("\r\n", "\n")
        if not payload.endswith("\n"):
            payload += "\n"
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        out = PATH.parent / name
        out.write_bytes(payload.encode("utf-8"))
        print("WRITEFILE", name, "bytes", len(payload.encode("utf-8")), "sha256", digest)
        print("  prefix8", digest[:8], REJECTED.get(digest[:8], "unknown"))
        print("  ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
        for name_asg in ("ROUTE_STEP", "FINAL_PLAN_STEP", "ADVANCE_START", "sale_horizon", "DECISIONS"):
            m = re.search(rf"^{name_asg}\s*=\s*(.+)$", payload, flags=re.M)
            if m:
                print("  assign", name_asg, m.group(1).strip()[:180])
        for needle in (
            "if step",
            "elif step",
            "ROUTE_STEP",
            "FINAL_PLAN",
            "reselect",
            "PROGRAM",
            "216",
            "226",
            "288",
            "360",
            "432",
            "576",
            "648",
            "712",
        ):
            lines = [ln for ln in payload.splitlines() if needle in ln]
            if lines:
                print(f"  lines[{needle}] n={len(lines)}")
                for ln in lines[:12]:
                    print("   ", ln[:220])
        try:
            tree = ast.parse(payload)
            print("  ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)))
        except SyntaxError as exc:
            print("  ast_ok", False, exc)


if __name__ == "__main__":
    main()
