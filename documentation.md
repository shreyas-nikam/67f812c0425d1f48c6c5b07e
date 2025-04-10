id: 67f812c0425d1f48c6c5b07e_documentation
summary: Worst Case Risk Analysis Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab Codelab: Exploring Worst-Case Risk Analysis

## Introduction to QuLab and Worst-Case Risk Analysis
Duration: 00:05

Welcome to the QuLab codelab! This codelab will guide you through the functionalities of the QuLab Streamlit application, a tool designed for understanding and visualizing worst-case risk analysis in portfolio management.

In financial modeling, particularly in portfolio optimization and risk management, we often rely on estimates of covariance matrices to quantify portfolio risk. However, these estimates are inherently uncertain and sensitive to market fluctuations and data limitations. Ignoring this uncertainty can lead to underestimation of risk and potentially flawed investment decisions.

QuLab addresses this critical issue by incorporating the concept of **covariance uncertainty** into risk analysis. It allows users to explore how uncertainty in the covariance matrix can impact portfolio risk, moving beyond traditional nominal risk assessments to a more robust and realistic worst-case scenario analysis.

This codelab will cover the following key concepts and functionalities within QuLab:

* **Understanding Covariance Uncertainty**: Learn how uncertainty in covariance matrices affects portfolio risk.
* **Nominal Portfolio Optimization**: Explore basic portfolio optimization using a nominal covariance matrix.
* **Worst-Case Risk Analysis**: Analyze portfolio risk under the most adverse covariance matrix within a defined uncertainty set.
* **Sensitivity Analysis**: Investigate how the level of uncertainty impacts the range of possible portfolio risks.
* **Interactive Visualization**: Utilize interactive plots to visualize covariance matrices and risk distributions.

By the end of this codelab, you will have a solid understanding of how QuLab can be used to perform robust risk analysis and make more informed investment decisions in the face of market uncertainty. Let's dive in!

## Overview Page: Grasping the Fundamentals
Duration: 00:10

The first page of QuLab, **Overview**, lays the foundation for understanding the core concepts behind worst-case risk analysis. It provides essential definitions, examples, and formulas that are crucial for navigating the application.

Let's examine the content of `pages/01_Overview.py`:

```python
import streamlit as st

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
```

This page uses `streamlit` library to present information in markdown format.

**Key Takeaways from the Overview Page:**

* **Covariance Matrix (Sigma)**: The page clearly defines the covariance matrix, explaining its role in representing asset relationships and providing a simple 2x2 example.
* **Portfolio Risk Formula**: The fundamental formula for portfolio risk calculation, `risk = w.T @ Sigma @ w`, is presented, highlighting the dependency of risk on portfolio weights (`w`) and the covariance matrix (`Sigma`).
* **Uncertainty Set (S)**: This is a crucial concept. The page defines the uncertainty set `S` as a range of possible covariance matrices around a nominal covariance matrix (`Sigma_nom`). The uncertainty is controlled by the parameter `delta`.  `Delta` represents the perturbation matrix added to the nominal covariance matrix, and the absolute value of each element `Delta_ij` is bounded by `delta`.
* **Sensitivity Analysis**:  The Overview page introduces the idea that the application will perform sensitivity analysis by varying `delta` to observe its impact on portfolio risk.

<aside class="positive">
Understanding these definitions is <b>essential</b> for interpreting the results on the subsequent pages. Pay close attention to the concept of the <b>uncertainty set</b> and how <b>delta</b> controls the level of uncertainty.
</aside>

By navigating to the **Overview** page in the sidebar, you can always refer back to these fundamental concepts as you explore the more advanced functionalities of QuLab.

## Optimization Page: Portfolio Construction with Nominal Covariance
Duration: 00:15

The **Optimization** page in QuLab demonstrates a standard portfolio optimization process using a **nominal covariance matrix**. This page serves as a baseline before we delve into worst-case risk analysis. It showcases how to construct an optimized portfolio based on traditional methods.

Let's examine the code in `pages/02_Optimization.py`:

```python
import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

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
```

**Functionality Breakdown:**

