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

## 2026-08-23 16:24 UTC+8 — public hunt: Kaito v41 + steven X594 (G5 + Moon)

- Champion main.py left untouched. SHA-256
  65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe.
  No Kaggle upload. V36 knobs not retuned. Did not overwrite h2.
- Kernel search (kaggle kernels list --search kaggriculture --sort-by dateCreated,
  plus kaitofukami / boatlee / prvsiyan / v36 / v37 / v41). Already scored or
  already materialized: boatlee V16/V21, Kaito V36/V37, Moon, Soil, steven
  strongest-farmer, EcoBot, premium-first, tetsutani adaptive. No boatlee after
  V21-R1. Kaito after V36 that was **not** scored: **v41**.
- Skipped as not new playable agents: lejandrofonda/kaggriculture-state-p1-2-2
  (P1.2.2 status sync, dataset copy, no standalone agent);
  denizeryilmaz/v111-8c4s-economic-core-premium-lead (%%writefile of V16-RC5).
- Materialized exact bytes (no Windows CRLF) via notebook literals, not notebook exec:
  - kaitofukami/22-24-unseen-lineages-v41-sparse-closed-loop payload b85+zlib
    experiments/candidates/kaitofukami_v41/main.py 70334 bytes SHA-256
    37b10294c8e7a9dd88355e70f1b67331fe22f112a1b3dbc68de7b3f8931b2380
    (notebook assert).
  - stevenleehans/kaggriculture-x578-i-m-the-strongest emits **X594** raw b85
    experiments/candidates/stevenleehans_x594/main.py 57322 bytes SHA-256
    d946545e01d5a07485ca348c16080b61ecd4f2eff6a8c5fc08be7a449c43abc5
    (notebook EXPECTED_SHA256). Distinct from strongest-farmer 3365ea27....
- Recorded-seat G5 replay-callback (h2: Subin **-7107**, James Y **-8551**):
  - v41 vs Subin An 97399969: 67549-73440, margin **-5891** (beats h2 margin, still loss)
  - v41 vs James Y 95677563: 73963-83175, margin **-9212** (worse than h2) **FAIL**
  - x594 vs Subin An: 47605-29215, margin **+18390** (beats h2, win)
  - x594 vs James Y: 108274-70864, margin **+37410** (beats h2, win)
- x594 passed both G5 streams. Moon H2H vs prvsiyan_moon, seeds 20260911-20260920
  both seats (20 games): **3-0-17**, paired+ **0/10**, mean margin **-10588.4**,
  worst **-26823**. Fail vs h2 Moon bar (>=16/20 and >=9/10 paired+).
- **Moon+G5 survivor: none.** v41 is still a V37-backbone fert-class miss on James Y.
  x594 is another G5-win / Moon-collapse public planner (same shape as boatlee V21
  and steven strongest-farmer). Do not wrap V36. No upload.
- Compact JSON: experiments/candidates/g5_public_new_20260823.json.
- Next concrete hunt (not V36, not fert_wheat wrappers):
  1. G5-screen already-materialized prvsiyan_soil (never scored on Subin/James).
  2. Pull 	etsutani/read-the-town-build-the-farm-kaggriculture only if SHA differs
     from 	etsutani_adaptive.
  3. Inspect xishengfeng/rl-v9-market-off-tape-rulemirror-league and
     ijaikm/kaggriculture-modular-agent-framework for a stdlib main.py.
  4. Search public kernels that claim **both** a 4Q/8-sheep fertilizer-wheat route
     **and** a Moon/melon holdout (the missing intersection).

## 2026-08-23 16:34 UTC+8 — prvsiyan_soil G5 + tetsutani read-the-town (G5 + Moon)

- Champion main.py left untouched. SHA-256
  65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe.
  No Kaggle upload. Did not overwrite h2.
- G5-screen already-materialized prvsiyan_soil
  (rtifacts/materialized/prvsiyan_soil/main.py, SHA-256
  b3c3a68897ba93a411751b75ed7a3ad18da218e7e0e92fbf247b46b4a993e24)
  via recorded-seat replay-callback (h2: Subin **-7107**, James Y **-8551**):
  - soil vs Subin An 97399969: 67729-72165, margin **-4436** (beats h2 margin, still loss)
  - soil vs James Y 95677563: 73873-83242, margin **-9369** (worse than h2) **FAIL**
  - Moon H2H skipped (both-stream G5 bar not met).
- Pulled 	etsutani/read-the-town-build-the-farm-kaggriculture without notebook exec.
  Embedded TOP_AGENT_FILES['main.py'] is 151151 bytes, SHA-256
  73834889054bb6a515fbb40a306a7e0e609105049c781e32197a205f6c339c4f.
  Differs from already-scored tetsutani_adaptive
  (34a54b960a0ebd304d8f3592c334108a6bdf772f164921d3e16380c5dba2ee8, 149042 bytes).
  Materialized LF-only to experiments/candidates/tetsutani_read_the_town/main.py; compile ok.
- Recorded-seat G5:
  - tetsutani vs Subin An: 101190-88745, margin **+12445** (beats h2, win)
  - tetsutani vs James Y: 68100-56322, margin **+11778** (beats h2, win)
- Both G5 streams passed. Moon H2H vs prvsiyan_moon, seeds 20260911-20260920
  both seats (20 games): **0-0-20**, paired+ **0/10**, mean margin **-1056.5**,
  worst **-2865**. Fail vs h2 Moon bar (>=16/20 and >=9/10 paired+).
- Optional kernels inspected, **no stdlib main.py agent emitted**:
  - xishengfeng/rl-v9-market-off-tape-rulemirror-league: torch/numpy PPO trainer;
    RuleMirror comment is a V16-RC5 port. Skipped.
  - vijaikm/kaggriculture-modular-agent-framework: notebook-only (numpy/pandas/
    matplotlib/seaborn) plus an embedded simple baseline string. Skipped.
- **Moon+G5 survivor: none.** Soil is a James fert-class miss (v41 shape).
  tetsutani read-the-town is another G5-win / Moon-collapse public planner
  (same intersection miss as boatlee V21, steven strongest-farmer, and X594;
  Moon loss is narrow, not a blowout). Do not wrap V36. No upload.
- Compact JSON: experiments/candidates/g5_soil_tetsutani_20260823.json.
  Per-stream: experiments/candidates/g5_soil_*.json, g5_tetsutani_rtt_*.json.
  Moon: experiments/20260823_tetsutani_rtt_vs_moon_20260911_20260920.json.

## 2026-08-23 17:10 UTC+8 — medal hunt: public G5 screen + Moon V127 vs boatlee

- Champion `main.py` left untouched. SHA-256
  `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`.
  No Kaggle upload. Did not overwrite h2. V36 knobs not retuned.
- Live snapshot (`kaggle competitions leaderboard -c kaggriculture -d`,
  5952 teams): heralces **rank 528 / 2044.7**. Featured 1000+ medal bars
  used here: gold rank 21 / 2729.1, silver rank 297 / 2246.4, bronze
  rank 595 / 2002.1. h2 submission `55658542` is 2044.7; variant_001
  `55698017` is 1784.5. Bronze is held by ~42 rating / 67 places.
  Analog live scores: boatlee 2494 (rank 106), flexonafft 2342 (224),
  stevenleehans 2314 (242), Amey 2117 (434), tetsutani 2012 (575),
  Kaito Fukami 1882 (818), prvsiyan 1619 (1389).
- destbreso `dissecting-the-top-two`: ranks 1–2 are mutants of the
  public flexonafft/BL-MDgogo multi-route chassis, not the 4Q/8-sheep
  fertilizer class. Winning knob is route-mix bias toward the
  lower-melon / higher-strawberry tape. Flex 3Q tapes still sell ~2932
  fertilizer (h2 sells 216), so the chassis already covers the G5 dump
  without buying SE.
- Static hunt (no notebook exec). New unique stdlib agents materialized
  under `experiments/candidates/`. Duplicates: andrewsokolovsky V22
  payload == boatlee V21 SHA `c6f96a85...`; strongest-farmer rerun
  unchanged; boatlee V20 packed source == flexonafft_rerun SHA
  `8ac34abce1...`.
- G5 recorded-seat vs Subin 97399969 / James Y 95677563 (h2 −7107 / −8551):

  | agent | Subin | James | both-win |
  |---|---:|---:|---|
  | stevenleehans_e284 | +4101 | +39908 | yes |
  | stevenleehans_x544 | +454 | +38250 | yes |
  | prvsiyan_moon_v127 | +13248 | +45193 | yes |
  | flexonafft_rerun | +12445 | +11778 | yes (same banks as tetsutani RTT) |
  | amey_premium_first_rerun | +13248 | +45193 | yes (same margins as Moon V127, different SHA) |
  | tuannm3812_htdc_v12 | −115543 | −106962 | no |
  | v22r2 6c8 / hold | 3000–138821 | 3000–126543 | no (agent idle) |
  | maverickss26_v1 / nekkon | loss | loss | no |

- H2H vs h2, seeds 20260911–20260920 both seats:
  - flexonafft: **4–16**, paired+ 1/10, mean **−5552.7**
  - e284: **6–14**, paired+ 3/10, mean **−44.6**
  - Moon V127: **15–5**, paired+ 8/10, mean **+5735.4**, worst −2981
- Moon V127 independent vs h2, seeds 20261021–20261030: **13–7**,
  paired+ 7/10, mean **+4944.1**, worst −2648. Fails G1 (≥18/20 and
  10/10 paired+). boatlee V21 on the same independent set remains
  **18–2 / 10/10 / +3977.6**.
- Moon V127 vs boatlee V21, seeds 20260911–20260920: **10–10**,
  paired+ 5/10, mean **+1243.6**, worst −566. Locally a coin flip;
  boatlee keeps the only G1-pass vs h2 plus a silver live analog.
- V22-R2 (second-YARN → 6c8 overlay on exact V21) compiled and SHA
  `b43d2eb0...`, but G5 banks stayed at the $3000 open. Overlay is
  closed; do not upload.
- Bundle built only, not submitted:
  `artifacts/submission/boatlee_v21_r1/submission.tar.gz`
  agent SHA `c6f96a85...` (158309 bytes), bundle SHA `d65410a4...`
  (124624 bytes), members `['main.py']`. Matches the V22 notebook's
  V21 `EXPECTED_ARCHIVE_SHA`.
- Compact JSON: `experiments/candidates/g5_hunt_20260823.json` and
  `experiments/candidates/g5_hunt_h2h_20260823.json`.
- **No upload.** Newest-2 would deactivate live h2 55658542 unless a
  second slot is used to re-upload h2 immediately after. Moon V127 is
  the first G5-winner that also beats h2 on both seed sets, but
  prvsiyan live 1619 would risk bronze. Preferred candidate if
  authorized: boatlee V21, then re-upload h2 so both stay active.

## 2026-08-23 17:04 UTC+8 — uploaded boatlee V21 then re-uploaded h2

- User instruction: act as the Kaggle participant; do not wait for a
  per-upload decision. Executed the two-slot plan immediately.
- **Upload 1** boatlee V21-R1:
  - Kaggle submission ID: `55710781`
  - Time: 2026-08-23 09:03:48 UTC
  - Bundle: `artifacts/submission/boatlee_v21_r1/submission.tar.gz`
  - Agent SHA-256: `c6f96a8521dc9aa369b6f27e5b36b9d481e5c1688f50c8ca215c3bb53f1f9eb8`
  - Bundle SHA-256: `d65410a4fc8a31226055e43085131468ac8af5721aabdf3593cb8eade59cabe3`
  - Status at upload: `PENDING`
- **Upload 2** h2 bytes (new submission, does not inherit 55658542 rating):
  - Kaggle submission ID: `55710788`
  - Time: 2026-08-23 09:04:01 UTC (13 seconds later)
  - Bundle: `artifacts/submission/kaito_v36_h2/submission.tar.gz`
  - Agent SHA-256: `65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe`
  - Bundle SHA-256: `049d7cc9c56d99c964f1ee0259e1c0477b4ae511f63611352b5800a143a5d5fc`
  - Status at upload: `PENDING`
- Active newest-2: `55710788` (h2) + `55710781` (boatlee). Inactive:
  variant_001 `55698017` (1784.5) and original h2 `55658542` (2044.7).
- Daily quota after both: 3 remaining. Root `main.py` still h2
  `65e6f5cd...`. Not overwritten with boatlee.
- Rating note: each submission is a new agent. Re-uploading h2 keeps
  the policy in the arena but **does not keep the 2044.7 BT rating**.
  Team score will be provisional while both new agents play. This is
  accepted: the 1784 second slot was wasted, and boatlee's live analog
  is 2494. Do not panic-upload a third agent today.
- Next: poll `55710781` / `55710788` until COMPLETE, then first
  public episodes. No GPU/TPU job in this cycle — still CPU simulator.

## 2026-08-23 20:40 UTC+8 — first live scores after boatlee+h2 pair

- Both new submissions `COMPLETE`. API scores: boatlee `55710781`
  **2115.2**; h2 re-upload `55710788` **1817.9**. Team leaderboard
  (5984 teams): **rank 429 / 2115.2** (was 528 / 2044.7). Medal bars:
  gold 21 / 2727.7, silver 299 / 2243.4, bronze 598 / 1997.9. Silver
  is +128 rating / 130 places. Bronze buffer is now ~117 rating.
- Newest-2 remain boatlee + h2. No third upload. 3 daily slots left,
  unused.
- Boatlee latest 12 public replays: **8-0-4**, mean margin **+208**.
  11/12 are 3Q fertilizer-dump mirrors (our fert 2932–2935). Clone
  latch on 11/12. Losses:
  - radji kraim 97591649 **−8132**: clone, opp 4Q, wheat 1205 vs 856
  - TIM 97603102 **−1828**: clone 3Q, fert 2985 vs 2935
  - Amey Thakur 97605392 **−373**: near-clone, identical 2935/856/4 sheep
  - Black Mamba Farm 97612240 **−19545**: **not clone**, opp fert 311
    wheat 384, 10 sheep vs our 8. New structural miss, not a fert-dump
    loss. Do not retune from n=1.
- h2 re-upload latest 8 public: **5-0-3**, mean **+3616**. Wins include
  fert-heavy opponents (1735 / 1906 / 1906). All three losses are
  near-clone 216-fert / 4-sheep timing (same class as Colton / asi1024).
  1817.9 is a fresh BT climb (old h2 opened at 1842.7); not a regression
  of the policy.
- Compact JSON: `experiments/20260823_live_sample_55710781_55710788.json`.
  Replay binaries stay under gitignored `artifacts/kaggle_runs/`.
- Decision: **hold**. boatlee is already the team score and is above
  the retired 2044.7. Let both agents play. Do not displace boatlee
  with Moon V127 or another public kernel today.

## 2026-08-23 20:55 UTC+8 — boatlee still climbing

- API: boatlee `55710781` **2125.4** (was 2115.2); h2 re-upload
  `55710788` 1818.4 (was 1817.9). Team **rank 416 / 2125.4** of 5990
  (was 429 / 2115.2). Silver bar 299 / 2239.9, gap **+114**. Bronze
  599 / 1998. 56 public episodes on boatlee, 5 new since the 12-game
  sample. No upload.

## 2026-08-23 21:20 UTC+8 — boatlee 2150.5 / rank 388

- API: boatlee `55710781` **2150.5** (was 2125.4, +25.1); h2 re-upload
  `55710788` 1823.1 (was 1818.4). Team **rank 388 / 2150.5** of 5999
  (was 416 / 2125.4). Silver 299 / 2238.6, gap **+88**. Bronze 599 /
  1997. boatlee 64 public episodes. No upload.

## 2026-08-24 — climb slowing, hold

- API: boatlee `55710781` **2163.3** (was 2150.5, +12.8); h2 re-upload
  `55710788` **1802.3** (was 1823.1, down). Team **rank 364 / 2163.3**
  of 6030 (was 388 / 2150.5). Silver bar eased to 301 / **2223.7**,
  gap **+60**. Bronze 603 / 1979.9. boatlee analog still 2492 / rank
  102. Public episode list shows 68 rows (matchmaking cadence down
  from ~10/h early to ~3/h). No new public stdlib agent worth
  swapping. No upload. Let the BT estimate settle.

## 2026-08-24 — first dip: 2163.3 -> 2153.5, hold

- API: boatlee `55710781` **2153.5** (peak this cycle 2163.3, **-9.8**);
  h2 re-upload `55710788` 1799.5. Team **rank 366 / 2153.5** of 6086
  (peak equivalent ~359 at 2163). Silver 304 / 2218.0, gap **+64.5**.
  Bronze 608 / 1987.7. Daily quota 5 remaining. 82 public episodes.
- Newest 12 public replays: **5-1-6**, mean +716. Eight of twelve are
  3Q fertilizer-dump near-clones (fert 2932–2935). Timing losses to
  the same chassis: BorisV −564, Jingxiang −2109, Bruce Zheng −116,
  Liquidus 0, Ignat −3447. One 4Q wheat loss (automatylicza −2916).
  One structural blowout: OceanMix −9800, opp fert 400, not clone
  (same shape as Black Mamba Farm −19545).
- This is the expected BT pullback after leaving the weak-field
  opener, not a runtime failure (all DONE). Do not upload. Do not
  displace 2153. Watch whether the next 12h settles 2130–2160 or
  keeps sliding.

## 2026-08-24 later — still sliding: 2153.5 -> 2137.6

- API: boatlee `55710781` **2137.6**; h2 re-upload 1805.0. Team **rank
  385 / 2137.6** of 6108 (was 366 / 2153.5; peak 2163.3 / ~359).
  Silver 305 / 2212.6, gap **+75**. Bronze 610 / 1983.7. 87 public
  episodes listed. No upload.
- Five newest publics after the dip sample: **0-1-4**. Kaileh57 twice
  (−12982, −9768) and One-For-All (−10844): 3Q, **not clone**, opp
  fertilizer 397–400 / wheat 313–326. Same structural miss as OceanMix
  and Black Mamba Farm. Ayush_Patel clone tie. Pixs −1751 (opp fert
  204). The late-window mix is this low-fert family, which explains
  the second dip. Still above retired h2 2044.7. Hold.

## 2026-08-24 continue — 2137.6 -> 2122.8; low-fert screen

- API: boatlee `55710781` **2122.8**; h2 re-upload 1802.2. Team **rank
  390 / 2122.8** of 6127 (peak 2163.3 / ~359). Silver 306 / 2206.5,
  gap **+84**. Bronze 612 / 1972. Newest-3 publics all losses: Amy Yuan
  −9485 (fert 400, same class), Audric −1922 clone, CoorDi −21 clone.
- Named crushers on the live board: OceanMix **rank 13 / 2820**,
  Black Mamba Farm 145 / 2403, One-For-All 188 / 2341, Kaileh57 353 /
  2156. boatlee the author submitted today and is **907 / 1810** (they
  reset their 2492 agent).
- Pulled `indarkarhana/rank-top10-read-the-market-choose-the-farm`
  (SHA `d39dba50...`) and thunder tape 2948.9 (SHA `18dd8cb9...`).
  Recorded-seat vs OceanMix 98031955 and Kaileh57 98118767:

  | agent | OceanMix | Kaileh57 |
  |---|---:|---:|
  | boatlee V21 (live match) | −9800 | −12982 |
  | h2 | −4831 | **+3331 win** |
  | Moon V127 | −7194 | −9181 |
  | Top10 | −7489 | −6155 |
  | flex | −10424 | −13154 |
  | thunder 2948 tape | −20998 | −21311 |

- Frozen-stream h2 beats Kaileh57 and loses less to OceanMix. No
  pulled public kernel wins OceanMix. Do not upload. Do not displace
  boatlee: 2122 is still the team score and still above 2044. If
  boatlee keeps sliding under ~2050 while new h2 climbs, revisit.

## 2026-08-24 — 2122.8 -> 2117.3; shops v43 uploaded as 55744278

- API: boatlee `55710781` **2117.3** (peak 2163.3, **−46.0**); h2
  re-upload `55710788` **1782.8** (still not climbing). Team **rank
  394 / 2117.3** of 6151. Silver 297 / **2211.5**, gap **+94.2**.
  Bronze 595 / 1978.0. Daily quota before this upload: 5 remaining.
- Newest two boatlee publics after obs3:
  - 98383311 alessandrozonta seat 1: **−7389**, not clone, opp fert
    **400** / wheat 326 vs our 2935 / 856. Same low-fert class.
  - 98447342 Carson Zhang seat 1: **tie 0**, perfect clone (max near
    720, median distance 0, fert 2932/2932).
- Named crushers now: Kaileh57 **rank 8 / 2868**, OceanMix 12 / 2825,
  Black Mamba Farm 156 / 2391, One-For-All 189 / 2339. boatlee the
  author 387 / 2123. Jiachen Li 868 / 1825.8.
- destbreso week-four x-ray (public, not executed): top five are live
  policies; the V21-style clade is a frozen plan plus sell layer; the
  public trail is one generation behind. Matches the live slide.
- Static hunt (no notebook exec), unique stdlib agents:

  | agent | SHA-256 prefix | OceanMix | Kaileh57 | Aless |
  |---|---|---:|---:|---:|
  | h2 | `65e6f5cd` | −4831 | **+3331** | **+3622** |
  | mugundhjb V21 guarder 10C4S | `c12f9704` | −10306 | −12865 | −7523 |
  | EcoBot v4 | `96ab5e6b` | −33317 | −20222 | −33606 |
  | llccqq624 counterbook | `c26402b6` | −10424 | −13154 | −7609 |
  | **llccqq624 shops v43** | `69f06a80` | **+1344** | **+1368** | **+1010** |

- shops v43 is the first public kernel that **wins OceanMix**. G5
  recorded-seat: Subin **+19547**, James Y **+67847**. Closed-loop
  20260911-20260920 both seats:
  - vs boatlee V21: **20-0-0**, paired+ **10/10**, mean **+9796.45**,
    worst **+2456**, Wilson 95 lower **0.839**
  - vs h2: **16-4**, paired+ **8/10**, mean **+6297.6**, worst
    **−6542**. Fails the strict G1 18/20 and 10/10 bar.
- Moon H2H: **not run** this cycle.
- **Upload** shops v43 only. Did **not** re-upload boatlee (that would
  reset the 2117.3 rating, same trap as the h2 re-upload). Did not
  overwrite root `main.py` (still h2 `65e6f5cd...`).
  - Kaggle submission ID: `55744278`
  - Time: 2026-08-24 13:33:39 UTC
  - Bundle: `artifacts/submission/llccqq624_shops/submission.tar.gz`
  - Agent SHA-256: `69f06a802b62aa08f28705dab5728eb924bb6a7c23ffe0164f65b104cc3dadf3`
  - Bundle SHA-256: `fb821a9f9867cd413e40323e1e79f1014b74eac7aab3db2bcdbfc6eea5e36a10`
  - Bundle size: 48105 bytes, members `['main.py']`, compile and
    byte-identity passed
  - Status at upload: `PENDING`
  - Daily quota after: 4 remaining
- Active newest-2: `55744278` (shops) + `55710781` (boatlee 2117.3).
  Inactive: h2 re-upload `55710788` (1782.8), variant_001 `55698017`
  (1784.5), original h2 `55658542` (2044.7).
- Analog risk: Jiachen Li live 1825.8 may be a different submission.
  Team score stays boatlee 2117.3 until shops completes and plays.
  Complementary pair: boatlee covers the V21 clone/fert-dump field;
  shops is the first local winner of the low-fert class that has been
  pulling boatlee down.
- Compact JSON: `experiments/20260824_boatlee_obs4.json`,
  `experiments/candidates/lowfert_screen_b_20260824.json`,
  `experiments/candidates/shops_g5_20260824.json`,
  `experiments/candidates/llccqq624_shops/h2h_vs_boatlee_20260911_20260920.json`,
  `experiments/candidates/llccqq624_shops/h2h_vs_h2_20260911_20260920.json`.
- Next: poll `55744278` until COMPLETE, then first public episodes.
  Do not panic-upload a third agent today. Independent 20261021-30
  and Moon vs shops remain local follow-ups.

## 2026-08-25 — team row is shops 1995.1 / rank 579; hold

- User reported rank 578. Public CSV
  `kaggriculture-publicleaderboard-2026-08-24T16:39:34.csv`:
  **rank 579 / 1995.1** of 6177. Medal bars: gold 21 / 2766.7, silver
  297 / 2213.9, bronze 595 / **1984.6**. Bronze buffer is **10.5
  rating / 16 places**.
- Submissions API (still newest-2 = shops + boatlee):
  - shops `55744278` **1995.1** COMPLETE
  - boatlee `55710781` **2108.4** (was 2117.3)
  - h2 re-upload `55710788` 1782.1 inactive
- The public **team score is shops**, not max(2108.4, 1995.1). Same
  number the user sees. Re-uploading boatlee would reset 2108 and
  would not restore rank 394. Do not do it.
- shops latest 12 publics: **9-0-3**, mean **+5894**, all DONE, all
  3Q, our fertilizer **400** (or 284 twice). Not a clone of V21.

  Wins vs 2932-class dumps: KoRo2_JP +14918, lemon1219 +6804,
  Наталья Скляр +10163, N_Matsumoto24 +11310, SCLim +6168, dk2lone
  +10892. Also beat 4Q 2026-fert (ra5anchor +293, Hồ Tuấn Khôi
  +12498) and a 216-fert (bangqun ZHAO +9118).

  Losses: Dread Development **−6553** (opp fert 2935, V21 dump that
  shops did not always beat); Leifson1337 **−598** (opp fert 338);
  JALKARNA GAUTAM **−4283** (opp fert 302). Two of three losses are
  other low-fert 300–338 tapes.
- boatlee after shops went live: only two more publics, both the
  same miss — 98474778 vs **boatlee** **−11149** (opp fert 400);
  98472503 vs BurntPotato **−5411** (opp fert 400). Then matchmaking
  moved to shops. The author is rank 375 / 2129 and is now the
  400-fert side.
- Jiachen Li live analog fell to 1689 / 1465.6; our shops 1995 is
  already a different, better submission than that analog.
- Decision: **hold**. 9-3 +5894 is a better opener than original h2
  at 1842. Let shops climb. Daily quota today unused. No third
  Agent. Compact JSON: `experiments/20260825_shops_public12.json`,
  `experiments/20260825_boatlee_obs5.json`.

## 2026-08-25 — shops 1995.1 -> 2072.5, rank 579 -> 443; hold

- User reported rank 444. Public CSV
  `kaggriculture-publicleaderboard-2026-08-25T02:25:05.csv`:
  **rank 443 / 2072.5** of 6231. Medal bars: gold 21 / 2733.8, silver
  297 / **2208.2** (gap **+135.7**), bronze 595 / **1971.0** (buffer
  **+101.5 / 152 places**). Above retired h2 2044.7.
- Submissions API: shops `55744278` **2072.5**; boatlee `55710781`
  still **2108.4**; h2 re-upload 1755.2 inactive. Public team row
  remains shops. Newest-2 unchanged. No upload.
- Latest 12 shops publics (98752625–98891557): **5-1-6**, mean
  **+449**, all DONE. The opener's V21-dump diet is thinning; this
  window is mostly other 400-fert clones.

  Still beating 2932-class: Valmorlee +13977 (our 299 vs 2932),
  tellurium_rrr +11693, Alexander Nord +2355.

  Clone/low-fert mixed: Pavlo Ivanin 0 (400/400), Chandramouli +132
  (400/327). Losses: Semyon Epanov −6340 (400/400 clone), Timass
  −7416 (284/304 clone), Umut Keltek −1199 and Mohamed El-Nageeb
  −1258 (400 vs 397 clone), GarrieD −4969 (299/299 clone),
  DOM-VASCONCELOS −9088 after an earlier +7503 vs the same name
  (opp fert 243).
- Analog movement: Jiachen Li is now **rank 31 / 2706.5** (was 1689 /
  1465). They shipped something stronger than the v43 we have. OceanMix
  250 / 2254, Kaileh57 532 / 2012, boatlee the author 325 / 2172.
  Do not chase Jiachen's new private agent from this rank tick.
- Decision: **hold**. 579→443 is the expected BT climb, not a new
  route. Re-uploading boatlee still resets 2108. Daily quota unused.
  Compact JSON: `experiments/20260825_shops_public12b.json`.

## 2026-08-25 — shops 2072.5 -> 2079.9, rank 443 -> 433; hold

- Public CSV `kaggriculture-publicleaderboard-2026-08-25T03:25:17.csv`:
  **rank 433 / 2079.9** of 6235 (was 443 / 2072.5 of 6231). Medal bars:
  gold 21 / 2733.1, silver 297 / **2206.2** (gap **+126.3**), bronze
  595 / **1970.5** (buffer **+109.4 / 162 places**). Still above
  retired h2 2044.7.
