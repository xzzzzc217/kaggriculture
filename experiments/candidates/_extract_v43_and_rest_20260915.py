"""Static extract Ahmed V43 SOURCE_BYTES and remaining hunt notebooks. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260915"
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
    "919fc1d6": "ahmed_v43_claimed",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def extract_join_bytes(src: str) -> bytes | None:
    tree = ast.parse(src)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "SOURCE_BYTES" for t in node.targets):
            continue
        value = node.value
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and value.func.attr == "join":
            parts = value.args[0] if value.args else None
            if isinstance(parts, ast.Tuple):
                out = b""
                for elt in parts.elts:
                    out += ast.literal_eval(elt)
                return out
        if isinstance(value, ast.Constant) and isinstance(value.value, (bytes, bytearray)):
            return bytes(value.value)
    return None


def inspect_text(payload: str) -> None:
    print(" 144/648", payload.count("144"), payload.count("648"), "288", payload.count("288"), "712", payload.count("712"))
    print(" ROUTE_STEP", "ROUTE_STEP" in payload, "PROGRAM", "PROGRAM" in payload, "sale_horizon", "sale_horizon" in payload)
    print(" ADVANCE_START", "ADVANCE_START" in payload, "reselect", "reselect" in payload.lower(), "ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
    for needle in ("if step", "elif step", "216", "226", "227", "288", "360", "432", "576", "648", "712", "desired_land", "COW"):
        lines = [ln for ln in payload.splitlines() if needle in ln]
        if lines:
            print(f"  lines[{needle}] n={len(lines)}")
            for ln in lines[:10]:
                print("   ", ln[:220])


def main() -> None:
    v43 = DIR / "ahmedberatozer__kaggriculture-v43-recovering-lost-harvests" / "kaggriculture-v43-recovering-lost-harvests.ipynb"
    nb = json.loads(v43.read_text(encoding="utf-8"))
    for index, cell in enumerate(nb.get("cells") or []):
        src = cell_source(cell)
        if "SOURCE_BYTES" not in src:
            continue
        payload = extract_join_bytes(src)
        print("V43 cell", index, "SOURCE_BYTES", None if payload is None else len(payload))
        if payload is None:
            continue
        digest = hashlib.sha256(payload).hexdigest()
        out = v43.parent / "main.py"
        out.write_bytes(payload)
        print("WROTE", out, "sha256", digest, "known", KNOWN.get(digest[:8], "NEW"))
        text = payload.decode("utf-8", errors="replace")
        inspect_text(text)
        try:
            ast.parse(text)
            print(" ast_ok True")
        except SyntaxError as exc:
            print(" ast_ok False", exc)

    rest = [
        "destbreso__agent-telemetry-catch-what-you-lose/agent-telemetry-catch-what-you-lose.ipynb",
        "hosen42__kaggriculture-v11-hc1-vs-h5-validation/kaggriculture-v11-hc1-vs-h5-validation.ipynb",
        "leoprovorov__god-s-mode-hacked-stores/god-s-mode-hacked-stores.ipynb",
        "nathanjacob__how-many-twins-strategy-clustering-kaggriculture/how-many-twins-strategy-clustering-kaggriculture.ipynb",
        "nathanjacob__kaggriculture-pipe-2-agent/kaggriculture-pipe-2-agent.ipynb",
        "prvsiyan__kaggriculture-field-clock-action-budget/kaggriculture-field-clock-action-budget.ipynb",
    ]
    for rel in rest:
        path = DIR / rel
        raw = path.read_bytes()
        nb = json.loads(raw.decode("utf-8"))
        text = raw.decode("utf-8", errors="ignore")
        print("=" * 72)
        print(rel, "bytes", len(raw), "cells", len(nb.get("cells") or []))
        print(" flags", [f for f in ("%%writefile", "agent.so", "ctypes", "CDLL", "SOURCE_BYTES", "main.py", "submission.py", "ROUTE_STEP", "PROGRAM") if f in text])
        for digest in list(dict.fromkeys(re.findall(r"[a-f0-9]{64}", text.lower())))[:8]:
            print(" sha", digest, KNOWN.get(digest[:8], ""))
        for index, cell in enumerate(nb.get("cells") or []):
            src = cell_source(cell)
            if "SOURCE_BYTES" in src:
                payload = extract_join_bytes(src)
                print(" SOURCE_BYTES cell", index, None if payload is None else len(payload))
                if payload:
                    digest = hashlib.sha256(payload).hexdigest()
                    name = "main.py" if "main.py" in src else "payload.py"
                    (path.parent / name).write_bytes(payload)
                    print(" WROTE", name, digest, KNOWN.get(digest[:8], "NEW"))
                    inspect_text(payload.decode("utf-8", errors="replace"))
            if src.lstrip().startswith("%%writefile"):
                first, _, rest_src = src.partition("\n")
                name = first.split("%%writefile", 1)[-1].strip()
                payload = rest_src.replace("\r\n", "\n")
                if not payload.endswith("\n"):
                    payload += "\n"
                digest = hashlib.sha256(payload.encode()).hexdigest()
                (path.parent / name).write_text(payload, encoding="utf-8")
                print(" WRITEFILE", name, digest, KNOWN.get(digest[:8], "NEW"))
                inspect_text(payload)
            if index < 4 or "agent" in src.lower()[:200] or "def agent" in src:
                head = src.strip().splitlines()[:4]
                print(f"-- cell {index} {cell.get('cell_type')} chars={len(src)} head={head}")


if __name__ == "__main__":
    main()
