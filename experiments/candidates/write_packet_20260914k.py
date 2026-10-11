"""Write 20260914k study JSON from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLING_IDS = [
    108889446,
    108889378,
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
]
PREV_14J = [
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
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (HaoChi 108817790 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -6212; "
    "\u0438\u0442\u043c\u043e\u043d\u044f\u044f\u044f 108762693 10c8s vs 8c6s3g PET_CAFE extra cow 218 extra sheep 227/242/266 already bought vs opp extra sheep 218/227 extra geese 242/266 -6320) "
    "+ extra-goose (LaiCxm 108851261 9c5s vs 9c5s3g PIZZA extra cow 218 extra sheep 227 extra geese 242/266 -16092; "
    "here we go 108704919 9c5s3g vs 6c6s6g FARMERS_MARKET extra geese 227/242 already bought -7788; "
    "Toru59er 108787437 9c5s vs 9c5s3g ICE_CREAM extra cow 218 extra sheep 227 extra geese 242/266 -6986) "
    "+ extra-sheep (Pietro Valocchi 108658948 7c6s vs 8c9s FARMERS_MARKET extra cow 218 vs opp extra sheep 218/227/242/266 -12549; "
    "Revanth Tambisetty 108822458 4c15s vs 6c11s SMOOTHIE extra sheep 218/242/266 already bought vs opp extra sheep 218/227 -11033; "
    "Adhiraj Jagtap 108889378 6c11s vs 9c9s YARN extra sheep 218/242/266 already bought vs opp extra sheep 218/227/242/266 -2087) "
    "+ identical-clone extra-sheep (\u0412\u0430\u0440\u0438\u043c \u0441\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0441\u0430\u043c\u043e\u0433\u043e\u043d 108889446 6c11s vs 6c11s YARN extra sheep 218/242/266 already bought vs opp extra sheep 218/227 -12131) "
    "+ identical-clone extra-goose (Cuong Le 108686716 9c5s3g vs 9c5s3g extra geese 227/242 already bought -590). "
    "Wins: Surya Bhattiprol 108669139 9c5s3g vs 9c5s4g +1729 extra geese 227/242 already bought; "
    "zard599 108723413 9c5s3g vs 9c5s4g +748 extra geese 227/242 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-22 not 0. "
    "Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: \u0412\u0430\u0440\u0438\u043c already bought extra sheep 218/242/266 and lost identical-clone 11s; "
    "Adhiraj already bought extra sheep 218/242/266 and lost vs 9c9s; "
    "LaiCxm lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; "
    "HaoChi extra cow 218 vs 8c6s3g -6212; "
    "\u0438\u0442\u043c\u043e\u043d\u044f\u044f\u044f already bought extra sheep 227/242/266 and lost vs 8c6s3g; "
    "Revanth already bought extra sheep 218/242/266 and lost 15s vs 11s; "
    "Pietro lost extra-sheep after opp extra sheep 218/227/242/266; "
    "here we go already bought extra geese 227/242 and lost vs 6g; "
    "Toru59er lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; "
    "Cuong Le already bought extra geese 227/242 and lost identical-clone; "
    "zard599/Surya already bought extra geese 227/242 and won vs 4g."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1619.1 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1295.7 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1619.1; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 3 new slugs vs _hunt_20260914j "
    "(public search newest sorcererbi/your-offline-arena-is-lying-to-you lastRunTime 2026-09-14 10:53:08.673000; "
    "analysis notebooks, no %%writefile / no farm-route reselect after 216). Do not reupload boatlee 55710781. Cut 12/13 Hold."
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
    "experiments/20260914j_top10_games.json",
]
HUNT = [
    {
        "kernel": "sorcererbi/your-offline-arena-is-lying-to-you",
        "path": "artifacts/public_sources/_hunt_20260914k/sorcererbi__your-offline-arena-is-lying-to-you/your-offline-arena-is-lying-to-you.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": "1fe769ac17c5ba28fbc8427195d3d01c181862ecd2fa43be9a87f3ba5af5ab00",
        "note": (
            "New slug vs _hunt_20260914j (lastRunTime 2026-09-14 10:53:08.673000; public-search newest by dateCreated). "
            "12-cell analysis notebook, no %%writefile, no main.py/submission.py payload. Toy replay_opponent / survival_gate plots. "
            "No farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "sorcererbi/where-does-your-score-actually-come-from",
        "path": "artifacts/public_sources/_hunt_20260914k/sorcererbi__where-does-your-score-actually-come-from/where-does-your-score-actually-come-from.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": "80c704754cfc7270b261194aeedc6a8187827f85aef34fb518f3d7770411552a",
        "note": (
            "New slug vs _hunt_20260914j (lastRunTime 2026-09-14 10:53:01.063000). 19-cell analysis notebook, no %%writefile. "
            "Elo crossing / ramp / noise-floor commentary plus a my_rating_curve helper that is not an agent. "
            "No farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "sorcererbi/how-to-a-b-two-agents-properly",
        "path": "artifacts/public_sources/_hunt_20260914k/sorcererbi__how-to-a-b-two-agents-properly/how-to-a-b-two-agents-properly.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": "dd2aeb9752f38ec9b7315208981d10f72dc495d67014ea8cce9ca04d7daa20ff",
        "note": (
            "New slug vs _hunt_20260914j (lastRunTime 2026-09-14 10:52:53.813000). 12-cell analysis notebook, no %%writefile. "
            "Toy A/B harness (run_panel / ab_test) with numpy RNG, not a Kaggriculture agent. "
            "No farm/route reselect after 216. No ctypes/agent.so. Cells not executed. Not copied to candidates/; not clone/G5."
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
        "packet": "20260914k",
        "kernels_not_in_0914j_packet": True,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260914k",
        "inspect_scripts": [
            "experiments/candidates/scan_hunt_20260914k.py",
            "experiments/candidates/inspect_hunt_20260914k.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_analysis_notebook_no_writefile",
        "compare_0914j": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260914j",
            "hunt_report": "experiments/20260914j_hunt_report.json",
            "gate": "experiments/20260914j_gate.json",
            "note": (
                "3 new slugs vs _hunt_20260914j. Public search newest is now "
                "sorcererbi/your-offline-arena-is-lying-to-you (lastRunTime 2026-09-14 10:53:08.673000). "
                "Did not re-pull rejected kernels (arsgorynich v40-challenger SHA 546c4224, xuantianfengwu r10 SHA 3b8a1d4d, "
                "aurax7 v5 SHA ea4c28e6, lime0001 t23 SHA 31ee22dc, nathanjacob V40 autopsy dataset wrapper, Ahmed V41 SHA 8951ff93, "
                "prvsiyan reserve-garden, alperen scored-agent SHA 85c8b532, xuantianfengwu adaptive-land-allocator SHA d12f2987, "
                "renjistarfall V39 reprint, alperen metacounter-r1 analysis, xuantianfengwu land-labor-capital, Ahmed V40 SHA 546c4224, "
                "guru V39, yhay81 0913, wei v46d review, Ahmed V39, aurax7 v4, crystalbaby V38, prvsiyan market-ledger, timed-six-cow, "
                "lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, "
                "melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
            ),
        },
        "public_search_newest": "sorcererbi/your-offline-arena-is-lying-to-you",
        "public_search_newest_lastRunTime": "2026-09-14 10:53:08.673000",
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
    dump("20260914k_hunt_report.json", hunt)

    gate = json.loads((ROOT / "experiments/20260914j_gate.json").read_text(encoding="utf-8"))
    gate["packet"] = "20260914k"
    gate["named_kernels_scanned"] = [row["kernel"] for row in HUNT]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260914k"
    gate["hunt_report"] = "experiments/20260914k_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1619.1
    gate["live"]["shopbag"]["score_complete"] = 1295.7
    new_rejected = [
        {
            "kernel": row["kernel"],
            "verdict": row["verdict"],
            "note": row["note"],
        }
        for row in HUNT
    ]
    old_rejected = [
        row for row in gate["rejected"] if row.get("kernel") not in {h["kernel"] for h in HUNT}
    ]
    gate["rejected"] = new_rejected + old_rejected
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1619.1 partnered with newer shopbag 56151155 COMPLETE 1295.7 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "3 new public slugs vs _hunt_20260914j, none licensed: sorcererbi analysis notebooks (no %%writefile, no later-block). "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
        "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: \u0412\u0430\u0440\u0438\u043c extra sheep 218/242/266 already bought identical-clone 11s -12131; "
        "LaiCxm extra cow 218 extra sheep 227 extra geese 242/266 -16092; "
        "Pietro extra sheep 218/227/242/266 -12549; "
        "Revanth extra sheep 218/242/266 already bought -11033; "
        "zard599/Surya already bought extra geese 227/242 and won +748/+1729."
    )
    dump("20260914k_gate.json", gate)

    algo = json.loads((ROOT / "experiments/20260914j_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-14"
    algo["packet"] = "20260914k"
    algo["live"]["cut16"]["csv_0914k_team_score"] = 1619.1
    algo["live"]["shopbag"]["score_complete"] = 1295.7
    algo["live"]["rank_csv_0914k"] = 2158
    algo["cut16_live_failure_class"]["0914k"] = {
        "file": "experiments/20260914k_cut16_rolling.json",
        "ids": ROLLING_IDS,
        "wtl": [2, 0, 10],
        "mean_margin": -6609.2,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-sheep plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 108851261,
                "opp": "LaiCxm",
                "margin": -16092,
                "shops72": ["PIZZA_SHOP"],
                "buy": "9c5s vs 9c5s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 108658948,
                "opp": "Pietro Valocchi",
                "margin": -12549,
                "shops72": ["FARMERS_MARKET"],
                "buy": "7c6s vs 8c9s",
                "clone": 1,
            },
            {
                "id": 108889446,
                "opp": "\u0412\u0430\u0440\u0438\u043c \u0441\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0441\u0430\u043c\u043e\u0433\u043e\u043d",
                "margin": -12131,
                "shops72": ["YARN_STORE"],
                "buy": "6c11s vs 6c11s",
                "clone": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "3 new public slugs vs _hunt_20260914j are sorcererbi analysis notebooks (no writefile). "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump("20260914k_algo_note.json", algo)

    dump(
        "20260914k_episode_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914k",
            "utc": "2026-09-14T11:41:49Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1619.1,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1619.1 (was 1627.8). Newest public 108889446. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1295.7 / ListEpisodes last_updated 1295.752) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1295.7 < 1500 "
                "and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1295.7,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2158,
            "heralces_score": 1619.1,
            "n_teams_csv": 9000,
            "public_56151152": {
                "n_public": 263,
                "n_validation": 1,
                "n_completed_public": 263,
                "wtl": [110, 2, 151],
                "mean_margin": -1692.4,
                "status": "COMPLETE",
                "publicScore": 1619.1,
            },
            "rolling_ids": ROLLING_IDS,
            "rolling_forbidden_0914j": PREV_14J,
            "ids_not_identical_to_0914j": True,
            "ids_disjoint_from_0914j": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [2, 0, 10],
            "mean_margin": -6609.2,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids disjoint from 20260914j packet, all 720 DONE/DONE. 2W 10L. "
                "Worst LaiCxm 108851261 L -16092 9c5s vs 9c5s3g clone=1 extra cow 218 extra sheep 227 extra geese 242/266. "
                "New-window \u0412\u0430\u0440\u0438\u043c 108889446 identical-clone extra-sheep 6c11s vs 6c11s -12131; "
                "Adhiraj 108889378 extra-sheep 6c11s vs 9c9s -2087. "
                "Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        "20260914k_cut16_loss_class.json",
        {
            "date": "2026-09-14",
            "packet": "20260914k",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": ROLLING_IDS,
            "ids_0914j": PREV_14J,
            "disjoint_from_0914j": True,
            "all_720_done_done": True,
            "wtl": [2, 0, 10],
            "mean_margin": -6609.2,
            "clone_n": 12,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 22.0],
            "wool_360": {
                108889446: 236,
                108889378: 237,
                108851261: 1,
                108822458: 231,
                108817790: 1,
                108787437: 1,
                108762693: 223,
                108723413: 43,
                108704919: 174,
                108686716: 183,
                108669139: 43,
                108658948: 1,
            },
            "wool_432": {
                108889446: 237,
                108889378: 230,
                108851261: 1,
                108822458: 137,
                108817790: 5,
                108787437: 1,
                108762693: 200,
                108723413: 1,
                108704919: 161,
                108686716: 189,
                108669139: 1,
                108658948: 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-14b/09-14c/09-14d/09-14e/09-14f/09-14g/09-14h/09-14i/09-14j: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-sheep plus identical-clone extra-goose. "
                "WTL 2-0-10 mean -6609.2 vs 09-14j 5-0-7 mean -3097.2. New window game \u0412\u0430\u0440\u0438\u043c 108889446 -12131. clone=12/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 108851261,
                    "opp": "LaiCxm",
                    "margin": -16092.0,
                    "herd_us": "9c5s",
                    "herd_opp": "9c5s3g",
                    "shops": ["PIZZA_SHOP"],
                }
            ],
        },
    )

    dump(
        "20260914k_study_packet.json",
        {
            "title": "Kaggriculture study packet 2026-09-14k",
            "not_the_0914j_packet": True,
            "no_upload": NO_UPLOAD,
            "upload_bail": True,
            "upload_bail_reasons": {
                "a_newest_cut_pending": False,
                "b_newest_cut_complete_below_1500": False,
                "c_drop_ge1500_without_ge1500_partner": True,
            },
            "sources": {
                "leaderboard_zip": "artifacts/kaggle_runs/lb_20260914k/kaggriculture.zip",
                "leaderboard_csv": "artifacts/kaggle_runs/lb_20260914k/kaggriculture-publicleaderboard-2026-09-14T11-41-49.csv",
                "leaderboard_api": "experiments/20260914k_public_leaderboard_api.json",
                "episodes_cut16": "experiments/episodes_56151152.json",
                "cut16_replays": "artifacts/kaggle_runs/cut16_20260914k",
                "top_replays": "artifacts/kaggle_runs/top_20260914k",
                "hunt_dir": "artifacts/public_sources/_hunt_20260914k",
                "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
                "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
                "gate": "experiments/20260914k_gate.json",
                "episode_report": "experiments/20260914k_episode_report.json",
                "hunt_report": "experiments/20260914k_hunt_report.json",
                "algo_note": "experiments/20260914k_algo_note.json",
                "loss_class": "experiments/20260914k_cut16_loss_class.json",
            },
            "live": {
                "sixday": 56028043,
                "sixday_score": 1590.8,
                "sixday_status": "COMPLETE",
                "team_score": 1619.1,
                "rank": 2158,
                "n_teams": 9000,
                "shopbag_previous": 56112309,
                "shopbag_reupload": 56151155,
                "shopbag_status": "COMPLETE",
                "shopbag_score": 1295.7,
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
                "cut16_score": 1619.1,
                "root_main_py": "h2 65e6f5cd... unchanged",
                "gold21": 2931.0,
                "rank10": {"team": "Thomas Tschinkel", "score": 2974.5},
                "rank1": {
                    "team": "Majkel1337",
                    "score": 3217.8,
                    "submissionId": 56156662,
                },
                "public_cut16": {
                    "n": 263,
                    "wtl": [110, 2, 151],
                    "mean_margin": -1692.4,
                },
            },
            "rolling": {
                "previous": "experiments/20260914j_cut16_rolling.json",
                "live_cut16": "experiments/20260914k_cut16_rolling.json",
                "ids": ROLLING_IDS,
                "ids_not_identical_to_0914j": True,
                "n": 12,
                "wtl": [2, 0, 10],
                "mean_margin": -6609.2,
                "loss_class": LOSS_CLASS,
            },
            "excluding": {
                "id": 108889446,
                "margin": -12131.0,
                "clone": True,
                "Q": [3, 3],
                "land": [151, 266],
                "herd_us": "6c11s",
                "herd_opp": "6c11s",
                "sheep_steps_us": [2, 151, 196, 218, 242, 266],
            },
            "top_board": {
                "source": "experiments/20260914k_top10_games.json",
                "not_copied_from": NOT_COPIED,
                "Majkel1337": {
                    "land": [
                        [150, 218, 220, 222],
                        [150, 220],
                        [150, 220, 222],
                        [150, 218, 220, 222],
                    ],
                    "herd": ["7c3s4g", "7c9s2g", "6c16s0g", "6c3s4g"],
                    "wheat": [449, 472, 420, 356],
                    "shops": ["BRUNCH_SPOT", "ICE_CREAM_SHOP", "YARN_STORE", "BRUNCH_SPOT"],
                    "clone": "0_of_4",
                    "episodes": [108890595, 108884658, 108694094, 108689966],
                    "note": (
                        "CSV #1 3217.8 live 3217.8 scoring sub 56156662 (current sub 56216119 is 3029.6). "
                        "Ids disjoint from 20260914j Majkel set. Mid-land 150 then 218-222 "
                        "(two 150/218/220/222; one 150/220; one 150/220/222), "
                        "wheat 356-472, clone=0 on 4/4, goose mix 4g/2g/0g/4g. Opening land is not a later-block license."
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
                "score": 1619.1,
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
                    "Already live COMPLETE 1619.1. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                    "Rolling 108851261 extra cow 218 extra sheep 227 extra geese 242/266 and lost 9c5s vs 9c5s3g -16092; "
                    "108889446 extra sheep 218/242/266 already bought and lost identical-clone 6c11s -12131; "
                    "108658948 extra cow 218 vs opp extra sheep 218/227/242/266 and lost 7c6s vs 8c9s -12549. "
                    "New-window \u0412\u0430\u0440\u0438\u043c 108889446 identical-clone extra-sheep; Adhiraj 108889378 extra-sheep vs 9c9s. Not cut 12/13."
                ),
            },
            "cut17": {
                "hold": True,
                "uploaded": None,
                "why": (
                    "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 3 new slugs vs 0914j, none licensed "
                    "(sorcererbi analysis notebooks, no %%writefile); "
                    "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                    "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1619.1 and keeps 1295.7."
                ),
            },
            "hunt": hunt["hunt"],
        },
    )


if __name__ == "__main__":
    main()
