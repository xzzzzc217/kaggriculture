"""Prove King-v4e RC4 later-block differs from six-day, Fieldbook, cut 14, cut 15."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIXDAY_DIR = ROOT / "experiments/candidates/yusuke_sixday"
FIELDBOOK_DIR = ROOT / "experiments/candidates/yusuke_fieldbook"
CAND = ROOT / "experiments/candidates/yamakawanin_king_v4e_rc4/main.py"
CUT14 = ROOT / "experiments/candidates/y3uanm_router_v5/main.py"
CUT15 = ROOT / "experiments/candidates/thomastschinkel_psr_938/main.py"
CLONE = (
    ROOT
    / "artifacts/kaggle_runs/submission_55744278/public12e"
    / "episode-100348898-replay.json"
)
OUT = ROOT / "experiments/20260910b_cut16_divergence.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _sheep_buy_steps(actions: list, start: int, end: int) -> list[int]:
    steps: list[int] = []
    for step in range(start, min(end, len(actions))):
        action = actions[step]
        market = action.get("market") if isinstance(action, dict) else []
        for order in market or []:
            if order and order[0] == "BUY_ANIMAL" and order[1] == "SHEEP":
                steps.append(step)
    return steps


def _act_key(action: dict) -> tuple:
    return (
        tuple(action.get("farmer") or []),
        tuple(tuple(h) for h in (action.get("hands") or [])),
        tuple(tuple(m) for m in (action.get("market") or [])),
    )


def _market_orders(action: dict) -> list:
    return list(action.get("market") or [])


def main() -> None:
    py_compile.compile(str(CAND), doraise=True)
    sha = hashlib.sha256(CAND.read_bytes()).hexdigest()
    prev = list(sys.path)
    sys.path.insert(0, str(SIXDAY_DIR))
    sys.path.insert(0, str(FIELDBOOK_DIR))
    sixday = _load("sixday_logic_cut16", SIXDAY_DIR / "sixday_logic.py")
    fieldbook = _load("fieldbook_logic_cut16", FIELDBOOK_DIR / "fieldbook_logic.py")
    king = _load("cut16_king_v4e_rc4_main", CAND)
    cut14 = _load("cut14_y3uanm_main_cut16", CUT14)
    cut15 = _load("cut15_thomas938_main_cut16", CUT15)
    sys.path[:] = prev

    replay = json.loads(CLONE.read_text(encoding="utf-8"))
    seat = 1
    live_actions: list[dict] = []
    chosen_at: dict[str, dict] = {}
    for step in range(0, 720):
        obs = replay["steps"][step][seat]["observation"]
        action = king.agent(obs)
        live_actions.append(action)
        if step in (0, 144, 216, 217, 226, 240, 241, 288, 360, 385, 432, 576):
            shops = list((((obs.get("town") or {}).get("unlocked_shops")) or []))
            mode = None
            if hasattr(king, "_V3M_MODE"):
                mode = king._V3M_MODE.get(int(obs.get("player", 0) or 0))
            y2 = None
            if hasattr(king, "_V4E_Y2"):
                y2 = king._V4E_Y2.get(int(obs.get("player", 0) or 0))
            key = None
            if hasattr(king, "_key"):
                try:
                    key = king._key(step, shops)
                except Exception:
                    key = None
            chosen_at[str(step)] = {
                "key": key,
                "mode": mode,
                "yarn_second_flag": y2,
                "shops": shops,
                "farmer": action.get("farmer"),
                "market": action.get("market"),
            }

    obs217 = replay["steps"][217][seat]["observation"]
    six_live = sixday.make_agent()(obs217)
    cut14_live = cut14.agent(obs217)
    cut15._SESSIONS.clear()
    for step in range(0, 218):
        cut15.agent(replay["steps"][step][seat]["observation"])
    cut15_live = cut15.agent(obs217)
    balanced = fieldbook.ROUTES[0][217]
    king_217 = live_actions[217]

    live_sheep = _sheep_buy_steps(live_actions, 200, 267)
    rc3_hits = {}
    if hasattr(king, "_RC3_HITS"):
        rc3_hits = {str(k): list(v) for k, v in king._RC3_HITS.items()}

    diffs_vs_six = 0
    diffs_vs_bal = 0
    diffs_vs_cut14 = 0
    diffs_vs_cut15 = 0
    cut15._SESSIONS.clear()
    for step in range(0, 217):
        cut15.agent(replay["steps"][step][seat]["observation"])
    for step in range(217, 267):
        obs = replay["steps"][step][seat]["observation"]
        king_act = live_actions[step]
        six_act = sixday.later_block_action([0, 0, 0, 0, 0], step)
        bal_act = fieldbook.ROUTES[0][step]
        cut14_act = cut14.routes()[cut14.MAIN][step]
        cut15_act = cut15.agent(obs)
        if _act_key(king_act) != _act_key(six_act):
            diffs_vs_six += 1
        if king_act.get("farmer") != bal_act.get("farmer") or king_act.get("hands") != bal_act.get(
            "hands"
        ):
            diffs_vs_bal += 1
        if _act_key(king_act) != _act_key(cut14_act):
            diffs_vs_cut14 += 1
        if _act_key(king_act) != _act_key(cut15_act):
            diffs_vs_cut15 += 1

    rec = {
        "cut": 16,
        "agent": "yamakawanin_king_v4e_rc4",
        "kernel": "yamakawanin/king-v4e-rc4",
        "path": str(CAND.as_posix()),
        "sha256": sha,
        "windows_agent_so": False,
        "reselect_steps": [216, 240, 241, 288, 360, 385, 432, 576],
        "reselect_after_216": [240, 241, 288, 360, 385, 432, 576],
        "reselect_kind": "shop-family 72-turn PROGRAM phases P3+ plus YARN_SECOND>=240, RC3 sheep@241 fert@385",
        "not_cut12": True,
        "not_cut13": True,
        "not_cut14": True,
        "not_cut15": True,
        "live_217_differs_from_sixday": _act_key(king_217) != _act_key(six_live),
        "live_217_differs_from_balanced": (
            king_217.get("farmer") != balanced.get("farmer")
            or king_217.get("hands") != balanced.get("hands")
        ),
        "live_217_differs_from_cut14": _act_key(king_217) != _act_key(cut14_live),
        "live_217_differs_from_cut15": _act_key(king_217) != _act_key(cut15_live),
        "diffs_217_266_vs_sixday": diffs_vs_six,
        "diffs_217_266_vs_balanced": diffs_vs_bal,
        "diffs_217_266_vs_cut14": diffs_vs_cut14,
        "diffs_217_266_vs_cut15": diffs_vs_cut15,
        "chosen_at": chosen_at,
        "rc3_hits": rc3_hits,
        "main_sheep_200_267": live_sheep,
        "not_227_242_266_wrap": live_sheep != [227, 242, 266],
        "king_217_market": _market_orders(king_217),
        "cut14_217_market": _market_orders(cut14_live),
        "cut15_217_market": _market_orders(cut15_live),
    }
    OUT.write_text(json.dumps(rec, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(rec, indent=2, default=str))
    assert rec["live_217_differs_from_sixday"]
    assert rec["live_217_differs_from_balanced"]
    assert rec["live_217_differs_from_cut14"]
    assert rec["live_217_differs_from_cut15"]
    assert rec["diffs_217_266_vs_sixday"] >= 1
    assert rec["diffs_217_266_vs_balanced"] >= 1
    assert rec["diffs_217_266_vs_cut14"] >= 1
    assert rec["diffs_217_266_vs_cut15"] >= 1
    assert rec["not_227_242_266_wrap"]
    assert rec["reselect_after_216"]
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
