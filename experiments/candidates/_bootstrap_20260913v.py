"""Copy 13u cycle scripts to 13v and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_13T = """PREV = {
    108586169,
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
}"""
PREV_13U = """PREV = {
    108594800,
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
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913u", "20260913v")
    text = text.replace("20260913t", "20260913u")
    text = text.replace("09-13t", "09-13u")
    text = text.replace("0913t", "0913u")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913v_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913v"
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

    hunt = ROOT / "artifacts/public_sources/_hunt_20260913v"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260913u.py", "live_state_20260913v.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13T not in text:
        raise SystemExit("PREV_13T block missing after copy")
    text = text.replace(PREV_13T, PREV_13U)
    text = text.replace('"publicScore": 1669.1', '"publicScore": 1681.2')
    needle = '    ROOT / "experiments/20260913u_top10_games.json",\n    ROOT / "experiments/20260913s_top10_games.json",\n]'
    insert = (
        '    ROOT / "experiments/20260913u_top10_games.json",\n'
        '    ROOT / "experiments/20260913t_top10_games.json",\n'
        '    ROOT / "experiments/20260913s_top10_games.json",\n]'
    )
    if needle not in text:
        needle = (
            '    ROOT / "experiments/20260913u_top10_games.json",\n'
            '    ROOT / "experiments/20260913s_top10_games.json",\n'
            '    ROOT / "experiments/20260913r_top10_games.json",\n]'
        )
        insert = (
            '    ROOT / "experiments/20260913u_top10_games.json",\n'
            '    ROOT / "experiments/20260913t_top10_games.json",\n'
            '    ROOT / "experiments/20260913s_top10_games.json",\n'
            '    ROOT / "experiments/20260913r_top10_games.json",\n]'
        )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260913t_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260913u.py", "fetch_cut16_replays_20260913v.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = '    ROOT / "artifacts/kaggle_runs/cut16_20260913u",\n    ROOT / "artifacts/kaggle_runs/cut16_20260913s",'
    new_prior = (
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913u",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913t",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913s",'
    )
    if old_prior not in ft:
        old_prior = '    ROOT / "artifacts/kaggle_runs/cut16_20260913u",\n    ROOT / "artifacts/kaggle_runs/cut16_20260913t",'
        new_prior = (
            '    ROOT / "artifacts/kaggle_runs/cut16_20260913u",\n'
            '    ROOT / "artifacts/kaggle_runs/cut16_20260913t",\n'
            '    ROOT / "artifacts/kaggle_runs/cut16_20260913s",'
        )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260913t" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 13t")
    else:
        print("fetch PRIOR already includes 13t")

    copy_patch("autopsy_cut16_20260913u.py", "autopsy_cut16_20260913v.py")
    copy_patch("inspect_cut16_losses_20260913u.py", "inspect_cut16_losses_20260913v.py")
    top = copy_patch("fetch_top_board_20260913u.py", "fetch_top_board_20260913v.py")
    tt = top.read_text(encoding="utf-8")
    if "108597320" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108584052,",
            "SKIP_IDS = {\n    108597320,\n    108590386,\n    108066211,\n    108061234,\n    108584052,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 13u Majkel ids")
    copy_patch("measure_top_board_20260913u.py", "measure_top_board_20260913v.py")
    copy_patch("inspect_hunt_20260913u.py", "inspect_hunt_20260913v.py")
    copy_patch("scan_hunt_20260913u.py", "scan_hunt_20260913v.py")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch_text = (CAND / "fetch_cut16_replays_20260913v.py").read_text(encoding="utf-8")
    print(fetch_text.split("PRIOR =", 1)[1][:500])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
