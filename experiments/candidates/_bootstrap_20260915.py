"""Copy 20260914o cycle scripts to 20260915 and patch paths/PREV/scores."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_14O = """PREV = {
    108944173,
    108941028,
    108910147,
    108889446,
    108889378,
    108851261,
    108822458,
    108817790,
    108787437,
    108762693,
    108741805,
    108723413,
}"""
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


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914o", "20260915")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    hunt = ROOT / "artifacts/public_sources/_hunt_20260915"
    hunt.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/lb_20260915").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/cut16_20260915").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/top_20260915").mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260914o.py", "live_state_20260915.py")
    text = live.read_text(encoding="utf-8")
    if PREV_14N not in text:
        raise SystemExit("PREV_14N block missing after copy")
    text = text.replace(PREV_14N, PREV_14O)
    text = text.replace('"publicScore": 1625.8', '"publicScore": 1606.1')
    text = text.replace('"publicScore": 1300.7', '"publicScore": 1293.6')
    needle = (
        '    ROOT / "experiments/20260914m_top10_games.json",\n'
        '    ROOT / "experiments/20260914n_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260914m_top10_games.json",\n'
        '    ROOT / "experiments/20260914n_top10_games.json",\n'
        '    ROOT / "experiments/20260914o_top10_games.json",\n]'
    )
    if "20260914o_top10_games.json" not in text:
        if needle not in text:
            raise SystemExit("PRIOR tail missing after copy")
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260914o.py", "fetch_cut16_replays_20260915.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior_after = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260914n",'
    new_prior_after = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914o",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260914n",'
    )
    if "cut16_20260914o" in ft.split("PRIOR =", 1)[1][:400]:
        print("fetch PRIOR already includes 14o")
    elif old_prior_after in ft:
        fetch.write_text(ft.replace(old_prior_after, new_prior_after, 1), encoding="utf-8")
        print("patched fetch PRIOR head to 14o")
    else:
        raise SystemExit("fetch PRIOR head missing after copy")

    copy_patch("autopsy_cut16_20260914o.py", "autopsy_cut16_20260915.py")
    copy_patch("inspect_cut16_losses_20260914o.py", "inspect_cut16_losses_20260915.py")
    top = copy_patch("fetch_top_board_20260914o.py", "fetch_top_board_20260915.py")
    tt = top.read_text(encoding="utf-8")
    if "108953610" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108939090,",
            "SKIP_IDS = {\n    108953610,\n    108946326,\n    108667748,\n    108663358,\n    108939090,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14o Majkel ids")
    else:
        print("top SKIP already has 14o Majkel ids")
    copy_patch("measure_top_board_20260914o.py", "measure_top_board_20260915.py")
    copy_patch("inspect_hunt_20260914o.py", "inspect_hunt_20260915.py")
    scan = copy_patch("scan_hunt_20260914o.py", "scan_hunt_20260915.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914n"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914n"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260914o"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260914o")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914o"' in st:
        print("scan PREV already points at _hunt_20260914o")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:400])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260915.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260915.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260915.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
