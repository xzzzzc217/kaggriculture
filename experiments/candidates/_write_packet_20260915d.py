"""Write 20260915d study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "20260915d"
PREV = "20260915c"

ROLLING_IDS = [
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
PREV_IDS = [
    109297997,
    109159847,
    109152510,
    109149160,
    109142116,
    109135062,
    109111080,
    109091091,
    109078755,
    109057555,
    109054323,
    109044160,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (yu9824 109316981 7c6s vs 8c6s3g FARMERS extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -1349; "
    "ManasviSharma 109251218 7c6s vs 8c6s3g FARMERS extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -18715; "
    "Ashraf 1232 109227483 9c5s vs 8c6s3g ICE_CREAM extra sheep 314 vs opp extra sheep 218/227 extra geese 242/266 -13342) "
    "+ extra-sheep (Fedor 109323301 10c8s vs 7c12s5g SMOOTHIE extra sheep 227/242/266 already bought vs extra geese 258+ -10162; "
    "Xiaowenhao404 109321947 6c11s vs 6c13s2g YARN extra sheep 218/242/266 already bought vs extra sheep 227/242/266/290 -14705; "
    "Sergei Fironov 109247247 10c8s vs 8c12s3g SMOOTHIE extra sheep 227/242/266 already bought vs extra sheep 218/227/290 -13194; "
    "Rifa Tamanna 109208871 9c8s vs 7c11s BAKERY extra sheep 227/242/266 already bought vs extra sheep 218-266 -3251) "
    "+ extra-goose (AimeeChen1 109205359 9c5s3g vs 9c5s4g PET_CAFE extra geese 227/242 already bought vs 4g -2466). "
    "Wins: Corgi-Samoyed 109309340 9c5s3g vs 9c6s3g FARMERS +1847 extra geese 227/242 already bought; "
    "Baha Enes Ören 109274859 9c5s3g vs 9c5s3g ICE_CREAM +114 extra geese 227/242 already bought; "
    "tetsuya 109241224 9c5s3g vs 6c5s BAKERY +18920 extra geese 227/242 clone=0; "
    "Jorrawar Grewal 109205772 9c5s3g vs 6c11s PIZZA +6116 extra geese 227/242 already bought. "
    "clone=11/12, Q=3/3 (opp Q=4 on Manasvi/Sergei), BUY_LAND 151/266 succeeded, cash_24 3-25. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Baha already bought extra geese 227/242 and won +114; "
    "Aimee already bought extra geese 227/242 and lost vs 4g; "
    "Fedor/Sergei/Rifa/Xiaowenhao already bought extra sheep 218-266 and lost; "
    "yu9824/Manasvi extra cow 218 lost vs 8c6s3g; Ashraf extra sheep 314 lost vs 8c6s3g."
)
V44_NOTE = (
    "New slug vs _hunt_20260915c (lastRunTime 2026-09-15 14:58:50.740000; public-search newest by dateCreated). "
    "SOURCE_BYTES static reconstruct SHA 797d9bca... Distinct from already-rejected Ahmed V43 SHA 919fc1d6, "
    "V42 728fdfb4, V41 8951ff93, and live cuts 14/15/16. Notebook embeds cut15 SHA b87a27ed and yhay81 "
    "shop-router-0913 SHA 77cf6772 as comments/payloads; payload itself is 797d9bca. "
    "V44 keeps complete V43 Shop0909 policy and adds a same-turn sale-race overlay "
    "(_RACE_HORIZON_CLONE=8 / _RACE_HORIZON_ESCALATED=24 wrapping _R37_HORIZONS). "
    "Day-6 144/648 plus _R37_HORIZONS=4 from 288 plus step==712 terminal planner. "
    "216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. "
    "No ROUTE_STEP/PROGRAM/sale_horizon/ADVANCE_START identifiers. No ctypes/agent.so. "
    "Cells not executed. Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1573.9 (submissions 1578.6) would drop without a "
    ">=1500 COMPLETE newest-2 partner (shopbag 56151155 COMPLETE 1282.2 < 1500 and newer than cut 16; "
    "a new cut alone keeps shopbag and drops 1573.9; re-upload is 600-provisional not a partner). "
    "No licensed later-block. Hunt 1 new slug vs _hunt_20260915c (public search newest "
    "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race lastRunTime 2026-09-15 14:58:50.740000 "
    "V43 Shop0909 plus same-turn sale-race overlay SHA 797d9bca; not farm-route reselect after 216). "
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
]


def dump(name: str, payload: dict) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    hunt_row = {
        "kernel": "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race",
        "path": "artifacts/public_sources/_hunt_20260915d/ahmedberatozer__kaggriculture-v44-winning-the-same-turn-sale-race/kaggriculture-v44-winning-the-same-turn-sale-race.ipynb",
        "verdict": "reject_v43_shop0909_plus_same_turn_sale_race_overlay",
        "sha256": "797d9bca309d481e18cdbb675ce6d6de9967d266cbafb4c2352c68fb10264e2f",
        "note": V44_NOTE,
    }
    packet = {
        "title": "Kaggriculture study packet 2026-09-15d",
        "not_the_0915c_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260915d/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260915d/kaggriculture-publicleaderboard-2026-09-15T15-01-30.csv",
            "leaderboard_api": "experiments/20260915d_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260915d",
            "top_replays": "artifacts/kaggle_runs/top_20260915d",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915d",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260915d_gate.json",
            "episode_report": "experiments/20260915d_episode_report.json",
            "hunt_report": "experiments/20260915d_hunt_report.json",
            "algo_note": "experiments/20260915d_algo_note.json",
            "loss_class": "experiments/20260915d_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1573.9,
            "rank": 2300,
            "n_teams": 9136,
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
            "cut16_score": 1573.9,
            "cut16_submissions_api_score": 1578.6,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2944.2,
            "rank10": {"team": "Mengfei Li", "score": 2986.9},
            "rank1": {
                "team": "Artem The Farmer \U0001f345",
                "score": 3149.3,
                "submissionId": 56232364,
            },
            "public_cut16": {"n": 305, "wtl": [125, 2, 178], "mean_margin": -2122.2},
        },
        "rolling": {
            "previous": "experiments/20260915c_cut16_rolling.json",
            "live_cut16": "experiments/20260915d_cut16_rolling.json",
            "ids": ROLLING_IDS,
            "ids_not_identical_to_0915c": True,
            "n": 12,
            "wtl": [4, 0, 8],
            "mean_margin": -4182.2,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": 109323301,
            "margin": -10162.0,
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "10c8s",
            "herd_opp": "7c12s5g",
            "sheep_steps_us": [2, 196, 227, 242, 266],
        },
        "top_board": {
            "source": "experiments/20260915d_top10_games.json",
            "not_copied_from": PRIOR_TOP,
            "Artem The Farmer \U0001f345": {
                "land": [[151, 198], [151, 198], [151, 198], [151, 198]],
                "herd": ["10c2s2g", "12c10s2g", "10c2s2g", "9c2s2g"],
                "wheat": [481, 302, 541, 380],
                "shops": ["ICE_CREAM_SHOP", "PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"],
                "clone": "1_of_4",
                "episodes": [109322609, 109322470, 109315236, 109308841],
                "note": (
                    "CSV #1 3149.3 live 3149.3 scoring sub 56232364 (current sub 56234362 is 3038.9). "
                    "Ids disjoint from 20260915c Majkel set. Mid-land 151 then 198 on 4/4, wheat 302-541, "
                    "clone=1 on 1/4, goose mix 2g/2g/2g/2g. Opening land 151 then 198 is not a later-block license."
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
            "score": 1573.9,
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
                "Already live COMPLETE 1573.9 (submissions 1578.6, was 1582.4). This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                "Extra sheep 226/241/265 not 227/242/266. Rolling 109251218 extra-animal 8c6s3g -18715; "
                "109321947 extra-sheep 6c11s vs 6c13s2g -14705; 109227483 extra-animal 8c6s3g -13342. "
                "New-window Fedor 109323301 extra-sheep 227/242/266 already bought -10162. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 1 new slug vs 0915c, "
                "not licensed (public-search newest ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race "
                "V43 Shop0909 plus same-turn sale-race overlay SHA 797d9bca). no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. "
                "Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1573.9 and keeps 1282.2."
            ),
        },
        "hunt": [hunt_row],
    }
    dump("20260915d_study_packet.json", packet)

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
            hunt_row,
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
                "score_complete": 1573.9,
                "sha256": "26ffba52",
            },
            "shopbag": {"submissionId": 56151155, "score_complete": 1282.2, "newer_than_cut16": True},
        },
        "upload_bail": True,
        "hunt_dir": "artifacts/public_sources/_hunt_20260915d",
        "hunt_report": "experiments/20260915d_hunt_report.json",
        "named_kernels_scanned": [
            "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race",
        ],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
    }
    dump("20260915d_gate.json", gate)

    episode = {
        "date": "2026-09-15",
        "packet": TAG,
        "utc": "2026-09-15T15:01:30Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1573.9,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": (
            "COMPLETE 1573.9 CSV / ListEpisodes 1573.96 (submissions 1578.6, was 1582.4). Newest public 109323301. "
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
        "heralces_rank_csv": 2300,
        "heralces_score": 1573.9,
        "n_teams_csv": 9136,
        "public_56151152": {
            "n_public": 305,
            "n_validation": 1,
            "n_completed_public": 305,
            "wtl": [125, 2, 178],
            "mean_margin": -2122.2,
            "status": "COMPLETE",
            "publicScore": 1573.9,
        },
        "rolling_ids": ROLLING_IDS,
        "rolling_forbidden_0915c": PREV_IDS,
        "ids_not_identical_to_0915c": True,
        "ids_disjoint_from_0915c": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": [4, 0, 8],
        "mean_margin": -4182.2,
        "all_720_done_done": True,
    }
    dump("20260915d_episode_report.json", episode)

    hunt = {
        "date": "2026-09-15",
        "packet": TAG,
        "kernels_not_in_0915c_packet": True,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260915d",
        "inspect_scripts": [
            "experiments/candidates/scan_hunt_20260915d.py",
            "experiments/candidates/inspect_hunt_20260915d.py",
            "experiments/candidates/_extract_hunt_payloads_20260915d.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "writefile_static_hash_only",
        "compare_0915c": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260915c",
            "hunt_report": "experiments/20260915c_hunt_report.json",
            "gate": "experiments/20260915c_gate.json",
            "note": (
                "1 new slug vs _hunt_20260915c. Public search newest is now "
                "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race "
                "(lastRunTime 2026-09-15 14:58:50.740000). Did not re-pull rejected kernels "
                "(alperen pipe-4 reprint SHA 7a37397f, public-state v58 SHA b041058e, momentum SHA 5fd73afd, "
                "market-smart V43 reprint SHA 919fc1d6, anandkumar369o analysis SHA 595d29fe, nathanjacob pipe-4 SHA 7a37397f, "
                "kenanzhang9 SHA 602ae8be)."
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
        "named_kernels_scanned": [
            "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race",
        ],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "kernels": [hunt_row],
    }
    dump("20260915d_hunt_report.json", hunt)

    prev_algo = json.loads((ROOT / f"experiments/{PREV}_algo_note.json").read_text(encoding="utf-8"))
    prev_algo["packet"] = TAG
    prev_algo["live"]["cut16"]["csv_0915d_team_score"] = 1573.9
    prev_algo["live"]["cut16"]["csv_0915c_team_score"] = 1582.4
    prev_algo["live"]["cut16"]["status"] = "COMPLETE"
    prev_algo["live"]["shopbag"]["score_complete"] = 1282.2
    prev_algo["live"]["rank_csv_0915d"] = 2300
    prev_algo["live"]["rank_csv_0915c"] = 2291
    prev_algo["cut16_live_failure_class"]["0915d"] = {
        "file": "experiments/20260915d_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [4, 0, 8],
        "mean_margin": -4182.2,
        "class": "extra-animal 8c6s3g plus extra-sheep plus extra-goose",
    }
    dump("20260915d_algo_note.json", prev_algo)

    loss = {
        "date": "2026-09-15",
        "packet": TAG,
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": ROLLING_IDS,
        "ids_0915c": PREV_IDS,
        "disjoint_from_0915c": True,
        "all_720_done_done": True,
        "wtl": [4, 0, 8],
        "mean_margin": -4182.2,
        "clone_n": 11,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [3.0, 25.0],
        "wool_360": {
            "109323301": 223,
            "109321947": 240,
            "109316981": 1,
            "109309340": 77,
            "109274859": 183,
            "109251218": 1,
            "109247247": 234,
            "109241224": 43,
            "109227483": 1,
            "109208871": 234,
            "109205772": 18,
            "109205359": 43,
        },
        "wool_432": {
            "109323301": 190,
            "109321947": 239,
            "109316981": 5,
            "109309340": 1,
            "109274859": 189,
            "109251218": 5,
            "109247247": 237,
            "109241224": 1,
            "109227483": 1,
            "109208871": 200,
            "109205772": 1,
            "109205359": 1,
        },
        "same_class_as_0913c": True,
        "same_class_note": (
            "Same extra-animal family as 09-13c/09-14/09-15c: extra-animal 8c6s3g plus extra-goose plus extra-sheep. "
            "WTL 4-0-8 mean -4182.2 vs 09-15c 5-0-7 mean -3963.6. New window game Fedor 109323301 -10162. clone=11/12."
        ),
        "loss_class": LOSS_CLASS,
        "worst_losses": [
            {"id": 109251218, "opp": "ManasviSharma", "margin": -18715.0},
            {"id": 109321947, "opp": "Xiaowenhao404", "margin": -14705.0},
            {"id": 109227483, "opp": "Ashraf 1232", "margin": -13342.0},
            {"id": 109247247, "opp": "Sergei Fironov", "margin": -13194.0},
        ],
        "not_227_242_266_license": True,
        "not_opening_broke": True,
        "not_freeze_after_day9_9c9s": True,
    }
    dump("20260915d_cut16_loss_class.json", loss)


if __name__ == "__main__":
    main()
