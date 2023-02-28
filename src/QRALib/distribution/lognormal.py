"""A model based on the lognormal distribution define by a 90% confidence interval
"""
import math
import numpy as np
from scipy.stats import norm, lognorm

class Lognormal:
    def __init__(self, low_bound: float, up_bound: float):
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
        self._parameters(low_bound, up_bound)
        
    def _parameters(self, low_bound, up_bound):
        """
        Calculate the parameters of the Lognormal distribution.

        :param low_bound: Lower bound estimate
        :type low_bound: float
        :param up_bound: Upper bound estimate
        :type up_bound: float
        """
        if low_bound >= up_bound:
            raise AssertionError("Upper bound must exceed lower bound")
        factor = -0.5 / norm.ppf(0.05)
        self.mu = (math.log(low_bound) + math.log(up_bound)) / 2.  
        self.sigma = factor * (math.log(up_bound) - math.log(low_bound))   
        self.distribution = lognorm(self.sigma, scale=math.exp(self.mu))


    def draw(self, n: int = 1) -> np.ndarray:
        """
        Generate random samples from the Lognormal distribution.

        :param n: Number of samples to return
        :type n: int
        :return: Array of size n with random values from distribution
        :rtype: numpy.ndarray
        """
        return self.distribution.rvs(size=n)

    def draw_ppf(self, percentile_sequences) -> np.ndarray:
        """
        Generate samples from the Lognormal distribution using the percent point function (PPF).

        :param percentile_sequences: List of numbers in the range [0, 1]
        :type percentile_sequences: list
        :return: Array of the same size as the input with values from the distribution PPF
        :rtype: numpy.ndarray
        """
        return self.distribution.ppf(percentile_sequences)

    def mean(self) -> np.float64:
        """
        Calculate the mean value of the Lognormal distribution.

        :return: Mean value of the distribution
        :rtype: numpy.float64
        """
        return self.distribution.mean()