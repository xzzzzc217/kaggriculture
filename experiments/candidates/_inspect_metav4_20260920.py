"""Deeper static inspect of notebooks that flagged writefile but extracted nothing."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260920"
TARGETS = [
    "thomastschinkel__the-metav4-farm-submission-v13",
    "guruprasaathas111__kaggriculture-master-engine-v4",
    "guruprasaathas111__kaggriculture-master-engine-v3",
    "tetsutani__demand-preserving-turn-sale-timing",
    "nathanjacob__kaggriculture-pipe16-idle-workers",
    "jaxa623__2802-two-identical-agents-90-points-apart",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    for slug in TARGETS:
        nbs = list((DIR / slug).glob("*.ipynb"))
        print("=" * 72)
        print(slug, "nbs", [p.name for p in nbs], flush=True)
        for path in nbs:
            nb = json.loads(path.read_text(encoding="utf-8"))
            for i, cell in enumerate(nb.get("cells") or []):
                src = cell_source(cell)
                ctype = cell.get("cell_type")
                head = src[:180].replace("\n", " | ")
                hits = []
                for needle in (
                    "%%writefile",
                    "SOURCE_BYTES",
                    "def agent",
                    "EXPECTED_MAIN_SHA256",
                    "open('main.py'",
                    'open("main.py"',
                    "Path('main.py'",
                    "write_text",
                    "submission.py",
                    "agent.so",
                    "b85",
                    "base64",
                    "zlib.decompress",
                    "lzma",
                ):
                    if needle in src:
                        hits.append(needle)
                if hits or ctype == "code":
                    print(
                        f"  cell{i:02d} {ctype:8s} chars={len(src):7d} hits={hits} head={head[:140]!r}",
                        flush=True,
                    )
                if "%%writefile" in src:
                    idx = src.find("%%writefile")
                    print("    writefile_at", idx, "context", src[max(0, idx - 40) : idx + 80].replace("\n", " | "), flush=True)
                for m in re.finditer(r"EXPECTED_[A-Z_]*SHA256\s*=\s*['\"]([0-9a-f]{64})['\"]", src):
                    print("    expected_sha", m.group(0)[:90], flush=True)
                if "def agent" in src and ctype == "code" and "%%writefile" not in src[:40]:
                    digest = hashlib.sha256(src.encode("utf-8")).hexdigest()
                    print("    inline_agent_sha", digest, "bytes", len(src.encode("utf-8")), flush=True)


if __name__ == "__main__":
    main()
