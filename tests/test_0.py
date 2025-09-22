import pytest
import numpy as np
from definition_2851cd8af11b4007aead2385875e6d9e import generate_nominal_covariance_matrix

@pytest.mark.parametrize("n, expected_shape", [
    (3, (3, 3)),
    (5, (5, 5)),
    (10, (10, 10)),
])
def test_generate_nominal_covariance_matrix_shape(n, expected_shape):
    result = generate_nominal_covariance_matrix(n)
    assert result.shape == expected_shape

def test_generate_nominal_covariance_matrix_positive_semi_definite():
    n = 5
    result = generate_nominal_covariance_matrix(n)
    eigenvalues = np.linalg.eigvalsh(result)
    assert np.all(eigenvalues >= 0)

def test_generate_nominal_covariance_matrix_symmetric():
    n = 4
    result = generate_nominal_covariance_matrix(n)
    assert np.allclose(result, result.T)

def test_generate_nominal_covariance_matrix_n_equals_1():
    n = 1
    result = generate_nominal_covariance_matrix(n)
    assert result.shape == (1, 1)
    assert result[0, 0] >= 0
    
def test_generate_nominal_covariance_matrix_n_equals_0():
    with pytest.raises(Exception):
        generate_nominal_covariance_matrix(0)
