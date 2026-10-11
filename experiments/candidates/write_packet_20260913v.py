"""Write 20260913v study packet JSON. Hold. No upload."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREV_U = [
    108594800,
    108568560,
    108559476,
    108534412,
    108504670,
    108472548,
    108461768,
    108432563,
    108429814,
    108426937,
    108422886,
    108399266,
]
IDS = [
    108608562,
    108604498,
    108586169,
    108550653,
    108545775,
    108520439,
    108509931,
    108489181,
    108484081,
    108445221,
    108441448,
    108441305,
]
LOSS = (
    "mixed extra-animal 8c6s3g (AQiDA19 108550653 7c6s vs 8c6s3g clone=1 BAKERY extra sheep "
    "218/227 extra geese 242/266 wheat 509 vs 17314 -21800; Hanaro 108545775 9c5s vs 8c6s3g "
    "PIZZA extra sheep 218/227 extra geese 242/266 -14377; Wei Han 108445221 9c5s vs 8c6s3g "
    "ICE_CREAM extra sheep 218/227 extra geese 242/266 -12688; Excluding 108520439 7c6s vs "
    "8c6s3g FARMERS_MARKET extra sheep 218/227 extra geese 242/266 -5345) + extra-sheep 15s "
    "(Hackoholics 108509931 4c15s vs 6c10s extra sheep 218/242/266 already bought -4788) + "
    "identical-clone extra-goose (mmwstudy 108484081 9c5s3g vs 9c5s3g extra geese 227/242 "
    "already bought -65). Wins: dupakdungking 108608562 6c12s vs 8c6s3g YARN extra sheep "
    "218/242/266 already bought +9867; XiaoYan12 108441448 9c5s3g vs 6c6s6g +6450 extra geese "
    "227/242 already bought; Agentmaster 108489181 9c5s3g vs 9c5s4g +2699 extra geese 227/242 "
    "already bought; wzyxp_123 108441305 9c5s3g vs 9c5s3g +2649 extra geese 227/242 already "
    "bought; Hanaro 108604498 4c14s vs 8c6s3g BRUNCH extra sheep 218/242/266 already bought "
    "+114; maxout 108586169 9c5s3g vs 9c5s3g identical-clone extra geese 227/242 already "
    "bought +8. clone=12/12, Q=3/3, BUY_LAND 151/266 succeeded, cash_24 3-27 not 0. Not "
    "opening-broke no-land. Not freeze-after-day-9 9c9s. Not a 227/242/266 license: "
    "AQiDA19/Hanaro/Wei Han/Excluding lost extra-animal after opp extra sheep 218/227 extra "
    "geese 242/266; Hackoholics already bought 218/242/266 and lost 15s; mmwstudy already "
    "bought extra geese 227/242 and lost identical-clone -65; dupakdungking already bought "
    "extra sheep 218/242/266 and won YARN 6c12s vs 8c6s3g +9867; Hanaro 108604498 already "
    "bought extra sheep 218/242/266 and won 4c14s +114; XiaoYan12/Agentmaster/wzyxp_123/"
    "maxout already bought extra geese 227/242 and won."
)
NO_UPLOAD = (
    "HOLD. Upload-bail (c): newest cut 56151152 COMPLETE 1681.2 would drop without a >=1500 "
    "COMPLETE newest-2 partner (shopbag 56151155 COMPLETE 1314.5 < 1500 and newer than cut 16; "
    "a new cut alone keeps shopbag and drops 1681.2; re-upload is 600-provisional not a "
    "partner). No licensed later-block. Public search newest still "
    "renjistarfall/kaggriculture-best-agent SHA 708c7485 V39 reprint Shop0909 144/648 + "
    "288/712 overlay (already rejected 0913s/0913t/0913u). Do not reupload boatlee 55710781. "
    "Cut 12/13 Hold."
)


def dump(name: str, obj: object) -> None:
    path = ROOT / "experiments" / name
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    print("WROTE", path)


def main() -> None:
    rolling = json.loads((ROOT / "experiments/20260913v_cut16_rolling.json").read_text(encoding="utf-8"))
    games = rolling["games"]
    assert [g["id"] for g in games] == IDS
    top = json.loads((ROOT / "experiments/20260913v_top10_games.json").read_text(encoding="utf-8"))
    old_packet = json.loads((ROOT / "experiments/20260913u_study_packet.json").read_text(encoding="utf-8"))
    old_algo = json.loads((ROOT / "experiments/20260913u_algo_note.json").read_text(encoding="utf-8"))
    old_gate = json.loads((ROOT / "experiments/20260913u_gate.json").read_text(encoding="utf-8"))
    old_hunt = json.loads((ROOT / "experiments/20260913u_hunt_report.json").read_text(encoding="utf-8"))
    old_loss = json.loads((ROOT / "experiments/20260913u_cut16_loss_class.json").read_text(encoding="utf-8"))

    dump(
        "20260913v_episode_report.json",
        {
            "date": "2026-09-13",
            "packet": "20260913v",
            "utc": "2026-09-13T17:38:14Z",
            "no_upload": True,
            "upload_bail": True,
            "hold": True,
            "root_main_py_untouched": True,
            "root_main_py_sha256": "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe",
            "boatlee_55710781_reupload": False,
            "live_newest_id": 56151152,
            "live_newest_score": 1681.2,
            "live_newest_status": "COMPLETE",
            "live_newest_name": "yamakawanin_king_v4e_rc4 cut 16",
            "live_newest_note": (
                "COMPLETE 1681.2 (was 1669.1). Newest public 108608562 updatedScore 1681.262. "
                "Newest-2 = shopbag reupload 56151155 (newer id, submissions 1314.5 / "
                "ListEpisodes last_updated 1314.519) + cut 16 56151152. Upload-bail TRUE (c): "
                "shopbag partner 1314.5 < 1500 and is newer than cut 16, so a new cut alone "
                "would drop the >=1500 COMPLETE. Study anyway. Hold."
            ),
            "cut15_id": 56146106,
            "cut15_score": 1864.4,
            "cut15_status": "COMPLETE",
            "cut15_note": "DROPPED from newest-2.",
            "shopbag_id": 56151155,
            "shopbag_score": 1314.5,
            "shopbag_status": "COMPLETE",
            "shopbag_lineage": 55962761,
            "newest_2": [56151155, 56151152],
            "heralces_rank_csv": 2022,
            "heralces_score": 1681.2,
            "n_teams_csv": 8911,
            "public_56151152": {
                "n_public": 234,
                "n_validation": 1,
                "n_completed_public": 234,
                "wtl": [103, 2, 129],
                "mean_margin": -1167.1,
                "status": "COMPLETE",
                "publicScore": 1681.2,
            },
            "rolling_ids": IDS,
            "rolling_forbidden_0913u": PREV_U,
            "ids_not_identical_to_0913u": True,
            "ids_disjoint_from_0913u": True,
            "rolling_n": 12,
            "rolling_n_steps": 720,
            "wtl": [6, 0, 6],
            "mean_margin": -3106.3,
            "rolling_note": (
                "Assigned cut16 newest-12 public ids from refreshed EpisodeService, all 720 "
                "DONE/DONE. Disjoint from 20260913u packet. 6W 6L. Worst AQiDA19 108550653 L "
                "-21800 7c6s vs 8c6s3g clone=1 extra sheep 218/227 extra geese 242/266. "
                "New-window dupakdungking 108608562 W +9867 6c12s vs 8c6s3g extra sheep "
                "218/242/266 already bought. Not opening-broke. Not freeze 9c9s."
            ),
        },
    )

    hunt = dict(old_hunt)
    hunt["packet"] = "20260913v"
    hunt["kernels_not_in_0913u_packet"] = False
    hunt.pop("kernels_not_in_0913t_packet", None)
    hunt["hunt_dir"] = "artifacts/public_sources/_hunt_20260913v"
    hunt["inspect_scripts"] = ["experiments/candidates/scan_hunt_20260913v.py"]
    hunt["payload_decode"] = "none_no_new_notebook"
    hunt["compare_0913u"] = {
        "hunt_dir": "artifacts/public_sources/_hunt_20260913u",
        "hunt_report": "experiments/20260913u_hunt_report.json",
        "gate": "experiments/20260913u_gate.json",
        "note": (
            "No new slug vs _hunt_20260913u. Public search newest is still "
            "renjistarfall/kaggriculture-best-agent (lastRunTime 2026-09-13 14:11:05.950000). "
            "Did not re-pull rejected kernels (renjistarfall V39 reprint, alperen metacounter, "
            "xuantianfengwu allocator, Ahmed V40, guru V39, yhay81 0913, wei v46d review, "
            "Ahmed V39 v39-ready-before-the-rush, aurax7 v4, crystalbaby V38, Ahmed V39 "
            "notebookda72f457f5, prvsiyan market-ledger, timed-six-cow, lokesh V37, "
            "crystalbaby dynamic-route, nusrati V35, sunil v4, dmitrii sale_horizon, "
            "municef1/bernubritz tapes, melomanpanda, zhincez, y3uanm rollback-v20, "
            "yhay81 0911-simple)."
        ),
    }
    hunt.pop("compare_0913t", None)
    hunt["public_search_newest"] = "renjistarfall/kaggriculture-best-agent"
    hunt["public_search_newest_lastRunTime"] = "2026-09-13 14:11:05.950000"
    hunt["author_list_note"] = (
        "yhay81 newest kaggriculture kernel is still shop-router-0913 2026-09-13 09:39 "
        "day-6 144/648. yamakawanin no rc5. Thomas no new tree. y3uanm no v6."
    )
    hunt["hunt"] = []
    dump("20260913v_hunt_report.json", hunt)

    gate = dict(old_gate)
    gate["packet"] = "20260913v"
    gate["live"] = dict(old_gate["live"])
    gate["live"]["cut16"] = dict(old_gate["live"]["cut16"])
    gate["live"]["cut16"]["score_complete"] = 1681.2
    gate["hunt_dir"] = "artifacts/public_sources/_hunt_20260913v"
    gate["hunt_report"] = "experiments/20260913v_hunt_report.json"
    gate["why"] = (
        "HOLD. Upload-bail is live: newest cut 56151152 COMPLETE 1681.2 partnered with newer "
        "shopbag 56151155 COMPLETE 1314.5 < 1500. A new cut uploaded alone would drop "
        "56151152 and keep shopbag as newest-2 partner (shopbag id is newer). Pairing a new "
        "cut with cut 16 would require a cut-16 reupload (600-provisional, two quota). freeze "
        "is false because of this upload-bail, not because a licensed later-block is ready. "
        "No new public later-block vs _hunt_20260913u. Public search newest still "
        "renjistarfall/kaggriculture-best-agent SHA 708c7485 (V39 reprint Shop0909 144/648 + "
        "288/712 overlay). king/Thomas/y3uanm/yhay81 author lists have no new later-block. "
        "Did not clone/G5-screen, did not pack or upload. Cut 12/13 stay Hold. Root main.py "
        "SHA untouched. Boatlee 55710781 never re-upload. Live cuts 14/15/16 not re-uploaded. "
        "227/242/266 wrap not licensed: AQiDA19/Hanaro/Wei Han/Excluding extra sheep 218/227 "
        "extra geese 242/266 and we lost; Hackoholics already bought 218/242/266 and lost 15s; "
        "mmwstudy already bought extra geese 227/242 and lost identical-clone -65; "
        "dupakdungking already bought extra sheep 218/242/266 and won YARN 6c12s +9867."
    )
    if gate["rejected"] and gate["rejected"][0]["kernel"] == "renjistarfall/kaggriculture-best-agent":
        gate["rejected"] = [dict(gate["rejected"][0])] + list(gate["rejected"][1:])
        gate["rejected"][0]["note"] = (
            "Still the public-search newest (lastRunTime 2026-09-13 14:11:05.950000). "
            "0913s/0913t/0913u already rejected SHA 708c7485 V39 reprint Shop0909 144/648 + "
            "288/712 overlay. Did not re-pull."
        )
    dump("20260913v_gate.json", gate)

    loss = dict(old_loss)
    loss["packet"] = "20260913v"
    loss["ids"] = IDS
    loss["ids_0913u"] = PREV_U
    loss.pop("ids_0913t", None)
    loss["disjoint_from_0913u"] = True
    loss.pop("disjoint_from_0913t", None)
    loss["wtl"] = [6, 0, 6]
    loss["mean_margin"] = -3106.3
    loss["clone_n"] = 12
    loss["land_pattern"] = "all 12 BUY_LAND 151/266 succeeded (prev_Q 1 then 2)"
    loss["cash_24_range"] = [3.0, 27.0]
    loss["wool_360"] = {
        "108608562": 236,
        "108604498": 232,
        "108586169": 37,
        "108550653": 1,
        "108545775": 1,
        "108520439": 1,
        "108509931": 231,
        "108489181": 43,
        "108484081": 37,
        "108445221": 1,
        "108441448": 11,
        "108441305": 37,
    }
    loss["wool_432"] = {
        "108608562": 232,
        "108604498": 209,
        "108586169": 1,
        "108550653": 5,
        "108545775": 24,
        "108520439": 5,
        "108509931": 158,
        "108489181": 1,
        "108484081": 125,
        "108445221": 1,
        "108441448": 1,
        "108441305": 1,
    }
    loss["same_class_as_0913c"] = True
    loss["same_class_note"] = (
        "Same extra-animal family as 09-13c/09-13t: extra-animal 8c6s3g plus extra-sheep 15s "
        "plus identical-clone extra-goose. WTL 6-0-6 mean -3106.3 vs 09-13u 4-0-8 mean -962.8. "
        "New window games are dupakdungking 108608562 YARN 6c12s +9867 and Hanaro 108604498 "
        "4c14s +114. clone=12/12."
    )
    loss["loss_class"] = LOSS
    loss["worst_losses"] = [
        {
            "id": 108550653,
            "opp": "AQiDA19",
            "margin": -21800.0,
            "herd_us": "7c6s",
            "herd_opp": "8c6s3g",
            "shops": ["BAKERY"],
        }
    ]
    dump("20260913v_cut16_loss_class.json", loss)

    algo = dict(old_algo)
    algo["packet"] = "20260913v"
    algo["live"] = dict(old_algo["live"])
    algo["live"]["cut16"] = dict(old_algo["live"]["cut16"])
    algo["live"]["cut16"]["csv_0913v_team_score"] = 1681.2
    algo["live"]["rank_csv_0913v"] = 2022
    fail = dict(old_algo["cut16_live_failure_class"])
    fail["0913v"] = {
        "file": "experiments/20260913v_cut16_rolling.json",
        "ids": IDS,
        "wtl": [6, 0, 6],
        "mean_margin": -3106.3,
        "clone": "12/12",
        "class": (
            "same extra-animal family: extra-animal 8c6s3g plus extra-sheep 15s plus "
            "identical-clone extra-goose"
        ),
        "heavy": [
            {
                "id": 108550653,
                "opp": "AQiDA19",
                "margin": -21800,
                "shops72": ["BAKERY"],
                "buy": "7c6s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
            {
                "id": 108545775,
                "opp": "Hanaro",
                "margin": -14377,
                "shops72": ["PIZZA_SHOP"],
                "buy": "9c5s vs 8c6s3g",
                "opp216": [218, 227, 242, 266],
                "wool_px_360": 1,
            },
        ],
    }
    algo["cut16_live_failure_class"] = fail
    algo["q1_reselect_after_216"] = {
        "licensed_this_fire": False,
        "note": (
            "No new Windows Python farm/route reselect after 216 distinct from cuts 14/15/16. "
            "Public search newest still renjistarfall/kaggriculture-best-agent writefile SHA "
            "708c7485 V39 reprint Shop0909 144/648 + 288/712 overlay (already rejected "
            "0913s/0913t/0913u). Author lists otherwise unchanged (no king rc5 / y3uanm v6 / "
            "Thomas new tree / Yusuke later-block)."
        ),
    }
    dump("20260913v_algo_note.json", algo)

    not_copied = list(old_packet["top_board"]["not_copied_from"]) + [
        "experiments/20260913u_top10_games.json"
    ]
    packet = {
        "title": "Kaggriculture study packet 2026-09-13v",
        "not_the_0913u_packet": True,
        "no_upload": NO_UPLOAD,
        "upload_bail": True,
        "upload_bail_reasons": {
            "a_newest_cut_pending": False,
            "b_newest_cut_complete_below_1500": False,
            "c_drop_ge1500_without_ge1500_partner": True,
        },
        "sources": {
            "leaderboard_zip": "artifacts/kaggle_runs/lb_20260913v/kaggriculture.zip",
            "leaderboard_csv": (
                "artifacts/kaggle_runs/lb_20260913v/"
                "kaggriculture-publicleaderboard-2026-09-13T17-38-14.csv"
            ),
            "leaderboard_api": "experiments/20260913v_public_leaderboard_api.json",
            "episodes_cut16": "experiments/episodes_56151152.json",
            "cut16_replays": "artifacts/kaggle_runs/cut16_20260913v",
            "top_replays": "artifacts/kaggle_runs/top_20260913v",
            "hunt_dir": "artifacts/public_sources/_hunt_20260913v",
            "cut16_screen": "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json",
            "cut16_divergence": "experiments/20260910b_cut16_divergence.json",
            "gate": "experiments/20260913v_gate.json",
            "episode_report": "experiments/20260913v_episode_report.json",
            "hunt_report": "experiments/20260913v_hunt_report.json",
            "algo_note": "experiments/20260913v_algo_note.json",
            "loss_class": "experiments/20260913v_cut16_loss_class.json",
        },
        "live": {
            "sixday": 56028043,
            "sixday_score": 1590.8,
            "sixday_status": "COMPLETE",
            "team_score": 1681.2,
            "rank": 2022,
            "n_teams": 8911,
            "shopbag_previous": 56112309,
            "shopbag_reupload": 56151155,
            "shopbag_status": "COMPLETE",
            "shopbag_score": 1314.5,
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
            "cut16_score": 1681.2,
            "root_main_py": "h2 65e6f5cd... unchanged",
            "gold21": 2901.3,
            "rank10": {"team": "binghua", "score": 2953.0},
            "rank1": {
                "team": "Majkel1337",
                "score": 3259.2,
                "submissionId": 56156662,
            },
            "public_cut16": {
                "n": 234,
                "wtl": [103, 2, 129],
                "mean_margin": -1167.1,
            },
        },
        "rolling": {
            "previous": "experiments/20260913u_cut16_rolling.json",
            "live_cut16": "experiments/20260913v_cut16_rolling.json",
            "ids": IDS,
            "ids_not_identical_to_0913u": True,
            "n": 12,
            "wtl": [6, 0, 6],
            "mean_margin": -3106.3,
            "loss_class": LOSS,
        },
        "excluding": {
            "id": 108550653,
            "margin": -21800.0,
            "clone": True,
            "Q": [3, 3],
            "land": [151, 266],
            "herd_us": "7c6s",
            "herd_opp": "8c6s3g",
            "sheep_steps_us": [2, 151, 196],
        },
        "top_board": {
            "source": "experiments/20260913v_top10_games.json",
            "not_copied_from": not_copied,
            "Majkel1337": {
                "land": [row["land"] for row in top],
                "herd": [row["herd"] for row in top],
                "wheat": [row["wheat"][0] for row in top],
                "shops": [row["shops72"][0] for row in top],
                "clone": "0_of_4",
                "episodes": [row["id"] for row in top],
                "note": (
                    "CSV #1 3259.2 live 3259.2 scoring sub 56156662. Ids disjoint from "
                    "20260913u Majkel set. Mid-land 150 then 218-222 (two 150/220/222; one "
                    "150/218/220/222; one 150/218), wheat 372-571, clone=0 on 4/4, goose mix "
                    "4g/0g/2g/0g. Opening land is not a later-block license."
                ),
            },
        },
        "cut12": old_packet["cut12"],
        "cut13": old_packet["cut13"],
        "cut15": old_packet["cut15"],
        "cut16": {
            "name": "yamakawanin king-v4e-rc4 shop-family later-block P3+ 288/360/432/576",
            "hold": False,
            "uploaded": 56151152,
            "status": "COMPLETE",
            "score": 1681.2,
            "windows_agent_so": False,
            "kernel": "yamakawanin/king-v4e-rc4",
            "agent_sha256": "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d",
            "reselect_steps": [216, 240, 241, 288, 360, 385, 432, 576],
            "reselect_after_216": [240, 241, 288, 360, 385, 432, 576],
            "sheep_200_267": [226, 241, 265],
            "not_227_242_266_wrap": True,
            "clone_g5": old_packet["cut16"]["clone_g5"],
            "why": (
                "Already live COMPLETE 1681.2. This cycle Hold: upload-bail (c) plus no new "
                "licensed later-block. Extra sheep 226/241/265 not 227/242/266. Rolling "
                "108550653 already faced opp extra sheep 218/227 extra geese 242/266 8c6s3g "
                "-21800; 108545775 extra sheep 218/227 extra geese 242/266 8c6s3g -14377; "
                "108509931 already bought 218/242/266 sheep and lost 15s -4788. New-window "
                "dupakdungking 108608562 already bought extra sheep 218/242/266 and won YARN "
                "6c12s vs 8c6s3g +9867. Not cut 12/13."
            ),
        },
        "cut17": {
            "hold": True,
            "uploaded": None,
            "why": (
                "No Windows-runnable Python later-block after 216 distinct from live cuts "
                "14/15/16. Hunt: no new slug vs 0913u; public search newest still "
                "renjistarfall/kaggriculture-best-agent SHA 708c7485 V39 reprint Shop0909 "
                "144/648 + 288/712 overlay; no king rc5 / y3uanm v6 / Thomas tree that "
                "actually splits after 216. Upload-bail would block even a licensed freeze: "
                "shopbag 56151155 is newer than cut 16, so a new cut alone drops 1681.2 and "
                "keeps 1314.5."
            ),
        },
        "hunt": [],
    }
    dump("20260913v_study_packet.json", packet)


if __name__ == "__main__":
    main()
