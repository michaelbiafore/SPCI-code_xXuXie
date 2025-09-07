"""
SPCI - Sequential Prediction Conformal Inference Package

This package provides tools for sequential prediction conformal inference 
and prediction intervals using EnbPI and related methods.
"""

from .SPCI_class import *
from .PI_class_EnbPI import prediction_interval
from .data import *
from .utils_SPCI import *
from .utils_EnbPI import *
from .visualize import *

__version__ = "0.1.0"
__author__ = "SPCI Contributors"

# Make main classes easily accessible
__all__ = [
    'prediction_interval',
    # Add other main classes/functions you want to expose
]
