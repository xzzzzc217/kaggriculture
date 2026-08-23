import json

# Extract h2 anchor results
with open('artifacts/evaluations/route_a_smoke/grid_smoke.json') as f:
    data = json.load(f)

h2 = None
for r in data['ranked']:
    if r.get('variant_id') == 'variant_040':
        h2 = r
        break

print("=== h2 anchor (variant_040) ===")
print(f"  wins={h2['wins']}/{h2['games']}")
print(f"  win_rate={h2['win_rate']:.3f}")
print(f"  mean_margin={h2['mean_margin']:+.1f}")
print(f"  worst_margin={h2['worst_margin']:+.1f}")
print(f"  paired_positive={h2['paired_positive']}")
print(f"  paired_negative={h2['paired_negative']}")
print(f"  wilson_95_lower={h2['wilson_95_lower']:.4f}")
print(f"  knobs={h2.get('knobs')}")
print()

# Find all variants with investment_horizon=2 (these are the h2 axis)
ih2_variants = [r for r in data['ranked'] if r.get('knobs', {}).get('investment_horizon') == 2]
print(f"=== Variants with investment_horizon=2 ({len(ih2_variants)} total) ===")
for r in sorted(ih2_variants, key=lambda x: (-x['paired_positive'], -x['mean_margin'])):
    k = r.get('knobs', {})
    print(f"  {r['variant_id']}: msb={k.get('maximum_sell_batch')} mr={k.get('market_reserve')} window=[{k.get('market_start')},{k.get('market_stop')}] wins={r['wins']}/{r['games']} mean_margin={r['mean_margin']:+.1f} paired+={r['paired_positive']}")
print()

# Find variants NOT with ih=2 that beat the h2 anchor
others = [r for r in data['ranked'] if r.get('knobs', {}).get('investment_horizon') != 2]
h2_margin = h2['mean_margin']
h2_paired = h2['paired_positive']
print(f"=== Variants with ih!=2 that beat h2 (mean_margin > {h2_margin:+.1f} AND paired_positive >= {h2_paired}) ===")
for r in sorted(others, key=lambda x: (-x['paired_positive'], -x['mean_margin'])):
    if r['mean_margin'] > h2_margin and r['paired_positive'] >= h2_paired:
        k = r.get('knobs', {})
        print(f"  {r['variant_id']}: ih={k.get('investment_horizon')} msb={k.get('maximum_sell_batch')} mr={k.get('market_reserve')} window=[{k.get('market_start')},{k.get('market_stop')}] wins={r['wins']}/{r['games']} mean_margin={r['mean_margin']:+.1f} paired+={r['paired_positive']} worst={r['worst_margin']:+.1f}")
print()

# Now understand the 27-variant grid for Route B
# ih=2 fixed, sweep msb, mr, market_window (3x3x3 = 27)
print("=== Route B 27-variant grid (ih=2 fixed, sweeping msb x mr x window) ===")
for msb in [50, 100, 150]:
    for mr in [300.0, 500.0, 700.0]:
        for (mstart, mstop) in [(60, 700), (72, 716), (84, 720)]:
            print(f"  msb={msb} mr={mr} window=[{mstart},{mstop}]")
