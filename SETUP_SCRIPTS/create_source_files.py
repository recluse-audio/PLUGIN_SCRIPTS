#!/usr/bin/env python3
"""
Creates PluginProcessor and PluginEditor source files for a JUCE plugin.
"""

from pathlib import Path


PLUGIN_PROCESSOR_H_TEMPLATE = """#pragma once

#include "Util/Juce_Header.h"

class {PROJECT_NAME}Processor : public juce::AudioProcessor
                               , public juce::AudioProcessorValueTreeState::Listener
{{
public:
    {PROJECT_NAME}Processor();
    ~{PROJECT_NAME}Processor() override;

    //==============================================================================
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

    bool isBusesLayoutSupported(const BusesLayout& layouts) const override;

    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int index) override;
    const juce::String getProgramName(int index) override;
    void changeProgramName(int index, const juce::String& newName) override;

    //==============================================================================
    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;

    //==============================================================================
    juce::AudioProcessorValueTreeState& getAPVTS() {{ return apvts; }}

    // Parameter listener callback
    void parameterChanged(const juce::String& parameterID, float newValue) override;

private:
    //==============================================================================
    juce::AudioProcessorValueTreeState apvts;

    juce::AudioProcessorValueTreeState::ParameterLayout _createParameterLayout();
    void _initParameterListeners();
    juce::AudioProcessor::BusesProperties _getBusesProperties();

    //==============================================================================
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR({PROJECT_NAME}Processor)
}};
"""


PLUGIN_PROCESSOR_CPP_TEMPLATE = """#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
{PROJECT_NAME}Processor::{PROJECT_NAME}Processor()
    : AudioProcessor(_getBusesProperties())
    , apvts(*this, nullptr, "Parameters", _createParameterLayout())
{{
    _initParameterListeners();
}}

{PROJECT_NAME}Processor::~{PROJECT_NAME}Processor()
{{
}}

//==============================================================================
const juce::String {PROJECT_NAME}Processor::getName() const
{{
    return JucePlugin_Name;
}}

bool {PROJECT_NAME}Processor::acceptsMidi() const
{{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}}

bool {PROJECT_NAME}Processor::producesMidi() const
{{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}}

bool {PROJECT_NAME}Processor::isMidiEffect() const
{{
   #if JucePlugin_IsMidiEffect
    return true;
   #else
    return false;
   #endif
}}

double {PROJECT_NAME}Processor::getTailLengthSeconds() const
{{
    return 0.0;
}}

int {PROJECT_NAME}Processor::getNumPrograms()
{{
    return 1;
}}

int {PROJECT_NAME}Processor::getCurrentProgram()
{{
    return 0;
}}

void {PROJECT_NAME}Processor::setCurrentProgram(int index)
{{
    juce::ignoreUnused(index);
}}

const juce::String {PROJECT_NAME}Processor::getProgramName(int index)
{{
    juce::ignoreUnused(index);
    return {{}};
}}

void {PROJECT_NAME}Processor::changeProgramName(int index, const juce::String& newName)
{{
    juce::ignoreUnused(index, newName);
}}

//==============================================================================
void {PROJECT_NAME}Processor::prepareToPlay(double sampleRate, int samplesPerBlock)
{{
    juce::ignoreUnused(sampleRate, samplesPerBlock);
    // Initialize your audio processing components here
}}

void {PROJECT_NAME}Processor::releaseResources()
{{
    // Release any resources when playback stops
}}

bool {PROJECT_NAME}Processor::isBusesLayoutSupported(const BusesLayout& layouts) const
{{
    // Only support stereo for now
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    if (layouts.getMainInputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    return true;
}}

void {PROJECT_NAME}Processor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{{
    juce::ignoreUnused(midiMessages);
    juce::ScopedNoDenormals noDenormals;

    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();

    // Clear any output channels that don't contain input data
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear(i, 0, buffer.getNumSamples());

    // Your audio processing code here
}}

//==============================================================================
bool {PROJECT_NAME}Processor::hasEditor() const
{{
    return true;
}}

juce::AudioProcessorEditor* {PROJECT_NAME}Processor::createEditor()
{{
    return new {PROJECT_NAME}Editor(*this);
}}

//==============================================================================
void {PROJECT_NAME}Processor::getStateInformation(juce::MemoryBlock& destData)
{{
    // Save parameters to XML
    auto state = apvts.copyState();
    std::unique_ptr<juce::XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}}

void {PROJECT_NAME}Processor::setStateInformation(const void* data, int sizeInBytes)
{{
    // Restore parameters from XML
    std::unique_ptr<juce::XmlElement> xmlState(getXmlFromBinary(data, sizeInBytes));

    if (xmlState.get() != nullptr)
        if (xmlState->hasTagName(apvts.state.getType()))
            apvts.replaceState(juce::ValueTree::fromXml(*xmlState));
}}

//==============================================================================
void {PROJECT_NAME}Processor::parameterChanged(const juce::String& parameterID, float newValue)
{{
    juce::ignoreUnused(parameterID, newValue);
    // Handle parameter changes here
}}

//==============================================================================
juce::AudioProcessorValueTreeState::ParameterLayout {PROJECT_NAME}Processor::_createParameterLayout()
{{
    juce::AudioProcessorValueTreeState::ParameterLayout layout;

    // Example parameter - add your own here
    layout.add(std::make_unique<juce::AudioParameterFloat>(
        "gain",           // Parameter ID
        "Gain",           // Parameter name
        juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f),
        0.5f));           // Default value

    return layout;
}}

void {PROJECT_NAME}Processor::_initParameterListeners()
{{
    // Register parameter listeners
    apvts.addParameterListener("gain", this);
}}

juce::AudioProcessor::BusesProperties {PROJECT_NAME}Processor::_getBusesProperties()
{{
    return BusesProperties()
        .withInput("Input", juce::AudioChannelSet::stereo(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true);
}}

//==============================================================================
// This creates new instances of the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{{
    return new {PROJECT_NAME}Processor();
}}
"""


