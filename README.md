# Kaggriculture medal sprint

Archived research snapshot, published after the submission deadline. Authenticated Kaggle API
checked on 2026-10-22 reports deadline 2026-10-14 23:59 UTC and user rank 2734.
This rank is an API observation, not a verified final medal result. Older scores below are dated
historical observations. The root agent is a local baseline, not necessarily the last online submission.

Source, experiment definitions and research notes are preserved here. Local virtual environments,
replays, caches, downloaded competition data and generated artifacts are excluded; historical
commands referencing those paths require regenerating or downloading the inputs.
See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for licensing scope.

Status as of 2026-10-11: Kaggle reports 10,148 entered teams, user rank 2,721,
and final submission deadline 2026-10-14 23:59 UTC. The newest active pair is
`56679778` (“kaggriculture challenger”, public 1376.7) and `56679782`
(“kaggriculture reupload then-best”, public 1309.6), both `COMPLETE`.
Submissions `56395547` and `56395540` have been displaced. The first leaderboard
page showed a leader at 3275.1. Playbook:
[`docs/shop_bag_strategy.md`](docs/shop_bag_strategy.md).

## Competition and medal objective

- Kaggle Featured Simulation competition with Awards Points & Medals and a $50,000 prize pool.
- Two autonomous Agents play a 720-turn farming season. Each manages land, workers, crops,
  livestock, inventory, and orders into a shared price-sensitive market.
- The leaderboard is driven by repeated wins/losses/ties and a final Bradley-Terry tournament.
  Raw coin margin is diagnostic, but it is not the ranking target.
- Entry/team-merger deadline: 2026-09-23 23:59 UTC.
- Final submission deadline: 2026-10-14 23:59 UTC (extension verified via Kaggle API on 2026-10-11).
- Daily limit: 5 Agents; only the newest 2 submissions stay active.
- Runtime contract: 1.6 vCPU, 6.5 GiB RAM, 8 GiB disk, maximum 100 MiB, with `main.py` at the
  archive root.
- Live leaderboard snapshot on 2026-08-21: first place 3173.7, second 3080.5, third 3057.8.

Official competition files live under `data/competition/official/` and are excluded from version
control.

## Current champion

The root [`main.py`](main.py) is the current local champion. It starts from Kaito Fukami's public
V36 robust-hybrid Agent and changes exactly one frozen control parameter:

| Item | Value |
|---|---:|
| Public V36 source SHA-256 | `f375ab7c67abecd116abd754ec76252d4e371f6e8d1743f88723e960e4eefc8f` |
| Clone SELL-preemption horizon | `1 -> 2` turns |
| Promoted Agent SHA-256 | `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe` |
| Agent size | 46,981 bytes |
| Bundle SHA-256 | `049d7cc9c56d99c964f1ee0259e1c0477b4ae511f63611352b5800a143a5d5fc` |
| Bundle size | 35,088 bytes |

V36 follows a fixed high-throughput route with state-drift repair, a latched near-clone detector,
SELL preemption against near-identical routes, and a reserve-safe wheat market maker. Extending the
preemption horizon from one to two turns is intended to break ties against the increasingly common
V36-like behavior without modifying the production route or taking a broad market-timing risk.

The variant is generated mechanically by
[`scripts/build_kaito_variant.py`](scripts/build_kaito_variant.py), so the single-variable change is
auditable. The former infrastructure baseline is preserved under the ignored
`artifacts/baselines/local_weak_v1/` directory.

## Evidence and promotion gate

All dynamic matches use the official `kaggle-environments==1.32.7` engine, run the full 720 turns,
reverse seat order for every seed, and require both Agents to finish with `DONE` status.

### Closed-loop dynamic holdout

| Opponent | Seeds | Games | W/T/L | Positive seed pairs | Mean margin | Worst margin |
|---|---:|---:|---:|---:|---:|---:|
| Exact public Kaito V36 | 10 | 20 | 20/0/0 | 10/10 | +2,315.7 | +1,443 |
| Boatlee V16-RC5 | 10 | 20 | 20/0/0 | 10/10 | +7,166.1 | +1,408 |
| Prvsiyan Moon | 10 | 20 | 16/0/4 | 9/10 | +4,926.4 | -6,215 |