- Submissions API: shops `55744278` **2079.9**; boatlee `55710781`
  still **2108.4**; h2 re-upload 1755.2 inactive. Public team row
  remains shops. Newest-2 unchanged. No upload.
- Two new shops publics after 98891557, both DONE, both wins:
  - 98916553 Tien N. seat 1 **+4016**: not clone, opp 4Q fert **1735**
    wheat **1469** vs our 299 / 216, sheep 10 vs 8. Fert-wheat 4Q class
    that original h2 lost (James Y / vladee family).
  - 98909778 ИТМОНИ AI B2B 67 SaaS seat 0 **+8852**: not clone, opp
    fert **2932** wheat 856 vs our 284 / 183. V21 dump still beaten.
- Rolling latest 12 (98772886–98916553): **5-1-6**, mean **+351**, all
  DONE. Same 400-fert clone diet as the prior window; the two new wins
  replaced older dump wins (tellurium +11693, Alexander Nord +2355),
  so the mean eased from +449.
- Analog movement: Jiachen Li **31 / 2700.9** (still a different,
  stronger private agent). OceanMix **45 / 2652.1** (was 250 / 2254).
  Kaileh57 **362 / 2139.5** (was 532 / 2012). boatlee the author
  323 / 2171.6. Do not chase Jiachen from this tick. Frozen-stream
  shops already beat OceanMix; the live analog climb is expected.
- Decision: **hold**. +7.4 rating / +10 places is the expected slow
  BT step, not a new route. Re-uploading boatlee still resets 2108.
  Daily quota unused. Compact JSON:
  `experiments/20260825_shops_public12c.json`,
  `experiments/20260825_shops_public12c_new2.json`.
- Deferred local Moon H2H, seeds 20260911-20260920 both seats, 720
  turns: shops vs Moon V127 **17-0-3**, paired+ **9/10**, mean
  **+6091.15**, worst **-2142**, Wilson 95 lower **0.640**. Losses
  are seed 20260914 seat 0 (−1050) and 20260915 both seats (−2142 /
  −2053). h2 on the same seeds was 16/20, 9/10 paired+, mean ~+4930.
  shops is not Moon-weak like V37 (8/20). This does not authorize a
  third upload. JSON:
  `experiments/candidates/llccqq624_shops/h2h_vs_moon_20260911_20260920.json`.
- Deferred independent shops vs h2, seeds 20261021-20261030 both
  seats: **6-0-14**, paired+ **4/10**, mean **-800.85**, worst
  **-10700**, Wilson 95 lower **0.145**. Opposite of the original
  20260911-20 slice (16-4, 8/10, mean +6298). shops is seed-sensitive
  against h2 and is **not** a general local upgrade. Do not overwrite
  root `main.py`. Do not upload h2 into newest-2: that would drop
  shops 2079.9 or boatlee 2108.4. JSON:
  `experiments/candidates/llccqq624_shops/h2h_vs_h2_20261021_20261030.json`.

## 2026-08-26 — shops 2079.9 -> 2077.6, rank 433 -> 399; hold

- Public CSV `kaggriculture-publicleaderboard-2026-08-26T02:25:29.csv`:
  **rank 399 / 2077.6** of 6372 (was 433 / 2079.9 of 6235). Medal bars:
  gold 21 / 2733.1, silver 297 / **2177.6** (gap **+100.0**), bronze
  595 / **1946.7** (buffer **+130.9 / 196 places**). Score dipped 2.3;
  rank improved because the field grew and the silver bar eased.
- Submissions API: shops `55744278` **2077.6**; boatlee `55710781`
  still **2108.4**; h2 re-upload `55710788` 1729.9 inactive. Public
  team row remains shops. Newest-2 unchanged. Daily quota unused
  (0/5). No upload.
- Latest 12 shops publics (99539249–99703632): **4-2-6**, mean
  **+545**, all DONE. Same 400-fert clone diet as 8/25.

  Wins: ra5anchor +11857 (opp fert 2932, V21 dump), animal crossing
  +5733 (opp 4Q fert 2026 / wheat 1648), sana slama +9401 (opp fert
  240), gnanadeepika karanam +670 (400/400 clone).

  Ties: chaojiwudiwujie 0 (284/284), El Mehdi EL JAIR 0 (400/400).

  Losses are clone timing, not runtime: Nozprod −9358 (400 vs 397),
  Ricky Shao −4498 (284 vs 397), AI After Hours −5059, Thomas
  Tschinkel −1765, Andrey Chankin −307, WeAreFarmers −132.
- Analog movement: Kaileh57 **16 / 2775.0** (was 362 / 2139.5).
  boatlee the author **85 / 2540.0**. Jiachen Li **235 / 2267.6**
  (was 31 / 2700.9). OceanMix **342 / 2136.1** (was 45 / 2652.1).
  Do not chase Kaileh or Jiachen private agents from this tick.
- Decision: **hold**. −2.3 rating is noise on the same 400-fert
  clone mix. Re-uploading boatlee still resets 2108. Compact JSON:
  `experiments/20260826_shops_public12d.json`. Snapshot:
  `artifacts/leaderboard_snapshots/20260826_obs1/`.

## 2026-08-27 — shops slide; open-source hunt; no upload

- Live: shops `55744278` **1993.2**, team **rank 479 / 1993.2** of 6526.
  Latest public-12 **1-1-10**, mean **-5818**. Bronze buffer **+69**.
  Newest-2 unchanged. Quota unused. No upload.
- Strategy change: shops is a failing live slot against 400-fert clones.
  Replacement must win this clone class, not just G5 dumps.
- Open-source sweep (GitHub / X / Hugging Face / Reddit): **no medal-tier
  standalone agent**. Amey GitHub still Premium-First + planner (already
  screened). deepeshumrao and R00tXyz-0 are capstone/exploration wheat
  loops. destbreso public work is analysis (`kagsim`), not a policy.
- New unique Kaggle kernels materialized (no notebook exec). Kaito v43
  sparse-shop SHA `69f06a80...` **is shops v43**. Shop-guard forks
  (reyhanksatria / morinokuma3 / hboyang) share one SHA
  `2fe71189...`.

  Clone blowouts (shops −14190 / −13387 / −9937):

  | agent | prvsiyan | fufu | masa | clone W |
  |---|---:|---:|---:|---:|
  | shops v43 | −14190 | −13387 | −9937 | 0 |
  | Jiachen PQS | −16949 | **+37** | −3084 | 1 |
  | Kaito v48 | −12192 | −4214 | −9937 | 0 |
  | shop_guard v44 | −15031 | −4214 | −9937 | 0 |
  | yamakawanin V21-like | −12697 | −13968 | −3613 | 0 |
  | evelyn scheduler | −138700 | −152326 | −146397 | 0 |
  | lixiuqixiaoke v24 | −16706 | −12625 | −8435 | 0 |
  | Moon V127 | −350 | −9362 | −3989 | 0 |
  | boatlee V21 | −12697 | −14312 | −4022 | 0 |
  | h2 | **+4544** | −2298 | −13104 | 1 |

- G5: v48 and shop_guard both-win (Subin +19584, James +67847, same
  James banks as shops). PQS fails both. yamakawanin both-win (V21
  shape). evelyn fail. v24 James-only.
- **No upload.** None of the new public files 3-0 the clone diet that
  is pulling the team row. PQS is a compressed action/front-run tape,
  not Jiachen's 2294 private agent. v48 is "v44 floor plus two
  fast-climber continuations" and still 0-3 on the live clone sample.
  Replacing shops with v48/PQS/shop_guard would reset 1993 for the
  same failure class.
- Compact JSON: `experiments/candidates/materialize_hunt_20260827.json`,
  `experiments/candidates/clone_screen_20260827.json`,
  `experiments/20260827_shops_public12e.json`.

## 2026-08-27 afternoon — shops 1993.2 -> 1958.8, rank 479 -> 523

- Public CSV `kaggriculture-publicleaderboard-2026-08-27T07:48:35.csv`:
  **rank 523 / 1958.8** of 6552. Medal bars: gold 21 / 2736.7, silver
  297 / 2155.0 (gap **+196**), bronze 595 / **1917.6** (buffer **+41.2
  / 72 places**).
- API: shops `55744278` **1958.8**; boatlee still **2108.4**; h2
  re-upload 1700.0 inactive. Newest-2 unchanged. Quota unused. No
  upload.
- Eight new publics after the morning 1-1-10 window: **0-0-8**, mean
  **-7744**, all DONE. Seven are 400-fert clones; one V21 dump loss
  (gogogo −3783, opp fert 2935). jasonstillchasin −21603 (299 vs 262
  clone). CroDoc −12230, Izzoudine −10636, yjshyfy −9085.
- Rolling latest 12 is **0-1-11**. Same failure class, denser.
  Analog: prvsiyan **130 / 2394** after a 05:44 upload (was 443);
  Kaileh57 **12 / 2797**. Do not chase those private agents.
- Decision: **hold**. No gated replacement. Re-uploading boatlee still
  resets 2108. Compact JSON: `experiments/20260827_shops_public8f.json`.

## 2026-08-28 — shops 1951.1 -> 1916.1, rank 539 -> 560; Moon V189C passes clone/G5/lowfert

- Public CSV `kaggriculture-publicleaderboard-2026-08-28T02:24:08.csv`:
  **rank 560 / 1916.1** of 6663. Bronze 595 / **1898.8** (buffer
  **+17.3 / 35 places**). Silver 297 / 2119.1 (gap +203). API shops
  `55744278` **1916.1**; boatlee still 2108.4. Quota unused. No upload.
- Problem restated: shops is dying to 400-fert clone timing, not to
  missing G5 or low-fert. Public shops-family (v48, shop_guard, PQS)
  failed that class. GitHub/X/HF had no medal-tier agent.
- New public: prvsiyan Moon notebook reran 2026-08-27 21:20 as
  **V189C** SHA `4158d6c803250c3e496c1dbc9bfea1c915c74cb4e4cc1554de99d1fce9e58352`
  (20423 bytes). Not V127 (`a7a6b4f5...`). Notebook live control Moon
  V197 2682.4; prvsiyan team row **27 / 2683.1**.
- Recorded-seat V189C: clone 3-0 (prvsiyan +5964, fufu +6937, masa
  +7511); G5 both-win (Subin +3514, James +51097); lowfert 3-0
  (OceanMix +9651, Kaileh +3567, Aless +15650). First public file that
  beats the diet eating shops **and** the class shops was uploaded for.
- H2H vs shops 20260911-20 both seats: **16-4**, paired+ 8/10, mean
  +7430, worst -8028. JSON:
  `experiments/candidates/prvsiyan_moon_v189c/h2h_vs_shops_20260911_20260920.json`.
- Recommended next: upload V189C so it becomes the team row. Do not
  re-upload boatlee (that would reset 2108 and become newest).

## 2026-08-28 — uploaded Moon V189C as 55832272

- User instruction: submit. Uploaded V189C only.
- Kaggle submission ID: `55832272`
- Time: 2026-08-28 03:15:42 UTC
- Bundle: `artifacts/submission/prvsiyan_moon_v189c/submission.tar.gz`
- Agent SHA-256: `4158d6c803250c3e496c1dbc9bfea1c915c74cb4e4cc1554de99d1fce9e58352`
- Bundle SHA-256: `a1219ee48e04aa0edca4a4bef424e175f4140a9b1bc51f7156852fc09a0bd56a`
- Bundle size: 14914 bytes, members `['main.py']`, compile and
  byte-identity passed. Independent re-extract matched.
- Status at upload: `PENDING`
- Daily quota after: 4 remaining
- Active newest-2 after COMPLETE: `55832272` (V189C) + `55744278`
  (shops 1916.1). Inactive: boatlee `55710781` (2108.4). Did **not**
  re-upload boatlee: that would reset 2108 and steal the team row.
  Root `main.py` still h2 `65e6f5cd...`.
- Team score stays shops 1916.1 until V189C completes and plays. Then
  the public row follows V189C. Analog: prvsiyan 27 / 2683.1.
- Next: poll `55832272` until COMPLETE, then first public episodes.
  Do not panic-upload a second agent today.

## 2026-08-28 — adopted shop-bag mix as team strategy

- User: learn Crop Dusta and crystallize it as our strategy. No upload.
- Playbook: `docs/shop_bag_strategy.md`. North star is Crop Dusta's live
  shop-bag class (3Q, wheat mountain with FM throttle, yarn-count wool,
  hinge dump D29-30). Legal chassis remains Moon V189C `55832272`.
- Inner V189C is a Ramesh 720-step tape (land 150/265, wheat 696, no
  tomato/egg, 8c4s) plus weed repair, 1-turn premium front-run, and a
  **first-shop** Yarn sheep cohort. It is not Crop Dusta. Oldest public
  Moon already branched on yarn in the first three shops; V189C
  narrowed that to `shops[0]`.
- Cut 1 coded, not uploaded: `experiments/candidates/moon_shopbag_v1/`
  SHA-256 `b37fa97f5bf35376ca7afec5509ede98c0ba1d52124106cfe412bfdaae4413a8`
  (20401 bytes). Payload unchanged. Gate is `YARN_STORE in shops`.
  First-unlock yarn = V189C; 2nd-unlock yarn now catches remaining cow
  buys at 150/171/217. Clone screen 3-0 with **zero** margin delta vs
  V189C (those three streams do not expose 2nd-unlock yarn). G5/lowfert
  still required before replacing shops. Do not overwrite root
  `main.py`. Do not re-upload boatlee. Wheat flood / hinge planting
  stay later cuts — they need production, not a market wrap.

## 2026-08-28 — shopbag v1 gates passed; hold (do not replace shops)

- User authorized G5 + lowfert, then a replace-shops decision.
- G5: James **+51097** (delta 0, yarn first); Subin **+17659** vs V189C
  +3514 (yarn 2nd at step 144 — the cut firing). Both DONE.
- Lowfert 3-0, all delta 0: OceanMix +9651 (yarn step 504), Kaileh +3567
  and Aless +15650 (yarn step 288). Last Ramesh cow buy is 217, so those
  bags are too late to convert cows.
- Clone still 3-0, delta 0.
- H2H vs V189C, seeds 20260911-20 both seats: **1-18-1**, mean **0**,
  paired **10/10 zero**, worst **−302**. Not a collapse; almost the same
  agent on this seed slice (yarn-2nd rarely hits).
- Live newest-2: V189C `55832272` **1521.8** COMPLETE (team row);
  shops `55744278` **1901.9**. Uploading shopbag would become newest and
  **reset 1521**, same trap as the h2 re-upload / boatlee. Shopbag is a
  one-line wrap of V189C, not a new class.
- **Hold. Do not upload.** Bundle ready:
  `artifacts/submission/moon_shopbag_v1/submission.tar.gz`
  SHA `2eaeae5eb1e1bcf3449e613b1ce3698604f255cdcce621ba7ab1601ebc573bb0`.
  JSON: `experiments/candidates/moon_shopbag_v1/gates_g5_lowfert.json`,
  `h2h_vs_v189c_20260911_20260920.json`. Revisit if V189C slides on
  yarn-second opponents, and only with an explicit submit.

## 2026-08-28 — uploaded moon_shopbag_v1 as 55840543

- User instruction: submit now. Uploaded shopbag only.
- Kaggle submission ID: `55840543`
- Time: 2026-08-28 09:22:09 UTC
- Bundle: `artifacts/submission/moon_shopbag_v1/submission.tar.gz`
- Agent SHA-256: `b37fa97f5bf35376ca7afec5509ede98c0ba1d52124106cfe412bfdaae4413a8`
- Bundle SHA-256: `2eaeae5eb1e1bcf3449e613b1ce3698604f255cdcce621ba7ab1601ebc573bb0`
- Bundle size: 14910 bytes, members `['main.py']`, compile and
  byte-identity passed. Independent re-extract matched.
- Status at upload: `PENDING`
- Daily quota after: 3 remaining
- Active newest-2 after COMPLETE: `55840543` (shopbag) + `55832272`
  (V189C 1521.8). Inactive: shops `55744278` (1901.9). Did **not**
  re-upload boatlee. Root `main.py` still h2 `65e6f5cd...`.
- Team row follows newest: stays V189C 1521.8 until shopbag completes
  and plays, then follows shopbag. V189C remains the second live slot.
- Next: poll `55840543` until COMPLETE, then first public episodes.
  Do not panic-upload another agent today.

## 2026-08-29 — shopbag 2771.0 / rank 15; hold

- User asked to look at rank. Public CSV
  `kaggriculture-publicleaderboard-2026-08-29T00:41:00.csv`:
  **rank 15 / 2771.0** of 6789. Gold 21 / **2740.2** (buffer **+30.8 /
  6 places**). Silver 297 / 2100.7. Bronze 595 / 1885.4.
- API: shopbag `55840543` **2771.0** COMPLETE (team row, newest);
  V189C `55832272` **1558.6**; shops `55744278` 1901.9 inactive.
  Newest-2 unchanged. Quota unused today. No upload.
- Last sub time on the row is shopbag 2026-08-28 09:22. Analog:
  Crop Dusta 2 / 3013; prvsiyan 190 / 2248.9; boatlee the author
  147 / 2321.8; Kaileh57 35 / 2625.4.
- Decision: **hold**. 1521 → 2771 is the expected BT climb of the
  yarn-in-bag wrap, not a reason to spend another slot. Snapshot:
  `artifacts/leaderboard_snapshots/20260829_obs1/`.

## 2026-08-29 — shopbag win/loss autopsy; v2 wheat FR coded, not uploaded

- Shopbag `55840543` public metadata: **86 games, 65-2-19**, mean
  **+8919**. Score 2764.8. Rank 15 of 6789.
- 16-replay autopsy `experiments/20260829_shopbag_public_autopsy.json`.
  Our requested sells are a **constant Ramesh tape**: wheat **696**,
  fert **561**, melon **85**, strawberry **362**, milk **478**, tomato 0,
  egg 0, carrot 20. Shed leftover wheat is **0–3** — there is no extra
  wheat to dump. Wool is the only wrap-variable (239 vs 335).
- Why we win:
  - TK256 `101864457` **+16291**, clone, yarn **2nd at 144**: extra sheep
    7 vs 4. This is cut 1 working.
  - Ryo Hasegawa `102083141` **+15193**. Ryo sold 366 wheat / 189 fert;
    our premium tape beat live-five #4 without a wheat mountain.
  - QQ Farming `102058617` **+8236** with yarn at 216 (one leftover cow).
- Why we lose (three classes):
  1. **Self-clone coin-flip**: TK256 `102114403` **−125**, identical
     696/561/239/362/478, yarn too late. Kenjo −1273, Semyon −2130.
  2. **10–11 sheep herds** even when we yarn-swap to 8: smsxgz −19727,
     Collin −13683, Carson −9986, ITMO −11173, Hanserong −14707.
  3. **Wheat mountain**: Collin sold **1742** wheat vs our 696.
- Crop Dusta 8/28 newest 8 (`experiments/20260829_crop_dusta_public8.json`):
  still wheat **724–2910**, fert 136–215, mixed vs new #1 Milan Leonard.
  Confirms the production gap is live, not stale.
- Cut 2/3 (throttle, hinge hold) **closed**: nothing in the shed, tape
  has no tomato/egg. Next score jump is a wheat-mountain public file,
  not another empty wrap.
- `moon_shopbag_v2`: add `WHEAT` to the 1-turn front-run. Frozen TK256
  −125 → **+59 win (+184)**. Ryo still +15184. prvsiyan clone still
  +5966. Collin still −13720. **Not uploaded** (would reset 2771).

## 2026-08-29 — rank 15 -> 20; 11-sheep clones, not Milan

- Public CSV `2026-08-29T15:20:40`: **rank 20 / 2737.0** of 6857.
  Gold 21 / 2723.9 (buffer **+13.1 / 1 place**). Rank 10 One Zero001
  2806.1 (gap **+69**). API shopbag `55840543` **2737.0**; V189C 1610.3.
- Full public 105 games **71-3-31**, mean +6929. Rolling latest 12:
  **3-0-9**, mean **−4120**. Same shape as shops' death window.
- New blowouts are **10–11 sheep near-clones of our tape**, wheat
  ~328–369 (not Crop Dusta 1700+): MtN −17420 (11 sheep), Yusuke
  −13434 (10 sheep, yarn-2nd already fired, we had 7), vkhydras −7015
  (11), lucaskna −11389 (10). Yarn extra sheep does not beat this band.
- Hunt (no notebook exec): salemali7 `kaggriculture-2900` is Boatlee
  V16-RC5 SHA `f029fa0c...` — reject. EcoBot v7 SHA `ac4058f7...`
  unique vs v4, then 0-5 on MtN/Yusuke/Hanserong/Collin/prvsiyan
  (margins −55k to −117k) — reject. nagatakengo V3.8 is a depth-3
  tree — reject. GitHub still no medal-tier standalone agent.
- **Hold. Do not upload v2.** JSON:
  `experiments/20260829_top10_gap.json`. Next chassis must 2/3-flip
  MtN/Yusuke/Hanserong, not another Ramesh wrap.

## 2026-08-30 — rank 26 / 2684.8, below gold; E776 better but not enough

- Public CSV `2026-08-30T01:28:31`: **rank 26 / 2684.8** of 6889.
  Gold 21 / 2736.8 (**−52**). Rank 10 Ryo 2811 (gap **+126**). Top 5:
  Crop Dusta 3030.6, Milan 3024.7, **Yusuke 2923.8**, **MtN 2892.1**,
  Subramanya 2885.5. The 11-sheep clones that beat us are now 3rd/4th.
- Shopbag public 123 games **74-4-45**, mean +5405. Rolling 12:
  **1-1-10**, mean **−3536**. Latest: Pavlo −8317/−11217 (clone, 6–8
  sheep, wheat ~370), One-For-All −2215, Michael Timbs −8220. One
  smsxgz **+8490** (same name as the −19727).
- Hunt: `indarkarhana` E776 (shop-conditioned extra pasture animal)
  vs frozen losses: Pavlo **+86** (flip), clone +9253, but MtN −14407,
  Yusuke −10750, Hanserong −13138. Better than shopbag, **not 2/3
  flips**. skomuro silver tape SHA `8d7d10be...` worse on Pavlo.
  GitHub still capstone-only. Rafif PPO notebook not a one-file agent.
- **Hold. Do not upload E776 or v2.** Resetting 2684 for an agent that
  still loses to rank 3–4 does not make top 10. JSON:
  `experiments/20260830_top10_gap.json`.

## 2026-08-30 later — rank 26 -> 37 / 2629

- CSV `2026-08-30T07:02:25`: **rank 37 / 2629.0** of 6913. Gold 21 /
  2719.6 (**−91**). Rank 10 Jiro2 2803.6 (gap **+175**). Shopbag
  `55840543` **2629.0**. Public 149 games **80-4-65**. Rolling 12:
  **2-0-10**, mean **−4722**. Latest: Hanserong −7058, nir afek −8889,
  Tom3 −11058, chupaletas −9446, Ryo Takaki −9717/−1824, Kenjo −6198.
  Lynxx +9240 / +1946 are the only recent wins.
- Same 10–11-sheep clone band, denser. No new chassis that 2/3-flips
  MtN/Yusuke/Hanserong. **Hold.** Do not reset 2629 with v2 or E776.

## 2026-08-30 evening — rank 42 / 2628.9; rolling 12 all clones

- CSV `2026-08-30T08:33:35`: **rank 42 / 2628.9** of 6919. Gold 21 /
  2726.8 (**−98**). Rank 10 Jiro2 2801.3 (gap **+172**). Top: Crop Dusta
  3033.7, Milan 3024.3, Yusuke 2929.6, tiki 2885.0, MtN 2876.2. Shopbag
  `55840543` still newest/team. Public 153 **82-4-67** mean +3474.
  Rolling 12 **3-9**, mean **−4912**, **all 12 clone=true**.
- Wins: Munal +7295 (8c4s vs 6c6s), nir afek +1744 (8c4s vs 11c4s),
  Lynxx +9240 (yarn 4c8s vs 9c6s). Losses split in two: no-yarn extra
  cow (Hanserong/Remielle/Ryo Takaki, we 8c4s they 7–11c, pastures
  14 vs 17) and yarn 10-sheep (Tom3 4c10s 17 pastures vs our 4c8s 14).
- Sheep window: we already buy 1 sheep at 218; cash 347–474 so we cannot
  add more there. Yusuke/MtN/Hanserong add 4–5 more at 218–266 and build
  17 pastures. Our tape has a serviced empty pasture at `(7,4)` and
  hand 4 PASS at the shed 255–262.
- Hunt: Yusuke notebook is **not** submitted CR2. Extracted two-shop
  demo SHA `ac615297...`. Screen 0-4-1: MtN −9019, Yusuke tie, Hanserong
  −4677, clone **−8108**. Method is right (route library on first two
  shops); published 10-history demo is not. destbreso/nikital7 C++ is
  4k–24k eps/s search infra. evelyn v27 / bina v31 / mansi 550 /
  songoku greedy / GitHub capstones rejected. Kenjo public
  `102125420` is the 11-sheep specialist (5c11s, 17 pastures, extra
  sheep 218/223/242/250/266, land 151/266 — same land tape as us).
- Cut 7 `moon_shopbag_v3` SHA `8f83bbc3...`: one extra shop-aligned
  animal into `(7,4)`. Clone 3-0 identical. Fired once (Yusuke +3138);
  other panel games delta 0 because 223 PLACE already filled the tile.
  **Not uploaded.**
- **Hold.** Do not reset 2629 with v2, v3, E776, or the Yusuke demo.
  Next gated chassis: shopbag default + Kenjo `102125420` as the yarn
  specialist, not a single Kenjo tape. JSON:
  `experiments/20260830b_top10_gap.json`.

## 2026-08-30 — user said 提交; v4 gated, not uploaded

- User instruction: submit. No already-gated candidate existed (v2/v3/
  Yusuke demo/E776 all fail 2/3 or clone). Built cut 8
  `moon_shopbag_v4` instead of resetting 2629 with a no-op.
- Shopbag 0–71 == Kenjo `102125420` 0–71. First shop yarn → Kenjo
  remainder (5c11s, 17 pastures). Else shopbag v1 (yarn-2nd wrap kept).
- Clone 3-0 identical (those games are not first-yarn). Hanserong
  11-sheep **+3879 flip** (+18586 vs live). MtN **−759** (+16661, still
  a loss). Yusuke yarn-2nd identical −13434. Rolling-12 Hanserong clone
  (brunch first) identical −11247.
- 1/3 flips on MtN/Yusuke/Hanserong. Current rolling 12 is mostly
  no-first-yarn clones, so uploading v4 would reset 2628.9 and then lose
  the same band. SHA after docstring
  `5dc4dccf78f840bbd5a46bb2b5e7274f44edde281b52a86dc83885426dab78d8`.

## 2026-08-30 — uploaded moon_shopbag_v4 as 55887331 (user: 提交 anyway)

- User override: submit anyway. G5 both-win DONE before upload: Subin
  +17659, James +51097 (identical to shopbag). Clone 3-0 already held.
- Kaggle submission ID: `55887331`
- Time: 2026-08-30 09:34:49 UTC
- Bundle: `artifacts/submission/moon_shopbag_v4/submission.tar.gz`
- Agent SHA-256: `5dc4dccf78f840bbd5a46bb2b5e7274f44edde281b52a86dc83885426dab78d8`
- Bundle SHA-256: `5cbecbf7d2bcc3f6d55a936d14e994790c8b720f3ab7e524b3aaf686d68f08c1`
- Bundle size: 24824 bytes, members `['main.py']`, compile and
  byte-identity passed.
- Status at upload: `PENDING`. Daily quota remaining: 4.
- Newest-2 after COMPLETE: v4 `55887331` + shopbag `55840543` (2628.9).
  V189C `55832272` drops off. Did **not** re-upload boatlee. Root
  `main.py` still h2 `65e6f5cd...`.
- Team row follows newest: stays shopbag 2628.9 until v4 completes and
  plays, then follows v4 (expected reset while it climbs).
- Known: Hanserong first-yarn **+3879**; MtN still −759; yarn-second and
  no-yarn clone band unchanged.

## 2026-08-31 — v4 1968; rolling-12 is non-yarn extra-animal clones; v5 gated

- CSV `2026-08-31T03:51:56`: heralces **rank 67 / 2552.1** of 7007
  (matches shopbag; LastSubmissionDate is v4). Gold 21 / 2713. Rank 10
  Kenjo 2774.7. Top: A Poor Vul 2914.9, Yusuke 2888.7, tiki 2888.1,
  MtN 2856.0. Crop Dusta 61 / 2580. v4 API **1968.0** COMPLETE, 78
  public **55-2-21** mean +11013. Rolling 12 **4-2-6**.
