"""Orchestrate 5-seed both-seat smoke evaluation of all Route A variants vs h2.

For each variant in ``artifacts/variants/kaito_route_a/`` the script runs
``evaluate_head_to_head`` against the current champion (root ``main.py``) on a
fixed list of seeds, both seats. Results are aggregated, ranked by mean margin
against the champion, and the top-8 candidates are surfaced as
ready-to-submit artifacts under ``artifacts/evaluations/route_a_smoke/``.

Usage:
    python scripts/evaluate_route_a_grid.py \
        --variant-dir artifacts/variants/kaito_route_a \
        --opponent main.py \
        --seeds <s1> <s2> <s3> <s4> <s5> \
        --output artifacts/evaluations/route_a_smoke/grid_smoke.json
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.evaluate_head_to_head import (
    play,
    wilson_lower_bound,
)


def _worker(args: tuple[str, str, list[int], int]) -> dict:
    candidate, opponent, seeds, steps = args
    games = [
        play(candidate, opponent, seed, seat, steps)
        for seed in seeds
        for seat in (0, 1)
    ]
    wins = sum(g["win"] for g in games)
    ties = sum(g["tie"] for g in games)
    paired = [
        {
            "seed": seed,
            "paired_margin": sum(g["margin"] for g in games if g["seed"] == seed),
        }
        for seed in seeds
    ]
    return {
        "candidate": candidate,
        "opponent": opponent,
        "games": len(games),
        "wins": wins,
        "ties": ties,
        "losses": len(games) - wins - ties,
        "win_rate": wins / len(games),
        "wilson_95_lower": wilson_lower_bound(wins, len(games)),
        "mean_margin": sum(g["margin"] for g in games) / len(games),
        "worst_margin": min(g["margin"] for g in games),
        "paired_positive": sum(p["paired_margin"] > 0 for p in paired),
        "paired_zero": sum(p["paired_margin"] == 0 for p in paired),
        "paired_negative": sum(p["paired_margin"] < 0 for p in paired),
        "mean_runtime_seconds": sum(g["runtime_seconds"] for g in games) / len(games),
        "games_detail": games,
    }


def _enumerate_variants(variant_dir: Path) -> list[Path]:
    return sorted(d / "main.py" for d in variant_dir.iterdir() if d.is_dir())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-dir", type=Path, required=True)
    parser.add_argument("--opponent", type=Path, required=True,
                        help="Path to the opponent's main.py (typically project root main.py)")
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--grid-index", type=Path, default=None,
                        help="Optional grid_index.json to attach knob metadata")
    args = parser.parse_args()

    variants = _enumerate_variants(args.variant_dir)
    opponent = str(args.opponent.resolve())
    seeds = args.seeds
    print(f"evaluating {len(variants)} variants x {len(seeds)} seeds x 2 seats "
          f"= {len(variants) * len(seeds) * 2} games with {args.workers} workers",
          file=sys.stderr)

    work = [(str(v.resolve()), opponent, seeds, args.steps) for v in variants]

    started = time.perf_counter()
    results: list[dict] = []
    failures: list[dict] = []
    if args.workers > 1:
        ctx = mp.get_context("spawn")
        with ctx.Pool(processes=args.workers) as pool:
            for outcome in pool.imap_unordered(_worker, work):
                if isinstance(outcome, dict) and "error" in outcome:
                    failures.append(outcome)
                else:
                    results.append(outcome)
    else:
        for w in work:
            try:
                results.append(_worker(w))
            except Exception as exc:  # noqa: BLE001
                failures.append({"candidate": w[0], "error": repr(exc)})

    elapsed = time.perf_counter() - started
    print(f"completed in {elapsed:.1f}s ({len(results)} ok, {len(failures)} failed)",
          file=sys.stderr)

    results.sort(key=lambda r: (-r["paired_positive"], -r["mean_margin"], -r["wins"]))
    for r in results:
        cpath = Path(r["candidate"])
        try:
            rel = cpath.relative_to(args.variant_dir.resolve())
            r["variant_id"] = rel.parent.name
        except ValueError:
            r["variant_id"] = cpath.name

    grid_meta = {}
    if args.grid_index and args.grid_index.exists():
        grid_meta = json.loads(args.grid_index.read_text(encoding="utf-8"))
        idx_to_knobs = {v["idx"]: v for v in grid_meta.get("variants", [])}
        for r in results:
            try:
                numeric_idx = int(r["variant_id"].split("_")[-1])
                r["knobs"] = {
                    k: idx_to_knobs[numeric_idx][k]
                    for k in (
                        "maximum_sell_batch",
                        "investment_horizon",
                        "market_reserve",
                        "market_start",
                        "market_stop",
                    )
                }
                r["sha256"] = idx_to_knobs[numeric_idx].get("sha256")
            except (KeyError, ValueError):
                r["knobs"] = None

    summary = {
        "variant_dir": str(args.variant_dir.resolve()),
        "opponent": opponent,
        "seeds": seeds,
        "steps": args.steps,
        "workers": args.workers,
        "elapsed_seconds": elapsed,
        "ok_count": len(results),
        "failure_count": len(failures),
        "failures": failures,
        "ranked": results,
        "top_k": results[: args.top_k],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}", file=sys.stderr)

    print("\n=== TOP-{} (mean margin vs h2) ===".format(args.top_k))
    for i, r in enumerate(results[: args.top_k], 1):
        knobs = r.get("knobs") or {}
        print(
            f"{i:2d}. {r['variant_id']}  wins={r['wins']}/{r['games']}  "
            f"mean_margin={r['mean_margin']:+.1f}  worst={r['worst_margin']:+.1f}  "
            f"paired+={r['paired_positive']}/{len(seeds)}  "
            f"msb={knobs.get('maximum_sell_batch')} ih={knobs.get('investment_horizon')} "
            f"mr={knobs.get('market_reserve')} window=[{knobs.get('market_start')},{knobs.get('market_stop')}]"
        )


if __name__ == "__main__":
    main()
