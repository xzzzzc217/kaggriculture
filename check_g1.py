"""Read G1 holdout results and check gate criteria."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
G1 = ROOT / "artifacts" / "evaluations" / "route_b_g1"


def main():
    print(f"=== G1 holdout results (20 games each, vs h2 champion) ===\n")
    for v in ["variant_000", "variant_001", "variant_002", "variant_011", "variant_018", "variant_019"]:
        path = G1 / f"{v}_holdout.json"
        if not path.exists():
            print(f"  {v}: MISSING\n")
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        wins = d["wins"]
        games = d["games"]
        pairs = d["pairs"]
        g1_wins = wins >= 18
        g1_paired = d["paired_positive"] == 10
        g1_mean = d["mean_margin"] >= 15.0
        g1_worst = d["worst_margin"] >= -400.0
        g1_pass = g1_wins and g1_paired and g1_mean and g1_worst
        print(f"=== {v} ===")
        print(f"  wins={wins}/{games}  win_rate={d['win_rate']:.1%}")
        print(f"  mean_margin={d['mean_margin']:+.2f}  worst_margin={d['worst_margin']:+.2f}")
        print(f"  paired_positive={d['paired_positive']}/{len(pairs)}")
        print(f"  paired_negative={d['paired_negative']}  paired_zero={d['paired_zero']}")
        print(f"  wilson_95_lower={d['wilson_95_lower']:.4f}")
        print(f"  G1 gate: wins>=18/20: {g1_wins}, paired+==10/10: {g1_paired}, mean>=+15: {g1_mean}, worst>=-400: {g1_worst}")
        print(f"  G1 PASS: {g1_pass}")
        # Show paired margins
        print(f"  paired_margins: " + ", ".join(f"{p['paired_margin']:+.1f}" for p in pairs))
        print()


if __name__ == "__main__":
    main()