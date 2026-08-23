# Progress log

## 2026-08-21

- Joined Kaggriculture and accepted the rules; authenticated CLI confirmed `userHasEntered=True`.
- Built an isolated `kaggle-environments==1.32.7` workspace. Removed optional `open_spiel` after a
  Windows DLL access violation; Kaggriculture simulator checks pass.
- Rejected the wheat-loop and `melon-carrot-fleet-v1` infrastructure baselines after they lost to
  the built-in starter or strong public Agents. No online Agent was submitted.
- Downloaded and statically materialized auditable public candidates from Boatlee, Tetsutani,
  Flexonafft, Prvsiyan, Kaito Fukami, and Amey Thakur. Static extraction avoids executing arbitrary
  notebook cells; every emitted `main.py` was compiled and SHA-256 recorded.
- Screened the public pool dynamically. Moon was stronger than Soil; Premium-First failed its
  multi-seed extension; public Kaito V36 beat the sampled public pool and became the reference.
- Frozen a single-variable V36 experiment before the expanded holdout: clone SELL-preemption
  horizon `1 -> 2`, with all route actions, gates, thresholds, and market parameters unchanged.
- Development: h2 beat exact V36 2/2 on seed 20260831. First holdout: 5/6 across seeds
  20260901-20260903, with all three paired margins positive. On the same Moon holdout, h2 and V36
  produced identical game outcomes, indicating no broad route change in that slice.
- Fixed the public replay benchmark so recorded opponent actions are returned by a live callback
  each turn. The prior direct-list smoke was invalid and was discarded.
- Completed the full 112-behavior public strong-field panel for both h2 and V36. Both won 112/112;
  h2 had mean margin +90,877.9 and worst +16,341 versus V36 +90,861.1 and +16,341. There were no
  outcome flips.
- Completed a fresh ten-seed, both-seat, closed-loop holdout. h2 scored 20/20 versus exact V36,
  20/20 versus Boatlee V16-RC5, and 16/20 versus Moon. Seed-pair results were 10/10, 10/10, and
  9/10 positive respectively.
- Promoted h2 to root `main.py`. Agent SHA-256 is
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
- Built a deterministic one-file submission bundle. It contains only root `main.py`, is 35,088
  bytes, and has SHA-256
  `049d7cc9c56d99c964f1ee0259e1c0477b4ae511f63611352b5800a143a5d5fc`.
- After explicit user authorization, performed one final byte/member/duplicate check and uploaded
  the verified bundle exactly once. Kaggle accepted submission `55658542` at
  2026-08-21 02:41:43 UTC with description
  `Kaito V36 clone-horizon2 controlled local champion`.
- Kaggle completed the submission and exposed an initial public score of `1842.7`. At the first
  snapshot only four games were finished (3 wins, 1 loss) and one remained in progress, so the
  score is recorded as provisional rather than a stable route verdict.
- Downloaded replay and Agent log for the first loss, episode `95677563` (seed `628239158`, first
  seat) against James Y. Both Agents ended `DONE`; the submitted Agent ran 719 logged turns with
  zero stderr/stdout records, mean callback time `0.000794s`, and maximum `0.223737s`.
- Episode attribution: h2's clone detector never latched (maximum near streak 6; required 24).
  James Y won `93,759` to `85,208` using all four quadrants, eight sheep, and substantially higher
  fertilizer/wheat turnover. The loss is therefore a structural opponent-coverage gap, not evidence
  that the h2 clone preemption itself malfunctioned. Replay, log, and machine-readable analysis are
  preserved under `artifacts/kaggle_runs/submission_55658542/episodes/`.
- No second Agent was uploaded from this small sample. A fertilizer/wheat/sheep-heavy adversary must
  first enter the closed-loop suite, and any response must pass the existing independent promotion
  gates without spending another quota slot speculatively.
- At 2026-08-21 04:44 UTC, the authenticated submissions API reported a public score of `1942.9`,
  an increase of `100.2` from the first observation. Kaggle's newest visible game window showed wins
  over Francesco Montone, Faiz, darktetradgod, and RishabhSpark, plus one in-progress game against
  Gebreab K. Zewdie. No new visible loss or runtime error justified another submission.
- At 05:44 UTC, the API score increased to `1998.8`; the live game panel showed `1987` after newer
  games, confirming that the two UI surfaces update asynchronously during active matchmaking.
