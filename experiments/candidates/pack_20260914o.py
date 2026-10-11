"""Write 20260914o packet JSON from live measurements. No upload."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV_14N = [
    108930713,
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
]
IDS = [
    108944173,
    108941028,
    108910147,
    108889446,
    108889378,
    108851261,
    108822458,
    108817790,
    108787437,
    108762693,
    108741805,
    108723413,
]
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (Floth 108944173 9c5s vs 8c6s3g PET_CAFE extra sheep 314 vs opp extra sheep 218/227 extra geese 242/266 -1793; "
    "HaoChi 108817790 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -6212; "
    "\u0438\u0442\u043c\u043e\u043d\u044f\u044f\u044f 108762693 10c8s vs 8c6s3g PET_CAFE extra cow 218 extra sheep 227/242/266 already bought vs opp extra sheep 218/227 extra geese 242/266 -6320) "
    "+ extra-goose (LaiCxm 108851261 9c5s vs 9c5s3g PIZZA extra cow 218 extra sheep 227 extra geese 242/266 -16092; "
    "Toru59er 108787437 9c5s vs 9c5s3g ICE_CREAM extra cow 218 extra sheep 227 extra geese 242/266 -6986) "
    "+ identical-clone extra-sheep (\u0412\u0430\u0440\u0438\u043c \u0441\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0441\u0430\u043c\u043e\u0433\u043e\u043d 108889446 6c11s vs 6c11s YARN extra sheep 218/242/266 already bought -12131) "
    "+ extra-sheep (Revanth Tambisetty 108822458 4c15s vs 6c11s SMOOTHIE extra sheep 218/242/266 already bought -11033; "
    "Adhiraj Jagtap 108889378 6c11s vs 9c9s YARN extra sheep 218/242/266 already bought -2087). "
    "Wins: \u7ea2\u70e7\u8089 108910147 9c5s3g vs 9c6s3g BAKERY +3039 extra geese 227/242 already bought vs opp extra sheep 218/227 extra geese 242/266; "
    "zard599 108723413 9c5s3g vs 9c5s4g BAKERY +748 extra geese 227/242 already bought vs opp extra geese 218/227/242 extra sheep 266; "
    "Yiwei Pu 108941028 9c5s3g vs 9c5s3g +106 identical-clone extra geese 227/242 already bought; "
    "y3uanm 108741805 9c5s3g vs 9c5s3g +54 identical-clone extra geese 227/242 already bought. "
    "clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: \u0438\u0442\u043c\u043e\u043d\u044f\u044f\u044f already bought extra sheep 227/242/266 and lost vs 8c6s3g; "
    "\u0412\u0430\u0440\u0438\u043c already bought extra sheep 218/242/266 and lost identical-clone 11s; "
    "Revanth already bought extra sheep 218/242/266 and lost 15s vs 11s; "
    "Adhiraj already bought extra sheep 218/242/266 and lost vs 9c9s; "
    "LaiCxm/Toru59er lost extra-goose after opp extra cow 218 extra sheep 227 extra geese 242/266; "
    "Floth did not buy extra sheep 227/242/266 and lost vs 8c6s3g; "
    "Yiwei/y3uanm already bought extra geese 227/242 and won identical-clone; "
    "\u7ea2\u70e7\u8089 already bought extra geese 227/242 and won vs extra-sheep 6s; "
    "zard599 already bought extra geese 227/242 and won vs 4g."
)
HUNT_NOTE = (
    "New slug vs _hunt_20260914n (lastRunTime 2026-09-14 15:05:09.980000; public-search newest by dateCreated). "
    "Python %%writefile submission.py SHA dc07c7a9... Distinct from xuantianfengwu r10 SHA 3b8a1d4d, "
    "adaptive-land-allocator SHA d12f2987, land-labor-capital SHA b49709bd, timed-six-cow SHA 5dc0c68c, "
    "guru fully-dynamic SHA f4e3935c, and live cuts 14/15/16. Fixed 3-land (`desired_land_target=3`). "
    "Hour 4 financing: at step>=4 if rival_units>5 set cow-target 4 until step 4 else delay 6-cow until step 24 "
    "(`return [\"COW\"] * (4 if step < _financing_threshold(obs) else 6)`). R10 melon leftover. "
    "No farm/route reselect after 216. No ROUTE_STEP/PROGRAM/sale_horizon/ADVANCE_START/648/712. "
    "No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1625.8 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1300.7 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1625.8; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 1 new slug vs _hunt_20260914n "
    "(public search newest xuantianfengwu/kaggriculture-hour-4-financing-allocator lastRunTime 2026-09-14 15:05:09.980000; "
    "%%writefile submission.py SHA dc07c7a9 heuristic Hour-4 4/6-cow allocator, distinct from r10 3b8a1d4d / "
    "adaptive-land-allocator d12f2987, not farm-route reselect after 216). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260914o_cut16_rolling.json").read_text(encoding="utf-8"))
    games = rolling["games"]
    assert [g["id"] for g in games] == IDS
    first = games[0]
    hunt_row = {
        "kernel": "xuantianfengwu/kaggriculture-hour-4-financing-allocator",
        "path": "artifacts/public_sources/_hunt_20260914o/xuantianfengwu__kaggriculture-hour-4-financing-allocator/kaggriculture-hour-4-financing-allocator.ipynb",
        "verdict": "reject_heuristic_hour4_financing_allocator",
        "sha256": "dc07c7a9fad947659ed3151ec7f846de99d583d5e95c9af21adbaef2a5d6883e",
        "note": HUNT_NOTE,
    }
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
        )
    ]
    packet = {
        "title": "Kaggriculture study packet 2026-09-14o",
        "not_the_0914n_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260914o/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260914o/kaggriculture-publicleaderboard-2026-09-14T15-42-31.csv",
            "leaderboard_api": "experiments/20260914o_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260914o",
            "top_replays": "artifacts/kaggle_runs/top_20260914o",
            "hunt_dir": "artifacts/public_sources/_hunt_20260914o",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260914o_gate.json",
            "episode_report": "experiments/20260914o_episode_report.json",
            "hunt_report": "experiments/20260914o_hunt_report.json",
            "algo_note": "experiments/20260914o_algo_note.json",
            "loss_class": "experiments/20260914o_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1625.8,
            "rank": 2160,
            "n_teams": 9028,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1300.7,
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
            "cut16_score": 1625.8,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2922.1,
            "rank10": {"team": "Orbital Terraformer", "score": 2982.3},
            "rank1": {"team": "Majkel1337", "score": 3230.8, "submissionId": 56156662},
            "public_cut16": {"n": 267, "wtl": [113, 2, 152], "mean_margin": -1643.0},
        },
        "rolling": {
            "previous": "experiments/20260914n_cut16_rolling.json",
            "live_cut16": "experiments/20260914o_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0914n": True,
            "n": 12,
            "wtl": [4, 0, 8],
            "mean_margin": -4892.2,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": first["id"],
            "margin": first["margin"],
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "9c5s",
            "herd_opp": "8c6s3g",
            "sheep_steps_us": [row["step"] for row in first["sheep_steps_us"]],
        },
        "top_board": {
            "source": "experiments/20260914o_top10_games.json",
            "not_copied_from": prior_top,
            "Majkel1337": {
                "land": [
                    [150, 220, 222],
                    [150, 218, 220, 222],
                    [150, 220, 222],
                    [150, 220, 222],
                ],
                "herd": ["9c3s2g", "6c3s4g", "5c16s0g", "9c6s2g"],
                "wheat": [464, 672, 409, 636],
                "shops": ["BRUNCH_SPOT", "BAKERY", "FARMERS_MARKET", "ICE_CREAM_SHOP"],
                "clone": "0_of_4",
                "episodes": [108953610, 108946326, 108667748, 108663358],
                "note": (
                    "CSV #1 3230.8 live 3230.8 scoring sub 56156662 (current sub 56216119 is 3057.1). "
                    "Ids disjoint from 20260914n Majkel set. Mid-land 150 then 218-222 "
                    "(three 150/220/222 plus one 150/218/220/222), wheat 409-672, clone=0 on 4/4, "
                    "goose mix 2g/4g/0g/2g. Opening land is not a later-block license."
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
            "score": 1625.8,
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
                "Already live COMPLETE 1625.8. This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                "Extra sheep 226/241/265 not 227/242/266. Rolling 108851261 extra-goose 9c5s vs 9c5s3g -16092; "
                "108889446 extra sheep 218/242/266 already bought identical-clone 6c11s -12131; "
                "108822458 extra sheep 218/242/266 already bought 4c15s vs 6c11s -11033. "
                "New-window Floth 108944173 extra-animal 8c6s3g -1793; Yiwei Pu 108941028 identical-clone extra-goose +106. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 1 new slug vs 0914n, "
                "not licensed (xuantianfengwu/kaggriculture-hour-4-financing-allocator %%writefile SHA dc07c7a9 Hour-4 4/6-cow heuristic); "
                "no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. Upload-bail would block even a licensed freeze: "
                "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1625.8 and keeps 1300.7."
            ),
        },
        "hunt": [hunt_row],
    }
    dump(ROOT / "experiments/20260914o_study_packet.json", packet)

    dump(
        ROOT / "experiments/20260914o_episode_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914o",
            "utc": "2026-09-14T15:42:31Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1625.8,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1625.8 (was 1627.7). Newest public 108944173. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1300.7 / ListEpisodes last_updated 1300.711) + cut 16 56151152. "
                "Upload-bail TRUE (c): shopbag partner 1300.7 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1300.7,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2160,
            "heralces_score": 1625.8,
            "n_teams_csv": 9028,
            "public_56151152": {
                "n_public": 267,
                "n_validation": 1,
                "n_completed_public": 267,
                "wtl": [113, 2, 152],
                "mean_margin": -1643.0,
                "status": "COMPLETE",
                "publicScore": 1625.8,
            },
            "rolling_ids": IDS,
            "rolling_forbidden_0914n": PREV_14N,
            "ids_not_identical_to_0914n": True,
            "ids_disjoint_from_0914n": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [4, 0, 8],
            "mean_margin": -4892.2,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids disjoint from 20260914n packet, all 720 DONE/DONE. 4W 8L. "
                "Worst LaiCxm 108851261 L -16092 9c5s vs 9c5s3g clone=1 extra-goose opp extra cow 218 extra sheep 227 extra geese 242/266. "
                "New-window Floth 108944173 extra-animal 8c6s3g -1793; Yiwei Pu 108941028 identical-clone extra-goose +106. "
                "Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        ROOT / "experiments/20260914o_hunt_report.json",
        {
            "date": "2026-09-14",
            "packet": "20260914o",
            "kernels_not_in_0914n_packet": True,
            "no_upload": True,
            "no_kaggle_submit": True,
            "cells_executed": False,
            "extracted_later_block_agent": False,
            "later_block_python_after_216": False,
            "any_licensed_for_extract": False,
            "licensed_kernel": None,
            "root_main_py": "unchanged",
            "hunt_dir": "artifacts/public_sources/_hunt_20260914o",
            "inspect_scripts": [
                "experiments/candidates/scan_hunt_20260914o.py",
                "experiments/candidates/inspect_hunt_20260914o.py",
                "experiments/candidates/_inspect_xuantian_20260914o.py",
            ],
            "python": "D:\\kaggle\\kaggriculture\\.venv\\Scripts\\python.exe",
            "payload_decode": "writefile_static_hash_only",
            "compare_0914n": {
                "hunt_dir": "artifacts/public_sources/_hunt_20260914n",
                "hunt_report": "experiments/20260914n_hunt_report.json",
                "gate": "experiments/20260914n_gate.json",
                "note": (
                    "1 new slug vs _hunt_20260914n. Public search newest is now "
                    "xuantianfengwu/kaggriculture-hour-4-financing-allocator (lastRunTime 2026-09-14 15:05:09.980000). "
                    "Did not re-pull rejected kernels (guruprasaathas111 fully-dynamic SHA f4e3935c, ahmedberatozer v42 SHA 728fdfb4, "
                    "rohitt94 route-replay SHA 62a80706, sorcererbi analysis trio, arsgorynich v40-challenger SHA 546c4224, "
                    "xuantianfengwu r10 SHA 3b8a1d4d, aurax7 v5 SHA ea4c28e6, lime0001 t23 SHA 31ee22dc, nathanjacob V40 autopsy dataset wrapper, "
                    "Ahmed V41 SHA 8951ff93, prvsiyan reserve-garden, alperen scored-agent SHA 85c8b532, "
                    "xuantianfengwu adaptive-land-allocator SHA d12f2987, renjistarfall V39 reprint, alperen metacounter-r1 analysis, "
                    "xuantianfengwu land-labor-capital, Ahmed V40 SHA 546c4224, guru V39, yhay81 0913, wei v46d review, Ahmed V39, "
                    "aurax7 v4, crystalbaby V38, prvsiyan market-ledger, timed-six-cow, lokesh V37, crystalbaby dynamic-route, "
                    "nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
                ),
            },
            "public_search_newest": "xuantianfengwu/kaggriculture-hour-4-financing-allocator",
            "public_search_newest_lastRunTime": "2026-09-14 15:05:09.980000",
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
            "named_kernels_scanned": ["xuantianfengwu/kaggriculture-hour-4-financing-allocator"],
            "author_list_no_new_later_block": [
                "yhay81/shop-router-0913",
                "yamakawanin/king-v4e-rc4",
                "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router",
                "thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing",
                "y3uanm/kaggriculture-conservative-market-router-v5",
                "y3uanm/kaggriculture-safe-baseline-rollback-v20",
            ],
            "author_list_note": "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6.",
            "hunt": [hunt_row],
        },
    )

    old_gate = json.loads((ROOT / "experiments/20260914n_gate.json").read_text(encoding="utf-8"))
    gate = deepcopy(old_gate)
    gate["packet"] = "20260914o"
    gate["named_kernels_scanned"] = ["xuantianfengwu/kaggriculture-hour-4-financing-allocator"]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260914o"
    gate["hunt_report"] = "experiments/20260914o_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1625.8
    gate["rejected"] = [
        {
            "kernel": hunt_row["kernel"],
            "verdict": hunt_row["verdict"],
            "note": hunt_row["note"],
        }
    ] + old_gate["rejected"]
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1625.8 partnered with newer shopbag 56151155 COMPLETE 1300.7 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "1 new public slug vs _hunt_20260914n, not licensed: xuantianfengwu/kaggriculture-hour-4-financing-allocator "
        "(%%writefile SHA dc07c7a9 Hour-4 4/6-cow heuristic, distinct from r10 3b8a1d4d / allocator d12f2987). "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. "
        "Cut 12/13 stay Hold. Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: \u0438\u0442\u043c\u043e\u043d\u044f\u044f\u044f extra sheep 227/242/266 already bought vs 8c6s3g -6320; "
        "\u0412\u0430\u0440\u0438\u043c extra sheep 218/242/266 already bought identical-clone -12131; "
        "LaiCxm extra-goose extra cow 218 extra sheep 227 extra geese 242/266 -16092; Floth extra-animal 8c6s3g -1793."
    )
    dump(ROOT / "experiments/20260914o_gate.json", gate)

    dump(
        ROOT / "experiments/20260914o_cut16_loss_class.json",
        {
            "date": "2026-09-14",
            "packet": "20260914o",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": IDS,
            "ids_0914n": PREV_14N,
            "disjoint_from_0914n": True,
            "all_720_done_done": True,
            "wtl": [4, 0, 8],
            "mean_margin": -4892.2,
            "clone_n": 12,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [3.0, 27.0],
            "wool_360": {
                "108944173": 1,
                "108941028": 37,
                "108910147": 37,
                "108889446": 236,
                "108889378": 237,
                "108851261": 1,
                "108822458": 231,
                "108817790": 1,
                "108787437": 1,
                "108762693": 223,
                "108741805": 37,
                "108723413": 43,
            },
            "wool_432": {
                "108944173": 1,
                "108941028": 125,
                "108910147": 1,
                "108889446": 237,
                "108889378": 230,
                "108851261": 1,
                "108822458": 137,
                "108817790": 5,
                "108787437": 1,
                "108762693": 200,
                "108741805": 1,
                "108723413": 1,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-14b/09-14c/09-14d/09-14e/09-14f/09-14g/09-14h/09-14i/09-14j/09-14k/09-14l/09-14m/09-14n: "
                "extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-sheep. "
                "WTL 4-0-8 mean -4892.2 vs 09-14n 5-0-7 mean -2680.0. New window game Floth 108944173 -1793. clone=12/12."
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

    algo = json.loads((ROOT / "experiments/20260914n_algo_note.json").read_text(encoding="utf-8"))
    algo["packet"] = "20260914o"
    algo["live"]["cut16"]["csv_0914o_team_score"] = 1625.8
    algo["live"]["rank_csv_0914o"] = 2160
    algo["cut16_live_failure_class"]["0914o"] = {
        "file": "experiments/20260914o_cut16_rolling.json",
        "ids": IDS,
        "wtl": [4, 0, 8],
        "mean_margin": -4892.2,
        "clone": "12/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-sheep",
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
                "id": 108889446,
                "opp": "\u0412\u0430\u0440\u0438\u043c \u0441\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0441\u0430\u043c\u043e\u0433\u043e\u043d",
                "margin": -12131,
                "shops72": ["YARN_STORE"],
                "buy": "6c11s vs 6c11s",
                "clone": 1,
            },
            {
                "id": 108822458,
                "opp": "Revanth Tambisetty",
                "margin": -11033,
                "shops72": ["SMOOTHIE_SHOP"],
                "buy": "4c15s vs 6c11s",
                "clone": 1,
            },
        ],
    }
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "1 new public slug vs _hunt_20260914n is xuantianfengwu hour-4 financing-allocator heuristic 4/6-cow (SHA dc07c7a9). "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump(ROOT / "experiments/20260914o_algo_note.json", algo)


if __name__ == "__main__":
    main()
