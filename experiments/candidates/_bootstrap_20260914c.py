"""Copy 20260914b cycle scripts to 20260914c and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

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
PREV_14B = """PREV = {
    108753975,
    108751924,
    108744906,
    108741805,
    108608562,
    108604498,
    108586169,
    108559476,
    108550653,
    108545775,
    108534412,
    108520439,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914b", "20260914c")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914c_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914c"
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

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914c"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914b.py", "live_state_20260914c.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14 not in text:
        raise SystemExit("PREV_14 block missing after copy")
    text = text.replace(PREV_14, PREV_14B)
    text = text.replace('"publicScore": 1644.6', '"publicScore": 1639.4')
    needle = (
        '    ROOT / "experiments/20260913s_top10_games.json",\n'
        '    ROOT / "experiments/20260913r_top10_games.json",\n'
        '    ROOT / "experiments/20260914_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260913s_top10_games.json",\n'
        '    ROOT / "experiments/20260913r_top10_games.json",\n'
        '    ROOT / "experiments/20260914_top10_games.json",\n'
        '    ROOT / "experiments/20260914b_top10_games.json",\n]'
    )
    if needle not in text:
        raise SystemExit("PRIOR tail missing after copy")
    if "20260914b_top10_games.json" not in text:
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914b.py", "fetch_cut16_replays_20260914c.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914",'
    new_prior = (
        'PRIOR = [\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914b",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914",'
    )
    if old_prior not in ft:
        raise SystemExit("fetch PRIOR head missing after copy")
    if "cut16_20260914b" not in ft.split("PRIOR =", 1)[1][:400]:
        fetch.write_text(ft.replace(old_prior, new_prior, 1), encoding="utf-8")
        print("patched fetch PRIOR to keep 14b")
    else:
        print("fetch PRIOR already includes 14b")

    copy_patch("autopsy_cut16_20260914b.py", "autopsy_cut16_20260914c.py")
    copy_patch("inspect_cut16_losses_20260914b.py", "inspect_cut16_losses_20260914c.py")
    top = copy_patch("fetch_top_board_20260914b.py", "fetch_top_board_20260914c.py")
    tt = top.read_text(encoding="utf-8")
    if "108751322" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108737107,",
            "SKIP_IDS = {\n    108751322,\n    108746349,\n    108741955,\n    108719359,\n    108737107,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14b Majkel ids")
    else:
        print("top SKIP already has 14b Majkel ids")
    copy_patch("measure_top_board_20260914b.py", "measure_top_board_20260914c.py")
    copy_patch("inspect_hunt_20260914b.py", "inspect_hunt_20260914c.py")
    scan = copy_patch("scan_hunt_20260914b.py", "scan_hunt_20260914c.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914b"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914b")
    else:
        print("scan PREV already points at _hunt_20260914b")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:500])
    print("--- fetch PRIOR head ---")
    fetch_text = (CAND / "fetch_cut16_replays_20260914c.py").read_text(encoding="utf-8")
    print(fetch_text.split("PRIOR =", 1)[1][:500])
    print("--- top SKIP head ---")
    print(tt.split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print(scan.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
