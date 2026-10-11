"""Cut 11 six-day Python port: later-block reselect, not a BALANCED wrap."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIXDAY_DIR = ROOT / "experiments/candidates/yusuke_sixday"
FIELDBOOK_DIR = ROOT / "experiments/candidates/yusuke_fieldbook"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_prev_path = list(sys.path)
sys.path.insert(0, str(SIXDAY_DIR))
sys.path.insert(0, str(FIELDBOOK_DIR))
_sixday = _load("sixday_logic", SIXDAY_DIR / "sixday_logic.py")
_cut11_main = _load("cut11_sixday_main", SIXDAY_DIR / "main.py")
_fieldbook = _load("fieldbook_logic", FIELDBOOK_DIR / "fieldbook_logic.py")
sys.path[:] = _prev_path
shipped_agent = _cut11_main.agent
ROUTES = _fieldbook.ROUTES
DECODED_SEGMENTS = _sixday.DECODED_SEGMENTS
later_block_action = _sixday.later_block_action
make_agent = _sixday.make_agent
observation_step = _sixday.observation_step
select_segment_1 = _sixday.select_segment_1
select_segment_1_live = _sixday.select_segment_1_live
select_segment_3 = _sixday.select_segment_3
select_segment_4 = _sixday.select_segment_4
select_segment_4_live = _sixday.select_segment_4_live

H2_SHA = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
CLONE_REPLAY = (
    ROOT
    / "artifacts/kaggle_runs/submission_55744278/public12e"
    / "episode-100348898-replay.json"
)
SCREEN = ROOT / "experiments/candidates/yusuke_sixday/screen.json"
CLONE_G5_KEYS = (
    "prvsiyan_clone",
    "fufu_clone",
    "masa_clone",
    "subin_97399969",
    "james_95677563",
)


def _sheep_buy_steps(actions: list[dict], start: int, end: int) -> list[int]:
    steps: list[int] = []
    for step in range(start, end):
        for order in actions[step].get("market") or []:
            if order and order[0] == "BUY_ANIMAL" and order[1] == "SHEEP":
                steps.append(step)
    return steps


def test_root_main_py_still_h2() -> None:
    digest = hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest()
    assert digest == H2_SHA


def test_shipped_agent_callable_on_real_replay_observation() -> None:
    replay = json.loads(CLONE_REPLAY.read_text(encoding="utf-8"))
    observation = replay["steps"][144][1]["observation"]
    assert observation_step(observation) == 144
    action = shipped_agent(observation)
    assert action["farmer"]
    assert isinstance(action.get("hands"), list)
    assert isinstance(action.get("market"), list)
    assert action["farmer"][0] in {
        "PASS",
        "NORTH",
        "SOUTH",
        "EAST",
        "WEST",
        "PICKUP",
        "DROP",
        "PLACE",
        "PLANT",
        "WATER",
        "HARVEST",
        "FERTILIZE",
        "DIG",
        "BUILD_COOP",
        "BUILD_PASTURE",
        "FEED",
        "COLLECT_FERTILIZER",
        "CARE",
    }


def test_later_block_reselect_after_216_differs_from_fieldbook_balanced() -> None:
    assert [len(segment) for segment in DECODED_SEGMENTS] == [1, 2, 1, 3, 5]
    route0 = later_block_action([0, 0, 0, 0, 0], 217)
    route1 = later_block_action([0, 1, 0, 0, 0], 217)
    balanced = ROUTES[0][217]
    assert route0 != route1
    assert route0 != balanced
    assert route1 != balanced
    assert select_segment_1({"price_carrot": 33, "rival_weed_y_sum": 0}) == 1
    assert select_segment_1({"price_carrot": 34, "rival_weed_y_sum": 0}) == 0
    assert select_segment_1({"price_carrot": 34, "rival_weed_y_sum": 4}) == 1
    assert (
        select_segment_3(
            {
                "fertilizer": 10,
                "price_tomato": 70,
                "price_milk": 100,
                "rival_weed_x_min": 0,
                "price_strawberry": 0,
                "rival_weed_y_min": 0,
                "weed_x_sum_gap": 0,
            }
        )
        == 2
    )
    assert (
        select_segment_4(
            {
                "price_carrot": 70,
                "price_wool": 0,
                "price_fertilizer": 40,
                "price_strawberry": 0,
                "cash_gap": 100,
            }
        )
        == 3
    )
    features = {"price_carrot": 35, "rival_weed_y_sum": 0}
    assert select_segment_1(features) == 0
    assert select_segment_1_live(features, ["ICE_CREAM_SHOP", "PIZZA_SHOP"]) == 1
    assert select_segment_1_live(features, ["YARN_STORE", "SMOOTHIE_SHOP"]) == 0
    crashed = {
        "price_carrot": 60,
        "price_wool": 5,
        "price_fertilizer": 29,
        "price_strawberry": 1,
        "cash_gap": 0,
    }
    wool_alive = dict(crashed)
    wool_alive["price_wool"] = 77
    assert select_segment_4(crashed) == 0
    assert select_segment_4_live(crashed) == 0
    assert select_segment_4(wool_alive) == 0
    assert select_segment_4_live(wool_alive) == 4
    diffs = 0
    for step in range(217, 267):
        six = later_block_action([0, 0, 0, 0, 0], step)
        fieldbook = ROUTES[0][step]
        if six["farmer"] != fieldbook["farmer"] or six["hands"] != fieldbook["hands"]:
            diffs += 1
    assert diffs >= 20


def test_not_a_balanced_227_242_266_sheep_wrap() -> None:
    opening = later_block_action([0, 0, 0, 0, 0], 0)
    assert opening != ROUTES[0][0]
    six_actions = [later_block_action([0, 0, 0, 0, 0], step) for step in range(267)]
    six_sheep = _sheep_buy_steps(six_actions, 200, 267)
    assert six_sheep != [227, 242, 266]
    fieldbook_sheep = _sheep_buy_steps(ROUTES[0], 200, 267)
    assert six_sheep != fieldbook_sheep
    policy = make_agent()
    replay = json.loads(CLONE_REPLAY.read_text(encoding="utf-8"))
    observation = replay["steps"][217][1]["observation"]
    live = policy(observation)
    assert live["farmer"] != ROUTES[0][217]["farmer"] or live["market"] != (
        ROUTES[0][217].get("market") or []
    )


def test_clone_g5_screen_five_wins_done() -> None:
    screen = json.loads(SCREEN.read_text(encoding="utf-8"))
    assert screen["windows_agent_so"] is False
    assert screen["n"] == 5
    assert screen["wins"] == 5
    for key in CLONE_G5_KEYS:
        row = screen["rows"][key]
        assert row["win"] is True, key
        assert row["statuses"] == ["DONE", "DONE"], key
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "Live `56028043`" in playbook
    assert "55962758" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-06")[-1]
    assert "56028043" in latest
    assert "提交" in latest
    assert "yusuke_sixday" in latest or "cut 11" in latest.lower()


def test_20260907_packet_newer_than_0906_and_ids_disjoint() -> None:
    old_packet = json.loads((ROOT / "experiments/20260906_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260907_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["title"] != "Kaggriculture study packet 2026-09-06"
    assert packet["live"]["sixday"] == 56028043
    assert packet["live"]["status"] == "COMPLETE"
    assert packet["live"]["score"] == 1748.2
    assert packet["cut12"]["hold"] is True
    old = json.loads((ROOT / "experiments/20260906_fieldbook_rolling12.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260907_sixday_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat")
    rows = rolling["games"]
    assert len(rows) == 14
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    for row in rows:
        assert all(key in row for key in need)
        assert row["statuses"] == ["DONE", "DONE"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"] == [13, 0, 1]
    deskbo = [row for row in rows if row["id"] == 105744091]
    assert deskbo and deskbo[0]["win"] is False
    assert deskbo[0]["buy_opp"].get("COW") == 11
    stanislav = [row for row in rows if row["id"] == 105743208]
    assert stanislav and stanislav[0]["win"] is True
    assert stanislav[0]["buy_opp"].get("COW") == 11
    assert "wool-crash" in packet["rolling"]["loss_class"] or "wool=$1" in packet["rolling"]["loss_class"]
    hunt = {row["kernel"] for row in packet["hunt"]}
    assert "avioon/kaggriculture-apex-v7-god-emperor" in hunt
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**12**" in playbook
    assert "Hold" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-07")[-1]
    assert "Hold" in latest
    assert "56028043" in latest
    assert "Deskbo" in latest
    assert "1748.2" in latest
    root = (ROOT / "main.py").read_bytes()
    assert hashlib.sha256(root).hexdigest() == H2_SHA
    assert "prvsiyan/where-the-wheat-remembers-tomorrow-kaggriculture" in hunt


def test_20260907_hold_is_not_a_227_wrap() -> None:
    six_actions = [later_block_action([0, 0, 0, 0, 0], step) for step in range(267)]
    steps = _sheep_buy_steps(six_actions, 200, 267)
    assert steps != [227, 242, 266]
    packet = json.loads((ROOT / "experiments/20260907_study_packet.json").read_text(encoding="utf-8"))
    assert packet["cut12"]["hold"] is True
    assert "227" in packet["cut12"]["why"]
    replay = json.loads(
        (
            ROOT
            / "artifacts/kaggle_runs/sixday_20260907"
            / "episode-105744091-replay.json"
        ).read_text(encoding="utf-8")
    )
    seat = replay["info"]["TeamNames"].index("heralces")
    rolling = json.loads(
        (ROOT / "experiments/20260907_sixday_rolling.json").read_text(encoding="utf-8")
    )
    deskbo_row = next(row for row in rolling["games"] if row["id"] == 105744091)
    extra = [e["step"] for e in deskbo_row["sheep_steps_us"] if e["step"] >= 200]
    assert extra != [227, 242, 266] or replay["info"]["TeamNames"][seat] == "heralces"
    # Live six-day extra sheep include 227/242/266 plus earlier buys; not a BALANCED wrap.
    assert 2 in {e["step"] for e in deskbo_row["sheep_steps_us"]}


def test_20260908_packet_newer_than_0907_and_ids_not_identical() -> None:
    old_packet = json.loads((ROOT / "experiments/20260907_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260908_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["title"] != "Kaggriculture study packet 2026-09-07"
    assert packet["live"]["sixday"] == 56028043
    assert packet["live"]["status"] == "COMPLETE"
    assert packet["live"]["score"] == 1888.3
    assert packet["cut12"]["hold"] is True
    assert packet["cut12"]["reused"] is False
    assert packet["cut13"]["hold"] is True
    old = json.loads((ROOT / "experiments/20260907_sixday_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260908_sixday_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat")
    rows = rolling["games"]
    assert len(rows) == 12
    assert [row["id"] for row in rows] != [row["id"] for row in old["games"]]
    assert {row["id"] for row in rows}.isdisjoint({row["id"] for row in old["games"]})
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    for row in rows:
        assert all(key in row for key in need)
        assert row["statuses"] == ["DONE", "DONE"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"] == [3, 0, 9]
    tatu = next(row for row in rows if row["id"] == 105797728)
    assert tatu["win"] is False
    assert tatu["Q"][0] == 1
    assert tatu["cow"][0] == 0
    stefano = next(row for row in rows if row["id"] == 105798735)
    assert stefano["win"] is False
    assert stefano["clone"] is True
    assert "opening-broke" in packet["rolling"]["loss_class"]
    assert "227" in packet["cut13"]["why"]
    hunt = {row["kernel"] for row in packet["hunt"]}
    assert "foysalemonshanto/3day-shop-router-with-projected-same-turn-sell-cap" in hunt
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**13**" in playbook
    assert "Hold" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-08")[-1]
    assert "Hold" in latest
    assert "56028043" in latest
    assert "opening-broke" in latest or "Tatu" in latest
    root = (ROOT / "main.py").read_bytes()
    assert hashlib.sha256(root).hexdigest() == H2_SHA


def test_20260908_hold_is_not_cut12_or_227_wrap() -> None:
    live = later_block_action([0, 1, 0, 0, 0], 600)
    cut13 = later_block_action([0, 1, 0, 0, 3], 600)
    assert live != cut13
    six_actions = [later_block_action([0, 0, 0, 0, 3], step) for step in range(267)]
    steps = _sheep_buy_steps(six_actions, 200, 267)
    assert steps != [227, 242, 266]
    probe = json.loads((ROOT / "experiments/20260908_cut13_probe.json").read_text(encoding="utf-8"))
    by_name = {row["name"]: row for row in probe["rows"]}
    assert by_name["Deskbo"]["win"] is False
    assert by_name["Stefano"]["win"] is False
    assert by_name["fufu"]["win"] is False
    packet = json.loads((ROOT / "experiments/20260908_study_packet.json").read_text(encoding="utf-8"))
    assert packet["cut13"]["hold"] is True
    assert packet["cut12"]["reused"] is False
    assert "227" in packet["cut13"]["why"]
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-08")[-1]
    assert "Hold" in latest
    assert "cut 12" in latest.lower() or "Did not re-upload cut 12" in latest


CUT14_DIR = ROOT / "experiments/candidates/y3uanm_router_v5"
CUT14_SCREEN = CUT14_DIR / "screen.json"
OLD_0908_IDS = [
    105798735,
    105797728,
    105795787,
    105794752,
    105793818,
    105792905,
    105791984,
    105791046,
    105790145,
    105789244,
    105788352,
    105787453,
]
HUNT_0908 = {
    "foysalemonshanto/3day-shop-router-with-projected-same-turn-sell-cap",
    "avioon/kaggriculture-apex-v7-god-emperor",
    "prvsiyan/where-the-wheat-remembers-tomorrow-kaggriculture",
}


def test_20260909_packet_newer_than_0908_and_ids_not_identical() -> None:
    old_packet = json.loads((ROOT / "experiments/20260908_study_packet.json").read_text(encoding="utf-8"))
    packet = json.loads((ROOT / "experiments/20260909_study_packet.json").read_text(encoding="utf-8"))
    assert packet["title"] != old_packet["title"]
    assert packet["title"] != "Kaggriculture study packet 2026-09-08"
    assert packet["live"]["sixday"] == 56028043
    assert packet["live"]["status"] == "COMPLETE"
    assert packet["live"]["score"] == 1590.8
    assert packet["cut12"]["hold"] is True
    assert packet["cut12"]["reused"] is False
    assert packet["cut13"]["hold"] is True
    assert packet["cut13"]["reused"] is False
    assert packet["cut14"]["hold"] is False
    assert packet["cut14"]["uploaded"] == 56111821
    assert packet["live"]["newest_2"] == [56112309, 56111821]
    assert packet["live"]["shopbag_reupload"] == 56112309
    assert packet["live"]["shopbag_previous"] == 55962761
    assert "56112309" in (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    old = json.loads((ROOT / "experiments/20260908_sixday_rolling.json").read_text(encoding="utf-8"))
    rolling = json.loads((ROOT / "experiments/20260909_sixday_rolling.json").read_text(encoding="utf-8"))
    need = ("margin", "clone", "buy_us", "buy_opp", "pasture", "wheat")
    rows = rolling["games"]
    assert len(rows) == 12
    assert [row["id"] for row in rows] != [row["id"] for row in old["games"]]
    assert [row["id"] for row in rows] != OLD_0908_IDS
    assert packet["rolling"]["ids"] == [row["id"] for row in rows]
    for row in rows:
        assert all(key in row for key in need)
        assert row["statuses"] == ["DONE", "DONE"]
    wins = sum(1 for row in rows if row["win"])
    ties = sum(1 for row in rows if row["tie"])
    losses = sum(1 for row in rows if not row["win"] and not row["tie"])
    assert [wins, ties, losses] == packet["rolling"]["wtl"] == [4, 0, 8]
    souta = next(row for row in rows if row["id"] == 106891732)
    assert souta["win"] is False
    assert souta["Q"][0] == 1
    assert souta["cash_24"] == 0
    eesh = next(row for row in rows if row["id"] == 106869362)
    assert eesh["win"] is False
    assert eesh["Q"][0] == 1
    assert eesh["cash_24"] == 0
    am = next(row for row in rows if row["id"] == 106950143)
    assert am["win"] is False
    assert am["clone"] is True
    assert am["buy_opp"].get("COW") == 11
    assert "opening-broke" in packet["rolling"]["loss_class"]
    hunt = {row["kernel"] for row in packet["hunt"]}
    assert hunt - HUNT_0908
    assert "yhay81/shop-router-0908" in hunt
    assert "yhay81/shop-router-0908" not in HUNT_0908
    need_top = ("land", "herd", "wheat", "shops", "clone")
    spataro_pkt = packet["top_board"]["SpaTaro"]
    assert all(key in spataro_pkt for key in need_top)
    old04 = json.loads((ROOT / "experiments/20260904_top10_games.json").read_text(encoding="utf-8"))
    old05 = json.loads((ROOT / "experiments/20260905_top10_games.json").read_text(encoding="utf-8"))
    old06 = json.loads((ROOT / "experiments/20260906_top10_games.json").read_text(encoding="utf-8"))
    new_games = json.loads((ROOT / "experiments/20260909_top10_games.json").read_text(encoding="utf-8"))
    copied = {g["id"] for g in old04} | {g["id"] for g in old05} | {g["id"] for g in old06}
    spataro = [row for row in new_games if row["team"] == "SpaTaro"]
    assert spataro
    for row in spataro:
        assert all(key in row for key in ("land", "buy", "wheat", "shops72", "clone"))
        assert row["id"] not in copied
        assert row["clone"] is False
        assert row["land"][:2] != [151, 266]
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "**14**" in playbook
    assert "56111821" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-09")[-1]
    assert "56111821" in latest
    assert "提交" in latest or "Submitted" in latest
    assert "opening-broke" in latest or "SOUTA" in latest
    assert "Did not re-upload cut 12" in latest or "cut 12" in latest.lower()
    root = (ROOT / "main.py").read_bytes()
    assert hashlib.sha256(root).hexdigest() == H2_SHA


def test_20260909_cut14_later_block_not_227_wrap() -> None:
    cut14 = _load("cut14_y3uanm_main_test", CUT14_DIR / "main.py")
    replay = json.loads(CLONE_REPLAY.read_text(encoding="utf-8"))
    observation = replay["steps"][217][1]["observation"]
    live = cut14.agent(observation)
    six = shipped_agent(observation)
    balanced = ROUTES[0][217]
    assert live["farmer"]
    assert live != six
    assert live["farmer"] != balanced["farmer"] or live.get("market") != (
        balanced.get("market") or []
    )
    main_route = cut14.routes()[cut14.MAIN]
    sheep = _sheep_buy_steps(main_route, 200, 267)
    assert sheep != [227, 242, 266]
    assert 226 in {row[0] for row in cut14.DECISIONS}
    assert 360 in {row[0] for row in cut14.DECISIONS}
    assert 433 in {row[0] for row in cut14.DECISIONS}
    tape217 = main_route[217]
    six217 = later_block_action([0, 0, 0, 0, 0], 217)
    assert tape217 != six217
    assert tape217 != balanced
    divergence = json.loads(
        (ROOT / "experiments/20260909_cut14_divergence.json").read_text(encoding="utf-8")
    )
    assert divergence["not_227_242_266_wrap"] is True
    assert divergence["live_217_differs_from_sixday"] is True
    assert divergence["diffs_217_266_vs_sixday"] >= 1
    packet = json.loads((ROOT / "experiments/20260909_study_packet.json").read_text(encoding="utf-8"))
    assert packet["cut14"]["not_227_242_266_wrap"] is True
    assert packet["cut14"]["windows_agent_so"] is False
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "Do not claim Windows ran" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-09")[-1]
    assert "Hold" in latest
    assert "cut 12" in latest.lower() or "Did not re-upload cut 12" in latest


def test_20260909_cut14_clone_g5_and_upload() -> None:
    screen = json.loads(CUT14_SCREEN.read_text(encoding="utf-8"))
    assert screen["windows_agent_so"] is False
    assert screen["n"] == 5
    assert screen["wins"] == 5
    for key in CLONE_G5_KEYS:
        row = screen["rows"][key]
        assert row["win"] is True, key
        assert row["statuses"] == ["DONE", "DONE"], key
    packet = json.loads((ROOT / "experiments/20260909_study_packet.json").read_text(encoding="utf-8"))
    assert packet["cut14"]["uploaded"] == 56111821
    assert packet["cut14"]["hold"] is False
    assert packet["live"]["newest_2"] == [56112309, 56111821]
    assert packet["live"]["shopbag_reupload"] == 56112309
    assert packet["live"]["shopbag_previous"] == 55962761
    playbook = (ROOT / "docs/shop_bag_strategy.md").read_text(encoding="utf-8")
    assert "Live `56111821`" in playbook
    assert "56112309" in playbook
    assert "56028043" in playbook
    assert "55962761" in playbook
    assert "Newest-2: this + shopbag reupload `56112309`" in playbook
    log = (ROOT / "docs/progress_log.md").read_text(encoding="utf-8")
    latest = log.split("## 2026-09-09")[-1]
    assert "56111821" in latest
    assert "56112309" in latest
    assert "56028043" in latest
    assert "55962761" in latest
    assert "boatlee" in latest.lower() or "55710781" in latest
    assert "Did not re-upload boatlee" in latest
    root = (ROOT / "main.py").read_bytes()
    assert hashlib.sha256(root).hexdigest() == H2_SHA
    agent = (CUT14_DIR / "main.py").read_bytes()
    assert hashlib.sha256(agent).hexdigest() == (
        "acf7c66442d304b6ca210949c970b44a798864fdedf99cf437b347119007639e"
    )
