# Yusuke Fieldbook (static extract)

Source: `yhay81/fieldbook-commit-for-three-days` + dataset
`yhay81/shopforge-fieldbook-tapes`. Notebook says this is a readable
six-route ShopForge study, not the submitted LossGuard (0.95549 vs
0.95883 on 27,520 frozen games). Apache-2.0 handwritten code. Public
tapes from Milan Leonard, Kenjo1209, and Shuwen (Shawn) Ge.

Assembled SHA-256 `de668f7f72a552640fe0e615fff937990596a47cbe95ba6f6f3992d3fcba3ae8`
(331,060 bytes).

| first two shops / gaps | route | herd | wheat / wool |
|---|---|---|---|
| yarn 1st, or yarn 2nd without land gap | YARN_ENGINE | 6c11s | 358 / 285 |
| yarn 2nd and land gap < 0 | LAND_RECOVERY | 6c11s | 340 / 283 |
| else, cash gap < 0 at day 9 | CASH_RECOVERY | 9c5s | 381 / 138 |
| else, 3rd shop yarn | YARN_LATE | 9c9s | 343 / 285 |
| else | BALANCED | 9c5s | 380 / 138 |

Shared opening 0–143. Land always 150/265, 17 pastures, melon 72, no
tomato/egg. 1-step SELL lead skips wheat and fertilizer. Terminal
liquidation on the last two turns.

Recorded-seat vs v4/shopbag streams (1.32.7, 720):

| stream | shopbag/v4 | Fieldbook | delta |
|---|---:|---:|---:|
| prvsiyan / fufu / masa clone | +5964 / +6937 / +7511 | **+4093 / +7516 / +11567** | still 3-0 |
| 3정훈 live L | −5290 | **+4611 win** | +9901 |
| satoooh live L | −3181 | −411 | +2770 still L |
| Plant City / Fernando / Liquidus | −4198 / −2605 / −3662 | **+7650 / +5223 / +8379** | flips |
| TK256 first-yarn / yarn-2nd | +16611 / +17159 | **+33234 / +34695** | +16k / +17k |
| Hanserong 11-sheep | +3879 | **+11446** | +7567 |
| MtN 11-sheep | −759 | **+2044 win** | +2803 |
| Yusuke 11-sheep | −13434 | **+18016 win** | +31450 |

G5: Subin **+31494**, James **+25530**, both win.

Rolling-12 sample 4/6 flips. The two remaining losses (Mostafa −443,
l1aF −574) are Fieldbook-vs-Fieldbook coin-flips.

Live `55962758` / **2071.0** COMPLETE (uploaded 2026-09-02 13:59:09 UTC).
Shopbag reupload `55962761` is 1688.5. Rolling-12 is freeze-after-day-9
ShopForge clones. Next chassis is Yusuke six-day (cut 11, not uploaded).
Root `main.py` still h2.
