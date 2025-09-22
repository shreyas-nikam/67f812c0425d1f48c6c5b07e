
# Notebook Overview

This Jupyter Notebook provides an interactive visualization of the impact of covariance uncertainty on portfolio risk, based on the "Worst-case risk analysis" example. It allows users to explore the range of possible covariance matrices within a defined uncertainty set and observe their effect on portfolio risk distribution.

**Learning Goals:**
*   Gain a visual understanding of the range of possible covariance matrices under uncertainty.
*   Visualize the impact of covariance uncertainty on the distribution of portfolio risk.
*   Explore the sensitivity of risk to changes in uncertainty parameters.

# Code Requirements

**Expected Libraries:**

*   `cvxpy`
*   `numpy`
*   `plotly.express`
*   `pandas`

**Algorithms and Functions to be Implemented:**

1.  **Generate Nominal Covariance Matrix:** Function to generate a synthetic nominal covariance matrix (`Sigma_nom`) using `numpy`.
2.  **Generate Uncertainty Set:** Function to generate a set of covariance matrices within the uncertainty set $S = \{\Sigma_{nom} + \Delta : |\Delta_{ij}| \le \delta\}$, where $\delta$ is the uncertainty parameter, using `numpy`.
3.  **Calculate Portfolio Risk:** Function to calculate the portfolio risk (`w.T @ Sigma @ w`) for a given portfolio weight vector (`w`) and covariance matrix (`Sigma`), using `numpy`.
4.  **Risk Distribution Visualization:** Function to generate a histogram or density plot of the calculated portfolio risk values using `plotly.express`.
5.  **Heatmap Visualization:** Function to generate a heatmap visualization of the nominal covariance matrix (`Sigma_nom`) and example covariance matrices from the uncertainty set using `plotly.express`.
6.  **Sensitivity Analysis:** Function to re-calculate and re-visualize the risk distribution for different values of the uncertainty parameter (`delta`).
7.  **Portfolio Optimization:** Function to calculate the optimal portfolio weights using `cvxpy` based on the nominal covariance matrix.

**Visualizations:**

1.  **Heatmap of Nominal Covariance Matrix:** Display `Sigma_nom` as a heatmap.
2.  **Heatmaps of Uncertainty Set Samples:** Display a few sampled covariance matrices from the uncertainty set as heatmaps.
3.  **Distribution of Portfolio Risk:** Display the distribution of portfolio risk values as a histogram or density plot.
4.  **Sensitivity Analysis Plots:** Show how the risk distribution changes with different values of `delta`.
5. **Optimal Portfolio Weights bar chart:** Display a bar chart of the optimal portfolio weights `w`.

# Notebook Sections

1.  **Introduction to Covariance Uncertainty**

    *   **Markdown Cell:** Explains the concept of covariance uncertainty in portfolio risk analysis. Introduces the problem setting where the true covariance matrix $\Sigma$ is unknown but belongs to an uncertainty set $S$. Defines the portfolio risk as $risk = w^T \Sigma w$, where $w$ is the portfolio weight vector. Explains the goal of visualizing how uncertainty in $\Sigma$ affects the distribution of `risk`.
    *   **Markdown Cell:** Explains the Uncertainty Set. The uncertainty set $S$ is defined as $S = \{\Sigma_{nom} + \Delta : |\Delta_{ij}| \le \delta\}$, where $\Sigma_{nom}$ is the nominal covariance matrix, $\Delta$ is a perturbation matrix, and $\delta$ is the uncertainty parameter. The element-wise constraint $|\Delta_{ij}| \le \delta$ limits the magnitude of deviations from the nominal covariance matrix.

2.  **Import Libraries**

    *   **Code Cell:** Imports the necessary libraries: `numpy` as `np`, `cvxpy` as `cp`, `plotly.express` as `px`, and `pandas` as `pd`.

3.  **Generate Nominal Covariance Matrix**

    *   **Markdown Cell:** Explains that this section generates a synthetic nominal covariance matrix (`Sigma_nom`) using `numpy`. It outlines the steps involved: setting the random seed for reproducibility, defining the size `n` of the matrix, creating a random matrix, and calculating `Sigma_nom` as the product of the random matrix and its transpose.
    *   **Code Cell:** Implements the generation of `Sigma_nom`.
    *   **Code Cell:** Prints the generated `Sigma_nom` using `np.round(Sigma_nom, decimals=2)`.
    *   **Markdown Cell:** Explains that the code cell generated a random nominal covariance matrix, `Sigma_nom`, by multiplying a random matrix with its transpose to guarantee that it's positive semi-definite. The seed is set to ensure reproducibility.

4.  **Visualize Nominal Covariance Matrix**

    *   **Markdown Cell:** Explains that this section visualizes the nominal covariance matrix (`Sigma_nom`) as a heatmap using `plotly.express`. This provides a visual representation of the correlations between different assets.
    *   **Code Cell:** Converts `Sigma_nom` to a Pandas DataFrame and creates a heatmap using `plotly.express.imshow`. The figure should have appropriate labels and a title.
    *   **Code Cell:** Displays the heatmap using `fig.show()`.
    *   **Markdown Cell:** Explains that the heatmap shows the correlations between assets, with warmer colors indicating positive correlations and cooler colors indicating negative correlations.

5.  **Define Uncertainty Set Parameters**

    *   **Markdown Cell:** Explains that this section defines the parameters for the uncertainty set, including the uncertainty parameter `delta`.
    *   **Code Cell:** Defines the uncertainty parameter `delta` (e.g., `delta = 0.2`).
    *   **Markdown Cell:** Explains that delta represents the magnitude of the allowed perturbation in the covariance matrix elements.

