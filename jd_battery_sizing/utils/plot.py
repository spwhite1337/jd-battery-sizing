import pandas as pd

import plotly.express as px


def series_plot(df: pd.DataFrame, x: str, y: str, title: str = None):
    return px.line(df, x=x, y=y, title=title)
