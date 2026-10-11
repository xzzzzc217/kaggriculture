"""Static extracts from 2026-09-10 gate hunt. No notebook cell exec."""

from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import json
import py_compile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUNT = ROOT / "artifacts/public_sources/_hunt_20260910_gate"
CUT14 = ROOT / "experiments/candidates/y3uanm_router_v5/main.py"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def strip_writefile(src: str) -> str:
    lines = src.splitlines(keepends=True)
    if lines and lines[0].startswith("%%writefile"):
        return "".join(lines[1:])
    return src


def write_py(path: Path, text: str) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = text.encode("utf-8").replace(b"\r\n", b"\n")
    if not raw.endswith(b"\n"):
        raw += b"\n"
    path.write_bytes(raw)
    py_compile.compile(str(path), doraise=True)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    src = path.read_text(encoding="utf-8")
    return {
        "path": str(path.as_posix()),
        "sha256": digest,
        "bytes": path.stat().st_size,
        "has_agent": "def agent(" in src,
        "ctypes": "ctypes" in src or "CDLL" in src or "agent.so" in src,
        "decisions": "DECISIONS" in src,
        "step_ge_144": "step>=144" in src or "step >= 144" in src or "ROUTE_STEP = 144" in src,
        "step_ge_216": bool(re.search(r"(step|t|turn).{0,12}(>=|>|==).{0,6}2(1[7-9]|[2-9]\d)", src)),
        "mentions": {
            "226": "226" in src,
            "241": "241" in src,
            "360": "360" in src,
            "385": "385" in src,
            "433": "433" in src,
            "648": "648" in src,
            "712": "712" in src,
        },
    }


def extract_writefile(nb_path: Path, out_path: Path, filename: str = "main.py") -> dict:
    notebook = json.loads(nb_path.read_text(encoding="utf-8"))
    for cell in notebook.get("cells") or []:
        src = cell_source(cell)
        if src.startswith(f"%%writefile {filename}") or src.startswith(f"%%writefile {filename}\n"):
            rec = write_py(out_path, strip_writefile(src))
            rec["source_nb"] = str(nb_path.as_posix())
            return rec
    raise SystemExit(f"no writefile {filename} in {nb_path}")


def extract_king() -> dict:
    nb_path = HUNT / "yamakawanin__king-v4e-rc4/king-v4e-rc4.ipynb"
    notebook = json.loads(nb_path.read_text(encoding="utf-8"))
    src = cell_source(notebook["cells"][7])
    match = re.search(
        r'EXPECTED_SOURCE_SHA256 = "([0-9a-f]+)".*?RC4_SOURCE_GZIP_B64 = """(.*?)"""',
        src,
        flags=re.S,
    )
    if not match:
        raise SystemExit("king payload not found")
    expected = match.group(1)
    payload = gzip.decompress(base64.b64decode(match.group(2)))
    digest = hashlib.sha256(payload).hexdigest()
    if digest != expected:
        raise SystemExit(f"king sha mismatch {digest} != {expected}")
    out = ROOT / "experiments/candidates/yamakawanin_king_v4e_rc4/main.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(payload if payload.endswith(b"\n") else payload + b"\n")
    py_compile.compile(str(out), doraise=True)
    text = out.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(out.as_posix()),
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "bytes": out.stat().st_size,
        "has_agent": "def agent(" in text,
        "ctypes": "ctypes" in text or "CDLL" in text or "agent.so" in text,
        "mentions": {k: (k in text) for k in ("226", "241", "360", "385", "433", "648", "712", "YARN")},
        "source_nb": str(nb_path.as_posix()),
    }


def main() -> None:
    cut14_sha = hashlib.sha256(CUT14.read_bytes()).hexdigest()
    recs = {
        "cut14": {"path": str(CUT14.as_posix()), "sha256": cut14_sha},
        "y3uanm_v4": extract_writefile(
            HUNT / "y3uanm__kaggriculture-market-impact-router-v4/kaggriculture-market-impact-router-v4.ipynb",
            ROOT / "experiments/candidates/y3uanm_router_v4/main.py",
        ),
        "thomas_745": extract_writefile(
            HUNT
            / "thomastschinkel__kaggriculture-public-state-router-74-5-win-rate"
            / "kaggriculture-public-state-router-74-5-win-rate.ipynb",
            ROOT / "experiments/candidates/thomastschinkel_psr_745/main.py",
        ),
        "thomas_938": extract_writefile(
            HUNT
            / "thomastschinkel__kaggriculture-93-8-win-rate-public-state-router"
            / "kaggriculture-93-8-win-rate-public-state-router.ipynb",
            ROOT / "experiments/candidates/thomastschinkel_psr_938/main.py",
        ),
        "aurax7_v2": extract_writefile(
            HUNT
            / "aurax7__kaggriculture-shop-router-reactive-v2"
            / "kaggriculture-shop-router-reactive-v2.ipynb",
            ROOT / "experiments/candidates/aurax7_reactive_v2/main.py",
        ),
        "yhay81_0909": extract_writefile(
            HUNT / "yhay81__shop-router-0909/shop-router-0909.ipynb",
            ROOT / "experiments/candidates/yhay81_shop_router_0909/main.py",
        ),
        "king_v4e_rc4": extract_king(),
    }
    recs["y3uanm_v4_eq_cut14"] = recs["y3uanm_v4"]["sha256"] == cut14_sha
    recs["thomas_745_eq_cut14"] = recs["thomas_745"]["sha256"] == cut14_sha
    recs["y3uanm_v4_eq_thomas_745"] = recs["y3uanm_v4"]["sha256"] == recs["thomas_745"]["sha256"]
    print(json.dumps(recs, indent=2))


if __name__ == "__main__":
    main()
