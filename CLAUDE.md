# JUCE CMake Project Generator - Development Guide

This document provides context for AI assistants working on this project.

## Project Overview

A Python-based project generator for JUCE audio plugins that eliminates CMake boilerplate. The goal is to make JUCE + CMake accessible to beginners while providing production-ready project structure.

## Architecture

### Two-Phase System

1. **Setup Phase** (`setup_project.py` + `SETUP_SCRIPTS/`)
   - Runs once to create a new project
   - Generates directory structure, source files, CMake config
   - Lives in this repository only

2. **Generated Project Phase** (`PLUGIN_SCRIPTS/`)
   - Scripts that get copied to generated projects
   - Used repeatedly by developers building their plugins
   - Must be standalone and dependency-free

### Key Principle
Setup scripts generate code. Build scripts work with existing code. Never mix the two.

## Directory Structure

```
SCRIPTS/
├── setup_project.py           # Main entry point - orchestrates everything
├── SETUP_SCRIPTS/             # Generator modules (not copied to projects)
│   ├── create_directories.py  # Creates folder structure
│   ├── create_cmake.py        # Generates CMakeLists.txt
│   ├── create_source_files.py # Generates PluginProcessor/Editor boilerplate
│   ├── create_gitignore.py    # Creates .gitignore
│   ├── create_readme.py       # Creates project README
│   ├── create_version.py      # Creates VERSION.txt and Version.h
│   ├── create_test_utils.py   # Creates test framework files
│   └── copy_scripts.py        # Copies PLUGIN_SCRIPTS to new project
└── PLUGIN_SCRIPTS/            # Files copied to generated projects
    ├── init_project.py        # Initializes git + JUCE submodule
    ├── rebuild_all.py         # Clean rebuild script
    ├── build_vst3.py          # VST3-only build
    ├── build_app.py           # Standalone-only build
    ├── build_tests.py         # Test build
    ├── build_au.py            # AU build (macOS)
    ├── update_version.py      # Version management
    ├── regenSource.py         # Auto-regenerates CMAKE/*.cmake from files
    ├── addClass.py            # Helper: creates new class files
    └── addFunction.py         # Helper: adds functions to existing classes
```

## Code Patterns

### Template Variables
All templates support these substitutions:
- `{PROJECT_NAME}` - Plugin name (e.g., "AudioFileChanger")
- `{PROJECT_NAME_LOWER}` - Lowercase plugin name
- `{PLUGIN_CODE}` - 4-char plugin code (first 4 chars of project name)

### File Encoding
**CRITICAL**: All file writes must use `encoding='utf-8'` on Windows to avoid codec errors.

```python
# Good
path.write_text(content, encoding='utf-8')

# Bad - will fail on Windows
path.write_text(content)
```

### Path Handling
- Always use `pathlib.Path`, never string concatenation
- Use forward slashes in templates for cross-platform CMake compatibility
- Test on Windows (backslashes), macOS, and Linux

### Plugin Name Detection
Build scripts auto-detect plugin name from directory:
```python
PLUGIN_NAME = Path.cwd().name
```

