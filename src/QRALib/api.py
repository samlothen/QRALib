# src/QRALib/api.py
# ---------------
from .pipeline import QRAPipeline
from dataclasses import dataclass
from typing import Dict, Any, Type, TypeVar, Optional
import numpy as np
from typing import List, Literal
from .risk.portfolio    import RiskPortfolio, Risk
from .simulation.smc    import StandardMonteCarlo
from .simulation.qmc    import QuasiMonteCarlo
from .simulation.rmc    import RandomQuasiMonteCarlo
#from .api               import SimulationResults

Method = Literal["smc", "qmc", "rmc"]

T = TypeVar("T", bound="SimulationResults")

@dataclass
class SimulationResults:
    summary: Dict[str, Any]
    results: Dict[str, Any]

    def to_json(self) -> Dict[str, Any]:
        """
        Convert this SimulationResults into a JSON-serializable dict.
        Walks through nested dicts/lists, converting any np.ndarray via .tolist().
        """
        def _serialize(obj):
            # base case: NumPy array → list
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            # dict → serialize each key/value
            if isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            # list or tuple → serialize each element
            if isinstance(obj, (list, tuple)):
                return [_serialize(v) for v in obj]
            # everything else (int, float, str, None) is safe as-is
            return obj

        return {
            "summary": _serialize(self.summary),
            "results": _serialize(self.results),
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "SimulationResults":
        def _rebuild(obj):
            if isinstance(obj, dict):
                return {k: _rebuild(v) for k, v in obj.items()}
            if isinstance(obj, list):
                # try array, otherwise list of mixed types
                try:
                    return np.array(obj)
                except:
                    return [_rebuild(v) for v in obj]
            return obj

        summary = _rebuild(data["summary"])
        results = _rebuild(data["results"])
        return cls(summary=summary, results=results)





def simulate(
    risks: List[Risk],
    method: Method = "smc",
    iterations: int = 10000
) -> SimulationResults:
    """
    Run a Monte Carlo (or QMC / RMC) simulation on a list of Risk objects.

    Parameters
    ----------
    risks
        A pre-built list of `Risk` instances (e.g. from RiskDataImporter.import_risks()).
    method
        Which algorithm to use: `"smc"`, `"qmc"` (Quasi Monte Carlo), or `"rmc"` (Randomized Quasi Monte Carlo).
    iterations
        Number of simulation years (draws) to perform.

    Returns
    -------
    SimulationResults
        A dataclass containing:
          - `summary`: metadata (method, iteration count, risk IDs)
          - `results`: a dict mapping risk_id → per-risk output arrays
    """
    # 1) Wrap your raw list in a Portfolio so existing sim code can consume it
    portfolio = RiskPortfolio(risks)

    # 2) Pick the simulation class
    sim_map = {
        "smc" : StandardMonteCarlo,
        "qmc" : QuasiMonteCarlo,
        "rmc": RandomQuasiMonteCarlo,
    }
    try:
        SimClass = sim_map[method]
    except KeyError:
        raise ValueError(f"Unknown method {method!r}, choose from {list(sim_map)}")

    # 3) Run the simulation
    sim = SimClass(portfolio)
    raw = sim.simulation(iterations)
    # raw is a dict with keys "summary" and "results" (list of per-risk dicts)

    # 4) Build a clean summary dict of primitives
    summary = {
        "method": method,
        "number_of_iterations": raw["summary"]["number_of_iterations"],
        "risk_ids": portfolio.ids(),
    }

    # 5) Turn the list-of-dicts into a dict keyed by risk_id
    results_by_id = {
        entry["id"]: {
            k: v for k, v in entry.items() if k != "id"
        }
        for entry in raw["results"]
    }

    # 6) Return your typed container
    return SimulationResults(summary=summary, results=results_by_id)


def run_full_qra(
    source: str,
    method: Method = "smc",
    iterations: int = 10000,
    tolerance: Optional[Any] = None,
    morris: int = 1000,
    sobol: int = 1024,
    single_risk_idx: Optional[int] = None,
) -> SimulationResults:
    # Import risks via pipeline's importer
    from .utils.importer import RiskDataImporter
    raw_dict = RiskDataImporter.import_risks(source)
    risks = [Risk(**r) for r in raw_dict]  # or however you reconstruct Risk

    # 1) simulate (using your new function)
    sim_res = simulate(risks, method=method, iterations=iterations)

    # 2) run analyses *in place* on the pipeline if you need side-effects*, or
    #    call your pure-analysis functions here:
    if tolerance is not None:
        from .analysis.mariq import MaRiQAnalysis
        mariq_data = MaRiQAnalysis(sim_res, tolerance).compute_total()
        sim_res.summary["mariq"] = mariq_data

    from .analysis.sensitivity import SensitivityAnalysis
    si = SensitivityAnalysis(risks)
    sim_res.summary["sobol"] = si.sobol_indices(sobol)
    sim_res.summary["morris"] = si.morris_indices(morris)

    from .analysis.tornado import TornadoAnalysis
    ta = TornadoAnalysis({"results": [
        {"id": rid, **sim_res.results[rid]} for rid in sim_res.summary["risk_ids"]
    ]})
    sim_res.summary["tornado_total"] = ta.compute_variation("total")

    if single_risk_idx is not None:
        from .analysis.single_risk import SingleRiskAnalysis
        sra = SingleRiskAnalysis({"results": [
            {"id": rid, **sim_res.results[rid]} for rid in sim_res.summary["risk_ids"]
        ]})
        sim_res.summary["single"] = {
            "stats": sra.compute_stats(single_risk_idx),
            "exceedance": sra.compute_exceedance(single_risk_idx)
        }

    return sim_res
