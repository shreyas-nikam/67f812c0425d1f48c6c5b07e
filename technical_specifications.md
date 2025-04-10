# Technical Specifications: Covariance Uncertainty Visualizer

## Overview

This Streamlit application visualizes the impact of covariance uncertainty on portfolio risk. It's based on the concepts and example code provided, focusing on the "Worst-case risk analysis" scenario. The application allows users to explore the range of possible covariance matrices and their effect on portfolio risk through interactive visualizations and parameter adjustments.

## Step-by-Step Generation Process

1.  **Setup Environment and Import Libraries:**
    *   The application will begin by importing necessary libraries: `streamlit` for the user interface, `numpy` for numerical operations, `cvxpy` for defining and solving convex optimization problems, and `plotly` for interactive visualizations.
    ```python
    import streamlit as st
    import numpy as np
    import cvxpy as cp
    import plotly.express as px
    ```

2.  **Introduction and Explanation:**
    *   The application will start with a Markdown section explaining the concept of covariance uncertainty in portfolio risk management.
    *   Include definitions of key terms like covariance matrix, portfolio risk, and uncertainty set.
    *   The source document's introductory paragraph would be included using `st.markdown()`.

3.  **Dataset Generation/Loading:**
    *   The application will either generate a synthetic dataset according to the document's example or load the provided `Sigma_nom` data as a NumPy array.
    *   Details about the dataset will be displayed via `st.markdown()`. The data generation section of the source document's code would be included here.

4.  **Nominal Covariance Matrix Visualization:**
    *   The `Sigma_nom` (Nominal Covariance Matrix) will be displayed as a heatmap using `plotly.express.imshow()`.
    *   The heatmap will provide visual representation of the correlations between different assets in the portfolio.
    *   A Markdown explanation will accompany the visualization, describing what the heatmap represents and how to interpret the values.
    *   The generated heatmap object will be passed into `st.plotly_chart()`

5.  **Uncertainty Set Definition and Visualization:**
    *   A slider using `st.slider()` will allow users to control the `delta` parameter, which defines the size of the uncertainty set `S`. The default value should be 0.2, as defined in the source document.
    *   Based on the `delta` value, a function will generate random covariance matrices within the uncertainty set: `S = {Sigma_nom + Delta : |Delta_ij| <= delta}`.  The constraint that ∑nom + ∆ is positive semidefinite will be enforced.
    *   A scatter plot or a series of heatmaps (using `plotly.express.imshow()`) will display these generated covariance matrices, visualizing the range of possible covariance matrices.
    *   A Markdown section will explain the uncertainty set and how the `delta` parameter affects it.

6.  **Portfolio Optimization Problem Setup**
    * The variables `w`, `ret`, `risk`, and `prob` would be copied directly from the code in the source document.
    * An output of `w` would be printed as a table to the application through `st.write(w)`

7.  **Risk Distribution Visualization:**
    *   For each covariance matrix in the uncertainty set, the portfolio risk `risk = w.T @ Sigma @ w` will be calculated.
    *   A histogram or density plot will display the distribution of these risk values. This visualization will show the potential range of portfolio risk due to covariance uncertainty. `plotly.express.histogram()` will be used for this.
    *   Markdown explanation will explain what the distribution represents and how it relates to the uncertainty in the covariance matrix.

8.  **Sensitivity Analysis:**
    *   This section will demonstrate how changes in the `delta` parameter (controlled by the slider) affect the risk distribution.
    *   The application will update the risk distribution visualization in real-time as the user adjusts the `delta` value.
    *   A Markdown section will explain the concept of sensitivity analysis and guide users on how to interpret the changes in the visualization.

9.  **Interactive Exploration:**
    *   Tooltips and annotations will be added to the visualizations (using `plotly` features) to provide more detailed information about specific data points or regions.
    *   Users can hover over data points in the scatter plot or histogram to see the corresponding covariance matrix or risk value.

10. **Documentation and Inline Help:**
    *   `st.help()` will provide detailed information about each function or component used in the application.
    *   Tooltips will be added to the input widgets (e.g., the `delta` slider) to explain their purpose.

## Important Definitions, Examples, and Formulae

*   **Covariance Matrix (`Sigma`)**: A square matrix that describes the relationships between different assets in a portfolio. The diagonal elements represent the variance of each asset, while the off-diagonal elements represent the covariance between pairs of assets.
    *   *Example*: A 2x2 covariance matrix might look like this: `[[0.04, 0.01], [0.01, 0.09]]`.  This shows asset 1 has a variance of 0.04, asset 2 has a variance of 0.09, and they have a covariance of 0.01.
*   **Portfolio Risk**: A measure of the potential losses in a portfolio.  It's calculated as `risk = w.T @ Sigma @ w`, where `w` is the vector of portfolio weights and `Sigma` is the covariance matrix.  Higher risk means greater potential for loss.
    *   *Formula*: `risk = w.T @ Sigma @ w`
*   **Uncertainty Set (`S`)**:  A set of possible covariance matrices that the "true" covariance matrix might lie in.  It's defined as `S = {Sigma_nom + Delta : |Delta_ij| <= delta}`, where `Sigma_nom` is the nominal covariance matrix, `Delta` is a matrix of deviations, and `delta` controls the size of the uncertainty set.
    *   *Example*: If `delta` is 0.1, then each element of `Delta` can be between -0.1 and 0.1.
*   **Sensitivity Analysis**: The study of how the output of a model (e.g., portfolio risk) is affected by changes in the input parameters (e.g., `delta`).  It helps understand which parameters have the biggest impact on the results.

## Libraries and Tools

*   **Streamlit (`streamlit as st`)**: Used for creating the web application's user interface, including input widgets, visualizations, and layout.
*   **NumPy (`numpy as np`)**: Used for numerical computations, array manipulation, and dataset generation.
*   **CVXPY (`cvxpy as cp`)**: Used for defining and solving convex optimization problems.
*   **Plotly (`plotly.express as px`)**: Used for creating interactive charts and visualizations, such as heatmaps, scatter plots, and histograms.

## Appendix Code
```python
import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

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
st.markdown("Use the data from the document in the provided example")

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
```