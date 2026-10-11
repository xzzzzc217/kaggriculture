"""Pack six-day tapes + logic into one submission main.py. No upload here."""

from __future__ import annotations

import hashlib
import py_compile
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = Path(__file__).resolve().parents[3] / "artifacts/submission/yusuke_sixday/main.py"

HEADER = '''# SPDX-License-Identifier: Apache-2.0
"""Yusuke six-day public-state Fieldbook (Python port). One-file submission.

Reselects at 144/288/432/576. Does not load agent.so. Not a 227/242/266
sheep wrap of Fieldbook BALANCED.
"""

from __future__ import annotations

'''


def _strip_module_preamble(text: str) -> str:
    text = re.sub(r"^# SPDX-License-Identifier: Apache-2.0\n", "", text)
    text = re.sub(r'^""".*?"""\n+', "", text, count=1, flags=re.S)
    text = re.sub(r"^from __future__ import annotations\n+", "", text)
    return text.lstrip()


def main() -> None:
    tapes = _strip_module_preamble((SRC / "sixday_tapes.py").read_text(encoding="utf-8"))
    logic = _strip_module_preamble((SRC / "sixday_logic.py").read_text(encoding="utf-8"))
    logic = logic.replace("from sixday_tapes import ENCODED_SEGMENTS\n\n", "")
    logic = logic.replace("from sixday_tapes import ENCODED_SEGMENTS\n", "")
    packed = (
        HEADER
        + tapes.rstrip()
        + "\n\n"
        + logic.rstrip()
        + "\n\nagent = make_agent()\nmain = agent\n"
    )
    if "from sixday_tapes import" in packed:
        raise SystemExit("sibling import still present")
    raw = packed.encode("utf-8").replace(b"\r\n", b"\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(raw)
    py_compile.compile(str(OUT), doraise=True)
    print("path", OUT)
    print("bytes", len(raw))
    print("sha256", hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
