 # src/QRALib/viz/single_risk.py
 import plotly.graph_objects as go
 from plotly.subplots import make_subplots
 from typing import Dict, Any


 def plot_single_risk(stats: Dict[str, Any], exceedance: Dict[str, Any]) -> go.Figure:
     """
     Create a Plotly figure for single-risk analysis.

     Parameters
     ----------
     stats : dict
         Output of `SingleRiskAnalysis.compute_stats`
     exceedance : dict
         Output of `SingleRiskAnalysis.compute_exceedance`
     """
     # Unpack
     freq = stats["frequency"]
     imp_ppf = stats["impact"]
     tbl = stats["table"]
     bins = exceedance["bins"]
     exc = exceedance["exceedance"]
     risk_id = stats["id"]

     fig = make_subplots(
         rows=3, cols=2,
         specs=[[{"type":"scatter","rowspan":2},{"type":"box"}],
                [None,{"type":"box"}],
                [{"type":"table","colspan":2},None]],
         subplot_titles=("Impact Exceedance","Frequency","Impact","Statistics")
     )

     # Exceedance curve
     fig.add_trace(
         go.Scatter(x=bins, y=exc, name="Exceedance", mode="lines", marker_color="crimson"),
         row=1, col=1
     )

     # Frequency box
     fig.add_trace(
         go.Box(x=freq, name="Frequency", boxpoints=False, showlegend=False),
         row=1, col=2
     )

     # Impact box
     fig.add_trace(
         go.Box(x=imp_ppf, name="Impact", boxpoints=False, showlegend=False),
         row=2, col=2
     )

     # Statistics table
     headers = ["Attribute","Min","5%","Mean","95%","Max"]
     values = [ ["Frequency","Impact"], tbl["min"], tbl["p5"], tbl["mean"], tbl["p95"], tbl["max"] ]
     fig.add_trace(
         go.Table(header=dict(values=headers,align="left"), cells=dict(values=values,align="left")),
         row=3, col=1
     )

     fig.update_layout(title_text=f"Single Risk Analysis — {risk_id}", height=750, width=1000)
     return fig
