
import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

def run_page2():
    st.header("Sensitivity Analysis")
    
    st.markdown(
    """
    This page demonstrates how sensitive the portfolio risk distribution is to the uncertainty parameter delta. 
    Adjust the slider below to see real-time changes in the risk distribution.
    """
    )
    
    np.random.seed(2)
    n = 5
    mu = np.abs(np.random.randn(n, 1)) / 15
    Sigma_rand = np.random.uniform(-0.15, 0.8, size=(n, n))
    Sigma_nom = Sigma_rand.T @ Sigma_rand
    
    st.subheader("Nominal Covariance Matrix Overview")
    st.write("Sigma_nom:")
    st.write(np.round(Sigma_nom, 2))
    fig_nom = px.imshow(Sigma_nom, text_auto=True, title="Nominal Covariance Matrix")
    st.plotly_chart(fig_nom)
    
    st.subheader("Portfolio Optimization Recap")
    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma_nom)
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w)==1, ret>=0.1, cp.norm(w, 1)<=2])
    prob.solve()
    st.write("Optimal portfolio weights (w):")
    st.write(np.round(w.value, 2))
    
    st.subheader("Sensitivity Analysis: Risk Distribution")
    delta = st.slider("Uncertainty Parameter (delta)", min_value=0.0, max_value=0.5, value=0.2, step=0.01, key="delta_sens")
    
    num_samples = 100
    risks = []
    for _ in range(num_samples):
        Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
        Delta_sample = np.triu(Delta_sample)
        Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
        Sigma_sample = Sigma_nom + Delta_sample
        risk_sample = w.value.reshape(-1, 1).T @ Sigma_sample @ w.value.reshape(-1, 1)
        risks.append(risk_sample[0][0])
    
    fig_risk = px.histogram(x=risks, nbins=30, title=f"Risk Distribution for delta={delta}", labels={'x': 'Portfolio Risk'})
    st.plotly_chart(fig_risk)
