"""Decode Moon V189C embedded payload to inspect shop/sell logic."""

from __future__ import annotations

import ast
import base64
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "experiments/candidates/prvsiyan_moon_v189c/main.py"
OUT = ROOT / "experiments/candidates/prvsiyan_moon_v189c/decoded_ramesh.py"


def main() -> None:
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    payload = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "b85decode":
            if node.args and isinstance(node.args[0], ast.Constant):
                payload = node.args[0].value
                break
    if not isinstance(payload, str):
        raise SystemExit("no b85 payload")
    blob = zlib.decompress(base64.b85decode(payload)).decode("utf-8")
    OUT.write_text(blob, encoding="utf-8")
    print("WROTE", OUT, "bytes", len(blob), "lines", blob.count("\n") + 1)


if __name__ == "__main__":
    main()
