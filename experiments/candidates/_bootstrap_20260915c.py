"""Copy 20260915b cycle scripts to 20260915c and patch paths/PREV/scores."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"

PREV_15 = """PREV = {
    109142116,
    109135062,
    109111080,
    109091091,
    109078755,
    109057555,
    109054323,
    109044160,
    109042689,
    109030720,
    109029822,
    109024708,
}"""
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


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260915b", "20260915c")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    hunt = ROOT / "artifacts/public_sources/_hunt_20260915c"
    hunt.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/lb_20260915c").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/cut16_20260915c").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts/kaggle_runs/top_20260915c").mkdir(parents=True, exist_ok=True)

    live = copy_patch("live_state_20260915b.py", "live_state_20260915c.py")
    text = live.read_text(encoding="utf-8")
    if PREV_15 not in text:
        raise SystemExit("PREV_15 block missing after copy")
    text = text.replace(PREV_15, PREV_15B)
    text = text.replace('"publicScore": 1588.3', '"publicScore": 1582.4')
    text = text.replace('"publicScore": 1286.1', '"publicScore": 1286.1')
    needle = (
        '    ROOT / "experiments/20260915_top10_games.json",\n]'
    )
    insert = (
        '    ROOT / "experiments/20260915_top10_games.json",\n'
        '    ROOT / "experiments/20260915b_top10_games.json",\n]'
    )
    if "20260915b_top10_games.json" not in text:
        if needle not in text:
            raise SystemExit("PRIOR tail missing after copy")
        text = text.replace(needle, insert)
    live.write_text(text, encoding="utf-8")
    print("patched live_state PREV+scores+PRIOR")

    fetch = copy_patch("fetch_cut16_replays_20260915b.py", "fetch_cut16_replays_20260915c.py")
    ft = fetch.read_text(encoding="utf-8")
    old_prior_after = 'PRIOR = [\n    ROOT / "artifacts/kaggle_runs/cut16_20260915",'
    new_prior_after = (
        "PRIOR = [\n"
        '    ROOT / "artifacts/kaggle_runs/cut16_20260915b",\n'
        '    ROOT / "artifacts/kaggle_runs/cut16_20260915",'
    )
    head = ft.split("PRIOR =", 1)[1][:500]
    if 'ROOT / "artifacts/kaggle_runs/cut16_20260915b"' in head:
        print("fetch PRIOR already includes 15b")
    elif old_prior_after in ft:
        fetch.write_text(ft.replace(old_prior_after, new_prior_after, 1), encoding="utf-8")
        print("patched fetch PRIOR head to 15b")
    else:
        print("WARN fetch PRIOR head")
        print(head)

    copy_patch("autopsy_cut16_20260915b.py", "autopsy_cut16_20260915c.py")
    copy_patch("inspect_cut16_losses_20260915b.py", "inspect_cut16_losses_20260915c.py")
    top = copy_patch("fetch_top_board_20260915b.py", "fetch_top_board_20260915c.py")
    tt = top.read_text(encoding="utf-8")
    if "109290715" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    109138748,",
            "SKIP_IDS = {\n    109290715,\n    109290020,\n    109284452,\n    109278362,\n    109138748,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 15b Majkel ids")
    else:
        print("top SKIP already has 15b Majkel ids")
    copy_patch("measure_top_board_20260915b.py", "measure_top_board_20260915c.py")
    copy_patch("inspect_hunt_20260915b.py", "inspect_hunt_20260915c.py")
    scan = copy_patch("scan_hunt_20260915b.py", "scan_hunt_20260915c.py")
    st = scan.read_text(encoding="utf-8")
    if 'PREV = ROOT / "artifacts/public_sources/_hunt_20260915"' in st:
        st = st.replace(
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260915"',
            'PREV = ROOT / "artifacts/public_sources/_hunt_20260915b"',
        )
        scan.write_text(st, encoding="utf-8")
        print("patched scan PREV to _hunt_20260915b")
    elif 'PREV = ROOT / "artifacts/public_sources/_hunt_20260915b"' in st:
        print("scan PREV already points at _hunt_20260915b")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- live PREV head ---")
    print(live.read_text(encoding="utf-8").split("PREV =", 1)[1][:400])
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260915c.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260915c.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260915c.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
