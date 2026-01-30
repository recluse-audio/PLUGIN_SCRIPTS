#!/usr/bin/env python3
"""
Creates basic test utility files for a JUCE plugin project.
"""

from pathlib import Path


TEST_UTILS_H_TEMPLATE = """#pragma once

#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>

#include "../../SOURCE/Util/Juce_Header.h"

/**
 * Test utilities for JUCE plugin testing.
 */

namespace TestUtils {{

/**
 * Creates a simple test audio buffer with a sine wave.
 *
 * @param numChannels Number of audio channels
 * @param numSamples Number of samples
 * @param frequency Frequency of the sine wave in Hz
 * @param sampleRate Sample rate in Hz
 * @return Audio buffer containing the sine wave
 */
juce::AudioBuffer<float> createSineBuffer(
    int numChannels,
    int numSamples,
    float frequency,
    double sampleRate);

/**
 * Checks if an audio buffer is silent (all samples near zero).
 *
 * @param buffer Audio buffer to check
 * @param threshold Maximum absolute value to consider silent
 * @return true if buffer is silent, false otherwise
 */
bool isSilent(const juce::AudioBuffer<float>& buffer, float threshold = 0.0001f);

/**
 * Calculates RMS level of an audio buffer.
 *
 * @param buffer Audio buffer
 * @param channel Channel to analyze
 * @return RMS level
 */
float calculateRMS(const juce::AudioBuffer<float>& buffer, int channel = 0);

}} // namespace TestUtils
"""


TEST_UTILS_CPP_TEMPLATE = """#include "TestUtils.h"
#include <cmath>

namespace TestUtils {{

juce::AudioBuffer<float> createSineBuffer(
    int numChannels,
    int numSamples,
    float frequency,
    double sampleRate)
{{
    juce::AudioBuffer<float> buffer(numChannels, numSamples);

    const float angleDelta = frequency * 2.0f * juce::MathConstants<float>::pi / static_cast<float>(sampleRate);
    float angle = 0.0f;

    for (int sample = 0; sample < numSamples; ++sample)
    {{
        const float value = std::sin(angle);

        for (int channel = 0; channel < numChannels; ++channel)
        {{
            buffer.setSample(channel, sample, value);
        }}

        angle += angleDelta;
    }}

    return buffer;
}}

bool isSilent(const juce::AudioBuffer<float>& buffer, float threshold)
{{
    for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
    {{
        const float* data = buffer.getReadPointer(channel);

        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
        {{
            if (std::abs(data[sample]) > threshold)
                return false;
        }}
    }}

    return true;
}}

float calculateRMS(const juce::AudioBuffer<float>& buffer, int channel)
{{
    if (channel >= buffer.getNumChannels())
        return 0.0f;

    const float* data = buffer.getReadPointer(channel);
    const int numSamples = buffer.getNumSamples();

    float sum = 0.0f;
    for (int i = 0; i < numSamples; ++i)
    {{
        sum += data[i] * data[i];
    }}

    return std::sqrt(sum / static_cast<float>(numSamples));
}}

}} // namespace TestUtils
"""


TEST_PROCESSOR_TEMPLATE = """#include "../TEST_UTILS/TestUtils.h"
#include "../../SOURCE/PluginProcessor.h"

TEST_CASE("{PROJECT_NAME}Processor basic functionality", "[{PROJECT_NAME}][processor]")
{{
    {PROJECT_NAME}Processor processor;

    SECTION("Plugin has correct properties")
    {{
        REQUIRE(processor.getName() == JucePlugin_Name);
        REQUIRE(processor.hasEditor() == true);
        REQUIRE(processor.getTailLengthSeconds() >= 0.0);
    }}

    SECTION("Plugin can be prepared for playback")
    {{
        const double sampleRate = 44100.0;
        const int samplesPerBlock = 512;

        REQUIRE_NOTHROW(processor.prepareToPlay(sampleRate, samplesPerBlock));
        REQUIRE_NOTHROW(processor.releaseResources());
    }}

    SECTION("Plugin can process audio")
    {{
        const double sampleRate = 44100.0;
        const int samplesPerBlock = 512;

        processor.prepareToPlay(sampleRate, samplesPerBlock);

        juce::AudioBuffer<float> buffer(2, samplesPerBlock);
        buffer.clear();

        juce::MidiBuffer midiBuffer;

        REQUIRE_NOTHROW(processor.processBlock(buffer, midiBuffer));

        processor.releaseResources();
    }}

    SECTION("Parameter state can be saved and restored")
    {{
        juce::MemoryBlock stateData;

        REQUIRE_NOTHROW(processor.getStateInformation(stateData));
        REQUIRE(stateData.getSize() > 0);

        REQUIRE_NOTHROW(processor.setStateInformation(stateData.getData(),
                                                      static_cast<int>(stateData.getSize())));
    }}
}}
"""


def create_test_utils(project_root: Path, project_name: str) -> None:
    """
    Create test utility files and a basic processor test.

    Args:
        project_root: Path to the project root directory
        project_name: Name of the project
    """
    test_utils_dir = project_root / "TESTS" / "TEST_UTILS"

    # Create TestUtils.h
    test_utils_h = test_utils_dir / "TestUtils.h"
    test_utils_h.write_text(TEST_UTILS_H_TEMPLATE, encoding='utf-8')
    print(f"  Created TESTS/TEST_UTILS/TestUtils.h")

    # Create TestUtils.cpp
    test_utils_cpp = test_utils_dir / "TestUtils.cpp"
    test_utils_cpp.write_text(TEST_UTILS_CPP_TEMPLATE, encoding='utf-8')
    print(f"  Created TESTS/TEST_UTILS/TestUtils.cpp")

    # Create a basic processor test
    test_processor = project_root / "TESTS" / "test_Processor.cpp"
    test_processor.write_text(TEST_PROCESSOR_TEMPLATE.format(PROJECT_NAME=project_name), encoding='utf-8')
    print(f"  Created TESTS/test_Processor.cpp")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_test_utils.py <project_root> <project_name>")
        sys.exit(1)

    root = Path(sys.argv[1])
    name = sys.argv[2]
    create_test_utils(root, name)
