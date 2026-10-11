"""Write 20260915b packet JSON from live measurements. No upload."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV_15 = [
    109142116,
    109135062,
    109111080,
    109091091,
    109078755,
    109057555,
    109054323,
    109044160,
    109042689,
    109030720,
    109029822,
    109024708,
]
IDS = [
    109274859,
    109251218,
    109247247,
    109241224,
    109227483,
    109208871,
    109205772,
    109205359,
    109184094,
    109178619,
    109169017,
    109168637,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (ManasviSharma 109251218 7c6s vs 8c6s3g FARMERS_MARKET extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -18715; "
    "Huy Le Ngoc Gia 109178619 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -13645; "
    "Ashraf 1232 109227483 9c5s vs 8c6s3g ICE_CREAM extra sheep 314 vs opp extra sheep 218/227 extra geese 242/266 -13342; "
    "Sergei Fironov 109247247 10c8s vs 8c12s3g SMOOTHIE extra cow 218 extra sheep 227/242/266 already bought vs opp extra sheep 218/227 extra geese 242/266 extra sheep 290 -13194) "
    "+ extra-goose (AimeeChen1 109205359 9c5s3g vs 9c5s4g PET_CAFE extra geese 227/242 already bought vs opp extra geese 218/227/242 extra sheep 266 -2466) "
    "+ identical-clone extra-goose (3G 109168637 9c5s3g vs 9c5s3g ICE_CREAM extra geese 227/242 already bought -10063) "
    "+ extra-sheep (Grim Reaper 109169017 6c11s vs 3c13s2g YARN extra sheep 218/242/266 already bought vs extra sheep 218/227/242/265 -10132; "
    "Rifa Tamanna 109208871 9c8s vs 7c11s BAKERY extra sheep 227/242/266 already bought vs extra sheep 218/227/242/266 -3251). "
    "Wins: tetsuya 109241224 9c5s3g vs 6c5s BAKERY +18920 extra geese 227/242 already bought clone=0; "
    "Stephen Schott 109184094 4c15s vs 8c6s3g ICE_CREAM +13159 extra sheep 218/242/266 already bought; "
    "Jorrawar Grewal 109205772 9c5s3g vs 6c11s PIZZA +6116 extra geese 227/242 already bought vs extra sheep 227/242/266; "
    "Baha Enes Oren 109274859 9c5s3g vs 9c5s3g ICE_CREAM +114 extra geese 227/242 already bought identical-clone. "
    "clone=11/12, Q=3/3 (two 3/4 losses), BUY_LAND 151/266 succeeded, cash_24 3-29. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Sergei already bought extra sheep 227/242/266 and lost vs 8c12s3g; "
    "Grim Reaper already bought extra sheep 218/242/266 and lost 11s vs 13s2g; "
    "Ashraf extra sheep 314 lost vs 8c6s3g; Rifa already bought extra sheep 227/242/266 and lost 8s vs 11s; "
    "3G already bought extra geese 227/242 identical-clone and lost; Aimee already bought extra geese 227/242 and lost vs 4g; "
    "Manasvi/Huy extra cow 218 lost vs 8c6s3g; Baha/Jorrawar already bought extra geese 227/242 and won; "
    "Stephen already bought extra sheep 218/242/266 and won vs 8c6s3g; tetsuya already bought extra geese 227/242 clone=0 and won."
)
HUNT_ROWS = [
    {
        "kernel": "anandkumar369o/kagg-team-decisions",
        "path": "artifacts/public_sources/_hunt_20260915b/anandkumar369o__kagg-team-decisions/kagg-team-decisions.py",
        "verdict": "reject_analysis_script_no_agent",
        "sha256": "595d29fe7b1ddbfaf066fe973c0269d8df088f5915f16b4a86c143a97b6eb635",
        "note": (
            "New slug vs _hunt_20260915 (lastRunTime 2026-09-15 08:55:04.753000; public-search newest by dateCreated). "
            "Python analysis of top-500 team turn decisions (parquet/CSV aggregates). SHA 595d29fe... "
            "No %%writefile agent, no farm/route reselect after 216, no ctypes/agent.so. Cells not executed. "
            "File hashed in hunt dir only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "nathanjacob/beyond-v43-what-the-top-clusters-do-on-turn-1",
        "path": "artifacts/public_sources/_hunt_20260915b/nathanjacob__beyond-v43-what-the-top-clusters-do-on-turn-1/beyond-v43-what-the-top-clusters-do-on-turn-1.ipynb",
        "verdict": "reject_v43_c9_opening_shop0909_overlay",
        "sha256": "7a37397fdb29cbbb17aaf7577352bef910fb4dd0f19bf763b9dcaff68595da54",
        "note": (
            "New slug vs _hunt_20260915 (lastRunTime 2026-09-15 07:12:17.730000). B85/gzip static reconstruct SHA 7a37397f... "
            "pipe-4 = Ahmed V43 Shop0909 chassis plus C9 turn-1 opening. Distinct from V43 SHA 919fc1d6, V42 728fdfb4, "
            "pipe-2 SHA 728fdfb4, and live cuts 14/15/16. Day-6 144/648 plus _R37_HORIZONS from 288 plus 712 terminal planner. "
            "216<=step<=227 is milk-shop livestock sub; C9 opening is step 0/24/25, not a farm/route reselect after 216. "
            "No ctypes/agent.so. Cells not executed. Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "kenanzhang9/notebook6cc8bf1c92",
        "path": "artifacts/public_sources/_hunt_20260915b/kenanzhang9__notebook6cc8bf1c92/notebook6cc8bf1c92.ipynb",
        "verdict": "reject_shop0909_144_648_and_712_overlay",
        "sha256": "602ae8be5b1e0d0c7483837c2e305dbf5d3aa41b6fe02c4efb3d1ca753820388",
        "note": (
            "New slug vs _hunt_20260915 (lastRunTime 2026-09-15 03:50:34.430000). Python %%writefile /kaggle/working/main.py SHA 602ae8be... "
            "V37-A3.1 Shop0909 overlay; distinct from Ahmed V43 SHA 919fc1d6, V42 728fdfb4, crystalbaby V37/V38, and live cuts 14/15/16. "
            "Notebook embeds cut15 SHA b87a27ed as comment/payload. Day-6 144/648 plus 288 sale overlay (_R37_HORIZONS 4/5 from 288) "
            "plus step==712 terminal planner. 216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. "
            "No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
]
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1588.3 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1286.1 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1588.3; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 3 new slugs vs _hunt_20260915 "
    "(public search newest anandkumar369o/kagg-team-decisions lastRunTime 2026-09-15 08:55:04.753000 analysis script SHA 595d29fe; "
    "nathanjacob pipe-4 SHA 7a37397f V43+C9 opening Shop0909 overlay; kenanzhang9 SHA 602ae8be Shop0909 144/648+288+712 overlay; "
    "none farm-route reselect after 216). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260915b_cut16_rolling.json").read_text(encoding="utf-8"))
    games = rolling["games"]
    assert [g["id"] for g in games] == IDS
    first = games[0]
    hunt_row = HUNT_ROWS[0]
    prior_top = [
        f"experiments/202609{d}_top10_games.json"
        for d in (
            "04",
            "05",
            "06",
            "09",
            "10",
            "11",
            "11b",
            "12",
            "12b",
            "12c",
            "12d",
            "12e",
            "13",
            "13b",
            "13c",
            "13d",
            "13e",
            "13f",
            "13g",
            "13h",
            "13i",
            "13j",
            "13k",
            "13l",
            "13m",
            "13n",
            "13o",
            "13p",
            "13q",
            "13r",
            "13s",
            "13t",
            "13u",
            "13v",
            "14",
            "14b",
            "14c",
            "14d",
            "14e",
            "14f",
            "14g",
            "14h",
            "14i",
            "14j",
            "14k",
            "14l",
            "14m",
            "14n",
            "14o",
            "15",
        )
    ]
    packet = {
        "title": "Kaggriculture study packet 2026-09-15b",
        "not_the_0915_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260915b/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260915b/kaggriculture-publicleaderboard-2026-09-15T13-02-08.csv",
            "leaderboard_api": "experiments/20260915b_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260915b",
            "top_replays": "artifacts/kaggle_runs/top_20260915b",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915b",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260915b_gate.json",
            "episode_report": "experiments/20260915b_episode_report.json",
            "hunt_report": "experiments/20260915b_hunt_report.json",
            "algo_note": "experiments/20260915b_algo_note.json",
            "loss_class": "experiments/20260915b_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1588.3,
            "rank": 2272,
            "n_teams": 9121,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1286.1,
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
            "cut16_score": 1588.3,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2954.7,
            "rank10": {"team": "Mengfei Li", "score": 2989.6},
            "rank1": {"team": "Majkel1337", "score": 3148.5, "submissionId": 56156662},
            "public_cut16": {"n": 300, "wtl": [124, 2, 174], "mean_margin": -1989.7},
        },
        "rolling": {
            "previous": "experiments/20260915_cut16_rolling.json",
            "live_cut16": "experiments/20260915b_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0915": True,
            "n": 12,
            "wtl": [4, 0, 8],
            "mean_margin": -3874.9,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": first["id"],
            "margin": first["margin"],
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "9c5s3g",
            "herd_opp": "9c5s3g",
            "sheep_steps_us": [row["step"] for row in first["sheep_steps_us"]],
        },
        "top_board": {
            "source": "experiments/20260915b_top10_games.json",
            "not_copied_from": prior_top,
            "Majkel1337": {
                "land": [
                    [150, 220, 222],
                    [150, 218, 220, 222],
                    [150, 220, 222],
                    [150, 218, 220, 222],
                ],
                "herd": ["11c3s2g", "9c3s4g", "11c3s2g", "6c7s4g"],
                "wheat": [476, 511, 472, 610],
                "shops": ["ICE_CREAM_SHOP", "BAKERY", "SMOOTHIE_SHOP", "BAKERY"],
                "clone": "0_of_4",
                "episodes": [109290715, 109290020, 109284452, 109278362],
                "note": (
                    "CSV #1 3148.5 live 3148.5 scoring sub 56156662 (current sub 56216119 is 3137.7). "
                    "Ids disjoint from 20260915 Majkel set. Mid-land 150 then 218-222 "
                    "(two 150/218/220/222 plus two 150/220/222), wheat 472-610, clone=0 on 4/4, "
                    "goose mix 2g/4g/2g/4g. Opening land is not a later-block license."
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
            "score": 1588.3,
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
                "Already live COMPLETE 1588.3. This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                "Extra sheep 226/241/265 not 227/242/266. Rolling 109251218 extra-animal 8c6s3g 7c6s vs 8c6s3g -18715; "
                "109168637 identical-clone extra-goose 9c5s3g -10063; "
                "109227483 extra-animal extra sheep 314 9c5s vs 8c6s3g -13342. New-window Baha 109274859 extra-goose +114. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 3 new slugs vs 0915, "
                "none licensed (public-search newest anandkumar369o/kagg-team-decisions analysis SHA 595d29fe; "
                "nathanjacob pipe-4 SHA 7a37397f V43+C9 opening Shop0909 overlay; kenanzhang9 SHA 602ae8be Shop0909 144/648+288+712 overlay). "
                "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. "
                "Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1588.3 and keeps 1286.1."
            ),
        },
        "hunt": HUNT_ROWS,
    }
    dump(ROOT / "experiments/20260915b_study_packet.json", packet)

    dump(
        ROOT / "experiments/20260915b_episode_report.json",
        {
            "date": "2026-09-15",
            "packet": "20260915b",
            "utc": "2026-09-15T13:02:08Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1588.3,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1588.3 (was 1606.1). Newest public 109274859. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1286.1 / ListEpisodes last_updated 1286.118) + cut 16 56151152. "
                "Upload-bail TRUE (c): shopbag partner 1286.1 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1286.1,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2272,
            "heralces_score": 1588.3,
            "n_teams_csv": 9121,
            "public_56151152": {
                "n_public": 300,
                "n_validation": 1,
                "n_completed_public": 300,
                "wtl": [124, 2, 174],
                "mean_margin": -1989.7,
                "status": "COMPLETE",
                "publicScore": 1588.3,
            },
            "rolling_ids": IDS,
            "rolling_forbidden_0915": PREV_15,
            "ids_not_identical_to_0915": True,
            "ids_disjoint_from_0915": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [4, 0, 8],
            "mean_margin": -3874.9,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids disjoint from 20260915 packet, all 720 DONE/DONE. 4W 8L. "
                "Worst ManasviSharma 109251218 L -18715 7c6s vs 8c6s3g clone=1 extra-animal opp extra sheep 218/227 extra geese 242/266. "
                "New-window Baha Enes Oren 109274859 extra-goose +114. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        ROOT / "experiments/20260915b_hunt_report.json",
        {
            "date": "2026-09-15",
            "packet": "20260915b",
            "kernels_not_in_0915_packet": True,
            "no_upload": True,
            "no_kaggle_submit": True,
            "cells_executed": False,
            "extracted_later_block_agent": False,
            "later_block_python_after_216": False,
            "any_licensed_for_extract": False,
            "licensed_kernel": None,
            "root_main_py": "unchanged",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915b",
            "inspect_scripts": [
                "experiments/candidates/scan_hunt_20260915b.py",
                "experiments/candidates/inspect_hunt_20260915b.py",
                "experiments/candidates/_inspect_hunt_payloads_20260915b.py",
                "experiments/candidates/_extract_pipe4_20260915b.py",
            ],
            "python": "D:\\kaggle\\kaggriculture\\.venv\\Scripts\\python.exe",
            "payload_decode": "writefile_static_hash_only",
            "compare_0915": {
                "hunt_dir": "artifacts/public_sources/_hunt_20260915",
                "hunt_report": "experiments/20260915_hunt_report.json",
                "gate": "experiments/20260915_gate.json",
                "note": (
                    "3 new slugs vs _hunt_20260915. Public search newest is now "
                    "anandkumar369o/kagg-team-decisions (lastRunTime 2026-09-15 08:55:04.753000). "
                    "Did not re-pull rejected kernels (xuantianfengwu terminal-logistics SHA 364ca885, "
                    "taylorclark637 sovereign-swarm SHA ffc0e6e2, ahmedberatozer v43 SHA 919fc1d6, "
                    "prvsiyan field-clock, alperen adaptive-route SHA 77cf6772, destbreso telemetry, "
                    "alperen harvestforge SHA 01f0cd47, nathanjacob clustering, hosen42 validation, "
                    "nathanjacob pipe-2 SHA 728fdfb4, leoprovorov god-s-mode, sunil v6 SHA 8951ff93, "
                    "xuantianfengwu hour-4 SHA dc07c7a9, guruprasaathas111 fully-dynamic SHA f4e3935c, "
                    "rohitt94 SHA 62a80706, xuantianfengwu r10 SHA 3b8a1d4d, aurax7 v5, lime0001 t23, "
                    "Ahmed V41 SHA 8951ff93, yhay81 0913, y3uanm rollback-v20)."
                ),
            },
            "public_search_newest": "anandkumar369o/kagg-team-decisions",
            "public_search_newest_lastRunTime": "2026-09-15 08:55:04.753000",
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
            "named_kernels_scanned": [row["kernel"] for row in HUNT_ROWS],
            "author_list_no_new_later_block": [
                "yhay81/shop-router-0913",
                "yamakawanin/king-v4e-rc4",
                "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
                "y3uanm/kaggriculture-conservative-market-router-v5",
                "y3uanm/kaggriculture-safe-baseline-rollback-v20",
            ],
            "author_list_note": "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6.",
            "hunt": HUNT_ROWS,
        },
    )

    old_gate = json.loads((ROOT / "experiments/20260915_gate.json").read_text(encoding="utf-8"))
    gate = deepcopy(old_gate)
    gate["date"] = "2026-09-15"
    gate["packet"] = "20260915b"
    gate["named_kernels_scanned"] = [row["kernel"] for row in HUNT_ROWS]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260915b"
    gate["hunt_report"] = "experiments/20260915b_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1588.3
    gate["live"]["shopbag"]["score_complete"] = 1286.1
    gate["rejected"] = [
        {"kernel": row["kernel"], "verdict": row["verdict"], "note": row["note"]} for row in HUNT_ROWS
    ] + old_gate["rejected"]
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1588.3 partnered with newer shopbag 56151155 COMPLETE 1286.1 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "3 new public slugs vs _hunt_20260915, none licensed: public-search newest anandkumar369o/kagg-team-decisions "
        "(analysis SHA 595d29fe); nathanjacob pipe-4 SHA 7a37397f V43+C9 opening Shop0909 overlay; kenanzhang9 SHA 602ae8be Shop0909 overlay. "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. "
        "Cut 12/13 stay Hold. Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: Sergei extra sheep 227/242/266 already bought vs 8c12s3g -13194; "
        "Grim Reaper extra sheep 218/242/266 already bought 11s vs 13s2g -10132; "
        "Ashraf extra-animal 8c6s3g extra sheep 314 -13342; 3G identical-clone extra-goose -10063."
    )
    dump(ROOT / "experiments/20260915b_gate.json", gate)

    dump(
        ROOT / "experiments/20260915b_cut16_loss_class.json",
        {
            "date": "2026-09-15",
            "packet": "20260915b",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": IDS,
            "ids_0915": PREV_15,
            "disjoint_from_0915": True,
            "all_720_done_done": True,
            "wtl": [4, 0, 8],
            "mean_margin": -3874.9,
            "clone_n": 11,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 29.0],
            "wool_360": {
                "109274859": 183,
                "109251218": 1,
                "109247247": 234,
                "109241224": 43,
                "109227483": 1,
                "109208871": 234,
                "109205772": 18,
                "109205359": 43,
                "109184094": 243,
                "109178619": 1,
                "109169017": 236,
                "109168637": 43,
            },
            "wool_432": {
                "109274859": 189,
                "109251218": 5,
                "109247247": 237,
                "109241224": 1,
                "109227483": 1,
                "109208871": 200,
                "109205772": 1,
                "109205359": 1,
                "109184094": 244,
                "109178619": 5,
                "109169017": 212,
                "109168637": 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-15: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-goose. "
                "WTL 4-0-8 mean -3874.9 vs 09-15 5-0-7 mean -7862.6. New window game Baha Enes Oren 109274859 +114. clone=11/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 109251218,
                    "opp": "ManasviSharma",
                    "margin": -18715.0,
                    "herd_us": "7c6s",
                    "herd_opp": "8c6s3g",
                    "shops": ["FARMERS_MARKET"],
                }
            ],
        },
    )

    algo = json.loads((ROOT / "experiments/20260915_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-15"
    algo["packet"] = "20260915b"
    algo["live"]["cut16"]["csv_0915b_team_score"] = 1588.3
    algo["live"]["shopbag"]["score_complete"] = 1286.1
    algo["live"]["rank_csv_0915b"] = 2272
    algo["cut16_live_failure_class"]["0915b"] = {
        "file": "experiments/20260915b_cut16_rolling.json",
        "ids": IDS,
        "wtl": [4, 0, 8],
        "mean_margin": -3874.9,
        "clone": "11/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 109251218,
                "opp": "ManasviSharma",
                "margin": -18715,
                "shops72": ["FARMERS_MARKET"],
                "buy": "7c6s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 109178619,
                "opp": "Huy Le Ngoc Gia",
                "margin": -13645,
                "shops72": ["BRUNCH_SPOT"],
                "buy": "7c6s vs 8c6s3g",
                "clone": 1,
            },
            {
                "id": 109227483,
                "opp": "Ashraf 1232",
                "margin": -13342,
                "shops72": ["ICE_CREAM_SHOP"],
                "buy": "9c5s vs 8c6s3g",
                "clone": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "3 new public slugs vs _hunt_20260915; public-search newest is anandkumar369o analysis (SHA 595d29fe). "
            "nathanjacob pipe-4 SHA 7a37397f is V43+C9 opening Shop0909 overlay; kenanzhang9 SHA 602ae8be is Shop0909 144/648+288+712. "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump(ROOT / "experiments/20260915b_algo_note.json", algo)
    print("hunt0", hunt_row["kernel"])


if __name__ == "__main__":
    main()
