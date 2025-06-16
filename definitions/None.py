
# filename: definitions/covariance_uncertainty_visualizer.py
def covariance_uncertainty_visualizer():
    """
    This function calculates and visualizes the impact of covariance uncertainty on portfolio risk.
    It allows exploration of possible covariance matrices and their effect on portfolio risk.

    Returns:
        tuple: A tuple containing the nominal covariance matrix, portfolio weights,
               worst-case standard deviation, and a list of risk samples.
    """
    import numpy as np
    import cvxpy as cp

    # Generate data for worst-case risk analysis.
    np.random.seed(2)
    n = 5
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)

    # Form and solve portfolio optimization problem.
    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()

    # Form and solve worst-case risk analysis problem.
    Sigma = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)
    risk = cp.quad_form(w.value, Sigma)
    prob = cp.Problem(
        cp.Maximize(risk),
        [Sigma == Sigma_nom + Delta, cp.diag(Delta) == 0, cp.abs(Delta) <= 0.2])
    prob.solve()

    worst_case_std_dev = cp.sqrt(risk).value

    delta = 0.2  # Uncertainty Parameter

    num_samples = 100
    risks = []
    for _ in range(num_samples):
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = Sigma_nom + Delta_sample

        # Ensure Sigma_sample is positive semi-definite
        try:
            w_val = w.value.reshape(-1, 1)
            risk_sample = w_val.T @ Sigma_sample @ w_val
            risks.append(risk_sample[0][0])  # Extract the scalar value
        except Exception as e:
            pass

    return Sigma_nom, w.value, worst_case_std_dev, risks
