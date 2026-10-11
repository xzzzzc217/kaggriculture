# moon_shopbag_v1

Cut 1 of `docs/shop_bag_strategy.md`. Wrapper around Moon V189C
(`4158d6c8...`). Inner Ramesh payload is unchanged.

One behaviour change: the sheep cohort runs when **any** unlocked shop is
`YARN_STORE`, not only when `shops[0] == "YARN_STORE"`.

- First-unlock yarn (day 3, step 72): identical to V189C (`_MAX_SWITCHES=5`).
- Yarn as 2nd shop (day 6, step 144): remaining cow buys at 150/171/217
  become sheep. V189C currently misses this bag.
- Yarn as 3rd shop (day 9, step 216): only the step-217 cow is left.

Gates (2026-08-28), recorded-seat 720, engine 1.32.7:

| stream | shopbag | V189C | yarn |
|---|---:|---:|---|
| prvsiyan 100348898 | **+5964** | +5964 | same |
| fufufukakaka 100504057 | **+6937** | +6937 | same |
| masayoshi 100444645 | **+7511** | +7511 | same |
| Subin An 97399969 | **+17659** | +3514 | 2nd shop, step 144 |
| James Y 95677563 | **+51097** | +51097 | 1st shop |
| OceanMix 98031955 | **+9651** | +9651 | step 504 (too late) |
| Kaileh57 98118767 | **+3567** | +3567 | step 288 (too late) |
| alessandrozonta 98383311 | **+15650** | +15650 | step 288 (too late) |

H2H vs V189C, seeds 20260911-20260920 both seats: **1-18-1**, mean **0**, paired **10/10 zero**, worst **−302** (seed 20260912 seats cancel).

Bundle: `artifacts/submission/moon_shopbag_v1/submission.tar.gz`
SHA-256 `2eaeae5eb1e1bcf3449e613b1ce3698604f255cdcce621ba7ab1601ebc573bb0`
(14910 bytes). Uploaded `55840543` at 2026-08-28 09:22:09 UTC (PENDING).
Newest-2 after COMPLETE: shopbag + V189C `55832272`. Do not overwrite
root `main.py`.