- v4 autopsy (12 newest): every loss and both ties are `kenjo=0
  clone=1` — first shop is not yarn, we stay 8c4s/14 pastures, they add
  animals and sometimes 17–18 pastures. Wins: first-yarn Kenjo vs TK256
  5c11s **+16611**; yarn-second shopbag wrap vs TK256 **+17159**.
- Hunt: evelyn v8 is old Blu3s tape+RC5; dodoshark melon-greedy 8c5s;
  sifi unrelated; destbreso "instrument for agent selection" is the
  funnel (filter/dedupe/screen/judge vs the fielded agent on its real
  matchups). No public A Poor Vul kernel. GitHub still capstone-only.
  Prescribe-then-Select (arXiv 2509.08194) is the same idea as Yusuke:
  keep several complete plans, pick by context.
- Cut 9 `moon_shopbag_v5` SHA `e254dd7d...`: non-yarn first shop plays
  Kenjo extra-cow `102078489` (prefix 0–71 identical). Clone 3-0
  **better**. Live-loss 3/5 flips (Plant City +6222, Fernando +1091,
  Liquidus +1546). 3정훈/satoooh closer but still L. Yarn first-shop
  unchanged. Yarn-2nd TK256 **+25093**. G5 Subin +21203 James +25514
  both win. **Hold. Do not upload** until user says 提交. JSON:
  `experiments/20260831_v4_autopsy.json`.


## 2026-08-28 — Crop Dusta public-12 strategy (learn, do not clone)

- User asked to study first-place Crop Dusta games. No upload.
- Live snapshot `20260828_obs2`: Crop Dusta **rank 1 / 3006.4**
  (rishigottumukkala, last sub 2026-08-28 01:26). destbreso week-four
  x-ray (cell 24, not executed) had them #3 as a live "supply shocker"
  (~1,900 wheat, peak days 10-19) plus the biggest hinge harvester
  (tomato / carrot / egg). That card still matches.
- GitHub pointer `FelixAllistar/PufferLib` commit `8aa699e` is a BC
  import pipeline over official `kaggle/kaggriculture-episodes-DATE`
  zips (`--agent "Crop Dusta"`). Replays are not in the repo. Useful
  only as confirmation of the same daily-zip source; it is not Crop
  Dusta source and must not be submitted as a tape.
- Source used here: official `kaggriculture-episodes-2026-08-27` zip
  (~545 MB). 36 Crop Dusta hits / 696 episodes; analyzed the newest
  12 publics (11 vs Ryo Hasegawa, 1 vs Subramanya N). Compact JSON
  `experiments/20260828_crop_dusta_public12.json`; strategy JSON
  `experiments/20260828_crop_dusta_strategy.json`.
- Record: **10-2**, mean **+7976**, all DONE, none clone (max near 3-5,
  median distance 17-35). Losses: 101012944 Ryo **−6020** (160k/154k
  strawberry-milk shop bag) and 101126945 Ryo **−4679**. destbreso
  week-four Ryo-vs-Crop-Dusta was 4-2 the other way; this later sample
  is Crop Dusta winning the hard summit matchup.
- Live, not a 720-turn tape: 12 unique full action hashes. Opening is
  frozen: **1 unique h24** (all 12), **2 unique h100** (11 share one
  prefix). Then sheep 0-8, cows 0-13, wheat 711-2695 diverge.
- Always **3Q**, always **2× BUY_LAND** at steps **122 and 200**
  (one game 122/225). destbreso: NW, NE ~day 6, SW ~day 10. Never SE.
  Always 12 hands. Fertilizer sold **119-269** (mean 202), not V21
  2932. Melon board always 0, but SELL:MELON **90-109**: two harvest
  pulses (mean D11 ~30, D17 ~56), ~18-20 melon seeds every game.
- Wheat flood (the card): mean **1828** vs opponent **317**. Volume
  sits near 0 until D11, then **159-176/day D12-15**, then eases.
  Wheat glut uses the log above-target, so the flood is a cash engine
  rather than a price crash. Not Flex/V21.
- Shop-conditioned mix (the hinge harvest), measured on this 12:

  | shop count | mean sell |
  |---|---:|
  | yarn 0/1/2/3 → wool | 84 / 137 / 246 / 355 (r **0.893**) |
  | pet cafe 0/1/2 → carrot | 6 / 40 / 100 (r **0.694**) |
  | bakery 0/1/2 → egg | 8 / 8 / 81 (r **0.582**) |
  | pizza 0/1/2 → tomato | 0 / 39 / 57 (r **0.578**) |
  | farmers market 0/1/2/4 → wheat | 1838 / 2204 / 1929 / **711** (r **−0.46**) |

  Tomato/carrot dumps are almost all **D29-30**. Eggs drip from ~D12
  then dump D30. Strawberry (127-312) and milk (104-309) are always
  on; ice-cream/smoothie counts move them only weakly. When wheat
  demand is already high (4× farmers market), they throttle the flood
  instead of glutting into a drained market — and still won +8549.
- Loss 101012944: 3 ice cream + 2 smoothie, zero pizza/pet-cafe/FM.
  Crop Dusta planted 47 strawberry (high) and sold 312 strawberry /
  309 milk; Ryo sold 328 / 317 of the same goods. Wheat 1819 did not
  cover a same-route premium duel at 160k. Loss 101126945: they did
  harvest tomato 117 and egg 38; Ryo still printed more strawberry
  and milk. Summit losses are premium-timing, not a broken flood.
- Contrast with our public files: V21/boatlee is 2932 fert + clone
  diet. shops v43 is 400-fert clones and died to them. Moon V189C
  already reads `unlocked_shops` but only branches when
  `shops[0]=="YARN_STORE"` (first-Yarn sheep cohort). Crop Dusta
  conditions on the **whole bag and counts**, holds hinge goods to
  terminal, and throttles wheat when town already drains it.
- Learnable: live policy with a short frozen opening; 3Q land tape
  at 122/200; wheat mountain D11-19 with FM throttle; yarn-count
  wool scale; pet-cafe carrots / bakery eggs / pizza tomatoes held
  until D29-30; melon pulse not a leftover plant. Closest public
  handle is Moon's yarn gate, not a Crop Dusta file (none exists).
- Not copyable / not a next upload: no Crop Dusta source; do not BC
  a 12-game average into a 720-turn tape; do not copy Flex/V21 2932;
  do not buy SE to chase 4Q fert-wheat; do not displace V189C with
  an untested wheat-flood fork; do not re-upload boatlee. A later
  gated experiment, if any, would widen Moon's first-Yarn test to
  shop-bag counts — only after clone/G5/lowfert still pass.

## 2026-09-01 — rank 214 / 2382; Fieldbook gated; tetsuya is a different class

- CSV `2026-09-01T13:35:44`: heralces **rank 214 / 2382.3** of 7173
  (shopbag `55840543`). Gold 21 / 2712.3 (**−330**). Rank 10 Mc10nys0n
  2775.2 (gap **+393**). v4 `55887331` **1927.0**. Top: tetsuya 2940,
  OceanMix 2885.7, Crop Dusta 2878.6, Driz Lo 2840.8, QQ Farming 2839.4.
  Yusuke 86 / 2548.5. Milan 959 / 1748.
- Shopbag public 250 **103-4-143**, mean **+261**. Rolling 12 **3-9**,
  mean **−4281**. v4 public 117 **70-2-45**, rolling 12 **5-7**.
- Rolling-12 autopsy: still `kenjo=0 clone=1`. The opponents are not
  Crop Dusta wheat mountains. They are **Fieldbook-class Kenjo tapes**:
  9c5s 17 pastures wheat **380** wool **138** fert **326** melon **72**
  (BALANCED) or 6c11s wheat **358** wool **285** (YARN_ENGINE). Our
  8c4s/14 pastures/696 wheat is the dying diet inside that band.
- destbreso field guide (no cell exec): a medal agent is a tape plus a
  thin rim; the recording is worth more than the layer; 1-step SELL
  lead is the smallest live adaptation; fertilizer drain is zero;
  carrot/tomato/egg still climb; field half-life **2.1 days**. Macro
  x-ray: leaders piled tomato/carrot then already rotated.
- 08-31 daily zip sample of the current top:
  - **tetsuya**: not Kenjo. Land **169/241**, never clone in the four
    games, mixed 4c11s / 9c5s / geese, wheat 402–509, fert 528–624.
    Beat Kenjo1209 **+20075** and MtN 9c5s by **28472**. No kernel.
  - **Crop Dusta**: still 3Q at **122/199**, wheat **338–2112**, carrot
    26–234, egg 0–112. Wins with the flood; loses to Hanserong/xi luo
    when throttled. No source.
  - Kaileh / QQ / Driz / Yusuke / MtN: Kenjo/Fieldbook 151/266, melon
    72, 9c5s or 6c11s or Yusuke **8c9s** (YARN_LATE). Clone=true.
  - OceanMix #2 submitted 09-01 00:01; not in the 08-31 zip. Old
    low-fert `98031955` is a different agent.
- Hunt: Yusuke **Fieldbook: Commit for Three Days** is the cleaned
  six-route ShopForge study (not the Aug-30 10-history demo that
  destroyed clone). Shared opening 0–143, branch day 6 (first two
  shops + cash/land gap) and day 9 (third shop). farming-score v5 is
  E776 Kenjo+Niklita. flexonafft AFI is a Flex archive. Strategic
  Decision-Making is beginner pathfinding. destbreso/motemen are infra.
- Cut 10 `yusuke_fieldbook` SHA
  `de668f7f72a552640fe0e615fff937990596a47cbe95ba6f6f3992d3fcba3ae8`
  (331,060 bytes). Static assemble of notebook `fieldbook_logic.py` +
  dataset tapes. Clone **3-0**. G5 Subin **+31494** James **+25530**.
  MtN/Yusuke/Hanserong **3/3 flips** (+2044 / +18016 / +11446). Panel
  **12/13**; only satoooh still L (−411). Rolling-12 sample **4/6**
  (Bandito −17060 → +919; Zhongyi −12940 → +11924). Mostafa −443 and
  l1aF −574 are Fieldbook-vs-Fieldbook coin-flips. Beats v5 on every
  gated stream except smaller prvsiyan/fufu clone margins.
- **Hold. Do not upload.** User did not say 提交. Uploading drops
  shopbag 2382.3 from newest-2 unless we re-upload it as the second
  slot (drop dying v4 1927). Do not upload v5; Fieldbook supersedes it.
  Do not upload v2 (Fieldbook sell-lead explicitly skips wheat/fert).
  Do not BC Crop Dusta. Do not submit the Aug-30 Yusuke demo.
- JSON: `experiments/20260901_top10_gap.json`,
  `experiments/20260901_fieldbook_tapes.json`,
  `experiments/20260901_rolling12_autopsy.json`,
  `experiments/candidates/yusuke_fieldbook/screen.json`.

## 2026-09-02 — uploaded Fieldbook 55962758 + shopbag reupload 55962761

- User: 按建议方案提交. Cut 10 Fieldbook plus shopbag reupload so newest-2
  is Fieldbook + yarn-wrap, not Fieldbook + dying v4.
- Preflight: Fieldbook SHA-256
  `de668f7f72a552640fe0e615fff937990596a47cbe95ba6f6f3992d3fcba3ae8`,
  331060 bytes, LF only, 6 routes × 719, `agent` callable. Bundle
  `artifacts/submission/yusuke_fieldbook/submission.tar.gz` 53616 bytes,
  SHA-256 `2fd2dfe1120ec619d7bd9ca0ab950af31087d16a0f586044ce6771263f24e026`,
  members `['main.py']`, compile and independent re-extract byte-identity
  passed. Shopbag tar.gz SHA-256 `2eaeae5e...` still matches original
  `55840543` agent `b37fa97f...`.
- At upload, live scores had already slid: shopbag `55840543` **1983.7**,
  v4 `55887331` **1848.4**. The 2382 floor was already gone.
- Kaggle submission IDs:
  - Fieldbook `55962758` at 2026-09-02 13:59:09 UTC
  - shopbag reupload `55962761` at 2026-09-02 13:59:21 UTC
- Both PENDING. Daily quota remaining: 3.
- Newest-2 after COMPLETE: `55962761` + `55962758`. v4 `55887331` and
  original shopbag `55840543` drop. Did **not** re-upload boatlee. Root
  `main.py` still h2 `65e6f5cd...`.
- Team row will reset while both climb. Fieldbook is the chassis;
  shopbag is the yarn-wrap partner, not a score floor.

## 2026-09-03 — Fieldbook 2071; freeze-after-day-9 deaths; six-day gated

- CSV `2026-09-03T12:56:48`: heralces **rank 650 / 2071.0** of 7476
  (Fieldbook). Gold 21 / 2846.7 (**−776**). Rank 10 lilishyxf 2904.5.
  Top: Giulio Ravasio 2969, Crop Dusta 2961, Knight of Favonius 2953,
  sbol ball 2947, 3정훈 2932. Yusuke 13 / 2884.1 (new sub 09-03 06:27).
  tetsuya 179 / 2568. Shopbag reupload `55962761` **1688.5**.
- Fieldbook public 210 **90-31-89**, mean +2766. Rolling 12 **2-3-7**,
  mean **−8852**. Autopsy `experiments/20260903_fieldbook_rolling12.json`:
  all 12 `clone=true`, land 151/266, 17 pastures, melon 72.
  - Ties: exact BALANCED 9c5s 380/138/326 (kwa, Kifine, shenjj02).
  - Yarn-2nd 6c11s coin-flip LKQ669 **−11**.
  - PET_CAFE-first we stay 9c5s; they play **8c9s** (Kaggle chan
    **−42826**, Peter Parker **−23363**).
  - Same 9c5s, heavier wheat tail: 没落者 432 vs 387 **−19546**; gogogo
    419 vs 387 **−37175**.
- Cut 10 freezes after day 9. The field now reselects later blocks.
- Hunt (no cell exec): `yhay81/six-day-public-state-fieldbook` + dataset
  `yhay81/six-day-public-state-agent-source`. Five 144-turn blocks,
  reselect at 144/288/432/576, trees on carrot/tomato/milk/strawberry/
  wool/fert prices, cash_gap, weed geometry. 8 tapes, 30 paths, Bantam
  and Zenith Ye donors. Frozen 24064 games point rate **0.9485**.
  Submission is `main.py` + Linux `agent.so`. **Hold. Do not upload.**
  Three-Day Shop Router is a step-360 patch on that C++ chassis.
  boatlee V29 is premium-hysteresis Flex lineage — reject.
- Cut 11 named, not assembled locally (needs g++ -shared). v5 stays
  superseded. Root `main.py` still h2. No new Kaggle upload.
- JSON: `experiments/20260903_top10_gap.json`,
  `experiments/20260903_fieldbook_rolling12.json`.

## 2026-09-04 — Giulio/Knight/sbol measured; still freeze-after-day-9; six-day Hold

- CSV `2026-09-04T04:01:32`: heralces **rank 808 / 1946.5** of 7546
  (Fieldbook `55962758`). Gold 21 / 2827.0 (**−880**). Rank 10 sbol ball
  2873.5. Top: Crop Dusta 3021.1, Giulio Ravasio 2956.4, Jesse Bullard
  2942.9, Knight of Favonius 2940.8, AI是我的豆包 2919.1. Yusuke 40 /
  2761.9 (sub `55975994`). tetsuya 247 / 2485.7. Shopbag reupload
  `55962761` public 166 **73-3-90**. No new Kaggle upload; user did not
  say 提交.
- Official daily zip `kaggle/kaggriculture-episodes-2026-09-03` is the
  newest complete day on the index (updated 09-04 00:08). Downloaded
  `artifacts/kaggle_runs/episodes_20260903/kaggriculture-episodes-2026-09-03.zip`
  (538,048,136 bytes). Newest Fieldbook/top-board publics are 09-04
  02:28–04:00 UTC, so those rows use official
  `kaggleusercontent.com/episodes/{id}.json` listed by EpisodeService
  from each team's public leaderboard submission. Hunt log: scratch
  `hunt.log`.
- Fieldbook public 315 **116-51-148**, mean **+1051**. Rolling 12
  **2-2-8**, mean **−2161**. Autopsy
  `experiments/20260904_fieldbook_rolling12.json`: land 151/266, 17
  pastures, melon 72 on our seat.
  - Ties: exact YARN_ENGINE 6c11s (mimi, rhythm master) 357–358 / 285.
  - Later 9c9s vs frozen BALANCED 9c5s (datnt114, yasu, Kaggriculture
    Agent).
  - Knight-class dump on a clone latch: chocolat wheat 2386 melon 2074
    fert 1554.
  - Non-clone goose: Chiranjieev 7c5s+2g **−20786**.
  - Heavier wheat tail: Liquidus 434 vs 391; Ryutaro 434 vs 377.
  Loss class: still freeze-after-day-9 vs later 9c9s / heavier wheat
  tails, not a new Fieldbook tape.
- Summit facts from newest 4 publics each (not copied from 09-01
  tetsuya/Crop Dusta 122/199 rows):
  - **Giulio Ravasio**: land **151/266**, clone=true, 9c5s wheat
    **406–414** fert 333 melon 72; one 7c5s+2g. Not tetsuya 169/241.
  - **Knight of Favonius**: land 151/266, wheat **1391–1888**, melon
    **1071–1075**, fert **1468–1554**, carrot/egg/tomato ~1000. Mixed
    clone. Beat Crop Dusta +2505 with geese; lost −21527 without.
  - **sbol ball**: land 151/266 clone=true, shop-routed **6c11s / 7c6s /
    4c14s / 9c5s**, wheat 360–448 melon 72.
  - **Crop Dusta** (newer publics): land **122/200–201**, clone=false,
    wheat **1556–2561**, geese 0–7. Still the mountain.
  - **Yusuke Hayashi** live: **9c9s in all four games** even when first
    shop is BAKERY or SMOOTHIE. Three-day Fieldbook cannot reselect that
    late.
- Hunt (no cell exec, `_hunt_20260904/`): six-day remains the only
  public later-block reselect chassis. anasriaz and degnonguidi
  republish the three-day C++ router. reyhanksatria v2 is an opaque
  zlib payload. pilkwang is Kaito v58. salemali7 is V16-RC5 8c4s.
  **Hold. Do not upload** six-day: C++ `agent.so`, no Windows clone/G5.
  No new Python cut. Root `main.py` still h2. Did not run `agent.so`.
- JSON: `experiments/20260904_study_packet.json`,
  `experiments/20260904_fieldbook_rolling12.json`,
  `experiments/20260904_top10_games.json`,
  `experiments/20260904_top10_gap.json`.

## 2026-09-05 — Jesse measured; 9c9s extra sheep at 227/242/266; six-day Hold

- CSV `2026-09-04T07:23:44`: heralces **rank 886 / 1896.5** of 7567
  (Fieldbook `55962758`). Gold 21 / 2814.7. Rank 10 Andrey Tikhomirov
  2873.7. Top: Crop Dusta 3033.1, **Jesse Bullard 2971.3**, Giulio
  2967.0. Yusuke 40 / 2751.0 sub `55975994`. No new Kaggle upload; user
  did not say 提交.
- No 09-04 daily zip yet. Measurements: official kaggleusercontent
  episode JSON listed by EpisodeService. 09-03 zip remains local
  fallback. Hunt: `_hunt_20260905/`.
- Fieldbook public 347 **124-57-166**, mean **+421**. Rolling 12
  **3-1-8**, mean **−19163** (east −175984 clone=0 Q=2 pasture 11).
  Autopsy `experiments/20260905_fieldbook_rolling12.json`. Episode ids
  **do not overlap** the 09-04 set `105353499…105333105`.
  - Tie: Timothee Henry exact 6c11s.
  - Later 9c9s vs frozen 9c5s: jasonstillchasin / Adrian Dubois extra
    sheep at **227/242/266**.
  - Heavier wheat: john inan 419 vs 387; gagacrow 434 vs 387.
  - Bantam hinge dump: wheat 1380 melon 1071 fert 1468.
  Loss class: still freeze-after-day-9 vs later 9c9s at 227/242/266.
- **Jesse Bullard** (absent from `20260904_top10_games.json`): land
  151/266 clone=true melon 72. Yarn-second **5c13s / 5c17s** extra
  sheep from step **179**; pizza-first **11c5s**. Wheat 277–397. Beat
  Giulio twice. Not Giulio 9c5s, not Knight dump, not sbol 4c14s.
- Yusuke live newest 4 (PIZZA / ICE_CREAM / PET_CAFE / BAKERY first):
  extra sheep always **227 (+1→6), 242 (+2→8), 266 (+1→9)**. Fieldbook
  YARN_LATE is **218/242/266** only when yarn is third.
- Hunt (no cell exec): six-day still the only later-block reselect.
  tetsutani shape-the-shop (absent from 09-04 packet hunt) is a six-day
  guard + last-turn SELL on two C++ tapes — same `agent.so` bar.
  aamir28 beginner; dariushafshar last-callable trap; destbreso x-ray
  infra. **Hold. Do not upload.** No Windows `agent.so`. No new Python
  cut. Root `main.py` still h2.
- JSON: `experiments/20260905_study_packet.json`,
  `experiments/20260905_fieldbook_rolling12.json`,
  `experiments/20260905_top10_games.json`,
  `experiments/20260905_9c9s_sheep_steps.json`.

## 2026-09-06 — keiz measured; Yusuke 9c9s is a frozen tape not a BALANCED patch; six-day Hold

- CSV `2026-09-04T10:48:46`: heralces **rank 898 / 1883.4** of 7586
  (Fieldbook `55962758`). Gold 21 / 2812.4. Rank 10 edteoh 2850.3.
  Top: Crop Dusta 3016.8, **keiz 2983.8**, Jesse Bullard 2967.8.
  Yusuke 71 / 2694.3. No new Kaggle upload; user did not say 提交.
- No 09-04 daily zip. CDN kaggleusercontent episode JSON + EpisodeService.
  Hunt: `_hunt_20260906/`.
- Fieldbook public 372 **133-60-179**, mean **+585**. Rolling 12
  **4-3-5**, mean **+2565**. Autopsy
  `experiments/20260906_fieldbook_rolling12.json`. Episode ids **do not
  overlap** the 09-05 set `105398589…105385215`. All 12 clone, land
  151/266, 17 pastures, melon 72.
  - Ties: exact BALANCED 9c5s (pardival, kumk, goh 6c11s).
  - Yarn-first 6c11s **wins** vs 9c9s xiannaix +8591 and 8c9s masayoshi
    +6214.
  - Small same-herd wheat tails: Ramesh 416 vs 380 **−933**; 史永刚 −1237.
  Loss class: still freeze-after-day-9 vs later 9c9s / heavier wheat.
- **keiz** (absent from 09-04 and 09-05 top-board files): land 151/266,
  **always 1 goose**, 7c6s / 11c11s / 8c6s / 5c14s, wheat 304–444, melon
  72–120, clone mixed. Beat Jesse +2115 and Crop Dusta three times.
  Not Giulio 9c5s, not Knight dump, not Jesse 5c13s.
- Yusuke live reselect-vs-patch (`20260906_yusuke_reselect_vs_patch.json`):
  four 09-05 games pairwise **identical 0–266**; two newest games match
  that tape (BRUNCH / FARMERS_MARKET first). Prefix vs Fieldbook
  BALANCED already diverges at **step 1** (farmer 180 / hands 209 /
  market 101). After 216, still 41/50/43 diffs besides extra SHEEP.
  **Neither** a later-block reselect **nor** a BALANCED-tail patch.
  Do not name a 227/242/266 wrap of cut 10.
- Hunt (no cell exec): six-day still gated next. evgendvorkin (absent
  from 09-05 packet hunt) is Kaito v27. three-day shop router still C++.
  farming-score-v5 Kenjo. **Hold. Do not upload.** No Windows `agent.so`.
  Root `main.py` still h2.
- JSON: `experiments/20260906_study_packet.json`,
  `experiments/20260906_fieldbook_rolling12.json`,
  `experiments/20260906_top10_games.json`,
  `experiments/20260906_yusuke_reselect_vs_patch.json`.

## 2026-09-06 — cut 11 Python six-day port; clone/G5 gated Hold

- Assembled a Windows-runnable Python port of Yusuke six-day public-state
  Fieldbook at `experiments/candidates/yusuke_sixday/`. Encoded 144-turn
  blocks and trees come from the local hunt C++ `policy.cpp`. Does **not**
  load Linux `agent.so`. Not a 227/242/266 sheep wrap of cut 10 BALANCED:
  opening already differs at step 0; after 216 farmer/hands differ on both
  day-6 routes; extra sheep are 217/226/241/265, not 227/242/266.
- Reselect at 144 / 288 / 432 / 576. Shop-bag overlay: no yarn in the
  unlocked shops at day 6 → segment-1 route 1. Strawberry-crash leaf of
  the last-block tree is used only when wool is still priced (> 32.5).
  Last two turns top up SELL to remaining shed goods. Sales-first order.
- Recorded-seat clone 3-0 and G5 both-win on official 1.32.7, 720 turns,
  both seats `DONE` (`experiments/candidates/yusuke_sixday/screen.json`):
  prvsiyan `100348898` **+1274**, fufufukakaka `100504057` **+8532**,
  masayoshi `100444645` **+1193**, Subin An `97399969` **+32946**,
  James Y `95677563` **+35432**.
- **Hold. Do not upload.** User did not say 提交. No new Kaggle upload.
  Newest-2 stays Fieldbook `55962758` + shopbag `55962761`. Root `main.py`
  still h2 `65e6f5cd...`.

## 2026-09-06 — uploaded cut 11 six-day `56028043`

- User: 你是kaggle的参与者，不用等我说提交. Cut 11 Python six-day is
  the gated chassis; clone 3-0 and G5 both-win already recorded.
- Packed one-file `artifacts/submission/yusuke_sixday/main.py` from
  `sixday_tapes.py` + `sixday_logic.py`. Split vs packed actions matched
  on replay steps 0/1/24/144/217/288/432/576/717/718. LF only.
- G6 bundle:
  - Agent SHA-256 `854c6efed022bebb4c7e6b50696be1b9036ef7e6c718524471088c7d7e6e1fed`
    (186,392 bytes)
  - Bundle `artifacts/submission/yusuke_sixday/submission.tar.gz`
  - Bundle SHA-256 `d7ae8ef7e470500a84d212b32be41dd2aeca5d4d6aaafa08d4b35d032a8b6cf4`
  - Bundle size 22,305 bytes. Members `['main.py']` only. compile and
    independent re-extract byte-identity passed.
- At upload, live newest-2 had already slid: Fieldbook `55962758`
  **1766.8**, shopbag reupload `55962761` **1627.2**.
- Kaggle submission ID `56028043` at 2026-09-05 08:04:54 UTC.
  Status at upload: PENDING. Daily quota remaining: 4.
  Description starts `yusuke_sixday SHA 854c6efe`.
- Newest-2 after COMPLETE: `56028043` + shopbag `55962761`. Fieldbook
  `55962758` drops. Did **not** re-upload boatlee. Did **not** re-upload
  shopbag (already newer than Fieldbook). Root `main.py` still h2
  `65e6f5cd...`.
- Screen recap (recorded-seat 1.32.7, 720, DONE/DONE): prvsiyan **+1274**,
  fufu **+8532**, masa **+1193**, Subin **+32946**, James **+35432**.

## 2026-09-07 — six-day COMPLETE 1748.2; Deskbo wool-crash Hold

- User: 你是kaggle的参与者，不用等我说提交. No licensed later-block
  cut, so **Hold** anyway. Did not burn quota.
- Submissions API + CSV `2026-09-05T09:10:17`: six-day `56028043`
  **COMPLETE 1748.2**. Shopbag `55962761` **1619.7**. Fieldbook
  `55962758` **1762.9** (inactive). heralces **rank 1152 / 1748.2** of
  7699 (six-day is the team floor). Gold 21 l1aF 2773.2. Rank 10 Syed
  Asad Ali 2827.3. Top: keiz 3057.3, Jesse 2972.4, Andrey 2937.1.
- EpisodeService listed 14 PUBLIC + 1 VALIDATION. Public W/T/L
  **13-0-1**, mean **+26135**. Ids `105746953…105735087` do not overlap
  the 09-06 Fieldbook rolling 12. Autopsy
  `experiments/20260907_sixday_rolling.json`. Land 151/266, melon 72.
  Charles Backman is the yarn path **8c9s**; the rest of our seat is
  7c10s except that one.
- Only loss: Deskbo `105744091` **−15628**, clone=0, 7c10s vs **11c4s**,
  no yarn, wool **$1** by 432, milk 264–292. Cash gap +5641 at 432,
  **−7709 at 576**. Selected `[0,1,0,0,0]`. Not freeze-after-day-9 9c9s.
- Same 11c4s **Stanislav Ilin `105743208` is a WIN +15963**: yarn at
  216, wool still 198 at 432, milk already cheap (120). 11 cows are
  not an automatic loss.
