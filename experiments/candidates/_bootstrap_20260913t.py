"""Copy 13s cycle scripts to 13t and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_13R = """PREV = {
    108550653,
    108545775,
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
}"""
PREV_13S = """PREV = {
    108568560,
    108559476,
    108534412,
    108504670,
    108472548,
    108461768,
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
    108374873,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913s", "20260913t")
    text = text.replace("20260913r", "20260913s")
    text = text.replace("09-13r", "09-13s")
    text = text.replace("0913r", "0913s")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913t_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913t"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    for name in lb_src.glob("kaggriculture-publicleaderboard-*.csv"):
        shutil.copy2(name, lb_dst / name.name)
        print("copied csv", name.name)
    for sid in (56151152, 56151155):
        src = lb_src / f"episodes_{sid}.json"
        if src.exists():
            shutil.copy2(src, ROOT / "experiments" / f"episodes_{sid}.json")
            print("copied episodes", sid)

    hunt = ROOT / "artifacts/public_sources/_hunt_20260913t"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260913s.py", "live_state_20260913t.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13R not in text:
        raise SystemExit("PREV_13R block missing after copy")
    text = text.replace(PREV_13R, PREV_13S)
    text = text.replace('"publicScore": 1670.2', '"publicScore": 1673.8')
    text = text.replace('"publicScore": 1319.5', '"publicScore": 1314.5')
    needle = '    ROOT / "experiments/20260913s_top10_games.json",\n]'
    insert = (
        '    ROOT / "experiments/20260913s_top10_games.json",\n'
        '    ROOT / "experiments/20260913r_top10_games.json",\n]'
    )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260913r_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260913s.py", "fetch_cut16_replays_20260913t.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = '    ROOT / "artifacts/kaggle_runs/cut16_20260913s",\n    ROOT / "artifacts/kaggle_runs/cut16_20260913q",'
    new_prior = (
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913s",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913r",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913q",'
    )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
    print("patched fetch PRIOR to keep 13r")

    copy_patch("autopsy_cut16_20260913s.py", "autopsy_cut16_20260913t.py")
    copy_patch("inspect_cut16_losses_20260913s.py", "inspect_cut16_losses_20260913t.py")
    top = copy_patch("fetch_top_board_20260913s.py", "fetch_top_board_20260913t.py")
    tt = top.read_text(encoding="utf-8")
    if "108570750" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108550584,",
            "SKIP_IDS = {\n    108570750,\n    108563756,\n    108557488,\n    108081303,\n    108550584,",
        )
        top.write_text(tt, encoding="utf-8")
    copy_patch("measure_top_board_20260913s.py", "measure_top_board_20260913t.py")
    copy_patch("inspect_hunt_20260913s.py", "inspect_hunt_20260913t.py")
    copy_patch("scan_hunt_20260913s.py", "scan_hunt_20260913t.py")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch_text = (CAND / "fetch_cut16_replays_20260913t.py").read_text(encoding="utf-8")
    print(fetch_text.split("PRIOR =", 1)[1][:500])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
