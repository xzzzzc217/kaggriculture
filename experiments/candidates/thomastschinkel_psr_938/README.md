# thomastschinkel public-state later-block router (cut 15)

Source: `thomastschinkel/kaggriculture-93-8-win-rate-public-state-router`.
Static `%%writefile` extract; notebook cells were not executed. Does not
load `agent.so`.

Public-state tree reselect every 144 turns, including after step 216:

| step | block | note |
|---|---|---|
| 0 | `_choose(0, features)` | opening |
| 144 | `_choose(1, features)` | day 6 |
| 288 | `_choose(2, features)` | later-block |
| 432 | `_choose(3, features)` | later-block |
| 576 | `_choose(4, features)` | later-block |

On the prvsiyan clone observation the live tape is 0→2 at 144, 2→0 at
288, 0→3 at 576. Extra sheep on the main tape is **265**, not
227/242/266. After 216 the tape differs from live six-day, Fieldbook
BALANCED, and cut 14 (226/360/433).

Recorded-seat clone 3-0 and G5 both-win (1.32.7, 720, DONE/DONE):

| stream | margin |
|---|---:|
| prvsiyan `100348898` | +5757 |
| fufufukakaka `100504057` | +28052 |
| masayoshi `100444645` | +16873 |
| Subin An `97399969` | +31605 |
| James Y `95677563` | +68313 |

Uploaded `56146106`. Newest-2 partner is shopbag `56112309`. Root
`main.py` stays h2. Do not claim Windows ran `agent.so`.
