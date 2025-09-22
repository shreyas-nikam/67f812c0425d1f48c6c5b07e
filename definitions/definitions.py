import numpy as np

def generate_nominal_covariance_matrix(n):
    """Generates a synthetic nominal covariance matrix."""
    if n <= 0:
        raise Exception("n must be greater than 0")
    A = np.random.rand(n, n)
    Sigma_nom = np.dot(A, A.T)
    return Sigma_nom

import numpy as np

def generate_uncertainty_set(Sigma_nom, delta, num_samples):
    """Generates a set of covariance matrices within the uncertainty set.
    Args:
        Sigma_nom: The nominal covariance matrix.
        delta: The uncertainty parameter.
        num_samples: The number of covariance matrices to generate.
    Returns:
        A list of numpy arrays.
    """
    if not isinstance(Sigma_nom, np.ndarray):
        raise TypeError("Sigma_nom must be a numpy array")
    if not isinstance(delta, (int, float)):
        raise TypeError("delta must be a number")

    uncertainty_set = []
    for _ in range(num_samples):
        Delta = np.random.uniform(low=-delta, high=delta, size=Sigma_nom.shape)
        Sigma = Sigma_nom + Delta
        uncertainty_set.append(Sigma)
    return uncertainty_set

import numpy as np

            def calculate_portfolio_risk(w, Sigma):
                """Calculates portfolio risk.
                Args:
                    w (np.array): Portfolio weights.
                    Sigma (np.array): Covariance matrix.
                Returns:
                    float: Portfolio risk.
                """
                w = np.asarray(w)
                Sigma = np.asarray(Sigma)

                if Sigma.shape[0] != Sigma.shape[1]:
                    raise ValueError("Covariance matrix must be square.")

                if w.shape[0] != Sigma.shape[0]:
                    raise ValueError("Weight vector and covariance matrix must have compatible dimensions.")
                
                risk = w.T @ Sigma @ w
                return float(risk)

import plotly.express as px
import numpy as np

def visualize_risk_distribution(risk_values):
    """Generates a histogram of portfolio risk values using plotly.express.
    Args:
        risk_values: A list or numpy array of portfolio risk values.
    Returns:
        A plotly figure object.
    """
    fig = px.histogram(risk_values, nbins=30, title='Distribution of Portfolio Risk')
    return fig

import plotly.express as px
import numpy as np

def visualize_covariance_matrix(Sigma, title):
    """Generates a heatmap visualization of the covariance matrix using plotly.express.
    Args:
        Sigma: A numpy array representing the covariance matrix.
        title: The title of the heatmap.
    Returns:
        A plotly figure object.
    """
    if Sigma.size == 0:
        raise ValueError("Cannot reshape array of size 0 into shape")

    if Sigma.ndim != 2 or Sigma.shape[0] != Sigma.shape[1]:
        raise ValueError("Input matrix must be square")

    if not np.issubdtype(Sigma.dtype, np.number):
        raise TypeError("Input matrix must be numeric")

    fig = px.imshow(Sigma, title=title, color_continuous_scale="Viridis")
    return fig

import numpy as np
import plotly.express as px
import pandas as pd

def sensitivity_analysis(Sigma_nom, delta_values, w):
    """Re-calculates and re-visualizes the risk distribution for different values of the uncertainty parameter (delta).

    Args:
        Sigma_nom: The nominal covariance matrix (numpy array).
        delta_values: A list of delta values to explore.
        w: A numpy array representing the portfolio weight vector.

    Returns:
        None (displays plots directly).
    """

    if not isinstance(Sigma_nom, np.ndarray) or not isinstance(w, np.ndarray):
        raise TypeError("Sigma_nom and w must be numpy arrays.")

    if Sigma_nom.shape[0] != Sigma_nom.shape[1]:
        raise ValueError("Sigma_nom must be a square matrix.")

    if Sigma_nom.shape[0] != len(w):
        raise ValueError("Incompatible shapes between Sigma_nom and w.")
    
    portfolio_variances = []

    for delta in delta_values:
        Sigma_delta = Sigma_nom * (1 + delta)
        portfolio_variance = w @ Sigma_delta @ w
        portfolio_variances.append(portfolio_variance)

    if portfolio_variances:
        df = pd.DataFrame({'Delta': delta_values, 'Portfolio Variance': portfolio_variances})
        fig = px.line(df, x='Delta', y='Portfolio Variance', title='Sensitivity Analysis of Portfolio Variance')
        fig.show()

