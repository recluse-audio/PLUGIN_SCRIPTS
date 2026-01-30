#!/usr/bin/env python3
"""
Copies build scripts to a new JUCE plugin project.
"""

import shutil
from pathlib import Path


def copy_scripts(scripts_source_dir: Path, project_root: Path) -> None:
    """
    Copy all build scripts from PLUGIN_SCRIPTS to the project SCRIPTS directory.

    Args:
        scripts_source_dir: Path to the SCRIPTS directory containing PLUGIN_SCRIPTS folder
        project_root: Path to the project root directory
    """
    # Look for PLUGIN_SCRIPTS folder first, fall back to source directory
    plugin_scripts_dir = scripts_source_dir / "PLUGIN_SCRIPTS"
    if plugin_scripts_dir.exists() and plugin_scripts_dir.is_dir():
        source_dir = plugin_scripts_dir
    else:
        # Fall back to source directory, but exclude setup-related files
        source_dir = scripts_source_dir

    dest_scripts_dir = project_root / "SCRIPTS"
    dest_scripts_dir.mkdir(exist_ok=True)

    # Files and folders to exclude from copying
    exclude = {'SETUP_SCRIPTS', 'PLUGIN_SCRIPTS', 'setup_project.py', '__pycache__'}

    copied_count = 0

    # Copy all files from source directory
    if source_dir.exists():
        for item in source_dir.iterdir():
            # Skip excluded items
            if item.name in exclude:
                continue

            # Skip directories (except if we add support for subdirectories later)
            if item.is_dir():
                continue

            # Copy file
            dest_file = dest_scripts_dir / item.name
            shutil.copy2(item, dest_file)
            copied_count += 1
            print(f"  Copied {item.name}")

    if copied_count == 0:
        print(f"  Warning: No files found to copy from {source_dir}")
    else:
        print(f"  Total: Copied {copied_count} file(s) to SCRIPTS/")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python copy_scripts.py <scripts_source_dir> <project_root>")
        sys.exit(1)

    source = Path(sys.argv[1])
    root = Path(sys.argv[2])
    copy_scripts(source, root)
