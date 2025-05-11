# src/QRALib/analysis/single_risk.py
"""
Data-only analysis for single-risk exploration (no plotting).
"""
import numpy as np
from typing import Dict, Any, Tuple

class SingleRiskAnalysis:
    """
    Compute statistics and exceedance data for one risk from simulation results.

    Parameters
    ----------
    sim_result : Dict[str, Any]
        Simulation result dict with keys:
          - "summary": {"number_of_iterations": int, ...}
          - "results": list of dicts with keys ["id","frequency","impact","single_risk_impact","total"]

    Attributes
    ----------
    num_iter : int
        Number of simulation iterations.
    """
    def __init__(self, sim_result: Dict[str, Any]) -> None:
        self.results = sim_result["results"]
        self.num_iter = sim_result["summary"]["number_of_iterations"]

    def compute_stats(self, risk_idx: int) -> Dict[str, Any]:
        """
        Compute summary statistics for a single risk.

        Returns
        -------
        Dict[str, Any]
            {
              "id": str,
              "frequency": np.ndarray,
              "impact": np.ndarray,
              "total": np.ndarray,
              "table": {
                  "min": [min_freq, min_imp],
                  "p5":  [..., ...],
                  "mean": [..., ...],
                  "p95": [..., ...],
                  "max":  [..., ...],
              }
            }
        """
        r = self.results[risk_idx]
        freq = np.asarray(r["frequency"])
        imp_ppf = np.asarray(r["single_risk_impact"])
        total = np.asarray(r["total"])

        stats = {
            "id": r["id"],
            "frequency": freq,
            "impact": imp_ppf,
            "total": total,
            "table": {
                "min":   [float(np.min(freq)), float(np.min(imp_ppf))],
                "p5":    [float(np.percentile(freq, 5)),  float(np.percentile(imp_ppf, 5))],
                "mean":  [float(np.mean(freq)),         float(np.mean(imp_ppf))],
                "p95":   [float(np.percentile(freq, 95)), float(np.percentile(imp_ppf, 95))],
                "max":   [float(np.max(freq)),         float(np.max(imp_ppf))],
            }
        }
        return stats

    def compute_exceedance(self, risk_idx: int, num_bins: int = 100) -> Dict[str, np.ndarray]:
        """
        Compute impact exceedance curve for a single risk.

        Returns
        -------
        Dict[str, np.ndarray]
            {"bins": np.ndarray, "exceedance": np.ndarray}
        """
        total = np.sort(self.results[risk_idx]["total"])
        max_val = np.percentile(total, 99)
        bins = np.linspace(0, max_val, num_bins)
        exceedance = np.array([np.mean(total >= b) for b in bins])
        return {"bins": bins, "exceedance": exceedance}
