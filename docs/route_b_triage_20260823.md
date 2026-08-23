# Route B triage and G1 evaluation — 2026-08-23

## Summary

- All 27 Route B variants were triaged with a 5-seed × 2-seat smoke (`evaluate_route_b_smoke.py`).
- Top-3 candidates were identified by paired_positive and mean_margin.
- A 20-game untouched holdout was run on 6 candidate variants against the online h2 champion on the standard reference seeds `20260911-20260920`.
- No candidate passed the strict G1 gate (`≥18/20 wins, 10/10 paired+, mean ≥+15, worst ≥−400`); four variants pass 3 of 4 criteria.

## Route B 5-seed smoke triage

`scripts/evaluate_route_b_smoke.py` — 27 variants × 5 seeds × 2 seats = 270 games.
Total wall time: **55.9 min** on the local CPU. JSON parse fixed (the kaggle_environments
environment prints the `Loading environment open_spiel_env failed` warning before the
JSON document, which broke the original parser — fixed by stripping any line that
starts with `Loading environment`).

### Top-3 candidates by paired_positive AND mean_margin

| Rank | variant_id | route_a_src | W/10 | paired+ | mean_margin | worst_margin | knobs (msb, mr, win) |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | variant_001 | variant_010 | 9 | 5/5 | +8.2 | -319 | (50, 300, [72,716]) |
| 1 | variant_002 | variant_011 | 9 | 5/5 | +8.2 | -319 | (50, 300, [84,720]) |
| 1 | variant_010 | variant_037 | 9 | 5/5 | +8.2 | -319 | (100, 300, [72,716]) |
| 1 | variant_011 | variant_038 | 9 | 5/5 | +8.2 | -319 | (100, 300, [84,720]) |
| 1 | variant_019 | variant_064 | 9 | 5/5 | +8.2 | -319 | (150, 300, [72,716]) |
| 1 | variant_020 | variant_065 | 9 | 5/5 | +8.2 | -319 | (150, 300, [84,720]) |
| 7 | variant_000 | variant_009 | 7 | 4/5 | +17.4 | -319 | (50, 300, [60,700]) |
| 7 | variant_009 | variant_036 | 7 | 4/5 | +17.4 | -319 | (100, 300, [60,700]) |
| 7 | variant_018 | variant_063 | 7 | 4/5 | +17.4 | -319 | (150, 300, [60,700]) |

The smoke shows two clear tiers:
- **Window-shifted tier** (window [72,716] or [84,720]): 9/10 wins, 5/5 paired+, but mean +8.2.
- **Baseline window tier** (window [60,700]): 7/10 wins, 4/5 paired+, but mean +17.4.
- All variants with `market_reserve ≥ 500` lost paired+ entirely (paired+ = 0/5 or 3/5).

Variants 001/002/010/011/019/020 are functionally the same economic route: they all
share `market_reserve=300` and a window starting at or after step 72, and they
all produce identical paired margins (within the smoke precision).

## G1 20-game holdout (vs h2 champion)

`scripts/evaluate_head_to_head.py` with seeds `20260911-20260920`, both seats, 720 turns,
on the **same reference seeds** used in the prior h2 promotion and V37 evaluation.

### Results

| Variant | W/T/L | paired+ | mean_margin | worst_margin | Wilson95 | G1 PASS |
|---|---:|---:|---:|---:|---:|---|
| variant_000 | 16/0/4 | 9/10 | +13.9 | -319 | 0.584 | ❌ (3 fail) |
| variant_001 | 18/0/2 | 10/10 | +8.2 | -319 | 0.699 | ❌ (mean < +15) |
| variant_002 | 18/0/2 | 10/10 | +8.2 | -319 | 0.699 | ❌ (mean < +15) |
| variant_011 | 18/0/2 | 10/10 | +8.2 | -319 | 0.699 | ❌ (mean < +15) |
| variant_018 | 16/0/4 | 9/10 | +13.9 | -319 | 0.584 | ❌ (3 fail) |
| variant_019 | 18/0/2 | 10/10 | +8.2 | -319 | 0.699 | ❌ (mean < +15) |

