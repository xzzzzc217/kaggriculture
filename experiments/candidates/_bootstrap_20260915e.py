"""Copy 20260915d cycle scripts to 20260915e and patch paths/PREV/scores."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_15C = """PREV = {
    109297997,
    109159847,
    109152510,
    109149160,
    109142116,
    109135062,
    109111080,
    109091091,
    109078755,
    109057555,
    109054323,
    109044160,
}"""
PREV_15D = """PREV = {
    109323301,
    109321947,
    109316981,
    109309340,
    109274859,
    109251218,
    109247247,
    109241224,
    109227483,
    109208871,
    109205772,
    109205359,
}"""


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260915d", "20260915e")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    hunt = ROOT / "artifacts/public_sources/_hunt_20260915e"
    hunt.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/lb_20260915e").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/cut16_20260915e").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/top_20260915e").mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260915d.py", "live_state_20260915e.py")
    text = live.read_text(encoding="utf-8")
    if PREV_15C not in text:
        raise SystemExit("PREV_15C block missing after copy")
    text = text.replace(PREV_15C, PREV_15D)
    text = text.replace('"publicScore": 1578.6', '"publicScore": 1569.5')
    text = text.replace('"publicScore": 1282.2', '"publicScore": 1282.2')
    needle = (
        '    ROOT / "experiments/20260915c_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260915c_top10_games.json",\n'
        '    ROOT / "experiments/20260915d_top10_games.json",\n]'
    )
    if "20260915d_top10_games.json" not in text:
        if needle not in text:
            raise SystemExit("PRIOR tail missing after copy")
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260915d.py", "fetch_cut16_replays_20260915e.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior_after = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260915c",'
    new_prior_after = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260915d",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260915c",'
    )
    head = ft.split("PRIOR =", 1)[1][:500]
    if 'ROOT / "artifacts/kaggle_runs/cut16_20260915d"' in head:
        print("fetch PRIOR already includes 15d")
    elif old_prior_after in ft:
        fetch.write_text(ft.replace(old_prior_after, new_prior_after, 1), encoding="utf-8")
        print("patched fetch PRIOR head to 15d")
    else:
        print("WARN fetch PRIOR head")
        print(head)

    copy_patch("autopsy_cut16_20260915d.py", "autopsy_cut16_20260915e.py")
    copy_patch("inspect_cut16_losses_20260915d.py", "inspect_cut16_losses_20260915e.py")
    top = copy_patch("fetch_top_board_20260915d.py", "fetch_top_board_20260915e.py")
    tt = top.read_text(encoding="utf-8")
    if "109322609" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    109308893,",
            "SKIP_IDS = {\n    109322609,\n    109322470,\n    109315236,\n    109308841,\n    109308893,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 15d Artem ids")
    else:
        print("top SKIP already has 15d Artem ids")
    copy_patch("measure_top_board_20260915d.py", "measure_top_board_20260915e.py")
    copy_patch("inspect_hunt_20260915d.py", "inspect_hunt_20260915e.py")
    scan = copy_patch("scan_hunt_20260915d.py", "scan_hunt_20260915e.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260915c"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260915c"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260915d"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260915d")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260915d"' in st:
        print("scan PREV already points at _hunt_20260915d")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    copy_patch("_extract_hunt_payloads_20260915d.py", "_extract_hunt_payloads_20260915e.py")
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:400])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260915e.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260915e.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260915e.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
