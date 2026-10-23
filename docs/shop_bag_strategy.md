# Shop-bag mix — adopted live strategy (2026-08-28)

This is the team playbook after the Crop Dusta public-12 study. It replaces
the older “copy a public tape and hope the diet matches” default. It does
**not** replace the live Agent until a candidate passes the gates below.

Evidence: `experiments/20260828_crop_dusta_strategy.json`, destbreso week-four
x-ray cell 24, Moon V189C inner tape `experiments/20260828_moon_v189c_tape.json`.

## Chassis vs north star

| Layer | Now (legal) | North star (Crop Dusta class) |
|---|---|---|
| Live Agent | 2026-10-11 API: challenger `56679778` **1376.7 COMPLETE** + then-best reupload `56679782` **1309.6 COMPLETE**. Newest-two; metav4 `56395547` and 2945 farm `56395540` have been displaced. Current API rank **2721 / 10148**; final deadline **2026-10-14 23:59 UTC**. Hold for a paired replacement that clears the frozen gates. | Live five, not Flex/V21 |
| Inner plan | Thomas six-day trees reselect at 144/288/432/576 | Six-day reselect at 144/288/432/576 |
| Land | 3Q at steps 150, 265 | 3Q at steps 122, 200 |
| Herd | Fieldbook 9c5s / 6c11s / YARN_LATE 9c9s at **218/242/266** | Yusuke live extra sheep **227/242/266** even without first-two yarn |
| Wheat | Fieldbook **343–391** (BALANCED 380); Knight dumps 1391–1888 | **1556–2561** Crop Dusta mountain D12–15, throttle if farmers market already drains |
| Hinge | No tomato, no egg; Knight dumps ~1000 carrot/egg/tomato | Tomato / carrot / egg held to D29–30 when those shops exist |
| Fertilizer | Fieldbook 326–362, never 2932 | 119–269, never 2932 |
| Melon | Fieldbook **72** | Two pulses D11 + D17, ~90–109, board cleared |

Root `main.py` stays h2. Do not overwrite it. Do not re-upload boatlee
`55710781` (resets 2108 and steals newest). Do not submit a 12-game Crop
Dusta average or a PufferLib BC clone.

## Adopted rules

1. **Stay in the live-five class.** Frozen V21/Flex 2932-fert dumps and
   400-fert shop clones are a dying diet. The current newest-two are
   `56679778` and `56679782`, both COMPLETE at 1376.7 and 1309.6. Earlier
   metav4 `56395547` and 2945 farm `56395540` have been displaced. Require a
   validated paired-replacement plan before another upload; do not re-upload
   boatlee.
   Historical cut-16 API observations before it left newest-two (retain for audit and regression fixtures): 1799.2 COMPLETE; 1757.2 COMPLETE; 1730.1 COMPLETE; 1695.1 COMPLETE; 1682.4 COMPLETE; 1686.8 COMPLETE; 1682.0 COMPLETE; 1683.4 COMPLETE; 1691.4 COMPLETE; 1696.4 COMPLETE; 1698.7 COMPLETE; 1695.5 COMPLETE; 1697.5 COMPLETE; 1702.8 COMPLETE; 1691.5 COMPLETE; 1692.8 COMPLETE; 1688.5 COMPLETE; 1692.2 COMPLETE; 1693.4 COMPLETE; 1693.6 COMPLETE; 1690.5 COMPLETE; 1682.9 COMPLETE; 1680.9 COMPLETE; 1670.2 COMPLETE; 1673.8 COMPLETE; 1669.1 COMPLETE; 1681.2 COMPLETE; 1654.7 COMPLETE; 1644.6 COMPLETE; 1639.4 COMPLETE; 1640.5 COMPLETE; 1637.6 COMPLETE; 1643.7 COMPLETE; 1636.0 COMPLETE; 1636.5 COMPLETE; 1632.1 COMPLETE; 1627.8 COMPLETE; 1619.1 COMPLETE.
   Historical shopbag scores: 1300.3 COMPLETE; 1300.7 COMPLETE; 1293.6 COMPLETE; 1286.1 COMPLETE; 1282.2 COMPLETE.
