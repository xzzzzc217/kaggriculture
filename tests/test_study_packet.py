"""Study packet vs shipped Fieldbook tapes and recorded screens."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/candidates/yusuke_fieldbook"))
from fieldbook_logic import ROUTE_NAMES, ROUTES  # noqa: E402


def _herd_and_wheat(actions: list) -> tuple[Counter, int]:
    herd: Counter = Counter()
    wheat = 0
    for action in actions:
        for order in action.get("market") or []:
            if not order:
                continue
            if order[0] == "BUY_ANIMAL":
                herd[str(order[1])] += int(order[2]) if len(order) > 2 else 1
            elif order[0] == "SELL" and order[1] == "WHEAT":
                wheat += int(order[2]) if len(order) > 2 else 1
    return herd, wheat


def test_shipped_fieldbook_routes_match_tape_packet() -> None:
    tapes = json.loads((ROOT / "experiments/20260901_fieldbook_tapes.json").read_text(encoding="utf-8"))
    assert set(ROUTE_NAMES.values()) >= {"BALANCED", "YARN_ENGINE"}
    for index, label in ROUTE_NAMES.items():
        herd, wheat = _herd_and_wheat(ROUTES[index])
        rec = tapes[label]
        assert dict(herd) == rec["buy_animals"], label
        assert wheat == rec["sells"]["WHEAT"], label
    assert tapes["BALANCED"]["buy_animals"] != tapes["YARN_ENGINE"]["buy_animals"]


def test_fieldbook_sha_and_root_h2() -> None:
    fieldbook = (ROOT / "experiments/candidates/yusuke_fieldbook/main.py").read_bytes()
    assert hashlib.sha256(fieldbook).hexdigest().startswith("de668f7f")
    root = (ROOT / "main.py").read_bytes()
    assert hashlib.sha256(root).hexdigest() == (
        "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
    )


def test_cut10_screen_clone_g5_and_summit_flips() -> None:
    screen = json.loads((ROOT / "experiments/candidates/yusuke_fieldbook/screen.json").read_text(encoding="utf-8"))
    assert screen["n"] == 13
    for key in ("prvsiyan_clone", "fufu_clone", "masa_clone"):
        assert screen["rows"][key]["win"] is True
    for key in ("mtn_11", "yusuke_11", "hanserong_11"):
        assert screen["rows"][key]["margin"] > 0
    g5 = json.loads((ROOT / "experiments/candidates/yusuke_fieldbook/g5.json").read_text(encoding="utf-8"))
    assert g5["subin_97399969"]["win"] is True
    assert g5["james_95677563"]["win"] is True


def test_rolling12_and_top_board_facts() -> None:
    rolling = json.loads((ROOT / "experiments/20260901_rolling12_autopsy.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "shops72")
    assert len(rolling["shopbag"]) == 12
    assert len(rolling["v4"]) == 12
    for row in rolling["shopbag"] + rolling["v4"]:
        assert all(key in row for key in need)
    eight_c4 = sum(
        1
        for row in rolling["shopbag"]
        if row["buy_us"].get("COW") == 8 and row["buy_us"].get("SHEEP") == 4
    )
    opp_17 = sum(1 for row in rolling["shopbag"] if row["pasture"][1] == 17)
    assert eight_c4 >= 8
    assert opp_17 >= 8

    games = json.loads((ROOT / "experiments/20260901_top10_games.json").read_text(encoding="utf-8"))
    tetsuya = [row for row in games if row["team"] == "tetsuya"]
    crop = [row for row in games if row["team"] == "Crop Dusta"]
    band = [
        row
        for row in games
        if row["team"] in {"Kaileh57", "QQ Farming", "Driz Lo", "Yusuke Hayashi", "MtN"}
    ]
    assert tetsuya and all(row["land"] == [169, 241] and row["clone"] is False for row in tetsuya)
    wheat = [row["wheat"][0] for row in crop]
    assert crop and all(row["land"] == [122, 199] for row in crop)
    assert min(wheat) < 600 and max(wheat) > 1800
    assert band and all(row["land"] == [151, 266] and row["melon"][0] == 72 for row in band)


def test_playbook_names_cut11_hold_and_v5_superseded() -> None:
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**10** `yusuke_fieldbook`" in playbook
    assert "**11** Yusuke six-day" in playbook
    assert "Live `56028043`" in playbook
    assert "Superseded by cut 10" in playbook
    assert "Live `55962758`" in playbook
    packet = json.loads((ROOT / "experiments/20260906_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != "Kaggriculture study packet 2026-09-05"
    assert packet["cut11"]["hold"] is False
    assert packet["cut11"]["uploaded"] == 56028043
    assert packet["live"]["fieldbook"] == 55962758
    assert "56028043" in packet["no_upload"]
    assert "agent.so" in playbook and "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    assert "按建议方案提交" in log and "55962758" in log
    assert "55962761" in log
    latest = log.split("## 2026-09-06")[-1]
    assert "56028043" in latest
    assert "提交" in latest


def test_20260904_packet_top_board_not_copied_from_0901() -> None:
    need = ("land", "herd", "wheat", "shops", "clone")
    packet = json.loads((ROOT / "experiments/20260904_study_packet.json").read_text(encoding="utf-8"))
    for team in ("Giulio Ravasio", "Knight of Favonius", "sbol ball"):
        row = packet["top_board"][team]
        assert all(key in row for key in need), team
    games = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old = json.loads((ROOT / "experiments/20260901_top10_games.json").read_text(encoding="utf-8"))
    assert {row["id"] for row in games}.isdisjoint({row["id"] for row in old})
    giulio = [row for row in games if row["team"] == "Giulio Ravasio"]
    knight = [row for row in games if row["team"] == "Knight of Favonius"]
    sbol = [row for row in games if row["team"] == "sbol ball"]
    crop = [row for row in games if row["team"] == "Crop Dusta"]
    yusuke = [row for row in games if row["team"] == "Yusuke Hayashi"]
    old_tetsuya = [row for row in old if row["team"] == "tetsuya"]
    old_crop = [row for row in old if row["team"] == "Crop Dusta"]
    assert giulio and all(row["land"] == [151, 266] for row in giulio)
    assert all(row["clone"] is True for row in giulio)
    assert all(row["land"] != [169, 241] for row in giulio)
    assert old_tetsuya and all(row["land"] == [169, 241] for row in old_tetsuya)
    assert knight and all(row["land"] == [151, 266] for row in knight)
    wheat_k = [row["wheat"][0] for row in knight]
    assert min(wheat_k) > 1000
    assert sbol and all(row["land"] == [151, 266] and row["melon"][0] == 72 for row in sbol)
    assert crop and all(row["clone"] is False for row in crop)
    assert all(row["land"][0] == 122 and row["land"][1] in {200, 201} for row in crop)
    assert old_crop and all(row["land"] == [122, 199] for row in old_crop)
    assert yusuke and all(row["buy"] == {"COW": 9, "SHEEP": 9} for row in yusuke)
    hunt_names = [row["kernel"] for row in packet["hunt"]]
    assert "yhay81/six-day-public-state-fieldbook" in hunt_names
    assert packet["cut11"]["hold"] is True
    assert "Windows" in packet["cut11"]["why"] or packet["cut10_screen"]["windows_agent_so"] is False


def test_20260904_fieldbook_newest12_autopsy_keys() -> None:
    rolling = json.loads((ROOT / "experiments/20260904_fieldbook_rolling12.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat")
    rows = rolling["games"]
    assert len(rows) == 12
    for row in rows:
        assert all(key in row for key in need)
        assert row["land"] == [151, 266]
    assert sum(1 for row in rows if row["clone"] is True) >= 10
    packet = json.loads((ROOT / "experiments/20260904_study_packet.json").read_text(encoding="utf-8"))
    assert "freeze-after-day-9" in packet["rolling12"]["loss_class"]
    assert packet["rolling12"]["wtl"] == [2, 2, 8]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == [2, 2, 8]


def test_20260905_packet_newer_than_0904_and_jesse_not_copied() -> None:
    old_packet = json.loads((ROOT / "experiments/20260904_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260905_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert "提交" in packet["no_upload"]
    assert packet["cut11"]["hold"] is True
    assert packet["live"]["fieldbook"] == 55962758
    assert packet["cut10_screen"]["windows_agent_so"] is False

    need = ("land", "herd", "wheat", "shops", "clone")
    jesse_pkt = packet["top_board"]["Jesse Bullard"]
    assert all(key in jesse_pkt for key in need)
    old_games = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    assert "Jesse Bullard" not in {row["team"] for row in old_games}
    jesse = [row for row in new_games if row["team"] == "Jesse Bullard"]
    assert jesse
    for row in jesse:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][:2] == [151, 266]
        assert row["clone"] is True
        assert row["id"] not in {g["id"] for g in old_games}
    herds = {(row["buy"].get("COW", 0), row["buy"].get("SHEEP", 0)) for row in jesse}
    assert (9, 5) not in herds
    wheat_j = [row["wheat"][0] for row in jesse]
    assert max(wheat_j) < 1000
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "tetsutani/shape-the-shop-work-the-pasture-kaggriculture" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**10** `yusuke_fieldbook`" in playbook
    assert "**11** Yusuke six-day" in playbook
    assert "Live `56028043`" in playbook
    assert "Live `55962758`" in playbook


def test_20260905_fieldbook_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260904_fieldbook_rolling12.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260905_fieldbook_rolling12.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat")
    rows = rolling["games"]
    assert len(rows) == 12
    old_ids = {row["id"] for row in old["games"]}
    new_ids = {row["id"] for row in rows}
    assert new_ids.isdisjoint(old_ids)
    for row in rows:
        assert all(key in row for key in need)
        assert row["land"][:2] == [151, 266]
    packet = json.loads((ROOT / "experiments/20260905_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling12"]["ids"] == [row["id"] for row in rows]
    assert "freeze-after-day-9" in packet["rolling12"]["loss_class"]
    assert "227" in packet["rolling12"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling12"]["wtl"]


def test_20260905_extra_sheep_steps_from_real_replay() -> None:
    sys.path.insert(0, str(ROOT / "experiments/candidates"))
    from measure_top_and_sheep_20260905 import sheep_timeline  # noqa: WPS433

    sheep = json.loads((ROOT / "experiments/20260905_9c9s_sheep_steps.json").read_text(encoding="utf-8"))
    yusuke = sheep["yusuke_live"]
    assert yusuke
    for rec in yusuke:
        steps = [e["step"] for e in rec["extra_sheep_steps"]]
        assert steps == [227, 242, 266], rec["id"]
        assert rec["id"] in {105395079, 105391598, 105388041, 105384084}
    named = [row for row in sheep["fieldbook_9c9s"] if row["role"] == "opp" and row["buy"].get("SHEEP") == 9]
    assert named
    for rec in named:
        steps = [e["step"] for e in rec["extra_sheep_steps"]]
        assert steps == [227, 242, 266], rec

    replay_path = (
        ROOT / "artifacts/kaggle_runs/top_20260905" / "episode-105395079-replay.json"
    )
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    seat = replay["info"]["TeamNames"].index("Yusuke Hayashi")
    _buy, _events, extra = sheep_timeline(replay, seat)
    assert [e["step"] for e in extra] == [227, 242, 266]
    assert [e["qty"] for e in extra] == [1, 2, 1]
    packet = json.loads((ROOT / "experiments/20260905_study_packet.json").read_text(encoding="utf-8"))
    assert packet["extra_sheep"]["yusuke_live"]["steps"] == [227, 242, 266]
    assert packet["extra_sheep"]["yusuke_live"]["episodes"]
    assert packet["extra_sheep"]["rolling12_9c9s_opponents"]


def test_20260906_packet_newer_than_0905_and_keiz_not_copied() -> None:
    old_packet = json.loads((ROOT / "experiments/20260905_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260906_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert "56028043" in packet["no_upload"]
    assert packet["cut11"]["hold"] is False
    assert packet["cut11"]["uploaded"] == 56028043
    assert packet["live"]["fieldbook"] == 55962758
    assert packet["cut10_screen"]["windows_agent_so"] is False
    need = ("land", "herd", "wheat", "shops", "clone")
    keiz_pkt = packet["top_board"]["keiz"]
    assert all(key in keiz_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    assert "keiz" not in {row["team"] for row in old04} | {row["team"] for row in old05}
    keiz = [row for row in new_games if row["team"] == "keiz"]
    assert keiz
    for row in keiz:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][:2] == [151, 266]
        assert row["buy"].get("GOOSE") == 1
        assert row["id"] not in {g["id"] for g in old04} | {g["id"] for g in old05}
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "evgendvorkin/kaggriculture" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**10** `yusuke_fieldbook`" in playbook
    assert "**11** Yusuke six-day" in playbook
    assert "Live `56028043`" in playbook
    assert "Live `55962758`" in playbook
    assert "BALANCED-tail patch" in playbook


def test_20260906_fieldbook_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260905_fieldbook_rolling12.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260906_fieldbook_rolling12.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
        assert row["land"][:2] == [151, 266]
    packet = json.loads((ROOT / "experiments/20260906_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling12"]["ids"] == [row["id"] for row in rows]
    assert "freeze-after-day-9" in packet["rolling12"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling12"]["wtl"]


def test_20260906_reselect_vs_patch_from_real_replays() -> None:
    sys.path.insert(0, str(ROOT / "experiments/candidates"))
    from study_20260906 import canon, count_diffs, load_acts  # noqa: WPS433
    from fieldbook_logic import ROUTES

    rec = json.loads((ROOT / "experiments/20260906_yusuke_reselect_vs_patch.json").read_text(encoding="utf-8"))
    assert rec["episodes"] if "episodes" in rec else rec["reference_episode"]
    assert rec["is_balanced_tail_patch"] is False
    assert rec["is_later_block_reselect"] is False
    assert rec["reference_episode"] == 105395079
    assert rec["newest_two"]
    for row in rec["newest_two"]:
        assert row["id"] in {105440805, 105437312}
        assert row["vs_old_tape_0_266"]["farmer"] == 0
        assert row["vs_old_tape_0_266"]["hands"] == 0
        assert row["vs_old_tape_0_266"]["market"] == 0

    _, _, yusuke = load_acts(
        ROOT / "artifacts/kaggle_runs/top_20260905/episode-105395079-replay.json",
        "Yusuke Hayashi",
    )
    balanced = [canon(a) for a in ROUTES[0]]
    prefix = count_diffs(yusuke, balanced, 0, 217)
    tail = count_diffs(yusuke, balanced, 217, 267, ignore_sheep=True)
    assert prefix["first"] == 1
    assert prefix["farmer"] > 0 and prefix["hands"] > 0
    assert tail["first"] == 217
    assert tail["farmer"] > 0 and tail["hands"] > 0
    packet = json.loads((ROOT / "experiments/20260906_study_packet.json").read_text(encoding="utf-8"))
    assert packet["reselect_vs_patch"]["episodes"]
    assert packet["reselect_vs_patch"]["is_balanced_tail_patch"] is False
    assert packet["reselect_vs_patch"]["is_later_block_reselect"] is False
    assert packet["reselect_vs_patch"]["vs_balanced_0_216"]["first"] == 1


def test_20260910_packet_newer_than_0909_and_otter_not_copied() -> None:
    old_packet = json.loads((ROOT / "experiments/20260909_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260910_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut15"]["hold"] is False
    assert packet["cut15"]["uploaded"] == 56146106
    assert packet["live"]["newest_2"] == [56146106, 56112309]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut15"]["not_227_242_266_wrap"] is True
    assert packet["cut15"]["sheep_200_267"] == [265]
    assert packet["cut15"]["windows_agent_so"] is False
    assert "56146106" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    otter_pkt = packet["top_board"]["Otter Vibe"]
    assert all(key in otter_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09}
    assert "Otter Vibe" not in prior_teams
    otter = [row for row in new_games if row["team"] == "Otter Vibe"]
    assert otter
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09}
    for row in otter:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 121
        assert row["land"][1] in {242, 247}
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "thomastschinkel/kaggriculture-93-8-win-rate-public-state-router" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**15** `thomastschinkel_psr_938`" in playbook
    assert "Live `56146106`" in playbook
    assert "Live `56111821`" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-10")[-1]
    assert "56146106" in latest
    assert "提交" in latest or "Submitted" in latest


def test_20260910_cut14_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260909_sixday_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260910_cut14_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260910_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0909"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [3, 2, 7]


def test_20260910_cut15_screen_sha_and_not_227_wrap() -> None:
    digest = hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest()
    assert digest == "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
    agent = (ROOT / "experiments/candidates/thomastschinkel_psr_938/main.py").read_bytes()
    assert hashlib.sha256(agent).hexdigest() == (
        "b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522"
    )
    text = agent.decode("utf-8")
    assert "ctypes" not in text
    assert "agent.so" not in text
    assert "t % 144 == 0" in text
    screen = json.loads(
        (ROOT / "experiments/candidates/thomastschinkel_psr_938/screen.json").read_text(encoding="utf-8")
    )
    assert screen["n"] == 5 and screen["wins"] == 5
    assert screen["windows_agent_so"] is False
    for key in ("prvsiyan_clone", "fufu_clone", "masa_clone", "subin_97399969", "james_95677563"):
        row = screen["rows"][key]
        assert row["win"] is True
        assert row["statuses"] == ["DONE", "DONE"]
    divergence = json.loads((ROOT / "experiments/20260910_cut15_divergence.json").read_text(encoding="utf-8"))
    assert divergence["reselect_after_216"] == [288, 432, 576]
    assert divergence["main_sheep_200_267"] == [265]
    assert divergence["not_227_242_266_wrap"] is True
    assert divergence["live_217_differs_from_sixday"] is True
    assert divergence["live_217_differs_from_balanced"] is True
    assert divergence["live_217_differs_from_cut14"] is True
    packet = json.loads((ROOT / "experiments/20260910_study_packet.json").read_text(encoding="utf-8"))
    assert packet["cut15"]["clone_g5"]["prvsiyan_clone"] == 5757.0
    assert packet["cut15"]["clone_g5"]["james_95677563"] == 68313.0


def test_20260910b_packet_newer_than_0910_and_ymg_aq_not_copied() -> None:
    old_packet = json.loads((ROOT / "experiments/20260910_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260910b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["sheep_200_267"] == [226, 241, 265]
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    ymg_pkt = packet["top_board"]["ymg_aq"]
    assert all(key in ymg_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260910b_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "ymg_aq" not in prior_teams
    ymg = [row for row in new_games if row["team"] == "ymg_aq"]
    assert ymg
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10}
    for row in ymg:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"] == [121, 170]
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "yamakawanin/king-v4e-rc4" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "Live `56146106`" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-10b")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Submitted" in latest


def test_20260910b_cut15_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260910_cut14_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260910b_cut15_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260910b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0910"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 1, 7]


def test_20260910b_cut16_screen_sha_and_not_227_wrap() -> None:
    digest = hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest()
    assert digest == "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
    agent = (ROOT / "experiments/candidates/yamakawanin_king_v4e_rc4/main.py").read_bytes()
    assert hashlib.sha256(agent).hexdigest() == (
        "26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d"
    )
    text = agent.decode("utf-8")
    assert "import ctypes" not in text
    assert text.strip().endswith("agent=king_v4e_rc4")
    screen = json.loads(
        (ROOT / "experiments/candidates/yamakawanin_king_v4e_rc4/screen.json").read_text(encoding="utf-8")
    )
    assert screen["n"] == 5 and screen["wins"] == 5
    assert screen["windows_agent_so"] is False
    for key in ("prvsiyan_clone", "fufu_clone", "masa_clone", "subin_97399969", "james_95677563"):
        row = screen["rows"][key]
        assert row["win"] is True
        assert row["statuses"] == ["DONE", "DONE"]
    divergence = json.loads((ROOT / "experiments/20260910b_cut16_divergence.json").read_text(encoding="utf-8"))
    assert 288 in divergence["reselect_after_216"]
    assert 432 in divergence["reselect_after_216"]
    assert 576 in divergence["reselect_after_216"]
    assert divergence["main_sheep_200_267"] == [226, 241, 265]
    assert divergence["not_227_242_266_wrap"] is True
    assert divergence["live_217_differs_from_sixday"] is True
    assert divergence["live_217_differs_from_balanced"] is True
    assert divergence["live_217_differs_from_cut14"] is True
    assert divergence["live_217_differs_from_cut15"] is True
    packet = json.loads((ROOT / "experiments/20260910b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["cut16"]["clone_g5"]["prvsiyan_clone"] == 12627.0
    assert packet["cut16"]["clone_g5"]["james_95677563"] == 77153.0


def test_20260911_packet_newer_than_0910b_and_majkel_not_copied() -> None:
    old_packet = json.loads((ROOT / "experiments/20260910b_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260911_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1799.2
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["sheep_200_267"] == [226, 241, 265]
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "Hold" in packet["no_upload"] or "HOLD" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "xuantianfengwu/kaggriculture-fixed-hybrid-core" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1799.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-11")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260911_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260910b_cut15_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260911_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260911_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0910b"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260911b_packet_newer_than_0911_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260911_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260911b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1757.2
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10 + old11}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "yhay81/shop-router-0911-simple" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1757.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-11b")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260911b_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260911_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260911b_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260911b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0911"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [1, 0, 11]


def test_20260912_packet_newer_than_0911b_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260911b_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260912_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1730.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10 + old11 + old11b}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "ahmedberatozer/kaggriculture-v36-guarded-four-turn-sales" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1730.1 COMPLETE" in playbook
    assert "1757.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-12")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260912_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260911b_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260912_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260912_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0911b"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260912b_packet_newer_than_0912_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260912_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260912b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1695.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10 + old11 + old11b + old12}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "y3uanm/kaggriculture-safe-baseline-rollback-v20" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1695.1 COMPLETE" in playbook
    assert "1730.1 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-12b")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260912b_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260912_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260912b_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260912b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0912"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [3, 0, 9]


def test_20260912c_packet_newer_than_0912b_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260912b_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260912c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1682.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10 + old11 + old11b + old12 + old12b}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "ahmedberatozer/smarter-feed-stronger-margins" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1682.4 COMPLETE" in playbook
    assert "1695.1 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-12c")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260912c_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260912b_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260912c_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260912c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0912b"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260912d_packet_newer_than_0912c_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260912c_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260912d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1686.8
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in old04 + old05 + old06 + old09 + old10 + old11 + old11b + old12 + old12b + old12c}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "nusrati/2650-score" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1686.8 COMPLETE" in playbook
    assert "1682.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-12d")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260912d_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260912c_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260912d_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260912d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0912c"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260912e_packet_newer_than_0912d_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260912d_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260912e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1682.0
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04 + old05 + old06 + old09 + old10 + old11 + old11b + old12 + old12b + old12c + old12d
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "lokesh0252/kaggriculture-v1" in hunt_new
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1682.0 COMPLETE" in playbook
    assert "1686.8 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-12e")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260912e_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260912d_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260912e_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260912e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0912d"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260913_packet_newer_than_0912e_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260912e_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1683.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    assert sum(1 for row in majkel if row["clone"] is False) >= 3
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0912e_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1683.4 COMPLETE" in playbook
    assert "1682.0 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260912e_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0912e"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913b_packet_newer_than_0913_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1691.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "xuantianfengwu/kaggriculture-timed-six-cow" in hunt_new
    hunt_report = json.loads((ROOT / "experiments/20260913b_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1691.4 COMPLETE" in playbook
    assert "1683.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13b")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913b_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913b_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260913c_packet_newer_than_0913b_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913b_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1696.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "prvsiyan/kaggriculture-market-ledger-seasonal-counterplay" in hunt_new
    hunt_report = json.loads((ROOT / "experiments/20260913c_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913b_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1696.4 COMPLETE" in playbook
    assert "1691.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13c")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913c_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913b_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913c_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913b"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913d_packet_newer_than_0913c_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913c_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1698.7
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913d_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913c_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1698.7 COMPLETE" in playbook
    assert "1696.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13d")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913d_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913c_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913d_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913c"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913e_packet_newer_than_0913d_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913d_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1695.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "ahmedberatozer/notebookda72f457f5" in hunt_new
    hunt_report = json.loads((ROOT / "experiments/20260913e_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913d_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1695.5 COMPLETE" in playbook
    assert "1698.7 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13e")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913e_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913d_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913e_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913d"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913f_packet_newer_than_0913e_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913e_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913f_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1697.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913f_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913e_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1697.5 COMPLETE" in playbook
    assert "1695.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13f")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913f_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913e_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913f_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913f_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913e"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260913g_packet_newer_than_0913f_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913f_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913g_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1702.8
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913g_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913f_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1702.8 COMPLETE" in playbook
    assert "1697.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13g")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913g_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913f_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913g_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913g_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913f"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913h_packet_newer_than_0913g_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913g_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913h_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1691.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["clone"] is False
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913h_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913g_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1691.5 COMPLETE" in playbook
    assert "1702.8 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13h")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913h_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913g_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913h_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913h_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913g"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260913i_packet_newer_than_0913h_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913h_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913i_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1696.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913i_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913h_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1696.4 COMPLETE" in playbook
    assert "1691.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13i")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913i_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913h_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913i_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913i_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913h"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913j_packet_newer_than_0913i_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913i_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913j_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1692.8
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    assert "crystalbaby/kaggriculture-v38-public-submission" in hunt_new
    hunt_report = json.loads((ROOT / "experiments/20260913j_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913i_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1692.8 COMPLETE" in playbook
    assert "1696.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13j")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913j_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913i_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913j_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913j_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913i"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260913k_packet_newer_than_0913j_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913j_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913k_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1688.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    old13j = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913k_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
        + old13j
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913k_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913j_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1688.5 COMPLETE" in playbook
    assert "1692.8 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13k")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913k_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913j_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913k_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913k_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913j"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913l_packet_newer_than_0913k_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913k_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913l_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1692.2
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    old13j = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    old13k = json.loads((ROOT / "experiments/20260913k_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913l_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
        + old13j
        + old13k
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913l_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913k_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1692.2 COMPLETE" in playbook
    assert "1688.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13l")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913l_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913k_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913l_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913l_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913k"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260913m_packet_newer_than_0913l_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913l_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913m_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1693.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    old13j = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    old13k = json.loads((ROOT / "experiments/20260913k_top10_games.json").read_text(encoding="utf-8"))
    old13l = json.loads((ROOT / "experiments/20260913l_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913m_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
        + old13j
        + old13k
        + old13l
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert "aurax7/kaggriculture-shop-router-reactive-v4" in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / "experiments/20260913m_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913l_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1693.4 COMPLETE" in playbook
    assert "1692.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13m")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913m_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913l_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913m_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913m_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913l"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913n_packet_newer_than_0913m_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913m_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913n_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1693.6
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    old13j = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    old13k = json.loads((ROOT / "experiments/20260913k_top10_games.json").read_text(encoding="utf-8"))
    old13l = json.loads((ROOT / "experiments/20260913l_top10_games.json").read_text(encoding="utf-8"))
    old13m = json.loads((ROOT / "experiments/20260913m_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913n_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
        + old13j
        + old13k
        + old13l
        + old13m
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert "ahmedberatozer/kaggriculture-v39-ready-before-the-rush" in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / "experiments/20260913n_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913m_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1693.6 COMPLETE" in playbook
    assert "1693.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13n")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913n_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913m_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913n_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913n_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913m"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913o_packet_newer_than_0913n_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913n_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913o_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1690.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    old13j = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    old13k = json.loads((ROOT / "experiments/20260913k_top10_games.json").read_text(encoding="utf-8"))
    old13l = json.loads((ROOT / "experiments/20260913l_top10_games.json").read_text(encoding="utf-8"))
    old13m = json.loads((ROOT / "experiments/20260913m_top10_games.json").read_text(encoding="utf-8"))
    old13n = json.loads((ROOT / "experiments/20260913n_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913o_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
        + old13j
        + old13k
        + old13l
        + old13m
        + old13n
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert "yhay81/shop-router-0913" in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / "experiments/20260913o_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913n_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1690.5 COMPLETE" in playbook
    assert "1693.6 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13o")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913o_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913n_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913o_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913o_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913n"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913p_packet_newer_than_0913o_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913o_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913p_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1682.9
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    old09 = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    old10 = json.loads((ROOT / "experiments/20260910_top10_games.json").read_text(encoding="utf-8"))
    old11 = json.loads((ROOT / "experiments/20260911_top10_games.json").read_text(encoding="utf-8"))
    old11b = json.loads((ROOT / "experiments/20260911b_top10_games.json").read_text(encoding="utf-8"))
    old12 = json.loads((ROOT / "experiments/20260912_top10_games.json").read_text(encoding="utf-8"))
    old12b = json.loads((ROOT / "experiments/20260912b_top10_games.json").read_text(encoding="utf-8"))
    old12c = json.loads((ROOT / "experiments/20260912c_top10_games.json").read_text(encoding="utf-8"))
    old12d = json.loads((ROOT / "experiments/20260912d_top10_games.json").read_text(encoding="utf-8"))
    old12e = json.loads((ROOT / "experiments/20260912e_top10_games.json").read_text(encoding="utf-8"))
    old13 = json.loads((ROOT / "experiments/20260913_top10_games.json").read_text(encoding="utf-8"))
    old13b = json.loads((ROOT / "experiments/20260913b_top10_games.json").read_text(encoding="utf-8"))
    old13c = json.loads((ROOT / "experiments/20260913c_top10_games.json").read_text(encoding="utf-8"))
    old13d = json.loads((ROOT / "experiments/20260913d_top10_games.json").read_text(encoding="utf-8"))
    old13e = json.loads((ROOT / "experiments/20260913e_top10_games.json").read_text(encoding="utf-8"))
    old13f = json.loads((ROOT / "experiments/20260913f_top10_games.json").read_text(encoding="utf-8"))
    old13g = json.loads((ROOT / "experiments/20260913g_top10_games.json").read_text(encoding="utf-8"))
    old13h = json.loads((ROOT / "experiments/20260913h_top10_games.json").read_text(encoding="utf-8"))
    old13i = json.loads((ROOT / "experiments/20260913i_top10_games.json").read_text(encoding="utf-8"))
    old13j = json.loads((ROOT / "experiments/20260913j_top10_games.json").read_text(encoding="utf-8"))
    old13k = json.loads((ROOT / "experiments/20260913k_top10_games.json").read_text(encoding="utf-8"))
    old13l = json.loads((ROOT / "experiments/20260913l_top10_games.json").read_text(encoding="utf-8"))
    old13m = json.loads((ROOT / "experiments/20260913m_top10_games.json").read_text(encoding="utf-8"))
    old13n = json.loads((ROOT / "experiments/20260913n_top10_games.json").read_text(encoding="utf-8"))
    old13o = json.loads((ROOT / "experiments/20260913o_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260913p_top10_games.json").read_text(encoding="utf-8"))
    prior_teams = {row["team"] for row in old04 + old05 + old06 + old09 + old10}
    assert "Majkel1337" not in prior_teams
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {
        g["id"]
        for g in old04
        + old05
        + old06
        + old09
        + old10
        + old11
        + old11b
        + old12
        + old12b
        + old12c
        + old12d
        + old12e
        + old13
        + old13b
        + old13c
        + old13d
        + old13e
        + old13f
        + old13g
        + old13h
        + old13i
        + old13j
        + old13k
        + old13l
        + old13m
        + old13n
        + old13o
    }
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert "guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f" in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / "experiments/20260913p_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913o_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1682.9 COMPLETE" in playbook
    assert "1690.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13p")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913p_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913o_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913p_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913p_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913o"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]

def test_20260913q_packet_newer_than_0913p_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / 'experiments/20260913p_study_packet.json').read_text(encoding='utf-8'))
    packet = json.loads((ROOT / 'experiments/20260913q_study_packet.json').read_text(encoding='utf-8'))
    assert packet['title'] != old_packet['title']
    assert packet['cut16']['hold'] is False
    assert packet['cut16']['uploaded'] == 56151152
    assert packet['cut16']['status'] == 'COMPLETE'
    assert packet['cut16']['score'] == 1687.3
    assert packet['live']['newest_2'] == [56151155, 56151152]
    assert packet['cut12']['hold'] is True
    assert packet['cut13']['hold'] is True
    assert packet['cut17']['hold'] is True
    assert packet['upload_bail'] is True
    assert packet['cut16']['not_227_242_266_wrap'] is True
    assert packet['cut16']['windows_agent_so'] is False
    assert '56151152' in packet['no_upload']
    assert '55710781' in packet['no_upload']
    assert 'HOLD' in packet['no_upload'] or 'Hold' in packet['no_upload']

    need = ('land', 'herd', 'wheat', 'shops', 'clone')
    majkel_pkt = packet['top_board']['Majkel1337']
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        '20260904','20260905','20260906','20260909','20260910','20260911','20260911b',
        '20260912','20260912b','20260912c','20260912d','20260912e','20260913','20260913b',
        '20260913c','20260913d','20260913e','20260913f','20260913g','20260913h','20260913i',
        '20260913j','20260913k','20260913l','20260913m','20260913n','20260913o','20260913p',
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f'experiments/{name}_top10_games.json').read_text(encoding='utf-8')))
    new_games = json.loads((ROOT / 'experiments/20260913q_top10_games.json').read_text(encoding='utf-8'))
    majkel = [row for row in new_games if row['team'] == 'Majkel1337']
    assert majkel
    prior_ids = {g['id'] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ('land', 'buy', 'wheat', 'shops72', 'clone'))
        assert row['land'][0] == 150
        assert row['id'] not in prior_ids
    hunt_new = {row['kernel'] for row in packet['hunt']}
    hunt_old = {row['kernel'] for row in old_packet['hunt']}
    assert 'ahmedberatozer/kaggriculture-v40-plans-that-fit-the-shops' in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / 'experiments/20260913q_hunt_report.json').read_text(encoding='utf-8'))
    assert hunt_report['any_licensed_for_extract'] is False
    assert hunt_report['kernels_not_in_0913p_packet'] is True
    playbook = (ROOT / 'docs/shop_bag_strategy.md').read_text(encoding='utf-8')
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert '1687.3 COMPLETE' in playbook
    assert '1682.9 COMPLETE' in playbook
    assert 'Do not claim Windows ran' in playbook
    log = (ROOT / 'docs/progress_log.md').read_text(encoding='utf-8')
    latest = log.split('## 2026-09-13q')[-1]
    assert '56151152' in latest
    assert '56151155' in latest
    assert 'Hold' in latest


def test_20260913q_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / 'experiments/20260913p_cut16_rolling.json').read_text(encoding='utf-8'))
    rolling = json.loads((ROOT / 'experiments/20260913q_cut16_rolling.json').read_text(encoding='utf-8'))
    need = ('margin', 'clone', 'buy_us', 'buy_opp', 'pasture', 'wheat', 'cash_24')
    rows = rolling['games']
    assert len(rows) == 12
    assert {row['id'] for row in rows}.isdisjoint({row['id'] for row in old['games']})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / 'experiments/20260913q_study_packet.json').read_text(encoding='utf-8'))
    assert packet['rolling']['ids'] == [row['id'] for row in rows]
    assert packet['rolling']['ids_not_identical_to_0913p'] is True
    assert 'extra-animal' in packet['rolling']['loss_class']
    wins = sum(1 for row in rows if row['win'])
    ties = sum(1 for row in rows if row['tie'])
    losses = sum(1 for row in rows if not row['win'] and not row['tie'])
    assert [wins, ties, losses] == packet['rolling']['wtl']
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260913r_packet_newer_than_0913q_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913q_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913r_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1680.9
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260913r_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert "alperen5252525/kaggriculture-metacounter-r1" in hunt_new
    assert "xuantianfengwu/kaggriculture-land-labor-capital-allocator" in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / "experiments/20260913r_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913q_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1680.9 COMPLETE" in playbook
    assert "1687.3 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13r")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913r_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913q_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913r_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913r_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913q"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [3, 0, 9]


def test_20260913s_packet_newer_than_0913r_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913r_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913s_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1670.2
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260913s_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert "renjistarfall/kaggriculture-best-agent" in hunt_new
    assert hunt_new - hunt_old
    hunt_report = json.loads((ROOT / "experiments/20260913s_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913r_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1670.2 COMPLETE" in playbook
    assert "1680.9 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13s")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913s_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913r_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913s_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913s_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913r"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913t_packet_newer_than_0913s_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913s_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913t_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1673.8
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260913t_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913t_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913s_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1673.8 COMPLETE" in playbook
    assert "1670.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13t")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913t_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913s_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913t_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913t_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913s"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913u_packet_newer_than_0913t_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913t_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913u_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1669.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260913u_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913u_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913t_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1669.1 COMPLETE" in playbook
    assert "1673.8 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13u")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913u_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913t_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913u_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913u_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913t"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260913v_packet_newer_than_0913u_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913u_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260913v_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1681.2
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260913v_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260913v_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913u_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1681.2 COMPLETE" in playbook
    assert "1669.1 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-13v")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260913v_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913u_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260913v_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260913v_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913u"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260914_packet_newer_than_0913v_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260913v_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1654.7
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old
    assert "ahmedberatozer/kaggriculture-v41-review-candidate" in hunt_new
    hunt_report = json.loads((ROOT / "experiments/20260914_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0913v_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1654.7 COMPLETE" in playbook
    assert "1681.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260913v_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0913v"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260914b_packet_newer_than_0914_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1644.6
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914b_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914b_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1644.6 COMPLETE" in playbook
    assert "1654.7 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14b")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914b_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914b_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260914c_packet_newer_than_0914b_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914b_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1639.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914c_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914c_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914b_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1639.4 COMPLETE" in playbook
    assert "1644.6 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14c")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914c_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914b_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914c_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914b"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260914d_packet_newer_than_0914c_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914c_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1640.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914d_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "xuantianfengwu/kaggriculture-adaptive-land-allocator-r10",
        "aurax7/kaggriculture-shop-router-reactive-v5",
        "lime0001/t23-kaggriculture-smart-adaptive-harvest",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914d_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914c_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1640.5 COMPLETE" in playbook
    assert "1639.4 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14d")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914d_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914c_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914d_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914c"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260914e_packet_newer_than_0914d_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914d_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1637.6
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914e_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "arsgorynich/kaggriculture-v40-challenger",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914e_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914d_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1637.6 COMPLETE" in playbook
    assert "1640.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14e")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914e_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914d_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914e_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914d"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260914f_packet_newer_than_0914e_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914e_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914f_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1643.7
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914f_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914f_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914e_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1643.7 COMPLETE" in playbook
    assert "1637.6 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14f")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914f_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914e_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914f_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914f_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914e"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [6, 0, 6]


def test_20260914g_packet_newer_than_0914f_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914f_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914g_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1636.0
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914g_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914g_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914f_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1636.0 COMPLETE" in playbook
    assert "1643.7 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14g")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914g_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914f_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914g_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914g_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914f"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260914h_packet_newer_than_0914g_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914g_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914h_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1636.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914h_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914h_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914g_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1636.5 COMPLETE" in playbook
    assert "1636.0 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14h")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914h_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914g_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914h_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914h_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914g"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260914i_packet_newer_than_0914h_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914h_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914i_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1632.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914i_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914i_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914h_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1632.1 COMPLETE" in playbook
    assert "1636.5 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14i")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914i_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914h_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914i_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914i_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914h"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260914j_packet_newer_than_0914i_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914i_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914j_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1627.8
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914j_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert not (hunt_new - hunt_old)
    hunt_report = json.loads((ROOT / "experiments/20260914j_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914i_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1627.8 COMPLETE" in playbook
    assert "1632.1 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14j")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914j_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914i_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914j_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914j_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914i"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260914k_packet_newer_than_0914j_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914j_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914k_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1619.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914k_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "sorcererbi/your-offline-arena-is-lying-to-you",
        "sorcererbi/where-does-your-score-actually-come-from",
        "sorcererbi/how-to-a-b-two-agents-properly",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914k_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914j_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1619.1 COMPLETE" in playbook
    assert "1627.8 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14k")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914k_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914j_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914k_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914k_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914j"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [2, 0, 10]


def test_20260914l_packet_newer_than_0914k_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914k_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914l_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1619.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914l_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "rohitt94/kaggriculture-route-replay-agent",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914l_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914k_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1619.1 COMPLETE" in playbook
    assert "1300.3 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14l")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914l_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914k_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914l_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914l_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914k"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260914m_packet_newer_than_0914l_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914l_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914m_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1623.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914m_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "ahmedberatozer/kaggriculture-v42-production-that-fits-the-marke",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914m_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914l_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1623.1 COMPLETE" in playbook
    assert "1300.3 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14m")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914m_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914l_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914m_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914m_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914l"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [3, 0, 9]


def test_20260914n_packet_newer_than_0914m_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914m_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914n_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1627.7
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914n_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "guruprasaathas111/kaggriculture-fully-dynamic-autonomous-agent",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914n_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914m_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1627.7 COMPLETE" in playbook
    assert "1300.7 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14n")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914n_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914m_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914n_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914n_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914m"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260914o_packet_newer_than_0914n_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914n_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260914o_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1625.8
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
        "20260914n",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260914o_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "xuantianfengwu/kaggriculture-hour-4-financing-allocator",
    }
    hunt_report = json.loads((ROOT / "experiments/20260914o_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914n_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1625.8 COMPLETE" in playbook
    assert "1300.7 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-14o")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260914o_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914n_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260914o_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260914o_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914n"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260915_packet_newer_than_0914o_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260914o_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260915_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1606.1
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
        "20260914n",
        "20260914o",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260915_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "xuantianfengwu/kaggriculture-terminal-logistics",
        "taylorclark637/sovereign-swarm-kinematics-the",
        "ahmedberatozer/kaggriculture-v43-recovering-lost-harvests",
        "prvsiyan/kaggriculture-field-clock-action-budget",
        "alperen5252525/adaptive-route-portfolio-kaggriculture",
        "destbreso/agent-telemetry-catch-what-you-lose",
        "alperen5252525/harvestforge-x-high-throughput-farming",
        "nathanjacob/how-many-twins-strategy-clustering-kaggriculture",
        "hosen42/kaggriculture-v11-hc1-vs-h5-validation",
        "nathanjacob/kaggriculture-pipe-2-agent",
        "leoprovorov/god-s-mode-hacked-stores",
        "sunil123kumar/kaggriculture-v6",
    }
    hunt_report = json.loads((ROOT / "experiments/20260915_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0914o_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1606.1 COMPLETE" in playbook
    assert "1293.6 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-15")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260915_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260914o_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260915_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260915_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0914o"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260915b_packet_newer_than_0915_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260915_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260915b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1588.3
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
        "20260914n",
        "20260914o",
        "20260915",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260915b_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "anandkumar369o/kagg-team-decisions",
        "nathanjacob/beyond-v43-what-the-top-clusters-do-on-turn-1",
        "kenanzhang9/notebook6cc8bf1c92",
    }
    hunt_report = json.loads((ROOT / "experiments/20260915b_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0915_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1588.3 COMPLETE" in playbook
    assert "1286.1 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-15b")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260915b_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260915_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260915b_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260915b_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0915"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260915c_packet_newer_than_0915b_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260915b_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260915c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1582.4
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
        "20260914n",
        "20260914o",
        "20260915",
        "20260915b",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260915c_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 150
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "alperen5252525/turn-one-market-advantage-kaggriculture",
        "alperen5252525/public-state-market-control-kaggriculture",
        "alperen5252525/market-momentum-farming-kaggriculture",
        "alperen5252525/market-smart-recovery-kaggriculture",
    }
    hunt_report = json.loads((ROOT / "experiments/20260915c_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0915b_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1582.4 COMPLETE" in playbook
    assert "1286.1 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-15c")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260915c_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260915b_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260915c_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260915c_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0915b"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]


def test_20260915d_packet_newer_than_0915c_and_artem_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260915c_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260915d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1573.9
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    artem_pkt = packet["top_board"]["Artem The Farmer \U0001f345"]
    assert all(key in artem_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
        "20260914n",
        "20260914o",
        "20260915",
        "20260915b",
        "20260915c",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260915d_top10_games.json").read_text(encoding="utf-8"))
    artem = [row for row in new_games if str(row["team"]).startswith("Artem The Farmer")]
    assert artem
    prior_ids = {g["id"] for g in prior_games}
    for row in artem:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["land"][0] == 151
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == {
        "ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race",
    }
    hunt_report = json.loads((ROOT / "experiments/20260915d_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0915c_packet"] is True
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1573.9 COMPLETE" in playbook
    assert "1282.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-15d")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260915d_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260915c_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260915d_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260915d_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0915c"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [4, 0, 8]


def test_20260915e_packet_newer_than_0915d_and_majkel_new_ids() -> None:
    old_packet = json.loads((ROOT / "experiments/20260915d_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260915e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["cut16"]["hold"] is False
    assert packet["cut16"]["uploaded"] == 56151152
    assert packet["cut16"]["status"] == "COMPLETE"
    assert packet["cut16"]["score"] == 1569.5
    assert packet["live"]["newest_2"] == [56151155, 56151152]
    assert packet["cut12"]["hold"] is True
    assert packet["cut13"]["hold"] is True
    assert packet["cut17"]["hold"] is True
    assert packet["upload_bail"] is True
    assert packet["cut16"]["not_227_242_266_wrap"] is True
    assert packet["cut16"]["windows_agent_so"] is False
    assert "56151152" in packet["no_upload"]
    assert "55710781" in packet["no_upload"]
    assert "HOLD" in packet["no_upload"] or "Hold" in packet["no_upload"]

    need = ("land", "herd", "wheat", "shops", "clone")
    majkel_pkt = packet["top_board"]["Majkel1337"]
    assert all(key in majkel_pkt for key in need)
    prior_files = [
        "20260904",
        "20260905",
        "20260906",
        "20260909",
        "20260910",
        "20260911",
        "20260911b",
        "20260912",
        "20260912b",
        "20260912c",
        "20260912d",
        "20260912e",
        "20260913",
        "20260913b",
        "20260913c",
        "20260913d",
        "20260913e",
        "20260913f",
        "20260913g",
        "20260913h",
        "20260913i",
        "20260913j",
        "20260913k",
        "20260913l",
        "20260913m",
        "20260913n",
        "20260913o",
        "20260913p",
        "20260913q",
        "20260913r",
        "20260913s",
        "20260913t",
        "20260913u",
        "20260913v",
        "20260914",
        "20260914b",
        "20260914c",
        "20260914d",
        "20260914e",
        "20260914f",
        "20260914g",
        "20260914h",
        "20260914i",
        "20260914j",
        "20260914k",
        "20260914l",
        "20260914m",
        "20260914n",
        "20260914o",
        "20260915",
        "20260915b",
        "20260915c",
        "20260915d",
    ]
    prior_games = []
    for name in prior_files:
        prior_games.extend(json.loads((ROOT / f"experiments/{name}_top10_games.json").read_text(encoding="utf-8")))
    new_games = json.loads((ROOT / "experiments/20260915e_top10_games.json").read_text(encoding="utf-8"))
    majkel = [row for row in new_games if row["team"] == "Majkel1337"]
    assert majkel
    prior_ids = {g["id"] for g in prior_games}
    for row in majkel:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert 150 in row["land"]
        assert row["id"] not in prior_ids
    hunt_new = {row["kernel"] for row in packet["hunt"]}
    hunt_old = {row["kernel"] for row in old_packet["hunt"]}
    assert hunt_new - hunt_old == set()
    hunt_report = json.loads((ROOT / "experiments/20260915e_hunt_report.json").read_text(encoding="utf-8"))
    assert hunt_report["any_licensed_for_extract"] is False
    assert hunt_report["kernels_not_in_0915d_packet"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**16** `yamakawanin_king_v4e_rc4`" in playbook
    assert "Live `56151152`" in playbook
    assert "1569.5 COMPLETE" in playbook
    assert "1282.2 COMPLETE" in playbook
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-15e")[-1]
    assert "56151152" in latest
    assert "56151155" in latest
    assert "Hold" in latest


def test_20260915e_cut16_newest12_ids_differ_and_keys() -> None:
    old = json.loads((ROOT / "experiments/20260915d_cut16_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260915e_cut16_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat", "cash_24")
    rows = rolling["games"]
    assert len(rows) == 12
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    for row in rows:
        assert all(key in row for key in need)
    packet = json.loads((ROOT / "experiments/20260915e_study_packet.json").read_text(encoding="utf-8"))
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    assert packet["rolling"]["ids_not_identical_to_0915d"] is True
    assert "extra-animal" in packet["rolling"]["loss_class"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"]
    assert packet["rolling"]["wtl"] == [5, 0, 7]
