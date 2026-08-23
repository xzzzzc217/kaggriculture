"""Compare route_a variant_000 holdout (the existing 18/20 winner) with route_b holdout."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]


def main():
    for label, path in [
        ("route_a variant_000 holdout", ROOT / "artifacts/evaluations/route_a_smoke/variant_000_holdout.json"),
        ("route_b variant_000 holdout", ROOT / "artifacts/evaluations/route_b_g1/variant_000_holdout.json"),
        ("route_b variant_001 holdout", ROOT / "artifacts/evaluations/route_b_g1/variant_001_holdout.json"),
    ]:
        if not path.exists():
            print(f"  {label}: MISSING")
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        wins = d["wins"]
        games = d["games"]
        pairs = d["pairs"]
        print(f"=== {label} ===")
        print(f"  wins={wins}/{games}  win_rate={d['win_rate']:.1%}")
        print(f"  mean_margin={d['mean_margin']:+.2f}  worst_margin={d['worst_margin']:+.2f}")
        print(f"  paired_positive={d['paired_positive']}/{len(pairs)}")
        print(f"  paired_negative={d['paired_negative']}  paired_zero={d['paired_zero']}")
        print(f"  wilson_95_lower={d['wilson_95_lower']:.4f}")
        print(f"  candidate={d['candidate']}")
        print(f"  pairs: " + ", ".join(f"{p['paired_margin']:+.1f}" for p in pairs))
        print()


if __name__ == "__main__":
    main()