- Cut 12 probe: force segment-3 route 1 (134 milk vs 48) on recorded-seat
  Deskbo. Still **L −15706**. Later blocks buy no extra cows after 288
  (s1 r1 has one cow at 217 only). Three-day 72-turn splice at 360 is
  C++ `agent.so` and would not fire (Deskbo first shop SMOOTHIE, not
  BAKERY/PET_CAFE). **Hold.** Do not upload. Newest-2 stays `56028043`
  + `55962761`. Did not re-upload boatlee. Root `main.py` still h2.
- Hunt (no cell exec) `_hunt_20260908/`: apex v7 is Yusuke three-day
  C++ 72-turn; mohui666 v66 is a GitHub Kaito-lineage rule agent;
  leoprovorov is a gzip Crop Dusta payload; dianat is a beginner
  `apex_agent`; aviral is an empty starter; rivaka has no agent.
  None licenses a Python later-block cut.
- JSON: `experiments/20260907_study_packet.json`,
  `experiments/20260907_sixday_rolling.json`.

## 2026-09-08 — six-day 1888.3; opening-broke + clone wool-crash Hold

- User: 你是kaggle的参与者，不用等我说提交. Cut 13 recorded-seat did
  not flip Deskbo/Stefano/fufu, so **Hold**. Did not burn quota. Did
  not re-upload cut 12.
- Submissions API + CSV `2026-09-05T12:59:29`: six-day `56028043`
  **COMPLETE 1888.3**. Shopbag `55962761` **1606.9**. Fieldbook
  `55962758` **1762.9** (inactive). heralces **rank 939 / 1888.3** of
  7723. Gold 21 YUK 2766.8. Rank 10 Atakan Aldemir 2838.1. Top: keiz
  3058.1, Jesse 2964.5, Andrey 2930.0.
- EpisodeService 78 PUBLIC + 1 VALIDATION. All-public W/T/L **44-0-34**,
  mean **−7318**. Newest-12 ids `105798735…105787453` do **not** match
  the 09-07 set. Autopsy `experiments/20260908_sixday_rolling.json`.
  Rolling **3-0-9**, mean **−40727**.
- Loss class mixed, not freeze-after-day-9 9c9s:
  - Opening-broke no-land: Tatu `105797728` **−167313** and Zimin
    `105791046` **−150937**, Q=1, 0 cows/sheep, cash 0 by step 24.
    shakedamo `105794752` Q=2, 0 cows, **−146543**. BUY_LAND at 150/265
    no-ops. Not fixable after 216.
  - Clone 9c5s/8c9s wool-crash: Stefano **−21909**, fufu **−11025**,
    Fih/weihao/Akira/dauletto. Q=3, live s4 tree picks route 0.
- Cut 13 probe (s4 route 3 when cash_gap<0 and milk>150), recorded-seat
  1.32.7: Deskbo **L −18470** (worse), Stefano **L −22834** (worse),
  fufu **L −8724** (still L). **Hold.** Not a 227 wrap. Newest-2 stays
  `56028043` + `55962761`. Did not re-upload boatlee. Root `main.py`
  still h2.
- Hunt (no cell exec) `_hunt_20260909/`: foysal 3-day sell-cap is Yusuke
  three-day C++ plus terminal sweep, `agent.so`. Apex v7 same chassis.
  None licenses a Python later-block cut.
- JSON: `experiments/20260908_study_packet.json`,
  `experiments/20260908_sixday_rolling.json`,
  `experiments/20260908_cut13_probe.json`.

## 2026-09-09 — six-day 1590.8; cut 14 y3uanm later-block uploaded `56111821`

- User: 你是kaggle的参与者，不用等我说提交. Cut 14 is a gated
  Windows-runnable later-block (clone 3-0 + G5). **Submitted.** Did not
  re-upload cut 12 or cut 13. Those stay **Hold**. Did not re-upload
  boatlee.
- Submissions API + CSV `2026-09-09T02:24:27`: six-day `56028043`
  **COMPLETE 1590.8**. Shopbag `55962761` **1464.2**. Fieldbook
  `55962758` **1762.9** (inactive). heralces **rank 1735 / 1590.8** of
  8262. Gold 21 unreal 2812.7. Rank 10 Sonu Yadav 2846.0. Top: SpaTaro
  2961.4, Otter Vibe 2951.4, Matthew Huang 2909.6.
- EpisodeService 346 PUBLIC + 1 VALIDATION. All-public W/T/L
  **138-0-208**, mean **−26304**. Newest-12 ids `106973284…106850799`
  do **not** match the 09-08 set `105798735…105787453`. Autopsy
  `experiments/20260909_sixday_rolling.json`. Rolling **4-0-8**, mean
  **−21257**.
- Loss class mixed, not freeze-after-day-9 9c9s:
  - Opening-broke no-land: SOUTA `106891732` **−122575** and Eesh
    `106869362` **−169174**, Q=1, cash 0 by step 24. BUY_LAND at 151/266
    no-ops. Not fixable after 216.
  - Clone later-block wool-crash: AM `106950143` 11c5s+3g **−21692**,
    wool=$1 by 432; Filippo wheat-mountain 2429 vs 398 **−17166**;
    8c9s/6c11s coin-flips. Cut 12/13 already lost Deskbo/Stefano/fufu.
- Current #1 SpaTaro measured from official JSON (not 09-04 Giulio /
  Knight / sbol, not 09-05 Jesse, not 09-06 keiz). Early/multi land
  (2–3 / 74 / 122 / 146–151 / 198–223), not 151/266. Herds 10c18s /
  8c6s / 14c4s / 11c6s. Wheat 697–1086. clone=0. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260909b/`: `yhay81/shop-router-0908` is
  ctypes native `.so`. aurax7 has no after-216 reselect. tetsutani
  market-smart is EDA. `y3uanm/kaggriculture-conservative-market-router-v5`
  is Python later-block at 226/360/433.
- Cut 14: static writefile extract SHA `acf7c664...`. After-216 differs
  from live six-day and Fieldbook BALANCED. Extra sheep **217/265**, not
  227/242/266. Recorded-seat 1.32.7 720 DONE/DONE: prvsiyan **+22889**,
  fufu **+27316**, masa **+17295**, Subin **+27188**, James **+69612**.
  Packed one-file `submission.tar.gz` 30098 bytes. **Submitted**
  `56111821` at 2026-09-09 02:47:28 UTC; **COMPLETE 1114.7** provisional.
- Shopbag reupload **`56112309`** PENDING at 2026-09-09 03:15:38 UTC
  (same `moon_shopbag_v1` SHA `b37fa97f...` as `55962761` / `55840543`).
  Newest-2: cut 14 `56111821` + shopbag `56112309` (lineage `55962761`).
  Six-day `56028043` drops. Did not re-upload boatlee. Did not
  re-upload cut 12 or cut 13. Root `main.py` still h2.
- JSON: `experiments/20260909_study_packet.json`,
  `experiments/20260909_sixday_rolling.json`,
  `experiments/20260909_top10_games.json`,
  `experiments/20260909_cut14_divergence.json`.

## 2026-09-10 — cut 14 1795.1; cut 15 Thomas later-block uploaded `56146106`

- Submissions API: cut 14 `56111821` **COMPLETE 1795.1**. Shopbag
  `56112309` **1429.4**. Six-day `56028043` **1590.8** (dropped). CSV
  `2026-09-10T14:10:04`: heralces **rank 1605 / 1795.1** of 8523. Gold 21
  c-number 2909.3. Rank 10 mtmr_s1 2951.5. Top: SpaTaro 3089.8 sub
  `56114097`, Otter Vibe 3025.3.
- EpisodeService cut 14: 215 PUBLIC + 1 VALIDATION. All-public W/T/L
  **80-34-101**, mean **+933**. Newest-12 ids `107493021…107453419` do
  **not** match the 09-09 set `106973284…106850799`. Autopsy
  `experiments/20260910_cut14_rolling.json`. Rolling **3-2-7**, mean
  **−7122**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal clones (Win Suthar 6c11s **−28286**, Black Mamba 4c13s
  **−25504**, Akira 6c11s **−22326**) plus Raster0x2a clone wool-crash
  **−5498**. BUY_LAND 151/266 succeeded; cash_24 6–24.
- #2 Otter Vibe measured from official JSON (not 09-09 SpaTaro ids).
  Mid-land 121/242–247, goose-heavy, clone=0. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260910/`: `yhay81/shop-router-0909` is
  Python day-6 144/648. aurax7 v2 same. dmitrii/flexonafft are 712
  harvest overlays. y3uanm v4 is cut-14 family. Header-only read of
  Thomas 93.8 looked day-6; static extract reselects at 288/432/576.
- Cut 15: static writefile extract SHA `b87a27ed...`. After-216 differs
  from live six-day, Fieldbook BALANCED, and cut 14. Extra sheep **265**,
  not 227/242/266. Recorded-seat 1.32.7 720 DONE/DONE: prvsiyan **+5757**,
  fufu **+28052**, masa **+16873**, Subin **+31605**, James **+68313**.
  Packed one-file `submission.tar.gz` 49544 bytes. **Submitted**
  `56146106` at 2026-09-10 14:24:40 UTC; **PENDING**. Newest-2: cut 15
  `56146106` + shopbag `56112309` (lineage `55962761`). Cut 14
  `56111821` drops. Did not re-upload shopbag (already newest-2 partner).
  Did not re-upload boatlee. Did not re-upload cut 12 or cut 13. Root
  `main.py` still h2. Quota remaining **4**.
- JSON: `experiments/20260910_study_packet.json`,
  `experiments/20260910_cut14_rolling.json`,
  `experiments/20260910_top10_games.json`,
  `experiments/20260910_cut15_divergence.json`.

## 2026-09-10b — cut 15 1864.4; cut 16 King v4e uploaded `56151152`

- Submissions API: cut 15 `56146106` **COMPLETE 1864.4** (was 1868.7 at
  study start). Shopbag `56112309` **1422.9**. Cut 14 `56111821`
  **1799.3**. Six-day `56028043` **1590.8** (dropped). CSV
  `2026-09-10T20:08:14`: heralces **rank 1530 / 1868.7** of 8566. Gold 21
  lc今天刷了吗 2909.7. Rank 10 kanno 2945.0. Top: SpaTaro 3109.9 sub
  `56114097`, ymg_aq 3040.2.
- EpisodeService cut 15: 92 PUBLIC + 1 VALIDATION. All-public W/T/L
  **50-7-35**, mean **+7542**. Newest-12 ids `107579117…107568611` do
  **not** match the 09-10 cut14 set `107493021…107453419`. Autopsy
  `experiments/20260910b_cut15_rolling.json`. Rolling **4-1-7**, mean
  **+2067**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal clones plus Junichiro Morita wool-crash **−11971**
  (wool=$1 by 360) and Cyrus 6c11s **−11938**. BUY_LAND 151/266
  succeeded; cash_24 23–67; clone=1.
- Missing high-rank team ymg_aq measured from official JSON (not SpaTaro
  / Otter Vibe ids). Mid-land 121/170, clone=0, wheat 1301–1478. Opening
  land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260910b/`: lucifer sale overlay; ahmed
  Shop0909+sale; dmitrii two-coins day-6; shashwat RL EDA; mzcao COK V7;
  boatlee v29 gzip not decoded. No new later-block Python there.
- Cut 16: static gzip extract of `yamakawanin/king-v4e-rc4` SHA
  `26ffba52...`. Shop-family PROGRAM reselect after 216 at 288/360/432/576
  plus YARN_SECOND from 240. After-216 differs from live six-day,
  Fieldbook BALANCED, cut 14, and cut 15. Extra sheep **226/241/265**,
  not 227/242/266. Recorded-seat 1.32.7 720 DONE/DONE: prvsiyan
  **+12627**, fufu **+12014**, masa **+40050**, Subin **+27159**, James
  **+77153**. Packed one-file `submission.tar.gz` 362692 bytes.
  **Submitted** `56151152` at 2026-09-10 20:20:29 UTC; **PENDING**.
  Shopbag reupload **`56151155`** PENDING at 20:20:39 UTC (same
  `moon_shopbag_v1` SHA `b37fa97f...` as `56112309` / `55962761`).
  Newest-2: cut 16 `56151152` + shopbag `56151155`. Cut 15 `56146106`
  drops. Did not re-upload boatlee. Did not re-upload cut 12 or cut 13.
  Root `main.py` still h2. Quota remaining **2**.
- JSON: `experiments/20260910b_study_packet.json`,
  `experiments/20260910b_cut15_rolling.json`,
  `experiments/20260910b_top10_games.json`,
  `experiments/20260910b_cut16_divergence.json`.

## 2026-09-11 — cut 16 COMPLETE 1799.2; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1799.2**. Shopbag
  reupload `56151155` **COMPLETE 1402.4** (68 public, not a tiny
  sample). Cut 15 `56146106` **1864.4** (dropped). Cut 14 `56111821`
  **1799.3**. Six-day `56028043` **1590.8**. CSV
  `2026-09-11T08:08:15`: heralces **rank 1624 / 1799.2** of 8609. Gold 21
  自己找差距 2894.0. Rank 10 Mengfei Li 2949.6. Top: SpaTaro 3101.2,
  Majkel1337 3086.5.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but a new cut would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (shopbag 1402.4; re-upload is 600-provisional). **Hold.** No Kaggle
  submit. Quota remaining **5**.
- EpisodeService cut 16: 109 PUBLIC + 1 VALIDATION. All-public W/T/L
  **57-2-50**, mean **+2331**. Newest-12 ids `107753711…107712285` do
  **not** match the 09-10b cut15 set `107579117…107568611`. Autopsy
  `experiments/20260911_cut16_rolling.json`. Rolling **6-0-6**, mean
  **+1150**. All 12 clone=1, BUY_LAND 151/266, cash_24 1–22.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal clones plus Syed Asad Ali 4Q 15-cow wool-crash **−39903**
  (wool=$1 by 432) and Suba S 4c15s **−11471**.
- Missing high-rank team Majkel1337 measured from official JSON (not
  SpaTaro / ymg_aq ids). Mid-land 150 then 218–222, clone=0, wheat
  472–511. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260911/`: xuantianfengwu hybrid-core
  heuristic; destbreso EDA; Ahmed v34 Shop0909+sale; Dmitrii herd-safe
  and two-coins sale windows; navazshfathi ctypes 0908. No new
  later-block Python. Cut 12/13 stay Hold. Did not re-upload boatlee.
  Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260911_study_packet.json`,
  `experiments/20260911_cut16_rolling.json`,
  `experiments/20260911_top10_games.json`,
  `experiments/20260911_gate.json`.

## 2026-09-11b — cut 16 1757.2; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1757.2** (was 1799.2).
  Shopbag `56151155` **COMPLETE 1383.3**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-11T14:06:14`: heralces **rank 1710 / 1757.2**
  of 8635. Gold 21 Le Viet 2909.1. Rank 10 carlos-tagosaku 2969.8. Top:
  Majkel1337 3126.4, SpaTaro 3070.4.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but a new cut would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (shopbag 1383.3; re-upload is 600-provisional). **Hold.** No Kaggle
  submit. Quota remaining **5**.
- EpisodeService cut 16: 130 PUBLIC. All-public W/T/L **63-2-65**, mean
  **+732**. Newest-12 ids `107839952…107789318` do **not** match the
  09-11 set `107753711…107712285`. Autopsy
  `experiments/20260911b_cut16_rolling.json`. Rolling **1-0-11**, mean
  **−11764**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal clones plus 8c6s3g PET_CAFE wool-crash **faye −36695**,
  Variiiiiii **−30222**, Yusuraume **−25695**. BUY_LAND 151/266;
  cash_24 3–22; clone=1 on 11/12.
- Missing high-rank team Majkel1337 now CSV/live #1, re-measured on
  scoring-sub ids disjoint from 09-11. Mid-land 150 then 218–224,
  clone=0, wheat 305–434. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260911b/`: Yusuke shop-router-0911-simple
  is day-6 144/648; Ahmed v35 Shop0909+sale/712; sunil/leoprovorov sale
  windows; xuantianfengwu heuristic; lucifer V2 rhythm; ziyiming 403.
  No new later-block Python. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260911b_study_packet.json`,
  `experiments/20260911b_cut16_rolling.json`,
  `experiments/20260911b_top10_games.json`,
  `experiments/20260911b_gate.json`.

## 2026-09-12 — cut 16 1730.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1730.1** (was 1757.2).
  Shopbag `56151155` **COMPLETE 1369.9**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T01:39:31`: heralces **rank 1797 / 1730.1**
  of 8684. Gold 21 Hiểu Vy 2912.9. Rank 10 THIRD FARM CLUB 2952.3. Top:
  Majkel1337 3171.4 (live 3174.4), ymg_aq 3072.6, Unknown Mother-Goose
  3053.7.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 161 PUBLIC + 1 VALIDATION. All-public W/T/L
  **74-2-85**, mean **−504**. Newest-12 ids `108010033…107959708` do
  **not** match the 09-11b set `107839952…107789318`. Autopsy
  `experiments/20260912_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−3452**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (wool still priced) plus extra-goose / identical-
  clone coin-flips. Newest Manu `108010033` **−10720** is 10c8s with
  extra sheep **227/242/266** and still lost to 8c6s3g. BlueSky_sora
  **−18477**, Suzumaru **−17701**. BUY_LAND 151/266; cash_24 3–22;
  clone=1 on 10/12.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-11 and 09-11b. Mid-land
  150 then 218–222, clone=0, wheat 404–520, 0 geese this window.
  Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260912/`: Ahmed v34 is a byte-identical
  re-pull of 0911 Shop0909+sale; v36/v37 are four-turn / fert-labor
  overlays on that chassis; hgh1024 herd-safe v2 is router `3a444a70`
  sale_horizon=2. Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260912_study_packet.json`,
  `experiments/20260912_cut16_rolling.json`,
  `experiments/20260912_top10_games.json`,
  `experiments/20260912_gate.json`.

## 2026-09-12b — cut 16 1695.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1695.1** (was 1730.1).
  Shopbag `56151155` **COMPLETE 1323.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T15:36:54`: heralces **rank 1910 / 1695.1**
  of 8768. Gold 21 Syed Asad Ali 2899.8. Rank 10 charmq 2961.4. Top:
  Majkel1337 3242.7, ymg_aq 3089.2, Unknown Mother-Goose 3060.9.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 187 PUBLIC + 1 VALIDATION. All-public W/T/L
  **83-2-102**, mean **−743**. Newest-12 ids `108208866…108124312` do
  **not** match the 09-12 set `108010033…107959708`. Autopsy
  `experiments/20260912b_cut16_rolling.json`. Rolling **3-0-9**, mean
  **−3920**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g with wool $1 by 360 (Iskander `108166009`
  **−12967**, extra sheep only 314) plus YARN clone timing (Juank
  **−12889**, TERMINUS **−9174**). BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 11/12. 09-12 Manu already bought extra sheep 227/242/266
  and still lost 8c6s3g — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-12. Mid-land 150 then
  218–222, clone=0, wheat 340–598, geese this window. Opening land is
  not a later-block license.
- Hunt (no cell exec) `_hunt_20260912b/`: y3uanm rollback-v20 writefile
  SHA `acf7c664` is live cut 14; crystalbaby decompressed SHA `94c1c2c0`
  is Ahmed v37 Shop0909; dmitrii smaller-market-shock is sale_horizon=5
  144/648; municef1/bernubritz are tapes; melomanpanda is 2g1c1s
  heuristic. Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260912b_study_packet.json`,
  `experiments/20260912b_cut16_rolling.json`,
  `experiments/20260912b_top10_games.json`,
  `experiments/20260912b_gate.json`.

## 2026-09-12c — cut 16 1682.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1682.4** (was 1695.1).
  Shopbag `56151155` **COMPLETE 1328.2**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T16:37:22`: heralces **rank 1942 / 1682.4**
  of 8771. Gold 21 Syed Asad Ali 2904.4. Rank 10 redblackbst 2972.6. Top:
  Majkel1337 3249.2, ymg_aq 3078.7, Unknown Mother-Goose 3065.1.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 190 PUBLIC + 1 VALIDATION. All-public W/T/L
  **83-2-105**, mean **−873**. Newest-12 ids `108227462…108057422` do
  **not** match the 09-12b set `108208866…108124312`. Autopsy
  `experiments/20260912c_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−5037**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (MoZayed `108222615` **−17529**, extra sheep only
  314; yomogii `108093419` **−16881** wool $1, no extra sheep after 216)
  plus extra-goose / identical-clone. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 12/12. Shaw Sebastian `108057422` already bought extra sheep
  227/242/266 and still lost 9c8s — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-12b. Mid-land 150 then
  218–222, clone=0, wheat 465–621, geese this window. Opening land is
  not a later-block license.
- Hunt (no cell exec) `_hunt_20260912c/`: Ahmed V38 writefile SHA
  `a2047ebd` is Shop0909 144/648 + 288/712 overlay; zhincez plateau
  decompressed SHA `07f6c806` is day-3/6 tape-mosaic; other zhincez are
  analysis. Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260912c_study_packet.json`,
  `experiments/20260912c_cut16_rolling.json`,
  `experiments/20260912c_top10_games.json`,
  `experiments/20260912c_gate.json`.

## 2026-09-12d — cut 16 1686.8; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1686.8** (was 1682.4).
  Shopbag `56151155` **COMPLETE 1328.2**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T17:36:42`: heralces **rank 1945 / 1686.8**
  of 8776. Gold 21 Kaggriculture Agent 2905.3. Rank 10 Mengfei Li 2964.0.
  Top: Majkel1337 3242.5 (live 3243.8), ymg_aq 3071.6, Unknown Mother-Goose
  3062.4.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 191 PUBLIC + 1 VALIDATION. All-public W/T/L
  **84-2-105**, mean **−868**. Newest-12 ids `108243488…108138037` do
  **not** match the 09-12c set `108227462…108057422`. Autopsy
  `experiments/20260912d_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−3151**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (IskanderAkhmetov `108166009` **−12967**, extra sheep only
  314; XIAO MA `108172639` **−6573** wool $1, no extra sheep after 216)
  plus extra-goose / identical-clone / YARN. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 11/12. Bonkoturyu `108243488` already bought extra sheep
  227/242/266 and won 9c8s +53 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-12c. Mid-land 150 then
  218–222, clone=0, wheat 393–495, geese this window. Opening land is
  not a later-block license.
- Hunt (no cell exec) `_hunt_20260912d/`: nusrati V35 writefile SHA
  `294e7e4d` is Shop0909 144/648 + 288/712 overlay; sunil v4 is Shop0909
  T4 overlay + 712 planner; two zhincez are analysis. Author lists: no
  Yusuke later-block, no king rc5, no y3uanm v6. Cut 12/13 stay Hold.
  Did not re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260912d_study_packet.json`,
  `experiments/20260912d_cut16_rolling.json`,
  `experiments/20260912d_top10_games.json`,
  `experiments/20260912d_gate.json`.

## 2026-09-12e — cut 16 1682.0; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1682.0** (was 1686.8).
  Shopbag `56151155` **COMPLETE 1324.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T18:37:09`: heralces **rank 1950 / 1682.0**
  of 8788. Gold 21 pupen_o 2905.1. Rank 10 QQ Farming 2954.7.
  Top: Majkel1337 3246.2 (live 3246.2), ymg_aq 3062.5, Unknown Mother-Goose
  3053.6.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 192 PUBLIC + 1 VALIDATION. All-public W/T/L
  **84-2-106**, mean **−864**. Newest-12 ids `108259280…108081993` do
  **not** match the 09-12d set `108243488…108138037`. Autopsy
  `experiments/20260912e_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−5767**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (MoZayed `108222615` **−17529**, extra sheep only
  314; yomogii `108093419` **−16881** wool $1, no extra sheep after 216)
  plus extra-goose / identical-clone / YARN. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 12/12. sol12378 `108123019` already bought extra sheep
  227/242/266 and won 9c8s +117 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-12d. Mid-land 150 then
  218–222, clone=0, wheat 450–520, geese this window. Opening land is
  not a later-block license.
- Hunt (no cell exec) `_hunt_20260912e/`: lokesh V37 writefile SHA
  `94c1c2c0` is Shop0909 144/648 + 288/712 overlay (already rejected as
  crystalbaby). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260912e_study_packet.json`,
  `experiments/20260912e_cut16_rolling.json`,
  `experiments/20260912e_top10_games.json`,
  `experiments/20260912e_gate.json`.

## 2026-09-13 — cut 16 1683.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1683.4** (was 1682.0).
  Shopbag `56151155` **COMPLETE 1324.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T19:37:07`: heralces **rank 1946 / 1683.4**
  of 8789. Gold 21 Catalyst 2915.1. Rank 10 Mengfei Li 2978.3.
  Top: Majkel1337 3249.7 (live 3249.7), ymg_aq 3056.9, Artem The Farmer 3037.4.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 194 PUBLIC + 1 VALIDATION. All-public W/T/L
  **85-2-107**, mean **−894**. Newest-12 ids `108273755…108153141` do
  **not** match the 09-12e set `108259280…108081993`. Autopsy
  `experiments/20260913_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−2869**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (IskanderAkhmetov `108166009` **−12967**, extra sheep only
  314; XIAO MA `108172639` **−6573** wool $1, no extra sheep after 216)
  plus extra-goose / identical-clone / YARN. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 11/12. automatylicza `108273755` already bought extra sheep
  218/242/266 and lost 6c12s YARN −7750. Bonkoturyu `108243488` already
  bought extra sheep 227/242/266 and won 9c8s +53 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-12e. Mid-land 150 then
  218–222, clone mixed 1/4, wheat 293–607, geese this window. Opening land is
  not a later-block license.
- Hunt (no cell exec) `_hunt_20260913/`: no new slug vs `_hunt_20260912e`.
  Public search newest still lokesh V37 SHA `94c1c2c0`. Author lists: no
  Yusuke later-block, no king rc5, no y3uanm v6. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913_study_packet.json`,
  `experiments/20260913_cut16_rolling.json`,
  `experiments/20260913_top10_games.json`,
  `experiments/20260913_gate.json`.

## 2026-09-13b — cut 16 1691.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1691.4** (was 1683.4).
  Shopbag `56151155` **COMPLETE 1319.3**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T20:36:44`: heralces **rank 1943 / 1691.4**
  of 8794. Gold 21 Xiangyu Liu 2908.8. Rank 10 QQ Farming 2960.8.
  Top: Majkel1337 3244.3 (live 3244.3), M & M & P & Q 3062.5, ymg_aq 3058.3.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 196 PUBLIC + 1 VALIDATION. All-public W/T/L
  **87-2-107**, mean **−810**. Newest-12 ids `108296309…108105086` do
  **not** match the 09-13 set `108273755…108153141`. Autopsy
  `experiments/20260913b_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−2813**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (MoZayed `108222615` **−17529**, extra sheep only
  314; Robson `108224822` **−7905** wool $1, extra sheep 314)
  plus extra-goose / identical-clone / YARN. BUY_LAND 151/266; cash_24 10–27;
  clone=1 on 12/12. Juank Suarez `108139022` already bought extra sheep
  218/242/266 and lost 6c11s YARN −12889. Chanhyuk Han `108296309` already
  bought extra sheep 227/242/266 and won 9c8s +67. sol12378 `108123019`
  already bought extra sheep 227/242/266 and won 9c8s +117 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13. Mid-land 150 then
  220–222 (one game 150/243), clone=0, wheat 471–515, no geese this window.
  Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913b/`: two new slugs vs `_hunt_20260913`.
  Public search newest `xuantianfengwu/kaggriculture-timed-six-cow` writefile
  SHA `5dc0c68c` is a 6-cow heuristic (not after-216 reselect). Ahmed V38
  new slug writefile SHA `a2047ebd` reprint. Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913b_study_packet.json`,
  `experiments/20260913b_cut16_rolling.json`,
  `experiments/20260913b_top10_games.json`,
  `experiments/20260913b_gate.json`.

