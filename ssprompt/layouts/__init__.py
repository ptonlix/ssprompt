from __future__ import annotations

from ssprompt.layouts.layout import Layout

_LAYOUTS = {"standard": Layout}


def layout(name: str) -> type[Layout]:
    if name not in _LAYOUTS:
        raise ValueError("Invalid layout")

    return _LAYOUTS[name]