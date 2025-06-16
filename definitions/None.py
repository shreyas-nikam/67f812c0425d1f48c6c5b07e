
import cvxpy as cp
import numpy as np

def calculate_worst_case_risk(
    sigma_nom: np.ndarray, w: np.ndarray, delta: float
) -> float:
    '''
    Calculates the worst-case portfolio risk given a nominal covariance matrix,
    portfolio weights, and an uncertainty parameter delta.

    Args:
        sigma_nom: The nominal covariance matrix (must be positive semi-definite).
        w: The portfolio weights.
        delta: The uncertainty parameter, which defines the size of the
            uncertainty set.

    Returns:
        The worst-case portfolio risk.

    Raises:
        ValueError: If sigma_nom is not positive semi-definite or delta is
            negative or if the optimization fails.
    '''
    if delta < 0:
        raise ValueError("Delta must be non-negative.")

    n = sigma_nom.shape[0]

    # Define the CVXPY variables
    Sigma = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)

    # Define the risk
    risk = cp.quad_form(w, Sigma)

    # Define the problem
    constraints = [
        Sigma == sigma_nom + Delta,
        cp.diag(Delta) == 0,
        cp.abs(Delta) <= delta,
    ]
    problem = cp.Problem(cp.Maximize(risk), constraints)

    # Solve the problem
    try:
        problem.solve()
    except Exception as e:
        raise ValueError(f"Solver failed: {e}")

    if problem.status != cp.OPTIMAL:
        raise ValueError(
            f"Optimization failed with status: {problem.status}.  Check inputs."
        )

    return risk.value
