"""Inspect Route B smoke results in detail and pick top-3 candidates."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
SMOKE = ROOT / "artifacts" / "evaluations" / "route_b_smoke" / "smoke_results.json"

# Debug
print(f"Looking for smoke results at: {SMOKE}")


def main():
    d = json.loads(SMOKE.read_text(encoding="utf-8"))
    ranked = d["ranked"]
    n_seeds = len(d["seeds"])

    print(f"=== Route B smoke results: {len(ranked)} variants × {n_seeds} seeds × 2 seats ===\n")

    print("=== Sort 1: default (paired_positive desc, mean_margin desc, win_rate desc) ===")
    for i, r in enumerate(ranked[:10], 1):
        k = r.get("knobs", {})
        print(
            f"  {i:2d}. {r['variant_id']}  route_a={k.get('route_a_variant_id')}  "
            f"W={r['wins']}/{r['games']}  mean={r['mean_margin']:+.1f}  "
            f"worst={r['worst_margin']:+.1f}  paired+={r['paired_positive']}/{n_seeds}  "
            f"msb={k.get('maximum_sell_batch')} ih={k.get('investment_horizon')} "
            f"mr={k.get('market_reserve')} window=[{k.get('market_start')},{k.get('market_stop')}]"
        )

    print("\n=== Sort 2: paired_positive>=4 then mean_margin (user's true criteria) ===")
    filtered = [r for r in ranked if r["paired_positive"] >= 4]
    filtered.sort(key=lambda r: (-r["paired_positive"], -r["mean_margin"]))
    for i, r in enumerate(filtered[:15], 1):
        k = r.get("knobs", {})
        print(
            f"  {i:2d}. {r['variant_id']}  route_a={k.get('route_a_variant_id')}  "
            f"W={r['wins']}/{r['games']}  mean={r['mean_margin']:+.1f}  "
            f"worst={r['worst_margin']:+.1f}  paired+={r['paired_positive']}/{n_seeds}  "
            f"msb={k.get('maximum_sell_batch')} ih={k.get('investment_horizon')} "
            f"mr={k.get('market_reserve')} window=[{k.get('market_start')},{k.get('market_stop')}]"
        )

    print("\n=== Sort 3: pure mean_margin (top 10 raw margin) ===")
    by_margin = sorted(ranked, key=lambda r: -r["mean_margin"])
    for i, r in enumerate(by_margin[:10], 1):
        k = r.get("knobs", {})
        print(
            f"  {i:2d}. {r['variant_id']}  W={r['wins']}/{r['games']}  "
            f"mean={r['mean_margin']:+.1f}  worst={r['worst_margin']:+.1f}  "
            f"paired+={r['paired_positive']}/{n_seeds}  msb={k.get('maximum_sell_batch')} "
            f"ih={k.get('investment_horizon')} mr={k.get('market_reserve')} "
            f"window=[{k.get('market_start')},{k.get('market_stop')}]"
        )

    # Identify the README-named "variant_000 (msb=50, mr=300, window=[60,700], ih=2)" baseline
    print("\n=== Variant_000 (named prior champion) ===")
    for r in ranked:
        if r["variant_id"] == "variant_000":
            k = r.get("knobs", {})
            print(
                f"  variant_000  route_a={k.get('route_a_variant_id')}  "
                f"W={r['wins']}/{r['games']}  mean={r['mean_margin']:+.1f}  "
                f"worst={r['worst_margin']:+.1f}  paired+={r['paired_positive']}/{n_seeds}  "
                f"msb={k.get('maximum_sell_batch')} ih={k.get('investment_horizon')} "
                f"mr={k.get('market_reserve')} window=[{k.get('market_start')},{k.get('market_stop')}]"
            )

    # Summary: list all 27 ranked variants with paired+, wins, mean_margin
    print("\n=== All 27 variants (sorted by smoke output) ===")
    print(f"{'#':>3}  {'vid':<12}  {'W/D/L':>8}  {'mean':>8}  {'worst':>8}  {'p+':>3}  knobs")
    for i, r in enumerate(ranked, 1):
        k = r.get("knobs", {})
        wins = r["wins"]
        ties = r.get("ties", 0)
        games = r["games"]
        wld = f"{wins}/{ties}/{games - wins - ties}"
        knobs_str = f"msb={k.get('maximum_sell_batch')} ih={k.get('investment_horizon')} mr={k.get('market_reserve')} win=[{k.get('market_start')},{k.get('market_stop')}]"
        print(f"{i:3d}  {r['variant_id']:<12}  {wld:>8}  {r['mean_margin']:>+8.1f}  {r['worst_margin']:>+8.1f}  {r['paired_positive']:>3}  {knobs_str}")


if __name__ == "__main__":
    main()