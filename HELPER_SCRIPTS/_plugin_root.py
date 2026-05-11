"""Locate the consuming plugin's repo root by walking up for marker files.

Scripts in this HELPER_SCRIPTS dir are used as a git submodule, so
`Path(__file__).parents[N]` cannot statically point at the plugin repo.
Walk up from the caller (or this file) until both CMakeLists.txt and
VERSION.txt are present — those mark a JUCE plugin repo root.
"""

from __future__ import annotations

from pathlib import Path


MARKERS = ("CMakeLists.txt", "VERSION.txt")


def find_plugin_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__)).resolve()
    if p.is_file():
        p = p.parent
    for ancestor in [p, *p.parents]:
        if all((ancestor / m).is_file() for m in MARKERS):
            return ancestor
    raise RuntimeError(
        f"Could not find plugin root (need {MARKERS}) above {start or __file__}"
    )
