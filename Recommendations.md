# Code Review Recommendations for SPCI Package

## Critical Issues (Must Fix)

### 1. **CRITICAL BUG: Duplicate Unreachable Code**
**Location**:
- `spci/SPCI_class.py` lines 656-695
- `spci/PI_class_EnbPI.py` lines 801-840

**Issue**: The `compute_AdaptiveCI_intervals()` method has duplicate code after a `return` statement. Lines 616-655 and 656-695 in SPCI_class.py are identical (same for PI_class_EnbPI.py lines 761-800 and 801-840). The second block is unreachable dead code.

**Fix**: Delete lines 656-695 in `spci/SPCI_class.py` and lines 801-840 in `spci/PI_class_EnbPI.py`.

```python
# Current (WRONG):
        if get_plots:
            return [PIs, results]
        else:
            return results
        # TODO: I guess I can use the QOOB idea, by using "get_rXY"
        Dcal_scores = np.array([...])  # THIS NEVER EXECUTES!
        # ... 40 more lines of duplicate code ...

# Should be:
        if get_plots:
            return [PIs, results]
        else:
            return results
```

### 2. **Invalid Escape Sequences in Docstrings**
**Location**:
- `spci/PI_class_EnbPI.py` lines 351, 402

**Issue**: Docstrings contain `\c` which is an invalid escape sequence causing SyntaxWarning.

**Fix**: Use raw strings for docstrings with LaTeX notation:
```python
# Current:
'''The residuals are weighted by fitting a logistic regression on
   (X_calibrate, C=0) \cup (X_predict, C=1'''

# Should be:
r'''The residuals are weighted by fitting a logistic regression on
    (X_calibrate, C=0) \cup (X_predict, C=1'''
```

### 3. **Missing Import for clone_model**
**Location**: `spci/PI_class_EnbPI.py` lines 61, 209

**Issue**: Code uses `clone_model()` but the import is commented out (line 5). This will cause a `NameError` if the code path is executed with Keras models.

**Fix**: Either:
- Remove the commented import and add keras as a dependency, OR
- Remove the unused Keras/TensorFlow code paths entirely if not needed

### 4. **Deprecated NumPy Type Usage**
**Location**: `spci/SPCI_class.py` line 101

**Issue**: `np.float` is deprecated since NumPy 1.20 and removed in NumPy 1.24+.

**Fix**:
```python
# Current:
boot_pred = boot_pred.astype(np.float)

# Should be:
boot_pred = boot_pred.astype(np.float64)
# Or simply:
boot_pred = boot_pred.astype(float)
```

## High Priority Issues

### 5. **Hardcoded CPU Device (GPU Ignored)**
**Location**: `spci/SPCI_class.py` lines 33-34

**Issue**: Code explicitly sets device to CPU even when CUDA is available:
```python
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
```

**Fix**: Enable GPU usage or make it configurable:
```python
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Or allow user configuration:
def get_device(use_cuda=True):
    if use_cuda and torch.cuda.is_available():
        return torch.device("cuda:0")
    return torch.device("cpu")
```

### 6. **Debug Imports in Production Code**
**Location**:
- `spci/SPCI_class.py` line 14: `import pdb`
- `spci/visualize.py` line 12: `import pdb`

**Issue**: Debug imports left in production code.

**Fix**: Remove these imports entirely, or make them conditional:
```python
# Only import for debugging if needed
if __debug__:
    import pdb
```

### 7. **Hardcoded Relative File Paths**
**Location**: Multiple files
- `spci/data.py` lines 37, 50, 81
- `spci/utils_EnbPI.py` lines 472, 1341, 1354

**Issue**: Hardcoded relative paths like `'Data/Solar_Atl_data.csv'` won't work reliably across different installations.

