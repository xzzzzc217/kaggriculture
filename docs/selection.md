# Agent selection record

## Current local champion

- Candidate: Kaito V36 clone-horizon-2 controlled variant.
- Root file: `main.py`.
- Agent SHA-256: `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
- Offline bundle: `artifacts/submission/kaito_v36_h2/submission.tar.gz`.
- Bundle SHA-256: `049d7cc9c56d99c964f1ee0259e1c0477b4ae511f63611352b5800a143a5d5fc`.
- Online submission: `55658542`, uploaded once at 2026-08-21 02:41:43 UTC.
- Online status: `COMPLETE`; latest submissions API score `2015.6`, with the newest completed public
  episode reporting `2015.69` (first observation `1842.7`).

## Why it was selected

The change is narrowly targeted at a common near-clone matchup and is isolated to the existing
SELL-preemption horizon. It passed three independent evidence layers:

1. exact-reference development and holdout comparisons in both seats;
2. a 112-behavior public high-rating action-stream regression panel;
3. a fresh ten-seed closed-loop suite against exact V36, Boatlee V16-RC5, and Prvsiyan Moon.

The exact-V36 ten-seed holdout was 20/20 with all ten paired margins positive. No loss was added in
the 112-behavior regression panel. The result is strong enough for a first live measurement, not
strong enough to claim a medal or leaderboard rating before Kaggle evaluates it.

## Rollback and limitations

- Public V36 reference SHA-256:
  `f375ab7c67abecd116abd754ec76252d4e371f6e8d1743f88723e960e4eefc8f`.
- The previous weak local Agent is preserved at
  `artifacts/baselines/local_weak_v1/main.py` (ignored from version control).
- Public action-stream replays are open-loop after recording and cannot reproduce adaptive
  decisions. Dynamic head-to-head tests remain primary.
- The public-agent pool is only a sample of the live field. Live rating can differ materially due
  to opponent mix, seed variance, and meta adaptation.
- The score is highly provisional: at the first terminal snapshot, four games had finished
  (3 wins, 1 loss) and one was still in progress.
- One hour later the rating increased by `100.2` to `1942.9`. The newest visible window showed four
  completed wins and one game in progress, with no new visible loss or runtime failure. Historical
  and current windows are not added as an exact cumulative record because Kaggle only exposes a
  rolling subset in this view.
- At 05:44 UTC the submissions API reported `1998.8`, while the continuously updating game panel
  showed `1987`. The two surfaces update asynchronously, so both are recorded with timestamps
  rather than treated as contradictory final results.
- The first loss was episode `95677563` against James Y (`85,208` to `93,759`). Both Agents
  completed normally and h2's clone gate did not latch, so this is evidence of an opponent-model
  coverage gap rather than failure of the promoted clone-horizon parameter.
- James Y used all four quadrants, eight sheep, and much heavier fertilizer/wheat turnover. The
  existing local pool did not represent this economy strongly enough.
- Episode `95741586` added a second fertilizer/wheat-heavy loss: tipstar0125 won by only `594`, sold
  `1,833` fertilizer and `1,031` wheat versus our `216` and `739`, and never triggered the clone
  latch. This confirms the route family as a real coverage gap.
- Episode `95734726` exposed a separate near-clone failure: Colton Martin won by `589`; the clone
  latch activated at step 48 and public-state distance stayed near one for the rest of the game.
  The existing h2 preemption is therefore not a universal live-clone tie-breaker.
- Episode `95780431` confirmed the fertilizer/wheat-heavy cluster for a third time. vladee won by
  `5,018`, sold `1,906` fertilizer and `1,147` wheat versus our `216` and `718`, and did not trigger
  the clone latch. Both Agents completed normally.
- Episode `95791884` added a second near-clone market-timing case. asi1024 won by `616`; both Agents
  ended `DONE`, the clone latch activated at step 48, maximum near streak was 383, and median
  public-state distance was two. Our route sold `829` wheat versus the opponent's `428`, while
  fertilizer volume was almost identical (`216` versus `215`). The Agent log was unavailable in
  this bounded cycle, so final statuses are verified but stderr is not asserted.

## Next selection gate

Continue accumulating live episodes and compare loss clusters by opponent opening behavior, seat,
market timing, and clone-detector activation. The next local opponent suite must add a faithful
fertilizer/wheat/sheep-heavy adversary before any response is designed. Only a frozen single-variable
candidate that passes an independent 20-game both-seat holdout, does not regress against Boat/Moon,
and preserves all 112 public action-stream outcomes may use the second active slot. Do not react to
the provisional online rating with correlated submissions.

Kaito V37 is now the only frozen challenger. Its linked Kaggle output compiled and matched its own
46,304-byte SHA contract (`d8fd091e...42b8d`), but the Notebook source payload did not reconstruct
those bytes, so only the linked output is admissible. V37 won the three-seed development screen
6/6 against h2 with 3/3 positive seed pairs, mean margin `+2,226`, and worst margin `+237`. It then
passed the untouched 20-game both-seat holdout 20/20, with 10/10 positive seed pairs, mean margin
`+1,615.35`, worst margin `+4`, and Wilson 95% lower bound `0.839`. V37 then matched h2's perfect
Boat regression result: 20/20 wins and 10/10 positive seed pairs, with mean margin `+4,224.1` and
worst margin `+2,048`. It failed Moon at 8/20 wins and 4/10 positive seed pairs, far below the frozen
16/20 and 9/10 threshold. Mean margin was `-6,579.75` and worst margin `-31,273`. V37 is permanently
closed under this protocol: do not upload, retune, or repackage it. The online h2 Agent remains the
selected champion, and the second active slot stays unused until a structurally new candidate
passes every gate.
