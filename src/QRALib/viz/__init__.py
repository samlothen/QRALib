# src/QRALib/viz/__init__.py

from .mariq         import plot_total_risk, plot_single_risk        # MaRiQ charts
from .sensitivity   import plot_morris, plot_sobol                  # Sensitivity tables
from .single_risk   import plot_single_risk as plot_risk_details    # Single‐risk chart
from .tornado       import (
    plot_tornado,
    plot_ale_variation,
    plot_total_variation
)                                                                    # Tornado charts

__all__ = [
    # MaRiQ
    "plot_total_risk",
    "plot_single_risk",
    # Sensitivity
    "plot_morris",
    "plot_sobol",
    # Single risk
    "plot_risk_details",
    # Tornado
    "plot_tornado",
    "plot_ale_variation",
    "plot_total_variation",
]
