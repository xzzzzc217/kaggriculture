"""Build shopbag + first-Yarn Kenjo specialist. No cell exec, no upload."""

from __future__ import annotations

import base64
import hashlib
import json
import py_compile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "artifacts/kaggle_runs/submission_55840543/extracted"
KENJO = LIVE / "episode-102125420-replay.json"
SHOPBAG = ROOT / "experiments/candidates/moon_shopbag_v1/main.py"
OUT = ROOT / "experiments/candidates/moon_shopbag_v4"
TAIL = r'''
_KENJO=json.loads(zlib.decompress(base64.b85decode(_KENJO_DATA)).decode("utf-8"))

def _kenjo_action(obs,step):
 step=min(max(int(step),0),len(_KENJO)-1)
 action=copy.deepcopy(_KENJO[step] or {})
 action={"farmer":list(action.get("farmer") or ["PASS"]),
         "hands":[list(order or ["PASS"]) for order in (action.get("hands") or [])],
         "market":[list(order) for order in (action.get("market") or [])]}
 player=int(_get(obs,"player",0) or 0)
 farms=list(_get(obs,"farms",[]) or [])
 expected=len(_get(farms[player],"hands",[]) or []) if player<len(farms) else 0
 hands=action["hands"]
 hands.extend([["PASS"] for _ in range(max(0,expected-len(hands)))])
 action["hands"]=hands[:expected]
 return action

def agent(obs,configuration=None):
 step=max(0,int(_get(obs,"step",0) or 0))
 shops=list(_get(_get(obs,"town",{}) or {},"unlocked_shops",[]) or [])
 if step>=72 and shops and shops[0]=="YARN_STORE":
  return _kenjo_action(obs,step)
 action=_BASE_NS["agent"](obs)
 if 72<=step<712 and "YARN_STORE" in shops:
  return _rebalance(obs,action,step)
 return action
'''


def extract_kenjo() -> list:
    replay = json.loads(KENJO.read_text(encoding="utf-8"))
    teams = replay["info"]["TeamNames"]
    seat = teams.index("Kenjo1209")
    actions = [turn[seat].get("action") or {} for turn in replay["steps"][1:]]
    if len(actions) != 719:
        raise SystemExit(f"expected 719 actions, got {len(actions)}")
    return actions


def main() -> None:
    actions = extract_kenjo()
    payload = base64.b85encode(zlib.compress(json.dumps(actions, separators=(",", ":")).encode("utf-8"), 9)).decode("ascii")
    shopbag = SHOPBAG.read_text(encoding="utf-8")
    shopbag = shopbag.replace("import base64, copy, zlib", "import base64, copy, json, zlib", 1)
    # Drop shopbag's agent() so we replace it.
    marker = "def agent(obs,configuration=None):"
    if marker not in shopbag:
        raise SystemExit("shopbag agent() missing")
    head = shopbag[: shopbag.index(marker)].rstrip() + "\n"
    body = head + "\n_KENJO_DATA=" + repr(payload) + TAIL
    if not body.endswith("\n"):
        body += "\n"
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "main.py"
    raw = body.encode("utf-8").replace(b"\r\n", b"\n")
    target.write_bytes(raw)
    py_compile.compile(str(target), doraise=True)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print("path", target)
    print("bytes", target.stat().st_size)
    print("sha256", digest)
    print("kenjo_actions", len(actions))
    print("payload_chars", len(payload))


if __name__ == "__main__":
    main()
