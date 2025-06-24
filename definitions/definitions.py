
import numpy as np

def analyze_covariance_uncertainty(cov_matrix: np.ndarray, uncertainty_level: float, portfolio_weights: np.ndarray) -> float:
    """
    Analyzes the worst-case portfolio risk given a covariance matrix, a specified uncertainty 
    level, and portfolio weights.

    Args:
        cov_matrix (np.ndarray): Original covariance matrix of asset returns.
        uncertainty_level (float): Level of uncertainty to consider in covariance matrix (>=0).
        portfolio_weights (np.ndarray): Weights of assets in the portfolio.

    Returns:
        float: Worst-case portfolio risk considering covariance uncertainty.

    Raises:
        TypeError: If inputs are not of expected types.
        ValueError: If inputs fail validation checks.
    """
    # Type checks
    if not isinstance(cov_matrix, np.ndarray):
        raise TypeError("cov_matrix must be a numpy.ndarray")
    if not isinstance(uncertainty_level, (float, int)) or isinstance(uncertainty_level, bool):
        raise TypeError("uncertainty_level must be a float")
    if not isinstance(portfolio_weights, np.ndarray):
        raise TypeError("portfolio_weights must be a numpy.ndarray")

    # Validate covariance matrix shape & properties
    if cov_matrix.ndim != 2 or cov_matrix.shape[0] != cov_matrix.shape[1]:
        raise ValueError("cov_matrix must be a square matrix")
    n = cov_matrix.shape[0]

    if portfolio_weights.ndim != 1 or portfolio_weights.size != n:
        raise ValueError("portfolio_weights size must match cov_matrix dimensions")

    # Validate values
    if np.isnan(cov_matrix).any():
        raise ValueError("cov_matrix contains NaN values")

    if np.any(np.diag(cov_matrix) < 0):
        raise ValueError("cov_matrix has negative diagonal elements")

    if uncertainty_level < 0:
        raise ValueError("uncertainty_level must be non-negative")

    s = np.sum(portfolio_weights)
    if not np.isfinite(s) or s == 0:
        raise ValueError("Sum of portfolio_weights must be non-zero and finite")
    if not np.isclose(s, 1, atol=1e-8):
        raise ValueError("Sum of portfolio_weights must be 1 (within tolerance)")

    # Compute nominal portfolio variance
    port_var = float(portfolio_weights @ cov_matrix @ portfolio_weights)

    # Worst-case risk under Frobenius norm uncertainty:
    # worst_case_risk = sqrt(port_var) + uncertainty_level * Frobenius norm of outer product w w^T
    # Frobenius norm of wwT = ||w||^2
    w_norm_sq = float(np.dot(portfolio_weights, portfolio_weights))
    worst_case_var = port_var + 2 * uncertainty_level * np.sqrt(port_var) * w_norm_sq + (uncertainty_level * w_norm_sq) ** 2
    # Numerical safety: worst_case_var >= 0
    worst_case_var = max(worst_case_var, 0)
    return float(np.sqrt(worst_case_var))


import numpy as np

def analyze_covariance_uncertainty(cov_matrix: np.ndarray, uncertainty_level: float, portfolio_weights: np.ndarray) -> float:
    """
    Analyzes the worst-case portfolio risk given a covariance matrix, a specified uncertainty 
    level, and portfolio weights.

    Args:
        cov_matrix (np.ndarray): Original covariance matrix of asset returns.
        uncertainty_level (float): Level of uncertainty to consider in covariance matrix (>=0).
        portfolio_weights (np.ndarray): Weights of assets in the portfolio.

    Returns:
        float: Worst-case portfolio risk considering covariance uncertainty.

    Raises:
        TypeError: If inputs are not of expected types.
        ValueError: If inputs fail validation checks.
    """
    # Type checks
    if not isinstance(cov_matrix, np.ndarray):
        raise TypeError("cov_matrix must be a numpy.ndarray")
    if not isinstance(uncertainty_level, (float, int)) or isinstance(uncertainty_level, bool):
        raise TypeError("uncertainty_level must be a float")
    if not isinstance(portfolio_weights, np.ndarray):
        raise TypeError("portfolio_weights must be a numpy.ndarray")

    # Validate covariance matrix shape & properties
    if cov_matrix.ndim != 2 or cov_matrix.shape[0] != cov_matrix.shape[1]:
        raise ValueError("cov_matrix must be a square matrix")
    n = cov_matrix.shape[0]

    if portfolio_weights.ndim != 1 or portfolio_weights.size != n:
        raise ValueError("portfolio_weights size must match cov_matrix dimensions")

    # Validate values
    if np.isnan(cov_matrix).any():
        raise ValueError("cov_matrix contains NaN values")

    if np.any(np.diag(cov_matrix) < 0):
        raise ValueError("cov_matrix has negative diagonal elements")

    if uncertainty_level < 0:
        raise ValueError("uncertainty_level must be non-negative")

    s = np.sum(portfolio_weights)
    if not np.isfinite(s) or s == 0:
        raise ValueError("Sum of portfolio_weights must be non-zero and finite")
    if not np.isclose(s, 1, atol=1e-8):
        raise ValueError("Sum of portfolio_weights must be 1 (within tolerance)")

    # Compute nominal portfolio variance
    port_var = float(portfolio_weights @ cov_matrix @ portfolio_weights)

    # Worst-case risk under Frobenius norm uncertainty:
    # worst_case_risk = sqrt(port_var) + uncertainty_level * Frobenius norm of outer product w w^T
    # Frobenius norm of wwT = ||w||^2
    w_norm_sq = float(np.dot(portfolio_weights, portfolio_weights))
    worst_case_var = port_var + 2 * uncertainty_level * np.sqrt(port_var) * w_norm_sq + (uncertainty_level * w_norm_sq) ** 2
    # Numerical safety: worst_case_var >= 0
    worst_case_var = max(worst_case_var, 0)
    return float(np.sqrt(worst_case_var))
