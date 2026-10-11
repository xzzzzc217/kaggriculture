"""Copy 20260914g cycle scripts to 20260914h and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_14G = """PREV = {
    108822458,
    108817790,
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
}"""
PREV_14F = """PREV = {
    108814509,
    108810346,
    108807526,
    108784373,
    108781918,
    108753975,
    108751924,
    108744906,
    108741805,
    108608562,
    108604498,
    108594800,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914g", "20260914h")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914h_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914h"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    for name in lb_src.glob("kaggriculture-publicleaderboard-*.csv"):
        shutil.copy2(name, lb_dst / name.name)
        print("copied csv", name.name)

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914h"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914g.py", "live_state_20260914h.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14F not in text:
        raise SystemExit("PREV_14F block missing after copy")
    text = text.replace(PREV_14F, PREV_14G)
    text = text.replace('"publicScore": 1636.0', '"publicScore": 1636.5')
    text = text.replace('"publicScore": 1304.9', '"publicScore": 1298.7')
    needle = (
        '    ROOT / "experiments/20260914e_top10_games.json",\n'
        '    ROOT / "experiments/20260914f_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260914e_top10_games.json",\n'
        '    ROOT / "experiments/20260914f_top10_games.json",\n'
        '    ROOT / "experiments/20260914g_top10_games.json",\n]'
    )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260914g_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914g.py", "fetch_cut16_replays_20260914h.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914f",'
    new_prior = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914g",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914f",'
    )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260914g" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 14g")
    else:
        print("fetch PRIOR already includes 14g")

    copy_patch("autopsy_cut16_20260914g.py", "autopsy_cut16_20260914h.py")
    copy_patch("inspect_cut16_losses_20260914g.py", "inspect_cut16_losses_20260914h.py")
    top = copy_patch("fetch_top_board_20260914g.py", "fetch_top_board_20260914h.py")
    tt = top.read_text(encoding="utf-8")
    if "108831165" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108813738,",
            "SKIP_IDS = {\n    108831165,\n    108825010,\n    108819121,\n    108706449,\n    108813738,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14g Majkel ids")
    else:
        print("top SKIP already has 14g Majkel ids")
    copy_patch("measure_top_board_20260914g.py", "measure_top_board_20260914h.py")
    copy_patch("inspect_hunt_20260914g.py", "inspect_hunt_20260914h.py")
    scan = copy_patch("scan_hunt_20260914g.py", "scan_hunt_20260914h.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914f"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914f"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914g"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914g")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914g"' in st:
        print("scan PREV already points at _hunt_20260914g")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914h.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914h.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914h.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
