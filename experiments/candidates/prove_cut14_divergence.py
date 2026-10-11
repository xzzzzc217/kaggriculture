"""Prove y3uanm cut 14 later-block differs from six-day and Fieldbook BALANCED."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIXDAY_DIR = ROOT / "experiments/candidates/yusuke_sixday"
FIELDBOOK_DIR = ROOT / "experiments/candidates/yusuke_fieldbook"
CUT14 = ROOT / "experiments/candidates/y3uanm_router_v5/main.py"
CLONE = (
    ROOT
    / "artifacts/kaggle_runs/submission_55744278/public12e"
    / "episode-100348898-replay.json"
)
OUT = ROOT / "experiments/20260909_cut14_divergence.json"


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
        for order in (actions[step].get("market") or []):
            if order and order[0] == "BUY_ANIMAL" and order[1] == "SHEEP":
                steps.append(step)
    return steps


def main() -> None:
    prev = list(sys.path)
    sys.path.insert(0, str(SIXDAY_DIR))
    sys.path.insert(0, str(FIELDBOOK_DIR))
    sixday = _load("sixday_logic_cut14", SIXDAY_DIR / "sixday_logic.py")
    fieldbook = _load("fieldbook_logic_cut14", FIELDBOOK_DIR / "fieldbook_logic.py")
    cut14 = _load("cut14_y3uanm_main", CUT14)
    sys.path[:] = prev

    replay = json.loads(CLONE.read_text(encoding="utf-8"))
    obs217 = replay["steps"][217][1]["observation"]
    six_live = sixday.make_agent()(obs217)
    cut_live = cut14.agent(obs217)
    balanced = fieldbook.ROUTES[0][217]
    six_tape = sixday.later_block_action([0, 0, 0, 0, 0], 217)

    main_route = cut14.routes()[cut14.MAIN]
    sheep_200_267 = _sheep_buy_steps(main_route, 200, 267)
    sheep_all = _sheep_buy_steps(main_route, 0, 720)
    diffs_vs_six = 0
    diffs_vs_bal = 0
    for step in range(217, 267):
        six_act = sixday.later_block_action([0, 0, 0, 0, 0], step)
        bal_act = fieldbook.ROUTES[0][step]
        cut_act = main_route[step]
        if cut_act.get("farmer") != six_act.get("farmer") or cut_act.get("hands") != six_act.get(
            "hands"
        ):
            diffs_vs_six += 1
        if cut_act.get("farmer") != bal_act.get("farmer") or cut_act.get("hands") != bal_act.get(
            "hands"
        ):
            diffs_vs_bal += 1

    rec = {
        "cut": 14,
        "agent": "y3uanm_router_v5",
        "reselect_steps": [226, 360, 433],
        "not_cut12": True,
        "not_cut13": True,
        "windows_agent_so": False,
        "live_217_differs_from_sixday": cut_live != six_live,
        "live_217_differs_from_balanced": (
            cut_live.get("farmer") != balanced.get("farmer")
            or cut_live.get("market") != (balanced.get("market") or [])
        ),
        "tape_217_differs_from_sixday": main_route[217] != six_tape,
        "tape_217_differs_from_balanced": main_route[217] != balanced,
        "diffs_217_266_vs_sixday": diffs_vs_six,
        "diffs_217_266_vs_balanced": diffs_vs_bal,
        "main_sheep_200_267": sheep_200_267,
        "main_sheep_all": sheep_all[:20],
        "not_227_242_266_wrap": sheep_200_267 != [227, 242, 266],
        "decisions": list(cut14.DECISIONS),
    }
    OUT.write_text(json.dumps(rec, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(rec, indent=2, default=str))
    assert rec["live_217_differs_from_sixday"]
    assert rec["tape_217_differs_from_balanced"]
    assert rec["diffs_217_266_vs_sixday"] >= 1
    assert rec["not_227_242_266_wrap"]
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