The Kaito comparison is the primary preregistered gate. On a prior three-seed holdout, h2 won 5/6
games and all three paired margins were positive; on the new ten-seed holdout it won 20/20. The
Moon slice remains seed-sensitive, so the candidate is not described as universally dominant.

### Public strong-field action-stream panel

The public daily-meta dataset contains 421 rows and 112 distinct 24-turn opening behaviors from
opponents rated at least 2000. For each behavior, the benchmark selects the highest-rated row and
replays its recorded action stream under the recorded seed and seat.

- h2: 112/112 wins, mean margin +90,877.9, worst margin +16,341.
- public V36: 112/112 wins, mean margin +90,861.1, worst margin +16,341.
- paired h2 minus V36: mean +16.8; 102 unchanged, 1 positive, 9 negative; no outcome flips.

This is a broad deterministic stress panel, not a substitute for closed-loop opponents: recorded
actions cannot adapt to the candidate, and market interaction means reproduced banks need not equal
the source episode. We therefore use it to catch regressions and behavior coverage gaps, not to
claim an official expected rating.

### Rejected routes

- The initial local melon/carrot fleet and wheat-loop baselines lost badly to strong public Agents
  and remain infrastructure-only.
- Flexonafft Adaptive and Tetsutani Adaptive were behaviorally equivalent in the sampled matchup.
- Prvsiyan Soil was weaker than Moon in the local paired screen.
- Amey Premium-First beat Moon on one development seed but lost the four-seed extension.
- Clone horizons 3 and 6 were not promoted because horizon 2 produced the strongest controlled
  clone result while exposing less timing surface.

## Reproducible workflow

Set up the isolated environment:

```powershell
C:\Users\21398\Miniconda3\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip uninstall -y open_spiel
```

`open_spiel==2.0.1` crashes during unrelated environment discovery on this Windows host;
Kaggriculture itself does not use it. The harmless missing-`pyspiel` warning can still appear at
startup.

Run the checks and rebuild the immutable package:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe scripts\build_submission_bundle.py `
  --main main.py `
  --output artifacts\submission\kaito_v36_h2\submission.tar.gz `
  --report artifacts\submission\kaito_v36_h2\bundle_report.json
```

Evaluation utilities:

- [`scripts/evaluate_head_to_head.py`](scripts/evaluate_head_to_head.py): full-season, both-seat,
  multi-seed closed-loop comparison.
- [`scripts/evaluate_replay_benchmark.py`](scripts/evaluate_replay_benchmark.py): deterministic
  behavior-stratified public action-stream stress panel.
- [`scripts/materialize_public_agent.py`](scripts/materialize_public_agent.py): static extraction of
  public notebook Agents without executing notebook code.
- [`scripts/build_submission_bundle.py`](scripts/build_submission_bundle.py): deterministic tarball
  construction plus compile, member, byte-identity, size, and SHA verification.

See [`docs/selection.md`](docs/selection.md), [`docs/progress_log.md`](docs/progress_log.md), and
[`docs/compute_strategy.md`](docs/compute_strategy.md) for the decision record and compute policy.

## Compute policy and next action

The current bottleneck is game simulation and opponent modeling, so CPU parallelism is materially
faster than forcing the RTX 4060 or Kaggle GPU into the loop. GPU time remains reserved for a
pre-registered behavior-cloning/value-model experiment only after a cached trajectory dataset and
a CPU promotion baseline exist.

The first loss, episode `95677563` against James Y, has been downloaded with the Agent log and
analyzed. Both Agents finished normally; h2's clone gate never latched (maximum near-clone streak
was 6 versus the required 24), so the loss was not caused by the clone-horizon change. James Y won
`93,759` to `85,208` with a structurally different four-quadrant, eight-sheep,
fertilizer/wheat-heavy economy. This route is now the priority adversarial coverage gap. No second
Agent will be uploaded until a frozen candidate beats the current champion on an independent
both-seat holdout, avoids regression on existing strong baselines, and preserves all 112 public
action-stream outcomes.

