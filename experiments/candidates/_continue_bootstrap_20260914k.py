"""Finish remaining 14k script copies after live_state/fetch already exist."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "experiments/candidates"


def copy_patch(src_name: str, dst_name: str) -> Path:
    text = (CAND / src_name).read_text(encoding="utf-8")
    text = text.replace("20260914j", "20260914k")
    dst = CAND / dst_name
    dst.write_text(text, encoding="utf-8")
    print("WROTE", dst)
    return dst


def main() -> None:
    copy_patch("autopsy_cut16_20260914j.py", "autopsy_cut16_20260914k.py")
    copy_patch("inspect_cut16_losses_20260914j.py", "inspect_cut16_losses_20260914k.py")
    top = copy_patch("fetch_top_board_20260914j.py", "fetch_top_board_20260914k.py")
    tt = top.read_text(encoding="utf-8")
    if "108878440" not in tt:
        tt = tt.replace(
            "SKIP_IDS = {\n    108860017,",
            "SKIP_IDS = {\n    108878440,\n    108872254,\n    108866071,\n    108694097,\n    108860017,",
        )
        top.write_text(tt, encoding="utf-8")
        print("patched top SKIP_IDS with 14j Majkel ids")
    else:
        print("top SKIP already has 14j Majkel ids")
    copy_patch("measure_top_board_20260914j.py", "measure_top_board_20260914k.py")
    copy_patch("inspect_hunt_20260914j.py", "inspect_hunt_20260914k.py")
    scan = copy_patch("scan_hunt_20260914j.py", "scan_hunt_20260914k.py")
    st = scan.read_text(encoding="utf-8")
    old = 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914k"'
    new = 'PREV = ROOT / "artifacts/public_sources/_hunt_20260914j"'
    if old in st:
        scan.write_text(st.replace(old, new), encoding="utf-8")
        print("patched scan PREV to _hunt_20260914j")
    elif new in st:
        print("scan PREV already points at _hunt_20260914j")
    else:
        print("WARN scan PREV unexpected")
        print(st)
    copy_patch("write_packet_20260914j.py", "write_packet_20260914k.py")
    print("--- fetch PRIOR head ---")
    print((CAND / "fetch_cut16_replays_20260914k.py").read_text(encoding="utf-8").split("PRIOR =", 1)[1][:350])
    print("--- top SKIP head ---")
    print((CAND / "fetch_top_board_20260914k.py").read_text(encoding="utf-8").split("SKIP_IDS =", 1)[1][:250])
    print("--- scan ---")
    print((CAND / "scan_hunt_20260914k.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
