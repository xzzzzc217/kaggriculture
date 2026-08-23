"""Check agent SHA matches between route_a and route_b."""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    print("=== Direct file SHAs ===")
    files = [
        ROOT / "artifacts/variants/kaito_route_a/variant_000/main.py",
        ROOT / "artifacts/variants/kaito_route_a/variant_009/main.py",
        ROOT / "artifacts/variants/kaito_route_b/variant_000/main.py",
        ROOT / "artifacts/variants/kaito_route_b/variant_001/main.py",
        ROOT / "main.py",
    ]
    for f in files:
        print(f"  {sha(f)[:16]}  {os.path.getsize(f):>6}  {f}")

    print("\n=== Route A grid variant_000/009 entries ===")
    d = json.loads((ROOT / "artifacts/variants/kaito_route_a/grid_index.json").read_text(encoding="utf-8"))
    for v in d["variants"]:
        if v["variant_dir"].endswith("variant_000") or v["variant_dir"].endswith("variant_009"):
            name = v["variant_dir"].rsplit("\\", 1)[-1]
            print(
                f"  {name}  sha={v['sha256'][:16]}  "
                f"msb={v['maximum_sell_batch']}  ih={v['investment_horizon']}  "
                f"mr={v['market_reserve']}  win=[{v['market_start']},{v['market_stop']}]"
            )

    print("\n=== Route B grid variant_000/001 entries ===")
    d = json.loads((ROOT / "artifacts/variants/kaito_route_b/grid_index.json").read_text(encoding="utf-8"))
    for v in d["variants"][:2]:
        name = v["variant_dir"].rsplit("\\", 1)[-1]
        print(
            f"  {name}  route_a={v['route_a_variant_id']}  sha={v['sha256'][:16]}  "
            f"msb={v['maximum_sell_batch']}  ih={v['investment_horizon']}  "
            f"mr={v['market_reserve']}  win=[{v['market_start']},{v['market_stop']}]"
        )


if __name__ == "__main__":
    main()