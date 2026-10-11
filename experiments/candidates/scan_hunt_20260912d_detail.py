"""Static payload hash of 20260912d hunt agents. No cell exec, no extract to candidates/."""

from __future__ import annotations

import ast
import base64
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260912d"
KNOWN = {
    "v35": "294e7e4d9d4b97413646960d318043e0f9116ce58f42fe02afd4716614a4e96d",
    "v37": "94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c",
    "v38": "a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e",
    "cut14": "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e",
    "cut15": "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522",
    "cut16": "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d",
    "router_3a444a70": "3a444a70",
}


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefile_rest(source: str) -> str | None:
    if not source.lstrip().startswith("%%writefile"):
        return None
    _, _, rest = source.partition("\n")
    return rest.replace("\r\n", "\n")


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260912d_cut16_rolling.json").read_text(encoding="utf-8"))
    games = rolling["games"]
    w = sum(1 for r in games if r["win"])
    t = sum(1 for r in games if r["tie"])
    l = sum(1 for r in games if not r["win"] and not r["tie"])
    mean = sum(r["margin"] for r in games) / len(games)
    print("ROLLING", w, t, l, "mean", round(mean, 1), "n", len(games))
    print("ids", [r["id"] for r in games])
    print("clone", sum(1 for r in games if r["clone"]))
    cash = [r["cash_24"] for r in games]
    print("cash24", min(cash), max(cash))
    print("land", {tuple(r["land"]) for r in games})
    print("Q", {tuple(r["Q"]) for r in games})

    nusrati = DIR / "nusrati__2650-score" / "2650-score.ipynb"
    nb = json.loads(nusrati.read_text(encoding="utf-8"))
    rest = writefile_rest(cell_source(nb["cells"][4]))
    assert rest is not None
    sha = hashlib.sha256(rest.encode("utf-8")).hexdigest()
    print("NUSRATI writefile sha", sha, "bytes", len(rest))
    print("NUSRATI eq_v35", sha == KNOWN["v35"])
    for name, known in KNOWN.items():
        print("  eq", name, sha == known or sha.startswith(known))

    sunil = DIR / "sunil123kumar__kaggriculture-v4" / "kaggriculture-v4.ipynb"
    nb = json.loads(sunil.read_text(encoding="utf-8"))
    src = cell_source(nb["cells"][4])
    print("SUNIL cell4 bytes", len(src), "writefile", src.lstrip().startswith("%%writefile"))
    tree = ast.parse(src)
    files = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "FILES":
                    files = ast.literal_eval(node.value)
    assert isinstance(files, dict), type(files)
    for name, rec in files.items():
        payload = rec["payload"]
        if isinstance(payload, (list, tuple)):
            blob = "".join(payload)
        else:
            blob = payload
        raw = zlib.decompress(base64.b85decode(blob.strip().encode("ascii")))
        sha = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8", errors="replace")
        print("SUNIL FILE", name, "declared", rec.get("sha256"), "got", sha, "bytes", len(raw), "match", sha == rec.get("sha256"))
        keys = [
            "ROUTE_STEP",
            "FINAL_PLAN_STEP",
            "sale_horizon",
            "ADVANCE_START",
            "DECISIONS",
            "PROGRAM",
            "reselect",
            "ctypes",
            "CDLL",
            "agent.so",
            "step>=144",
            "step >= 144",
            "step>=648",
            "216<=step<=227",
            "712",
            "288",
            "360",
            "432",
            "576",
            "226",
            "433",
        ]
        print("  flags", {k: (k in text) for k in keys if k in text})
        print("  eq_known", {n: sha == k or sha.startswith(k) for n, k in KNOWN.items()})
        for line in text.splitlines()[:12]:
            print("  ", line[:200])


if __name__ == "__main__":
    main()
