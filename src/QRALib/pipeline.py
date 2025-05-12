# src/QRALib/pipeline.py
# ----------------------
import os

from .utils.importer import RiskDataImporter
from .risk import RiskPortfolio
from .simulation.smc import StandardMonteCarlo
from .simulation.qmc import QuasiMonteCarlo
from .simulation.rmc import RandomQuasiMonteCarlo
from .analysis.mariq import MaRiQAnalysis
from .analysis.sensitivity_analysis import SensitivityAnalysis
from .analysis.tornado import TornadoAnalysis
from .analysis.single_risk_analysis import SingleRiskAnalysis


class QRAPipeline:
    """
    Pipeline for Quantitative Risk Analysis:
      - import data
      - run simulation (SMC, QMC, RQMC)
      - perform analyses (MaRiQ, sensitivity, tornado, single risk)
    """
    SIMULATORS = {
        "smc": StandardMonteCarlo,
        "qmc": QuasiMonteCarlo,
        "rqmc": RandomQuasiMonteCarlo,
    }

    def __init__(self, source: str, method: str = "smc", iterations: int = 10000):
        self.source = source
        self.method = method
        self.iterations = iterations
        self.portfolio = RiskPortfolio(RiskDataImporter.import_risks(source))
        self.results = None

    def run_simulation(self):
        sim_cls = self.SIMULATORS.get(self.method)
        if not sim_cls:
            raise ValueError(f"Unknown method '{self.method}'. Choose from {list(self.SIMULATORS)}")
        simulator = sim_cls(self.portfolio)
        self.results = simulator.simulation(self.iterations)
        return self.results

    def analyze_mariq(self, tolerance):
        if self.results is None:
            raise RuntimeError("Simulation must be run before analysis.")
        analysis = MaRiQAnalysis(self.results, tolerance)
        return {
            "total": analysis.compute_total(),
            "single": analysis.compute_single()
        }

    def analyze_sensitivity(self, morris_samples: int = 1000, sobol_n: int = 1024):
        sa = SensitivityAnalysis(self.portfolio)
        morris = sa.morris_indices(N=morris_samples)
        sobol = sa.sobol_indices(N=sobol_n)
        return {"morris": morris, "sobol": sobol}

    def analyze_tornado(self, attribute: str = "total"):
        if self.results is None:
            raise RuntimeError("Simulation must be run before analysis.")
        ta = TornadoAnalysis(self.results)
        return ta.compute_variation(attribute)

    def analyze_single_risk(self, risk_index: int):
        if self.results is None:
            raise RuntimeError("Simulation must be run before analysis.")
        sra = SingleRiskAnalysis(self.results)
        stats = sra.compute_stats(risk_index)
        exceedance = sra.compute_exceedance(risk_index)
        return {"stats": stats, "exceedance": exceedance}