1. **Import Libraries**: The code imports necessary libraries:
    * `streamlit` for creating the web application.
    * `numpy` for numerical operations, especially matrix manipulations.
    * `cvxpy` for convex optimization, used to solve the portfolio optimization problem.
    * `plotly.express` for creating interactive plots.

2. **Nominal Covariance Matrix Generation**:
   ```python
   np.random.seed(2)
   n = 5
   mu = np.abs(np.random.randn(n, 1)) / 15
   Sigma = np.random.uniform(-0.15, 0.8, size=(n, n))
   Sigma_nom = Sigma.T.dot(Sigma)
   ```
   This section generates synthetic data:
    * `n = 5`: Defines the number of assets as 5.
    * `mu`: Generates random expected returns (`mu`) for each asset.
    * `Sigma`: Creates a random matrix `Sigma`.
    * `Sigma_nom = Sigma.T.dot(Sigma)`: Calculates the nominal covariance matrix `Sigma_nom` by multiplying `Sigma` with its transpose, ensuring it's a symmetric positive semi-definite matrix, a valid covariance matrix.

3. **Display Nominal Covariance Matrix**:
   ```python
   st.write("Sigma_nom =")
   st.write(np.round(Sigma_nom, decimals=2))

   fig_sigma_nom = px.imshow(Sigma_nom, text_auto=True, title="Nominal Covariance Matrix (Sigma_nom)")
   st.plotly_chart(fig_sigma_nom)
   ```
   * `st.write(np.round(Sigma_nom, decimals=2))`: Displays the nominal covariance matrix rounded to 2 decimal places in a readable format.
   * `px.imshow(...)`: Generates a heatmap visualization of the `Sigma_nom` matrix using `plotly.express`. The `text_auto=True` argument displays the numerical values on the heatmap, making it easier to interpret.
   * `st.plotly_chart(...)`: Renders the generated heatmap in the Streamlit application.

4. **Portfolio Optimization**:
   ```python
   w = cp.Variable(n)
   ret = mu.T @ w
   risk = cp.quad_form(w, Sigma_nom)
   prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
   prob.solve()

   st.write("Optimal portfolio weights (w) =")
   st.write(np.round(w.value, decimals=2))
   ```
   This is the core optimization part:
    * `w = cp.Variable(n)`: Defines `w` as a CVXPY variable representing the portfolio weights (a vector of size `n`).
    * `ret = mu.T @ w`: Defines the portfolio return as the dot product of the transpose of expected returns `mu` and the weights `w`.
    * `risk = cp.quad_form(w, Sigma_nom)`: Defines the portfolio risk using the quadratic form, `w.T * Sigma_nom * w`, where `Sigma_nom` is the nominal covariance matrix.
    * `prob = cp.Problem(...)`: Formulates the convex optimization problem. The objective is to minimize `risk` subject to the following constraints:
        * `cp.sum(w) == 1`: The sum of portfolio weights must equal 1 (fully invested portfolio).
        * `ret >= 0.1`: The portfolio return must be greater than or equal to 10% (an example return target).
        * `cp.norm(w, 1) <= 2`: The L1 norm of weights is less than or equal to 2. This constraint, also known as a budget constraint or turnover constraint, can help in diversifying the portfolio and preventing extreme weight allocations.
    * `prob.solve()`: Solves the defined optimization problem using CVXPY's solver.
    * `st.write("Optimal portfolio weights (w) =")`: Displays the calculated optimal portfolio weights `w.value` rounded to 2 decimal places.

**Running the Optimization Page:**

When you navigate to the **Optimization** page in QuLab, you will see:

1. **Nominal Covariance Matrix (Sigma_nom)**: Displayed as both numerical values and a heatmap. This visualization helps understand the correlations and variances within the nominal covariance matrix.
2. **Optimal Portfolio Weights (w)**: The calculated optimal portfolio weights that minimize risk under the given constraints, based on the `Sigma_nom`.

<aside class="positive">
The <b>Optimization</b> page demonstrates a standard Markowitz-style portfolio optimization. It's important to note that the results here are based on the <b>nominal covariance matrix</b>, which is assumed to be known with certainty in traditional portfolio theory. The next page will address the uncertainty in this covariance matrix.
</aside>

## Risk Analysis Page: Exploring Worst-Case Scenarios
Duration: 00:20

