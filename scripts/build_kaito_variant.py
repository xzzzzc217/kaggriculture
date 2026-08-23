"""Build one or many frozen Kaito v36-clone-horizon variants for local evaluation.

Supports two modes:
- Single variant: ``source output --clone-horizon N``
- Grid sweep: ``source output_dir --grid-route-a`` (writes 81 variants into
  ``<output_dir>/variant_<idx>/main.py`` plus a ``grid_index.json`` summary).

The grid produces a 3x3x3x3 = 81 combinatorial sweep over four knobs:
``maximum_sell_batch``, ``investment_horizon``, ``market_reserve``, and the
paired ``market_start``/``market_stop`` window. The 3 levels per knob are
chosen to bracket the current h2 champion value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import py_compile
from pathlib import Path


_GRID_AXES = {
    "maximum_sell_batch": [50, 100, 150],
    "investment_horizon": [1, 2, 3],
    "market_reserve": [300.0, 500.0, 700.0],
    "market_window": [(60, 700), (72, 716), (84, 720)],
}


def _grid_spec() -> list[dict]:
    """Enumerate all 81 grid combinations in a deterministic order."""
    spec: list[dict] = []
    for msb in _GRID_AXES["maximum_sell_batch"]:
        for ih in _GRID_AXES["investment_horizon"]:
            for mr in _GRID_AXES["market_reserve"]:
                for mstart, mstop in _GRID_AXES["market_window"]:
                    spec.append(
                        {
                            "maximum_sell_batch": msb,
                            "investment_horizon": ih,
                            "market_reserve": mr,
                            "market_start": mstart,
                            "market_stop": mstop,
                        }
                    )
    return spec


def _apply_replacements(source: str, knobs: dict) -> str:
    """Apply all knob substitutions on the v36 config block.

    Each marker in ``main.py`` is a stable, anchored token. The script refuses
    to proceed when a marker is absent or ambiguous so the variant file is
    always an exact, auditable copy of the source.
    """
    replacements: list[tuple[str, str]] = [
        (
            "    maximum_sell_batch=100,",
            f"    maximum_sell_batch={knobs['maximum_sell_batch']},",
        ),
        (
            "    investment_horizon=2,",
            f"    investment_horizon={knobs['investment_horizon']},",
        ),
        (
            "    market_reserve=500.0,",
            f"    market_reserve={knobs['market_reserve']},",
        ),
        (
            "    market_start=72,",
            f"    market_start={knobs['market_start']},",
        ),
        (
            "    market_stop=716,",
            f"    market_stop={knobs['market_stop']},",
        ),
    ]
    for marker, replacement in replacements:
        if source.count(marker) != 1:
            raise ValueError(
                f"expected exactly one marker for {marker!r}, "
                f"found {source.count(marker)}"
            )
        source = source.replace(marker, replacement)
    return source


def build_variant(source_path: Path, output_path: Path, knobs: dict) -> str:
    source = source_path.read_text(encoding="utf-8")
    rendered = _apply_replacements(source, knobs)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    py_compile.compile(str(output_path), doraise=True)
    return hashlib.sha256(output_path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    single = sub.add_parser("single", help="Build a single variant from explicit knobs")
    single.add_argument("source", type=Path)
    single.add_argument("output", type=Path)
    single.add_argument("--clone-horizon", type=int, required=True)
    single.add_argument("--maximum-sell-batch", type=int, default=None)
    single.add_argument("--investment-horizon", type=int, default=None)
    single.add_argument("--market-reserve", type=float, default=None)
    single.add_argument("--market-start", type=int, default=None)
    single.add_argument("--market-stop", type=int, default=None)

    grid = sub.add_parser(
        "grid", help="Write the 81-combination Route A grid into a directory"
    )
    grid.add_argument("source", type=Path)
    grid.add_argument("output_dir", type=Path)

    args = parser.parse_args()

    if args.cmd == "single":
        if not 1 <= args.clone_horizon <= 6:
            raise ValueError("clone horizon must be between 1 and 6")
        source = args.source.read_text(encoding="utf-8")
        marker = "    clone_horizon=1,"
        if source.count(marker) != 1:
            raise ValueError("expected exactly one frozen v36 clone_horizon marker")
        source = source.replace(marker, f"    clone_horizon={args.clone_horizon},")
        knobs: dict = {}
        if args.maximum_sell_batch is not None:
            knobs["maximum_sell_batch"] = args.maximum_sell_batch
        if args.investment_horizon is not None:
            knobs["investment_horizon"] = args.investment_horizon
        if args.market_reserve is not None:
            knobs["market_reserve"] = args.market_reserve
        if args.market_start is not None:
            knobs["market_start"] = args.market_start
        if args.market_stop is not None:
            knobs["market_stop"] = args.market_stop
        if knobs:
            source = _apply_replacements(source, knobs)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(source, encoding="utf-8")
        py_compile.compile(str(args.output), doraise=True)
        digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
        print(
            f"clone_horizon={args.clone_horizon} knobs={knobs} "
            f"sha256={digest} path={args.output.resolve()}"
        )
        return

    # grid mode -------------------------------------------------------
    args.output_dir.mkdir(parents=True, exist_ok=True)
    index: list[dict] = []
    for idx, knobs in enumerate(_grid_spec()):
        variant_dir = args.output_dir / f"variant_{idx:03d}"
        main_path = variant_dir / "main.py"
        sha = build_variant(args.source, main_path, knobs)
        entry = {
            "idx": idx,
            "variant_dir": str(variant_dir.resolve()),
            "main_path": str(main_path.resolve()),
            "sha256": sha,
            **knobs,
        }
        index.append(entry)
        print(
            f"variant_{idx:03d} msb={knobs['maximum_sell_batch']} "
            f"ih={knobs['investment_horizon']} mr={knobs['market_reserve']} "
            f"window=[{knobs['market_start']},{knobs['market_stop']}] "
            f"sha256={sha}"
        )

    summary = {
        "source": str(args.source.resolve()),
        "output_dir": str(args.output_dir.resolve()),
        "axes": _GRID_AXES,
        "combo_count": len(index),
        "expected": math.prod(len(v) for v in _GRID_AXES.values()),
        "variants": index,
    }
    index_path = args.output_dir / "grid_index.json"
    index_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {len(index)} variants -> {args.output_dir.resolve()} "
        f"(index: {index_path.resolve()})"
    )


if __name__ == "__main__":
    main()
