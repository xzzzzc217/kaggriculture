"""Copy 20260914 cycle scripts to 20260914b and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_13V = """PREV = {
    108608562,
    108604498,
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
}"""
PREV_14 = """PREV = {
    108723413,
    108704919,
    108686716,
    108669139,
    108658948,
    108656070,
    108642657,
    108636667,
    108635673,
    108620320,
    108594800,
    108568560,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914", "20260914b")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914b_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914b"
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

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914b"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914.py", "live_state_20260914b.py")
    text = live.read_text(encoding="utf-8")
    if PREV_13V not in text:
        raise SystemExit("PREV_13V block missing after copy")
    text = text.replace(PREV_13V, PREV_14)
    text = text.replace('"publicScore": 1654.7', '"publicScore": 1644.6')
    text = text.replace('"publicScore": 1309.4', '"publicScore": 1310.6')
    needle = (
        '    ROOT / "experiments/20260913v_top10_games.json",\n'
        '    ROOT / "experiments/20260913u_top10_games.json",\n'
        '    ROOT / "experiments/20260913t_top10_games.json",\n'
        '    ROOT / "experiments/20260913s_top10_games.json",\n'
        '    ROOT / "experiments/20260913r_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260913v_top10_games.json",\n'
        '    ROOT / "experiments/20260913u_top10_games.json",\n'
        '    ROOT / "experiments/20260913t_top10_games.json",\n'
        '    ROOT / "experiments/20260913s_top10_games.json",\n'
        '    ROOT / "experiments/20260913r_top10_games.json",\n'
        '    ROOT / "experiments/20260914_top10_games.json",\n]'
    )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260914_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914.py", "fetch_cut16_replays_20260914b.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260913v",'
    new_prior = (
        'PRIOR = [\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260913v",'
    )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260914\"" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 14")
    else:
        print("fetch PRIOR already includes 14")

    copy_patch("autopsy_cut16_20260914.py", "autopsy_cut16_20260914b.py")
    copy_patch("inspect_cut16_losses_20260914.py", "inspect_cut16_losses_20260914b.py")
    top = copy_patch("fetch_top_board_20260914.py", "fetch_top_board_20260914b.py")
    tt = top.read_text(encoding="utf-8")
    if "108737107" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108610498,",
            "SKIP_IDS = {\n    108737107,\n    108732800,\n    108727954,\n    108723695,\n    108610498,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14 Majkel ids")
    else:
        print("top SKIP already has 14 Majkel ids")
    copy_patch("measure_top_board_20260914.py", "measure_top_board_20260914b.py")
    copy_patch("inspect_hunt_20260914.py", "inspect_hunt_20260914b.py")
    scan = copy_patch("scan_hunt_20260914.py", "scan_hunt_20260914b.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260913v"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260913v"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914")
    else:
        print("scan PREV already points at _hunt_20260914")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch_text = (CAND / "fetch_cut16_replays_20260914b.py").read_text(encoding="utf-8")
    print(fetch_text.split("PRIOR =", 1)[1][:500])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print(scan.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
