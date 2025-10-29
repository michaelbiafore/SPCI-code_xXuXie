import pytest
import numpy as np
import torch
from sklearn.ensemble import RandomForestRegressor
from spci.data import real_data_loader
import spci.SPCI_class as SPCI

class TestSPCIBaseline:
    """Baseline tests for SPCI method"""

    @pytest.fixture
    def setup_data(self):
        """Setup data matching notebook configuration"""
        dloader = real_data_loader()
        X_full, Y_full = dloader.electric_dataset()
        X_full = torch.from_numpy(X_full)
        Y_full = torch.from_numpy(Y_full)

        train_frac = 0.8
        N = int(X_full.shape[0] * train_frac)
        X_train = X_full[:N]
        X_predict = X_full[N:]
        Y_train = Y_full[:N]
        Y_predict = Y_full[N:]

        return X_train, X_predict, Y_train, Y_predict

    @pytest.mark.slow
    def test_spci_coverage_and_width(self, setup_data):
        """Test SPCI produces expected coverage and width (baseline from notebook)

        Notebook results: Coverage ~93.32%, Width ~0.224
        Allow ±5% tolerance for coverage and ±10% for width

        Note: This test is marked as slow because SPCI takes ~133 seconds
        """
        X_train, X_predict, Y_train, Y_predict = setup_data
        fit_func = RandomForestRegressor(
            n_estimators=10, max_depth=1, criterion='squared_error',
            bootstrap=False, n_jobs=-1, random_state=1103
        )
        spci = SPCI.SPCI_and_EnbPI(X_train, X_predict, Y_train, Y_predict, fit_func=fit_func)

        # Fit models
        spci.fit_bootstrap_models_online_multistep(B=25, fit_sigmaX=False, stride=1)

        # Compute PIs with SPCI
        alpha = 0.1
        past_window = 300
        spci.compute_PIs_Ensemble_online(
            alpha, smallT=False, past_window=past_window,
            use_SPCI=True, quantile_regr=True, stride=1
        )

        # Get results
        results = spci.get_results(alpha, 'electric', 1)

        coverage = results['coverage'].item()
        width = results['width'].item()

        # Baseline assertions with tolerance
        # Expected: coverage ~0.9332, width ~0.224
        assert 0.88 < coverage < 0.98, f"Coverage {coverage} outside expected range [0.88, 0.98]"
        assert 0.20 < width < 0.25, f"Width {width} outside expected range [0.20, 0.25]"

        print(f"SPCI Coverage: {coverage:.4f}, Width: {width:.4f}")
