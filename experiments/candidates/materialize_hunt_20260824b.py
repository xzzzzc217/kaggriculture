"""Statically materialize 2026-08-24b hunt notebooks. Never executes notebook cells."""

from __future__ import annotations

import ast
import base64
import hashlib
import io
import json
import py_compile
import tarfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUNT = ROOT / "artifacts/public_sources/_hunt_20260824b"
OUT = ROOT / "experiments/candidates"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def extract_writefile(notebook: dict, filename: str) -> str:
    marker = f"%%writefile {filename}"
    for cell in notebook.get("cells", []):
        source = cell_source(cell)
        lines = source.splitlines(keepends=True)
        if cell.get("cell_type") == "code" and lines and lines[0].strip() == marker:
            return "".join(lines[1:])
    raise ValueError(f"no {marker!r}")


def find_blob(notebook: dict) -> str:
    for cell in notebook.get("cells", []):
        source = cell_source(cell)
        if "BLOB" not in source:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if (
                isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "BLOB" for t in node.targets)
            ):
                return ast.literal_eval(node.value)
    raise ValueError("BLOB not found")


def write_main(dest: Path, text: str) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / "main.py"
    raw = text.encode("utf-8")
    if raw.endswith(b"\r\n") or b"\r\n" in raw:
        # keep exact bytes from notebook; do not convert
        pass
    target.write_bytes(raw.replace(b"\r\n", b"\n") if b"\r\n" in raw else raw)
    # notebooks we care about are LF; if mixed, LF-normalize only CRLF pairs
    py_compile.compile(str(target), doraise=True)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return {"path": str(target), "bytes": target.stat().st_size, "sha256": digest}


def unpack_blob(blob: str, dest: Path) -> dict:
    payload = zlib.decompress(base64.b85decode(blob.encode("ascii")))
    dest.mkdir(parents=True, exist_ok=True)
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        text = None
    if text is not None and ("def agent" in text or "class " in text[:4000]):
        rec = write_main(dest, text)
        rec["kind"] = "source-string"
        return rec
    bio = io.BytesIO(payload)
    if tarfile.is_tarfile(bio):
        bio.seek(0)
        with tarfile.open(fileobj=bio, mode="r:*") as archive:
            names = archive.getnames()
            member = next((n for n in names if n.endswith("main.py") or n == "main.py"), None)
            if member is None:
                raise ValueError(f"tar has no main.py: {names[:20]}")
            extracted = archive.extractfile(member)
            assert extracted is not None
            rec = write_main(dest, extracted.read().decode("utf-8"))
            rec["kind"] = "tar"
            rec["tar_names"] = names
            return rec
    raise ValueError(f"unrecognized blob prefix {payload[:40]!r}")


def main() -> None:
    report: dict = {"agents": []}

    v21 = json.loads((HUNT / "v21-multi-route-agent-sell-divergence-guarder.ipynb").read_text(encoding="utf-8"))
    rec = write_main(OUT / "mugundhjb_v21_guarder", extract_writefile(v21, "main.py"))
    rec["agent"] = "mugundhjb_v21_guarder"
    report["agents"].append(rec)
    print(json.dumps(rec), flush=True)

    eco = json.loads((HUNT / "economics-driven-rule-agent-ecobot-v4.ipynb").read_text(encoding="utf-8"))
    rec = write_main(OUT / "ecobot_v4", extract_writefile(eco, "main.py"))
    rec["agent"] = "ecobot_v4"
    report["agents"].append(rec)
    print(json.dumps(rec), flush=True)

    for slug, name in (
        ("kaggriculture-adaptive-counterbook.ipynb", "llccqq624_counterbook"),
        ("kaggriculture-the-shops-remember-the-route.ipynb", "llccqq624_shops"),
    ):
        notebook = json.loads((HUNT / slug).read_text(encoding="utf-8"))
        rec = unpack_blob(find_blob(notebook), OUT / name)
        rec["agent"] = name
        rec["notebook"] = slug
        report["agents"].append(rec)
        print(json.dumps({k: rec[k] for k in rec if k != "tar_names"}), flush=True)

    known = {
        "boatlee_v21": OUT / "boatlee_v21_r1/main.py",
        "flexonafft": OUT / "flexonafft_rerun/main.py",
        "ecobot_v2": OUT / "joymietalicuad_ecobot_v2/main.py",
        "h2": ROOT / "main.py",
        "moon_v127": OUT / "prvsiyan_moon_rerun/main.py",
        "tetsutani_rtt": OUT / "tetsutani_read_the_town/main.py",
        "steven_strongest": OUT / "stevenleehans_strongest_farmer/main.py",
    }
    known_sha = {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in known.items()
        if path.exists()
    }
    for rec in report["agents"]:
        matches = [name for name, digest in known_sha.items() if digest == rec["sha256"]]
        rec["duplicate_of"] = matches
    report["known_sha"] = known_sha
    dest = OUT / "materialize_hunt_20260824b.json"
    dest.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
