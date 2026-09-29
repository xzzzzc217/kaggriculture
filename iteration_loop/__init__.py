"""In-repo Kaggriculture iteration loop."""

from __future__ import annotations

from typing import Any

__all__ = ["decide", "main"]


def __getattr__(name: str) -> Any:
    if name == "decide":
        from iteration_loop.promotion import decide

        return decide
    if name == "main":
        from iteration_loop.loop import main

        return main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
