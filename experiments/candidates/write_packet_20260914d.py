"""Write 20260914d study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
    108784373,
    108781918,
    108753975,
    108751924,
    108744906,
    108741805,
    108608562,
    108604498,
    108586169,
    108568560,
    108559476,
    108550653,
]
PREV_14C = [
    108762693,
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
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (AQiDA19 108550653 7c6s vs 8c6s3g BAKERY extra sheep 218/227 extra geese 242/266 -21800; "
    "Quillbolt 108753975 4c15s vs 8c6s3g FARMERS_MARKET extra sheep 218/227 extra geese 242/266 and we already bought extra sheep 218/242/266 -9650) "
    "+ extra-goose (alcanta 108568560 9c5s vs 9c5s3g SMOOTHIE extra cow 218 extra sheep 227 extra geese 242/266 -19224; "
    "bplyc15 108784373 9c5s vs 9c5s3g PIZZA extra cow 218 extra sheep 227 extra geese 242/266 -7879) "
    "+ identical-clone extra-goose (我是刘大聪 108744906 9c5s3g vs 9c5s3g extra geese 227/242 already bought -9197) "
    "+ extra-sheep (higuuu 108751924 9c8s vs 7c11s BRUNCH extra sheep 218/227/242/266 already bought -3065) "
    "+ extra-animal YARN (Farmer Shuang 108559476 6c11s vs 7c11s extra sheep 218/242/266 already bought -418). "
    "Wins: dupakdungking 108608562 6c12s vs 8c6s3g YARN +9867 extra sheep 218/242/266 already bought; "
    "DASH村 108781918 4c14s vs 6c6s5g FARMERS_MARKET +6327 extra sheep 218/242/266 already bought vs extra geese 227/242; "
    "Hanaro 108604498 4c14s vs 8c6s3g BRUNCH +114 extra sheep 218/242/266 already bought; "
    "y3uanm 108741805 9c5s3g vs 9c5s3g +54 extra geese 227/242 already bought; "
    "maxout 108586169 9c5s3g vs 9c5s3g +8 extra geese 227/242 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-25 not 0. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: AQiDA19/Quillbolt lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
    "alcanta/bplyc15 lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; "
    "我是刘大聪 already bought extra geese 227/242 and lost identical-clone; higuuu already bought extra sheep 218/227/242/266 and lost 11s; "
    "Farmer Shuang already bought extra sheep 218/242/266 and lost YARN 11s; "
    "dupakdungking/DASH村/Hanaro already bought extra sheep 218/242/266 and won; y3uanm/maxout already bought extra geese 227/242 and won identical-clone."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1640.5 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1310.6 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1640.5; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 3 new slugs vs _hunt_20260914c "
    "(aurax7 reactive-v5 SHA ea4c28e6 Shop0909 144/648 + 288/712 overlay; xuantianfengwu land-allocator-r10 SHA 3b8a1d4d "
    "heuristic 6-cow; lime0001 t23 SHA 31ee22dc Shop0909 144/648 + 288/712 overlay). Do not reupload boatlee 55710781. Cut 12/13 Hold."
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
]
HUNT = [
    {
        "kernel": "xuantianfengwu/kaggriculture-adaptive-land-allocator-r10",
        "path": "artifacts/public_sources/_hunt_20260914d/xuantianfengwu__adaptive-land-allocator-r10/kaggriculture-adaptive-land-allocator-r10.ipynb",
        "verdict": "reject_heuristic_six_cow_allocator_r10",
        "sha256": "3b8a1d4d0115968dbef2b3414b23346653cd402fe006c37bed63b30a27854423",
        "note": (
            "New slug vs _hunt_20260914c (lastRunTime 2026-09-14 04:37:17.347000; public-search newest by dateCreated). "
            "Python %%writefile submission.py SHA 3b8a1d4d... Distinct from adaptive-land-allocator SHA d12f2987, "
            "land-labor-capital SHA b49709bd, and timed-six-cow SHA 5dc0c68c. Still heuristic 6-cow (`[\"COW\"] * 6`). "
            "No farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; "
            "not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "aurax7/kaggriculture-shop-router-reactive-v5",
        "path": "artifacts/public_sources/_hunt_20260914d/aurax7__shop-router-reactive-v5/kaggriculture-shop-router-reactive-v5.ipynb",
        "verdict": "reject_shop0909_144_648_and_712_overlay",
        "sha256": "ea4c28e64d77ddcdd5f08cb150b408de3c10f4bc9a18c6e681758b7da2e8f022",
        "note": (
            "New slug vs _hunt_20260914c (lastRunTime 2026-09-14 04:31:10.073000). Python %%writefile main.py SHA ea4c28e6... "
            "Distinct from reactive-v4 SHA 3dd123c5 and live cuts 14/15/16 (notebook embeds cut15 SHA b87a27ed as a comment/payload, "
            "writefile itself is not cut15). Shop0909 day-6 144/648 plus 288 quote overlay plus step==712 terminal planner. "
            "216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. No ctypes/agent.so. Cells not executed. "
            "Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "lime0001/t23-kaggriculture-smart-adaptive-harvest",
        "path": "artifacts/public_sources/_hunt_20260914d/lime0001__t23-smart-adaptive-harvest/t23-kaggriculture-smart-adaptive-harvest.py",
        "verdict": "reject_shop0909_144_648_and_712_overlay",
        "sha256": "31ee22dce4afba3f335a971fa405ec7d151c65a4a8ec56028aaae78225b7dea9",
        "note": (
            "New slug vs _hunt_20260914c files (lastRunTime 2026-09-14 00:27:07.057000; script kernel, no %%writefile). "
            "SHA 31ee22dc... Distinct from Ahmed V41 SHA 8951ff93, V39 708c7485, V38 a2047ebd, aurax7 v5 ea4c28e6. "
            "Shop0909 day-6 144/648 plus 288 overlay plus step==712 terminal planner. 216<=step<=227 is milk-shop livestock sub, "
            "not a farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
]


def dump(name: str, obj) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    hunt = {
        "date": "2026-09-14",
        "packet": "20260914d",
        "kernels_not_in_0914c_packet": True,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260914d",
        "inspect_scripts": [
            "experiments/candidates/scan_hunt_20260914d.py",
            "experiments/candidates/inspect_hunt_20260914d.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "writefile_sha_only_no_cell_exec",
        "compare_0914c": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260914c",
            "hunt_report": "experiments/20260914c_hunt_report.json",
            "gate": "experiments/20260914c_gate.json",
            "note": (
                "3 new slugs vs _hunt_20260914c. Public search newest is now "
                "xuantianfengwu/kaggriculture-adaptive-land-allocator-r10 (lastRunTime 2026-09-14 04:37:17.347000). "
                "Did not re-pull rejected kernels (nathanjacob V40 autopsy dataset wrapper, Ahmed V41 SHA 8951ff93, "
                "prvsiyan reserve-garden, alperen scored-agent SHA 85c8b532, xuantianfengwu adaptive-land-allocator SHA d12f2987, "
                "renjistarfall V39 reprint, alperen metacounter-r1 analysis, xuantianfengwu land-labor-capital, Ahmed V40, "
                "guru V39, yhay81 0913, wei v46d review, Ahmed V39, aurax7 v4, crystalbaby V38, prvsiyan market-ledger, "
                "timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, "
                "municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
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
    dump("20260914d_hunt_report.json", hunt)

    gate = json.loads((ROOT / "experiments/20260914c_gate.json").read_text(encoding="utf-8"))
    gate["packet"] = "20260914d"
    gate["named_kernels_scanned"] = [row["kernel"] for row in HUNT]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260914d"
    gate["hunt_report"] = "experiments/20260914d_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1640.5
    gate["live"]["shopbag"]["score_complete"] = 1310.6
    new_rejected = [
        {
            "kernel": row["kernel"],
            "verdict": row["verdict"],
            "note": row["note"],
        }
        for row in HUNT
    ]
    old_rejected = [
        row
        for row in gate["rejected"]
        if row.get("kernel") not in {h["kernel"] for h in HUNT}
    ]
    gate["rejected"] = new_rejected + old_rejected
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1640.5 partnered with newer shopbag 56151155 COMPLETE 1310.6 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "3 new public slugs vs _hunt_20260914c, none licensed: aurax7 reactive-v5 SHA ea4c28e6 Shop0909 overlay; "
        "xuantianfengwu land-allocator-r10 SHA 3b8a1d4d heuristic 6-cow; lime0001 t23 SHA 31ee22dc Shop0909 overlay. "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
        "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: AQiDA19 extra sheep 218/227 extra geese 242/266 -21800; "
        "alcanta extra cow 218 extra sheep 227 extra geese 242/266 -19224; "
        "bplyc15 extra cow 218 extra sheep 227 extra geese 242/266 -7879; "
        "我是刘大聪 already bought extra geese 227/242 and lost -9197; DASH村 already bought extra sheep 218/242/266 and won +6327."
    )
    dump("20260914d_gate.json", gate)

    algo = json.loads((ROOT / "experiments/20260914c_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-14"
    algo["packet"] = "20260914d"
    algo["live"]["cut16"]["csv_0914d_team_score"] = 1640.5
    algo["live"]["shopbag"]["score_complete"] = 1310.6
    algo["live"]["rank_csv_0914d"] = 2089
    algo["cut16_live_failure_class"]["0914d"] = {
        "file": "experiments/20260914d_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [5, 0, 7],
        "mean_margin": -4571.9,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus identical-clone extra-goose plus extra-sheep plus extra-animal YARN",
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
                "id": 108568560,
                "opp": "alcanta",
                "margin": -19224,
                "shops72": ["SMOOTHIE_SHOP"],
                "buy": "9c5s vs 9c5s3g",
                "opp216": [218, 227, 242, 266],
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "3 new public slugs vs _hunt_20260914c, none licensed (aurax7 v5 Shop0909 overlay; r10 heuristic 6-cow; lime0001 Shop0909 overlay). "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump("20260914d_algo_note.json", algo)

    dump(
        "20260914d_episode_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914d",
            "utc": "2026-09-14T04:42:02Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1640.5,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1640.5 (was 1639.4). Newest public 108784373 updatedScore 1640.501. Newest-2 = shopbag reupload 56151155 "
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
            "heralces_rank_csv": 2089,
            "heralces_score": 1640.5,
            "n_teams_csv": 8946,
            "public_56151152": {
                "n_public": 251,
                "n_validation": 1,
                "n_completed_public": 251,
                "wtl": [107, 2, 142],
                "mean_margin": -1501.2,
                "status": "COMPLETE",
                "publicScore": 1640.5,
            },
            "rolling_ids": ROLLING_IDS,
            "rolling_forbidden_0914c": PREV_14C,
            "ids_not_identical_to_0914c": True,
            "ids_disjoint_from_0914c": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [5, 0, 7],
            "mean_margin": -4571.9,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260914c packet. 5W 7L. "
                "Worst AQiDA19 108550653 L -21800 7c6s vs 8c6s3g clone=1 extra sheep 218/227 extra geese 242/266. "
                "New-window bplyc15 108784373 L -7879 9c5s vs 9c5s3g extra cow 218 extra sheep 227 extra geese 242/266. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        "20260914d_cut16_loss_class.json",
        {
            "date": "2026-09-14",
            "packet": "20260914d",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": ROLLING_IDS,
            "ids_0914c": PREV_14C,
            "disjoint_from_0914c": True,
            "all_720_done_done": True,
            "wtl": [5, 0, 7],
            "mean_margin": -4571.9,
            "clone_n": 12,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 25.0],
            "wool_360": {
                108784373: 1,
                108781918: 232,
                108753975: 231,
                108751924: 234,
                108744906: 43,
                108741805: 37,
                108608562: 236,
                108604498: 232,
                108586169: 37,
                108568560: 1,
                108559476: 245,
                108550653: 1,
            },
            "wool_432": {
                108784373: 88,
                108781918: 209,
                108753975: 200,
                108751924: 200,
                108744906: 1,
                108741805: 1,
                108608562: 232,
                108604498: 209,
                108586169: 1,
                108568560: 1,
                108559476: 246,
                108550653: 5,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-14b/09-14c: extra-animal 8c6s3g plus extra-goose plus identical-clone extra-goose plus extra-sheep plus extra-animal YARN. "
                "WTL 5-0-7 mean -4571.9 vs 09-14c 2-0-10 mean -6781.9. New window games are bplyc15 108784373 -7879 and DASH村 108781918 +6327. clone=12/12."
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
        "20260914d_study_packet.json",
        {
            "title": "Kaggriculture study packet 2026-09-14d",
            "not_the_0914c_packet": True,
            "no_upload": NO_UPLOAD,
            "upload_bail": True,
            "upload_bail_reasons": {
                "a_newest_cut_pending": False,
                "b_newest_cut_complete_below_1500": False,
                "c_drop_ge1500_without_ge1500_partner": True,
            },
            "sources": {
                "leaderboard_zip": "artifacts/kaggle_runs/lb_20260914d/kaggriculture.zip",
                "leaderboard_csv": "artifacts/kaggle_runs/lb_20260914d/kaggriculture-publicleaderboard-2026-09-14T04-42-02.csv",
                "leaderboard_api": "experiments/20260914d_public_leaderboard_api.json",
                "episodes_cut16": "experiments/episodes_56151152.json",
                "cut16_replays": "artifacts/kaggle_runs/cut16_20260914d",
                "top_replays": "artifacts/kaggle_runs/top_20260914d",
                "hunt_dir": "artifacts/public_sources/_hunt_20260914d",
                "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
                "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
                "gate": "experiments/20260914d_gate.json",
                "episode_report": "experiments/20260914d_episode_report.json",
                "hunt_report": "experiments/20260914d_hunt_report.json",
                "algo_note": "experiments/20260914d_algo_note.json",
                "loss_class": "experiments/20260914d_cut16_loss_class.json",
            },
            "live": {
                "sixday": 56028043,
                "sixday_score": 1590.8,
                "sixday_status": "COMPLETE",
                "team_score": 1640.5,
                "rank": 2089,
                "n_teams": 8946,
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
                "cut16_score": 1640.5,
                "root_main_py": "h2 65e6f5cd... unchanged",
                "gold21": 2922.3,
                "rank10": {"team": "feel the agi", "score": 2964.7},
                "rank1": {
                    "team": "Majkel1337",
                    "score": 3196.8,
                    "submissionId": 56156662,
                },
                "public_cut16": {
                    "n": 251,
                    "wtl": [107, 2, 142],
                    "mean_margin": -1501.2,
                },
            },
            "rolling": {
                "previous": "experiments/20260914c_cut16_rolling.json",
                "live_cut16": "experiments/20260914d_cut16_rolling.json",
                "ids": ROLLING_IDS,
                "ids_not_identical_to_0914c": True,
                "n": 12,
                "wtl": [5, 0, 7],
                "mean_margin": -4571.9,
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
                "source": "experiments/20260914d_top10_games.json",
                "not_copied_from": NOT_COPIED,
                "Majkel1337": {
                    "land": [
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 218, 220, 222],
                    ],
                    "herd": ["11c9s0g", "11c3s0g", "9c5s2g", "9c3s4g"],
                    "wheat": [483, 576, 567, 449],
                    "shops": ["PIZZA_SHOP", "ICE_CREAM_SHOP", "ICE_CREAM_SHOP", "BAKERY"],
                    "clone": "1_of_4",
                    "episodes": [108784043, 108777858, 108771918, 108714609],
                    "note": (
                        "CSV #1 3196.8 live 3196.8 scoring sub 56156662 (current sub 56216119 is 2944.9). "
                        "Ids disjoint from 20260914c Majkel set. Mid-land 150 then 218-222 "
                        "(three 150/220/222; one 150/218/220/222), "
                        "wheat 449-576, clone=1 on 4/4, goose mix 0g/0g/2g/4g. Opening land is not a later-block license."
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
                "score": 1640.5,
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
                    "Already live COMPLETE 1640.5. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                    "Rolling 108550653 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -21800; 108568560 extra cow 218 extra sheep 227 extra geese 242/266 -19224; "
                    "108784373 extra cow 218 extra sheep 227 extra geese 242/266 -7879. New-window DASH村 108781918 already bought extra sheep 218/242/266 and won +6327. Not cut 12/13."
                ),
            },
            "cut17": {
                "hold": True,
                "uploaded": None,
                "why": (
                    "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 3 new slugs vs 0914c, none licensed "
                    "(aurax7 v5 Shop0909 overlay SHA ea4c28e6; r10 heuristic 6-cow SHA 3b8a1d4d; lime0001 Shop0909 overlay SHA 31ee22dc); "
                    "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                    "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1640.5 and keeps 1310.6."
                ),
            },
            "hunt": hunt["hunt"],
        },
    )


if __name__ == "__main__":
    main()
