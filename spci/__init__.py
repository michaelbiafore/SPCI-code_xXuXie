"""
SPCI - Sequential Prediction Conformal Inference Package

This package provides tools for sequential prediction conformal inference 
and prediction intervals using EnbPI and related methods.
"""

__version__ = "0.1.0"
__author__ = "SPCI Contributors"

# Import modules safely with error handling
try:
    from .PI_class_EnbPI import prediction_interval
except ImportError as e:
    print(f"Warning: Could not import prediction_interval: {e}")
    prediction_interval = None

try:
    from . import SPCI_class
except ImportError as e:
    print(f"Warning: Could not import SPCI_class: {e}")
    SPCI_class = None

try:
    from . import data
except ImportError as e:
    print(f"Warning: Could not import data: {e}")
    data = None

try:
    from . import utils_SPCI
except ImportError as e:
    print(f"Warning: Could not import utils_SPCI: {e}")
    utils_SPCI = None

try:
    from . import utils_EnbPI
except ImportError as e:
    print(f"Warning: Could not import utils_EnbPI: {e}")
    utils_EnbPI = None

try:
    from . import visualize
except ImportError as e:
    print(f"Warning: Could not import visualize: {e}")
    visualize = None

# Make main classes easily accessible
__all__ = [
    'prediction_interval',
    'SPCI_class',
    'data',
    'utils_SPCI', 
    'utils_EnbPI',
    'visualize'
]
