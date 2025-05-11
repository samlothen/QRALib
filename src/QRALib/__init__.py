# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

# — version setup (unchanged) —
try:
    dist_name = 'QRALib'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = '0.0.1'
finally:
    del get_distribution, DistributionNotFound

# — public API exports —
from .utils.importer           import RiskDataImporter
from .risk.portfolio           import RiskPortfolio
from .simulation.smc           import StandardMonteCarlo
from .simulation.qmc           import QuasiMonteCarlo
from .simulation.rmc           import RandomQuasiMonteCarlo
from .analysis.mariq           import MaRiQAnalysis
from .analysis.sensitivity_analysis import SensitivityAnalysis
from .analysis.tornado         import TornadoAnalysis
from .analysis.single_risk_analysis import SingleRiskAnalysis
from .pipeline                 import QRAPipeline
from .api                      import run_full_qra

__all__ = [
    "RiskDataImporter",
    "RiskPortfolio",
    "StandardMonteCarlo",
    "QuasiMonteCarlo",
    "RandomQuasiMonteCarlo",
    "MaRiQAnalysis",
    "SensitivityAnalysis",
    "TornadoAnalysis",
    "SingleRiskAnalysis",
    "QRAPipeline",
    "run_full_qra",
]
