# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A zero-dependency Python-based generator for JUCE audio plugin projects. It creates production-ready CMake + JUCE boilerplate in seconds, targeting beginners who want to skip CMake complexity while giving experts clean, hackable output.

**Core value proposition**: 3 commands from nothing to a working VST3/Standalone plugin with tests.

## Critical Architectural Concepts

### Two-Phase Separation (NEVER Mix These)

1. **Generator Phase** - Lives in this repo only:
   - `setup_project.py` - Orchestrator
   - `SETUP_SCRIPTS/*.py` - Individual generators (directories, CMake, source templates, etc.)
   - Runs ONCE per project to generate boilerplate

2. **Build Phase** - Gets copied to generated projects:
   - `HELPER_SCRIPTS/*.py` - Build/utility scripts that users run repeatedly
   - Must be standalone (no imports from SETUP_SCRIPTS)
   - Must auto-detect plugin name from current directory: `Path.cwd().name`

**Why this matters**: Generator scripts create projects. Build scripts work inside projects. If you add logic to the wrong phase, it breaks.

### The Copy Mechanism

`SETUP_SCRIPTS/copy_scripts.py` copies `HELPER_SCRIPTS/*.py` → generated project's `SCRIPTS/` folder. This means:
- Changes to HELPER_SCRIPTS only affect NEW projects (not existing ones)
- Build scripts must never import from SETUP_SCRIPTS
- Build scripts must be self-contained Python 3.7+ standard library code

### regenSource.py Auto-Discovery Pattern

Build scripts call `regenSource.py` before building. It:
1. Scans `SOURCE/` and `TESTS/` (plus any `SUBMODULES/*/SOURCE` and `SUBMODULES/*/TESTS`)
2. Auto-generates `CMAKE/SOURCES.cmake` and `CMAKE/TESTS.cmake` with all `.h/.cpp` files
3. Ensures CMake always has current file lists

This means users never manually edit CMake file lists - just add files and rebuild.

### Multi-Config vs Single-Config Generators

**Critical for build scripts**: CMake generators differ across platforms.

**Multi-config** (Windows Visual Studio, macOS Xcode):
```bash
cmake --build BUILD --config Debug    # Output: BUILD/Debug/
cmake --build BUILD --config Release  # Output: BUILD/Release/
```

**Single-config** (Linux Makefiles, Ninja):
```bash
cmake -B BUILD -DCMAKE_BUILD_TYPE=Debug  # Output: BUILD/
cmake --build BUILD
```

All build scripts must handle both. Check existing `rebuild_all.py` or `build_vst3.py` for the pattern.

## Common Development Commands

### Test the Generator (Full End-to-End)

```bash
# From this repository root
python setup_project.py /tmp/TestPlugin
cd /tmp/TestPlugin
python SCRIPTS/init_project.py   # Adds JUCE submodule (1-2 min download)
python SCRIPTS/rebuild_all.py    # Full build (2-5 min first time)
```

### Test a Single Setup Module

```bash
# Example: test directory creation
python SETUP_SCRIPTS/create_directories.py /tmp/test_output
```

### Modify Generated Templates

Templates are embedded as strings in `SETUP_SCRIPTS/create_*.py`:
- `create_source_files.py` - PluginProcessor/Editor boilerplate
- `create_cmake.py` - CMakeLists.txt template
- `create_readme.py` - Generated project README

Use `{PROJECT_NAME}`, `{PROJECT_NAME_LOWER}`, `{PLUGIN_CODE}` placeholders.

## Non-Obvious Implementation Details

### File Encoding Requirement

**CRITICAL on Windows**: Always use `encoding='utf-8'` when writing files.

```python
# Correct
path.write_text(content, encoding='utf-8')

# WRONG - Fails on Windows with codec errors
path.write_text(content)
```

### Path Handling for Cross-Platform

- Use `pathlib.Path` exclusively (never string concatenation)
- In CMake templates, use forward slashes: `SOURCE/Util/Juce_Header.h` (CMake normalizes them)
- In Python, `Path` objects handle OS differences automatically

### Template Variable Substitution

All templates support:
- `{PROJECT_NAME}` - e.g., "AudioFileChanger"
- `{PROJECT_NAME_LOWER}` - e.g., "audiofilechanger"
- `{PLUGIN_CODE}` - First 4 chars of project name (e.g., "Audi")

Applied via: `template.format(PROJECT_NAME=name, PROJECT_NAME_LOWER=name.lower(), ...)`

### Version Management Pattern

- `VERSION.txt` - Plain text: "0.0.1"
- `update_version.py` - Reads VERSION.txt, increments patch, writes `Version.h`
- CMake reads VERSION.txt at configure time
- `Version.h` auto-generated before each build via custom target

### JUCE Module Centralization

