# Message From A Human 
Hello, I am writting you with intentoinal typos so you know I'm not wireback!
But seriously, this project is useful to me and I thought you'd use it to0.

JUCE projects - CMake - Catch2 - Claude -

## JUCE Project Helper Scripts.

A streamlined project generator for JUCE audio plugins that eliminates CMake boilerplate and gets you coding faster.

## Why This Exists

Setting up a JUCE plugin project with CMake can be daunting:
- Complex CMakeLists.txt configuration
- Manual directory structure setup
- Boilerplate code for processors and editors
- Test framework integration
- Build script maintenance

This generator handles all of that for you, creating production-ready JUCE projects in seconds.

## What It Generates

A complete JUCE plugin project with:
- Modern CMake configuration (C++20, multi-platform)
- Source files (PluginProcessor, PluginEditor) with APVTS parameter management
- Cross-platform build scripts (Windows/macOS/Linux)
- Catch2 test framework integration
- Version management system
- Proper .gitignore and project structure

## Quick Start

### 1. Download This Repository

```bash
git clone <repository-url> ~/juce-generator
cd ~/juce-generator
```

### 2. Generate Your Plugin Project

```bash
python setup_project.py /path/to/MyAwesomePlugin
```

This creates a complete project structure with the plugin name derived from the directory.

### 3. Initialize Git and Add JUCE

```bash
cd /path/to/MyAwesomePlugin
python SCRIPTS/init_project.py
```

This initializes git and adds JUCE as a submodule (takes 1-2 minutes).

### 4. Build Your Plugin

```bash
python SCRIPTS/rebuild_all.py
```

That's it! You now have a working VST3 and Standalone plugin.

## Requirements

- Python 3.7 or higher (standard library only, no pip installs needed)
- CMake 3.24.1 or higher
- C++20 compatible compiler (MSVC 2022, GCC 10+, Clang 12+)
- Git (for JUCE submodule)

## Generated Project Structure

```
MyAwesomePlugin/
├── SOURCE/
│   ├── PluginProcessor.h/.cpp    # Main audio processor
│   ├── PluginEditor.h/.cpp       # GUI editor
│   └── Util/
│       ├── Juce_Header.h         # Centralized JUCE includes
│       └── Version.h             # Auto-generated version macros
├── CMAKE/
│   ├── SOURCES.cmake             # Source file list
│   └── TESTS.cmake               # Test file list
├── SCRIPTS/
│   ├── init_project.py           # Git/JUCE initialization
│   ├── rebuild_all.py            # Clean rebuild
│   ├── build_vst3.py             # VST3 build
│   ├── build_app.py              # Standalone build
│   ├── build_tests.py            # Test build
│   └── update_version.py         # Version management
├── TESTS/
│   ├── TEST_UTILS/               # Test utilities
│   └── test_Processor.cpp        # Example tests
├── SUBMODULES/
│   └── JUCE/                     # JUCE framework (added by init_project.py)
├── BUILD/                        # Build artifacts (gitignored)
├── NOTES/                        # Development notes
├── DIAGRAMS/                     # Architecture diagrams
├── CMakeLists.txt                # Main CMake configuration
├── VERSION.txt                   # Version number (0.0.1)
├── .gitignore                    # Comprehensive ignore patterns
└── README.md                     # Project documentation
```

## Build Scripts

All scripts automatically detect the plugin name from the current directory.

### `init_project.py`
Initializes git repository and adds JUCE as a submodule. Run this once after generating a new project.

```bash
python SCRIPTS/init_project.py
```

### `rebuild_all.py`
Clean rebuild of all targets. Supports Debug/Release configurations.

```bash
python SCRIPTS/rebuild_all.py
python SCRIPTS/rebuild_all.py --config Release
```

### `build_vst3.py`
Build VST3 plugin only.

```bash
python SCRIPTS/build_vst3.py
```

### `build_app.py`
Build standalone application.

```bash
python SCRIPTS/build_app.py
```

### `build_tests.py`
Build and run Catch2 unit tests.

```bash
python SCRIPTS/build_tests.py
```

### `update_version.py`
Increment patch version and regenerate Version.h.

```bash
python SCRIPTS/update_version.py VERSION.txt SOURCE/Util/Version.h
```

## CMake Features

The generated CMakeLists.txt includes:

- **Automatic version management** from VERSION.txt
- **Multi-format support** (VST3, AU, Standalone - easily configurable)
- **Cross-platform builds** with proper generator detection
- **Test integration** with Catch2 (automatic fetch)
- **JUCE splash screen** enabled by default (JUCE_DISPLAY_SPLASH_SCREEN=1)
- **Optimized compiler flags** for each platform
- **Version header generation** before each build

## Customization

### Adding Parameters

Edit `SOURCE/PluginProcessor.cpp` in `_createParameterLayout()`:

```cpp
layout.add(std::make_unique<juce::AudioParameterFloat>(
    "my_param",
    "My Parameter",
    juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f),
    0.5f));
```

### Adding UI Components

