"""Guarded Kaggle upload. The default loop never calls this.

A real upload has to be a root-``main.py`` bundle of at most 100 MiB, stay
inside five submissions per UTC day, and reupload the then-best file after
the challenger so the challenger is not the only active agent.
"""

from __future__ import annotations

import csv
import importlib.util
import io
import os
import subprocess
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Protocol

MAX_BUNDLE_BYTES = 100 * 1024 * 1024
DAILY_SUBMISSION_LIMIT = 5
SLOTS_PER_PROMOTION = 2
COMPETITION = "kaggriculture"
FORBID_SUBMIT_ENV = "KAGGRICULTURE_LOOP_FORBID_SUBMIT"
FULL_SEASON_STEPS = 720

_DATE_FIELDS = ("date", "submitted", "submissiondate")


class SubmissionClient(Protocol):
    def count_today(self) -> int: ...

    def submit(self, bundle: Path, message: str) -> None: ...


def _load_build_bundle():
    path = Path(__file__).resolve().parents[1] / "scripts" / "build_submission_bundle.py"
    spec = importlib.util.spec_from_file_location("kaggriculture_build_submission_bundle", path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_bundle


build_bundle = _load_build_bundle()


def kaggle_executable() -> str:
    bundled = Path(__file__).resolve().parents[1] / ".venv" / "Scripts" / "kaggle.exe"
    if bundled.exists():
        return str(bundled)
    return "kaggle"


def kaggle_competitions_submit(bundle: Path, message: str) -> None:
    """The only Kaggle submit call site in this package."""
    if os.environ.get(FORBID_SUBMIT_ENV) == "1":
        raise RuntimeError("kaggle submit is forbidden in this launch")
    subprocess.run(
        [
            kaggle_executable(),
            "competitions",
            "submit",
            "-c",
            COMPETITION,
            "-f",
            str(bundle),
            "-m",
            message,
        ],
        check=True,
    )


def parse_utc_date(value: str) -> date:
    text = value.strip().replace("Z", "+00:00")
    for parser in (
        lambda item: datetime.fromisoformat(item),
        lambda item: datetime.strptime(item, "%Y-%m-%d %H:%M:%S"),
        lambda item: datetime.strptime(item, "%Y-%m-%d"),
    ):
        try:
            return parser(text).date()
        except ValueError:
            continue
    raise ValueError(f"unrecognized submission date: {value}")


def count_submission_rows_today(csv_text: str, today: date) -> int:
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    if not reader.fieldnames:
        raise RuntimeError("submission list has no header")
    normalized = {name.lower(): name for name in reader.fieldnames if name}
    date_field = next((normalized[name] for name in _DATE_FIELDS if name in normalized), None)
    if date_field is None:
        raise RuntimeError(f"submission list has no date column: {reader.fieldnames}")
    count = 0
    for row in reader:
        if parse_utc_date(row[date_field]) == today:
            count += 1
    return count


class KaggleCliClient:
    def count_today(self) -> int:
        completed = subprocess.run(
            [
                kaggle_executable(),
                "competitions",
                "submissions",
                "-c",
                COMPETITION,
                "--csv",
                "-q",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return count_submission_rows_today(
            completed.stdout,
            today=datetime.now(UTC).date(),
        )

    def submit(self, bundle: Path, message: str) -> None:
        kaggle_competitions_submit(bundle, message)


def _verified_bundle(main_path: Path, output_path: Path) -> dict[str, Any]:
    report = build_bundle(main_path, output_path)
    members = list(report["members"])
    if members != ["main.py"]:
        raise RuntimeError(f"bundle root must be main.py, got {members}")
    size = int(report["bundle_bytes"])
    if size > MAX_BUNDLE_BYTES or size <= 0:
        raise RuntimeError(f"bundle exceeds 100 MiB or is empty: {size} bytes")
    return report


def promotion_upload(
    *,
    eligible: bool,
    submit: bool,
    episode_steps: int,
    candidate_main: Path,
    then_best_main: Path,
    output_dir: Path,
    client: SubmissionClient | None = None,
) -> dict[str, Any]:
    """Upload a challenger only after the predicate passes, then reupload then-best."""
    if not submit:
        return {"submitted": False, "reuploaded_best": False, "reason": "submit_not_requested"}
    if episode_steps != FULL_SEASON_STEPS:
        return {
            "submitted": False,
            "reuploaded_best": False,
            "reason": "upload_requires_720_steps",
        }
    if not eligible:
        return {"submitted": False, "reuploaded_best": False, "reason": "not_upload_eligible"}
    if client is None:
        client = KaggleCliClient()
    used = int(client.count_today())
    if used < 0 or used + SLOTS_PER_PROMOTION > DAILY_SUBMISSION_LIMIT:
        return {
            "submitted": False,
            "reuploaded_best": False,
            "reason": "daily_cap",
            "submissions_today": used,
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        challenger = _verified_bundle(candidate_main, output_dir / "challenger.tar.gz")
        best = _verified_bundle(then_best_main, output_dir / "then_best.tar.gz")
    except (OSError, RuntimeError) as exc:
        return {
            "submitted": False,
            "reuploaded_best": False,
            "reason": "bundle_rejected",
            "detail": str(exc),
        }
    client.submit(Path(str(challenger["output"])), "kaggriculture challenger")
    client.submit(Path(str(best["output"])), "kaggriculture reupload then-best")
    return {
        "submitted": True,
        "reuploaded_best": True,
        "reason": "uploaded",
        "submissions_today_before": used,
        "challenger_bytes": int(challenger["bundle_bytes"]),
        "then_best_bytes": int(best["bundle_bytes"]),
        "members": list(challenger["members"]),
        "challenger_bundle": str(challenger["output"]),
        "then_best_bundle": str(best["output"]),
    }
