
import pytest
import plotly.express as px
from definitions.px import px_histogram
from typing import List, Union

def test_px_histogram_empty_list():
    with pytest.raises(ValueError):
        px_histogram(x=[], nbins=10, title="Empty List Test")

def test_px_histogram_positive_values():
    data = [1, 2, 3, 4, 5]
    fig = px_histogram(x=data, nbins=5, title="Positive Values Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "Positive Values Test"

def test_px_histogram_negative_values():
    data = [-1, -2, -3, -4, -5]
    fig = px_histogram(x=data, nbins=5, title="Negative Values Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "Negative Values Test"

def test_px_histogram_mixed_values():
    data = [-1, 0, 1, 2, -2]
    fig = px_histogram(x=data, nbins=5, title="Mixed Values Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "Mixed Values Test"

def test_px_histogram_float_values():
    data = [1.1, 2.2, 3.3, 4.4, 5.5]
    fig = px_histogram(x=data, nbins=5, title="Float Values Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "Float Values Test"

def test_px_histogram_large_nbins():
    data = [1, 2, 3, 4, 5]
    fig = px_histogram(x=data, nbins=100, title="Large Nbins Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "Large Nbins Test"

def test_px_histogram_duplicate_values():
    data = [1, 1, 2, 2, 3, 3]
    fig = px_histogram(x=data, nbins=3, title="Duplicate Values Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "Duplicate Values Test"

def test_px_histogram_zero_nbins():
     with pytest.raises(ValueError):
        px_histogram(x=[1, 2, 3], nbins=0, title="Zero Nbins Test")

def test_px_histogram_one_value():
    data = [1]
    fig = px_histogram(x=data, nbins=1, title="One Value Test")
    assert fig.data[0]['type'] == 'histogram'
    assert fig.layout.title.text == "One Value Test"