### Build Script Pattern
All build scripts follow this pattern:
1. Call `regenSource.py` to update CMAKE/*.cmake
2. Configure CMake
3. Build target
4. Handle multi-config vs single-config generators

## Important Constraints

### No External Dependencies
- Python standard library only (no pip installs)
- Must work with Python 3.7+
- This is a key selling point for the project

### No Emojis
User preference: no emoji characters in any generated output or script messages.

### Cross-Platform Support
Must work on:
- Windows (Visual Studio, Ninja)
- macOS (Xcode, Makefiles)
- Linux (GCC, Makefiles, Ninja)

## Generated Project Structure

When `setup_project.py MyPlugin` runs, it creates:

```
MyPlugin/
├── SOURCE/
│   ├── PluginProcessor.h/.cpp    # APVTS-based processor
│   ├── PluginEditor.h/.cpp       # Timer-based editor with example slider
│   └── Util/
│       ├── Juce_Header.h         # Centralized JUCE includes (Catch2 compatible)
│       └── Version.h             # Auto-generated from VERSION.txt
├── CMAKE/
│   ├── SOURCES.cmake             # Auto-updated by regenSource.py
│   └── TESTS.cmake               # Auto-updated by regenSource.py
├── SCRIPTS/                      # Copied from PLUGIN_SCRIPTS/
├── TESTS/
│   ├── TEST_UTILS/
│   │   ├── TestUtils.h/.cpp      # Test helpers (sine generator, RMS, etc.)
│   └── test_Processor.cpp        # Example tests
├── SUBMODULES/                   # Empty until init_project.py runs
├── BUILD/                        # Created by build scripts
├── NOTES/, DIAGRAMS/             # Empty, for developer use
├── CMakeLists.txt                # Main CMake config
├── VERSION.txt                   # "0.0.1"
├── .gitignore                    # Comprehensive ignore patterns
└── README.md                     # Instructions for using the generated project
```

## Common Tasks

### Adding a New Setup Module
1. Create `SETUP_SCRIPTS/my_module.py`
2. Implement `def my_function(project_root: Path, project_name: str):`
3. Call it from `setup_project.py` in `setup_project()` function
4. Add description to README.md

### Adding a New Build Script
1. Create `PLUGIN_SCRIPTS/my_script.py`
2. Add `regenerate_cmake_lists()` call at the start
3. Make plugin name dynamic: `PLUGIN_NAME = Path.cwd().name`
4. Handle multi-config generators (VS/Xcode) properly
5. Test on Windows and macOS if possible

### Modifying Generated Code Templates
Templates are embedded in `SETUP_SCRIPTS/create_source_files.py`:
- `PLUGIN_PROCESSOR_H_TEMPLATE`
- `PLUGIN_PROCESSOR_CPP_TEMPLATE`
- `PLUGIN_EDITOR_H_TEMPLATE`
- `PLUGIN_EDITOR_CPP_TEMPLATE`

When changing, ensure:
- Include paths use `Util/Juce_Header.h` (not `../Util/`)
- Class names use `{PROJECT_NAME}Processor` pattern
- APVTS parameter management is consistent

### Updating JUCE Modules
The `Juce_Header.h` includes are in `create_source_files.py` in `JUCE_HEADER_TEMPLATE`.
Must match what's linked in CMakeLists.txt.

Current modules:
- juce_audio_utils
- juce_audio_processors
- juce_gui_extra
- juce_gui_basics
- juce_graphics
- juce_events
- juce_core
- juce_data_structures
- juce_audio_basics
- juce_audio_formats
- juce_audio_devices
- juce_opengl
- juce_audio_plugin_client
- juce_dsp

## Testing Protocol

Before releasing changes:

1. **Clean test:**
   ```bash
   python setup_project.py /tmp/TestPlugin
   cd /tmp/TestPlugin
   python SCRIPTS/init_project.py
   python SCRIPTS/rebuild_all.py
   ```

2. **Verify:**
   - Project generates without errors
   - Git initializes
   - JUCE downloads (takes time)
   - CMake configures
   - Build completes
   - Plugin loads in a DAW

3. **Cross-platform:**
   - Test on Windows if possible
   - Check generator detection (VS vs Makefiles vs Ninja)

## Known Issues / Gotchas

### regenSource.py Auto-Discovery
- Scans `SUBMODULES/*/SOURCE` and `SUBMODULES/*/TESTS`
- Will include any submodule's files automatically
- Users might need to customize for specific workflows

### Multi-Config Generators
Windows (Visual Studio) and macOS (Xcode) use multi-config:
- Plugins go to `BUILD/Debug/` or `BUILD/Release/`
- Must pass `--config` to build command

Single-config (Makefiles, Ninja):
- Plugins go to `BUILD/`
- Configure time: `-DCMAKE_BUILD_TYPE=Debug`

### JUCE Splash Screen
Currently enabled by default (`JUCE_DISPLAY_SPLASH_SCREEN=1`).
Some users might want to disable this, but it requires a JUCE license.

### Version Management
- `VERSION.txt` is plain text: "0.0.1"
- `update_version.py` increments patch and regenerates `Version.h`
- CMake reads VERSION.txt at configure time
- Must reconfigure if version changes

## Development Philosophy

1. **Minimize friction** - 3 commands to working plugin
2. **No magic** - Generated code is readable and modifiable
3. **Modern defaults** - C++20, APVTS, tests included
4. **Beginner friendly** - No CMake knowledge required
5. **Expert extensible** - Generated CMake is clean and hackable

## Future Considerations

Potential features to discuss:
- GUI wizard for project setup
- Multiple templates (minimal, effects, synth)
- AAX format support (requires iLok SDK)
- CI/CD template files
- VSCode extension
- Web-based generator

## Performance Notes

- JUCE submodule download: ~200MB, 1-2 minutes
- Initial CMake configure: 10-30 seconds
- First build: 2-5 minutes (JUCE compilation)
- Incremental builds: 5-30 seconds

## Contribution Guidelines

See CONTRIBUTING.md for:
- Code style
- PR process
- Testing requirements
- Documentation expectations

## Support Channels

- GitHub Issues for bugs
- GitHub Discussions for questions
- JUCE Forum for JUCE-specific help

## Release Checklist

Before tagging a release:
- [ ] All build scripts tested
- [ ] README accurate
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Cross-platform tested
- [ ] No TODO/FIXME comments
- [ ] Examples work

## Project Governance

This is a personal project made public. The maintainer has final say on:
- Feature additions
- Breaking changes
- Code style
- Project direction

PRs welcome but no guarantees on merge timeline.
