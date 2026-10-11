"""Static JSON scan of 20260911b hunt notebooks. No cell exec."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260911b"
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
        if path.suffix.lower() not in {".ipynb", ".py"}:
            continue
        if path.name == "kernel-metadata.json":
            continue
        raw = path.read_bytes()
        print("=" * 78)
        print(path.relative_to(DIR), "bytes", len(raw), "sha256", hashlib.sha256(raw).hexdigest())
        if path.suffix == ".py":
            text = raw.decode("utf-8", errors="ignore")
            flags = {
                k: (k in text or k.lower() in text.lower())
                for k in (
                    "ctypes",
                    "CDLL",
                    "agent.so",
                    "ROUTE_STEP",
                    "FINAL_PLAN_STEP",
                    "DECISIONS",
                    "reselect",
                    "216",
                    "226",
                    "288",
                    "360",
                    "432",
                    "576",
                    "144",
                    "648",
                    "712",
                    "sale_horizon",
                    "PROGRAM",
                )
            }
            print("FLAGS", {k: v for k, v in flags.items() if v})
            for i, line in enumerate(text.splitlines()[:90]):
                if any(k in line for k in KEYS):
                    print(f"  L{i+1}", line[:220])
            continue
        nb = json.loads(raw.decode("utf-8"))
        cells = nb.get("cells") or []
        text = "\n".join(cell_source(c) for c in cells)
        flags = {
            "writefile": "%%writefile" in text,
            "ctypes": "ctypes" in text,
            "CDLL": "CDLL" in text or "cdll" in text.lower(),
            "agent.so": "agent.so" in text,
            "reselect": "reselect" in text.lower(),
            "DECISIONS": "DECISIONS" in text,
            "ROUTE_STEP": "ROUTE_STEP" in text,
            "FINAL_PLAN": "FINAL_PLAN_STEP" in text,
            "later-block": "later-block" in text.lower() or "later_block" in text,
            "226": "226" in text,
            "360": "360" in text,
            "433": "433" in text,
            "144": "144" in text,
            "288": "288" in text,
            "432": "432" in text,
            "576": "576" in text,
            "227": "227" in text,
            "242": "242" in text,
            "266": "266" in text,
            "216": "216" in text,
            "gzip": "gzip" in text.lower() or "zlib" in text.lower() or "b85" in text.lower(),
            "sale_horizon": "sale_horizon" in text,
            "ADVANCE_START": "ADVANCE_START" in text,
            "PROGRAM": "PROGRAM" in text,
            "712": "712" in text,
            "648": "648" in text,
        }
        print("cells", len(cells), "FLAGS", {k: v for k, v in flags.items() if v})
        for i, cell in enumerate(cells):
            src = cell_source(cell)
            for name, payload in writefile_payloads(src):
                sha = hashlib.sha256(payload.replace("\r\n", "\n").encode("utf-8")).hexdigest()
                print(f"WRITEFILE cell={i} name={name!r} bytes={len(payload)} sha256={sha}")
                for line in payload.splitlines():
                    if any(k in line for k in KEYS) and len(line) < 240:
                        print("  ", line)
            if any(
                k in src
                for k in (
                    "CDLL",
                    "ctypes",
                    "agent.so",
                    "EXPECTED_SOURCE_SHA256",
                    "def agent",
                    "%%writefile",
                )
            ):
                print(f"HIT cell={i} {cell.get('cell_type')} {len(src)}")
                n = 0
                for line in src.splitlines():
                    if line.strip():
                        print(" ", line[:200])
                        n += 1
                        if n >= 18:
                            break
        for cell in cells[:3]:
            if cell.get("cell_type") == "markdown":
                title = cell_source(cell).strip().splitlines()
                if title:
                    print("TITLE", title[0][:200])
                for line in title[1:14]:
                    print(" MD", line[:200])
                break


if __name__ == "__main__":
    main()
