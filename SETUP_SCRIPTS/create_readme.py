#!/usr/bin/env python3
"""
Creates a README.md file for a JUCE plugin project.
"""

from pathlib import Path


README_TEMPLATE = """# {PROJECT_NAME}

A JUCE audio plugin project.

## Building

### Prerequisites
- CMake 3.24.1 or higher
- C++20 compatible compiler
- JUCE framework (included as submodule)

### Setup

If this is a new project (not cloned from a repository):
```bash
# Initialize git and add JUCE submodule
python SCRIPTS/init_project.py
```

If cloning from an existing repository:
```bash
# Clone with submodules
git clone --recursive <repository-url>

# Or if already cloned, initialize submodules
git submodule update --init --recursive
```

### Build Commands

#### All Targets (Clean Rebuild)
```bash
python SCRIPTS/rebuild_all.py
```

#### VST3
```bash
python SCRIPTS/build_vst3.py
```

#### Standalone Application
```bash
python SCRIPTS/build_app.py
```

#### Run Tests
```bash
python SCRIPTS/build_tests.py
cd BUILD
ctest
```

### Build Configuration

By default, builds are created in Debug mode. To build in Release mode:
```bash
# On Windows (multi-config generator)
python SCRIPTS/rebuild_all.py --config Release

# On macOS/Linux (single-config generator)
CMAKE_BUILD_TYPE=Release python SCRIPTS/rebuild_all.py
```

## Project Structure

```
{PROJECT_NAME}/
├── SOURCE/           # Plugin source code
│   ├── PluginProcessor.h/.cpp
│   ├── PluginEditor.h/.cpp
│   └── Util/        # Utility headers
├── CMAKE/           # CMake configuration files
├── SCRIPTS/         # Build scripts
├── TESTS/           # Unit tests
├── SUBMODULES/      # Git submodules (JUCE, etc.)
├── BUILD/           # Build artifacts (not tracked)
├── NOTES/           # Development notes
└── DIAGRAMS/        # Architecture diagrams
```

## Development

### Version Management
Version is tracked in `VERSION.txt`. The build system automatically generates
`SOURCE/Util/Version.h` with version macros.

To increment version:
```bash
python SCRIPTS/update_version.py VERSION.txt SOURCE/Util/Version.h
```

### Adding Source Files
1. Add your .h/.cpp files to the `SOURCE/` directory
2. List them in `CMAKE/SOURCES.cmake`
3. Rebuild

### Adding Tests
1. Add test files to `TESTS/` directory
2. List them in `CMAKE/TESTS.cmake`
3. Run `python SCRIPTS/build_tests.py`

## License

[Add your license here]
"""


def create_readme(project_root: Path, project_name: str) -> None:
    """
    Create a README.md file for the project.

    Args:
        project_root: Path to the project root directory
        project_name: Name of the project
    """
    readme_content = README_TEMPLATE.format(PROJECT_NAME=project_name)
    readme_path = project_root / "README.md"
    readme_path.write_text(readme_content.lstrip(), encoding='utf-8')
    print(f"  Created README.md")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_readme.py <project_root> <project_name>")
        sys.exit(1)

    root = Path(sys.argv[1])
    name = sys.argv[2]
    create_readme(root, name)
