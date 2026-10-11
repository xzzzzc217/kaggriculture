"""Readable source slices from 20260912b hunt. No cell exec, no payload decode of unrelated blobs."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260912b"
CUT14 = (
    Path(__file__).resolve().parents[2]
    / "experiments/candidates/y3uanm_router_v5/main.py"
)


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def dump_nb(rel: str) -> None:
    path = DIR / rel
    print("=" * 78)
    print(rel, "bytes", path.stat().st_size, "sha256", hashlib.sha256(path.read_bytes()).hexdigest())
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells") or []
    print("n_cells", len(cells))
    for i, cell in enumerate(cells):
        src = cell_source(cell)
        print(f"-- cell {i} {cell.get('cell_type')} {len(src)} exec={cell.get('execution_count')} outputs={len(cell.get('outputs') or [])} --")
        lines = src.splitlines()
        if cell.get("cell_type") == "markdown":
            for line in lines[:22]:
                print(line[:220])
            continue
        if src.lstrip().startswith("%%writefile"):
            first = lines[0] if lines else ""
            rest = "\n".join(lines[1:])
            sha = hashlib.sha256(rest.replace("\r\n", "\n").encode("utf-8")).hexdigest()
            print("WRITEFILE", first[:120], "payload_sha256", sha, "payload_bytes", len(rest))
            shown = 0
            for line in lines:
                if len(line) > 240 and any(
                    k in line for k in ("b85decode", "b64", "zlib", "lzma", "_DATA", "_INLINE", "PROGRAM")
                ):
                    print(line[:100] + " ...[payload truncated]...")
                    continue
                interesting = any(
                    k in line
                    for k in (
                        "ROUTE_STEP",
                        "FINAL_PLAN",
                        "ADVANCE_START",
                        "sale_horizon",
                        "reselect",
                        "later",
                        "ctypes",
                        "CDLL",
                        "agent.so",
                        "EXPECTED",
                        "216",
                        "226",
                        "227",
                        "242",
                        "266",
                        "288",
                        "360",
                        "432",
                        "433",
                        "576",
                        "648",
                        "712",
                        "def agent",
                        "SETTINGS",
                        "SALE_HORIZON",
                        "DECISIONS",
                    )
                )
                if interesting or shown < 18:
                    print(line[:220])
                    shown += 1
                    if shown > 90:
                        print("...[truncated writefile]...")
                        break
            real_ctypes = bool(re.search(r"\bctypes\b", rest))
            real_cdll = "CDLL(" in rest or "cdll." in rest.lower()
            real_so = "agent.so" in rest or "agent.dylib" in rest
            print("REAL_CTYPES", real_ctypes, "REAL_CDLL", real_cdll, "REAL_AGENT_SO", real_so)
            print("reselect", "reselect" in rest.lower(), "later_block", "later-block" in rest.lower() or "later_block" in rest)
            continue
        for line in lines[:50]:
            if len(line) > 240:
                print(line[:120] + " ...[long]...")
            else:
                print(line[:220])
        if len(lines) > 50:
            print(f"...[{len(lines)-50} more lines]...")


def crystalbaby_static_flags() -> None:
    path = DIR / "crystalbaby__kaggriculture-dynamic-route-agent/kaggriculture-dynamic-route-agent.ipynb"
    nb = json.loads(path.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][0])
    print("=" * 78)
    print("crystalbaby cell0 static flags (no decompress, no cell exec)")
    for key in (
        "%%writefile",
        "b85decode",
        "a85decode",
        "zlib",
        "main.py",
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
    ):
        print(key, key in src, src.count(key))
    short = [ln for ln in src.splitlines() if len(ln) < 240]
    print("short_lines", len(short))
    for ln in short:
        print(ln[:220])


def y3uanm_vs_cut14() -> None:
    path = DIR / "y3uanm__kaggriculture-safe-baseline-rollback-v20/kaggriculture-safe-baseline-rollback-v20.ipynb"
    nb = json.loads(path.read_text(encoding="utf-8"))
    payload = None
    for cell in nb["cells"]:
        src = cell_source(cell)
        if src.lstrip().startswith("%%writefile"):
            payload = "\n".join(src.splitlines()[1:]).replace("\r\n", "\n")
            break
    assert payload is not None
    wf = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    cut14 = hashlib.sha256(CUT14.read_bytes()).hexdigest()
    print("=" * 78)
    print("y3uanm_v20_writefile", wf)
    print("cut14_main", cut14)
    print("IDENTICAL", wf == cut14)


def main() -> None:
    dump_nb("y3uanm__kaggriculture-safe-baseline-rollback-v20/kaggriculture-safe-baseline-rollback-v20.ipynb")
    dump_nb("dmitriigluzdov__kaggriculture-a-smaller-market-shock/kaggriculture-a-smaller-market-shock.ipynb")
    dump_nb("municef1__lb-2448-single-file-kaggriculture-agent/lb-2448-single-file-kaggriculture-agent.ipynb")
    dump_nb("crystalbaby__kaggriculture-dynamic-route-agent/kaggriculture-dynamic-route-agent.ipynb")
    dump_nb("bernubritz__kaggriculture-h4-best/kaggriculture-h4-best.ipynb")
    dump_nb("melomanpanda__main-py/main-py.ipynb")
    crystalbaby_static_flags()
    y3uanm_vs_cut14()


if __name__ == "__main__":
    main()
