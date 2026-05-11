#!/usr/bin/env python3
"""
Creates a .gitignore file for a JUCE plugin project.
"""

from pathlib import Path


GITIGNORE_TEMPLATE = """# CMake artifacts
CMakeLists.txt.user
CMakeCache.txt
CMakeFiles/
Makefile
cmake_install.cmake
compile_commands.json
CTestTestfile.cmake
_deps/

# Build directory (keep .gitkeep)
BUILD/*
!BUILD/.gitkeep

# Installation artifacts
Install/*

# IDE configurations
.idea/
.vscode/
cmake-build-*/
.DS_Store

# Packaging output
packaging/Output/*

# VS Code workspace (optional - comment out if you want to track it)
*.code-workspace

# Visual Studio
.vs/
out/
*.user
*.suo
*.sln
*.vcxproj
*.vcxproj.filters

# Xcode
*.xcodeproj/
*.xcworkspace/
DerivedData/

# Python
__pycache__/
*.pyc
*.pyo

# Signed build output
SIGNED/PC/OUTPUT/
SIGNED/MAC/OUTPUT/

# Installer build output
INSTALLERS/PC/BUILD/

# Release packages
RELEASE/

# Operating system
.DS_Store
Thumbs.db
"""


def create_gitignore(project_root: Path) -> None:
    """
    Create a .gitignore file with standard JUCE project ignore patterns.

    Args:
        project_root: Path to the project root directory
    """
    gitignore_path = project_root / ".gitignore"
    gitignore_path.write_text(GITIGNORE_TEMPLATE.lstrip(), encoding='utf-8')
    print(f"  Created .gitignore")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_gitignore.py <project_root>")
        sys.exit(1)

    root = Path(sys.argv[1])
    create_gitignore(root)
