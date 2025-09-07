# Dependency Conflict Resolution

## Problem Identified

```
sklearn-quantile 0.1.1 requires numpy>=2, but you have numpy 1.26.4 which is incompatible.
```

**Root cause**: Incompatible numpy requirements between packages:
- `skranger` needs `numpy<2.0` 
- `sklearn-quantile` needs `numpy>=2.0`

## Solution: Replace sklearn-quantile

Since `sklearn-quantile` is forcing numpy 2.0, let's use an alternative or remove it if not essential.

### Step 1: Check if sklearn-quantile is Essential

Let's see what functionality it provides and if we can replace it:

```powershell
# Search for sklearn_quantile usage in the code
grep -r "sklearn_quantile" spci/
```

### Step 2: Remove sklearn-quantile and Use Alternatives

If sklearn-quantile is used for quantile regression, we can use sklearn's built-in alternatives:

```python
# Instead of:
from sklearn_quantile import RandomForestQuantileRegressor

# Use:
from sklearn.ensemble import RandomForestRegressor
# Or use sklearn.linear_model.QuantileRegressor (sklearn 1.0+)
```

### Step 3: Clean Environment and Reinstall

```powershell
# Remove conflicting package
pip uninstall sklearn-quantile -y

# Keep numpy downgraded
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"  # Should be 1.26.4

# Test if skranger works now
python -c "import skranger; print('skranger works')"

# Reinstall SPCI without sklearn-quantile
pip uninstall spci -y
pip install git+https://github.com/michaelbiafore/SPCI-code_xXuXie.git

# Test
python -c "import spci; print('SPCI works!')"
```

### Step 4: Update Requirements (if needed)

If sklearn-quantile isn't essential, remove it from requirements.txt:

```
numpy>=1.21,<2.0
statsmodels
# sklearn_quantile  ← Remove this line
skranger
pandas
scikit-learn
matplotlib
torch
seaborn
```

### Alternative: Use conda-forge

If sklearn-quantile is essential, try conda-forge versions:

```powershell
# Create fresh environment with conda-forge
conda create -n spci_conda python=3.9 -y
conda activate spci_conda

# Install from conda-forge (better dependency resolution)
conda install -c conda-forge numpy skranger statsmodels pandas scikit-learn matplotlib pytorch seaborn -y

# Try to install sklearn-quantile with conda
conda install -c conda-forge sklearn-quantile

# If that fails, skip sklearn-quantile
pip install git+https://github.com/michaelbiafore/SPCI-code_xXuXie.git
```

## Quick Test Commands

```powershell
# Current status
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"

# Remove conflicting package
pip uninstall sklearn-quantile -y

# Test individual components
python -c "import skranger; print('skranger: OK')"
python -c "import statsmodels; print('statsmodels: OK')"

# Test SPCI
python -c "import spci; print('SPCI: SUCCESS!')"
```
