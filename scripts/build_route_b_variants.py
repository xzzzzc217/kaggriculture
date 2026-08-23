"""Build Route B 27-variant directory from the existing ih=2 variants in kaito_route_a.

Route B freezes investment_horizon=2 (the h2 axis from Route A) and re-sweeps
the other three axes: maximum_sell_batch × market_reserve × market_window
(3×3×3 = 27 variants).  Variants are symlinked/copied from the existing
kaito_route_a directory and a grid_index.json is written alongside.

Usage:
    python scripts/build_route_b_variants.py
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

_GRID_AXES = {
    "maximum_sell_batch": [50, 100, 150],
    "investment_horizon": [2],
    "market_reserve": [300.0, 500.0, 700.0],
    "market_window": [(60, 700), (72, 716), (84, 720)],
}


def _grid_spec() -> list[dict]:
    spec: list[dict] = []
    for msb in _GRID_AXES["maximum_sell_batch"]:
        for ih in _GRID_AXES["investment_horizon"]:
            for mr in _GRID_AXES["market_reserve"]:
                for mstart, mstop in _GRID_AXES["market_window"]:
                    spec.append({
                        "maximum_sell_batch": msb,
                        "investment_horizon": ih,
                        "market_reserve": mr,
                        "market_start": mstart,
                        "market_stop": mstop,
                    })
    return spec


def build(output_dir: Path, source_dir: Path) -> list[dict]:
    output_dir.mkdir(parents=True, exist_ok=True)

    grid_index_src = source_dir / "grid_index.json"
    if not grid_index_src.exists():
        raise FileNotFoundError(f"grid_index.json not found in {source_dir}")
    src_data = json.loads(grid_index_src.read_text(encoding="utf-8"))
    idx_map = {(v["maximum_sell_batch"],
                 v["investment_horizon"],
                 v["market_reserve"],
                 v["market_start"],
                 v["market_stop"]): v
               for v in src_data["variants"]}

    spec = _grid_spec()
    index: list[dict] = []
    for idx, knobs in enumerate(spec):
        key = (knobs["maximum_sell_batch"],
               knobs["investment_horizon"],
               knobs["market_reserve"],
               knobs["market_start"],
               knobs["market_stop"])
        src_variant = idx_map.get(key)
        if not src_variant:
            raise ValueError(f"No Route A variant found for knobs: {knobs}")

        src_main = Path(src_variant["main_path"])
        variant_dir = output_dir / f"variant_{idx:03d}"
        variant_dir.mkdir(parents=True, exist_ok=True)
        dst_main = variant_dir / "main.py"
        shutil.copy2(src_main, dst_main)
        sha = hashlib.sha256(dst_main.read_bytes()).hexdigest()

        entry = {
            "idx": idx,
            "route_a_variant_id": src_variant["variant_dir"].rsplit("\\", 1)[-1]
                                if "\\" in src_variant["variant_dir"]
                                else src_variant["variant_dir"].split("/")[-1],
            "variant_dir": str(variant_dir.resolve()),
            "main_path": str(dst_main.resolve()),
            "sha256": sha,
            **knobs,
        }
        index.append(entry)
        print(
            f"variant_{idx:03d} route_a={entry['route_a_variant_id']} "
            f"msb={knobs['maximum_sell_batch']} ih={knobs['investment_horizon']} "
            f"mr={knobs['market_reserve']} window=[{knobs['market_start']},{knobs['market_stop']}] "
            f"sha256={sha}"
        )

    summary = {
        "source": str(source_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "axes": _GRID_AXES,
        "combo_count": len(index),
        "expected": math.prod(len(v) for v in _GRID_AXES.values()),
        "variants": index,
    }
    index_path = output_dir / "grid_index.json"
    index_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {len(index)} variants -> {output_dir.resolve()} (index: {index_path.resolve()})")
    return index


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    SOURCE_DIR = PROJECT_ROOT / "artifacts" / "variants" / "kaito_route_a"
    OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "variants" / "kaito_route_b"
    build(OUTPUT_DIR, SOURCE_DIR)