The **Risk Analysis** page is the core of QuLab, where we delve into **worst-case risk analysis** by considering the uncertainty set defined earlier. This page allows you to explore how portfolio risk can vary when the true covariance matrix can deviate from the nominal one.

Let's examine the code in `pages/03_Risk_Analysis.py`:

```python
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
```

**Functionality Breakdown:**

1. **Setup and Nominal Risk Calculation**:
   ```python
   # ... (Data generation and nominal portfolio optimization from Optimization page) ...
   w_opt = w.value

   st.markdown("**Nominal Portfolio Risk**")
   nominal_risk = math.sqrt(np.dot(w_opt, np.dot(Sigma_nom, w_opt)))
   st.write("Nominal standard deviation:", np.round(nominal_risk, 2))
   ```
   This section re-uses the data generation and portfolio optimization code from the **Optimization** page to obtain the optimal portfolio weights `w_opt` based on the nominal covariance matrix. It then calculates and displays the **nominal portfolio risk** (standard deviation) using `Sigma_nom` and `w_opt`. This serves as a reference point for comparison with the worst-case risk.

2. **Uncertainty Parameter Slider**:
   ```python
   delta = st.slider("Uncertainty Parameter (delta)", min_value=0.0, max_value=0.5, value=0.2, step=0.01)
   ```
   A Streamlit slider is introduced to allow users to interactively control the **uncertainty parameter `delta`**.  As you move the slider, the application will recalculate and display the worst-case risk and the risk distribution, demonstrating sensitivity analysis.

3. **Worst-Case Risk Optimization**:
   ```python
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
   ```
   This is the core of the worst-case risk analysis:
    * `Sigma_var = cp.Variable((n, n), PSD=True)`:  Defines `Sigma_var` as a CVXPY variable representing the uncertain covariance matrix. `PSD=True` constraint ensures that `Sigma_var` remains positive semi-definite (a valid covariance matrix).
    * `Delta_var = cp.Variable((n, n), symmetric=True)`: Defines `Delta_var` as the perturbation matrix, constrained to be symmetric.
    * `risk_expr = cp.quad_form(w_opt, Sigma_var)`: Defines the risk expression using the optimized portfolio weights `w_opt` (from the nominal optimization) and the variable covariance matrix `Sigma_var`.
    * `prob_wc = cp.Problem(...)`: Formulates the **worst-case risk maximization problem**. The objective is to **maximize** `risk_expr` (portfolio risk) subject to the following constraints:
        * `Sigma_var == Sigma_nom + Delta_var`:  `Sigma_var` is defined as the sum of the nominal covariance matrix and the perturbation matrix.
        * `cp.diag(Delta_var) == 0`: The diagonal elements of `Delta_var` are constrained to be zero. This means we are only considering uncertainty in the covariance terms (off-diagonal elements) and assuming variances (diagonal elements) are known.
        * `cp.abs(Delta_var) <= delta`:  The absolute value of each element in `Delta_var` is bounded by the uncertainty parameter `delta`, defining the uncertainty set.
    * `prob_wc.solve()`: Solves this maximization problem to find the covariance matrix within the uncertainty set that maximizes portfolio risk.
    * `worst_risk = math.sqrt(risk_expr.value)`: Calculates the worst-case standard deviation.
    * `st.write(...)`: Displays the **worst-case standard deviation** and the **worst-case perturbation matrix `Delta_var.value`**.

4. **Risk Distribution Visualization**:
   ```python
   # ... (Sampling and risk calculation loop) ...

   fig_risk_distribution = px.histogram(...)
   st.plotly_chart(fig_risk_distribution)
   ```
   This section visualizes the distribution of portfolio risk under covariance uncertainty:
    * **Sampling Loop**:  It iterates `num_samples = 100` times. In each iteration:
        * `Delta_sample = np.random.uniform(-delta, delta, size=(n, n))`: Generates a random perturbation matrix `Delta_sample` within the bounds defined by `delta`.
        * `Delta_sample = np.triu(...)`: Ensures symmetry of `Delta_sample` and sets the diagonal to zero as per the constraints in the worst-case optimization problem.
        * `Sigma_sample = Sigma_nom + Delta_sample`: Creates a sample covariance matrix `Sigma_sample` within the uncertainty set.
        * `risk_sample = np.dot(...)`: Calculates the portfolio risk for this `Sigma_sample` using the optimal weights `w_opt`.
        * `risks.append(...)`: Stores the calculated risk value.
    * **Histogram Plot**:
        * `px.histogram(...)`: Generates a histogram of the collected `risks` values using `plotly.express`.
        * `st.plotly_chart(...)`: Renders the histogram, showing the distribution of portfolio risk for different covariance matrices within the uncertainty set defined by the current `delta` value.

