import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any

def plot_total_risk(data: Dict[str, Any]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["buckets"], y=data["exceedance"], name="Total Risk"))
    fig.add_trace(go.Scatter(x=data["tol_x"],   y=data["tol_y"],       name="Tolerance"))
    fig.update_layout(
        title="Impact Exceedance Curve",
        xaxis_title="Impact",
        yaxis_title="Probability",
        yaxis_tickformat=".2%"
    )
    return fig

def plot_single_risk(data: Dict[str, Any]) -> go.Figure:
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type":"scatter"},{"type":"box"}],
               [{"type":"table"},  {"type":"table"}]],
        subplot_titles=("Heatmap","Uncertainty","Top 10 Risks","Estimated Risks")
    )
    # Uncertainty boxplots
    for idx, arr in enumerate(data["uncertainty"][: data["top_n"]]):
        fig.add_trace(go.Box(y=arr, name=data["top_ids"][idx]), row=1, col=2)

    # Heatmap scatter
    fig.add_trace(go.Scatter(
        x=data["heatmap_x"][: data["top_n"]],
        y=data["heatmap_y"][: data["top_n"]],
        text=data["top_ids"][: data["top_n"]],
        mode="markers"
    ), row=1, col=1)

    # Top 10 Risks table
    fig.add_trace(go.Table(
        header=dict(values=["Risk ID","Expected Loss"]),
        cells=dict(values=[data["top_ids"], data["top_losses"]])
    ), row=2, col=1)

    # Estimated Risks table (all)
    fig.add_trace(go.Table(
        header=dict(values=["Risk ID","Expected Loss"]),
        cells=dict(values=[data["risk_ids"], data["mean_expected_loss"]])
    ), row=2, col=2)

    fig.update_layout(title="MaRiQ Results — Single Risk")
    return fig
