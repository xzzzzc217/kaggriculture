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
