# NumPy Compatibility Issue Fix

## Problem

Error when importing SPCI package:
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
```

This is a **numpy version compatibility issue** with compiled packages like `skranger`.

## Root Cause

- NumPy 2.0+ changed internal structures
- `skranger` and `sklearn_quantile` were compiled with older NumPy versions
- Binary incompatibility between NumPy versions

## Solutions (Try in Order)

### Solution 1: Reinstall Problematic Packages (Recommended)
```powershell
# Uninstall problematic packages
pip uninstall skranger sklearn_quantile -y

# Force reinstall with no cache (gets latest compatible versions)
pip install --no-cache-dir --force-reinstall skranger sklearn_quantile

# Test
python -c "import skranger; print('skranger works')"
```

### Solution 2: Downgrade NumPy (If Solution 1 fails)
```powershell
# Downgrade to NumPy 1.x
pip install "numpy<2.0"

# Test
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import skranger; print('skranger works')"
```

### Solution 3: Use Conda Instead of Pip
```powershell
# If using conda environment
conda install -c conda-forge skranger

# Or create fresh environment with compatible versions
conda create -n spci_fixed python=3.9 numpy=1.24 -y
conda activate spci_fixed
conda install -c conda-forge skranger
pip install sklearn_quantile statsmodels seaborn matplotlib torch pandas scikit-learn
```

### Solution 4: Remove Problematic Dependencies (Last Resort)
If the package can work without `skranger`:
```python
# Comment out the problematic import in SPCI_class.py:
# from skranger.ensemble import RangerForestRegressor
```

## Testing After Fix

```powershell
# Test individual packages
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import skranger; print('skranger: OK')"
python -c "import sklearn_quantile; print('sklearn_quantile: OK')"

# Test SPCI package
python -c "import spci; print('SPCI: OK')"

# Run full diagnostic
python diagnostic_test.py
```

## Prevention for Future

When creating requirements.txt, pin numpy version:
```
numpy>=1.21,<2.0
skranger
sklearn_quantile
statsmodels
```

This ensures compatibility across different environments.
