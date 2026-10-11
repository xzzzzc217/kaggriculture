"""Copy 13n cycle scripts to 13o and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

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
PREV_13N = """PREV = {
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
    108349751,
    108345614,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913n", "20260913o")
    text = text.replace("20260913m", "20260913n")
    text = text.replace("09-13m", "09-13n")
    text = text.replace("0913m", "0913n")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913o_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913o"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    for name in lb_src.glob("kaggriculture-publicleaderboard-*.csv"):
        shutil.copy2(name, lb_dst / name.name)
        print("copied csv", name.name)
    for sid in (56151152, 56151155):
        shutil.copy2(lb_src / f"episodes_{sid}.json", ROOT / "experiments" / f"episodes_{sid}.json")
        print("copied episodes", sid)

    live = copy_patch("live_state_20260913n.py", "live_state_20260913o.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13M not in text:
        raise SystemExit("PREV_13M block missing after copy")
    text = text.replace(PREV_13M, PREV_13N)
    text = text.replace('"publicScore": 1693.6', '"publicScore": 1690.5')
    text = text.replace('"publicScore": 1332.1', '"publicScore": 1328.0')
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores")

    copy_patch("fetch_cut16_replays_20260913n.py", "fetch_cut16_replays_20260913o.py")
    copy_patch("autopsy_cut16_20260913n.py", "autopsy_cut16_20260913o.py")
    copy_patch("inspect_cut16_losses_20260913n.py", "inspect_cut16_losses_20260913o.py")
    top = copy_patch("fetch_top_board_20260913n.py", "fetch_top_board_20260913o.py")
    tt = top.read_text(encoding="utf-8")
    if "108494524" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108477110,",
            "SKIP_IDS = {\n    108494524,\n    108488494,\n    108483149,\n    108453811,\n    108477110,",
        )
        top.write_text(tt, encoding="utf-8")
    copy_patch("measure_top_board_20260913n.py", "measure_top_board_20260913o.py")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch = (CAND / "fetch_cut16_replays_20260913o.py").read_text(encoding="utf-8")
    print(fetch.split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
