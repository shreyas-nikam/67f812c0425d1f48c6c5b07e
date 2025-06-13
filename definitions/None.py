
import numpy as np

def generate_nominal_covariance_matrix(n, seed=2):
    """
    Generates a nominal covariance matrix.

    Args:
        n: The dimension of the covariance matrix.
        seed: Random seed for reproducibility.

    Returns:
        A numpy array representing the nominal covariance matrix.

    Raises:
        ValueError: If n is not a positive integer.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer.")

    np.random.seed(seed)
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)
    return Sigma_nom

def generate_sample_covariance_matrix(sigma_nom, delta, seed=None):
    """
    Generates a sample covariance matrix within the uncertainty set.

    Args:
        sigma_nom: The nominal covariance matrix.
        delta: The uncertainty parameter.
        seed: Random seed for reproducibility.

    Returns:
        A numpy array representing the sample covariance matrix, or None if it could not generate a PSD matrix.

    Raises:
        TypeError: If sigma_nom is not a numpy array or delta is not a float.
        ValueError: If sigma_nom is not square, delta is negative or greater than 1.
    """
    if not isinstance(sigma_nom, np.ndarray):
        raise TypeError("sigma_nom must be a numpy array.")
    if len(sigma_nom.shape) != 2 or sigma_nom.shape[0] != sigma_nom.shape[1]:
        raise ValueError("sigma_nom must be a square matrix.")
    if not isinstance(delta, float):
        raise TypeError("delta must be a float.")
    if delta < 0 or delta > 1:
        raise ValueError("delta must be between 0 and 1.")

    n = sigma_nom.shape[0]
    if seed is not None:
        np.random.seed(seed)

    for _ in range(100): # Try to generate a PSD matrix 100 times
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = sigma_nom + Delta_sample
        try:
            np.linalg.cholesky(Sigma_sample)  # Check if positive semi-definite
            return Sigma_sample
        except np.linalg.LinAlgError:
            continue  # Matrix is not positive semi-definite, try again
    return None

def calculate_portfolio_risk(w, sigma):
    """
    Calculates the portfolio risk.

    Args:
        w: The portfolio weights.
        sigma: The covariance matrix.

    Returns:
        The portfolio risk (a float).

    Raises:
        TypeError: If w or sigma are not numpy arrays.
        ValueError: If dimensions of w and sigma are incompatible.
    """
    if not isinstance(w, np.ndarray) or not isinstance(sigma, np.ndarray):
        raise TypeError("w and sigma must be numpy arrays.")
    if len(w.shape) != 1 and (len(w.shape) != 2 or w.shape[1] != 1):
        raise ValueError("w must be a 1-D array or a column vector.")
    if len(sigma.shape) != 2 or sigma.shape[0] != sigma.shape[1]:
        raise ValueError("sigma must be a square matrix.")
    if sigma.shape[0] != w.shape[0] :
        raise ValueError("The dimensions of w and sigma are incompatible.")

    if len(w.shape) == 2:
        w = w.flatten()
    return float(w.T @ sigma @ w)

def solve_portfolio_optimization_problem(mu, sigma_nom, risk_target=0.1):
    """
    Solves the portfolio optimization problem to minimize risk while requiring a target return.
    This simplified version finds a feasible solution, but not necessarily the optimal one.

    Args:
        mu: Expected returns of the assets.
        sigma_nom: Nominal covariance matrix.
        risk_target: The minimum target return.

    Returns:
        Optimal portfolio weights (numpy array), or None if a feasible solution is not found.
    """
    n = mu.shape[0]
    # Initial guess: equal weights
    w = np.ones(n) / n

    # Check constraints: sum(w) == 1 and ret >= risk_target
    ret = mu.T @ w
    if ret < risk_target:
        return None  # Infeasible: cannot achieve target return with equal weights

    # Normalize weights to sum to 1
    w = w / np.sum(w)
    return w
