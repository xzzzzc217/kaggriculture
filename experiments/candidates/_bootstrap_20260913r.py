"""Copy 13q cycle scripts to 13r and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_13P = """PREV = {
    108520439,
    108509931,
    108489181,
    108484081,
    108445221,
    108441448,
    108441305,
    108412731,
    108383915,
    108377691,
    108374873,
    108351144,
}"""
PREV_13Q = """PREV = {
    108534412,
    108504670,
    108472548,
    108461768,
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
    108371627,
    108369265,
    108366745,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913q", "20260913r")
    text = text.replace("20260913p", "20260913q")
    text = text.replace("09-13p", "09-13q")
    text = text.replace("0913p", "0913q")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913r_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913r"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    for name in lb_src.glob("kaggriculture-publicleaderboard-*.csv"):
        shutil.copy2(name, lb_dst / name.name)
        print("copied csv", name.name)
    for sid in (56151152, 56151155):
        shutil.copy2(lb_src / f"episodes_{sid}.json", ROOT / "experiments" / f"episodes_{sid}.json")
        print("copied episodes", sid)

    live = copy_patch("live_state_20260913q.py", "live_state_20260913r.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13P not in text:
        raise SystemExit("PREV_13P block missing after copy")
    text = text.replace(PREV_13P, PREV_13Q)
    text = text.replace('"publicScore": 1687.3', '"publicScore": 1680.9')
    text = text.replace('"publicScore": 1315.6', '"publicScore": 1315.6')
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores")

    copy_patch("fetch_cut16_replays_20260913q.py", "fetch_cut16_replays_20260913r.py")
    copy_patch("autopsy_cut16_20260913q.py", "autopsy_cut16_20260913r.py")
    copy_patch("inspect_cut16_losses_20260913q.py", "inspect_cut16_losses_20260913r.py")
    top = copy_patch("fetch_top_board_20260913q.py", "fetch_top_board_20260913r.py")
    tt = top.read_text(encoding="utf-8")
    if "108538106" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108518840,",
            "SKIP_IDS = {\n    108538106,\n    108531216,\n    108525049,\n    108098091,\n    108518840,",
        )
        top.write_text(tt, encoding="utf-8")
    copy_patch("measure_top_board_20260913q.py", "measure_top_board_20260913r.py")
    copy_patch("inspect_hunt_20260913q.py", "inspect_hunt_20260913r.py")
    copy_patch("scan_hunt_20260913q.py", "scan_hunt_20260913r.py")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch = (CAND / "fetch_cut16_replays_20260913r.py").read_text(encoding="utf-8")
    print(fetch.split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
