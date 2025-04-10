id: 67f812c0425d1f48c6c5b07e_documentation
summary: Worst Case Risk Analysis Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab Codelab: Visualizing Covariance Uncertainty in Portfolio Risk

This codelab will guide you through the QuLab application, a Streamlit-based tool designed to visualize the impact of covariance uncertainty on portfolio risk. You'll learn how the application utilizes concepts from portfolio optimization and risk analysis to demonstrate the effects of uncertain covariance matrices on portfolio performance. This application is based on the concept of worst-case risk analysis. By the end of this codelab, you'll understand the key functionalities of the application, the underlying mathematical concepts, and how to interact with the application to explore different scenarios.

## Understanding the Core Concepts
Duration: 00:05

Before diving into the application, let's clarify the fundamental concepts:

*   **Covariance Matrix (Σ)**: A square matrix representing the relationships between different assets in a portfolio. Diagonal elements are variances, and off-diagonal elements are covariances.
*   **Portfolio Risk**: The potential for losses in a portfolio, calculated as `risk = w.T @ Sigma @ w`, where `w` is the vector of portfolio weights.
*   **Uncertainty Set (S)**: A set of possible covariance matrices within which the 'true' covariance matrix might lie. It's defined as `S = {Sigma_nom + Delta : |Delta_ij| <= delta}`, where `Sigma_nom` is the nominal covariance matrix, `Delta` represents deviations, and `delta` controls the uncertainty size.
*   **Worst-Case Risk Analysis**: A technique to determine the maximum possible risk a portfolio can face, given the uncertainty in the covariance matrix.
*   **Sensitivity Analysis**: The study of how the output of a model (e.g., portfolio risk) is affected by changes in the input parameters (e.g., `delta`).

## Application Overview
Duration: 00:03

The QuLab application has three main sections, accessible through the sidebar:

1.  **Overview**: Provides a brief introduction to the application and its purpose.
2.  **Risk Analysis**: The core of the application, allowing you to visualize and analyze the impact of covariance uncertainty on portfolio risk.
3.  **About**: Information about the application and QuantUniversity.

## Navigating to the Risk Analysis Page
Duration: 00:01

Select "Risk Analysis" from the sidebar to access the main interactive component of the application.

## Exploring the Risk Analysis Page
Duration: 00:10

The Risk Analysis page is structured as follows:

*   **Introduction**: An overview of the page's purpose and the concepts it demonstrates.
*   **Important Definitions, Examples, and Formulae**: Explanations of key terms and equations used in the application.
*   **Dataset Details**: Information about the data used (in this case, synthetic data).
*   **Nominal Covariance Matrix**: Displays and visualizes the nominal covariance matrix (Sigma\_nom) used as a starting point for the analysis.
*   **Portfolio Optimization**: Shows the portfolio optimization process, including the calculation of portfolio weights (w) based on the nominal covariance matrix.
*   **Worst Case Delta**: Presents the worst-case deviation (Delta) and its impact on portfolio risk.
*   **Uncertainty Parameter (delta) Slider**: An interactive slider that allows you to adjust the level of uncertainty in the covariance matrix.
*   **Distribution of Portfolio Risk**: A histogram visualizing the distribution of portfolio risk based on the uncertainty parameter (delta).

## Understanding the Nominal Covariance Matrix and Portfolio Optimization
Duration: 00:10

The application generates a nominal covariance matrix (`Sigma_nom`) using `numpy`.  This matrix represents the estimated relationships between the assets in the portfolio *before* considering any uncertainty.

The application then performs a simplified portfolio optimization.  It calculates the optimal portfolio weights (`w`) that minimize risk, subject to constraints such as a minimum return target (0.1) and a limit on the portfolio's leverage (`cp.norm(w, 1) <= 2`). The `cvxpy` library is used to solve this optimization problem. The calculated portfolio weights are displayed on the screen.

