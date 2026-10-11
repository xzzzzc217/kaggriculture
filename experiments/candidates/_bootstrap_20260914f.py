"""Copy 20260914e cycle scripts to 20260914f and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_14E = """PREV = {
    108787437,
    108762693,
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
}"""
PREV_14D = """PREV = {
    108784373,
    108781918,
    108753975,
    108751924,
    108744906,
    108741805,
    108608562,
    108604498,
    108586169,
    108568560,
    108559476,
    108550653,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914e", "20260914f")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914f_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914f"
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

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914f"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914e.py", "live_state_20260914f.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14D not in text:
        raise SystemExit("PREV_14D block missing after copy")
    text = text.replace(PREV_14D, PREV_14E)
    text = text.replace('"publicScore": 1637.6', '"publicScore": 1643.7')
    text = text.replace('"publicScore": 1309.1', '"publicScore": 1304.9')
    needle = (
        '    ROOT / "experiments/20260914c_top10_games.json",\n'
        '    ROOT / "experiments/20260914d_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260914c_top10_games.json",\n'
        '    ROOT / "experiments/20260914d_top10_games.json",\n'
        '    ROOT / "experiments/20260914e_top10_games.json",\n]'
    )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260914e_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914e.py", "fetch_cut16_replays_20260914f.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914d",'
    new_prior = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914e",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914d",'
    )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260914e" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 14e")
    else:
        print("fetch PRIOR already includes 14e")

    copy_patch("autopsy_cut16_20260914e.py", "autopsy_cut16_20260914f.py")
    copy_patch("inspect_cut16_losses_20260914e.py", "inspect_cut16_losses_20260914f.py")
    top = copy_patch("fetch_top_board_20260914e.py", "fetch_top_board_20260914f.py")
    tt = top.read_text(encoding="utf-8")
    if "108801472" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108784043,",
            "SKIP_IDS = {\n    108801472,\n    108795516,\n    108790149,\n    108710580,\n    108784043,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14e Majkel ids")
    else:
        print("top SKIP already has 14e Majkel ids")
    copy_patch("measure_top_board_20260914e.py", "measure_top_board_20260914f.py")
    copy_patch("inspect_hunt_20260914e.py", "inspect_hunt_20260914f.py")
    scan = copy_patch("scan_hunt_20260914e.py", "scan_hunt_20260914f.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914d"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914d"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914e"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914e")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914e"' in st:
        print("scan PREV already points at _hunt_20260914e")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914f.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914f.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914f.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