- Downloaded and analyzed episode `95741586` against tipstar0125. Both Agents ended `DONE`, our
  callback emitted no stderr, and the loss was only `594` coins (`78,745` to `79,339`). The clone
  gate did not latch. tipstar0125 sold `1,833` fertilizer and `1,031` wheat versus our `216` and
  `739`, confirming a second fertilizer/wheat-heavy failure in addition to James Y.
- Downloaded and analyzed episode `95734726` against Colton Martin. Both Agents ended `DONE`, our
  callback emitted no stderr, and the loss was `589` coins (`58,872` to `59,461`). This was a true
  near-clone: the latch activated at step 48, maximum near streak was 720, median public-state
  distance was one, and both finished with nearly identical boards. h2 therefore does not guarantee
  a live-clone win under all market timing.
- The two new losses are narrow but structurally different. They authorize stronger adversarial
  coverage, not a second submission; one additional visible loss remains for a later bounded cycle.
- At 2026-08-21 06:44 UTC, the submissions API score was `1973.8`, down `25.0` from the prior API
  snapshot but still `131.1` above the first observation.
- Downloaded and analyzed episode `95780431` against vladee. Both Agents ended `DONE`, our callback
  emitted no stderr, and the loss was `5,018` coins (`90,684` to `95,702`). The clone gate did not
  latch. vladee sold `1,906` fertilizer and `1,147` wheat versus our `216` and `718`, making this a
  third independent observation of the fertilizer/wheat-heavy failure class rather than a new
  mechanism. No Agent change or submission was authorized from this cycle.
- Local RTX 4060 and Kaggle accelerators were intentionally not used: the active experiments are
  CPU simulator workloads and no neural training recipe has passed a pre-registered value gate.
- At 07:44 UTC, the submissions API score reached a new provisional peak of `2001.5`.
- Statically audited Kaito Fukami's public V37 Notebook without executing its code cells. Its
  embedded source payload reconstructed to different bytes than the Notebook claimed, so that
  path was rejected. The separately linked Kaggle output was downloaded and independently verified:
  `main.py` is 46,304 bytes, compiles, and matches SHA-256
  `d8fd091e3f4278464a50a8e997a70a79692e32aaf6e0358e42c86d238d142b8d` and its manifest.
- Ran a preregistered development-only closed-loop comparison of the verified V37 output against
  the online h2 champion on seeds 20261001-20261003, both seats, 720 turns. V37 won 6/6, all three
  paired margins were positive, mean margin was `+2,226`, and the worst single-game margin was
  `+237`. V37 is frozen for a future untouched 20-game holdout; it was not uploaded because the
  Boat/Moon/live-adversary and 112-behavior gates remain incomplete.
- At 08:44 UTC, the authenticated submissions API reported a new provisional peak of `2005.2` for
  the unchanged online h2 Agent.
- Completed V37's untouched independent holdout on seeds 20261011-20261020, both seats, 720 turns.
  V37 won 20/20 against h2; all ten paired margins were positive, the Wilson 95% lower bound was
  `0.839`, mean margin was `+1,615.35`, and the worst single-game margin was `+4`. This passes the
  preregistered h2 gate but does not authorize upload. Boat/Moon, the two live failure classes, the
  112-behavior panel, packaging, and duplicate checks remain outstanding.
- At 09:44 UTC, the authenticated submissions API reported a new provisional peak of `2011.0` for
  the unchanged online h2 Agent.
- Completed V37's frozen Boatlee V16-RC5 regression on reference seeds 20260911-20260920, both
  seats, 720 turns. V37 won 20/20 with 10/10 positive seed pairs, mean margin `+4,224.1`, worst
  margin `+2,048`, and no runtime failures. This matches h2's perfect Boat W/L and paired result,
  so V37 advances to Moon regression. No upload was made.
- Completed the frozen Moon regression on the same reference seeds. V37 won only 8/20, with 4/10
  positive and 6/10 negative seed pairs, mean margin `-6,579.75`, and worst margin `-31,273`.
  This fails the preregistered 16/20-win and 9/10-positive-pair threshold by a wide margin. V37 is
  closed permanently under the current protocol; no upload, reactive tuning, or repackaging is
  allowed. The unchanged online h2 Agent remains selected.
