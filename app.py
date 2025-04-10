
import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

# Your code goes here
page = st.sidebar.selectbox(["Overview", "Risk Analysis", "About"])

if page == "Overview":
    st.write("## Overview")
    st.markdown("This application visualizes the impact of covariance uncertainty on portfolio risk. It is based on the concepts and example code provided, focusing on the 'Worst-case risk analysis' scenario. The application allows users to explore the range of possible covariance matrices and their effect on portfolio risk through interactive visualizations and parameter adjustments.")
    st.markdown("Navigate to the 'Risk Analysis' page to explore the uncertainty in portfolio risk due to the uncertain covariance matrix")
elif page == "Risk Analysis":
    st.title("Covariance Uncertainty Visualizer")

    st.markdown("## Overview")
    st.markdown("This Streamlit application visualizes the impact of covariance uncertainty on portfolio risk. It's based on the concepts and example code provided, focusing on the 'Worst-case risk analysis' scenario. The application allows users to explore the range of possible covariance matrices and their effect on portfolio risk through interactive visualizations and parameter adjustments.")

    st.markdown("## Important Definitions, Examples, and Formulae")
    st.markdown("*   **Covariance Matrix (`Sigma`)**: A square matrix that describes the relationships between different assets in a portfolio. The diagonal elements represent the variance of each asset, while the off-diagonal elements represent the covariance between pairs of assets.")
    st.markdown("*   *Example*: A 2x2 covariance matrix might look like this: `[[0.04, 0.01], [0.01, 0.09]]`.  This shows asset 1 has a variance of 0.04, asset 2 has a variance of 0.09, and they have a covariance of 0.01.")
    st.markdown("*   **Portfolio Risk**: A measure of the potential losses in a portfolio.  It's calculated as `risk = w.T @ Sigma @ w`, where `w` is the vector of portfolio weights and `Sigma` is the covariance matrix.  Higher risk means greater potential for loss.")
    st.markdown("*   *Formula*: `risk = w.T @ Sigma @ w`")
    st.markdown("*   **Uncertainty Set (`S`)**:  A set of possible covariance matrices that the 'true' covariance matrix might lie in.  It's defined as `S = {Sigma_nom + Delta : |Delta_ij| <= delta}`, where `Sigma_nom` is the nominal covariance matrix, `Delta` is a matrix of deviations, and `delta` controls the size of the uncertainty set.")
    st.markdown("*   *Example*: If `delta` is 0.1, then each element of `Delta` can be between -0.1 and 0.1.")
    st.markdown("*   **Sensitivity Analysis**: The study of how the output of a model (e.g., portfolio risk) is affected by changes in the input parameters (e.g., `delta`).  It helps understand which parameters have the biggest impact on the results.")

    st.markdown("## Dataset Details")
    st.markdown("Using synthetic data")

    st.markdown("## Nominal Covariance Matrix")
    # Generate data for worst-case risk analysis.
    np.random.seed(2)
    n = 5
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform (-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma. T.dot (Sigma)
    st.write("Sigma_nom =")
    st.write(np.round(Sigma_nom, decimals=2))

    fig_sigma_nom = px.imshow(Sigma_nom, text_auto=True, title="Nominal Covariance Matrix (Sigma_nom)")
    st.plotly_chart(fig_sigma_nom)

    st.markdown("## Portfolio Optimization")
    st.markdown("# Form and solve portfolio optimization problem.")
    st.markdown("# Here we minimize risk while requiring a 0.1 return.")
    # Form and solve portfolio optimization problem.
    # Here we minimize risk while requiring a 0.1 return.
    w = cp.Variable(n)
    ret = mu.T @w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem (cp.Minimize (risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()
    st.write("w =")
    st.write(np.round(w.value, decimals=2))

    st.markdown("## Worst Case Delta")
    st.markdown("# Form and solve worst-case risk analysis problem.")
    Sigma = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)
    risk = cp.quad_form(w.value, Sigma)
    prob = cp.Problem(
        cp.Maximize (risk),
        [Sigma == Sigma_nom + Delta, cp.diag (Delta) == 0, cp.abs (Delta) <= 0.2])
    prob.solve()

    st.write("standard deviation =", cp.sqrt(cp.quad_form(w.value, Sigma_nom)).value)
    st.write("worst-case standard deviation =", cp.sqrt(risk).value)
    st.write("worst-case Delta =")
    st.write(np.round(Delta.value, decimals=2))

    delta = st.slider("Uncertainty Parameter (delta)", min_value=0.0, max_value=0.5, value=0.2, step=0.01)

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

    fig_risk_distribution = px.histogram(x=risks, nbins=30, title=f"Distribution of Portfolio Risk (delta={delta})")
    st.plotly_chart(fig_risk_distribution)

elif page == "About":
    st.write("## About")
    st.write("This application was created by QuantUniversity for educational purposes.")

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")
