"""Emit 20260913l study packet JSONs from live measurements. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLL = json.loads((ROOT / "experiments/20260913l_cut16_rolling.json").read_text(encoding="utf-8"))
API = json.loads((ROOT / "experiments/20260913l_public_leaderboard_api.json").read_text(encoding="utf-8"))
TOP = json.loads((ROOT / "experiments/20260913l_top10_games.json").read_text(encoding="utf-8"))

IDS = [g["id"] for g in ROLL["games"]]
PREV = [
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
    108273755,
    108270318,
]
LOSS = (
    "mixed extra-goose 9c5s3g (haonan zhengh 108412731 9c5s vs 9c5s3g clone=1 ICE_CREAM extra cow 218 extra sheep 227 extra geese 242/266 wheat 425 vs 17356 -18535) "
    "+ extra-animal YARN 6c11s (Peter Cnudde 108383915 6c11s vs 7c11s clone=1 YARN extra sheep 218/242/266 already bought -13315) "
    "+ extra-animal 8c6s3g (Wei Han 108445221 9c5s vs 8c6s3g clone=1 ICE_CREAM extra sheep 218/227 extra geese 242/266 wheat 426 vs 17329 -12688) "
    "+ extra-sheep 11s (Oleg Smirnov 108345614 9c8s vs 7c11s extra sheep 227/242/266 already bought -11762) "
    "+ extra-goose (Rafael Molina Castano 108377691 9c5s3g vs 9c5s4g extra geese 218/227/242 we already bought 227/242 -5101; "
    "CodeHacker 108349751 identical 9c5s3g extra geese 227/242 already bought -3571; "
    "Sophie555 108374873 9c5s3g vs 6c6s6g extra geese 227/242 already bought -3339). "
    "Wins: Igor Aranovsky 108326448 9c5s3g vs 9c9s +6833 extra geese 227/242 already bought; "
    "XiaoYan12 108441448 9c5s3g vs 6c6s6g +6450 extra geese 227/242 already bought; "
    "Floth 108343489 4c14s vs 8c6s3g +4018 extra sheep 218/242/266 already bought; "
    "wzyxp_123 108441305 identical 9c5s3g +2649 extra geese 227/242 already bought; "
    "Sean Peppers 108351144 4c15s vs 6c10s +2394 extra sheep 218/242/266 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: haonan lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; "
    "Wei Han lost 8c6s3g after opp extra sheep 218/227 extra geese 242/266; "
    "Peter already bought 218/242/266 and lost YARN 6c11s; Oleg already bought 227/242/266 and lost extra-sheep 11s; "
    "extra-goose losses/wins bought geese at 227/242 and sheep at 266; Floth already bought 218/242/266 and won vs 8c6s3g."
)
WOOL360 = {
    108445221: 1,
    108441448: 11,
    108441305: 37,
    108412731: 1,
    108383915: 237,
    108377691: 43,
    108374873: 11,
    108351144: 231,
    108349751: 43,
    108345614: 234,
    108343489: 231,
    108326448: 37,
}
WOOL432 = {
    108445221: 1,
    108441448: 1,
    108441305: 1,
    108412731: 1,
    108383915: 227,
    108377691: 1,
    108374873: 1,
    108351144: 158,
    108349751: 1,
    108345614: 231,
    108343489: 197,
    108326448: 1,
}
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1692.2 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1327.7 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1692; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Public search newest still "
    "crystalbaby/kaggriculture-v38-public-submission SHA a2047ebd Ahmed V38 Shop0909 144/648 + 288/712 overlay "
    "(already rejected 0913b). Do not reupload boatlee 55710781. Cut 12/13 Hold."
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
    wins = sum(1 for g in games if g["win"])
    ties = sum(1 for g in games if g["tie"])
    losses = sum(1 for g in games if not g["win"] and not g["tie"])
    wtl = [wins, ties, losses]
    margins = [float(g["margin"]) for g in games]
    mean_margin = round(sum(margins) / len(margins), 1)
    wei = next(g for g in games if g["id"] == 108445221)
    haonan = next(g for g in games if g["id"] == 108412731)
    peter = next(g for g in games if g["id"] == 108383915)
    majkel = [g for g in TOP if g["team"] == "Majkel1337"]
    clone_n = sum(1 for g in games if g["clone"])
    cash24 = [float(g["cash_24"]) for g in games]
    cut16 = API["cut16"]
    her = API["heralces_csv"]
    gold21 = float(API["gold21_csv"]["score"])
    rank10_score = float(API["rank10"]["score"])
    rank1_score = float(API["rank1"]["score"])
    n_teams = int(API["n"])
    rank = int(her["rank"])
    team_score = 1692.2
    shopbag_score = 1327.7

    hunt_report = {
        "date": "2026-09-13",
        "packet": "20260913l",
        "kernels_not_in_0913k_packet": False,
        "no_upload": True,
        "no_kaggle_submit": True,
        "cells_executed": False,
        "extracted_later_block_agent": False,
        "later_block_python_after_216": False,
        "any_licensed_for_extract": False,
        "licensed_kernel": None,
        "root_main_py": "unchanged",
        "hunt_dir": "artifacts/public_sources/_hunt_20260913l",
        "inspect_scripts": ["experiments/candidates/scan_hunt_20260913l.py"],
        "python": r"D:\kaggle\kaggriculture\.venv\Scripts\python.exe",
        "payload_decode": "none_no_new_notebook",
        "compare_0913k": {
            "hunt_dir": "artifacts/public_sources/_hunt_20260913k",
            "hunt_report": "experiments/20260913k_hunt_report.json",
            "gate": "experiments/20260913k_gate.json",
            "note": (
                "No new slug vs _hunt_20260913k. Public search newest is still crystalbaby/kaggriculture-v38-public-submission "
                "(lastRunTime 2026-09-13 04:15:33). Did not re-pull rejected kernels (crystalbaby V38, Ahmed V39/V38, prvsiyan market-ledger, "
                "timed-six-cow, lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, "
                "melomanpanda, zhincez, y3uanm rollback-v20)."
            ),
        },
        "public_search_newest": "crystalbaby/kaggriculture-v38-public-submission",
        "public_search_newest_lastRunTime": "2026-09-13 04:15:33.700000",
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
        "packet": "20260913l",
        "freeze": False,
        "hold": True,
        "candidate": None,
        "clone_g5_run": False,
        "extracted_later_block_agent": False,
        "cells_executed": False,
        "rejected": [
            {
                "kernel": "crystalbaby/kaggriculture-v38-public-submission",
                "verdict": "reject_v38_reprint",
                "note": "Still public-search newest 2026-09-13 04:15:33. 0913k already rejected SHA a2047ebd Ahmed V38 Shop0909 144/648 + 288/712 overlay. Did not re-pull.",
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
                "note": "Author list 2026-09-13l: still newest Yusuke kaggriculture kernel (2026-09-11 08:38). Day-6 144/648. Did not re-pull.",
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
            "Prior losses stand. Extra-goose / extra-animal YARN 6c11s / extra-animal 8c6s3g / extra-sheep 11s is not a milk-heavy license. Did not re-screen."
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
                "score_complete": team_score,
                "sha256": "26ffba52",
            },
            "shopbag": {"submissionId": 56151155, "score_complete": shopbag_score, "newer_than_cut16": True},
        },
        "upload_bail": True,
        "hunt_dir": "artifacts/public_sources/_hunt_20260913l",
        "hunt_report": "experiments/20260913l_hunt_report.json",
        "named_kernels_scanned": [],
        "author_list_no_new_later_block": [
            "yhay81/shop-router-0911-simple",
            "yamakawanin/king-v4e-rc4",
            "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
            "y3uanm/kaggriculture-conservative-market-router-v5",
            "y3uanm/kaggriculture-safe-baseline-rollback-v20",
        ],
        "why": (
            "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1692.2 partnered with newer shopbag 56151155 COMPLETE 1327.7 < 1500. "
            "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). Pairing a new cut with cut 16 "
            "would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
            "No new public slug this fire vs _hunt_20260913k. Public search newest still crystalbaby/kaggriculture-v38-public-submission writefile SHA a2047ebd Ahmed V38 reprint (already rejected). "
            "Yusuke/king/Thomas/y3uanm author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. "
            "Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. 227/242/266 wrap not licensed: "
            "haonan lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; Wei Han lost 8c6s3g after opp extra sheep 218/227 extra geese 242/266; "
            "Peter already bought 218/242/266 and lost YARN 6c11s; Oleg already bought 227/242/266 and lost extra-sheep 11s; extra-goose games bought geese at 227/242 and sheep at 266."
        ),
    }

    episode_report = {
        "date": "2026-09-13",
        "packet": "20260913l",
        "utc": "2026-09-13T06:38:36Z",
        "no_upload": True,
        "upload_bail": True,
        "hold": True,
        "root_main_py_untouched": True,
        "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
        "boatlee_55710781_reupload": False,
        "live_newest_id": 56151152,
        "live_newest_score": team_score,
        "live_newest_status": "COMPLETE",
        "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
        "live_newest_note": (
            "COMPLETE 1692.2 (was 1688.5). Newest public 108445221 updatedScore 1692.215. Newest-2 = shopbag reupload 56151155 "
            "(newer id, submissions 1327.7 / ListEpisodes last_updated 1327.8) + cut 16 56151152. Upload-bail TRUE (c): shopbag partner "
            "1327.7 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
        ),
        "cut15_id": 56146106,
        "cut15_score": 1864.4,
        "cut15_status": "COMPLETE",
        "cut15_note": "DROPPED from newest-2.",
        "shopbag_id": 56151155,
        "shopbag_score": shopbag_score,
        "shopbag_status": "COMPLETE",
        "shopbag_lineage": 55962761,
        "newest_2": [56151155, 56151152],
        "heralces_rank_csv": rank,
        "heralces_score": team_score,
        "n_teams_csv": n_teams,
        "public_56151152": {
            "n_public": cut16["n_public"],
            "n_validation": cut16["n_validation"],
            "n_completed_public": cut16["n_public"],
            "wtl": cut16["wtl"],
            "mean_margin": cut16["mean_margin"],
            "status": "COMPLETE",
            "publicScore": team_score,
        },
        "rolling_ids": IDS,
        "rolling_forbidden_0913k": PREV,
        "ids_not_identical_to_0913k": True,
        "ids_disjoint_from_0913k": True,
        "rolling_n": 12,
        "rolling_n_steps": 720,
        "wtl": wtl,
        "mean_margin": mean_margin,
        "rolling_note": (
            "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 DONE/DONE. Disjoint from 20260913k packet. "
            "5W 7L. Worst haonan zhengh 108412731 L -18535 9c5s vs 9c5s3g clone=1 extra cow 218 extra sheep 227 extra geese 242/266. "
            "New-window Wei Han 108445221 L -12688 9c5s vs 8c6s3g extra sheep 218/227 extra geese 242/266. "
            "Peter Cnudde 108383915 L -13315 6c11s vs 7c11s YARN extra sheep 218/242/266 already bought. Not opening-broke. Not freeze 9c9s."
        ),
    }

    loss_class = {
        "date": "2026-09-13",
        "packet": "20260913l",
        "live": "yamakawanin king-v4e-rc4",
        "submission": 56151152,
        "team": "heralces",
        "ids": IDS,
        "ids_0913k": PREV,
        "disjoint_from_0913k": True,
        "all_720_done_done": True,
        "wtl": wtl,
        "mean_margin": mean_margin,
        "clone_n": clone_n,
        "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
        "cash_24_range": [min(cash24), max(cash24)],
        "wool_360": {str(k): v for k, v in WOOL360.items()},
        "wool_432": {str(k): v for k, v in WOOL432.items()},
        "same_class_as_0913c": True,
        "same_class_note": (
            "Same extra-animal family as 09-13c/09-13k: extra-goose 9c5s3g plus extra-animal YARN 6c11s plus extra-animal 8c6s3g plus extra-sheep 11s plus identical-clone. "
            "WTL 5-0-7 mean -3830.6 vs 09-13k 6-0-6 mean -2447.2. New window games are Wei Han 108445221 extra-animal 8c6s3g, XiaoYan12 extra-goose win, wzyxp identical extra-goose win. clone=12/12."
        ),
        "loss_class": LOSS,
        "worst_losses": [
            {
                "id": 108412731,
                "opp": "haonan zhengh",
                "margin": -18535.0,
                "herd_us": "9c5s",
                "herd_opp": "9c5s3g",
                "shops": ["ICE_CREAM_SHOP"],
                "clone": True,
                "sheep_us": sheep_steps(haonan),
            },
            {
                "id": 108383915,
                "opp": "Peter Cnudde",
                "margin": -13315.0,
                "herd_us": "6c11s",
                "herd_opp": "7c11s",
                "shops": ["YARN_STORE"],
                "clone": True,
                "sheep_us": sheep_steps(peter),
            },
            {
                "id": 108445221,
                "opp": "Wei Han",
                "margin": -12688.0,
                "herd_us": "9c5s",
                "herd_opp": "8c6s3g",
                "shops": ["ICE_CREAM_SHOP"],
                "clone": True,
                "sheep_us": sheep_steps(wei),
            },
        ],
        "not_227_242_266_wrap": True,
        "not_opening_broke": True,
        "not_freeze_after_day9_9c9s": True,
    }

    algo_note = {
        "date": "2026-09-13",
        "packet": "20260913l",
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
                "csv_0913l_team_score": team_score,
                "status": "COMPLETE",
            },
            "shopbag": {
                "submissionId": 56151155,
                "lineage": 55962761,
                "score_complete": shopbag_score,
                "newer_than_cut16": True,
            },
            "newest_2": [56151155, 56151152],
            "rank_csv_0913l": rank,
        },
        "cut16_live_failure_class": {
            "0913k": {
                "file": "experiments/20260913k_cut16_rolling.json",
                "ids": PREV,
                "wtl": [6, 0, 6],
                "mean_margin": -2447.2,
                "class": "extra-animal 8c6s3g plus extra-animal YARN 6c11s plus extra-sheep 16s plus extra-goose/identical-clone",
            },
            "0913l": {
                "file": "experiments/20260913l_cut16_rolling.json",
                "ids": IDS,
                "wtl": wtl,
                "mean_margin": mean_margin,
                "clone": f"{clone_n}/12",
                "class": "same extra-animal family: extra-goose 9c5s3g plus extra-animal YARN 6c11s plus extra-animal 8c6s3g plus extra-sheep 11s plus identical-clone",
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
                        "id": 108445221,
                        "opp": "Wei Han",
                        "margin": -12688,
                        "shops72": ["ICE_CREAM_SHOP"],
                        "buy": "9c5s vs 8c6s3g",
                        "opp216": [218, 227, 242, 266],
                        "wool_px_360": 1,
                    },
                ],
            },
        },
        "q1_reselect_after_216": {
            "licensed_this_fire": False,
            "note": (
                "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. Public search newest still "
                "crystalbaby/kaggriculture-v38-public-submission (V38 writefile SHA a2047ebd) Shop0909 144/648 + 288/712 overlay. Author lists unchanged."
            ),
        },
    }

    packet = {
        "title": "Kaggriculture study packet 2026-09-13l",
        "not_the_0913k_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913l/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260913l/kaggriculture-publicleaderboard-2026-09-13T06-38-36.csv",
            "leaderboard_api": "experiments/20260913l_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913l",
            "top_replays": "artifacts/kaggle_runs/top_20260913l",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913l",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913l_gate.json",
            "episode_report": "experiments/20260913l_episode_report.json",
            "hunt_report": "experiments/20260913l_hunt_report.json",
            "algo_note": "experiments/20260913l_algo_note.json",
            "loss_class": "experiments/20260913l_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": team_score,
            "rank": rank,
            "n_teams": n_teams,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": shopbag_score,
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
            "cut16_score": team_score,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": gold21,
            "rank10": {"team": API["rank10"]["team"], "score": rank10_score},
            "rank1": {
                "team": "Majkel1337",
                "score": rank1_score,
                "submissionId": 56156662,
            },
            "public_cut16": {
                "n": cut16["n_public"],
                "wtl": cut16["wtl"],
                "mean_margin": cut16["mean_margin"],
            },
        },
        "rolling": {
            "previous": "experiments/20260913k_cut16_rolling.json",
            "live_cut16": "experiments/20260913l_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0913k": True,
            "n": 12,
            "wtl": wtl,
            "mean_margin": mean_margin,
            "loss_class": LOSS,
        },
        "wei_han": {
            "id": 108445221,
            "margin": -12688.0,
            "clone": True,
            "Q": wei["Q"],
            "land": wei["land"],
            "herd_us": herd(wei["buy_us"]),
            "herd_opp": herd(wei["buy_opp"]),
            "sheep_steps_us": sheep_steps(wei),
        },
        "top_board": {
            "source": "experiments/20260913l_top10_games.json",
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
            ],
            "Majkel1337": {
                "land": [row["land"] for row in majkel],
                "herd": [row["herd"] for row in majkel],
                "wheat": [row["wheat"][0] for row in majkel],
                "shops": [row["shops72"][0] for row in majkel],
                "clone": "0_of_4",
                "episodes": [row["id"] for row in majkel],
                "note": (
                    "CSV #1 3220.0 live 3220.0 scoring sub 56156662. Ids disjoint from 20260913k Majkel set. "
                    "Mid-land 150 then 218-222 (two 150/218/220/222; two 150/220/222), wheat 333-598, clone=0 on 4/4, "
                    "goose mix 4g/2g/0g/2g. Opening land is not a later-block license."
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
            "score": team_score,
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
                "Already live COMPLETE 1692.2. This cycle Hold: upload-bail (c) plus no new licensed later-block. Extra sheep 226/241/265 not 227/242/266. "
                "Rolling 108412731 already faced opp extra cow 218 extra sheep 227 extra geese 242/266 9c5s3g -18535; "
                "108445221 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g -12688; "
                "108383915 already bought 218/242/266 sheep and lost YARN 6c11s -13315; "
                "108345614 already bought 227/242/266 sheep and lost extra-sheep 11s -11762. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: public search newest still "
                "crystalbaby/kaggriculture-v38-public-submission SHA a2047ebd Ahmed V38 Shop0909 144/648 + 288/712 overlay; Yusuke 0911-simple still day-6; no king rc5 / y3uanm v6 / Thomas tree "
                "that actually splits after 216. Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1692 and keeps 1327."
            ),
        },
        "hunt": [],
    }

    outs = {
        "experiments/20260913l_hunt_report.json": hunt_report,
        "experiments/20260913l_gate.json": gate,
        "experiments/20260913l_episode_report.json": episode_report,
        "experiments/20260913l_cut16_loss_class.json": loss_class,
        "experiments/20260913l_algo_note.json": algo_note,
        "experiments/20260913l_study_packet.json": packet,
    }
    for rel, payload in outs.items():
        path = ROOT / rel
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print("WROTE", path)
    print("wei", wei["id"], herd(wei["buy_us"]), sheep_steps(wei))
    print("haonan", haonan["id"], herd(haonan["buy_us"]))
    print("peter", peter["id"], herd(peter["buy_us"]))
    print("majkel_ids", [m["id"] for m in majkel])
    print("disjoint", set(IDS).isdisjoint(PREV))
    print("wtl", wtl, "mean", mean_margin)


if __name__ == "__main__":
    main()
