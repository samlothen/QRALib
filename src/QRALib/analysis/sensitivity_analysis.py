# src/QRALib/analysis/sensitivity.py
import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol, morris
from SALib.sample.morris import sample as morris_sample
from typing import List, Dict, Any, Tuple

class SensitivityAnalysis:
    """
    Compute Morris & Sobol sensitivity indices, but do not plot.
    """

    def __init__(self, risks: List):
        # build SALib problem and PPF functions
        self.names: List[str] = []
        self.equation: List = []
        for risk in risks:
            self.names += [risk.uniq_id + "_frequency", risk.uniq_id + "_impact"]
            self.equation += [risk.get_frequency_ppf, risk.get_impact_ppf]

        self.num_vars = len(self.names)
        self.problem = {
            "num_vars": self.num_vars,
            "names": self.names,
            "dists": ["unif"] * self.num_vars,
            "bounds": [[0, 0.9999]] * self.num_vars,
        }

    def morris_indices(self, N: int = 1000, num_levels: int = 4) -> Dict[str, Any]:
        """Return SALib Morris result dict (mu_star, sigma, etc)."""
        params = morris_sample(self.problem, N=N, num_levels=num_levels)
        # build model output Y
        Y = np.sum([
            self.equation[i](params[:, i]) * self.equation[i + 1](params[:, i + 1])
            for i in range(0, self.num_vars, 2)
        ], axis=0)
        Si = morris.analyze(
            self.problem, params, Y,
            print_to_console=False,
            num_levels=num_levels,
            num_resamples=100
        )
        Si["names"] = self.names
        return Si

    def sobol_indices(self, N: int = 1024) -> Dict[str, Any]:
        """Return SALib Sobol result dict (S1, ST, etc)."""
        params = saltelli.sample(self.problem, N, calc_second_order=False)
        Y = np.sum([
            self.equation[i](params[:, i]) * self.equation[i + 1](params[:, i + 1])
            for i in range(0, self.num_vars, 2)
        ], axis=0)
        Si = sobol.analyze(
            self.problem,
            Y,
            calc_second_order=False,
            print_to_console=False
        )
        Si["names"] = self.names
        return Si

    @staticmethod
    def sort_Si(Si: Dict[str, Any], key: str, by: str) -> np.ndarray:
        """
        Return the array Si[key] sorted by Si[by].
        """
        idx = np.argsort(Si[by])
        return np.array(Si[key])[idx]
