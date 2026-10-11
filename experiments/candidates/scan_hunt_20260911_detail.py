"""Deeper static notes for 20260911 hunt. No cell exec. No live agent extract."""

from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260911"
PRIOR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910b"


def src(cell):
    s = cell.get("source") or ""
    return "".join(s) if isinstance(s, list) else str(s)


def dump(folder: str, needles: list[str], around: int = 1) -> None:
    path = next(DIR.glob(folder + "/**/*.ipynb"))
    nb = json.loads(path.read_text(encoding="utf-8"))
    print("=" * 78)
    print(path.parent.name, "cells", len(nb.get("cells") or []))
    for i, cell in enumerate(nb.get("cells") or []):
        text = src(cell)
        low = text.lower()
        if cell.get("cell_type") == "markdown" and i < 4:
            print(f"-- md {i} --")
            for line in text.strip().splitlines()[:10]:
                print(line[:200])
        if any(n.lower() in low for n in needles):
            print(f"-- hit cell {i} {cell.get('cell_type')} {len(text)} --")
            lines = text.splitlines()
            shown = 0
            for j, line in enumerate(lines):
                if any(n.lower() in line.lower() for n in needles):
                    lo = max(0, j - around)
                    hi = min(len(lines), j + around + 1)
                    for k in range(lo, hi):
                        print(f"{k:4d}|{lines[k][:220]}")
                    print("    ...")
                    shown += 1
                    if shown >= 18:
                        print("  (truncated hits)")
                        break


def sha_of_writefile(folder: str) -> None:
    path = next(DIR.glob(folder + "/**/*.ipynb"))
    nb = json.loads(path.read_text(encoding="utf-8"))
    for i, cell in enumerate(nb.get("cells") or []):
        text = src(cell)
        if text.lstrip().startswith("%%writefile"):
            first, _, rest = text.partition("\n")
            name = first.split("%%writefile", 1)[-1].strip()
            payload = rest.replace("\r\n", "\n")
            print(
                f"WRITEFILE {folder} cell={i} {name!r} bytes={len(payload)} "
                f"sha256={hashlib.sha256(payload.encode()).hexdigest()}"
            )


def inspect_navaz_tar() -> None:
    path = next(DIR.glob("navazshfathi__shop-router-0908/**/*.ipynb"))
    nb = json.loads(path.read_text(encoding="utf-8"))
    text = "\n".join(src(c) for c in nb.get("cells") or [])
    marker = "Path(\"submission.tar.gz\").write_bytes(base64.b64decode('"
    if marker not in text:
        # fallback
        start = text.find("base64.b64decode('")
        print("NAV AZ marker missing, start", start)
        return
    rest = text.split("base64.b64decode('", 1)[1]
    b64 = rest.split("')", 1)[0]
    blob = base64.b64decode(b64)
    print("NAV AZ tar.gz bytes", len(blob), "sha256", hashlib.sha256(blob).hexdigest())
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        names = tar.getnames()
        print("NAV AZ members", names)
        for info in tar.getmembers():
            print(" ", info.name, info.size, oct(info.mode))
            if info.isfile() and info.size < 400_000:
                data = tar.extractfile(info).read()
                print("   sha256", hashlib.sha256(data).hexdigest())
                sample = data[:800].decode("utf-8", errors="replace")
                for needle in ("ctypes", "CDLL", "agent.so", "dylib", "%%writefile", "DECISIONS", "ROUTE_STEP"):
                    if needle in sample or needle.encode() in data[:4000]:
                        print("   HIT", needle)
                if info.name.endswith((".py", ".txt", ".md", ".json")):
                    for line in sample.splitlines()[:12]:
                        print("   |", line[:180])


def compare_dmitrii() -> None:
    new_a = next(DIR.glob("dmitriigluzdov__kaggriculture-two-coins-one-sheep/*.ipynb"))
    new_b = next(DIR.glob("dmitriigluzdov__kaggriculture-herd-safe-sale-window/*.ipynb"))
    old = PRIOR / "dmitriigluzdov__kaggriculture-two-coins-one-sheep-lb-2700" / "kaggriculture-two-coins-one-sheep-lb-2700.ipynb"
    for label, path in (("new_two_coins", new_a), ("herd_safe", new_b), ("old_lb2700", old)):
        raw = path.read_bytes()
        print(label, path.name, "bytes", len(raw), "sha256", hashlib.sha256(raw).hexdigest())
    a = new_a.read_bytes()
    b = new_b.read_bytes()
    print("two_coins vs herd_safe identical", a == b, "len_delta", len(a) - len(b))


def xuan_steps() -> None:
    path = next(DIR.glob("xuantianfengwu__kaggriculture-fixed-hybrid-core/**/*.ipynb"))
    nb = json.loads(path.read_text(encoding="utf-8"))
    text = "\n".join(src(c) for c in nb.get("cells") or [])
    for needle in ("step", "216", "226", "144", "288", "reselect", "later", "BUY_LAND", "COW", "SHEEP"):
        print("XUAN count", needle, text.count(needle))


if __name__ == "__main__":
    sha_of_writefile("xuantianfengwu__kaggriculture-fixed-hybrid-core")
    sha_of_writefile("ahmedberatozer__notebooka4fc70fd19")
    sha_of_writefile("dmitriigluzdov__kaggriculture-herd-safe-sale-window")
    sha_of_writefile("dmitriigluzdov__kaggriculture-two-coins-one-sheep")
    compare_dmitrii()
    xuan_steps()
    dump(
        "xuantianfengwu__kaggriculture-fixed-hybrid-core",
        ["BUY_LAND", "step", "COW", "SHEEP", "def agent", "later", "216"],
        1,
    )
    dump(
        "destbreso__who-is-beating-you-and-is-it-you",
        ["writefile", "agent", "replay", "leaderboard", "ctypes", "later"],
        1,
    )
    dump(
        "ahmedberatozer__notebooka4fc70fd19",
        ["216<=step", "reselect", "DECISIONS", "ROUTE_STEP", "226", "360", "433", "ctypes", "CDLL", "later-block"],
        1,
    )
    dump(
        "dmitriigluzdov__kaggriculture-herd-safe-sale-window",
        ["sale_horizon", "CDLL", "ctypes", "agent.so", "SALE_HORIZON", "ROUTE_STEP", "herd"],
        1,
    )
    dump(
        "dmitriigluzdov__kaggriculture-two-coins-one-sheep",
        ["sale_horizon", "CDLL", "ctypes", "agent.so", "SALE_HORIZON", "ROUTE_STEP"],
        1,
    )
    dump(
        "navazshfathi__shop-router-0908",
        ["ctypes", "CDLL", "agent.so", "base64", "observation.py"],
        1,
    )
    inspect_navaz_tar()