Generated projects use `SOURCE/Util/Juce_Header.h` to centralize JUCE includes. This:
- Makes Catch2 tests work (Catch2 conflicts with JUCE's global `using namespace` unless controlled)
- Provides single point to add/remove JUCE modules
- Must stay in sync with `CMakeLists.txt` linked libraries

## Project Constraints (Never Violate)

1. **No external dependencies** - Python 3.7+ standard library only (no pip, no imports outside stdlib)
2. **No emojis** - User preference, applies to all output/messages/generated code
3. **Cross-platform mandatory** - Must work on Windows/macOS/Linux with standard CMake generators

## Current Directory Structure Issues

**IMPORTANT**: The folder was recently renamed from `PLUGIN_SCRIPTS/` to `HELPER_SCRIPTS/`, but some references are stale:

Files needing updates:
1. `.gitignore:32-33` - Still references `!PLUGIN_SCRIPTS/`
2. `CONTRIBUTING.md:62,82,95` - Documentation uses old name
3. `SETUP_SCRIPTS/copy_scripts.py:12,15,18,19,30` - Code looks for `PLUGIN_SCRIPTS/` folder
4. `setup_project.py:12` - Example command uses old path structure

Correct structure:
```
PLUGIN_SCRIPTS/              # Repository root (somewhat confusing name now)
├── setup_project.py         # Main entry point
├── SETUP_SCRIPTS/           # Generator modules
│   ├── create_directories.py
│   ├── create_cmake.py
│   └── ...
├── HELPER_SCRIPTS/          # Files copied to generated projects (NEW NAME)
│   ├── init_project.py
│   ├── rebuild_all.py
│   └── ...
├── README.md
└── CLAUDE.md (this file)
```

## Testing Protocol Before Releases

1. **Clean generation test** (critical path):
   ```bash
   python setup_project.py /tmp/CleanTest
   cd /tmp/CleanTest
   python SCRIPTS/init_project.py
   python SCRIPTS/rebuild_all.py
   ```

2. **Verify outputs**:
   - All directories created
   - Git initialized
   - JUCE submodule added
   - CMake configures without errors
   - Build completes (both Debug and Release)
   - VST3 loads in a DAW (manual test)

3. **Cross-platform** (if possible):
   - Test on Windows (Visual Studio generator)
   - Test on macOS (Xcode or Makefiles)
   - Verify Linux compatibility (Ubuntu/Arch with GCC)

## Known Edge Cases

### regenSource.py Submodule Discovery

If users add submodules with `SOURCE/` or `TESTS/` folders (beyond JUCE), regenSource.py will include them automatically. This is usually desired but can cause issues if submodule structure is unexpected.

### JUCE Splash Screen Licensing

Generated projects enable `JUCE_DISPLAY_SPLASH_SCREEN=1` by default. Disabling requires a JUCE license. Users sometimes ask about this - point them to JUCE licensing docs.

### CMAKE_BUILD_TYPE vs --config

Beginners confuse single-config (`-DCMAKE_BUILD_TYPE=Release`) with multi-config (`--config Release`). Build scripts auto-detect the generator and use the correct approach.

### Python Version Compatibility

Target: Python 3.7+ (for wider compatibility)
- Use `pathlib.Path` (available since 3.4)
- Avoid f-strings if supporting <3.6 (currently we use f-strings, so 3.6+ minimum)
- No match/case statements (requires 3.10+)

## How to Add Features

### New Setup Module (Generator)

1. Create `SETUP_SCRIPTS/my_feature.py`
2. Define `def create_my_feature(project_root: Path, project_name: str):`
3. Call from `setup_project.py` in `setup_project()` function
4. Update README.md with description

### New Build Script (User-Facing)

1. Create `HELPER_SCRIPTS/my_script.py`
2. Add shebang: `#!/usr/bin/env python3`
3. Import only stdlib: `import sys, subprocess, shutil` (no setup module imports)
4. Auto-detect plugin name: `PLUGIN_NAME = Path.cwd().name`
5. Call `regenSource.py` if modifying CMake inputs
6. Handle multi-config vs single-config generators
7. Test on Windows/macOS if possible

### Modify Generated Code Templates

Templates are multiline strings in `SETUP_SCRIPTS/create_*.py`. When modifying:
- Maintain `{VARIABLE}` placeholder syntax
- Test template rendering with edge-case names (spaces, special chars)
- Verify CMake syntax validity (forward slashes, proper escaping)
- Check JUCE requirements (processor/editor virtual methods, APVTS usage)

## Philosophy & Design Goals

1. **Minimize friction** - 3 commands to working plugin (setup, init, build)
2. **No magic** - Generated code is readable, modifiable, and uses standard JUCE patterns
3. **Modern defaults** - C++20, APVTS, Catch2 tests, version management included
4. **Beginner friendly** - No CMake knowledge required to get started
5. **Expert extensible** - Generated CMake is clean, well-commented, easy to customize

## When to Say No

This project intentionally stays simple. Reject feature requests for:
- GUI wizards (keep it CLI)
- External dependencies (maintain zero-dependency promise)
- Platform-specific hacks (maintain cross-platform purity)
- Overly complex templates (users should customize generated projects, not templates)

The generator creates a starting point. Users customize the generated projects themselves.
