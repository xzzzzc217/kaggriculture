"""Inspect 0-reward six-day games: status, last step, error info."""

from __future__ import annotations

import json
from pathlib import Path

LIVE = Path("artifacts/kaggle_runs/sixday_20260908")
IDS = [105797728, 105791046, 105794752]


def main() -> None:
    for eid in IDS:
        path = LIVE / f"episode-{eid}-replay.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = replay["info"]["TeamNames"]
        steps = replay["steps"]
        seat = teams.index("heralces")
        print("=" * 72)
        print(eid, teams, "n_steps", len(steps), "info_keys", list(replay.get("info") or {})[:12])
        last = steps[-1]
        for i, st in enumerate(last):
            print(
                " seat", i, teams[i],
                "status", st.get("status"),
                "reward", st.get("reward"),
                "info", st.get("info"),
                "error", (st.get("error") or "")[:200] if st.get("error") else None,
            )
        # first non-ACTIVE
        for t, states in enumerate(steps):
            stats = [s.get("status") for s in states]
            if any(s not in (None, "ACTIVE") for s in stats):
                print(" first_non_active", t, stats)
                for i, st in enumerate(states):
                    err = st.get("error") or (st.get("info") or {}).get("error")
                    if err:
                        print("  err seat", i, str(err)[:400])
                break
        # money at last
        obs = last[seat].get("observation") or {}
        farms = obs.get("farms") or [{}, {}]
        print(" last_money", [f.get("money") for f in farms], "step_field", obs.get("step"))


if __name__ == "__main__":
    main()
