"""Headers and flags from 2026-09-10 hunt notebooks. No cell exec."""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260910"
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
    "PufferLib",
    "agent.dylib",
    ".so",
    "native",
    "later-block",
    "later_block",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def main() -> None:
    for path in sorted(DIR.rglob("*")):
        if path.suffix.lower() not in {".ipynb", ".py", ".json", ".md"}:
            continue
        if path.name == "kernel-metadata.json":
            meta = json.loads(path.read_text(encoding="utf-8"))
            print("=" * 70)
            print("META", path.parent.name, {k: meta.get(k) for k in ("id", "title", "code_file", "language", "kernel_type", "is_private")})
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        print("=" * 70)
        print(path.relative_to(DIR), "bytes", len(raw), "suffix", path.suffix)
        hits = [f for f in FLAGS if f.lower() in text.lower() or f in text]
        print("flags", hits)
        if path.suffix == ".ipynb":
            notebook = json.loads(raw.decode("utf-8"))
            cells = notebook.get("cells") or []
            print("cells", len(cells))
            for index, cell in enumerate(cells[:8]):
                source = cell_source(cell)
                first = source.strip().splitlines()[:10]
                if not first:
                    continue
                print(f"-- cell {index} {cell.get('cell_type')} {len(source)} --")
                for line in first:
                    print(line[:220])
            # extra: search later-block-ish snippets
            for index, cell in enumerate(cells):
                source = cell_source(cell)
                low = source.lower()
                if any(k in low for k in ("%%writefile", "ctypes", "cdll", "agent.so", "reselect", "later")):
                    print(f".. hit cell {index} {cell.get('cell_type')} {len(source)}")
                    for line in source.strip().splitlines()[:12]:
                        print("   ", line[:220])
        else:
            for line in text.splitlines()[:12]:
                print(line[:220])


if __name__ == "__main__":
    main()