6.  **Generate Uncertainty Set Samples**

    *   **Markdown Cell:** Explains that this section generates a set of covariance matrices within the uncertainty set $S$. For each matrix, a random perturbation matrix $\Delta$ is generated, subject to the constraint $|\Delta_{ij}| \le \delta$.
    *   **Code Cell:** Generates a specified number (e.g., `num_samples = 100`) of covariance matrices within the uncertainty set. Each matrix should satisfy the condition $|\Delta_{ij}| \le \delta$. Store the generated matrices in a list.
    *   **Markdown Cell:** Explains the code generated a list of covariance matrices within the uncertainty set by adding a random perturbation to the nominal covariance matrix.

7.  **Visualize Uncertainty Set Samples**

    *   **Markdown Cell:** Explains that this section visualizes a few samples of the covariance matrices from the uncertainty set as heatmaps.
    *   **Code Cell:** Selects a few (e.g., 3-5) covariance matrices from the generated list.
    *   **Code Cell:** Generates heatmaps for the selected matrices using `plotly.express.imshow` and displays them.
    *   **Markdown Cell:** Explains that these heatmaps visualize the range of possible covariance matrices within the uncertainty set.

8.  **Define Portfolio Weights**

    *   **Markdown Cell:** Explains that this section defines the portfolio weights `w`. For now, we will use an equal weight portfolio.
    *   **Code Cell:** Defines the portfolio weights `w` (e.g., `w = np.ones(n) / n`).
    *   **Markdown Cell:** Explains that `w` represents the allocation of capital to each asset in the portfolio.

9. **Portfolio Optimization using CVXPY (Nominal)**

    *   **Markdown Cell:**  This section finds the optimal portfolio weights *w* that minimize risk given a nominal covariance matrix Sigma_nom, budget constraint, minimum return target, and limit on the L1 norm of portfolio weights.  It frames it as a convex optimization problem which we solve using CVXPY. It clearly explains that the portfolio optimization problem is defined as:
        $$
        \begin{aligned}
        & \underset{w}{\text{minimize}} & w^T \Sigma_{nom} w \\
        & \text{subject to} & 1^T w = 1 \\
        & & \mu^T w \ge 0.1 \\
        & & \|w\|_1 \le 2
        \end{aligned}
        $$
        where
        * $w$ is the vector of portfolio weights,
        * $\Sigma_{nom}$ is the nominal covariance matrix,
        * $1$ is a vector of ones representing the budget constraint,
        * $\mu$ is the vector of expected returns for each asset,
        * $\|w\|_1$ is the L1 norm of the portfolio weights,
        * 0.1 is the target minimum return.
    *   **Code Cell:** Define the optimization variables, problem and constraints using `cvxpy`. Also solve the problem.
    *   **Code Cell:** Print the optimal portfolio weights `w.value` and the corresponding minimum risk `risk.value`.
    *   **Markdown Cell:** Explains that the optimal portfolio weights were found by solving a convex optimization problem. These weights minimize portfolio risk subject to the budget, return, and L1 norm constraints.

10. **Calculate Portfolio Risk Distribution**

    *   **Markdown Cell:** Explains that this section calculates the portfolio risk for each covariance matrix in the uncertainty set using the *optimized* portfolio weights obtained from the previous step. The risk is calculated using the formula $risk = w^T \Sigma w$.
    *   **Code Cell:** Calculates the portfolio risk for each covariance matrix in the uncertainty set and stores the results in a list.
    *   **Markdown Cell:** Explains the calculated portfolio risk distribution.

11. **Visualize Portfolio Risk Distribution**

    *   **Markdown Cell:** Explains that this section visualizes the distribution of the calculated portfolio risk values as a histogram or density plot using `plotly.express`.
    *   **Code Cell:** Creates a histogram or density plot of the portfolio risk values using `plotly.express.histogram` or `plotly.express.kde`.
    *   **Code Cell:** Displays the plot using `fig.show()`.
    *   **Markdown Cell:** Explains that the histogram or density plot shows the range of possible portfolio risk values given the uncertainty in the covariance matrix.

12. **Sensitivity Analysis: Impact of Delta**

    *   **Markdown Cell:** Explains that this section explores how the risk distribution changes with different values of the uncertainty parameter `delta`. This provides insights into the sensitivity of portfolio risk to the level of covariance uncertainty.
    *   **Code Cell:** Defines a range of `delta` values to explore (e.g., `delta_values = [0.1, 0.2, 0.3]`).
    *   **Code Cell:** For each `delta` value, regenerates the uncertainty set, calculates the portfolio risk distribution, and creates a corresponding histogram or density plot. Display each plot.
    *   **Markdown Cell:** Explains that the set of generated distributions shows how the range of possible portfolio risk values widens as the uncertainty parameter delta increases.

13. **Visualize Optimal Portfolio Weights**

    *   **Markdown Cell:** Explains this section visualizes the optimal portfolio weights.
    *   **Code Cell:** Creates a Pandas Series from the optimized weights `w.value` for better plotting
    *   **Code Cell:** Creates a bar chart of the optimal portfolio weights using `plotly.express`.
    *   **Code Cell:** Displays the plot using `fig.show()`.
    *   **Markdown Cell:** Explains the generated chart.

14. **Conclusion**

    *   **Markdown Cell:** Summarizes the key findings of the notebook, emphasizing the impact of covariance uncertainty on portfolio risk and the importance of considering this uncertainty in portfolio management. Mentions how this visualization helps understand the "Worst-case risk analysis" example by providing an intuitive tool.

