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
        def _convert(v):
            return v.tolist() if isinstance(v, np.ndarray) else v
        summary_json = {k: _convert(v) for k, v in self.summary.items()}
        results_json = {
            rid: {field: _convert(arr) for field, arr in data.items()}
            for rid, data in self.results.items()
        }
        return {"summary": summary_json, "results": results_json}

    @classmethod
    def from_json(cls: Type[T], data: Dict[str, Any]) -> T:
        def _rebuild(v):
            return np.array(v) if isinstance(v, list) else v
        summary = {k: _rebuild(v) for k, v in data["summary"].items()}
        results = {
            rid: {f: _rebuild(arr) for f, arr in rd.items()}
            for rid, rd in data["results"].items()
        }
        return cls(summary=summary, results=results)


def simulate(source: str, method: str, iterations: int) -> SimulationResults:
    pipe = QRAPipeline(source, method, iterations)
    raw = pipe.run_simulation()      # raw["results"] is a list of dicts
    # Turn list-of-dicts into dict[risk_id → data-dict]
    results_by_id = {
        r["id"]: {k: v for k, v in r.items() if k != "id"}
        for r in raw["results"]
    }
    return SimulationResults(summary=raw["summary"], results=results_by_id)


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
