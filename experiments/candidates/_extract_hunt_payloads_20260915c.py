"""Static reconstruct of 20260915c hunt payloads. No cell exec."""

from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import json
import re
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260915c"
CUT14 = "acf7c664"
CUT15 = "b87a27ed"
CUT16 = "26ffba52"
KNOWN = {
    "728fdfb4": "ahmed_v42",
    "8951ff93": "ahmed_v41",
    "919fc1d6": "ahmed_v43",
    "77cf6772": "yhay81_0913",
    "7a37397f": "nathan_pipe4",
    "01f0cd47": "harvestforge",
    "85c8b532": "alperen_scored",
    "acf7c664": "cut14",
    "b87a27ed": "cut15",
    "26ffba52": "cut16",
    "602ae8be": "kenan_shop0909",
    "5dc0c68c": "timed_six_cow",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def inspect(label: str, payload: str, digest: str) -> None:
    print("PAYLOAD", label, "bytes", len(payload.encode("utf-8")), "sha256", digest, "known", KNOWN.get(digest[:8], "NEW"))
    print(" ctypes", "ctypes" in payload or "CDLL" in payload or "agent.so" in payload)
    print(" 144/648", payload.count("144"), payload.count("648"), "288", payload.count("288"), "712", payload.count("712"))
    print(" ROUTE_STEP", "ROUTE_STEP" in payload, "PROGRAM", "PROGRAM" in payload)
    print(" sale_horizon", "sale_horizon" in payload, "ADVANCE_START", "ADVANCE_START" in payload)
    print(" reselect", "reselect" in payload.lower(), "Shop0909", "Shop0909" in payload)
    print(" 216<=step<=227", "216<=step<=227" in payload.replace(" ", ""))
    for needle in (
        "if step>=144",
        "if step>=216",
        "if step>=226",
        "if step>=288",
        "if step>=360",
        "if step>=432",
        "if step>=576",
        "if step>=648",
        "if step==712",
        "ROUTE_STEP",
        "PROGRAM",
        "_R37_HORIZONS",
        "C9",
    ):
        n = payload.count(needle)
        if n:
            print(f"  count[{needle}]={n}")
    lines = [ln for ln in payload.splitlines() if "if step" in ln or "elif step" in ln]
    print(" if-step n", len(lines))
    for ln in lines[:24]:
        print("  ", ln[:220])
    try:
        tree = ast.parse(payload)
        print(" ast_ok", True, "n_nodes", sum(1 for _ in ast.walk(tree)))
    except SyntaxError as exc:
        print(" ast_ok", False, exc)


def decode_gzip_b64(blob: str) -> bytes:
    raw = base64.b64decode(blob)
    if raw[:2] == b"\x1f\x8b":
        return gzip.decompress(raw)
    try:
        return gzip.decompress(raw)
    except OSError:
        return zlib.decompress(raw)


def decode_b85_gzip(blob: str) -> bytes:
    raw = base64.b85decode(blob)
    if raw[:2] == b"\x1f\x8b":
        return gzip.decompress(raw)
    try:
        return gzip.decompress(raw)
    except OSError:
        return zlib.decompress(raw)


def write_payload(path: Path, payload: str) -> str:
    if not payload.endswith("\n"):
        payload += "\n"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    path.write_bytes(payload.encode("utf-8"))
    print("WROTE", path, "sha", digest)
    return digest


def extract_turn_one() -> None:
    nb_path = DIR / "alperen5252525__turn-one-market-advantage-kaggriculture" / "turn-one-market-advantage-kaggriculture.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][7])
    expected = re.search(r"EXPECTED_SHA256\s*=\s*'([a-f0-9]{64})'", src)
    b85 = re.search(r"B85_SOURCE\s*=\s*'([^']+)'", src)
    print("=" * 72)
    print("turn-one expected", expected.group(1) if expected else None, "b85", bool(b85))
    raw = gzip.decompress(base64.b85decode(b85.group(1)))
    payload = raw.decode("utf-8")
    digest = write_payload(nb_path.parent / "main.py", payload)
    inspect("turn-one", payload, digest)


def extract_v43_reprint() -> None:
    nb_path = DIR / "alperen5252525__market-smart-recovery-kaggriculture" / "market-smart-recovery-kaggriculture.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][4])
    print("=" * 72)
    expected = re.search(r"EXPECTED_MAIN_SHA256\s*=\s*'([a-f0-9]{64})'", src)
    print("market-smart expected", expected.group(1) if expected else None)
    ns: dict = {}
    # SOURCE_BYTES is a bytes join; execute assignment only via ast-safe compile of the assignment chunk.
    chunk = src
    start = chunk.find("SOURCE_BYTES")
    if start < 0:
        raise SystemExit("SOURCE_BYTES missing")
    # Take from SOURCE_BYTES through the closing paren of join.
    sub = chunk[start:]
    tree = ast.parse(sub, mode="exec")
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    if not assigns:
        raise SystemExit("no SOURCE_BYTES assign")
    module = ast.Module(body=assigns[:1], type_ignores=[])
    ast.fix_missing_locations(module)
    exec(compile(module, "<source_bytes>", "exec"), ns)
    raw = ns["SOURCE_BYTES"]
    if not isinstance(raw, (bytes, bytearray)):
        raise SystemExit(type(raw))
    digest_raw = hashlib.sha256(raw).hexdigest()
    print("market-smart raw sha", digest_raw)
    payload = raw.decode("utf-8")
    digest = write_payload(nb_path.parent / "main.py", payload)
    inspect("market-smart", payload, digest)


def extract_momentum() -> None:
    nb_path = DIR / "alperen5252525__market-momentum-farming-kaggriculture" / "market-momentum-farming-kaggriculture.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][2])
    print("=" * 72)
    blob = re.search(r"SOURCE_BLOB\s*=\s*'([^']+)'", src)
    print("momentum blob", bool(blob), "len", len(blob.group(1)) if blob else None)
    raw = decode_gzip_b64(blob.group(1))
    print("momentum decompressed", len(raw), "head", raw[:80])
    # may be tar.gz of main.py or raw main.py
    if raw[:2] == b"\x1f\x8b" or raw[:5] == b"main.":
        pass
    text = None
    if raw[:2] == b"PY" or raw.startswith(b"#") or b"def agent" in raw[:2000] or b"import " in raw[:400]:
        text = raw.decode("utf-8", errors="replace")
    else:
        import io
        import tarfile

        try:
            tf = tarfile.open(fileobj=io.BytesIO(raw), mode="r:*")
            names = tf.getnames()
            print("momentum tar names", names)
            member = tf.extractfile("main.py") or tf.extractfile(names[0])
            text = member.read().decode("utf-8")
        except tarfile.TarError:
            text = raw.decode("utf-8", errors="replace")
    digest = write_payload(nb_path.parent / "main.py", text)
    inspect("momentum", text, digest)


def extract_public_state() -> None:
    nb_path = DIR / "alperen5252525__public-state-market-control-kaggriculture" / "public-state-market-control-kaggriculture.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][9])
    print("=" * 72)
    # payload = ( '...' '...' )
    m = re.search(r"payload\s*=\s*\((.*)\)\s*", src, flags=re.S)
    print("public-state payload paren", bool(m))
    blob = "".join(re.findall(r"'([^']*)'", m.group(1) if m else src))
    print("public-state blob_len", len(blob), "head", blob[:40])
    raw = None
    for decoder in (decode_b85_gzip, decode_gzip_b64, lambda s: zlib.decompress(base64.b85decode(s))):
        try:
            raw = decoder(blob)
            print("public-state decoded", type(decoder).__name__ if hasattr(decoder, "__name__") else decoder, "len", len(raw), "head", raw[:60])
            break
        except Exception as exc:
            print("public-state decoder fail", decoder, type(exc).__name__, exc)
    if raw is None:
        raise SystemExit("public-state decode failed")
    text = None
    if raw.startswith(b"#") or b"def " in raw[:800] or b"import " in raw[:400]:
        text = raw.decode("utf-8")
    else:
        import io
        import tarfile

        try:
            tf = tarfile.open(fileobj=io.BytesIO(raw), mode="r:*")
            names = tf.getnames()
            print("public-state tar names", names[:8], "n", len(names))
            member = tf.extractfile("main.py") or tf.extractfile(names[0])
            text = member.read().decode("utf-8")
        except tarfile.TarError:
            text = raw.decode("utf-8", errors="replace")
    digest = write_payload(nb_path.parent / "main.py", text)
    inspect("public-state", text, digest)


def main() -> None:
    extract_turn_one()
    extract_v43_reprint()
    extract_momentum()
    extract_public_state()


if __name__ == "__main__":
    main()
