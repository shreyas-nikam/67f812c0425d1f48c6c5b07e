
import numpy as np
import cvxpy as cp
from typing import Tuple

def generate_nominal_covariance_matrix(n: int = 5, seed: int = 2) -> np.ndarray:
    """
    Generates a nominal covariance matrix.

    Args:
        n: The size of the covariance matrix (n x n).
        seed: The random seed for reproducibility.

    Returns:
        A numpy array representing the nominal covariance matrix.

    Raises:
        ValueError: if n is not a positive integer.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    np.random.seed(seed)
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)
    return Sigma_nom

def solve_portfolio_optimization(Sigma_nom: np.ndarray, mu: np.ndarray) -> cp.Variable:
    """
    Form and solve portfolio optimization problem.
    Here we minimize risk while requiring a 0.1 return.

    Args:
        Sigma_nom: The nominal covariance matrix.
        mu: Expected returns for each asset.

    Returns:
        The optimal portfolio weights.

    Raises:
        ValueError: if Sigma_nom is not a square matrix or mu does not have the correct dimensions.
    """
    n = Sigma_nom.shape[0]
    if Sigma_nom.shape[0] != Sigma_nom.shape[1]:
        raise ValueError("Sigma_nom must be a square matrix")
    if mu.shape[0] != n:
        raise ValueError("mu must have the same number of rows as Sigma_nom")

    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()
    return w

def calculate_worst_case_risk(Sigma_nom: np.ndarray, w: cp.Variable, delta: float = 0.2) -> Tuple[float, np.ndarray]:
    """
    Form and solve worst-case risk analysis problem.

    Args:
        Sigma_nom: The nominal covariance matrix.
        w: Optimal portfolio weights.
        delta: The uncertainty parameter.

    Returns:
        A tuple containing the worst-case standard deviation and the worst-case Delta matrix.

    Raises:
        ValueError: if delta is not between 0 and 0.5.
    """
    n = Sigma_nom.shape[0]
    if not 0 <= delta <= 0.5:
        raise ValueError("delta must be between 0 and 0.5")

    Sigma = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)
    risk = cp.quad_form(w.value, Sigma)
    prob = cp.Problem(
        cp.Maximize(risk),
        [Sigma == Sigma_nom + Delta, cp.diag(Delta) == 0, cp.abs(Delta) <= delta])
    prob.solve()
    return cp.sqrt(risk).value, Delta.value

def generate_sample_covariance_matrices(Sigma_nom: np.ndarray, delta: float = 0.2, num_samples: int = 100) -> list:
    """
    Generates sample covariance matrices within the uncertainty set.

    Args:
        Sigma_nom: The nominal covariance matrix.
        delta: The uncertainty parameter.
        num_samples: The number of sample covariance matrices to generate.

    Returns:
        A list of sample covariance matrices.

    Raises:
        ValueError: if delta is not between 0 and 0.5 or num_samples is not a positive integer.
    """
    n = Sigma_nom.shape[0]
    if not 0 <= delta <= 0.5:
        raise ValueError("delta must be between 0 and 0.5")
    if not isinstance(num_samples, int) or num_samples <= 0:
        raise ValueError("num_samples must be a positive integer")

    covariance_matrices = []
    for _ in range(num_samples):
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = Sigma_nom + Delta_sample
        covariance_matrices.append(Sigma_sample)
    return covariance_matrices

def calculate_portfolio_risk(w: np.ndarray, Sigma: np.ndarray) -> float:
    """
    Calculates portfolio risk for a given covariance matrix and weights.

    Args:
        w: Portfolio weights.
        Sigma: Covariance matrix.

    Returns:
        The portfolio risk.

    Raises:
        ValueError: if the dimensions of w and Sigma are incompatible.
    """
    if w.shape[0] != Sigma.shape[0]:
        raise ValueError("The dimensions of w and Sigma are incompatible.")

    w_val = w.reshape(-1, 1)
    risk = w_val.T @ Sigma @ w_val
    return risk[0][0]
