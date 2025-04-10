import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

def main():
    st.title("Portfolio Optimization and Nominal Covariance Matrix")
    st.markdown("### Nominal Covariance Matrix")

    # Generate synthetic dataset
    np.random.seed(2)
    n = 5
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma.T.dot(Sigma)

    st.write("Sigma_nom =")
    st.write(np.round(Sigma_nom, decimals=2))

    fig_sigma_nom = px.imshow(Sigma_nom, text_auto=True, title="Nominal Covariance Matrix (Sigma_nom)")
    st.plotly_chart(fig_sigma_nom)

    st.markdown("### Portfolio Optimization")
    # Solve portfolio optimization to minimize risk subject to return and weight constraints
    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
    prob.solve()

    st.write("Optimal portfolio weights (w) =")
    st.write(np.round(w.value, decimals=2))
