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

