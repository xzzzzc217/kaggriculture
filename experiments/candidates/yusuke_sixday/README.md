# Yusuke six-day public-state Fieldbook (Python port)

Source: `yhay81/six-day-public-state-fieldbook` + dataset
`yhay81/six-day-public-state-agent-source`. Apache-2.0. Trees and
144-turn blocks copied from local hunt `policy.cpp`. Does not load
`agent.so`.

| period | turns | plans | decision |
|---|---|---:|---|
| day 0–6 | 0–143 | 1 | fixed opening |
| day 6–12 | 144–287 | 2 | carrot / rival weed; no-yarn shop bag → route 1 |
| day 12–18 | 288–431 | 1 | fixed bridge |
| day 18–24 | 432–575 | 3 | fert stock, tomato/milk/strawberry prices, weed geometry |
| day 24–30 | 576–719 | 5 | published tree; strawberry-crash leaf if wool still priced |

30 full-season paths from 8 stored tapes. Donors: rank-3 Bantam and
rank-8 Zenith Ye public blocks. Runtime excludes opponent identity,
seed, result, and future shops.

Recorded-seat clone 3-0 and G5 both-win (1.32.7, 720, DONE/DONE):

| stream | margin |
|---|---:|
| prvsiyan `100348898` | +1274 |
| fufufukakaka `100504057` | +8532 |
| masayoshi `100444645` | +1193 |
| Subin An `97399969` | +32946 |
| James Y `95677563` | +35432 |

After step 216 both day-6 routes differ from Fieldbook BALANCED. Extra
sheep are not 227/242/266. Uploaded `56028043` PENDING (2026-09-05
08:04:54 UTC). Newest-2 after COMPLETE: this + shopbag `55962761`. Root
`main.py` stays h2. Do not claim Windows ran `agent.so`.
