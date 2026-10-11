"""Write 20260913m packet JSON (no upload, no cell exec)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDS = [
    108472548,
    108461768,
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
    108371627,
    108369265,
    108366745,
    108328160,
    108311577,
]
IDS_13L = [
    108445221,
    108441448,
    108441305,
    108412731,
    108383915,
    108377691,
    108374873,
    108351144,
    108349751,
    108345614,
    108343489,
    108326448,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (Ju 108369265 9c5s vs 8c6s3g clone=1 SMOOTHIE extra sheep 218/227 extra geese 242/266 wheat 425 vs 17369 -17212; "
    "linyifangzhenshuai 108426937 7c6s vs 8c6s3g BRUNCH extra sheep 218/227 extra geese 242/266 wheat 486 vs 17346 -9514; "
    "carlos-tagosaku 108429814 7c6s vs 8c6s3g FARMERS extra sheep 218/227 extra geese 242/266 wheat 481 vs 17346 -8454; "
    "Brian Chua 108472548 9c5s vs 8c6s3g SMOOTHIE extra sheep 218/227 extra geese 242/266 wheat 411 vs 458 -659) "
    "+ extra-animal YARN 6c11s (wuwuwu 108432563 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought -10575) "
    "+ extra-sheep 16s (Artem The Farmer 108328160 9c8s vs 4c16s1g extra sheep 227/242/266 already bought -8536). "
    "Wins: Joyal 108422886 6c11s vs 9c5s3g +27397 extra sheep 218/242/266 already bought; "
    "Sidharth Hulyalkar 108399266 9c5s3g vs 9c5s4g +2525 extra geese 227/242 already bought; "
    "Andrey Shpigar 108461768 9c8s vs 6c6s6g +1827 extra sheep 227/242/266 already bought; "
    "Kometa 108366745 9c5s3g vs 9c9s +1244 extra geese 227/242 already bought; "
    "ocean240812 108311577 9c5s3g vs 9c5s4g +1058 extra geese 227/242 already bought; "
    "Rafael Molina Castano 108371627 9c5s3g vs 9c5s4g +395 extra geese 227/242 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-24 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Ju/linyi/carlos/Brian lost 8c6s3g after opp extra sheep 218/227 extra geese 242/266; "
    "wuwuwu already bought 218/242/266 and lost YARN 6c11s; Artem already bought 227/242/266 and lost extra-sheep 16s; "
    "extra-goose wins bought geese at 227/242 and sheep at 266; Andrey already bought 227/242/266 and won vs 6c6s6g."
)
AURAX = {
    "kernel": "aurax7/kaggriculture-shop-router-reactive-v4",
    "path": "artifacts/public_sources/_hunt_20260913m/aurax7__kaggriculture-shop-router-reactive-v4/kaggriculture-shop-router-reactive-v4.ipynb",
    "verdict": "reject_day6_144_648_and_712_overlay",
    "sha256": "3dd123c5b484b533eb5b6d50a4d549433d715c92efb79a7dbe8e1e324c3c32e8",
    "note": (
        "New vs _hunt_20260913l (public-search newest; lastRunTime 2026-09-13 04:30:42). "
        "Python %%writefile main.py SHA 3dd123c5... Inspired by yhay81/shop-router-0911-simple. "
        "day6 at 144, day27 at 648, E182 Shop0909 last-seven-turn 712 planner. "
        "216<=step<=227 is milk-shop livestock sub, not a farm/route reselect. "
        "288 sales-first / R37 horizon overlay. Distinct from cut14 acf7c664, cut15 b87a27ed, cut16 26ffba52. "
        "No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
    ),
}


def dump(name: str, obj: object) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260913m_cut16_rolling.json").read_text(encoding="utf-8"))
    games = rolling["games"]
    top = json.loads((ROOT / "experiments/20260913m_top10_games.json").read_text(encoding="utf-8"))
    api = json.loads((ROOT / "experiments/20260913m_public_leaderboard_api.json").read_text(encoding="utf-8"))
    assert [g["id"] for g in games] == IDS
    wtl = [6, 0, 6]
    mean = -1708.7
    wool_360 = {
        108472548: 1,
        108461768: 224,
        108432563: 237,
        108429814: 1,
        108426937: 1,
        108422886: 240,
        108399266: 43,
        108371627: 43,
        108369265: 1,
        108366745: 43,
        108328160: 230,
        108311577: 185,
    }
    wool_432 = {
        108472548: 55,
        108461768: 189,
        108432563: 227,
        108429814: 5,
        108426937: 5,
        108422886: 241,
        108399266: 1,
        108371627: 1,
        108369265: 1,
        108366745: 1,
        108328160: 158,
        108311577: 179,
    }

    hunt_report = {
        "date": "2026-09-13",
        "packet": "20260913m",
        "kernels_not_in_0913l_packet": True,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260913m",
        "inspect_scripts": [
            "experiments/candidates/inspect_hunt_20260913m.py",
            "experiments/candidates/scan_hunt_20260913m.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_writefile_dumped_for_sha_only",
        "compare_0913l": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260913l",
            "hunt_report": "experiments/20260913l_hunt_report.json",
            "gate": "experiments/20260913l_gate.json",
            "note": "New slug aurax7/kaggriculture-shop-router-reactive-v4 vs empty _hunt_20260913l. Did not re-pull rejected kernels (crystalbaby V38, Ahmed V39/V38, prvsiyan market-ledger, timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20).",
        },
        "public_search_newest": "aurax7/kaggriculture-shop-router-reactive-v4",
        "public_search_newest_lastRunTime": "2026-09-13 04:30:42.083000",
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
        "named_kernels_scanned": ["aurax7/kaggriculture-shop-router-reactive-v4"],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0911-simple",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "author_list_note": "yhay81 newest is still arc-agi-2-atlas-program-corpus (not kaggriculture). Newest kaggriculture kernel remains shop-router-0911-simple 2026-09-11 08:38 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6. aurax7 published v4 (new).",
        "hunt": [AURAX],
    }
    dump("20260913m_hunt_report.json", hunt_report)

    gate = {
        "date": "2026-09-13",
        "packet": "20260913m",
        "freeze": False,
        "hold": True,
        "candidate": None,
        "clone_g5_run": False,
        "extracted_later_block_agent": False,
        "cells_executed": False,
        "rejected": [
            AURAX,
            {
                "kernel": "crystalbaby/kaggriculture-v38-public-submission",
                "verdict": "reject_v38_reprint",
                "note": "Still a public search hit. 0913l already rejected SHA a2047ebd Ahmed V38 Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
            },
            {
                "kernel": "ahmedberatozer/notebookda72f457f5",
                "verdict": "reject_v39_shop0909_overlay",
                "note": "Still a public search hit. 0913e already rejected SHA 708c7485 Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
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
                "note": "0912e already rejected SHA 94c1c2c0. Did not re-pull.",
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
                "note": "Author list 2026-09-13m: still newest Yusuke kaggriculture kernel (2026-09-11 08:38). Day-6 144/648. Did not re-pull.",
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
        "cut12_13_note": "No new recorded-seat flipping evidence vs Deskbo 105744091 AND Stefano 105798735 or fufu 105790145. Prior losses stand. Extra-animal 8c6s3g / YARN 6c11s / extra-sheep 16s is not a milk-heavy license. Did not re-screen.",
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
                "score_complete": 1693.4,
                "sha256": "26ffba52",
            },
            "shopbag": {
                "submissionId": 56151155,
                "score_complete": 1332.1,
                "newer_than_cut16": True,
            },
        },
        "upload_bail": True,
        "hunt_dir": "artifacts/public_sources/_hunt_20260913m",
        "hunt_report": "experiments/20260913m_hunt_report.json",
        "named_kernels_scanned": ["aurax7/kaggriculture-shop-router-reactive-v4"],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0911-simple",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "why": (
            "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1693.4 partnered with newer shopbag 56151155 COMPLETE 1332.1 < 1500. "
            "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
            "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
            "New public slug aurax7/kaggriculture-shop-router-reactive-v4 writefile SHA 3dd123c5 is day-6 144/648 + Shop0909 712 overlay, not a later-block. "
            "Yusuke/king/Thomas/y3uanm author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. Root main.py SHA untouched. "
            "Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. 227/242/266 wrap not licensed: Ju/linyi/carlos/Brian lost 8c6s3g after opp extra sheep 218/227 extra geese 242/266; "
            "wuwuwu already bought 218/242/266 and lost YARN 6c11s; Artem already bought 227/242/266 and lost extra-sheep 16s; extra-goose wins bought geese at 227/242 and sheep at 266."
        ),
    }
    dump("20260913m_gate.json", gate)

    episode_report = {
        "date": "2026-09-13",
        "packet": "20260913m",
        "utc": "2026-09-13T08:36:44Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1693.4,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": (
            "COMPLETE 1693.4 (was 1692.2). Newest public 108472548 updatedScore 1693.466. "
            "Newest-2 = shopbag reupload 56151155 (newer id, submissions 1332.1 / ListEpisodes last_updated 1332.1) + cut 16 56151152. "
            "Upload-bail TRUE (c): shopbag partner 1332.1 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
        ),
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": 1332.1,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": 1981,
        "heralces_score": 1693.4,
        "n_teams_csv": 8849,
        "public_56151152": {
            "n_public": 220,
            "n_validation": 1,
            "n_completed_public": 220,
            "wtl": [98, 2, 120],
            "mean_margin": -1024.1,
            "status": "COMPLETE",
            "publicScore": 1693.4,
        },
        "rolling_ids": IDS,
        "rolling_forbidden_0913l": IDS_13L,
        "ids_not_identical_to_0913l": True,
        "ids_disjoint_from_0913l": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": wtl,
        "mean_margin": mean,
        "rolling_note": (
            "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913l packet. 6W 6L. "
            "Worst Ju 108369265 L -17212 9c5s vs 8c6s3g clone=1 extra sheep 218/227 extra geese 242/266. "
            "New-window Brian Chua 108472548 L -659 9c5s vs 8c6s3g extra sheep 218/227 extra geese 242/266. "
            "wuwuwu 108432563 L -10575 6c11s vs 7c11s YARN extra sheep 218/242/266 already bought. Not opening-broke. Not freeze 9c9s."
        ),
    }
    dump("20260913m_episode_report.json", episode_report)

    loss_class = {
        "date": "2026-09-13",
        "packet": "20260913m",
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": IDS,
        "ids_0913l": IDS_13L,
        "disjoint_from_0913l": True,
        "all_720_done_done": True,
        "wtl": wtl,
        "mean_margin": mean,
        "clone_n": 12,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [3.0, 24.0],
        "wool_360": {str(k): v for k, v in wool_360.items()},
        "wool_432": {str(k): v for k, v in wool_432.items()},
        "same_class_as_0913c": True,
        "same_class_note": "Same extra-animal family as 09-13c/09-13l: extra-animal 8c6s3g plus extra-animal YARN 6c11s plus extra-sheep 16s plus extra-goose/identical-clone. WTL 6-0-6 mean -1708.7 vs 09-13l 5-0-7 mean -3830.6. New window games are Brian Chua 108472548 extra-animal 8c6s3g and Andrey Shpigar extra-sheep win vs 6c6s6g. clone=12/12.",
        "loss_class": LOSS_CLASS,
        "worst_losses": [
            {
                "id": 108369265,
                "opp": "Ju",
                "margin": -17212.0,
                "herd_us": "9c5s",
                "herd_opp": "8c6s3g",
                "shops": ["SMOOTHIE_SHOP"],
                "clone": True,
                "sheep_us": [2, 196, 314],
            },
            {
                "id": 108432563,
                "opp": "wuwuwu",
                "margin": -10575.0,
                "herd_us": "6c11s",
                "herd_opp": "7c11s",
                "shops": ["YARN_STORE"],
                "clone": True,
                "sheep_us": [2, 151, 196, 218, 242, 266],
            },
            {
                "id": 108426937,
                "opp": "linyifangzhenshuai",
                "margin": -9514.0,
                "herd_us": "7c6s",
                "herd_opp": "8c6s3g",
                "shops": ["BRUNCH_SPOT"],
                "clone": True,
                "sheep_us": [2, 151, 196],
            },
        ],
        "not_227_242_266_wrap": True,
        "not_opening_broke": True,
        "not_freeze_after_day9_9c9s": True,
    }
    dump("20260913m_cut16_loss_class.json", loss_class)

    algo_note = {
        "date": "2026-09-13",
        "packet": "20260913m",
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
                "csv_0913i_team_score": 1696.4,
                "csv_0913j_team_score": 1692.8,
                "csv_0913k_team_score": 1688.5,
                "csv_0913l_team_score": 1692.2,
                "csv_0913m_team_score": 1693.4,
                "status": "COMPLETE",
            },
            "shopbag": {
                "submissionId": 56151155,
                "lineage": 55962761,
                "score_complete": 1332.1,
                "newer_than_cut16": True,
            },
            "newest_2": [56151155, 56151152],
            "rank_csv_0913m": 1981,
        },
        "cut16_live_failure_class": {
            "0913l": {
                "file": "experiments/20260913l_cut16_rolling.json",
                "ids": IDS_13L,
                "wtl": [5, 0, 7],
                "mean_margin": -3830.6,
                "class": "extra-goose 9c5s3g plus extra-animal YARN 6c11s plus extra-animal 8c6s3g plus extra-sheep 11s plus identical-clone",
            },
            "0913m": {
                "file": "experiments/20260913m_cut16_rolling.json",
                "ids": IDS,
                "wtl": wtl,
                "mean_margin": mean,
                "clone": "12/12",
                "class": "same extra-animal family: extra-animal 8c6s3g plus extra-animal YARN 6c11s plus extra-sheep 16s plus extra-goose/identical-clone",
                "heavy": [
                    {
                        "id": 108369265,
                        "opp": "Ju",
                        "margin": -17212,
                        "shops72": ["SMOOTHIE_SHOP"],
                        "buy": "9c5s vs 8c6s3g",
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
            },
        },
        "q1_reselect_after_216": {
            "licensed_this_fire": False,
            "note": "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. New public kernel aurax7/kaggriculture-shop-router-reactive-v4 writefile SHA 3dd123c5 is day-6 144/648 + Shop0909 712 overlay. Author lists otherwise unchanged.",
        },
    }
    dump("20260913m_algo_note.json", algo_note)

    prior_top = [
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
    ]
    brian = next(g for g in games if g["id"] == 108472548)
    packet = {
        "title": "Kaggriculture study packet 2026-09-13m",
        "not_the_0913l_packet": True,
        "no_upload": (
            "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1693.4 would drop without a >=1500 COMPLETE newest-2 partner "
            "(shopbag 56151155 COMPLETE 1332.1 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1693; re-upload is 600-provisional not a partner). "
            "No licensed later-block. Public search newest aurax7/kaggriculture-shop-router-reactive-v4 SHA 3dd123c5 day-6 144/648 + Shop0909 712 overlay. "
            "Do not reupload boatlee 55710781. Cut 12/13 Hold."
        ),
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913m/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913m/kaggriculture-publicleaderboard-2026-09-13T08-36-44.csv",
            "leaderboard_api": "experiments/20260913m_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913m",
            "top_replays": "artifacts/kaggle_runs/top_20260913m",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913m",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913m_gate.json",
            "episode_report": "experiments/20260913m_episode_report.json",
            "hunt_report": "experiments/20260913m_hunt_report.json",
            "algo_note": "experiments/20260913m_algo_note.json",
            "loss_class": "experiments/20260913m_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1693.4,
            "rank": 1981,
            "n_teams": 8849,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1332.1,
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
            "cut16_score": 1693.4,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2905.0,
            "rank10": {"team": "binghua", "score": 2968.1},
            "rank1": {"team": "Majkel1337", "score": 3221.5, "submissionId": 56156662},
            "public_cut16": {"n": 220, "wtl": [98, 2, 120], "mean_margin": -1024.1},
        },
        "rolling": {
            "previous": "experiments/20260913l_cut16_rolling.json",
            "live_cut16": "experiments/20260913m_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0913l": True,
            "n": 12,
            "wtl": wtl,
            "mean_margin": mean,
            "loss_class": LOSS_CLASS,
        },
        "brian_chua": {
            "id": 108472548,
            "margin": brian["margin"],
            "clone": True,
            "Q": brian["Q"],
            "land": brian["land"],
            "herd_us": "9c5s",
            "herd_opp": "8c6s3g",
            "sheep_steps_us": [2, 196, 314],
        },
        "top_board": {
            "source": "experiments/20260913m_top10_games.json",
            "not_copied_from": prior_top,
            "Majkel1337": {
                "land": [row["land"] for row in top],
                "herd": ["12c3s0g", "8c9s2g", "5c13s0g", "11c6s0g"],
                "wheat": [row["wheat"][0] for row in top],
                "shops": [row["shops72"][0] for row in top],
                "clone": "0_of_4",
                "episodes": [row["id"] for row in top],
                "note": (
                    "CSV #1 3221.5 live 3221.5 scoring sub 56156662. Ids disjoint from 20260913l Majkel set. "
                    "Mid-land 150 then 220-222 (all four 150/220/222), wheat 411-607, clone=0 on 4/4, goose mix 0g/2g/0g/0g. "
                    "Opening land is not a later-block license."
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
            "score": 1693.4,
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
                "Already live COMPLETE 1693.4. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                "Rolling 108369265 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -17212; "
                "108432563 already bought 218/242/266 sheep and lost YARN 6c11s -10575; "
                "108328160 already bought 227/242/266 sheep and lost extra-sheep 16s -8536. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: public search newest "
                "aurax7/kaggriculture-shop-router-reactive-v4 SHA 3dd123c5 day-6 144/648 + Shop0909 712 overlay; Yusuke 0911-simple still day-6; "
                "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1693 and keeps 1332."
            ),
        },
        "hunt": [AURAX],
    }
    dump("20260913m_study_packet.json", packet)
    print("top shops", [row["shops72"] for row in top])
    print("top land", [row["land"] for row in top])
    print("top wheat", [row["wheat"][0] for row in top])
    print("api gold21", api.get("gold21_csv"))
    print("api rank", api.get("heralces_csv"))


if __name__ == "__main__":
    main()