2. **Read the whole shop bag, not `shops[0]`.** Crop Dusta’s strongest
   measured adaptation is yarn-count → wool (r 0.893). Pet cafe → carrot
   (0.694), bakery → egg (0.582), pizza → tomato (0.578). Farmers market
   4× **cuts** wheat sales to 711 (r −0.46). Older public Moon already
   branched on yarn in the first three shops; V189C regressed that to
   first-unlock only.
3. **Wheat is a glut-tolerant cash engine, not a clone dump.** Log
   above-target absorbs oversupply. Do not copy 2932 fertilizer. Do not
   buy SE to chase 4Q fert-wheat (that path broke h2).
4. **Hold hinge goods to the last two days** when the matching shops
   exist. Do not drip tomato/carrot/egg through midgame.
5. **Keep 3Q.** Crop Dusta never bought the fourth quadrant. MiMi’s 4Q
   is a different conviction, not this card.
6. **Melon is a scheduled harvest, not a leftover plant.** Two pulses,
   then the tile is empty.
7. **No 720-turn imitation.** 12 unique full hashes, one shared opening.
   A mean action stream is not Crop Dusta.

## What we will not do

- Upload Crop Dusta BC / PufferLib import / averaged publics.
- Copy Flex/V21 fertilizer volume or SE pathing.
- Displace V189C with an untested wheat-flood fork.
- Retune h2 V36 knobs.
- Exhaust daily quota speculatively.

## Experiment queue

One frozen cut at a time. Cuts 1–9 wrap V189C/Kenjo. Cut 10 is a
chassis switch to Yusuke's published six-route Fieldbook.

