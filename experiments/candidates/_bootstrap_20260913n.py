"""Copy 13m cycle scripts to 13n and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

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
PREV_13M = """PREV = {
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
    108328160,
    108311577,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913m", "20260913n")
    text = text.replace("20260913l", "20260913m")
    text = text.replace("09-13l", "09-13m")
    text = text.replace("0913l", "0913m")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913n_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913n"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    for name in lb_src.glob("kaggriculture-publicleaderboard-*.csv"):
        shutil.copy2(name, lb_dst / name.name)
        print("copied csv", name.name)
    for sid in (56151152, 56151155):
        shutil.copy2(lb_src / f"episodes_{sid}.json", ROOT / "experiments" / f"episodes_{sid}.json")
        print("copied episodes", sid)

    live = copy_patch("live_state_20260913m.py", "live_state_20260913n.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13L not in text:
        raise SystemExit("PREV_13L block missing after copy")
    text = text.replace(PREV_13L, PREV_13M)
    text = text.replace('"publicScore": 1693.4', '"publicScore": 1693.6')
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores")

    copy_patch("fetch_cut16_replays_20260913m.py", "fetch_cut16_replays_20260913n.py")
    copy_patch("autopsy_cut16_20260913m.py", "autopsy_cut16_20260913n.py")
    copy_patch("inspect_cut16_losses_20260913m.py", "inspect_cut16_losses_20260913n.py")
    top = copy_patch("fetch_top_board_20260913m.py", "fetch_top_board_20260913n.py")
    tt = top.read_text(encoding="utf-8")
    if "108477110" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108447904,",
            "SKIP_IDS = {\n    108477110,\n    108470978,\n    108464894,\n    108459064,\n    108447904,",
        )
        top.write_text(tt, encoding="utf-8")
    copy_patch("measure_top_board_20260913m.py", "measure_top_board_20260913n.py")
    copy_patch("inspect_hunt_20260913m.py", "inspect_hunt_20260913n.py")
    scan = copy_patch("scan_hunt_20260913m.py", "scan_hunt_20260913n.py")
    print("--- scan ---\n", scan.read_text(encoding="utf-8"))
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch = (CAND / "fetch_cut16_replays_20260913n.py").read_text(encoding="utf-8")
    print(fetch.split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
