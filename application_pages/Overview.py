import streamlit as st

def main():
    st.title("Covariance Uncertainty Visualizer")
    st.markdown("## Overview")
    st.markdown("This Streamlit application visualizes the impact of covariance uncertainty on portfolio risk. It is based on the 'Worst-case risk analysis' scenario. Users can explore how different covariance matrices within an uncertainty set affect portfolio risk.")

    st.markdown("## Important Definitions, Examples, and Formulae")
    st.markdown("* **Covariance Matrix (`Sigma`)**: A square matrix describing relationships between assets. Diagonals represent variances while off-diagonals represent covariances.")
    st.markdown("* *Example*: A 2x2 covariance matrix: `[[0.04, 0.01], [0.01, 0.09]]`.")
    st.markdown("* **Portfolio Risk**: Calculated as `risk = w.T @ Sigma @ w`, where `w` is the weight vector. A higher risk indicates a greater potential for loss.")
    st.markdown("* **Uncertainty Set (`S`)**: Defined as `S = {Sigma_nom + Delta : |Delta_ij| <= delta}`, where `delta` controls the size of uncertainty.")
    st.markdown("* **Sensitivity Analysis**: Demonstrates how varying `delta` impacts portfolio risk.")
    st.markdown("Use the navigation in the sidebar to explore portfolio optimization and risk analysis.")
