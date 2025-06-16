
import unittest
import numpy as np
import cvxpy as cp
from definitions.covariance_uncertainty_visualizer import (
    generate_nominal_covariance_matrix,
    solve_portfolio_optimization,
    calculate_worst_case_risk,
    generate_risk_samples,
    create_risk_distribution_plot,
)

class TestCovarianceUncertaintyVisualizer(unittest.TestCase):
    def test_generate_nominal_covariance_matrix(self):
        n = 3
        Sigma_nom = generate_nominal_covariance_matrix(n)
        self.assertEqual(Sigma_nom.shape, (n, n))
        self.assertTrue(np.all(np.linalg.eigvals(Sigma_nom) >= 0))

    def test_solve_portfolio_optimization(self):
        n = 3
        mu = np.abs(np.random.randn(n, 1)) / 15
        Sigma_nom = generate_nominal_covariance_matrix(n)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        self.assertIsInstance(w, cp.Variable)

    def test_calculate_worst_case_risk(self):
        n = 3
        mu = np.abs(np.random.randn(n, 1)) / 15
        Sigma_nom = generate_nominal_covariance_matrix(n)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        w_value = np.array([0.3, 0.4, 0.3]) # setting a value, since the cvxpy variable doesn't have a value
        worst_case_std_dev, worst_case_delta = calculate_worst_case_risk(w_value, Sigma_nom)
        self.assertIsInstance(worst_case_std_dev, float)
        self.assertEqual(worst_case_delta.shape, (n, n))

    def test_generate_risk_samples(self):
        n = 3
        mu = np.abs(np.random.randn(n, 1)) / 15
        Sigma_nom = generate_nominal_covariance_matrix(n)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        w_value = np.array([0.3, 0.4, 0.3])
        risks = generate_risk_samples(w_value, Sigma_nom, delta=0.1, num_samples=5)
        self.assertIsInstance(risks, list)
        self.assertEqual(len(risks), 5)

    def test_create_risk_distribution_plot(self):
        risks = [0.01, 0.02, 0.03, 0.04, 0.05]
        fig = create_risk_distribution_plot(risks, delta=0.1)
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()