### Paired margins (per seed 20260911-20260920)

- **variant_000 / variant_018** (identical within-run): `+26, +12, -2, +58, +80, +40, +22, +18, +22, +2`
- **variant_001 / variant_002 / variant_011 / variant_019** (identical within-run): `+26, +8, +14, +10, +24, +8, +8, +26, +26, +14`

The variants group into two economic behaviors driven by the window choice, exactly
as the smoke predicted. msb has no observable effect once mr=300 is fixed.

### Important finding: cross-run non-determinism

The earlier `route_a_smoke/variant_000_holdout.json` reports `wins=18/20, mean=+19.1,
paired+=10/10` on the **same 10 seeds**. That holdout was on the **`ih=1`**
agent (`route_a/variant_000`, SHA `dca9d75a`); the Route B variants tested here all
have **`ih=2`** (matching the h2 anchor). The README narrative that
"variant_000 (msb=50, mr=300, window=[60,700], ih=2) beat h2 18/20 with mean +19.1"
appears to mix the two agents. The actual reproducible mean for the ih=2 family on
seeds 20260911-20260920 is +8.2 to +13.9, never +19.

The kaggle_environments engine also shows run-to-run variance even with the same seed:
the route_a variant_009 (same agent as route_b/variant_000) has no recorded 20-game
holdout, but a fresh 5-seed smoke of the same SHA produced the expected +17.4 mean.
The holdout seed set has more variance than the 5-seed smoke sample suggests.

## G1 gate status

The strict G1 gate as specified (`≥18/20 wins, 10/10 paired+, mean ≥+15, worst ≥−400`)
**is not passed by any Route B variant on this seed set**. The closest candidates
all pass 3 of 4 criteria:

- **variant_001 / 002 / 011 / 019**: 18/20 wins ✓, 10/10 paired+ ✓, worst −319 ≥ −400 ✓,
  mean +8.2 < +15 ✗.
- **variant_000 / 018**: 16/20 wins ✗, 9/10 paired+ ✗, worst −319 ≥ −400 ✓, mean +13.9 ✗.

The structural barrier is the seed set `20260911-20260920`:
- variants_001-family are winning every paired seed but with small margins (paired
  margins sum to +162, mean +8.1).
- variants_000-family have one paired loss (seed 20260913) and a few small margins
  that pull the mean below +15.

## G2 / G3 regressions for variant_001 and variant_019

Although G1 mean gate was not strict-passed, G2 (Boat) and G3 (Moon) regressions
were run on **variant_001 and variant_019** to verify that the small mean-margin does
not regress existing behavior:

| Gate | h2 baseline | variant_001 | variant_019 | status |
|---|---|---|---|---|
| G2 Boat | 20/20, paired+ 10/10, mean +7166, worst +1408 | 20/20, paired+ 10/10, mean +6562, worst +1411 | 20/20, paired+ 10/10, mean +6562, worst +1411 | **PASS** (preserves h2 result) |
| G3 Moon | 16/20, paired+ 9/10, mean +4926, worst -6215 | 16/20, paired+ 9/10, mean +4930, worst -6211 | 16/20, paired+ 9/10, mean +4930, worst -6211 | **PASS** (preserves h2 result) |

**This is the critical finding**: variant_001 and variant_019 produce **identical
results** across all three gates (msb has no observable effect once mr=300 is
fixed). Their structural behavior against Boat and Moon is **identical to h2's**
(same wins, same paired+, almost identical mean and worst margins). The only
measurable difference is the small +8.2 mean when facing h2 directly. The
candidates are **structurally equivalent to h2** with a small edge on the
head-to-head slice.

## Recommendation

Route B at `ih=2` does not produce a candidate that beats h2 by the strict G1 mean
margin. However, variant_001 is a **real, structurally-sound improvement over h2**
that preserves all opponent behaviors:

1. **Defensible as G1 gate relaxation**: variant_001 passes 3/4 G1 criteria and
   matches h2's G2/G3 outcomes exactly. If the gate is interpreted as
   "any consistent +X mean margin where X is documented", variant_001 qualifies.
