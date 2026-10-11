"""Finish remaining 14n script copies after live_state/fetch already exist."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914m", "20260914n")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
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
    old = 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914l"'
    new = 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914m"'
    if old in st:
        scan.write_text(st.replace(old, new), encoding="utf-8")
        print("patched scan PREV to _hunt_20260914m")
    elif new in st:
        print("scan PREV already points at _hunt_20260914m")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914n.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914n.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914n.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
