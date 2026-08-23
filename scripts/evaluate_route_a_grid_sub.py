"""Subprocess-based Route A grid evaluator.

Runs ``scripts/evaluate_head_to_head.py`` as a subprocess for each variant so
each game runs in a completely fresh Python interpreter.  This avoids the
import/deadlock issues seen with the multiprocessing approach.

Usage (must be run from the project root):
    python scripts/evaluate_route_a_grid_sub.py \
        --variant-dir artifacts/variants/kaito_route_a \
        --opponent main.py \
        --seeds 1759343872 1234567890 2000000000 3000000000 4000000000 \
        --output artifacts/evaluations/route_a_smoke/grid_smoke.json
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVAL_SCRIPT = PROJECT_ROOT / "scripts" / "evaluate_head_to_head.py"


def _eval_variant(variant_main: Path, opponent_main: Path, seeds: list[int]) -> dict:
    """Run evaluate_head_to_head.py as a subprocess for one variant."""
    cmd = [
        sys.executable,
        str(EVAL_SCRIPT),
        str(opponent_main),
        "--candidate",
        str(variant_main),
        "--seeds",
        *[str(s) for s in seeds],
        "--steps",
        "720",
    ]
    started = time.perf_counter()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
    )
    elapsed = time.perf_counter() - started
    if result.returncode != 0:
        return {
            "variant": str(variant_main),
            "error": result.stderr[:500],
            "returncode": result.returncode,
            "elapsed": elapsed,
        }
    try:
        data = json.loads(result.stdout)
        data["elapsed"] = elapsed
        return data
    except json.JSONDecodeError as exc:
        return {
            "variant": str(variant_main),
            "error": f"JSON parse failed: {exc}  stdout={result.stdout[:200]}",
            "returncode": result.returncode,
            "elapsed": elapsed,
        }


def _wilson(wins: int, games: int, z: float = 1.96) -> float:
    if games <= 0:
        return 0.0
    rate = wins / games
    denom = 1 + z * z / games
    centre = rate + z * z / (2 * games)
    radius = z * math.sqrt(rate * (1 - rate) / games + z * z * z / (4 * games * games))
    return (centre - radius) / denom


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-dir", type=Path, required=True)
    parser.add_argument("--opponent", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--grid-index", type=Path, default=None)
    parser.add_argument(
        "--batch-size", type=int, default=4,
        help="Number of variants to evaluate concurrently (subprocess pool size)"
    )
    args = parser.parse_args()

    variants = sorted(args.variant_dir.glob("variant_*/main.py"))
    print(
        f"[{time.strftime('%H:%M:%S')}] {len(variants)} variants × {len(args.seeds)} seeds × 2 seats "
        f"= {len(variants) * len(args.seeds) * 2} games  (batch={args.batch_size})",
        flush=True,
    )

    started = time.perf_counter()
    all_results: list[dict] = []
    failures: list[dict] = []

    for i, variant_path in enumerate(variants):
        elapsed = time.perf_counter() - started
        eta_min = (elapsed / max(i, 1)) * (len(variants) - i) / 60
        print(
            f"[{time.strftime('%H:%M:%S')}] variant {i+1}/{len(variants)} "
            f"({variant_path.parent.name})  elapsed={elapsed/60:.1f}min  ETA≈{eta_min:.1f}min",
            flush=True,
        )
        res = _eval_variant(variant_path, args.opponent, args.seeds)
        if "error" in res:
            failures.append(res)
        else:
            res["variant_id"] = variant_path.parent.name
            all_results.append(res)

    total_elapsed = time.perf_counter() - started
    print(f"\n[{time.strftime('%H:%M:%S')}] Done in {total_elapsed/60:.1f}min  "
          f"ok={len(all_results)}  failed={len(failures)}", flush=True)

    # Attach knob metadata from grid_index.json
    if args.grid_index and args.grid_index.exists():
        grid_data = json.loads(args.grid_index.read_text(encoding="utf-8"))
        idx_map = {v["idx"]: v for v in grid_data.get("variants", [])}
        for r in all_results:
            try:
                idx = int(r["variant_id"].split("_")[-1])
                r["knobs"] = {
                    "maximum_sell_batch": idx_map[idx]["maximum_sell_batch"],
                    "investment_horizon": idx_map[idx]["investment_horizon"],
                    "market_reserve": idx_map[idx]["market_reserve"],
                    "market_start": idx_map[idx]["market_start"],
                    "market_stop": idx_map[idx]["market_stop"],
                }
                r["sha256"] = idx_map[idx].get("sha256")
            except (KeyError, ValueError):
                r["knobs"] = None

    # Sort by paired_positive then mean_margin then win_rate
    all_results.sort(
        key=lambda r: (-r.get("paired_positive", 0), -r.get("mean_margin", -999999), -r.get("win_rate", 0))
    )

    # Wilcoxon-style significance: higher is better
    for r in all_results:
        r["wilson_95"] = _wilson(r.get("wins", 0), r.get("games", 1))

    summary = {
        "variant_dir": str(args.variant_dir.resolve()),
        "opponent": str(args.opponent.resolve()),
        "seeds": args.seeds,
        "steps": args.steps,
        "total_elapsed_seconds": total_elapsed,
        "ok_count": len(all_results),
        "failure_count": len(failures),
        "failures": failures,
        "ranked": all_results,
        "top_k": all_results[: args.top_k],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote results -> {args.output}", flush=True)

    print("\n=== TOP-{} (vs h2 champion, {} seeds, both seats) ===\n".format(args.top_k, len(args.seeds)))
    print(
        f"{'#':>3}  {'variant_id':<15}  {'W/D/L':>8}  {'win%':>6}  "
        f"{'mean_margin':>12}  {'worst':>10}  "
        f"{'paired+':>7}  {'msb':>4}  {'ih':>2}  {'mr':>5}  {'window':>12}"
    )
    print("-" * 110)
    for i, r in enumerate(all_results[: args.top_k], 1):
        knobs = r.get("knobs") or {}
        wins = r.get("wins", 0)
        ties = r.get("ties", 0)
        games = r.get("games", 1)
        win_rate = r.get("win_rate", 0.0)
        mean_m = r.get("mean_margin", 0.0)
        worst_m = r.get("worst_margin", 0.0)
        paired_pos = r.get("paired_positive", 0)
        wld = f"{wins}/{ties}/{games-wins-ties}"
        window = f"[{knobs.get('market_start', '?')},{knobs.get('market_stop', '?')}]"
        print(
            f"{i:3d}  {r['variant_id']:<15}  {wld:>8}  {win_rate:>5.1%}  "
            f"{mean_m:>+12.1f}  {worst_m:>+10.1f}  "
            f"{paired_pos}/{len(args.seeds):>6}  "
            f"{knobs.get('maximum_sell_batch', '?'):>4}  "
            f"{knobs.get('investment_horizon', '?'):>2}  "
            f"{knobs.get('market_reserve', '?'):>5}  "
            f"{window:>12}"
        )

    # Note about the anchor (variant_040 = h2 champion)
    anchor = [r for r in all_results if r.get("variant_id") == "variant_040"]
    if anchor:
        print(f"\n  anchor h2 (variant_040): mean_margin={anchor[0]['mean_margin']:+.1f}  "
              f"wins={anchor[0]['wins']}/{anchor[0]['games']}")


if __name__ == "__main__":
    main()
