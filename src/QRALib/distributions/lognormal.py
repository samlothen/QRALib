"""A model based on the lognormal distribution define by a 90% confidence interval
"""
import math
import numpy as np
from scipy.stats import norm, lognorm
from typing import Optional

class Lognormal:
    def __init__(self, low_bound: float, up_bound: float) -> None:
        """
        :param low_bound: Lower bound estimate
        :type low_bound: float
        :param up_bound: Upper bound estimate
        :type up_bound: float
    
        The range low_bound -> up_bound should represent the 90% confidence interval
        that the loss will fall in that range.
    
        These values are then fit to a lognormal distribution so that they fall at the 5% and
        95% cumulative probability points.
        """
        if not isinstance(low_bound, float):
            raise TypeError("low_bound must be a float")
        if not isinstance(up_bound, float):
            raise TypeError("up_bound must be a float")
        if low_bound >= up_bound:
            raise ValueError("up_bound must exceed low_bound")
        self.low_bound = low_bound
        self.up_bound = up_bound
        self._parameters()
        
    def _parameters(self) -> None:
        """
        Calculate the parameters of the Lognormal distribution.

        :param low_bound: Lower bound estimate
        :type low_bound: float
        :param up_bound: Upper bound estimate
        :type up_bound: float
        """

        factor = -0.5 / norm.ppf(0.05)
        self.mu = (math.log(self.low_bound) + math.log(self.up_bound)) / 2.  
        self.sigma = factor * (math.log(self.up_bound) - math.log(self.low_bound))   
        self.distribution = lognorm(self.sigma, scale=math.exp(self.mu))


    def draw(self, n: int = 1) -> np.ndarray:
        """
        Generate random samples from the Lognormal distribution.

        :param n: Number of samples to return
        :type n: int
        :return: Array of size n with random values from distribution
        :rtype: numpy.ndarray
        """

        return lognorm.rvs(self.sigma, scale=np.exp(self.mu), size=n)

    def draw_ppf(self, percentile_sequences: np.ndarray) -> np.ndarray:
        """
        Generate samples from the Lognormal distribution using the percent point function (PPF).

        :param percentile_sequences: Array of numbers in the range [0, 1)
        :type percentile_sequences: numpy.ndarray
        :return: Array of the same size as the input with values from the distribution PPF
        :rtype: numpy.ndarray
        """
        if not isinstance(percentile_sequences, np.ndarray) or not np.issubdtype(percentile_sequences.dtype, np.number) or not (0 <= percentile_sequences).all() or not (percentile_sequences < 1).all():
            raise ValueError("percentile_sequences must be a numpy array of numbers in the range [0, 1)")
        return self.distribution.ppf(percentile_sequences)

    def mean(self, round_to: Optional[int] = None) -> np.float64:
        """
        Calculate the mean value of the Lognormal distribution.

        :param round_to: Number of decimal places to round the mean value to
        :type round_to: int or None
        :return: Mean value of the distribution
        :rtype: numpy.float64
        """
        mean = self.distribution.mean()
        if round_to is not None:
            mean = round(mean, round_to)
        return mean