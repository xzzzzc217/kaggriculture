"""Copy 13t cycle scripts to 13u and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

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


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260913t", "20260913u")
    text = text.replace("20260913s", "20260913t")
    text = text.replace("09-13s", "09-13t")
    text = text.replace("0913s", "0913t")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260913u_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260913u"
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

    hunt = ROOT / "artifacts/public_sources/_hunt_20260913u"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260913t.py", "live_state_20260913u.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13S not in text:
        raise SystemExit("PREV_13S block missing after copy")
    text = text.replace(PREV_13S, PREV_13T)
    text = text.replace('"publicScore": 1673.8', '"publicScore": 1669.1')
    needle = '    ROOT / "experiments/20260913t_top10_games.json",\n]'
    insert = (
        '    ROOT / "experiments/20260913t_top10_games.json",\n'
        '    ROOT / "experiments/20260913s_top10_games.json",\n]'
    )
    if needle not in text:
        # after s->t the tail may still list 13t then 13r
        needle = '    ROOT / "experiments/20260913t_top10_games.json",\n    ROOT / "experiments/20260913r_top10_games.json",\n]'
        insert = (
            '    ROOT / "experiments/20260913t_top10_games.json",\n'
            '    ROOT / "experiments/20260913s_top10_games.json",\n'
            '    ROOT / "experiments/20260913r_top10_games.json",\n]'
        )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260913s_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260913t.py", "fetch_cut16_replays_20260913u.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = '    ROOT / "artifacts/kaggle_runs/cut16_20260913t",\n    ROOT / "artifacts/kaggle_runs/cut16_20260913r",'
    new_prior = (
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913t",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913s",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913r",'
    )
    if old_prior not in ft:
        old_prior = '    ROOT / "artifacts/kaggle_runs/cut16_20260913t",\n    ROOT / "artifacts/kaggle_runs/cut16_20260913s",'
        new_prior = (
            '    ROOT / "artifacts/kaggle_runs/cut16_20260913t",\n'
            '    ROOT / "artifacts/kaggle_runs/cut16_20260913s",\n'
            '    ROOT / "artifacts/kaggle_runs/cut16_20260913r",'
        )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260913s" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 13s")
    else:
        print("fetch PRIOR already includes 13s")

    copy_patch("autopsy_cut16_20260913t.py", "autopsy_cut16_20260913u.py")
    copy_patch("inspect_cut16_losses_20260913t.py", "inspect_cut16_losses_20260913u.py")
    top = copy_patch("fetch_top_board_20260913t.py", "fetch_top_board_20260913u.py")
    tt = top.read_text(encoding="utf-8")
    if "108584052" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108570750,",
            "SKIP_IDS = {\n    108584052,\n    108577054,\n    108076337,\n    108071295,\n    108570750,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 13t Majkel ids")
    copy_patch("measure_top_board_20260913t.py", "measure_top_board_20260913u.py")
    copy_patch("inspect_hunt_20260913t.py", "inspect_hunt_20260913u.py")
    copy_patch("scan_hunt_20260913t.py", "scan_hunt_20260913u.py")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch_text = (CAND / "fetch_cut16_replays_20260913u.py").read_text(encoding="utf-8")
    print(fetch_text.split("PRIOR =", 1)[1][:500])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])


if __name__ == "__main__":
    main()
