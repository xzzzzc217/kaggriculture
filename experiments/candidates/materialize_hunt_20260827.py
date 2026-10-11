"""Statically materialize 2026-08-27 hunt agents. Never executes notebook cells."""

from __future__ import annotations

import ast
import base64
import hashlib
import json
import py_compile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUNT = ROOT / "artifacts/public_sources/_hunt_20260827"
OUT = ROOT / "experiments/candidates"

KNOWN = {
    "h2": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
    "shops_v43": "69f06a802b62aa08f28705dab5728eb924bb6a7c23ffe0164f65b104cc3dadf3",
    "boatlee_v21": "c6f96a8521dc9aa369b6f27e5b36b9d481e5c1688f50c8ca215c3bb53f1f9eb8",
    "moon_v127": "a7a6b4f5317938fdbeb79b54fa1ceab9fc884a5f027f61a3b65cf7a212dd6676",
    "counterbook": "c26402b67a0d04a46348353069645b1a49c3cb3df6fa35d8adbbdbeae4",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def find_literal(notebook: dict, variable: str) -> object:
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell_source(cell)
        if variable not in source:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if any(isinstance(t, ast.Name) and t.id == variable for t in node.targets):
                return ast.literal_eval(node.value)
    raise ValueError(f"{variable} not found")


def extract_writefile(notebook: dict, filename: str) -> str:
    marker = f"%%writefile {filename}"
    for cell in notebook.get("cells", []):
        source = cell_source(cell)
        lines = source.splitlines(keepends=True)
        if cell.get("cell_type") == "code" and lines and lines[0].strip() == marker:
            return "".join(lines[1:])
    raise ValueError(f"no {marker!r}")


def write_main(dest: Path, raw: bytes) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / "main.py"
    if b"\r\n" in raw:
        raw = raw.replace(b"\r\n", b"\n")
    target.write_bytes(raw)
    py_compile.compile(str(target), doraise=True)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    dupes = [name for name, sha in KNOWN.items() if sha == digest]
    return {
        "path": str(target),
        "bytes": target.stat().st_size,
        "sha256": digest,
        "duplicate_of": dupes,
    }


def blob_to_source(blob: str) -> bytes:
    return zlib.decompress(base64.b85decode(blob.encode("ascii")))


def main() -> None:
    rows = []

    pqs = json.loads(
        (
            HUNT
            / "llccqq624__kaggriculture-premium-queue-split"
            / "kaggriculture-premium-queue-split.ipynb"
        ).read_text(encoding="utf-8")
    )
    rec = write_main(OUT / "llccqq624_pqs", blob_to_source(find_literal(pqs, "BLOB")))
    rec["agent"] = "llccqq624_pqs"
    rec["kind"] = "BLOB"
    rec["expected_live_analog"] = "Jiachen Li"
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    v48 = json.loads(
        (
            HUNT
            / "kaitofukami__40-40-early-floor-39-46-top-10-v48-fast-routes"
            / "40-40-early-floor-39-46-top-10-v48-fast-routes.ipynb"
        ).read_text(encoding="utf-8")
    )
    rec = write_main(OUT / "kaitofukami_v48", blob_to_source(find_literal(v48, "payload")))
    rec["agent"] = "kaitofukami_v48"
    rec["kind"] = "payload"
    rec["notebook_sha"] = "dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a"
    rec["sha_match"] = rec["sha256"] == rec["notebook_sha"]
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    v43 = json.loads(
        (
            HUNT
            / "kaitofukami__103-128-fresh-public-v43-sparse-shop-hybrid"
            / "103-128-fresh-public-v43-sparse-shop-hybrid.ipynb"
        ).read_text(encoding="utf-8")
    )
    rec = write_main(
        OUT / "kaitofukami_v43_sparse", blob_to_source(find_literal(v43, "payload"))
    )
    rec["agent"] = "kaitofukami_v43_sparse"
    rec["kind"] = "payload"
    rec["notebook_sha"] = "69f06a802b62aa08f28705dab5728eb924bb6a7c23ffe0164f65b104cc3dadf3"
    rec["sha_match"] = rec["sha256"] == rec["notebook_sha"]
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    guard = json.loads(
        (
            HUNT
            / "reyhanksatria__kaggriculture-adaptive-shop-guard"
            / "kaggriculture-adaptive-shop-guard.ipynb"
        ).read_text(encoding="utf-8")
    )
    rec = write_main(OUT / "shop_guard", blob_to_source(find_literal(guard, "BLOB")))
    rec["agent"] = "shop_guard"
    rec["kind"] = "BLOB"
    rec["forks"] = ["reyhanksatria", "morinokuma3", "hboyang"]
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    yama = json.loads(
        (
            HUNT
            / "yamakawanin__kaggriculture-adaptive-public-state-multi-route"
            / "kaggriculture-adaptive-public-state-multi-route.ipynb"
        ).read_text(encoding="utf-8")
    )
    rec = write_main(OUT / "yamakawanin_v21", extract_writefile(yama, "main.py").encode("utf-8"))
    rec["agent"] = "yamakawanin_v21"
    rec["kind"] = "writefile"
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    evelyn = (
        HUNT
        / "evelyn3976__kaggriculture-adaptive-market-scheduler-v1"
        / "kaggriculture-adaptive-market-scheduler-v1.py"
    )
    rec = write_main(OUT / "evelyn_scheduler_v1", evelyn.read_bytes())
    rec["agent"] = "evelyn_scheduler_v1"
    rec["kind"] = "raw-py"
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    v24 = HUNT / "lixiuqixiaoke__v24-robustmarketlead" / "v24-robustmarketlead.py"
    rec = write_main(OUT / "lixiuqixiaoke_v24", v24.read_bytes())
    rec["agent"] = "lixiuqixiaoke_v24"
    rec["kind"] = "raw-py"
    rows.append(rec)
    print(json.dumps(rec, indent=2))

    unique = [r for r in rows if not r["duplicate_of"]]
    report = {
        "date": "2026-08-27",
        "agents": rows,
        "unique_new": [r["agent"] for r in unique],
        "duplicates": [r["agent"] for r in rows if r["duplicate_of"]],
    }
    dest = OUT / "materialize_hunt_20260827.json"
    dest.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("WROTE", dest)
    print("unique_new", report["unique_new"])
    print("duplicates", report["duplicates"])


if __name__ == "__main__":
    main()
