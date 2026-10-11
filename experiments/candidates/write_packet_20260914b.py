"""Write 20260914b study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
    108753975,
    108751924,
    108744906,
    108741805,
    108608562,
    108604498,
    108586169,
    108559476,
    108550653,
    108545775,
    108534412,
    108520439,
]
PREV_14 = [
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
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (AQiDA19 108550653 7c6s vs 8c6s3g BAKERY extra sheep 218/227 extra geese 242/266 wheat 509 vs 17314 -21800; "
    "Hanaro 108545775 9c5s vs 8c6s3g PIZZA extra sheep 218/227 extra geese 242/266 -14377; "
    "Quillbolt 108753975 4c15s vs 8c6s3g FARMERS_MARKET extra sheep 218/227 extra geese 242/266 and we already bought extra sheep 218/242/266 -9650; "
    "Excluding 108520439 7c6s vs 8c6s3g FARMERS_MARKET extra sheep 218/227 extra geese 242/266 -5345) "
    "+ extra-sheep 11s (higuuu 108751924 9c8s vs 7c11s BRUNCH extra sheep 218/227/242/266 already bought -3065) "
    "+ extra-animal YARN 6c11s (Farmer Shuang 108559476 6c11s vs 7c11s extra sheep 218/242/266 already bought -418) "
    "+ identical-clone extra-goose (我是刘大聪 108744906 9c5s3g vs 9c5s3g extra geese 227/242 already bought -9197). "
    "Wins: dupakdungking 108608562 6c12s vs 8c6s3g +9867 extra sheep 218/242/266 already bought; "
    "zg l1218 108534412 6c12s vs 8c6s3g +8548 extra sheep 218/242/266 already bought; "
    "Hanaro 108604498 4c14s vs 8c6s3g +114 extra sheep 218/242/266 already bought; "
    "y3uanm 108741805 9c5s3g vs 9c5s3g identical-clone extra geese 227/242 already bought +54; "
    "maxout 108586169 9c5s3g vs 9c5s3g identical-clone extra geese 227/242 already bought +8. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: AQiDA19/Hanaro/Excluding/Quillbolt lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
    "higuuu already bought extra sheep 227/242/266 and lost 11s; Farmer Shuang already bought 218/242/266 and lost YARN 11s; "
    "我是刘大聪 already bought extra geese 227/242 and lost identical-clone -9197; "
    "y3uanm/maxout already bought extra geese 227/242 and won identical-clone; "
    "dupakdungking/zg l1218/Hanaro already bought extra sheep 218/242/266 and won vs 8c6s3g."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1644.6 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1310.6 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1644.6; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 0 new slugs vs _hunt_20260914. "
    "Public search newest still nathanjacob/no-cow-left-behind-v40-autopsy-fix analysis/dataset wrapper "
    "(already rejected 0914). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)
NOT_COPIED = [
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
    "experiments/20260914_top10_games.json",
]


def dump(name: str, obj) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    hunt = {
        "date": "2026-09-14",
        "packet": "20260914b",
        "kernels_not_in_0914_packet": False,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260914b",
        "inspect_scripts": ["experiments/candidates/scan_hunt_20260914b.py"],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_no_new_notebook",
        "compare_0914": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260914",
            "hunt_report": "experiments/20260914_hunt_report.json",
            "gate": "experiments/20260914_gate.json",
            "note": (
                "No new slug vs _hunt_20260914. Public search newest is still "
                "nathanjacob/no-cow-left-behind-v40-autopsy-fix (lastRunTime 2026-09-14 01:37:45.493000). "
                "Did not re-pull rejected kernels (Ahmed V41 SHA 8951ff93, nathanjacob V40 autopsy dataset wrapper, "
                "prvsiyan reserve-garden, alperen scored-agent SHA 85c8b532, xuantianfengwu adaptive-land-allocator SHA d12f2987, "
                "renjistarfall V39 reprint, alperen metacounter-r1 analysis, xuantianfengwu land-labor-capital, Ahmed V40, "
                "guru V39, yhay81 0913, wei v46d review, Ahmed V39, aurax7 v4, crystalbaby V38, prvsiyan market-ledger, "
                "timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, "
                "municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
            ),
        },
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
        "named_kernels_scanned": [],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "author_list_note": (
            "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. "
            "yamakawanin no rc5. Thomas no new tree. y3uanm no v6."
        ),
        "hunt": [],
    }
    dump("20260914b_hunt_report.json", hunt)

    gate = json.loads((ROOT / "experiments/20260914_gate.json").read_text(encoding="utf-8"))
    gate["packet"] = "20260914b"
    gate["named_kernels_scanned"] = []
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260914b"
    gate["hunt_report"] = "experiments/20260914b_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1644.6
    gate["live"]["shopbag"]["score_complete"] = 1310.6
    gate["rejected"] = [
        {
            "kernel": "nathanjacob/no-cow-left-behind-v40-autopsy-fix",
            "verdict": "reject_analysis_dataset_wrapper",
            "note": (
                "Still the public-search newest (lastRunTime 2026-09-14 01:37:45.493000). "
                "0914 already rejected analysis/dataset wrapper. Did not re-pull."
            ),
        },
    ] + [
        row
        for row in gate["rejected"]
        if row.get("kernel") != "nathanjacob/no-cow-left-behind-v40-autopsy-fix"
    ]
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1644.6 partnered with newer shopbag 56151155 COMPLETE 1310.6 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "No new public later-block vs _hunt_20260914. Public search newest still nathanjacob/no-cow-left-behind-v40-autopsy-fix. "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
        "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: AQiDA19 extra sheep 218/227 extra geese 242/266 -21800; "
        "Hanaro/Excluding/Quillbolt lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
        "higuuu already bought extra sheep 227/242/266 and lost 11s; Farmer Shuang already bought 218/242/266 and lost YARN 11s; "
        "我是刘大聪 already bought extra geese 227/242 and lost identical-clone -9197; "
        "y3uanm already bought extra geese 227/242 and won identical-clone +54."
    )
    dump("20260914b_gate.json", gate)

    algo = json.loads((ROOT / "experiments/20260914_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-14"
    algo["packet"] = "20260914b"
    algo["live"]["cut16"]["csv_0914b_team_score"] = 1644.6
    algo["live"]["shopbag"]["score_complete"] = 1310.6
    algo["live"]["rank_csv_0914b"] = 2088
    algo["cut16_live_failure_class"]["0914b"] = {
        "file": "experiments/20260914b_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [5, 0, 7],
        "mean_margin": -3771.8,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-sheep 11s plus extra-animal YARN 6c11s plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 108550653,
                "opp": "AQiDA19",
                "margin": -21800,
                "shops72": ["BAKERY"],
                "buy": "7c6s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 108545775,
                "opp": "Hanaro",
                "margin": -14377,
                "shops72": ["PIZZA_SHOP"],
                "buy": "9c5s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "No new public slug vs _hunt_20260914. Public search newest still nathanjacob/no-cow-left-behind-v40-autopsy-fix "
            "(already rejected 0914). Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump("20260914b_algo_note.json", algo)

    dump(
        "20260914b_episode_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914b",
            "utc": "2026-09-14T02:42:53Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1644.6,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1644.6 (was 1654.7). Newest public 108753975 updatedScore 1644.607. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1310.6 / ListEpisodes last_updated 1310.643) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1310.6 < 1500 "
                "and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1310.6,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2088,
            "heralces_score": 1644.6,
            "n_teams_csv": 8938,
            "public_56151152": {
                "n_public": 248,
                "n_validation": 1,
                "n_completed_public": 248,
                "wtl": [106, 2, 140],
                "mean_margin": -1487.6,
                "status": "COMPLETE",
                "publicScore": 1644.6,
            },
            "rolling_ids": ROLLING_IDS,
            "rolling_forbidden_0914": PREV_14,
            "ids_not_identical_to_0914": True,
            "ids_disjoint_from_0914": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [5, 0, 7],
            "mean_margin": -3771.8,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260914 packet. 5W 7L. "
                "Worst AQiDA19 108550653 L -21800 7c6s vs 8c6s3g clone=1 extra sheep 218/227 extra geese 242/266. "
                "New-window y3uanm 108741805 W +54 9c5s3g vs 9c5s3g identical-clone extra geese 227/242 already bought. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        "20260914b_cut16_loss_class.json",
        {
            "date": "2026-09-14",
            "packet": "20260914b",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": ROLLING_IDS,
            "ids_0914": PREV_14,
            "disjoint_from_0914": True,
            "all_720_done_done": True,
            "wtl": [5, 0, 7],
            "mean_margin": -3771.8,
            "clone_n": 12,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 27.0],
            "wool_360": {
                "108753975": 231,
                "108751924": 234,
                "108744906": 43,
                "108741805": 37,
                "108608562": 236,
                "108604498": 232,
                "108586169": 37,
                "108559476": 245,
                "108550653": 1,
                "108545775": 1,
                "108534412": 236,
                "108520439": 1,
            },
            "wool_432": {
                "108753975": 200,
                "108751924": 200,
                "108744906": 1,
                "108741805": 1,
                "108608562": 232,
                "108604498": 209,
                "108586169": 1,
                "108559476": 246,
                "108550653": 5,
                "108545775": 24,
                "108534412": 232,
                "108520439": 5,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14: extra-animal 8c6s3g plus extra-sheep 11s plus extra-animal YARN 6c11s plus identical-clone extra-goose. "
                "WTL 5-0-7 mean -3771.8 vs 09-14 2-0-10 mean -7857.2. New window games are Quillbolt 108753975 -9650, higuuu 108751924 -3065, "
                "我是刘大聪 108744906 -9197, y3uanm 108741805 +54. clone=12/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 108550653,
                    "opp": "AQiDA19",
                    "margin": -21800.0,
                    "herd_us": "7c6s",
                    "herd_opp": "8c6s3g",
                    "shops": ["BAKERY"],
                }
            ],
        },
    )

    dump(
        "20260914b_study_packet.json",
        {
            "title": "Kaggriculture study packet 2026-09-14b",
            "not_the_0914_packet": True,
            "no_upload": NO_UPLOAD,
            "upload_bail": True,
            "upload_bail_reasons": {
                "a_newest_cut_pending": False,
                "b_newest_cut_complete_below_1500": False,
                "c_drop_ge1500_without_ge1500_partner": True,
            },
            "sources": {
                "leaderboard_zip": "artifacts/kaggle_runs/lb_20260914b/kaggriculture.zip",
                "leaderboard_csv": "artifacts/kaggle_runs/lb_20260914b/kaggriculture-publicleaderboard-2026-09-14T02-42-53.csv",
                "leaderboard_api": "experiments/20260914b_public_leaderboard_api.json",
                "episodes_cut16": "experiments/episodes_56151152.json",
                "cut16_replays": "artifacts/kaggle_runs/cut16_20260914b",
                "top_replays": "artifacts/kaggle_runs/top_20260914b",
                "hunt_dir": "artifacts/public_sources/_hunt_20260914b",
                "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
                "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
                "gate": "experiments/20260914b_gate.json",
                "episode_report": "experiments/20260914b_episode_report.json",
                "hunt_report": "experiments/20260914b_hunt_report.json",
                "algo_note": "experiments/20260914b_algo_note.json",
                "loss_class": "experiments/20260914b_cut16_loss_class.json",
            },
            "live": {
                "sixday": 56028043,
                "sixday_score": 1590.8,
                "sixday_status": "COMPLETE",
                "team_score": 1644.6,
                "rank": 2088,
                "n_teams": 8938,
                "shopbag_previous": 56112309,
                "shopbag_reupload": 56151155,
                "shopbag_status": "COMPLETE",
                "shopbag_score": 1310.6,
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
                "cut16_score": 1644.6,
                "root_main_py": "h2 65e6f5cd... unchanged",
                "gold21": 2925.8,
                "rank10": {"team": "Otter Vibe", "score": 2954.1},
                "rank1": {
                    "team": "Majkel1337",
                    "score": 3197.1,
                    "submissionId": 56156662,
                },
                "public_cut16": {
                    "n": 248,
                    "wtl": [106, 2, 140],
                    "mean_margin": -1487.6,
                },
            },
            "rolling": {
                "previous": "experiments/20260914_cut16_rolling.json",
                "live_cut16": "experiments/20260914b_cut16_rolling.json",
                "ids": ROLLING_IDS,
                "ids_not_identical_to_0914": True,
                "n": 12,
                "wtl": [5, 0, 7],
                "mean_margin": -3771.8,
                "loss_class": LOSS_CLASS,
            },
            "excluding": {
                "id": 108550653,
                "margin": -21800.0,
                "clone": True,
                "Q": [3, 3],
                "land": [151, 266],
                "herd_us": "7c6s",
                "herd_opp": "8c6s3g",
                "sheep_steps_us": [2, 151, 196],
            },
            "top_board": {
                "source": "experiments/20260914b_top10_games.json",
                "not_copied_from": NOT_COPIED,
                "Majkel1337": {
                    "land": [
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                    ],
                    "herd": ["7c5s3g", "7c15s0g", "9c3s2g", "10c3s2g"],
                    "wheat": [508, 441, 444, 465],
                    "shops": ["FARMERS_MARKET", "ICE_CREAM_SHOP", "ICE_CREAM_SHOP", "FARMERS_MARKET"],
                    "clone": "0_of_4",
                    "episodes": [108751322, 108746349, 108741955, 108719359],
                    "note": (
                        "CSV #1 3197.1 live 3197.1 scoring sub 56156662 (current sub 56216119 is 2870.6). "
                        "Ids disjoint from 20260914 Majkel set. Mid-land 150 then 220-222 (four 150/220/222), "
                        "wheat 441-508, clone=0 on 4/4, goose mix 3g/0g/2g/2g. Opening land is not a later-block license."
                    ),
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
                "score": 1644.6,
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
                    "Already live COMPLETE 1644.6. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                    "Rolling 108550653 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -21800; 108545775 extra sheep 218/227 extra geese 242/266 -14377; "
                    "108753975 extra sheep 218/242/266 already bought and lost 15s vs 8c6s3g -9650. New-window y3uanm 108741805 already bought extra geese 227/242 and won identical-clone +54. Not cut 12/13."
                ),
            },
            "cut17": {
                "hold": True,
                "uploaded": None,
                "why": (
                    "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: no new slug vs 0914; "
                    "public search newest still nathanjacob/no-cow-left-behind-v40-autopsy-fix; "
                    "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                    "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1644.6 and keeps 1310.6."
                ),
            },
            "hunt": hunt["hunt"],
        },
    )


if __name__ == "__main__":
    main()
