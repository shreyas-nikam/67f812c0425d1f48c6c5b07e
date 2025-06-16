
import pytest
import numpy as np
import cvxpy as cp
from typing import Tuple
from numpy.testing import assert_allclose

import covariance_uncertainty as cu  # Replace your_module

# Test generate_nominal_covariance_matrix
def test_generate_nominal_covariance_matrix():
    n = 3
    Sigma_nom = cu.generate_nominal_covariance_matrix(n)
    assert Sigma_nom.shape == (n, n)
    assert np.all(np.linalg.eigvals(Sigma_nom) >= 0)  # Positive semi-definite

# Test calculate_portfolio_risk
def test_calculate_portfolio_risk():
    w = np.array([0.2, 0.3, 0.5])
    Sigma = np.array([[0.04, 0.01, 0.00], [0.01, 0.09, 0.02], [0.00, 0.02, 0.25]])
    risk = cu.calculate_portfolio_risk(w, Sigma)
    assert isinstance(risk, float)
    assert risk > 0

# Test generate_uncertainty_set_sample
def test_generate_uncertainty_set_sample():
    n = 3
    Sigma_nom = cu.generate_nominal_covariance_matrix(n)
    delta = 0.1
    Sigma_sample = cu.generate_uncertainty_set_sample(Sigma_nom, delta, n)
    if Sigma_sample is not None:
        assert Sigma_sample.shape == (n, n)
        assert np.all(np.linalg.eigvals(Sigma_sample) >= 0)
        assert np.all(np.abs(Sigma_sample - Sigma_nom) <= delta)

def test_generate_uncertainty_set_sample_failure():
    n = 3
    Sigma_nom = cu.generate_nominal_covariance_matrix(n)
    delta = 100 # large delta
    Sigma_sample = cu.generate_uncertainty_set_sample(Sigma_nom, delta, n)
    #With a large enough delta, the sample might not be PSD
    #The function must return None in such cases.
    if Sigma_sample is not None:
        try:
            np.linalg.cholesky(Sigma_sample)
        except np.linalg.LinAlgError:
            assert True  #test passes because the matrix is not PSD
        else:
            assert False #test fails because the matrix should have been non-PSD

# Test optimize_portfolio
def test_optimize_portfolio():
    n = 3
    Sigma_nom = cu.generate_nominal_covariance_matrix(n)
    np.random.seed(2)
    mu = np.abs(np.random.randn(n, 1)) / 15
    w_optimized = cu.optimize_portfolio(Sigma_nom, mu)
    assert w_optimized.shape == (n,)
    assert np.isclose(np.sum(w_optimized), 1)

# Test worst_case_risk_analysis
def test_worst_case_risk_analysis():
    n = 3
    Sigma_nom = cu.generate_nominal_covariance_matrix(n)
    np.random.seed(2)
    mu = np.abs(np.random.randn(n, 1)) / 15
    w_optimized = cu.optimize_portfolio(Sigma_nom, mu)
    delta = 0.2
    worst_case_std_dev, worst_case_delta = cu.worst_case_risk_analysis(w_optimized, Sigma_nom, delta)
    assert isinstance(worst_case_std_dev, float)
    assert worst_case_delta.shape == (n, n)
