import numpy as np

def generate_nominal_covariance_matrix(n=5):
    """
    Generates a nominal covariance matrix.

    Args:
        n: The size of the covariance matrix (n x n).

    Returns:
        A numpy array representing the nominal covariance matrix.
    """
    np.random.seed(2)
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)
    return Sigma_nom

def portfolio_optimization(mu, Sigma_nom):
    """
    Approximates portfolio optimization to minimize risk while requiring a 0.1 return.

    Args:
        mu: A numpy array representing the expected returns of the assets.
        Sigma_nom: A numpy array representing the nominal covariance matrix.

    Returns:
        A numpy array representing the approximate optimal portfolio weights.
    """
    n = Sigma_nom.shape[0]
    # Simplified approximation: equal weights
    w = np.ones(n) / n
    return w

def worst_case_risk_analysis(w, Sigma_nom, delta=0.2):
    """
    Approximates worst-case risk analysis to find the maximum risk within an uncertainty set.

    Args:
        w: A numpy array representing the approximate optimal portfolio weights.
        Sigma_nom: A numpy array representing the nominal covariance matrix.
        delta: A float representing the uncertainty parameter.

    Returns:
        A tuple containing the worst-case standard deviation and the corresponding Delta matrix.
    """
    n = Sigma_nom.shape[0]
    Delta = np.random.uniform(-delta, delta, size=(n, n))
    risk = w.T @ (Sigma_nom + Delta) @ w
    return np.sqrt(risk), Delta

def generate_random_covariance_matrix(Sigma_nom, delta):
    """
    Generates a random covariance matrix within the uncertainty set.
    """
    n = Sigma_nom.shape[0]
    Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
    Delta_sample = np.triu(Delta_sample)
    Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
    Sigma_sample = Sigma_nom + Delta_sample
    try:
        np.linalg.cholesky(Sigma_sample)
    except np.linalg.LinAlgError:
        Sigma_sample = Sigma_nom  # Fallback to nominal if not PSD
    return Sigma_sample