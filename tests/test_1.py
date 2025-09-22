import pytest
import numpy as np
from definition_609d6f157f43485fa766b23f4680ed67 import generate_uncertainty_set

@pytest.mark.parametrize("Sigma_nom, delta, num_samples, expected_shape", [
    (np.array([[1, 0], [0, 1]]), 0.1, 5, (5, 2, 2)),
    (np.array([[4, 2], [2, 3]]), 0.2, 3, (3, 2, 2)),
    (np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 0.05, 2, (2, 3, 3)),
])
def test_generate_uncertainty_set_shape(Sigma_nom, delta, num_samples, expected_shape):
    result = generate_uncertainty_set(Sigma_nom, delta, num_samples)
    assert np.array(result).shape == expected_shape

@pytest.mark.parametrize("Sigma_nom, delta, num_samples", [
    (np.array([[1, 0], [0, 1]]), 0.1, 5),
])
def test_generate_uncertainty_set_delta_constraint(Sigma_nom, delta, num_samples):
    result = generate_uncertainty_set(Sigma_nom, delta, num_samples)
    for matrix in result:
        delta_matrix = matrix - Sigma_nom
        assert np.all(np.abs(delta_matrix) <= delta)

@pytest.mark.parametrize("Sigma_nom, delta, num_samples", [
    (np.array([[1, 0], [0, 1]]), 0.1, 5),
])
def test_generate_uncertainty_set_type(Sigma_nom, delta, num_samples):
    result = generate_uncertainty_set(Sigma_nom, delta, num_samples)
    assert isinstance(result, list)
    for matrix in result:
        assert isinstance(matrix, np.ndarray)

def test_generate_uncertainty_set_invalid_sigma():
    with pytest.raises(TypeError):
        generate_uncertainty_set("not a matrix", 0.1, 5)

def test_generate_uncertainty_set_invalid_delta():
    with pytest.raises(TypeError):
        generate_uncertainty_set(np.array([[1, 0], [0, 1]]), "not a number", 5)
