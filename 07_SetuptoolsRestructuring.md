# Setuptools Package Structure Issues and Solutions

## Problem Summary

When converting an existing GitHub repository (research code) into an installable Python package, we encountered issues where `pip install` would complete successfully but `import packagename` would fail with "No module named 'packagename'".

## Root Cause Analysis

### Issue 1: Flat Directory Structure
**Problem**: The original repo had a flat structure with Python files in the root directory:
```
repo/
├── setup.py
├── requirements.txt
├── module1.py
├── module2.py
├── utils.py
└── __init__.py  ← In root directory
```

**Symptom**: 
- `pip list` shows package is installed
- `pip install` completes without errors
- But `import packagename` fails with "No module named 'packagename'"
- Individual `.py` files appear directly in site-packages instead of in a package directory

### Issue 2: Incorrect setup.py Configuration
**Problem**: Tried to force setuptools to work with flat structure using:
```python
packages=['spci'],
package_dir={'spci': '.'},
py_modules=[list_of_modules]
```

**Result**: Files were installed as individual modules in site-packages, but no package directory was created.

## The Solution: Standard Python Package Structure

### Required Structure
Move all code into a subdirectory named after your package:
```
repo/
├── setup.py              ← In root
├── requirements.txt      ← In root
├── README.md            ← In root
├── pyproject.toml       ← In root
└── packagename/         ← Package directory
    ├── __init__.py      ← Package init file
    ├── module1.py       ← All Python modules
    ├── module2.py
    ├── utils.py
    └── Data/            ← Data files (if any)
        └── *.csv
```

### Correct setup.py Configuration
Use the standard approach that works with this structure:
```python
from setuptools import setup, find_packages

setup(
    name="packagename",
    version="0.1.0",
    packages=find_packages(),  # Automatically finds packagename/
    include_package_data=True,
    package_data={
        'packagename': ['Data/*.csv'],  # Include data files
    },
    # ... other standard setup parameters
)
```

## Step-by-Step Restructuring Process

### 1. Create Package Directory
```bash
mkdir packagename
```

### 2. Move All Python Files
```bash
move *.py packagename/
move __init__.py packagename/
```

### 3. Move Data Directories (if any)
```bash
move Data/ packagename/
```

### 4. Fix setup.py
Replace complex package configuration with simple `find_packages()`:
```python
# WRONG (what we tried first):
packages=['spci'],
package_dir={'spci': '.'},
py_modules=['module1', 'module2', ...]

# RIGHT (standard approach):
packages=find_packages(),
```

### 5. Test Installation
```bash
pip uninstall packagename -y
pip install .
python -c "import packagename; print('Success!')"
```

## Verification Steps

After restructuring, verify the installation creates the correct structure in site-packages:
```
site-packages/
├── packagename/              ← Proper package directory
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
│   └── Data/
└── packagename-0.1.0.dist-info/  ← Package metadata
```

## Common Symptoms of Incorrect Structure

1. **pip list shows package but import fails**: Files installed as individual modules, no package directory
2. **Individual .py files in site-packages**: Using wrong setup.py configuration
3. **"No module named 'packagename'" error**: Package directory not created

## Why This Happens with Research Code

- **Academic repos**: Often just collection of scripts, not designed as packages
- **Flat structure**: Researchers put everything in root directory for simplicity
- **Missing package conventions**: No understanding of Python packaging standards
- **Direct script usage**: Designed to run scripts directly, not import as modules

## Template for Future Conversions

When converting another repo from this author (or similar research code):

### 1. Assessment
- [ ] Check if files are in root directory (likely yes)
- [ ] Identify main Python modules
- [ ] Look for data directories
- [ ] Check for existing setup.py (likely none)

### 2. Create Package Files
- [ ] Create `setup.py` with standard structure
- [ ] Create `pyproject.toml`
- [ ] Create/update `requirements.txt`
- [ ] Create `__init__.py` with safe imports

### 3. Restructure
- [ ] Create `packagename/` directory
- [ ] Move all `.py` files to `packagename/`
- [ ] Move data directories to `packagename/`
- [ ] Move `__init__.py` to `packagename/`

### 4. Test
- [ ] Install locally: `pip install .`
- [ ] Test import: `python -c "import packagename"`
- [ ] Run diagnostic script if needed
- [ ] Test from separate environment

## Key Lesson

**Never fight setuptools** - use the standard package structure it expects. Trying to force a flat structure with complex `setup.py` configuration leads to broken installations. The standard structure with `find_packages()` just works.

## Diagnostic Script Template

Keep a diagnostic script handy for testing package installations:
```python
def test_import():
    try:
        import packagename
        print(f"✅ SUCCESS: {packagename.__version__}")
        return True
    except ImportError as e:
        print(f"❌ FAILED: {e}")
        return False
```

This approach should work for any research code repository that needs to be converted to a proper Python package.
