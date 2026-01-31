#!/usr/bin/env python3
"""
Creates CMake configuration files for a JUCE plugin project.
"""

from pathlib import Path


CMAKELISTS_TEMPLATE = """cmake_minimum_required(VERSION 3.24.1)

# Read version from VERSION.txt
file(STRINGS "${{CMAKE_CURRENT_SOURCE_DIR}}/VERSION.txt" VERSION_STRING)
string(STRIP "${{VERSION_STRING}}" VERSION_STRING)

# Parse version components
string(REPLACE "." ";" VERSION_LIST ${{VERSION_STRING}})
list(GET VERSION_LIST 0 PROJECT_VERSION_MAJOR)
list(GET VERSION_LIST 1 PROJECT_VERSION_MINOR)
list(GET VERSION_LIST 2 PROJECT_VERSION_PATCH)

# Project definition
project({PROJECT_NAME} VERSION ${{VERSION_STRING}} LANGUAGES CXX)

# C++ Standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Export compile commands for IDE integration
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# JUCE setup
add_subdirectory(SUBMODULES/JUCE)

# Plugin formats to build
set(FORMATS VST3 Standalone)

# Create version header before building
add_custom_target(update_version_header
    COMMAND python "${{CMAKE_CURRENT_SOURCE_DIR}}/HELPER_SCRIPTS/update_version.py"
            "${{CMAKE_CURRENT_SOURCE_DIR}}/VERSION.txt"
            "${{CMAKE_CURRENT_SOURCE_DIR}}/SOURCE/Util/Version.h"
    BYPRODUCTS "${{CMAKE_CURRENT_SOURCE_DIR}}/SOURCE/Util/Version.h"
    COMMENT "Updating version header"
)

# Plugin configuration
juce_add_plugin({PROJECT_NAME}
    COMPANY_NAME "YourCompanyName"
    BUNDLE_ID com.yourcompany.{PROJECT_NAME_LOWER}
    PLUGIN_MANUFACTURER_CODE Manu
    PLUGIN_CODE {PLUGIN_CODE}
    FORMATS ${{FORMATS}}
    PRODUCT_NAME "{PROJECT_NAME}"
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD FALSE
    VST3_CATEGORIES Fx
)

# Source files
include(CMAKE/SOURCES.cmake)
target_sources({PROJECT_NAME} PRIVATE ${{SOURCES}})

# Make version header generation a dependency
add_dependencies({PROJECT_NAME} update_version_header)

# Compiler options
target_compile_features({PROJECT_NAME} PRIVATE cxx_std_20)

# Link JUCE modules
target_link_libraries({PROJECT_NAME}
    PRIVATE
        juce::juce_audio_utils
        juce::juce_audio_processors
        juce::juce_dsp
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
)

# Preprocessor definitions
target_compile_definitions({PROJECT_NAME}
    PUBLIC
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_VST3_CAN_REPLACE_VST2=0
        JUCE_DISPLAY_SPLASH_SCREEN=1
        JUCE_REPORT_APP_USAGE=0
)

# Platform-specific settings
if(MSVC)
    target_compile_options({PROJECT_NAME} PRIVATE /W4)
else()
    target_compile_options({PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)
endif()

#==============================================================================
# Tests (optional)
#==============================================================================
option(BUILD_TESTS "Build unit tests" OFF)

if(BUILD_TESTS OR TARGET Tests)
    include(FetchContent)

    # Fetch Catch2
    FetchContent_Declare(
        Catch2
        GIT_REPOSITORY https://github.com/catchorg/Catch2.git
        GIT_TAG v3.1.0
    )
    FetchContent_MakeAvailable(Catch2)

    # Test executable
    add_executable(Tests)
    include(CMAKE/TESTS.cmake)
    include(CMAKE/SOURCES.cmake)
    target_sources(Tests PRIVATE ${{TEST_SOURCES}} ${{SOURCES}})

    target_include_directories(Tests PRIVATE ${{CMAKE_CURRENT_SOURCE_DIR}})

    target_link_libraries(Tests PRIVATE
        Catch2::Catch2WithMain
        juce::juce_audio_utils
        juce::juce_audio_processors
        juce::juce_dsp
    )

    target_compile_features(Tests PRIVATE cxx_std_20)

    # Define JUCE plugin macros for Tests target
    target_compile_definitions(Tests PRIVATE
        JucePlugin_Name="{PROJECT_NAME}"
        JucePlugin_WantsMidiInput=0
        JucePlugin_ProducesMidiOutput=0
        JucePlugin_IsMidiEffect=0
    )

    # Enable CTest
    include(CTest)
    include(Catch)
    catch_discover_tests(Tests)
endif()
"""


SOURCES_CMAKE_TEMPLATE = """# List all source files for the plugin

set(SOURCES
    # Core plugin files
    SOURCE/PluginProcessor.h
    SOURCE/PluginProcessor.cpp
    SOURCE/PluginEditor.h
    SOURCE/PluginEditor.cpp

    # Utility files
    SOURCE/Util/Juce_Header.h
    SOURCE/Util/Version.h

    # Add your additional source files here
    # SOURCE/MyComponent.h
    # SOURCE/MyComponent.cpp
)
"""


TESTS_CMAKE_TEMPLATE = """# List all test source files

set(TEST_SOURCES
    # Test utilities
    TESTS/TEST_UTILS/TestUtils.h
    TESTS/TEST_UTILS/TestUtils.cpp

    # Test files
    # TESTS/test_PluginProcessor.cpp

    # Add your test files here
)
"""


def create_cmake_files(project_root: Path, project_name: str) -> None:
    """
    Create CMake configuration files.

    Args:
        project_root: Path to the project root directory
        project_name: Name of the project
    """
    # Generate a simple 4-character plugin code from project name
    plugin_code = (project_name[:4].ljust(4, 'X')).upper()

    # Create CMakeLists.txt
    cmakelists = project_root / "CMakeLists.txt"
    cmakelists.write_text(CMAKELISTS_TEMPLATE.format(
        PROJECT_NAME=project_name,
        PROJECT_NAME_LOWER=project_name.lower(),
        PLUGIN_CODE=plugin_code
    ), encoding='utf-8')
    print(f"  Created CMakeLists.txt")

    # Create CMAKE/SOURCES.cmake
    sources_cmake = project_root / "CMAKE" / "SOURCES.cmake"
    sources_cmake.write_text(SOURCES_CMAKE_TEMPLATE, encoding='utf-8')
    print(f"  Created CMAKE/SOURCES.cmake")

    # Create CMAKE/TESTS.cmake
    tests_cmake = project_root / "CMAKE" / "TESTS.cmake"
    tests_cmake.write_text(TESTS_CMAKE_TEMPLATE, encoding='utf-8')
    print(f"  Created CMAKE/TESTS.cmake")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_cmake.py <project_root> <project_name>")
        sys.exit(1)

    root = Path(sys.argv[1])
    name = sys.argv[2]
    create_cmake_files(root, name)
