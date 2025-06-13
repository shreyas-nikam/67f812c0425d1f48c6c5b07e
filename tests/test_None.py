
import unittest
import numpy as np
import math
import statistics

def generate_covariance_data(n: int = 5, seed: int = 2):
    """Generates synthetic covariance data.

    Args:
        n: The number of assets.
        seed: The random seed for reproducibility.

    Returns:
        A tuple containing the mean returns (mu) and the nominal covariance matrix (Sigma_nom).
    """
    np.random.seed(seed)
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)
    return mu, Sigma_nom


def solve_portfolio_optimization(mu: np.ndarray, Sigma_nom: np.ndarray):
    """Solves the portfolio optimization problem (simplified).

    Args:
        mu: The mean returns.
        Sigma_nom: The nominal covariance matrix.

    Returns:
        The optimal portfolio weights (w). Returns equal weights for simplicity.
    """
    n = mu.shape[0]
    w = np.ones(n) / n  # Assign equal weights to each asset
    return w

def calculate_worst_case_risk(w: np.ndarray, Sigma_nom: np.ndarray, delta: float = 0.2):
    """Calculates the worst-case portfolio risk given covariance uncertainty (simplified).

    Args:
        w: The portfolio weights.
        Sigma_nom: The nominal covariance matrix.
        delta: The uncertainty parameter.

    Returns:
        A tuple containing the worst-case standard deviation and the corresponding Delta matrix.
    """
    n = Sigma_nom.shape[0]
    Delta = np.random.uniform(-delta, delta, size=(n, n))
    Sigma_worst = Sigma_nom + Delta
    risk = w.T @ Sigma_worst @ w
    worst_case_std_dev = np.sqrt(risk)
    return worst_case_std_dev, Delta


def calculate_risk_distribution(w: np.ndarray, Sigma_nom: np.ndarray, delta: float = 0.2, num_samples: int = 100):
    """Calculates the distribution of portfolio risk under covariance uncertainty.

    Args:
        w: The portfolio weights.
        Sigma_nom: The nominal covariance matrix.
        delta: The uncertainty parameter.
        num_samples: The number of samples to generate.

    Returns:
        A list of portfolio risk values.
    """
    n = Sigma_nom.shape[0]
    risks = []
    for _ in range(num_samples):
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = Sigma_nom + Delta_sample
        try:
            w_val = w.reshape(-1, 1)
            risk_sample = w_val.T @ Sigma_sample @ w_val
            risks.append(risk_sample[0][0])  # Extract the scalar value
        except Exception as e:
            pass
    return risks

class TestPortfolioFunctions(unittest.TestCase):

    def test_generate_covariance_data(self):
        mu, Sigma_nom = generate_covariance_data(n=5)
        self.assertEqual(mu.shape, (5, 1))
        self.assertEqual(Sigma_nom.shape, (5, 5))

    def test_solve_portfolio_optimization(self):
        mu, Sigma_nom = generate_covariance_data(n=5)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        self.assertIsInstance(w, np.ndarray)
        self.assertEqual(len(w), 5)

    def test_calculate_worst_case_risk(self):
        mu, Sigma_nom = generate_covariance_data(n=5)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        worst_case_std_dev, _ = calculate_worst_case_risk(w, Sigma_nom)
        self.assertGreaterEqual(worst_case_std_dev, 0)

    def test_calculate_risk_distribution(self):
        mu, Sigma_nom = generate_covariance_data(n=5)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        risks = calculate_risk_distribution(w, Sigma_nom)
        self.assertIsInstance(risks, list)
        self.assertEqual(len(risks), 100)

    def test_generate_covariance_data_diff_n(self):
        mu, Sigma_nom = generate_covariance_data(n=10)
        self.assertEqual(mu.shape, (10, 1))
        self.assertEqual(Sigma_nom.shape, (10, 10))

    def test_calculate_worst_case_risk_diff_delta(self):
        mu, Sigma_nom = generate_covariance_data(n=5)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        worst_case_std_dev, _ = calculate_worst_case_risk(w, Sigma_nom, delta = 0.3)
        self.assertGreaterEqual(worst_case_std_dev, 0)

    def test_calculate_risk_distribution_diff_num_samples(self):
        mu, Sigma_nom = generate_covariance_data(n=5)
        w = solve_portfolio_optimization(mu, Sigma_nom)
        risks = calculate_risk_distribution(w, Sigma_nom, num_samples = 50)
        self.assertIsInstance(risks, list)
        self.assertEqual(len(risks), 50)
