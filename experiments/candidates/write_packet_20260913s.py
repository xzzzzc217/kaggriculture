"""Write 20260913s study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
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
PREV_13R = [
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
    108377691,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (linyifangzhenshuai 108426937 7c6s vs 8c6s3g clone=1 BRUNCH extra sheep 218/227 extra geese 242/266 wheat 486 vs 17346 -9514; "
    "carlos-tagosaku 108429814 7c6s vs 8c6s3g FARMERS_MARKET extra sheep 218/227 extra geese 242/266 -8454; "
    "Brian Chua 108472548 9c5s vs 8c6s3g SMOOTHIE extra sheep 218/227 extra geese 242/266 -659) "
    "+ extra-goose (alcanta 108568560 9c5s vs 9c5s3g extra cow 218 extra sheep 227 extra geese 242/266 wheat 426 vs 17337 -19224; "
    "Sophie555 108374873 9c5s3g vs 6c6s6g extra geese 227/242 already bought -3339) "
    "+ extra-animal YARN 6c11s (wuwuwu 108432563 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought -10575; "
    "Farmer Shuang 108559476 6c11s vs 7c11s extra sheep 218/242/266 already bought -418) "
    "+ identical-clone extra-goose (maverick_ss_26 108504670 9c5s3g vs 9c5s3g extra geese 227/242 already bought -1920). "
    "Wins: Joyal 108422886 6c11s vs 9c5s3g +27397 extra sheep 218/242/266 already bought; "
    "zg l1218 108534412 6c12s vs 8c6s3g +8548 extra sheep 218/242/266 already bought; "
    "Sidharth Hulyalkar 108399266 9c5s3g vs 9c5s4g +2525 extra geese 227/242 already bought; "
    "Andrey Shpigar 108461768 9c8s vs 6c6s6g +1827 extra sheep 227/242/266. "
    "clone=12/12, Q=3/3 (Joyal opp Q=4), BUY_LAND 151/266 succeeded, cash_24 3-24 not 0. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: alcanta extra cow 218 extra sheep 227 extra geese 242/266 and we lost; "
    "linyi/carlos/Brian lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
    "wuwuwu/Farmer Shuang already bought 218/242/266 and lost YARN 6c11s; "
    "maverick already bought extra geese 227/242 and lost identical-clone -1920; "
    "Sophie555 already bought extra geese 227/242 and lost vs 6c6s6g; "
    "Joyal/zg l1218 already bought 218/242/266 and won; Sidharth already bought extra geese 227/242 and won."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1670.2 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1319.5 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1670.2; "
    "re-upload is 600-provisional not a partner). No licensed later-block. New slug "
    "renjistarfall/kaggriculture-best-agent SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay "
    "(same writefile as guruprasaathas111 V39). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(name: str, obj: dict) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    hunt = {
        "date": "2026-09-13",
        "packet": "20260913s",
        "kernels_not_in_0913r_packet": True,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260913s",
        "inspect_scripts": [
            "experiments/candidates/inspect_hunt_20260913s.py",
            "experiments/candidates/scan_hunt_20260913s.py",
        ],
        "python": "D:\\kaggle\\kaggriculture\\.venv\\Scripts\\python.exe",
        "payload_decode": "renjistarfall_writefile_dumped_for_sha_only",
        "compare_0913r": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260913r",
            "hunt_report": "experiments/20260913r_hunt_report.json",
            "gate": "experiments/20260913r_gate.json",
            "note": "New slug renjistarfall/kaggriculture-best-agent vs alperen5252525/kaggriculture-metacounter-r1 and xuantianfengwu/kaggriculture-land-labor-capital-allocator in _hunt_20260913r. Did not re-pull rejected kernels (alperen metacounter, xuantianfengwu allocator, Ahmed V40, guru V39, yhay81 0913, wei v46d review, Ahmed V39 v39-ready-before-the-rush, aurax7 v4, crystalbaby V38, Ahmed V39 notebookda72f457f5, prvsiyan market-ledger, timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple).",
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
        "named_kernels_scanned": ["renjistarfall/kaggriculture-best-agent"],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "author_list_note": "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6.",
        "hunt": [
            {
                "kernel": "renjistarfall/kaggriculture-best-agent",
                "path": "artifacts/public_sources/_hunt_20260913s/renjistarfall__kaggriculture-best-agent/kaggriculture-best-agent.ipynb",
                "verdict": "reject_v39_reprint_shop0909_overlay",
                "sha256": "708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8",
                "note": "New slug vs _hunt_20260913r (lastRunTime 2026-09-13 14:11:05.950000; public-search newest by dateCreated). Title Kaggriculture Master Engine V5. Python %%writefile main.py SHA 708c7485... identical to already-rejected guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f V39 reprint. Distinct from cut14 acf7c664, cut15 b87a27ed, cut16 26ffba52. Shop0909 day-6 144/648 plus 288/696 sales overlay plus step==712 terminal planner. 216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5.",
            }
        ],
    }
    dump("20260913s_hunt_report.json", hunt)

    gate = json.loads((ROOT / "experiments/20260913r_gate.json").read_text(encoding="utf-8"))
    gate["packet"] = "20260913s"
    gate["rejected"] = [
        {
            "kernel": "renjistarfall/kaggriculture-best-agent",
            "path": "artifacts/public_sources/_hunt_20260913s/renjistarfall__kaggriculture-best-agent/kaggriculture-best-agent.ipynb",
            "verdict": "reject_v39_reprint_shop0909_overlay",
            "sha256": "708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8",
            "note": "New slug vs _hunt_20260913r (lastRunTime 2026-09-13 14:11:05.950000; public-search newest by dateCreated). Writefile main.py SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay, same as guruprasaathas111 V39. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5.",
        },
        {
            "kernel": "alperen5252525/kaggriculture-metacounter-r1",
            "verdict": "reject_analysis_no_writefile",
            "note": "Still a public search hit. 0913r already rejected analysis no-writefile. Did not re-pull.",
        },
        {
            "kernel": "xuantianfengwu/kaggriculture-land-labor-capital-allocator",
            "verdict": "reject_heuristic_six_cow_allocator",
            "note": "Still a public search hit. 0913r already rejected SHA b49709bd heuristic 6-cow allocator. Did not re-pull.",
        },
    ] + [
        row
        for row in gate["rejected"]
        if row.get("kernel")
        not in {
            "alperen5252525/kaggriculture-metacounter-r1",
            "xuantianfengwu/kaggriculture-land-labor-capital-allocator",
        }
    ]
    gate["live"]["cut16"]["score_complete"] = 1670.2
    gate["live"]["shopbag"]["score_complete"] = 1319.5
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260913s"
    gate["hunt_report"] = "experiments/20260913s_hunt_report.json"
    gate["named_kernels_scanned"] = ["renjistarfall/kaggriculture-best-agent"]
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1670.2 partnered with newer shopbag 56151155 COMPLETE 1319.5 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "New public slug renjistarfall/kaggriculture-best-agent writefile SHA 708c7485 (V39 reprint Shop0909 144/648 + 288/712 overlay) is not later-block. "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
        "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: alcanta extra cow 218 extra sheep 227 extra geese 242/266 -19224; "
        "linyi/carlos/Brian lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
        "wuwuwu/Farmer Shuang already bought 218/242/266 and lost YARN 6c11s; "
        "maverick already bought extra geese 227/242 and lost identical-clone -1920; Sophie555 already bought extra geese 227/242 and lost vs 6c6s6g."
    )
    dump("20260913s_gate.json", gate)

    algo = json.loads((ROOT / "experiments/20260913r_algo_note.json").read_text(encoding="utf-8"))
    algo["packet"] = "20260913s"
    algo["live"]["cut16"]["csv_0913s_team_score"] = 1670.2
    algo["live"]["shopbag"]["score_complete"] = 1319.5
    algo["live"]["rank_csv_0913s"] = 2026
    algo["cut16_live_failure_class"]["0913s"] = {
        "file": "experiments/20260913s_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [4, 0, 8],
        "mean_margin": -1150.5,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-animal YARN 6c11s plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 108568560,
                "opp": "alcanta",
                "margin": -19224,
                "shops72": ["SMOOTHIE_SHOP"],
                "buy": "9c5s vs 9c5s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 108432563,
                "opp": "wuwuwu",
                "margin": -10575,
                "shops72": ["YARN_STORE"],
                "buy": "6c11s vs 7c11s",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 237,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. New public kernel renjistarfall/kaggriculture-best-agent writefile SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay. Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block).",
    }
    dump("20260913s_algo_note.json", algo)

    episode = {
        "date": "2026-09-13",
        "packet": "20260913s",
        "utc": "2026-09-13T14:36:51Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1670.2,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": "COMPLETE 1670.2 (was 1680.9). Newest public 108568560 updatedScore 1670.287. Newest-2 = shopbag reupload 56151155 (newer id, submissions 1319.5 / ListEpisodes last_updated 1319.596) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1319.5 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold.",
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": 1319.5,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": 2026,
        "heralces_score": 1670.2,
        "n_teams_csv": 8896,
        "public_56151152": {
            "n_public": 230,
            "n_validation": 1,
            "n_completed_public": 230,
            "wtl": [100, 2, 128],
            "mean_margin": -1226.1,
            "status": "COMPLETE",
            "publicScore": 1670.2,
        },
        "rolling_ids": ROLLING_IDS,
        "rolling_forbidden_0913r": PREV_13R,
        "ids_not_identical_to_0913r": True,
        "ids_disjoint_from_0913r": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": [4, 0, 8],
        "mean_margin": -1150.5,
        "rolling_note": "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913r packet. 4W 8L. Worst alcanta 108568560 L -19224 9c5s vs 9c5s3g clone=1 extra cow 218 extra sheep 227 extra geese 242/266. New-window Farmer Shuang 108559476 L -418 6c11s vs 7c11s extra sheep 218/242/266 already bought. Not opening-broke. Not freeze 9c9s.",
    }
    dump("20260913s_episode_report.json", episode)

    loss = {
        "date": "2026-09-13",
        "packet": "20260913s",
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": ROLLING_IDS,
        "ids_0913r": PREV_13R,
        "disjoint_from_0913r": True,
        "all_720_done_done": True,
        "wtl": [4, 0, 8],
        "mean_margin": -1150.5,
        "clone_n": 12,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [3.0, 24.0],
        "wool_360": {
            "108568560": 1,
            "108559476": 245,
            "108534412": 236,
            "108504670": 43,
            "108472548": 1,
            "108461768": 224,
            "108432563": 237,
            "108429814": 1,
            "108426937": 1,
            "108422886": 240,
            "108399266": 43,
            "108374873": 11,
        },
        "wool_432": {
            "108568560": 1,
            "108559476": 246,
            "108534412": 232,
            "108504670": 1,
            "108472548": 55,
            "108461768": 189,
            "108432563": 227,
            "108429814": 5,
            "108426937": 5,
            "108422886": 241,
            "108399266": 1,
            "108374873": 1,
        },
        "same_class_as_0913c": True,
        "same_class_note": "Same extra-animal family as 09-13c/09-13r: extra-animal 8c6s3g plus extra-goose plus extra-animal YARN 6c11s plus identical-clone extra-goose. WTL 4-0-8 mean -1150.5 vs 09-13r 3-0-9 mean -7018.0. New window games are alcanta 108568560 extra-goose -19224 and Farmer Shuang 108559476 extra-animal YARN 6c11s -418. clone=12/12.",
        "loss_class": LOSS_CLASS,
        "worst_losses": [
            {
                "id": 108568560,
                "opp": "alcanta",
                "margin": -19224.0,
                "herd_us": "9c5s",
                "herd_opp": "9c5s3g",
                "shops": ["SMOOTHIE_SHOP"],
            }
        ],
    }
    dump("20260913s_cut16_loss_class.json", loss)

    packet = {
        "title": "Kaggriculture study packet 2026-09-13s",
        "not_the_0913r_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913s/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913s/kaggriculture-publicleaderboard-2026-09-13T14-36-51.csv",
            "leaderboard_api": "experiments/20260913s_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913s",
            "top_replays": "artifacts/kaggle_runs/top_20260913s",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913s",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913s_gate.json",
            "episode_report": "experiments/20260913s_episode_report.json",
            "hunt_report": "experiments/20260913s_hunt_report.json",
            "algo_note": "experiments/20260913s_algo_note.json",
            "loss_class": "experiments/20260913s_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1670.2,
            "rank": 2026,
            "n_teams": 8896,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1319.5,
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
            "cut16_score": 1670.2,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2904.6,
            "rank10": {"team": "binghua", "score": 2964.4},
            "rank1": {"team": "Majkel1337", "score": 3248.1, "submissionId": 56156662},
            "public_cut16": {"n": 230, "wtl": [100, 2, 128], "mean_margin": -1226.1},
        },
        "rolling": {
            "previous": "experiments/20260913r_cut16_rolling.json",
            "live_cut16": "experiments/20260913s_cut16_rolling.json",
            "ids": ROLLING_IDS,
            "ids_not_identical_to_0913r": True,
            "n": 12,
            "wtl": [4, 0, 8],
            "mean_margin": -1150.5,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": 108568560,
            "margin": -19224.0,
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "9c5s",
            "herd_opp": "9c5s3g",
            "sheep_steps_us": [2, 196, 314],
        },
        "top_board": {
            "source": "experiments/20260913s_top10_games.json",
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
            ],
            "Majkel1337": {
                "land": [
                    [150, 220, 222],
                    [150, 218, 220, 222],
                    [150, 220, 222],
                    [150, 220, 222],
                ],
                "herd": ["6c16s0g", "6c7s4g", "8c9s2g", "8c11s0g"],
                "wheat": [497, 510, 497, 466],
                "shops": ["BAKERY", "BRUNCH_SPOT", "SMOOTHIE_SHOP", "YARN_STORE"],
                "clone": "0_of_4",
                "episodes": [108570750, 108563756, 108557488, 108081303],
                "note": "CSV #1 3248.1 live 3249.0 scoring sub 56156662. Ids disjoint from 20260913r Majkel set. Mid-land 150 then 218-222 (three 150/220/222; one 150/218/220/222), wheat 466-510, clone=0 on 4/4, goose mix 0g/4g/2g/0g. Opening land is not a later-block license.",
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
            "score": 1670.2,
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
            "why": "Already live COMPLETE 1670.2. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. Rolling 108568560 already faced opp extra cow 218 extra sheep 227 extra geese 242/266 9c5s3g -19224; 108432563 already bought 218/242/266 sheep and lost YARN 6c11s -10575. Not cut 12/13.",
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: new slug renjistarfall/kaggriculture-best-agent SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay; no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1670.2 and keeps 1319.5.",
        },
        "hunt": hunt["hunt"],
    }
    dump("20260913s_study_packet.json", packet)


if __name__ == "__main__":
    main()
