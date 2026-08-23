"""List ih=2 route_a variants."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]


def main():
    d = json.loads((ROOT / "artifacts/variants/kaito_route_a/grid_index.json").read_text(encoding="utf-8"))
    ih2 = [v for v in d["variants"] if v["investment_horizon"] == 2]
    print(f"Total ih=2 variants in route_a: {len(ih2)}")
    for v in ih2:
        name = v["variant_dir"].rsplit("\\", 1)[-1] if "\\" in v["variant_dir"] else v["variant_dir"].rsplit("/", 1)[-1]
        print(
            f"  {name}  msb={v['maximum_sell_batch']}  mr={v['market_reserve']}  "
            f"win=[{v['market_start']},{v['market_stop']}]  sha256={v['sha256'][:16]}"
        )


if __name__ == "__main__":
    main()