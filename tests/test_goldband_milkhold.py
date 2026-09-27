"""Milk-hold candidate on the pet-cafe game ice-hold still lost.

Drives the shipped candidate through the official engine from the recorded
seed and opponent stream of episode 111433719. The margin comes from engine
rewards. It must move off ice-hold's stored -327.
"""

from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "candidates"))

from run_replay_callback import play  # noqa: E402

CANDIDATE = ROOT / "experiments" / "candidates" / "goldband_milkhold" / "main.py"
REPLAY = ROOT / "tests" / "fixtures" / "goldband" / "episode-111433719-slim.json"
ICEHOLD_PREFIX = "56d876eb"
GSC_PREFIX = "67a44e39"
METAV4_PREFIX = "9d634946"
H2_SHA = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
ICEHOLD_MARGIN_111433719 = -327


def test_milkhold_bytes_are_not_icehold_gsc_or_root_h2() -> None:
    digest = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    root = hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest()
    assert not digest.startswith(ICEHOLD_PREFIX)
    assert not digest.startswith(GSC_PREFIX)
    assert not digest.startswith(METAV4_PREFIX)
    assert digest != H2_SHA
    assert root == H2_SHA
    assert root.startswith("65e6f5cd")


def test_milkhold_replays_icehold_nonwin_111433719() -> None:
    report = play(CANDIDATE, REPLAY, seat=1, steps=720)
    assert report["statuses"] == ["DONE", "DONE"]
    banks = [float(r) for r in report["rewards"]]
    assert all(math.isfinite(b) for b in banks)
    margin = banks[1] - banks[0]
    assert margin == report["margin"]
    assert margin != ICEHOLD_MARGIN_111433719
