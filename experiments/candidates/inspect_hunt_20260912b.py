"""Headers and flags from 2026-09-12b hunt notebooks. No cell exec."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260912b"
FLAGS = [
    "%%writefile",
    "agent.so",
    "ctypes",
    "CDLL",
    "reselect",
    "226",
    "360",
    "433",
    "144",
    "288",
    "432",
    "576",
    "227",
    "242",
    "266",
    "216",
    "PufferLib",
    "agent.dylib",
    ".so",
    "native",
    "later-block",
    "later_block",
    "ROUTE_STEP",
    "DECISIONS",
    "FINAL_PLAN_STEP",
    "writefile",
    "EXPECTED_SOURCE_SHA256",
    "EXPECTED_MAIN_SHA256",
    "gzip",
    "PROGRAM",
    "sale_horizon",
    "ADVANCE_START",
]
KEYS = (
    "ROUTE_STEP",
    "FINAL_PLAN",
    "DECISIONS",
    "ctypes",
    "CDLL",
    "agent.so",
    "reselect",
    "226",
    "360",
    "433",
    "288",
    "432",
    "576",
    "216",
    "BUY_ANIMAL",
    "def agent",
    "PROGRAM",
    "sale_horizon",
    "ADVANCE_START",
    "712",
    "648",
    "144",
    "P3",
    "P4",
    "P5",
    "P6",
    "P8",
    "EXPECTED_SOURCE_SHA256",
    "EXPECTED_MAIN_SHA256",
)


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefile_payloads(source: str) -> list[tuple[str, str]]:
    out = []
    if source.lstrip().startswith("%%writefile"):
        first, _, rest = source.partition("\n")
        name = first.split("%%writefile", 1)[-1].strip()
        if name.startswith("-a "):
            name = name[3:].strip()
        out.append((name, rest))
        return out
    for m in re.finditer(r"open\(['\"]([^'\"]+)['\"].*?['\"]w", source):
        out.append((m.group(1), source[:400]))
    return out


def main() -> None:
    for path in sorted(DIR.rglob("*")):
        if path.name == "kernel-metadata.json":
            meta = json.loads(path.read_text(encoding="utf-8"))
            print("=" * 70)
            print(
                "META",
                path.parent.name,
                {
                    k: meta.get(k)
                    for k in ("id", "title", "code_file", "language", "kernel_type", "is_private")
                },
            )
            continue
        if path.suffix.lower() not in {".ipynb", ".py", ".json", ".md"}:
            continue
        if path.name == "kernel-metadata.json":
            continue
        raw = path.read_bytes()
        print("=" * 70)
        print(path.relative_to(DIR), "bytes", len(raw), "sha256", hashlib.sha256(raw).hexdigest())
        text = raw.decode("utf-8", errors="ignore")
        hits = [f for f in FLAGS if f.lower() in text.lower() or f in text]
        print("flags", hits)
        if path.suffix == ".py":
            for i, line in enumerate(text.splitlines()[:40], 1):
                if line.strip():
                    print(f"PY {i}: {line[:220]}")
            continue
        if path.suffix != ".ipynb":
            continue
        notebook = json.loads(raw.decode("utf-8"))
        cells = notebook.get("cells") or []
        joined = "\n".join(cell_source(c) for c in cells)
        flags = {
            "writefile": "%%writefile" in joined,
            "ctypes": "ctypes" in joined,
            "CDLL": "CDLL" in joined or "cdll" in joined.lower(),
            "agent.so": "agent.so" in joined,
            "reselect": "reselect" in joined.lower(),
            "DECISIONS": "DECISIONS" in joined,
            "ROUTE_STEP": "ROUTE_STEP" in joined,
            "FINAL_PLAN": "FINAL_PLAN_STEP" in joined,
            "later-block": "later-block" in joined.lower() or "later_block" in joined,
            "226": "226" in joined,
            "360": "360" in joined,
            "433": "433" in joined,
            "144": "144" in joined,
            "288": "288" in joined,
            "432": "432" in joined,
            "576": "576" in joined,
            "227": "227" in joined,
            "242": "242" in joined,
            "266": "266" in joined,
            "216": "216" in joined,
            "gzip": "gzip" in joined.lower() or "zlib" in joined.lower() or "b85" in joined.lower(),
            "sale_horizon": "sale_horizon" in joined,
            "ADVANCE_START": "ADVANCE_START" in joined,
            "PROGRAM": "PROGRAM" in joined,
            "712": "712" in joined,
            "648": "648" in joined,
        }
        print("cells", len(cells), "FLAGS", {k: v for k, v in flags.items() if v})
        for index, cell in enumerate(cells[:8]):
            source = cell_source(cell)
            first = source.strip().splitlines()[:10]
            if not first:
                continue
            print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
            for line in first:
                print(line[:220])
        for index, cell in enumerate(cells):
            source = cell_source(cell)
            for name, payload in writefile_payloads(source):
                sha = hashlib.sha256(payload.replace("\r\n", "\n").encode("utf-8")).hexdigest()
                print(f"WRITEFILE cell={index} name={name!r} bytes={len(payload)} sha256={sha}")
                n = 0
                for line in payload.splitlines():
                    if any(k in line for k in KEYS) and len(line) < 240:
                        print("  ", line[:220])
                        n += 1
                        if n >= 40:
                            print("  ...[more KEY hits]...")
                            break
            low = source.lower()
            if any(
                k in source or k in low
                for k in (
                    "%%writefile",
                    "ctypes",
                    "CDLL",
                    "agent.so",
                    "EXPECTED_SOURCE_SHA256",
                    "EXPECTED_MAIN_SHA256",
                    "def agent",
                )
            ):
                print(f"HIT cell {index} {cell.get('cell_type')} {len(source)}")
                shown = 0
                for line in source.splitlines():
                    if not line.strip():
                        continue
                    if len(line) > 240 and any(
                        k in line for k in ("b85decode", "b64", "zlib", "lzma", "_DATA", "_INLINE")
                    ):
                        print(" ", line[:120] + " ...[payload truncated]...")
                        continue
                    print(" ", line[:200])
                    shown += 1
                    if shown >= 22:
                        break


if __name__ == "__main__":
    main()
