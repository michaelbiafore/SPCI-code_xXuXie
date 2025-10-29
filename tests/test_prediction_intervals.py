import pytest
import numpy as np
import torch
from sklearn.ensemble import RandomForestRegressor
from spci.data import real_data_loader
import spci.SPCI_class as SPCI

class TestPredictionIntervals:
    """Test prediction interval properties"""

    @pytest.fixture
    def setup_enbpi(self):
        """Setup EnbPI instance with predictions computed"""
        dloader = real_data_loader()
        X_full, Y_full = dloader.electric_dataset()
        X_full = torch.from_numpy(X_full)
        Y_full = torch.from_numpy(Y_full)

        train_frac = 0.8
        N = int(X_full.shape[0] * train_frac)
        X_train, X_predict = X_full[:N], X_full[N:]
        Y_train, Y_predict = Y_full[:N], Y_full[N:]

        fit_func = RandomForestRegressor(
            n_estimators=10, max_depth=1, criterion='squared_error',
            bootstrap=False, n_jobs=-1, random_state=1103
        )
        enbpi = SPCI.SPCI_and_EnbPI(X_train, X_predict, Y_train, Y_predict, fit_func=fit_func)
        enbpi.fit_bootstrap_models_online_multistep(B=25, fit_sigmaX=False, stride=1)
        enbpi.compute_PIs_Ensemble_online(0.1, smallT=True, past_window=300,
                                         use_SPCI=False, quantile_regr=False, stride=1)
        return enbpi

    def test_pi_bounds_are_valid(self, setup_enbpi):
        """Test that lower bounds <= upper bounds"""
        enbpi = setup_enbpi
        PIs = enbpi.PIs_Ensemble

        assert np.all(PIs['lower'] <= PIs['upper']), "Some lower bounds exceed upper bounds"

    def test_pi_length_matches_test_data(self, setup_enbpi):
        """Test that PIs have same length as test data"""
        enbpi = setup_enbpi
        PIs = enbpi.PIs_Ensemble

        assert len(PIs['lower']) == len(enbpi.Y_predict)
        assert len(PIs['upper']) == len(enbpi.Y_predict)

    def test_pi_centers_are_finite(self, setup_enbpi):
        """Test that prediction centers are all finite"""
        enbpi = setup_enbpi

        assert np.all(np.isfinite(enbpi.Ensemble_pred_interval_centers))

    def test_target_coverage_met(self, setup_enbpi):
        """Test that actual coverage is close to target (1-alpha)"""
        enbpi = setup_enbpi
        results = enbpi.get_results(0.1, 'electric', 1)
        coverage = results['coverage'].item()

        # For 90% target, actual should be at least 85% (conservative)
        assert coverage >= 0.85, f"Coverage {coverage} is below minimum threshold 0.85"
