# Quick Start Guide

Get from zero to a working JUCE plugin.

## Prerequisites

Install these first:
- Python 3.7+ ([python.org](https://python.org))
- CMake 3.24+ ([cmake.org](https://cmake.org))
- Git ([git-scm.com](https://git-scm.com))
- C++ Compiler (MSVC 2022, GCC 10+, or Clang 12+)

## Three Commands

```bash
# 1. Generate project
python setup_project.py ~/MyPlugin

# 2. Initialize git and JUCE
cd ~/MyPlugin
python SCRIPTS/init_project.py

# 3. Build
python SCRIPTS/rebuild_all.py
```

Done! Your plugin is in `BUILD/MyPlugin_artefacts/`

## What You Get

- Working VST3 and Standalone plugin
- Example gain parameter with UI slider
- Version management (VERSION.txt)
- Test framework ready to use
- Cross-platform CMake setup

## Next Steps

### Add a Parameter

Edit `SOURCE/PluginProcessor.cpp`, find `_createParameterLayout()`:

```cpp
layout.add(std::make_unique<juce::AudioParameterFloat>(
    "cutoff",      // Parameter ID
    "Cutoff",      // Display name
    juce::NormalisableRange<float>(20.0f, 20000.0f, 1.0f),
    1000.0f));     // Default value
```

Rebuild: `python SCRIPTS/rebuild_all.py`

### Add UI for the Parameter

Edit `SOURCE/PluginEditor.cpp`, add to constructor:

```cpp
mCutoffSlider = std::make_unique<juce::Slider>(
    juce::Slider::Rotary,
    juce::Slider::TextBoxBelow);
addAndMakeVisible(mCutoffSlider.get());

mCutoffAttachment = std::make_unique<AudioProcessorValueTreeState::SliderAttachment>(
    mProcessor.getAPVTS(), "cutoff", *mCutoffSlider);
```

### Write a Test

Create `TESTS/test_MyFeature.cpp`:

```cpp
#include "../TEST_UTILS/TestUtils.h"
#include "../SOURCE/PluginProcessor.h"

TEST_CASE("My feature works", "[MyFeature]")
{
    MyPluginProcessor processor;
    processor.prepareToPlay(44100.0, 512);

    // Your test code here
    REQUIRE(true);
}
```

Add to `CMAKE/TESTS.cmake`:
```cmake
set(TEST_SOURCES
    # ... existing files ...
    TESTS/test_MyFeature.cpp
)
```

Run: `python SCRIPTS/build_tests.py && cd BUILD && ctest`

## Common Commands

```bash
# Build specific target
python SCRIPTS/build_vst3.py     # VST3 only
python SCRIPTS/build_app.py      # Standalone only

# Release build
python SCRIPTS/rebuild_all.py --config Release

# Bump version
python SCRIPTS/update_version.py VERSION.txt SOURCE/Util/Version.h
```

## File Organization

Put your code in:
- `SOURCE/` - All .h/.cpp files
- `SOURCE/Util/` - Utility headers
- `TESTS/` - Test files

Update these after adding files:
- `CMAKE/SOURCES.cmake` - List of source files
- `CMAKE/TESTS.cmake` - List of test files

## Platform Differences

**Windows:**
- Uses Visual Studio (multi-config)
- Plugins: `BUILD/Debug/VST3/` or `BUILD/Release/VST3/`

**macOS:**
- Uses Xcode or Makefiles
- Plugins: `BUILD/Debug/VST3/` (Xcode) or `BUILD/VST3/` (Makefiles)
- AU available (change FORMATS in CMakeLists.txt)

**Linux:**
- Uses Makefiles or Ninja
- Plugins: `BUILD/VST3/`
- May need JUCE dependencies: `sudo apt install libasound2-dev libx11-dev ...`

## Troubleshooting

**"CMake can't find JUCE"**
```bash
python SCRIPTS/init_project.py
```

**"Include file not found"**
- Check `SOURCE/Util/Juce_Header.h` has the modules you need
- Check `CMakeLists.txt` links those modules

**"Tests won't build"**
- Check internet connection (Catch2 downloads automatically)
- Or manually clone Catch2 to `BUILD/_deps/`

**"Plugin doesn't load in DAW"**
- Make sure it built successfully
- Check plugin format matches DAW (VST3/AU)
- Check architecture matches (x64 vs ARM)

## Help & Resources

- JUCE Docs: [docs.juce.com](https://docs.juce.com)
- JUCE Forum: [forum.juce.com](https://forum.juce.com)
- CMake Docs: [cmake.org/documentation](https://cmake.org/documentation)
- This generator: [Open an issue!](issues)
