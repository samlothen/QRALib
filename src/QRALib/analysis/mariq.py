# src/QRALib/analysis/mariq.py
"""
Analysis module for MaRiQ quantitative risk analysis (data-only, no visualization).
"""
import numpy as np
from typing import Dict, Any, List, Tuple

class MaRiQAnalysis:
    """
    Perform MaRiQ analysis on simulation results.

    Parameters
    ----------
    sim_result : Dict[str, Any]
        A simulation result structure with keys:
        - "summary": {"number_of_iterations": int, "risk_list": ...}
        - "results": list of dicts with keys ["id","frequency","impact","single_risk_impact","total"]
    tolerance : Tuple[List[float], List[float]]
        User-defined risk tolerance as (x_values, y_percentages).
    """
    def __init__(
        self,
        sim_result: Dict[str, Any],
        tolerance: Tuple[List[float], List[float]]
    ):
        self.sim = sim_result
        self.tolerance = tolerance
        self.num_iter = self.sim["summary"]["number_of_iterations"]
        results = self.sim["results"]

        # Extract risk IDs
        self.risk_ids: List[str] = [r["id"] for r in results]

        # Build matrix of total outcomes: shape (n_risks, num_iter)
        self._risk_matrix = np.vstack([r["total"] for r in results])
        # Total risk across all risks per iteration
        self.total_risk: np.ndarray = self._risk_matrix.sum(axis=0)

        # Prepare per-risk lists
        freq_list = [r["frequency"] for r in results]
        imp_list = [r["impact"] for r in results]
        sri_list = [r["single_risk_impact"] for r in results]

        # Compute means
        self.mean_frequency = np.array([np.mean(f) for f in freq_list])
        self.mean_impact    = np.array([np.mean(i) for i in imp_list])
        self.mean_expected_loss = np.array([
            np.mean(np.asarray(f) * np.asarray(sri))
            for f, sri in zip(freq_list, sri_list)
        ])

        # Uncertainty matrix for each risk (single risk impacts)
        self.uncertainty = np.vstack(sri_list)

        # Normalize tolerance y-values (percentages to fraction)
        tol_x, tol_y = tolerance
        self.tol_x = np.asarray(tol_x)
        self.tol_y = np.asarray(tol_y) / 100.0

    def compute_total(self, num_buckets: int = 200) -> Dict[str, np.ndarray]:
        """
        Compute the impact exceedance (total-risk) curve.

        Parameters
        ----------
        num_buckets : int
            Number of impact bins for the exceedance curve.

        Returns
        -------
        Dict[str, np.ndarray]
            {
              "buckets": impact bin edges,
              "exceedance": exceedance probabilities,
              "tol_x": tolerance x-values,
              "tol_y": tolerance y-fractions
            }
        """
        # Sort total risk outcomes
        sorted_total = np.sort(self.total_risk)
        # Use 99th percentile as maximum
        max_outcome = np.percentile(sorted_total, 99)
        buckets = np.linspace(0, max_outcome, num_buckets)
        # Probability of exceeding each bucket
        exceedance = np.array([np.mean(sorted_total >= b) for b in buckets])
        return {
            "buckets": buckets,
            "exceedance": exceedance,
            "tol_x": self.tol_x,
            "tol_y": self.tol_y,
        }

    def compute_single(self, top_n: int = 10) -> Dict[str, Any]:
        """
        Compute single-risk analysis data.

        Parameters
        ----------
        top_n : int
            Number of top risks by expected loss to include.

        Returns
        -------
        Dict[str, Any]
            {
              "risk_ids": list of all risk IDs,
              "mean_frequency": array of mean frequencies,
              "mean_impact": array of mean impacts,
              "mean_expected_loss": array of mean expected losses,
              "top_ids": list of top_n risk IDs sorted by loss,
              "top_losses": array of their mean losses,
              "heatmap_x": array of mean frequencies for top risks,
              "heatmap_y": array of mean impacts for top risks,
              "uncertainty": matrix (top_n x num_iter) of single-risk impacts,
              "top_n": top_n
            }
        """
        # Sort by expected loss ascending, then reverse for descending
        idx_sorted = np.argsort(self.mean_expected_loss)
        top_idx = idx_sorted[::-1][:top_n]

        return {
            "risk_ids": self.risk_ids,
            "mean_frequency": self.mean_frequency,
            "mean_impact": self.mean_impact,
            "mean_expected_loss": self.mean_expected_loss,
            "top_ids": [self.risk_ids[i] for i in top_idx],
            "top_losses": self.mean_expected_loss[top_idx],
            "heatmap_x": self.mean_frequency[top_idx],
            "heatmap_y": self.mean_impact[top_idx],
            "uncertainty": self.uncertainty[top_idx],
            "top_n": top_n,
        }
