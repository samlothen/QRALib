# QRALib/api.py
# ---------------
from .pipeline import QRAPipeline

def run_full_qra(
    source: str,
    method: str = "smc",
    iterations: int = 10000,
    tolerance=None,
    morris: int = 1000,
    sobol: int = 1024,
    single_risk_idx: int = 0,
):
    """
    Run the full QRA pipeline: import, simulate, analyze, and optionally single-risk.

    Returns the raw simulation results dict.
    """
    pipe = QRAPipeline(source, method, iterations)
    pipe.run_simulation()
    if tolerance is not None:
        pipe.analyze_mariq(tolerance)
    pipe.analyze_sensitivity(morris, sobol)
    pipe.analyze_tornado()
    if single_risk_idx is not None:
        pipe.analyze_single_risk(single_risk_idx)
    return pipe.results
