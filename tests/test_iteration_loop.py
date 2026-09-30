"""Launch the shipped iteration loop and drive its promotion predicate."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tarfile
from datetime import date
from pathlib import Path

from iteration_loop.leaderboard import gold_rank_cutoff, heralces_from_csv, team_in_gold
from iteration_loop.loop import main, resolve_upload
from iteration_loop.promotion import decide
from iteration_loop.submit_guard import (
    FORBID_SUBMIT_ENV,
    count_submission_rows_today,
    kaggle_competitions_submit,
    promotion_upload,
)

ROOT = Path(__file__).resolve().parents[1]
CHAMPION_SHA256 = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
MAIN_PY = ROOT / "main.py"


def _root_sha256() -> str:
    return hashlib.sha256(MAIN_PY.read_bytes()).hexdigest()


def _records(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def leaderboard_csv(team_count: int, heralces_rank: int | None) -> str:
    lines = [
        "Rank,TeamId,TeamName,LastSubmissionDate,Score,SubmissionCount,TeamMemberUserNames"
    ]
    for rank in range(1, team_count + 1):
        name = "heralces" if rank == heralces_rank else f"team{rank}"
        lines.append(
            f"{rank},{16000000 + rank},{name},2026-09-24 12:49:00,{4000 - rank},{2},{name}"
        )
    return "\n".join(lines) + "\n"


def write_leaderboard(path: Path, heralces_rank: int | None, team_count: int = 9967) -> Path:
    path.write_text(leaderboard_csv(team_count, heralces_rank), encoding="utf-8")
    return path


def _summary(completed: subprocess.CompletedProcess[str]) -> dict:
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout.strip().splitlines()[-1])


def _launch(
    log: Path,
    cycles: int = 2,
    extra: list[str] | None = None,
    *,
    heralces_rank: int | None = 30,
    leaderboard: Path | None = None,
    team_count: int = 9967,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env[FORBID_SUBMIT_ENV] = "1"
    if leaderboard is None:
        leaderboard = log.parent / f"leaderboard_{heralces_rank}_{team_count}.csv"
        write_leaderboard(leaderboard, heralces_rank, team_count)
    command = [
        sys.executable,
        "-m",
        "iteration_loop",
        "--cycles",
        str(cycles),
        "--steps",
        "48",
        "--seed",
        "20260821",
        "--opponent",
        "pass",
        "--log",
        str(log),
        "--leaderboard",
        str(leaderboard),
    ]
    if extra:
        command.extend(extra)
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _official_rewards(candidate: str, seat: int) -> list[float]:
    from kaggle_environments import make

    players = [candidate, "pass"] if seat == 0 else ["pass", candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 48, "seed": 20260821},
        debug=False,
    )
    env.run(players)
    assert len(env.steps) == 48
    final = env.steps[-1]
    assert [str(state.status) for state in final] == ["DONE", "DONE"]
    return [float(state.reward) for state in final]


def _assert_reject_cycle(record: dict) -> None:
    assert record["decision"] == "reject"
    assert record["upload_eligible"] is False
    assert record["submitted"] is False
    assert record["upload"]["submitted"] is False
    seats = sorted(game["seat"] for game in record["games"])
    assert seats == [0, 1]
    for game in record["games"]:
        assert game["statuses"] == ["DONE", "DONE"]
        assert game["opponent_class"] == "pass"
        assert all(
            isinstance(reward, (int, float)) and not isinstance(reward, bool)
            for reward in game["rewards"]
        )
        assert isinstance(game["own_reward"], (int, float))
        assert isinstance(game["opponent_reward"], (int, float))
    verdict = decide(record)
    assert verdict["upload_eligible"] is False
    assert verdict["decision"] == "reject"
    assert verdict["reasons"] == record["reasons"]


def _decision_key(row: dict) -> tuple:
    return (row["decision"], row["upload_eligible"], tuple(row["reasons"]))


def test_two_launches_reject_weak_opponent_and_do_not_submit(tmp_path: Path) -> None:
    before = _root_sha256()
    assert before == CHAMPION_SHA256
    board = write_leaderboard(tmp_path / "not_gold.csv", 30)
    parsed = heralces_from_csv(board.read_text(encoding="utf-8"))
    assert parsed["in_gold"] is False
    assert parsed["rank"] == 30
    assert parsed["team_count"] == 9967
    log = tmp_path / "cycles.jsonl"
    first = _launch(log, leaderboard=board)
    assert "competitions submit" not in first.stdout
    assert "competitions submit" not in first.stderr
    summary = _summary(first)
    assert summary["cycles_completed"] == 2
    assert summary["decisions"] == ["reject", "reject"]
    assert summary["submitted"] is False
    assert summary["gold_condition"] is False
    assert summary["in_gold"] is False
    assert summary["rank"] == 30
    assert summary["root_main_unchanged"] is True
    assert summary["root_main_sha256"] == before
    snapshot = log.read_bytes()
    rows = _records(log)
    assert [row["cycle"] for row in rows] == [1, 2]
    for record in rows:
        _assert_reject_cycle(record)
    first_cycle = rows[0]
    for game in first_cycle["games"]:
        assert game["rewards"] == _official_rewards(first_cycle["candidate"], game["seat"])
    second = _launch(log, leaderboard=board)
    assert "competitions submit" not in second.stdout
    assert "competitions submit" not in second.stderr
    assert log.read_bytes().startswith(snapshot)
    summary2 = _summary(second)
    assert summary2["cycles_completed"] == 2
    assert summary2["decisions"] == ["reject", "reject"]
    assert summary2["submitted"] is False
    assert summary2["gold_condition"] is False
    assert summary2["in_gold"] is False
    assert summary2["root_main_sha256"] == before
    continued = _records(log)
    assert [row["cycle"] for row in continued] == [1, 2, 3, 4]
    assert log.read_bytes()[: len(snapshot)] == snapshot
    assert [_decision_key(row) for row in continued[:2]] == [
        _decision_key(row) for row in continued[2:]
    ]
    assert _root_sha256() == before
    forged = dict(continued[0])
    forged["upload_eligible"] = True
    forged["decision"] = "accept"
    assert decide(forged)["upload_eligible"] is False
    assert decide(forged)["decision"] == "reject"


def test_resume_appends_without_rewriting_history(tmp_path: Path) -> None:
    log = tmp_path / "cycles.jsonl"
    first = _launch(log, cycles=2)
    assert first.returncode == 0, first.stderr
    snapshot = log.read_bytes()
    second = _launch(log, cycles=1)
    assert second.returncode == 0, second.stderr
    assert log.read_bytes().startswith(snapshot)
    rows = _records(log)
    assert [row["cycle"] for row in rows] == [1, 2, 3]
    assert _root_sha256() == CHAMPION_SHA256


def _game(
    screen: str,
    seat: int,
    *,
    opponent_class: str,
    opponent_id: str,
    score: float | None,
    win: bool,
) -> dict:
    own = 100.0 if win else 10.0
    opponent = 40.0 if win else 90.0
    rewards = [0.0, 0.0]
    rewards[seat] = own
    rewards[1 - seat] = opponent
    return {
        "screen": screen,
        "opponent_class": opponent_class,
        "opponent_id": opponent_id,
        "opponent_public_score": score,
        "seat": seat,
        "seed": 20260821,
        "statuses": ["DONE", "DONE"],
        "rewards": rewards,
        "own_reward": own,
        "opponent_reward": opponent,
        "win": win,
    }


def _pair(
    screen: str,
    opponent_class: str,
    opponent_id: str,
    score: float | None,
    win: bool = True,
) -> list[dict]:
    return [
        _game(
            screen,
            seat,
            opponent_class=opponent_class,
            opponent_id=opponent_id,
            score=score,
            win=win,
        )
        for seat in (0, 1)
    ]


def _intact(score: float) -> dict:
    games: list[dict] = []
    games.extend(_pair("gold_band", "public_gold", "public-gold", score))
    games.extend(_pair("clone", "clone", "clone-opponent", None))
    games.extend(_pair("fertilizer_wheat", "fertilizer_wheat", "fertilizer-opponent", None))
    games.extend(_pair("low_fertilizer", "low_fertilizer", "low-fertilizer-opponent", None))
    return {"episode_steps": 720, "games": games}


def _collapse(record: dict, screen: str) -> dict:
    games = []
    flipped = False
    for game in record["games"]:
        copied = dict(game)
        if copied["screen"] == screen and copied["seat"] == 1 and not flipped:
            copied.update(
                win=False,
                own_reward=10.0,
                opponent_reward=90.0,
                rewards=[90.0, 10.0] if copied["seat"] == 1 else [10.0, 90.0],
            )
            flipped = True
        games.append(copied)
    assert flipped
    return {"episode_steps": record["episode_steps"], "games": games}


def test_promotion_predicate_accepts_only_intact_gold_band(tmp_path: Path) -> None:
    weak_log = tmp_path / "weak.jsonl"
    completed = _launch(weak_log)
    assert completed.returncode == 0, completed.stderr
    weak = _records(weak_log)[0]
    intact = _intact(2900.0)
    collapsed = {
        "clone": _collapse(intact, "clone"),
        "fertilizer_wheat": _collapse(intact, "fertilizer_wheat"),
        "low_fertilizer": _collapse(intact, "low_fertilizer"),
    }
    mirror = _intact(2900.0)
    for game in mirror["games"]:
        if game["screen"] == "gold_band":
            game["opponent_class"] = "mirror"
            game["opponent_id"] = "mirror"
    one_seat = _intact(2900.0)
    one_seat["games"] = [
        game
        for game in one_seat["games"]
        if not (game["screen"] == "gold_band" and game["seat"] == 1)
    ]
    pass_only = {"games": _pair("weak", "pass", "pass", None)}
    champion_only = _intact(2900.0)
    for game in champion_only["games"]:
        if game["screen"] == "gold_band":
            game["opponent_class"] = "local_champion"
            game["opponent_id"] = "local-champion"
    outside_low = _intact(2699.0)
    outside_high = _intact(3101.0)
    cases = {
        "weak": weak,
        "intact": intact,
        "lower_edge": _intact(2700.0),
        "upper_edge": _intact(3100.0),
        "clone": collapsed["clone"],
        "fertilizer_wheat": collapsed["fertilizer_wheat"],
        "low_fertilizer": collapsed["low_fertilizer"],
        "mirror": mirror,
        "one_seat": one_seat,
        "pass_only": pass_only,
        "local_champion": champion_only,
        "below_band": outside_low,
        "above_band": outside_high,
    }
    eligible = {name for name, record in cases.items() if decide(record)["upload_eligible"]}
    assert eligible == {"intact", "lower_edge", "upper_edge"}
    rejected = (
        "clone",
        "fertilizer_wheat",
        "low_fertilizer",
        "weak",
        "mirror",
        "pass_only",
        "local_champion",
    )
    for name in rejected:
        verdict = decide(cases[name])
        assert verdict["decision"] == "reject"
        assert verdict["upload_eligible"] is False


def _agent(path: Path, marker: str) -> None:
    path.write_text(
        f"MARKER = {marker!r}\n\ndef agent(observation):\n    return {{}}\n",
        encoding="utf-8",
    )


class _Spy:
    def __init__(self, used: int) -> None:
        self.used = used
        self.submits: list[tuple[Path, str]] = []
        self.counts = 0

    def count_today(self) -> int:
        self.counts += 1
        return self.used

    def submit(self, bundle: Path, message: str) -> None:
        self.submits.append((bundle, message))


def _bundle_root_member(path: Path) -> bytes:
    with tarfile.open(path, "r:gz") as bundle:
        assert bundle.getnames() == ["main.py"]
        packed = bundle.extractfile("main.py")
        assert packed is not None
        return packed.read()


def test_submit_guard_reuploads_then_best_inside_the_daily_cap(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.py"
    best = tmp_path / "best.py"
    _agent(candidate, "candidate")
    _agent(best, "then-best")
    spy = _Spy(used=3)
    result = promotion_upload(
        eligible=True,
        submit=True,
        episode_steps=720,
        candidate_main=candidate,
        then_best_main=best,
        output_dir=tmp_path / "out",
        client=spy,
    )
    assert result["submitted"] is True
    assert result["reuploaded_best"] is True
    assert result["members"] == ["main.py"]
    assert [message for _, message in spy.submits] == [
        "kaggriculture challenger",
        "kaggriculture reupload then-best",
    ]
    assert _bundle_root_member(spy.submits[0][0]) == candidate.read_bytes()
    assert _bundle_root_member(spy.submits[1][0]) == best.read_bytes()
    assert int(result["challenger_bytes"]) <= 100 * 1024 * 1024
    assert _root_sha256() == CHAMPION_SHA256


def test_submit_guard_blocks_ineligible_short_and_capped_uploads(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.py"
    best = tmp_path / "best.py"
    _agent(candidate, "candidate")
    _agent(best, "then-best")
    blocked = _Spy(used=0)
    ineligible = promotion_upload(
        eligible=False,
        submit=True,
        episode_steps=720,
        candidate_main=candidate,
        then_best_main=best,
        output_dir=tmp_path / "ineligible",
        client=blocked,
    )
    assert ineligible["submitted"] is False
    assert ineligible["reason"] == "not_upload_eligible"
    assert blocked.submits == []
    short = promotion_upload(
        eligible=True,
        submit=True,
        episode_steps=48,
        candidate_main=candidate,
        then_best_main=best,
        output_dir=tmp_path / "short",
        client=blocked,
    )
    assert short["reason"] == "upload_requires_720_steps"
    assert blocked.submits == []
    capped = _Spy(used=4)
    at_cap = promotion_upload(
        eligible=True,
        submit=True,
        episode_steps=720,
        candidate_main=candidate,
        then_best_main=best,
        output_dir=tmp_path / "cap",
        client=capped,
    )
    assert at_cap["submitted"] is False
    assert at_cap["reason"] == "daily_cap"
    assert capped.submits == []
    idle = promotion_upload(
        eligible=True,
        submit=False,
        episode_steps=720,
        candidate_main=candidate,
        then_best_main=best,
        output_dir=tmp_path / "idle",
        client=blocked,
    )
    assert idle["reason"] == "submit_not_requested"
    assert blocked.submits == []


def test_submit_guard_rejects_a_bundle_that_is_not_root_main(tmp_path: Path, monkeypatch) -> None:
    def fake_build(main_path: Path, output_path: Path) -> dict:
        return {
            "members": ["pkg/main.py"],
            "bundle_bytes": 10,
            "output": str(output_path),
        }

    monkeypatch.setattr("iteration_loop.submit_guard.build_bundle", fake_build)
    spy = _Spy(used=0)
    result = promotion_upload(
        eligible=True,
        submit=True,
        episode_steps=720,
        candidate_main=tmp_path / "candidate.py",
        then_best_main=tmp_path / "best.py",
        output_dir=tmp_path / "bad",
        client=spy,
    )
    assert result["submitted"] is False
    assert result["reason"] == "bundle_rejected"
    assert spy.submits == []


def test_submit_guard_rejects_an_oversize_bundle(tmp_path: Path, monkeypatch) -> None:
    def fake_build(main_path: Path, output_path: Path) -> dict:
        return {
            "members": ["main.py"],
            "bundle_bytes": 100 * 1024 * 1024 + 1,
            "output": str(output_path),
        }

    monkeypatch.setattr("iteration_loop.submit_guard.build_bundle", fake_build)
    spy = _Spy(used=0)
    result = promotion_upload(
        eligible=True,
        submit=True,
        episode_steps=720,
        candidate_main=tmp_path / "candidate.py",
        then_best_main=tmp_path / "best.py",
        output_dir=tmp_path / "huge",
        client=spy,
    )
    assert result["submitted"] is False
    assert result["reason"] == "bundle_rejected"
    assert "100 MiB" in result["detail"]
    assert spy.submits == []


def test_forbid_env_blocks_the_kaggle_submit_call() -> None:
    previous = os.environ.get(FORBID_SUBMIT_ENV)
    os.environ[FORBID_SUBMIT_ENV] = "1"
    try:
        try:
            kaggle_competitions_submit(Path("missing.tar.gz"), "should not upload")
        except RuntimeError as exc:
            assert "forbidden" in str(exc)
        else:
            raise AssertionError("submit call was not blocked")
    finally:
        if previous is None:
            os.environ.pop(FORBID_SUBMIT_ENV, None)
        else:
            os.environ[FORBID_SUBMIT_ENV] = previous


def test_daily_submission_counter_uses_the_date_column() -> None:
    text = (
        "ref,date,description\n"
        "1,2026-09-29 01:02:03,a\n"
        "2,2026-09-28 23:00:00,b\n"
        "3,2026-09-29 23:59:59,c\n"
    )
    assert count_submission_rows_today(text, date(2026, 9, 29)) == 2


def test_short_submit_flag_does_not_call_the_client(tmp_path: Path) -> None:
    best = tmp_path / "best.py"
    _agent(best, "then-best")
    spy = _Spy(used=0)
    log = tmp_path / "cycles.jsonl"
    code = main(
        [
            "--cycles",
            "2",
            "--steps",
            "48",
            "--seed",
            "20260821",
            "--opponent",
            "pass",
            "--log",
            str(log),
            "--submit",
            "--then-best",
            str(best),
        ],
        client=spy,
    )
    assert code == 0
    assert spy.submits == []
    assert spy.counts == 0
    rows = _records(log)
    assert len(rows) == 2
    assert all(row["upload"]["reason"] == "upload_requires_720_steps" for row in rows)
    assert _root_sha256() == CHAMPION_SHA256


def test_gold_cutoff_matches_the_9967_team_field() -> None:
    assert gold_rank_cutoff(9967) == 29
    assert team_in_gold(29, 9967) is True
    assert team_in_gold(30, 9967) is False
    at_cut = heralces_from_csv(leaderboard_csv(9967, 29))
    assert at_cut["team_count"] == 9967
    assert at_cut["rank"] == 29
    assert at_cut["gold_cutoff"] == 29
    assert at_cut["in_gold"] is True
    outside = heralces_from_csv(leaderboard_csv(9967, 30))
    assert outside["rank"] == 30
    assert outside["in_gold"] is False
    missing = heralces_from_csv(leaderboard_csv(9967, None))
    assert missing["rank"] is None
    assert missing["team"] is None
    assert missing["gold_cutoff"] == 29
    assert missing["in_gold"] is False


def test_in_gold_snapshot_records_gold_and_plays_no_cycles(tmp_path: Path) -> None:
    before = _root_sha256()
    board = write_leaderboard(tmp_path / "gold.csv", 29)
    log = tmp_path / "cycles.jsonl"
    log.write_text('{"cycle": 1, "kept": true}\n', encoding="utf-8")
    prior = log.read_bytes()
    completed = _launch(log, cycles=2, leaderboard=board, heralces_rank=29)
    summary = _summary(completed)
    assert summary["gold_condition"] is True
    assert summary["in_gold"] is True
    assert summary["rank"] == 29
    assert summary["team_count"] == 9967
    assert summary["gold_cutoff"] == 29
    assert summary["cycles_completed"] == 0
    assert summary["decisions"] == []
    assert summary["submitted"] is False
    assert summary["upload_eligible"] == []
    assert summary["root_main_unchanged"] is True
    assert summary["root_main_sha256"] == before
    assert log.read_bytes() == prior
    assert _root_sha256() == before
    assert "competitions submit" not in completed.stdout
    assert "competitions submit" not in completed.stderr


def test_in_gold_snapshot_does_not_start_the_engine_or_submit(
    tmp_path: Path, monkeypatch
) -> None:
    def explode(*_args, **_kwargs):
        raise AssertionError("gold snapshot must not play or upload")

    monkeypatch.setattr("iteration_loop.loop.play_match", explode)
    monkeypatch.setattr("iteration_loop.loop.promotion_upload", explode)
    board = write_leaderboard(tmp_path / "gold.csv", 29)
    best = tmp_path / "best.py"
    _agent(best, "then-best")
    spy = _Spy(used=0)
    log = tmp_path / "cycles.jsonl"
    code = main(
        [
            "--cycles",
            "2",
            "--steps",
            "720",
            "--seed",
            "20260821",
            "--opponent",
            "pass",
            "--log",
            str(log),
            "--leaderboard",
            str(board),
            "--submit",
            "--then-best",
            str(best),
        ],
        client=spy,
    )
    assert code == 0
    assert not log.exists()
    assert spy.submits == []
    assert spy.counts == 0
    assert _root_sha256() == CHAMPION_SHA256


def test_missing_team_does_not_record_gold_and_appends_cycles(tmp_path: Path) -> None:
    before = _root_sha256()
    board = write_leaderboard(tmp_path / "missing.csv", None)
    log = tmp_path / "cycles.jsonl"
    completed = _launch(log, cycles=2, leaderboard=board)
    summary = _summary(completed)
    assert summary["gold_condition"] is False
    assert summary["in_gold"] is False
    assert summary["rank"] is None
    assert summary["team_count"] == 9967
    assert summary["gold_cutoff"] == 29
    assert summary["cycles_completed"] == 2
    assert summary["decisions"] == ["reject", "reject"]
    assert summary["submitted"] is False
    rows = _records(log)
    assert [row["cycle"] for row in rows] == [1, 2]
    for record in rows:
        _assert_reject_cycle(record)
    assert _root_sha256() == before


def _upload_case(
    record: dict,
    tmp_path: Path,
    name: str,
    *,
    steps: int = 720,
    used: int = 0,
) -> tuple[dict, _Spy]:
    candidate = tmp_path / "candidate.py"
    best = tmp_path / "best.py"
    if not candidate.exists():
        _agent(candidate, "candidate")
        _agent(best, "then-best")
    spy = _Spy(used=used)
    result = resolve_upload(
        record,
        submit=True,
        episode_steps=steps,
        candidate_main=candidate,
        then_best_main=best,
        output_dir=tmp_path / name,
        client=spy,
        root_sha=_root_sha256(),
    )
    return result, spy


def test_intact_gold_band_uploads_challenger_then_best(tmp_path: Path) -> None:
    assert _root_sha256() == CHAMPION_SHA256
    candidate = tmp_path / "candidate.py"
    best = tmp_path / "best.py"
    _agent(candidate, "candidate")
    _agent(best, "then-best")
    for score in (2700, 2900, 3100):
        record = _intact(float(score))
        record["decision"] = "reject"
        record["upload_eligible"] = False
        result, spy = _upload_case(record, tmp_path, f"band_{score}", used=3)
        assert result["decision"] == "accept"
        assert result["upload_eligible"] is True
        assert result["submitted"] is True
        assert result["upload"]["reuploaded_best"] is True
        assert result["upload"]["members"] == ["main.py"]
        assert int(result["upload"]["challenger_bytes"]) <= 100 * 1024 * 1024
        assert int(result["upload"]["then_best_bytes"]) <= 100 * 1024 * 1024
        assert [message for _, message in spy.submits] == [
            "kaggriculture challenger",
            "kaggriculture reupload then-best",
        ]
        assert _bundle_root_member(spy.submits[0][0]) == candidate.read_bytes()
        assert _bundle_root_member(spy.submits[1][0]) == best.read_bytes()
    assert _root_sha256() == CHAMPION_SHA256


def _reject_records() -> dict[str, dict]:
    intact = _intact(2900.0)
    collapsed = {
        screen: _collapse(intact, screen)
        for screen in ("clone", "fertilizer_wheat", "low_fertilizer")
    }
    missing = {}
    for screen in ("clone", "fertilizer_wheat", "low_fertilizer"):
        missing[screen] = {
            "episode_steps": 720,
            "games": [game for game in intact["games"] if game["screen"] != screen],
        }
    mirror = _intact(2900.0)
    starter = _intact(2900.0)
    champion = _intact(2900.0)
    pass_band = _intact(2900.0)
    for game in mirror["games"]:
        if game["screen"] == "gold_band":
            game["opponent_class"] = "mirror"
            game["opponent_id"] = "mirror"
    for game in starter["games"]:
        if game["screen"] == "gold_band":
            game["opponent_class"] = "starter"
            game["opponent_id"] = "starter"
    for game in champion["games"]:
        if game["screen"] == "gold_band":
            game["opponent_class"] = "local_champion"
            game["opponent_id"] = "local-champion"
    for game in pass_band["games"]:
        if game["screen"] == "gold_band":
            game["opponent_class"] = "pass"
            game["opponent_id"] = "pass"
    one_seat = _intact(2900.0)
    one_seat["games"] = [
        game
        for game in one_seat["games"]
        if not (game["screen"] == "gold_band" and game["seat"] == 1)
    ]
    forged = {
        "episode_steps": 720,
        "decision": "accept",
        "upload_eligible": True,
        "games": _pair("weak", "pass", "pass", None),
    }
    cases = {
        "pass": pass_band,
        "starter": starter,
        "mirror": mirror,
        "local_champion": champion,
        "one_seat": one_seat,
        "below_band": _intact(2699.0),
        "above_band": _intact(3101.0),
        "pass_only": {"episode_steps": 720, "games": _pair("weak", "pass", "pass", None)},
        "forged_accept": forged,
    }
    for screen, record in collapsed.items():
        cases[f"collapsed_{screen}"] = record
    for screen, record in missing.items():
        cases[f"missing_{screen}"] = record
    return cases


def test_promotion_records_do_not_submit(tmp_path: Path) -> None:
    for name, record in _reject_records().items():
        forged = dict(record)
        forged["decision"] = "accept"
        forged["upload_eligible"] = True
        result, spy = _upload_case(forged, tmp_path, name, steps=720, used=0)
        assert result["submitted"] is False, name
        assert result["decision"] == "reject", name
        assert result["upload_eligible"] is False, name
        assert spy.submits == [], name
        assert spy.counts == 0, name
    short, short_spy = _upload_case(_intact(2900.0), tmp_path, "short_season", steps=48, used=0)
    assert short["submitted"] is False
    assert short["upload"]["reason"] == "upload_requires_720_steps"
    assert short_spy.submits == []
    assert short_spy.counts == 0
    for used in (4, 5):
        capped, capped_spy = _upload_case(
            _intact(2900.0), tmp_path, f"daily_{used}", steps=720, used=used
        )
        assert capped["submitted"] is False
        assert capped["upload"]["reason"] == "daily_cap"
        assert capped_spy.submits == []
    assert _root_sha256() == CHAMPION_SHA256


def test_resolve_upload_rejects_non_root_and_oversize_archives(
    tmp_path: Path, monkeypatch
) -> None:
    def fake_non_root(main_path: Path, output_path: Path) -> dict:
        return {
            "members": ["pkg/main.py"],
            "bundle_bytes": 10,
            "output": str(output_path),
        }

    monkeypatch.setattr("iteration_loop.submit_guard.build_bundle", fake_non_root)
    rejected, spy = _upload_case(_intact(2900.0), tmp_path, "non_root", steps=720, used=0)
    assert rejected["submitted"] is False
    assert rejected["upload"]["reason"] == "bundle_rejected"
    assert spy.submits == []

    def fake_oversize(main_path: Path, output_path: Path) -> dict:
        return {
            "members": ["main.py"],
            "bundle_bytes": 100 * 1024 * 1024 + 1,
            "output": str(output_path),
        }

    monkeypatch.setattr("iteration_loop.submit_guard.build_bundle", fake_oversize)
    huge, huge_spy = _upload_case(_intact(2900.0), tmp_path, "oversize", steps=720, used=0)
    assert huge["submitted"] is False
    assert huge["upload"]["reason"] == "bundle_rejected"
    assert "100 MiB" in huge["upload"]["detail"]
    assert huge_spy.submits == []
    assert _root_sha256() == CHAMPION_SHA256
