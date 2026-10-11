"""Static inspect of 20260914j hunt notebooks. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260914j"
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
    "EXPECTED_MAIN_SHA256",
    "EXPECTED_SOURCE_SHA256",
    "PufferLib",
]
KEYS = (
    "ROUTE_STEP",
    "FINAL_PLAN_STEP",
    "sale_horizon",
    "ADVANCE_START",
    "reselect",
    "ctypes",
    "CDLL",
    "agent.so",
    "PROGRAM",
    "DECISIONS",
    "144",
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
    "433",
    "576",
    "648",
    "712",
    "P3",
    "P4",
    "P5",
    "P6",
    "EXPECTED_MAIN_SHA256",
    "EXPECTED_SOURCE_SHA256",
)
CUT14 = "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
CUT15 = "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
CUT16 = "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def assignments(src: str, names: tuple[str, ...]) -> dict[str, str]:
    out: dict[str, str] = {}
    for name in names:
        for m in re.finditer(rf"^{name}\s*=\s*(.+)$", src, flags=re.M):
            out[name] = m.group(1).strip()[:180]
    return out


def later_block_hits(src: str) -> list[str]:
    hits = []
    for pat in (
        r"step\s*>=\s*216",
        r"step\s*>\s*216",
        r"if step in",
        r"RESELECT",
        r"reselect",
        r"phase",
        r"PROGRAM",
        r"ROUTE_STEP",
        r"FINAL_PLAN",
        r"ADVANCE_START",
        r"sale_horizon",
    ):
        if re.search(pat, src, flags=re.I):
            hits.append(pat)
    return hits


def main() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        print("=" * 72)
        print(path.relative_to(DIR), "bytes", len(raw), "cells", len(notebook.get("cells") or []), flush=True)
        text = raw.decode("utf-8", errors="ignore")
        print("flags", [f for f in FLAGS if f in text], flush=True)
        for digest in list(dict.fromkeys(re.findall(r"[a-f0-9]{64}", text.lower())))[:12]:
            tag = []
            if digest == CUT14:
                tag.append("CUT14")
            if digest == CUT15:
                tag.append("CUT15")
            if digest == CUT16:
                tag.append("CUT16")
            print(" sha", digest, " ".join(tag), flush=True)
        for index, cell in enumerate(notebook.get("cells") or []):
            src = cell_source(cell)
            if not src.lstrip().startswith("%%writefile"):
                continue
            first, _, rest = src.partition("\n")
            name = first.split("%%writefile", 1)[-1].strip()
            payload = rest.replace("\r\n", "\n")
            if not payload.endswith("\n"):
                payload += "\n"
            digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            out = path.parent / name
            out.write_bytes(payload.encode("utf-8"))
            print("WRITEFILE", name, "bytes", len(payload.encode("utf-8")), "sha256", digest, "out", out, flush=True)
            if digest == CUT14:
                print("MATCH live cut14", flush=True)
            if digest == CUT15:
                print("MATCH live cut15", flush=True)
            if digest == CUT16:
                print("MATCH live cut16", flush=True)
            print("ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload, flush=True)
            print(
                "assign",
                assignments(
                    payload,
                    ("ROUTE_STEP", "FINAL_PLAN_STEP", "ADVANCE_START", "sale_horizon", "DECISIONS"),
                ),
                flush=True,
            )
            print("later_block_pats", later_block_hits(payload), flush=True)
            print("key_counts", {k: payload.count(k) for k in KEYS if k in payload}, flush=True)
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
                    print(f"  lines[{needle}] n={len(lines)}", flush=True)
                    for ln in lines[:18]:
                        print("   ", ln[:220], flush=True)
            try:
                tree = ast.parse(payload)
                print("ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)), flush=True)
            except SyntaxError as exc:
                print("ast_ok", False, exc, flush=True)


if __name__ == "__main__":
    main()