At 2026-08-21 04:44 UTC, Kaggle reported `1942.9` (up `100.2`). The newest visible completed games
were wins over Francesco Montone, Faiz, darktetradgod, and RishabhSpark, with a game against Gebreab
K. Zewdie in progress. No new failure cluster or runtime error was visible, so this rating movement
does not authorize a reactive second submission.

At 05:44 UTC, the API score reached `1998.8`, while the live panel showed `1987` after newer games.
Two new losses were downloaded and analyzed. Episode `95741586` was a `594`-coin loss to
tipstar0125: no runtime error or clone latch occurred, and the opponent again used much heavier
fertilizer/wheat turnover. Episode `95734726` was a `589`-coin loss to Colton Martin: the Agents
remained near-identical for the entire game and the clone gate latched at step 48, but small market
timing differences still favored the opponent. These are two distinct, narrow failure modes; they
justify extending the adversarial suite, not immediately changing or uploading the Agent.

At 06:44 UTC, the API score was `1973.8`. Episode `95780431` against vladee added a third
fertilizer/wheat-heavy loss: `-5,018`, no clone latch, no runtime error, with the opponent selling
`1,906` fertilizer and `1,147` wheat versus our `216` and `718`. This strengthens the existing
failure cluster without introducing a new mechanism, so the correct response remains local
closed-loop adversary coverage rather than a speculative upload.

At 07:44 UTC, the API score reached a new provisional peak of `2001.5`. A new public Kaito V37
candidate was audited without executing its Notebook. The Notebook's embedded source payload did
not reproduce its claimed artifact, but the separately linked Kaggle output was internally
consistent: 46,304 bytes, compiling successfully, with SHA-256
`d8fd091e3f4278464a50a8e997a70a79692e32aaf6e0358e42c86d238d142b8d`. Using only that verified
output, V37 beat the current h2 champion 6/6 on three new full-season, both-seat development seeds;
all three paired margins were positive and the worst game margin was `+237`. This promotes V37 to
a frozen independent-holdout candidate, not to an upload: the required 20-game holdout, Boat/Moon
regression checks, live failure-class opponents, and 112-behavior panel remain incomplete.

At 08:44 UTC, the API score reached `2005.2`. V37 then passed its untouched independent holdout
against h2 on seeds 20261011-20261020: 20/20 wins, 10/10 positive paired margins, Wilson 95% lower
bound `0.839`, mean margin `+1,615.35`, and worst margin `+4`. The perfect W/L result is strong, but
the four-coin minimum shows that it is not a universal margin improvement. V37 is therefore
promoted only to the next local gate; Boat, Moon, live fertilizer/wheat and near-clone adversaries,
and the 112-behavior panel must still pass before the second online slot can be used.

At 09:44 UTC, the API score reached `2011.0`. V37 passed the frozen Boatlee V16-RC5 regression on
the existing reference seeds: 20/20 wins, 10/10 positive seed pairs, mean margin `+4,224.1`, and
worst margin `+2,048`. This exactly preserves h2's Boat W/L and paired outcomes. V37 advances to
Moon regression, but no upload is authorized until the remaining live-adversary and behavior-panel
gates also pass.

At 10:45 UTC, V37 failed the frozen Moon regression decisively: 8/20 wins, only 4/10 positive seed
pairs, mean margin `-6,579.75`, and worst margin `-31,273`, versus the preregistered minimum of
16/20 wins and 9/10 positive pairs. V37 is therefore closed and will not be uploaded, tuned, or
repackaged. The existing online h2 Agent remains the selected champion.

At 11:46 UTC, the submissions API reported `2015.6`; the newest completed public episode,
`95922096`, puts the provisional rating at `2015.69`. One bounded failure-attribution cycle analyzed
episode `95791884` against asi1024, a `616`-coin loss. Both Agents ended `DONE`; the clone gate
latched at step 48, maximum near streak was 383, and median public-state distance was two. The
submitted Agent sold `829` wheat versus the opponent's `428`, while fertilizer volume was nearly
identical (`216` versus `215`). This is a second near-clone market-timing/economic-divergence case,
not another fertilizer-heavy opponent. No Agent log was retrieved in this cycle, so no stderr claim
is made. The result strengthens the adversarial test requirement but does not authorize an upload.

## Repository visibility

Public research archive after the competition submission deadline.
