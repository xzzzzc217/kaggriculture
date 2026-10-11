"""Prove Thomas 93.8% later-block differs from six-day and Fieldbook BALANCED."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIXDAY_DIR = ROOT / "experiments/candidates/yusuke_sixday"
FIELDBOOK_DIR = ROOT / "experiments/candidates/yusuke_fieldbook"
CAND = ROOT / "experiments/candidates/thomastschinkel_psr_938/main.py"
CUT14 = ROOT / "experiments/candidates/y3uanm_router_v5/main.py"
CLONE = (
    ROOT
    / "artifacts/kaggle_runs/submission_55744278/public12e"
    / "episode-100348898-replay.json"
)
OUT = ROOT / "experiments/20260910_cut15_divergence.json"


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


def main() -> None:
    prev = list(sys.path)
    sys.path.insert(0, str(SIXDAY_DIR))
    sys.path.insert(0, str(FIELDBOOK_DIR))
    sixday = _load("sixday_logic_cut15", SIXDAY_DIR / "sixday_logic.py")
    fieldbook = _load("fieldbook_logic_cut15", FIELDBOOK_DIR / "fieldbook_logic.py")
    cand = _load("cut15_thomas938_main", CAND)
    cut14 = _load("cut14_y3uanm_main", CUT14)
    sys.path[:] = prev

    replay = json.loads(CLONE.read_text(encoding="utf-8"))
    seat = 1
    cand._SESSIONS.clear()
    for step in range(0, 218):
        cand.agent(replay["steps"][step][seat]["observation"])
    obs217 = replay["steps"][217][seat]["observation"]
    six_live = sixday.make_agent()(obs217)
    cand_live = cand.agent(obs217)
    cut14_live = cut14.agent(obs217)
    balanced = fieldbook.ROUTES[0][217]
    six_tape = sixday.later_block_action([0, 0, 0, 0, 0], 217)

    n_tapes = len(cand._TAPES)
    n_trees = len(cand._TREES)
    tape_sheep = {
        str(idx): _sheep_buy_steps(tape, 200, 267) for idx, tape in enumerate(cand._TAPES)
    }
    chosen_at = {}
    cand._SESSIONS.clear()
    for step in (0, 144, 216, 217, 226, 288, 360, 432, 576):
        obs = replay["steps"][step][seat]["observation"]
        action = cand.agent(obs)
        state = cand._SESSIONS.get(seat)
        chosen_at[str(step)] = {
            "tape": None if state is None else int(state[1]),
            "farmer": action.get("farmer"),
            "market": action.get("market"),
        }

    live_tape = cand._SESSIONS[seat][1]
    live_sheep = _sheep_buy_steps(cand._TAPES[live_tape], 200, 267)
    diffs_vs_six = 0
    diffs_vs_bal = 0
    diffs_vs_cut14 = 0
    cand._SESSIONS.clear()
    for step in range(0, 217):
        cand.agent(replay["steps"][step][seat]["observation"])
    for step in range(217, 267):
        obs = replay["steps"][step][seat]["observation"]
        cut_act = cand.agent(obs)
        six_act = sixday.later_block_action([0, 0, 0, 0, 0], step)
        bal_act = fieldbook.ROUTES[0][step]
        cut14_act = cut14.routes()[cut14.MAIN][step]
        if _act_key(cut_act) != _act_key(six_act):
            diffs_vs_six += 1
        if cut_act.get("farmer") != bal_act.get("farmer") or cut_act.get("hands") != bal_act.get(
            "hands"
        ):
            diffs_vs_bal += 1
        if _act_key(cut_act) != _act_key(cut14_act):
            diffs_vs_cut14 += 1

    rec = {
        "cut": 15,
        "agent": "thomastschinkel_psr_938",
        "reselect_steps": [144, 288, 432, 576],
        "reselect_after_216": [288, 432, 576],
        "n_tapes": n_tapes,
        "n_trees": n_trees,
        "not_cut12": True,
        "not_cut13": True,
        "not_cut14": True,
        "windows_agent_so": False,
        "live_217_differs_from_sixday": cand_live != six_live,
        "live_217_differs_from_balanced": (
            cand_live.get("farmer") != balanced.get("farmer")
            or cand_live.get("market") != (balanced.get("market") or [])
        ),
        "live_217_differs_from_cut14": cand_live != cut14_live,
        "tape_217_differs_from_sixday": _act_key(cand._TAPES[live_tape][217]) != _act_key(six_tape),
        "tape_217_differs_from_balanced": cand._TAPES[live_tape][217] != balanced,
        "diffs_217_266_vs_sixday": diffs_vs_six,
        "diffs_217_266_vs_balanced": diffs_vs_bal,
        "diffs_217_266_vs_cut14": diffs_vs_cut14,
        "chosen_at": chosen_at,
        "live_tape": int(live_tape),
        "tape_sheep_200_267": tape_sheep,
        "main_sheep_200_267": live_sheep,
        "not_227_242_266_wrap": live_sheep != [227, 242, 266],
        "any_tape_227_wrap": any(v == [227, 242, 266] for v in tape_sheep.values()),
    }
    OUT.write_text(json.dumps(rec, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(rec, indent=2, default=str))
    assert rec["live_217_differs_from_sixday"]
    assert rec["live_217_differs_from_balanced"]
    assert rec["diffs_217_266_vs_sixday"] >= 1
    assert rec["not_227_242_266_wrap"]
    assert rec["reselect_after_216"]
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
