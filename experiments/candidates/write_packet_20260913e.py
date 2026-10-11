"""Write 20260913e study packet JSON. No upload. No cell exec."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = "20260913e"
IDS = [
    108328160,
    108311577,
    108273755,
    108270318,
    108243488,
    108208866,
    108204278,
    108191120,
    108175982,
    108172639,
    108166009,
    108162165,
]
IDS_13D = [
    108326448,
    108296309,
    108290336,
    108259280,
    108227462,
    108224822,
    108222615,
    108153141,
    108139022,
    108138037,
    108124312,
    108123019,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (IskanderAkhmetov 108166009 9c5s vs 8c6s3g clone=1 SMOOTHIE extra sheep only 314 -12967 wool $1 at 360; "
    "Ke Ma Ke 108175982 9c5s vs 8c6s3g extra sheep 314 -3323 wool $1; XIAO MA 108172639 7c6s vs 8c6s3g sheep 2/151/196 -6573 wool $1) "
    "+ extra-sheep 4c16s1g (Artem The Farmer 108328160 9c8s vs 4c16s1g BRUNCH extra sheep 227/242/266 already bought -8536) "
    "+ extra-goose/identical-clone + YARN clone timing. Newest-window Artem 108328160 extra-sheep 16s BRUNCH -8536 extra sheep 227/242/266 already bought. "
    "Bonkoturyu 108243488 identical 9c8s SMOOTHIE +53 extra sheep 227/242/266 already bought. "
    "automatylicza 108273755 6c12s vs 6c11s YARN -7750 extra sheep 218/242/266 already bought. "
    "rick11224 108208866 clone=0 9c5s vs 7c4s PET_CAFE extra sheep 314 -6392. "
    "clone=11/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: 8c6s3g losses bought sheep at 314 or skipped 227; YARN losses already bought 218/242/266 and lost; "
    "Artem already bought 227/242/266 (9c8s) and lost -8536 vs 16 sheep; Bonkoturyu already bought 227/242/266 (9c8s identical clone) coin-flip +53. "
    "Same extra-animal family as 09-13c plus one extra-sheep 16s game."
)
HUNT_V39 = {
    "kernel": "ahmedberatozer/notebookda72f457f5",
    "verdict": "reject_v39_shop0909_overlay",
    "note": (
        "New vs _hunt_20260913d. Title V39 Ready Before the Rush. lastRunTime 2026-09-12 22:41:36. "
        "Notebook SHA e8c047a1 (340329 bytes). %%writefile main.py cell 4 sha256 "
        "708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8 distinct from V38 a2047ebd, "
        "V37 94c1c2c0, and live cuts 14/15/16. Shop0909 chassis (step>=144 day6 / step>=648 day27) plus "
        "712-718 terminal planner, 216-227 milk-shop livestock sub, four-turn reservations from 288. "
        "Feed/calendar overlay, not after-216 farm/route reselect. No ROUTE_STEP/PROGRAM/reselect/"
        "YARN_SECOND/sale_horizon/ADVANCE_START/ctypes.CDLL/agent.so. Cells not executed. Did not extract to candidates/."
    ),
    "writefile": {
        "cell": 4,
        "name": "main.py",
        "sha256": "708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8",
    },
    "expected_main_sha256": "708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8",
}
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1695.5 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1321.1 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1695; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Ahmed V39 SHA 708c7485 is Shop0909 144/648 + 288/712 overlay. "
    "Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(name: str, obj: object) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    dump(
        "20260913e_hunt_report.json",
        {
            "date": "2026-09-13",
            "packet": P,
            "kernels_not_in_0913d_packet": True,
            "no_upload": True,
            "no_kaggle_submit": True,
            "cells_executed": False,
            "extracted_later_block_agent": False,
            "later_block_python_after_216": False,
            "any_licensed_for_extract": False,
            "licensed_kernel": None,
            "root_main_py": "unchanged",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913e",
            "inspect_scripts": [
                "experiments/candidates/scan_hunt_20260913e.py",
                "experiments/candidates/inspect_hunt_20260913e.py",
                "experiments/candidates/scan_hunt_20260913e_detail.py",
            ],
            "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
            "payload_decode": "writefile_static_only",
            "compare_0913d": {
                "hunt_dir": "artifacts/public_sources/_hunt_20260913d",
                "hunt_report": "experiments/20260913d_hunt_report.json",
                "gate": "experiments/20260913d_gate.json",
                "note": (
                    "This fire pulled one new public slug vs _hunt_20260913d. "
                    "ahmedberatozer/notebookda72f457f5 is Ahmed V39 Shop0909 144/648 + 288/712 overlay SHA 708c7485, not later-block. "
                    "Did not re-pull rejected kernels (prvsiyan market-ledger, timed-six-cow, Ahmed V38, lokesh V37, crystalbaby, "
                    "nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20)."
                ),
            },
            "public_search_newest": "ahmedberatozer/notebookda72f457f5",
            "public_search_newest_lastRunTime": "2026-09-12 22:41:36.970000",
            "live_cuts_not_matched": {
                "cut14": {
                    "name": "y3uanm_router_v5",
                    "sha256_prefix": "acf7c664",
                    "reselect": [226, 360, 433],
                },
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
            "named_kernels_scanned": ["ahmedberatozer/notebookda72f457f5"],
            "author_list_no_new_later_block": [
                "yhay81/shop-router-0911-simple",
                "yamakawanin/king-v4e-rc4",
                "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
                "y3uanm/kaggriculture-conservative-market-router-v5",
                "y3uanm/kaggriculture-safe-baseline-rollback-v20",
            ],
            "author_list_note": (
                "yhay81 newest is still arc-agi-2-atlas-program-corpus (not kaggriculture). "
                "Newest kaggriculture kernel remains shop-router-0911-simple 2026-09-11 08:38 day-6 144/648. "
                "yamakawanin no rc5. Thomas no new tree. y3uanm no v6."
            ),
            "hunt": [HUNT_V39],
        },
    )

    rejected = [
        HUNT_V39,
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
            "note": "0913b already rejected SHA a2047ebd. Did not re-pull. V39 is a new slug, not this V38 kernel.",
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
            "note": "Author list 2026-09-13e: still newest Yusuke kaggriculture kernel (2026-09-11 08:38). Day-6 144/648. Did not re-pull.",
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
    ]
    dump(
        "20260913e_gate.json",
        {
            "date": "2026-09-13",
            "packet": P,
            "freeze": False,
            "hold": True,
            "candidate": None,
            "clone_g5_run": False,
            "extracted_later_block_agent": False,
            "cells_executed": False,
            "rejected": rejected,
            "cut12_hold": True,
            "cut13_hold": True,
            "cut12_13_note": (
                "No new recorded-seat flipping evidence vs Deskbo 105744091 AND Stefano 105798735 or fufu 105790145. "
                "Prior losses stand. Extra-animal 8c6s3g / extra-sheep 16s is not a milk-heavy license. Did not re-screen."
            ),
            "not_227_wrap": True,
            "root_main_untouched": True,
            "root_main_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "no_upload": True,
            "no_kaggle_submit": True,
            "windows_agent_so": False,
            "engine": "kaggle-environments==1.32.7",
            "live": {
                "cut14": {
                    "name": "y3uanm_router_v5",
                    "submissionId": 56111821,
                    "sha256": "acf7c664",
                },
                "cut15": {
                    "name": "thomastschinkel_psr_938",
                    "submissionId": 56146106,
                    "sha256": "b87a27ed",
                },
                "cut16": {
                    "name": "yamakawanin_king_v4e_rc4",
                    "submissionId": 56151152,
                    "score_complete": 1695.5,
                    "sha256": "26ffba52",
                },
                "shopbag": {
                    "submissionId": 56151155,
                    "score_complete": 1321.1,
                    "newer_than_cut16": True,
                },
            },
            "upload_bail": True,
            "hunt_dir": "artifacts/public_sources/_hunt_20260913e",
            "hunt_report": "experiments/20260913e_hunt_report.json",
            "named_kernels_scanned": ["ahmedberatozer/notebookda72f457f5"],
            "author_list_no_new_later_block": [
                "yhay81/shop-router-0911-simple",
                "yamakawanin/king-v4e-rc4",
                "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "y3uanm/kaggriculture-conservative-market-router-v5",
                "y3uanm/kaggriculture-safe-baseline-rollback-v20",
            ],
            "why": (
                "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1695.5 partnered with newer shopbag 56151155 COMPLETE 1321.1 < 1500. "
                "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
                "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). "
                "freeze is false because of this upload-bail, not because a licensed later-block is ready. "
                "One new public slug this fire vs _hunt_20260913d: Ahmed V39 notebookda72f457f5 writefile SHA 708c7485 "
                "(Shop0909 144/648 + 288/712 overlay, not later-block). Yusuke/king/Thomas/y3uanm author lists have no new later-block. "
                "Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. Root main.py SHA untouched. "
                "Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. 227/242/266 wrap not licensed: "
                "8c6s3g losses bought sheep at 314; YARN losses already bought 218/242/266 and lost; "
                "Artem 108328160 already bought 227/242/266 (9c8s) and lost -8536 vs 16 sheep; "
                "Bonkoturyu already bought 227/242/266 (9c8s identical clone) and won coin-flip +53."
            ),
        },
    )

    dump(
        "20260913e_episode_report.json",
        {
            "date": "2026-09-13",
            "packet": P,
            "utc": "2026-09-12T23:36:41Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1695.5,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1695.5 (was 1698.7). Newest public 108328160 updatedScore 1695.506. "
                "Newest-2 = shopbag reupload 56151155 (newer id, 1321.1) + cut 16 56151152. "
                "Upload-bail TRUE (c): shopbag partner 1321.1 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1321.1,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 1949,
            "heralces_score": 1695.5,
            "n_teams_csv": 8809,
            "public_56151152": {
                "n_public": 199,
                "n_validation": 1,
                "n_completed_public": 199,
                "wtl": [89, 2, 108],
                "mean_margin": -801.4,
                "status": "COMPLETE",
                "publicScore": 1695.5,
            },
            "rolling_ids": IDS,
            "rolling_forbidden_0913d": IDS_13D,
            "ids_not_identical_to_0913d": True,
            "ids_disjoint_from_0913d": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [4, 0, 8],
            "mean_margin": -3395.0,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. "
                "Disjoint from 20260913d packet; 11/12 overlap 20260913c (Joyal 108161412 dropped; Artem 108328160 new). "
                "4W 8L. Worst IskanderAkhmetov 108166009 L -12967 9c5s vs 8c6s3g clone=1 SMOOTHIE extra sheep only 314. "
                "Artem The Farmer 108328160 L -8536 9c8s vs 4c16s1g BRUNCH extra sheep 227/242/266 already bought. "
                "automatylicza 108273755 L -7750 6c12s vs 6c11s YARN extra sheep 218/242/266 already bought. "
                "Bonkoturyu 108243488 identical 9c8s +53 extra sheep 227/242/266 already bought. "
                "Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        "20260913e_cut16_loss_class.json",
        {
            "date": "2026-09-13",
            "packet": P,
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": IDS,
            "ids_0913d": IDS_13D,
            "disjoint_from_0913d": True,
            "all_720_done_done": True,
            "wtl": [4, 0, 8],
            "mean_margin": -3395.0,
            "clone_n": 11,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 27.0],
            "wool_360": {
                "108328160": 230,
                "108311577": 185,
                "108273755": 236,
                "108270318": 183,
                "108243488": 235,
                "108208866": 49,
                "108204278": 11,
                "108191120": 237,
                "108175982": 1,
                "108172639": 1,
                "108166009": 1,
                "108162165": 37,
            },
            "wool_432": {
                "108328160": 158,
                "108311577": 179,
                "108273755": 212,
                "108270318": 189,
                "108243488": 233,
                "108208866": 1,
                "108204278": 1,
                "108191120": 228,
                "108175982": 1,
                "108172639": 5,
                "108166009": 1,
                "108162165": 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal 8c6s3g family as 09-13c/09-13d plus newest extra-sheep 16s (Artem). "
                "WTL 4-0-8 mean -3395.0 vs 09-13d 6-0-6 mean -2130.1. Wool $1 by 360 on Iskander/XIAO MA/Ke Ma Ke. clone=11/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 108166009,
                    "opp": "IskanderAkhmetov",
                    "margin": -12967.0,
                    "herd_us": "9c5s",
                    "herd_opp": "8c6s3g",
                    "shops": ["SMOOTHIE_SHOP"],
                    "clone": True,
                    "sheep_us": [2, 196, 314],
                },
                {
                    "id": 108328160,
                    "opp": "Artem The Farmer",
                    "margin": -8536.0,
                    "herd_us": "9c8s",
                    "herd_opp": "4c16s1g",
                    "shops": ["BRUNCH_SPOT"],
                    "clone": True,
                    "sheep_us": [2, 196, 227, 242, 266],
                },
                {
                    "id": 108273755,
                    "opp": "automatylicza",
                    "margin": -7750.0,
                    "herd_us": "6c12s",
                    "herd_opp": "6c11s",
                    "shops": ["YARN_STORE"],
                    "clone": True,
                    "sheep_us": [2, 151, 196, 218, 242, 266],
                },
            ],
            "not_227_242_266_wrap": True,
            "not_opening_broke": True,
            "not_freeze_after_day9_9c9s": True,
        },
    )

    dump(
        "20260913e_algo_note.json",
        {
            "date": "2026-09-13",
            "packet": P,
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
                    "status": "COMPLETE",
                },
                "shopbag": {
                    "submissionId": 56151155,
                    "lineage": 55962761,
                    "score_complete": 1321.1,
                    "newer_than_cut16": True,
                },
                "newest_2": [56151155, 56151152],
                "rank_csv_0913e": 1949,
            },
            "cut16_live_failure_class": {
                "0913d": {
                    "file": "experiments/20260913d_cut16_rolling.json",
                    "ids": IDS_13D,
                    "wtl": [6, 0, 6],
                    "mean_margin": -2130.1,
                    "class": "extra-animal 8c6s3g + extra-goose/identical-clone + YARN clone timing",
                },
                "0913e": {
                    "file": "experiments/20260913e_cut16_rolling.json",
                    "ids": IDS,
                    "wtl": [4, 0, 8],
                    "mean_margin": -3395.0,
                    "clone": "11/12",
                    "class": "same extra-animal 8c6s3g family plus extra-sheep 16s (Artem); wool $1 by 360 on Iskander/XIAO MA/Ke Ma Ke; plus extra-goose/identical-clone + YARN clone timing",
                    "heavy": [
                        {
                            "id": 108166009,
                            "opp": "IskanderAkhmetov",
                            "margin": -12967,
                            "shops72": ["SMOOTHIE_SHOP"],
                            "buy": "9c5s vs 8c6s3g",
                            "us216": [314],
                            "wool_px_360": 1,
                        },
                        {
                            "id": 108328160,
                            "opp": "Artem The Farmer",
                            "margin": -8536,
                            "shops72": ["BRUNCH_SPOT"],
                            "buy": "9c8s vs 4c16s1g",
                            "us216": [227, 242, 266],
                            "wool_px_360": 230,
                        },
                    ],
                },
            },
            "q1_reselect_after_216": {
                "licensed_this_fire": False,
                "note": (
                    "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
                    "Public search newest ahmedberatozer/notebookda72f457f5 (V39 writefile SHA 708c7485) is Shop0909 144/648 + 288/712 overlay. "
                    "Author lists unchanged."
                ),
            },
        },
    )

    dump(
        "20260913e_top_board_note.json",
        {
            "date": "2026-09-13",
            "packet": P,
            "team": "Majkel1337",
            "teamId": 16718819,
            "rank": 1,
            "scoring_sub": 56156662,
            "score": 3223.8,
            "last_updated_score": 3223.8562184172947,
            "dateSubmitted": "2026-09-11 02:18:56.837000",
            "csv": "D:/kaggle/kaggriculture/artifacts/kaggle_runs/lb_20260913e/kaggriculture-publicleaderboard-2026-09-12T23-36-41.csv",
            "csv_time": "2026-09-12T23:36:41",
            "live_score": "3223.8",
            "replays": "artifacts/kaggle_runs/top_20260913e",
            "games_file": "experiments/20260913e_top10_games.json",
            "games_json_complete": True,
            "episodes_file": "experiments/episodes_sub_56156662_majkel1337.json",
            "leaderboard_snapshot": "experiments/20260913e_public_leaderboard_api.json",
            "episode_ids": [108340909, 108336738, 108332509, 108327803],
            "disjoint_from_0913d": True,
            "0913d_ids": [108323526, 108318789, 108314478, 108151282],
            "0913d_same_sub": 56156662,
            "record": "0-4",
            "clone": "0_of_4",
            "class": "mid_land_not_opening_not_later_block",
            "note": (
                "CSV #1 3223.8 live 3223.8 scoring sub 56156662. Ids disjoint from 20260913d Majkel set. "
                "Mid-land 150 then 218-222 (three games 150/220/222; one 150/218), wheat 349-674, clone=0 on 4/4, "
                "two 2-goose games and one 4-goose. Opening land is not a later-block license."
            ),
        },
    )

    dump(
        "20260913e_study_packet.json",
        {
            "title": "Kaggriculture study packet 2026-09-13e",
            "not_the_0913d_packet": True,
            "no_upload": NO_UPLOAD,
            "upload_bail": True,
            "upload_bail_reasons": {
                "a_newest_cut_pending": False,
                "b_newest_cut_complete_below_1500": False,
                "c_drop_ge1500_without_ge1500_partner": True,
            },
            "sources": {
                "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913e/kaggriculture.zip",
                "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913e/kaggriculture-publicleaderboard-2026-09-12T23-36-41.csv",
                "leaderboard_api": "experiments/20260913e_public_leaderboard_api.json",
                "episodes_cut16": "experiments/episodes_56151152.json",
                "cut16_replays": "artifacts/kaggle_runs/cut16_20260913e",
                "top_replays": "artifacts/kaggle_runs/top_20260913e",
                "hunt_dir": "artifacts/public_sources/_hunt_20260913e",
                "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
                "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
                "gate": "experiments/20260913e_gate.json",
                "episode_report": "experiments/20260913e_episode_report.json",
                "hunt_report": "experiments/20260913e_hunt_report.json",
                "algo_note": "experiments/20260913e_algo_note.json",
                "loss_class": "experiments/20260913e_cut16_loss_class.json",
            },
            "live": {
                "sixday": 56028043,
                "sixday_score": 1590.8,
                "sixday_status": "COMPLETE",
                "team_score": 1695.5,
                "rank": 1949,
                "n_teams": 8809,
                "shopbag_previous": 56112309,
                "shopbag_reupload": 56151155,
                "shopbag_status": "COMPLETE",
                "shopbag_score": 1321.1,
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
                "cut16_score": 1695.5,
                "root_main_py": "h2 65e6f5cd... unchanged",
                "gold21": 2918.7,
                "rank10": {"team": "redblackbst", "score": 2979.5},
                "rank1": {
                    "team": "Majkel1337",
                    "score": 3223.8,
                    "submissionId": 56156662,
                },
                "public_cut16": {
                    "n": 199,
                    "wtl": [89, 2, 108],
                    "mean_margin": -801.4,
                },
            },
            "rolling": {
                "previous": "experiments/20260913d_cut16_rolling.json",
                "live_cut16": "experiments/20260913e_cut16_rolling.json",
                "ids": IDS,
                "ids_not_identical_to_0913d": True,
                "n": 12,
                "wtl": [4, 0, 8],
                "mean_margin": -3395.0,
                "loss_class": LOSS_CLASS,
            },
            "mozayed": {
                "id": 108166009,
                "margin": -12967.0,
                "clone": True,
                "Q": [3, 3],
                "land": [151, 266],
                "herd_us": "9c5s",
                "herd_opp": "8c6s3g",
                "sheep_steps_us": [2, 196, 314],
            },
            "top_board": {
                "source": "experiments/20260913e_top10_games.json",
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
                ],
                "Majkel1337": {
                    "land": [
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 220, 222],
                        [150, 218],
                    ],
                    "herd": ["8c3s2g", "9c6s2g", "5c13s0g", "6c4s4g"],
                    "wheat": [674, 523, 349, 394],
                    "shops": ["BRUNCH_SPOT", "FARMERS_MARKET", "YARN_STORE", "PET_CAFE"],
                    "clone": "0_of_4",
                    "episodes": [108340909, 108336738, 108332509, 108327803],
                    "note": (
                        "CSV #1 3223.8 live 3223.8 scoring sub 56156662. Ids disjoint from 20260913d Majkel set. "
                        "Mid-land 150 then 218-222 (three games 150/220/222; one 150/218), wheat 349-674, clone=0 on 4/4, "
                        "two 2-goose games and one 4-goose. Opening land is not a later-block license."
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
                "score": 1695.5,
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
                    "Already live COMPLETE 1695.5. This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                    "Extra sheep 226/241/265 not 227/242/266. Rolling 108166009 bought sheep at 314 vs 8c6s3g; "
                    "108273755 already bought 218/242/266 sheep and lost YARN 6c12s; "
                    "108328160 already bought 227/242/266 sheep and lost 9c8s vs 16s -8536; "
                    "108243488 already bought 227/242/266 sheep and won identical 9c8s +53. Not cut 12/13."
                ),
            },
            "cut17": {
                "hold": True,
                "uploaded": None,
                "why": (
                    "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. "
                    "Hunt: Ahmed V39 notebookda72f457f5 SHA 708c7485 is Shop0909 144/648 + 288/712 overlay; "
                    "Yusuke 0911-simple still day-6; no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. "
                    "Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1695 and keeps 1321."
                ),
            },
            "hunt": [HUNT_V39],
        },
    )
    print("done")


if __name__ == "__main__":
    main()
