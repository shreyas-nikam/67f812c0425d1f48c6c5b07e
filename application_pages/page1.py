
import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

def run_page1():
    st.header("Worst-Case Risk Analysis")
    
    st.markdown(
    """
    This page explores worst-case risk analysis by perturbing the nominal covariance matrix within an uncertainty set.

    **How It Works:**
    - A nominal covariance matrix is generated from random data.
    - The portfolio optimization problem minimizes risk while achieving a target return.
    - Worst-case risk is computed by perturbing the covariance matrix with Delta bounded by a slider-controlled delta.
    """
    )
    
    np.random.seed(2)
    n = 5  # number of assets
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma_rand = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma_rand.T @ Sigma_rand
    
    st.subheader("Nominal Covariance Matrix")
    st.write("Sigma_nom:")
    st.write(np.round(Sigma_nom, 2))
    fig_nom = px.imshow(Sigma_nom, text_auto=True, title="Nominal Covariance Matrix")
    st.plotly_chart(fig_nom)
    
    st.subheader("Portfolio Optimization")
    st.markdown("We minimize portfolio risk while ensuring a minimum return of 0.1.")
    
    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()
    
    st.write("Optimal portfolio weights (w):")
    st.write(np.round(w.value, 2))
    
    st.subheader("Worst-Case Risk Analysis")
    st.markdown(
    """
    Vary the uncertainty parameter delta to perturb the covariance matrix:
    S = { Sigma_nom + Delta : |Delta_ij| <= delta }
    """
    )
    
    delta = st.slider("Uncertainty Parameter (delta)", min_value=0.0, max_value=0.5, value=0.2, step=0.01)
    
    Sigma_var = cp.Variable((n, n), PSD=True)
    Delta = cp.Variable((n, n), symmetric=True)
    risk_var = cp.quad_form(w.value, Sigma_var)
    prob_wc = cp.Problem(
        cp.Maximize(risk_var),
        [Sigma_var == Sigma_nom + Delta, cp.diag(Delta) == 0, cp.abs(Delta) <= delta]
    )
    prob_wc.solve()
    
    st.write("Nominal portfolio standard deviation:", np.sqrt(cp.quad_form(w.value, Sigma_nom).value))
    st.write("Worst-case portfolio standard deviation:", np.sqrt(risk_var).value)
    st.write("Perturbation (Delta) matrix:")
    st.write(np.round(Delta.value, 2))
    
    num_samples = 100
    risks = []
    for _ in range(num_samples):
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = Sigma_nom + Delta_sample
        risk_sample = w.value.reshape(-1, 1).T @ Sigma_sample @ w.value.reshape(-1, 1)
        risks.append(risk_sample[0][0])
    
    fig_hist = px.histogram(x=risks, nbins=30, title=f"Portfolio Risk Distribution (delta={delta})", labels={'x': 'Portfolio Risk'})
    st.plotly_chart(fig_hist)
