"""Ice-hold candidate on the GSC non-win where cow-to-sheep collapsed the bank.

Drives the shipped candidate through the official engine from the recorded
seed and opponent stream of episode 111340693. The margin comes from engine
rewards. It must move off GSC's stored -7669.
"""

from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "candidates"))

from run_replay_callback import play  # noqa: E402

CANDIDATE = ROOT / "experiments" / "candidates" / "goldband_icehold" / "main.py"
REPLAY = ROOT / "tests" / "fixtures" / "goldband" / "episode-111340693-slim.json"
GSC_SHA = "67a44e393bd33618b00595052a2172e2b16fa735bd22cf844a37dc008a1276e5"
METAV4_PREFIX = "9d634946"
H2_SHA = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
GSC_MARGIN_111340693 = -7669


def test_icehold_bytes_are_not_gsc_metav4_or_root_h2() -> None:
    digest = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    root = hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest()
    assert digest != GSC_SHA
    assert not digest.startswith(METAV4_PREFIX)
    assert digest != H2_SHA
    assert root == H2_SHA
    assert root.startswith("65e6f5cd")


def test_icehold_replays_gsc_nonwin_111340693() -> None:
    report = play(CANDIDATE, REPLAY, seat=0, steps=720)
    assert report["statuses"] == ["DONE", "DONE"]
    banks = [float(r) for r in report["rewards"]]
    assert all(math.isfinite(b) for b in banks)
    margin = banks[0] - banks[1]
    assert margin == report["margin"]
    assert margin != GSC_MARGIN_111340693