| Cut | Change | Why | Status |
|---|---|---|---|
| **1** `moon_shopbag_v1` | Yarn cohort if `YARN_STORE in shops`, not only `shops[0]` | Highest-leverage bag read our chassis can spend; remaining cow buys after step 72 are exactly five | **Live `55840543` / 2628.9, rank 42.** Public 153 **82-4-67**. Rolling 12 **3-9 all clones** |
| 2 | Farmers-market wheat throttle | Crop Dusta throttles when town already drains wheat | **Closed.** Tape already empties the shed (0–3 wheat left). Throttle cannot create a mountain |
| 3 | Terminal hinge hold | D29–30 tomato/carrot/egg | **Blocked.** Tape plants no tomato/egg |
| **4** hunt | Later public live-five / Moon with wheat mountain | Collin-class 1742 wheat and 10–11 sheep herds beat 696/8 | Next real score jump. prvsiyan Soil reran 8/28; Moon notebook still V189C |
| 5 `moon_shopbag_v2` | Add `WHEAT` to the 1-turn front-run set | TK256 self-clone −125 with identical 696/561/239 sells | Coded, **not uploaded**. Must beat frozen TK256 `102114403` and keep clone/G5 |
| 6 Yusuke two-shop demo | 10 public Milan/Kenjo/Shuwen histories routed on first two shops | #3's published method (full CR2 is 68-18, not in the notebook) | Extracted SHA `ac615297...`. Panel 0-4-1: MtN −9019, Yusuke tie, Hanserong −4677, clone **−8108**. **Reject upload** |
| 7 `moon_shopbag_v3` | One extra yarn-or-cow animal into serviced empty `(7,4)` via hand 4 PASS 255–260 | Rolling-12 is extra-animal clones; `(7,4)` is fed all season | SHA `8f83bbc3...`. Clone 3-0 identical. Fired once (Yusuke +3138). Other 11-sheep / clone losses delta 0 because 223 PLACE already filled the tile. **Hold** |
| **8** `moon_shopbag_v4` | Shopbag default; Kenjo `102125420` from step 72 iff `shops[0]==YARN_STORE` | First-yarn 11-sheep specialist, same 0–71 opening | **Live `55887331` / 1968.0.** SHA `5dc4dccf...`. Clone 3-0. Hanserong **+3879**. MtN −759. Rolling-12 deaths are non-yarn extra-animal clones |
| **9** `moon_shopbag_v5` | First shop yarn → Kenjo 11-sheep; else Kenjo extra-cow `102078489` + yarn wrap | Rolling-12 all `kenjo=0 clone=1` extra cow/pasture | SHA `e254dd7d...`. Clone 3-0 **stronger**. Live-loss **3/5 flips**. Yarn-2nd TK256 +7934. G5 both win. MtN still −759. **Superseded by cut 10** |
| **10** `yusuke_fieldbook` | Six-route ShopForge: shared 0–143, branch day 6 and 9 on shops + cash/land gap | Rolling-12 is Fieldbook BALANCED 9c5s / YARN_ENGINE 6c11s clones; v5 still loses MtN | **Live `55962758` / 1883.4.** SHA `de668f7f...`. Public 372 **133-60-179**. Rolling-12 **4-3-5** freeze-after-day-9 vs later 9c9s / wheat tails |
| **11** Yusuke six-day | Reselect every 144 turns; 8 tapes / 30 paths; price + cash_gap + weed trees | Yusuke live `55975994` 9c9s is **not** a BALANCED-tail patch (prefix diverges at step 1) and **not** a later-block reselect (shop-independent tape through 266). Six-day stays the public reselect chassis | **Live `56028043` / 1590.8 COMPLETE** (was 1888.3). Public 346 **138-0-208**. Rolling 12 **4-0-8**: opening-broke no-land + clone wool-crash. Dropped from newest-2 after shopbag reupload `56112309`. Do not reupload boatlee |
| **12** s3 milk-heavy on wool crash | Day-18 route 1 (134 milk vs 48) when wool≤12 and milk>200 | Deskbo 105744091: ahead +5641 at 432, behind −7709 at 576, milk 243 vs 335, wool=$1. Stanislav 11c4s **+15963** with wool 198 | Recorded-seat vs Deskbo still **L −15706**. Later blocks buy no extra cows after 288. **Hold.** Not reused this cycle. Not a 227 wrap |
| **13** s4 milk-heavy when behind | Last-block route 3 if cash_gap<0 and milk>150 (140 milk vs 96; also SELL:COW 5) | Stefano clone 9c5s −21909; Deskbo −15628; fufu clone 8c9s −11025. Live s4 tree picks 0 | Recorded-seat **Deskbo L −18470**, **Stefano L −22834**, fufu L −8724. **Hold.** Not cut 12. Not a 227 wrap. Not reused this cycle |
| **14** `y3uanm_router_v5` | Later-block reselect at 226 (yarn) / 360 (carrot) / 433 (milk); prefix-guarded tape tails | Six-day rolling 12 **4-0-8** is opening-broke + clone wool-crash. Yusuke shop-router-0908 is ctypes `agent.so`. This kernel is Windows-runnable Python after 216 | **Live `56111821` / 1795.1 COMPLETE.** SHA `acf7c664...`. Clone 3-0 prvsiyan **+22889** fufu **+27316** masa **+17295**. G5 Subin **+27188** James **+69612**. Extra sheep 217/265, not 227/242/266. Newest-2: this + shopbag reupload `56112309` (lineage `55962761`) until cut 15. Dropped from newest-2 after cut 15 `56146106`. Do not reupload boatlee |
| **15** `thomastschinkel_psr_938` | Public-state tree reselect at 144/288/432/576 (after 216: 288/432/576) | Cut 14 rolling 12 **3-2-7** is extra-animal clones + wool-crash, not opening-broke. Header-only hunt called this kernel day-6; extract reselects after 216. Distinct from live six-day, Fieldbook BALANCED, and cut 14 | **Live `56146106` / 1864.4 COMPLETE.** SHA `b87a27ed...`. Clone 3-0 prvsiyan **+5757** fufu **+28052** masa **+16873**. G5 Subin **+31605** James **+68313**. Extra sheep **265**, not 227/242/266. Dropped from newest-2 after cut 16 `56151152`. Do not reupload boatlee |
| **16** `yamakawanin_king_v4e_rc4` | Shop-family PROGRAM reselect at 72-turn phases after 216 (P3+/288/360/432/576) plus YARN_SECOND from 240 | Cut 15 rolling 12 **4-1-7** is extra-animal clones + wool-crash, not opening-broke. Distinct from live six-day, Fieldbook BALANCED, cut 14, and cut 15. Extra sheep 226/241/265 | **Live `56151152` / 1569.5 COMPLETE** (was 1573.9 COMPLETE / 1578.6 COMPLETE / 1582.4 COMPLETE / 1588.3 COMPLETE / 1606.1 COMPLETE / 1625.8 COMPLETE / 1627.7 COMPLETE / 1623.1 COMPLETE / 1619.1 COMPLETE / 1627.8 COMPLETE / 1632.1 COMPLETE / 1636.5 COMPLETE / 1636.0 COMPLETE / 1643.7 COMPLETE / 1637.6 COMPLETE / 1640.5 COMPLETE / 1639.4 COMPLETE / 1644.6 COMPLETE / 1654.7 COMPLETE / 1681.2 COMPLETE / 1669.1 COMPLETE / 1673.8 COMPLETE / 1670.2 COMPLETE / 1680.9 COMPLETE / 1687.3 COMPLETE / 1682.9 COMPLETE / 1690.5 COMPLETE / 1693.6 COMPLETE / 1693.4 COMPLETE / 1692.2 COMPLETE / 1688.5 COMPLETE / 1692.8 COMPLETE / 1696.4 COMPLETE / 1691.5 COMPLETE / 1702.8 COMPLETE / 1697.5 COMPLETE / 1695.5 COMPLETE / 1698.7 COMPLETE / 1696.4 COMPLETE / 1691.4 COMPLETE / 1683.4 COMPLETE / 1682.0 COMPLETE / 1686.8 COMPLETE / 1682.4 COMPLETE / 1695.1 COMPLETE / 1730.1 COMPLETE / 1757.2 COMPLETE / 1799.2 COMPLETE). SHA `26ffba52...`. Clone 3-0 prvsiyan **+12627** fufu **+12014** masa **+40050**. G5 Subin **+27159** James **+77153**. Extra sheep **226/241/265**, not 227/242/266. Newest-2: this + shopbag reupload `56151155` **1282.2**. Cut 15 `56146106` dropped. 2026-09-15e **Hold** (upload-bail). Do not reupload boatlee |

