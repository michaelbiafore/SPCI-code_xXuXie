# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPCI (Sequential Predictive Conformal Inference) is a Python package for time series prediction intervals using conformal inference methods. This implements the ICML 2023 paper "Sequential Predictive Conformal Inference for Time Series" (Xu & Xie).

**Key Concepts:**
- **EnbPI**: Ensemble Batch Prediction Intervals - an earlier method using bootstrap aggregation
- **SPCI**: Sequential Predictive Conformal Inference - uses conditional quantile regression on residuals for adaptive interval widths
- **Conformal Prediction**: Distribution-free framework for uncertainty quantification

## Development Setup

### Installation
```bash
# Install in development mode (editable)
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

### Important Dependencies
- **numpy**: Must be <2.0 for compatibility with sklearn_quantile and other packages
- **sklearn_quantile**: Optional dependency for quantile regression forests. If not available, falls back to standard RandomForestRegressor
- **torch**: Used for MLP models in heteroskedastic error estimation
- **skranger**: For RangerForestRegressor (quantile-capable RF)
- **statsmodels**: For time series models

### Running the Tutorial
```bash
jupyter notebook tutorial_electric_EnbPI_SPCI.ipynb
```

This notebook demonstrates SPCI vs EnbPI on the electricity dataset with significant interval width reduction.

## Architecture

### Core Classes

**`SPCI_and_EnbPI` (in `SPCI_class.py`)**
- Main class combining both SPCI and EnbPI methods
- Key workflow:
  1. `fit_bootstrap_models_online_multistep()` - Trains B bootstrap models, computes LOO residuals
  2. `compute_PIs_Ensemble_online()` - Computes prediction intervals using either:
     - **EnbPI**: Empirical quantiles of residuals (`use_SPCI=False`)
     - **SPCI**: Quantile regression on residuals (`use_SPCI=True`)
  3. `get_results()` - Returns coverage and width metrics

**`prediction_interval` (in `PI_class_EnbPI.py`)**
- Original EnbPI implementation
- Handles ICP, Weighted CP, and other baseline methods
- Less commonly used than SPCI_and_EnbPI class

**`QOOB_or_adaptive_CI` (in `SPCI_class.py`)**
- Competing methods: QOOB (Gupta et al., 2021) and Adaptive CI (Gibbs et al., 2022)

### Key Architecture Patterns

**Bootstrap Aggregation Flow:**
1. Generate B bootstrap samples from training data
2. For each bootstrap sample, train a model (MLP, RF, or custom `fit_func`)
3. Use leave-one-out (LOO) prediction: for training point i, aggregate predictions from models that didn't use i
4. Compute LOO residuals: `ε_i = (Y_i - f̂_{-i}(X_i)) / σ̂(X_i)`

**Multi-step Prediction (`stride` parameter):**
- When `stride > 1`, models predict s steps ahead
- Trains `stride * B` bootstrap models, one for each step offset
- Used for multi-horizon forecasting

**SPCI Quantile Regression:**
- Fits quantile random forests on residuals in auto-regressive fashion
- Uses sliding window (`past_window` parameter) of past residuals as features
- Searches for optimal β* in [0, α] via binning method
- Predicts conditional quantiles rather than marginal quantiles (key innovation)

**Heteroskedastic Error Modeling:**
- When `fit_sigmaX=True`, estimates both f(X) and σ(X) using MLPs
- Residuals normalized: `ε_i = (Y_i - f(X_i)) / σ(X_i)`
- Only works with MLP models (fit_func=None), not sklearn models

### Data Module (`data.py`)

**`real_data_loader`:**
- `get_data()` - Unified interface for loading solar, electric, wind datasets
- Data preprocessing includes rolling windows for feature creation
- Datasets stored in `spci/Data/` directory

**`simulate_data_loader`:**
- Generates synthetic data for three scenarios:
  1. Simple state-space model
  2. Non-stationary time series
  3. Heteroskedastic errors

### Utilities

**`utils_SPCI.py`:**
- `binning()` - Optimal β selection for SPCI
- `binning_use_RF_quantile_regr()` - QRF-based binning
- `strided_app()` - Create sliding windows for multi-step prediction

**`utils_EnbPI.py`:**
- `generate_bootstrap_samples()` - Bootstrap sample generation
- Coverage and width computation helpers

**`visualize.py`:**
- Plotting utilities for prediction intervals and coverage

## Important Implementation Details

### Numpy Compatibility
The package requires numpy <2.0 due to sklearn_quantile dependencies. This is enforced in pyproject.toml and requirements.txt.

### sklearn_quantile Handling
The code has conditional imports for sklearn_quantile. If not available:
- Falls back to standard RandomForestRegressor
- Warning printed: "sklearn_quantile not available, using standard RandomForestRegressor"
- SPCI quantile functionality may be limited

### Multi-step Prediction Indexing
Multi-step prediction with `stride > s` has complex indexing:
- `train_pred_idx = np.arange(0, n, stride)` - indices predicted during training
- `test_pred_idx = np.arange(n, n+n1, stride)` - indices predicted at test time
- LOO residuals only computed at these stride intervals

### Method Selection Parameters
- `use_SPCI=True` → Quantile regression on residuals (SPCI)
- `use_SPCI=False, smallT=True` → Empirical quantiles with limited history (EnbPI)
- `use_SPCI=False, smallT=False` → Empirical quantiles with full history
- `past_window` parameter: Window size for both empirical quantiles (EnbPI) and features (SPCI)

### WLS for Linear Models
When `use_WLS=True` and model is LinearRegression, applies weighted least squares with exponential decay weights (`WLS_c` parameter). Used for comparison with Nex-CP method.

## Testing Functions

The test functions in `SPCI_class.py` (e.g., `test_EnbPI_or_SPCI()`, `test_adaptive_CI()`, `test_NEX_CP()`) are used for reproducing paper experiments. They:
- Load data based on simulation/real data flags
- Train models with various train fractions
- Compare coverage and width across methods
- Save rolling prediction results

## Common Gotchas

1. **Syntax Warnings**: Invalid escape sequences in docstrings at `PI_class_EnbPI.py:350,401` - non-critical but should use raw strings
2. **Device Selection**: Code hardcodes `device = torch.device("cpu")` even when CUDA available
3. **Random Seeds**: Many functions have hardcoded seeds (1103, 524, etc.) - change for reproducibility testing
4. **Data Paths**: Uses relative paths like `'Data/Solar_Atl_data.csv'` - assumes execution from package root

## Citation

When working with this code, refer to:
```bibtex
@InProceedings{xu2023SPCI,
  title = {Sequential Predictive Conformal Inference for Time Series},
  author = {Xu, Chen and Xie, Yao},
  booktitle = {Proceedings of the 40th International Conference on Machine Learning},
  year = {2023}
}
```
