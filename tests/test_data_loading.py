import pytest
import numpy as np
import torch
from spci.data import real_data_loader

class TestElectricDataset:
    """Test electric dataset loading"""

    def test_electric_dataset_loads(self):
        """Verify electric dataset loads without errors"""
        dloader = real_data_loader()
        X_full, Y_full = dloader.electric_dataset()
        assert X_full is not None
        assert Y_full is not None

    def test_electric_dataset_shape(self):
        """Verify expected shape from notebook: (3444, 4) and (3444,)"""
        dloader = real_data_loader()
        X_full, Y_full = dloader.electric_dataset()
        assert X_full.shape == (3444, 4), f"Expected (3444, 4), got {X_full.shape}"
        assert Y_full.shape == (3444,), f"Expected (3444,), got {Y_full.shape}"

    def test_electric_dataset_types(self):
        """Verify data types are float64"""
        dloader = real_data_loader()
        X_full, Y_full = dloader.electric_dataset()
        assert X_full.dtype == np.float64
        assert Y_full.dtype == np.float64

    def test_electric_dataset_no_nans(self):
        """Verify no NaN values in loaded data"""
        dloader = real_data_loader()
        X_full, Y_full = dloader.electric_dataset()
        assert not np.isnan(X_full).any()
        assert not np.isnan(Y_full).any()
