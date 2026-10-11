"""Write 20260914j study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
    108871316,
    108846707,
    108842428,
    108814509,
    108810346,
    108807526,
    108784373,
    108781918,
    108753975,
    108751924,
    108744906,
    108741805,
]
PREV_14I = [
    108851261,
    108822458,
    108817790,
    108787437,
    108762693,
    108723413,
    108704919,
    108686716,
    108669139,
    108658948,
    108656070,
    108642657,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (Quillbolt 108753975 4c15s vs 8c6s3g FARMERS_MARKET extra sheep 218/242/266 already bought vs opp extra sheep 218/227 extra geese 242/266 -9650) "
    "+ extra-goose (bplyc15 108784373 9c5s vs 9c5s3g PIZZA extra cow 218 extra sheep 227 extra geese 242/266 -7879; "
    "Scorn100 108846707 9c8s vs 6c6s6g PET_CAFE extra sheep 227/242/266 already bought vs opp extra geese 218/227/242 extra sheep 266 -5681; "
    "refine123 108871316 9c5s3g vs 9c5s4g ICE_CREAM extra geese 227/242 already bought vs opp extra goose 218 extra geese 227/242 extra sheep 266 -6523) "
    "+ identical-clone extra-goose (\u6211\u662f\u5218\u5927\u806a 108744906 9c5s3g vs 9c5s3g extra geese 227/242 already bought -9197) "
    "+ identical-clone extra-sheep (trung 108814509 6c11s vs 6c11s YARN extra sheep 218/242/266 already bought -5487) "
    "+ extra-sheep (higuuu 108751924 9c8s vs 7c11s BRUNCH extra sheep 227/242/266 already bought -3065). "
    "Wins: DASH\u6751 108781918 4c14s vs 6c6s5g +6327 extra sheep 218/242/266 already bought; "
    "Finca Nagano 108810346 6c12s vs 6c11s YARN +2249 extra sheep 218/242/266 already bought; "
    "Andrew Reed 108807526 7c6s vs 8c6s3g +1635 extra cow 218 vs opp extra sheep 218/227 extra geese 242/266; "
    "Cathy 108842428 9c5s3g vs 9c5s3g +51 identical-clone extra geese 227/242 already bought; "
    "y3uanm 108741805 9c5s3g vs 9c5s3g +54 extra geese 227/242 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Quillbolt already bought extra sheep 218/242/266 and lost vs 8c6s3g; "
    "Scorn100 already bought extra sheep 227/242/266 and lost vs 6g; "
    "higuuu already bought extra sheep 227/242/266 and lost 11s; "
    "trung already bought extra sheep 218/242/266 and lost identical-clone 11s; "
    "bplyc15 lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; "
    "refine123 already bought extra geese 227/242 and lost vs 4g; "
    "\u6211\u662f\u5218\u5927\u806a already bought extra geese 227/242 and lost identical-clone; "
    "Cathy/y3uanm already bought extra geese 227/242 and won identical-clone; "
    "DASH already bought extra sheep 218/242/266 and won vs 5g; "
    "Finca already bought extra sheep 218/242/266 and won 12s vs 11s; "
    "Andrew Reed extra cow 218 vs 8c6s3g and won."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1627.8 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1298.7 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1627.8; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt no new slug vs _hunt_20260914i "
    "(public search newest still xuantianfengwu/kaggriculture-adaptive-land-allocator-r10 SHA 3b8a1d4d heuristic 6-cow). "
    "Do not reupload boatlee 55710781. Cut 12/13 Hold."
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
    "experiments/20260914b_top10_games.json",
    "experiments/20260914c_top10_games.json",
    "experiments/20260914d_top10_games.json",
    "experiments/20260914e_top10_games.json",
    "experiments/20260914f_top10_games.json",
    "experiments/20260914g_top10_games.json",
    "experiments/20260914h_top10_games.json",
    "experiments/20260914i_top10_games.json",
]
HUNT: list[dict] = []


def dump(name: str, obj) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    hunt = {
        "date": "2026-09-14",
        "packet": "20260914j",
        "kernels_not_in_0914i_packet": False,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260914j",
        "inspect_scripts": [
            "experiments/candidates/scan_hunt_20260914j.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_no_new_notebook",
        "compare_0914i": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260914i",
            "hunt_report": "experiments/20260914i_hunt_report.json",
            "gate": "experiments/20260914i_gate.json",
            "note": (
                "No new slug vs _hunt_20260914i. Public search newest is still "
                "xuantianfengwu/kaggriculture-adaptive-land-allocator-r10 (lastRunTime 2026-09-14 04:37:17.347000). "
                "Did not re-pull rejected kernels (arsgorynich v40-challenger SHA 546c4224, xuantianfengwu r10 SHA 3b8a1d4d, "
                "aurax7 v5 SHA ea4c28e6, lime0001 t23 SHA 31ee22dc, nathanjacob V40 autopsy dataset wrapper, Ahmed V41 SHA 8951ff93, "
                "prvsiyan reserve-garden, alperen scored-agent SHA 85c8b532, xuantianfengwu adaptive-land-allocator SHA d12f2987, "
                "renjistarfall V39 reprint, alperen metacounter-r1 analysis, xuantianfengwu land-labor-capital, Ahmed V40 SHA 546c4224, "
                "guru V39, yhay81 0913, wei v46d review, Ahmed V39, aurax7 v4, crystalbaby V38, prvsiyan market-ledger, timed-six-cow, "
                "lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, "
                "melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
            ),
        },
        "public_search_newest": "xuantianfengwu/kaggriculture-adaptive-land-allocator-r10",
        "public_search_newest_lastRunTime": "2026-09-14 04:37:17.347000",
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
        "named_kernels_scanned": [row["kernel"] for row in HUNT],
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
        "hunt": HUNT,
    }
    dump("20260914j_hunt_report.json", hunt)

    gate = json.loads((ROOT / "experiments/20260914i_gate.json").read_text(encoding="utf-8"))
    gate["packet"] = "20260914j"
    gate["named_kernels_scanned"] = [row["kernel"] for row in HUNT]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260914j"
    gate["hunt_report"] = "experiments/20260914j_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1627.8
    gate["live"]["shopbag"]["score_complete"] = 1298.7
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1627.8 partnered with newer shopbag 56151155 COMPLETE 1298.7 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "No new public slug vs _hunt_20260914i. Public search newest still xuantianfengwu/kaggriculture-adaptive-land-allocator-r10 SHA 3b8a1d4d heuristic 6-cow. "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
        "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: Quillbolt extra sheep 218/242/266 already bought vs 8c6s3g -9650; "
        "\u6211\u662f\u5218\u5927\u806a extra geese 227/242 already bought identical-clone -9197; "
        "bplyc15 extra cow 218 extra sheep 227 extra geese 242/266 -7879; "
        "refine123 extra geese 227/242 already bought vs 4g -6523; "
        "Cathy/y3uanm already bought extra geese 227/242 and won +51/+54."
    )
    dump("20260914j_gate.json", gate)

    algo = json.loads((ROOT / "experiments/20260914i_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-14"
    algo["packet"] = "20260914j"
    algo["live"]["cut16"]["csv_0914j_team_score"] = 1627.8
    algo["live"]["shopbag"]["score_complete"] = 1298.7
    algo["live"]["rank_csv_0914j"] = 2120
    algo["cut16_live_failure_class"]["0914j"] = {
        "file": "experiments/20260914j_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [5, 0, 7],
        "mean_margin": -3097.2,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus identical-clone extra-goose plus identical-clone extra-sheep plus extra-sheep",
        "heavy": [
            {
                "id": 108753975,
                "opp": "Quillbolt",
                "margin": -9650,
                "shops72": ["FARMERS_MARKET"],
                "buy": "4c15s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 231,
            },
            {
                "id": 108744906,
                "opp": "\u6211\u662f\u5218\u5927\u806a",
                "margin": -9197,
                "shops72": ["FARMERS_MARKET"],
                "buy": "9c5s3g vs 9c5s3g",
                "clone": 1,
            },
            {
                "id": 108784373,
                "opp": "bplyc15",
                "margin": -7879,
                "shops72": ["PIZZA_SHOP"],
                "buy": "9c5s vs 9c5s3g",
                "clone": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "No new public slug vs _hunt_20260914i. "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump("20260914j_algo_note.json", algo)

    dump(
        "20260914j_episode_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914j",
            "utc": "2026-09-14T10:41:40Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1627.8,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1627.8 (was 1632.1). Newest public 108871316 updatedScore 1627.847. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1298.7 / ListEpisodes last_updated 1298.735) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1298.7 < 1500 "
                "and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1298.7,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2120,
            "heralces_score": 1627.8,
            "n_teams_csv": 8984,
            "public_56151152": {
                "n_public": 261,
                "n_validation": 1,
                "n_completed_public": 261,
                "wtl": [110, 2, 149],
                "mean_margin": -1650.9,
                "status": "COMPLETE",
                "publicScore": 1627.8,
            },
            "rolling_ids": ROLLING_IDS,
            "rolling_forbidden_0914i": PREV_14I,
            "ids_not_identical_to_0914i": True,
            "ids_disjoint_from_0914i": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [5, 0, 7],
            "mean_margin": -3097.2,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids disjoint from 20260914i packet, all 720 DONE/DONE. 5W 7L. "
                "Worst Quillbolt 108753975 L -9650 4c15s vs 8c6s3g clone=1 extra sheep 218/242/266 already bought vs opp extra sheep 218/227 extra geese 242/266. "
                "New-window refine123 108871316 extra-goose 3g vs 4g. "
                "Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        "20260914j_cut16_loss_class.json",
        {
            "date": "2026-09-14",
            "packet": "20260914j",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": ROLLING_IDS,
            "ids_0914i": PREV_14I,
            "disjoint_from_0914i": True,
            "all_720_done_done": True,
            "wtl": [5, 0, 7],
            "mean_margin": -3097.2,
            "clone_n": 12,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 27.0],
            "wool_360": {
                108871316: 43,
                108846707: 224,
                108842428: 37,
                108814509: 236,
                108810346: 245,
                108807526: 1,
                108784373: 1,
                108781918: 232,
                108753975: 231,
                108751924: 234,
                108744906: 43,
                108741805: 37,
            },
            "wool_432": {
                108871316: 1,
                108846707: 189,
                108842428: 1,
                108814509: 223,
                108810346: 244,
                108807526: 5,
                108784373: 88,
                108781918: 209,
                108753975: 200,
                108751924: 200,
                108744906: 1,
                108741805: 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-14b/09-14c/09-14d/09-14e/09-14f/09-14g/09-14h/09-14i: extra-animal 8c6s3g plus extra-goose plus identical-clone extra-goose plus identical-clone extra-sheep plus extra-sheep. "
                "WTL 5-0-7 mean -3097.2 vs 09-14i 2-0-10 mean -7716.1. New window game refine123 108871316 -6523. clone=12/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 108753975,
                    "opp": "Quillbolt",
                    "margin": -9650.0,
                    "herd_us": "4c15s",
                    "herd_opp": "8c6s3g",
                    "shops": ["FARMERS_MARKET"],
                }
            ],
        },
    )

    dump(
        "20260914j_study_packet.json",
        {
            "title": "Kaggriculture study packet 2026-09-14j",
            "not_the_0914i_packet": True,
            "no_upload": NO_UPLOAD,
            "upload_bail": True,
            "upload_bail_reasons": {
                "a_newest_cut_pending": False,
                "b_newest_cut_complete_below_1500": False,
                "c_drop_ge1500_without_ge1500_partner": True,
            },
            "sources": {
                "leaderboard_zip": "artifacts/kaggle_runs/lb_20260914j/kaggriculture.zip",
                "leaderboard_csv": "artifacts/kaggle_runs/lb_20260914j/kaggriculture-publicleaderboard-2026-09-14T10-41-40.csv",
                "leaderboard_api": "experiments/20260914j_public_leaderboard_api.json",
                "episodes_cut16": "experiments/episodes_56151152.json",
                "cut16_replays": "artifacts/kaggle_runs/cut16_20260914j",
                "top_replays": "artifacts/kaggle_runs/top_20260914j",
                "hunt_dir": "artifacts/public_sources/_hunt_20260914j",
                "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
                "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
                "gate": "experiments/20260914j_gate.json",
                "episode_report": "experiments/20260914j_episode_report.json",
                "hunt_report": "experiments/20260914j_hunt_report.json",
                "algo_note": "experiments/20260914j_algo_note.json",
                "loss_class": "experiments/20260914j_cut16_loss_class.json",
            },
            "live": {
                "sixday": 56028043,
                "sixday_score": 1590.8,
                "sixday_status": "COMPLETE",
                "team_score": 1627.8,
                "rank": 2120,
                "n_teams": 8984,
                "shopbag_previous": 56112309,
                "shopbag_reupload": 56151155,
                "shopbag_status": "COMPLETE",
                "shopbag_score": 1298.7,
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
                "cut16_score": 1627.8,
                "root_main_py": "h2 65e6f5cd... unchanged",
                "gold21": 2928.9,
                "rank10": {"team": "Thomas Tschinkel", "score": 2974.0},
                "rank1": {
                    "team": "Majkel1337",
                    "score": 3211.7,
                    "submissionId": 56156662,
                },
                "public_cut16": {
                    "n": 261,
                    "wtl": [110, 2, 149],
                    "mean_margin": -1650.9,
                },
            },
            "rolling": {
                "previous": "experiments/20260914i_cut16_rolling.json",
                "live_cut16": "experiments/20260914j_cut16_rolling.json",
                "ids": ROLLING_IDS,
                "ids_not_identical_to_0914i": True,
                "n": 12,
                "wtl": [5, 0, 7],
                "mean_margin": -3097.2,
                "loss_class": LOSS_CLASS,
            },
            "excluding": {
                "id": 108871316,
                "margin": -6523.0,
                "clone": True,
                "Q": [3, 3],
                "land": [151, 266],
                "herd_us": "9c5s3g",
                "herd_opp": "9c5s4g",
                "sheep_steps_us": [2, 196, 218, 266],
            },
            "top_board": {
                "source": "experiments/20260914j_top10_games.json",
                "not_copied_from": NOT_COPIED,
                "Majkel1337": {
                    "land": [
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                    ],
                    "herd": ["7c15s0g", "9c5s2g", "9c3s2g", "5c11s0g"],
                    "wheat": [391, 538, 659, 409],
                    "shops": ["PIZZA_SHOP", "ICE_CREAM_SHOP", "PIZZA_SHOP", "YARN_STORE"],
                    "clone": "0_of_4",
                    "episodes": [108878440, 108872254, 108866071, 108694097],
                    "note": (
                        "CSV #1 3211.7 live 3213.9 scoring sub 56156662 (current sub 56216119 is 3008.3). "
                        "Ids disjoint from 20260914i Majkel set. Mid-land 150 then 220-222 "
                        "(all four 150/220/222), "
                        "wheat 391-659, clone=0 on 4/4, goose mix 0g/2g/2g/0g. Opening land is not a later-block license."
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
                "score": 1627.8,
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
                    "Already live COMPLETE 1627.8. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                    "Rolling 108753975 extra sheep 218/242/266 already bought and lost 4c15s vs 8c6s3g -9650; "
                    "108744906 extra geese 227/242 already bought and lost identical-clone 9c5s3g -9197; "
                    "108871316 extra geese 227/242 already bought and lost 9c5s3g vs 9c5s4g -6523. "
                    "New-window refine123 108871316 extra-goose 3g vs 4g. Not cut 12/13."
                ),
            },
            "cut17": {
                "hold": True,
                "uploaded": None,
                "why": (
                    "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: no new slug vs 0914i; "
                    "public search newest still xuantianfengwu/kaggriculture-adaptive-land-allocator-r10 SHA 3b8a1d4d heuristic 6-cow; "
                    "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                    "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1627.8 and keeps 1298.7."
                ),
            },
            "hunt": hunt["hunt"],
        },
    )


if __name__ == "__main__":
    main()