## 2026-09-13c — cut 16 1696.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1696.4** (was 1691.4).
  Shopbag `56151155` **COMPLETE 1321.1**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T21:37:38`: heralces **rank 1943 / 1696.4**
  of 8801. Gold 21 自己找差距 2921.6. Rank 10 redblackbst 2960.9.
  Top: Majkel1337 3249.6 (live 3249.6), M & M & P & Q 3080.6, ymg_aq 3049.0.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 197 PUBLIC + 1 VALIDATION. All-public W/T/L
  **88-2-107**, mean **−801**. Newest-12 ids `108311577…108161412` do
  **not** match the 09-13b set `108296309…108105086`. Autopsy
  `experiments/20260913c_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−2786**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (IskanderAkhmetov `108166009` **−12967**, extra sheep
  only 314 wool $1; Ke Ma Ke `108175982` **−3323** extra sheep 314;
  XIAO MA `108172639` **−6573** sheep 2/151/196 wool $1)
  plus extra-goose / identical-clone / YARN. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 11/12. automatylicza `108273755` already bought extra sheep
  218/242/266 and lost 6c12s YARN −7750. Bonkoturyu `108243488` already
  bought extra sheep 227/242/266 and won 9c8s +53 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13b. Mid-land 150 then
  218–228 (one game 150/220/222; one 4Q 150/224/227/228), clone=0, wheat
  455–608, one 4-goose game. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913c/`: one new slug vs `_hunt_20260913b`.
  Public search newest `prvsiyan/kaggriculture-market-ledger-seasonal-counterplay`
  policy SHA `1c98c297` is an educational ledger/phase framework (not
  after-216 reselect). Author lists: no Yusuke later-block, no king rc5,
  no y3uanm v6. Did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913c_study_packet.json`,
  `experiments/20260913c_cut16_rolling.json`,
  `experiments/20260913c_top10_games.json`,
  `experiments/20260913c_gate.json`.

## 2026-09-13d — cut 16 1698.7; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1698.7** (was 1696.4).
  Shopbag `56151155` **COMPLETE 1321.1**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T22:36:54`: heralces **rank 1946 / 1698.7**
  of 8804. Gold 21 Gleb Tumanov 2925.1. Rank 10 redblackbst 2963.5.
  Top: Majkel1337 3254.7 (live 3254.7), M & M & P & Q 3078.0, ymg_aq 3048.2.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 198 PUBLIC + 1 VALIDATION. All-public W/T/L
  **89-2-107**, mean **−762**. Newest-12 ids `108326448…108123019` do
  **not** match the 09-13c set `108311577…108161412`. Autopsy
  `experiments/20260913d_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−2130**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (MoZayed `108222615` **−17529**, extra sheep
  only 314; Robson `108224822` **−7905** wool $1, extra sheep 314)
  plus extra-goose / identical-clone / YARN. BUY_LAND 151/266; cash_24 10–27;
  clone=1 on 12/12. Juank Suarez `108139022` already bought extra sheep
  218/242/266 and lost 6c11s YARN −12889. Chanhyuk Han `108296309` already
  bought extra sheep 227/242/266 and won 9c8s +67. sol12378 `108123019`
  already bought extra sheep 227/242/266 and won 9c8s +117 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13c. Mid-land 150 then
  218–222 (one game 150/220; one 4Q 150/218/220/222), clone=0, wheat
  364–611, two goose games. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913d/`: no new slug vs `_hunt_20260913c`.
  Public search newest still `prvsiyan/kaggriculture-market-ledger-seasonal-counterplay`
  (SHA `1c98c297` educational framework). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913d_study_packet.json`,
  `experiments/20260913d_cut16_rolling.json`,
  `experiments/20260913d_top10_games.json`,
  `experiments/20260913d_gate.json`.

## 2026-09-13e — cut 16 1695.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1695.5** (was 1698.7).
  Shopbag `56151155` **COMPLETE 1321.1**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-12T23:36:41`: heralces **rank 1949 / 1695.5**
  of 8809. Gold 21 自己找差距 2918.7. Rank 10 redblackbst 2979.5.
  Top: Majkel1337 3223.8 (live 3223.8), M & M & P & Q 3109.6, ymg_aq 3039.4.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 199 PUBLIC + 1 VALIDATION. All-public W/T/L
  **89-2-108**, mean **−801**. Newest-12 ids `108328160…108162165` do
  **not** match the 09-13d set `108326448…108123019`. Autopsy
  `experiments/20260913e_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−3395**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (IskanderAkhmetov `108166009` **−12967**, extra sheep
  only 314 wool $1; Ke Ma Ke `108175982` **−3323** extra sheep 314;
  XIAO MA `108172639` **−6573** sheep 2/151/196)
  plus extra-sheep 16s (Artem The Farmer `108328160` **−8536**, extra sheep
  227/242/266 already bought) plus extra-goose / identical-clone / YARN.
  BUY_LAND 151/266; cash_24 3–27; clone=1 on 11/12. automatylicza
  `108273755` already bought extra sheep 218/242/266 and lost 6c12s YARN
  −7750. Bonkoturyu `108243488` already bought extra sheep 227/242/266
  and won 9c8s +53 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13d. Mid-land 150 then
  218–222 (three games 150/220/222; one 150/218), clone=0, wheat
  349–674, two 2-goose games and one 4-goose. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260913e/`: one new slug vs `_hunt_20260913d`.
  Public search newest `ahmedberatozer/notebookda72f457f5` V39 writefile
  SHA `708c7485` is Shop0909 144/648 + 288/712 overlay (not later-block).
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6. Did
  not extract to candidates/. Did not re-extract rejected kernels. Cut
  12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still h2
  SHA `65e6f5cd...`.
- JSON: `experiments/20260913e_study_packet.json`,
  `experiments/20260913e_cut16_rolling.json`,
  `experiments/20260913e_top10_games.json`,
  `experiments/20260913e_gate.json`.

## 2026-09-13f — cut 16 1697.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1697.5** (was 1695.5).
  Shopbag `56151155` **COMPLETE 1325.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T00:36:51`: heralces **rank 1936 / 1697.5**
  of 8810. Gold 21 mtmr_s1 2913.0. Rank 10 QQ Farming 2955.5.
  Top: Majkel1337 3234.1 (live 3234.1), M & M & P & Q 3123.6, ymg_aq 3042.5.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 203 PUBLIC + 1 VALIDATION. All-public W/T/L
  **91-2-110**, mean **−829**. Newest-12 ids `108351144…108161412` do
  **not** match the 09-13e set `108328160…108162165`. Autopsy
  `experiments/20260913f_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−1303**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (MoZayed `108222615` **−17529**, extra sheep
  only 314) plus extra-sheep 11s (Oleg Smirnov `108345614` **−11762**,
  extra sheep 227/242/266 already bought) plus extra-goose (Robson
  `108224822` **−7905** wool $1, extra sheep 314)
  plus identical-clone / YARN. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 12/12. Joyal `108161412` already bought extra sheep
  218/242/266 and lost 6c12s YARN −1227. Chanhyuk Han `108296309` already
  bought extra sheep 227/242/266 and won 9c8s +67 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13e. Mid-land 150 then
  220–222 (two games 150/220/222; two 150/220), clone=0, wheat
  435–535, four 2-goose games. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913f/`: no new slug vs `_hunt_20260913e`.
  Public search newest still `ahmedberatozer/notebookda72f457f5`
  (SHA `708c7485` Shop0909 144/648 + 288/712 overlay). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913f_study_packet.json`,
  `experiments/20260913f_cut16_rolling.json`,
  `experiments/20260913f_top10_games.json`,
  `experiments/20260913f_gate.json`.

## 2026-09-13g — cut 16 1702.8; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1702.8** (was 1697.5).
  Shopbag `56151155` **COMPLETE 1325.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T01:36:26`: heralces **rank 1943 / 1702.8**
  of 8811. Gold 21 Knight of Favonius 2906.2. Rank 10 binghua 2956.6.
  Top: Majkel1337 3242.7 (live 3242.7), M & M & P & Q 3130.2, Mengfei Li 3035.3.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 206 PUBLIC + 1 VALIDATION. All-public W/T/L
  **93-2-111**, mean **−893**. Newest-12 ids `108371627…108175982` do
  **not** match the 09-13f set `108351144…108161412`. Autopsy
  `experiments/20260913g_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−3016**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Ju `108369265` **−17212**, extra sheep
  only 314) plus extra-sheep 16s (Artem The Farmer `108328160` **−8536**,
  extra sheep 227/242/266 already bought) plus extra-goose (Kaipeng Zheng
  `108204278` **−1427**) plus identical-clone / YARN. BUY_LAND 151/266;
  cash_24 3–27; clone=1 on 11/12. automatylicza `108273755` already
  bought extra sheep 218/242/266 and lost 6c12s YARN −7750. Bonkoturyu
  `108243488` already bought extra sheep 227/242/266 and won 9c8s +53 —
  not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13f. Mid-land 150 then
  219–222 (one game 150/219/222/227/228; one 150/219; one 150/219/227/243;
  one 150/220/222), clone=0, wheat 364–483, goose mix 0g/2g/4g/0g.
  Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913g/`: no new slug vs `_hunt_20260913f`.
  Public search newest still `ahmedberatozer/notebookda72f457f5`
  (SHA `708c7485` Shop0909 144/648 + 288/712 overlay). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913g_study_packet.json`,
  `experiments/20260913g_cut16_rolling.json`,
  `experiments/20260913g_top10_games.json`,
  `experiments/20260913g_gate.json`.

## 2026-09-13h — cut 16 1691.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1691.5** (was 1702.8).
  Shopbag `56151155` **COMPLETE 1319.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T02:37:25`: heralces **rank 1956 / 1691.5**
  of 8814. Gold 21 Civitasmass 2909.9. Rank 10 3정훈 2962.3.
  Top: Majkel1337 3220.9 (live 3220.9), M & M & P & Q 3154.5, Mengfei Li 3060.9.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 209 PUBLIC + 1 VALIDATION. All-public W/T/L
  **93-2-114**, mean **−984**. Newest-12 ids `108383915…108227462` do
  **not** match the 09-13g set `108371627…108175982`. Autopsy
  `experiments/20260913h_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−894**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal YARN 6c11s (Peter Cnudde `108383915` **−13315**, extra sheep
  218/242/266 already bought) plus extra-sheep 11s (Oleg Smirnov
  `108345614` **−11762**, extra sheep 227/242/266 already bought) plus
  extra-goose (Rafael Molina Castaño `108377691` **−5101**) plus
  identical-clone / YARN. BUY_LAND 151/266; cash_24 3–27;
  clone=1 on 12/12. Chanhyuk Han `108296309` already bought extra sheep
  227/242/266 and won 9c8s +67. tksfjn `108290336` already bought extra
  sheep 218/242/266 and won 6c12s YARN +14627 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13g. Mid-land 150 then
  218–222 (one game 150/218; one 150/219/220/221/222/226/227/228; one
  150/219/221/227/228; one 150/220/222), clone=0, wheat 429–562, goose
  mix 2g/2g/3g/0g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913h/`: no new slug vs `_hunt_20260913g`.
  Public search newest still `ahmedberatozer/notebookda72f457f5`
  (SHA `708c7485` Shop0909 144/648 + 288/712 overlay). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913h_study_packet.json`,
  `experiments/20260913h_cut16_rolling.json`,
  `experiments/20260913h_top10_games.json`,
  `experiments/20260913h_gate.json`.

## 2026-09-13i — cut 16 1696.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1696.4** (was 1691.5).
  Shopbag `56151155` **COMPLETE 1319.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T03:37:26`: heralces **rank 1952 / 1696.4**
  of 8816. Gold 21 自己找差距 2913.6. Rank 10 Kaggriculture Agent 2965.9.
  Top: Majkel1337 3227.9 (live 3227.9), Mengfei Li 3042.5, Artem The Farmer 3037.5.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 210 PUBLIC + 1 VALIDATION. All-public W/T/L
  **94-2-114**, mean **−968**. Newest-12 ids `108399266…108208866` do
  **not** match the 09-13h set `108383915…108227462`. Autopsy
  `experiments/20260913i_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−4999**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (MoZayed `108222615` **−17529**, extra sheep
  218/227 extra geese 242/266; Ju `108369265` **−17212**) plus extra-sheep
  16s (Artem The Farmer `108328160` **−8536**, we already bought 227/242/266)
  plus extra-goose (Robson `108224822` **−7905**) plus YARN extra-sheep
  (automatylicza `108273755` **−7750**, extra sheep 218/242/266 already bought).
  BUY_LAND 151/266; cash_24 3–27; clone=11/12. Sidharth `108399266`
  already bought extra geese 227/242 and won 9c5s3g vs 9c5s4g +2525.
  Bonkoturyu `108243488` already bought extra sheep 227/242/266 and won
  identical 9c8s +53 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13h. Mid-land 150 then
  220–222 (one game 150/220; three 150/220/222), clone=1/4, wheat 377–597,
  goose mix 0g/2g/2g/0g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913i/`: no new slug vs `_hunt_20260913h`.
  Public search newest still `ahmedberatozer/notebookda72f457f5`
  (SHA `708c7485` Shop0909 144/648 + 288/712 overlay). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913i_study_packet.json`,
  `experiments/20260913i_cut16_rolling.json`,
  `experiments/20260913i_top10_games.json`,
  `experiments/20260913i_gate.json`.

## 2026-09-13j — cut 16 1692.8; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1692.8** (was 1696.4).
  Shopbag `56151155` **COMPLETE 1323.0**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T04:36:58`: heralces **rank 1949 / 1692.8**
  of 8818. Gold 21 redblackbst 2909.8. Rank 10 Catalyst 2949.1.
  Top: Majkel1337 3222.2 (live 3222.2), Mengfei Li 3051.5, Artem The Farmer 3032.8.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 211 PUBLIC + 1 VALIDATION. All-public W/T/L
  **94-2-115**, mean **−1051**. Newest-12 ids `108412731…108259280` do
  **not** match the 09-13i set `108399266…108208866`. Autopsy
  `experiments/20260913j_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−2308**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-goose (haonan zhengh `108412731` **−18535**, extra sheep 227 extra
  geese 242/266) plus extra-animal YARN 6c11s (Peter Cnudde `108383915`
  **−13315**, extra sheep 218/242/266 already bought) plus extra-sheep
  11s (Oleg Smirnov `108345614` **−11762**, extra sheep 227/242/266
  already bought). BUY_LAND 151/266; cash_24 3–27; clone=12/12.
  Chanhyuk Han `108296309` already bought extra sheep 227/242/266 and
  won identical 9c8s +67. tksfjn `108290336` already bought extra sheep
  218/242/266 and won 6c12s YARN +14627 — not a 227 wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13i. Mid-land 150 then
  218–222 (three games 150/220/222; one 150/218/220/222), clone=0/4,
  wheat 419–517, goose mix 0g/0g/4g/0g. Opening land is not a later-block
  license.
- Hunt (no cell exec) `_hunt_20260913j/`: one new slug vs `_hunt_20260913i`
  `crystalbaby/kaggriculture-v38-public-submission` writefile SHA
  `a2047ebd` (Ahmed V38 Shop0909 144/648 + 288/712 overlay, already
  rejected 0913b). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py`
  still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913j_study_packet.json`,
  `experiments/20260913j_cut16_rolling.json`,
  `experiments/20260913j_top10_games.json`,
  `experiments/20260913j_gate.json`.

## 2026-09-13k — cut 16 1688.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1688.5** (was 1692.8).
  Shopbag `56151155` **COMPLETE 1327.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T05:36:26`: heralces **rank 1961 / 1688.5**
  of 8829. Gold 21 kyy666 2908.5. Rank 10 Farmer 2958.8.
  Top: Majkel1337 3226.5 (live 3226.5), Mengfei Li 3047.6, THIRD FARM CLUB 3034.0.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 215 PUBLIC + 1 VALIDATION. All-public W/T/L
  **95-2-118**, mean **−1037**. Newest-12 ids `108432563…108270318` do
  **not** match the 09-13j set `108412731…108259280`. Autopsy
  `experiments/20260913k_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−2447**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Ju `108369265` **−17212**, extra sheep 218/227 extra
  geese 242/266; linyifangzhenshuai `108426937` **−9514**; carlos-tagosaku
  `108429814` **−8454**) plus extra-animal YARN 6c11s (wuwuwu `108432563`
  **−10575**, extra sheep 218/242/266 already bought; automatylicza
  `108273755` **−7750**) plus extra-sheep 16s (Artem The Farmer `108328160`
  **−8536**, we already bought 227/242/266). BUY_LAND 151/266; cash_24
  3–24; clone=12/12. Joyal `108422886` already bought extra sheep
  218/242/266 and won 6c11s YARN +27397. Sidharth `108399266` already
  bought extra geese 227/242 and won 9c5s3g vs 9c5s4g +2525 — not a 227
  wrap license.
- Missing high-rank team Majkel1337 still CSV/live #1, re-measured on
  scoring-sub `56156662` ids disjoint from 09-13j. Mid-land 150 then
  218–222 (three games 150/218/220/222; one 150/218), clone=0/4,
  wheat 430–623, goose mix 4g/0g/2g/4g. Opening land is not a later-block
  license.
- Hunt (no cell exec) `_hunt_20260913k/`: no new slug vs `_hunt_20260913j`.
  Public search newest still `crystalbaby/kaggriculture-v38-public-submission`
  (SHA `a2047ebd` Ahmed V38 Shop0909 144/648 + 288/712 overlay). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913k_study_packet.json`,
  `experiments/20260913k_cut16_rolling.json`,
  `experiments/20260913k_top10_games.json`,
  `experiments/20260913k_gate.json`.

## 2026-09-13l — cut 16 1692.2; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1692.2** (was 1688.5).
  Shopbag `56151155` **COMPLETE 1327.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T06:38:36`: heralces **rank 1966 / 1692.2**
  of 8838. Gold 21 自己找差距 2909.0. Rank 10 Subramanya N 2957.5.
  Top: Majkel1337 3220.0 (live 3220.0), Mengfei Li 3053.8, ymg_aq 3030.0.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 218 PUBLIC + 1 VALIDATION. All-public W/T/L
  **97-2-119**, mean **−1039**. Newest-12 ids `108445221…108326448` do
  **not** match the 09-13k set `108432563…108270318`. Autopsy
  `experiments/20260913l_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−3831**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-goose 9c5s3g (haonan zhengh `108412731` **−18535**, extra cow 218
  extra sheep 227 extra geese 242/266) plus extra-animal YARN 6c11s
  (Peter Cnudde `108383915` **−13315**, extra sheep 218/242/266 already
  bought) plus extra-animal 8c6s3g (Wei Han `108445221` **−12688**, extra
  sheep 218/227 extra geese 242/266) plus extra-sheep 11s (Oleg Smirnov
  `108345614` **−11762**, we already bought 227/242/266). BUY_LAND 151/266;
  cash_24 3–27; clone=12/12. Igor Aranovsky `108326448` already bought
  extra geese 227/242 and won 9c5s3g vs 9c9s +6833. Floth `108343489`
  already bought extra sheep 218/242/266 and won 4c14s vs 8c6s3g +4018
  — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13k.
  Mid-land 150 then 218–222 (two games 150/218/220/222; two 150/220/222),
  clone=0/4, wheat 333–598, goose mix 4g/2g/0g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913l/`: no new slug vs `_hunt_20260913k`.
  Public search newest still `crystalbaby/kaggriculture-v38-public-submission`
  (SHA `a2047ebd` Ahmed V38 Shop0909 144/648 + 288/712 overlay). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913l_study_packet.json`,
  `experiments/20260913l_cut16_rolling.json`,
  `experiments/20260913l_top10_games.json`,
  `experiments/20260913l_gate.json`.

## 2026-09-13m — cut 16 1693.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1693.4** (was 1692.2).
  Shopbag `56151155` **COMPLETE 1332.1**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T08:36:44`: heralces **rank 1981 / 1693.4**
  of 8849. Gold 21 let cats farm 2905.0. Rank 10 binghua 2968.1.
  Top: Majkel1337 3221.5 (live 3221.5), Mengfei Li 3079.0, THIRD FARM CLUB 3034.0.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 220 PUBLIC + 1 VALIDATION. All-public W/T/L
  **98-2-120**, mean **−1024**. Newest-12 ids `108472548…108311577` do
  **not** match the 09-13l set `108445221…108326448`. Autopsy
  `experiments/20260913m_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−1709**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Ju `108369265` **−17212**, extra sheep 218/227
  extra geese 242/266) plus extra-animal YARN 6c11s
  (wuwuwu `108432563` **−10575**, extra sheep 218/242/266 already
  bought) plus extra-animal 8c6s3g (linyifangzhenshuai `108426937`
  **−9514** / carlos-tagosaku `108429814` **−8454** / Brian Chua
  `108472548` **−659**) plus extra-sheep 16s (Artem The Farmer
  `108328160` **−8536**, we already bought 227/242/266). BUY_LAND 151/266;
  cash_24 3–24; clone=12/12. Joyal `108422886` already bought extra
  sheep 218/242/266 and won 6c11s vs 9c5s3g +27397. Andrey Shpigar
  `108461768` already bought extra sheep 227/242/266 and won 9c8s vs
  6c6s6g +1827 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13l.
  Mid-land 150 then 220–222 (all four 150/220/222), clone=0/4, wheat
  411–607, goose mix 0g/2g/0g/0g. Opening land is not a later-block
  license.
- Hunt (no cell exec) `_hunt_20260913m/`: new slug
  `aurax7/kaggriculture-shop-router-reactive-v4` writefile SHA
  `3dd123c5` day-6 144/648 + Shop0909 712 overlay (not licensed).
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6.
  Did not extract to candidates/. Did not re-extract rejected kernels.
  Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still
  h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913m_study_packet.json`,
  `experiments/20260913m_cut16_rolling.json`,
  `experiments/20260913m_top10_games.json`,
  `experiments/20260913m_gate.json`.

## 2026-09-13n — cut 16 1693.6; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1693.6** (was 1693.4).
  Shopbag `56151155` **COMPLETE 1332.1**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T09:36:46`: heralces **rank 1983 / 1693.6**
  of 8859. Gold 21 kyy666 2903.8. Rank 10 binghua 2966.1.
  Top: Majkel1337 3226.2 (live 3227.0), Mengfei Li 3074.7, Artem The Farmer 3048.2.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 222 PUBLIC + 1 VALIDATION. All-public W/T/L
  **99-2-121**, mean **−1003**. Newest-12 ids `108489181…108345614` do
  **not** match the 09-13m set `108472548…108311577`. Autopsy
  `experiments/20260913n_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−4515**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-goose 9c5s3g (haonan zhengh `108412731` **−18535**, extra cow 218
  extra sheep 227 extra geese 242/266) plus extra-animal YARN 6c11s
  (Peter Cnudde `108383915` **−13315**, extra sheep 218/242/266 already
  bought) plus extra-animal 8c6s3g (Wei Han `108445221` **−12688**) plus
  extra-sheep 11s (Oleg Smirnov `108345614` **−11762**, we already bought
  227/242/266) plus identical-clone (mmwstudy `108484081` **−65**).
  BUY_LAND 151/266; cash_24 3–22; clone=12/12. XiaoYan12 `108441448`
  already bought extra geese 227/242 and won 9c5s3g vs 6c6s6g +6450.
  Agentmaster `108489181` already bought extra geese 227/242 and won
  9c5s3g vs 9c5s4g +2699 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13m.
  Mid-land 150 then 218–222 (one 150/218/220/222; two 150/220/222; one
  150/218), clone=0/4, wheat 451–620, goose mix 2g/0g/0g/2g. Opening
  land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913n/`: new slug
  `ahmedberatozer/kaggriculture-v39-ready-before-the-rush` writefile SHA
  `708c7485` V39 reprint Shop0909 144/648 + 288/712 overlay (not licensed).
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6.
  Did not extract to candidates/. Did not re-extract rejected kernels.
  Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still
  h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913n_study_packet.json`,
  `experiments/20260913n_cut16_rolling.json`,
  `experiments/20260913n_top10_games.json`,
  `experiments/20260913n_gate.json`.

## 2026-09-13o — cut 16 1690.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1690.5** (was 1693.6).
  Shopbag `56151155` **COMPLETE 1328.0**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T10:37:34`: heralces **rank 1985 / 1690.5**
  of 8870. Gold 21 Thomas Tschinkel 2914.4. Rank 10 binghua 2964.8.
  Top: Majkel1337 3231.2 (live 3231.2), Mengfei Li 3078.3, Artem The Farmer 3037.7.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 223 PUBLIC + 1 VALIDATION. All-public W/T/L
  **99-2-122**, mean **−1007**. Newest-12 ids `108504670…108343489` do
  **not** match the 09-13n set `108489181…108345614`. Autopsy
  `experiments/20260913o_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−911**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Ju `108369265` **−17212**, extra sheep 218/227
  extra geese 242/266) plus extra-animal YARN 6c11s
  (wuwuwu `108432563` **−10575**, extra sheep 218/242/266 already
  bought) plus identical-clone (maverick_ss_26 `108504670` **−1920**,
  extra geese 227/242 already bought). BUY_LAND 151/266; cash_24 3–27;
  clone=12/12. Joyal `108422886` already bought extra sheep 218/242/266
  and won 6c11s vs 9c5s3g +27397. Floth `108343489` already bought extra
  sheep 218/242/266 and won 4c14s vs 8c6s3g +4018 — not a 227 wrap
  license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13n.
  Mid-land 150 then 218–222 (two 150/220/222; one 150/218; one
  150/218/220/222), clone=0/4, wheat 462–542, goose mix 0g/2g/0g/0g.
  Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260913o/`: new slug
  `yhay81/shop-router-0913` writefile SHA `77cf6772` day-6 144/648
  (not licensed). `wei111111/v46d-skill-rebuild-review-guide` analysis
  only. Author lists: no king rc5, no y3uanm v6, no Thomas new tree.
  Did not extract to candidates/. Did not re-extract rejected kernels.
  Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still
  h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913o_study_packet.json`,
  `experiments/20260913o_cut16_rolling.json`,
  `experiments/20260913o_top10_games.json`,
  `experiments/20260913o_gate.json`.

## 2026-09-13p — cut 16 1682.9; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1682.9** (was 1690.5).
  Shopbag `56151155` **COMPLETE 1328.0**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T11:37:05`: heralces **rank 1999 / 1682.9**
  of 8878. Gold 21 pupen_o 2919.9. Rank 10 binghua 2968.7.
  Top: Majkel1337 3235.1 (live 3235.1), Mengfei Li 3068.4, Artem The Farmer 3036.8.
- Upload-bail **(c)**: newest cut COMPLETE ≥1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a ≥1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 225 PUBLIC + 1 VALIDATION. All-public W/T/L
  **99-2-124**, mean **−1043**. Newest-12 ids `108520439…108351144` do
  **not** match the 09-13o set `108504670…108343489`. Autopsy
  `experiments/20260913p_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−4082**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-goose (haonan zhengh `108412731` **−18535**, extra cow 218 extra
  sheep 227 extra geese 242/266) plus extra-animal YARN 6c11s
  (Peter Cnudde `108383915` **−13315**, extra sheep 218/242/266 already
  bought) plus extra-animal 8c6s3g (Wei Han `108445221` **−12688**;
  Excluding `108520439` **−5345**, extra sheep 218/227 extra geese
  242/266) plus extra-sheep 15s (Hackoholics `108509931` **−4788**,
  extra sheep 218/242/266 already bought) plus identical-clone
  (mmwstudy `108484081` **−65**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3–27; clone=12/12. XiaoYan12 `108441448`
  already bought extra geese 227/242 and won 9c5s3g vs 6c6s6g +6450.
  Sean Peppers `108351144` already bought extra sheep 218/242/266 and
  won 4c15s vs 6c10s +2394 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13o.
  Mid-land 150 then 218–222 (three 150/220/222; one 150/218/220/222),
  clone=0/4, wheat 387–452, goose mix 0g/0g/0g/4g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913p/`: new slug
  `guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f` writefile
  SHA `708c7485` V39 reprint Shop0909 144/648 + 288/712 overlay
  (not licensed). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Did not extract to candidates/. Did not re-extract
  rejected kernels. Cut 12/13 stay Hold. Did not re-upload boatlee.
  Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913p_study_packet.json`,
  `experiments/20260913p_cut16_rolling.json`,
  `experiments/20260913p_top10_games.json`,
  `experiments/20260913p_gate.json`.

## 2026-09-13q — cut 16 1687.3; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1687.3** (was 1682.9).
  Shopbag `56151155` **COMPLETE 1315.6**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T12:37:09`: heralces **rank 1996 / 1687.3**
  of 8886. Gold 21 ra5anchor 2916.3. Rank 10 binghua 2964.6.
  Top: Majkel1337 3239.9 (live 3239.9), Mengfei Li 3072.1, Artem The Farmer 3064.4.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 226 PUBLIC + 1 VALIDATION. All-public W/T/L
  **100-2-124**, mean **-1000.8**. Newest-12 ids `108534412...108366745` do
  **not** match the 09-13p set `108520439...108351144`. Autopsy
  `experiments/20260913q_cut16_rolling.json`. Rolling **6-0-6**, mean
  **-533.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Ju `108369265` **-17212**, extra sheep 218/227 extra
  geese 242/266; linyifangzhenshuai `108426937` **-9514**; carlos-tagosaku
  `108429814` **-8454**; Brian Chua `108472548` **-659**) plus extra-animal
  YARN 6c11s (wuwuwu `108432563` **-10575**, extra sheep 218/242/266 already
  bought) plus identical-clone (maverick_ss_26 `108504670` **-1920**, extra
  geese 227/242 already bought). BUY_LAND 151/266; cash_24 3-24; clone=12/12.
  Joyal `108422886` already bought extra sheep 218/242/266 and won 6c11s vs
  9c5s3g +27397. zg l1218 `108534412` already bought extra sheep 218/242/266
  and won 6c12s vs 8c6s3g +8548 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13p.
  Mid-land 150 then 218-222 (three 150/220/222; one 150/218),
  clone=0/4, wheat 381-517, goose mix 0g/0g/0g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913q/`: new slug
  `ahmedberatozer/kaggriculture-v40-plans-that-fit-the-shops` writefile
  SHA `546c4224` V40 Shop0909 144/648 + 288/712 overlay
  (not licensed). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Did not extract to candidates/. Did not re-extract
  rejected kernels. Cut 12/13 stay Hold. Did not re-upload boatlee.
  Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913q_study_packet.json`,
  `experiments/20260913q_cut16_rolling.json`,
  `experiments/20260913q_top10_games.json`,
  `experiments/20260913q_gate.json`.

