"""Write 20260913p packet JSON (no upload, no cell exec)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDS = [
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
    108374873,
    108351144,
]
IDS_13O = [
    108504670,
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
    108343489,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (Excluding 108520439 7c6s vs 8c6s3g clone=1 FARMERS_MARKET extra sheep 218/227 extra geese 242/266 wheat 497 vs 17446 -5345; "
    "Wei Han 108445221 9c5s vs 8c6s3g ICE_CREAM extra sheep 218/227 extra geese 242/266 -12688) "
    "+ extra-goose 9c5s vs 9c5s3g (haonan zhengh 108412731 extra cow 218 extra sheep 227 extra geese 242/266 -18535) "
    "+ extra-animal YARN 6c11s (Peter Cnudde 108383915 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought -13315) "
    "+ extra-sheep 4c15s (Hackoholics 108509931 4c15s vs 6c10s extra sheep 218/242/266 already bought -4788) "
    "+ extra-goose 9c5s3g (Rafael Molina Castano 108377691 vs 9c5s4g extra geese 227/242 already bought -5101; "
    "Sophie555 108374873 vs 6c6s6g extra geese 227/242 already bought -3339) "
    "+ identical-clone extra-goose (mmwstudy 108484081 9c5s3g vs 9c5s3g extra geese 227/242 already bought -65). "
    "Wins: XiaoYan12 108441448 9c5s3g vs 6c6s6g +6450 extra geese 227/242 already bought; "
    "Agentmaster 108489181 9c5s3g vs 9c5s4g +2699 extra geese 227/242 already bought; "
    "wzyxp_123 108441305 9c5s3g vs 9c5s3g +2649 extra geese 227/242 already bought; "
    "Sean Peppers 108351144 4c15s vs 6c10s +2394 extra sheep 218/242/266 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Excluding/Wei Han/haonan lost extra-animal after opp extra sheep 218/227 extra geese 242/266; "
    "Peter already bought 218/242/266 and lost YARN 6c11s; Hackoholics already bought 218/242/266 and lost extra-sheep 15s; "
    "mmwstudy already bought 227/242/266 (geese/sheep) and lost identical-clone -65; "
    "XiaoYan/Agentmaster/wzyxp already bought extra geese 227/242 and won; Sean already bought extra sheep 218/242/266 and won."
)
GURU_V39 = {
    "kernel": "guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f",
    "path": "artifacts/public_sources/_hunt_20260913p/guruprasaathas111__kaggriculture-master-engine-v53e01d74d8f/kaggriculture-master-engine-v53e01d74d8f.ipynb",
    "verdict": "reject_v39_reprint_shop0909_overlay",
    "sha256": "708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8",
    "note": (
        "New slug vs _hunt_20260913o (lastRunTime 2026-09-13 11:25:11; public-search newest by dateCreated). "
        "Python %%writefile main.py SHA 708c7485... same as already-rejected ahmedberatozer V39-ready-before-the-rush / notebookda72f457f5. "
        "Archive cell names submission_competitive_v39.tar.gz. day6 at 144, day27 at 648, E182 Shop0909 last-seven-turn 712 planner. "
        "216<=step<=227 is milk-shop livestock sub, not a farm/route reselect. 288 sales-first / R37 horizon overlay. "
        "Distinct from cut14 acf7c664, cut15 b87a27ed, cut16 26ffba52. No ctypes/agent.so. Cells not executed. "
        "Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
    ),
}


def dump(name: str, obj: object) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260913p_cut16_rolling.json").read_text(encoding="utf-8"))
    games = rolling["games"]
    top = json.loads((ROOT / "experiments/20260913p_top10_games.json").read_text(encoding="utf-8"))
    api = json.loads((ROOT / "experiments/20260913p_public_leaderboard_api.json").read_text(encoding="utf-8"))
    assert [g["id"] for g in games] == IDS
    wtl = [4, 0, 8]
    mean = -4082.0
    wool_360 = {
        108520439: 1,
        108509931: 231,
        108489181: 43,
        108484081: 37,
        108445221: 1,
        108441448: 11,
        108441305: 37,
        108412731: 1,
        108383915: 237,
        108377691: 43,
        108374873: 11,
        108351144: 231,
    }
    wool_432 = {
        108520439: 5,
        108509931: 158,
        108489181: 1,
        108484081: 125,
        108445221: 1,
        108441448: 1,
        108441305: 1,
        108412731: 1,
        108383915: 227,
        108377691: 1,
        108374873: 1,
        108351144: 158,
    }

    hunt_report = {
        "date": "2026-09-13",
        "packet": "20260913p",
        "kernels_not_in_0913o_packet": True,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260913p",
        "inspect_scripts": [
            "experiments/candidates/inspect_hunt_20260913p.py",
            "experiments/candidates/scan_hunt_20260913p.py",
        ],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_writefile_dumped_for_sha_only",
        "compare_0913o": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260913o",
            "hunt_report": "experiments/20260913o_hunt_report.json",
            "gate": "experiments/20260913o_gate.json",
            "note": "New slug guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f vs yhay81/shop-router-0913 and wei111111/v46d-skill-rebuild-review-guide in _hunt_20260913o. Did not re-pull rejected kernels (yhay81 0913, wei v46d review, Ahmed V39 v39-ready-before-the-rush, aurax7 v4, crystalbaby V38, Ahmed V39 notebookda72f457f5, prvsiyan market-ledger, timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple).",
        },
        "public_search_newest": "guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f",
        "public_search_newest_lastRunTime": "2026-09-13 11:25:11.587000",
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
        "named_kernels_scanned": [
            "guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f",
        ],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "author_list_note": "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6.",
        "hunt": [GURU_V39],
    }
    dump("20260913p_hunt_report.json", hunt_report)

    gate = {
        "date": "2026-09-13",
        "packet": "20260913p",
        "freeze": False,
        "hold": True,
        "candidate": None,
        "clone_g5_run": False,
        "extracted_later_block_agent": False,
        "cells_executed": False,
        "rejected": [
            GURU_V39,
            {
                "kernel": "yhay81/shop-router-0913",
                "verdict": "reject_day6_144_648",
                "note": "Still a public search hit. 0913o already rejected SHA 77cf6772 day-6 144/648. Did not re-pull.",
            },
            {
                "kernel": "wei111111/v46d-skill-rebuild-review-guide",
                "verdict": "reject_analysis_review_guide",
                "note": "Re-ran 2026-09-13 11:23:54 vs 0913o 10:33:54. Same analysis slug, no writefile agent. Did not re-pull.",
            },
            {
                "kernel": "ahmedberatozer/kaggriculture-v39-ready-before-the-rush",
                "verdict": "reject_v39_reprint_shop0909_overlay",
                "note": "0913n already rejected SHA 708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay. Same SHA as this cycle's guruprasaathas slug. Did not re-pull.",
            },
            {
                "kernel": "aurax7/kaggriculture-shop-router-reactive-v4",
                "verdict": "reject_day6_144_648_and_712_overlay",
                "note": "Still a public search hit. 0913m already rejected SHA 3dd123c5 day-6 144/648 + Shop0909 712 overlay. Did not re-pull.",
            },
            {
                "kernel": "crystalbaby/kaggriculture-v38-public-submission",
                "verdict": "reject_v38_reprint",
                "note": "Still a public search hit. 0913l already rejected SHA a2047ebd Ahmed V38 Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
            },
            {
                "kernel": "ahmedberatozer/notebookda72f457f5",
                "verdict": "reject_v39_shop0909_overlay",
                "note": "Still a public search hit. 0913e already rejected SHA 708c7485. Did not re-pull.",
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
                "note": "Superseded on author list by shop-router-0913. Day-6 144/648. Did not re-pull.",
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
        "cut12_13_note": "No new recorded-seat flipping evidence vs Deskbo 105744091 AND Stefano 105798735 or fufu 105790145. Prior losses stand. Extra-animal 8c6s3g / YARN 6c11s / extra-sheep 15s / extra-goose is not a milk-heavy license. Did not re-screen.",
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
                "score_complete": 1682.9,
                "sha256": "26ffba52",
            },
            "shopbag": {
                "submissionId": 56151155,
                "score_complete": 1328.0,
                "newer_than_cut16": True,
            },
        },
        "upload_bail": True,
        "hunt_dir": "artifacts/public_sources/_hunt_20260913p",
        "hunt_report": "experiments/20260913p_hunt_report.json",
        "named_kernels_scanned": [
            "guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f",
        ],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0913",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "why": (
            "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1682.9 partnered with newer shopbag 56151155 COMPLETE 1328.0 < 1500. "
            "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
            "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
            "New public slug guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f writefile SHA 708c7485 is Ahmed V39 reprint Shop0909 144/648 + 288/712 overlay, not a later-block. "
            "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. Root main.py SHA untouched. "
            "Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. 227/242/266 wrap not licensed: Excluding lost extra-animal 8c6s3g after opp extra sheep 218/227 extra geese 242/266; "
            "Peter already bought 218/242/266 and lost YARN 6c11s; Hackoholics already bought 218/242/266 and lost extra-sheep 15s; mmwstudy already bought 227/242/266 (geese/sheep) and lost identical-clone -65."
        ),
    }
    dump("20260913p_gate.json", gate)

    episode_report = {
        "date": "2026-09-13",
        "packet": "20260913p",
        "utc": "2026-09-13T11:37:05Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": 1682.9,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": (
            "COMPLETE 1682.9 (was 1690.5). Newest public 108520439 updatedScore 1682.943. "
            "Newest-2 = shopbag reupload 56151155 (newer id, submissions 1328.0 / ListEpisodes last_updated 1328.025) + cut 16 56151152. "
            "Upload-bail TRUE (c): shopbag partner 1328.0 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
        ),
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": 1328.0,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": 1999,
        "heralces_score": 1682.9,
        "n_teams_csv": 8878,
        "public_56151152": {
            "n_public": 225,
            "n_validation": 1,
            "n_completed_public": 225,
            "wtl": [99, 2, 124],
            "mean_margin": -1043.2,
            "status": "COMPLETE",
            "publicScore": 1682.9,
        },
        "rolling_ids": IDS,
        "rolling_forbidden_0913o": IDS_13O,
        "ids_not_identical_to_0913o": True,
        "ids_disjoint_from_0913o": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": wtl,
        "mean_margin": mean,
        "rolling_note": (
            "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913o packet. 4W 8L. "
            "Worst haonan zhengh 108412731 L -18535 9c5s vs 9c5s3g clone=1 extra cow 218 extra sheep 227 extra geese 242/266. "
            "New-window Excluding 108520439 L -5345 7c6s vs 8c6s3g extra sheep 218/227 extra geese 242/266; "
            "Hackoholics 108509931 L -4788 4c15s vs 6c10s extra sheep 218/242/266 already bought. Not opening-broke. Not freeze 9c9s."
        ),
    }
    dump("20260913p_episode_report.json", episode_report)

    loss_class = {
        "date": "2026-09-13",
        "packet": "20260913p",
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": IDS,
        "ids_0913o": IDS_13O,
        "disjoint_from_0913o": True,
        "all_720_done_done": True,
        "wtl": wtl,
        "mean_margin": mean,
        "clone_n": 12,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [3.0, 27.0],
        "wool_360": {str(k): v for k, v in wool_360.items()},
        "wool_432": {str(k): v for k, v in wool_432.items()},
        "same_class_as_0913c": True,
        "same_class_note": "Same extra-animal family as 09-13c/09-13o: extra-animal 8c6s3g plus extra-goose plus extra-animal YARN 6c11s plus extra-sheep 15s plus identical-clone extra-goose. WTL 4-0-8 mean -4082.0 vs 09-13o 6-0-6 mean -910.7. New window games are Excluding 108520439 extra-animal 8c6s3g -5345 and Hackoholics 108509931 extra-sheep 15s -4788. clone=12/12.",
        "loss_class": LOSS_CLASS,
        "worst_losses": [
            {
                "id": 108412731,
                "opp": "haonan zhengh",
                "margin": -18535.0,
                "herd_us": "9c5s",
                "herd_opp": "9c5s3g",
                "shops": ["ICE_CREAM_SHOP"],
                "clone": True,
                "sheep_us": [2, 196, 314],
            },
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
                "id": 108445221,
                "opp": "Wei Han",
                "margin": -12688.0,
                "herd_us": "9c5s",
                "herd_opp": "8c6s3g",
                "shops": ["ICE_CREAM_SHOP"],
                "clone": True,
                "sheep_us": [2, 196, 314],
            },
        ],
        "not_227_242_266_wrap": True,
        "not_opening_broke": True,
        "not_freeze_after_day9_9c9s": True,
    }
    dump("20260913p_cut16_loss_class.json", loss_class)

    algo_note = {
        "date": "2026-09-13",
        "packet": "20260913p",
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
                "csv_0913n_team_score": 1693.6,
                "csv_0913o_team_score": 1690.5,
                "csv_0913p_team_score": 1682.9,
                "status": "COMPLETE",
            },
            "shopbag": {
                "submissionId": 56151155,
                "lineage": 55962761,
                "score_complete": 1328.0,
                "newer_than_cut16": True,
            },
            "newest_2": [56151155, 56151152],
            "rank_csv_0913p": 1999,
        },
        "cut16_live_failure_class": {
            "0913o": {
                "file": "experiments/20260913o_cut16_rolling.json",
                "ids": IDS_13O,
                "wtl": [6, 0, 6],
                "mean_margin": -910.7,
                "class": "extra-animal 8c6s3g plus extra-animal YARN 6c11s plus identical-clone extra-goose",
            },
            "0913p": {
                "file": "experiments/20260913p_cut16_rolling.json",
                "ids": IDS,
                "wtl": wtl,
                "mean_margin": mean,
                "clone": "12/12",
                "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-animal YARN 6c11s plus extra-sheep 15s plus identical-clone extra-goose",
                "heavy": [
                    {
                        "id": 108412731,
                        "opp": "haonan zhengh",
                        "margin": -18535,
                        "shops72": ["ICE_CREAM_SHOP"],
                        "buy": "9c5s vs 9c5s3g",
                        "opp216": [218, 227, 242, 266],
                        "wool_px_360": 1,
                    },
                    {
                        "id": 108383915,
                        "opp": "Peter Cnudde",
                        "margin": -13315,
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
            "note": "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. New public kernel guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f writefile SHA 708c7485 is Ahmed V39 reprint day-6 144/648 + Shop0909 712 overlay. Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block).",
        },
    }
    dump("20260913p_algo_note.json", algo_note)

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
        "experiments/20260913m_top10_games.json",
        "experiments/20260913n_top10_games.json",
        "experiments/20260913o_top10_games.json",
    ]
    excl = next(g for g in games if g["id"] == 108520439)
    packet = {
        "title": "Kaggriculture study packet 2026-09-13p",
        "not_the_0913o_packet": True,
        "no_upload": (
            "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1682.9 would drop without a >=1500 COMPLETE newest-2 partner "
            "(shopbag 56151155 COMPLETE 1328.0 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1682; re-upload is 600-provisional not a partner). "
            "No licensed later-block. New slug guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f SHA 708c7485 V39 reprint Shop0909 144/648. "
            "Do not reupload boatlee 55710781. Cut 12/13 Hold."
        ),
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913p/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913p/kaggriculture-publicleaderboard-2026-09-13T11-37-05.csv",
            "leaderboard_api": "experiments/20260913p_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913p",
            "top_replays": "artifacts/kaggle_runs/top_20260913p",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913p",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913p_gate.json",
            "episode_report": "experiments/20260913p_episode_report.json",
            "hunt_report": "experiments/20260913p_hunt_report.json",
            "algo_note": "experiments/20260913p_algo_note.json",
            "loss_class": "experiments/20260913p_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1682.9,
            "rank": 1999,
            "n_teams": 8878,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1328.0,
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
            "cut16_score": 1682.9,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2919.9,
            "rank10": {"team": "binghua", "score": 2968.7},
            "rank1": {"team": "Majkel1337", "score": 3235.1, "submissionId": 56156662},
            "public_cut16": {"n": 225, "wtl": [99, 2, 124], "mean_margin": -1043.2},
        },
        "rolling": {
            "previous": "experiments/20260913o_cut16_rolling.json",
            "live_cut16": "experiments/20260913p_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0913o": True,
            "n": 12,
            "wtl": wtl,
            "mean_margin": mean,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": 108520439,
            "margin": excl["margin"],
            "clone": True,
            "Q": excl["Q"],
            "land": excl["land"],
            "herd_us": "7c6s",
            "herd_opp": "8c6s3g",
            "sheep_steps_us": [2, 151, 196],
        },
        "top_board": {
            "source": "experiments/20260913p_top10_games.json",
            "not_copied_from": prior_top,
            "Majkel1337": {
                "land": [row["land"] for row in top],
                "herd": [row["herd"] for row in top],
                "wheat": [row["wheat"][0] for row in top],
                "shops": [row["shops72"][0] for row in top],
                "clone": "0_of_4",
                "episodes": [row["id"] for row in top],
                "note": (
                    "CSV #1 3235.1 live 3235.1 scoring sub 56156662. Ids disjoint from 20260913o Majkel set. "
                    "Mid-land 150 then 218-222 (three 150/220/222; one 150/218/220/222), wheat 387-452, clone=0 on 4/4, goose mix 0g/0g/0g/4g. "
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
            "score": 1682.9,
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
                "Already live COMPLETE 1682.9. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                "Rolling 108412731 already faced opp extra cow 218 extra sheep 227 extra geese 242/266 9c5s3g -18535; "
                "108383915 already bought 218/242/266 sheep and lost YARN 6c11s -13315; "
                "108520439 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -5345. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: new slug "
                "guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f SHA 708c7485 V39 reprint Shop0909 144/648; "
                "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1682 and keeps 1328."
            ),
        },
        "hunt": [GURU_V39],
    }
    dump("20260913p_study_packet.json", packet)
    print("top shops", [row["shops72"] for row in top])
    print("top land", [row["land"] for row in top])
    print("top wheat", [row["wheat"][0] for row in top])
    print("api gold21", api.get("gold21_csv"))
    print("api rank", api.get("heralces_csv"))


if __name__ == "__main__":
    main()
