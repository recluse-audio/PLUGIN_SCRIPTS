#!/usr/bin/env python3
"""
JUCE Plugin Project Setup Script

Creates a complete boilerplate JUCE plugin project with directory structure,
source files, CMake configuration, build scripts, and test framework.

Usage:
    python setup_project.py <project_path>

Example:
`C:\REPOS\PLUGIN_PROJECTS> python C:\REPOS\PLUGIN_PROJECTS\SCRIPTS\setup_project.py C:\REPOS\PLUGIN_PROJECTS\AudioFileChanger`

The project name is automatically derived from the directory name.
"""

import sys
import subprocess
from pathlib import Path


def run_module(module_name: str, *args) -> None:
    """
    Run a setup module script.

    Args:
        module_name: Name of the Python module in SETUP_SCRIPTS
        *args: Arguments to pass to the module
    """
    script_dir = Path(__file__).parent / "SETUP_SCRIPTS"
    script_path = script_dir / f"{module_name}.py"

    if not script_path.exists():
        raise FileNotFoundError(f"Setup module not found: {script_path}")

    cmd = [sys.executable, str(script_path)] + list(args)
    subprocess.run(cmd, check=True)


def setup_project(project_path: str) -> None:
    """
    Set up a complete JUCE plugin project.

    Args:
        project_path: Path to the project directory (will be created if it doesn't exist)
    """
    project_root = Path(project_path).resolve()
    project_name = project_root.name

    # Validate project name
    if not project_name:
        raise ValueError("Project path must have a directory name")

    if not project_name.replace("_", "").replace("-", "").isalnum():
        raise ValueError(
            f"Project name '{project_name}' contains invalid characters. "
            "Use only alphanumeric characters, underscores, and hyphens."
        )

    # Create project root directory
    project_root.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"Setting up JUCE Plugin Project: {project_name}")
    print(f"Location: {project_root}")
    print(f"{'='*70}\n")

    # Step 1: Create directory structure
    print("Creating directory structure...")
    run_module("create_directories", str(project_root))

    # Step 2: Create .gitignore
    print("\nCreating .gitignore...")
    run_module("create_gitignore", str(project_root))

    # Step 3: Create README
    print("\nCreating README.md...")
    run_module("create_readme", str(project_root), project_name)

    # Step 4: Create source files
    print("\nCreating source files...")
    run_module("create_source_files", str(project_root), project_name)

    # Step 5: Create version files
    print("\nCreating version files...")
    run_module("create_version", str(project_root))

    # Step 6: Create CMake configuration
    print("\nCreating CMake configuration...")
    run_module("create_cmake", str(project_root), project_name)

    # Step 7: Create test utilities
    print("\nCreating test utilities...")
    run_module("create_test_utils", str(project_root), project_name)

    # Step 8: Copy build scripts
    print("\nCopying build scripts...")
    scripts_source = Path(__file__).parent
    run_module("copy_scripts", str(scripts_source), str(project_root))

    # Final message
    print(f"\n{'='*70}")
    print(f"Project '{project_name}' created successfully!")
    print(f"{'='*70}\n")

    print("Next steps:")
    print(f"  1. cd {project_root}")
    print("  2. Initialize git: git init")
    print("  3. Add JUCE submodule:")
    print("     git submodule add https://github.com/juce-framework/JUCE.git SUBMODULES/JUCE")
    print("  4. Update submodules: git submodule update --init --recursive")
    print("  5. Build the project: python SCRIPTS/rebuild_all.py")
    print("\nOptional:")
    print("  - Update CMakeLists.txt with your company name and plugin codes")
    print("  - Add your custom parameters in PluginProcessor.cpp")
    print("  - Design your UI in PluginEditor.cpp")
    print("  - Add tests in TESTS/ directory")
    print()


def main() -> int:
    """Main entry point."""
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    project_path = sys.argv[1]

    try:
        setup_project(project_path)
        return 0
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
