"""Official-engine 720 both-seat screen of distinct donor agents vs live metav4."""

from __future__ import annotations

import json
from pathlib import Path

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[2]
METAV4 = ROOT / "experiments/candidates/thomastschinkel_metav4_v13/main.py"
DONORS = ROOT / "artifacts/public_sources/_donors_20260921/agents"
SCRATCH = Path(r"C:\Users\21398\AppData\Local\Temp\grok-goal-30badd27e438\implementer")
SEED = 20260921
CANDIDATES = [
    "koshinm-local-best-2026-09-21.py",
    "goodpjw2008-melon-threshold-squeeze-2749.py",
    "zihengedie-best-version.py",
    "lynnsakurai-farming-score-v4-a-better-shop.py",
    "guruprasaathas111-master-engine-v4.py",
    "hanifnoerrofiq-wonderful-life.py",
    "shiiin9-beat-v48-100-0-your.py",
    "bruceqdu-route1.py",
    "rayk-topmeta-consensus-route.py",
    "municef1-lb-2448-single-file-agent.py",
]


def play(candidate: str, opponent: str, seed: int, seat: int) -> dict:
    players = [candidate, opponent] if seat == 0 else [opponent, candidate]
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run(players)
    final = env.steps[-1]
    statuses = [str(state.status) for state in final]
    rewards = [float(state.reward) for state in final]
    if statuses != ["DONE", "DONE"]:
        raise RuntimeError(f"{candidate} seat={seat} statuses={statuses}")
    own, opp = rewards[seat], rewards[1 - seat]
    return {
        "seat": seat,
        "own": own,
        "opp": opp,
        "margin": own - opp,
        "win": own > opp,
        "tie": own == opp,
    }


def main() -> None:
    opp = str(METAV4.resolve())
    results = []
    for name in CANDIDATES:
        path = DONORS / name
        rec = {"name": name, "path": str(path), "ok": False}
        print("SCREEN", name, flush=True)
        try:
            games = [play(str(path.resolve()), opp, SEED, seat) for seat in (0, 1)]
            rec.update(
                {
                    "ok": True,
                    "wins": sum(g["win"] for g in games),
                    "ties": sum(g["tie"] for g in games),
                    "mean_margin": sum(g["margin"] for g in games) / len(games),
                    "worst_margin": min(g["margin"] for g in games),
                    "games": games,
                }
            )
        except Exception as exc:  # noqa: BLE001
            rec["error"] = repr(exc)
        print(json.dumps({k: rec[k] for k in rec if k != "games"}, default=str), flush=True)
        results.append(rec)
    out = SCRATCH / "donor_screen_vs_metav4.json"
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out, flush=True)


if __name__ == "__main__":
    main()
