"""Extract a public Kaggle agent from a downloaded notebook without executing it."""

from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import py_compile
import zlib
from pathlib import Path
from typing import Any


def _source(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def extract_writefile(notebook: dict[str, Any], filename: str) -> dict[str, str]:
    marker = f"%%writefile {filename}"
    for cell in notebook.get("cells", []):
        source = _source(cell)
        lines = source.splitlines(keepends=True)
        if cell.get("cell_type") == "code" and lines and lines[0].strip() == marker:
            return {filename: "".join(lines[1:])}
    raise ValueError(f"no code cell starts with {marker!r}")


def find_literal(notebook: dict[str, Any], variable: str) -> Any:
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = _source(cell)
        if variable not in source:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            is_target = any(
                isinstance(target, ast.Name) and target.id == variable for target in node.targets
            )
            if not is_target:
                continue
            return ast.literal_eval(node.value)
    raise ValueError(f"literal assignment for {variable!r} was not found")


def extract_literal_dict(notebook: dict[str, Any], variable: str) -> dict[str, str]:
    value = find_literal(notebook, variable)
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{variable} is not a non-empty literal dict")
    all_strings = all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    )
    if not all_strings:
        raise ValueError(f"{variable} must map string paths to string contents")
    return value


def extract_b85_zlib(notebook: dict[str, Any], variable: str, filename: str) -> dict[str, str]:
    payload = find_literal(notebook, variable)
    if not isinstance(payload, str):
        raise ValueError(f"{variable} is not a string literal")
    source = zlib.decompress(base64.b85decode(payload.encode("ascii"))).decode("utf-8")
    return {filename: source}


def materialize(files: dict[str, str], output_dir: Path) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for relative_name, contents in files.items():
        relative = Path(relative_name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe embedded path: {relative_name!r}")
        target = output_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")
        if target.suffix == ".py":
            py_compile.compile(str(target), doraise=True)
        raw = target.read_bytes()
        report.append(
            {
                "path": str(target.resolve()),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "compiled": target.suffix == ".py",
            }
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--mode", choices=("writefile", "literal-dict", "b85-zlib"), required=True
    )
    parser.add_argument("--filename", default="main.py")
    parser.add_argument("--variable", default="TOP_AGENT_FILES")
    args = parser.parse_args()

    notebook = json.loads(args.notebook.read_text(encoding="utf-8"))
    if args.mode == "writefile":
        files = extract_writefile(notebook, args.filename)
    elif args.mode == "literal-dict":
        files = extract_literal_dict(notebook, args.variable)
    else:
        files = extract_b85_zlib(notebook, args.variable, args.filename)

    report = {
        "notebook": str(args.notebook.resolve()),
        "mode": args.mode,
        "files": materialize(files, args.output_dir),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