Cut 1 is the only change that is a true single-variable wrap: when yarn
unlocks first, behaviour equals V189C; when it unlocks second (day 6,
step 144) the four remaining cow buys become sheep.

## Gates (cut 1 and later)

Same screens that promoted V189C. All must stay wins. Recorded-seat,
720 turns, official `kaggle-environments==1.32.7`.

- Clone 3-0: prvsiyan `100348898`, fufufukakaka `100504057`, masayoshi `100444645`
- G5 both-win: Subin An `97399969`, James Y `95677563`
- Low-fert 3-0: OceanMix `98031955`, Kaileh57 `98118767`, alessandrozonta `98383311`

Then closed-loop vs V189C, seeds `20260911–20260920` both seats. Promote
only if clone/G5/lowfert still pass **and** the V189C holdout is not a
collapse (do not require 18/20; require no new failure class). Upload
only with explicit user authorization. Newest-2: a passing cut 1 would
replace shops `55744278`, not V189C.

## Hunt rule

Prefer a later public Moon / live-five / ShopForge kernel over inventing
a wheat mountain inside the Ramesh tape. Official daily zips
`kaggle/kaggriculture-episodes-DATE` remain the replay source. GitHub
PufferLib `8aa699e` is a BC pipeline over those zips, not an Agent.
Yusuke Fieldbook (cut 10) was live `55962758`. Cut 11 six-day `56028043`
is **1590.8 COMPLETE** (dropped from newest-2). Cut 14 `y3uanm_router_v5`
`56111821` is **1799.3 COMPLETE** (dropped). Cut 15
`thomastschinkel_psr_938` `56146106` is **1864.4 COMPLETE** (dropped).
Cut 16 `yamakawanin_king_v4e_rc4` `56151152` is **1569.5 COMPLETE**
(was 1573.9 COMPLETE / 1578.6 COMPLETE / 1582.4 COMPLETE / 1588.3 COMPLETE / 1606.1 COMPLETE / 1625.8 COMPLETE / 1627.7 COMPLETE / 1623.1 COMPLETE / 1619.1 COMPLETE / 1627.8 COMPLETE / 1632.1 COMPLETE / 1636.5 COMPLETE / 1636.0 COMPLETE / 1643.7 COMPLETE / 1637.6 COMPLETE / 1640.5 COMPLETE / 1639.4 COMPLETE / 1644.6 COMPLETE / 1654.7 COMPLETE / 1681.2 COMPLETE / 1669.1 COMPLETE / 1673.8 COMPLETE / 1670.2 COMPLETE / 1680.9 COMPLETE / 1687.3 COMPLETE / 1682.9 COMPLETE / 1690.5 COMPLETE / 1693.6 COMPLETE / 1693.4 COMPLETE / 1692.2 COMPLETE / 1688.5 COMPLETE / 1692.8 COMPLETE / 1696.4 COMPLETE / 1691.5 COMPLETE / 1702.8 COMPLETE / 1697.5 COMPLETE / 1695.5 COMPLETE / 1698.7 COMPLETE / 1696.4 COMPLETE / 1691.4 COMPLETE / 1683.4 COMPLETE / 1682.0 COMPLETE / 1686.8 COMPLETE / 1682.4 COMPLETE / 1695.1 COMPLETE / 1730.1 COMPLETE). Newest-2: cut 16 `56151152` + shopbag reupload
`56151155` **1282.2** (lineage `55962761`). Cut 16 rolling 12 **5-0-7**
ids `109329693…109111080` (not the 09-15d set `109323301…109205359`):
extra-animal 8c6s3g (Huy −13645 extra cow 218 vs opp extra sheep 218/227 extra geese 242/266; Filip −6855 extra cow 218 vs opp extra sheep 218/227 extra geese 242/266)
plus extra-goose vs extra-cow (Gaddam −26009 extra geese 227/242 already bought vs 11c)
plus identical-clone extra-goose (3G −10063 extra geese 227/242 already bought)
plus extra-sheep (Dhruv −12590 extra sheep 218/242/266 already bought vs 6c10s; Grim −10132 extra sheep 218/242/266 already bought vs 3c13s2g)
plus extra-goose (Corgi-Samoyed −325 extra geese 227/242 already bought vs 6g).
Gaddam `109297997` already bought extra geese 227/242 and lost vs 11c — not a 227 wrap
license.
Not opening-broke no-land. Not freeze-after-day-9 9c9s.
Cut 12 s3 and cut 13 s4 milk-heavy stay **Hold** (not reused). Current
#1 Majkel1337 is mid-land 150 then 220-222 (one game 126/150/220), clone 1/4 — opening land is
not a later-block license. 2026-09-15e hunt (0 new slugs vs `_hunt_20260915d`;
public search newest still `ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race` already rejected SHA 797d9bca)
is not later-block.
**Hold**: shopbag partner <1500 and newer than cut 16, so a new cut
alone would drop the ≥1500 COMPLETE without a ≥1500 newest-2 partner.
Do **not** name a 227/242/266 sheep wrap of cut 10. Do not claim Windows ran `agent.so`.