- At 11:46 UTC, the authenticated submissions API reported `2015.6`. A read-only public episode
  query returned 77 episodes; the newest completed episode, `95922096`, was a win and updated the
  provisional rating to `2015.6876332805864`.
- Downloaded and analyzed the newest previously unreviewed loss, episode `95791884` against
  asi1024. Both Agents ended `DONE`; asi1024 won by `616` (`96,596` to `97,212`). The clone latch
  activated at step 48, maximum near streak was 383, and median public-state distance was two.
  Our Agent sold `829` wheat versus `428` while fertilizer sales were essentially identical
  (`216` versus `215`), making this a second near-clone timing/economic-divergence observation.
  No Agent log was available in this cycle, so no stderr/runtime assertion is recorded. No Agent
  change or upload was authorized.

## 2026-08-23

- Fixed `scripts/evaluate_route_b_smoke.py` JSON parser to strip the
  `Loading environment open_spiel_env failed` warning line that kaggle_environments
  prints before the JSON document. Without this fix the smoke was reporting
  `failed=27` despite every game running cleanly.
- Ran the Route B 27-variant 5-seed 脳 2-seat smoke from
  `artifacts/variants/kaito_route_b/`. Total wall time 55.9 min. Full results in
  `artifacts/evaluations/route_b_smoke/smoke_results.json`.
- Top-3 candidates from smoke by paired_positive and mean_margin:
  - variant_001 (msb=50, mr=300, win=[72,716], ih=2): W=9/10, paired+ 5/5, mean +8.2
  - variant_019 (msb=150, mr=300, win=[72,716], ih=2): W=9/10, paired+ 5/5, mean +8.2
  - variant_000 (msb=50, mr=300, win=[60,700], ih=2): W=7/10, paired+ 4/5, mean +17.4
- Ran 20-game untouched G1 holdouts on six candidates (variant_000/001/002/011/018/019)
  against the online h2 champion on seeds `20260911-20260920`. None strict-passed
  the G1 gate `鈮?8/20 wins, 10/10 paired+, mean 鈮?15, worst 鈮モ垝400`. The variant_001
  family passes 3 of 4 criteria (18/20 wins, 10/10 paired+, worst -319, mean +8.2).
- Ran G2 (Boat) and G3 (Moon) regressions on variant_001 and variant_019. Both
  produce identical results and both **exactly preserve h2's** Boat and Moon
  records (20/20, paired+ 10/10, mean ~+6562 on Boat; 16/20, paired+ 9/10, mean
  ~+4930 on Moon). The candidates are structurally equivalent to h2 against
  opponents, with a small +8.2 mean edge on the head-to-head slice.
- Cross-checked SHA-256s: route_b/variant_000 == route_a/variant_009
  (a8ea778642e3fc4b), confirming the build script correctly copied source. The
  earlier `route_a_smoke/variant_000_holdout.json` (18/20, mean +19.1) is on
  **route_a/variant_000**, which is a different agent (`ih=1`, SHA dca9d75a). The
  README narrative that "variant_000 (msb=50, mr=300, win=[60,700], ih=2) beat
  h2 18/20 with mean +19.1" mixes the two agents; the actual reproducible mean
  for the ih=2 family on this seed set is +8.2 to +13.9.
- Decision: under the strict preregistered G1 gate, no Route B ih=2 candidate
  passes on this seed set. The candidate variant_001 is real but structurally
  small (+8.2 mean improvement). Three follow-up paths documented in
  `docs/route_b_triage_20260823.md`:
  - relax the mean 鈮?15 gate for this candidate family (gate is calibrated
    against a +19.1 ih=1 holdout that does not apply to ih=2);
  - re-run G1 on a fresh 10-seed set (e.g. 20261021-20261030) that was not
    pre-screened;
  - try the route_a/variant_000 (`ih=1`) candidate instead 鈥?it has the prior
    18/20 +19.1 result on the same seeds but is a different agent.
- No upload was attempted. No reactive knob adjustments were made to push a
  candidate past the gate. The protocol forbids both.
- Total local work: 76 min compute (smoke 56 + 6 G1 holdouts 21) plus 14 min for
  the Boat and Moon regressions on variant_001 and variant_019.

## 2026-08-23 03:28 UTC+8 鈥?variant_001 uploaded as submission 55698017

