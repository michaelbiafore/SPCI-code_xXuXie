import pytest
import numpy as np
import torch
from sklearn.ensemble import RandomForestRegressor
from spci.data import real_data_loader
import spci.SPCI_class as SPCI

class TestEnbPIBaseline:
    """Baseline tests for EnbPI method"""

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

    def test_enbpi_initialization(self, setup_data):
        """Test EnbPI class initializes correctly"""
        X_train, X_predict, Y_train, Y_predict = setup_data
        fit_func = RandomForestRegressor(
            n_estimators=10, max_depth=1, criterion='squared_error',
            bootstrap=False, n_jobs=-1, random_state=1103
        )
        enbpi = SPCI.SPCI_and_EnbPI(X_train, X_predict, Y_train, Y_predict, fit_func=fit_func)

        assert enbpi is not None
        assert enbpi.X_train.shape == (2755, 4)
        assert enbpi.X_predict.shape == (689, 4)

    def test_enbpi_fit_bootstrap_models(self, setup_data):
        """Test bootstrap model fitting completes"""
        X_train, X_predict, Y_train, Y_predict = setup_data
        fit_func = RandomForestRegressor(
            n_estimators=10, max_depth=1, criterion='squared_error',
            bootstrap=False, n_jobs=-1, random_state=1103
        )
        enbpi = SPCI.SPCI_and_EnbPI(X_train, X_predict, Y_train, Y_predict, fit_func=fit_func)

        # Should complete without error
        enbpi.fit_bootstrap_models_online_multistep(B=25, fit_sigmaX=False, stride=1)

        # Check that predictions were made
        assert not np.all(enbpi.Ensemble_pred_interval_centers == np.inf)

    def test_enbpi_coverage_and_width(self, setup_data):
        """Test EnbPI produces expected coverage and width (baseline from notebook)

        Notebook results: Coverage ~90.86%, Width ~0.322
        Allow ±5% tolerance for coverage and ±10% for width
        """
        X_train, X_predict, Y_train, Y_predict = setup_data
        fit_func = RandomForestRegressor(
            n_estimators=10, max_depth=1, criterion='squared_error',
            bootstrap=False, n_jobs=-1, random_state=1103
        )
        enbpi = SPCI.SPCI_and_EnbPI(X_train, X_predict, Y_train, Y_predict, fit_func=fit_func)

        # Fit models
        enbpi.fit_bootstrap_models_online_multistep(B=25, fit_sigmaX=False, stride=1)

        # Compute PIs
        alpha = 0.1
        past_window = 300
        enbpi.compute_PIs_Ensemble_online(
            alpha, smallT=True, past_window=past_window,
            use_SPCI=False, quantile_regr=False, stride=1
        )

        # Get results
        results = enbpi.get_results(alpha, 'electric', 1)

        coverage = results['coverage'].item()
        width = results['width'].item()

        # Baseline assertions with tolerance
        # Expected: coverage ~0.9086, width ~0.322
        assert 0.85 < coverage < 0.95, f"Coverage {coverage} outside expected range [0.85, 0.95]"
        assert 0.29 < width < 0.36, f"Width {width} outside expected range [0.29, 0.36]"

        print(f"EnbPI Coverage: {coverage:.4f}, Width: {width:.4f}")

    def test_enbpi_reproducibility(self, setup_data):
        """Test EnbPI produces consistent results with same random seed"""
        X_train, X_predict, Y_train, Y_predict = setup_data

        results_list = []
        for _ in range(2):
            fit_func = RandomForestRegressor(
                n_estimators=10, max_depth=1, criterion='squared_error',
                bootstrap=False, n_jobs=-1, random_state=1103
            )
            enbpi = SPCI.SPCI_and_EnbPI(X_train, X_predict, Y_train, Y_predict, fit_func=fit_func)
            enbpi.fit_bootstrap_models_online_multistep(B=25, fit_sigmaX=False, stride=1)
            enbpi.compute_PIs_Ensemble_online(0.1, smallT=True, past_window=300,
                                             use_SPCI=False, quantile_regr=False, stride=1)
            results = enbpi.get_results(0.1, 'electric', 1)
            results_list.append(results)

        # Results should be nearly identical (allowing for threading non-determinism)
        # Both coverage and width can vary slightly due to parallel RandomForest execution
        assert np.isclose(results_list[0]['coverage'].item(),
                         results_list[1]['coverage'].item(), rtol=1e-2)
        assert np.isclose(results_list[0]['width'].item(),
                         results_list[1]['width'].item(), rtol=2e-2)
