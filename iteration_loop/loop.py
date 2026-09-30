"""Official-engine iteration loop.

Each launch reads an optional public leaderboard snapshot. When that snapshot
places heralces inside the gold cutoff, the launch records the gold condition,
submits nothing, and plays no match cycles. Otherwise it plays the candidate
from both seats for every requested cycle, appends one decision record per
cycle, and does not submit unless ``--submit`` is set and this cycle's own
games pass the promotion predicate on a 720-turn season.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from iteration_loop.leaderboard import heralces_from_csv
from iteration_loop.promotion import NON_PROMOTING_OPPONENTS, decide
from iteration_loop.submit_guard import promotion_upload

CHAMPION_SHA256 = "65e6f5cd8e582803aea4446a7b2bfabb050bbee382d771c60c9c66aec8fc3dbe"
DEFAULT_SEED = 20260821
DEFAULT_STEPS = 48
DEFAULT_CYCLES = 2
REPO_ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cycles(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def append_cycle(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")


def leaderboard_status(path: Path | None) -> dict[str, Any]:
    """Gold comes only from a public leaderboard snapshot, never from local coins."""
    if path is None:
        return {
            "gold_condition": False,
            "gold_cutoff": None,
            "in_gold": False,
            "rank": None,
            "score": None,
            "team_count": None,
        }
    board = heralces_from_csv(path.read_text(encoding="utf-8"))
    in_gold = bool(board["in_gold"])
    return {
        "gold_condition": in_gold,
        "gold_cutoff": board["gold_cutoff"],
        "in_gold": in_gold,
        "rank": board["rank"],
        "score": board["score"],
        "team_count": board["team_count"],
    }


def resolve_upload(
    record: Mapping[str, Any],
    *,
    submit: bool,
    episode_steps: int,
    candidate_main: Path,
    then_best_main: Path | None,
    output_dir: Path,
    client: Any | None,
    root_sha: str,
) -> dict[str, Any]:
    """Decide from this cycle's games, then apply the upload guard.

    Pre-baked ``decision`` and ``upload_eligible`` fields on ``record`` are
    ignored. A forged accept flag cannot upload.
    """
    verdict = decide(record)
    if not submit:
        upload_meta: dict[str, Any] = {
            "reason": "submit_not_requested",
            "reuploaded_best": False,
            "submitted": False,
        }
    elif root_sha != CHAMPION_SHA256:
        upload_meta = {
            "reason": "root_main_is_not_champion",
            "reuploaded_best": False,
            "submitted": False,
        }
    elif then_best_main is None:
        upload_meta = {
            "reason": "then_best_required",
            "reuploaded_best": False,
            "submitted": False,
        }
    else:
        upload_meta = promotion_upload(
            eligible=bool(verdict["upload_eligible"]),
            submit=True,
            episode_steps=episode_steps,
            candidate_main=candidate_main,
            then_best_main=then_best_main,
            output_dir=output_dir,
            client=client,
        )
    return {
        "decision": verdict["decision"],
        "reasons": verdict["reasons"],
        "submitted": bool(upload_meta["submitted"]),
        "upload": upload_meta,
        "upload_eligible": verdict["upload_eligible"],
    }


def classify_opponent(opponent: str, candidate: str, root_main: Path) -> str:
    if opponent in {"pass", "starter"}:
        return opponent
    opponent_path = Path(opponent)
    candidate_path = Path(candidate)
    if opponent_path.exists() and candidate_path.exists():
        if opponent_path.resolve() == candidate_path.resolve():
            return "mirror"
        if opponent_path.resolve() == root_main.resolve():
            return "local_champion"
    return "file"


def play_match(
    candidate: str,
    opponent: str,
    seed: int,
    seat: int,
    steps: int,
    *,
    screen: str,
    opponent_class: str,
    opponent_id: str,
    opponent_public_score: float | None,
) -> dict[str, Any]:
    from kaggle_environments import make

    players = [candidate, opponent] if seat == 0 else [opponent, candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": steps, "seed": seed},
        debug=False,
    )
    error = None
    try:
        env.run(players)
        final = env.steps[-1]
        statuses = [str(state.status) for state in final]
        rewards: list[float | None] = []
        for state in final:
            reward = getattr(state, "reward", None)
            rewards.append(None if reward is None else float(reward))
    except Exception as exc:
        statuses = ["ERROR", "ERROR"]
        rewards = [None, None]
        error = f"{type(exc).__name__}: {exc}"
    own = rewards[seat]
    other = rewards[1 - seat]
    win = own is not None and other is not None and own > other
    game: dict[str, Any] = {
        "opponent": opponent,
        "opponent_class": opponent_class,
        "opponent_id": opponent_id,
        "opponent_public_score": opponent_public_score,
        "own_reward": own,
        "opponent_reward": other,
        "rewards": rewards,
        "screen": screen,
        "seat": seat,
        "seed": seed,
        "statuses": statuses,
        "win": win,
    }
    if error:
        game["error"] = error
    return game


def _matchups(
    opponent: str,
    candidate: str,
    root_main: Path,
    manifest: Path | None,
) -> list[dict[str, Any]]:
    if manifest is None:
        opponent_class = classify_opponent(opponent, candidate, root_main)
        return [
            {
                "opponent": opponent,
                "screen": "weak",
                "opponent_class": opponent_class,
                "opponent_id": opponent,
                "opponent_public_score": None,
            }
        ]
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    raw_rows = payload["matchups"] if isinstance(payload, dict) else payload
    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        name = str(raw["opponent"])
        opponent_class = classify_opponent(name, candidate, root_main)
        if opponent_class in NON_PROMOTING_OPPONENTS:
            rows.append(
                {
                    "opponent": name,
                    "screen": "weak",
                    "opponent_class": opponent_class,
                    "opponent_id": name,
                    "opponent_public_score": None,
                }
            )
            continue
        score = raw.get("opponent_public_score")
        rows.append(
            {
                "opponent": name,
                "screen": str(raw.get("screen") or "gold_band"),
                "opponent_class": str(raw.get("opponent_class") or opponent_class),
                "opponent_id": str(raw.get("opponent_id") or name),
                "opponent_public_score": None if score is None else float(score),
            }
        )
    return rows


def _candidate_main(candidate: str, root_main: Path) -> Path:
    path = Path(candidate)
    if path.exists():
        return path
    return root_main


def _gold_stop_summary(status: Mapping[str, Any], root_sha: str) -> dict[str, Any]:
    return {
        "cycles_completed": 0,
        "decisions": [],
        "gold_condition": True,
        "gold_cutoff": status["gold_cutoff"],
        "in_gold": True,
        "rank": status["rank"],
        "root_main_sha256": root_sha,
        "root_main_unchanged": True,
        "score": status["score"],
        "submitted": False,
        "team_count": status["team_count"],
        "upload_eligible": [],
    }


def launch(argv: list[str] | None = None, client: Any | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=DEFAULT_CYCLES)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--opponent", default="pass")
    parser.add_argument("--candidate", default=None)
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--leaderboard", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--then-best", type=Path, default=None)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    if args.cycles < 1:
        raise SystemExit("--cycles must be at least 1")

    repo_root = args.repo_root.resolve()
    root_main = repo_root / "main.py"
    before = sha256_file(root_main)
    status = leaderboard_status(args.leaderboard)
    if status["in_gold"]:
        after = sha256_file(root_main)
        if before != after:
            raise RuntimeError("root main.py bytes changed during the loop")
        print(json.dumps(_gold_stop_summary(status, before), sort_keys=True))
        return 0

    candidate = str(root_main if args.candidate is None else Path(args.candidate))
    log_path = (
        args.log
        if args.log is not None
        else repo_root / "artifacts" / "iteration_loop" / "cycles.jsonl"
    )
    existing = read_cycles(log_path)
    next_cycle = 1 + max((int(row["cycle"]) for row in existing), default=0)
    matchups = _matchups(args.opponent, candidate, root_main, args.manifest)
    new_rows: list[dict[str, Any]] = []

    for offset in range(args.cycles):
        cycle_number = next_cycle + offset
        games = [
            play_match(
                candidate,
                str(matchup["opponent"]),
                args.seed,
                seat,
                args.steps,
                screen=str(matchup["screen"]),
                opponent_class=str(matchup["opponent_class"]),
                opponent_id=str(matchup["opponent_id"]),
                opponent_public_score=matchup["opponent_public_score"],
            )
            for matchup in matchups
            for seat in (0, 1)
        ]
        partial = {
            "candidate": candidate,
            "cycle": cycle_number,
            "episode_steps": args.steps,
            "games": games,
            "opponent": args.opponent,
            "root_main_sha256": before,
            "seed": args.seed,
        }
        resolved = resolve_upload(
            partial,
            submit=bool(args.submit),
            episode_steps=args.steps,
            candidate_main=_candidate_main(candidate, root_main),
            then_best_main=args.then_best,
            output_dir=log_path.parent / f"cycle_{cycle_number}",
            client=client,
            root_sha=before,
        )
        record = {
            **partial,
            "decision": resolved["decision"],
            "reasons": resolved["reasons"],
            "submitted": resolved["submitted"],
            "upload": resolved["upload"],
            "upload_eligible": resolved["upload_eligible"],
        }
        append_cycle(log_path, record)
        new_rows.append(record)

    after = sha256_file(root_main)
    if before != after:
        raise RuntimeError("root main.py bytes changed during the loop")
    summary = {
        "cycles_completed": len(new_rows),
        "decisions": [row["decision"] for row in new_rows],
        "gold_condition": False,
        "gold_cutoff": status["gold_cutoff"],
        "in_gold": False,
        "rank": status["rank"],
        "root_main_sha256": before,
        "root_main_unchanged": True,
        "score": status["score"],
        "submitted": any(row["submitted"] for row in new_rows),
        "team_count": status["team_count"],
        "upload_eligible": [row["upload_eligible"] for row in new_rows],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


def main(argv: list[str] | None = None, client: Any | None = None) -> int:
    return launch(argv, client=client)