PLUGIN_EDITOR_H_TEMPLATE = """#pragma once

#include "PluginProcessor.h"

class {PROJECT_NAME}Editor : public juce::AudioProcessorEditor
                            , public juce::Timer
{{
public:
    explicit {PROJECT_NAME}Editor({PROJECT_NAME}Processor&);
    ~{PROJECT_NAME}Editor() override;

    //==============================================================================
    void paint(juce::Graphics&) override;
    void resized() override;

    // Timer callback for updating the UI
    void timerCallback() override;

private:
    {PROJECT_NAME}Processor& mProcessor;

    // UI Components
    std::unique_ptr<juce::Label> mVersionLabel;
    std::unique_ptr<juce::Slider> mGainSlider;
    std::unique_ptr<juce::Label> mGainLabel;

    // Parameter attachments
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> mGainAttachment;

    //==============================================================================
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR({PROJECT_NAME}Editor)
}};
"""


PLUGIN_EDITOR_CPP_TEMPLATE = """#include "PluginEditor.h"
#include "Util/Version.h"

//==============================================================================
{PROJECT_NAME}Editor::{PROJECT_NAME}Editor({PROJECT_NAME}Processor& p)
    : AudioProcessorEditor(&p)
    , mProcessor(p)
{{
    // Version label
    mVersionLabel = std::make_unique<juce::Label>("version", "v" BUILD_VERSION_STRING);
    mVersionLabel->setFont(juce::Font(10.0f));
    addAndMakeVisible(mVersionLabel.get());

    // Gain slider
    mGainSlider = std::make_unique<juce::Slider>(juce::Slider::Rotary, juce::Slider::TextBoxBelow);
    mGainSlider->setTextValueSuffix("");
    addAndMakeVisible(mGainSlider.get());

    // Gain label
    mGainLabel = std::make_unique<juce::Label>("gain_label", "Gain");
    mGainLabel->setJustificationType(juce::Justification::centred);
    addAndMakeVisible(mGainLabel.get());

    // Attach slider to parameter
    mGainAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        mProcessor.getAPVTS(), "gain", *mGainSlider);

    // Start timer for UI updates (30 Hz)
    startTimerHz(30);

    // Set window size
    setSize(400, 300);
}}

{PROJECT_NAME}Editor::~{PROJECT_NAME}Editor()
{{
    stopTimer();
}}

//==============================================================================
void {PROJECT_NAME}Editor::paint(juce::Graphics& g)
{{
    // Background
    g.fillAll(juce::Colour(0xff202020));

    // Title
    g.setColour(juce::Colours::white);
    g.setFont(juce::Font(24.0f, juce::Font::bold));
    g.drawText("{PROJECT_NAME}", getLocalBounds().removeFromTop(60), juce::Justification::centred);
}}

void {PROJECT_NAME}Editor::resized()
{{
    auto bounds = getLocalBounds();

    // Version label in bottom left
    mVersionLabel->setBounds(10, getHeight() - 20, 100, 12);

    // Center gain control
    auto centerArea = bounds.reduced(50);
    mGainLabel->setBounds(centerArea.removeFromTop(30));
    mGainSlider->setBounds(centerArea.removeFromTop(100).withSizeKeepingCentre(100, 100));
}}

void {PROJECT_NAME}Editor::timerCallback()
{{
    // Update UI elements that need periodic refresh
}}
"""


