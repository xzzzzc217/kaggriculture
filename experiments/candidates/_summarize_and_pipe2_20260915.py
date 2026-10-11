"""Summarize rolling-12 extra-animal tapes and static-decode pipe-2 AGENT_B64."""

from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def extra(steps, kind: str) -> list[int]:
    return [e["step"] for e in steps if e.get("kind") == kind and e.get("qty") and e["step"] >= 200]


def herd(buy: dict) -> str:
    c = int(buy.get("COW") or 0)
    s = int(buy.get("SHEEP") or 0)
    g = int(buy.get("GOOSE") or 0)
    if g:
        return f"{c}c{s}s{g}g"
    return f"{c}c{s}s"


def main() -> None:
    rows = json.loads((ROOT / "experiments/20260915_cut16_rolling.json").read_text(encoding="utf-8"))["games"]
    print("n", len(rows))
    print(
        "wtl",
        sum(r["win"] for r in rows),
        sum(r["tie"] for r in rows),
        sum(not r["win"] and not r["tie"] for r in rows),
    )
    print("mean", round(sum(r["margin"] for r in rows) / len(rows), 1))
    print("clone", sum(bool(r["clone"]) for r in rows))
    print("cash24", min(r["cash_24"] for r in rows), max(r["cash_24"] for r in rows))
    print("land", {tuple(r["land"]) for r in rows})
    print("Q", {tuple(r["Q"]) for r in rows})
    print("n_steps", {r["n_steps"] for r in rows})
    print("status", {tuple(r["statuses"]) for r in rows})
    for r in rows:
        flag = "W" if r["win"] else ("T" if r["tie"] else "L")
        us_s = [e["step"] for e in r["sheep_steps_us"] if e["qty"] and e["step"] >= 200]
        opp_s = [e["step"] for e in r["sheep_steps_opp"] if e["qty"] and e["step"] >= 200]
        print(
            r["id"],
            flag,
            r["margin"],
            r["opp"],
            herd(r["buy_us"]),
            "vs",
            herd(r["buy_opp"]),
            "clone",
            int(bool(r["clone"])),
            r["shops72"],
            "sheep_us",
            us_s,
            "sheep_opp",
            opp_s,
            "cash24",
            r["cash_24"],
        )

    inspect_log = Path(
        r"C:\Users\21398\.grok\sessions\D%3A%5Ckaggle%5Ckaggriculture\01a0a164-27af-7e92-a275-fed1363c29fc\terminal\call-1bb95598-f4f2-493d-9aa3-babac16a6e49-73.log"
    )
    if inspect_log.exists():
        text = inspect_log.read_text(encoding="utf-8", errors="ignore")
        for eid in [109091091, 109057555, 109054323, 109044160, 109078755]:
            print("----- inspect", eid)
            grab = False
            n = 0
            for line in text.splitlines():
                if line.startswith(str(eid) + " "):
                    grab = True
                if grab:
                    print(line[:240])
                    n += 1
                    if n > 16:
                        break

    nb_path = (
        ROOT
        / "artifacts/public_sources/_hunt_20260915"
        / "nathanjacob__kaggriculture-pipe-2-agent"
        / "kaggriculture-pipe-2-agent.ipynb"
    )
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][0])
    tree = ast.parse(src)
    blob = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "AGENT_B64" for t in node.targets):
            blob = ast.literal_eval(node.value)
            break
    print("pipe2 AGENT_B64", None if blob is None else type(blob), None if blob is None else len(blob) if hasattr(blob, "__len__") else blob)
    if blob is not None:
        if isinstance(blob, (list, tuple)):
            raw = "".join(blob).encode("ascii")
        elif isinstance(blob, str):
            raw = blob.encode("ascii")
        else:
            raw = bytes(blob)
        payload = gzip.decompress(base64.b64decode(raw))
        digest = hashlib.sha256(payload).hexdigest()
        out = nb_path.parent / "main.py"
        out.write_bytes(payload)
        print("pipe2 sha256", digest, "bytes", len(payload), "ctypes", b"ctypes" in payload or b"CDLL" in payload or b"agent.so" in payload)
        text = payload.decode("utf-8", errors="replace")
        print(" 144/648", text.count("144"), text.count("648"), "288", text.count("288"), "712", text.count("712"))
        print(" ROUTE_STEP", "ROUTE_STEP" in text, "PROGRAM", "PROGRAM" in text, "sale_horizon", "sale_horizon" in text)
        print(" ADVANCE_START", "ADVANCE_START" in text, "reselect", "reselect" in text.lower())
        for needle in ("if step", "216", "226", "227", "288", "360", "432", "576", "648", "712", "agent.so", "CDLL"):
            lines = [ln for ln in text.splitlines() if needle in ln]
            if lines:
                print(f"  lines[{needle}] n={len(lines)}")
                for ln in lines[:8]:
                    print("   ", ln[:220])


if __name__ == "__main__":
    main()