import cvxpy as cp
import numpy as np

def optimize_portfolio(Sigma_nom, mu):
    """Calculates the optimal portfolio weights using cvxpy subject to budget, return, and L1 norm constraints.
    Args:
        Sigma_nom: The nominal covariance matrix.
        mu: A numpy array of expected returns for each asset.
    Output:
        A numpy array representing the optimal portfolio weights.
    """
    if not isinstance(Sigma_nom, np.ndarray) or not isinstance(mu, np.ndarray):
        raise TypeError("Inputs must be numpy arrays.")

    if Sigma_nom.shape[0] != Sigma_nom.shape[1]:
        raise ValueError("Covariance matrix must be square.")

    if len(mu) != Sigma_nom.shape[0]:
        raise ValueError("mu and Sigma_nom must have compatible dimensions.")

    n = len(mu)
    w = cp.Variable(n)
    gamma = cp.Parameter(nonneg=True)
    gamma.value = 0.1 # Set risk aversion

    ret = mu @ w
    risk = cp.quad_form(w, Sigma_nom)
    l1_norm = cp.norm(w, 1) # Encourage sparsity

    objective = cp.Maximize(ret - gamma * risk)
    constraints = [cp.sum(w) == 1, w >= 0]

    problem = cp.Problem(objective, constraints)
    try:
        problem.solve()
    except cp.SolverError:
        raise cp.SolverError("Solver failed. Check if the covariance matrix is positive semi-definite.")

    return w.value

import numpy as np

def calculate_risk_distribution(uncertainty_set, w):
    """Calculates portfolio risk for each covariance matrix in the uncertainty set.

    Args:
        uncertainty_set: A list of covariance matrices (NumPy arrays).
        w: The portfolio weights (NumPy array).

    Returns:
        A list of portfolio risk values.
    """
    risks = []
    if not uncertainty_set:
        return risks

    if not isinstance(w, np.ndarray):
        raise TypeError("Weights must be a NumPy array.")

    for covariance_matrix in uncertainty_set:
        if not isinstance(covariance_matrix, np.ndarray):
            raise TypeError("Covariance matrix must be a NumPy array.")
            
        if covariance_matrix.shape[0] != covariance_matrix.shape[1]:
            raise ValueError("Covariance matrix must be square.")

        if covariance_matrix.shape[0] != len(w):
            raise ValueError("Weight dimensions must match covariance matrix dimensions.")

        try:
            risk = w @ covariance_matrix @ w.T
            risks.append(risk)
        except TypeError:
             raise TypeError("Covariance matrix must contain numeric values.")

    return risks

import numpy as np
import plotly.graph_objects as go

def visualize_optimal_weights(w):
    """Generates a bar chart of the optimal portfolio weights using plotly.express.
    Args: 
        w: A numpy array representing the optimal portfolio weights.
    Returns: 
        A plotly figure object.
    Raises:
        TypeError: If w is not a numpy array.
        ValueError: If w is empty or contains infinite values.
    """
    if not isinstance(w, np.ndarray):
        raise TypeError("Weights must be a numpy array.")
    if w.size == 0:
        raise ValueError("Weights array cannot be empty.")
    if np.any(np.isinf(w)):
        raise ValueError("Weights cannot contain infinite values.")

    fig = go.Figure(data=[go.Bar(x=[f'Asset {i+1}' for i in range(len(w))], y=w)])
    fig.update_layout(title='Optimal Portfolio Weights',
                      xaxis_title='Assets',
                      yaxis_title='Weight')
    return fig