
import numpy as np
import unittest

class TestPortfolioFunctions(unittest.TestCase):

    def test_generate_nominal_covariance_matrix(self):
        # Test case 1: Valid input
        n = 5
        sigma_nom = generate_nominal_covariance_matrix(n)
        self.assertEqual(sigma_nom.shape, (n, n))

        # Test case 2: Invalid input (n <= 0)
        with self.assertRaises(ValueError):
            generate_nominal_covariance_matrix(0)

        # Test case 3: Invalid input (n not an integer)
        with self.assertRaises(ValueError):
            generate_nominal_covariance_matrix(1.5)

    def test_generate_sample_covariance_matrix(self):
        # Test case 1: Valid input
        n = 5
        sigma_nom = generate_nominal_covariance_matrix(n)
        delta = 0.2
        sigma_sample = generate_sample_covariance_matrix(sigma_nom, delta)
        if sigma_sample is not None:
            self.assertEqual(sigma_sample.shape, (n, n))

        # Test case 2: Invalid input (sigma_nom not a numpy array)
        with self.assertRaises(TypeError):
            generate_sample_covariance_matrix("not a numpy array", 0.2)

        # Test case 3: Invalid input (sigma_nom not square)
        sigma_nom_non_square = np.array([[1, 2], [3, 4], [5, 6]])
        with self.assertRaises(ValueError):
            generate_sample_covariance_matrix(sigma_nom_non_square, 0.2)

        # Test case 4: Invalid input (delta not a float)
        n = 5
        sigma_nom = generate_nominal_covariance_matrix(n)
        with self.assertRaises(TypeError):
            generate_sample_covariance_matrix(sigma_nom, "not a float")

        # Test case 5: Invalid input (delta < 0)
        n = 5
        sigma_nom = generate_nominal_covariance_matrix(n)
        with self.assertRaises(ValueError):
            generate_sample_covariance_matrix(sigma_nom, -0.1)

        # Test case 6: Invalid input (delta > 1)
        n = 5
        sigma_nom = generate_nominal_covariance_matrix(n)
        with self.assertRaises(ValueError):
            generate_sample_covariance_matrix(sigma_nom, 1.1)

    def test_calculate_portfolio_risk(self):
        # Test case 1: Valid input
        n = 5
        sigma = generate_nominal_covariance_matrix(n)
        w = np.ones(n) / n
        risk = calculate_portfolio_risk(w, sigma)
        self.assertIsInstance(risk, float)

        # Test case 2: Invalid input (w not a numpy array)
        with self.assertRaises(TypeError):
            calculate_portfolio_risk("not a numpy array", sigma)

        # Test case 3: Invalid input (sigma not a numpy array)
        w = np.ones(n) / n
        with self.assertRaises(TypeError):
            calculate_portfolio_risk(w, "not a numpy array")

        # Test case 4: Invalid input (w and sigma incompatible dimensions)
        sigma = generate_nominal_covariance_matrix(n)
        w = np.ones(n + 1) / (n + 1)
        with self.assertRaises(ValueError):
            calculate_portfolio_risk(w, sigma)

    def test_solve_portfolio_optimization_problem(self):
        # Test case 1: Valid input
        n = 5
        mu = np.abs(np.random.randn(n, 1)) / 15
        sigma_nom = generate_nominal_covariance_matrix(n)
        w = solve_portfolio_optimization_problem(mu, sigma_nom)
        if w is not None:
            self.assertEqual(w.shape, (n,))

        # Test case 2: Infeasible problem
        mu = np.zeros(n)  # Zero returns make the problem infeasible
        sigma_nom = generate_nominal_covariance_matrix(n)
        w = solve_portfolio_optimization_problem(mu, sigma_nom)
        self.assertIsNone(w)
