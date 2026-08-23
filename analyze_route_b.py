"""Analyze Route B smoke results and pick top-3 candidates for G1.

Reads:
  artifacts/evaluations/route_b_smoke/smoke_results.json
  (also prints a comparison vs the route_a_smoke variant_000 baseline).

Outputs top-3 selection and the G1-gate criteria status for each.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "artifacts" / "evaluations" / "route_b_smoke" / "smoke_results.json"
ROUTE_A = ROOT / "artifacts" / "evaluations" / "route_a_smoke" / "grid_smoke.json"


def main() -> None:
    if not SMOKE.exists():
        print(f"ERROR: {SMOKE} not found")
        return

    data = json.loads(SMOKE.read_text(encoding="utf-8"))
    ranked = data.get("ranked", [])

    # Baseline reference: variant_000 from Route A (the named prior winner)
    baseline = None
    if ROUTE_A.exists():
        ra = json.loads(ROUTE_A.read_text(encoding="utf-8"))
        for r in ra.get("ranked", []):
            if r.get("variant_id") == "variant_000":
                baseline = r
                break

    print(f"=== Route B smoke results: {len(ranked)} variants evaluated ===")
    print(f"Baseline: variant_000 (Route A winner)")
    if baseline:
        bk = baseline.get("knobs", {})
        print(
            f"  W/T/L={baseline['wins']}/{baseline['ties']}/{baseline['games']-baseline['wins']-baseline['ties']}  "
            f"mean={baseline['mean_margin']:+.1f}  worst={baseline['worst_margin']:+.1f}  "
            f"paired+={baseline['paired_positive']}/{baseline['games']//2}  "
            f"msb={bk.get('maximum_sell_batch')} ih={bk.get('investment_horizon')} "
            f"mr={bk.get('market_reserve')} window=[{bk.get('market_start')},{bk.get('market_stop')}]"
        )

    # Gate criteria for G1 holdout (10 seeds × 2 seats = 20 games)
    G1_GATES = {
        "wins_min": 18,            # ≥18/20 wins
        "paired_positive_min": 10, # 10/10 paired+ (=10 seeds)
        "mean_margin_min": 15.0,   # mean ≥ +15
        "worst_margin_min": -400.0 # worst ≥ -400
    }

    print(
        f"\nG1 gate thresholds: wins≥{G1_GATES['wins_min']}/20  "
        f"paired+≥{G1_GATES['paired_positive_min']}/10  "
        f"mean≥{G1_GATES['mean_margin_min']:+.1f}  worst≥{G1_GATES['worst_margin_min']:+.1f}"
    )

    # Filter to candidates that pass all smoke criteria first
    print("\n=== Candidates passing all smoke criteria (5 paired+/5, wins≥4/10, mean>0) ===")
    passing = []
    for r in ranked:
        wins = r.get("wins", 0)
        games = r.get("games", 0)
        paired_pos = r.get("paired_positive", 0)
        mean_m = r.get("mean_margin", 0.0)
        worst_m = r.get("worst_margin", 0.0)
        if paired_pos >= 5 and wins >= 4 and mean_m > 0 and worst_m > -500:
            passing.append(r)

    print(f"{len(passing)} of {len(ranked)} candidates passed smoke filters")

    # Top 3
    print(f"\n=== TOP-3 Route B candidates (ranked by paired_positive then mean_margin) ===")
    print(
        f"{'#':>3}  {'variant_id':<12}  {'route_a':<12}  {'W/D/L':>8}  {'win%':>6}  "
        f"{'mean_margin':>12}  {'worst':>10}  {'paired+':>8}  {'wilson95':>8}  "
        f"{'msb':>4}  {'mr':>5}  {'window':>12}"
    )
    print("-" * 130)
    top3 = ranked[:3]
    for i, r in enumerate(top3, 1):
        k = r.get("knobs") or {}
        wins = r.get("wins", 0)
        ties = r.get("ties", 0)
        games = r.get("games", 1)
        wld = f"{wins}/{ties}/{games-wins-ties}"
        window = f"[{k.get('market_start','?')},{k.get('market_stop','?')}]"
        route_a_id = k.get("route_a_variant_id", "?")
        print(
            f"{i:3d}  {r['variant_id']:<12}  {route_a_id:<12}  {wld:>8}  "
            f"{r['win_rate']:>5.1%}  {r['mean_margin']:>+12.1f}  {r['worst_margin']:>+10.1f}  "
            f"{r['paired_positive']}/{len(data['seeds']):>6}  {r['wilson_95']:>8.4f}  "
            f"{k.get('maximum_sell_batch','?'):>4}  {k.get('market_reserve','?'):>5}  {window:>12}"
        )

    # G1 holdout projection: smoke is 5 seeds × 2 = 10 games; holdout is 10 seeds × 2 = 20 games
    # Project expected holdout W/L on the assumption that paired seeds generalise
    print("\n=== G1 20-game holdout projection (smoke→holdout expected) ===")
    for i, r in enumerate(top3, 1):
        k = r.get("knobs") or {}
        smoke_paired_pos = r["paired_positive"]
        smoke_paired_neg = r.get("paired_negative", 0)
        smoke_paired_zero = r.get("paired_zero", 0)
        # If all 5 paired positives, holdout would likely also have ~10/10 positive
        proj_paired_pos = "10/10" if smoke_paired_pos == 5 else f"{smoke_paired_pos*2}/{10}"
        print(
            f"  {i}. {r['variant_id']} route_a={k.get('route_a_variant_id')} "
            f"msb={k.get('maximum_sell_batch')} mr={k.get('market_reserve')} "
            f"window=[{k.get('market_start')},{k.get('market_stop')}]"
        )
        print(
            f"     smoke  W={r['wins']}/10  paired+={smoke_paired_pos}/5  "
            f"mean={r['mean_margin']:+.1f}  worst={r['worst_margin']:+.1f}"
        )
        print(
            f"     expected G1 holdout (paired+ projected): {proj_paired_pos} "
            f"(mean margin expected to compound ~2× to ~{r['mean_margin']*2:+.1f})"
        )

    return top3, baseline, G1_GATES


if __name__ == "__main__":
    main()