
import streamlit as st

st.set_page_config(page_title="Worst Case Risk Analysis", layout="wide")
st.sidebar.image("https://via.placeholder.com/150")
st.sidebar.divider()
st.title("Worst Case Risk Analysis Lab")
st.divider()

st.markdown(
"""
# Worst Case Risk Analysis Lab

This lab visualizes the impact of covariance uncertainty on portfolio risk. It allows you to adjust the uncertainty parameter (delta) interactively to observe its effect on the portfolio risk distribution.

### Business Logic:
- **Nominal Covariance Matrix Visualization:** Displays a heatmap of the nominal covariance matrix.
- **Risk Analysis:** Optimizes a portfolio using convex optimization to minimize risk while achieving a target return and computes worst-case risk.
- **Sensitivity Analysis:** Lets users adjust the uncertainty parameter (delta) to see real-time changes in the risk distribution via interactive visualizations using Plotly.
"""
)

page = st.sidebar.selectbox(label="Navigation", options=["Worst-Case Risk Analysis", "Sensitivity Analysis"])

if page == "Worst-Case Risk Analysis":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Sensitivity Analysis":
    from application_pages.page2 import run_page2
    run_page2()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("This demonstration is solely for educational use and illustration. Any reproduction requires prior written consent from QuantUniversity.")