**Fix**: Use `importlib.resources` or package-relative paths:
```python
import os
import importlib.resources as pkg_resources

# Get package data directory
if hasattr(pkg_resources, 'files'):
    # Python 3.9+
    data_path = pkg_resources.files('spci') / 'Data' / 'Solar_Atl_data.csv'
else:
    # Fallback
    data_path = os.path.join(os.path.dirname(__file__), 'Data', 'Solar_Atl_data.csv')

data = pd.read_csv(str(data_path))
```

### 8. **Global Warning Suppression**
**Location**: Multiple files
- `spci/SPCI_class.py` line 32
- `spci/PI_class_EnbPI.py` line 14
- `spci/data.py` line 11
- `spci/visualize.py` line 15

**Issue**: `warnings.filterwarnings("ignore")` suppresses ALL warnings globally, hiding potential issues.

**Fix**: Be specific about which warnings to suppress:
```python
# Instead of:
warnings.filterwarnings("ignore")

# Use specific filters:
warnings.filterwarnings("ignore", category=DeprecationWarning, module="statsmodels")
warnings.filterwarnings("ignore", message=".*sklearn.*")

# Or use context managers for temporary suppression:
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # Code that generates expected warnings
```

## Medium Priority Issues

### 9. **TODO Comments Not Addressed**
**Location**:
- `spci/SPCI_class.py` lines 616, 656
- `spci/PI_class_EnbPI.py` lines 761, 801

**Issue**: TODO comments suggest using QOOB's `get_rXY` method but this is never implemented.

**Fix**: Either implement the suggested improvement or remove the TODO comments if not planning to address them.

### 10. **Hardcoded Random Seeds Everywhere**
**Location**: Throughout codebase (20+ instances)

**Issue**: Many functions have hardcoded seeds (0, 1, 1103, 98765, etc.) which:
- Makes results deterministic when they shouldn't be
- Reduces reproducibility control
- Makes testing difficult

**Fix**: Make seed a configurable parameter with a default:
```python
def function_name(data, seed=None):
    if seed is not None:
        np.random.seed(seed)
    # ... rest of function
```

### 11. **Non-Cross-Platform Path Construction**
**Location**: `spci/data.py` and elsewhere

**Issue**: File paths constructed with f-strings won't work on all platforms:
```python
data = pd.read_csv(f'Data/electricity-normalized.csv')
```

**Fix**: Use `os.path.join()`:
```python
data_dir = os.path.join(os.path.dirname(__file__), 'Data')
data = pd.read_csv(os.path.join(data_dir, 'electricity-normalized.csv'))
```

### 12. **Personal Directory Path in Comment**
**Location**: `spci/utils_EnbPI.py` line 408

**Issue**: Comment contains personal directory path:
```python
# Note, data at many other grid cells are available. Others are in Downloads/🌟AISTATS Data/Greenhouse Data
```

**Fix**: Remove or update to generic path.

### 13. **Unused Commented Code**
**Location**: Multiple files

**Issue**: Large blocks of commented-out code (Keras/TensorFlow imports, alternative implementations).

**Fix**: Remove commented code that's not being used. Use version control (git) to track history instead.

## Low Priority / Code Quality Issues

### 14. **Inconsistent Error Handling**
**Issue**: Most functions don't validate inputs or handle errors gracefully.

**Recommendation**: Add input validation and meaningful error messages:
```python
def fit_bootstrap_models_online_multistep(self, B, fit_sigmaX=True, stride=1):
    if B <= 0:
        raise ValueError(f"B must be positive, got {B}")
    if stride <= 0:
        raise ValueError(f"stride must be positive, got {stride}")
    # ... rest of function
```

### 15. **Inconsistent Naming Conventions**
**Issue**: Mix of naming styles (camelCase vs snake_case, e.g., `fit_sigmaX` vs `Ensemble_train_interval_centers`).

**Recommendation**: Follow PEP 8 consistently:
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### 16. **Mutable Default Arguments**
**Location**: `spci/SPCI_class.py` line 698

**Issue**: Mutable default arguments (empty lists) can cause bugs:
```python
def NEX_CP(X, Y, x, alpha, weights=[], tags=[], seed=1103):
```

