"""Write 20260913t study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
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
    108412731,
    108383915,
]
PREV_13S = [
    108568560,
    108559476,
    108534412,
    108504670,
    108472548,
    108461768,
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
    108374873,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (AQiDA19 108550653 7c6s vs 8c6s3g clone=1 BAKERY extra sheep 218/227 extra geese 242/266 wheat 509 vs 17314 -21800; "
    "Hanaro 108545775 9c5s vs 8c6s3g PIZZA extra sheep 218/227 extra geese 242/266 -14377; "
    "Wei Han 108445221 9c5s vs 8c6s3g ICE_CREAM extra sheep 218/227 extra geese 242/266 -12688; "
    "Excluding 108520439 7c6s vs 8c6s3g FARMERS_MARKET extra sheep 218/227 extra geese 242/266 -5345) "
    "+ extra-goose (haonan zhengh 108412731 9c5s vs 9c5s3g extra cow 218 extra sheep 227 extra geese 242/266 -18535) "
    "+ extra-animal YARN 6c11s (Peter Cnudde 108383915 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought -13315) "
    "+ extra-sheep 15s (Hackoholics 108509931 4c15s vs 6c10s extra sheep 218/242/266 already bought -4788) "
    "+ identical-clone extra-goose (mmwstudy 108484081 9c5s3g vs 9c5s3g extra geese 227/242 already bought -65). "
    "Wins: XiaoYan12 108441448 9c5s3g vs 6c6s6g +6450 extra geese 227/242 already bought; "
    "Agentmaster 108489181 9c5s3g vs 9c5s4g +2699 extra geese 227/242 already bought; "
    "wzyxp_123 108441305 9c5s3g vs 9c5s3g +2649 extra geese 227/242 already bought; "
    "maxout 108586169 9c5s3g vs 9c5s3g identical-clone extra geese 227/242 already bought +8. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: AQiDA19/Hanaro/Wei Han/Excluding lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
    "haonan extra cow 218 extra sheep 227 extra geese 242/266 and we lost; "
    "Peter/Hackoholics already bought 218/242/266 and lost; "
    "mmwstudy already bought extra geese 227/242 and lost identical-clone -65; "
    "XiaoYan12/Agentmaster/wzyxp_123 already bought extra geese 227/242 and won; "
    "maxout already bought extra geese 227/242 and won identical-clone +8."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1673.8 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1314.5 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1673.8; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Public search newest still "
    "renjistarfall/kaggriculture-best-agent SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay "
    "(already rejected 0913s). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(name: str, obj: dict) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    hunt = {
        "date": "2026-09-13",
        "packet": "20260913t",
        "kernels_not_in_0913s_packet": False,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260913t",
        "inspect_scripts": [
            "experiments/candidates/scan_hunt_20260913t.py",
        ],
        "python": "D:\\kaggle\\kaggriculture\\.venv\\Scripts\\python.exe",
        "payload_decode": "none_no_new_notebook",
        "compare_0913s": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260913s",
            "hunt_report": "experiments/20260913s_hunt_report.json",
            "gate": "experiments/20260913s_gate.json",
            "note": "No new slug vs _hunt_20260913s. Public search newest is still renjistarfall/kaggriculture-best-agent (lastRunTime 2026-09-13 14:11:05.950000). Did not re-pull rejected kernels (renjistarfall V39 reprint, alperen metacounter, xuantianfengwu allocator, Ahmed V40, guru V39, yhay81 0913, wei v46d review, Ahmed V39 v39-ready-before-the-rush, aurax7 v4, crystalbaby V38, Ahmed V39 notebookda72f457f5, prvsiyan market-ledger, timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple).",
        },
        "public_search_newest": "renjistarfall/kaggriculture-best-agent",
        "public_search_newest_lastRunTime": "2026-09-13 14:11:05.950000",
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
        "author_list_note": "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6.",
        "hunt": [],
    }
    dump("20260913t_hunt_report.json", hunt)

    gate = json.loads((ROOT / "experiments/20260913s_gate.json").read_text(encoding="utf-8"))
    gate["packet"] = "20260913t"
    gate["rejected"] = [
        {
            "kernel": "renjistarfall/kaggriculture-best-agent",
            "verdict": "reject_v39_reprint_shop0909_overlay",
            "note": "Still the public-search newest (lastRunTime 2026-09-13 14:11:05.950000). 0913s already rejected SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
        },
    ] + [
        row
        for row in gate["rejected"]
        if row.get("kernel") != "renjistarfall/kaggriculture-best-agent"
    ]
    gate["live"]["cut16"]["score_complete"] = 1673.8
    gate["live"]["shopbag"]["score_complete"] = 1314.5
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260913t"
    gate["hunt_report"] = "experiments/20260913t_hunt_report.json"
    gate["named_kernels_scanned"] = []
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1673.8 partnered with newer shopbag 56151155 COMPLETE 1314.5 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "No new public later-block vs _hunt_20260913s. Public search newest still renjistarfall/kaggriculture-best-agent SHA 708c7485 (V39 reprint Shop0909 144/648 + 288/712 overlay). "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
        "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: AQiDA19 extra sheep 218/227 extra geese 242/266 -21800; "
        "Hanaro/Wei Han/Excluding lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
        "haonan extra cow 218 extra sheep 227 extra geese 242/266 -18535; "
        "Peter/Hackoholics already bought 218/242/266 and lost; "
        "mmwstudy already bought extra geese 227/242 and lost identical-clone -65; "
        "maxout already bought extra geese 227/242 and won identical-clone +8."
    )
    dump("20260913t_gate.json", gate)

    algo = json.loads((ROOT / "experiments/20260913s_algo_note.json").read_text(encoding="utf-8"))
    algo["packet"] = "20260913t"
    algo["live"]["cut16"]["csv_0913t_team_score"] = 1673.8
    algo["live"]["shopbag"]["score_complete"] = 1314.5
    algo["live"]["rank_csv_0913t"] = 2027
    algo["cut16_live_failure_class"]["0913t"] = {
        "file": "experiments/20260913t_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [4, 0, 8],
        "mean_margin": -6592.2,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-animal YARN 6c11s plus extra-sheep 15s plus identical-clone extra-goose",
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
                "id": 108412731,
                "opp": "haonan zhengh",
                "margin": -18535,
                "shops72": ["ICE_CREAM_SHOP"],
                "buy": "9c5s vs 9c5s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. Public search newest still renjistarfall/kaggriculture-best-agent writefile SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay (already rejected 0913s). Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block).",
    }
    dump("20260913t_algo_note.json", algo)

    episode = {
        "date": "2026-09-13",
        "packet": "20260913t",
        "utc": "2026-09-13T15:37:20Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1673.8,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": "COMPLETE 1673.8 (was 1670.2). Newest public 108586169 updatedScore 1673.807. Newest-2 = shopbag reupload 56151155 (newer id, submissions 1314.5 / ListEpisodes last_updated 1314.519) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1314.5 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold.",
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": 1314.5,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": 2027,
        "heralces_score": 1673.8,
        "n_teams_csv": 8902,
        "public_56151152": {
            "n_public": 231,
            "n_validation": 1,
            "n_completed_public": 231,
            "wtl": [101, 2, 128],
            "mean_margin": -1220.7,
            "status": "COMPLETE",
            "publicScore": 1673.8,
        },
        "rolling_ids": ROLLING_IDS,
        "rolling_forbidden_0913s": PREV_13S,
        "ids_not_identical_to_0913s": True,
        "ids_disjoint_from_0913s": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": [4, 0, 8],
        "mean_margin": -6592.2,
        "rolling_note": "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913s packet. 4W 8L. Worst AQiDA19 108550653 L -21800 7c6s vs 8c6s3g clone=1 extra sheep 218/227 extra geese 242/266. New-window maxout 108586169 W +8 9c5s3g vs 9c5s3g identical-clone extra geese 227/242 already bought. Not opening-broke. Not freeze 9c9s.",
    }
    dump("20260913t_episode_report.json", episode)

    loss = {
        "date": "2026-09-13",
        "packet": "20260913t",
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": ROLLING_IDS,
        "ids_0913s": PREV_13S,
        "disjoint_from_0913s": True,
        "all_720_done_done": True,
        "wtl": [4, 0, 8],
        "mean_margin": -6592.2,
        "clone_n": 12,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [3.0, 27.0],
        "wool_360": {
            "108586169": 37,
            "108550653": 1,
            "108545775": 1,
            "108520439": 1,
            "108509931": 231,
            "108489181": 43,
            "108484081": 37,
            "108445221": 1,
            "108441448": 11,
            "108441305": 37,
            "108412731": 1,
            "108383915": 237,
        },
        "wool_432": {
            "108586169": 1,
            "108550653": 5,
            "108545775": 24,
            "108520439": 5,
            "108509931": 158,
            "108489181": 1,
            "108484081": 125,
            "108445221": 1,
            "108441448": 1,
            "108441305": 1,
            "108412731": 1,
            "108383915": 227,
        },
        "same_class_as_0913c": True,
        "same_class_note": "Same extra-animal family as 09-13c/09-13s: extra-animal 8c6s3g plus extra-goose plus extra-animal YARN 6c11s plus extra-sheep 15s plus identical-clone extra-goose. WTL 4-0-8 mean -6592.2 vs 09-13s 4-0-8 mean -1150.5. New window game is maxout 108586169 identical-clone extra-goose +8. clone=12/12.",
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
    }
    dump("20260913t_cut16_loss_class.json", loss)

    packet = {
        "title": "Kaggriculture study packet 2026-09-13t",
        "not_the_0913s_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913t/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913t/kaggriculture-publicleaderboard-2026-09-13T15-37-20.csv",
            "leaderboard_api": "experiments/20260913t_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913t",
            "top_replays": "artifacts/kaggle_runs/top_20260913t",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913t",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913t_gate.json",
            "episode_report": "experiments/20260913t_episode_report.json",
            "hunt_report": "experiments/20260913t_hunt_report.json",
            "algo_note": "experiments/20260913t_algo_note.json",
            "loss_class": "experiments/20260913t_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1673.8,
            "rank": 2027,
            "n_teams": 8902,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1314.5,
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
            "cut16_score": 1673.8,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2908.8,
            "rank10": {"team": "Catalyst", "score": 2958.0},
            "rank1": {"team": "Majkel1337", "score": 3252.7, "submissionId": 56156662},
            "public_cut16": {"n": 231, "wtl": [101, 2, 128], "mean_margin": -1220.7},
        },
        "rolling": {
            "previous": "experiments/20260913s_cut16_rolling.json",
            "live_cut16": "experiments/20260913t_cut16_rolling.json",
            "ids": ROLLING_IDS,
            "ids_not_identical_to_0913s": True,
            "n": 12,
            "wtl": [4, 0, 8],
            "mean_margin": -6592.2,
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
            "source": "experiments/20260913t_top10_games.json",
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
            ],
            "Majkel1337": {
                "land": [
                    [150, 220, 222],
                    [150, 220, 222],
                    [150, 218, 220, 222],
                    [150, 218, 220, 222],
                ],
                "herd": ["11c3s2g", "7c9s2g", "13c3s0g", "6c3s4g"],
                "wheat": [590, 488, 543, 425],
                "shops": ["BAKERY", "BAKERY", "ICE_CREAM_SHOP", "FARMERS_MARKET"],
                "clone": "0_of_4",
                "episodes": [108584052, 108577054, 108076337, 108071295],
                "note": "CSV #1 3252.7 live 3252.7 scoring sub 56156662. Ids disjoint from 20260913s Majkel set. Mid-land 150 then 218-222 (two 150/220/222; two 150/218/220/222), wheat 425-590, clone=0 on 4/4, goose mix 2g/2g/0g/4g. Opening land is not a later-block license.",
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
            "score": 1673.8,
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
            "why": "Already live COMPLETE 1673.8. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. Rolling 108550653 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -21800; 108412731 extra cow 218 extra sheep 227 extra geese 242/266 -18535; 108383915 already bought 218/242/266 sheep and lost YARN 6c11s -13315. New-window maxout 108586169 already bought extra geese 227/242 and won identical-clone +8. Not cut 12/13.",
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: no new slug vs 0913s; public search newest still renjistarfall/kaggriculture-best-agent SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay; no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1673.8 and keeps 1314.5.",
        },
        "hunt": hunt["hunt"],
    }
    dump("20260913t_study_packet.json", packet)


if __name__ == "__main__":
    main()
