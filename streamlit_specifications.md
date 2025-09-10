
# Streamlit Application Requirements Specification

## 1. Application Overview

This Streamlit application aims to illustrate the impact of covariance uncertainty on portfolio risk management, specifically focusing on worst-case risk scenarios. By allowing users to interact with key parameters, the application will provide a hands-on understanding of how uncertainty in covariance estimates can affect portfolio risk assessments.

**Learning Goals:**

- Gain an understanding of Covariance uncertainty demonstrated through an example.

## 2. User Interface Requirements

**2.1. Layout and Navigation Structure:**

-   The application will have a single-page layout.
-   A title will be displayed at the top of the page, explaining the purpose of the application.
-   Sections will be clearly delineated using headings and subheadings.

**2.2. Input Widgets and Controls:**

-   **Covariance Matrix Input:** A text area where users can input the covariance matrix. The application should provide a default covariance matrix as an example, prepopulating the text area.
-   **Portfolio Weights Input:** A text area for users to specify the portfolio weights. A default set of portfolio weights summing to 1 should be provided as an example.
-   **Uncertainty Level Input:** A slider or number input field that allows users to adjust the uncertainty level. The range should be from 0 to a maximum value (e.g., 0.2), with a step size (e.g., 0.01).

**2.3. Visualization Components:**

-   **Worst-Case Risk Output:** A text or metric display showing the calculated worst-case portfolio risk based on the user-provided inputs.
-   **Nominal Portfolio Risk Output:** A text or metric display showing the calculated nominal portfolio risk.
-   **Visual Comparison:** A bar chart to visualize the difference between the nominal portfolio risk and worst-case portfolio risk under different uncertainty levels.

**2.4. Interactive Elements and Feedback Mechanisms:**

-   The application should automatically recalculate and update the outputs (worst-case risk, risk difference, and bar chart) whenever the user changes the input values.
-   Input validation: Error messages should be displayed if the user provides invalid inputs, such as a non-square covariance matrix, portfolio weights that do not sum to 1, or a negative uncertainty level.

## 3. Additional Requirements

**3.1. Annotation and Tooltip Specifications:**

-   Tooltips should be added to the input widgets, explaining the purpose and expected format of each input.
-   The output display should include a brief explanation of what the worst-case risk and risk difference represent.
-   The bar chart should have axis labels and a title that clearly explains the information being displayed.

**3.2. Save the states of the fields properly so that changes are not lost**
-   Use `st.session_state` to save the states of the fields properly so that changes are not lost.

## 4. Notebook Content and Code Requirements

**4.1. Extracted Code Stubs:**

```python
import streamlit as st
import numpy as np

def analyze_covariance_uncertainty(cov_matrix: np.ndarray, uncertainty_level: float, portfolio_weights: np.ndarray) -> float:
    """
    Analyzes the worst-case portfolio risk given a covariance matrix, a specified uncertainty 
    level, and portfolio weights.

    Args:
        cov_matrix (np.ndarray): Original covariance matrix of asset returns.
        uncertainty_level (float): Level of uncertainty to consider in covariance matrix (>=0).
        portfolio_weights (np.ndarray): Weights of assets in the portfolio.

    Returns:
        float: Worst-case portfolio risk considering covariance uncertainty.

    Raises:
        TypeError: If inputs are not of expected types.
        ValueError: If inputs fail validation checks.
    """
    # Type checks
    if not isinstance(cov_matrix, np.ndarray):
        raise TypeError("cov_matrix must be a numpy.ndarray")
    if not isinstance(uncertainty_level, (float, int)) or isinstance(uncertainty_level, bool):
        raise TypeError("uncertainty_level must be a float")
    if not isinstance(portfolio_weights, np.ndarray):
        raise TypeError("portfolio_weights must be a numpy.ndarray")

    # Validate covariance matrix shape & properties
    if cov_matrix.ndim != 2 or cov_matrix.shape[0] != cov_matrix.shape[1]:
        raise ValueError("cov_matrix must be a square matrix")
    n = cov_matrix.shape[0]

    if portfolio_weights.ndim != 1 or portfolio_weights.size != n:
        raise ValueError("portfolio_weights size must match cov_matrix dimensions")

    # Validate values
    if np.isnan(cov_matrix).any():
        raise ValueError("cov_matrix contains NaN values")

    if np.any(np.diag(cov_matrix) < 0):
        raise ValueError("cov_matrix has negative diagonal elements")

    if uncertainty_level < 0:
        raise ValueError("uncertainty_level must be non-negative")

    s = np.sum(portfolio_weights)
    if not np.isfinite(s) or s == 0:
        raise ValueError("Sum of portfolio_weights must be non-zero and finite")
    if not np.isclose(s, 1, atol=1e-8):
        raise ValueError("Sum of portfolio_weights must be 1 (within tolerance)")

    # Compute nominal portfolio variance
    port_var = float(portfolio_weights @ cov_matrix @ portfolio_weights)

    # Worst-case risk under Frobenius norm uncertainty:
    # worst_case_risk = sqrt(port_var) + uncertainty_level * Frobenius norm of outer product w w^T
    # Frobenius norm of wwT = ||w||^2
    w_norm_sq = float(np.dot(portfolio_weights, portfolio_weights))
    worst_case_var = port_var + 2 * uncertainty_level * np.sqrt(port_var) * w_norm_sq + (uncertainty_level * w_norm_sq) ** 2
    # Numerical safety: worst_case_var >= 0
    worst_case_var = max(worst_case_var, 0)
    return float(np.sqrt(worst_case_var))

# Example Usage (for default values)
cov_matrix_example = np.array([
    [0.1, 0.02, 0.04],
    [0.02, 0.08, 0.01],
    [0.04, 0.01, 0.07]
])

portfolio_weights_example = np.array([0.5, 0.3, 0.2])

uncertainty_levels = [0.0, 0.05, 0.1, 0.15]

results = []
for u in uncertainty_levels:
    risk = analyze_covariance_uncertainty(cov_matrix_example, u, portfolio_weights_example)
    results.append((u, risk))
```