```python
import cvxpy as cp
import numpy as np

# Number of assets
n = 5

# Expected returns (mu) - Generate random data
mu = np.abs(np.random.randn(n, 1)) / 15

# Generate a random covariance matrix (Sigma)
Sigma = np.random.uniform (-0.15, 0.8, size=(n, n))
Sigma_nom = Sigma. T.dot (Sigma)

# Portfolio optimization
w = cp.Variable(n)  # Portfolio weights
ret = mu.T @ w        # Portfolio return
risk = cp.quad_form(w, Sigma_nom) # Portfolio risk

# Define the optimization problem
prob = cp.Problem (cp.Minimize (risk), [cp.sum(w) == 1, ret >= 0.1, cp.norm(w, 1) <= 2])
prob.solve()
```

## Analyzing the Worst-Case Delta
Duration: 00:15

The application calculates the "worst-case Delta," which represents the deviation from the nominal covariance matrix that would maximize portfolio risk. This is done by solving another optimization problem using `cvxpy`.  The goal is to find a `Delta` matrix, within the defined uncertainty set, that, when added to `Sigma_nom`, results in the highest possible portfolio risk. The calculated worst-case delta is displayed on the screen.

```python
Sigma = cp.Variable((n, n), PSD=True)
Delta = cp.Variable((n, n), symmetric=True)
risk = cp.quad_form(w.value, Sigma) # w.value are the optimal weights calcualted in the previous step
prob = cp.Problem(
    cp.Maximize (risk),
    [Sigma == Sigma_nom + Delta, cp.diag (Delta) == 0, cp.abs (Delta) <= 0.2])
prob.solve()
```

<aside class="negative">
<b>Note:</b> The worst-case Delta calculation is constrained to ensure the resulting covariance matrix remains positive semi-definite (PSD). This is crucial for the validity of the risk calculations.
</aside>

## Interacting with the Uncertainty Parameter (delta) Slider
Duration: 00:15

The `delta` slider is the key interactive element of the application. By adjusting the value of `delta`, you control the size of the uncertainty set. A larger `delta` means a wider range of possible covariance matrices, leading to greater uncertainty in portfolio risk.

As you move the slider, the application generates a sample of covariance matrices within the uncertainty set (defined by `delta`). For each sample, it calculates the portfolio risk using the previously determined optimal portfolio weights (`w`).

```python
delta = st.slider("Uncertainty Parameter (delta)", min_value=0.0, max_value=0.5, value=0.2, step=0.01)

num_samples = 100
risks = []
for _ in range(num_samples):
    Delta_sample = np.random.uniform(-delta, delta, size=(n, n))
    Delta_sample = np.triu(Delta_sample)
    Delta_sample = Delta_sample + Delta_sample.T - np.diag(np.diag(Delta_sample))
    Sigma_sample = Sigma_nom + Delta_sample
    try:
      w_val = w.value.reshape(-1, 1)
      risk_sample = w_val.T @ Sigma_sample @ w_val
      risks.append(risk_sample[0][0])  # Extract the scalar value
    except Exception as e:
      pass
```

## Analyzing the Distribution of Portfolio Risk
Duration: 00:10

The histogram displays the distribution of portfolio risk values obtained from the Monte Carlo simulation described above. As you increase `delta`, you'll observe the following:

*   **Wider Distribution**: The range of possible risk values widens, indicating greater uncertainty.
*   **Shift in Mean**: The average risk value may shift, reflecting the potential for higher risk under uncertainty.
*   **Shape Changes**: The shape of the distribution may change, revealing how the uncertainty affects the likelihood of different risk levels.

By observing these changes, you can gain insights into the sensitivity of your portfolio's risk to covariance uncertainty.

## Exploring the "About" Page
Duration: 00:02

Navigate to the "About" page to find information about the application's creators and its purpose.

## Conclusion
Duration: 00:02

This codelab provided a comprehensive guide to the QuLab application. You learned about the key concepts, the application's structure, and how to interact with the interactive elements to visualize the impact of covariance uncertainty on portfolio risk. By understanding these concepts, you can use QuLab as an educational tool to explore the challenges of portfolio management in the face of uncertain market conditions. Remember that this is a simplified demonstration for educational purposes. Real-world portfolio management involves more complex models and data.
