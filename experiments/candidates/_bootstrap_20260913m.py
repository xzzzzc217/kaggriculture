"""Copy 13l cycle scripts to 13m and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_13K = """PREV = {
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
    108371627,
    108369265,
    108366745,
    108328160,
    108311577,
    108273755,
    108270318,
}"""
PREV_13L = """PREV = {
    108445221,
    108441448,
    108441305,
    108412731,
    108383915,
    108377691,
    108374873,
    108351144,
    108349751,
    108345614,
    108343489,
    108326448,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913l", "20260913m")
    text = text.replace("20260913k", "20260913l")
    text = text.replace("09-13k", "09-13l")
    text = text.replace("0913k", "0913l")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913m_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913m"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    for name in lb_src.glob("kaggriculture-publicleaderboard-*.csv"):
        shutil.copy2(name, lb_dst / name.name)
        print("copied csv", name.name)
    for sid in (56151152, 56151155):
        shutil.copy2(lb_src / f"episodes_{sid}.json", ROOT / "experiments" / f"episodes_{sid}.json")
        print("copied episodes", sid)

    live = copy_patch("live_state_20260913l.py", "live_state_20260913m.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13K not in text:
        raise SystemExit("PREV_13K block missing after copy")
    text = text.replace(PREV_13K, PREV_13L)
    text = text.replace('"publicScore": 1692.2', '"publicScore": 1693.4')
    text = text.replace('"publicScore": 1327.7', '"publicScore": 1332.1')
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores")

    copy_patch("fetch_cut16_replays_20260913l.py", "fetch_cut16_replays_20260913m.py")
    copy_patch("autopsy_cut16_20260913l.py", "autopsy_cut16_20260913m.py")
    copy_patch("inspect_cut16_losses_20260913l.py", "inspect_cut16_losses_20260913m.py")
    top = copy_patch("fetch_top_board_20260913l.py", "fetch_top_board_20260913m.py")
    tt = top.read_text(encoding="utf-8")
    tt = tt.replace(
        "SKIP_IDS = {\n    108430587,",
        "SKIP_IDS = {\n    108447904,\n    108441866,\n    108436524,\n    108127188,\n    108430587,",
    )
    top.write_text(tt, encoding="utf-8")
    copy_patch("measure_top_board_20260913l.py", "measure_top_board_20260913m.py")
    scan = copy_patch("scan_hunt_20260913l.py", "scan_hunt_20260913m.py")
    st = scan.read_text(encoding="utf-8")
    print("--- scan ---\n", st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch = (CAND / "fetch_cut16_replays_20260913m.py").read_text(encoding="utf-8")
    print(fetch.split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
