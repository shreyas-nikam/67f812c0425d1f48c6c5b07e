
import pytest
import numpy as np
import cvxpy as cp
from No functions to document import (  # Replace your_module
    generate_nominal_covariance_matrix,
    solve_portfolio_optimization,
    calculate_worst_case_risk,
    generate_sample_covariance_matrices,
    calculate_portfolio_risk,
)

# Test generate_nominal_covariance_matrix
def test_generate_nominal_covariance_matrix_positive():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    assert isinstance(Sigma_nom, np.ndarray)
    assert Sigma_nom.shape == (3, 3)

def test_generate_nominal_covariance_matrix_default():
    Sigma_nom = generate_nominal_covariance_matrix()
    assert isinstance(Sigma_nom, np.ndarray)
    assert Sigma_nom.shape == (5, 5)

def test_generate_nominal_covariance_matrix_invalid_n():
    with pytest.raises(ValueError):
        generate_nominal_covariance_matrix(n=-1)
    with pytest.raises(ValueError):
        generate_nominal_covariance_matrix(n=0)
    with pytest.raises(ValueError):
        generate_nominal_covariance_matrix(n=1.5)

# Test solve_portfolio_optimization
def test_solve_portfolio_optimization_positive():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    mu = np.abs(np.random.randn(3, 1)) / 15
    w = solve_portfolio_optimization(Sigma_nom, mu)
    assert isinstance(w, cp.Variable)
    assert w.shape == (3,)

def test_solve_portfolio_optimization_invalid_Sigma_nom():
    Sigma_nom = np.array([[1, 2], [3, 4], [5, 6]])
    mu = np.abs(np.random.randn(3, 1)) / 15
    with pytest.raises(ValueError):
        solve_portfolio_optimization(Sigma_nom, mu)

def test_solve_portfolio_optimization_invalid_mu():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    mu = np.abs(np.random.randn(2, 1)) / 15
    with pytest.raises(ValueError):
        solve_portfolio_optimization(Sigma_nom, mu)

# Test calculate_worst_case_risk
def test_calculate_worst_case_risk_positive():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    mu = np.abs(np.random.randn(3, 1)) / 15
    w = solve_portfolio_optimization(Sigma_nom, mu)
    risk, Delta = calculate_worst_case_risk(Sigma_nom, w, delta=0.1)
    assert isinstance(risk, float)
    assert isinstance(Delta, np.ndarray)
    assert Delta.shape == (3, 3)

def test_calculate_worst_case_risk_invalid_delta():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    mu = np.abs(np.random.randn(3, 1)) / 15
    w = solve_portfolio_optimization(Sigma_nom, mu)
    with pytest.raises(ValueError):
        calculate_worst_case_risk(Sigma_nom, w, delta=-0.1)
    with pytest.raises(ValueError):
        calculate_worst_case_risk(Sigma_nom, w, delta=0.6)

# Test generate_sample_covariance_matrices
def test_generate_sample_covariance_matrices_positive():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    matrices = generate_sample_covariance_matrices(Sigma_nom, delta=0.1, num_samples=5)
    assert isinstance(matrices, list)
    assert len(matrices) == 5
    for matrix in matrices:
        assert isinstance(matrix, np.ndarray)
        assert matrix.shape == (3, 3)

def test_generate_sample_covariance_matrices_invalid_delta():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    with pytest.raises(ValueError):
        generate_sample_covariance_matrices(Sigma_nom, delta=-0.1, num_samples=5)
    with pytest.raises(ValueError):
        generate_sample_covariance_matrices(Sigma_nom, delta=0.6, num_samples=5)

def test_generate_sample_covariance_matrices_invalid_num_samples():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    with pytest.raises(ValueError):
        generate_sample_covariance_matrices(Sigma_nom, delta=0.1, num_samples=-1)
    with pytest.raises(ValueError):
        generate_sample_covariance_matrices(Sigma_nom, delta=0.1, num_samples=0)
    with pytest.raises(ValueError):
        generate_sample_covariance_matrices(Sigma_nom, delta=0.1, num_samples=1.5)

# Test calculate_portfolio_risk
def test_calculate_portfolio_risk_positive():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    w = np.array([0.2, 0.3, 0.5])
    risk = calculate_portfolio_risk(w, Sigma_nom)
    assert isinstance(risk, float)

def test_calculate_portfolio_risk_invalid_dimensions():
    Sigma_nom = generate_nominal_covariance_matrix(n=3, seed=2)
    w = np.array([0.2, 0.3])
    with pytest.raises(ValueError):
        calculate_portfolio_risk(w, Sigma_nom)
