# src/QRALib/viz/sensitivity.py
import plotly.graph_objects as go
from typing import Dict, Any

def plot_morris(Si: Dict[str, Any], top_n: int = None) -> go.Figure:
    """
    Plot a Morris indices table or bar chart.

    Parameters
    ----------
    Si : dict
        SALib Morris result dict with keys 'names','mu_star','mu_star_conf','sigma'.
    top_n : int, optional
        Number of top parameters to show. Defaults to all.
    """
    names = Si["names"]
    mu_star = Si["mu_star"]
    mu_star_conf = Si["mu_star_conf"]
    sigma = Si["sigma"]

    # sort descending by mu_star
    idx = (-np.array(mu_star)).argsort()
    if top_n:
        idx = idx[:top_n]

    fig = go.Figure(data=[
        go.Table(
            header=dict(values=["Parameter", "μ*", "σ*", "σ"], align="left"),
            cells=dict(values=[
                [names[i] for i in idx],
                [round(mu_star[i],4)    for i in idx],
                [round(mu_star_conf[i],4) for i in idx],
                [round(sigma[i],4)      for i in idx]
            ], align="left")
        )
    ])
    fig.update_layout(title="Morris Sensitivity Indices")
    return fig

def plot_sobol(Si: Dict[str, Any], top_n: int = None) -> go.Figure:
    """
    Plot a Sobol indices table.

    Parameters
    ----------
    Si : dict
        SALib Sobol result dict with keys 'names','S1','S1_conf','ST','ST_conf'.
    top_n : int, optional
        Number of top parameters to show. Defaults to all.
    """
    names = Si["names"]
    S1 = Si["S1"]
    S1_conf = Si["S1_conf"]
    ST = Si["ST"]
    ST_conf = Si["ST_conf"]

    idx = (-np.array(S1)).argsort()
    if top_n:
        idx = idx[:top_n]

    fig = go.Figure(data=[
        go.Table(
            header=dict(values=["Parameter","S1","S1_conf","ST","ST_conf"], align="left"),
            cells=dict(values=[
                [names[i] for i in idx],
                [round(S1[i],4)     for i in idx],
                [round(S1_conf[i],4) for i in idx],
                [round(ST[i],4)     for i in idx],
                [round(ST_conf[i],4) for i in idx],
            ], align="left")
        )
    ])
    fig.update_layout(title="Sobol Sensitivity Indices")
    return fig
