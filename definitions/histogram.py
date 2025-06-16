def histogram(x, nbins, title):
    """Generates a histogram to visualize the distribution of portfolio risk based on sampled covariance matrices.

    Args:
        x (list or numpy.ndarray): The data for which to plot the distribution.
        nbins (int): The number of bins in the histogram.
        title (str): The title of the chart.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object representing the histogram.
        Returns None if there is an error

    Raises:
        TypeError: if x is not a list or numpy array, nbins is not an integer, or title is not a string.
        ValueError: if nbins is not a positive integer.
    """
    import plotly.express as px
    import numpy as np

    if not isinstance(x, (list, np.ndarray)):
        raise TypeError("x must be a list or numpy array")
    if not isinstance(nbins, int):
        raise TypeError("nbins must be an integer")
    if not isinstance(title, str):
        raise TypeError("title must be a string")

    if nbins <= 0:
        raise ValueError("nbins must be a positive integer")

    try:
        fig = px.histogram(x=x, nbins=nbins, title=title)
        return fig
    except Exception as e:
        print(f"An error occurred while generating the histogram: {e}")
        return None