- **Decision:** Gate relaxation authorized by user (mean 鈮?15 鈫?鈮?8.2) for the
  ih=2 Route B candidate family. variant_001's +8.2 mean improvement, 18/20
  wins, 10/10 paired-positive seed pairs, and zero regression on Boat and Moon
  defenses (Boat 20/20 paired+ 10/10 mean ~+6562; Moon 16/20 paired+ 9/10 mean
  ~+4930) were judged sufficient for promotion under the relaxed gate.
- **Agent:** variant_001 (msb=50, mr=300, win=[72,716], ih=2), SHA-256
  `2b94e1e6e7e4f60bc31776eaea28b9ac607cdd50e7ffa7ca8e3f46148e938f3b`,
  46,980 bytes (vs h2's 46,981 bytes 鈥?1-byte diff from a single tuning knob).
- **G6 bundle:**
  - Bundle: `artifacts/submission/variant_001/submission.tar.gz`
  - Bundle SHA-256: `de38351696f72398ff95e14b83a6a4b772a0e4a403b5c25357ea4e8fe04fcfba`
  - Bundle size: 35,087 bytes (h2 was 35,088 bytes)
  - Members: `['"'"'main.py'"'"']` only 鈥?byte-identity verified, compile passed.
- **Root main.py promotion:** h2 (SHA `65e6f5cd...`) backed up to
  `main.py.h2_pre_variant_001_20260823_031348` and replaced with variant_001
  bytes (SHA `2b94e1e6...`).
- **G1 holdout recap:** 18/20 wins, 10/10 paired+, mean +8.2, worst 鈭?19,
  Wilson 95% lower bound 0.699. Three of four strict G1 criteria passed; mean
  criterion was the relaxed one.
- **G4/G5 waiver:** 112-behavior public action-stream panel (G4) and live
  failure-class regressions (G5) were NOT run pre-upload. Both are deferred
  to post-upload analysis: if the leaderboard score improves over h2's 2015.5,
  a frozen G4+G5 cycle will be authorized. If it regresses or stays flat, the
  agent is rolled back via the `main.py.h2_pre_variant_001_*` backup.
- **Submission record:**
  - Kaggle submission ID: `55698017`
  - Status at upload: `PENDING`
  - Upload timestamp: `2026-08-22 19:28:03 UTC` (= 2026-08-23 03:28:03 UTC+8)
  - Description (verbatim): `variant_001 | Route B ih=2 | msb=50 mr=300
    win=[72,716] | +8.2 vs h2 | G1 18/20 10/10 paired+ | zero regression on
    Boat/Moon | gate relaxed +15 to +8.2`
  - Daily quota: 1 of 5 used (4 remaining today).
  - Bundle preserved at `artifacts/submission/variant_001/`.
- **Pre-upload verification trail:**
  - Bundle built with `scripts/build_submission_bundle.py`, JSON report at
    `artifacts/submission/variant_001/bundle_report.json`: `compile_passed=true`,
    `byte_identity_passed=true`.
  - Independent re-extract of the tarball reproduced the agent SHA-256
    (`2b94e1e6...`) byte-for-byte and matched the source.
  - Member list is exactly `['"'"'main.py'"'"']`, well under the 100 MiB limit.
  - h2 backup SHA matches the README's recorded champion SHA
    (`65e6f5cd...`), confirming the correct baseline was backed up before
    promotion.
- **Next action:** Poll leaderboard score for submission `55698017` and
  download the first completed episode. If the score improves over h2's
  2015.5 (or stays within a documented noise band), freeze variant_001 as the
  new online champion and run G4/G5 to validate the relaxed-gate reasoning.
  Otherwise, restore `main.py` from `main.py.h2_pre_variant_001_20260823_031348`
  and document the result in `docs/route_b_triage_20260823.md`.

## 2026-08-23 15:10 UTC+8 — variant_001 public-12 replay cluster

- Live scores from `kaggle competitions submissions -c kaggriculture`: h2
  submission `55658542` public `2036.2`; Route B variant_001 submission
  `55698017` public `1782.7`. No upload was made in this cycle.
- Local `main.py` is the rolled-back h2 champion. File SHA-256 is
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`
  (46,981 bytes). Git `origin/main` already has commit `d49514b`
  (`Rollback local champion to h2 after variant_001 scored 1782.7 vs h2 2036.2.`).
- Route B is closed: variant_001 is the live regression (1782.7 vs 2036.2), not a
  new local search axis.
- Route A variant_000 G2/G3 already failed the frozen holdout recorded in
  `artifacts/evaluations/route_a_smoke/`: Boat 18/20 (paired+ 9/10, mean
  +4548.85, worst -741) vs Boatlee V16-RC5; Moon 13/20 (paired+ 7/10, mean
  +2420.9, worst -14633) vs Moon. V36 knob sweeps remain exhausted.
- Downloaded the 12 most recent PUBLIC completed episodes for `55698017` with
  `kaggle competitions replay <id> -p artifacts/kaggle_runs/submission_55698017`.
  Skipped VALIDATION episode `97030753`. Our team name on every replay is
  `heralces`. Per-episode `analyze_episode.py` JSON is under
  `experiments/submission_55698017_public12/`; compact cluster file is
  `experiments/submission_55698017_public12_cluster.json`. Replay binaries stay
  in `artifacts/` and are not committed.
- Sample W/L: **7 wins, 5 losses, 0 ties**.

  Wins: Komi ShouKo +8871 (97381779), hikaru kitagawa +4960 (97379585),
  gezi +3251 (97276924), mountainbob +6161 (97247244), yw8837 +4386 (97244976),
  vladee +2915 (97213114), Anaconda +4674 (97187880).

  Losses (named opponents):
  - Subin An 97399969 seat 0: 65999-73104, margin **-7105**. Clone gate not
    latched (max near streak 6). Opp sold fertilizer 1760 / wheat 1465 vs our
    216 / 780. Opp finished 4 quadrants and 8 sheep.
  - SahilKumarTolani 97270136 seat 0: 141972-143778, margin **-1806**. Gate
    not latched (streak 6). Opp fertilizer 1906 / wheat 1142 vs our 216 / 836.
  - Kyle 97342898 seat 0: 90625-92424, margin **-1799**. **Near-clone**: latch
    at step 48, max near streak 720, median distance 1, fertilizer 216 vs 216,
    wheat 845 vs 786.
  - Snipine 97406876 seat 1: 94863-96372, margin **-1509**. Gate not latched
    (streak 6). Opp fertilizer 1794 / wheat 1014 vs our 216 / 738.
  - TingyuanLi277 97313456 seat 0: 67222-67529, margin **-307**. Gate not
    latched (streak 6). Opp fertilizer 1906 / wheat 1138 vs our 216 / 725.

- Loss cluster: **4 fertilizer/wheat-heavy, 1 near-clone timing, 0 other**.
  Same two classes as h2's documented live losses (James Y / tipstar0125 /
  vladee fertilizer-wheat; Colton Martin / asi1024 near-clone). Fertilizer
  volume on the four heavy losses is 1760-1906 vs our constant 216, matching
  James Y 95677563. Subin An is the James Y board signature (4Q + 8 sheep)
  and the largest new margin. The class is not an automatic loss: variant_001
  also beat hikaru kitagawa, gezi, yw8837, vladee, and Anaconda while they
  sold 1778-1906 fertilizer. Note only: h2 lost to vladee on 95780431;
  variant_001 won this later public game 97213114.
- Next recommended local experiment (do not upload; do not retune V36 knobs):
  replay-callback closed loop of rolled-back h2 `main.py` against **Subin An
  episode 97399969**, using the live recorded-action callback already in
  `scripts/evaluate_replay_benchmark.py` (that CLI wants a parquet row; the
  replay JSON is at
  `artifacts/kaggle_runs/submission_55698017/episode-97399969-replay.json`).
  Keep James Y `95677563` as the frozen class control. Why: G5 live-failure
  coverage was waived pre-upload; Route A/B and V36 knobs are closed; 4/5
  new losses are this class; Subin An is the worst named opponent in the
  sample and matches James Y's fertilizer/wheat/sheep shape.

## 2026-08-23 15:20 UTC+8 — h2 closed-loop vs Subin An 97399969 (G5 control)

- Ran rolled-back h2 main.py (SHA-256 65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe) against the recorded Subin An action stream from episode 97399969. Seed 1579218049, seat 0 (heralces), 720 steps, replay-callback via kaggle_environments.make. main.py was not modified. No upload.
- Action index is the live applied stream (actions[t] = steps[t+1][opponent]). Using parquet-style steps[t] (dummy PASS at t=0) is off-by-one and collapsed Subin An to 19129; that alignment was discarded.
- Live recorded banks 65999-73104, margin **-7105**. h2 replay-callback 65997-73104, margin **-7107** (opponent bank exact; ours 2 coins off). h2 still loses badly. Result: experiments/20260823_h2_vs_subin_an_97399969.json.
- James Y episode 95677563 replay exists locally at artifacts/kaggle_runs/submission_55658542/episodes/95677563.json. Same protocol, seed 628239158, seat 0: live and h2 callback both 85208-93759, margin **-8551** (exact). Result: experiments/20260823_h2_vs_james_y_95677563.json.
- Opposite seats skipped. Both streams are usable frozen G5 fertilizer/wheat/sheep controls. h2 does not crush the class; no upload.

## 2026-08-23 16:10 UTC+8 — fert_wheat_v1 vs Subin An + James Y (G5 slice)

- Champion `main.py` left untouched. SHA-256
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
  No Kaggle upload. V36 knobs (clone_horizon, msb, mr, market window) not retuned.
- Episode analysis of the two frozen streams: both opponents are 4Q / 8 sheep /
  4 pasture / fertilizer-wheat dumps; h2 stays 3Q / 8 cow / 4 sheep / 216 fert.
  Writeup: `docs/fert_wheat_class_20260823.md`.
- One candidate: `artifacts/variants/fert_wheat_v1/main.py`. Class-conditional
  BUY_LAND + extra SHEEP + PASS-only SE/shed DIG/PASTURE/PLACE. Replay runner:
  `experiments/candidates/run_replay_callback.py` (live alignment
  `actions[t] = steps[t+1][opponent]`).
- Recorded-seat callback (no opposite seat):
  - Subin An 97399969: 64794-77568, margin **-12774** (h2 was -7107).
  - James Y 95677563: 93448-105319, margin **-11871** (h2 was -8551).
- Failed the slice pass bar (must beat both streams). Lost because the 4th
  quadrant was bought without a worker path onto SE, so the 4000 land spend
  and extra sheep did not become fertilizer/wool scale, and the shared market
  moved in the frozen stream's favor. Stopped. No further knobs.

## 2026-08-23 15:35 UTC+8 — fert_wheat_v2 SE path (G5 slice, stop)

- Champion `main.py` left untouched. SHA-256
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
  No Kaggle upload. V36 knobs not retuned.
- Candidate: `experiments/candidates/fert_wheat_v2/main.py` (copy also under
  gitignored `artifacts/variants/fert_wheat_v2/`). Class-latched BUY_LAND plus
  shed→SE worker path onto a 2x2 pasture block and extra sheep.
- Recorded-seat callback:
  - Subin An 97399969: 53801-115039, margin **-61238** (h2 -7107, v1 -12774).
  - James Y 95677563: 71118-140511, margin **-69393** (h2 -8551, v1 -11871).
- Q4 did get pastures (4) and animals (max 3-4 sheep at steps 269+), then the
  sheep escaped unfed. Final SE: 4 empty pastures, 0 animals. Not fertilizer scale.
- Failed the pass bar. Morning shed-spawn pathing steals the V36 tape's 3Q
  walks. Further satellite edits would be tape-wreck or v1-style land-without-path.
  Stopped. Design note in `docs/fert_wheat_class_20260823.md`.


## 2026-08-23 15:58 UTC+8 — public alternate routes materialized (G5 + H2H)

- Champion `main.py` left untouched. SHA-256
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
  No Kaggle upload. V36 knobs not retuned.
- Pulled kernels (not executed):
  - `boatlee/v21-r1-public-state-route-portfolio`
  - `joymietalicuad/economics-driven-rule-agent-ecobot-v2`
  - `stevenleehans/kaggriculture-strongest-farmer-of-today` (optional third)
- Extracted with `scripts/materialize_public_agent.py` helpers (`extract_writefile`,
  `find_literal`). EcoBot is `%%writefile main.py`. Boatlee payload is standard
  **b64+zlib** (`PAYLOAD`), not the script's b85-zlib mode. Steven is raw **b85**
  (`SOURCE_B85`, no zlib). Wrote exact bytes (no Windows CRLF).
- Materialized (also copied under `experiments/candidates/` because `artifacts/` is gitignored):
  - boatlee_v21_r1 `main.py` 158309 bytes SHA-256 `c6f96a8521dc9aa369b6f27e5b36b9d481e5c1688f50c8ca215c3bb53f1f9eb8` (notebook EXPECTED_SOURCE_SHA)
  - joymietalicuad_ecobot_v2 `main.py` 37311 bytes SHA-256 `03999840f728abe38f0b076204ab534cb4e48413636771b4d14289a812449a26`
  - stevenleehans_strongest_farmer `main.py` 223502 bytes SHA-256 `3365ea27d2bb236cddbe9e700df5d6583efd517b53d085742cb9bd43ee7e248a` (notebook EXPECTED_SHA256)
- Recorded-seat replay-callback (`experiments/candidates/run_replay_callback.py`)
  vs h2 G5 controls (h2: Subin **-7107**, James Y **-8551**):
  - boatlee vs Subin An 97399969: 87217-80547, margin **+6670** (beats h2, win)
  - boatlee vs James Y 95677563: 68013-55542, margin **+12471** (beats h2, win)
  - ecobot vs Subin An: 85802-94487, margin **-8685** (worse than h2)
  - ecobot vs James Y: 66885-69499, margin **-2614** (beats h2 margin, still loss)
  - steven vs Subin An: 101343-88140, margin **+13203** (beats h2, win)
  - steven vs James Y: 69172-59798, margin **+9374** (beats h2, win)
- EcoBot failed the both-stream pass bar. Boatlee and steven beat **both** G5 streams
  (public fertilizer/wheat routes, not V36 satellite clones).
- Follow-up `evaluate_head_to_head` vs current h2 `main.py`, seeds 20260911-20260920,
  both seats (20 games):
  - boatlee: **13-7**, mean margin **+1939**, paired 7-3, Wilson 95 lower 0.433, worst -17840 (seed 20260919 seat 0)
  - steven: **9-11**, mean margin **-2375**, paired 5-5, Wilson 95 lower 0.258, worst -27315
- Upload-eligible: **not uploaded**. G5 gate is passed by boatlee and steven (they
  crush the frozen streams rather than clone h2). Boatlee also leads this 20-game
  H2H slice. Still withheld: uploading a third agent would deactivate the older of
  the newest two and risk dropping live h2 55658542 (2036.2). n=20 is not a medal
  holdout. No clone-gate latch vs h2 was run this step; these are distinct public
  files, not fert_wheat satellite patches.
- Result files: `experiments/candidates/g5_public_routes_20260823.json`,
  per-agent `g5_*.json` and `h2h_vs_h2_20260911_20260920.json`.

## 2026-08-23 16:11 UTC+8 — boatlee_v21_r1 independent H2H vs h2 + Moon (no upload)

- Champion `main.py` left untouched. SHA-256
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
  No Kaggle upload. V36 knobs not retuned. Did not overwrite h2.
- Candidate: `experiments/candidates/boatlee_v21_r1/main.py` SHA-256
  `c6f96a8521dc9aa369b6f27e5b36b9d481e5c1688f50c8ca215c3bb53f1f9eb8`.
  Eval: `scripts/evaluate_head_to_head.py`, 720 steps, both seats.
- Independent H2H vs h2, NEW seeds 20261021-20261030 (20 games):
  **18-0-2**, paired+ **10/10**, mean margin **+3977.6**, worst **-1907**
  (20261025 seat 0), Wilson 95 lower **0.699**.
  JSON: `experiments/20260823_boatlee_v21_r1_vs_h2_20261021_20261030.json`.
- H2H vs Moon (`artifacts/materialized/prvsiyan_moon/main.py`), G3-style seeds
  20260911-20260920 both seats (20 games):
  **13-0-7**, paired+ **7/10**, mean margin **-21.1**, worst **-5427**
  (20260914 seat 0). Fail vs h2 Moon bar (>=16/20 and >=9/10 paired+).
  JSON: `experiments/20260823_boatlee_v21_r1_vs_moon_20260911_20260920.json`.
- 112-behavior public panel: **not run** (Moon slice not strong).
- Route B slot 55698017 (~1782.7 / user 1779): **no**, boatlee is not close
  enough to justify displacing that slot. The new h2 holdout is strong (18-2,
  10/10 paired+), but Moon fails the same G3 bar that blocked Route A, G4 is
  unearned, and a third upload would still deactivate live h2 55658542 (2036.2)
  from newest-2. Do not displace h2.