**Interacting with the Risk Analysis Page:**

When you interact with the **Risk Analysis** page by moving the `delta` slider:

1. **Nominal Risk**: The nominal risk (calculated with `Sigma_nom`) remains constant as it's independent of `delta`.
2. **Worst-Case Risk**: The "Worst-case standard deviation" value will change. As you increase `delta` (wider uncertainty set), the worst-case risk generally increases, showing the potential for higher risk under greater covariance uncertainty.
3. **Worst-case Delta**: The "Worst-case Delta" matrix represents the perturbation that leads to the maximum portfolio risk within the defined uncertainty set.
4. **Risk Distribution Histogram**: The histogram will dynamically update to show the distribution of portfolio risks for the currently selected `delta` value. As `delta` increases, you'll typically observe a wider distribution, indicating a larger range of possible portfolio risks.

<aside class="negative">
It's crucial to understand that the <b>worst-case risk</b> is not necessarily the most <i>likely</i> risk. It represents the <b>maximum possible risk</b> within the defined uncertainty set. The risk distribution histogram provides a more comprehensive view of the range of potential risks and their likelihood.
</aside>

<aside class="positive">
By using the <b>delta slider</b> and observing the changes in worst-case risk and the risk distribution, you can perform a powerful <b>sensitivity analysis</b> to understand how covariance uncertainty impacts portfolio risk. This is invaluable for making robust investment decisions that account for model risk.
</aside>

## Conclusion: QuLab for Robust Risk Management
Duration: 00:05

Congratulations on completing the QuLab codelab! You've now explored the key functionalities of the QuLab Streamlit application and gained insights into worst-case risk analysis.

**Key takeaways from QuLab:**

* **Visualizing Covariance Uncertainty**: QuLab effectively visualizes the impact of covariance uncertainty on portfolio risk, moving beyond traditional point estimates.
* **Worst-Case Risk Assessment**: The application provides a framework for calculating and understanding worst-case portfolio risk, offering a more conservative and robust approach to risk management.
* **Interactive Sensitivity Analysis**: The `delta` slider enables interactive sensitivity analysis, allowing users to explore how different levels of covariance uncertainty affect risk outcomes.
* **Risk Distribution Exploration**: The risk distribution histogram provides a richer understanding of the range of potential portfolio risks and their likelihood under covariance uncertainty.

**Importance of QuLab and Worst-Case Risk Analysis:**

In real-world financial markets, covariance matrices are never known with perfect certainty. Using nominal covariance matrices without considering uncertainty can lead to:

* **Underestimation of Risk**: Potentially leading to portfolios that are riskier than anticipated.
* **Suboptimal Portfolio Decisions**: Resulting in portfolios that are not truly robust to market fluctuations and model errors.

QuLab and the principles of worst-case risk analysis help mitigate these issues by:

* **Providing a more realistic risk assessment**: By considering a set of possible covariance matrices rather than just a single nominal estimate.
* **Enabling robust portfolio optimization**: Allowing for the construction of portfolios that are less sensitive to covariance uncertainty.
* **Improving decision-making under uncertainty**: Providing valuable insights into the potential range of risk outcomes.

QuLab serves as a valuable educational tool and a practical demonstration of how to incorporate worst-case risk analysis into portfolio management. By understanding and utilizing tools like QuLab, developers and financial professionals can build more robust and reliable risk management systems.

This codelab provides a foundational understanding of QuLab.  Further exploration and experimentation with different parameter settings and data inputs will deepen your understanding and allow you to leverage the full potential of this application for your own risk analysis needs.

