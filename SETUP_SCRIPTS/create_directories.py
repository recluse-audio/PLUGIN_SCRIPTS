#!/usr/bin/env python3
"""
Creates the standard directory structure for a JUCE plugin project.
"""

from pathlib import Path
from typing import List


def create_directories(project_root: Path) -> List[str]:
    """
    Create standard JUCE project directories.

    Args:
        project_root: Path to the project root directory

    Returns:
        List of created directory names
    """
    directories = [
        "SOURCE",
        "SOURCE/Util",
        "CMAKE",
        "SUBMODULES",
        "TESTS",
        "TESTS/TEST_UTILS",
        "BUILD",
        "HELPER_SCRIPTS",
        "NOTES",
        "DIAGRAMS",
    ]

    created = []
    for dir_name in directories:
        dir_path = project_root / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        created.append(dir_name)
        print(f"  Created {dir_name}/")

    # Create .gitkeep in BUILD directory to track it in git
    (project_root / "BUILD" / ".gitkeep").touch()

    return created


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_directories.py <project_root>")
        sys.exit(1)

    root = Path(sys.argv[1])
    create_directories(root)
