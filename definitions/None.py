
import numpy as np
import cvxpy as cp
from typing import Tuple

def generate_nominal_covariance_matrix(n: int = 5) -> np.ndarray:
    """Generates a nominal covariance matrix."""
    np.random.seed(2)
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)
    return Sigma_nom

def calculate_portfolio_risk(w: np.ndarray, Sigma: np.ndarray) -> float:
    """Calculates the portfolio risk."""
    return w.T @ Sigma @ w

def generate_uncertainty_set_sample(Sigma_nom: np.ndarray, delta: float, n: int = 5) -> np.ndarray:
    """Generates a sample covariance matrix within the uncertainty set."""
    Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
    Delta_sample = np.triu(Delta_sample)
    Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
    Sigma_sample = Sigma_nom + Delta_sample
    try:
        np.linalg.cholesky(Sigma_sample)
        return Sigma_sample
    except np.linalg.LinAlgError:
        return None

def optimize_portfolio(Sigma_nom: np.ndarray, mu: np.ndarray) -> np.ndarray:
    """Optimizes the portfolio weights to minimize risk while requiring a 0.1 return."""
    n = Sigma_nom.shape[0]
    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()
    return w.value

def worst_case_risk_analysis(w: np.ndarray, Sigma_nom: np.ndarray, delta: float) -> Tuple[float, np.ndarray]:
    """Performs worst-case risk analysis."""
    n = Sigma_nom.shape[0]
    Sigma = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)
    risk = cp.quad_form(w, Sigma)
    prob = cp.Problem(
        cp.Maximize(risk),
        [Sigma == Sigma_nom + Delta, cp.diag(Delta) == 0, cp.abs(Delta) <= delta])
    prob.solve()
    return np.sqrt(risk.value), Delta.value
