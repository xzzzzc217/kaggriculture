# moon_shopbag_v3 — latent (7,4) extra animal

Shopbag v1 yarn wrap, plus one guarded extra animal into the already
serviced empty pasture at `(7,4)`.

Rolling-12 (2026-08-30) is **3-9, all clones**. Yarn games still lose to
10–11 sheep; no-yarn games lose to +1–3 extra cows. `(7,4)` is built at
step 161, left empty after a failed PLACE at 223, then fed/cared/harvested
all season. Hand 4 is PASS at the shed `(4,4)` for steps 255–262 on every
checked replay.

| step | action |
|---|---|
| 255 | `BUY_ANIMAL` SHEEP if yarn in bag else COW |
| 256 | hand 4 `PICKUP` |
| 257–259 | EAST EAST EAST |
| 260 | `PLACE` on `(7,4)` |
| later | sell extra wool/milk from harvests on that tile |

Cancels on money, empty-pasture, PASS, or inventory mismatch.

Recorded-seat (1.32.7, 720):

| stream | shopbag | v3 | delta |
|---|---:|---:|---:|
| prvsiyan / fufu / masa clone | +5964 / +6937 / +7511 | identical | 0 |
| MtN 11-sheep | −17420 | −17420 | 0 |
| Yusuke 11-sheep | −13434 | −10296 | **+3138** |
| Hanserong 11-sheep | −14707 | −14707 | 0 |
| Hanserong clone rolling-12 | −11247 | −11247 | 0 |
| Lynxx win | +9240 | +9240 | 0 |

Fires only when the tape's step-223 PLACE left `(7,4)` empty. Most seeds
already occupy that tile, so the wrap is a no-op. **Not uploaded.**
