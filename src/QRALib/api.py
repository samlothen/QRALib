# src/QRALib/api.py
from .pipeline import QRAPipeline
from dataclasses import dataclass
from typing import Dict, Any, Type, TypeVar, Optional, List, Literal, Tuple
import numpy as np

from .risk.portfolio    import RiskPortfolio, Risk
from .simulation.smc    import StandardMonteCarlo
from .simulation.qmc    import QuasiMonteCarlo
from .simulation.rmc    import RandomQuasiMonteCarlo
from .analysis.mariq    import MaRiQAnalysis
from .analysis.sensitivity_analysis import SensitivityAnalysis
from .analysis.single_risk_analysis import SingleRiskAnalysis
from .analysis.tornado    import TornadoAnalysis


Method = Literal["smc", "qmc", "rqmc"]
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



def analyze_mariq(
    sim: SimulationResults,
    tolerance: Tuple[List[float], List[float]]
) -> Dict[str, Any]:
    """
    Run MaRiQ analysis on a SimulationResults object.

    Parameters
    ----------
    sim : SimulationResults
        The result of simulate(...).
    tolerance : Tuple[List[float], List[float]]
        User‐specified risk tolerance (x_values, y_percentages).

    Returns
    -------
    Dict[str, Any]
        {
          "total": <output of compute_total()>,
          "single": <output of compute_single()>
        }
    """
    # 1) Rebuild the raw dict shape for MaRiQAnalysis
    raw = {
        "summary": {
            "number_of_iterations": sim.summary["number_of_iterations"],
            # we no longer pass a RiskPortfolio here
        },
        "results": [
            {"id": rid, **{k: v for k, v in data.items()}}
            for rid, data in sim.results.items()
        ]
    }

    # 2) Delegate to the pure‐data MaRiQAnalysis
    ma = MaRiQAnalysis(raw, tolerance)

    # 3) Return both total‐risk and single‐risk data
    return {
        "total": ma.compute_total(),
        "single": ma.compute_single()
    }

def compute_morris(
    risks: List[Risk],
    N: int = 1000,
    num_levels: int = 4
) -> Dict[str, Any]:
    """
    Compute Morris sensitivity indices for a list of Risk objects.

    Parameters
    ----------
    risks : List[Risk]
        The original Risk instances used in simulate().
    N : int
        Number of trajectories / samples (default 1000).
    num_levels : int
        Number of grid levels for Morris (default 4).

    Returns
    -------
    Dict[str, Any]
        SALib result dict containing keys 'names','mu_star','mu_star_conf','sigma'.
    """
    sa = SensitivityAnalysis(risks)
    return sa.morris_indices(N=N, num_levels=num_levels)


def compute_sobol(
    risks: List[Risk],
    N: int = 1024
) -> Dict[str, Any]:
    """
    Compute Sobol sensitivity indices for a list of Risk objects.

    Parameters
    ----------
    risks : List[Risk]
        The original Risk instances used in simulate().
    N : int
        Number of base samples (must be a power of 2, default 1024).

    Returns
    -------
    Dict[str, Any]
        SALib result dict containing keys 'names','S1','S1_conf','ST','ST_conf'.
    """
    sa = SensitivityAnalysis(risks)
    return sa.sobol_indices(N=N)


def compute_single_risk(
    sim: SimulationResults,
    risk_id: str,
    num_bins: int = 100
) -> Dict[str, Any]:
    """
    Compute summary stats and exceedance for a single risk.

    Parameters
    ----------
    sim : SimulationResults
        The object returned by `simulate()`.
    risk_id : str
        The ID of the risk to analyze.
    num_bins : int, optional
        Number of bins for the exceedance curve (default 100).

    Returns
    -------
    Dict[str, Any]
        {
          "stats":    output of SingleRiskAnalysis.compute_stats,
          "exceedance": output of SingleRiskAnalysis.compute_exceedance
        }
    """
    # 1) Rebuild the raw dict shape SingleRiskAnalysis expects
    raw = {
        "summary": {
            "number_of_iterations": sim.summary["number_of_iterations"]
        },
        "results": [
            {"id": rid, **data}
            for rid, data in sim.results.items()
        ]
    }

    # 2) Instantiate & find the index for our risk_id
    sra = SingleRiskAnalysis(raw)
    # build a map from id → index
    id_list = [r["id"] for r in raw["results"]]
    try:
        idx = id_list.index(risk_id)
    except ValueError:
        raise KeyError(f"Risk ID {risk_id!r} not found in SimulationResults")

    # 3) Compute stats & exceedance
    stats      = sra.compute_stats(idx)
    exceedance = sra.compute_exceedance(idx, num_bins=num_bins)

    return {"stats": stats, "exceedance": exceedance}


def compute_tornado(
    sim: SimulationResults,
    attribute: str
    ) -> Dict[str, Any]:
    """
    Compute Tornado variation for a given attribute ('single_risk_impact', 'frequency', 'total').
    """
    raw = {"results": [{"id": rid, **data} for rid, data in sim.results.items()]}
    ta = TornadoAnalysis(raw)
    return ta.compute_variation(attribute)
