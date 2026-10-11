"""Copy 20260914n cycle scripts to 20260914o and patch paths/PREV/scores."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_14N = """PREV = {
    108930713,
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
}"""
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


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914n", "20260914o")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    lb_src = ROOT / "artifacts/kaggle_runs/lb_20260914o_live"
    lb_dst = ROOT / "artifacts/kaggle_runs/lb_20260914o"
    lb_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lb_src / "kaggriculture.zip", lb_dst / "kaggriculture.zip")
    print("copied zip")

    hunt = ROOT / "artifacts/public_sources/_hunt_20260914o"
    hunt.mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914n.py", "live_state_20260914o.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14M not in text:
        raise SystemExit("PREV_14M block missing after copy")
    text = text.replace(PREV_14M, PREV_14N)
    text = text.replace('"publicScore": 1627.7', '"publicScore": 1625.8')
    text = text.replace('"publicScore": 1300.7', '"publicScore": 1300.7')
    needle = (
        '    ROOT / "experiments/20260914l_top10_games.json",\n'
        '    ROOT / "experiments/20260914m_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260914l_top10_games.json",\n'
        '    ROOT / "experiments/20260914m_top10_games.json",\n'
        '    ROOT / "experiments/20260914n_top10_games.json",\n]'
    )
    if "20260914n_top10_games.json" not in text:
        if needle not in text:
            raise SystemExit("PRIOR tail missing after copy")
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914n.py", "fetch_cut16_replays_20260914o.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior_after = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914m",'
    new_prior_after = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914n",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914m",'
    )
    if "cut16_20260914n" in ft.split("PRIOR =", 1)[1][:400]:
        print("fetch PRIOR already includes 14n")
    elif old_prior_after in ft:
        fetch.write_text(ft.replace(old_prior_after, new_prior_after, 1), encoding="utf-8")
        print("patched fetch PRIOR head to 14n")
    else:
        raise SystemExit("fetch PRIOR head missing after copy")

    copy_patch("autopsy_cut16_20260914n.py", "autopsy_cut16_20260914o.py")
    copy_patch("inspect_cut16_losses_20260914n.py", "inspect_cut16_losses_20260914o.py")
    top = copy_patch("fetch_top_board_20260914n.py", "fetch_top_board_20260914o.py")
    tt = top.read_text(encoding="utf-8")
    if "108939090" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108917355,",
            "SKIP_IDS = {\n    108939090,\n    108931874,\n    108924592,\n    108672552,\n    108917355,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14n Majkel ids")
    else:
        print("top SKIP already has 14n Majkel ids")
    copy_patch("measure_top_board_20260914n.py", "measure_top_board_20260914o.py")
    copy_patch("inspect_hunt_20260914n.py", "inspect_hunt_20260914o.py")
    scan = copy_patch("scan_hunt_20260914n.py", "scan_hunt_20260914o.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914m"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914m"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914n"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914n")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914n"' in st:
        print("scan PREV already points at _hunt_20260914n")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:400])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914o.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914o.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914o.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
