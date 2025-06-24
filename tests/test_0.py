import pytest
import numpy as np
from definition_55c8998e5b9e448bb265a14732b915a4 import analyze_covariance_uncertainty

@pytest.mark.parametrize(
    "cov_matrix, uncertainty_level, portfolio_weights, expected",
    [
        # Basic valid case: 2x2 covariance matrix, simple weights, zero uncertainty
        (
            np.array([[1.0, 0.2], [0.2, 1.5]]),
            0.0,
            np.array([0.5, 0.5]),
            float  # expect float output
        ),
        # Valid case with positive uncertainty_level
        (
            np.array([[0.5, 0.1], [0.1, 0.7]]),
            0.1,
            np.array([0.4, 0.6]),
            float
        ),
        # Larger covariance matrix 3x3, equal weights
        (
            np.array([[1.0, 0.3, 0.2],
                      [0.3, 1.1, 0.5],
                      [0.2, 0.5, 1.3]]),
            0.2,
            np.array([1/3, 1/3, 1/3]),
            float
        ),
        # Covariance matrix is identity, uncertainty 0
        (
            np.eye(4),
            0.0,
            np.array([0.25, 0.25, 0.25, 0.25]),
            float
        ),
        # Covariance matrix is zero-matrix, uncertainty 0
        (
            np.zeros((2,2)),
            0.0,
            np.array([0.5, 0.5]),
            float
        ),
        # Uncertainty level is negative (invalid)
        (
            np.array([[1.0, 0.2],[0.2, 1.5]]),
            -0.1,
            np.array([0.5, 0.5]),
            ValueError
        ),
        # Cov_matrix is not square
        (
            np.array([[1.0, 0.2, 0.3],[0.2, 1.5, 0.4]]),
            0.1,
            np.array([0.5, 0.5]),
            ValueError
        ),
        # portfolio_weights length mismatch
        (
            np.array([[1.0,0.2],[0.2,1.5]]),
            0.1,
            np.array([0.6, 0.3, 0.1]),
            ValueError
        ),
        # portfolio_weights sum not 1 (e.g. sum > 1)
        (
            np.array([[1.0,0.2],[0.2,1.5]]),
            0.1,
            np.array([0.6, 0.6]),
            ValueError
        ),
        # portfolio_weights sum zero (edge case)
        (
            np.array([[1.0,0.2],[0.2,1.5]]),
            0.1,
            np.array([0.0, 0.0]),
            ValueError
        ),
        # covariance matrix contains NaNs
        (
            np.array([[np.nan, 0.2], [0.2, 1.5]]),
            0.1,
            np.array([0.5, 0.5]),
            ValueError
        ),
        # covariance matrix contains negative diagonal elements (invalid covariance)
        (
            np.array([[1.0, 0.2], [0.2, -1.5]]),
            0.1,
            np.array([0.5, 0.5]),
            ValueError
        ),
        # Inputs are of wrong type: cov_matrix as list of lists
        (
            [[1.0, 0.2],[0.2, 1.5]],
            0.1,
            np.array([0.5, 0.5]),
            TypeError
        ),
        # Inputs are of wrong type: uncertainty_level as string
        (
            np.array([[1.0, 0.2],[0.2, 1.5]]),
            "0.1",
            np.array([0.5, 0.5]),
            TypeError
        ),
        # Inputs are of wrong type: portfolio_weights as list of floats
        (
            np.array([[1.0, 0.2],[0.2, 1.5]]),
            0.1,
            [0.5, 0.5],
            TypeError
        ),
        # Very large uncertainty level (to test upper bound handling or exceptions)
        (
            np.array([[1.0, 0.1],[0.1, 1.0]]),
            10.0,
            np.array([0.5, 0.5]),
            float
        ),
        # Very small positive uncertainty (close to zero)
        (
            np.array([[2.0, 0.3],[0.3, 2.0]]),
            1e-10,
            np.array([0.7, 0.3]),
            float
        ),
        # Single asset covariance matrix (1x1)
        (
            np.array([[0.5]]),
            0.05,
            np.array([1.0]),
            float
        ),
        # portfolio_weights contain negative weights (valid if shorting allowed)
        (
            np.array([[1.0, 0.2],[0.2, 1.5]]),
            0.1,
            np.array([1.2, -0.2]),
            float
        ),
        # portfolio_weights sum close to 1 but slight floating point deviation
        (
            np.array([[1.0, 0.2],[0.2, 1.5]]),
            0.2,
            np.array([0.5, 0.5000000001]),
            float
        ),
    ]
)
def test_analyze_covariance_uncertainty(cov_matrix, uncertainty_level, portfolio_weights, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            analyze_covariance_uncertainty(cov_matrix, uncertainty_level, portfolio_weights)
    else:
        result = analyze_covariance_uncertainty(cov_matrix, uncertainty_level, portfolio_weights)
        assert isinstance(result, float)
        # result should be non-negative (risk measure usually >= 0)
        assert result >= 0