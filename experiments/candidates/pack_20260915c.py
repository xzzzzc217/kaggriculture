"""Write 20260915c packet JSON from live measurements. No upload."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV_15B = [
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
IDS = [
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
    "mixed extra-animal 8c6s3g (Filip Strzalka 109159847 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -6855; "
    "Quillbolt 109054323 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -12417) "
    "+ extra-cow vs extra-goose (Gaddam Shiva Teja 109297997 9c5s3g vs 11c5s ICE_CREAM extra geese 227/242 already bought vs extra cow -26009; "
    "Harshith revuru 109044160 7c6s vs 6c6s5g BRUNCH extra cow 218 vs opp extra geese 227/242 extra sheep 266 -15134) "
    "+ identical-clone extra-goose (Liyi xin jie 109057555 9c5s3g vs 9c5s3g PET_CAFE extra geese 227/242 already bought -23988) "
    "+ extra-sheep (Dhruv #2 109149160 4c15s vs 6c10s BRUNCH extra sheep 218/242/266 already bought vs extra sheep 218/252/253/265 -12590; "
    "SatoshiN04 109091091 4c14s vs 2c12s2g PET_CAFE extra sheep 218/242/266 already bought clone=0 -12300). "
    "Wins: Suliman Tadros 109152510 4c15s vs 9c3s PET_CAFE +43169 extra sheep 218/242/266 clone=0; "
    "alexbstl 109078755 6c11s vs 11c8s6g YARN +8823 extra sheep 218/242/266 already bought; "
    "Yichi 109111080 9c8s vs 9c5s3g BRUNCH +6951 extra sheep 227/242/266 already bought; "
    "Duc-Anh Nguyen 109135062 9c5s3g vs 9c5s4g PIZZA +2713 extra geese 227/242 already bought vs 4g; "
    "ocean240812 109142116 9c8s vs 6c6s6g BAKERY +74 extra sheep 227/242/266 already bought. "
    "clone=10/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 0-22. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Gaddam already bought extra geese 227/242 and lost vs 11c; "
    "Liyi already bought extra geese 227/242 identical-clone and lost; "
    "Dhruv/Satoshi already bought extra sheep 218/242/266 and lost; "
    "Filip/Quillbolt extra cow 218 lost vs 8c6s3g; Harshith extra cow 218 lost vs 6c6s5g; "
    "Suliman already bought extra sheep 218/242/266 clone=0 and won; "
    "alexbstl/Yichi/ocean already bought extra sheep 218-266 and won; Duc-Anh already bought extra geese 227/242 and won."
)
HUNT_ROWS = [
    {
        "kernel": "alperen5252525/turn-one-market-advantage-kaggriculture",
        "path": "artifacts/public_sources/_hunt_20260915c/alperen5252525__turn-one-market-advantage-kaggriculture/turn-one-market-advantage-kaggriculture.ipynb",
        "verdict": "reject_v43_c9_opening_shop0909_overlay_reprint",
        "sha256": "7a37397fdb29cbbb17aaf7577352bef910fb4dd0f19bf763b9dcaff68595da54",
        "note": (
            "New slug vs _hunt_20260915b (lastRunTime 2026-09-15 13:24:02.117000; public-search newest by dateCreated). "
            "Exact reprint of already-rejected nathanjacob pipe-4. B85/gzip static reconstruct SHA 7a37397f... "
            "pipe-4 = Ahmed V43 Shop0909 chassis plus C9 turn-1 opening. Day-6 144/648 plus _R37_HORIZONS from 288 plus 712 terminal planner. "
            "216<=step<=227 is milk-shop livestock sub; C9 opening is step 0/24/25, not a farm/route reselect after 216. "
            "No ctypes/agent.so. Cells not executed. Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "alperen5252525/public-state-market-control-kaggriculture",
        "path": "artifacts/public_sources/_hunt_20260915c/alperen5252525__public-state-market-control-kaggriculture/public-state-market-control-kaggriculture.ipynb",
        "verdict": "reject_v58_day6_shop_prefix_plus_clone_latch_360",
        "sha256": "b041058ec187a8d0a01edc0eab8de068b53deca3e6c1973faf74ace6916ddcb9",
        "note": (
            "New slug vs _hunt_20260915b (lastRunTime 2026-09-15 13:16:12.917000). "
            "b85/gzip static reconstruct SHA b041058e... Distinct from live cuts 14/15/16 and alperen harvestforge SHA 01f0cd47 / 0913 reprint 77cf6772. "
            "v58 compiled tape library. Mode selected at step 72; second-shop branches at step>=144 (SMOOTHIE/YARN/PET). "
            "Yarn first-shop clone latch at step==360 if mirror_streak>=240, then clone tape. Not a farm/route reselect after 216. "
            "Not day-6 144/648 later-block license. No ROUTE_STEP/PROGRAM/sale_horizon/ADVANCE_START. No ctypes/agent.so. "
            "Cells not executed. Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "alperen5252525/market-momentum-farming-kaggriculture",
        "path": "artifacts/public_sources/_hunt_20260915c/alperen5252525__market-momentum-farming-kaggriculture/market-momentum-farming-kaggriculture.ipynb",
        "verdict": "reject_frozen_shop_prefix_tape_portfolio_no_later_block",
        "sha256": "5fd73afd3c5337e391958a0621e40c84d6c47e4050ff82f42c78b4a1c239193e",
        "note": (
            "New slug vs _hunt_20260915b (lastRunTime 2026-09-15 13:11:44.253000). "
            "gzip/base64 static reconstruct SHA 5fd73afd... Frozen public-route portfolio (`research/route_factory`). "
            "Route index by shop prefix depth 1 at step 72 and depth 2 at step 144. No 216/226/288/360/432/576/648/712 reselect. "
            "No ROUTE_STEP/PROGRAM/sale_horizon/ADVANCE_START. No ctypes/agent.so. Cells not executed. "
            "Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "alperen5252525/market-smart-recovery-kaggriculture",
        "path": "artifacts/public_sources/_hunt_20260915c/alperen5252525__market-smart-recovery-kaggriculture/market-smart-recovery-kaggriculture.ipynb",
        "verdict": "reject_v43_reprint_shop0909_overlay",
        "sha256": "919fc1d61050cd96f799979e49177ae3ac7bce98ec9835724238bea73f4a08ed",
        "note": (
            "New slug vs _hunt_20260915b (lastRunTime 2026-09-15 13:03:18.593000). "
            "SOURCE_BYTES static reconstruct SHA 919fc1d6... Exact reprint of already-rejected ahmedberatozer V43. "
            "Shop0909 day-6 144/648 plus 288 four-turn sale overlay plus step==712 terminal planner. "
            "216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. No ctypes/agent.so. "
            "Cells not executed. Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
]
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1582.4 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1286.1 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1582.4; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 4 new slugs vs _hunt_20260915b "
    "(public search newest alperen5252525/turn-one-market-advantage-kaggriculture lastRunTime 2026-09-15 13:24:02.117000 "
    "pipe-4 reprint SHA 7a37397f; public-state v58 SHA b041058e day-6 72/144 plus yarn clone-latch 360; "
    "momentum SHA 5fd73afd frozen shop-prefix tapes; market-smart V43 reprint SHA 919fc1d6; none farm-route reselect after 216). "
    "Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260915c_cut16_rolling.json").read_text(encoding="utf-8"))
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
            "15b",
        )
    ]
    packet = {
        "title": "Kaggriculture study packet 2026-09-15c",
        "not_the_0915b_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260915c/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260915c/kaggriculture-publicleaderboard-2026-09-15T14-03-28.csv",
            "leaderboard_api": "experiments/20260915c_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260915c",
            "top_replays": "artifacts/kaggle_runs/top_20260915c",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915c",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260915c_gate.json",
            "episode_report": "experiments/20260915c_episode_report.json",
            "hunt_report": "experiments/20260915c_hunt_report.json",
            "algo_note": "experiments/20260915c_algo_note.json",
            "loss_class": "experiments/20260915c_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1582.4,
            "rank": 2291,
            "n_teams": 9128,
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
            "cut16_score": 1582.4,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2953.4,
            "rank10": {"team": "leave you", "score": 2987.6},
            "rank1": {"team": "Majkel1337", "score": 3147.0, "submissionId": 56156662},
            "public_cut16": {"n": 301, "wtl": [124, 2, 175], "mean_margin": -2069.5},
        },
        "rolling": {
            "previous": "experiments/20260915b_cut16_rolling.json",
            "live_cut16": "experiments/20260915c_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0915b": True,
            "n": 12,
            "wtl": [5, 0, 7],
            "mean_margin": -3963.6,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": first["id"],
            "margin": first["margin"],
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "9c5s3g",
            "herd_opp": "11c5s",
            "sheep_steps_us": [row["step"] for row in first["sheep_steps_us"]],
        },
        "top_board": {
            "source": "experiments/20260915c_top10_games.json",
            "not_copied_from": prior_top,
            "Majkel1337": {
                "land": [
                    [150, 218],
                    [150, 220],
                    [150, 218, 220, 222],
                    [150, 220, 222],
                ],
                "herd": ["5c9s4g", "6c10s0g", "11c3s2g", "9c3s2g"],
                "wheat": [466, 430, 411, 399],
                "shops": ["PET_CAFE", "YARN_STORE", "PET_CAFE", "FARMERS_MARKET"],
                "clone": "0_of_4",
                "episodes": [109308893, 109302525, 109302443, 109296294],
                "note": (
                    "CSV #1 3147.0 live 3147.1 scoring sub 56156662 (current sub 56216119 is 3144.5). "
                    "Ids disjoint from 20260915b Majkel set. Mid-land 150 then 218-222 "
                    "(150/218, 150/220, 150/218/220/222, 150/220/222), wheat 399-466, clone=0 on 4/4, "
                    "goose mix 4g/0g/2g/2g. Opening land is not a later-block license."
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
            "score": 1582.4,
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
                "Already live COMPLETE 1582.4. This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                "Extra sheep 226/241/265 not 227/242/266. Rolling 109297997 extra-goose vs extra-cow 9c5s3g vs 11c5s -26009; "
                "109057555 identical-clone extra-goose 9c5s3g -23988; "
                "109044160 extra-cow vs extra-goose 7c6s vs 6c6s5g -15134. New-window Gaddam 109297997 extra-goose -26009. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 4 new slugs vs 0915b, "
                "none licensed (public-search newest alperen5252525/turn-one-market-advantage-kaggriculture pipe-4 reprint SHA 7a37397f; "
                "public-state v58 SHA b041058e day-6 72/144 plus yarn clone-latch 360; momentum SHA 5fd73afd frozen shop-prefix tapes; "
                "market-smart V43 reprint SHA 919fc1d6). "
                "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. "
                "Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1582.4 and keeps 1286.1."
            ),
        },
        "hunt": HUNT_ROWS,
    }
    dump(ROOT / "experiments/20260915c_study_packet.json", packet)

    dump(
        ROOT / "experiments/20260915c_episode_report.json",
        {
            "date": "2026-09-15",
            "packet": "20260915c",
            "utc": "2026-09-15T14:03:28Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1582.4,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1582.4 (was 1588.3). Newest public 109297997. Newest-2 = shopbag reupload 56151155 "
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
            "heralces_rank_csv": 2291,
            "heralces_score": 1582.4,
            "n_teams_csv": 9128,
            "public_56151152": {
                "n_public": 301,
                "n_validation": 1,
                "n_completed_public": 301,
                "wtl": [124, 2, 175],
                "mean_margin": -2069.5,
                "status": "COMPLETE",
                "publicScore": 1582.4,
            },
            "rolling_ids": IDS,
            "rolling_forbidden_0915b": PREV_15B,
            "ids_not_identical_to_0915b": True,
            "ids_disjoint_from_0915b": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [5, 0, 7],
            "mean_margin": -3963.6,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids disjoint from 20260915b packet, all 720 DONE/DONE. 5W 7L. "
                "Worst Gaddam Shiva Teja 109297997 L -26009 9c5s3g vs 11c5s clone=1 extra-goose vs extra-cow. "
                "New-window Gaddam extra-goose -26009. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        ROOT / "experiments/20260915c_hunt_report.json",
        {
            "date": "2026-09-15",
            "packet": "20260915c",
            "kernels_not_in_0915b_packet": True,
            "no_upload": True,
            "no_kaggle_submit": True,
            "cells_executed": False,
            "extracted_later_block_agent": False,
            "later_block_python_after_216": False,
            "any_licensed_for_extract": False,
            "licensed_kernel": None,
            "root_main_py": "unchanged",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915c",
            "inspect_scripts": [
                "experiments/candidates/scan_hunt_20260915c.py",
                "experiments/candidates/inspect_hunt_20260915c.py",
                "experiments/candidates/_inspect_hunt_payloads_20260915c.py",
                "experiments/candidates/_extract_hunt_payloads_20260915c.py",
            ],
            "python": "D:\\kaggle\\kaggriculture\\.venv\\Scripts\\python.exe",
            "payload_decode": "writefile_static_hash_only",
            "compare_0915b": {
                "hunt_dir": "artifacts/public_sources/_hunt_20260915b",
                "hunt_report": "experiments/20260915b_hunt_report.json",
                "gate": "experiments/20260915b_gate.json",
                "note": (
                    "4 new slugs vs _hunt_20260915b. Public search newest is now "
                    "alperen5252525/turn-one-market-advantage-kaggriculture (lastRunTime 2026-09-15 13:24:02.117000). "
                    "Did not re-pull rejected kernels (anandkumar369o analysis SHA 595d29fe, "
                    "nathanjacob pipe-4 SHA 7a37397f, kenanzhang9 SHA 602ae8be, "
                    "xuantianfengwu terminal-logistics SHA 364ca885, taylorclark637 sovereign-swarm SHA ffc0e6e2, "
                    "ahmedberatozer v43 SHA 919fc1d6, prvsiyan field-clock, alperen adaptive-route SHA 77cf6772, "
                    "destbreso telemetry, alperen harvestforge SHA 01f0cd47, nathanjacob clustering, hosen42 validation, "
                    "nathanjacob pipe-2 SHA 728fdfb4, leoprovorov god-s-mode, sunil v6 SHA 8951ff93, "
                    "xuantianfengwu hour-4 SHA dc07c7a9, guruprasaathas111 fully-dynamic SHA f4e3935c, "
                    "rohitt94 SHA 62a80706, xuantianfengwu r10 SHA 3b8a1d4d, aurax7 v5, lime0001 t23, "
                    "Ahmed V41 SHA 8951ff93, yhay81 0913, y3uanm rollback-v20)."
                ),
            },
            "public_search_newest": "alperen5252525/turn-one-market-advantage-kaggriculture",
            "public_search_newest_lastRunTime": "2026-09-15 13:24:02.117000",
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

    old_gate = json.loads((ROOT / "experiments/20260915b_gate.json").read_text(encoding="utf-8"))
    gate = deepcopy(old_gate)
    gate["date"] = "2026-09-15"
    gate["packet"] = "20260915c"
    gate["named_kernels_scanned"] = [row["kernel"] for row in HUNT_ROWS]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260915c"
    gate["hunt_report"] = "experiments/20260915c_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1582.4
    gate["live"]["shopbag"]["score_complete"] = 1286.1
    gate["rejected"] = [
        {"kernel": row["kernel"], "verdict": row["verdict"], "note": row["note"]} for row in HUNT_ROWS
    ] + old_gate["rejected"]
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1582.4 partnered with newer shopbag 56151155 COMPLETE 1286.1 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "4 new public slugs vs _hunt_20260915b, none licensed: public-search newest alperen5252525/turn-one-market-advantage-kaggriculture "
        "(pipe-4 reprint SHA 7a37397f); public-state v58 SHA b041058e day-6 72/144 plus yarn clone-latch 360; "
        "momentum SHA 5fd73afd frozen shop-prefix tapes; market-smart V43 reprint SHA 919fc1d6. "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. "
        "Cut 12/13 stay Hold. Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: Gaddam extra geese 227/242 already bought vs 11c -26009; "
        "Liyi extra geese 227/242 identical-clone -23988; "
        "Dhruv extra sheep 218/242/266 already bought vs 6c10s -12590; Satoshi extra sheep 218/242/266 clone=0 -12300."
    )
    dump(ROOT / "experiments/20260915c_gate.json", gate)

    dump(
        ROOT / "experiments/20260915c_cut16_loss_class.json",
        {
            "date": "2026-09-15",
            "packet": "20260915c",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": IDS,
            "ids_0915b": PREV_15B,
            "disjoint_from_0915b": True,
            "all_720_done_done": True,
            "wtl": [5, 0, 7],
            "mean_margin": -3963.6,
            "clone_n": 10,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [0.0, 22.0],
            "wool_360": {
                "109297997": 1,
                "109159847": 1,
                "109152510": 236,
                "109149160": 231,
                "109142116": 224,
                "109135062": 43,
                "109111080": 226,
                "109091091": 195,
                "109078755": 238,
                "109057555": 43,
                "109054323": 1,
                "109044160": 1,
            },
            "wool_432": {
                "109297997": 1,
                "109159847": 5,
                "109152510": 238,
                "109149160": 158,
                "109142116": 189,
                "109135062": 1,
                "109111080": 197,
                "109091091": 1,
                "109078755": 234,
                "109057555": 1,
                "109054323": 5,
                "109044160": 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-15b: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-goose. "
                "WTL 5-0-7 mean -3963.6 vs 09-15b 4-0-8 mean -3874.9. New window game Gaddam Shiva Teja 109297997 -26009. clone=10/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 109297997,
                    "opp": "Gaddam Shiva Teja",
                    "margin": -26009.0,
                    "herd_us": "9c5s3g",
                    "herd_opp": "11c5s",
                    "shops": ["ICE_CREAM_SHOP"],
                }
            ],
        },
    )

    algo = json.loads((ROOT / "experiments/20260915b_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-15"
    algo["packet"] = "20260915c"
    algo["live"]["cut16"]["csv_0915c_team_score"] = 1582.4
    algo["live"]["shopbag"]["score_complete"] = 1286.1
    algo["live"]["rank_csv_0915c"] = 2291
    algo["cut16_live_failure_class"]["0915c"] = {
        "file": "experiments/20260915c_cut16_rolling.json",
        "ids": IDS,
        "wtl": [5, 0, 7],
        "mean_margin": -3963.6,
        "clone": "10/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 109297997,
                "opp": "Gaddam Shiva Teja",
                "margin": -26009,
                "shops72": ["ICE_CREAM_SHOP"],
                "buy": "9c5s3g vs 11c5s",
                "us216": [227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 109057555,
                "opp": "Liyi xin jie",
                "margin": -23988,
                "shops72": ["PET_CAFE"],
                "buy": "9c5s3g vs 9c5s3g",
                "clone": 1,
            },
            {
                "id": 109044160,
                "opp": "Harshith revuru",
                "margin": -15134,
                "shops72": ["BRUNCH_SPOT"],
                "buy": "7c6s vs 6c6s5g",
                "clone": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "4 new public slugs vs _hunt_20260915b; public-search newest is alperen turn-one pipe-4 reprint (SHA 7a37397f). "
            "public-state v58 SHA b041058e is day-6 72/144 plus yarn clone-latch at 360; momentum SHA 5fd73afd is frozen shop-prefix tapes; "
            "market-smart SHA 919fc1d6 is Ahmed V43 reprint. "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump(ROOT / "experiments/20260915c_algo_note.json", algo)
    print("hunt0", hunt_row["kernel"])


if __name__ == "__main__":
    main()