## 2026-09-13r — cut 16 1680.9; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1680.9** (was 1687.3).
  Shopbag `56151155` **COMPLETE 1315.6**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T13:37:38`: heralces **rank 2011 / 1680.9**
  of 8891. Gold 21 Civitasmass 2910.3. Rank 10 Subramanya N 2967.8.
  Top: Majkel1337 3244.1 (live 3244.1), Mengfei Li 3070.4, Artem The Farmer 3063.7.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 228 PUBLIC + 1 VALIDATION. All-public W/T/L
  **100-2-126**, mean **-1150.7**. Newest-12 ids `108550653...108377691` do
  **not** match the 09-13q set `108534412...108366745`. Autopsy
  `experiments/20260913r_cut16_rolling.json`. Rolling **3-0-9**, mean
  **-7018.0**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (AQiDA19 `108550653` **-21800**, extra sheep 218/227 extra
  geese 242/266; Hanaro `108545775` **-14377**; Wei Han `108445221` **-12688**;
  Excluding `108520439` **-5345**) plus extra-goose (haonan zhengh `108412731`
  **-18535**, extra cow 218 extra sheep 227 extra geese 242/266; Rafael Molina
  Castano `108377691` **-5101**, extra geese 227/242 already bought) plus
  extra-animal YARN 6c11s (Peter Cnudde `108383915` **-13315**, extra sheep
  218/242/266 already bought) plus extra-sheep 15s (Hackoholics `108509931`
  **-4788**, extra sheep 218/242/266 already bought) plus identical-clone
  (mmwstudy `108484081` **-65**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-27; clone=12/12.
  XiaoYan12 `108441448` already bought extra geese 227/242 and won 9c5s3g vs
  6c6s6g +6450 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13q.
  Mid-land 150 then 218-222 (one 150/218/220/222; three 150/220/222),
  clone=0/4, wheat 364-565, goose mix 4g/0g/0g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913r/`: new slugs
  `alperen5252525/kaggriculture-metacounter-r1` analysis no-writefile and
  `xuantianfengwu/kaggriculture-land-labor-capital-allocator` writefile
  SHA `b49709bd` heuristic 6-cow allocator (not licensed). Author lists:
  no Yusuke later-block, no king rc5, no y3uanm v6. Did not extract to
  candidates/. Did not re-extract rejected kernels. Cut 12/13 stay Hold.
  Did not re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913r_study_packet.json`,
  `experiments/20260913r_cut16_rolling.json`,
  `experiments/20260913r_top10_games.json`,
  `experiments/20260913r_gate.json`.

## 2026-09-13s — cut 16 1670.2; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1670.2** (was 1680.9).
  Shopbag `56151155` **COMPLETE 1319.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T14:36:51`: heralces **rank 2026 / 1670.2**
  of 8896. Gold 21 HowardLeeTW 2904.6. Rank 10 binghua 2964.4.
  Top: Majkel1337 3248.1 (live 3249.0), Mengfei Li 3065.3, Artem The Farmer 3060.9.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 230 PUBLIC + 1 VALIDATION. All-public W/T/L
  **100-2-128**, mean **-1226.1**. Newest-12 ids `108568560...108374873` do
  **not** match the 09-13r set `108550653...108377691`. Autopsy
  `experiments/20260913s_cut16_rolling.json`. Rolling **4-0-8**, mean
  **-1150.5**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-goose (alcanta `108568560` **-19224**, extra cow 218 extra sheep
  227 extra geese 242/266; Sophie555 `108374873` **-3339**, extra geese
  227/242 already bought) plus extra-animal 8c6s3g (linyifangzhenshuai
  `108426937` **-9514**; carlos-tagosaku `108429814` **-8454**; Brian Chua
  `108472548` **-659**, extra sheep 218/227 extra geese 242/266) plus
  extra-animal YARN 6c11s (wuwuwu `108432563` **-10575**; Farmer Shuang
  `108559476` **-418**, extra sheep 218/242/266 already bought) plus
  identical-clone (maverick_ss_26 `108504670` **-1920**, extra geese
  227/242 already bought). BUY_LAND 151/266; cash_24 3-24; clone=12/12.
  Joyal `108422886` already bought extra sheep 218/242/266 and won 6c11s
  vs 9c5s3g +27397 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13r.
  Mid-land 150 then 218-222 (three 150/220/222; one 150/218/220/222),
  clone=0/4, wheat 466-510, goose mix 0g/4g/2g/0g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913s/`: new slug
  `renjistarfall/kaggriculture-best-agent` writefile SHA `708c7485` V39
  reprint Shop0909 144/648 + 288/712 overlay (not licensed). Author
  lists: no Yusuke later-block, no king rc5, no y3uanm v6. Did not
  extract to candidates/. Did not re-extract rejected kernels. Cut
  12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still h2
  SHA `65e6f5cd...`.
- JSON: `experiments/20260913s_study_packet.json`,
  `experiments/20260913s_cut16_rolling.json`,
  `experiments/20260913s_top10_games.json`,
  `experiments/20260913s_gate.json`.

## 2026-09-13t — cut 16 1673.8; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1673.8** (was 1670.2).
  Shopbag `56151155` **COMPLETE 1314.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T15:37:20`: heralces **rank 2027 / 1673.8**
  of 8902. Gold 21 Xiangyu Liu 2908.8. Rank 10 Catalyst 2958.0.
  Top: Majkel1337 3252.7 (live 3252.7), Artem The Farmer 3076.9, Mengfei Li 3047.5.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 231 PUBLIC + 1 VALIDATION. All-public W/T/L
  **101-2-128**, mean **-1220.7**. Newest-12 ids `108586169...108383915` do
  **not** match the 09-13s set `108568560...108374873`. Autopsy
  `experiments/20260913t_cut16_rolling.json`. Rolling **4-0-8**, mean
  **-6592.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (AQiDA19 `108550653` **-21800**, extra sheep 218/227 extra
  geese 242/266; Hanaro `108545775` **-14377**; Wei Han `108445221` **-12688**;
  Excluding `108520439` **-5345**) plus extra-goose (haonan zhengh `108412731`
  **-18535**, extra cow 218 extra sheep 227 extra geese 242/266) plus
  extra-animal YARN 6c11s (Peter Cnudde `108383915` **-13315**, extra sheep
  218/242/266 already bought) plus extra-sheep 15s (Hackoholics `108509931`
  **-4788**, extra sheep 218/242/266 already bought) plus identical-clone
  (mmwstudy `108484081` **-65**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-27; clone=12/12.
  maxout `108586169` already bought extra geese 227/242 and won identical-clone
  9c5s3g vs 9c5s3g +8 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13s.
  Mid-land 150 then 218-222 (two 150/220/222; two 150/218/220/222),
  clone=0/4, wheat 425-590, goose mix 2g/2g/0g/4g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913t/`: no new slug vs `_hunt_20260913s`.
  Public search newest still `renjistarfall/kaggriculture-best-agent`
  SHA `708c7485` V39 reprint Shop0909 144/648 + 288/712 overlay (already
  rejected 0913s). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py`
  still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913t_study_packet.json`,
  `experiments/20260913t_cut16_rolling.json`,
  `experiments/20260913t_top10_games.json`,
  `experiments/20260913t_gate.json`.

## 2026-09-13u — cut 16 1669.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1669.1** (was 1673.8).
  Shopbag `56151155` **COMPLETE 1314.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T16:36:51`: heralces **rank 2040 / 1669.1**
  of 8908. Gold 21 chocolat 2908.7. Rank 10 THIRD FARM CLUB 2956.0.
  Top: Majkel1337 3255.3 (live 3255.3), Artem The Farmer 3085.4, Mengfei Li 3053.6.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 232 PUBLIC + 1 VALIDATION. All-public W/T/L
  **101-2-129**, mean **-1220.1**. Newest-12 ids `108594800...108399266` do
  **not** match the 09-13t set `108586169...108383915`. Autopsy
  `experiments/20260913u_cut16_rolling.json`. Rolling **4-0-8**, mean
  **-962.8**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (linyifangzhenshuai `108426937` **-9514**, extra sheep
  218/227 extra geese 242/266; carlos-tagosaku `108429814` **-8454**; Brian
  Chua `108472548` **-659**) plus extra-goose (alcanta `108568560` **-19224**,
  extra cow 218 extra sheep 227 extra geese 242/266; higuuu `108594800`
  **-1087**, extra geese 227/242 already bought) plus extra-animal YARN 6c11s
  (wuwuwu `108432563` **-10575**; Farmer Shuang `108559476` **-418**, extra
  sheep 218/242/266 already bought) plus identical-clone (maverick_ss_26
  `108504670` **-1920**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-24; clone=12/12.
  Joyal `108422886` already bought extra sheep 218/242/266 and won 6c11s vs
  9c5s3g +27397 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13t.
  Mid-land 150 then 218-222 (three 150/220/222; one 150/218/220/222),
  clone=0/4, wheat 367-506, goose mix 2g/2g/0g/4g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913u/`: no new slug vs `_hunt_20260913t`.
  Public search newest still `renjistarfall/kaggriculture-best-agent`
  SHA `708c7485` V39 reprint Shop0909 144/648 + 288/712 overlay (already
  rejected 0913s). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py`
  still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913u_study_packet.json`,
  `experiments/20260913u_cut16_rolling.json`,
  `experiments/20260913u_top10_games.json`,
  `experiments/20260913u_gate.json`.

## 2026-09-13v — cut 16 1681.2; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1681.2** (was 1669.1).
  Shopbag `56151155` **COMPLETE 1314.5**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-13T17:38:14`: heralces **rank 2022 / 1681.2**
  of 8911. Gold 21 pupen_o 2901.3. Rank 10 binghua 2953.0.
  Top: Majkel1337 3259.2 (live 3259.2), Artem The Farmer 3091.9, Mengfei Li 3046.3.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 234 PUBLIC + 1 VALIDATION. All-public W/T/L
  **103-2-129**, mean **−1167.1**. Newest-12 ids `108608562...108441305` do
  **not** match the 09-13u set `108594800...108399266`. Autopsy
  `experiments/20260913v_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−3106.3**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (AQiDA19 `108550653` **−21800**, extra sheep 218/227 extra
  geese 242/266; Hanaro `108545775` **−14377**; Wei Han `108445221` **−12688**;
  Excluding `108520439` **−5345**) plus extra-sheep 15s (Hackoholics `108509931`
  **−4788**, extra sheep 218/242/266 already bought) plus identical-clone
  (mmwstudy `108484081` **−65**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-27; clone=12/12.
  dupakdungking `108608562` already bought extra sheep 218/242/266 and won
  6c12s vs 8c6s3g +9867 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13u.
  Mid-land 150 then 218-222 (two 150/220/222; one 150/218/220/222; one 150/218),
  clone=0/4, wheat 372-571, goose mix 4g/0g/2g/0g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260913v/`: no new slug vs `_hunt_20260913u`.
  Public search newest still `renjistarfall/kaggriculture-best-agent`
  SHA `708c7485` V39 reprint Shop0909 144/648 + 288/712 overlay (already
  rejected 0913s). Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py`
  still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260913v_study_packet.json`,
  `experiments/20260913v_cut16_rolling.json`,
  `experiments/20260913v_top10_games.json`,
  `experiments/20260913v_gate.json`.

## 2026-09-14 — cut 16 1654.7; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1654.7** (was 1681.2).
  Shopbag `56151155` **COMPLETE 1309.4**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T01:41:29`: heralces **rank 2068 / 1654.7**
  of 8938. Gold 21 アルモンド 2926.0. Rank 10 Otter Vibe 2948.5.
  Top: Majkel1337 3189.8 (live 3189.8 scoring-sub `56156662`; current
  sub `56216119` is 2778.2), SpaTaro 3047.9, ymg_aq 3022.7.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 244 PUBLIC + 1 VALIDATION. All-public W/T/L
  **105-2-137**, mean **−1422.4**. Newest-12 ids `108723413...108568560` do
  **not** match the 09-13v set `108608562...108441305`. Autopsy
  `experiments/20260914_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−7857.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (LuanHengYu `108636667` **−20223**, extra sheep
  218/227 extra geese 242/266; Les 2 oies `108642657` **−12935**; BigAngel
  `108635673` **−5892**) plus extra-sheep 8c9s/16s/15s (Pietro Valocchi
  `108658948` **−12549**; Gracie `108656070` **−14565** clone=0; Akhil
  Chinta `108620320` **−1911**, extra sheep 218/242/266 already bought)
  plus extra-goose (alcanta `108568560` **−19224**, extra cow 218 extra
  sheep 227 extra geese 242/266; here we go `108704919` **−7788**; higuuu
  `108594800` **−1087**) plus identical-clone (Cuong Le `108686716`
  **−590**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-27; clone=11/12.
  zard599 `108723413` already bought extra geese 227/242 and won 9c5s3g vs
  9c5s4g +748 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-13v.
  Mid-land 150 then 218-222 (three 150/220/222; one 150/218),
  clone=0/4, wheat 469-569, goose 2g/2g/2g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260914/`: 5 new slugs vs `_hunt_20260913v`.
  Public search newest `nathanjacob/no-cow-left-behind-v40-autopsy-fix`
  analysis/dataset wrapper (no writefile). Ahmed V41 SHA `8951ff93`
  Shop0909 144/648 + 288/712 overlay. alperen scored-agent SHA `85c8b532`
  day-6 144/648 overlay. xuantianfengwu adaptive-land-allocator SHA
  `d12f2987` heuristic 6-cow. prvsiyan reserve-garden educational.
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6. Did
  not extract to candidates/. Did not re-extract rejected kernels. Cut
  12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still h2
  SHA `65e6f5cd...`.
- JSON: `experiments/20260914_study_packet.json`,
  `experiments/20260914_cut16_rolling.json`,
  `experiments/20260914_top10_games.json`,
  `experiments/20260914_gate.json`.

## 2026-09-14b — cut 16 1644.6; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1644.6** (was 1654.7).
  Shopbag `56151155` **COMPLETE 1310.6**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T02:42:53`: heralces **rank 2088 / 1644.6**
  of 8938. Gold 21 nilochan 2925.8. Rank 10 Otter Vibe 2954.1.
  Top: Majkel1337 3197.1 (live 3197.1 scoring-sub `56156662`; current
  sub `56216119` is 2870.6), SpaTaro 3053.2, ymg_aq 3024.6.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 248 PUBLIC + 1 VALIDATION. All-public W/T/L
  **106-2-140**, mean **−1487.6**. Newest-12 ids `108753975…108520439` do
  **not** match the 09-14 set `108723413…108568560`. Autopsy
  `experiments/20260914b_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−3771.8**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (AQiDA19 `108550653` **−21800**, extra sheep
  218/227 extra geese 242/266; Hanaro `108545775` **−14377**; Quillbolt
  `108753975` **−9650**, extra sheep 218/242/266 already bought; Excluding
  `108520439` **−5345**) plus extra-sheep 11s (higuuu `108751924`
  **−3065**, extra sheep 218/227/242/266 already bought) plus extra-animal
  YARN 6c11s (Farmer Shuang `108559476` **−418**, extra sheep 218/242/266
  already bought) plus identical-clone extra-goose (我是刘大聪 `108744906`
  **−9197**, extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-27; clone=12/12.
  y3uanm `108741805` already bought extra geese 227/242 and won identical-clone
  9c5s3g vs 9c5s3g +54 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14.
  Mid-land 150 then 220-222 (four 150/220/222), clone=0/4, wheat 441-508,
  goose mix 3g/0g/2g/2g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914b/`: no new slug vs `_hunt_20260914`.
  Public search newest still `nathanjacob/no-cow-left-behind-v40-autopsy-fix`
  analysis/dataset wrapper (already rejected 0914). Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914b_study_packet.json`,
  `experiments/20260914b_cut16_rolling.json`,
  `experiments/20260914b_top10_games.json`,
  `experiments/20260914b_gate.json`.

## 2026-09-14c — cut 16 1639.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1639.4** (was 1644.6).
  Shopbag `56151155` **COMPLETE 1310.6**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T03:42:10`: heralces **rank 2093 / 1639.4**
  of 8940. Gold 21 Cow Boy 2926.7. Rank 10 redblackbst 2952.2.
  Top: Majkel1337 3191.4 (live 3191.4 scoring-sub `56156662`; current
  sub `56216119` is 2925.9), SpaTaro 3049.9, ymg_aq 3024.2.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 249 PUBLIC + 1 VALIDATION. All-public W/T/L
  **106-2-141**, mean **−1507.0**. Newest-12 ids `108762693…108594800` do
  **not** match the 09-14b set `108753975…108520439`. Autopsy
  `experiments/20260914c_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−6781.9**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (LuanHengYu `108636667` **−20223**, extra sheep
  218/227 extra geese 242/266; Les 2 oies `108642657` **−12935**; итмоняяя
  `108762693` **−6320**, extra sheep 227/242/266 already bought; BigAngel
  `108635673` **−5892**) plus extra-sheep (Gracie `108656070` **−14565**
  clone=0 extra sheep 227/242/266 already bought; Pietro Valocchi
  `108658948` **−12549**; Akhil Chinta `108620320` **−1911**, extra sheep
  218/242/266 already bought) plus extra-goose (here we go `108704919`
  **−7788**; higuuu `108594800` **−1087**, extra geese 227/242 already
  bought) plus identical-clone extra-goose (Cuong Le `108686716` **−590**,
  extra geese 227/242 already bought).
  BUY_LAND 151/266; cash_24 3-27; clone=11/12.
  zard599 `108723413` already bought extra geese 227/242 and won 9c5s3g vs
  9c5s4g +748 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14b.
  Mid-land 150 then 218-222 (two 150/220/222; one 150/218/220/222; one
  150/218/219/222/226-229), clone=0/4, wheat 439-569, goose 3g/2g/2g/2g.
  Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914c/`: no new slug vs `_hunt_20260914b`.
  Public search newest still `nathanjacob/no-cow-left-behind-v40-autopsy-fix`
  analysis/dataset wrapper (already rejected 0914/0914b). Author lists: no
  Yusuke later-block, no king rc5, no y3uanm v6. Did not extract to
  candidates/. Did not re-extract rejected kernels. Cut 12/13 stay Hold.
  Did not re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914c_study_packet.json`,
  `experiments/20260914c_cut16_rolling.json`,
  `experiments/20260914c_top10_games.json`,
  `experiments/20260914c_gate.json`.

## 2026-09-14d — cut 16 1640.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1640.5** (was 1639.4).
  Shopbag `56151155` **COMPLETE 1310.6**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T04:42:02`: heralces **rank 2089 / 1640.5**
  of 8946. Gold 21 goosehaaan 2922.3. Rank 10 feel the agi 2964.7.
  Top: Majkel1337 3196.8 (live 3196.8 scoring-sub `56156662`; current
  sub `56216119` is 2944.9), SpaTaro 3038.7, ymg_aq 3020.6.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 251 PUBLIC + 1 VALIDATION. All-public W/T/L
  **107-2-142**, mean **−1501.2**. Newest-12 ids `108784373…108550653` do
  **not** match the 09-14c set `108762693…108594800`. Autopsy
  `experiments/20260914d_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−4571.9**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (AQiDA19 `108550653` **−21800**, extra sheep
  218/227 extra geese 242/266; Quillbolt `108753975` **−9650**, extra
  sheep 218/242/266 already bought) plus extra-goose (alcanta `108568560`
  **−19224**, extra cow 218 extra sheep 227 extra geese 242/266; bplyc15
  `108784373` **−7879**) plus identical-clone extra-goose (我是刘大聪
  `108744906` **−9197**, extra geese 227/242 already bought) plus
  extra-sheep (higuuu `108751924` **−3065**, extra sheep 218/227/242/266
  already bought) plus extra-animal YARN (Farmer Shuang `108559476`
  **−418**, extra sheep 218/242/266 already bought).
  BUY_LAND 151/266; cash_24 3-25; clone=12/12.
  DASH村 `108781918` already bought extra sheep 218/242/266 and won 4c14s
  vs 6c6s5g +6327 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14c.
  Mid-land 150 then 218-222 (three 150/220/222; one 150/218/220/222),
  clone=1/4, wheat 449-576, goose 0g/0g/2g/4g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260914d/`: 3 new slugs vs `_hunt_20260914c`.
  Public search newest `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. `aurax7/kaggriculture-shop-router-reactive-v5`
  SHA `ea4c28e6` Shop0909 144/648 + 288/712 overlay. `lime0001/t23-kaggriculture-smart-adaptive-harvest`
  SHA `31ee22dc` Shop0909 overlay. Author lists: no Yusuke later-block, no
  king rc5, no y3uanm v6. Did not extract to candidates/. Did not
  re-extract rejected kernels. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914d_study_packet.json`,
  `experiments/20260914d_cut16_rolling.json`,
  `experiments/20260914d_top10_games.json`,
  `experiments/20260914d_gate.json`.

## 2026-09-14e — cut 16 1637.6; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1637.6** (was 1640.5).
  Shopbag `56151155` **COMPLETE 1309.1**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T05:46:19`: heralces **rank 2103 / 1637.6**
  of 8949. Gold 21 Gleb Tumanov 2920.8. Rank 10 feel the agi 2961.4.
  Top: Majkel1337 3202.7 (live 3202.7 scoring-sub `56156662`; current
  sub `56216119` is 2951.8), SpaTaro 3021.1, DSM 3015.5.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 252 PUBLIC + 1 VALIDATION. All-public W/T/L
  **107-2-143**, mean **−1522.9**. Newest-12 ids `108787437…108620320` do
  **not** match the 09-14d set `108784373…108550653`. Autopsy
  `experiments/20260914e_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−7273.5**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (LuanHengYu `108636667` **−20223**, extra sheep
  218/227 extra geese 242/266; Les 2 oies `108642657` **−12935**;
  итмоняяя `108762693` **−6320**, extra sheep 227/242/266 already bought;
  BigAngel `108635673` **−5892**) plus extra-sheep (Gracie `108656070`
  **−14565** clone=0; Pietro Valocchi `108658948` **−12549**; Akhil
  Chinta `108620320` **−1911**) plus extra-goose (here we go `108704919`
  **−7788**; Toru59er `108787437` **−6986**) plus identical-clone
  extra-goose (Cuong Le `108686716` **−590**). BUY_LAND 151/266;
  cash_24 3-27; clone=11/12.
  zard599 `108723413` already bought extra geese 227/242 and won 9c5s3g
  vs 9c5s4g +748 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14d.
  Mid-land 150 then 218-225 (two 150/218/220/222; one 150/218/225; one
  150/220/222), clone=0/4, wheat 407-663, goose 4g/4g/4g/0g. Opening
  land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914e/`: 1 new slug vs `_hunt_20260914d`.
  Public search newest still `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. `arsgorynich/kaggriculture-v40-challenger`
  SHA `546c4224` Ahmed V40 reprint Shop0909 144/648 + 288/712 overlay.
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6. Did
  not extract to candidates/. Did not re-extract rejected kernels. Cut
  12/13 stay Hold. Did not re-upload boatlee. Root `main.py` still h2
  SHA `65e6f5cd...`.
- JSON: `experiments/20260914e_study_packet.json`,
  `experiments/20260914e_cut16_rolling.json`,
  `experiments/20260914e_top10_games.json`,
  `experiments/20260914e_gate.json`.

## 2026-09-14f — cut 16 1643.7; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1643.7** (was 1637.6).
  Shopbag `56151155` **COMPLETE 1304.9**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T06:42:14`: heralces **rank 2096 / 1643.7**
  of 8952. Gold 21 keiz 2920.0. Rank 10 HowardLeeTW 2973.5.
  Top: Majkel1337 3195.5 (live 3195.5 scoring-sub `56156662`; current
  sub `56216119` is 2961.5), SpaTaro 3024.2, DSM 3014.3.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 255 PUBLIC + 1 VALIDATION. All-public W/T/L
  **109-2-144**, mean **−1511.3**. Newest-12 ids `108814509…108594800` do
  **not** match the 09-14e set `108787437…108620320`. Autopsy
  `experiments/20260914f_cut16_rolling.json`. Rolling **6-0-6**, mean
  **−1343.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Quillbolt `108753975` **−9650**, extra sheep
  218/227 extra geese 242/266 already bought extra sheep 218/242/266)
  plus identical-clone extra-goose (我是刘大聪 `108744906` **−9197**, extra
  geese 227/242 already bought) plus extra-goose (bplyc15 `108784373`
  **−7879**, extra cow 218 extra sheep 227 extra geese 242/266; higuuu
  `108594800` **−1087**) plus identical-clone extra-sheep (trung
  `108814509` **−5487**, extra sheep 218/242/266 already bought) plus
  extra-sheep (higuuu `108751924` **−3065**, extra sheep 227/242/266
  already bought). BUY_LAND 151/266; cash_24 3-27; clone=12/12.
  DASH村 `108781918` already bought extra sheep 218/242/266 and won 4c14s
  vs 6c6s5g +6327 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14e.
  Mid-land 150 then 220-222 (one 150/220; three 150/220/222),
  clone=1/4, wheat 393-519, goose 2g/0g/2g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260914f/`: no new slug vs `_hunt_20260914e`.
  Public search newest still `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. Author lists: no Yusuke later-block, no
  king rc5, no y3uanm v6. Did not extract to candidates/. Did not
  re-extract rejected kernels. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914f_study_packet.json`,
  `experiments/20260914f_cut16_rolling.json`,
  `experiments/20260914f_top10_games.json`,
  `experiments/20260914f_gate.json`.

## 2026-09-14g — cut 16 1636.0; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1636.0** (was 1643.7).
  Shopbag `56151155` **COMPLETE 1304.9**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T07:42:06`: heralces **rank 2108 / 1636.0**
  of 8961. Gold 21 Cow Boy 2914.3. Rank 10 HowardLeeTW 2978.3.
  Top: Majkel1337 3200.6 (live 3200.6 scoring-sub `56156662`; current
  sub `56216119` is 2975.6), SpaTaro 3019.0, ymg_aq 3014.3.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 257 PUBLIC + 1 VALIDATION. All-public W/T/L
  **109-2-146**, mean **−1566.7**. Newest-12 disjoint-from-14f ids
  `108822458…108636667` do **not** match the 09-14f set
  `108814509…108594800`. Autopsy
  `experiments/20260914g_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−8060.3**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (LuanHengYu `108636667` **−20223**, extra sheep
  218/227 extra geese 242/266; Les 2 oies `108642657` **−12935**; HaoChi
  `108817790` **−6212**, extra cow 218 vs opp extra sheep 218/227 extra
  geese 242/266) plus extra-sheep (Gracie `108656070` **−14565**, extra
  sheep 227/242/266 already bought; Pietro Valocchi `108658948`
  **−12549**; Revanth Tambisetty `108822458` **−11033**, extra sheep
  218/242/266 already bought) plus extra-goose (here we go `108704919`
  **−7788**; Toru59er `108787437` **−6986**) plus identical-clone
  extra-goose (Cuong Le `108686716` **−590**). BUY_LAND 151/266; cash_24
  3-27; clone=11/12. zard599 `108723413` already bought extra geese
  227/242 and won 9c5s3g vs 9c5s4g +748 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14f.
  Mid-land 150 then 218-222 (three 150/220/222; one 150/218),
  clone=2/4, wheat 452-571, goose 0g/0g/0g/0g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260914g/`: no new slug vs `_hunt_20260914f`.
  Public search newest still `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. Author lists: no Yusuke later-block, no
  king rc5, no y3uanm v6. Did not extract to candidates/. Did not
  re-extract rejected kernels. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914g_study_packet.json`,
  `experiments/20260914g_cut16_rolling.json`,
  `experiments/20260914g_top10_games.json`,
  `experiments/20260914g_gate.json`.

## 2026-09-14h — cut 16 1636.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1636.5** (was 1636.0).
  Shopbag `56151155` **COMPLETE 1298.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T08:43:29`: heralces **rank 2114 / 1636.5**
  of 8968. Gold 21 Crop Dustas 2917.3. Rank 10 Orbital Terraformer 2969.6.
  Top: Majkel1337 3204.0 (live 3204.0 scoring-sub `56156662`; current
  sub `56216119` is 2977.7), SpaTaro 3024.7, Artem The Farmer 3021.5.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 259 PUBLIC + 1 VALIDATION. All-public W/T/L
  **110-2-147**, mean **−1576.3**. Newest-12 disjoint-from-14g ids
  `108846707…108635673` do **not** match the 09-14g set
  `108822458…108636667`. Autopsy
  `experiments/20260914h_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−3044.6**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Quillbolt `108753975` **−9650**, extra sheep
  218/242/266 already bought vs opp extra sheep 218/227 extra geese
  242/266; BigAngel `108635673` **−5892**, extra cow 218) plus extra-goose
  (bplyc15 `108784373` **−7879**; Scorn100 `108846707` **−5681**, extra
  sheep 227/242/266 already bought vs 6g) plus identical-clone extra-goose
  (我是刘大聪 `108744906` **−9197**) plus identical-clone extra-sheep
  (trung `108814509` **−5487**) plus extra-sheep (higuuu `108751924`
  **−3065**). BUY_LAND 151/266; cash_24 3-27; clone=12/12. DASH村
  `108781918` already bought extra sheep 218/242/266 and won 4c14s vs
  6c6s5g +6327 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14g.
  Mid-land 150 then 218-222 (one 150/218/220/222; three 150/220/222),
  clone=0/4, wheat 442-651, goose 2g/0g/0g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260914h/`: no new slug vs `_hunt_20260914g`.
  Public search newest still `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. Author lists: no Yusuke later-block, no
  king rc5, no y3uanm v6. Did not extract to candidates/. Did not
  re-extract rejected kernels. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914h_study_packet.json`,
  `experiments/20260914h_cut16_rolling.json`,
  `experiments/20260914h_top10_games.json`,
  `experiments/20260914h_gate.json`.

## 2026-09-14i — cut 16 1632.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1632.1** (was 1636.5).
  Shopbag `56151155` **COMPLETE 1298.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T09:47:25`: heralces **rank 2124 / 1632.1**
  of 8980. Gold 21 Cow Boy 2924.1. Rank 10 Orbital Terraformer 2968.7.
  Top: Majkel1337 3208.0 (live 3208.0 scoring-sub `56156662`; current
  sub `56216119` is 2998.1), SpaTaro 3036.0, Artem The Farmer 3033.1.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 260 PUBLIC + 1 VALIDATION. All-public W/T/L
  **110-2-148**, mean **−1632.1**. Newest-12 disjoint-from-14h ids
  `108851261…108642657` do **not** match the 09-14h set
  `108846707…108635673`. Autopsy
  `experiments/20260914i_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−7716.1**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Les 2 oies `108642657` **−12935**, extra sheep
  218/227 extra geese 242/266; HaoChi `108817790` **−6212**, extra cow
  218; итмоняяя `108762693` **−6320**) plus extra-sheep (Gracie
  `108656070` **−14565**, extra sheep 227/242/266 already bought; Pietro
  Valocchi `108658948` **−12549**; Revanth Tambisetty `108822458`
  **−11033**, extra sheep 218/242/266 already bought) plus extra-goose
  (LaiCxm `108851261` **−16092**, extra cow 218 extra sheep 227 extra
  geese 242/266; here we go `108704919` **−7788**; Toru59er `108787437`
  **−6986**) plus identical-clone extra-goose (Cuong Le `108686716`
  **−590**). BUY_LAND 151/266; cash_24 3-22; clone=11/12. zard599
  `108723413` already bought extra geese 227/242 and won 9c5s3g vs
  9c5s4g +748 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14h.
  Mid-land 150 then 218-222 (two 150/220/222; two 150/218),
  clone=1/4, wheat 388-494, goose 2g/4g/2g/2g. Opening land is not
  a later-block license.
- Hunt (no cell exec) `_hunt_20260914i/`: no new slug vs `_hunt_20260914h`.
  Public search newest still `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. Author lists: no Yusuke later-block, no
  king rc5, no y3uanm v6. Did not extract to candidates/. Did not
  re-extract rejected kernels. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914i_study_packet.json`,
  `experiments/20260914i_cut16_rolling.json`,
  `experiments/20260914i_top10_games.json`,
  `experiments/20260914i_gate.json`.

## 2026-09-14j — cut 16 1627.8; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1627.8** (was 1632.1).
  Shopbag `56151155` **COMPLETE 1298.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T10:41:40`: heralces **rank 2120 / 1627.8**
  of 8984. Gold 21 Deodims 2928.9. Rank 10 Thomas Tschinkel 2974.0.
  Top: Majkel1337 3211.7 (live 3213.9 scoring-sub `56156662`; current
  sub `56216119` is 3008.3), SpaTaro 3043.0, Artem The Farmer 3040.0.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 261 PUBLIC + 1 VALIDATION. All-public W/T/L
  **110-2-149**, mean **−1650.9**. Newest-12 disjoint-from-14i ids
  `108871316…108741805` do **not** match the 09-14i set
  `108851261…108642657`. Autopsy
  `experiments/20260914j_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−3097.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Quillbolt `108753975` **−9650**, extra sheep
  218/242/266 already bought vs opp extra sheep 218/227 extra geese
  242/266) plus extra-goose (bplyc15 `108784373` **−7879**; Scorn100
  `108846707` **−5681**; refine123 `108871316` **−6523**, extra geese
  227/242 already bought vs 4g) plus identical-clone extra-goose (我是刘大聪
  `108744906` **−9197**) plus identical-clone extra-sheep (trung
  `108814509` **−5487**) plus extra-sheep (higuuu `108751924` **−3065**).
  BUY_LAND 151/266; cash_24 3-27; clone=12/12. Cathy `108842428` already
  bought extra geese 227/242 and won identical-clone +51 — not a 227 wrap
  license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14i.
  Mid-land 150 then 220-222 (all four 150/220/222), clone=0/4, wheat
  391-659, goose 0g/2g/2g/0g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914j/`: no new slug vs `_hunt_20260914i`.
  Public search newest still `xuantianfengwu/kaggriculture-adaptive-land-allocator-r10`
  SHA `3b8a1d4d` heuristic 6-cow. Author lists: no Yusuke later-block, no
  king rc5, no y3uanm v6. Did not extract to candidates/. Did not
  re-extract rejected kernels. Cut 12/13 stay Hold. Did not re-upload
  boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914j_study_packet.json`,
  `experiments/20260914j_cut16_rolling.json`,
  `experiments/20260914j_top10_games.json`,
  `experiments/20260914j_gate.json`.

## 2026-09-14k — cut 16 1619.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1619.1** (was 1627.8).
  Shopbag `56151155` **COMPLETE 1295.7**. Cut 15 `56146106` **1864.4**
  (dropped). CSV `2026-09-14T11:41:49`: heralces **rank 2158 / 1619.1**
  of 9000. Gold 21 binghua 2931.0. Rank 10 Thomas Tschinkel 2974.5.
  Top: Majkel1337 3217.8 (live 3217.8 scoring-sub `56156662`; current
  sub `56216119` is 3029.6), Artem The Farmer 3048.7, SpaTaro 3026.0.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 263 PUBLIC + 1 VALIDATION. All-public W/T/L
  **110-2-151**, mean **−1692.4**. Newest-12 disjoint-from-14j ids
  `108889446…108658948` do **not** match the 09-14j set
  `108871316…108741805`. Autopsy
  `experiments/20260914k_cut16_rolling.json`. Rolling **2-0-10**, mean
  **−6609.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (HaoChi `108817790` **−6212**; итмоняяя
  `108762693` **−6320**) plus extra-goose (LaiCxm `108851261` **−16092**,
  extra cow 218 extra sheep 227 extra geese 242/266; here we go
  `108704919` **−7788**; Toru59er `108787437` **−6986**) plus extra-sheep
  (Pietro Valocchi `108658948` **−12549**; Revanth Tambisetty `108822458`
  **−11033**; Adhiraj Jagtap `108889378` **−2087**) plus identical-clone
  extra-sheep (Варим сельский самогон `108889446` **−12131**) plus
  identical-clone extra-goose (Cuong Le `108686716` **−590**). BUY_LAND
  151/266; cash_24 3-22; clone=12/12. zard599 `108723413` already bought
  extra geese 227/242 and won 9c5s3g vs 9c5s4g +748 — not a 227 wrap
  license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14j.
  Mid-land 150 then 218-222 (two 150/218/220/222; one 150/220; one
  150/220/222), clone=0/4, wheat 356-472, goose 4g/2g/0g/4g. Opening
  land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914k/`: 3 new slugs vs `_hunt_20260914j`
  (`sorcererbi/your-offline-arena-is-lying-to-you`,
  `where-does-your-score-actually-come-from`,
  `how-to-a-b-two-agents-properly`). All analysis notebooks, no
  `%%writefile`, no later-block. Public search newest
  `sorcererbi/your-offline-arena-is-lying-to-you`. Author lists: no
  Yusuke later-block, no king rc5, no y3uanm v6. Did not extract to
  candidates/. Did not re-extract rejected kernels. Cut 12/13 stay Hold.
  Did not re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914k_study_packet.json`,
  `experiments/20260914k_cut16_rolling.json`,
  `experiments/20260914k_top10_games.json`,
  `experiments/20260914k_gate.json`.

## 2026-09-14l — cut 16 1619.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1619.1**.
  Shopbag `56151155` **COMPLETE 1300.3** (was 1295.7). Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-14T12:42:08`: heralces **rank 2156 /
  1619.1** of 9003. Gold 21 lucaskna 2929.5. Rank 10 Unknown Mother-Goose
  2973.7. Top: Majkel1337 3220.4 (live 3220.4 scoring-sub `56156662`;
  current sub `56216119` is 3030.9), Artem The Farmer 3047.5, SpaTaro
  3031.2.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 263 PUBLIC + 1 VALIDATION. All-public W/T/L
  **110-2-151**, mean **−1692.4**. Newest-12 disjoint-from-14k ids
  `108871316…108741805` do **not** match the 09-14k set
  `108889446…108658948`. Autopsy
  `experiments/20260914l_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−3097.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Quillbolt `108753975` **−9650**) plus extra-goose
  (bplyc15 `108784373` **−7879**, extra cow 218 extra sheep 227 extra
  geese 242/266; Scorn100 `108846707` **−5681**; refine123 `108871316`
  **−6523**) plus identical-clone extra-goose (我是刘大聪 `108744906`
  **−9197**) plus identical-clone extra-sheep (trung `108814509`
  **−5487**) plus extra-sheep (higuuu `108751924` **−3065**). BUY_LAND
  151/266; cash_24 3-27; clone=12/12. Cathy `108842428` already bought
  extra geese 227/242 and won identical-clone +51 — not a 227 wrap
  license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14k.
  Mid-land 150 then 218-222 (one 150/218/220/222; three 150/220/222),
  clone=0/4, wheat 416-489, goose 4g/3g/2g/0g. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260914l/`: 1 new slug vs `_hunt_20260914k`
  (`rohitt94/kaggriculture-route-replay-agent`). Python `%%writefile
  main.py` SHA `62a80706` Shop0909 144/648 + 288 four-turn + 712 planner;
  distinct from aurax7 v5 `ea4c28e6`. Not later-block. Public search
  newest `rohitt94/kaggriculture-route-replay-agent`. Author lists: no
  Yusuke later-block, no king rc5, no y3uanm v6. Writefile hashed in hunt
  dir only; did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root `main.py`
  still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914l_study_packet.json`,
  `experiments/20260914l_cut16_rolling.json`,
  `experiments/20260914l_top10_games.json`,
  `experiments/20260914l_gate.json`.

