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