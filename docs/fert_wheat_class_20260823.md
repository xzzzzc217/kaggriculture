# Fertilizer / wheat / 4Q-8-sheep class (2026-08-23)

Frozen G5 controls: Subin An `97399969` and James Y `95677563`. h2 replay-callback
already matches live banks (65997-73104 / 85208-93759). V36 knobs stay closed.

## Structural gap

- h2 tape buys land only at steps 160 and 240 (Q2 then Q3). It never buys SE.
  Final public board is always 3Q / 10 hands / 8 cows / 4 sheep / 1 pasture.
- Both opponents buy land at 149, 265, 289 and finish 4Q / 8 hands / 5-6 cows /
  8 sheep / 4 pastures. Sheep are added from day 8 through day 14 (12 bought).
- Fertilizer volume is an animal-scale effect, not a sell-knob: h2 sells a
  tape-scripted 216; opponents sell 1760 (Subin) and 2701 (James). Collect
  counts are close (h2 ~295 vs ~330); the extra units are stockpiled from more
  animal tiles, then dumped (D11 ~140, then 150-280/day after D16).
- Town does not consume fertilizer. Price starts at I0=10000 / base 100 and
  falls linearly as inventory rises. The D11 dump is the cash spike (plus
  ~60 melon vs h2's 30). Late fert sales are near the floor.
- Late wheat is a second gap: opponents BUY_PRODUCT 50-140/day and sell
  100-190 after D20; h2's wheat MM stays at `market_quantity=10`.
- By day 12 h2's 3Q is full (~3 empty tiles, 35 strawberry). Extra pastures
  do not fit without SE. Hands follow the 3Q tape and almost never stand on SE
  after unlock, so a market-only BUY_LAND does not create a worked quadrant.
- Clone gate is off on both streams (max near streak 6). This is not a
  near-clone timing loss.

## What a correct next change needs

One expert, class-latched, that (1) buys SE after the D11 cash print when
`money >= 4000 + route reserve`, (2) paths a small worker set from shed-access
onto empty SE tiles, (3) DIG/BUILD_PASTURE/PLACE up to 4 sheep, (4) collects
and sells fertilizer on those tiles. Do not retune clone_horizon / msb / mr /
market window. Do not plant a second wheat MM by editing `_V36_CONFIG`.

PASS-only edits on whatever tile a 3Q worker already occupies cannot staff SE.

## fert_wheat_v1 result

Implemented that market half plus PASS-only SE/shed edits. Recorded-seat
callback lost both controls by a wider margin than h2. Likely causes: 4000
land + 500/sheep spent without a SE worker plan; extra SELL/BUY volume moved
the shared market so the frozen opponent stream printed more than live; 3Q
PASS replacements at shed-access stole CARE/feed idle slots.

Stop. No knob-spam. No upload.

## fert_wheat_v2 result

One auditable pathing candidate: `experiments/candidates/fert_wheat_v2/main.py`.
It is not a PASS-only fallback. After the same class latch and 4000 SE unlock it
redirects up to two non-farmer workers from shed-access onto SE, builds the
compact 2x2 `(5,5)/(6,5)/(5,6)/(6,6)`, and places extra sheep.

Recorded-seat callback (no opposite seat):

| Stream | h2 | v1 | v2 |
| --- | --- | --- | --- |
| Subin An 97399969 | 65997-73104 (-7107) | 64794-77568 (-12774) | 53801-115039 (-61238) |
| James Y 95677563 | 85208-93759 (-8551) | 93448-105319 (-11871) | 71118-140511 (-69393) |

Q4 occupancy: unlock at step 266 / 262. First pasture 267. First sheep 269.
`max_se_sheep` was 3-4. Final SE boards were 4 empty pastures, 0 animals.
Sheep escaped (`consecutive_unfed >= 2`). No fertilizer/wool scale appeared.

Failed the slice pass bar (must beat both streams, or at least beat h2's
margins on both). Worse than both h2 and v1.

## Why SE pathing wrecks the V36 tape

Hands are wiped at end of day and re-hired onto the four shed-access tiles.
The open-loop tape's first hours are walks from that spawn to 3Q WATER/CARE/FEED.
Any real SE path has to steal those morning NORTH/SOUTH/EAST/WEST actions.
Doing so:

1. places the 2x2 and sheep (so this is not the v1 empty-Q4 *construction* failure);
2. starves the new sheep because feed/wheat pickup stay on the 3Q tape;
3. desynchronizes the 3Q animal/crop loops, so our bank falls and the frozen
   opponent stream prints far more (115k-140k vs live 73k-94k).

A tighter second cut (override MOVE/PASS only; no extra SELL) still escaped
the sheep and still lost ~54k-61k extra vs h2.

Extra HIRE for a dedicated SE hand would change the observed hand count and
desync the 719-step tape. PASS-only cannot staff SE (v1). There is no remaining
satellite that paths onto SE without wrecking the tape.

Stop. No further v2 knobs. No upload. Root `main.py` remains h2
`65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.

