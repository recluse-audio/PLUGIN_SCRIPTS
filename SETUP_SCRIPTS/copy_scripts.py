#!/usr/bin/env python3
"""
Copies build, signing, and installer scripts to a new JUCE plugin project.
"""

import shutil
from pathlib import Path


def copy_flat(source_dir: Path, dest_dir: Path, exclude: set[str]) -> int:
    """Copy all files (not directories) from source to dest. Returns count."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    if source_dir.exists():
        for item in source_dir.iterdir():
            if item.name in exclude or item.is_dir():
                continue
            shutil.copy2(item, dest_dir / item.name)
            count += 1
            print(f"  Copied {item.name}")
    return count


def copy_tree(source_dir: Path, dest_dir: Path) -> int:
    """Recursively copy all files preserving subdirectory structure. Returns count."""
    count = 0
    if not source_dir.exists():
        return count
    for item in source_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(source_dir)
            dest_file = dest_dir / rel
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_file)
            count += 1
            print(f"  Copied {rel}")
    return count


def copy_scripts(scripts_source_dir: Path, project_root: Path) -> None:
    """
    Copy all build, signing, and installer scripts to the project.

    Args:
        scripts_source_dir: Path to the PLUGIN_SCRIPTS directory
        project_root: Path to the project root directory
    """
    exclude = {'SETUP_SCRIPTS', 'PLUGIN_SCRIPTS', 'setup_project.py', '__pycache__',
               'SIGNED_SCRIPTS', 'INSTALLER_SCRIPTS'}

    # 1. Copy HELPER_SCRIPTS
    plugin_scripts_dir = scripts_source_dir / "HELPER_SCRIPTS"
    if plugin_scripts_dir.exists() and plugin_scripts_dir.is_dir():
        source_dir = plugin_scripts_dir
    else:
        source_dir = scripts_source_dir

    print("Copying HELPER_SCRIPTS/...")
    count = copy_flat(source_dir, project_root / "HELPER_SCRIPTS", exclude)
    if count == 0:
        print(f"  Warning: No files found to copy from {source_dir}")
    else:
        print(f"  Total: {count} file(s) to HELPER_SCRIPTS/")

    # 2. Copy SIGNED_SCRIPTS -> SIGNED/
    signed_source = scripts_source_dir / "SIGNED_SCRIPTS"
    if signed_source.exists():
        print("\nCopying SIGNED_SCRIPTS/ -> SIGNED/...")
        count = copy_tree(signed_source, project_root / "SIGNED")
        print(f"  Total: {count} file(s) to SIGNED/")

    # 3. Copy INSTALLER_SCRIPTS -> INSTALLERS/
    installer_source = scripts_source_dir / "INSTALLER_SCRIPTS"
    if installer_source.exists():
        print("\nCopying INSTALLER_SCRIPTS/ -> INSTALLERS/...")
        count = copy_tree(installer_source, project_root / "INSTALLERS")
        print(f"  Total: {count} file(s) to INSTALLERS/")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python copy_scripts.py <scripts_source_dir> <project_root>")
        sys.exit(1)

    source = Path(sys.argv[1])
    root = Path(sys.argv[2])
    copy_scripts(source, root)
