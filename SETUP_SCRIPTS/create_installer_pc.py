#!/usr/bin/env python3
"""
Generates an Inno Setup script (.iss) for a JUCE plugin project.

Places the script at INSTALLERS/PC/<ProductName>.iss.
The plugin/product name and CMake target are parsed from CMakeLists.txt.
The version is read from VERSION.txt.
The AppId GUID is derived deterministically from the product name.
"""

import re
import uuid
from pathlib import Path


ISS_TEMPLATE = """\
#define MyAppName "{product_name}"
#define MyAppVersion "{version}"
#define MyAppPublisher "recluse-audio"
#define MyAppURL "https://recluse-audio.com"
#define VST3Source SourcePath + "\\..\\..\\BUILD\\{target}_artefacts\\Release\\VST3\\{product_name}.vst3"
#define OutputDir SourcePath + "\\BUILD"

[Setup]
AppId={{{app_id}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppPublisher}}\\{{#MyAppName}}
UninstallFilesDir={{app}}
DefaultGroupName={{#MyAppName}}
DisableDirPage=yes
DisableProgramGroupPage=yes
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


def get_plugin_names(project_root: Path) -> tuple[str, str]:
    """
    Parse CMakeLists.txt for the CMake target name and PRODUCT_NAME.

    Returns (target, product_name). Falls back to directory name if
    CMakeLists.txt doesn't exist or can't be parsed.
    """
    cmake_file = project_root / "CMakeLists.txt"
    fallback = project_root.name

    if not cmake_file.exists():
        return fallback, fallback

    text = cmake_file.read_text(encoding="utf-8")

    m = re.search(r'project\(\s*(\S+)', text)
    target = m.group(1) if m else fallback

    m = re.search(r'PRODUCT_NAME\s+"([^"]+)"', text)
    product_name = m.group(1) if m else target

    return target, product_name


def make_app_id(product_name: str) -> str:
    """Generate a stable GUID from the product name."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"recluse-audio.{product_name}")).upper()


def create_installer_pc(project_root: Path) -> None:
    target, product_name = get_plugin_names(project_root)
    version = read_version(project_root)
    app_id = make_app_id(product_name)

    iss_content = ISS_TEMPLATE.format(
        product_name=product_name,
        target=target,
        version=version,
        app_id=app_id,
    )

    out_path = project_root / "INSTALLERS" / "PC" / f"{product_name}.iss"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(iss_content, encoding="utf-8")
    print(f"  Created INSTALLERS/PC/{product_name}.iss")
    print(f"  Target: {target}, Product: {product_name}")
    print(f"  AppId: {{{app_id}}}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_installer_pc.py <project_root>")
        sys.exit(1)

    root = Path(sys.argv[1])
    create_installer_pc(root)
