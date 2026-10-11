from __future__ import annotations

import json
from pathlib import Path

g = json.loads(Path("experiments/20260915c_cut16_rolling.json").read_text(encoding="utf-8"))["games"]
print("n", len(g), "w", sum(x["win"] for x in g), "t", sum(x["tie"] for x in g), "l", sum((not x["win"]) and (not x["tie"]) for x in g))
print("mean", round(sum(x["margin"] for x in g) / len(g), 1))
print("clone", sum(bool(x["clone"]) for x in g))
print("cash24", min(x["cash_24"] for x in g), max(x["cash_24"] for x in g))
for x in g:
    su = [s["step"] for s in x["sheep_steps_us"] if s["qty"]]
    so = [s["step"] for s in x["sheep_steps_opp"] if s["qty"]]
    flag = "W" if x["win"] else "L"
    print(
        f"{x['id']} {flag} {x['margin']:+.0f} {x['opp'][:22]!r:24s} "
        f"{x['buy_us']} vs {x['buy_opp']} shops={x['shops72']} clone={int(x['clone'])} "
        f"sheep_us={su} sheep_opp={so} land={x['land']}"
    )