**Fix**:
```python
def NEX_CP(X, Y, x, alpha, weights=None, tags=None, seed=1103):
    if weights is None:
        weights = []
    if tags is None:
        tags = []
```

### 17. **Magic Numbers Throughout Code**
**Issue**: Hard-coded values like `0.99`, `0.995`, `10`, `300`, etc. without explanation.

**Recommendation**: Define as named constants with documentation:
```python
# At module level:
DEFAULT_WLS_DECAY = 0.99  # Exponential decay rate for weighted least squares
DEFAULT_PAST_WINDOW = 300  # Number of historical residuals to use
DEFAULT_N_ESTIMATORS = 10  # Number of trees in random forest
```

### 18. **Missing Type Hints**
**Issue**: No type hints on functions make the API unclear.

**Recommendation**: Add type hints for better IDE support and documentation:
```python
from typing import Optional, Tuple
import numpy.typing as npt

def fit_bootstrap_models_online_multistep(
    self,
    B: int,
    fit_sigmaX: bool = True,
    stride: int = 1
) -> None:
    """Train B bootstrap estimators..."""
```

### 19. **Long Functions**
**Issue**: Some functions are extremely long (500+ lines), making them hard to understand and maintain.

**Recommendation**: Break down into smaller, focused functions:
- `fit_bootstrap_models_online_multistep()` could be split into helper functions
- `test_EnbPI_or_SPCI()` could be modularized

### 20. **No Logging**
**Issue**: Code uses print statements for output. This makes it hard to control verbosity.

**Recommendation**: Use Python's `logging` module:
```python
import logging
logger = logging.getLogger(__name__)

# Instead of print():
logger.info(f'Finish Fitting {B} Bootstrap models, took {time.time()-start} secs.')
logger.debug(f'At test time {t}')
```

## Testing Recommendations

### 21. **Add Unit Tests**
**Current State**: No tests directory or test files.

**Recommendation**: Create `tests/` directory with:
- Unit tests for each class
- Integration tests for full workflows
- Regression tests for published results

### 22. **Add Data Validation Tests**
**Recommendation**: Test that included data files exist and load correctly:
```python
def test_data_files_exist():
    from spci.data import real_data_loader
    loader = real_data_loader()
    # Test that data loads without error
    X, Y = loader.get_data('electric', ...)
    assert len(X) > 0
    assert len(Y) > 0
```

## Documentation Recommendations

### 23. **Add Docstring Examples**
**Issue**: Many docstrings lack usage examples.

**Recommendation**: Add examples in docstrings:
```python
def compute_PIs_Ensemble_online(self, alpha, stride=1, ...):
    """
    Compute prediction intervals using ensemble methods.

    Parameters
    ----------
    alpha : float
        Miscoverage level (e.g., 0.1 for 90% coverage)
    ...

    Examples
    --------
    >>> model = SPCI_and_EnbPI(X_train, X_test, Y_train, Y_test)
    >>> model.fit_bootstrap_models_online_multistep(B=25)
    >>> model.compute_PIs_Ensemble_online(alpha=0.1)
    """
```

### 24. **Add a CONTRIBUTING.md**
**Recommendation**: Document development setup, coding standards, and contribution guidelines.

## Summary

**Must fix immediately:**
1. Remove duplicate unreachable code (lines 656-695 in SPCI_class.py and 801-840 in PI_class_EnbPI.py)
2. Fix invalid escape sequences in docstrings
3. Fix deprecated `np.float` usage
4. Either fix or remove `clone_model` import issue

**Should fix soon:**
5. Enable GPU support or make it configurable
6. Remove debug imports (pdb)
7. Fix hardcoded relative file paths using package resources
8. Replace global warning suppression with specific filters

**Nice to have:**
9-24. Code quality, testing, and documentation improvements

These changes will make the package more maintainable, reliable, and user-friendly.
