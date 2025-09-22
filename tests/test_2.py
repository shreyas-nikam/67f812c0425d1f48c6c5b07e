import pytest
import numpy as np
from definition_d211b7b608644376933d1dcd4142821a import calculate_portfolio_risk

@pytest.fixture
def sample_weight_vector():
    return np.array([0.2, 0.3, 0.5])

@pytest.fixture
def sample_covariance_matrix():
    return np.array([[0.1, 0.05, 0.02],
                     [0.05, 0.2, 0.03],
                     [0.02, 0.03, 0.3]])

def test_calculate_portfolio_risk_positive(sample_weight_vector, sample_covariance_matrix):
    risk = calculate_portfolio_risk(sample_weight_vector, sample_covariance_matrix)
    assert risk > 0

def test_calculate_portfolio_risk_small_weights(sample_covariance_matrix):
    w = np.array([0.01, 0.02, 0.03])
    risk = calculate_portfolio_risk(w, sample_covariance_matrix)
    assert risk > 0

def test_calculate_portfolio_risk_zero_weights(sample_covariance_matrix):
    w = np.array([0, 0, 0])
    risk = calculate_portfolio_risk(w, sample_covariance_matrix)
    assert risk == 0

def test_calculate_portfolio_risk_non_square_covariance_matrix(sample_weight_vector):
    Sigma = np.array([[1, 2], [3, 4], [5, 6]])
    with pytest.raises(ValueError):
        calculate_portfolio_risk(sample_weight_vector, Sigma)

def test_calculate_portfolio_risk_invalid_input_types():
    with pytest.raises(TypeError):
        calculate_portfolio_risk([1,2,3], "abc")
