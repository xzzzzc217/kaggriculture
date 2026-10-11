"""Static b85/zlib payload extract. No notebook cell execution."""

from __future__ import annotations

import ast
import base64
import hashlib
import json
import py_compile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260920"
OUT = ROOT / "experiments/candidates/_hunt_20260920_extract"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def literal_str_assign(src: str, names: tuple[str, ...]) -> str | None:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        if isinstance(value, str):
            return value
    return None


def decode_payload(raw: str) -> bytes:
    # try b85+zlib first, then b64+zlib, then gzip+b64
    last_err = None
    for decoder in (base64.b85decode, base64.b64decode):
        try:
            blob = decoder(raw.encode("ascii"))
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
        for unzip in (zlib.decompress,):
            try:
                return unzip(blob)
            except Exception as exc:  # noqa: BLE001
                last_err = exc
        try:
            import gzip

            return gzip.decompress(blob)
        except Exception as exc:  # noqa: BLE001
            last_err = exc
    raise RuntimeError(f"decode failed: {last_err}")


def extract_from_cell(src: str) -> bytes | None:
    payload = literal_str_assign(src, ("_PAYLOAD", "PAYLOAD", "SOURCE", "source_b85"))
    if payload is None:
        # nathan style: SOURCE or source_bytes constructed later; look for a huge string assign
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return None
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            if isinstance(value, str) and len(value) > 10_000:
                payload = value
                break
    if payload is None:
        return None
    return decode_payload(payload)


def write_agent(dest: Path, data: bytes, expected: str | None) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    compile_ok = False
    compile_err = None
    if dest.suffix == ".py" or dest.name == "main.py":
        try:
            py_compile.compile(str(dest), doraise=True)
            compile_ok = True
        except Exception as exc:  # noqa: BLE001
            compile_err = repr(exc)
    rec = {
        "out": str(dest.relative_to(ROOT).as_posix()),
        "bytes": len(data),
        "sha256": digest,
        "expected": expected,
        "sha_match": (digest == expected) if expected else None,
        "compile_ok": compile_ok,
        "compile_err": compile_err,
        "has_agent": b"def agent" in data,
    }
    print(json.dumps(rec, ensure_ascii=False), flush=True)
    return rec


def main() -> None:
    jobs = [
        (
            "thomastschinkel__the-metav4-farm-submission-v13",
            "the-metav4-farm-submission-v13.ipynb",
            5,
            "9d63494603f88219857a3101d7dc19cc750ded04e5886732ee428580326967d9",
            "metav4_v13/main.py",
        ),
        (
            "guruprasaathas111__kaggriculture-master-engine-v4",
            "kaggriculture-master-engine-v4.ipynb",
            5,
            "9d63494603f88219857a3101d7dc19cc750ded04e5886732ee428580326967d9",
            "guru_v4_reprint/main.py",
        ),
        (
            "nathanjacob__kaggriculture-pipe16-idle-workers",
            "kaggriculture-pipe16-idle-workers.ipynb",
            6,
            "827ddf2997fa442e80baadebc4cc91ffaeedec1ff333c1fa7d872b0f1d448181",
            "nathan_pipe16/main.py",
        ),
        (
            "tetsutani__demand-preserving-turn-sale-timing",
            "demand-preserving-turn-sale-timing.ipynb",
            9,
            "1aa3717b3201997a95920c80cf5612c23f78f8716c7b1084b6a345ca4eae7e4f",
            "tetsutani_demand/main.py",
        ),
        (
            "jaxa623__2802-two-identical-agents-90-points-apart",
            "2802-two-identical-agents-90-points-apart.ipynb",
            8,
            None,
            "jaxa_2802/main.py",
        ),
    ]
    reports = []
    for slug, nb_name, cell_index, expected, rel_out in jobs:
        path = DIR / slug / nb_name
        nb = json.loads(path.read_text(encoding="utf-8"))
        src = cell_source((nb.get("cells") or [])[cell_index])
        print("JOB", slug, "cell", cell_index, "chars", len(src), flush=True)
        data = extract_from_cell(src)
        if data is None:
            print("FAIL extract", slug, flush=True)
            reports.append({"slug": slug, "ok": False, "reason": "extract_none"})
            continue
        rec = write_agent(OUT / rel_out, data, expected)
        rec["slug"] = slug
        rec["ok"] = True
        reports.append(rec)
    out = ROOT / "experiments/20260920_gold_payloads.json"
    out.write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out, flush=True)


if __name__ == "__main__":
    main()