## 2026-09-14m — cut 16 1623.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1623.1** (was 1619.1).
  Shopbag `56151155` **COMPLETE 1300.3**. Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-14T13:41:29`: heralces **rank 2161 /
  1623.1** of 9012. Gold 21 JezzLynn 2925.3. Rank 10 Unknown Mother-Goose
  2984.3. Top: Majkel1337 3223.9 (live 3223.9 scoring-sub `56156662`;
  current sub `56216119` is 3037.9), Artem The Farmer 3050.1, SpaTaro
  3027.8.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 264 PUBLIC + 1 VALIDATION. All-public W/T/L
  **111-2-151**, mean **−1674.5**. Newest-12 disjoint-from-14l ids
  `108910147…108669139` do **not** match the 09-14l set
  `108871316…108741805`. Autopsy
  `experiments/20260914m_cut16_rolling.json`. Rolling **3-0-9**, mean
  **−5310.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (HaoChi `108817790` **−6212**; итмоняяя
  `108762693` **−6320**) plus extra-goose (LaiCxm `108851261` **−16092**,
  extra cow 218 extra sheep 227 extra geese 242/266; here we go
  `108704919` **−7788**; Toru59er `108787437` **−6986**) plus extra-sheep
  (Revanth Tambisetty `108822458` **−11033**; Adhiraj Jagtap `108889378`
  **−2087**) plus identical-clone extra-sheep (Варим сельский самогон
  `108889446` **−12131**) plus identical-clone extra-goose (Cuong Le
  `108686716` **−590**). BUY_LAND 151/266; cash_24 3-27; clone=12/12.
  红烧肉 `108910147` already bought extra geese 227/242 and won vs extra
  sheep 218/227 extra geese 242/266 +3039 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14l.
  Mid-land 150 then 218-222 (one 150/220; one 150/220/222; one
  150/218/220/222; one 150/218), clone=0/4, wheat 332-521, goose
  0g/2g/4g/0g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914m/`: 1 new slug vs `_hunt_20260914l`
  (`ahmedberatozer/kaggriculture-v42-production-that-fits-the-marke`).
  Python `%%writefile main.py` SHA `728fdfb4` Shop0909 144/648 + 288
  four-turn + 712 planner; distinct from V41 `8951ff93` and rohitt94
  `62a80706`. Not later-block. Public search newest
  `ahmedberatozer/kaggriculture-v42-production-that-fits-the-marke`.
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6.
  Writefile hashed in hunt dir only; did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914m_study_packet.json`,
  `experiments/20260914m_cut16_rolling.json`,
  `experiments/20260914m_top10_games.json`,
  `experiments/20260914m_gate.json`.

## 2026-09-14n — cut 16 1627.7; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1627.7** (was 1623.1).
  Shopbag `56151155` **COMPLETE 1300.7**. Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-14T14:41:57`: heralces **rank 2162 /
  1627.7** of 9023. Gold 21 nilochan 2927.1. Rank 10 Catalyst 2981.6.
  Top: Majkel1337 3227.6 (live 3227.6 scoring-sub `56156662`;
  current sub `56216119` is 3045.8), ymg_aq 3027.0, SpaTaro 3012.7.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 265 PUBLIC + 1 VALIDATION. All-public W/T/L
  **112-2-151**, mean **−1649.0**. Newest-12 disjoint-from-14m ids
  `108930713…108744906` do **not** match the 09-14m set
  `108910147…108669139`. Autopsy
  `experiments/20260914n_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−2680.0**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Quillbolt `108753975` **−9650**) plus extra-goose
  (bplyc15 `108784373` **−7879**, extra cow 218 extra sheep 227 extra
  geese 242/266; Scorn100 `108846707` **−5681**; refine123 `108871316`
  **−6523**) plus identical-clone extra-goose (我是刘大聪 `108744906`
  **−9197**) plus identical-clone extra-sheep (trung `108814509`
  **−5487**) plus extra-sheep (higuuu `108751924` **−3065**). BUY_LAND
  151/266; cash_24 3-27; clone=12/12. たがやす `108930713` already bought
  extra sheep 227/242/266 and won vs extra geese 227/242 extra sheep
  266 +5060 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14m.
  Mid-land 150 then 220-222 (four 150/220/222), clone=0/4, wheat
  448-513, goose 0g/2g/0g/2g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260914n/`: 1 new slug vs `_hunt_20260914m`
  (`guruprasaathas111/kaggriculture-fully-dynamic-autonomous-agent`).
  Python `%%writefile main.py` SHA `f4e3935c` Shop0909 144/648 + 288
  four-turn + 712 planner; distinct from guru V39 `708c7485` and Ahmed
  V42 `728fdfb4`. Not later-block. Public search newest
  `guruprasaathas111/kaggriculture-fully-dynamic-autonomous-agent`.
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6.
  Writefile hashed in hunt dir only; did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914n_study_packet.json`,
  `experiments/20260914n_cut16_rolling.json`,
  `experiments/20260914n_top10_games.json`,
  `experiments/20260914n_gate.json`.

## 2026-09-14o — cut 16 1625.8; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1625.8** (was 1627.7).
  Shopbag `56151155` **COMPLETE 1300.7**. Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-14T15:42:31`: heralces **rank 2160 /
  1625.8** of 9028. Gold 21 Crop Dustas 2922.1. Rank 10 Orbital
  Terraformer 2982.3. Top: Majkel1337 3230.8 (live 3230.8 scoring-sub
  `56156662`; current sub `56216119` is 3057.1), ymg_aq 3021.7,
  SpaTaro 3010.4.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 267 PUBLIC + 1 VALIDATION. All-public W/T/L
  **113-2-152**, mean **−1643.0**. Newest-12 disjoint-from-14n ids
  `108944173…108723413` do **not** match the 09-14n set
  `108930713…108744906`. Autopsy
  `experiments/20260914o_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−4892.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Floth `108944173` **−1793**, HaoChi `108817790`
  **−6212**, итмоняяя `108762693` **−6320**) plus extra-goose (LaiCxm
  `108851261` **−16092**, Toru59er `108787437` **−6986**) plus
  identical-clone extra-sheep (Варим `108889446` **−12131**) plus
  extra-sheep (Revanth `108822458` **−11033**, Adhiraj `108889378`
  **−2087**). BUY_LAND 151/266; cash_24 3-27; clone=12/12. Yiwei Pu
  `108941028` already bought extra geese 227/242 and won identical-clone
  +106 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14n.
  Mid-land 150 then 218-222 (three 150/220/222 plus one 150/218/220/222),
  clone=0/4, wheat 409-672, goose 2g/4g/0g/2g. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260914o/`: 1 new slug vs `_hunt_20260914n`
  (`xuantianfengwu/kaggriculture-hour-4-financing-allocator`).
  Python `%%writefile submission.py` SHA `dc07c7a9` Hour-4 4/6-cow
  heuristic; distinct from r10 `3b8a1d4d` and allocator `d12f2987`.
  Not later-block. Public search newest
  `xuantianfengwu/kaggriculture-hour-4-financing-allocator`.
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6.
  Writefile hashed in hunt dir only; did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260914o_study_packet.json`,
  `experiments/20260914o_cut16_rolling.json`,
  `experiments/20260914o_top10_games.json`,
  `experiments/20260914o_gate.json`.

## 2026-09-15 — cut 16 1606.1; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1606.1** (was 1625.8).
  Shopbag `56151155` **COMPLETE 1293.6**. Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-15T03:30:25`: heralces **rank 2211 /
  1606.1** of 9077. Gold 21 Kilupy 2946.4. Rank 10 Catalyst
  2978.3. Top: Majkel1337 3198.4 (live 3198.4 scoring-sub
  `56156662`; current sub `56216119` is 3131.7), Artem The Farmer 3082.2,
  DSM 3070.6.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 285 PUBLIC + 1 VALIDATION. All-public W/T/L
  **119-2-164**, mean **−2014.5**. Newest-12 disjoint-from-14o ids
  `109142116…109024708` do **not** match the 09-14o set
  `108944173…108723413`. Autopsy
  `experiments/20260915_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−7862.6**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (My second life `109030720` **−29665**, Nazmus
  `109042689` **−13653**, Quillbolt `109054323` **−12417**, Goua Henri
  `109029822` **−7452**) plus extra-goose (Harshith `109044160`
  **−15134**) plus identical-clone extra-goose (Liyi `109057555`
  **−23988** cash_24=0) plus extra-sheep (SatoshiN04 `109091091`
  **−12300** clone=0). BUY_LAND 151/266; cash_24 0-22; clone=11/12.
  ocean240812 `109142116` already bought extra sheep 227/242/266 and won
  +74 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-14o.
  Mid-land 150 then 218-222 (three 150/218/220/222 plus one 150/220/222),
  clone=0/4, wheat 433-543, goose 4g/4g/0g/4g. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260915/`: 12 new slugs vs `_hunt_20260914o`
  (public search newest `xuantianfengwu/kaggriculture-terminal-logistics`).
  Python `%%writefile submission.py` SHA `364ca885` Hour-4 4/6-cow
  heuristic; distinct from hour-4 `dc07c7a9` and r10 `3b8a1d4d`.
  Not later-block. Also Ahmed V43 SHA `919fc1d6` Shop0909 overlay,
  alperen adaptive-route SHA `77cf6772` yhay81 0913 reprint, sunil v6
  SHA `8951ff93` V41 reprint, pipe-2 SHA `728fdfb4` V42 reprint.
  Author lists: no Yusuke later-block, no king rc5, no y3uanm v6.
  Writefile hashed in hunt dir only; did not extract to candidates/.
  Did not re-extract rejected kernels. Cut 12/13 stay Hold. Did not
  re-upload boatlee. Root `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260915_study_packet.json`,
  `experiments/20260915_cut16_rolling.json`,
  `experiments/20260915_top10_games.json`,
  `experiments/20260915_gate.json`.

## 2026-09-15b — cut 16 1588.3; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1588.3** (was 1606.1).
  Shopbag `56151155` **COMPLETE 1286.1**. Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-15T13:02:08`: heralces **rank 2272 /
  1588.3** of 9121. Gold 21 Sida Zuo 2954.7. Rank 10 Mengfei Li
  2989.6. Top: Majkel1337 3148.5 (live 3148.5 scoring-sub
  `56156662`; current sub `56216119` is 3137.7), Artem The Farmer 3138.2,
  Unknown Mother-Goose 3093.3.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 300 PUBLIC + 1 VALIDATION. All-public W/T/L
  **124-2-174**, mean **−1989.7**. Newest-12 disjoint-from-15 ids
  `109274859…109168637` do **not** match the 09-15 set
  `109142116…109024708`. Autopsy
  `experiments/20260915b_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−3874.9**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (ManasviSharma `109251218` **−18715**, Huy
  `109178619` **−13645**, Ashraf `109227483` **−13342**, Sergei
  `109247247` **−13194**) plus extra-goose (AimeeChen1 `109205359`
  **−2466**) plus identical-clone extra-goose (3G `109168637`
  **−10063**) plus extra-sheep (Grim Reaper `109169017`
  **−10132**; Rifa `109208871` **−3251**). BUY_LAND 151/266; cash_24
  3-29; clone=11/12. Baha `109274859` already bought extra geese
  227/242 and won +114 — not a 227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-15.
  Mid-land 150 then 218-222 (two 150/218/220/222 plus two 150/220/222),
  clone=0/4, wheat 472-610, goose 2g/4g/2g/4g. Opening land is not a
  later-block license.
- Hunt (no cell exec) `_hunt_20260915b/`: 3 new slugs vs `_hunt_20260915`
  (public search newest `anandkumar369o/kagg-team-decisions`).
  Analysis SHA `595d29fe`. nathanjacob pipe-4 B85 SHA `7a37397f` V43+C9
  opening Shop0909 overlay; kenanzhang9 SHA `602ae8be` Shop0909
  144/648+288+712 overlay. Not later-block. Author lists: no Yusuke
  later-block, no king rc5, no y3uanm v6. Writefile hashed in hunt dir
  only; did not extract to candidates/. Did not re-extract rejected
  kernels. Cut 12/13 stay Hold. Did not re-upload boatlee. Root
  `main.py` still h2 SHA `65e6f5cd...`.
- JSON: `experiments/20260915b_study_packet.json`,
  `experiments/20260915b_cut16_rolling.json`,
  `experiments/20260915b_top10_games.json`,
  `experiments/20260915b_gate.json`.

## 2026-09-15c — cut 16 1582.4; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1582.4** (was 1588.3).
  Shopbag `56151155` **COMPLETE 1286.1**. Cut 15 `56146106`
  **1864.4** (dropped). CSV `2026-09-15T14:03:28`: heralces **rank 2291 /
  1582.4** of 9128. Gold 21 Ebi 2953.4. Rank 10 leave you
  2987.6. Top: Majkel1337 3147.0 (live 3147.1 scoring-sub
  `56156662`; current sub `56216119` is 3144.5), Artem The Farmer 3146.4,
  Unknown Mother-Goose 3089.1.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 301 PUBLIC + 1 VALIDATION. All-public W/T/L
  **124-2-175**, mean **−2069.5**. Newest-12 disjoint-from-15b ids
  `109297997…109044160` do **not** match the 09-15b set
  `109274859…109168637`. Autopsy
  `experiments/20260915c_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−3963.6**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Filip `109159847` **−6855**, Quillbolt
  `109054323` **−12417**) plus extra-goose vs extra-cow (Gaddam
  `109297997` **−26009**, Harshith `109044160` **−15134**) plus
  identical-clone extra-goose (Liyi `109057555` **−23988**) plus
  extra-sheep (Dhruv `109149160` **−12590**; Satoshi `109091091`
  **−12300**). BUY_LAND 151/266; cash_24 0-22; clone=10/12. Gaddam
  `109297997` already bought extra geese 227/242 and lost vs 11c — not a
  227 wrap license.
- Missing high-rank team none at #1; Majkel1337 still CSV/live #1,
  re-measured on scoring-sub `56156662` ids disjoint from 09-15b.
  Mid-land 150 then 218-222 (150/218, 150/220, 150/218/220/222,
  150/220/222), clone=0/4, wheat 399-466, goose 4g/0g/2g/2g. Opening
  land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260915c/`: 4 new slugs vs `_hunt_20260915b`
  (public search newest `alperen5252525/turn-one-market-advantage-kaggriculture`).
  pipe-4 reprint SHA `7a37397f`. public-state v58 SHA `b041058e` day-6
  72/144 plus yarn clone-latch 360; momentum SHA `5fd73afd` frozen
  shop-prefix tapes; market-smart V43 reprint SHA `919fc1d6`. Not
  later-block. Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Writefile hashed in hunt dir only; did not extract to
  candidates/. Did not re-extract rejected kernels. Cut 12/13 stay
  Hold. Did not re-upload boatlee. Root `main.py` still h2 SHA
  `65e6f5cd...`.
- JSON: `experiments/20260915c_study_packet.json`,
  `experiments/20260915c_cut16_rolling.json`,
  `experiments/20260915c_top10_games.json`,
  `experiments/20260915c_gate.json`.

## 2026-09-15d — cut 16 1573.9; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1578.6** (CSV/ListEpisodes
  **1573.9** / 1573.96; was 1582.4). Shopbag `56151155` **COMPLETE 1282.2**.
  Cut 15 `56146106` **1864.4** (dropped). CSV `2026-09-15T15:01:30`:
  heralces **rank 2300 / 1573.9** of 9136. Gold 21 Otter Vibe 2944.2.
  Rank 10 Mengfei Li 2986.9. Top: Artem The Farmer 3149.3 (live 3149.3
  scoring-sub `56232364`; current sub `56234362` is 3038.9), Majkel1337
  3144.3, SpaTaro 3054.5.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 305 PUBLIC + 1 VALIDATION. All-public W/T/L
  **125-2-178**, mean **−2122.2**. Newest-12 disjoint-from-15c ids
  `109323301…109205359` do **not** match the 09-15c set
  `109297997…109044160`. Autopsy
  `experiments/20260915d_cut16_rolling.json`. Rolling **4-0-8**, mean
  **−4182.2**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Manasvi `109251218` **−18715**, Ashraf
  `109227483` **−13342**, yu9824 `109316981` **−1349**) plus extra-sheep
  (Xiaowenhao404 `109321947` **−14705**, Sergei `109247247` **−13194**,
  Fedor `109323301` **−10162**, Rifa `109208871` **−3251**) plus
  extra-goose (AimeeChen1 `109205359` **−2466**). BUY_LAND 151/266;
  cash_24 3-25; clone=11/12. Baha `109274859` already bought extra geese
  227/242 and won +114 — not a 227 wrap license.
