# QRALib/pipeline.py
# -----------------
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

SIMULATORS = {
    "smc": StandardMonteCarlo,
    "qmc": QuasiMonteCarlo,
    "rqmc": RandomQuasiMonteCarlo,
}

class QRAPipeline:
    def __init__(self, source: str, method: str = "smc", iterations: int = 10000):
        self.source = source
        self.method = method
        self.iterations = iterations

        risks = RiskDataImporter.import_risks(source)
        self.portfolio = RiskPortfolio(risks)
        self.results = None

    def run_simulation(self):
        sim_cls = SIMULATORS.get(self.method)
        if not sim_cls:
            raise ValueError(f"Unknown method '{self.method}'. Choose from {list(SIMULATORS)}")
        sim = sim_cls(self.portfolio)
        self.results = sim.simulation(self.iterations)
        return self.results

    def analyze_mariq(self, tolerance):
        if self.results is None:
            raise RuntimeError("Simulation must be run before analysis.")
        analysis = MaRiQ(self.results, tolerance)
        analysis.total_risk_analysis()
        analysis.single_risk_analysis()

    def analyze_sensitivity(self, morris_samples: int = 1000, sobol_n: int = 1024):
        sa = SensitivityAnalysis(self.portfolio)
        sa.morris(morris_samples)
        sa.sobol(sobol_n)

    def analyze_tornado(self):
        if self.results is None:
            raise RuntimeError("Simulation must be run before analysis.")
        ta = Tornado(self.results)
        ta.draw_total()
        ta.draw_ale()

    def analyze_single_risk(self, risk_index: int):
        if self.results is None:
            raise RuntimeError("Simulation must be run before analysis.")
        sra = SingleRiskAnalysis(self.results)
        sra.single_risk_analysis(risk_index)
