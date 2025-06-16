
import unittest
import numpy as np
from definitions.generate_covariance_matrix import generate_covariance_matrix

class TestGenerateCovarianceMatrix(unittest.TestCase):
    def test_valid_generation(self):
        n = 3
        Sigma_nom, mu = generate_covariance_matrix(n)
        self.assertEqual(Sigma_nom.shape, (n, n))
        self.assertEqual(mu.shape, (n,))
        self.assertIsInstance(Sigma_nom, np.ndarray)
        self.assertIsInstance(mu, np.ndarray)

    def test_default_size(self):
        Sigma_nom, mu = generate_covariance_matrix()
        self.assertEqual(Sigma_nom.shape, (5, 5))
        self.assertEqual(mu.shape, (5,))
