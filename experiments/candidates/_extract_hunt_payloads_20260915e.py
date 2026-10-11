"""Static reconstruct of 20260915e hunt payloads. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260915e"
KNOWN = {
    "728fdfb4": "ahmed_v42",
    "8951ff93": "ahmed_v41",
    "546c4224": "ahmed_v40",
    "708c7485": "v39_reprint",
    "a2047ebd": "ahmed_v38",
    "919fc1d6": "ahmed_v43",
    "7a37397f": "nathan_pipe4",
    "77cf6772": "yhay81_0913",
    "acf7c664": "cut14",
    "b87a27ed": "cut15",
    "26ffba52": "cut16",
    "602ae8be": "kenan_shop0909",
    "b041058e": "alperen_v58",
    "5fd73afd": "alperen_momentum",
    "01f0cd47": "harvestforge",
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


def inspect(label: str, payload: str, digest: str) -> None:
    print("PAYLOAD", label, "bytes", len(payload.encode("utf-8")), "sha256", digest, "known", KNOWN.get(digest[:8], "NEW"))
    print(" ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
    print(" 144/648", payload.count("144"), payload.count("648"), "288", payload.count("288"), "712", payload.count("712"))
    print(" ROUTE_STEP", "ROUTE_STEP" in payload, "PROGRAM", "PROGRAM" in payload)
    print(" sale_horizon", "sale_horizon" in payload, "ADVANCE_START", "ADVANCE_START" in payload)
    print(" reselect", "reselect" in payload.lower(), "Shop0909", "Shop0909" in payload)
    print(" 216<=step<=227", "216<=step<=227" in payload.replace(" ", ""))
    for needle in (
        "if step>=144",
        "if step>=216",
        "if step>=226",
        "if step>=288",
        "if step>=360",
        "if step>=432",
        "if step>=576",
        "if step>=648",
        "if step==712",
        "ROUTE_STEP",
        "PROGRAM",
        "_R37_HORIZONS",
        "sale_horizon",
        "ADVANCE_START",
    ):
        n = payload.count(needle)
        if n:
            print(f"  count[{needle}]={n}")
    lines = [ln for ln in payload.splitlines() if "if step" in ln or "elif step" in ln or "sale_horizon" in ln or "ADVANCE_START" in ln]
    print(" if-step/horizon n", len(lines))
    for ln in lines[:40]:
        print("  ", ln[:220])
    try:
        tree = ast.parse(payload)
        print(" ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)))
    except SyntaxError as exc:
        print(" ast_ok", False, exc)


def write_payload(path: Path, payload: str) -> str:
    if not payload.endswith("\n"):
        payload += "\n"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    path.write_bytes(payload.encode("utf-8"))
    print("WROTE", path, "sha", digest)
    return digest


def extract_v44() -> None:
    nb_path = DIR / "ahmedberatozer__kaggriculture-v44-winning-the-same-turn-sale-race" / "kaggriculture-v44-winning-the-same-turn-sale-race.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    print("=" * 72)
    print("v44 cells", len(nb.get("cells") or []))
    for index, cell in enumerate(nb.get("cells") or []):
        src = cell_source(cell)
        head = src.strip().splitlines()[:3]
        print(f"-- cell {index} {cell.get('cell_type')} chars={len(src)} head={head}")
        expected = re.search(r"EXPECTED_MAIN_SHA256\s*=\s*'([a-f0-9]{64})'", src)
        if expected:
            print(" expected", expected.group(1))
        if "SOURCE_BYTES" in src:
            payload = extract_join_bytes(src)
            print(" SOURCE_BYTES", None if payload is None else len(payload))
            if payload is None:
                continue
            digest_raw = hashlib.sha256(payload).hexdigest()
            print(" raw sha", digest_raw, "known", KNOWN.get(digest_raw[:8], "NEW"))
            text = payload.decode("utf-8")
            digest = write_payload(nb_path.parent / "main.py", text)
            inspect("v44", text, digest)
        if src.lstrip().startswith("%%writefile"):
            first, _, rest_src = src.partition("\n")
            name = Path(first.split("%%writefile", 1)[-1].strip()).name or "main.py"
            payload_txt = rest_src.replace("\r\n", "\n")
            digest = write_payload(nb_path.parent / name, payload_txt)
            inspect("v44_writefile", payload_txt, digest)


def main() -> None:
    extract_v44()


if __name__ == "__main__":
    main()
