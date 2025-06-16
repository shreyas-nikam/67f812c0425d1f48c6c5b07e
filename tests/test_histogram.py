import unittest
import numpy as np
from definitions.histogram import histogram

class TestHistogram(unittest.TestCase):

    def test_valid_input(self):
        data = [1, 2, 3, 4, 5]
        nbins = 5
        title = "Test Histogram"
        fig = histogram(data, nbins, title)
        self.assertTrue(fig is not None)

    def test_empty_data(self):
        data = []
        nbins = 5
        title = "Empty Histogram"
        fig = histogram(data, nbins, title)
        self.assertTrue(fig is not None)

    def test_numpy_array_input(self):
        data = np.array([1, 2, 3, 4, 5])
        nbins = 5
        title = "NumPy Histogram"
        fig = histogram(data, nbins, title)
        self.assertTrue(fig is not None)

    def test_invalid_nbins_type(self):
        data = [1, 2, 3, 4, 5]
        nbins = "5"
        title = "Invalid nbins"
        with self.assertRaises(TypeError):
            histogram(data, nbins, title)

    def test_invalid_title_type(self):
        data = [1, 2, 3, 4, 5]
        nbins = 5
        title = 123
        with self.assertRaises(TypeError):
            histogram(data, nbins, title)

    def test_invalid_data_type(self):
        data = 123
        nbins = 5
        title = "Invalid data"
        with self.assertRaises(TypeError):
            histogram(data, nbins, title)

    def test_non_positive_nbins(self):
        data = [1, 2, 3, 4, 5]
        nbins = 0
        title = "Non-positive nbins"
        with self.assertRaises(ValueError):
            histogram(data, nbins, title)

    def test_negative_data(self):
        data = [-1, -2, -3, -4, -5]
        nbins = 5
        title = "Negative Data Histogram"
        fig = histogram(data, nbins, title)
        self.assertTrue(fig is not None)

if __name__ == '__main__':
    unittest.main()
