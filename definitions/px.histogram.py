
import plotly.express as px
import pandas as pd
from typing import List, Union

def px_histogram(x: List[Union[int, float]], nbins: int, title: str) -> px.histogram:
    """Displays the distribution of portfolio risk values as a histogram.

    Args:
        x: The data for the histogram (portfolio risk values).
        nbins: The number of bins in the histogram.
        title: The title of the histogram.

    Returns:
        A plotly histogram object.
    """
    df = pd.DataFrame(x, columns=['risk'])
    fig = px.histogram(df, x="risk", nbins=nbins, title=title)
    return fig
