"""Scan unzipped official episodes for Crop Dusta / heralces prefixes."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(r"D:\kaggle\kaggriculture\artifacts\kaggle_runs\episodes_20260828")
needles = (b"Crop Dusta", b"heralces")
counts = {n: 0 for n in needles}
hits = {n: [] for n in needles}
for path in ROOT.glob("*.json"):
    head = path.read_bytes()[:4000]
    for n in needles:
        if n in head:
            counts[n] += 1
            if len(hits[n]) < 15:
                hits[n].append(path.name)
print("counts", {k.decode(): v for k, v in counts.items()})
print("crop hits", hits[b"Crop Dusta"])
print("us hits", hits[b"heralces"])
