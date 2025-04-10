# QuLab - Worst Case Risk Analysis Application

This repository contains a Streamlit multi-page application for analyzing the impact of covariance uncertainty on portfolio risk. Users can explore worst-case risk analysis in portfolio optimization by adjusting the uncertainty parameter and dynamically visualizing the effects.

## Features
- **Overview:** Explanation of key concepts in portfolio risk management.
- **Nominal Covariance Matrix & Portfolio Optimization:** Visualization of a synthetic covariance matrix and computation of optimal portfolio weights.
- **Worst-Case Risk Analysis:** Interactive slider for uncertainty (delta), worst-case risk computation, and a risk distribution histogram.

## File Structure
- **app.py:** Main entry point for the Streamlit application.
- **/pages:**
  - **01_Overview.py:** Overview and conceptual explanations.
  - **02_Optimization.py:** Nominal covariance matrix generation and portfolio optimization.
  - **03_Risk_Analysis.py:** Worst-case risk analysis with covariance uncertainty.
- **requirements.txt:** Python dependencies.
- **Dockerfile:** Docker configuration for containerized deployment.

## Getting Started

### Local Setup
1. Install dependencies:
   pip install -r requirements.txt
2. Run the application:
   streamlit run app.py

### Docker Setup
1. Build the Docker image:
   docker build -t qulabrisk .
2. Run the container:
   docker run -p 8501:8501 qulabrisk

## License
© 2025 QuantUniversity. All Rights Reserved.
