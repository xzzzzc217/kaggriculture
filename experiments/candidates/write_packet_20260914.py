"""Write 20260914 study packet JSON reports. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
    108723413,
    108704919,
    108686716,
    108669139,
    108658948,
    108656070,
    108642657,
    108636667,
    108635673,
    108620320,
    108594800,
    108568560,
]
PREV_13V = [
    108608562,
    108604498,
    108586169,
    108550653,
    108545775,
    108520439,
    108509931,
    108489181,
    108484081,
    108445221,
    108441448,
    108441305,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (LuanHengYu 108636667 9c5s vs 8c6s3g PET_CAFE extra sheep 218/227 extra geese 242/266 wheat 396 vs 13489 -20223; "
    "Les 2 oies 108642657 9c5s3g vs 8c6s3g SMOOTHIE extra sheep 218/227 extra geese 242/266 -12935; "
    "BigAngel 108635673 7c6s vs 8c6s3g BRUNCH extra sheep 218/227 extra geese 242/266 -5892) "
    "+ extra-sheep 8c9s (Pietro Valocchi 108658948 7c6s vs 8c9s FARMERS_MARKET extra sheep 218/227/242/266 -12549) "
    "+ extra-sheep 16s (Gracie 108656070 9c8s vs 7c16s1g PIZZA extra sheep 218/221/222/242/249/530 clone=0 -14565) "
    "+ extra-sheep 15s (Akhil Chinta 108620320 4c15s vs 6c10s extra sheep 218/242/266 already bought -1911) "
    "+ extra-goose 6g (here we go 108704919 9c5s3g vs 6c6s6g extra geese 218/227/242 already bought -7788; "
    "higuuu 108594800 9c5s3g vs 6c6s6g extra geese 218/227/242 already bought -1087) "
    "+ extra-goose 3g (alcanta 108568560 9c5s vs 9c5s3g extra cow 218 extra sheep 227 extra geese 242/266 -19224) "
    "+ identical-clone extra-goose (Cuong Le 108686716 9c5s3g vs 9c5s3g extra geese 227/242 already bought -590). "
    "Wins: zard599 108723413 9c5s3g vs 9c5s4g extra geese 227/242 already bought +748; "
    "Surya Bhattiprol 108669139 9c5s3g vs 9c5s4g extra geese 227/242 already bought +1729. "
    "clone=11/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: LuanHengYu/Les 2 oies/BigAngel lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
    "Pietro extra sheep 218/227/242/266 and we lost; Gracie extra sheep 218+ clone=0 and we lost 16s; "
    "Akhil already bought 218/242/266 and lost 15s; here we go/higuuu already bought extra geese 227/242 and lost 6g; "
    "alcanta extra cow 218 extra sheep 227 extra geese 242/266 and we lost; Cuong Le already bought extra geese 227/242 and lost identical-clone -590; "
    "zard599/Surya already bought extra geese 227/242 and won 9c5s4g."
)
HUNT = [
    {
        "kernel": "ahmedberatozer/kaggriculture-v41-review-candidate",
        "path": "artifacts/public_sources/_hunt_20260914/ahmedberatozer__kaggriculture-v41-review-candidate/kaggriculture-v41-review-candidate.ipynb",
        "verdict": "reject_v41_shop0909_overlay",
        "sha256": "8951ff93742015cba535b125223cf2e541bb7b602080fc4584f30c2613d210f3",
        "note": "New slug vs _hunt_20260913v (lastRunTime 2026-09-13 22:21:39.587000). Python %%writefile main.py SHA 8951ff93... Distinct from V40 SHA 546c4224 and V39 708c7485 and live cuts 14/15/16. Shop0909 day-6 144/648 plus 288/696 sales overlay plus step==712 terminal planner. 216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5.",
    },
    {
        "kernel": "nathanjacob/no-cow-left-behind-v40-autopsy-fix",
        "path": "artifacts/public_sources/_hunt_20260914/nathanjacob__no-cow-left-behind-v40-autopsy-fix/no-cow-left-behind-v40-autopsy-fix.ipynb",
        "verdict": "reject_analysis_dataset_wrapper",
        "sha256": None,
        "note": "New slug vs _hunt_20260913v (lastRunTime 2026-09-14 01:37:45.493000; public-search newest by dateCreated). Analysis of Ahmed V40 plus shutil.copy of companion dataset submission.tar.gz. No %%writefile agent. Cells not executed. Did not pull the dataset. Not a later-block.",
    },
    {
        "kernel": "prvsiyan/kaggriculture-reserve-garden-counterfactuals",
        "path": "artifacts/public_sources/_hunt_20260914/prvsiyan__kaggriculture-reserve-garden-counterfactuals/kaggriculture-reserve-garden-counterfactuals.ipynb",
        "verdict": "reject_educational_framework",
        "sha256": None,
        "note": "New slug vs _hunt_20260913v (lastRunTime 2026-09-13 21:15:06.187000). Educational Path.write_text reserve_garden_policy.py, not %%writefile main.py. Distinct from already-rejected prvsiyan market-ledger SHA 1c98c297. No farm/route reselect after 216. Cells not executed. Not copied to candidates/.",
    },
    {
        "kernel": "alperen5252525/kaggriculture-metacounter-r1-scored-agent",
        "path": "artifacts/public_sources/_hunt_20260914/alperen5252525__kaggriculture-metacounter-r1-scored-agent/kaggriculture-metacounter-r1-scored-agent.py",
        "verdict": "reject_day6_144_648_and_712_overlay",
        "sha256": "85c8b53208a311e9101cf27ce02918e90b925e5b108d572a306d3b08a83dbdc3",
        "note": "New slug vs _hunt_20260913v (lastRunTime 2026-09-13 22:03:43.617000). Script kernel SHA 85c8b532... day-6 144/648 plus Shop0909 288 quote overlay. Distinct from already-rejected analysis metacounter-r1 (no writefile). Not a farm/route reselect after 216. No ctypes/agent.so. Not copied to candidates/; not clone/G5.",
    },
    {
        "kernel": "xuantianfengwu/kaggriculture-adaptive-land-allocator",
        "path": "artifacts/public_sources/_hunt_20260914/xuantianfengwu__kaggriculture-adaptive-land-allocator/kaggriculture-adaptive-land-allocator.ipynb",
        "verdict": "reject_heuristic_six_cow_allocator",
        "sha256": "d12f29875f137e7429dec73e1d5aadf33147a21f3b3505c7d49d60d094ae454b",
        "note": "New slug vs _hunt_20260913v (lastRunTime 2026-09-13 18:25:50.667000). Python %%writefile submission.py SHA d12f2987... heuristic 6-cow (`[\"COW\"] * 6`). Distinct from land-labor-capital SHA b49709bd and timed-six-cow SHA 5dc0c68c. No later-block after 216. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/.",
    },
]


def dump(name: str, obj) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    dump(
        "20260914_study_packet.json",
        {
            "title": "Kaggriculture study packet 2026-09-14",
            "not_the_0913v_packet": True,
            "no_upload": (
                "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1654.7 would drop without a >=1500 COMPLETE newest-2 partner "
                "(shopbag 56151155 COMPLETE 1309.4 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1654.7; "
                "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 5 new slugs vs _hunt_20260913v, none later-block: "
                "Ahmed V41 SHA 8951ff93 Shop0909 144/648 + 288/712 overlay; nathanjacob V40 autopsy dataset wrapper; "
                "prvsiyan reserve-garden educational; alperen scored-agent SHA 85c8b532 day-6 144/648 overlay; "
                "xuantianfengwu adaptive-land-allocator SHA d12f2987 heuristic 6-cow. Do not reupload boatlee 55710781. Cut 12/13 Hold."
            ),
            "upload_bail": True,
            "upload_bail_reasons": {
                "a_newest_cut_pending": False,
                "b_newest_cut_complete_below_1500": False,
                "c_drop_ge1500_without_ge1500_partner": True,
            },
            "sources": {
                "leaderboard_zip": "artifacts/kaggle_runs/lb_20260914/kaggriculture.zip",
                "leaderboard_csv": "artifacts/kaggle_runs/lb_20260914/kaggriculture-publicleaderboard-2026-09-14T01-41-29.csv",
                "leaderboard_api": "experiments/20260914_public_leaderboard_api.json",
                "episodes_cut16": "experiments/episodes_56151152.json",
                "cut16_replays": "artifacts/kaggle_runs/cut16_20260914",
                "top_replays": "artifacts/kaggle_runs/top_20260914",
                "hunt_dir": "artifacts/public_sources/_hunt_20260914",
                "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
                "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
                "gate": "experiments/20260914_gate.json",
                "episode_report": "experiments/20260914_episode_report.json",
                "hunt_report": "experiments/20260914_hunt_report.json",
                "algo_note": "experiments/20260914_algo_note.json",
                "loss_class": "experiments/20260914_cut16_loss_class.json",
            },
            "live": {
                "sixday": 56028043,
                "sixday_score": 1590.8,
                "sixday_status": "COMPLETE",
                "team_score": 1654.7,
                "rank": 2068,
                "n_teams": 8938,
                "shopbag_previous": 56112309,
                "shopbag_reupload": 56151155,
                "shopbag_status": "COMPLETE",
                "shopbag_score": 1309.4,
                "newest_2": [56151155, 56151152],
                "fieldbook": 55962758,
                "fieldbook_score": 1762.9,
                "cut14": 56111821,
                "cut14_status": "COMPLETE",
                "cut14_score": 1799.3,
                "cut15": 56146106,
                "cut15_status": "COMPLETE",
                "cut15_score": 1864.4,
                "cut16": 56151152,
                "cut16_status": "COMPLETE",
                "cut16_score": 1654.7,
                "root_main_py": "h2 65e6f5cd... unchanged",
                "gold21": 2926.0,
                "rank10": {"team": "Otter Vibe", "score": 2948.5},
                "rank1": {
                    "team": "Majkel1337",
                    "score": 3189.8,
                    "submissionId": 56156662,
                },
                "public_cut16": {
                    "n": 244,
                    "wtl": [105, 2, 137],
                    "mean_margin": -1422.4,
                },
            },
            "rolling": {
                "previous": "experiments/20260913v_cut16_rolling.json",
                "live_cut16": "experiments/20260914_cut16_rolling.json",
                "ids": ROLLING_IDS,
                "ids_not_identical_to_0913v": True,
                "n": 12,
                "wtl": [2, 0, 10],
                "mean_margin": -7857.2,
                "loss_class": LOSS_CLASS,
            },
            "excluding": {
                "id": 108636667,
                "margin": -20223.0,
                "clone": True,
                "Q": [3, 3],
                "land": [151, 266],
                "herd_us": "9c5s",
                "herd_opp": "8c6s3g",
                "sheep_steps_us": [2, 196, 314],
            },
            "top_board": {
                "source": "experiments/20260914_top10_games.json",
                "not_copied_from": [
                    "experiments/20260904_top10_games.json",
                    "experiments/20260905_top10_games.json",
                    "experiments/20260906_top10_games.json",
                    "experiments/20260909_top10_games.json",
                    "experiments/20260910_top10_games.json",
                    "experiments/20260911_top10_games.json",
                    "experiments/20260911b_top10_games.json",
                    "experiments/20260912_top10_games.json",
                    "experiments/20260912b_top10_games.json",
                    "experiments/20260912c_top10_games.json",
                    "experiments/20260912d_top10_games.json",
                    "experiments/20260912e_top10_games.json",
                    "experiments/20260913_top10_games.json",
                    "experiments/20260913b_top10_games.json",
                    "experiments/20260913c_top10_games.json",
                    "experiments/20260913d_top10_games.json",
                    "experiments/20260913e_top10_games.json",
                    "experiments/20260913f_top10_games.json",
                    "experiments/20260913g_top10_games.json",
                    "experiments/20260913h_top10_games.json",
                    "experiments/20260913i_top10_games.json",
                    "experiments/20260913j_top10_games.json",
                    "experiments/20260913k_top10_games.json",
                    "experiments/20260913l_top10_games.json",
                    "experiments/20260913m_top10_games.json",
                    "experiments/20260913n_top10_games.json",
                    "experiments/20260913o_top10_games.json",
                    "experiments/20260913p_top10_games.json",
                    "experiments/20260913q_top10_games.json",
                    "experiments/20260913r_top10_games.json",
                    "experiments/20260913s_top10_games.json",
                    "experiments/20260913t_top10_games.json",
                    "experiments/20260913u_top10_games.json",
                    "experiments/20260913v_top10_games.json",
                ],
                "Majkel1337": {
                    "land": [
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 218],
                    ],
                    "herd": ["9c6s2g", "9c3s2g", "8c9s2g", "8c5s2g"],
                    "wheat": [469, 567, 515, 569],
                    "shops": ["PIZZA_SHOP", "PIZZA_SHOP", "PIZZA_SHOP", "BAKERY"],
                    "clone": "0_of_4",
                    "episodes": [108737107, 108732800, 108727954, 108723695],
                    "note": "CSV #1 3189.8 live 3189.8 scoring sub 56156662 (current sub 56216119 is 2778.2). Ids disjoint from 20260913v Majkel set. Mid-land 150 then 218-222 (three 150/220/222; one 150/218), wheat 469-569, clone=0 on 4/4, goose 2g/2g/2g/2g. Opening land is not a later-block license.",
                },
            },
            "cut12": {
                "hold": True,
                "reused": False,
                "why": "Already lost recorded-seat vs Deskbo. No flipping evidence vs Deskbo 105744091 AND Stefano 105798735 or fufu 105790145. This cycle did not re-upload it.",
            },
            "cut13": {
                "hold": True,
                "reused": False,
                "why": "Already lost recorded-seat vs Deskbo/Stefano/fufu. This cycle did not re-upload it. Not a 227/242/266 BALANCED wrap.",
            },
            "cut15": {
                "name": "thomastschinkel later-block reselect 144/288/432/576",
                "hold": False,
                "uploaded": 56146106,
                "status": "COMPLETE",
                "score": 1864.4,
                "dropped_from_newest_2": True,
                "windows_agent_so": False,
            },
            "cut16": {
                "name": "yamakawanin king-v4e-rc4 shop-family later-block P3+ 288/360/432/576",
                "hold": False,
                "uploaded": 56151152,
                "status": "COMPLETE",
                "score": 1654.7,
                "windows_agent_so": False,
                "kernel": "yamakawanin/king-v4e-rc4",
                "agent_sha256": "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d",
                "reselect_steps": [216, 240, 241, 288, 360, 385, 432, 576],
                "reselect_after_216": [240, 241, 288, 360, 385, 432, 576],
                "sheep_200_267": [226, 241, 265],
                "not_227_242_266_wrap": True,
                "clone_g5": {
                    "prvsiyan_clone": 12627.0,
                    "fufu_clone": 12014.0,
                    "masa_clone": 40050.0,
                    "subin_97399969": 27159.0,
                    "james_95677563": 77153.0,
                },
                "why": (
                    "Already live COMPLETE 1654.7. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                    "Rolling 108636667 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -20223; 108568560 extra cow 218 extra sheep 227 extra geese 242/266 9c5s3g -19224; "
                    "108656070 extra sheep 218+ 16s clone=0 -14565. New-window zard599 108723413 already bought extra geese 227/242 and won 9c5s4g +748. Not cut 12/13."
                ),
            },
            "cut17": {
                "hold": True,
                "uploaded": None,
                "why": (
                    "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt 5 new slugs vs 0913v: Ahmed V41 SHA 8951ff93 Shop0909 144/648 + 288/712 overlay; "
                    "nathanjacob dataset wrapper; prvsiyan educational; alperen scored-agent SHA 85c8b532 day-6 144/648; xuantianfengwu SHA d12f2987 heuristic 6-cow. "
                    "No king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1654.7 and keeps 1309.4."
                ),
            },
            "hunt": HUNT,
        },
    )

    dump(
        "20260914_gate.json",
        {
            "date": "2026-09-14",
            "packet": "20260914",
            "freeze": False,
            "hold": True,
            "candidate": None,
            "clone_g5_run": False,
            "extracted_later_block_agent": False,
            "cells_executed": False,
            "rejected": [
                {
                    "kernel": h["kernel"],
                    "verdict": h["verdict"],
                    "note": h["note"],
                }
                for h in HUNT
            ]
            + [
                {
                    "kernel": "renjistarfall/kaggriculture-best-agent",
                    "verdict": "reject_v39_reprint_shop0909_overlay",
                    "note": "Still a public search hit (lastRunTime 2026-09-13 14:11:05.950000). 0913s/0913t/0913u/0913v already rejected SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
                },
                {
                    "kernel": "yhay81/shop-router-0913",
                    "verdict": "reject_day6_144_648",
                    "note": "Author list: still newest Yusuke kaggriculture kernel. 0913o already rejected SHA 77cf6772 day-6 144/648. Did not re-pull.",
                },
                {
                    "kernel": "yamakawanin/king-v4e-rc4",
                    "verdict": "cut16_already_live",
                    "note": "Author list: no rc5. Already uploaded as 56151152 SHA 26ffba52. Do not re-upload.",
                },
                {
                    "kernel": "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                    "verdict": "cut15_already_live",
                    "note": "Already uploaded as 56146106 SHA b87a27ed. Do not re-upload.",
                },
                {
                    "kernel": "y3uanm/kaggriculture-safe-baseline-rollback-v20",
                    "verdict": "cut14_already_live",
                    "note": "Author list: still newest y3uanm kaggriculture kernel. Writefile SHA acf7c664 = live cut 14. Did not re-pull.",
                },
            ],
            "cut12_hold": True,
            "cut13_hold": True,
            "cut12_13_note": "No new recorded-seat flipping evidence vs Deskbo 105744091 AND Stefano 105798735 or fufu 105790145. Prior losses stand. Extra-animal 8c6s3g / extra-goose / extra-sheep is not a milk-heavy license. Did not re-screen.",
            "not_227_wrap": True,
            "root_main_untouched": True,
            "root_main_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "no_upload": True,
            "no_kaggle_submit": True,
            "windows_agent_so": False,
            "engine": "kaggle-environments==1.32.7",
            "live": {
                "cut14": {"name": "y3uanm_router_v5", "submissionId": 56111821, "sha256": "acf7c664"},
                "cut15": {"name": "thomastschinkel_psr_938", "submissionId": 56146106, "sha256": "b87a27ed"},
                "cut16": {
                    "name": "yamakawanin_king_v4e_rc4",
                    "submissionId": 56151152,
                    "score_complete": 1654.7,
                    "sha256": "26ffba52",
                },
                "shopbag": {
                    "submissionId": 56151155,
                    "score_complete": 1309.4,
                    "newer_than_cut16": True,
                },
            },
            "upload_bail": True,
            "hunt_dir": "artifacts/public_sources/_hunt_20260914",
            "hunt_report": "experiments/20260914_hunt_report.json",
            "named_kernels_scanned": [
                "ahmedberatozer/kaggriculture-v41-review-candidate",
                "nathanjacob/no-cow-left-behind-v40-autopsy-fix",
                "prvsiyan/kaggriculture-reserve-garden-counterfactuals",
                "alperen5252525/kaggriculture-metacounter-r1-scored-agent",
                "xuantianfengwu/kaggriculture-adaptive-land-allocator",
            ],
            "author_list_no_new_later_block": [
                "yhay81/shop-router-0913",
                "yamakawanin/king-v4e-rc4",
                "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "y3uanm/kaggriculture-conservative-market-router-v5",
                "y3uanm/kaggriculture-safe-baseline-rollback-v20",
            ],
            "why": (
                "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1654.7 partnered with newer shopbag 56151155 COMPLETE 1309.4 < 1500. "
                "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). "
                "freeze is false because of this upload-bail, not because a licensed later-block is ready. Five new public slugs vs _hunt_20260913v, none licensed later-block. "
                "Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded."
            ),
        },
    )

    dump(
        "20260914_episode_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914",
            "utc": "2026-09-14T01:41:29Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1654.7,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1654.7 (was 1681.2). Newest public 108723413 updatedScore 1654.766. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1309.4 / ListEpisodes last_updated 1309.485) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1309.4 < 1500 "
                "and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1309.4,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2068,
            "heralces_score": 1654.7,
            "n_teams_csv": 8938,
            "public_56151152": {
                "n_public": 244,
                "n_validation": 1,
                "n_completed_public": 244,
                "wtl": [105, 2, 137],
                "mean_margin": -1422.4,
                "status": "COMPLETE",
                "publicScore": 1654.7,
            },
            "rolling_ids": ROLLING_IDS,
            "rolling_forbidden_0913v": PREV_13V,
            "ids_not_identical_to_0913v": True,
            "ids_disjoint_from_0913v": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [2, 0, 10],
            "mean_margin": -7857.2,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913v packet. 2W 10L. "
                "Worst LuanHengYu 108636667 L -20223 9c5s vs 8c6s3g clone=1 extra sheep 218/227 extra geese 242/266. "
                "New-window zard599 108723413 W +748 9c5s3g vs 9c5s4g extra geese 227/242 already bought. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        "20260914_hunt_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914",
            "no_upload": True,
            "no_kaggle_submit": True,
            "cells_executed": False,
            "extracted_later_block_agent": False,
            "later_block_python_after_216": False,
            "any_licensed_for_extract": False,
            "licensed_kernel": None,
            "root_main_py": "unchanged",
            "hunt_dir": "artifacts/public_sources/_hunt_20260914",
            "inspect_scripts": ["experiments/candidates/scan_hunt_20260914.py"],
            "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
            "payload_decode": "writefile_sha_only_no_candidates",
            "public_search_newest": "nathanjacob/no-cow-left-behind-v40-autopsy-fix",
            "public_search_newest_lastRunTime": "2026-09-14 01:37:45.493000",
            "live_cuts_not_matched": {
                "cut14": {"name": "y3uanm_router_v5", "sha256_prefix": "acf7c664", "reselect": [226, 360, 433]},
                "cut15": {
                    "name": "thomastschinkel_psr_938",
                    "sha256_prefix": "b87a27ed",
                    "reselect": [144, 288, 432, 576],
                },
                "cut16": {
                    "name": "yamakawanin_king_v4e_rc4",
                    "sha256_prefix": "26ffba52",
                    "reselect": ["P3+", 288, 360, 432, 576],
                    "extra_sheep": [226, 241, 265],
                },
            },
            "not_227_242_266_fieldbook_balanced_wrap": True,
            "named_kernels_scanned": [h["kernel"] for h in HUNT],
            "author_list_no_new_later_block": [
                "yhay81/shop-router-0913",
                "yamakawanin/king-v4e-rc4",
                "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
                "y3uanm/kaggriculture-conservative-market-router-v5",
                "y3uanm/kaggriculture-safe-baseline-rollback-v20",
            ],
            "author_list_note": "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6.",
            "hunt": HUNT,
            "kernels_not_in_0913v_packet": True,
            "compare_0913v": {
                "hunt_dir": "artifacts/public_sources/_hunt_20260913v",
                "hunt_report": "experiments/20260913v_hunt_report.json",
                "gate": "experiments/20260913v_gate.json",
                "note": (
                    "Five new slugs vs _hunt_20260913v. Public search newest is now nathanjacob/no-cow-left-behind-v40-autopsy-fix (lastRunTime 2026-09-14 01:37:45.493000). "
                    "Did not re-pull already-rejected kernels (renjistarfall V39 reprint, alperen metacounter-r1 analysis, xuantianfengwu land-labor-capital, Ahmed V40, guru V39, yhay81 0913, wei v46d review, Ahmed V39, aurax7 v4, crystalbaby V38, Ahmed V39 notebookda72f457f5, prvsiyan market-ledger, timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
                ),
            },
        },
    )

    dump(
        "20260914_cut16_loss_class.json",
        {
            "date": "2026-09-14",
            "packet": "20260914",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": ROLLING_IDS,
            "all_720_done_done": True,
            "wtl": [2, 0, 10],
            "mean_margin": -7857.2,
            "clone_n": 11,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 27.0],
            "wool_360": {
                "108723413": 43,
                "108704919": 174,
                "108686716": 183,
                "108669139": 43,
                "108658948": 1,
                "108656070": 227,
                "108642657": 1,
                "108636667": 1,
                "108635673": 1,
                "108620320": 237,
                "108594800": 11,
                "108568560": 1,
            },
            "wool_432": {
                "108723413": 1,
                "108704919": 161,
                "108686716": 189,
                "108669139": 1,
                "108658948": 1,
                "108656070": 129,
                "108642657": 1,
                "108636667": 1,
                "108635673": 5,
                "108620320": 234,
                "108594800": 1,
                "108568560": 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-13v: extra-animal 8c6s3g plus extra-sheep plus extra-goose plus identical-clone extra-goose. "
                "WTL 2-0-10 mean -7857.2 vs 09-13v 6-0-6 mean -3106.3. New window games are zard599 108723413 +748 and Surya 108669139 +1729. clone=11/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 108636667,
                    "opp": "LuanHengYu",
                    "margin": -20223.0,
                    "herd_us": "9c5s",
                    "herd_opp": "8c6s3g",
                    "shops": ["PET_CAFE"],
                }
            ],
            "ids_0913v": PREV_13V,
            "disjoint_from_0913v": True,
        },
    )

    prev = json.loads((ROOT / "experiments/20260913v_algo_note.json").read_text(encoding="utf-8"))
    prev["date"] = "2026-09-14"
    prev["packet"] = "20260914"
    prev["live"]["cut16"]["csv_0914_team_score"] = 1654.7
    prev["live"]["shopbag"]["score_complete"] = 1309.4
    prev["live"]["rank_csv_0914"] = 2068
    prev["cut16_live_failure_class"]["0914"] = {
        "file": "experiments/20260914_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [2, 0, 10],
        "mean_margin": -7857.2,
        "clone": "11/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-sheep 8c9s/16s/15s plus extra-goose 6g/3g plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 108636667,
                "opp": "LuanHengYu",
                "margin": -20223,
                "shops72": ["PET_CAFE"],
                "buy": "9c5s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 108568560,
                "opp": "alcanta",
                "margin": -19224,
                "shops72": ["SMOOTHIE_SHOP"],
                "buy": "9c5s vs 9c5s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
        ],
    }
    prev["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. Five new public slugs vs 0913v: "
            "Ahmed V41 writefile SHA 8951ff93 Shop0909 144/648 + 288/712 overlay; nathanjacob analysis/dataset wrapper; "
            "prvsiyan educational; alperen scored-agent SHA 85c8b532 day-6 144/648 overlay; xuantianfengwu SHA d12f2987 heuristic 6-cow. "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump("20260914_algo_note.json", prev)


if __name__ == "__main__":
    main()
