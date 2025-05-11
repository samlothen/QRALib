# src/QRALib/api.py
# ---------------
from .pipeline import QRAPipeline
from dataclasses import dataclass
from typing import Dict, Any, Type, TypeVar, Optional
import numpy as np

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



def simulate(source: str, method: str, iterations: int) -> SimulationResults:
    pipe = QRAPipeline(source, method, iterations)
    raw = pipe.run_simulation()  # raw["summary"]["risk_list"] is a RiskPortfolio

    # build a clean summary
    summary = {
        "number_of_iterations": raw["summary"]["number_of_iterations"],
        "risk_ids": raw["summary"]["risk_list"].ids(),   # just the list of IDs
        "method": method,
        # any other metadata you want...
    }

    # convert results list→dict by ID (as we discussed earlier)
    results_by_id = { r["id"]: {k:v for k,v in r.items() if k!="id"}
                      for r in raw["results"] }

    return SimulationResults(summary=summary, results=results_by_id)


def run_full_qra(
    source: str,
    method: str = "smc",
    iterations: int = 10000,
    tolerance: Optional[Any] = None,
    morris: int = 1000,
    sobol: int = 1024,
    single_risk_idx: Optional[int] = None,
) -> SimulationResults:
    """
    Full pipeline: import, simulate, analyze (MaRiQ, sensitivity, tornado, single-risk).
    Returns a SimulationResults object.
    """
    pipe = QRAPipeline(source, method, iterations)
    raw = pipe.run_simulation()

    if tolerance is not None:
        pipe.analyze_mariq(tolerance)
    pipe.analyze_sensitivity(morris, sobol)
    pipe.analyze_tornado()
    if single_risk_idx is not None:
        pipe.analyze_single_risk(single_risk_idx)

    # Wrap the final raw results dict
    final = pipe.results
    return SimulationResults(summary=final["summary"], results=final["results"])
