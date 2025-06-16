
import random
import numpy as np

def generate_covariance_matrix(n=5):
    """
    Generates a nominal covariance matrix.

    Args:
        n: The number of assets.

    Returns:
        A tuple containing:
        - Sigma_nom: The nominal covariance matrix.
        - mu: A vector of expected returns.
    """

    random.seed(2)
    mu = [abs(random.gauss(0, 1)) / 15 for _ in range(n)]
    Sigma_nom = [[random.uniform(-0.15, 0.8) for _ in range(n)] for _ in range(n)]
    Sigma_nom = np.array(Sigma_nom)
    mu = np.array(mu)

    return Sigma_nom, mu
