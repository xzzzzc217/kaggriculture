"""Static inspect of 20260920 gold-band hunt notebooks. No cell exec."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260920"
OUT = ROOT / "experiments/candidates/_hunt_20260920_extract"
CUT14 = "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
CUT15 = "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
CUT16 = "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"
H2 = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
FLAGS = [
    "%%writefile",
    "agent.so",
    "ctypes",
    "CDLL",
    "SOURCE_BYTES",
    "EXPECTED_MAIN_SHA256",
    "EXPECTED_SOURCE_SHA256",
    "def agent",
    "PufferLib",
    "submission.tar.gz",
]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def extract_join_bytes(src: str) -> bytes | None:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
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


def tag_sha(digest: str) -> str:
    known = {
        CUT14: "CUT14",
        CUT15: "CUT15",
        CUT16: "CUT16",
        H2: "H2",
    }
    return known.get(digest, "")


def inspect_payload(label: str, payload: str, dest: Path) -> dict:
    raw = payload.encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    rec = {
        "label": label,
        "bytes": len(raw),
        "sha256": digest,
        "known": tag_sha(digest) or "NEW",
        "out": str(dest.relative_to(ROOT).as_posix()),
        "has_agent": "def agent" in payload or "def agent(" in payload,
        "ctypes": any(x in payload for x in ("ctypes", "CDLL", "agent.so")),
        "writefile_ok": True,
    }
    print(
        "PAYLOAD",
        label,
        "bytes",
        rec["bytes"],
        "sha256",
        digest,
        rec["known"],
        "agent",
        rec["has_agent"],
        "ctypes",
        rec["ctypes"],
        flush=True,
    )
    return rec


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    reports = []
    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        notebook = json.loads(raw.decode("utf-8"))
        rel = path.relative_to(DIR).as_posix()
        text = raw.decode("utf-8", errors="ignore")
        print("=" * 72, flush=True)
        print(rel, "bytes", len(raw), "cells", len(notebook.get("cells") or []), flush=True)
        flags = [f for f in FLAGS if f in text]
        print("flags", flags, flush=True)
        rec = {
            "notebook": rel,
            "bytes": len(raw),
            "cells": len(notebook.get("cells") or []),
            "flags": flags,
            "payloads": [],
        }
        slug = path.parent.name
        for index, cell in enumerate(notebook.get("cells") or []):
            src = cell_source(cell)
            stripped = src.lstrip()
            if stripped.startswith("%%writefile"):
                first, _, rest = src.partition("\n")
                name = Path(first.split("%%writefile", 1)[-1].strip()).name or "main.py"
                payload = rest.replace("\r\n", "\n")
                if not payload.endswith("\n"):
                    payload += "\n"
                dest = OUT / slug / name
                rec["payloads"].append(inspect_payload(f"{rel}:cell{index}:{name}", payload, dest))
                continue
            joined = extract_join_bytes(src)
            if joined is not None:
                dest = OUT / slug / "SOURCE_BYTES_main.py"
                try:
                    text_payload = joined.decode("utf-8")
                except UnicodeDecodeError:
                    dest = OUT / slug / "SOURCE_BYTES.bin"
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(joined)
                    print("SOURCE_BYTES binary", rel, "cell", index, "bytes", len(joined), flush=True)
                    rec["payloads"].append(
                        {
                            "label": f"{rel}:cell{index}:SOURCE_BYTES.bin",
                            "bytes": len(joined),
                            "sha256": hashlib.sha256(joined).hexdigest(),
                            "known": "NEW",
                            "binary": True,
                        }
                    )
                    continue
                rec["payloads"].append(
                    inspect_payload(f"{rel}:cell{index}:SOURCE_BYTES", text_payload, dest)
                )
        # markdown claims
        md = "\n".join(cell_source(c) for c in notebook.get("cells") or [] if c.get("cell_type") == "markdown")
        for pat in (
            r"2944\.7",
            r"2945",
            r"2950",
            r"submission 56\d+",
            r"Live ladder",
            r"40 – 0",
            r"40-0",
        ):
            m = re.search(pat, md, flags=re.I)
            if m:
                print("md_hit", pat, m.group(0)[:80], flush=True)
        reports.append(rec)
        print("payload_count", len(rec["payloads"]), flush=True)
    summary_path = ROOT / "experiments/20260920_hunt_extract.json"
    summary_path.write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
    print("WROTE", summary_path, flush=True)


if __name__ == "__main__":
    main()
