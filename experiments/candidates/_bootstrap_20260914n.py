"""Copy 20260914m cycle scripts to 20260914n and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_14M = """PREV = {
    108910147,
    108889446,
    108889378,
    108851261,
    108822458,
    108817790,
    108787437,
    108762693,
    108723413,
    108704919,
    108686716,
    108669139,
}"""
PREV_14L = """PREV = {
    108871316,
    108846707,
    108842428,
    108814509,
    108810346,
    108807526,
    108784373,
    108781918,
    108753975,
    108751924,
    108744906,
    108741805,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914m", "20260914n")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914n_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914n"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    print("copied zip")

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914n"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914m.py", "live_state_20260914n.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14L not in text:
        raise SystemExit("PREV_14L block missing after copy")
    text = text.replace(PREV_14L, PREV_14M)
    text = text.replace('"publicScore": 1623.1', '"publicScore": 1627.7')
    text = text.replace('"publicScore": 1300.3', '"publicScore": 1300.7')
    needle = (
        '    ROOT / "experiments/20260914k_top10_games.json",\n'
        '    ROOT / "experiments/20260914l_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260914k_top10_games.json",\n'
        '    ROOT / "experiments/20260914l_top10_games.json",\n'
        '    ROOT / "experiments/20260914m_top10_games.json",\n]'
    )
    if "20260914m_top10_games.json" not in text:
        if needle not in text:
            raise SystemExit("PRIOR tail missing after copy")
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914m.py", "fetch_cut16_replays_20260914n.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior_after = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914n",'
    new_prior_after = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914m",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914l",'
    )
    if "cut16_20260914m" in ft.split("PRIOR =", 1)[1][:400]:
        print("fetch PRIOR already includes 14m")
    elif old_prior_after in ft:
        fetch.write_text(ft.replace(old_prior_after, new_prior_after, 1), encoding="utf-8")
        print("patched fetch PRIOR head to 14m")
    else:
        raise SystemExit("fetch PRIOR head missing after copy")

    copy_patch("autopsy_cut16_20260914m.py", "autopsy_cut16_20260914n.py")
    copy_patch("inspect_cut16_losses_20260914m.py", "inspect_cut16_losses_20260914n.py")
    top = copy_patch("fetch_top_board_20260914m.py", "fetch_top_board_20260914n.py")
    tt = top.read_text(encoding="utf-8")
    if "108917355" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108903865,",
            "SKIP_IDS = {\n    108917355,\n    108910285,\n    108681060,\n    108676856,\n    108903865,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14m Majkel ids")
    else:
        print("top SKIP already has 14m Majkel ids")
    copy_patch("measure_top_board_20260914m.py", "measure_top_board_20260914n.py")
    copy_patch("inspect_hunt_20260914m.py", "inspect_hunt_20260914n.py")
    scan = copy_patch("scan_hunt_20260914m.py", "scan_hunt_20260914n.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914l"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914l"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914m"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914m")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914m"' in st:
        print("scan PREV already points at _hunt_20260914m")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:400])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914n.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914n.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914n.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
