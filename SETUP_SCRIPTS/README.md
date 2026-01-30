# JUCE Project Setup Scripts

This directory contains modular scripts for setting up new JUCE plugin projects.

## Main Script

**`../setup_project.py`** - Main orchestrator script that calls all the modules below.

### Usage

```bash
python setup_project.py <project_path>
```

### Example

```bash
python setup_project.py C:\REPOS\PLUGIN_PROJECTS\AudioFileChanger
```

This will:
1. Create the project directory if it doesn't exist
2. Extract the plugin name from the directory name ("AudioFileChanger")
3. Run all setup modules to create a complete JUCE project structure

---

## Module Scripts

These scripts are called by `setup_project.py` but can also be run individually:

### `create_directories.py`
Creates the standard directory structure:
- SOURCE/ - Plugin source code
- SOURCE/Util/ - Utility headers
- CMAKE/ - CMake configuration
- SUBMODULES/ - Git submodules
- TESTS/ - Unit tests
- TESTS/TEST_UTILS/ - Test utilities
- BUILD/ - Build artifacts (with .gitkeep)
- HELPER_SCRIPTS/ - Build scripts
- NOTES/ - Development notes
- DIAGRAMS/ - Architecture diagrams

**Usage:** `python create_directories.py <project_root>`

---

### `create_gitignore.py`
Creates a `.gitignore` file with patterns for:
- CMake artifacts
- Build directory (preserving .gitkeep)
- IDE configurations (VS Code, Visual Studio, Xcode, CLion)
- Operating system files

**Usage:** `python create_gitignore.py <project_root>`

---

### `create_readme.py`
Creates a comprehensive `README.md` with:
- Build instructions
- Prerequisites
- Project structure diagram
- Development guidelines
- Common commands

**Usage:** `python create_readme.py <project_root> <project_name>`

---

### `create_source_files.py`
Creates boilerplate C++ source files:
- **PluginProcessor.h/cpp** - Main audio processor class
  - APVTS parameter management
  - Audio processing callbacks
  - State save/load
  - Example parameter ("gain")
- **PluginEditor.h/cpp** - GUI editor class
  - Basic UI with version label and gain slider
  - Parameter bindings via SliderAttachment
  - Timer for UI updates (30 Hz)
- **Util/Juce_Header.h** - Centralized JUCE includes

**Usage:** `python create_source_files.py <project_root> <project_name>`

---

### `create_version.py`
Creates version tracking files:
- **VERSION.txt** - Plain text version number (0.0.1)
- **SOURCE/Util/Version.h** - C++ version header with macros

**Usage:** `python create_version.py <project_root>`

---

### `create_cmake.py`
Creates CMake build configuration:
- **CMakeLists.txt** - Main build configuration
  - JUCE plugin setup
  - Version management from VERSION.txt
  - VST3 and Standalone formats
  - Test framework integration (Catch2)
  - Cross-platform compiler settings
- **CMAKE/SOURCES.cmake** - Source file list
- **CMAKE/TESTS.cmake** - Test file list

**Usage:** `python create_cmake.py <project_root> <project_name>`

---

### `create_test_utils.py`
Creates test framework files:
- **TESTS/TEST_UTILS/TestUtils.h/cpp** - Test utilities
  - Sine wave buffer generator
  - Silence detection
  - RMS calculation
- **TESTS/test_Processor.cpp** - Basic processor tests
  - Plugin properties
  - Prepare/release resources
  - Audio processing
  - State save/restore

**Usage:** `python create_test_utils.py <project_root> <project_name>`

---

### `copy_scripts.py`
Copies build scripts from the SCRIPTS directory:
- rebuild_all.py - Clean rebuild
- build_vst3.py - VST3 build
- build_app.py - Standalone app build
- build_tests.py - Test build
- build_au.py - Audio Unit build (macOS)
- build_complete.py - Build utilities
- update_version.py - Version management
- add_test_tag.py - Test tagging utility

**Usage:** `python copy_scripts.py <scripts_source_dir> <project_root>`

---

## Project Name Requirements

The project name (derived from the directory name) must:
- Contain only alphanumeric characters, underscores, and hyphens
- Not be empty
- Will be used for:
  - C++ class names (e.g., `AudioFileChangerProcessor`)
  - CMake project name
  - Plugin target names
  - Bundle identifiers

---

## What Gets Created

After running `setup_project.py C:\REPOS\PLUGIN_PROJECTS\MyPlugin`, you'll have:

```
MyPlugin/
├── SOURCE/
│   ├── PluginProcessor.h
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h
│   ├── PluginEditor.cpp
│   └── Util/
│       ├── Juce_Header.h
│       └── Version.h
├── CMAKE/
│   ├── SOURCES.cmake
│   └── TESTS.cmake
├── SCRIPTS/
│   ├── rebuild_all.py
│   ├── build_vst3.py
│   ├── build_app.py
│   ├── build_tests.py
│   ├── build_au.py
│   ├── build_complete.py
│   ├── update_version.py
│   └── add_test_tag.py
├── TESTS/
│   ├── TEST_UTILS/
│   │   ├── TestUtils.h
│   │   └── TestUtils.cpp
│   └── test_Processor.cpp
├── SUBMODULES/
├── BUILD/
│   └── .gitkeep
├── NOTES/
├── DIAGRAMS/
├── CMakeLists.txt
├── VERSION.txt
├── .gitignore
└── README.md
```

---

## Next Steps After Setup

1. **Initialize Git**
   ```bash
   cd MyPlugin
   git init
   ```

2. **Add JUCE Submodule**
   ```bash
   git submodule add https://github.com/juce-framework/JUCE.git SUBMODULES/JUCE
   git submodule update --init --recursive
   ```

3. **Customize CMakeLists.txt**
   - Update `COMPANY_NAME`
   - Update `BUNDLE_ID`
   - Update `PLUGIN_MANUFACTURER_CODE` (4-char code)
   - Update `PLUGIN_CODE` (unique 4-char code)

4. **Build the Project**
   ```bash
   python SCRIPTS/rebuild_all.py
   ```

5. **Run Tests**
   ```bash
   python SCRIPTS/build_tests.py
   cd BUILD
   ctest
   ```

---

## Customization

### Adding Parameters
Edit `PluginProcessor.cpp` in the `_createParameterLayout()` function.

### Modifying UI
Edit `PluginEditor.cpp` to add/remove UI components.

### Adding Source Files
1. Create your .h/.cpp files in SOURCE/
2. Add them to CMAKE/SOURCES.cmake
3. Rebuild

### Adding Tests
1. Create test files in TESTS/
2. Add them to CMAKE/TESTS.cmake
3. Run `python SCRIPTS/build_tests.py`

---

## Template Variables

These are automatically replaced during setup:

| Variable | Example | Source |
|----------|---------|--------|
| `{PROJECT_NAME}` | AudioFileChanger | Directory name |
| `{PROJECT_NAME_LOWER}` | audiofilechanger | Lowercase directory name |
| `{PLUGIN_CODE}` | Audi | First 4 chars of project name |

---

## Dependencies

- Python 3.7+
- CMake 3.24.1+
- C++20 compatible compiler
- JUCE framework (added as submodule)
- Catch2 (automatically fetched by CMake for tests)