Edit `SOURCE/PluginEditor.cpp` to add sliders, labels, etc. The example includes APVTS parameter binding.

### Adding Source Files

1. Create your .h/.cpp files in `SOURCE/`
2. Add them to `CMAKE/SOURCES.cmake`
3. Run `python SCRIPTS/rebuild_all.py`

### Adding Tests

1. Create test files in `TESTS/`
2. Add them to `CMAKE/TESTS.cmake`
3. Run `python SCRIPTS/build_tests.py`

## Platform-Specific Notes

### Windows (Visual Studio)
- Uses multi-config generators (Debug/Release)
- Build artifacts in `BUILD/Debug` or `BUILD/Release`
- Plugins copied to system plugin folders automatically by JUCE

### macOS (Xcode or Makefile)
- Xcode uses multi-config, Makefiles use single-config
- Use `CMAKE_BUILD_TYPE=Release` for Makefiles
- AU and AUv3 formats available (set in CMakeLists.txt FORMATS variable)

### Linux
- Uses single-config generators (Ninja, Unix Makefiles)
- Requires additional JUCE dependencies (see JUCE docs)

## Example Workflow

```bash
# Generate project
python ~/juce-generator/setup_project.py ~/dev/MyReverb

# Initialize
cd ~/dev/MyReverb
python SCRIPTS/init_project.py

# Customize
# Edit SOURCE/PluginProcessor.cpp to add your DSP
# Edit SOURCE/PluginEditor.cpp to design your UI

# Build and test
python SCRIPTS/rebuild_all.py --config Release
python SCRIPTS/build_tests.py

# Version bump
python SCRIPTS/update_version.py VERSION.txt SOURCE/Util/Version.h
```

## What's Included in Generated Code

### PluginProcessor
- APVTS parameter management
- Example "gain" parameter
- Stereo I/O bus configuration
- State save/load (XML-based)
- Parameter listener callbacks
- Proper JUCE AudioProcessor boilerplate

### PluginEditor
- Timer-based UI updates (30 Hz)
- Version label display
- Example slider with APVTS binding
- 400x300 default window size
- Modern dark theme

### Test Framework
- Catch2 v3.1.0 integration
- Test utilities (sine wave generator, silence detection, RMS calculation)
- Example processor tests
- CTest integration for CI/CD

## Advanced Configuration

### Changing Plugin Formats

Edit `CMakeLists.txt`:

```cmake
set(FORMATS VST3 AU Standalone)  # Add/remove formats
```

### Changing Company Info

Edit `CMakeLists.txt`:

```cmake
juce_add_plugin(MyPlugin
    COMPANY_NAME "YourCompanyName"
    BUNDLE_ID com.yourcompany.myplugin
    PLUGIN_MANUFACTURER_CODE Manu  # 4-char code (at least 1 uppercase)
    PLUGIN_CODE Plug               # Unique 4-char plugin ID
    ...
)
```

### Adding JUCE Modules

Edit `CMakeLists.txt`:

```cmake
target_link_libraries(MyPlugin
    PRIVATE
        juce::juce_audio_utils
        juce::juce_audio_processors
        juce::juce_dsp
        juce::juce_opengl           # Add additional modules
    ...
)
```

Then update `SOURCE/Util/Juce_Header.h` with the corresponding includes.

## Troubleshooting

**CMake can't find JUCE:**
- Run `python SCRIPTS/init_project.py` to add JUCE as a submodule
- Or manually: `git submodule update --init --recursive`

**Build fails with include errors:**
- Check that `SOURCE/Util/Juce_Header.h` includes the JUCE modules you're using
- Verify those modules are linked in `CMakeLists.txt`

**Version header not found:**
- The version header is auto-generated during build
- Run `python SCRIPTS/update_version.py VERSION.txt SOURCE/Util/Version.h` manually if needed

**Tests won't build:**
- Make sure Catch2 is fetched: check `BUILD/_deps/catch2-src/`
- If behind a proxy, CMake's FetchContent may fail - manually clone Catch2

## Generator Script Details

### `setup_project.py`
Main orchestrator that creates the project structure. Located in this repository root.

**Modules it runs:**
- `create_directories.py` - Directory structure
- `create_gitignore.py` - .gitignore file
- `create_readme.py` - Project README.md
- `create_source_files.py` - Processor/Editor boilerplate
- `create_version.py` - VERSION.txt and Version.h
- `create_cmake.py` - CMake configuration
- `create_test_utils.py` - Test framework
- `copy_scripts.py` - Build scripts

All modules are in `SETUP_SCRIPTS/` and can be run independently if needed.

## Contributing

This is a personal tool made public. If you find bugs or have suggestions:
- Open an issue describing the problem
- Include your platform (Windows/macOS/Linux) and CMake/compiler versions
- PRs welcome for bug fixes and improvements

## License

[Add your license here - MIT recommended for generators]

## Credits

Built for the JUCE community to make CMake-based plugin development more accessible.

JUCE is owned by ROLI Ltd. This generator is not affiliated with or endorsed by ROLI.
