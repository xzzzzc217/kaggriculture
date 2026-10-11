"""Write 20260915 packet JSON from live measurements. No upload."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV_14O = [
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
IDS = [
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
LOSS_CLASS = (
    "mixed extra-animal 8c6s3g (My second life 109030720 9c5s vs 8c6s3g PET_CAFE extra sheep 314 vs opp extra sheep 218/227 extra geese 242/266 -29665; "
    "MD. Nazmus Sakib Anik 109042689 7c6s vs 8c6s3g FARMERS_MARKET extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -13653; "
    "Quillbolt 109054323 7c6s vs 8c6s3g BRUNCH extra cow 218 vs opp extra sheep 218/227 extra geese 242/266 -12417; "
    "Goua Henri 109029822 10c8s vs 8c6s3g PET_CAFE extra cow 218 extra sheep 227/242/266 already bought vs opp extra sheep 218/227 extra geese 242/266 -7452) "
    "+ extra-goose (Harshith revuru 109044160 7c6s vs 6c6s5g BRUNCH extra cow 218 vs opp extra geese 218/227/242 extra sheep 266 -15134) "
    "+ identical-clone extra-goose (Liyi xin jie 109057555 9c5s3g vs 9c5s3g PET_CAFE extra geese 227/242 already bought -23988 cash_24=0) "
    "+ extra-sheep (SatoshiN04 109091091 4c14s vs 2c12s2g PET_CAFE extra sheep 218/242/266 already bought -12300 clone=0). "
    "Wins: alexbstl 109078755 6c11s vs 11c8s6g YARN +8823 extra sheep 218/242/266 already bought; "
    "Yichi 109111080 9c8s vs 9c5s3g BRUNCH +6951 extra sheep 227/242/266 already bought vs opp extra geese 227/242 extra sheep 266; "
    "Duc-Anh Nguyen 109135062 9c5s3g vs 9c5s4g PIZZA +2713 extra geese 227/242 already bought vs opp extra geese 218/227/242 extra sheep 266; "
    "KIRTAN RUPESHBHAI BHOJANI 109024708 6c11s vs 7c10s YARN +1697 extra sheep 218/242/266 already bought vs extra sheep 227/242/266; "
    "ocean240812 109142116 9c8s vs 6c6s6g BAKERY +74 extra sheep 227/242/266 already bought vs opp extra geese 218/227/242 extra sheep 266. "
    "clone=11/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 0-22. Not opening-broke no-land. Not freeze-after-day-9 9c9s. "
    "Not a 227/242/266 license: Goua Henri already bought extra sheep 227/242/266 and lost vs 8c6s3g; "
    "SatoshiN04 already bought extra sheep 218/242/266 and lost 14s vs 12s2g; "
    "My second life did not buy extra sheep 227/242/266 and lost vs 8c6s3g (extra sheep 314); "
    "Quillbolt/Nazmus extra cow 218 lost vs 8c6s3g; Harshith extra cow 218 lost extra-goose 5g; "
    "Liyi identical-clone extra-goose 227/242 already bought -23988; "
    "ocean/Yichi already bought extra sheep 227/242/266 and won; Duc-Anh already bought extra geese 227/242 and won vs 4g; "
    "alexbstl/KIRTAN already bought extra sheep 218/242/266 and won yarn 11s."
)
HUNT_ROWS = [
    {
        "kernel": "xuantianfengwu/kaggriculture-terminal-logistics",
        "path": "artifacts/public_sources/_hunt_20260915/xuantianfengwu__kaggriculture-terminal-logistics/kaggriculture-terminal-logistics.ipynb",
        "verdict": "reject_heuristic_hour4_financing_allocator",
        "sha256": "364ca885fee9c92aeee1069e83f44756d6082b489f54a6aea76565e74591442b",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-15 02:30:28.237000; public-search newest by dateCreated). "
            "Python %%writefile submission.py SHA 364ca885... Distinct from hour-4 SHA dc07c7a9, r10 SHA 3b8a1d4d, "
            "adaptive-land-allocator SHA d12f2987, land-labor-capital SHA b49709bd, timed-six-cow SHA 5dc0c68c, and live cuts 14/15/16. "
            "Fixed 3-land (`desired_land_target=3`). Hour 4 financing still `return [\"COW\"] * (4 if step < _financing_threshold(obs) else 6)`. "
            "R10 melon leftover. No farm/route reselect after 216. No ROUTE_STEP/PROGRAM/sale_horizon/ADVANCE_START/648/712. "
            "No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "taylorclark637/sovereign-swarm-kinematics-the",
        "path": "artifacts/public_sources/_hunt_20260915/taylorclark637__sovereign-swarm-kinematics-the/sovereign-swarm-kinematics-the.ipynb",
        "verdict": "reject_heuristic_fib_hire",
        "sha256": "ffc0e6e2c2a408915220f51e3af8eb9dbc34315e70f548d32c15d9567380a40b",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-15 01:08:57.847000). Python %%writefile submission.py SHA ffc0e6e2 "
            "(earlier cell SHA e0b36b51 overwritten). Fib-hire heuristic (`if step < 680` HIRE). No farm/route reselect after 216. "
            "No ctypes/agent.so. Cells not executed. Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "ahmedberatozer/kaggriculture-v43-recovering-lost-harvests",
        "path": "artifacts/public_sources/_hunt_20260915/ahmedberatozer__kaggriculture-v43-recovering-lost-harvests/kaggriculture-v43-recovering-lost-harvests.ipynb",
        "verdict": "reject_shop0909_144_648_and_712_overlay",
        "sha256": "919fc1d61050cd96f799979e49177ae3ac7bce98ec9835724238bea73f4a08ed",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 21:41:24.923000). SOURCE_BYTES static reconstruct SHA 919fc1d6... "
            "Distinct from Ahmed V42 SHA 728fdfb4, V41 8951ff93, V40 546c4224, V39 708c7485, V38 a2047ebd. Notebook embeds cut15 SHA b87a27ed "
            "and yhay81 shop-router-0913 SHA 77cf6772 as comments/payloads; payload itself is 919fc1d6. Shop0909 day-6 144/648 plus 288 four-turn "
            "sale overlay (_R37_HORIZONS=4 from 288) plus step==712 terminal planner. 216<=step<=227 is milk-shop livestock sub, not a farm/route "
            "reselect after 216. No ctypes/agent.so. Cells not executed. SOURCE_BYTES dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "prvsiyan/kaggriculture-field-clock-action-budget",
        "path": "artifacts/public_sources/_hunt_20260915/prvsiyan__kaggriculture-field-clock-action-budget/kaggriculture-field-clock-action-budget.ipynb",
        "verdict": "reject_educational_framework",
        "sha256": None,
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 21:24:39.473000). Educational energy/food/risk task ranker, not %%writefile main.py. "
            "Distinct from already-rejected prvsiyan reserve-garden and market-ledger SHA 1c98c297. No farm/route reselect after 216. "
            "Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "alperen5252525/adaptive-route-portfolio-kaggriculture",
        "path": "artifacts/public_sources/_hunt_20260915/alperen5252525__adaptive-route-portfolio-kaggriculture/adaptive-route-portfolio-kaggriculture.ipynb",
        "verdict": "reject_yhay81_0913_reprint_day6",
        "sha256": "77cf67723a753be957cf70fdb8abbce7ef5c020299e8acd16ed8d2dc8b929dfa",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 20:57:26.583000). Python %%writefile main.py SHA 77cf6772... Exact reprint of already-rejected "
            "yhay81/shop-router-0913. CDLL present. Day-6 144/648 only, not farm/route reselect after 216. Cells not executed. Writefile dumped in hunt dir "
            "for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "destbreso/agent-telemetry-catch-what-you-lose",
        "path": "artifacts/public_sources/_hunt_20260915/destbreso__agent-telemetry-catch-what-you-lose/agent-telemetry-catch-what-you-lose.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": None,
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-15 01:10:28.813000). 67-cell telemetry/analysis notebook, no %%writefile, no main.py/submission.py payload. "
            "No farm/route reselect after 216. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "alperen5252525/harvestforge-x-high-throughput-farming",
        "path": "artifacts/public_sources/_hunt_20260915/alperen5252525__harvestforge-x-high-throughput-farming/harvestforge-x-high-throughput-farming.ipynb",
        "verdict": "reject_heuristic_step_mod4",
        "sha256": "01f0cd470f669f86d4b53eb5b014614d3b383970d0755f119de14153fd77c1eb",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 19:16:59.873000). Python %%writefile main.py SHA 01f0cd47... Distinct from alperen scored-agent SHA 85c8b532 "
            "and yhay81 0913 SHA 77cf6772. Heuristic `if step % 4 != 0`. No farm/route reselect after 216. No ctypes/agent.so. Cells not executed. "
            "Writefile dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "nathanjacob/how-many-twins-strategy-clustering-kaggriculture",
        "path": "artifacts/public_sources/_hunt_20260915/nathanjacob__how-many-twins-strategy-clustering-kaggriculture/how-many-twins-strategy-clustering-kaggriculture.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": None,
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 19:18:54.140000). 30-cell clustering analysis, no %%writefile. Distinct from already-rejected "
            "nathanjacob V40 autopsy dataset wrapper. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "hosen42/kaggriculture-v11-hc1-vs-h5-validation",
        "path": "artifacts/public_sources/_hunt_20260915/hosen42__kaggriculture-v11-hc1-vs-h5-validation/kaggriculture-v11-hc1-vs-h5-validation.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": None,
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 17:15:18.683000). Validation/analysis notebook (embeds cut15 SHA b87a27ed as comment/payload). "
            "No %%writefile agent. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "nathanjacob/kaggriculture-pipe-2-agent",
        "path": "artifacts/public_sources/_hunt_20260915/nathanjacob__kaggriculture-pipe-2-agent/kaggriculture-pipe-2-agent.ipynb",
        "verdict": "reject_v42_reprint_shop0909_overlay",
        "sha256": "728fdfb4405ba313f8b14ffb3e0f8eceaddcaa0de49e4835928d89aaf71467e9",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 18:47:53.680000). AGENT_B64 gzip static reconstruct SHA 728fdfb4... Exact reprint of already-rejected "
            "ahmedberatozer V42. Shop0909 day-6 144/648 plus 288/712 overlay. 216<=step<=227 is milk-shop livestock sub, not a farm/route reselect after 216. "
            "Cells not executed. Payload dumped in hunt dir for SHA only; not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "leoprovorov/god-s-mode-hacked-stores",
        "path": "artifacts/public_sources/_hunt_20260915/leoprovorov__god-s-mode-hacked-stores/god-s-mode-hacked-stores.ipynb",
        "verdict": "reject_analysis_notebook_no_writefile",
        "sha256": None,
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 17:13:51.407000). Shop-seed analysis notebook, no %%writefile agent. Distinct from already-listed "
            "leoprovorov v65. Cells not executed. Not copied to candidates/; not clone/G5."
        ),
    },
    {
        "kernel": "sunil123kumar/kaggriculture-v6",
        "path": "artifacts/public_sources/_hunt_20260915/sunil123kumar__kaggriculture-v6/kaggriculture-v6.ipynb",
        "verdict": "reject_v41_reprint_shop0909_overlay",
        "sha256": "8951ff93742015cba535b125223cf2e541bb7b602080fc4584f30c2613d210f3",
        "note": (
            "New slug vs _hunt_20260914o (lastRunTime 2026-09-14 09:18:59.717000). Python %%writefile main.py SHA 8951ff93... Exact reprint of already-rejected "
            "ahmedberatozer V41. Distinct from sunil v4. Shop0909 day-6 144/648 plus 288/712 overlay. Cells not executed. Writefile dumped in hunt dir for SHA only; "
            "not copied to candidates/; not clone/G5."
        ),
    },
]
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1606.1 would drop without a >=1500 COMPLETE newest-2 partner "
    "(shopbag 56151155 COMPLETE 1293.6 < 1500 and newer than cut 16; a new cut alone keeps shopbag and drops 1606.1; "
    "re-upload is 600-provisional not a partner). No licensed later-block. Hunt 12 new slugs vs _hunt_20260914o "
    "(public search newest xuantianfengwu/kaggriculture-terminal-logistics lastRunTime 2026-09-15 02:30:28.237000; "
    "%%writefile submission.py SHA 364ca885 heuristic Hour-4 4/6-cow allocator, distinct from hour-4 dc07c7a9 / r10 3b8a1d4d, "
    "not farm-route reselect after 216). Do not reupload boatlee 55710781. Cut 12/13 Hold."
)


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260915_cut16_rolling.json").read_text(encoding="utf-8"))
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
        )
    ]
    packet = {
        "title": "Kaggriculture study packet 2026-09-15",
        "not_the_0914o_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260915/kaggriculture.zip",
            "leaderboard_csv": "artifacts/kaggle_runs/lb_20260915/kaggriculture-publicleaderboard-2026-09-15T03-30-25.csv",
            "leaderboard_api": "experiments/20260915_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260915",
            "top_replays": "artifacts/kaggle_runs/top_20260915",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260915_gate.json",
            "episode_report": "experiments/20260915_episode_report.json",
            "hunt_report": "experiments/20260915_hunt_report.json",
            "algo_note": "experiments/20260915_algo_note.json",
            "loss_class": "experiments/20260915_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1606.1,
            "rank": 2211,
            "n_teams": 9077,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1293.6,
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
            "cut16_score": 1606.1,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2946.4,
            "rank10": {"team": "Catalyst", "score": 2978.3},
            "rank1": {"team": "Majkel1337", "score": 3198.4, "submissionId": 56156662},
            "public_cut16": {"n": 285, "wtl": [119, 2, 164], "mean_margin": -2014.5},
        },
        "rolling": {
            "previous": "experiments/20260914o_cut16_rolling.json",
            "live_cut16": "experiments/20260915_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0914o": True,
            "n": 12,
            "wtl": [5, 0, 7],
            "mean_margin": -7862.6,
            "loss_class": LOSS_CLASS,
        },
        "excluding": {
            "id": first["id"],
            "margin": first["margin"],
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "9c8s",
            "herd_opp": "6c6s6g",
            "sheep_steps_us": [row["step"] for row in first["sheep_steps_us"]],
        },
        "top_board": {
            "source": "experiments/20260915_top10_games.json",
            "not_copied_from": prior_top,
            "Majkel1337": {
                "land": [
                    [150, 218, 220, 222],
                    [150, 218, 220, 222],
                    [150, 220, 222],
                    [150, 218, 220, 222],
                ],
                "herd": ["6c6s4g", "7c3s4g", "11c3s0g", "6c3s4g"],
                "wheat": [529, 433, 434, 543],
                "shops": ["BRUNCH_SPOT", "BRUNCH_SPOT", "PIZZA_SHOP", "PET_CAFE"],
                "clone": "0_of_4",
                "episodes": [109138748, 109133305, 109128514, 109122968],
                "note": (
                    "CSV #1 3198.4 live 3198.4 scoring sub 56156662 (current sub 56216119 is 3131.7). "
                    "Ids disjoint from 20260914o Majkel set. Mid-land 150 then 218-222 "
                    "(three 150/218/220/222 plus one 150/220/222), wheat 433-543, clone=0 on 4/4, "
                    "goose mix 4g/4g/0g/4g. Opening land is not a later-block license."
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
            "score": 1606.1,
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
                "Already live COMPLETE 1606.1. This cycle Hold: upload-bail (c) plus no new licensed later-block. "
                "Extra sheep 226/241/265 not 227/242/266. Rolling 109030720 extra-animal 8c6s3g 9c5s vs 8c6s3g -29665; "
                "109057555 identical-clone extra-goose 9c5s3g -23988 cash_24=0; "
                "109044160 extra-goose 7c6s vs 6c6s5g -15134. New-window ocean240812 109142116 extra-sheep +74. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts 14/15/16. Hunt: 12 new slugs vs 0914o, "
                "none licensed (public-search newest xuantianfengwu/kaggriculture-terminal-logistics %%writefile SHA 364ca885 Hour-4 4/6-cow heuristic; "
                "Ahmed V43 SHA 919fc1d6 Shop0909 overlay; alperen adaptive-route SHA 77cf6772 yhay81 0913 reprint; sunil v6 SHA 8951ff93 V41 reprint; "
                "pipe-2 SHA 728fdfb4 V42 reprint). no king rc5 / y3uanm v6 / Thomas tree that actually splits after 216. "
                "Upload-bail would block even a licensed freeze: shopbag 56151155 is newer than cut 16, so a new cut alone drops 1606.1 and keeps 1293.6."
            ),
        },
        "hunt": HUNT_ROWS,
    }
    dump(ROOT / "experiments/20260915_study_packet.json", packet)

    dump(
        ROOT / "experiments/20260915_episode_report.json",
        {
            "date": "2026-09-15",
            "packet": "20260915",
            "utc": "2026-09-15T03:30:25Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1606.1,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1606.1 (was 1625.8). Newest public 109142116. Newest-2 = shopbag reupload 56151155 "
                "(newer id, submissions 1293.6 / ListEpisodes last_updated 1293.626) + cut 16 56151152. "
                "Upload-bail TRUE (c): shopbag partner 1293.6 < 1500 and is newer than cut 16, so a new cut alone would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1293.6,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2211,
            "heralces_score": 1606.1,
            "n_teams_csv": 9077,
            "public_56151152": {
                "n_public": 285,
                "n_validation": 1,
                "n_completed_public": 285,
                "wtl": [119, 2, 164],
                "mean_margin": -2014.5,
                "status": "COMPLETE",
                "publicScore": 1606.1,
            },
            "rolling_ids": IDS,
            "rolling_forbidden_0914o": PREV_14O,
            "ids_not_identical_to_0914o": True,
            "ids_disjoint_from_0914o": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [5, 0, 7],
            "mean_margin": -7862.6,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids disjoint from 20260914o packet, all 720 DONE/DONE. 5W 7L. "
                "Worst My second life 109030720 L -29665 9c5s vs 8c6s3g clone=1 extra-animal opp extra sheep 218/227 extra geese 242/266. "
                "New-window ocean240812 109142116 extra-sheep +74. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    dump(
        ROOT / "experiments/20260915_hunt_report.json",
        {
            "date": "2026-09-15",
            "packet": "20260915",
            "kernels_not_in_0914o_packet": True,
            "no_upload": True,
            "no_kaggle_submit": True,
            "cells_executed": False,
            "extracted_later_block_agent": False,
            "later_block_python_after_216": False,
            "any_licensed_for_extract": False,
            "licensed_kernel": None,
            "root_main_py": "unchanged",
            "hunt_dir": "artifacts/public_sources/_hunt_20260915",
            "inspect_scripts": [
                "experiments/candidates/scan_hunt_20260915.py",
                "experiments/candidates/inspect_hunt_20260915.py",
                "experiments/candidates/_inspect_hunt_payloads_20260915.py",
                "experiments/candidates/_extract_v43_and_rest_20260915.py",
                "experiments/candidates/_summarize_and_pipe2_20260915.py",
            ],
            "python": "D:\\kaggle\\kaggriculture\\.venv\\Scripts\\python.exe",
            "payload_decode": "writefile_static_hash_only",
            "compare_0914o": {
                "hunt_dir": "artifacts/public_sources/_hunt_20260914o",
                "hunt_report": "experiments/20260914o_hunt_report.json",
                "gate": "experiments/20260914o_gate.json",
                "note": (
                    "12 new slugs vs _hunt_20260914o. Public search newest is now "
                    "xuantianfengwu/kaggriculture-terminal-logistics (lastRunTime 2026-09-15 02:30:28.237000). "
                    "Did not re-pull rejected kernels (xuantianfengwu hour-4 SHA dc07c7a9, guruprasaathas111 fully-dynamic SHA f4e3935c, "
                    "ahmedberatozer v42 SHA 728fdfb4, rohitt94 route-replay SHA 62a80706, sorcererbi analysis trio, "
                    "arsgorynich v40-challenger SHA 546c4224, xuantianfengwu r10 SHA 3b8a1d4d, aurax7 v5 SHA ea4c28e6, "
                    "lime0001 t23 SHA 31ee22dc, nathanjacob V40 autopsy dataset wrapper, Ahmed V41 SHA 8951ff93, "
                    "prvsiyan reserve-garden, alperen scored-agent SHA 85c8b532, xuantianfengwu adaptive-land-allocator SHA d12f2987, "
                    "renjistarfall V39 reprint, alperen metacounter-r1 analysis, xuantianfengwu land-labor-capital, Ahmed V40 SHA 546c4224, "
                    "guru V39, yhay81 0913, wei v46d review, Ahmed V39, aurax7 v4, crystalbaby V38, prvsiyan market-ledger, timed-six-cow, "
                    "lokesh V37, crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, municef1/bernubritz tapes, "
                    "melomanpanda, zhincez, y3uanm rollback-v20, yhay81 0911-simple)."
                ),
            },
            "public_search_newest": "xuantianfengwu/kaggriculture-terminal-logistics",
            "public_search_newest_lastRunTime": "2026-09-15 02:30:28.237000",
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

    old_gate = json.loads((ROOT / "experiments/20260914o_gate.json").read_text(encoding="utf-8"))
    gate = deepcopy(old_gate)
    gate["date"] = "2026-09-15"
    gate["packet"] = "20260915"
    gate["named_kernels_scanned"] = [row["kernel"] for row in HUNT_ROWS]
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260915"
    gate["hunt_report"] = "experiments/20260915_hunt_report.json"
    gate["live"]["cut16"]["score_complete"] = 1606.1
    gate["live"]["shopbag"]["score_complete"] = 1293.6
    gate["rejected"] = [
        {"kernel": row["kernel"], "verdict": row["verdict"], "note": row["note"]} for row in HUNT_ROWS
    ] + old_gate["rejected"]
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1606.1 partnered with newer shopbag 56151155 COMPLETE 1293.6 < 1500. "
        "A new cut uploaded alone would drop 56151152 and keep shopbag as newest-2 partner (shopbag id is newer). "
        "Pairing a new cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze is false because of this upload-bail, not because a licensed later-block is ready. "
        "12 new public slugs vs _hunt_20260914o, none licensed: public-search newest xuantianfengwu/kaggriculture-terminal-logistics "
        "(%%writefile SHA 364ca885 Hour-4 4/6-cow heuristic, distinct from hour-4 dc07c7a9 / r10 3b8a1d4d). "
        "king/Thomas/y3uanm/yhay81 author lists have no new later-block. Did not clone/G5-screen, did not pack or upload. "
        "Cut 12/13 stay Hold. Root main.py SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: Goua Henri extra sheep 227/242/266 already bought vs 8c6s3g -7452; "
        "SatoshiN04 extra sheep 218/242/266 already bought 14s vs 12s2g -12300; "
        "My second life extra-animal 8c6s3g extra sheep 314 -29665; Liyi identical-clone extra-goose -23988."
    )
    dump(ROOT / "experiments/20260915_gate.json", gate)

    dump(
        ROOT / "experiments/20260915_cut16_loss_class.json",
        {
            "date": "2026-09-15",
            "packet": "20260915",
            "live": "yamakawanin king-v4e-rc4",
            "submission": 56151152,
            "team": "heralces",
            "ids": IDS,
            "ids_0914o": PREV_14O,
            "disjoint_from_0914o": True,
            "all_720_done_done": True,
            "wtl": [5, 0, 7],
            "mean_margin": -7862.6,
            "clone_n": 11,
            "land_pattern": "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)",
            "cash_24_range": [0.0, 22.0],
            "wool_360": {
                "109142116": 224,
                "109135062": 43,
                "109111080": 226,
                "109091091": 195,
                "109078755": 238,
                "109057555": 43,
                "109054323": 1,
                "109044160": 1,
                "109042689": 1,
                "109030720": 37,
                "109029822": 223,
                "109024708": 237,
            },
            "wool_432": {
                "109142116": 189,
                "109135062": 1,
                "109111080": 197,
                "109091091": 1,
                "109078755": 234,
                "109057555": 1,
                "109054323": 5,
                "109044160": 1,
                "109042689": 55,
                "109030720": 82,
                "109029822": 200,
                "109024708": 225,
            },
            "same_class_as_0913c": True,
            "same_class_note": (
                "Same extra-animal family as 09-13c/09-14/09-14o: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-goose. "
                "WTL 5-0-7 mean -7862.6 vs 09-14o 4-0-8 mean -4892.2. New window game ocean240812 109142116 +74. clone=11/12."
            ),
            "loss_class": LOSS_CLASS,
            "worst_losses": [
                {
                    "id": 109030720,
                    "opp": "My second life",
                    "margin": -29665.0,
                    "herd_us": "9c5s",
                    "herd_opp": "8c6s3g",
                    "shops": ["PET_CAFE"],
                }
            ],
        },
    )

    algo = json.loads((ROOT / "experiments/20260914o_algo_note.json").read_text(encoding="utf-8"))
    algo["date"] = "2026-09-15"
    algo["packet"] = "20260915"
    algo["live"]["cut16"]["csv_0915_team_score"] = 1606.1
    algo["live"]["shopbag"]["score_complete"] = 1293.6
    algo["live"]["rank_csv_0915"] = 2211
    algo["cut16_live_failure_class"]["0915"] = {
        "file": "experiments/20260915_cut16_rolling.json",
        "ids": IDS,
        "wtl": [5, 0, 7],
        "mean_margin": -7862.6,
        "clone": "11/12",
        "class": "same extra-animal family: extra-animal 8c6s3g plus extra-goose plus extra-sheep plus identical-clone extra-goose",
        "heavy": [
            {
                "id": 109030720,
                "opp": "My second life",
                "margin": -29665,
                "shops72": ["PET_CAFE"],
                "buy": "9c5s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 37,
            },
            {
                "id": 109057555,
                "opp": "Liyi xin jie",
                "margin": -23988,
                "shops72": ["PET_CAFE"],
                "buy": "9c5s3g vs 9c5s3g",
                "clone": 1,
                "cash_24": 0,
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
            "12 new public slugs vs _hunt_20260914o; public-search newest is xuantianfengwu terminal-logistics heuristic 4/6-cow (SHA 364ca885). "
            "Author lists otherwise unchanged (no king rc5 / y3uanm v6 / Thomas new tree / Yusuke later-block)."
        ),
    }
    dump(ROOT / "experiments/20260915_algo_note.json", algo)


if __name__ == "__main__":
    main()
