"""Build and verify a deterministic one-file Kaggriculture submission bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

MAX_BUNDLE_BYTES = 100 * 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_bundle(main_path: Path, output_path: Path) -> dict[str, object]:
    agent_bytes = main_path.read_bytes()
    compile(agent_bytes, main_path.name, "exec")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode="w") as bundle:
            info = tarfile.TarInfo("main.py")
            info.size = len(agent_bytes)
            info.mode = 0o644
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            bundle.addfile(info, io.BytesIO(agent_bytes))
    bundle_bytes = buffer.getvalue()
    output_path.write_bytes(bundle_bytes)

    with tarfile.open(output_path, "r:gz") as bundle:
        members = bundle.getnames()
        packed = bundle.extractfile("main.py")
        if packed is None:
            raise RuntimeError("bundle does not contain readable root main.py")
        packed_bytes = packed.read()

    if members != ["main.py"]:
        raise RuntimeError(f"unexpected bundle members: {members}")
    if packed_bytes != agent_bytes:
        raise RuntimeError("packed main.py differs from source bytes")
    if len(bundle_bytes) > MAX_BUNDLE_BYTES:
        raise RuntimeError(f"bundle exceeds 100 MiB: {len(bundle_bytes)} bytes")

    return {
        "source": str(main_path.resolve()),
        "output": str(output_path.resolve()),
        "members": members,
        "agent_bytes": len(agent_bytes),
        "agent_sha256": sha256(agent_bytes),
        "bundle_bytes": len(bundle_bytes),
        "bundle_sha256": sha256(bundle_bytes),
        "max_bundle_bytes": MAX_BUNDLE_BYTES,
        "compile_passed": True,
        "byte_identity_passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--main", type=Path, default=Path("main.py"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    report = build_bundle(args.main, args.output)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
