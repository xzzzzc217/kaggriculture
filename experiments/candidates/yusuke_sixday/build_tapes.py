"""Extract six-day encoded blocks from the local hunt C++ source. No upload."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "artifacts/public_sources/_hunt_20260903/yusuke_sixday_src/policy.cpp"
OUT = Path(__file__).resolve().parent / "sixday_tapes.py"

HEADER = '''# SPDX-License-Identifier: Apache-2.0
"""Encoded 144-turn blocks copied from Yusuke six-day public-state policy.cpp.

Source: artifacts/public_sources/_hunt_20260903/yusuke_sixday_src/policy.cpp
(Apache-2.0). Do not load agent.so. Strings are the C tape payload, not a
Fieldbook BALANCED wrap.
"""

from __future__ import annotations

# segment -> list of routes -> list of encoded turn strings
ENCODED_SEGMENTS: list[list[list[str]]] = [
'''

ARRAY = re.compile(
    r"const char\* const kSegment(\d+)Route(\d+)\[(\d+)\] = \{([^;]+)\};",
    re.S,
)
STRING = re.compile(r'"([^"]*)"')


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    found: dict[tuple[int, int], list[str]] = {}
    expected_len = {0: 144, 1: 144, 2: 144, 3: 144, 4: 143}
    for match in ARRAY.finditer(text):
        segment = int(match.group(1))
        route = int(match.group(2))
        declared = int(match.group(3))
        strings = STRING.findall(match.group(4))
        if declared != expected_len[segment]:
            raise SystemExit(f"segment {segment} route {route} declared {declared}")
        if len(strings) != declared:
            raise SystemExit(
                f"segment {segment} route {route} got {len(strings)} != {declared}"
            )
        found[(segment, route)] = strings
    expected_routes = {0: 1, 1: 2, 2: 1, 3: 3, 4: 5}
    lines = [HEADER]
    for segment in range(5):
        n_routes = expected_routes[segment]
        lines.append(f"    [  # segment {segment}\n")
        for route in range(n_routes):
            strings = found.get((segment, route))
            if strings is None:
                raise SystemExit(f"missing kSegment{segment}Route{route}")
            lines.append(f"        [  # route {route}\n")
            for encoded in strings:
                lines.append(f"            {encoded!r},\n")
            lines.append("        ],\n")
        lines.append("    ],\n")
    lines.append("]\n")
    OUT.write_text("".join(lines), encoding="utf-8", newline="\n")
    print("wrote", OUT, "bytes", OUT.stat().st_size, "arrays", len(found))


if __name__ == "__main__":
    main()
