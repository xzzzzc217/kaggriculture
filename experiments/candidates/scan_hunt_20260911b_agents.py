"""Extract plaintext agent functions from hunt writefiles. No cell exec."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "artifacts/public_sources/_hunt_20260911b"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefiles(source: str) -> list[tuple[str, str]]:
    out = []
    if source.lstrip().startswith("%%writefile"):
        first, _, rest = source.partition("\n")
        name = first.split("%%writefile", 1)[-1].strip()
        if name.startswith("-a "):
            name = name[3:].strip()
        out.append((name, rest))
    return out


def native_hits(text: str) -> list[str]:
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if any(k in low for k in ("ctypes.cdll", "agent.so", "agent.dylib", ".so'", '.so"', "cdll(")):
            hits.append(f"L{i} {line[:200]}")
    return hits


def main() -> None:
    for path in sorted(DIR.rglob("*")):
        if path.suffix.lower() not in {".ipynb", ".py"}:
            continue
        print("=" * 78)
        print(path.relative_to(DIR))
        payloads: list[tuple[str, str]] = []
        if path.suffix == ".py":
            payloads.append((path.name, path.read_text(encoding="utf-8", errors="ignore")))
        else:
            nb = json.loads(path.read_text(encoding="utf-8"))
            cells = nb.get("cells") or []
            print("n_cells", len(cells))
            for i, cell in enumerate(cells):
                src = cell_source(cell)
                wfs = writefiles(src)
                payloads.extend(wfs)
                if not wfs and cell.get("cell_type") == "code":
                    print(f"CODE cell={i} chars={len(src)}")
                    for line in src.splitlines()[:12]:
                        if line.strip():
                            print(" ", line[:200])
        for name, payload in payloads:
            sha = hashlib.sha256(payload.replace("\r\n", "\n").encode("utf-8")).hexdigest()
            print(f"FILE {name} bytes={len(payload)} sha256={sha}")
            print(" native", native_hits(payload)[:8] or "none")
            # print agent-related functions without compressed blobs
            in_agent = False
            shown = 0
            for i, line in enumerate(payload.splitlines(), 1):
                if line.startswith("def agent") or line.startswith("    def agent"):
                    in_agent = True
                    shown = 0
                    print(f" AGENT_START L{i}")
                if in_agent:
                    if len(line) > 180 and ("b85decode" in line or "b64decode" in line or "decompress" in line):
                        print(f"  L{i} <blob {len(line)} chars>")
                    else:
                        print(f"  L{i} {line[:220]}")
                    shown += 1
                    if shown >= 28:
                        print("  ...")
                        in_agent = False
            # step comparisons
            for i, line in enumerate(payload.splitlines(), 1):
                if any(
                    tok in line
                    for tok in (
                        "step == 144",
                        "step==144",
                        "step == 216",
                        "step == 226",
                        "step == 288",
                        "step == 360",
                        "step == 432",
                        "step == 433",
                        "step == 576",
                        "step == 648",
                        "step == 712",
                        "ROUTE_STEP",
                        "FINAL_PLAN_STEP",
                        "ADVANCE_START",
                        "SALE_HORIZON",
                        "sale_horizon",
                    )
                ):
                    if "b85decode" not in line and len(line) < 220:
                        print(f" STEP L{i} {line.strip()}")


if __name__ == "__main__":
    main()