JUCE_HEADER_TEMPLATE = """
/*

	A bunch on includes from the JuceHeader.h to make it available and actually work with Catch2
 */
#pragma once

#include <juce_audio_utils/juce_audio_utils.h>
#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_gui_extra/juce_gui_extra.h>
#include <juce_gui_basics/juce_gui_basics.h>
#include <juce_graphics/juce_graphics.h>
#include <juce_events/juce_events.h>
#include <juce_core/juce_core.h>
#include <juce_data_structures/juce_data_structures.h>
#include <juce_audio_basics/juce_audio_basics.h>
#include <juce_audio_formats/juce_audio_formats.h>
#include <juce_audio_devices/juce_audio_devices.h>
#include <juce_opengl/juce_opengl.h>
#include <juce_audio_plugin_client/juce_audio_plugin_client.h>
#include <juce_dsp/juce_dsp.h>
"""


def create_source_files(project_root: Path, project_name: str) -> None:
    """
    Create PluginProcessor and PluginEditor source files.

    Args:
        project_root: Path to the project root directory
        project_name: Name of the project (used for class names)
    """
    source_dir = project_root / "SOURCE"
    util_dir = source_dir / "Util"

    # Create PluginProcessor.h
    processor_h = source_dir / "PluginProcessor.h"
    processor_h.write_text(PLUGIN_PROCESSOR_H_TEMPLATE.format(PROJECT_NAME=project_name), encoding='utf-8')
    print(f"  Created SOURCE/PluginProcessor.h")

    # Create PluginProcessor.cpp
    processor_cpp = source_dir / "PluginProcessor.cpp"
    processor_cpp.write_text(PLUGIN_PROCESSOR_CPP_TEMPLATE.format(PROJECT_NAME=project_name), encoding='utf-8')
    print(f"  Created SOURCE/PluginProcessor.cpp")

    # Create PluginEditor.h
    editor_h = source_dir / "PluginEditor.h"
    editor_h.write_text(PLUGIN_EDITOR_H_TEMPLATE.format(PROJECT_NAME=project_name), encoding='utf-8')
    print(f"  Created SOURCE/PluginEditor.h")

    # Create PluginEditor.cpp
    editor_cpp = source_dir / "PluginEditor.cpp"
    editor_cpp.write_text(PLUGIN_EDITOR_CPP_TEMPLATE.format(PROJECT_NAME=project_name), encoding='utf-8')
    print(f"  Created SOURCE/PluginEditor.cpp")

    # Create Juce_Header.h
    juce_header = util_dir / "Juce_Header.h"
    juce_header.write_text(JUCE_HEADER_TEMPLATE, encoding='utf-8')
    print(f"  Created SOURCE/Util/Juce_Header.h")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_source_files.py <project_root> <project_name>")
        sys.exit(1)

    root = Path(sys.argv[1])
    name = sys.argv[2]
    create_source_files(root, name)
