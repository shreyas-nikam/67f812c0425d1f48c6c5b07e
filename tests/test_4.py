import pytest
import numpy as np
import plotly.express as px
from definition_5ace1b05ca05485291f432737f4f06b8 import visualize_covariance_matrix

@pytest.fixture
def sample_sigma():
    """Generates a sample covariance matrix for testing."""
    return np.array([[1, 0.5], [0.5, 1]])

def test_visualize_covariance_matrix_returns_figure(sample_sigma):
    """Test that the function returns a plotly figure."""
    title = "Test Covariance Matrix"
    fig = visualize_covariance_matrix(sample_sigma, title)
    assert isinstance(fig, type(px.imshow(sample_sigma))), "Function should return a plotly figure"

def test_visualize_covariance_matrix_handles_non_square_matrix():
    """Test that the function raises an error when the input matrix is not square."""
    sigma = np.array([[1, 2, 3], [4, 5, 6]])
    title = "Non-Square Matrix"
    with pytest.raises(ValueError) as excinfo:
        visualize_covariance_matrix(sigma, title)
    assert "Input matrix must be square" in str(excinfo.value)

def test_visualize_covariance_matrix_handles_non_numeric_matrix():
    """Test that the function raises an error when the input matrix is not numeric."""
    sigma = np.array([['a', 'b'], ['c', 'd']])
    title = "Non-Numeric Matrix"
    with pytest.raises(TypeError) as excinfo:
        visualize_covariance_matrix(sigma, title)
    assert "must be real number, not str" in str(excinfo.value)

def test_visualize_covariance_matrix_empty_matrix():
    """Test that the function handles an empty matrix."""
    sigma = np.array([])
    title = "Empty Matrix"
    with pytest.raises(ValueError) as excinfo:
        visualize_covariance_matrix(sigma, title)
    assert "Cannot reshape array of size 0 into shape" in str(excinfo.value)
