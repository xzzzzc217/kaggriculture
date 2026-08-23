"""Check Boat and Moon regression results for variant_001 and variant_019."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]


def main():
    for variant in ["variant_001", "variant_019"]:
        print(f"=== {variant} regression gates ===\n")
        for label, path in [
            ("vs h2 (G1)", ROOT / f"artifacts/evaluations/route_b_g1/{variant}_holdout.json"),
            ("vs Boatlee (G2)", ROOT / f"artifacts/evaluations/route_b_g1/{variant}_vs_boat.json"),
            ("vs Moon (G3)", ROOT / f"artifacts/evaluations/route_b_g1/{variant}_vs_moon.json"),
        ]:
            if not path.exists():
                print(f"  {label}: MISSING\n")
                continue
            d = json.loads(path.read_text(encoding="utf-8"))
            print(f"=== {label} ===")
            print(f"  wins={d['wins']}/{d['games']}  win_rate={d['win_rate']:.1%}")
            print(f"  mean_margin={d['mean_margin']:+.2f}  worst_margin={d['worst_margin']:+.2f}")
            print(f"  paired_positive={d['paired_positive']}/{len(d['pairs'])}")
            print(f"  paired_negative={d['paired_negative']}  paired_zero={d['paired_zero']}")
            print(f"  wilson_95_lower={d['wilson_95_lower']:.4f}")
            print()
        print()


if __name__ == "__main__":
    main()