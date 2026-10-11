"""Static writefile/payload dump for 20260915c hunt. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260915c"
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
    "dc07c7a9": "xuantian_hour4",
    "364ca885": "xuantian_terminal",
    "ffc0e6e2": "taylor_fib",
    "919fc1d6": "ahmed_v43",
    "01f0cd47": "harvestforge",
    "7a37397f": "nathan_pipe4",
    "595d29fe": "anand_analysis",
    "602ae8be": "kenan_shop0909",
}
FLAGS = [
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
    "SOURCE_BYTES",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def inspect_payload(label: str, payload: str, digest: str) -> None:
    print("PAYLOAD", label, "bytes", len(payload.encode("utf-8")), "sha256", digest, "known", KNOWN.get(digest[:8], "NEW"))
    print(" ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
    print(" 144/648", payload.count("144"), payload.count("648"), "288", payload.count("288"), "712", payload.count("712"))
    print(" ROUTE_STEP", "ROUTE_STEP" in payload, "PROGRAM", "PROGRAM" in payload, "sale_horizon", "sale_horizon" in payload)
    print(" ADVANCE_START", "ADVANCE_START" in payload, "reselect", "reselect" in payload.lower())
    for needle in (
        "if step",
        "elif step",
        "ROUTE_STEP",
        "FINAL_PLAN",
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
        "COW",
        "desired_land",
        "BUY_ANIMAL",
    ):
        lines = [ln for ln in payload.splitlines() if needle in ln]
        if not lines:
            continue
        print(f"  lines[{needle}] n={len(lines)}")
        for ln in lines[:12]:
            print("   ", ln[:220])
    try:
        tree = ast.parse(payload)
        print(" ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)))
    except SyntaxError as exc:
        print(" ast_ok", False, exc)


def main() -> None:
    for path in sorted(DIR.rglob("*")):
        if not path.is_file():
            continue
        print("=" * 72)
        print(path.relative_to(DIR), "bytes", path.stat().st_size)
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        print("flags", [f for f in FLAGS if f in text])
        for digest in list(dict.fromkeys(re.findall(r"[a-f0-9]{64}", text.lower())))[:16]:
            tag = KNOWN.get(digest[:8], "")
            if digest == CUT14:
                tag = "CUT14"
            if digest == CUT15:
                tag = "CUT15"
            if digest == CUT16:
                tag = "CUT16"
            print(" sha", digest, tag)
        if path.suffix == ".py":
            digest = hashlib.sha256(raw).hexdigest()
            inspect_payload(path.name, text, digest)
            continue
        if path.suffix != ".ipynb":
            continue
        nb = json.loads(text)
        print("cells", len(nb.get("cells") or []))
        for index, cell in enumerate(nb.get("cells") or []):
            src = cell_source(cell)
            m = re.search(r"%%writefile\s+(\S+)", src)
            if m:
                first, _, rest = src.partition("\n")
                name = Path(first.split("%%writefile", 1)[-1].strip()).name or "main.py"
                payload = rest.replace("\r\n", "\n")
                if not payload.endswith("\n"):
                    payload += "\n"
                digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
                out = path.parent / name
                out.write_bytes(payload.encode("utf-8"))
                print("WRITEFILE cell", index, name, "sha", digest)
                inspect_payload(name, payload, digest)
            elif "SOURCE_BYTES" in src or "EXPECTED_MAIN_SHA256" in src or "writefile" in src.lower() or "AGENT_B64" in src:
                print(f"-- cell {index} {cell.get('cell_type')} chars={len(src)} writefile/sha mention")
                for ln in src.splitlines()[:40]:
                    print("   ", ln[:200])
            elif index < 12:
                head = src[:240].replace("\n", " / ")
                print(f"-- cell {index} {cell.get('cell_type')} chars={len(src)} head={head}")


if __name__ == "__main__":
    main()
