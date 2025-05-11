# src/QRALib/analysis/tornado.py
"""
Data-only analysis for Tornado sensitivity charts (no plotting).
"""
import numpy as np
from typing import Dict, Any, List, Tuple

class TornadoAnalysis:
    """
    Compute Tornado variations for risks based on simulation results.

    Parameters
    ----------
    sim_result : Dict[str, Any]
        Simulation result dict with keys "results": list of dicts having ["id","frequency","single_risk_impact","total"].
    """
    def __init__(self, sim_result: Dict[str, Any]) -> None:
        self.results = sim_result["results"]
        self.risk_ids = [r["id"] for r in self.results]

    def compute_variation(
        self,
        attribute: str
    ) -> Dict[str, np.ndarray]:
        """
        Compute positive and negative variations for Tornado chart.

        Parameters
        ----------
        attribute : str
            One of 'single_risk_impact', 'frequency', or 'total'.

        Returns
        -------
        Dict[str, np.ndarray]
            {
              'id': sorted ids by absolute difference,
              'negative_variation': sorted negative variation arrays,
              'positive_variation': sorted positive variation arrays
            }
        """
        assert attribute in ['single_risk_impact', 'frequency', 'total']
        # Gather stats: mean, 5th, 95th percentiles
        mean_vals = []
        p5_vals = []
        p95_vals = []
        for r in self.results:
            arr = np.asarray(r[attribute])
            mean_vals.append(np.mean(arr))
            p5_vals.append(np.percentile(arr, 5))
            p95_vals.append(np.percentile(arr, 95))
        mean_sum = sum(mean_vals)

        neg_var = []
        pos_var = []
        # compute one-at-a-time OAT variations
        for i in range(len(mean_vals)):
            # negative: replace mean[i] by p5_vals[i]
            neg = (sum(mean_vals[:i]) + p5_vals[i] + sum(mean_vals[i+1:])) - mean_sum
            # positive: replace mean[i] by p95_vals[i]
            pos = (sum(mean_vals[:i]) + p95_vals[i] + sum(mean_vals[i+1:])) - mean_sum
            neg_var.append(min(neg, 0))
            pos_var.append(max(pos, 0))

        # sort by absolute variation
        abs_diff = [abs(p - n) for p, n in zip(pos_var, neg_var)]
        idx = np.argsort(abs_diff)

        return {
            'id': np.array(self.risk_ids)[idx],
            'negative_variation': np.array(neg_var)[idx],
            'positive_variation': np.array(pos_var)[idx]
        }
