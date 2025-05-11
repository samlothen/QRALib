# src/QRALib/viz/tornado.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any

def plot_tornado(data: Dict[str, Any], attribute: str) -> go.Figure:
    """
    Single-attribute Tornado chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['negative_variation'],
        y=data['id'],
        name='Lower bound (5th pct)',
        orientation='h',
    ))
    fig.add_trace(go.Bar(
        x=data['positive_variation'],
        y=data['id'],
        name='Upper bound (95th pct)',
        orientation='h',
    ))
    fig.update_layout(
        title=f"Tornado: {attribute}",
        barmode='overlay',
        xaxis_title='Variation in Mean ALE',
        yaxis_title='Risk ID'
    )
    return fig


def plot_ale_variation(
    data_single: Dict[str, Any],
    data_frequency: Dict[str, Any]
) -> go.Figure:
    """
    Two‐panel Tornado chart for ALE: single risk impact vs. frequency.
    """
    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        subplot_titles=("Impact Variation", "Frequency Variation"),
        horizontal_spacing=0.1,
    )
    # Left panel: single_risk_impact
    fig.add_trace(
        go.Bar(
            x=data_single['negative_variation'],
            y=data_single['id'],
            name='Impact 5th pct',
            orientation='h',
            marker_color='crimson'
        ), row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=data_single['positive_variation'],
            y=data_single['id'],
            name='Impact 95th pct',
            orientation='h',
            marker_color='steelblue'
        ), row=1, col=1
    )
    # Right panel: frequency
    fig.add_trace(
        go.Bar(
            x=data_frequency['negative_variation'],
            y=data_frequency['id'],
            name='Freq 5th pct',
            orientation='h',
            marker_color='crimson'
        ), row=1, col=2
    )
    fig.add_trace(
        go.Bar(
            x=data_frequency['positive_variation'],
            y=data_frequency['id'],
            name='Freq 95th pct',
            orientation='h',
            marker_color='steelblue'
        ), row=1, col=2
    )
    fig.update_layout(
        title="Tornado ALE Variation",
        barmode='overlay',
        height=600, width=1000,
    )
    return fig


def plot_total_variation(data_total: Dict[str, Any]) -> go.Figure:
    """
    Two‐panel Tornado chart for the total risk variation.
    """
    return plot_tornado(data_total, "total")
