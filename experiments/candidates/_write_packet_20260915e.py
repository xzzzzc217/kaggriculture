"""Write 20260915e study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "20260915e"
PREV = "20260915d"

ROLLING_IDS = [
    109329693,
    109297997,
    109184094,
    109178619,
    109169017,
    109168637,
    109159847,
    109152510,
    109149160,
    109142116,
    109135062,
    109111080,
]
PREV_IDS = [
    109323301,
    109321947,
    109316981,
    109309340,
    109274859,
    109251218,
    109247247,
    109241224,
    109227483,
    109208871,
    109205772,
    109205359,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (Huy Lê Ngọc Gia 109178619 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -13645; "
    "Filip Strzałka 109159847 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -6855) "
    "+ extra-goose vs extra-cow (Gaddam Shiva Teja 109297997 9c5s3g vs 11c5s ICE_CREAM extra geese 227/242 already bought vs extra cow -26009) "
    "+ identical-clone extra-goose (3G 109168637 9c5s3g vs 9c5s3g ICE_CREAM extra geese 227/242 already bought -10063) "
    "+ extra-sheep (Dhruv #2 109149160 4c15s vs 6c10s BRUNCH extra sheep 218/242/266 already bought vs extra sheep 218-265 -12590; "
    "Grim Reaper 109169017 6c11s vs 3c13s2g YARN extra sheep 218/242/266 already bought vs extra sheep 218-265 -10132) "
    "+ extra-goose (Corgi-Samoyed 109329693 9c5s3g vs 6c6s6g BAKERY extra geese 227/242 already bought vs 6g -325). "
    "Wins: Suliman Tadros 109152510 4c15s vs 9c3s PET_CAFE +43169 extra sheep 218/242/266 clone=0; "
    "Stephen Schott 109184094 4c15s vs 8c6s3g ICE_CREAM +13159 extra sheep 218/242/266 already bought; "
    "Yichi 109111080 9c8s vs 9c5s3g BRUNCH +6951 extra sheep 227/242/266 already bought; "
    "Duc-Anh Nguyen 109135062 9c5s3g vs 9c5s4g PIZZA +2713 extra geese 227/242 already bought vs 4g; "
    "ocean240812 109142116 9c8s vs 6c6s6g BAKERY +74 extra sheep 227/242/266 already bought. "
    "clone=11/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 1-29. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Gaddam already bought extra geese 227/242 and lost vs 11c; "
    "Corgi already bought extra geese 227/242 and lost vs 6g; 3G identical extra-goose lost; "
    "Duc-Anh extra geese 227/242 won vs 4g; Huy/Filip extra cow 218 lost vs 8c6s3g; "
    "Dhruv/Grim extra sheep 218-266 already bought and lost."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1569.5 (CSV and submissions 1569.5, was 1573.9 / 1578.6) would drop without a "
    ">=1500 COMPLETE newest-2 partner (shopbag 56151155 COMPLETE 1282.2 < 1500 and newer than cut 16; "
    "a new cut alone keeps shopbag and drops 1569.5; re-upload is 600-provisional not a partner). "
    "No licensed later-block. Hunt 0 new slugs vs _hunt_20260915d (public search newest still "
    "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race lastRunTime 2026-09-15 14:58:50.740000 "
    "already rejected SHA 797d9bca; did not re-pull). Author lists: no Yusuke later-block, no king rc5, no y3uanm v6. "
    "Do not reupload boatlee 55710781. Cut 12/13 Hold."
)
PRIOR_TOP = [
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
    "experiments/20260914b_top10_games.json",
    "experiments/20260914c_top10_games.json",
    "experiments/20260914d_top10_games.json",
    "experiments/20260914e_top10_games.json",
    "experiments/20260914f_top10_games.json",
    "experiments/20260914g_top10_games.json",
    "experiments/20260914h_top10_games.json",
    "experiments/20260914i_top10_games.json",
    "experiments/20260914j_top10_games.json",
    "experiments/20260914k_top10_games.json",
    "experiments/20260914l_top10_games.json",
    "experiments/20260914m_top10_games.json",
    "experiments/20260914n_top10_games.json",
    "experiments/20260914o_top10_games.json",
    "experiments/20260915_top10_games.json",
    "experiments/20260915b_top10_games.json",
    "experiments/20260915c_top10_games.json",
    "experiments/20260915d_top10_games.json",
]


def dump(name: str, payload: dict) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    packet = {
        "title": "Kaggriculture study packet 2026-09-15e",
        "not_the_0915d_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260915e/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260915e/kaggriculture-publicleaderboard-2026-09-15T16-00-41.csv",
            "leaderboard_api": "experiments/20260915e_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260915e",
            "top_replays": "artifacts/kaggle_runs/top_20260915e",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915e",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260915e_gate.json",
            "episode_report": "experiments/20260915e_episode_report.json",
            "hunt_report": "experiments/20260915e_hunt_report.json",
            "algo_note": "experiments/20260915e_algo_note.json",
            "loss_class": "experiments/20260915e_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1569.5,
            "rank": 2319,
            "n_teams": 9139,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1282.2,
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
            "cut16_score": 1569.5,
            "cut16_submissions_api_score": 1569.5,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2938.0,
            "rank10": {"team": "leave you", "score": 2985.6},
            "rank1": {
                "team": "Majkel1337",
                "score": 3155.3,
                "submissionId": 56216119,
            },
            "public_cut16": {"n": 306, "wtl": [125, 2, 179], "mean_margin": -2116.4},
        },
        "rolling": {
            "previous": "experiments/20260915d_cut16_rolling.json",
            "live_cut16": "experiments/20260915e_cut16_rolling.json",
            "ids": ROLLING_IDS,
            "ids_not_identical_to_0915d": True,
            "n": 12,
            "wtl": [5, 0, 7],
            "mean_margin": -1129.4,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": 109329693,
            "margin": -325.0,
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "9c5s3g",
            "herd_opp": "6c6s6g",
            "sheep_steps_us": [2, 196, 266],
        },
        "top_board": {
            "source": "experiments/20260915e_top10_games.json",
            "not_copied_from": PRIOR_TOP,
            "Majkel1337": {
                "land": [[150, 220, 222], [150, 220], [150, 220, 222], [126, 150, 220]],
                "herd": ["7c9s0g", "9c3s4g", "14c4s0g", "7c3s4g"],
                "wheat": [530, 404, 511, 433],
                "shops": ["BRUNCH_SPOT", "FARMERS_MARKET", "SMOOTHIE_SHOP", "BRUNCH_SPOT"],
                "clone": "1_of_4",
                "episodes": [109338323, 109329975, 109329773, 109322480],
                "note": (
                    "CSV #1 3155.3 live 3155.3 scoring sub 56216119 (current sub same). "
                    "Ids disjoint from 20260915d Artem set. Mid-land 150 then 220-222 on 3/4 "
                    "(one game 126 then 150/220), wheat 404-530, clone=1 on 1/4, goose mix 0g/4g/0g/4g. "
                    "Opening land 150/126 is not a later-block license."
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
            "score": 1569.5,
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
                "Already live COMPLETE 1569.5 (CSV and submissions 1569.5, was 1573.9). This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                "Extra sheep 226/241/265 not 227/242/266. Rolling 109297997 extra-goose vs extra-cow -26009; "
                "109178619 extra-animal 8c6s3g -13645; 109149160 extra-sheep 4c15s vs 6c10s -12590. "
                "New-window Corgi 109329693 extra-goose 227/242 already bought -325. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 0 new slugs vs 0915d, "
                "not licensed (public-search newest still ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race "
                "already rejected SHA 797d9bca; did not re-pull). no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. "
                "Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1569.5 and keeps 1282.2."
            ),
        },
        "hunt": [],
    }
    dump("20260915e_study_packet.json", packet)

    gate = {
        "date": "2026-09-15",
        "packet": TAG,
        "freeze": False,
        "hold": True,
        "candidate": None,
        "clone_g5_run": False,
        "extracted_later_block_agent": False,
        "cells_executed": False,
        "rejected": [
            {
                "kernel": "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race",
                "verdict": "reject_already_in_0915d_v43_shop0909_plus_same_turn_sale_race_overlay",
                "note": "Already rejected in 20260915d SHA 797d9bca. Public-search newest unchanged. Did not re-pull.",
            },
            {
                "kernel": "alperen5252525/turn-one-market-advantage-kaggriculture",
                "verdict": "reject_v43_c9_opening_shop0909_overlay_reprint",
                "note": "Already rejected in 20260915c SHA 7a37397f. Did not re-pull.",
            },
            {
                "kernel": "alperen5252525/public-state-market-control-kaggriculture",
                "verdict": "reject_v58_day6_shop_prefix_plus_clone_latch_360",
                "note": "Already rejected in 20260915c SHA b041058e. Did not re-pull.",
            },
            {
                "kernel": "alperen5252525/market-momentum-farming-kaggriculture",
                "verdict": "reject_frozen_shop_prefix_tape_portfolio_no_later_block",
                "note": "Already rejected in 20260915c SHA 5fd73afd. Did not re-pull.",
            },
            {
                "kernel": "alperen5252525/market-smart-recovery-kaggriculture",
                "verdict": "reject_v43_reprint_shop0909_overlay",
                "note": "Already rejected in 20260915c SHA 919fc1d6. Did not re-pull.",
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
                "score_complete": 1569.5,
                "sha256": "26ffba52",
            },
            "shopbag": {"submissionId": 56151155, "score_complete": 1282.2, "newer_than_cut16": True},
        },
        "upload_bail": True,
        "hunt_dir": "artifacts/public_sources/_hunt_20260915e",
        "hunt_report": "experiments/20260915e_hunt_report.json",
        "named_kernels_scanned": [],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
    }
    dump("20260915e_gate.json", gate)

    episode = {
        "date": "2026-09-15",
        "packet": TAG,
        "utc": "2026-09-15T16:00:41Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1569.5,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": (
            "COMPLETE 1569.5 CSV / ListEpisodes 1569.56 (submissions 1569.5, was 1573.9). Newest public 109329693. "
            "Newest-2 = shopbag reupload 56151155 (newer id, submissions 1282.2 / ListEpisodes last_updated 1282.250) "
            "+ cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1282.2 < 1500 and is newer than cut 16, "
            "so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
        ),
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": 1282.2,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": 2319,
        "heralces_score": 1569.5,
        "n_teams_csv": 9139,
        "public_56151152": {
            "n_public": 306,
            "n_validation": 1,
            "n_completed_public": 306,
            "wtl": [125, 2, 179],
            "mean_margin": -2116.4,
            "status": "COMPLETE",
            "publicScore": 1569.5,
        },
        "rolling_ids": ROLLING_IDS,
        "rolling_forbidden_0915d": PREV_IDS,
        "ids_not_identical_to_0915d": True,
        "ids_disjoint_from_0915d": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": [5, 0, 7],
        "mean_margin": -1129.4,
        "all_720_done_done": True,
    }
    dump("20260915e_episode_report.json", episode)

    hunt = {
        "date": "2026-09-15",
        "packet": TAG,
        "kernels_not_in_0915d_packet": False,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260915e",
        "inspect_scripts": [
            "experiments/candidates/scan_hunt_20260915e.py",
            "experiments/candidates/inspect_hunt_20260915e.py",
            "experiments/candidates/_extract_hunt_payloads_20260915e.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "writefile_static_hash_only",
        "compare_0915d": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260915d",
            "hunt_report": "experiments/20260915d_hunt_report.json",
            "gate": "experiments/20260915d_gate.json",
            "note": (
                "0 new slugs vs _hunt_20260915d. Public search newest is still "
                "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race "
                "(lastRunTime 2026-09-15 14:58:50.740000). Did not re-pull rejected kernels "
                "(Ahmed V44 SHA 797d9bca, alperen pipe-4 reprint SHA 7a37397f, public-state v58 SHA b041058e, "
                "momentum SHA 5fd73afd, market-smart V43 reprint SHA 919fc1d6)."
            ),
        },
        "public_search_newest": "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race",
        "public_search_newest_lastRunTime": "2026-09-15 14:58:50.740000",
        "live_cuts_not_matched": {
            "cut14": {"name": "y3uanm_router_v5", "sha256_prefix": "acf7c664", "reselect": [226, 360, 433]},
            "cut15": {"name": "thomastschinkel_psr_938", "sha256_prefix": "b87a27ed", "reselect": [144, 288, 432, 576]},
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
        "kernels": [],
    }
    dump("20260915e_hunt_report.json", hunt)

    prev_algo = json.loads((ROOT / f"experiments/{PREV}_algo_note.json").read_text(encoding="utf-8"))
    prev_algo["packet"] = TAG
    prev_algo["live"]["cut16"]["csv_0915e_team_score"] = 1569.5
    prev_algo["live"]["cut16"]["csv_0915d_team_score"] = 1573.9
    prev_algo["live"]["cut16"]["status"] = "COMPLETE"
    prev_algo["live"]["shopbag"]["score_complete"] = 1282.2
    prev_algo["live"]["rank_csv_0915e"] = 2319
    prev_algo["live"]["rank_csv_0915d"] = 2300
    prev_algo["cut16_live_failure_class"]["0915e"] = {
        "file": "experiments/20260915e_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [5, 0, 7],
        "mean_margin": -1129.4,
        "class": "extra-animal 8c6s3g plus extra-goose vs extra-cow plus extra-sheep plus extra-goose",
    }
    dump("20260915e_algo_note.json", prev_algo)

    loss = {
        "date": "2026-09-15",
        "packet": TAG,
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": ROLLING_IDS,
        "ids_0915d": PREV_IDS,
        "disjoint_from_0915d": True,
        "all_720_done_done": True,
        "wtl": [5, 0, 7],
        "mean_margin": -1129.4,
        "clone_n": 11,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [1.0, 29.0],
        "wool_360": {
            "109329693": 11,
            "109297997": 1,
            "109184094": 243,
            "109178619": 1,
            "109169017": 236,
            "109168637": 43,
            "109159847": 1,
            "109152510": 236,
            "109149160": 231,
            "109142116": 224,
            "109135062": 43,
            "109111080": 226,
        },
        "wool_432": {
            "109329693": 1,
            "109297997": 1,
            "109184094": 244,
            "109178619": 5,
            "109169017": 212,
            "109168637": 1,
            "109159847": 5,
            "109152510": 238,
            "109149160": 158,
            "109142116": 189,
            "109135062": 1,
            "109111080": 197,
        },
        "same_class_as_0913c": True,
        "same_class_note": (
            "Same extra-animal family as 09-13c/09-14/09-15d: extra-animal 8c6s3g plus extra-goose plus extra-sheep. "
            "WTL 5-0-7 mean -1129.4 vs 09-15d 4-0-8 mean -4182.2. New window game Corgi 109329693 -325. clone=11/12."
        ),
        "loss_class": LOSS_CLASS,
        "worst_losses": [
            {"id": 109297997, "opp": "Gaddam Shiva Teja", "margin": -26009.0},
            {"id": 109178619, "opp": "Huy Lê Ngọc Gia", "margin": -13645.0},
            {"id": 109149160, "opp": "Dhruv #2", "margin": -12590.0},
            {"id": 109169017, "opp": "Grim Reaper", "margin": -10132.0},
        ],
        "not_227_242_266_license": True,
        "not_opening_broke": True,
        "not_freeze_after_day9_9c9s": True,
    }
    dump("20260915e_cut16_loss_class.json", loss)


if __name__ == "__main__":
    main()
