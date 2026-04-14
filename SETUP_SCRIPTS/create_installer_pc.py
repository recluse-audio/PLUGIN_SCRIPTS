#!/usr/bin/env python3
"""
Generates an Inno Setup script (.iss) for a JUCE plugin project.

Places the script at INSTALLERS/PC/<PluginName>.iss.
The plugin name is derived from the repo directory name.
The version is read from VERSION.txt.
The AppId GUID is derived deterministically from the plugin name.
"""

import uuid
from pathlib import Path


ISS_TEMPLATE = """\
#define MyAppName "{plugin_name}"
#define MyAppVersion "{version}"
#define MyAppPublisher "recluse-audio"
#define MyAppURL "https://recluse-audio.com"
#define VST3Source "{vst3_source}"
#define OutputDir "{output_dir}"

[Setup]
AppId={{{app_id}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
DefaultDirName={{commoncf}}\\VST3
DefaultGroupName={{#MyAppName}}
DisableDirPage=yes
OutputDir={{#OutputDir}}
OutputBaseFilename={{#MyAppName}}_v{{#MyAppVersion}}_Windows_Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{{#VST3Source}}\\*"; DestDir: "{{commoncf}}\\VST3\\{{#MyAppName}}.vst3"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
"""


def read_version(project_root: Path) -> str:
    version_file = project_root / "VERSION.txt"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.1"


def make_app_id(plugin_name: str) -> str:
    """Generate a stable GUID from the plugin name."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"recluse-audio.{plugin_name}")).upper()


def create_installer_pc(project_root: Path) -> None:
    plugin_name = project_root.name
    version = read_version(project_root)
    app_id = make_app_id(plugin_name)

    vst3_source = (
        str(project_root / "BUILD" / f"{plugin_name}_artefacts" / "Release" / "VST3" / f"{plugin_name}.vst3")
        .replace("/", "\\")
    )
    output_dir = r"C:\STORAGE\INSTALLERS"

    iss_content = ISS_TEMPLATE.format(
        plugin_name=plugin_name,
        version=version,
        app_id=app_id,
        vst3_source=vst3_source,
        output_dir=output_dir,
    )

    out_path = project_root / "INSTALLERS" / "PC" / f"{plugin_name}.iss"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(iss_content, encoding="utf-8")
    print(f"  Created INSTALLERS/PC/{plugin_name}.iss")
    print(f"  AppId: {{{app_id}}}")
    print(f"  VST3Source: {vst3_source}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_installer_pc.py <project_root>")
        sys.exit(1)

    root = Path(sys.argv[1])
    create_installer_pc(root)
