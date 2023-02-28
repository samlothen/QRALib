"""A model based on the lognormal distribution define by a 90% confidence interval
"""
import math

from scipy.stats import norm
from scipy.stats import lognorm

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
        if low_bound >= up_bound:
            raise AssertionError("Upper bound must exceed lower bound")
        factor = -0.5 / norm.ppf(0.05)
        self.mu = (math.log(low_bound) + math.log(up_bound)) / 2.  
        self.sigma = factor * (math.log(up_bound) - math.log(low_bound))   
        self.distribution = lognorm(self.sigma, scale=math.exp(self.mu))


    def draw(self, n=1):
        """:param  n = Number of samples to return
        :return: array of size n with random values from distribtuion 
        :rtype: numpy.ndarray
        """
        return self.distribution.rvs(size=n)

    def draw_ppf(self, percentile_sequences):
        """:param  percentile_sequences = list of numbers in range [0,1]
        :return: array of same size as inpu with values from the distribtuions
        percent point function. 
        :rtype: numpy.ndarray
        """
        return self.distribution.ppf(percentile_sequences)

    def mean(self):
        """:return: mean value of the distribution
        :rtype: numpy.float64
        """
        return self.distribution.mean()