"""Drive the shipped scoring Agent (metav4 geese+yarn-sheep+pizza-cows), not root h2 main.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[1]
SHIPPED_MAIN = ROOT / "artifacts/submission/metav4_gsc/main.py"
SHIPPED_SHA256 = "67a44e393bd33618b00595052a2172e2b16fa735bd22cf844a37dc008a1276e5"
REPLAY = (
    ROOT
    / "artifacts/kaggle_runs/submission_55744278/public12e"
    / "episode-100348898-replay.json"
)
H2_SHA = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"


def _load_shipped_agent():
    spec = importlib.util.spec_from_file_location("shipped_scoring_agent", SHIPPED_MAIN)
    if spec is None or spec.loader is None:
        raise ImportError(SHIPPED_MAIN)
    module = importlib.util.module_from_spec(spec)
    sys.modules["shipped_scoring_agent"] = module
    spec.loader.exec_module(module)
    agent = module.agent
    if not callable(agent):
        raise TypeError("shipped scoring agent is not callable")
    return agent


def test_shipped_scoring_agent_bytes_are_metav4_gsc() -> None:
    digest = hashlib.sha256(SHIPPED_MAIN.read_bytes()).hexdigest()
    assert digest == SHIPPED_SHA256
    assert hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest() == H2_SHA
    assert digest != H2_SHA


def test_shipped_scoring_agent_callable_on_real_observation() -> None:
    agent = _load_shipped_agent()
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    observation = dict(replay["steps"][144][1]["observation"])
    # Engine callbacks include `step`; stored replays keep day/hour only.
    observation["step"] = int(observation["day"]) * 24 + int(observation["hour"])
    assert observation["step"] == 144
    action = agent(observation)
    assert isinstance(action, dict)
    assert action.get("farmer") is not None


def test_shipped_scoring_agent_720_both_seats() -> None:
    agent = _load_shipped_agent()
    for seat in (0, 1):
        players = [agent, "pass"] if seat == 0 else ["pass", agent]
        env = make(
            "kaggriculture",
            configuration={"episodeSteps": 720, "seed": 20260920},
            debug=False,
        )
        env.run(players)
        final = env.steps[-1]
        statuses = [str(state.status) for state in final]
        rewards = [float(state.reward) for state in final]
        assert statuses == ["DONE", "DONE"]
        assert all(math.isfinite(r) for r in rewards)
        own = rewards[seat]
        assert math.isfinite(own)
