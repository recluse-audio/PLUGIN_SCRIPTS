# Contributing to JUCE CMake Project Generator

Thank you for your interest in contributing!

## How to Contribute

### Reporting Bugs

Open an issue with:
- Your operating system and version
- Python version (`python --version`)
- CMake version (`cmake --version`)
- Compiler version (MSVC/GCC/Clang)
- Full error message or unexpected behavior
- Steps to reproduce

### Suggesting Features

Open an issue describing:
- The use case (what problem does it solve?)
- How it should work
- Any alternative approaches you considered

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test thoroughly on your platform
5. Commit with clear messages
6. Push and open a Pull Request

## Development Guidelines

### Code Style

- Follow existing Python style (PEP 8 generally)
- Use type hints for function signatures
- Add docstrings for new functions
- Keep functions focused and single-purpose

### Testing Your Changes

Before submitting:

1. Test the setup script:
   ```bash
   python setup_project.py /tmp/TestPlugin
   cd /tmp/TestPlugin
   python SCRIPTS/init_project.py
   python SCRIPTS/rebuild_all.py
   ```

2. Verify generated files are correct
3. Test on your platform (Windows/macOS/Linux)
4. Check that all build scripts work

### Modular Design

The generator is intentionally modular:
- Each SETUP_SCRIPTS/*.py file handles one responsibility
- PLUGIN_SCRIPTS/ contains files that get copied to generated projects
- Keep setup logic separate from generated project logic

### Template Changes

When modifying templates (in create_*.py files):
- Test with various project names
- Ensure paths work cross-platform (use pathlib.Path)
- Maintain compatibility with JUCE's requirements

## Architecture

```
SCRIPTS/
├── setup_project.py          # Main entry point
├── SETUP_SCRIPTS/            # Generator modules
│   ├── create_directories.py
│   ├── create_cmake.py
│   ├── create_source_files.py
│   └── ...
└── PLUGIN_SCRIPTS/           # Files copied to generated projects
    ├── init_project.py
    ├── rebuild_all.py
    └── ...
```

## What Gets Generated vs What Stays

**Generator files (stay in this repo):**
- `setup_project.py`
- Everything in `SETUP_SCRIPTS/`

**Generated project files (copied to new projects):**
- Everything in `PLUGIN_SCRIPTS/`
- Source file templates (embedded in create_source_files.py)
- CMake templates (embedded in create_cmake.py)

## Testing Checklist

- [ ] Project generates without errors
- [ ] Git initialization works
- [ ] JUCE submodule adds correctly
- [ ] CMake configure succeeds
- [ ] Build completes successfully
- [ ] Generated plugin loads in a DAW (if possible)
- [ ] Tests build and run
- [ ] README is accurate

## Questions?

Open an issue or discussion. This is a community tool and questions help improve documentation!
