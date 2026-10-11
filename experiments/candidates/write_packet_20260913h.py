"""Emit 20260913h study packet JSONs from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLL = json.loads((ROOT / "experiments/20260913h_cut16_rolling.json").read_text(encoding="utf-8"))
API = json.loads((ROOT / "experiments/20260913h_public_leaderboard_api.json").read_text(encoding="utf-8"))
TOP = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))

IDS = [g["id"] for g in ROLL["games"]]
PREV = [
    108371627,
    108369265,
    108366745,
    108328160,
    108311577,
    108273755,
    108270318,
    108243488,
    108208866,
    108204278,
    108191120,
    108175982,
]
LOSS = (
    "mixed extra-animal YARN 6c11s vs 7c11s (Peter Cnudde 108383915 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought -13315) "
    "+ extra-sheep 11s (Oleg Smirnov 108345614 9c8s vs 7c11s extra sheep 227/242/266 already bought -11762) "
    "+ extra-goose (Rafael Molina Castano 108377691 9c5s3g vs 9c5s4g extra geese 227/242 sheep 266 -5101; Sophie555 108374873 9c5s3g vs 6c6s6g extra geese 227/242 sheep 266 -3339) "
    "+ identical-clone extra-goose (CodeHacker 108349751 9c5s3g vs 9c5s3g extra geese 227/242 -3571; phi 108259280 identical 9c5s3g -14; Gappy 108227462 identical 9c5s3g extra geese 227/242 -1566). "
    "Newest-window Peter YARN extra-sheep 6c11s. Chanhyuk Han 108296309 identical 9c8s +67 extra sheep 227/242/266 already bought. "
    "tksfjn 108290336 6c12s YARN +14627 extra sheep 218/242/266. Sean Peppers 108351144 4c15s FARMERS +2394 extra sheep 218/242/266. "
    "Floth 108343489 4c14s +4018 extra sheep 218/242/266. Igor Aranovsky 108326448 9c5s3g vs 9c9s +6833 extra geese 227/242. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Peter already bought 218/242/266 and lost YARN 6c11s vs 7c11s; Oleg already bought 227/242/266 and lost extra-sheep 11s; Chanhyuk already bought 227/242/266 and won identical 9c8s +67; extra-goose losses bought geese at 227/242 and sheep at 266."
)
WOOL360 = {
    108383915: 237,
    108377691: 43,
    108374873: 11,
    108351144: 231,
    108349751: 43,
    108345614: 234,
    108343489: 231,
    108326448: 37,
    108296309: 226,
    108290336: 237,
    108259280: 37,
    108227462: 37,
}
WOOL432 = {
    108383915: 227,
    108377691: 1,
    108374873: 1,
    108351144: 158,
    108349751: 1,
    108345614: 231,
    108343489: 197,
    108326448: 1,
    108296309: 221,
    108290336: 228,
    108259280: 1,
    108227462: 129,
}
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1691.5 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1319.5 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1691; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Ahmed V39 SHA 708c7485 is Shop0909 144/648 + 288/712 overlay "
    "(already rejected 0913e). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def herd(buy: dict) -> str:
    c = int(buy.get("COW") or 0)
    s = int(buy.get("SHEEP") or 0)
    g = int(buy.get("GOOSE") or 0)
    return f"{c}c{s}s{g}g" if g else f"{c}c{s}s"


def sheep_steps(game: dict) -> list[int]:
    return [e["step"] for e in game.get("sheep_steps_us") or []]


def main() -> None:
    games = ROLL["games"]
    peter = games[0]
    oleg = next(g for g in games if g["id"] == 108345614)
    rafael = next(g for g in games if g["id"] == 108377691)
    majkel = [g for g in TOP if g["team"] == "Majkel1337"]

    hunt_report = {
        "date": "2026-09-13",
        "packet": "20260913h",
        "kernels_not_in_0913g_packet": False,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260913h",
        "inspect_scripts": ["experiments/candidates/scan_hunt_20260913h.py"],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_no_new_notebook",
        "compare_0913g": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260913g",
            "hunt_report": "experiments/20260913g_hunt_report.json",
            "gate": "experiments/20260913g_gate.json",
            "note": (
                "No new slug vs _hunt_20260913g. Public search newest is still ahmedberatozer/notebookda72f457f5 "
                "(lastRunTime 2026-09-12 22:41:36). Did not re-pull rejected kernels (Ahmed V39/V38, prvsiyan market-ledger, "
                "timed-six-cow, lokesh V37, crystalbaby, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, "
                "melomanpanda, zhincez, y3uanm rollback-v20)."
            ),
        },
        "public_search_newest": "ahmedberatozer/notebookda72f457f5",
        "public_search_newest_lastRunTime": "2026-09-12 22:41:36.970000",
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
            "yhay81/shop-router-0911-simple",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "author_list_note": (
            "yhay81 newest is still arc-agi-2-atlas-program-corpus (not kaggriculture). Newest kaggriculture kernel remains "
            "shop-router-0911-simple 2026-09-11 08:38 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6."
        ),
        "hunt": [],
    }

    gate = {
        "date": "2026-09-13",
        "packet": "20260913h",
        "freeze": False,
        "hold": True,
        "candidate": None,
        "clone_g5_run": False,
        "extracted_later_block_agent": False,
        "cells_executed": False,
        "rejected": [
            {
                "kernel": "ahmedberatozer/notebookda72f457f5",
                "verdict": "reject_v39_shop0909_overlay",
                "note": "Still public search newest. 0913e already rejected SHA 708c7485 Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
            },
            {
                "kernel": "prvsiyan/kaggriculture-market-ledger-seasonal-counterplay",
                "verdict": "reject_educational_framework",
                "note": "0913c already rejected SHA 1c98c297. Did not re-pull.",
            },
            {
                "kernel": "xuantianfengwu/kaggriculture-timed-six-cow",
                "verdict": "reject_heuristic_six_cow",
                "note": "0913b already rejected SHA 5dc0c68c. Did not re-pull.",
            },
            {
                "kernel": "ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins",
                "verdict": "reject_v38_reprint",
                "note": "0913b already rejected SHA a2047ebd. Did not re-pull.",
            },
            {
                "kernel": "lokesh0252/kaggriculture-v1",
                "verdict": "reject_v37_reprint",
                "note": "Still a public search hit. 0912e already rejected SHA 94c1c2c0. Did not re-pull.",
            },
            {
                "kernel": "melomanpanda/main-py",
                "verdict": "reject_heuristic",
                "note": "Already rejected. Did not re-pull.",
            },
            {
                "kernel": "crystalbaby/kaggriculture-dynamic-route-agent",
                "verdict": "reject_v37_reprint",
                "note": "Already rejected SHA 94c1c2c0. Did not re-pull.",
            },
            {
                "kernel": "y3uanm/kaggriculture-safe-baseline-rollback-v20",
                "verdict": "cut14_already_live",
                "note": "Author list: still newest y3uanm kaggriculture kernel. Writefile SHA acf7c664 = live cut 14. Did not re-pull.",
            },
            {
                "kernel": "municef1/lb-2448-single-file-kaggriculture-agent",
                "verdict": "reject_tape",
                "note": "Already rejected. Did not re-pull.",
            },
            {
                "kernel": "zhincez/the-base-schedule-is-a-plateau-not-a-lever",
                "verdict": "reject_analysis",
                "note": "Already rejected plateau tape 07f6c806 + analysis nbs. Did not re-pull.",
            },
            {
                "kernel": "bernubritz/kaggriculture-h4-best",
                "verdict": "reject_tape",
                "note": "Already rejected. Did not re-pull.",
            },
            {
                "kernel": "dmitriigluzdov/kaggriculture-a-smaller-market-shock",
                "verdict": "reject_sale_horizon",
                "note": "Already rejected sale_horizon=5. Did not re-pull.",
            },
            {
                "kernel": "nusrati/2650-score",
                "verdict": "reject_sale_overlay",
                "note": "0912d already rejected Ahmed V35 reprint SHA 294e7e4d. Did not re-pull.",
            },
            {
                "kernel": "sunil123kumar/kaggriculture-v4",
                "verdict": "reject_shop0909_t4_overlay",
                "note": "0912d already rejected Shop0909 T4 overlay / 712 planner. Did not re-pull.",
            },
            {
                "kernel": "yhay81/shop-router-0911-simple",
                "verdict": "reject_day6_only",
                "note": "Author list 2026-09-13h: still newest Yusuke kaggriculture kernel (2026-09-11 08:38). Day-6 144/648. Did not re-pull.",
            },
            {
                "kernel": "yamakawanin/king-v4e-rc4",
                "verdict": "cut16_already_live",
                "note": "Author list: no rc5. Already uploaded as 56151152 SHA 26ffba52. Do not re-upload.",
            },
            {
                "kernel": "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "verdict": "cut15_already_live",
                "note": "Already uploaded as 56146106 SHA b87a27ed. Do not re-upload.",
            },
        ],
        "cut12_hold": True,
        "cut13_hold": True,
        "cut12_13_note": (
            "No new recorded-seat flipping evidence vs Deskbo 105744091 AND Stefano 105798735 or fufu 105790145. "
            "Prior losses stand. Extra-animal YARN 6c11s / extra-sheep 11s / extra-goose is not a milk-heavy license. Did not re-screen."
        ),
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
                "score_complete": 1691.5,
                "sha256": "26ffba52",
            },
            "shopbag": {"submissionId": 56151155, "score_complete": 1319.5, "newer_than_cut16": True},
        },
        "upload_bail": True,
        "hunt_dir": "artifacts/public_sources/_hunt_20260913h",
        "hunt_report": "experiments/20260913h_hunt_report.json",
        "named_kernels_scanned": [],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0911-simple",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "why": (
            "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1691.5 partnered with newer shopbag 56151155 COMPLETE 1319.5 < 1500. "
            "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). Pairing a new cut with cut 16 "
            "would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
            "No new public slug this fire vs _hunt_20260913g. Public search newest remains Ahmed V39 notebookda72f457f5 (SHA 708c7485 Shop0909 overlay). "
            "Yusuke/king/Thomas/y3uanm author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
            "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. 227/242/266 wrap not licensed: "
            "Peter already bought 218/242/266 and lost YARN 6c11s vs 7c11s; Oleg already bought 227/242/266 and lost extra-sheep 11s; "
            "Chanhyuk already bought 227/242/266 and won identical 9c8s +67; extra-goose losses bought geese at 227/242 and sheep at 266."
        ),
    }

    episode_report = {
        "date": "2026-09-13",
        "packet": "20260913h",
        "utc": "2026-09-13T02:37:25Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1691.5,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": (
            "COMPLETE 1691.5 (was 1702.8). Newest public 108383915 updatedScore 1691.511. Newest-2 = shopbag reupload 56151155 "
            "(newer id, 1319.5) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner 1319.5 < 1500 and is newer than cut 16, "
            "so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
        ),
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": 1319.5,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": 1956,
        "heralces_score": 1691.5,
        "n_teams_csv": 8814,
        "public_56151152": {
            "n_public": 209,
            "n_validation": 1,
            "n_completed_public": 209,
            "wtl": [93, 2, 114],
            "mean_margin": -984.3,
            "status": "COMPLETE",
            "publicScore": 1691.5,
        },
        "rolling_ids": IDS,
        "rolling_forbidden_0913g": PREV,
        "ids_not_identical_to_0913g": True,
        "ids_disjoint_from_0913g": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": [5, 0, 7],
        "mean_margin": -894.1,
        "rolling_note": (
            "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913g packet. "
            "5W 7L. Worst Peter Cnudde 108383915 L -13315 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought. "
            "Oleg Smirnov 108345614 L -11762 9c8s vs 7c11s extra sheep 227/242/266 already bought. "
            "Chanhyuk Han 108296309 identical 9c8s +67 extra sheep 227/242/266 already bought. Not opening-broke. Not freeze 9c9s."
        ),
    }

    loss_class = {
        "date": "2026-09-13",
        "packet": "20260913h",
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": IDS,
        "ids_0913g": PREV,
        "disjoint_from_0913g": True,
        "all_720_done_done": True,
        "wtl": [5, 0, 7],
        "mean_margin": -894.1,
        "clone_n": 12,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [3.0, 27.0],
        "wool_360": {str(k): v for k, v in WOOL360.items()},
        "wool_432": {str(k): v for k, v in WOOL432.items()},
        "same_class_as_0913c": True,
        "same_class_note": (
            "Same extra-animal family as 09-13c/09-13d/09-13e/09-13f/09-13g: YARN extra-sheep 6c11s plus extra-sheep 11s plus extra-goose/identical-clone. "
            "WTL 5-0-7 mean -894.1 vs 09-13g 6-0-6 mean -3016.2. No 8c6s3g in this window. clone=12/12."
        ),
        "loss_class": LOSS,
        "worst_losses": [
            {
                "id": 108383915,
                "opp": "Peter Cnudde",
                "margin": -13315.0,
                "herd_us": "6c11s",
                "herd_opp": "7c11s",
                "shops": ["YARN_STORE"],
                "clone": True,
                "sheep_us": [2, 151, 196, 218, 242, 266],
            },
            {
                "id": 108345614,
                "opp": "Oleg Smirnov",
                "margin": -11762.0,
                "herd_us": "9c8s",
                "herd_opp": "7c11s",
                "shops": ["PET_CAFE"],
                "clone": True,
                "sheep_us": [2, 196, 218, 227, 242, 266],
            },
            {
                "id": 108377691,
                "opp": "Rafael Molina Castaño",
                "margin": -5101.0,
                "herd_us": "9c5s3g",
                "herd_opp": "9c5s4g",
                "shops": ["ICE_CREAM_SHOP"],
                "clone": True,
                "sheep_us": [2, 196, 218, 266],
            },
        ],
        "not_227_242_266_wrap": True,
        "not_opening_broke": True,
        "not_freeze_after_day9_9c9s": True,
    }

    algo_note = {
        "date": "2026-09-13",
        "packet": "20260913h",
        "role": "strategy/algorithm analyst",
        "no_upload": True,
        "root_main_py": "unchanged",
        "windows_agent_so": False,
        "cells_executed": False,
        "live": {
            "cut14": {
                "name": "y3uanm_router_v5",
                "kernel": "y3uanm/kaggriculture-conservative-market-router-v5",
                "submissionId": 56111821,
                "sha256": "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e",
                "score_complete": 1799.3,
                "dropped_from_newest_2": True,
            },
            "cut15": {
                "name": "thomastschinkel_psr_938",
                "kernel": "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "submissionId": 56146106,
                "sha256": "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522",
                "score_complete": 1864.4,
                "dropped_from_newest_2": True,
            },
            "cut16": {
                "name": "yamakawanin_king_v4e_rc4",
                "kernel": "yamakawanin/king-v4e-rc4",
                "submissionId": 56151152,
                "sha256": "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d",
                "score_complete_0912": 1730.1,
                "csv_0913_team_score": 1683.4,
                "csv_0913b_team_score": 1691.4,
                "csv_0913c_team_score": 1696.4,
                "csv_0913d_team_score": 1698.7,
                "csv_0913e_team_score": 1695.5,
                "csv_0913f_team_score": 1697.5,
                "csv_0913g_team_score": 1702.8,
                "csv_0913h_team_score": 1691.5,
                "status": "COMPLETE",
            },
            "shopbag": {
                "submissionId": 56151155,
                "lineage": 55962761,
                "score_complete": 1319.5,
                "newer_than_cut16": True,
            },
            "newest_2": [56151155, 56151152],
            "rank_csv_0913h": 1956,
        },
        "cut16_live_failure_class": {
            "0913g": {
                "file": "experiments/20260913g_cut16_rolling.json",
                "ids": PREV,
                "wtl": [6, 0, 6],
                "mean_margin": -3016.2,
                "class": "extra-animal 8c6s3g + extra-sheep 16s + extra-goose/identical-clone + YARN clone timing",
            },
            "0913h": {
                "file": "experiments/20260913h_cut16_rolling.json",
                "ids": IDS,
                "wtl": [5, 0, 7],
                "mean_margin": -894.1,
                "clone": "12/12",
                "class": "same extra-animal family: YARN 6c11s vs 7c11s plus extra-sheep 11s plus extra-goose/identical-clone; no 8c6s3g in this window",
                "heavy": [
                    {
                        "id": 108383915,
                        "opp": "Peter Cnudde",
                        "margin": -13315,
                        "shops72": ["YARN_STORE"],
                        "buy": "6c11s vs 7c11s",
                        "us216": [218, 242, 266],
                        "wool_px_360": 237,
                    },
                    {
                        "id": 108345614,
                        "opp": "Oleg Smirnov",
                        "margin": -11762,
                        "shops72": ["PET_CAFE"],
                        "buy": "9c8s vs 7c11s",
                        "us216": [227, 242, 266],
                        "wool_px_360": 234,
                    },
                ],
            },
        },
        "q1_reselect_after_216": {
            "licensed_this_fire": False,
            "note": (
                "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. Public search newest still "
                "ahmedberatozer/notebookda72f457f5 (V39 writefile SHA 708c7485) Shop0909 144/648 + 288/712 overlay. Author lists unchanged."
            ),
        },
    }

    packet = {
        "title": "Kaggriculture study packet 2026-09-13h",
        "not_the_0913g_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913h/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913h/kaggriculture-publicleaderboard-2026-09-13T02-37-25.csv",
            "leaderboard_api": "experiments/20260913h_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913h",
            "top_replays": "artifacts/kaggle_runs/top_20260913h",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913h",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913h_gate.json",
            "episode_report": "experiments/20260913h_episode_report.json",
            "hunt_report": "experiments/20260913h_hunt_report.json",
            "algo_note": "experiments/20260913h_algo_note.json",
            "loss_class": "experiments/20260913h_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1691.5,
            "rank": 1956,
            "n_teams": 8814,
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
            "cut16_score": 1691.5,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2909.9,
            "rank10": {"team": API["rank10"]["team"], "score": 2962.3},
            "rank1": {
                "team": "Majkel1337",
                "score": 3220.9,
                "submissionId": 56156662,
            },
            "public_cut16": {"n": 209, "wtl": [93, 2, 114], "mean_margin": -984.3},
        },
        "rolling": {
            "previous": "experiments/20260913g_cut16_rolling.json",
            "live_cut16": "experiments/20260913h_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0913g": True,
            "n": 12,
            "wtl": [5, 0, 7],
            "mean_margin": -894.1,
            "loss_class": LOSS,
        },
        "ju": {
            "id": 108383915,
            "margin": -13315.0,
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "6c11s",
            "herd_opp": "7c11s",
            "sheep_steps_us": sheep_steps(peter),
        },
        "top_board": {
            "source": "experiments/20260913h_top10_games.json",
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
            ],
            "Majkel1337": {
                "land": [row["land"] for row in majkel],
                "herd": [row["herd"] for row in majkel],
                "wheat": [row["wheat"][0] for row in majkel],
                "shops": [row["shops72"][0] for row in majkel],
                "clone": "0_of_4",
                "episodes": [row["id"] for row in majkel],
                "note": (
                    "CSV #1 3220.9 live 3220.9 scoring sub 56156662. Ids disjoint from 20260913g Majkel set. "
                    "Mid-land 150 then 218-222 (one 150/218; one 150/219/220/221/222/226/227/228; one 150/219/221/227/228; one 150/220/222), "
                    "wheat 429-562, clone=0 on 4/4, goose mix 2g/2g/3g/0g. Opening land is not a later-block license."
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
            "score": 1691.5,
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
                "Already live COMPLETE 1691.5. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                "Rolling 108383915 already bought sheep at 218/242/266 vs 7c11s YARN -13315; 108345614 already bought 227/242/266 sheep and lost extra-sheep 11s -11762; "
                "108296309 already bought 227/242/266 sheep and won identical 9c8s +67. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: public search newest still Ahmed V39 "
                "notebookda72f457f5 SHA 708c7485 Shop0909 144/648 + 288/712 overlay; Yusuke 0911-simple still day-6; no king rc5 / y3uanm v6 / Thomas tree "
                "that actually splits after 216. Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1691 and keeps 1319."
            ),
        },
        "hunt": [],
    }

    outs = {
        "experiments/20260913h_hunt_report.json": hunt_report,
        "experiments/20260913h_gate.json": gate,
        "experiments/20260913h_episode_report.json": episode_report,
        "experiments/20260913h_cut16_loss_class.json": loss_class,
        "experiments/20260913h_algo_note.json": algo_note,
        "experiments/20260913h_study_packet.json": packet,
    }
    for rel, payload in outs.items():
        path = ROOT / rel
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print("WROTE", path)
    print("peter", peter["id"], herd(peter["buy_us"]), sheep_steps(peter))
    print("oleg", oleg["id"], herd(oleg["buy_us"]))
    print("rafael", rafael["id"], herd(rafael["buy_us"]))
    print("majkel_ids", [m["id"] for m in majkel])
    print("disjoint", set(IDS).isdisjoint(PREV))


if __name__ == "__main__":
    main()
