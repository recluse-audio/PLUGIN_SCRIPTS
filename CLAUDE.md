# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

Zero-dependency Python generator for JUCE audio plugin projects. Produces CMake + JUCE boilerplate with build, signing, and installer tooling. Targets Python 3.7+ stdlib only.

## Two-Phase Architecture (Do Not Mix)

1. **Generator phase** — lives in this repo:
   - `setup_project.py` — orchestrator
   - `SETUP_SCRIPTS/*.py` — generators called once per new project
2. **Runtime phase** — copied into generated projects by `SETUP_SCRIPTS/copy_scripts.py`:
   - `HELPER_SCRIPTS/*.py` → generated `HELPER_SCRIPTS/`
   - `SIGNED_SCRIPTS/**` → generated `SIGNED/` (preserves subtree, includes `MAC/` and `PC/` subdirs)
   - `INSTALLER_SCRIPTS/**` → generated `INSTALLERS/` (preserves subtree)

Runtime scripts must be self-contained — no imports from `SETUP_SCRIPTS`. Editing `HELPER_SCRIPTS/`, `SIGNED_SCRIPTS/`, or `INSTALLER_SCRIPTS/` affects only NEW projects, not previously generated ones.

Runtime scripts auto-detect plugin name from `Path.cwd().name` or `Path(__file__).resolve().parents[1].name`.

## `regenSource.py` Auto-Discovery

Build scripts call `regenSource.py` before building. Scans:
- **Sources**: top-level `SOURCE/` only. Submodule SOURCE trees are NOT auto-scanned (see `discover_source_folders` in the script). If a submodule needs its sources compiled in, the consuming project must list them explicitly via a hand-maintained CMake file (e.g. `CMAKE/RD_DSP_SOURCES.cmake` in the RD repo) and a wrapper include like `CMAKE/CONSUMER_SOURCES.cmake` that downstream plugins can pull in without being clobbered by regen.
- **Tests**: top-level `TESTS/` plus `SUBMODULES/*/TESTS/TEST_UTILS` (shared test helpers only — not the submodule's own `TEST_CASE` files).

Writes `CMAKE/SOURCES.cmake` and `CMAKE/TESTS.cmake`. Users never hand-edit those two file lists — they get overwritten on every regen. Anything that must survive regen lives in a separately named `.cmake` file.

## Multi-Config vs Single-Config Generators

Build scripts must handle both — see `rebuild_all.py` / `build_vst3.py` for the pattern.

- Multi-config (Windows VS, macOS Xcode): `cmake --build BUILD --config Debug` → `BUILD/Debug/`
- Single-config (Linux Make/Ninja): `cmake -B BUILD -DCMAKE_BUILD_TYPE=Debug` → `BUILD/`

## Repository Layout

```
PLUGIN_SCRIPTS/              # repo root
├── setup_project.py         # main entry point
├── SETUP_SCRIPTS/           # generator modules (create_*, copy_scripts)
├── HELPER_SCRIPTS/          # build/regen/update scripts copied to projects
├── SIGNED_SCRIPTS/          # MAC/ + PC/ signing + release workflow scripts
├── INSTALLER_SCRIPTS/       # MAC/ + PC/ installer scripts (Inno Setup for PC)
├── README.md, CONTRIBUTING.md, QUICK_START.md
```

The `'PLUGIN_SCRIPTS'` entry in `SETUP_SCRIPTS/copy_scripts.py`'s `exclude` set is an intentional safeguard against an older folder name — leave it.

## Common Commands

```bash
# End-to-end generator smoke test
python setup_project.py /tmp/TestPlugin
cd /tmp/TestPlugin
python HELPER_SCRIPTS/init_project.py    # adds JUCE submodule
python HELPER_SCRIPTS/rebuild_all.py     # full build

# Run a single setup module in isolation
python SETUP_SCRIPTS/create_directories.py /tmp/test_output
```

(Note: `README.md` still shows `python SCRIPTS/...` from an earlier layout — actual copy destination is `HELPER_SCRIPTS/`.)

## Template Substitution

Templates are multiline strings in `SETUP_SCRIPTS/create_*.py`. Placeholders:

- `{PROJECT_NAME}` — e.g., `AudioFileChanger`
- `{PROJECT_NAME_LOWER}` — lowercased
- `{PLUGIN_CODE}` — first 4 chars

Applied via `template.format(PROJECT_NAME=..., PROJECT_NAME_LOWER=..., ...)`.

## Non-Obvious Implementation Details

- **File encoding on Windows**: always pass `encoding='utf-8'` to `write_text` / `open` — default codec fails.
- **Paths**: use `pathlib.Path` everywhere. In CMake templates use forward slashes (CMake normalizes them).
- **Version flow**: `VERSION.txt` (plain `MAJOR.MINOR.PATCH`) is sole source of truth. `update_version.py` is read-only — it regenerates `SOURCE/Util/Version.h` from `VERSION.txt` and never modifies the version. Bumping is a deliberate manual edit. CMake reads `VERSION.txt` at configure time; `Version.h` regenerates before each build via the `update_version_header` custom target. Malformed `VERSION.txt` is a hard error, not a silent reset.
- **JUCE include centralization**: generated projects route JUCE includes through `SOURCE/Util/Juce_Header.h`. Needed because Catch2 conflicts with JUCE's global `using namespace` unless controlled. Keep in sync with linked libraries in the generated `CMakeLists.txt`.
- **Brace style**: Allman in all C/C++ output (per user-level rule).
- **No emojis** in generated code or terminal output.

## Constraints (Do Not Violate)

1. Python 3.7+ stdlib only — no pip, no third-party imports.
2. Cross-platform (Windows/macOS/Linux) with standard CMake generators.
3. No emojis anywhere in output, messages, or generated code.

## Off-Limits

- `README.md`, `CONTRIBUTING.md`, `QUICK_START.md`, `SIGNED_SCRIPTS/TODO_mac.md`, `SETUP_SCRIPTS/README.md`, `SIGNED_SCRIPTS/README.md` — human-authored, do not edit without explicit ask.
- Any `NOTES/` directory at any depth — human scratch.

## Adding Features

**New setup module**: create `SETUP_SCRIPTS/my_feature.py` exposing `create_my_feature(project_root: Path, project_name: str)`, then call it from `setup_project()` in `setup_project.py`.

**New runtime script**: drop in `HELPER_SCRIPTS/` (or `SIGNED_SCRIPTS/`, `INSTALLER_SCRIPTS/` for signing/installer flows). Shebang `#!/usr/bin/env python3`, stdlib only, auto-detect plugin name, call `regenSource.py` if it touches CMake inputs, handle both generator types.

**Edit a template**: modify the string in `SETUP_SCRIPTS/create_*.py`; preserve `{VARIABLE}` placeholders; verify CMake syntax (forward slashes) and JUCE virtual-method requirements.

## Known Edge Cases

- `regenSource.py` includes `SUBMODULES/*/SOURCE` and `SUBMODULES/*/TESTS` automatically. Unexpected submodule layouts can pull in unwanted files.
- `JUCE_DISPLAY_SPLASH_SCREEN=1` by default in generated projects — disabling needs a JUCE license.
- Beginners conflate `-DCMAKE_BUILD_TYPE=Release` (single-config) with `--config Release` (multi-config). Build scripts auto-detect.
