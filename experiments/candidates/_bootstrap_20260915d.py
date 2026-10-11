"""Copy 20260915c cycle scripts to 20260915d and patch paths/PREV/scores."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_15B = """PREV = {
    109274859,
    109251218,
    109247247,
    109241224,
    109227483,
    109208871,
    109205772,
    109205359,
    109184094,
    109178619,
    109169017,
    109168637,
}"""
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


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260915c", "20260915d")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    hunt = ROOT / "artifacts/public_sources/_hunt_20260915d"
    hunt.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/lb_20260915d").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/cut16_20260915d").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/top_20260915d").mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260915c.py", "live_state_20260915d.py")
    text = live.read_text(encoding="utf-8")
    if PREV_15B not in text:
        raise SystemExit("PREV_15B block missing after copy")
    text = text.replace(PREV_15B, PREV_15C)
    text = text.replace('"publicScore": 1582.4', '"publicScore": 1578.6')
    text = text.replace('"publicScore": 1286.1', '"publicScore": 1282.2')
    needle = (
        '    ROOT / "experiments/20260915b_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260915b_top10_games.json",\n'
        '    ROOT / "experiments/20260915c_top10_games.json",\n]'
    )
    if "20260915c_top10_games.json" not in text:
        if needle not in text:
            raise SystemExit("PRIOR tail missing after copy")
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260915c.py", "fetch_cut16_replays_20260915d.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior_after = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260915b",'
    new_prior_after = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260915c",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260915b",'
    )
    head = ft.split("PRIOR =", 1)[1][:500]
    if 'ROOT / "artifacts/kaggle_runs/cut16_20260915c"' in head:
        print("fetch PRIOR already includes 15c")
    elif old_prior_after in ft:
        fetch.write_text(ft.replace(old_prior_after, new_prior_after, 1), encoding="utf-8")
        print("patched fetch PRIOR head to 15c")
    else:
        print("WARN fetch PRIOR head")
        print(head)

    copy_patch("autopsy_cut16_20260915c.py", "autopsy_cut16_20260915d.py")
    copy_patch("inspect_cut16_losses_20260915c.py", "inspect_cut16_losses_20260915d.py")
    top = copy_patch("fetch_top_board_20260915c.py", "fetch_top_board_20260915d.py")
    tt = top.read_text(encoding="utf-8")
    if "109308893" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    109290715,",
            "SKIP_IDS = {\n    109308893,\n    109302525,\n    109302443,\n    109296294,\n    109290715,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 15c Majkel ids")
    else:
        print("top SKIP already has 15c Majkel ids")
    copy_patch("measure_top_board_20260915c.py", "measure_top_board_20260915d.py")
    copy_patch("inspect_hunt_20260915c.py", "inspect_hunt_20260915d.py")
    scan = copy_patch("scan_hunt_20260915c.py", "scan_hunt_20260915d.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260915b"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260915b"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260915c"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260915c")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260915c"' in st:
        print("scan PREV already points at _hunt_20260915c")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:400])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260915d.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260915d.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260915d.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