**4.2. Markdown Content:**

The application should include the following markdown content to explain the concepts and formulas:

```markdown
## Covariance Uncertainty and Worst-Case Portfolio Risk Analysis

In portfolio management, understanding the risk associated with asset returns is vital for making informed investment decisions. Typically, this risk is quantified using the covariance matrix of asset returns, which captures how assets move together.

However, covariance estimates are inherently uncertain due to limited historical data and changing market conditions. This uncertainty can influence portfolio risk in unpredictable ways.

This application explores the impact of **covariance uncertainty** on portfolio risk, focusing on the **worst-case risk scenario**. By considering an uncertainty level in the covariance matrix, we assess how much the portfolio risk could potentially increase beyond what is estimated under nominal conditions.

The analysis provides valuable insights to risk managers and portfolio analysts by quantifying risk under adverse covariance conditions, enabling more robust investment strategies.

## Mathematical Foundations and Business Significance

The core of portfolio risk analysis is the computation of the portfolio variance given by:

$$
	ext{Portfolio Variance} = \mathbf{w}^T \Sigma \mathbf{w}
$$

where:
- \( \mathbf{w} \) is the vector of portfolio weights,
- \( \Sigma \) is the covariance matrix of asset returns.

This variance quantifies the expected volatility of portfolio returns under the assumption that \( \Sigma \) is known exactly.

However, in practice, \( \Sigma \) is estimated and thus subject to uncertainty. To incorporate this, we consider a perturbation \( \Delta \) to the covariance matrix such that:

$$
\| \Delta \|_F \leq \epsilon
$$

where \( \| \cdot \|_F \) denotes the Frobenius norm, and \( \epsilon \) is the uncertainty level.

The worst-case portfolio variance under this uncertainty can be bounded by:

$$
	ext{Worst-case Variance} = \left( \sqrt{\mathbf{w}^T \Sigma \mathbf{w}} + \epsilon \| \mathbf{w} \mathbf{w}^T \|_F ight)^2
$$

Noting that:

$$
\| \mathbf{w} \mathbf{w}^T \|_F = \| \mathbf{w} \|^2
$$

This leads to the formula implemented in the function where the worst-case portfolio standard deviation is:

$$
\sqrt{\mathbf{w}^T \Sigma \mathbf{w} + 2 \epsilon \sqrt{\mathbf{w}^T \Sigma \mathbf{w}} \| \mathbf{w} \|^2 + \epsilon^2 \| \mathbf{w} \|^4}
$$

Business-wise, this quantifies how much the perceived risk can increase under covariance uncertainty, thus providing a more robust risk measure for portfolio management decisions.

## Interpretation of Results

By adjusting the uncertainty level, you can observe how the worst-case portfolio risk changes compared to the nominal portfolio risk. This demonstrates the importance of considering covariance uncertainty in risk management. As the uncertainty level increases, the potential for higher risk becomes more apparent.

These insights underline the importance of including covariance uncertainty in risk modeling frameworks to make more informed and prudent investment decisions.
```

**4.3. Implementation Notes:**

-   Use `st.markdown()` to display the markdown content.
-   Use `st.number_input()` or `st.slider()` for the uncertainty level input.
-   Implement input validation using `try...except` blocks to catch `ValueError` exceptions raised by the `analyze_covariance_uncertainty` function.
-   Use `st.metric()` to display the nominal and worst-case risk.
-   Use `st.bar_chart()` to compare the nominal and worst-case risk visually for a default range of uncertainty levels.