- Missing high-rank team #1 is now Artem The Farmer (CSV/live), measured
  on scoring-sub `56232364` ids disjoint from 09-15c Majkel set.
  Mid-land 151 then 198 on 4/4, clone=1/4, wheat 302-541, goose 2g.
  Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260915d/`: 1 new slug vs `_hunt_20260915c`
  (public search newest `ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race`).
  SOURCE_BYTES SHA `797d9bca` V43 Shop0909 plus same-turn sale-race
  overlay (`_RACE_HORIZON_CLONE=8` / 24 wrapping `_R37_HORIZONS`). Not
  later-block. Author lists: no Yusuke later-block, no king rc5, no
  y3uanm v6. Writefile hashed in hunt dir only; did not extract to
  candidates/. Did not re-extract rejected kernels. Cut 12/13 stay
  Hold. Did not re-upload boatlee. Root `main.py` still h2 SHA
  `65e6f5cd...`.
- JSON: `experiments/20260915d_study_packet.json`,
  `experiments/20260915d_cut16_rolling.json`,
  `experiments/20260915d_top10_games.json`,
  `experiments/20260915d_gate.json`.

## 2026-09-15e — cut 16 1569.5; Hold (upload-bail)

- Submissions API: cut 16 `56151152` **COMPLETE 1569.5** (CSV/ListEpisodes
  **1569.5** / 1569.56; was 1573.9). Shopbag `56151155` **COMPLETE 1282.2**.
  Cut 15 `56146106` **1864.4** (dropped). CSV `2026-09-15T16:00:41`:
  heralces **rank 2319 / 1569.5** of 9139. Gold 21 Driz Lo 2938.0.
  Rank 10 leave you 2985.6. Top: Majkel1337 3155.3 (live 3155.3
  scoring-sub `56216119`), Artem The Farmer 3140.2, SpaTaro 3053.4.
- Upload-bail **(c)**: newest cut COMPLETE >=1500, but shopbag
  `56151155` is newer than cut 16 and <1500, so a new cut alone would
  drop `56151152` without a >=1500 COMPLETE remaining as newest-2 partner
  (re-upload is 600-provisional). **Hold.** No Kaggle submit. Quota
  remaining **5**.
- EpisodeService cut 16: 306 PUBLIC + 1 VALIDATION. All-public W/T/L
  **125-2-179**, mean **−2116.4**. Newest-12 disjoint-from-15d ids
  `109329693…109111080` do **not** match the 09-15d set
  `109323301…109205359`. Autopsy
  `experiments/20260915e_cut16_rolling.json`. Rolling **5-0-7**, mean
  **−1129.4**.
- Loss class mixed, not freeze-after-day-9 9c9s, not opening-broke:
  extra-animal 8c6s3g (Huy `109178619` **−13645**, Filip
  `109159847` **−6855**) plus extra-goose vs extra-cow (Gaddam
  `109297997` **−26009**) plus identical-clone extra-goose (3G
  `109168637` **−10063**) plus extra-sheep (Dhruv `109149160` **−12590**,
  Grim `109169017` **−10132**) plus extra-goose (Corgi `109329693`
  **−325**). BUY_LAND 151/266; cash_24 1-29; clone=11/12. Gaddam
  `109297997` already bought extra geese 227/242 and lost vs 11c — not a
  227 wrap license.
- Missing high-rank team #1 is now Majkel1337 (CSV/live), measured
  on scoring-sub `56216119` ids disjoint from 09-15d Artem set.
  Mid-land 150 then 220-222 (one game 126/150/220), clone=1/4, wheat
  404-530, goose 0g/4g/0g/4g. Opening land is not a later-block license.
- Hunt (no cell exec) `_hunt_20260915e/`: 0 new slugs vs `_hunt_20260915d`
  (public search newest still `ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race`).
  Already rejected SHA `797d9bca`. Did not re-pull. Author lists: no
  Yusuke later-block, no king rc5, no y3uanm v6. Cut 12/13 stay Hold.
  Did not re-upload boatlee. Root `main.py` still h2 SHA
  `65e6f5cd...`.
- JSON: `experiments/20260915e_study_packet.json`,
  `experiments/20260915e_cut16_rolling.json`,
  `experiments/20260915e_top10_games.json`,
  `experiments/20260915e_gate.json`.

## 2026-09-19 — live-state refresh; hold retained

- Read-only submissions API: newest-two cut 16 `56151152` is **1411.5
  COMPLETE** and shopbag reupload `56151155` is **1223.9 COMPLETE**. Both
  have decayed below the 2026-09-15 values; no retry or replacement was made.
- Competition API confirms 9,538 entered teams and deadline 2026-09-30
  23:59 UTC. The public leader is `3276.2`; this is a material field shift,
  not evidence that an unvalidated local variant should consume an upload.
- Existing upload-bail remains correct: shopbag is the newer weak partner, so
  a single new cut would evict the stronger current Agent while retaining the
  weak one. No newly audited, later-block candidate exists to justify a paired
  replacement.

## 2026-09-20 — gold-class pair uploaded (metav4 v13 + 2945 farm)

- Live oracle before upload: N=9643, gold_cut=floor(10+0.002*N)=29,
  gold-band score 2918.0 (KawattaTaido), leader Majkel1337 3223.6.
  heralces rank 2946 score 1358.1. Newest-2 was cut 16 `56151152`
  1358.1 COMPLETE + shopbag `56151155` 1203.1 COMPLETE.
- Static hunt (no cell exec) materialized Thomas Tschinkel metav4 v13
  SHA `9d634946...` (byte-exact vs published EXPECTED_SHA256) and the
  2945 farm SHA `bfee70e9...` (claimed live 2944.7 on sub 56269928).
- Official-engine 720 both-seat vs live cut 16: metav4 **4/4**, mean
  margin **+22216**, worst **+21709**, both seats DONE/DONE.
- Bundles: metav4 621560 bytes SHA `79400f75...`; 2945 farm 520554
  bytes SHA `97e0ac07...`; members `['main.py']`; compile+byte-identity
  passed. Root `main.py` still h2 `65e6f5cd...`.
- Uploaded partner 2945 farm `56395540` then scoring metav4 `56395547`.
  Newest-2 is this pair; cut 16 and shopbag dropped. Quota remaining 3.
  Did not re-upload boatlee `55710781`.
- JSON: `experiments/20260920_gate.json`.
- Validation COMPLETE for both: metav4 `56395547` episode `111237210`
  self-play 71310 vs 71978; 2945 farm `56395540` episode `111237208`
  72101 vs 72762. Public scores **600.0** starting rating, 0 public games
  yet. Leaderboard rank **5900 / 9645** at 600.0 vs gold_cut 29 / 2923.8.
  Matchmaking has not produced a verifiable gold rank.
- First public games (not gold): metav4 `111238472` win 148925-37855,
  score 600→679.2; 2945 farm `111237392` win 158955-21236 →673.6 and
  `111238480` win 156849-73056 →775.2. Rank 5387 / 9645 vs gold_cut 29.
  Pair is COMPLETE and scoring, not stuck at 600.
- After ~30 min matchmaking: metav4 `56395547` **5-0 COMPLETE 987.8**;
  2945 farm `56395540` **7-0 COMPLETE 1314.2**. Rank **3053 / 9648** vs
  gold_cut 29 / 2920.8. Latest 2945 win vs ~1229-rated opponent was
  close (+9565). Climbing; not gold.
- ~50 min: metav4 **11-0 COMPLETE 1509.5**; 2945 farm **13-0 COMPLETE
  1846.3**. Rank **1938 / 9649** vs gold_cut 29 / 2916.9. Still unbeaten
  vs ~1500-1600 opponents. Not gold.
- ~70 min: metav4 **15-1-0 COMPLETE 1989.6** (one tie); 2945 farm
  **17-0 COMPLETE 2227.6**. Rank **1337 / 9652** vs gold_cut 29.
  Latest 2945 win vs ~2100 was thin (+1483). Still no evidence the pair
  cannot reach ~2900.
- ~90 min: ListEpisodes 429 RESOURCE_EXHAUSTED. Submissions+LB still live:
  metav4 COMPLETE **2224.9**, 2945 farm COMPLETE **2419.4**, rank
  **1012 / 9655** vs gold_cut 29 / 2921.1. Pair still climbing. Not gold.
- ~2h: scoring metav4 overtook the partner. metav4 COMPLETE **2489.7**,
  2945 farm **2434.4**, rank **890 / 9658** vs gold_cut 29 / 2920.1.
  Partner had a dip 2481.9→2413 then recovered. haideptry 2950 vs 2945
  local 2/2 but only +50 coins — not a quota-worthy replacement. Not gold.
- ~2.5h: metav4 crossed 2500. COMPLETE **2545.6**, partner **2490.9**,
  rank **863** at 2501 then still climbing vs gold_cut 29 / 2920.3.
  Small dips at this band, then recovery. Not gold.
- ~3h: metav4 COMPLETE **2607.4**, partner **2434.9**, still grinding
  ~+10/game. Rank was 678 at 2563.9. Gold_cut 29 / ~2921. Not gold.
- Later same day: metav4 COMPLETE **2667.7**, partner **2344.7**, rank
  **400 / 9693** vs gold_cut 29 / 2906.1. Six-hour grind 2633→2685 then
  a dip to 2667. Still ~238 from gold band. Not gold.
- ListEpisodes recovered: metav4 **126 public 76-20-30**, last six vs
  2625-2732 all losses/ties (margins -619..-327). 2945 farm 131 public
  59-15-57 decaying. Live ceiling ~2660, not gold ~2905. Ahmed v53 loses
  to metav4 local 0-2 mean -1721; pipe16/2950 are +50 overlays. Did not
  drop the 2664 COMPLETE scoring Agent. Not gold.
- Replacement hunt 2026-09-21: no gold-class Agent that beats metav4
  by a gold-relevant margin. 2945 reprints rejected. Lynn V2 −989,
  Alperen first-in-line −2756, wheat-race wrap of metav4 collapsed
  −68602 on 4/4. Kept metav4 `56395547` in newest-2. Not gold.
- destbreso donor dataset 2026-09-20 pulled. finance7 main.py SHA `196b1aa2`
  needs `agent.so` (Windows skip). 10 distinct Python donors 720 both-seat
  vs metav4: all lose except guru v4 **+50 overlay**. Closest real loss:
  koshinm 09-21 **−327**. Did not submit. Not gold.
- Remaining compile_ok donors 720 both-seat vs metav4: koshinm 09-20
  **−794**, pipe15 **−640**, Ahmed v49/v50 **−658**, aurax7 v4–v7
  **−2377..−6007**, Tschinkel routers **−11k..−31k**, hesoponyo RL
  **−51927**. No gold-relevant winner. Did not submit. Not gold.
- 2026-09-21 original-agent hunt (do not rescreen destbreso compile_ok pool).
  Live oracle: N=9697 gold_cut=29 / **2906.7**, heralces **R=442 / 2652.0**.
  Scoring metav4 `56395547` COMPLETE 2652.0; partner 2945 `56395540` 2340.8.
  API top: DSM **3117.2** scoring `56401245` (112 public **109-0-3** vs 3000-band);
  Ebi gold-cut `56386270` 2901.2. Quota unused today. Not gold.
- Local official-engine 720 both-seat vs live metav4, seed 20260921:
  finwheat (hire-finance + bounded wheat) **0-2 mean −13** identical seats;
  dmitrii smaller-market-shock **0-4 mean −2295**; tomato12 PASS-steal
  **0-2 mean −6117**; v219open shop-gate drop **2-2 ties 0** (vs metav4
  tomato price 62 < 70 so crew never commits; vs pass it commits and
  scores −1529); indarkarhana e776 **0-2 mean −15618**. Today's public
  kernels (kenanzhang9 A1-T31, ghazaros K0013, yeshawang, haideptry 2900,
  xuanzhang V54 auto-top1) are reprints of already-screened donors.
  Did not submit. Kept metav4 `56395547`.
- DSM gold-board fingerprint (8 replays): same 3 quads NW/NE/SW land=75
  as metav4; opening always `BUY_ANIMAL COW 1` + `BUY_PRODUCT WHEAT 5`;
  tomatoes 0–14 tiles by day 18 on wheat/SW coords, not V219's locked SE
  band; geese 6–11. Cannot bolt those tomatoes onto metav4 wheat tiles
  without destroying the wheat engine (tomato12 already collapsed).
  DSM-opening-only wrap of metav4 (correct last-callable) collapsed
  **0-2 mean −121738**. Do not graft DSM fragments onto metav4. Not gold.
- DSM shop-world harvest: 112 public scoring-sub `56401245` replays, **54**
  distinct first-two-shop worlds. DSM action prefixes already diverge by
  step 24 (before shop 1 at step 72), so a yhay81-style switch at 144 is
  invalid. Seat-keyed best-tape chassis vs metav4 collapsed **0-2 mean
  −179333** (seat1 bank 0). Observation-driven DSM live farm still ~5
  coins vs pass (animals escape unfed; not gold-class). Did not submit.
  Kept metav4 `56395547`. Not gold.
- DSM live farm rewrite: job-assigned daily feed/care, NW melon, SW
  tomatoes, three quadrants. Survives 720 vs pass at **~60k** (4 cows /
  3 sheep / 2 geese, 18 melon + 7 tomato at day 18). Official 720
  both-seat vs metav4 still **0-2 mean −100k to −125k** (best own 37730
  vs metav4 138572). Not gold-relevant. Did not submit. Kept metav4
  `56395547`. Not gold.
- DSM live farm crop-first rebuild: **69834 vs pass** (24 melon day 12,
  20 melon + 9 tomato day 18). vs metav4 **0-2 mean −128617** (own 3211–
  5098). Animal-product mix and price floors did not close the glut.
- haideptry `the-2965-master-hybrid-engine` (2026-09-21) SHA `949e2eed`
  is Pipe-16 idle-worker hybrid on the metav4 controller. Official 720
  both-seat vs metav4 **2-2 mean +50 identical seats** — +50 overlay, not
  gold-relevant. Did not submit. Kept metav4 `56395547`. Not gold.
- fill_farm sticky rewrite (2026-09-21): per-worker sticky jobs, seed-count
  so the engine does not drop a whole PLANT wave, NE strawberries, SW wheat
  after day 20, 11 hands. vs pass seed 20260921 **91358** DONE/DONE (was
  81976 with 4–6 berries; metav4 vs pass is 185012 with 33 berries / 37
  wheat). Official 720 both-seat vs live metav4 **0-2 mean −82510**
  (30460 vs 112970 both seats). Better than the prior fill_farm −103755
  but not gold-relevant (~400+). Aggressive board-fill variants (dedicated
  planters, plant-before-fert, cows in SW) collapsed to 6k–47k vs pass.
  Extra SW hands on top of the 11-hand crew (isolated skip-set, hire-13
  after $8k) filled SW wheat/berries but vs-pass fell to 79k–81k: extra
  crops steal watering and milk harvest. Restored the 91k chassis.
  vs metav4 still **0-2 mean −82510**. Did not submit. Kept metav4
  `56395547`. Quota unused. Not gold.
- Nearby-only strawberry fertilize on the 91k 11-hand chassis (collectors
  within 2 tiles, no stolen feed/milk walks): vs pass **97914** (strawberry
  sells 112 vs 64). Official 720 both-seat vs metav4 **0-2 mean −77431**
  (31525/31607 vs 109720/108274). Better than −82510, not gold-relevant.
  Did not submit. Kept metav4 `56395547`. Quota unused. Not gold.
- region_farm (distinct engine, not fill_farm squeeze): workers stay in herd /
  NE strawberry / SW wheat zones. vs pass **89912**. Official 720 both-seat
  vs metav4 **0-2 mean −89270** (own 56252/56398 vs 145658/145532). Own
  coins vs metav4 are the best this hunt (~56k vs fill_farm ~31k) but the
  margin is still a collapse, not ~400+. Did not submit. Kept metav4
  `56395547`. Quota unused. Not gold.
- Hunt 2026-09-21b (new public kernels, not destbreso rescreen, not
  region_farm): sunil idle-workers / tetsutani demand-preserving = pipe16
  SHA `827ddf29`; sunil v8 = Ahmed v48. Extracted and official-720 vs
  metav4 seed 20260921: guru game-theoretic SHA `ed89be8c` **0-2 mean
  −658** identical seats (Ahmed v49-class); crystalbaby God-mode (lynn v2
  + shop overlay) **0-2 mean −786**; sunil top-10 V39+v9 SHA `4f3ca95d`
  **0-2 mean −694**. None gold-relevant. Did not submit. Kept metav4
  `56395547`. Quota unused. Not gold.
- Gold-band tape engines 2026-09-21 (not destbreso compile_ok rescreen, not
  +50 overlay, not fill/region farm): destbreso finance7 yhay81 v7 tapes
  ported to Python and also compiled as a Windows DLL — both **164203 vs
  pass**, official 720 both-seat vs live metav4 **0-2 mean −20222**
  (79577 vs 99799 identical seats). yhay81-shop-router-0913 (29 shop-pair
  plans, never eval'd vs metav4) **168179 vs pass**, **0-2 mean −14650**
  (85669 vs 100319). shopforge_race = 0913 plus three-turn non-wheat sell
  lookahead, official 720 **0-2 mean −7625** (90076 vs 97701). Forcing
  plan 10 on this seed is the closest real loss (**−4876**, 92487 vs
  97363) but still not ~400+. Hunt 2026-09-21c: kaibaur f46e91 = pipe16
  `827ddf29`; CropSense/FarmPilot are beginner ROI notebooks. Did not
  submit. Kept metav4 `56395547` COMPLETE. Live oracle 08:06 UTC: N=9714
  gold_cut=29 / **2910.8** (ShunkiKyoya), heralces **R=495 / 2625.1**,
  DSM 3162.2. Quota unused. Not gold.
- 0913 plan sweep vs metav4 (seat 0, l3): best **plan 10 −4876** (92487 vs
  97363). Plan 10 + l3 + shed liquidate from step 600: **−2389** (94722 vs
  97111) — closest real loss this hunt, still not ~400+. Default 0913
  router + l3 + liquidate-600: vs pass 162493 (down from 168k), vs metav4
  **−6797**. Forcing plan 10 is a this-seed counter, not a general gold
  Agent. Did not submit. Kept metav4 `56395547`. Not gold.
- Opponent-detect plan 10 (generalizable): start on 0913 plan 10, at step 144
  lock it if the rival already has a real farm (≥8 plants / ≥2 animals / 2
  quads), else fall back to the 64 shop-pair router. Switching at 144 without
  the plan-10 opening desyncs and scores **−12460**. Starting on 10 then
  staying vs a farm keeps the −2389 race. Official 720 both-seat vs metav4
  **0-2 mean −2389** (94722 vs 97111). vs pass stays gold-band: 166878 /
  195583 / 140748 on seeds 20260921 / 20260922 / 11. Lift vs previous
  shopforge_race −7625 is **+5236**, not the remaining ~8k to a +400 win.
  Shed-capping SELL 1000 collapsed (−75441). Did not submit. Kept metav4
  `56395547`. Quota unused. Not gold.
- Tried to close the remaining −2389: workers carry strawberries/fert/eggs
  in the field (e.g. step 618: 21 S + 19 fert in hands, empty shed) while
  market SELL no-ops; metav4 dumps at 630/694. Courier-to-shed and
  projected DROP+sell both desync the tape (−6k to −65k). One heavy
  carrier (min 15) is a no-op (−2386). Ahmed v54 SHA `5fbb75c9`
  (metav4 + Pipe-16 HybridOpening + wheat SELL guard price<31) official
  720 both-seat **2-2 mean +104 identical seats** (97490 vs 97386) — a
  win, but not gold-relevant (~400+) and the same identical-seat overlay
  class as +50. Did not submit. Kept metav4 `56395547`. Quota unused.
  Not gold.
- Distinct-engine hunt after −2389: yhay81-0909 (13 tapes + weed/sale
  repairs, sibling actions.json) **168672 vs pass**, official-style 720
  vs metav4 **0-2 mean −9653**. Lynn wheat-seller SHA `3abd40ee` (metav4 +
  Pipe-16 + delayed wheat cycle + close-queue) **2-2 mean +77 identical
  seats**. FarmCraft 8k beginner **638 vs pass**. Hour-0 shed-sell bump
  displaces HIREs (−8588). SELL-first reorder collapses (−71533). No
  gold-relevant winner. Did not submit. Kept metav4 `56395547`. Quota
  unused. Not gold.
- shopforge_race plan-10 lock is seed-overfit: 7-seed official-style 720
  both-seat vs metav4 **0/14 mean −22164**, best still −2389 on 20260921;
  yarn worlds −31k to −44k. Raw 0913 shop router **0/10 mean −22806**,
  best −3733. Extra shed SELLs on metav4/v54 collapse −29k. Bumping
  existing SELL qtys to shed: metav4 −3392, v54 −3314. Hour-0 HIRE→SELL
  swaps −5k to −19k (hires are load-bearing). dmitrii 7-turn-rescue
  **168874 vs pass**, vs metav4 **−9648** (0909-class). No gold-relevant
  winner. Did not submit. Kept metav4 `56395547`. Quota unused. Not gold.
- Hunt 2026-09-21e (live oracle 09:31 UTC): N=9724 gold_cut=29 / **2907.9**
  (Snorlax), heralces **R=546 / 2606.5** (down from 2625.1), DSM 3177.3.
  Newest-2 still metav4 `56395547` COMPLETE 2606.5 + 2945 `56395540` 2285.7.
  New public kernels: lynn idle-seller SHA `2e614aa2` official 720 both-seat
  vs metav4 **2-2 mean +50 identical seats** (97464 vs 97414) — same overlay
  class as pipe16. dmitrii more-wheat SHA `a5362d13` **2-2 mean +77 identical
  seats** (97475 vs 97398) — same numbers as lynn wheat-seller. tetsutani
  market-smart SHA `f6a756cf` (V41-class) **0-2 mean −2442** identical seats
  (95796 vs 98238). haideptry 2965 is Pipe-16 `_alt_install` EarlyCycle.
  destbreso dataset still lastUpdated 2026-09-20 23:48. No PET_CAFE/BRUNCH
  public DSM pair in 41 shop-pair tapes.
- Wrote a distinct production engine `dsm_goldtape` (not a +50 overlay): 41
  DSM gold-board winning-seat tapes (off-by-one corrected), first-shop
  branch at step 72, 0909 weed/sale repairs, inlined zlib/b85, 497069 B.
  vs pass seed 20260921 **174932** (gold-band, above 0913 168k). Official
  720 both-seat vs live metav4 **0-2 mean −84703** (37154 vs 121857
  identical seats). Locking PET_CAFE/ICE_CREAM from t=0 worse **−132454**
  (26228 vs 158682). DSM public tapes do not transfer vs metav4 (pairing
  changes weeds/shops; metav4 is already the same melon+livestock family:
  vs pass 185012 with melon from t=6, vs self 6 coops / 4 geese on this
  seed). No gold-relevant winner. Did not submit. Kept metav4 `56395547`.
  Quota unused. Not gold.
- metav4_egg_boost (BRUNCH/BAKERY extra GOOSE + BUILD_COOP on PASS workers):
  official 720 both-seat vs metav4 **0-2 mean −119713**, own reward **0** both
  seats (invalid action disabled the agent). Did not submit. Kept metav4
  `56395547`. Quota unused. Not gold.
- Metav4 leftover-shed flush (spare slots, skip hour-0 HIREs): all-premium
  **0-2 mean −170**; late strawberry/egg only **−13**. PASS-only courier of
  in-hand premium **−12162**. haideptry 2965 **+50** identical seats.
  DSM goldtape on DSM live seed 706654605 (ICE/BAKERY, where metav4 vs
  itself is only 70439 and live DSM scored 109125) still **0-2 −89895**
  (34206 vs 124101). Ahmed v54 on that weak world is still a **+109**
  identical-seat overlay at ~70k, not DSM's 109k. Destbreso 2026-09-20
  field matrix: almost no public donor beats Tschinkel 2945 (guru v4
  +267). No gold-relevant winner. Did not submit. Kept metav4
  `56395547`. Quota unused. Not gold.

## 2026-09-24 — gold-band replay gate; no-winner

- ListEpisodes for mature metav4 `56395547` (SHA `9d634946`): 184 public
  completed, 1 validation. Public loss or tie versus an opponent whose
  initialScore was at least 2625: **63**. Replay set is the 8 highest
  ratings; the other 55 are listed only. Seeds came from GetEpisode.
  Recorded-seat official 720 replay of those frozen bytes reproduced every
  recorded bank exactly, all `DONE`/`DONE`, **0 wins**. A recorded loss or
  tie stayed a loss or tie.
- Replay set, recorded margin (own − opponent): `111359304` seat 1 rating
  2791.5 **−375**; `111340693` seat 0 2770.6 **−50**; `111313575` seat 1
  2749.4 **tie**; `111302018` seat 1 2746.7 **tie**; `111299745` seat 1
  2744.1 **−50**; `111361412` seat 1 2738.1 **−77**; `111428313` seat 0
  2732.1 **−53**; `111433719` seat 1 2729.9 **−327**.
- Same recorded-seat gate on the two files Kaggle is still scoring.
  `56434565` is those same metav4 bytes, so the same 0/8. GSC `56435986`
  SHA `67a44e39` (`artifacts/submission/metav4_gsc/main.py`) won **4/8**:
  **+1262, −7669, +459, +989, +2879, −472, −53, −327**. Four wins is not
  every game. Neither file is gold-eligible. The earlier 19-seed mirror
  mean +1659 against our own metav4 is not this gate. Clone, fertilizer,
  and low-fertilizer screens were not run.
- Verdict: **no-winner**. Did not submit. Newest submission remains
  `56435986` at 2026-09-21 15:38:45. Root `main.py` still h2 SHA
  `65e6f5cd`. Not gold.

## 2026-09-25 — ice-hold on the gold-band eight; no-winner

- New candidate `experiments/candidates/goldband_icehold/main.py` SHA
  `56d876eb` (not GSC `67a44e39`, not metav4 `9d634946`). One chassis
  change on the GSC sheep wrap: when the opening pair is ice cream +
  yarn, keep the cow buys if the opponent is already ahead in cash.
  Episode `111340693` is that case. GSC turned those cows into sheep
  and the margin fell from metav4's −50 to −7669. An even ice-cream +
  yarn mirror still converts, which is the `111302018` win.
- Official 720 recorded-seat replay, all `DONE`/`DONE`. Margins, own
  minus opponent, beside the GSC margin: `111359304` seat 1 **+1262**
  (GSC +1262); `111340693` seat 0 **−50** (GSC −7669); `111313575`
  seat 1 **+459** (GSC +459); `111302018` seat 1 **+989** (GSC +989);
  `111299745` seat 1 **+2879** (GSC +2879); `111361412` seat 1 **−472**
  (GSC −472); `111428313` seat 0 **−53** (GSC −53); `111433719` seat 1
  **−327** (GSC −327). Repeat of `111340693` returned the same banks
  114165 / 114215. Four GSC wins held. Not 8/8 strict. Clone,
  fertilizer/wheat, and low-fertilizer screens were not run.
- Verdict: **no-winner**. Did not submit. Newest submission remains
  `56435986` at 2026-09-21 15:38:45 (public score on this listing
  1872.8). Root `main.py` still h2 SHA `65e6f5cd`. Not gold.

## 2026-09-27 — milk-hold on the four ice-hold losses; no-winner

- `111428313` (brunch + farmers market) is a same-tape mirror: gap stays
  +50 from turn 144, opponent sells 2 more wheat, final margin −53.
  `111433719` (pet cafe + smoothie) is not. We lead by 148 at turn 648,
  then sell 8 shed milk at price 38 while the recorded opponent holds
  shed milk and sells 7 at 53 on turn 709. Final margin −327. The other
  two losses stay flat gaps (−50 and −472).
- New candidate `experiments/candidates/goldband_milkhold/main.py` SHA
  `ef62bf4a` (not ice-hold `56d876eb`, not GSC `67a44e39`, not metav4
  `9d634946`). One change: on a pet-cafe opening that also has a
  smoothie, hold a milk sell of 8 or more while the price is under 50
  before turn 708, then sell the shed milk. Other openings are
  untouched, so the four ice-hold wins stay.
- Official 720 recorded-seat replay, all `DONE`/`DONE`. Margins beside
  the ice-hold margin: `111359304` seat 1 **+1262** (+1262);
  `111340693` seat 0 **−50** (−50); `111313575` seat 1 **+459** (+459);
  `111302018` seat 1 **+989** (+989); `111299745` seat 1 **+2879**
  (+2879); `111361412` seat 1 **−472** (−472); `111428313` seat 0
  **−53** (−53); `111433719` seat 1 **−154** (−327), banks 65183 /
  65337. Repeat of `111433719` returned the same banks. Not 8/8.
  Clone, fertilizer/wheat, and low-fertilizer screens were not run.
- Verdict: **no-winner**. Did not submit. Newest submission remains
  `56435986` at 2026-09-21 15:38:45 (public score on this listing
  1648.1). Root `main.py` still h2 SHA `65e6f5cd`. Not gold.
