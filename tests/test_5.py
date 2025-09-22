import pytest
import numpy as np
import plotly.express as px
import pandas as pd
from definition_98f8fd1617284a9699418e6ab2ab4b4c import sensitivity_analysis


def generate_test_data():
    n = 5  # Number of assets
    Sigma_nom = np.random.rand(n, n)
    Sigma_nom = Sigma_nom @ Sigma_nom.T  # Ensure positive semi-definite
    delta_values = [0.1, 0.2]
    w = np.ones(n) / n
    return Sigma_nom, delta_values, w

@pytest.fixture
def test_data():
    return generate_test_data()

def test_sensitivity_analysis_no_errors(test_data, monkeypatch):
    Sigma_nom, delta_values, w = test_data
    # Mock plotly.express.histogram and show to prevent actual plot generation
    monkeypatch.setattr(px, "histogram", lambda *args, **kwargs: None)
    monkeypatch.setattr(px, "imshow", lambda *args, **kwargs: None)

    try:
        sensitivity_analysis(Sigma_nom, delta_values, w)
    except Exception as e:
        pytest.fail(f"sensitivity_analysis raised an exception: {e}")

def test_sensitivity_analysis_delta_values_empty(test_data, monkeypatch):
    Sigma_nom, _, w = test_data
    delta_values = []

    monkeypatch.setattr(px, "histogram", lambda *args, **kwargs: None)
    monkeypatch.setattr(px, "imshow", lambda *args, **kwargs: None)

    try:
        sensitivity_analysis(Sigma_nom, delta_values, w)
    except Exception as e:
        pytest.fail(f"sensitivity_analysis raised an exception: {e}")

def test_sensitivity_analysis_non_numpy_input(monkeypatch):
     monkeypatch.setattr(px, "histogram", lambda *args, **kwargs: None)
     monkeypatch.setattr(px, "imshow", lambda *args, **kwargs: None)
     with pytest.raises(TypeError):
          sensitivity_analysis([[1,2],[3,4]], [0.1], [0.2, 0.8])

def test_sensitivity_analysis_incompatible_shapes(monkeypatch):
    Sigma_nom = np.array([[1, 2], [3, 4]])
    delta_values = [0.1, 0.2]
    w = np.array([0.2, 0.3, 0.5])

    monkeypatch.setattr(px, "histogram", lambda *args, **kwargs: None)
    monkeypatch.setattr(px, "imshow", lambda *args, **kwargs: None)
    with pytest.raises(ValueError):
        sensitivity_analysis(Sigma_nom, delta_values, w)
