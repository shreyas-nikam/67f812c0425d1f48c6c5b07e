import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px
import math

st.title("Worst-Case Risk Analysis and Uncertainty Set Visualization")
st.markdown("### Worst-Case Analysis Setup")

n = 5
np.random.seed(2)
mu = np.abs(np.random.randn(n, 1)) / 15
Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
Sigma_nom = Sigma.T.dot(Sigma)

# Solve portfolio optimization to obtain optimal weights
w = cp.Variable(n)
ret = mu.T @ w
risk_nom = cp.quad_form(w, Sigma_nom)
prob = cp.Problem(cp.Minimize(risk_nom), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
prob.solve()
w_opt = w.value

st.markdown("**Nominal Portfolio Risk**")
nominal_risk = math.sqrt(np.dot(w_opt, np.dot(Sigma_nom, w_opt)))
st.write("Nominal standard deviation:", np.round(nominal_risk, 2))

st.markdown("### Worst-Case Risk Analysis")
delta = st.slider("Uncertainty Parameter (delta)", min_value=0.0, max_value=0.5, value=0.2, step=0.01)

# Define and solve the worst-case risk problem
Sigma_var = cp.Variable((n, n), PSD=True)
Delta_var = cp.Variable((n, n), symmetric=True)
risk_expr = cp.quad_form(w_opt, Sigma_var)
prob_wc = cp.Problem(
    cp.Maximize(risk_expr),
    [Sigma_var == Sigma_nom + Delta_var, cp.diag(Delta_var) == 0, cp.abs(Delta_var) <= delta]
)
prob_wc.solve()

worst_risk = math.sqrt(risk_expr.value)
st.write("Worst-case standard deviation:", np.round(worst_risk, 2))
st.write("Worst-case Delta:")
st.write(np.round(Delta_var.value, decimals=2))

st.markdown("### Risk Distribution under Covariance Uncertainty")
num_samples = 100
risks = []
for _ in range(num_samples):
    Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
    Delta_sample = np.triu(Delta_sample)
    Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
    Sigma_sample = Sigma_nom + Delta_sample
    try:
        risk_sample = np.dot(w_opt, np.dot(Sigma_sample, w_opt))
        risks.append(math.sqrt(risk_sample))
    except Exception:
        pass

fig_risk_distribution = px.histogram(x=risks, nbins=30,
    title=f"Distribution of Portfolio Risk (delta={delta})",
    labels={"x": "Portfolio Risk (std dev)"})
st.plotly_chart(fig_risk_distribution)
