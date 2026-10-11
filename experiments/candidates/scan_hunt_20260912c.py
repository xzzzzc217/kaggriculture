"""Static JSON/payload scan of 20260912c hunt. No cell exec."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "artifacts/public_sources/_hunt_20260912c"
V37 = "94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c"
CUT14 = "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
CUT15 = "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
CUT16 = "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"


def cell_source(cell: dict) -> str:
    source = cell.get("source") or ""
    return "".join(source) if isinstance(source, list) else str(source)


def writefile_rest(source: str) -> str | None:
    if not source.lstrip().startswith("%%writefile"):
        return None
    _, _, rest = source.partition("\n")
    return rest.replace("\r\n", "\n")


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260912c_cut16_rolling.json").read_text(encoding="utf-8"))
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

    for path in sorted(DIR.rglob("*.ipynb")):
        raw = path.read_bytes()
        nb = json.loads(raw.decode("utf-8"))
        cells = nb.get("cells") or []
        print("=" * 70)
        print(path.parent.name, "bytes", len(raw), "sha256", hashlib.sha256(raw).hexdigest())
        print("n_cells", len(cells), "exec", [c.get("execution_count") for c in cells][:8], "outputs", sum(len(c.get("outputs") or []) for c in cells))
        for i, cell in enumerate(cells):
            rest = writefile_rest(cell_source(cell))
            if rest is None:
                continue
            sha = hashlib.sha256(rest.encode("utf-8")).hexdigest()
            print("WRITEFILE", i, "bytes", len(rest), "sha", sha)
            print("eq_v37", sha == V37, "eq_cut14", sha == CUT14, "eq_cut15", sha == CUT15, "eq_cut16", sha == CUT16)
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
                "step>=648",
                "216<=step<=227",
                "712",
            ]
            print("payload_flags", {k: (k in rest) for k in keys})
            for line in rest.splitlines():
                if any(
                    k in line
                    for k in (
                        "step>=144",
                        "step>=648",
                        "216<=step<=227",
                        "ROUTE_STEP",
                        "sale_horizon",
                        "ADVANCE_START",
                        "DECISIONS",
                        "ctypes",
                        "CDLL",
                        "agent.so",
                        "if step<288",
                        "if step>=288",
                    )
                ) and len(line) < 240:
                    print("HIT", line[:220])


if __name__ == "__main__":
    main()
