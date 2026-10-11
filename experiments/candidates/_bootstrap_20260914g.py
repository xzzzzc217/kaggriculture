"""Copy 20260914f cycle scripts to 20260914g and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

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


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914f", "20260914g")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914g_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914g"
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

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914g"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914f.py", "live_state_20260914g.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14E not in text:
        raise SystemExit("PREV_14E block missing after copy")
    text = text.replace(PREV_14E, PREV_14F)
    text = text.replace('"publicScore": 1643.7', '"publicScore": 1636.0')
    text = text.replace('"publicScore": 1304.9', '"publicScore": 1304.9')
    needle = (
        '    ROOT / "experiments/20260914d_top10_games.json",\n'
        '    ROOT / "experiments/20260914e_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260914d_top10_games.json",\n'
        '    ROOT / "experiments/20260914e_top10_games.json",\n'
        '    ROOT / "experiments/20260914f_top10_games.json",\n]'
    )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260914f_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914f.py", "fetch_cut16_replays_20260914g.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914e",'
    new_prior = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914f",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914e",'
    )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260914f" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 14f")
    else:
        print("fetch PRIOR already includes 14f")

    copy_patch("autopsy_cut16_20260914f.py", "autopsy_cut16_20260914g.py")
    copy_patch("inspect_cut16_losses_20260914f.py", "inspect_cut16_losses_20260914g.py")
    top = copy_patch("fetch_top_board_20260914f.py", "fetch_top_board_20260914g.py")
    tt = top.read_text(encoding="utf-8")
    if "108813738" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108801472,",
            "SKIP_IDS = {\n    108813738,\n    108807571,\n    108710581,\n    108706451,\n    108801472,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14f Majkel ids")
    else:
        print("top SKIP already has 14f Majkel ids")
    copy_patch("measure_top_board_20260914f.py", "measure_top_board_20260914g.py")
    copy_patch("inspect_hunt_20260914f.py", "inspect_hunt_20260914g.py")
    scan = copy_patch("scan_hunt_20260914f.py", "scan_hunt_20260914g.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914e"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914e"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914f"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914f")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914f"' in st:
        print("scan PREV already points at _hunt_20260914f")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914g.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:400])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914g.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914g.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
