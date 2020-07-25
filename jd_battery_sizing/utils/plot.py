import pandas as pd

import plotly.express as px


def series_plot(df: pd.DataFrame, x: str, y: str, title: str = None, **kwargs):
    return px.line(df, x=x, y=y, title=title)


def scatter_plot(df: pd.DataFrame, x: str, y: str, title: str = None, **kwargs):
    return None