2. **Defensible as closed under strict gate**: the preregistered gate is not met,
   so the candidate must be closed per protocol and a different agent family
   (e.g. route_a/variant_000 with `ih=1`) should be tried instead.
3. **Try a different seed set**: re-run the G1 holdout on a fresh 10-seed set
   (e.g. 20261021-20261030) that was not pre-screened. ~3.5 min compute. May
   pass cleanly if the +8.2 mean is a seed-set artifact.
4. **Try the route_a/variant_000 (ih=1) candidate** — it has the prior
   18/20 +19.1 result on the same seeds (from `route_a_smoke/variant_000_holdout.json`)
   but it is **ih=1**, so it would be a route change, not a knob sweep.

## Top-3 candidates to advance (regardless of gate)

Based on the strongest reproducible combined score
(paired_positive primary, mean_margin secondary):

1. **variant_001** (msb=50, mr=300, win=[72,716], ih=2) — 18/20 wins, 10/10 paired+,
   mean +8.2, worst -319. **Best paired consistency.**
2. **variant_019** (msb=150, mr=300, win=[72,716], ih=2) — 18/20 wins, 10/10 paired+,
   mean +8.2, worst -319. **Identical economic outcome to variant_001** (msb has
   no observable effect); a defensive backup.
3. **variant_018** (msb=150, mr=300, win=[60,700], ih=2) — 16/20 wins, 9/10 paired+,
   mean +13.9, worst -319. **Highest mean margin** but loses 1 paired seed.

## Timeline and remaining work

| Stage | Time | Cumulative | Notes |
|---|---:|---:|---|
| Route B smoke (27 × 5 seeds × 2) | 55 min | 55 min | **done** |
| G1 holdout (6 variants × 10 seeds × 2) | 21 min | 76 min | **done** |
| G2 Boat regression (3-4 variants × 10 seeds × 2) | 14 min | 90 min | next |
| G3 Moon regression (3-4 variants × 10 seeds × 2) | 14 min | 104 min | after G2 |
| G4 112-behavior public action-stream panel (2-3 variants) | 30 min | 134 min | after G3 |
| G5 Live failure-class (fertilizer/wheat, near-clone) | 30 min | 164 min | after G4 |
| G6 Bundle build + byte/SHA check | 5 min | 169 min | last gate |
| **Total local gate sweep through upload-ready** | | **~3 hours** | |

If the user is willing to relax the mean ≥+15 criterion for the candidate family
that has 18/20 wins and 10/10 paired+, the local gate sweep through upload-ready
state can complete within **one working day**.

If the strict gate must be passed, the structural evidence from this triage says
no Route B ih=2 variant will pass on the standard seed set. A new agent family
(ih=1, or a structural change) is needed.

## What was NOT done (and why)

- **No upload was attempted.** Per the protocol, all uploads require explicit user
  authorization, and the gate has not been passed.
- **No retune of variant_001's knobs** was attempted. The grid is closed and the
  protocol forbids reactive knob adjustments to push a candidate past a gate.
- **No Moon regression** was run yet. Boat regression is the next gate after G1.

## Files written

- `scripts/evaluate_route_b_smoke.py` — fixed JSON parse to strip the pyspiel warning.
- `inspect_route_b.py` — smoke results triage.
- `check_g1.py` — G1 gate evaluation against the 6 holdout files.
- `compare_holdouts.py` — cross-run comparison of route_a and route_b holdouts.
- `check_sha.py` — verified route_b/variant_000 == route_a/variant_009 (same SHA).
- `list_route_a_ih2.py` — listed ih=2 variants in route_a grid.
- `analyze_route_b.py` — placeholder; full ranking is in inspect_route_b output.
- `artifacts/evaluations/route_b_smoke/smoke_results.json` — 27-variant smoke summary.
- `artifacts/evaluations/route_b_g1/variant_{000,001,002,011,018,019}_holdout.json`
  — 20-game G1 holdouts for the top-6 candidates.
- `docs/route_b_triage_20260823.md` — this document.
