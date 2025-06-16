
import numpy as np
import cvxpy as cp
import plotly.express as px

def generate_nominal_covariance_matrix(n: int = 5) -> np.ndarray:
    """
    Generates a nominal covariance matrix.
    Args:
        n: The size of the matrix (n x n).
    Returns:
        A numpy array representing the nominal covariance matrix.
    """
    np.random.seed(2)
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)
    return Sigma_nom

def solve_portfolio_optimization(mu: np.ndarray, Sigma_nom: np.ndarray) -> cp.Variable:
    """
    Solves the portfolio optimization problem.
    Args:
        mu: Expected returns for each asset.
        Sigma_nom: Nominal covariance matrix.
    Returns:
        A cvxpy Variable representing the optimal portfolio weights.
    """
    n = Sigma_nom.shape[0]
    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()
    return w

def calculate_worst_case_risk(w: cp.Variable, Sigma_nom: np.ndarray, delta: float = 0.2) -> tuple[float, np.ndarray]:
    """
    Calculates the worst-case risk given the portfolio weights and uncertainty parameter.
    Args:
        w: Portfolio weights (cvxpy Variable).
        Sigma_nom: Nominal covariance matrix.
        delta: Uncertainty parameter.
    Returns:
        A tuple containing the worst-case standard deviation and the corresponding Delta matrix.
    """
    n = Sigma_nom.shape[0]
    Sigma = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)
    risk = cp.quad_form(w, Sigma)
    prob = cp.Problem(
        cp.Maximize(risk),
        [Sigma == Sigma_nom + Delta, cp.diag(Delta) == 0, cp.abs(Delta) <= delta])
    prob.solve()

    worst_case_std_dev = np.sqrt(risk.value)
    worst_case_delta = Delta.value

    return worst_case_std_dev, worst_case_delta

def generate_risk_samples(w: np.ndarray, Sigma_nom: np.ndarray, delta: float, num_samples: int = 100) -> list[float]:
    """
    Generates a list of portfolio risk samples based on the uncertainty parameter delta.
    Args:
        w: Portfolio weights.
        Sigma_nom: Nominal covariance matrix.
        delta: Uncertainty parameter.
        num_samples: Number of risk samples to generate.
    Returns:
        A list of portfolio risk samples.
    """
    n = Sigma_nom.shape[0]
    risks = []
    for _ in range(num_samples):
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = Sigma_nom + Delta_sample

        # Ensure Sigma_sample is positive semi-definite
        try:
            w_val = w.reshape(-1, 1)
            risk_sample = w_val.T @ Sigma_sample @ w_val
            risks.append(risk_sample[0][0])  # Extract the scalar value
        except Exception as e:
            pass
    return risks

def create_risk_distribution_plot(risks: list[float], delta: float) -> plotly.graph_objects.Figure:
    """
    Creates a histogram of the portfolio risk distribution.
    Args:
        risks: A list of portfolio risk samples.
        delta: The uncertainty parameter (delta).
    Returns:
        A plotly figure object.
    """
    fig_risk_distribution = px.histogram(x=risks, nbins=30, title=f"Distribution of Portfolio Risk (delta={delta})")
    return fig_risk_distribution
