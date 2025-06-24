
# Worst Case Risk Analysis Lab

This repository contains a Streamlit application for performing worst-case risk analysis on a portfolio based on covariance uncertainty.

## Overview

The application allows users to:
- Visualize a nominal covariance matrix.
- Optimize a portfolio under constraints using convex optimization (cvxpy).
- Analyze worst-case portfolio risk by perturbing the covariance matrix within an uncertainty set.
- Perform sensitivity analysis to observe how changes in the uncertainty parameter (delta) affect the risk distribution.

## Structure

- **app.py**: Main application file with sidebar navigation.
- **application_pages/page1.py**: Contains the worst-case risk analysis page.
- **application_pages/page2.py**: Contains the sensitivity analysis page.
- **requirements.txt**: Lists all dependencies.
- **Dockerfile**: For containerizing the application.

## Running the Application

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the application:
   ```
   streamlit run app.py
   ```
3. Alternatively, build and run using Docker.
