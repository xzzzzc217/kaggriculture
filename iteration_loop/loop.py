"""Official-engine iteration loop.

Each launch plays the candidate from both seats for every requested cycle,
appends one decision record per cycle, and does not submit unless ``--submit``
is set and the promotion predicate accepts a full 720-turn cycle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from kaggle_environments import make

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


def launch(argv: list[str] | None = None, client: Any | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=DEFAULT_CYCLES)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--opponent", default="pass")
    parser.add_argument("--candidate", default=None)
    parser.add_argument("--log", type=Path, default=None)
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
        verdict = decide(partial)
        upload_meta: dict[str, Any] = {
            "reason": "submit_not_requested",
            "reuploaded_best": False,
            "submitted": False,
        }
        if args.submit:
            if before != CHAMPION_SHA256:
                upload_meta = {
                    "reason": "root_main_is_not_champion",
                    "reuploaded_best": False,
                    "submitted": False,
                }
            elif args.then_best is None:
                upload_meta = {
                    "reason": "then_best_required",
                    "reuploaded_best": False,
                    "submitted": False,
                }
            else:
                upload_meta = promotion_upload(
                    eligible=bool(verdict["upload_eligible"]),
                    submit=True,
                    episode_steps=args.steps,
                    candidate_main=_candidate_main(candidate, root_main),
                    then_best_main=args.then_best,
                    output_dir=log_path.parent / f"cycle_{cycle_number}",
                    client=client,
                )
        record = {
            **partial,
            "decision": verdict["decision"],
            "reasons": verdict["reasons"],
            "submitted": bool(upload_meta["submitted"]),
            "upload": upload_meta,
            "upload_eligible": verdict["upload_eligible"],
        }
        append_cycle(log_path, record)
        new_rows.append(record)

    after = sha256_file(root_main)
    if before != after:
        raise RuntimeError("root main.py bytes changed during the loop")
    summary = {
        "cycles_completed": len(new_rows),
        "decisions": [row["decision"] for row in new_rows],
        "root_main_sha256": before,
        "root_main_unchanged": True,
        "submitted": any(row["submitted"] for row in new_rows),
        "upload_eligible": [row["upload_eligible"] for row in new_rows],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


def main(argv: list[str] | None = None, client: Any | None = None) -> int:
    return launch(argv, client=client)
