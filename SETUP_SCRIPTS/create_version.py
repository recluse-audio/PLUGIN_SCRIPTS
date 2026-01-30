#!/usr/bin/env python3
"""
Creates VERSION.txt and initial Version.h files for a JUCE plugin project.
"""

from pathlib import Path


VERSION_H_TEMPLATE = """#pragma once
#define BUILD_VERSION_MAJOR 0
#define BUILD_VERSION_MINOR 0
#define BUILD_VERSION_PATCH 1
#define BUILD_VERSION_STRING "0.0.1"
"""


def create_version_files(project_root: Path) -> None:
    """
    Create VERSION.txt and VERSION.h files.

    Args:
        project_root: Path to the project root directory
    """
    # Create VERSION.txt
    version_txt = project_root / "VERSION.txt"
    version_txt.write_text("0.0.1\n", encoding='utf-8')
    print(f"  Created VERSION.txt")

    # Create SOURCE/Util/Version.h
    version_h = project_root / "SOURCE" / "Util" / "Version.h"
    version_h.write_text(VERSION_H_TEMPLATE, encoding='utf-8')
    print(f"  Created SOURCE/Util/Version.h")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_version.py <project_root>")
        sys.exit(1)

    root = Path(sys.argv[1])
    create_version_files(root)
